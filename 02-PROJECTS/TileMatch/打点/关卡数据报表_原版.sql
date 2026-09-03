WITH level_stats AS (
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
        
    FROM ta.v_event_48 e
    JOIN ta.v_user_48 u
      ON e."#account_id" = u."#account_id"
    WHERE  ${PartDate:date1} 
      AND date_add('minute',cast((cast('${timezone}' as int )-if("#zone_offset" is null,0,"#zone_offset"))*60 as integer),"#event_time") ${Time:time1} 
      AND e.is_test = false
      AND e."#country_code" <> 'CN'
     
     /* 关卡区间限制 */ -- AND e.lv_id BETWEEN 1 AND 200
     /* 版本筛选 */  -- AND "#app_version" = '1.2.16'
     /* 关卡测试 */ -- AND e.test_id = 1
     /* AB测试筛选 */  -- AND contains(u."ab_group1", '53_2')
     /* 操作系统筛选 */ -- AND e."#os" = 'iOS'
     /* 广告分层 */ -- AND e."ul_ad_layer" in (1,2,3,6)
     /* 用户分群 */ -- AND u."ul_user_type" <> 'Tile'
     /* 渠道筛选 */ -- AND "#carrier" <> 'Verizon Wireless'
     /* 用户id筛选 */ -- AND e."#account_id" <> '43073964951502848'
     /* campaign筛选 */ -- AND json_extract_scalar(CAST(u."te_ads_object" AS JSON), '$.campaign_name') IN ('Mergevia-AL-IOS-BLD-D7-0617-Tile Test','Mergevia-AL-IOS-CPP-D7-0617-Tile Test')
           
    GROUP BY e.lv_id
)
SELECT
    lv_id AS "Level",
    start_count AS "开始次数",
    start_users AS "开始人数",
    finish_count AS "完成次数",
    finish_users AS "完成人数",
    ROUND(start_count * 1.0 / NULLIF(finish_count, 0), 3) AS "难度",
    ROUND(start_count * 1.0 / NULLIF(no_add_win,0), 3) AS "裸难度",
    ROUND((revive_count * 900+shuffle_use * 900+hint_use * 900+remove_use * 1300 + remove1_use * 500)/start_users,1) AS "人均消耗",
    ROUND(add_moves_show* 1.0 / NULLIF(start_count * 1.0, 0), 3) AS "次均复活时机数",
    ROUND(deadlock_times * 1.0 / NULLIF(start_users * 1.0, 0), 3) AS "人均死局次数",
    ROUND((start_users * 1.0 - finish_users * 1.0) / NULLIF(start_users * 1.0, 0) * 100, 5) AS "关内流失率(%)",
    ROUND( (LAG(finish_users) OVER (ORDER BY lv_id) * 1.0 - start_users * 1.0) / NULLIF(LAG(finish_users) OVER (ORDER BY lv_id) * 1.0, 0) * 100, 5) AS "关间流失率(%)",
    ROUND((LAG(finish_users) OVER (ORDER BY lv_id) * 1.0 - start_users * 1.0) 
         / NULLIF(LAG(finish_users) OVER (ORDER BY lv_id) * 1.0, 0) * 100 + (start_users * 1.0 - finish_users * 1.0) / NULLIF(start_users * 1.0, 0) * 100, 5) AS "总流失率(%)",
    ROUND(revive_count * 1.0 / NULLIF(start_users * 1.0, 0), 3) AS "人均复活",
    ROUND(revive_count_IAP * 1.0 / NULLIF(start_users * 1.0, 0), 3) AS "人均钻石复活",
    ROUND(revive_count_IAA * 1.0 / NULLIF(start_users * 1.0, 0), 3) AS "人均广告复活",
    ROUND(revive_count * 1.0 / NULLIF(start_count * 1.0, 0), 3) AS "次均复活",
    ROUND(revive_count_IAP * 1.0 / NULLIF(start_count * 1.0, 0), 3) AS "次均钻石复活",
    ROUND(revive_count_IAA * 1.0 / NULLIF(start_count * 1.0, 0), 3) AS "次均广告复活",
    ROUND((add1_use+shuffle_use+hint_use+remove_use+remove1_use)/start_users,2) AS "人均道具使用",
    ROUND((add1_use+shuffle_use+hint_use+remove_use+remove1_use)/start_count,2) AS "次均道具使用",
    ROUND(DDA_times,1) AS "通关调控次数",
    ROUND(DDA_times_firstfail,1) AS "首次失败调控次数",
    ROUND(DDA_times_25/DDA_times,2) AS "通关调控占比_25",
    ROUND(DDA_times_50/DDA_times,2) AS "通关调控占比_50",
    ROUND(DDA_times_75/DDA_times,2) AS "通关调控占比_75",
    ROUND(DDA_times_100/DDA_times,2) AS "通关调控占比_100",
    ROUND(avg_lose_card_left / card_num,2) AS "平均失败剩余率",
    ROUND(avg_firstlose_card_left / card_num,2) AS "首次失败剩余率",
    ROUND(reviveshow_count_fuuu * 1.0 / NULLIF(add_moves_show, 0), 3) AS "强复活时机占比",
    ROUND(revive_count / NULLIF(add_moves_show, 0), 2) AS "复活转化率",
    ROUND(revive_count_IAP / NULLIF(add_moves_show, 0), 2) AS "钻石复活转化率",
    ROUND(sum_lv_time_win / NULLIF(finish_count, 0) / 60, 2) AS "成功平均用时(分钟)",
    ROUND(sum_lv_time_lose / NULLIF(start_count - finish_count, 0) / 60, 2) AS "失败平均用时(分钟)",
    ROUND(gold_collect,1) AS "平均金牌收集"
FROM level_stats
ORDER BY lv_id;
