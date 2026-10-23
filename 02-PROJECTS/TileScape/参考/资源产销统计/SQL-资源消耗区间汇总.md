---
title: 资源消耗区间汇总 SQL
date: 2026-10-23
type: reference
status: needs-review
project: TileScape
source: 当前 TileScape report_item 代码、打点工作簿与用户确认口径
verification: 静态编写，尚未在当前 TA 环境执行；运行前须复核字段、时间参数和事件覆盖。
tags: [TileScape, ThinkingData, TA, SQL, 资源产销, 资源消耗]
---

# 资源消耗区间汇总 SQL

> [!warning] 验证状态
> 本 SQL 尚未在当前 TA 环境执行。当前统计排除体力相关 `power`、`main`，并只纳入物品 ID `1, 6, 7, 8, 11, 12, 13, 14`。

```sql
/*
资源消耗区间汇总。
仅统计物品 ID：1、6、7、8、11、12、13、14。
数据源：TileScape 历史已核对事件表 ta.v_event_54。
时间参数沿用 TA SQL IDE：${PartDate:date1}、${timezone}、${Time:time1}。
查询结果直接汇总所选时间区间，不固定按天拆分；TA 日期控件默认选择最近 7 天。
人均口径分两类：
- 活跃人均：所选时间区间内触发 ta_app_start 的去重用户数。
- 场景参与人均：使用对应上游场景事件；暂无可靠上游事件时保持为空，不回退为实际消耗用户。
结果字段说明：
- 消耗性质：统一用于钻石和道具的途径分组；钻石拆为关前购买道具、局内购买道具和复活。
- 变化途径：客户端上报的原始 change_method，保留它便于数据核查。
- 途径说明：变化途径的中文业务含义。
- 实际消耗用户人均：消耗数量 / 实际发生资源扣除的用户数。
- 场景参与人均：消耗数量 / 上游场景参与用户数。
- 场景使用率：实际消耗用户数 / 上游场景参与用户数；没有可靠上游分母时为空。
- 主结果不直接按原始 sub_change_method 拆行；该字段只用于把钻石归入四类稳定业务途径。
- 本表不输出具体关卡、商品或道具 ID；后续确有需求时再建立独立下钻表。
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

upstream_events AS (
    SELECT
        e."#user_id" AS user_id,
        e."#event_name" AS event_name,
        CAST(e.gold_num AS BIGINT) AS gold_num
    FROM ta.v_event_54 e
    WHERE ${PartDate:date1}
      AND DATE_ADD(
          'minute',
          CAST((CAST('${timezone}' AS INTEGER) - IF(e."#zone_offset" IS NULL, 0, e."#zone_offset")) * 60 AS INTEGER),
          e."#event_time"
      ) ${Time:time1}
      AND e."#event_name" IN ('lv_start', 'add_moves_show')
      AND e.is_test = false
      AND e."#user_id" IS NOT NULL
),

upstream_participants AS (
    SELECT user_id, 'level_start' AS change_method
    FROM upstream_events
    WHERE event_name = 'lv_start'

    UNION ALL

    SELECT user_id, 'tile_prop_use' AS change_method
    FROM upstream_events
    WHERE event_name = 'lv_start'

    UNION ALL

    SELECT user_id, 'revive' AS change_method
    FROM upstream_events
    WHERE event_name = 'add_moves_show'

    UNION ALL

    SELECT user_id, 'GoldCard' AS change_method
    FROM upstream_events
    WHERE event_name = 'lv_start' AND gold_num > 0
),

participant_counts AS (
    SELECT
        change_method,
        COUNT(DISTINCT user_id) AS participant_user_count
    FROM upstream_participants
    GROUP BY change_method
),

consumption_events AS (
    SELECT
        e."#user_id" AS user_id,
        CAST(e.report_item_type AS INTEGER) AS report_item_type,
        CAST(e.report_item_id AS INTEGER) AS report_item_id,
        CAST(e.change_num AS BIGINT) AS change_num,
        COALESCE(CAST(e.change_method AS VARCHAR), '') AS change_method,
        COALESCE(CAST(e.sub_change_method AS VARCHAR), '') AS sub_change_method
    FROM ta.v_event_54 e
    WHERE ${PartDate:date1}
      AND DATE_ADD(
          'minute',
          CAST((CAST('${timezone}' AS INTEGER) - IF(e."#zone_offset" IS NULL, 0, e."#zone_offset")) * 60 AS INTEGER),
          e."#event_time"
      ) ${Time:time1}
      AND e."#event_name" = 'report_item'
      AND e.is_test = false
      AND CAST(e.change_type AS INTEGER) = -1
      AND CAST(e.change_num AS BIGINT) > 0
      AND CAST(e.report_item_id AS INTEGER) IN (1, 6, 7, 8, 11, 12, 13, 14)
      AND COALESCE(CAST(e.change_method AS VARCHAR), '') <> ''
      AND CAST(e.change_method AS VARCHAR) NOT IN ('power', 'main', 'GM', 'Trade', 'ignore')
),

classified AS (
    SELECT
        user_id,
        report_item_type,
        report_item_id,
        CASE report_item_type
            WHEN 1 THEN '基础资源'
            WHEN 10 THEN '局内道具'
            WHEN 11000 THEN '头像'
            WHEN 12000 THEN '头像框'
            ELSE CONCAT('其他类型_', CAST(report_item_type AS VARCHAR))
        END AS report_item_type_name,
        CASE report_item_id
            WHEN 1 THEN '钻石'
            WHEN 6 THEN '魔法棒'
            WHEN 7 THEN '增加收集槽位'
            WHEN 8 THEN '结算奖励翻倍'
            WHEN 11 THEN '移出一个'
            WHEN 12 THEN '洗牌/风车'
            WHEN 13 THEN '磁铁/提示'
            WHEN 14 THEN '移除/手套'
            ELSE CONCAT('未知物品_', CAST(report_item_id AS VARCHAR))
        END AS item_name,
        change_num,
        change_method,
        CASE
            WHEN report_item_id = 1 AND change_method = 'purchase' AND sub_change_method IN ('6', '7')
                THEN 'diamond_pre_level_prop_purchase'
            WHEN report_item_id = 1 AND change_method = 'purchase' AND sub_change_method IN ('11', '12', '13', '14')
                THEN 'diamond_in_level_prop_purchase'
            WHEN report_item_id = 1 AND change_method = 'revive' THEN 'diamond_revive_consumption'
            WHEN change_method = 'purchase' THEN 'purchase_exchange'
            WHEN change_method = 'level_start' THEN 'pre_level_consumption'
            WHEN change_method = 'tile_prop_use' THEN 'in_level_consumption'
            WHEN change_method = 'revive' THEN 'revive_consumption'
            WHEN change_method = 'GoldCard' THEN 'activity_consumption'
            ELSE 'other_consumption'
        END AS consumption_category,
        CASE
            WHEN report_item_id = 1 AND change_method = 'purchase' AND sub_change_method IN ('6', '7')
                THEN '关前购买道具'
            WHEN report_item_id = 1 AND change_method = 'purchase' AND sub_change_method IN ('11', '12', '13', '14')
                THEN '局内购买道具'
            WHEN report_item_id = 1 AND change_method = 'revive' THEN '复活消耗'
            WHEN change_method = 'purchase' THEN '购买/兑换消耗'
            WHEN change_method = 'level_start' THEN '关前消耗'
            WHEN change_method = 'tile_prop_use' THEN '关内道具消耗'
            WHEN change_method = 'revive' THEN '复活消耗'
            WHEN change_method = 'GoldCard' THEN '活动消耗'
            ELSE '其他资源消耗'
        END AS consumption_category_name,
        CASE
            WHEN report_item_id = 1 AND change_method = 'purchase' AND sub_change_method IN ('6', '7')
                THEN '使用钻石购买关前道具'
            WHEN report_item_id = 1 AND change_method = 'purchase' AND sub_change_method IN ('11', '12', '13', '14')
                THEN '使用钻石购买局内道具'
            WHEN report_item_id = 1 AND change_method = 'revive' THEN '使用钻石复活'
            WHEN change_method = 'purchase' THEN '购买或兑换时消耗支付资源'
            WHEN change_method = 'level_start' THEN '开始关卡时消耗体力或关前道具'
            WHEN change_method = 'tile_prop_use' THEN '关卡内实际使用道具'
            WHEN change_method = 'revive' THEN '关卡失败后的复活消耗'
            WHEN change_method = 'GoldCard' THEN '金牌活动内资源消耗'
            ELSE '尚未配置中文说明的消耗途径'
        END AS change_method_name,
        CASE
            WHEN report_item_id = 1 AND change_method = 'purchase' AND sub_change_method IN ('6', '7')
                THEN '钻石支付侧；副途径仅用于识别为关前购买，不按具体道具拆行'
            WHEN report_item_id = 1 AND change_method = 'purchase' AND sub_change_method IN ('11', '12', '13', '14')
                THEN '钻石支付侧；副途径仅用于识别为局内购买，不按具体道具拆行'
            WHEN report_item_id = 1 AND change_method = 'revive'
                THEN '钻石复活消耗；不按具体关卡拆行'
            WHEN change_method = 'purchase' THEN '购买或兑换的支付侧消耗；获得的道具在产出表另行统计，二者不能直接按数量相减'
            WHEN change_method = 'level_start' THEN '进入关卡时实际扣除的体力或关前道具'
            WHEN change_method = 'tile_prop_use' THEN '关卡内真正使用并扣除库存的道具'
            WHEN change_method = 'revive' THEN '关卡失败后执行复活产生的实际消耗'
            WHEN change_method = 'GoldCard' THEN '金牌活动业务内产生的实际资源消耗'
            ELSE '未归类消耗；需要根据原始途径补充业务映射'
        END AS statistics_note
    FROM consumption_events
),

aggregated AS (
    SELECT
        report_item_type,
        report_item_id,
        report_item_type_name,
        item_name,
        consumption_category,
        consumption_category_name,
        change_method,
        change_method_name,
        statistics_note,
        SUM(change_num) AS consumption_amount,
        COUNT(*) AS consumption_events,
        COUNT(DISTINCT user_id) AS consumption_users
    FROM classified
    GROUP BY
        report_item_type,
        report_item_id,
        report_item_type_name,
        item_name,
        consumption_category,
        consumption_category_name,
        change_method,
        change_method_name,
        statistics_note
)

SELECT
    agg.report_item_type_name AS "物品类型",
    agg.item_name AS "物品名称",
    agg.consumption_category_name AS "消耗性质",
    agg.change_method_name AS "消耗途径",
    agg.consumption_amount AS "消耗数量",
    agg.consumption_events AS "消耗次数",
    agg.consumption_users AS "消耗人数",
    active.active_user_count AS "区间活跃人数",
    ROUND(
        CAST(agg.consumption_amount AS DOUBLE) / NULLIF(active.active_user_count, 0),
        4
    ) AS "活跃人均消耗数量",
    ROUND(
        CAST(agg.consumption_amount AS DOUBLE) / NULLIF(agg.consumption_users, 0),
        4
    ) AS "实际消耗用户人均",
    ROUND(
        CAST(agg.consumption_users AS DOUBLE) / NULLIF(active.active_user_count, 0) * 100,
        2
    ) AS "活跃消耗用户率(%)",
    participant.participant_user_count AS "场景参与人数",
    ROUND(
        CAST(agg.consumption_amount AS DOUBLE)
        / NULLIF(participant.participant_user_count, 0),
        4
    ) AS "场景参与人均消耗数量",
    ROUND(
        CAST(agg.consumption_users AS DOUBLE)
        / NULLIF(participant.participant_user_count, 0) * 100,
        2
    ) AS "场景使用率(%)",
    CASE agg.change_method
        WHEN 'level_start' THEN '进关用户：lv_start'
        WHEN 'tile_prop_use' THEN '进关用户：lv_start'
        WHEN 'revive' THEN '复活机会展示用户：add_moves_show'
        WHEN 'GoldCard' THEN '金牌活动进关用户：lv_start，且 gold_num>0'
        WHEN 'purchase' THEN '暂无可靠统一分母：purchase 同时包含多种购买/兑换入口'
        ELSE '暂无可靠上游场景分母'
    END AS "场景分母口径",
    agg.report_item_type AS "物品类型ID",
    agg.report_item_id AS "物品ID",
    agg.change_method AS "原始变化途径",
    agg.statistics_note AS "统计备注"
FROM aggregated agg
CROSS JOIN active_users active
LEFT JOIN participant_counts participant
    ON participant.change_method = agg.change_method
ORDER BY
    agg.report_item_type,
    agg.report_item_id,
    agg.consumption_category_name,
    agg.change_method
```

## 关联

- [[02-PROJECTS/TileScape/参考/资源产销统计/分析-资源产销统计口径-2026-10-23|资源产销统计口径]]
- [[02-PROJECTS/TileScape/参考/资源产销统计/SQL-资源产出区间汇总|资源产出区间汇总 SQL]]
- [[02-PROJECTS/TileScape/参考/资源产销统计/SQL-资源收支总览|资源收支总览 SQL]]

