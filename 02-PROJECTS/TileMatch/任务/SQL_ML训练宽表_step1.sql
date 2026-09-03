-- ============================================================
-- ML 训练宽表 - Step 1: base_events + user_level_y + level_static + level_group
-- 用途：从打点事件中提取样本标签（y 值）及关卡级特征（静态 + 群体）
-- ============================================================
-- 数据源：ta.v_event_48 + ta.v_user_48
-- 聚合键：lv_name（关卡配置文件名）
-- 清洗：排除测试用户、CN、空 lv_name、Level_ 前缀
-- 排序：默认按 lv_name；备选按 lv_num（lv_name 首个 _ 前的数字）
-- ============================================================

WITH base_events AS (
    /* 事件清洗与字段标准化。
       将 lv_name 转为关卡序号（lv_num），CAST 字符串字段为数值类型。
       过滤事件类型：lv_start / lv_end / lv_revive */
    SELECT
        e."#user_id"                                    AS user_id,
        e."#event_name"                                 AS event_name,
        e."#event_time"                                 AS event_time,
        /* 从 lv_name 提取关卡数字序号，如 "50" → 50，"51_test" → 51 */
        CAST(SPLIT_PART(e.lv_name, '_', 1) AS INTEGER)  AS lv_num,
        e.lv_name,
        
        -- 进入
        /* 进入次数，首次=0，需 +1 修正 */
        CAST(e.level_enter_num AS INTEGER)              AS enter_num,
        e.enter_type,
        
        -- 关卡结果
        /* 1=通关 2=失败 4=退出 5=闪退 6=保底胜利 */
        CAST(e.levelend AS INTEGER)                     AS levelend,
        /* 牌块总数（lv_end / lv_revive 有值，lv_start 无） */
        CAST(e.card_total AS INTEGER)                   AS card_total,
        /* 结束时剩余牌数 */
        CAST(e.card_left AS INTEGER)                    AS card_left,
        /* 死局累计次数 */
        CAST(e.deadlock_times AS INTEGER)               AS deadlock_times,
        /* 关卡用时（秒） */
        CAST(e.lv_time AS DOUBLE)                       AS lv_time,
        
        -- 道具（lv_end 累积值）
        CAST(e.level_shuffle_num AS INTEGER)            AS shuffle_num,
        CAST(e.level_hint_num AS INTEGER)               AS hint_num,
        CAST(e.level_remove_num AS INTEGER)             AS remove_num,
        CAST(e.level_removeone_num AS INTEGER)          AS removeone_num,
        
        -- 调控
        /* 用户实际拿到的期望难度（可能被活动/付费修正） */
        CAST(e.exp_hard AS INTEGER)                     AS exp_hard,
        /* DDA 调控触发次数 */
        CAST(e.control_times AS INTEGER)                AS control_times,
        
        -- 复活
        /* 本次挑战已复活次数 */
        CAST(e.revive_times_cur AS INTEGER)             AS revive_cur,
        /* 该关历史总复活次数 */
        CAST(e.revive_times AS INTEGER)                 AS revive_total,
        /* 该关历史总失败次数 */
        CAST(e.failed_times AS INTEGER)                 AS failed_total,
        /* 0=广告 1=钻石 2=免费 */
        e.revive_type,
        
        -- 环境
        e.activityid,
        e."#app_version"                                AS app_version,
        e."#country_code"                               AS country_code
        
    FROM ta.v_event_48 e
    JOIN ta.v_user_48 u
      ON e."#account_id" = u."#account_id"
    WHERE ${PartDate:date1}
      AND date_add('minute', cast((cast('${timezone}' as int) 
           - if("#zone_offset" is null, 0, "#zone_offset")) * 60 as integer), "#event_time") ${Time:time1}
      /* 排除测试用户 */
      AND e.is_test = false
      /* 排除国内用户 */
      AND e."#country_code" <> 'CN'
      /* 过滤 lv_name 为空的无效事件（无文件名，无分析意义） */
      AND e.lv_name IS NOT NULL
      /* 过滤已弃用的 Level_ 前缀关卡（如 Level_001，SPLIT_PART 返回 'Level' 无法 CAST） */
      AND e.lv_name NOT LIKE 'Level_%'
      /* 关卡事件筛选 */
      AND e."#event_name" IN ('lv_start', 'lv_end', 'lv_revive')
      
      /* 关卡区间限制 */ -- AND CAST(SPLIT_PART(e.lv_name, '_', 1) AS INTEGER) BETWEEN 1 AND 200
      /* 版本筛选 */     -- AND e."#app_version" = '1.2.16'
      /* 关卡测试 */     -- AND e.test_id = 1
      /* AB测试筛选 */   -- AND contains(u."ab_group1", '73_4')
      /* 操作系统筛选 */ -- AND e."#os" = 'iOS'
      /* 广告分层 */     -- AND e."ul_ad_layer" in (1,2,3,6)
      /* 用户分群 */     -- AND u."ul_user_type" <> 'Tile'
      /* campaign筛选 */ -- AND json_extract_scalar(CAST(u."te_ads_object" AS JSON), '$.campaign_name') IN ('...')
      /* 渠道筛选 */     -- AND "#carrier" <> 'Verizon Wireless'
      /* 用户id筛选 */   -- AND e."#account_id" <> '...'
),

-- ============================================================
-- CTE 2: user_level_y — 每行 = 一个用户对一个关卡的汇总结果（y 标签）
-- ============================================================
user_level_y AS (
    SELECT
        user_id,
        lv_name,
        MAX(lv_num) AS lv_num,
        
        -- ===== y1: 是否通关 =====
        /* 只要有一次 lv_end 且 levelend=1，即视为通关 */
        MAX(CASE WHEN event_name = 'lv_end' AND levelend = 1 THEN 1 ELSE 0 END) AS is_clear,
        
        -- ===== y2: 通关所需尝试次数 =====
        /* enter_num 首次=0，取最大+1 得总尝试次数 */
        MAX(CASE WHEN event_name = 'lv_start' THEN enter_num ELSE 0 END) + 1 AS total_attempts,
        
        -- ===== y3: 资源消耗 =====
        /* 道具消耗：取最后一次 lv_end 的累积值 */
        MAX(CASE WHEN event_name = 'lv_end' THEN shuffle_num   ELSE 0 END) AS shuffle_used,
        MAX(CASE WHEN event_name = 'lv_end' THEN hint_num      ELSE 0 END) AS hint_used,
        MAX(CASE WHEN event_name = 'lv_end' THEN remove_num    ELSE 0 END) AS remove_used,
        MAX(CASE WHEN event_name = 'lv_end' THEN removeone_num ELSE 0 END) AS removeone_used,
        /* 道具总数 */
        MAX(CASE WHEN event_name = 'lv_end' THEN 
            shuffle_num + hint_num + remove_num + removeone_num
        ELSE 0 END) AS total_props,
        
        /* 复活消耗：SUM lv_revive 事件数，按类型区分 */
        SUM(CASE WHEN event_name = 'lv_revive' AND revive_type = 1 THEN 1 ELSE 0 END) AS iap_revive,
        SUM(CASE WHEN event_name = 'lv_revive' AND revive_type = 0 THEN 1 ELSE 0 END) AS ad_revive,
        COUNT(CASE WHEN event_name = 'lv_revive' THEN 1 END)     AS total_revive,
        
        -- ===== y 补充指标 =====
        MAX(CASE WHEN event_name = 'lv_end' THEN deadlock_times ELSE 0 END) AS total_deadlock,
        MAX(CASE WHEN event_name = 'lv_end' THEN control_times   ELSE 0 END) AS total_dda,
        MAX(CASE WHEN event_name = 'lv_end' AND levelend = 1 THEN lv_time ELSE 0 END) AS time_win,
        MAX(CASE WHEN event_name = 'lv_end' AND levelend = 2 THEN lv_time ELSE 0 END) AS time_lose,
        
        -- ===== 时间截断点 =====
        /* 该用户首次进入该关卡的时间，用于后续计算用户历史特征 */
        MIN(CASE WHEN event_name = 'lv_start' THEN event_time END) AS first_start_time
        
    FROM base_events
    GROUP BY user_id, lv_name
),

-- ============================================================
-- CTE 3: level_static — 每行 = 一个关卡，静态属性（来自打点）
-- ============================================================
/* 从打点事件中可获取的关卡常量或众数特征。
   花色种类/排列结构/背景/通道数等需从关卡配置文件另取，不在本 CTE 内。 */
level_static AS (
    SELECT
        lv_name,
        MAX(lv_num) AS lv_num,

        /* 牌块总数：同一关卡为常量，取 lv_end 的 AVG 即可 */
        ROUND(AVG(CASE WHEN event_name = 'lv_end' THEN card_total END), 0) AS card_total,

        /* exp_hard 实际值的分布：中位数反映"典型"难度档位 */
        approx_percentile(
            CASE WHEN event_name = 'lv_end' THEN CAST(exp_hard AS DOUBLE) END,
            0.50
        ) AS exp_hard_median,

        /* 是否测试关（lv_name 含 _ 后缀，如 "51_test"） */
        MAX(CASE WHEN lv_name LIKE '%\_%' THEN 1 ELSE 0 END) AS is_test_level

    FROM base_events
    GROUP BY lv_name
),

-- ============================================================
-- CTE 4: level_group — 每行 = 一个关卡，其他用户的群体画像
-- ============================================================
/* 统计该关卡所有用户的行为聚合指标。
   注：此处为全局统计，含所有用户（包括目标用户自身）。
   后续可做 leave-one-out 处理。 */
level_group AS (
    SELECT
        lv_name,
        MAX(lv_num) AS lv_num,

        /* === 基础量 === */
        SUM(CASE WHEN event_name = 'lv_start' THEN 1 ELSE 0 END) * 1.0000                          AS start_count,
        COUNT(DISTINCT CASE WHEN event_name = 'lv_start' THEN user_id END) * 1.0000                 AS start_users,
        SUM(CASE WHEN event_name = 'lv_end' AND levelend = 1 THEN 1 ELSE 0 END) * 1.0000            AS finish_count,
        COUNT(DISTINCT CASE WHEN event_name = 'lv_end' AND levelend = 1 THEN user_id END) * 1.0000  AS finish_users,

        /* === 难度指标 === */
        /* 传统难度：开始次数 / 通关次数 */
        ROUND(SUM(CASE WHEN event_name = 'lv_start' THEN 1 ELSE 0 END) * 1.0
            / NULLIF(SUM(CASE WHEN event_name = 'lv_end' AND levelend = 1 THEN 1 ELSE 0 END), 0), 3) AS difficulty,
        /* 裸难度：开始次数 / 无复活通关次数 */
        ROUND(SUM(CASE WHEN event_name = 'lv_start' THEN 1 ELSE 0 END) * 1.0
            / NULLIF(SUM(CASE WHEN event_name = 'lv_end' AND levelend = 1 AND revive_cur = 0 THEN 1 ELSE 0 END), 0), 3) AS difficulty_raw,

        /* === 复活指标 === */
        SUM(CASE WHEN event_name = 'lv_revive' THEN 1 ELSE 0 END) * 1.0000                           AS total_revive,
        SUM(CASE WHEN event_name = 'lv_revive' AND revive_type = 1 THEN 1 ELSE 0 END) * 1.0000       AS iap_revive,
        SUM(CASE WHEN event_name = 'lv_revive' AND revive_type = 0 THEN 1 ELSE 0 END) * 1.0000       AS ad_revive,

        /* === 人均消耗金额（等价钻） === */
        /* 复活900 / 风车900 / 磁铁900 / 手套1300 / 撤回500 */
        ROUND((
            SUM(CASE WHEN event_name = 'lv_revive' THEN 1 ELSE 0 END) * 900
            + SUM(CASE WHEN event_name = 'lv_end' THEN shuffle_num   ELSE 0 END) * 900
            + SUM(CASE WHEN event_name = 'lv_end' THEN hint_num      ELSE 0 END) * 900
            + SUM(CASE WHEN event_name = 'lv_end' THEN remove_num    ELSE 0 END) * 1300
            + SUM(CASE WHEN event_name = 'lv_end' THEN removeone_num ELSE 0 END) * 500
        ) * 1.0 / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'lv_start' THEN user_id END), 0), 1) AS avg_cost_per_user,

        /* === 死局 / DDA === */
        SUM(CASE WHEN event_name = 'lv_end' THEN deadlock_times END) * 1.0000   AS total_deadlock,
        SUM(CASE WHEN event_name = 'lv_end' THEN control_times   END) * 1.0000   AS total_dda,

        /* === 用时（分钟） === */
        ROUND(SUM(CASE WHEN event_name = 'lv_end' AND levelend = 1 THEN lv_time END)
            / NULLIF(SUM(CASE WHEN event_name = 'lv_end' AND levelend = 1 THEN 1 ELSE 0 END), 0) / 60, 2) AS avg_time_win_min,
        ROUND(SUM(CASE WHEN event_name = 'lv_end' AND levelend = 2 THEN lv_time END)
            / NULLIF(SUM(CASE WHEN event_name = 'lv_end' AND levelend = 2 THEN 1 ELSE 0 END), 0) / 60, 2) AS avg_time_lose_min,

        /* === 关内流失率 === */
        ROUND((COUNT(DISTINCT CASE WHEN event_name = 'lv_start' THEN user_id END)
             - COUNT(DISTINCT CASE WHEN event_name = 'lv_end' AND levelend = 1 THEN user_id END)) * 1.0
            / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'lv_start' THEN user_id END), 0) * 100, 2) AS churn_rate_pct

    FROM base_events
    GROUP BY lv_name
)

SELECT
    y.user_id,
    y.lv_name,
    y.lv_num,
    y.is_clear,
    y.total_attempts,
    y.shuffle_used,
    y.hint_used,
    y.remove_used,
    y.removeone_used,
    y.total_props,
    y.iap_revive,
    y.ad_revive,
    y.total_revive,
    y.total_deadlock,
    y.total_dda,
    y.time_win,
    y.time_lose,

    ls.card_total,
    ls.exp_hard_median,
    ls.is_test_level,

    lg.start_count  AS lg_start_count,
    lg.start_users  AS lg_start_users,
    lg.finish_count AS lg_finish_count,
    lg.finish_users AS lg_finish_users,
    lg.difficulty   AS lg_difficulty,
    lg.difficulty_raw AS lg_difficulty_raw,
    lg.total_revive AS lg_total_revive,
    lg.iap_revive   AS lg_iap_revive,
    lg.ad_revive    AS lg_ad_revive,
    lg.avg_cost_per_user AS lg_avg_cost_per_user,
    lg.total_deadlock AS lg_total_deadlock,
    lg.total_dda    AS lg_total_dda,
    lg.avg_time_win_min  AS lg_avg_time_win_min,
    lg.avg_time_lose_min AS lg_avg_time_lose_min,
    lg.churn_rate_pct AS lg_churn_rate_pct

FROM user_level_y y
LEFT JOIN level_static ls ON y.lv_name = ls.lv_name
LEFT JOIN level_group lg  ON y.lv_name = lg.lv_name
ORDER BY y.user_id, y.lv_num
