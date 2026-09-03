---
tags: [TileMatch, 游戏逻辑, 障碍牌, 分支排查]
status: draft
date: 2026-07-15
type: reference
---

# 分支 tile/tile_blockerdda 障碍牌调控逻辑变更排查

> 排查范围：HEAD~15..HEAD，共 15 个 commit
> 分支主题：障碍牌序列容器的 DDA 调控逻辑重构

---

## 一、变更总览

| 变更类型 | 文件数 | 核心改动 |
|---------|--------|---------|
| C# 逻辑层 | 12 个 | 序列约束精简 + 调控服务扩展 + HasSeen 重构 |
| JSON 配置层 | 7 个 | 新增调控参数 + Curtain DDA 延迟机制 |
| 关卡数据 | 100+ | 关卡占位/暂存（非逻辑变更） |

---

## 二、核心变更逐项分析

### 1. SequenceConstraintHelper — 大幅精简（-145 行）

**文件**: `Services/SequenceConstraints/SequenceConstraintHelper.cs`

| 变更 | 之前 | 之后 |
|------|------|------|
| Profile 系统 | `SequenceConstraintProfile` 结构体 + 5 种 TileType 映射 | **完全删除** |
| 花色去重 | Flip / JokerFlip / CardBox / SuitCase 均 Prefer | **仅保留 Flip** |
| DDA 保护 | `IsProtectedFromDDA()` 阻止 A 类容器子牌参与 DDA | **删除，序列子牌可参与 DDA** |
| `CanTileJoinDDA` | 检查 `IsProtectedFromDDA` | 直接返回 `true`（不再阻止） |

**影响**：CardBox / SuitCase / JokerFlip 的序列子牌不再受花色去重保护，也不再被 DDA 排除。

---

### 2. SequenceRegulationService — 大幅扩展（+150 行）

**文件**: `Services/SequenceRegulationService.cs`

#### 新增能力

| 方法 | 作用 |
|------|------|
| `TryRegulateVisibleReveal()` | 替代原来的 `CollectVisibleDdaTargets` + `Board.InvokeLevelDDAInOrder`，统一入口 |
| `TryRegulateNextHiddenBeforeEject()` | **新增**：在弹出子牌前预调控隐藏的序列 Tile |
| `TryRegulateHiddenBeforeEject()` | **新增**：针对特定 Tile 的隐藏预调控 |
| `InitializeActivationEligibility()` | **新增**：初始化激活调控资格追踪（Switch 用） |
| `ExecuteRegulationStep()` | 统一执行 DDA 调控步骤（含 try/finally 保护） |

#### 新增配置字段

```csharp
SequenceRegulationConfig 新增:
  EnableDdaRegulationOnActivation  // Visible→Highlight 变化时触发 DDA
```

#### Activation 调控机制

> 当序列子牌从 Visible 变为 Highlight（被"激活"）时，触发 DDA 调控。
> 通过 `_activationEligibleIndicesBySequence` 字典追踪哪些索引有资格触发。

---

### 3. SequenceActions — 删除两个 Helper 类（-180 行）

**文件**: `Behaviours/Action/Implementation/SequenceActions.cs`

| 删除 | 替代 |
|------|------|
| `SequenceActionRegulationHelper` | → `SequenceRegulationService.TryRegulateVisibleReveal()` |
| `SequenceHiddenTileRegulationHelper` | → `SequenceRegulationService.TryRegulateNextHiddenBeforeEject()` |
| `TryGetActiveIndex()` 私有方法 | → `SequenceDisplayService.CreateDisplayConfig()` 统一解析 |

---

### 4. HasSeen 机制重构

#### TileData.cs

| 之前 | 之后 |
|------|------|
| `SetHasSeen(bool)` | `MarkSeen()` + `ExchangeHasSeenWith(other)` |
| `RefreshSeenFromCurrentVisibility()` | `RebuildHasSeenFromCurrentVisibility()` |

#### TileService.cs — 新增 `TileExchangeHasSeenMode` 枚举

```csharp
public enum TileExchangeHasSeenMode
{
    Swap,                        // DDA 交换：HasSeen 跟着 Tile 走
    RebuildFromCurrentVisibility  // 洗牌：交换后按当前可见性重建
}
```

| 调用方 | 模式 | 含义 |
|--------|------|------|
| `InLevelDDAV1Strategy` | `Swap` | DDA 交换时 HasSeen 互换（保持调控状态） |
| `InLevelDDAV2Strategy` | `Swap` | 同上 |
| `ShuffleProp` | `RebuildFromCurrentVisibility` | 洗牌后按新位置可见性重建 HasSeen |

**之前**：洗牌和 DDA 交换后都调用 `RefreshHasSeen()` → 按当前可见性刷新。
**之后**：DDA 交换时 HasSeen 互换（不丢失调控标记），洗牌时重建。

---

### 5. ActionConfig — 统一显示配置接口

**文件**: `Config/Behaviours/Action/ActionConfig.cs`

所有序列相关 ActionConfig 新增 `ISequenceDisplayConfigProvider` 接口：

| ActionConfig | 新增字段 |
|-------------|---------|
| `UpdateSequenceStateActionConfig` | `EnableDdaRegulationOnActivation` |
| `RefreshSequenceStateActionConfig` | `EnableDdaRegulationOnActivation` |
| `TransformSequenceActionConfig` | （接口实现，无新字段） |
| `SetSequenceTileHighlightByIndexActionConfig` | `EnableDdaRegulationOnActivation` + `SequenceVisibleDdaMode` + `SequenceRegulationEventPolicy` |

新结构体 `SequenceDisplayDefinition` + 接口 `ISequenceDisplayConfigProvider` 统一了解析逻辑。

---

### 6. SequenceDisplayService — 工厂方法 + 可见性提取

| 变更 | 说明 |
|------|------|
| `CreateDisplayConfig()` | **新增**：统一从 ISequenceDisplayConfigProvider 创建显示配置 |
| `ApplyTileVisibility()` | **新增**：提取 TileData + EffectData 可见性设置 |
| `ResolveActiveIndex()` | **新增**：从 SharedBag 解析 ActiveIndex |
| `ApplyInitialSequenceDisplayFromTileConfigs()` | **删除**：不再提前初始化序列显示 |
| `SequenceTileDisplayChange` | 新增 `SequenceId` 字段 |

---

### 7. Board.cs — DDA 调用安全加固

```csharp
// 之前：无 try/finally 保护
dda.OnStepBegin();
dda.UpdateComplexity();
dda.TryExchangeTile(target);
dda.OnStepEnd();

// 之后：try/finally 确保 OnStepEnd 总会执行
try {
    dda.OnStepBegin();
    dda.UpdateComplexity();
    dda.TryExchangeTile(target);
} finally {
    dda.OnStepEnd();
}
```

---

### 8. EventType.cs — 新增事件

```csharp
AddingToBarByClickStateUpdate  // 收集栏内部阶段
```

---

## 三、JSON 配置变更

### Curtain（帷幕）

| Behaviour | 变更 |
|-----------|------|
| `50003` (Open) | 事件 `AddingToBarByClick` → `AddingToBarByClickStateUpdate`；新增 `VisibilityState=4` 条件；移除内联 `HandleCoveredTileReveal`；新增 `SetBlackboard("CurtainRevealDdaPending","Pending")` |
| `50004` (Close) | 同上事件变更 + VisibilityState 条件；新增 `SetBlackboard("CurtainRevealDdaPending","None")` |
| `50009` **(新增)** | `RegulateCoveredTileAfterAddingToBarByClick`：当 DdaPending=Pending 且遮挡已关闭时，执行 `HandleCoveredTileReveal(TryDdaRegulation=true)` |

> **Curtain DDA 延迟机制**：开/闭状态切换 → 标记 Pending → AddingToBarByClick 事件时统一执行 DDA 调控

### CardBox（卡盒）

```json
"EnableDdaRegulationOnActivation": true  // 打开后子牌 Visible→Highlight 时触发 DDA
```

### SlotMachine（老虎机）

```json
"FirstNHighlightTailVisibility": "NotVisible"  // 非高亮子牌设为不可见
```

### SuitCase（行李箱）

```json
"EnableDdaRegulationOnActivation": true  // 脱盖后子牌激活时触发 DDA
```

### Switch（开关）

| Behaviour | 变更 |
|-----------|------|
| 初始化 (`5132001`) | 新增 `EnableDdaRegulationOnActivation: true` |
| 切换规则 (6 条) | 新增 `SequenceVisibleDdaMode: "VisibleOrEnterDisplayWindow"` + `SequenceRegulationEventPolicy: "AllEvents"` |

> Switch 现在在切换激活索引时也参与 DDA 调控。

### Mystery / Pig

- Mystery.json：+1 行（具体内容需查看）
- Pig1/2/3.json：各 +1 行（具体内容需查看）

---

## 四、各障碍调控逻辑变更总结

| 障碍 | 调控变更 | 影响 |
|------|---------|------|
| **Flip** | 花色去重保留，DDA 保护移除 | 子牌可参与 DDA 交换 |
| **JokerFlip** | 花色去重移除，DDA 保护移除 | 子牌完全参与 DDA |
| **CardBox** | 新增 Activation DDA | 打开后子牌激活即触发调控 |
| **SuitCase** | 新增 Activation DDA | 脱盖后子牌激活即触发调控 |
| **SlotMachine** | 非高亮子牌设为 NotVisible | 摇牌后隐藏非高亮子牌 |
| **Switch** | 切换时触发 DDA + 初始化时追踪资格 | 每次切换都有调控机会 |
| **Curtain** | DDA 延迟到 AddingToBarByClick 执行 | 避免开/闭切换时立即调控 |
| **所有序列容器** | HasSeen 机制重构 | DDA 交换时 HasSeen 互换，洗牌时重建 |

---

## 五、修复类提交

| Commit | 修复内容 |
|--------|---------|
| `432f9ae` | 遮挡多个开关盒变 Highlight 后没同时切换状态 |
| `b6a54cf` | 老虎机第二张 Tile 点不动，unlock 后刷新 Clickable |
| `684fb73` | 老虎机白板问题（TileView 修复） |
| `1d1fe0a` / `7dea707` | 盲盒牌闪烁问题（Mystery EffectView） |
| `25876ca` | 2×1 开关盒 ActiveIndex 和 HasSeen 独立性 + 序列上锁/解锁时机整理 |
| `dbad081` | 开关盒 Visible 状态下切换状态修复 |
| `ad3ffce` | 统一 Sequence 类 Tile 初始化时机 |
| `5d031da` | 多次点击饼干位置偏移修复 |

---

## 六、知识库笔记需更新的要点

| Obsidian 笔记 | 需补充内容 |
|-------------|-----------|
| `障碍牌-翻转系列.md` | Flip DDA 保护移除、JokerFlip 花色去重移除 |
| `障碍牌-容器系列.md` | CardBox/SuitCase 新增 Activation DDA、SlotMachine 新增 TailVisibility |
| `障碍牌-类型全览.md` | 序列约束从 A/B 两类简化为仅 Flip |
| `Effect/Effect-Cirrus.md` (含 Curtain) | Curtain DDA 延迟机制 + 新事件 |
| `分析-障碍Tile生成与序列逻辑-v1.md` | A/B 类容器区分已失效，需更新 |

---

## 关联

- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]]
