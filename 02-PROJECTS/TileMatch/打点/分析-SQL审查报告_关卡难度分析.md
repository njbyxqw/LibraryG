---
tags: [TileMatch, 打点, SQL]
type: report
status: draft
date: 2026-07-03
cat_order: 005
---

# 关卡难度 SQL 审查报告

## 审查对象

用户提供的 TA (ThinkingData) 关卡难度分析 SQL，运行于 Presto/Trino 引擎。

---

## 🔴 Critical — 会导致计算结果错误

### 1. `levelend = 6`（保底胜利 GuaranteeSuccess）被遗漏

**代码验证** (`LevelFinishReason.cs`)：

```csharp
public enum LevelFinishReason
{
    None = 0,
    Success = 1,           // 正常通关
    Fail = 2,              // 放弃复活失败
    Quit = 4,              // 主动退出
    Crash = 5,             // 闪退
    GuaranteeSuccess = 6,  // 保底胜利
}
```

**问题**：SQL 中所有"通关"相关指标只判断 `levelend = 1`，完全遗漏了 `levelend = 6`（保底胜利）。保底胜利对玩家来说也是通关，但被排除在：

| 受影响指标 | 当前条件 | 影响 |
|-----------|---------|------|
| `finish_count` | `levelend = 1` | 通关次数偏低 |
| `no_add_win` | `levelend = 1 AND revive_times_cur = 0` | 裸难度偏高 |
| `First_try_win` | `levelend = 1 AND ...` | 首胜次数偏低 |
| `sum_lv_time_win` | `levelend = 1` | 通关用时统计偏低 |
| `exp_hard_win` | `levelend = 1` | 通关期望难度偏低 |
| `gold_collect` | `levelend = 1` | 金币采集统计偏低 |
| `shuffle_use` / `hint_use` 等 | `levelend = 1` | 道具使用统计偏低 |
| 所有 DDA 指标 | `levelend = 1` | 调控次数统计偏低 |
| `finish_users_user` | `levelend = 1`（user_lv_base 层） | 通关人数偏低 → 难度指标全部偏高 |

**修复**：将所有 `levelend = 1` 改为 `levelend IN (1, 6)`

```sql
-- 修改前
SUM(CASE WHEN "#event_name" = 'lv_end' AND levelend = 1 THEN 1 ELSE 0 END)

-- 修改后
SUM(CASE WHEN "#event_name" = 'lv_end' AND levelend IN (1, 6) THEN 1 ELSE 0 END)
```

> 同理 `user_lv_base` 中的 `MAX(CASE WHEN "#event_name"='lv_end' AND levelend=1 THEN 1 ELSE 0 END)` 也需要改。

---

### 2. `lv_id` 字符串排序导致 `ORDER BY` 和 `LAG` 顺序错误

**代码验证** (`TaDataManager.cs`)：

```csharp
int lvID = DataCenter.Instance.LevelCommonData.Level;
dict["lv_id"] = lvID;  // C# 端是 int
```

**问题**：TA 平台上 `lv_id` 实际存储为 **VARCHAR**（TA SDK 序列化时转为字符串）。SQL 中的排序操作会产生字典序而非数值序：

```
字典序: 1, 10, 100, 101, ..., 11, 12, ..., 19, 2, 20, 21, ...
数值序: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...
```

**受影响**：
- `ORDER BY ea.lv_id` — 结果集排序错乱
- `LAG(ua.finish_users_user) OVER (ORDER BY ea.lv_id)` — **"关间流失率(%)"** 取到了错误的"上一关"
- 注释掉的 `e.lv_id BETWEEN 1 AND 200` — 隐式转换不可靠

**修复**：

```sql
-- 修改前
ORDER BY ea.lv_id

-- 修改后
ORDER BY CAST(ea.lv_id AS INT)

-- LAG 也要改
LAG(ua.finish_users_user) OVER (ORDER BY CAST(ea.lv_id AS INT))
```

---

### 3. "失败平均用时" 分母不匹配

**问题**：

```sql
-- 分子：只包含 levelend = 2 (Fail) 的 lv_time 之和
SUM(CASE WHEN "#event_name" = 'lv_end' AND levelend = 2 THEN lv_time END) AS sum_lv_time_lose

-- 分母：start_count - finish_count
--   = lv_start 次数 - lv_end(levelend=1) 次数
--   包含了：Fail(2) + Quit(4) + Crash(5) + GuaranteeSuccess(6) + 无 lv_end 的中途退出
ROUND(ea.sum_lv_time_lose / NULLIF(ea.start_count - ea.finish_count, 0) / 60, 2)
```

分母远大于实际失败事件数（因为包含了退出/闪退/保底/中途退出），导致**失败平均用时被低估**。

**修复**：新增一个实际失败次数的指标

```sql
-- 在 event_lv_agg 中新增
SUM(CASE WHEN "#event_name" = 'lv_end' AND levelend IN (2, 4) THEN 1 ELSE 0 END)*1.0000 AS fail_count,

-- 最终 SELECT 中
ROUND(ea.sum_lv_time_lose / NULLIF(ea.fail_count, 0) / 60, 2) AS "失败平均用时(分钟)"
```

> 注：是否包含 Quit(4) 取决于业务定义。如果只统计"打完了但没赢"的失败，用 `levelend = 2`；如果也包含中途退出，用 `levelend IN (2, 4)`。

---

### 4. "首次失败剩余率" 分母用了全量 card_num

**问题**：

```sql
-- 分子：仅首次失败（level_enter_num=1 AND revive_times_cur=0）的 card_left 均值
AVG(CASE WHEN "#event_name" = 'add_moves_show' AND "level_enter_num" = 1 AND revive_times_cur = 0 
    THEN card_left ELSE NULL END) AS avg_firstlose_card_left

-- 分母：所有 add_moves_show 事件的 card_total 均值
AVG(CASE WHEN "#event_name" = 'add_moves_show' THEN card_total ELSE NULL END) AS card_num

-- 最终比率
ROUND(ea.avg_firstlose_card_left / NULLIF(ea.card_num, 0), 2) AS "首次失败剩余率"
```

分子是首次失败子集的 `card_left`，分母是全量的 `card_total`，**两个不同人群的均值做除法**，结果无实际意义。

**修复**：新增首次失败的 `card_total` 均值

```sql
-- 在 event_lv_agg 中新增
AVG(CASE WHEN "#event_name" = 'add_moves_show' AND "level_enter_num" = 1 AND revive_times_cur = 0 
    THEN card_total ELSE NULL END) AS card_num_firstlose,

-- 最终 SELECT 中
ROUND(ea.avg_firstlose_card_left / NULLIF(ea.card_num_firstlose, 0), 2) AS "首次失败剩余率"
```

---

## 🟡 Medium — 可能导致偏差

### 5. `level_enter_num` 值需验证

**代码分析**：

调用顺序 (`LevelFlowData.cs`)：
```
OnLevelStartEvent()
  ├── LevelControlData.OnLevelStart()  → SetLevelEnterTimes()  // 首次进入: 0→1, 存储 "lvId_1"
  └── TaDataManager.SendLvStartEvent() → GetLevelDataTimes()    // 读取存储值, 返回 1
```

从代码看，首次进入应上报 `level_enter_num = 1`。

但打点测试文档（2026-06-08）记录："首次进入上报为 0"。

**可能原因**：
- 测试时 ProfileHub 数据未初始化（全新安装 + 特殊路径）
- 测试时版本代码与当前不同
- 重连场景下 `SetLevelEnterTimes()` 被跳过

**建议**：在 TA 中执行验证查询

```sql
SELECT lv_id, level_enter_num, COUNT(*) as cnt
FROM ta.v_event_48
WHERE "#event_name" = 'lv_start' AND ${PartDate:date1}
GROUP BY lv_id, level_enter_num
ORDER BY CAST(lv_id AS INT), CAST(level_enter_num AS INT)
LIMIT 20
```

如果确认首次进入确实是 0，则 SQL 中所有 `level_enter_num = 1` 需改为 `level_enter_num = 0`。

---

### 6. `revive_var_user` / `revive_std_user` 计算范围不一致

**问题**：

```sql
-- attempt 指标：只算通关用户
AVG(CASE WHEN b.user_is_finish=1 THEN b.user_start_cnt ELSE NULL END) AS apw_finish_user

-- revive 指标：算了所有用户（含未通关）
VAR_POP(b.user_revive_cnt) AS revive_var_user
STDDEV_POP(b.user_revive_cnt) AS revive_std_user
```

如果业务意图是"通关用户的复活次数方差"，应加 `CASE WHEN b.user_is_finish=1`。如果意图是"所有用户的复活次数方差"，则当前正确但与 attempt 指标的口径不一致。

---

### 7. 缺少 NULLIF 保护

以下三处除法缺少 NULLIF，当 `start_users` 或 `start_count` 为 0 时会报错：

```sql
-- "人均消耗"
ROUND((ea.revive_count * 900 + ...) / ea.start_users, 1)          -- ⚠️ 缺少 NULLIF

-- "人均道具使用"
ROUND((ea.add1_use + ea.shuffle_use + ...) / ea.start_users, 2)   -- ⚠️ 缺少 NULLIF

-- "次均道具使用"
ROUND((ea.add1_use + ea.shuffle_use + ...) / ea.start_count, 2)   -- ⚠️ 缺少 NULLIF
```

**修复**：加上 `NULLIF(..., 0)`

---

### 8. `user_start_cnt` 包含通关后继续玩的次数

**问题**：`user_lv_base` 按 `("#user_id", lv_id)` 分组，如果用户通关后又重玩同一关（刷奖励），`user_start_cnt` 会包含通关后的次数，导致 `apw_finish_user`（通关用户平均尝试次数）被高估。

**当前逻辑**：所有 `lv_start` 事件都计入，不管是否已经通关过。

**影响场景**：刷金币/刷三星等重玩场景较多的关卡，难度指标偏高。

**修复方案**（如果意图是"首次通关所需次数"）：需要在 `user_lv_base` 中只统计首次通关前的 `lv_start`，但这需要事件时间排序，SQL 复杂度大增。如果当前口径可接受（"总尝试次数"而非"首次通关尝试次数"），则保持不变。

---

## 🟢 Minor — 设计备注

### 9. `VAR_POP` vs `VAR_SAMP`

使用总体方差 `VAR_POP` 而非样本方差 `VAR_SAMP`。对于大样本（finish_users_user > 100），差异可忽略。如果样本量小，`VAR_SAMP` 更合适。当前 SQL 在 `finish_users_user < 30` 时不显示方差，有一定保护。

### 10. 两个均值的比率 vs 均值的比率

```sql
-- 当前：先分别求均值，再做除法
ROUND(ea.avg_lose_card_left / NULLIF(ea.card_num, 0), 2)

-- 更精确：对每个事件先求比率，再取均值
AVG(CASE WHEN "#event_name" = 'add_moves_show' THEN card_left * 1.0 / card_total ELSE NULL END)
```

当前方式是常见近似，在 `card_total` 跨事件差异不大时可接受。

### 11. 道具消耗金额系数需验证

```sql
revive_count * 900 + shuffle_use * 900 + hint_use * 900 + remove_use * 1300 + remove1_use * 500
```

这些系数（900/900/900/1300/500）是道具的单价。如果游戏内价格有调整，系数需同步更新。建议在 SQL 注释中标注来源。

### 12. `"leve_mode"` 拼写

代码中字段名确实是 `"leve_mode"`（少一个 `l`），SQL 与代码一致，不是 bug。但属于源头 typo，长期建议修正。

---

## 修复优先级总览

| 优先级 | 编号 | 问题 | 影响范围 |
|--------|------|------|---------|
| 🔴 P0 | #1 | 保底胜利(levelend=6)遗漏 | 所有通关/难度指标 |
| 🔴 P0 | #2 | lv_id 字符串排序 | 关间流失率、结果排序 |
| 🔴 P1 | #3 | 失败平均用时分母错误 | 失败用时指标 |
| 🔴 P1 | #4 | 首次失败剩余率分母错误 | 首次失败剩余率 |
| 🟡 P2 | #5 | level_enter_num 需验证 | 首次尝试相关指标 |
| 🟡 P2 | #6 | revive方差计算范围 | 复活方差/标准差 |
| 🟡 P2 | #7 | 缺少NULLIF | 3个指标可能报错 |
| 🟡 P3 | #8 | user_start_cnt 含重玩 | 难度(通关用户平均) |
| 🟢 — | #9-12 | 设计备注 | 可接受/需确认 |

## 关联

- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]] — 返回项目总入口
