---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：CardBox 卡盒（5140）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5140` | |
| Group | `Blocker` | |
| MatchCount | `0` | |
| 尺寸 | 1×2 Fixed | |
| 血量 | **6** | `Life: {"0": 6}` |
| **ZeroLifePolicy** | **`StayAlive`** | 0 血仍存活 |
| CoveredTileIgnoreVisible | `true` | |
| CustomTileController | `CardBoxTileController` | |

## 二、数据层

### 花色去重（blockerdda 变更）

| 阶段 | 之前 | 之后 |
|------|------|------|
| 初始分配 | Prefer | **移除** |
| 洗牌 | Prefer | **移除** |
| DDA 保护 | ProtectSequenceChildrenFromDda | **移除** |

### HasSeen 机制

| 场景 | 之前 | 之后 |
|------|------|------|
| DDA 交换 | RefreshSeen | **Swap 互换** |
| 洗牌 | RefreshSeen | **Rebuild 重建** |

## 三、逻辑层：8 条 ECA（当前分支最新）

### ① UpdateSequenceState（`5140001`）— 进场初始化

| 事件 | 条件 | 动作 |
|------|------|------|
| `LevelEnterAnimationStepOneFinished` | `SequenceCount >= 1` | `UpdateSequenceState(FirstNVisible, Count=1)` |

> 闭盒状态：显示第 1 张子牌为 Visible（不可交互）。

### ② HandleAttack_Add（`5140002`）— 承受攻击

| 事件 | 条件 | 动作 |
|------|------|------|
| `Attack` | `DamageSourceType=4`(AddToBar) AND `Lives>=1` | `HandleAttack` |

### ③ OpenWhenLifeZero_Add（`5140003`）`Once=true` — 血量归零标记

| 事件 | 条件 | 动作 |
|------|------|------|
| `Attack` | DamageSourceType=4 AND `Lives<=0` | `SetBlackboard(CardBox_OpenPending=1)` → `UpdateSequenceState(FirstNVisible, Count=1, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow)` |

### ④ OpenAfterAttack_HighlightSequence（`5140007`）`Once=true` — 开盒高亮

| 事件 | 条件 | 动作 |
|------|------|------|
| `AfterAttack` | `Lives<=0` AND Blackboard("CardBox_OpenPending"="1") | **`UpdateSequenceState(FirstNHighlight, Count=1, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow, EnableDdaRegulationOnActivation=true)`** → `SetBlackboard(CardBox_OpenPending=0)` |

> **blockerdda 变更**：新增 `EnableDdaRegulationOnActivation=true`。开盒后子牌从 Visible→Highlight 时触发 DDA 调控。

### ⑤ AutoDestroyWhenNoInteractableTiles_Candidate（`5140008`）— 死局候选

| 事件 | 条件 | 动作 |
|------|------|------|
| `BlockerGuaranteeCandidateCheck` | Visible + Board无交互Tile + Board无锁定Tile + Lives>=1 | `RegisterBlockerGuaranteeCandidate(GuaranteeKey="Tile.CardBox.AutoDestroyWhenNoInteractableTiles")` |

> **blockerdda 变更**：死局保底改为两阶段——先注册候选，再由 `BlockerGuaranteeSelected` 事件触发执行。

### ⑥ AutoDestroyWhenNoInteractableTiles（`5140004`）`Once=true` — 死局执行

| 事件 | 条件 | 动作 |
|------|------|------|
| `BlockerGuaranteeSelected` | `BlockerGuaranteeKeyEquals("Tile.CardBox.AutoDestroyWhenNoInteractableTiles")` | `ChangeTileLives(-999)` → `UpdateSequenceState(FirstNHighlight, Count=1)` |

### ⑦ RefreshOpenedSequenceOnTakeOrDestroy（`5140005`）— 开盒后刷新

| 事件 | 条件 | 动作 |
|------|------|------|
| `AddingToBarByClick` / `AfterAttack` / `AutoMatchUse` | `Lives<=0` AND `SequenceCountChange` AND Count>=1 | **`UpdateSequenceState(FirstNHighlight, Count=1, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow, EnableDdaRegulationOnActivation=true)`** |

> **blockerdda 变更**：刷新时也带 `EnableDdaRegulationOnActivation`。

### ⑧ DestroyWhenEmpty（`5140006`）`Once=true` — 序列空销毁

| 事件 | 条件 | 动作 |
|------|------|------|
| `AddingToBarByClick` / `AfterAttack` / `AutoMatchUse` | `Lives<=0` AND `SequenceCount=0` | `PlayDestroyAnim` → `DestroyTile` |

## 四、调控层

### Activation DDA（新增）
- 规则 ④⑦ 设置 `EnableDdaRegulationOnActivation=true`
- 子牌从 Visible→Highlight 时触发 `SequenceRegulationService.TryRegulateVisibleReveal()`
- 通过 `InitializeActivationEligibility()` 追踪资格

### 死局保底（重构）
- **之前**：直接在 4 个事件上检查条件并执行
- **之后**：两阶段——`BlockerGuaranteeCandidateCheck` → 注册候选 → `BlockerGuaranteeSelected` → 执行

## 五、视图层

| 血量 | 外观 |
|------|------|
| 6→4 | 完整卡盒 |
| 3→2 | 卡盒磨损 |
| 1→0 | 卡盒打开（Open） |

## 六、可见性 & 选中规则

| 状态 | 子牌可见性 | 可交互 |
|------|-----------|--------|
| 闭盒（Life>0） | FirstNVisible(1) | ❌ |
| 开盒（Life=0） | FirstNHighlight(1) | ✅ |
| 死局保底 | 强制 -999 血 → 开盒 | ✅ |

## 七、关联笔记

- [[障碍牌-SlotMachine]]
- [[障碍牌-SuitCase]]
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
