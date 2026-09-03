---
title: 关卡间隔时长 SQL
tags: [TileMatch, 打点, SQL, 关卡间隔, 留存]
type: analysis
status: finalized
version: v3
date: 2026-08-28
cat_order: 006
---

# 关卡间隔时长 SQL（v3）

> 背景：以用户分组、列 = 关卡区间 `[n, n+m]`，单元格 = 用户通关 n → 开启 n+m 之间 **m 关的平均关间停留时长（秒/关）**。
> v3 变更：**m=1 每关一列**，`[1,2] [2,3] … [99,100]` 共 99 列全量输出；列配置改用 `SEQUENCE` 简写。
> v3.1 变更：~~上限 `${MaxLevel:100}` 可配置~~ **已回退**：TA 平台动态参数仅支持系统预置（`${PartDate}`/`${Time}`/`${timezone}`），自定义变量会报"动态参数表达式错误"。上限改为硬编码 `SEQUENCE(1, 99)`，即改数字 99。

## 口径（最终版）

| 项 | 定义 |
|---|---|
| 指标 | (n 关首次通关时间 → n+m 关首次开启时间) / m，单位**秒/关** |
| n 关节点 | `lv_end AND levelend IN (1,6)` 的最早时间（保底胜利也算通关） |
| n+m 节点 | `lv_start` 的最早时间 |
| 列 | 每列一个相邻区间 `[n, n+1]`，默认覆盖 1~100 关（99 列）；上限改 `SEQUENCE(1, 99)` 中的 99 |
| 跳关 | 假设不存在跳关（实际验证过），不处理 |
| 用户属性 | 暂不加 |

## 一、宽表版：m=1 每关一列（当前需求）

```sql
WITH base_events AS (
    SELECT
        e."#user_id"              AS user_id,
        CAST(e.lv_id AS INT)      AS lv_num,      -- lv_id 实为 VARCHAR，必须转 INT
        e."#event_name"           AS event_name,
        e.levelend,
        e."#event_time"           AS evt_time
    FROM ta.v_event_48 e
    JOIN ta.v_user_48 u
      ON e."#account_id" = u."#account_id"
    WHERE ${PartDate:date1}
      AND date_add('minute', cast((cast('${timezone}' as int)
           - if("#zone_offset" is null, 0, "#zone_offset")) * 60 as integer),
           "#event_time") ${Time:time1}
      AND e.is_test = false
      AND e."#country_code" <> 'CN'
      AND e."#event_name" IN ('lv_start', 'lv_end')
      /* 关卡区间限制：覆盖列终点即可（100） */
      -- AND CAST(e.lv_id AS INT) BETWEEN 1 AND 100
),

/* 用户-关卡节点：首次开启时间 + 首次通关时间 */
user_lv_node AS (
    SELECT
        user_id,
        lv_num,
        MIN(CASE WHEN event_name = 'lv_start' THEN evt_time END) AS first_start_time,
        MIN(CASE WHEN event_name = 'lv_end' AND levelend IN (1, 6)
                 THEN evt_time END) AS first_clear_time
    FROM base_events
    GROUP BY user_id, lv_num
),

/* ===== 列配置 =====
   默认覆盖前 100 关：SEQUENCE(1, 99) → [1,2] ~ [99,100] 共 99 列
   想改上限：只改数字 99（如前 150 关改 149），并同步下方宽表列段
   想换任意长度分段（如 10 关一段）：改回
   SELECT m, SUM(m) OVER (ORDER BY rn) - m + 1 AS n, SUM(m) OVER (ORDER BY rn) AS n_end
   FROM (SELECT m, ROW_NUMBER() OVER () AS rn
         FROM (VALUES (10),(10),(10),(10),(10),(10),(10),(10),(10),(10)) AS t(m))   */
col_config AS (
    SELECT 1 AS m, x AS n, x + 1 AS n_end
    FROM UNNEST(SEQUENCE(1, 99)) AS t(x)
),

/* 区间时长：n 关通关 → n_end 关开启 */
seg_interval AS (
    SELECT
        a.user_id,
        c.n,
        c.n_end,
        c.m,
        date_diff('second', a.first_clear_time, b.first_start_time) AS seg_sec
    FROM user_lv_node a
    JOIN col_config c
      ON a.lv_num = c.n AND a.first_clear_time IS NOT NULL
    JOIN user_lv_node b
      ON b.user_id = a.user_id AND b.lv_num = c.n_end AND b.first_start_time IS NOT NULL
)

/* 宽表列段 = 静态生成（默认前 100 关 = 99 列）。
   改上限后，此处列段需按区间数同步重生成，规律：
   每行一个 CASE WHEN n = k（k = 1..上限-1），列名 "k-(k+1)"；
   不想维护列段就直接用下方「长表版」，上限改了列自动跟着变 */
SELECT
    user_id,
    ROUND(MAX(CASE WHEN n = 1  THEN seg_sec * 1.0 / m END), 1) AS "1-2",
    ROUND(MAX(CASE WHEN n = 2  THEN seg_sec * 1.0 / m END), 1) AS "2-3",
    ROUND(MAX(CASE WHEN n = 3  THEN seg_sec * 1.0 / m END), 1) AS "3-4",
    ROUND(MAX(CASE WHEN n = 4  THEN seg_sec * 1.0 / m END), 1) AS "4-5",
    ROUND(MAX(CASE WHEN n = 5  THEN seg_sec * 1.0 / m END), 1) AS "5-6",
    ROUND(MAX(CASE WHEN n = 6  THEN seg_sec * 1.0 / m END), 1) AS "6-7",
    ROUND(MAX(CASE WHEN n = 7  THEN seg_sec * 1.0 / m END), 1) AS "7-8",
    ROUND(MAX(CASE WHEN n = 8  THEN seg_sec * 1.0 / m END), 1) AS "8-9",
    ROUND(MAX(CASE WHEN n = 9  THEN seg_sec * 1.0 / m END), 1) AS "9-10",
    ROUND(MAX(CASE WHEN n = 10 THEN seg_sec * 1.0 / m END), 1) AS "10-11",
    ROUND(MAX(CASE WHEN n = 11 THEN seg_sec * 1.0 / m END), 1) AS "11-12",
    ROUND(MAX(CASE WHEN n = 12 THEN seg_sec * 1.0 / m END), 1) AS "12-13",
    ROUND(MAX(CASE WHEN n = 13 THEN seg_sec * 1.0 / m END), 1) AS "13-14",
    ROUND(MAX(CASE WHEN n = 14 THEN seg_sec * 1.0 / m END), 1) AS "14-15",
    ROUND(MAX(CASE WHEN n = 15 THEN seg_sec * 1.0 / m END), 1) AS "15-16",
    ROUND(MAX(CASE WHEN n = 16 THEN seg_sec * 1.0 / m END), 1) AS "16-17",
    ROUND(MAX(CASE WHEN n = 17 THEN seg_sec * 1.0 / m END), 1) AS "17-18",
    ROUND(MAX(CASE WHEN n = 18 THEN seg_sec * 1.0 / m END), 1) AS "18-19",
    ROUND(MAX(CASE WHEN n = 19 THEN seg_sec * 1.0 / m END), 1) AS "19-20",
    ROUND(MAX(CASE WHEN n = 20 THEN seg_sec * 1.0 / m END), 1) AS "20-21",
    ROUND(MAX(CASE WHEN n = 21 THEN seg_sec * 1.0 / m END), 1) AS "21-22",
    ROUND(MAX(CASE WHEN n = 22 THEN seg_sec * 1.0 / m END), 1) AS "22-23",
    ROUND(MAX(CASE WHEN n = 23 THEN seg_sec * 1.0 / m END), 1) AS "23-24",
    ROUND(MAX(CASE WHEN n = 24 THEN seg_sec * 1.0 / m END), 1) AS "24-25",
    ROUND(MAX(CASE WHEN n = 25 THEN seg_sec * 1.0 / m END), 1) AS "25-26",
    ROUND(MAX(CASE WHEN n = 26 THEN seg_sec * 1.0 / m END), 1) AS "26-27",
    ROUND(MAX(CASE WHEN n = 27 THEN seg_sec * 1.0 / m END), 1) AS "27-28",
    ROUND(MAX(CASE WHEN n = 28 THEN seg_sec * 1.0 / m END), 1) AS "28-29",
    ROUND(MAX(CASE WHEN n = 29 THEN seg_sec * 1.0 / m END), 1) AS "29-30",
    ROUND(MAX(CASE WHEN n = 30 THEN seg_sec * 1.0 / m END), 1) AS "30-31",
    ROUND(MAX(CASE WHEN n = 31 THEN seg_sec * 1.0 / m END), 1) AS "31-32",
    ROUND(MAX(CASE WHEN n = 32 THEN seg_sec * 1.0 / m END), 1) AS "32-33",
    ROUND(MAX(CASE WHEN n = 33 THEN seg_sec * 1.0 / m END), 1) AS "33-34",
    ROUND(MAX(CASE WHEN n = 34 THEN seg_sec * 1.0 / m END), 1) AS "34-35",
    ROUND(MAX(CASE WHEN n = 35 THEN seg_sec * 1.0 / m END), 1) AS "35-36",
    ROUND(MAX(CASE WHEN n = 36 THEN seg_sec * 1.0 / m END), 1) AS "36-37",
    ROUND(MAX(CASE WHEN n = 37 THEN seg_sec * 1.0 / m END), 1) AS "37-38",
    ROUND(MAX(CASE WHEN n = 38 THEN seg_sec * 1.0 / m END), 1) AS "38-39",
    ROUND(MAX(CASE WHEN n = 39 THEN seg_sec * 1.0 / m END), 1) AS "39-40",
    ROUND(MAX(CASE WHEN n = 40 THEN seg_sec * 1.0 / m END), 1) AS "40-41",
    ROUND(MAX(CASE WHEN n = 41 THEN seg_sec * 1.0 / m END), 1) AS "41-42",
    ROUND(MAX(CASE WHEN n = 42 THEN seg_sec * 1.0 / m END), 1) AS "42-43",
    ROUND(MAX(CASE WHEN n = 43 THEN seg_sec * 1.0 / m END), 1) AS "43-44",
    ROUND(MAX(CASE WHEN n = 44 THEN seg_sec * 1.0 / m END), 1) AS "44-45",
    ROUND(MAX(CASE WHEN n = 45 THEN seg_sec * 1.0 / m END), 1) AS "45-46",
    ROUND(MAX(CASE WHEN n = 46 THEN seg_sec * 1.0 / m END), 1) AS "46-47",
    ROUND(MAX(CASE WHEN n = 47 THEN seg_sec * 1.0 / m END), 1) AS "47-48",
    ROUND(MAX(CASE WHEN n = 48 THEN seg_sec * 1.0 / m END), 1) AS "48-49",
    ROUND(MAX(CASE WHEN n = 49 THEN seg_sec * 1.0 / m END), 1) AS "49-50",
    ROUND(MAX(CASE WHEN n = 50 THEN seg_sec * 1.0 / m END), 1) AS "50-51",
    ROUND(MAX(CASE WHEN n = 51 THEN seg_sec * 1.0 / m END), 1) AS "51-52",
    ROUND(MAX(CASE WHEN n = 52 THEN seg_sec * 1.0 / m END), 1) AS "52-53",
    ROUND(MAX(CASE WHEN n = 53 THEN seg_sec * 1.0 / m END), 1) AS "53-54",
    ROUND(MAX(CASE WHEN n = 54 THEN seg_sec * 1.0 / m END), 1) AS "54-55",
    ROUND(MAX(CASE WHEN n = 55 THEN seg_sec * 1.0 / m END), 1) AS "55-56",
    ROUND(MAX(CASE WHEN n = 56 THEN seg_sec * 1.0 / m END), 1) AS "56-57",
    ROUND(MAX(CASE WHEN n = 57 THEN seg_sec * 1.0 / m END), 1) AS "57-58",
    ROUND(MAX(CASE WHEN n = 58 THEN seg_sec * 1.0 / m END), 1) AS "58-59",
    ROUND(MAX(CASE WHEN n = 59 THEN seg_sec * 1.0 / m END), 1) AS "59-60",
    ROUND(MAX(CASE WHEN n = 60 THEN seg_sec * 1.0 / m END), 1) AS "60-61",
    ROUND(MAX(CASE WHEN n = 61 THEN seg_sec * 1.0 / m END), 1) AS "61-62",
    ROUND(MAX(CASE WHEN n = 62 THEN seg_sec * 1.0 / m END), 1) AS "62-63",
    ROUND(MAX(CASE WHEN n = 63 THEN seg_sec * 1.0 / m END), 1) AS "63-64",
    ROUND(MAX(CASE WHEN n = 64 THEN seg_sec * 1.0 / m END), 1) AS "64-65",
    ROUND(MAX(CASE WHEN n = 65 THEN seg_sec * 1.0 / m END), 1) AS "65-66",
    ROUND(MAX(CASE WHEN n = 66 THEN seg_sec * 1.0 / m END), 1) AS "66-67",
    ROUND(MAX(CASE WHEN n = 67 THEN seg_sec * 1.0 / m END), 1) AS "67-68",
    ROUND(MAX(CASE WHEN n = 68 THEN seg_sec * 1.0 / m END), 1) AS "68-69",
    ROUND(MAX(CASE WHEN n = 69 THEN seg_sec * 1.0 / m END), 1) AS "69-70",
    ROUND(MAX(CASE WHEN n = 70 THEN seg_sec * 1.0 / m END), 1) AS "70-71",
    ROUND(MAX(CASE WHEN n = 71 THEN seg_sec * 1.0 / m END), 1) AS "71-72",
    ROUND(MAX(CASE WHEN n = 72 THEN seg_sec * 1.0 / m END), 1) AS "72-73",
    ROUND(MAX(CASE WHEN n = 73 THEN seg_sec * 1.0 / m END), 1) AS "73-74",
    ROUND(MAX(CASE WHEN n = 74 THEN seg_sec * 1.0 / m END), 1) AS "74-75",
    ROUND(MAX(CASE WHEN n = 75 THEN seg_sec * 1.0 / m END), 1) AS "75-76",
    ROUND(MAX(CASE WHEN n = 76 THEN seg_sec * 1.0 / m END), 1) AS "76-77",
    ROUND(MAX(CASE WHEN n = 77 THEN seg_sec * 1.0 / m END), 1) AS "77-78",
    ROUND(MAX(CASE WHEN n = 78 THEN seg_sec * 1.0 / m END), 1) AS "78-79",
    ROUND(MAX(CASE WHEN n = 79 THEN seg_sec * 1.0 / m END), 1) AS "79-80",
    ROUND(MAX(CASE WHEN n = 80 THEN seg_sec * 1.0 / m END), 1) AS "80-81",
    ROUND(MAX(CASE WHEN n = 81 THEN seg_sec * 1.0 / m END), 1) AS "81-82",
    ROUND(MAX(CASE WHEN n = 82 THEN seg_sec * 1.0 / m END), 1) AS "82-83",
    ROUND(MAX(CASE WHEN n = 83 THEN seg_sec * 1.0 / m END), 1) AS "83-84",
    ROUND(MAX(CASE WHEN n = 84 THEN seg_sec * 1.0 / m END), 1) AS "84-85",
    ROUND(MAX(CASE WHEN n = 85 THEN seg_sec * 1.0 / m END), 1) AS "85-86",
    ROUND(MAX(CASE WHEN n = 86 THEN seg_sec * 1.0 / m END), 1) AS "86-87",
    ROUND(MAX(CASE WHEN n = 87 THEN seg_sec * 1.0 / m END), 1) AS "87-88",
    ROUND(MAX(CASE WHEN n = 88 THEN seg_sec * 1.0 / m END), 1) AS "88-89",
    ROUND(MAX(CASE WHEN n = 89 THEN seg_sec * 1.0 / m END), 1) AS "89-90",
    ROUND(MAX(CASE WHEN n = 90 THEN seg_sec * 1.0 / m END), 1) AS "90-91",
    ROUND(MAX(CASE WHEN n = 91 THEN seg_sec * 1.0 / m END), 1) AS "91-92",
    ROUND(MAX(CASE WHEN n = 92 THEN seg_sec * 1.0 / m END), 1) AS "92-93",
    ROUND(MAX(CASE WHEN n = 93 THEN seg_sec * 1.0 / m END), 1) AS "93-94",
    ROUND(MAX(CASE WHEN n = 94 THEN seg_sec * 1.0 / m END), 1) AS "94-95",
    ROUND(MAX(CASE WHEN n = 95 THEN seg_sec * 1.0 / m END), 1) AS "95-96",
    ROUND(MAX(CASE WHEN n = 96 THEN seg_sec * 1.0 / m END), 1) AS "96-97",
    ROUND(MAX(CASE WHEN n = 97 THEN seg_sec * 1.0 / m END), 1) AS "97-98",
    ROUND(MAX(CASE WHEN n = 98 THEN seg_sec * 1.0 / m END), 1) AS "98-99",
    ROUND(MAX(CASE WHEN n = 99 THEN seg_sec * 1.0 / m END), 1) AS "99-100"
FROM seg_interval
GROUP BY user_id
ORDER BY user_id;
```

## 二、长表版（备用：改长度零维护）

列不固定时用此版，输出 `user_id, seg_name, from_lv, to_lv, m, avg_dwell_sec`，BI/Excel 按 seg_name 透视即可。

```sql
-- 前面 CTE（base_events / user_lv_node / col_config / seg_interval）完全同上，
-- 仅 col_config 按需改为任意长度列表（见上方注释里的 VALUES 写法），最终 SELECT 替换为：
SELECT
    user_id,
    seg_name,
    n      AS from_lv,
    n_end  AS to_lv,
    m,
    ROUND(seg_sec * 1.0 / m, 1) AS avg_dwell_sec
FROM seg_interval
ORDER BY user_id, n;
```

> 注：长表版需要 `seg_interval` 额外带出 `seg_name`，即 `CAST(c.n AS VARCHAR) || '-' || CAST(c.n_end AS VARCHAR)`。

## 版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1 | 2026-08-28 | 初版：10 关一段宽表 + 列配置 VALUES |
| v2 | 2026-08-28 | 修复 `...` 占位符导致的解析报错；列配置改为只配长度 m、起点自动累加 |
| v3 | 2026-08-28 | **m=1 每关一列**：`[1,2] [2,3] … [99,100]` 全量输出，`col_config` 改用 `SEQUENCE(1,99)` 简写 |
| v3.1 | 2026-08-28 | 上限曾试 `${MaxLevel:100}` 配置，**TA 平台不支持自定义动态参数（报"动态参数表达式错误"），已回退**：`SEQUENCE(1, 99)` 硬编码，上限改数字 99 |

---

## 关联

- [[_MOC|TileMatch 知识库 MOC]]
