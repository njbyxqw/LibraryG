WITH base_events AS (
    /* 共享数据源：一次扫描承接 JOIN + 全部过滤条件，与原版 FROM/JOIN/WHERE 逐字一致。
       后续 level_stats / user_lv_base 全部派生自此，杜绝多方独立扫描导致的数据量偏差。
       lv_id 从 lv_name 取首个 _ 前的数字部分（SPLIT_PART，纯数字=基础关卡，带后缀=测试关卡，数字相同=同 lv_id）；不再依赖 e.lv_id（语义为玩家序号而非关卡 ID）；base_events 过滤 lv_name IS NOT NULL。 */
    SELECT
        e."#user_id",
        CAST(SPLIT_PART(e.lv_name, '_', 1) AS INTEGER) AS lv_id,
        e.lv_name,
        e."#event_name",
        e.levelend,
        e.failed_times,
        e.revive_times,
        e.level_enter_num,
        e.revive_times_cur,
        e.card_left,
        e.card_total,
        e.deadlock_times,
        e.lv_time,
        e.gold_num_claim,
        e.level_shuffle_num,
        e.level_hint_num,
        e.level_remove_num,
        e.level_addslotnum,
        e.level_removeone_num,
        e.exp_hard,
        e.control_times,
        e.control_times_progress_25,
        e.control_times_progress_50,
        e.control_times_progress_75,
        e.control_times_progress_100,
        e.revive_type
    FROM ta.v_event_48 e
    JOIN ta.v_user_48 u
      ON e."#account_id" = u."#account_id"
    WHERE  ${PartDate:date1} 
      AND date_add('minute',cast((cast('${timezone}' as int )-if("#zone_offset" is null,0,"#zone_offset"))*60 as integer),"#event_time") ${Time:time1} 
      AND e.is_test = false
      AND e."#country_code" <> 'CN'
      /* 过滤 lv_name 为空的无效事件（lv_id 从 lv_name 提取，lv_name 为 NULL 无意义） */
      AND e.lv_name IS NOT NULL
      /* campaign筛选（与原版一致：保持注释，包含全部投放计划） */
      -- AND json_extract_scalar(CAST(u."te_ads_object" AS JSON), '$.campaign_name') IN ('Mergevia-AL-IOS-BLD-D7-0617-Tile Test','Mergevia-AL-IOS-CPP-D7-0617-Tile Test')
     
     /* 关卡区间限制 */ -- AND CAST(SPLIT_PART(e.lv_name, '_', 1) AS INTEGER) BETWEEN 1 AND 200
     /* 版本筛选 */  -- AND "#app_version" = '1.2.16'
     /* 关卡测试 */ -- AND e.test_id = 1
     /* AB测试筛选 */  -- AND contains(u."ab_group1", '73_4')
     /* 操作系统筛选 */ -- AND e."#os" = 'iOS'
     /* 广告分层 */ -- AND e."ul_ad_layer" in (1,2,3,6)
     /* 用户分群 */ -- AND u."ul_user_type" <> 'Tile'
     /* 渠道筛选 */ -- AND "#carrier" <> 'Verizon Wireless'
     /* 用户id筛选 */ -- AND e."#account_id" <> '43073964951502848'
)

, level_stats AS (
    SELECT
        lv_id,
        /* 开始次数 */SUM(CASE WHEN "#event_name" = 'lv_start' THEN 1 ELSE 0 END)*1.0000 AS start_count,
        /* 开始人数 */COUNT(DISTINCT CASE WHEN "#event_name" = 'lv_start' THEN e."#user_id" END)*1.0000 AS start_users,
        /* 完成次数 */SUM(CASE WHEN "#event_name" = 'lv_end' AND levelend = 1 THEN 1 ELSE 0 END)*1.0000 AS finish_count,
        /* 完成人数 */COUNT(DISTINCT CASE WHEN "#event_name" = 'lv_end' AND levelend = 1 THEN e."#user_id" END)*1.0000 AS finish_users,
        /* FirstTry次数 */SUM(CASE WHEN "#event_name" = 'lv_start' AND level_enter_num = 1 THEN 1 ELSE 0 END)*1.0000 AS First_try_count,
        /* FirstTry胜利次数 */SUM(CASE WHEN "#event_name" = 'lv_end' AND levelend = 1 AND failed_times = 0 AND revive_times = 0 AND level_enter_num = 1 THEN 1 ELSE 0 END)*1.0000 AS First_try_win,
        /* 无复活过关次数 */SUM(CASE WHEN "#event_name" = 'lv_end' AND levelend = 1 AND revive_times_cur = 0 THEN 1 ELSE 0 END)*1.0000 AS no_add_win,
        /* 单次挑战首次复活时机数 */SUM(CASE WHEN "#event_name" = 'add_moves_show' AND revive_times_cur = 0 THEN 1 ELSE 0 END)*1.0000 AS add_moves_show_1,
        /* 复活时机数 */SUM(CASE WHEN "#event_name" = 'add_moves_show'  THEN 1 ELSE 0 END)*1.0000 AS add_moves_show,
        /* 强复活时机数 */SUM(CASE WHEN "#event_name" = 'add_moves_show' AND e.card_left < 30 THEN 1 ELSE 0 END) * 1.0000 AS reviveshow_count_fuuu,
        /* 总复活数 */SUM(CASE WHEN "#event_name" = 'lv_revive' THEN 1 ELSE 0 END)*1.0000 AS revive_count,
        /* 钻石复活数 */SUM(CASE WHEN "#event_name" = 'lv_revive'AND revive_type = 1 THEN 1 ELSE 0 END)*1.0000 AS revive_count_IAP,
        /* 广告复活数 */SUM(CASE WHEN "#event_name" = 'lv_revive' AND revive_type = 0 THEN 1 ELSE 0 END)*1.0000 AS revive_count_IAA,
        /* 本关牌块总数 */AVG(CASE WHEN "#event_name" = 'add_moves_show' THEN card_total ELSE NULL END) AS card_num,
        /* 平均失败时机剩余牌数 */AVG(CASE WHEN "#event_name" = 'add_moves_show' THEN card_left ELSE NULL END) AS avg_lose_card_left,
        /* 平均首次失败时机剩余牌数 */AVG(CASE WHEN "#event_name" = 'add_moves_show' AND "level_enter_num" = 1 AND revive_times_cur = 0 THEN card_left ELSE NULL END) AS avg_firstlose_card_left,
        /* 平均失败结束剩余牌数 */AVG(CASE WHEN "#event_name" = 'lv_end' AND revive_times_cur = 0 AND levelend = 2 THEN card_left ELSE NULL END) AS avg_firstend_card_left,
        /*死局次数*/sum(CASE WHEN "#event_name" = 'lv_end' THEN deadlock_times ELSE NULL END) AS deadlock_times,
        
        /* 平均过关用时 */SUM(CASE WHEN "#event_name" = 'lv_end'AND levelend = 1 THEN lv_time END)*1.000 AS sum_lv_time_win,
        /* 平均失败用时 */SUM(CASE WHEN "#event_name" = 'lv_end'AND levelend = 2 THEN lv_time END)*1.000 AS sum_lv_time_lose,
        /* 关均金牌收集数 */AVG(CASE WHEN "#event_name" = 'lv_end'AND levelend = 1 THEN gold_num_claim END)*1.000 AS gold_collect,
        /* 风车使用总数 */SUM(CASE WHEN "#event_name" = 'lv_end' AND levelend = 1 THEN level_shuffle_num END)*1.000 AS shuffle_use,
        /* 磁铁使用总数 */SUM(CASE WHEN "#event_name" = 'lv_end' THEN level_hint_num END)*1.000 AS hint_use,
        /* 手套使用总数 */SUM(CASE WHEN "#event_name" = 'lv_end' THEN level_remove_num END)*1.000 AS remove_use,
        /* +1使用总数 */SUM(CASE WHEN "#event_name" = 'lv_end' THEN level_addslotnum END)*1.000 AS add1_use,
        /* 撤回使用总数 */SUM(CASE WHEN "#event_name" = 'lv_end' THEN level_removeone_num END)*1.000 AS remove1_use,
        /* 过关平均期望难度 */AVG(CASE WHEN "#event_name" = 'lv_end'AND levelend = 1 THEN exp_hard END)*1.000 AS exp_hard_win,
        /* 失败平均期望难度 */AVG(CASE WHEN "#event_name" = 'lv_end'AND levelend = 2 THEN exp_hard END)*1.000 AS exp_hard_lose,
        
        /* 通关调控次数 */AVG(CASE WHEN "#event_name" = 'lv_end'AND levelend = 1 THEN control_times END)*1.000 AS DDA_times,
        /* 通关调控次数25 */AVG(CASE WHEN "#event_name" = 'lv_end'AND levelend = 1 THEN control_times_progress_25 END)*1.000 AS DDA_times_25,
        /* 通关调控次数50 */AVG(CASE WHEN "#event_name" = 'lv_end'AND levelend = 1 THEN control_times_progress_50 END)*1.000 AS DDA_times_50,
        /* 通关调控次数75 */AVG(CASE WHEN "#event_name" = 'lv_end'AND levelend = 1 THEN control_times_progress_75 END)*1.000 AS DDA_times_75,
        /* 通关调控次数100 */AVG(CASE WHEN "#event_name" = 'lv_end'AND levelend = 1 THEN control_times_progress_100 END)*1.000 AS DDA_times_100,
        /* 首次失败调控次数 */AVG(CASE WHEN "#event_name" = 'add_moves_show' AND "level_enter_num" = 1 AND revive_times_cur = 0 THEN control_times ELSE NULL END) AS DDA_times_firstfail
        
    FROM base_events e
    GROUP BY e.lv_id
)

-- ==================== 拓展：用户级难度分析 ====================

/* 用户-关卡粒度：每个用户每关一行，含是否通关、尝试次数、复活次数 */
, user_lv_base AS (
    SELECT
        e."#user_id",
        e.lv_id,
        MAX(CASE WHEN "#event_name" = 'lv_end' AND levelend = 1 THEN 1 ELSE 0 END) AS user_is_finish,
        SUM(CASE WHEN "#event_name" = 'lv_start' THEN 1 ELSE 0 END) AS user_start_cnt,
        SUM(CASE WHEN "#event_name" = 'lv_revive' THEN 1 ELSE 0 END) AS user_revive_cnt
    FROM base_events e
    WHERE "#event_name" IN ('lv_start', 'lv_end', 'lv_revive')
    GROUP BY e."#user_id", e.lv_id
)

/* 每关分位值：通关用户(1/0.90/0.99) + 未通关用户(0.90) */
, user_lv_quantile AS (
    SELECT
        b.lv_id,
        approx_percentile(CASE WHEN b.user_is_finish = 1 THEN b.user_start_cnt ELSE NULL END, 0.50) AS p50_attempt,
        approx_percentile(CASE WHEN b.user_is_finish = 1 THEN b.user_start_cnt ELSE NULL END, 0.90) AS p90_attempt,
        approx_percentile(CASE WHEN b.user_is_finish = 1 THEN b.user_start_cnt ELSE NULL END, 0.99) AS p99_attempt,
        approx_percentile(CASE WHEN b.user_is_finish = 0 THEN b.user_start_cnt ELSE NULL END, 0.90) AS p90_attempt_quit
    FROM user_lv_base b
    GROUP BY b.lv_id
)

/* 用户级聚合：通关平均尝试、方差、分位值、trim均值 */
, user_lv_agg AS (
    SELECT
        b.lv_id,
        COUNT(DISTINCT CASE WHEN b.user_is_finish = 1 THEN b."#user_id" END) AS user_finish_users,
        COUNT(DISTINCT CASE WHEN b.user_is_finish = 0 THEN b."#user_id" END) AS user_quit_users,
        /* 通关用户平均尝试次数 */AVG(CASE WHEN b.user_is_finish = 1 THEN b.user_start_cnt ELSE NULL END) AS apw_finish_user,
        /* 难度方差(关内) */VAR_POP(CASE WHEN b.user_is_finish = 1 THEN b.user_start_cnt ELSE NULL END) AS apw_var_user,
        /* 难度标准差(关内) */STDDEV_POP(CASE WHEN b.user_is_finish = 1 THEN b.user_start_cnt ELSE NULL END) AS apw_std_user,
        /* 复活次数方差 */VAR_POP(b.user_revive_cnt) AS revive_var_user,
        /* 复活次数标准差 */STDDEV_POP(b.user_revive_cnt) AS revive_std_user,
        MAX(q.p50_attempt) AS p50_attempt,
        MAX(q.p90_attempt) AS p90_attempt,
        MAX(q.p99_attempt) AS p99_attempt,
        MAX(q.p90_attempt_quit) AS p90_attempt_quit,
        /* 去掉top1%后的trim均值 */AVG(CASE WHEN b.user_is_finish = 1 AND b.user_start_cnt <= q.p99_attempt THEN b.user_start_cnt ELSE NULL END) AS apw_trim1pct
    FROM user_lv_base b
    LEFT JOIN user_lv_quantile q ON b.lv_id = q.lv_id
    GROUP BY b.lv_id
)

-- ==================== 最终输出：原版列 + 拓展列 ====================
SELECT
    -- ===== 原版列 =====
    ls.lv_id AS "Level",
    start_count AS "开始次数",
    start_users AS "开始人数",
    finish_count AS "完成次数",
    finish_users AS "完成人数",
    ROUND(start_count * 1.0 / NULLIF(finish_count, 0), 3) AS "难度",
    ROUND(start_count * 1.0 / NULLIF(no_add_win,0), 3) AS "裸难度",
    /* 消耗金额系数：复活900/风车900/磁铁900/手套1300/撤回500 */
    ROUND((revive_count * 900+shuffle_use * 900+hint_use * 900+remove_use * 1300 + remove1_use * 500)/NULLIF(start_users,0),1) AS "人均消耗",
    ROUND(add_moves_show* 1.0 / NULLIF(start_count * 1.0, 0), 3) AS "次均复活时机数",
    ROUND(deadlock_times * 1.0 / NULLIF(start_users * 1.0, 0), 3) AS "人均死局次数",
    ROUND((start_users * 1.0 - finish_users * 1.0) / NULLIF(start_users * 1.0, 0) * 100, 5) AS "关内流失率(%)",
    ROUND( (LAG(finish_users) OVER (ORDER BY ls.lv_id) * 1.0 - start_users * 1.0) / NULLIF(LAG(finish_users) OVER (ORDER BY ls.lv_id) * 1.0, 0) * 100, 5) AS "关间流失率(%)",
    ROUND((LAG(finish_users) OVER (ORDER BY ls.lv_id) * 1.0 - start_users * 1.0) 
         / NULLIF(LAG(finish_users) OVER (ORDER BY ls.lv_id) * 1.0, 0) * 100 + (start_users * 1.0 - finish_users * 1.0) / NULLIF(start_users * 1.0, 0) * 100, 5) AS "总流失率(%)",
    ROUND(revive_count * 1.0 / NULLIF(start_users * 1.0, 0), 3) AS "人均复活",
    ROUND(revive_count_IAP * 1.0 / NULLIF(start_users * 1.0, 0), 3) AS "人均钻石复活",
    ROUND(revive_count_IAA * 1.0 / NULLIF(start_users * 1.0, 0), 3) AS "人均广告复活",
    ROUND(revive_count * 1.0 / NULLIF(start_count * 1.0, 0), 3) AS "次均复活",
    ROUND(revive_count_IAP * 1.0 / NULLIF(start_count * 1.0, 0), 3) AS "次均钻石复活",
    ROUND(revive_count_IAA * 1.0 / NULLIF(start_count * 1.0, 0), 3) AS "次均广告复活",
    ROUND((add1_use+shuffle_use+hint_use+remove_use+remove1_use)/NULLIF(start_users,0),2) AS "人均道具使用",
    ROUND((add1_use+shuffle_use+hint_use+remove_use+remove1_use)/NULLIF(start_count,0),2) AS "次均道具使用",
    ROUND(DDA_times,1) AS "通关调控次数",
    ROUND(DDA_times_firstfail,1) AS "首次失败调控次数",
    ROUND(DDA_times_25/NULLIF(DDA_times,0),2) AS "通关调控占比_25",
    ROUND(DDA_times_50/NULLIF(DDA_times,0),2) AS "通关调控占比_50",
    ROUND(DDA_times_75/NULLIF(DDA_times,0),2) AS "通关调控占比_75",
    ROUND(DDA_times_100/NULLIF(DDA_times,0),2) AS "通关调控占比_100",
    ROUND(avg_lose_card_left / NULLIF(card_num,0),2) AS "平均失败剩余率",
    ROUND(avg_firstlose_card_left / NULLIF(card_num,0),2) AS "首次失败剩余率",
    ROUND(reviveshow_count_fuuu * 1.0 / NULLIF(add_moves_show, 0), 3) AS "强复活时机占比",
    ROUND(revive_count / NULLIF(add_moves_show, 0), 2) AS "复活转化率",
    ROUND(revive_count_IAP / NULLIF(add_moves_show, 0), 2) AS "钻石复活转化率",
    ROUND(sum_lv_time_win / NULLIF(finish_count, 0) / 60, 2) AS "成功平均用时(分钟)",
    ROUND(sum_lv_time_lose / NULLIF(start_count - finish_count, 0) / 60, 2) AS "失败平均用时(分钟)",
    ROUND(gold_collect,1) AS "平均金牌收集",

    -- ===== 拓展列：用户级难度分析 =====
    ua.user_finish_users AS "完成人数(用户口径)",
    /* 通关用户平均尝试次数 */ROUND(ua.apw_finish_user, 3) AS "难度(通关用户平均)",
    /* 方差/标准差仅在样本>=30时显示 */CASE WHEN ua.user_finish_users >= 30 THEN ROUND(ua.apw_var_user,3) ELSE NULL END AS "难度方差(关内)",
    CASE WHEN ua.user_finish_users >= 30 THEN ROUND(ua.apw_std_user,3) ELSE NULL END AS "难度标准差(关内,次)",
    CASE WHEN ua.user_finish_users >= 30 THEN ROUND(ua.apw_std_user/NULLIF(ua.apw_finish_user,0),3) ELSE NULL END AS "难度变异系数(关内)",
    CASE WHEN ua.user_finish_users >= 30 THEN ROUND(ua.revive_var_user,3) ELSE NULL END AS "复活次数方差(关内)",
    CASE WHEN ua.user_finish_users >= 30 THEN ROUND(ua.revive_std_user,3) ELSE NULL END AS "复活次数标准差(关内)",
    /* 排名性指标 */ROUND(ua.p50_attempt,1) AS "中位数尝试(通关用户)",
    ROUND(ua.p90_attempt,1) AS "P90尝试",
    ROUND(ua.p99_attempt,1) AS "P99尝试",
    /* 未通关用户：90%的放弃者尝试了多少次以内就放弃 */ROUND(ua.p90_attempt_quit,1) AS "P90尝试(未通关)",
    /* 极端值拉高度：(均值-trim均值)/trim均值，衡量top1%对均值的拉升幅度 */
    ROUND((ua.apw_finish_user-ua.apw_trim1pct)/NULLIF(ua.apw_trim1pct,0)*100,1) AS "极端值拉高度(%)",
    /* 中高分位倍数：p90/p50，衡量分布宽度 */ROUND(ua.p90_attempt/NULLIF(ua.p50_attempt,0),2) AS "中高分位倍数",
    /* 极端值断档倍数：p99/p90，衡量尾部断崖程度 */ROUND(ua.p99_attempt/NULLIF(ua.p90_attempt,0),2) AS "极端值断档倍数",
    /* 关卡数据质量标签：p90>5(=难度>5红线) + p90/p50>2.0 双重过滤（v2，命中率~9.3%） */
    CASE
        WHEN ua.user_finish_users < 100 THEN '样本量不足'
        WHEN (ua.apw_finish_user-ua.apw_trim1pct)/NULLIF(ua.apw_trim1pct,0) > 0.10
             AND ua.p99_attempt/NULLIF(ua.p90_attempt,0) > 2.0
        THEN '少数极端用户影响，关卡本身正常'
        WHEN (ua.apw_finish_user-ua.apw_trim1pct)/NULLIF(ua.apw_trim1pct,0) > 0.10
        THEN '存在异常值影响，建议关注'
        WHEN ua.p90_attempt > 5
             AND ua.p90_attempt/NULLIF(ua.p50_attempt,0) > 2.0
        THEN '关卡自身波动大，需剔除'
        ELSE '体验正常'
    END AS "关卡数据质量标签"

FROM level_stats ls
LEFT JOIN user_lv_agg ua ON ls.lv_id = ua.lv_id
ORDER BY ls.lv_id
