---
title: 资源产出区间汇总 SQL
date: 2026-10-23
type: reference
status: needs-review
project: TileScape
source: 当前 TileScape report_item 代码、打点工作簿与用户确认口径
verification: 静态编写，尚未在当前 TA 环境执行；运行前须复核字段、时间参数和事件覆盖。
tags: [TileScape, ThinkingData, TA, SQL, 资源产销, 资源产出]
---

# 资源产出区间汇总 SQL

> [!warning] 验证状态
> 本 SQL 尚未在当前 TA 环境执行。当前统计排除体力相关 `power`、`main`，并只纳入物品 ID `1, 6, 7, 8, 11, 12, 13, 14`。

```sql
/*
资源产出区间汇总。
仅统计物品 ID：1、6、7、8、11、12、13、14。
数据源：TileScape 历史已核对事件表 ta.v_event_54。
时间参数沿用 TA SQL IDE：${PartDate:date1}、${timezone}、${Time:time1}。
查询结果直接汇总所选时间区间，不固定按天拆分；TA 日期控件默认选择最近 7 天。
人均口径分两类：
- 活跃人均：所选时间区间内触发 ta_app_start 的去重用户数。
- 渠道参与人均：优先使用对应上游参与/完成事件；暂无可靠上游事件时回退为该途径实际产出用户数。
结果字段说明：
- 产出性质：区分免费投放、玩法奖励、广告获得、购买/兑换获得、返还和初始资源。
- 是否免费投放：广告、购买/兑换获得和返还均为“否”，避免与纯免费投放混算。
- 渠道参与人数 / 参与分母口径：同时展示实际分母及其来源，避免将全活跃用户误当渠道参与用户。
- 产出覆盖率：实际获得该物品的用户数 / 渠道参与人数；没有可靠上游分母时为空。
- 不再计算“渠道参与人数 / ta_app_start 用户数”，两组用户不一定是包含关系，该比例可能超过 100%。
- 产出计量口径：change_unit=count 表示数量，duration_seconds 表示限时时长秒数；二者分行统计。
- 历史数据没有 change_unit：物品 6/7/8 标记为“历史混合口径”，不能无损拆分；其他物品按数量处理。
- 当前兼容：TA 事件表尚未出现 change_unit 列时，SQL 使用空值占位并把物品 6/7/8 标记为历史混合口径。
- 上线切换：确认 TA 已出现 report_item.change_unit 列后，将 output_events 中标注的兼容行替换为正式读取行。
- 主结果不按 sub_change_method 拆行，关卡 ID、商品 ID、广告入口和奖励档位仅用于下钻。
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
        TRY_CAST(e.ad_result AS INTEGER) AS ad_result,
        TRY_CAST(e.gold_num AS BIGINT) AS gold_num,
        COALESCE(CAST(e.result AS VARCHAR), '') AS level_result
    FROM ta.v_event_54 e
    WHERE ${PartDate:date1}
      AND DATE_ADD(
          'minute',
          CAST((CAST('${timezone}' AS INTEGER) - IF(e."#zone_offset" IS NULL, 0, e."#zone_offset")) * 60 AS INTEGER),
          e."#event_time"
      ) ${Time:time1}
      AND e."#event_name" IN (
          'ad_result',
          'lv_start',
          'lv_end',
          'day_sign_reward',
          'channel_bind'
      )
      AND e.is_test = false
      AND e."#user_id" IS NOT NULL
),

upstream_participants AS (
    SELECT user_id, 'ads' AS change_method
    FROM upstream_events
    WHERE event_name = 'ad_result' AND ad_result = 1

    UNION ALL

    SELECT user_id, 'level_end' AS change_method
    FROM upstream_events
    WHERE event_name = 'lv_end' AND level_result = 'win'

    UNION ALL

    SELECT user_id, 'level' AS change_method
    FROM upstream_events
    WHERE event_name = 'lv_end'

    UNION ALL

    SELECT user_id, 'daily_sign' AS change_method
    FROM upstream_events
    WHERE event_name = 'day_sign_reward'

    UNION ALL

    SELECT user_id, 'account_in' AS change_method
    FROM upstream_events
    WHERE event_name = 'channel_bind'

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

output_events AS (
    SELECT
        e."#user_id" AS user_id,
        TRY_CAST(e.report_item_type AS INTEGER) AS report_item_type,
        TRY_CAST(e.report_item_id AS INTEGER) AS report_item_id,
        TRY_CAST(e.change_num AS BIGINT) AS change_num,
        -- 当前兼容行：保证新属性尚未入库时 SQL 仍可运行。
        CAST('' AS VARCHAR) AS change_unit,
        -- TA 出现 change_unit 列后，用下一行替换上一行：
        -- COALESCE(CAST(e.change_unit AS VARCHAR), '') AS change_unit,
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
      AND TRY_CAST(e.change_type AS INTEGER) = 1
      AND TRY_CAST(e.change_num AS BIGINT) > 0
      AND TRY_CAST(e.report_item_id AS INTEGER) IN (1, 6, 7, 8, 11, 12, 13, 14)
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
        CASE
            WHEN change_unit = 'duration_seconds' THEN 'duration_seconds'
            WHEN change_unit = 'count' THEN 'count'
            WHEN report_item_id IN (6, 7, 8) THEN 'legacy_mixed'
            ELSE 'count'
        END AS change_unit,
        change_method,
        CASE
            WHEN change_method = 'purchase' THEN 'purchase_acquisition'
            WHEN change_method = 'ads' THEN 'ad_reward'
            WHEN change_method IN ('level_end', 'home_chest') THEN 'gameplay_reward'
            WHEN change_method IN ('endless', 'GoldCard') THEN 'activity_reward'
            WHEN change_method IN ('daily_sign', 'total_day_sign', 'account_in', 'mail') THEN 'free_grant'
            WHEN change_method = 'level' THEN 'refund'
            WHEN change_method = 'ItemInit' THEN 'initial_grant'
            ELSE 'other_source'
        END AS source_category,
        CASE
            WHEN change_method IN (
                'level_end',
                'home_chest',
                'endless',
                'GoldCard',
                'daily_sign',
                'total_day_sign',
                'account_in',
                'mail',
                'ItemInit'
            ) THEN 1
            ELSE 0
        END AS is_free_source,
        CASE
            WHEN change_method = 'purchase' THEN '购买/兑换获得'
            WHEN change_method = 'ads' THEN '广告获得'
            WHEN change_method IN ('level_end', 'home_chest') THEN '关卡玩法奖励'
            WHEN change_method IN ('endless', 'GoldCard') THEN '活动奖励'
            WHEN change_method IN ('daily_sign', 'total_day_sign', 'account_in', 'mail') THEN '免费投放'
            WHEN change_method = 'level' THEN '资源返还'
            WHEN change_method = 'ItemInit' THEN '初始资源'
            ELSE '其他资源获得'
        END AS source_category_name,
        CASE change_method
            WHEN 'purchase' THEN '商业化购买或游戏内资源兑换'
            WHEN 'ads' THEN '观看广告获得奖励'
            WHEN 'level_end' THEN '关卡结算奖励'
            WHEN 'home_chest' THEN 'Journey路线宝箱奖励'
            WHEN 'daily_sign' THEN '每日签到奖励'
            WHEN 'total_day_sign' THEN '累计签到奖励'
            WHEN 'account_in' THEN '账号绑定奖励'
            WHEN 'endless' THEN '无尽活动免费奖励'
            WHEN 'GoldCard' THEN '金牌活动奖励'
            WHEN 'mail' THEN '邮件附件奖励'
            WHEN 'level' THEN '关卡流程资源返还'
            WHEN 'ItemInit' THEN '新账号初始资源'
            ELSE '尚未配置中文说明的产出途径'
        END AS change_method_name,
        CASE change_method
            WHEN 'purchase' THEN '非免费产出；本行只统计实际获得的道具，支付资源在消耗表另行统计'
            WHEN 'ads' THEN '广告激励产出；与纯免费投放分开统计'
            WHEN 'level_end' THEN '关卡结算实际发放的资源'
            WHEN 'home_chest' THEN 'Journey路线宝箱实际发放的资源'
            WHEN 'daily_sign' THEN '每日签到实际领取的免费资源'
            WHEN 'total_day_sign' THEN '累计签到实际领取的免费资源'
            WHEN 'account_in' THEN '完成账号绑定后实际领取的免费资源'
            WHEN 'endless' THEN '无尽活动免费档实际领取的资源'
            WHEN 'GoldCard' THEN '金牌活动实际领取的奖励资源'
            WHEN 'mail' THEN '通过邮件附件实际领取的资源'
            WHEN 'level' THEN '关卡流程返还，不作为运营免费投放'
            WHEN 'ItemInit' THEN '新账号初始化发放，建议与日常运营投放分开展示'
            ELSE '未归类产出；需要根据原始途径补充业务映射'
        END AS statistics_note
    FROM output_events
),

aggregated AS (
    SELECT
        report_item_type,
        report_item_id,
        change_unit,
        report_item_type_name,
        item_name,
        source_category,
        source_category_name,
        is_free_source,
        change_method,
        change_method_name,
        statistics_note,
        SUM(change_num) AS output_amount,
        COUNT(*) AS output_events,
        COUNT(DISTINCT user_id) AS output_users
    FROM classified
    GROUP BY
        report_item_type,
        report_item_id,
        change_unit,
        report_item_type_name,
        item_name,
        source_category,
        source_category_name,
        is_free_source,
        change_method,
        change_method_name,
        statistics_note
)

SELECT
    agg.report_item_type_name AS "物品类型",
    agg.item_name AS "物品名称",
    CASE agg.change_unit
        WHEN 'duration_seconds' THEN '限时时长（秒）'
        WHEN 'legacy_mixed' THEN '历史混合：数量/时长秒数（不可拆）'
        ELSE '数量（个）'
    END AS "产出计量口径",
    agg.source_category_name AS "产出性质",
    CASE WHEN agg.is_free_source = 1 THEN '是' ELSE '否' END AS "是否免费投放",
    agg.change_method_name AS "产出途径",
    agg.output_amount AS "产出值",
    agg.output_events AS "产出次数",
    agg.output_users AS "产出人数",
    active.active_user_count AS "区间活跃人数",
    ROUND(
        CAST(agg.output_amount AS DOUBLE) / NULLIF(active.active_user_count, 0),
        4
    ) AS "活跃人均产出值",
    COALESCE(participant.participant_user_count, agg.output_users) AS "渠道参与人数",
    ROUND(
        CAST(agg.output_amount AS DOUBLE)
        / NULLIF(COALESCE(participant.participant_user_count, agg.output_users), 0),
        4
    ) AS "渠道参与人均产出值",
    CASE
        WHEN participant.participant_user_count IS NULL THEN NULL
        ELSE ROUND(
            CAST(agg.output_users AS DOUBLE)
            / NULLIF(participant.participant_user_count, 0) * 100,
            2
        )
    END AS "产出覆盖率(%)",
    CASE agg.change_method
        WHEN 'ads' THEN '广告完成用户：ad_result，且 ad_result=1'
        WHEN 'level_end' THEN '关卡胜利结算用户：lv_end，且 result=win'
        WHEN 'level' THEN '关卡结算用户：lv_end'
        WHEN 'daily_sign' THEN '签到领取用户：day_sign_reward'
        WHEN 'account_in' THEN '账号绑定成功用户：channel_bind'
        WHEN 'GoldCard' THEN '金牌活动进关用户：lv_start，且 gold_num>0'
        ELSE '实际产出用户：report_item'
    END AS "参与分母口径",
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
    agg.change_unit,
    agg.is_free_source DESC,
    agg.source_category_name,
    agg.change_method
```

## 关联

- [[02-PROJECTS/TileScape/参考/资源产销统计/分析-资源产销统计口径-2026-10-23|资源产销统计口径]]
- [[02-PROJECTS/TileScape/参考/资源产销统计/SQL-资源消耗区间汇总|资源消耗区间汇总 SQL]]
- [[02-PROJECTS/TileScape/参考/资源产销统计/SQL-资源收支总览|资源收支总览 SQL]]

