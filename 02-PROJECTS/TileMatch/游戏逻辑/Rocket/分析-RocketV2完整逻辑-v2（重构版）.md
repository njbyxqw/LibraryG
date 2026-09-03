---
title: 火箭牌 V2 — 完整逻辑文档（重构提交版）
tags:
  - TileMatch
  - Rocket
  - 游戏逻辑
type: analysis
version: v2
status: finalized
date: 2026-06-25
cat_order: 001
---
[[分析-RocketV2技术实现-v1]]
# 火箭牌 V2 — 完整逻辑文档（重构提交版）

> **TileType**: `5000` | **牌组**: Blocker | **配置**: `Rocket.json` | **版本**: V2  
> **最近提交**: `e83f832fe7` — 火箭牌重构 (2026-06-24)  
> **本文档依据**: 最新代码实现 + RocketModify.md 设计文档

---

## 目录

- [一、架构概览](#一架构概览)
- [二、主线一：生成规则](#二主线一生成规则)
- [三、主线二：Lucky Rocket](#三主线二lucky-rocket)
- [四、主线三：Chain Rocket（连锁火箭）](#四主线三chain-rocket连锁火箭)
- [五、Rocket.json 行为定义](#五rocketjson-行为定义)
- [六、数据流总览](#六数据流总览)
- [七、涉及文件清单](#七涉及文件清单)
- [八、配置常量表](#八配置常量表)

---

## 一、架构概览

### 1.1 核心变化

| 维度 | 旧版本 (V1) | 重构版 (V2) |
|------|------------|------------|
| 生成策略 | `RocketNormalStrategy` | `RocketDepthStrategy`（深度分桶） |
| Action 类型 | `PrepareAttack` | `PrepareChainedAttack` |
| TargetFilter 主波 | `Rocket`（Rocket fallback） | `RocketPrimary`（Rocket 与普通同权重） |
| TargetFilter 链式 | 无独立 filter | `RocketChain`（优先普通，降级火箭） |
| Lucky Rocket | 独立 TileType | 概率强化效果（无独立牌型） |
| 链式传播 | 1 层（旧 ChainController） | 最多 2 层（逻辑层预计算） |
| 录像兼容 | 无 Lucky 数据 | `0xDC` marker 标记概率 |
| Condition | 无 | `DirectTileDestroyedAttackNotSuppressed` |

### 1.2 ECA 架构约束

```
逻辑层（Logic） → 产出 DTO → View 层只播放表现
     ↓                          ↑
  不引用 View/Transform         不选目标/不判定Lucky/不计算传播层
```

---

## 二、主线一：生成规则

### 2.1 开启条件（不变）

`LevelRocketTypeInit.ShouldInvoke()`:

1. `GameMode != Bonus`
2. `LevelConfig.LevelExcelInfo.RocketOpen == true`
3. `isCanShowRocket == true`  
   （正式模式：功能锁解锁 + 关卡≥解锁等级 + 累计胜利≥10 关）

### 2.2 策略选择

`LevelRocketTypeInit` 支持两种策略枚举：

```csharp
enum RocketStrategyType
{
    Normal = 1,  // 旧策略（保留兼容）
    Depth = 2,   // 新策略（重构使用）
}
```

当前 `Depth` 策略生效，`Normal` 保留作为兼容降级。

### 2.3 候选牌判定（IsNormalCandidate）

| 条件 | 说明 |
|------|------|
| `FromRandom == true` | 必须是随机分配牌 |
| 排除 `TileType.Rocket` | 不把已有 Rocket 当候选 |
| 排除 `TileType.Golden` | 金罐牌不转换 |
| 排除 `TileType.CandyBottle` | 糖果瓶不转换 |
| 排除 `TileGroup.Blocker` | Blocker 组不转换（含 Volcano/Butterfly 等） |
| 排除 `TileGroup.Collectable` | Collectable 组不转换 |

### 2.4 生成数量

```
火箭组数 = base(3) + (普通牌组数 - 25) / 5
```

| 普通牌组数 | 火箭组数 | 火箭张数 |
|-----------|---------|---------|
| ≤25 | 3 | 9 |
| 26~29 | 3 (有余数截断) | 9 |
| 30 | 4 | 12 |
| 35 | 5 | 15 |
| 40 | 6 | 18 |

> **注意**：与早期 PRD 中 `min=4` 的设定不同，实装代码 `base = 3`。这是重构已提交的实际实现。

额外逻辑：
- 若已有火箭数不是 3 的倍数，跳过本次生成（保护机制）
- `addRocketGroupCount = targetRocketGroupCount - currentRocketGroupCount`
- `addRocketGroupCount <= 0` 时跳过（已达标则不再多生成）

### 2.5 深度计算（核心新增）

`RocketDepthStrategy` 使用批量深度计算 API：

```
TileDepthComputer.ComputeTileDepths(Board, candidates)
  → Dictionary<long, int>  tileId → depth
```

深度定义：`1 + 压住该牌的块数」，depth 越大表示牌越深（底层）。

排序规则：
1. Depth 升序（浅层优先）
2. Z 升序（Position.z 越小越浅）
3. Tile.Id 升序（稳定排序）

### 2.6 深度分桶

```
前 30%  → 浅层区 (bucket[0])   — 优先分配
30%-60% → 中层区 (bucket[1])   — 次优先分配
> 60%   → 深层区 (bucket[2])   — 不主动分配
```

### 2.7 分布规则

| 连胜状态 | 浅层区 (前30%) | 中层区 (30%-60%) | 深层区 (>60%) |
|---------|---------------|-----------------|--------------|
| ≤ 2 连胜 | 分配 2 组 | 分配剩余组 | 不分配 |
| > 2 连胜 | 分配 1 组 | 分配剩余组 | 不分配 |

- 如果分桶不足（某区牌数不够组成完整组），从后续桶顺延补足
- 始终优先保证总火箭组数达标

### 2.8 Highlight 全火箭兜底

生成完成后检查 Highlight 可见区是否全是 Rocket（`EntityVisibility.Highlight`）：
- 如果是，从已选火箭组中找到属于 Highlight 区的第一组
- 将这组恢复为原始牌型
- 从未选中的候选牌中重新选 3 张同花色转换为火箭（必须是非 Highlight 牌）
- 保证 Highlight 区不会全是火箭

### 2.9 选牌型策略

当前 `RocketDepthStrategy` 不再使用旧版 `GetTileIdList()`（选第二多花色）：
- 改为 `CollectGroupsFromBucket`，在每个深度分区内按 TileType 分组
- 随机选取有 ≥3 张同花色的候选组
- 从该花色中随机选 3 张转换为火箭

---

## 三、主线二：Lucky Rocket

### 3.1 核心设计

Lucky Rocket **不是一张独立的牌**，而是火箭匹配消除时触发的概率强化效果。

```
3 张火箭入栏匹配 → BarMatched
  → PrepareChainedAttackAction.Execute()
    → IsLuckyRocket() 概率判定
      → 成功: PrimaryMaxTarget = 6 + 3 = 9（多打1组）
      → 失败: PrimaryMaxTarget = 6
```

### 3.2 概率来源

概率基于火箭解锁后的**累计胜场**（跨局累计）：

```
rocketOpenWinTimesAtLevelStart = LevelRocketOpenWinTimes
expectedRocketWinTimes = rocketOpenWinTimesAtLevelStart + 1
```

| expectedRocketWinTimes | Lucky 概率 |
|----------------------|-----------|
| ≤ 10 | 0% |
| 11 | 15% |
| 12 | 30% |
| 13 | 50% |
| 14 | 70% |
| ≥ 15 | 100% |

### 3.3 全链路传递

```
LevelRocketData.GetRocketLuckyProbability()
  → ITileMatchProxy.GetRocketLuckyProbability() / Proxy
    → TileMatchV2Proxy.GetRocketLuckyProbability()
      → TileMatchRecordController.SetDataBridgeInfo()
        → DataBridge.RocketLuckyProbability（局内存储）
          → PrepareChainedAttackAction.IsLuckyRocket()
            └─ ctx.RandomService.Range(0, 100) < probability
```

### 3.4 判定规则

- **时机**：每次 Bar 内 Rocket 三消时独立判定
- **位置**：`PrepareChainedAttackAction` 逻辑层
- **随机源**：`ctx.RandomService`（可回放）
- **局内固定**：进关前确定概率，局内不变化
- **Trial/Bot/Editor 模式**：从 `CustomData.RocketLuckyProbability` 进入，默认 0

### 3.5 链式波与 Lucky

| 规则 | 说明 |
|------|------|
| 链式波判定 | **不判定** Lucky |
| 链式波表现 | 不播放 Lucky 特效 |
| Lucky 影响范围 | 只影响主波目标数（9 vs 6），链式波不受影响 |

---

## 四、主线三：Chain Rocket（连锁火箭）

### 4.1 整体架构

所有波次在 `PrepareChainedAttackAction` 内**一次性预计算**（逻辑层），然后通过 DTO 分发给 View 层播放。

```
PrepareChainedAttackAction.Execute()
  ├─ IsLuckyRocket() → 确定主波目标数
  ├─ CreateWave(主波) → WaveIndex=0, 用 RocketPrimaryTargetFilter
  ├─ AppendChainWaves() → 从主波命中Rocket生成链式波
  │   └─ 递归处理每波，直到 maxChainWave 上限
  └─ enqueue(ActionResult) → 整个链式攻击计划一次性提交
```

### 4.2 核心 DTO

```csharp
ChainedAttackActionData
├── Data           // 匹配源 TileData
├── Match          // 匹配信息
├── IsLucky        // Lucky 标记
└── Waves[]        // 攻击波次列表
     ├── Wave[0] —— 主波, IsChainWave=false
     ├── Wave[1] —— 第一链式波, IsChainWave=true
     └── Wave[2] —— 第二链式波, IsChainWave=true

AttackWaveData
├── SourceTile     // 发射源 Tile
├── SourceTiles[]  // 发射源列表（链式波多个源）
├── WaveIndex      // 波次索引
├── IsChainWave    // 是否链式波
└── Targets[]      // 目标列表

AttackTargetData
├── Tile             // 目标 Tile
├── LaunchSourceTile // 该目标对应的发射源
└── DestroyContext   // 销毁上下文（链式命中Rocket时含 SuppressDirectTileDestroyedAttack）
```

### 4.3 主波（Wave 0）

| 参数 | 值 |
|------|-----|
| Filter | `RocketPrimaryTargetFilter` |
| 目标数 | Lucky 成功时 9，否则 6 |
| 权重 | Rocket 与普通 Tile 同权重（不再 fallback） |

**`RocketPrimaryTargetFilter`** 规则（继承自 `RocketCustomTargetFilterV2`）：

| 规则 | 说明 |
|------|------|
| Highlight > bar > overBar 优先级遍历 | 同旧逻辑 |
| 按花色成组选目标 | 每组 3 张 |
| Rocket 可被选中 | `TileGroup.Blocker` 排除但 `TileType.Rocket` 例外通过 |
| 排除 | Golden、CandyBottle、Collectable、Locked、WillDestroy |
| 不足时 | 从其他池补足（含 Rocket 兜底） |

### 4.4 链式波（Wave 1~2）

| 参数 | 值 |
|------|-----|
| Filter | `RocketChainTargetFilter` |
| 最大传播层数 | 2 波（WaveIndex=1, 2） |
| 每波最大目标 | 6 个 |
| 触发条件 | 上一波命中 Rocket ≥ 3 张（每 3 张组成一个源组） |
| 目标偏好 | **优先普通 Tile**，不足时允许选 Rocket |

**`RocketChainTargetFilter`** 规则：

```
Phase 1 (优先): 
  TileGroup == Normal 且 非 Golden/CandyBottle/Rocket
  从 highlight → visible → notVisible → overBar → bar 依次收集
  同一张牌不重复选，支持 eligible 回调去重

Phase 2 (降级):
  只收集 TileType == Rocket（兜底）
```

### 4.5 链式发射源分配

每个链式源组有 3 个被命中的 Rocket 作为发射源。

```csharp
targetsPerSource = ceil(maxTarget / sourceCount)
                  = ceil(6 / 3) = 2
```

- source[0] → target[0], target[1]
- source[1] → target[2], target[3]  
- source[2] → target[4], target[5]

### 4.6 防无限循环机制

| 机制 | 实现 |
|------|------|
| 最大层数 | `maxChainWave=2`（Wave 1~2） |
| 跨层去重 | `selectedTiles` HashSet，避免同一张牌被多次锁定 |
| 末层命中 Rocket | 到达最大层后命中 Rocket 只销毁，不继续传播 |
| 链式命中不触发邻居攻击 | `DestroyContext.SuppressDirectTileDestroyedAttack = true` |

### 4.7 邻居攻击抑制（新 Condition）

新增 `DirectTileDestroyedAttackNotSuppressed` Condition：

```json
{
  "BehaviourId": "5000004",
  "Conditions": [
    { "ConditionType": "StateEquals", "ExpectedState": 1 },
    { "ConditionType": "DirectTileDestroyedAttackNotSuppressed" }
  ],
  "Actions": [
    { "ActionType": "EmitEvent", ... "DamageSourceType": 2 }
  ]
}
```

- 链式命中 Rocket 时，ViewAction 发布 TileDestroyed 事件带 `TileDestroyedEventData.SuppressDirectTileDestroyedAttack = true`
- Condition 检查该标记 → 返回 false → 不触发旧邻居攻击
- 普通 `TileDestroyed` 不传上下文 → Condition 返回 true → 正常触发邻居攻击

### 4.8 Chain Rocket 完整流程示例

```
初始层（Wave 0）：
  A 火箭匹配 → 6枚攻击目标
  └── 命中的目标中包含：
      B 火箭（3张）、C 火箭（2张）

第一链式波（Wave 1）：
  满3张的 B 组触发 → 发射源组 [B1, B2, B3]
  选 6 个目标（优先普通 Tile）
  └── 命中的目标中包含 D 火箭（3张）

第二链式波（Wave 2）：
  D 组触发 → 发射源组 [D1, D2, D3]
  选 6 个目标（优先普通 Tile）
  └── 命中的 Rocket 只销毁，不继续传播

不满足 3 张的 C(2张) 不触发链式波
```

---

## 五、Rocket.json 行为定义

### 5.1 Behaviour 总览

| BehaviourId | 名称 | 事件 | 核心变更 |
|------------|------|------|---------|
| 5000001 | Rocket_TileClicked | TileClicked | 不变 |
| 5000002 | Rocket_BarChanged | BarChanged | 不变 |
| **5000003** | **Rocket_BarMatched** | **BarMatched** | **Action 从 PrepareAttack 改为 PrepareChainedAttack** |
| **5000004** | **Rocket_Attack_When_Direct_TileDestroyed** | TileDestroyed | **新增 DirectTileDestroyedAttackNotSuppressed Condition** |
| 5000005 | Rocket_TileDestroyed | TileDestroyed | 不变 |

### 5.2 BarMatched 配置（核心变更）

```json
// 旧配置
{
  "ActionType": "PrepareAttack",
  "TargetFilter": "Rocket",
  "MaxTarget": 6
}

// 新配置
{
  "ActionType": "PrepareChainedAttack",
  "TargetFilter": "RocketPrimary",    // Rocket 与普通同权重
  "PrimaryMaxTarget": 6,              // 主波基础目标数
  "LuckyExtraTarget": 3,             // Lucky 额外目标数
  "ChainMaxTarget": 6,               // 链式波每波目标数
  "MaxChainWave": 2,                 // 最大链式传播层数
  "ChainTriggerTileType": 5000,      // 链式触发 TileType (Rocket)
  "ChainTargetFilter": "RocketChain" // 链式目标 filter
}
```

### 5.3 TileDestroyed 配置（新增 Condition）

```json
// Behaviour 5000004 — 新增 Condition
{
  "ConditionType": "DirectTileDestroyedAttackNotSuppressed"
}
```

Behaviour 5000005（纯销毁）不增加该 Condition，保证链式命中的 Rocket 仍然正常销毁。

---

## 六、数据流总览

### 6.1 关卡初始化

```
Board.InitializeFromLevelConfig()
  └── LevelRocketTypeInit.ShouldInvoke()
       ├── false → 跳过
       └── true → RocketDepthStrategy（策略类型=Depth）
            ├── GetNormalCandidates()
            │    └── FromRandom && 非Blocker/Collectable/Rocket/Golden/CandyBottle
            ├── GetRocketGroupCount(normalGroupCount)
            │    └── base=3, >25时每多5组+1
            ├── FillCandidateDepths() → TileDepthComputer.ComputeTileDepths()
            ├── SplitByDepthBuckets() → 前30%/30-60%/>60%
            ├── SelectRocketCandidates()
            │    └── 连胜≤2:浅层2组, 连胜>2:浅层1组, 剩余从中层补
            ├── ModifyTiles() → TileService.ModifyTile() × N
            └── EnsureHighlightNotAllRocket()
```

### 6.2 Lucky 概率链路

```
关卡开始前:
  LevelRocketData.GetRocketLuckyProbability()
    → expectedRocketWinTimes = LevelRocketOpenWinTimes + 1
    → 映射到 0/15/30/50/70/100

关卡进入时:
  TileMatchV2Proxy.GetRocketLuckyProbability()
    → TileMatchRecordController → DataBridge.RocketLuckyProbability

录像写入:
  PersistDataBridge → 写入 DataBridge payload
  → 写入 0xDC marker
  → 写入 RocketLuckyProbability

录像读取:
  Load → 读取 DataBridge
  → 检测 0xDC → 读取概率 / 回退1字节默认0
```

### 6.3 游戏内（匹配 → 攻击）

```
3张火箭入栏 → BarMatched → PrepareChainedAttackAction
  ├── IsLuckyRocket() → ctx.RandomService.Range(0,100) < probability
  ├── CreateWave(主波, RocketPrimary, targetCount)
  │    └── RocketPrimaryTargetFilter 选目标（Rocket与普通牌同权重）
  ├── AppendChainWaves()
  │    └── 递归检测每波命中Rocket→每3张生成一条链式波
  │         └── RocketChainTargetFilter 选目标（优先普通）
  └── enqueue(ActionResult)

→ ViewAction.DoAction(ChainedAttackActionData)
  ├── 主波从 Match Rocket 位置发射
  ├── 链式波从缓存Rocket原位置发射
  └── 全部完成后 publish AfterAttack（仅1次）
```

---

## 七、涉及文件清单

### 7.1 新增文件

| 文件 | 职责 |
|------|------|
| `RocketDepthStrategy.cs` | 生成策略：深度分桶 + 数量计算 |
| `RocketPrimaryTargetFilter.cs` | 主波 target filter（Rocket 与普通同权重） |
| `RocketChainTargetFilter.cs` | 链式波 target filter（优先普通，降级火箭） |
| `PrepareChainedAttackAction.cs` | 链式攻击 Action（预计算所有波次） |
| `PrepareChainedAttackActionInvoker.cs` | 新 Action Invoker |
| `DirectTileDestroyedAttackNotSuppressedCondition.cs` | 抑制链式 Rocket 邻居攻击的 Condition |
| `TileDestroyedEventData.cs` | 销毁事件上下文标记 |

### 7.2 修改文件

| 文件 | 变更 |
|------|------|
| `Rocket.json` | BarMatched: PrepareAttack→PrepareChainedAttack；TileDestroyed新增 Condition |
| `ActionType.cs` | 新增 `PrepareChainedAttack` 枚举 |
| `ActionConfig.cs` | 新增 `PrepareChainedAttackActionConfig` |
| `ConditionType.cs` | 新增 `DirectTileDestroyedAttackNotSuppressed` 枚举 |
| `ConditionConfig.cs` | 新增 `DirectTileDestroyedAttackNotSuppressedConditionConfig` |
| `DataBridge.cs` | 新增 `RocketLuckyProbability` 字段 |
| `CustomData.cs` | 新增 `RocketLuckyProbability` 字段 |
| `ITileMatchProxy.cs` | 新增 `GetRocketLuckyProbability()` 接口 |
| `TileMatchV2Proxy.cs` | 实现 `GetRocketLuckyProbability()` |
| `LevelRocketData.cs` | 新增 `GetRocketLuckyProbability()` 概率计算方法 |
| `LevelRocketTypeInit.cs` | 新增 `RocketStrategyType.Depth` + `RocketDepthStrategy` 调用 |
| `TileDepthComputer.cs` | 新增 `ComputeTileDepths()` 批量深度计算 API |
| `TileMatchGameRecord.cs` | 新增 DataBridge 中 RocketLucky 字段持久化 |
| `TileMatchGameRecordBinaryPersister.cs` | 新增 `0xDC` marker 写入 |
| `TileMatchGameRecordBinaryLoader.cs` | 新增 `0xDC` marker 读取 |
| `RocketCustomTargetFilterV2.cs` | 基类，virtual 方法供 RocketPrimaryTargetFilter 重写 |

### 7.3 未改动文件

| 文件 | 原因 |
|------|------|
| `TileType.cs` | 不需要新枚举值（Lucky 不是独立牌型） |
| `RocketTileView.cs` | 牌面不变 |
| `Board.cs` | 初始化入口流程不变 |
| `ResourceLoadService.cs` | 不需要新资源路径 |

---

## 八、配置常量表

### 8.1 Rocket.json 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `PrimaryMaxTarget` | 6 | 主波基础目标数 |
| `LuckyExtraTarget` | 3 | Lucky 额外目标数（6+3=9） |
| `ChainMaxTarget` | 6 | 链式波每波最大目标数 |
| `MaxChainWave` | 2 | 最大链式传播层数（Wave 1~2） |
| `ChainTriggerTileType` | 5000 (Rocket) | 触发链式的 TileType |
| `ChainTargetFilter` | `RocketChain` | 链式目标 filter 名称 |

### 8.2 Lucky 概率常量

| 条件 | 概率值 |
|------|-------|
| expectedRocketWinTimes ≤ 10 | 0% |
| = 11 | 15% |
| = 12 | 30% |
| = 13 | 50% |
| = 14 | 70% |
| ≥ 15 | 100% |

### 8.3 生成规则常量

| 参数 | 值 | 说明 |
|------|-----|------|
| baseRocketGroupCount | 3 | 基础火箭组数 |
| normalGroupBase | 25 | 普通牌组数基准值 |
| extraGroupStep | 5 | 每多 5 组普通牌 +1 组火箭 |
| shallowRatio | 30% | 浅层区深度比例 |
| middleRatio | 30% | 中层区深度比例 |
| shallowGroupsWinStreakLTE2 | 2 | 连胜≤2时浅层组数 |
| shallowGroupsWinStreakGT2 | 1 | 连胜>2时浅层组数 |

## 关联
- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]]
- [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑分析]]
- [[分析-RocketV2技术实现-v1|RocketV2 技术实现]]
