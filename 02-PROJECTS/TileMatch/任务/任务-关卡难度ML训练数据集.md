---
title: 任务-关卡难度ML训练数据集
tags: [TileMatch, ML, 训练数据, 关卡难度]
type: task
status: planning
date: 2026-07-24
---

# 关卡难度 ML 训练数据集

> 基于 ta.v_event_48 打点事件表，构建用户×关卡粒度的训练数据集，预测关卡难度与资源消耗。
> **2026-07-24 重构**：原一期方案存在数据泄露，已改为四维特征体系。

## 零、核心原则（铁律）

### 数据泄露红线

> **训练时的特征，必须在预测那一刻也可获取。**

判定标准：用户点击"进入关卡"的瞬间，这条特征能否通过 SQL 查到？

- ✅ 可以 → 安全
- ❌ 不可以（需要等关卡结束后才知道）→ 泄露，禁止入特征

**所有特征只来自两个时间窗口**：
1. 用户 A 在关卡 N **之前**的历史行为
2. **其他用户**在关卡 N 的已发生行为

用户 A 自身在关卡 N 内的任何行为（道具使用、复活、死局、DDA、用时）一律不作为预测特征的来源。这些只出现在 y（预测目标）一侧。

### 决策节奏

- 先逻辑推敲、后数据验证，每步走稳
- 用户提出设想时，评估合理性、标注存疑点，不硬圆
- 特征先全量列出，验证阶段再砍

---

## 一、预测目标（y）

每行 = 用户 A × 关卡 N，预测：

| 方向 | 含义 | 类型 |
|---|---|---|
| 通关概率 | 用户进入一关后是否通关 | 分类（0/1） |
| 通关尝试次数 | 用户需要多少次才能通关 | 回归 |
| 资源消耗 | 钻石/道具消耗（可分关均、最大、分位值） | 回归 |

## 二、数据源

### 事件表

- `ta.v_event_48`：所有打点事件（lv_start / lv_end / lv_revive / add_moves_show / prop_used）
- `ta.v_user_48`：用户属性（ab_group1, ul_user_type, country_code 等）

### 打点代码

- `client/Assets/Game/TileV2/Scripts/UILogic/Data/TaDataManager.cs`
  - `SendLvStartEvent()`：lv_start + lv_start_reconnect（独立构造 dict，不含 card_total）
  - `SendLvEndEvent()`：lv_end / lv_revive（调用 GetLevelEventCommonProperty）
  - `SendLvReviveShowEvent()`：add_moves_show（调用 GetLevelEventCommonProperty）
  - `SendLvPropUseEvent()`：prop_used（调用 GetLevelEventCommonProperty）
  - `GetLevelEventCommonProperty()`：所有关卡事件（除 lv_start）的公共属性，含 card_total / exp_hard 等

### 关键字段语义（已通过代码验证）

| 字段 | 来源 | 含义 |
|---|---|---|
| `e.lv_id` | 玩家关卡序号 | ≠ 关卡 ID，同一 lv_name 可对应多个 e.lv_id |
| `e.lv_name` | 关卡配置文件名 | **聚合键，关卡的正确标识** |
| `e.card_total` | `GetLevelEventCommonProperty` | 在 lv_end / lv_revive / add_moves_show / prop_used 均有值；lv_start 没有 |
| `e.exp_hard` | 打点上报 | **用户实际拿到的期望难度**（可能被活动/付费修正） |
| `e.exp_hard_reason` | 打点上报 | 期望难度被修改的原因 |
| 关卡标称 exp_hard | LevelGroup 关卡表 | **配置文件的默认档位**，本地可能无此字段，待确认 |

### 数据清洗要点

- `lv_name IS NOT NULL`：过滤无效事件
- `lv_name NOT LIKE 'Level_%'`：排除已弃用的 Level_ 前缀关卡
- `e.is_test = false`：排除测试用户
- lv_name 作为唯一聚合键，不使用 e.lv_id

---

## 三、特征体系（四维）

### I. 关卡基础属性（独立于用户）

> 来源：关卡配置文件、打点事件中可获取的字段。新关卡冷启动时可完整获取。

| 子维度 | 特征 | 来源 |
|---|---|---|
| 牌块 | 牌块总数 `card_total` | 打点 `lv_end` 等事件 |
| 花色 | 花色种类数、各花色数量、花色比例 | 需从配置文件提取 |
| 排列结构 | 层级数、各层牌块分布 | 需从配置文件提取 |
| 结构衍生 | 通道数、不可见牌占比、最大深度、被藏牌花色种类 | 需算法计算 |
| 背景 | 背景主题类型 | 配置文件 |
| 难度标称 | 关卡默认 exp_hard | LevelGroup 表（待确认本地可得性） |
| 调控结果 | 用户实际 exp_hard、exp_hard_reason | 打点上报 |
| 测试标记 | 是否测试关（lv_name 含 `_` 后缀） | lv_name 解析 |

### II. 关卡群体画像（来自其他用户）

> 来源：已打过该关卡的其他用户的打点数据。**对每条训练样本，需排除目标用户自身（leave-one-out）。**
> 新关卡冷启动时此维度缺失，需用代理关卡或静态推断代替。

| 维度 | 可造特征 | 统计方式 |
|---|---|---|
| 尝试 | 群体通关率、人均尝试次数、尝试分位值（P50/P90/P99） | AVG / approx_percentile |
| 道具 | 人均道具消耗、关均消耗、最大消耗、分位值 | AVG / MAX / 分位值 |
| 复活 | 人均复活次数、钻石/广告复活占比 | AVG / 比例 |
| 进度 | 人均死局次数、平均失分率、首次失败剩余率 | AVG |
| 用时 | 平均通关用时、平均失败用时 | AVG |
| DDA | 关卡 DDA 触发率、首次失败 DDA 率 | AVG |
| 分层画像 | 按付费档次/资源量/能力分组的各项指标 | 同上 + GROUP BY 分层维度 |

### III. 用户个体（进入关卡 N 前已知）

> 来源：用户 A 在关卡 N **之前**所有关卡的历史打点数据。

| 维度 | 特征 | 说明 |
|---|---|---|
| ⚡ 当前状态 | 钻石余额、道具库存、累计付费额度 | 快照值，进入关卡 N 时的状态 |
| 🏃 能力 | 历史通关率、通关关卡数、均过关用时 | 全局均值 |
| 💰 习惯 | 均道具消耗、复活频率、付费次数、付费金额 | 全局均值 |
| 🎯 条件化 | 在 exp_hard=X 下的通过率 | 按难度档位分层统计 |
| | 在当前资源区间下的通过率 | 按钻石/道具量分层统计 |
| 📈 趋势 | 最近 N 关通关率 vs 全局通关率 | 判断状态上升/下降 |

> ⚠️ "能力"不作为人造特征（如"菜鸟/高手"标签），由模型从交互中学习隐式表征。但条件化的历史统计仍直接作为特征。

### IV. 环境特征（活动/版本/时间）

| 特征 | 说明 |
|---|---|
| 活动阶段 | 是否在活动期内（可能影响道具获取和付费意愿） |
| 版本号 | 不同版本关卡可能调整 |
| 时段 | 周末/假期 vs 工作日 |
| AB 分组 | ab_group1 等用户分群 |

> 环境特征可能在大样本下影响减弱，先全量纳入，验证阶段再筛。

---

## 四、应用场景

| 场景 | 可用特征 | 说明 |
|---|---|---|
| 已有关卡预测 | I + II + III + IV 齐全 | 全维度可获取 |
| 新关卡冷启动 | I + III + IV（II 缺失） | 用代理关或两阶段模型 |
| 关卡参数推演 | 仅 I | what-if：调整牌块数/exp_hard 的影响 |
| 特定用户预测 | III + (I+II+IV) | 个性化通关概率 |

---

## 五、分步计划

| 期数 | 内容 | 状态 |
|---|---|---|
| 一期 | **数据泄露逻辑确认 + 四维特征体系的 SQL 实现**（user×level 宽表） | ✅ SQL 框架完成，待细调 |
| 二期 | 特征工程：关卡配置文件静态特征（花色/排列/深度）+ 衍生指标 | ✅ 提取脚本完成，待运行 |
| 三期 | 模型训练与特征筛选（验证哪些特征有效） | ✅ 方案文档完成 |
| 四期 | 新关卡冷启动方案（代理关 / 两阶段模型） | 待规划 |

### 产出文件

- `SQL_ML训练宽表_step1.sql` — 完整训练宽表 SQL（base_events + y + 四维特征）
- `local_py_script\extract_level_features.py` — 关卡配置文件静态特征提取脚本
- `level_static_features.csv` — 提取后的关卡特征表（跑脚本生成）
- `打点\报告-关卡难度ML训练管线_Phase3.md` — 模型训练与特征筛选方案

---

## 六、参考文件

- `D:\LibraryG\02-PROJECTS\TileMatch\打点\关卡数据报表_难度指标拓展版(lv_name).sql` — 关卡级聚合 SQL，部分逻辑可复用
- `D:\LibraryG\02-PROJECTS\TileMatch\打点\报告-Tile打点事件梳理_2026-06-08.md` — 打点事件完整清单
- `D:\meatloaf_client01\client\Assets\Game\TileV2\Scripts\UILogic\Data\TaDataManager.cs` — 打点代码实现
- [[_MOC|TileMatch 知识库 MOC]]
