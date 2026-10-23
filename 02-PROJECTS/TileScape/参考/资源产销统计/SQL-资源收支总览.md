---
title: 资源收支总览 SQL
date: 2026-10-23
type: reference
status: needs-review
project: TileScape
source: 当前 TileScape report_item 代码、打点工作簿与用户确认口径
verification: 静态编写，尚未在当前 TA 环境执行；运行前须复核字段、时间参数和事件覆盖。
tags: [TileScape, ThinkingData, TA, SQL, 资源产销, 净产出]
---

# 资源收支总览 SQL

> [!warning] 验证状态
> 本 SQL 尚未在当前 TA 环境执行。当前统计排除体力相关 `power`、`main`，并只纳入物品 ID `1, 6, 7, 8, 11, 12, 13, 14`。

```sql
/*
资源区间收支总览。
仅统计物品 ID：1、6、7、8、11、12、13、14。
净产出只在“所选时间区间 × 物品”粒度计算，不按 change_method 计算。
数据源：TileScape 历史已核对事件表 ta.v_event_54。
时间参数沿用 TA SQL IDE：${PartDate:date1}、${timezone}、${Time:time1}。
查询结果直接汇总所选时间区间，不固定按天拆分；TA 日期控件默认选择最近 7 天。
人均口径：所选时间区间内触发 ta_app_start 的去重用户数。
结果字段说明：
- 总产出数量：排除 power、main、GM、Trade、ignore 等非本次统计口径。
- 总消耗数量：同样排除 power、main、GM、Trade、ignore；本期不统计体力购买相关流水。
- 净产出数量：总产出数量 - 总消耗数量；正数为净流入，负数为净流出。
- 资源变动人数：区间内发生过正式产出或消耗的去重用户数，用于计算变动用户人均净产出。
- 期末库存：区间内每名用户最后一次有效上报的 remain 之和，仅覆盖区间内发生过变化的用户。
- 库存用户数：参与期末库存汇总的用户数；与活跃用户数不是同一口径。
*/

WITH active_users AS (
    SELECT COUNT(DISTINCT e."#user_id") AS active_user_count
    FROM ta.v_event_54 e
    WHERE ${PartDate:date1}
      AND DATE_ADD(
          'minute',
          CAST((CAST('${timezone}' AS INTEGER) - IF(e."#zone_offset" IS NULL, 0, e."#zone_offset")) * 60 AS INTEGER),
          e."#event_time"
      ) ${Time:time1}
      AND e."#event_name" = 'ta_app_start'
      AND e.is_test = false
      AND e."#user_id" IS NOT NULL
),

valid_events AS (
    SELECT
        DATE_ADD(
            'minute',
            CAST((CAST('${timezone}' AS INTEGER) - IF(e."#zone_offset" IS NULL, 0, e."#zone_offset")) * 60 AS INTEGER),
            e."#event_time"
        ) AS local_event_time,
        e."#user_id" AS user_id,
        TRY_CAST(e.change_type AS INTEGER) AS change_type,
        TRY_CAST(e.report_item_type AS INTEGER) AS report_item_type,
        TRY_CAST(e.report_item_id AS INTEGER) AS report_item_id,
        TRY_CAST(e.change_num AS BIGINT) AS change_num,
        TRY_CAST(e.remain AS BIGINT) AS remain,
        COALESCE(CAST(e.change_method AS VARCHAR), '') AS change_method
    FROM ta.v_event_54 e
    WHERE ${PartDate:date1}
      AND DATE_ADD(
          'minute',
          CAST((CAST('${timezone}' AS INTEGER) - IF(e."#zone_offset" IS NULL, 0, e."#zone_offset")) * 60 AS INTEGER),
          e."#event_time"
      ) ${Time:time1}
      AND e."#event_name" = 'report_item'
      AND e.is_test = false
      AND TRY_CAST(e.change_type AS INTEGER) IN (1, -1)
      AND TRY_CAST(e.change_num AS BIGINT) > 0
      AND TRY_CAST(e.report_item_id AS INTEGER) IN (1, 6, 7, 8, 11, 12, 13, 14)
      AND e."#user_id" IS NOT NULL
),

formal_flow AS (
    SELECT *
    FROM valid_events
    WHERE change_method <> ''
      AND change_method NOT IN ('power', 'main', 'GM', 'Trade', 'ignore')
),

flow_period AS (
    SELECT
        report_item_type,
        report_item_id,
        SUM(CASE WHEN change_type = 1 THEN change_num ELSE 0 END) AS total_output,
        SUM(CASE WHEN change_type = -1 THEN change_num ELSE 0 END) AS total_consumption,
        SUM(
            CASE
                WHEN change_type = 1 THEN change_num
                WHEN change_type = -1 THEN -change_num
                ELSE 0
            END
        ) AS net_output,
        COUNT(DISTINCT user_id) AS flow_users
    FROM formal_flow
    GROUP BY report_item_type, report_item_id
),

stock_ranked AS (
    SELECT
        user_id,
        report_item_type,
        report_item_id,
        remain,
        ROW_NUMBER() OVER (
            PARTITION BY user_id, report_item_type, report_item_id
            ORDER BY local_event_time DESC
        ) AS row_num
    FROM valid_events
),

stock_period AS (
    SELECT
        report_item_type,
        report_item_id,
        SUM(remain) AS ending_stock,
        COUNT(DISTINCT user_id) AS stock_users
    FROM stock_ranked
    WHERE row_num = 1
    GROUP BY report_item_type, report_item_id
)

SELECT
    CASE flow.report_item_type
        WHEN 1 THEN '基础资源'
        WHEN 10 THEN '局内道具'
        WHEN 11000 THEN '头像'
        WHEN 12000 THEN '头像框'
        ELSE CONCAT('其他类型_', CAST(flow.report_item_type AS VARCHAR))
    END AS "物品类型",
    CASE flow.report_item_id
        WHEN 1 THEN '钻石'
        WHEN 6 THEN '魔法棒'
        WHEN 7 THEN '增加收集槽位'
        WHEN 8 THEN '结算奖励翻倍'
        WHEN 11 THEN '移出一个'
        WHEN 12 THEN '洗牌/风车'
        WHEN 13 THEN '磁铁/提示'
        WHEN 14 THEN '移除/手套'
        ELSE CONCAT('未知物品_', CAST(flow.report_item_id AS VARCHAR))
    END AS "物品名称",
    flow.total_output AS "总产出数量",
    flow.total_consumption AS "总消耗数量",
    flow.net_output AS "净产出数量",
    active.active_user_count AS "区间活跃人数",
    ROUND(
        CAST(flow.total_output AS DOUBLE) / NULLIF(active.active_user_count, 0),
        4
    ) AS "活跃人均产出数量",
    ROUND(
        CAST(flow.total_consumption AS DOUBLE) / NULLIF(active.active_user_count, 0),
        4
    ) AS "活跃人均消耗数量",
    ROUND(
        CAST(flow.net_output AS DOUBLE) / NULLIF(active.active_user_count, 0),
        4
    ) AS "活跃人均净产出",
    flow.flow_users AS "资源变动人数",
    ROUND(
        CAST(flow.net_output AS DOUBLE) / NULLIF(flow.flow_users, 0),
        4
    ) AS "变动用户人均净产出",
    ROUND(
        CAST(flow.flow_users AS DOUBLE) / NULLIF(active.active_user_count, 0) * 100,
        2
    ) AS "资源变动用户占活跃比例(%)",
    stock.ending_stock AS "期末库存",
    stock.stock_users AS "库存用户数",
    CASE
        WHEN flow.net_output > 0 THEN '净流入'
        WHEN flow.net_output < 0 THEN '净流出'
        ELSE '产销平衡'
    END AS "收支状态",
    flow.report_item_type AS "物品类型ID",
    flow.report_item_id AS "物品ID",
    '净产出=总产出-总消耗；期末库存为区间内每名用户最后一次remain之和，不代表全服库存' AS "统计备注"
FROM flow_period flow
LEFT JOIN stock_period stock
    ON stock.report_item_type = flow.report_item_type
   AND stock.report_item_id = flow.report_item_id
CROSS JOIN active_users active
ORDER BY
    flow.report_item_type,
    flow.report_item_id
```

## 关联

- [[02-PROJECTS/TileScape/参考/资源产销统计/分析-资源产销统计口径-2026-10-23|资源产销统计口径]]
- [[02-PROJECTS/TileScape/参考/资源产销统计/SQL-资源产出区间汇总|资源产出区间汇总 SQL]]
- [[02-PROJECTS/TileScape/参考/资源产销统计/SQL-资源消耗区间汇总|资源消耗区间汇总 SQL]]

