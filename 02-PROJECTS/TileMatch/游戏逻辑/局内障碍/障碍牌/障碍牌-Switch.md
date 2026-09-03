---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：Switch 开关（5132/5133）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5132`(H) / `5133`(V) | |
| Group | `Blocker` | |
| MatchCount | `0` | |
| 尺寸 | 2×1 / 1×2 Fixed | |
| 血量 | 1 | |
| CoveredTileIgnoreVisible | `false` | |
| CustomTileController | `SwitchTileController` | |
| Capabilities.CanExposeSequenceMembersToDeadlockHint | `false` | |

## 二、数据层

### 序列结构
- 固定 2 张子牌，分别对应 Index 0 和 Index 1
- 使用 **Blackboard `ActiveIndex`** 追踪当前激活侧（0 或 1）
- `SharedSequenceCount` 同步多开关间的序列计数

### HasSeen 独立性（blockerdda 分支修复）
- 2×1 开关盒的 ActiveIndex 和 HasSeen 需保持独立性
- 使用 Shuffle 后不影响 2×1 开关盒的调控
- DDA 交换时 HasSeen **互换**；洗牌时 **重建**

## 三、逻辑层：10 条 ECA

### ① InitActiveState（`5132001`）Priority=100

| 项目 | 内容 |
|------|------|
| 事件 | `LevelEnterAnimationStepOneFinished` |
| 条件 | `SequenceCount >= 2` |
| 动作 | `SetBlackboard(ActiveIndex=$DefaultActiveIndex)` → **`SetSequenceTileHighlightByIndex(AssignIndex=0, EnableDdaRegulationOnActivation=true)`** → `SyncSharedSequenceCount` |

> **blockerdda 变更**：初始化时新增 `EnableDdaRegulationOnActivation=true`，初始化即追踪调控资格。

### ② MarkFirstHighlight（`5132010`）Priority=200

| 事件 | 条件 | 动作 |
|------|------|------|
| `TileVisibilityChanged` / `LevelEnterAnimationStepOneFinished` | Visible AND NOT HasBeenHighlighted | `SetBlackboard(HasBeenHighlighted=true)` |

### ③ SyncSharedSequenceCountBeforeNormalToggle（`5132009`）Priority=10

| 事件 | 条件 | 动作 |
|------|------|------|
| `AddingToBarByClick` | `SharedSequenceCountChange` AND NOT ActiveIndexTileMissing AND Count>=1 | `SyncSharedSequenceCount` |

> 外部伤害移除非激活位子牌后，在下次拿牌前先同步计数，避免常规切换被误判拦住。

### ④⑤ 正常切换（`5132002` 0→1 / `5132003` 1→0）

| 事件 | 条件 | 动作 |
|------|------|------|
| `AddingToBarByClick`（别牌进 Bar） | HasBeenHighlighted + NOT SharedSequenceCountChange + Count>=1 + ANY(HasTileAtIndex / HasInteractableSwitch / HasInteractableTile>=2) + Visible + NotLocked + ActiveIndex=0(或1) | `LockSelf` → `SetBlackboard(ActiveIndex=1/0)` → **`SetSequenceTileHighlightByIndex(AssignIndex=1/0, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow, SequenceRegulationEventPolicy=AllEvents)`** |

> **blockerdda 变更**：切换时新增 `SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow` + `SequenceRegulationEventPolicy=AllEvents`，每次切换都参与 DDA 调控。

### ⑥⑦ 子牌取走时切换（`5132004` 0→1 / `5132005` 1→0）

| 事件 | 条件 | 动作 |
|------|------|------|
| `AddingToBarByClick` / `AfterAttack` / `AutoMatchUse` | HasBeenHighlighted + SharedSequenceCountChange + ActiveIndexTileMissing + HasTileAtIndex(目标) + Visible + NotLocked + ActiveIndex=当前 | `LockSelf` → `SetBlackboard` → `SetSequenceTileHighlightByIndex(DdaMode+AllEvents)` → `SyncSharedSequenceCount` |

### ⑧ DestroyWhenEmpty（`5132006`）Priority=90 `Once=true`

| 事件 | 条件 | 动作 |
|------|------|------|
| `AfterAttack` / `AddingToBarByClick` / `AutoMatchUse` | `SharedSequenceCountChange` AND `SequenceCount=0` | `PlayDestroyAnim` → `DestroyTile` |

### ⑨⑩ Fallback 保底切换（`5132007` 1→0 / `5132008` 0→1）Priority=80 StopPolicy=FirstMatchStops

| 事件 | 条件 | 动作 |
|------|------|------|
| 进场/进Bar/自动/道具用完 | HasBeenHighlighted + Visible + Board无交互Tile + Board无锁定Tile + HasTileAtIndex(目标) + ActiveIndex=当前 + Lives>=1 | `SetBlackboard(ActiveIndex=目标)` → `SetSequenceTileHighlightByIndex(AssignIndex=目标)` |

> 死局保底：Switch 自动切换到有子牌的一侧。**注意：保底切换不带 DDA 参数**。

## 四、调控层（blockerdda 分支核心变更）

### Activation DDA 机制
1. **初始化时**（规则①）：`EnableDdaRegulationOnActivation=true` → `InitializeActivationEligibility()` 记录非激活索引
2. **切换时**（规则④⑤⑥⑦）：`SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow` + `AllEvents` → 子牌从 Visible→Highlight 时触发 DDA
3. **资格消费**：`TryConsumeActivationRegulationEligibility()` 消费一次资格后不再重复触发

### HasSeen 机制
- DDA 交换：`ExchangeHasSeenWith()` 互换
- 洗牌：`RebuildHasSeenFromCurrentVisibility()` 重建
- ActiveIndex 和 HasSeen 独立性修复（commit `25876ca`）

## 五、视图层

| 模块 | 职责 |
|------|------|
| `SwitchTileController.cs` | 开关切换动画 + ActiveIndex 驱动 |
| Spine 动画 | 按钮按下/弹起状态切换 |

## 六、可见性 & 选中规则

| 状态 | 规则 |
|------|------|
| 初始 | ActiveIndex 侧高亮可点，另一侧 NotVisible |
| 切换后 | 新激活侧高亮，旧侧 NotVisible |
| 死局保底 | 自动切换到有子牌侧 |
| 序列空 | 销毁容器 |

## 七、关联笔记

- [[障碍牌-Flip]]
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
