---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：SlotMachine 老虎机（5050）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5050` | |
| Group | `Blocker` | |
| MatchCount | `0` | |
| 尺寸 | 2×1 Fixed | |
| 血量 | 1 | |
| CoveredTileIgnoreVisible | `true` | |
| CustomTileController | `SlotMachineTileController` | |
| SequenceDepthMode | `1` | 与其他容器不同 |

## 二、数据层

### 花色去重（blockerdda 变更）
- **之前**：无去重约束（B 类容器）
- **之后**：无变化（本来就是 None）

### HasSeen 机制
| 场景 | 之后 |
|------|------|
| DDA 交换 | Swap 互换 |
| 洗牌 | Rebuild 重建 |

## 三、逻辑层：6 条 ECA（当前分支最新）

### ① UpdateSequenceState（`5050001`）— 进场初始化

| 事件 | 条件 | 动作 |
|------|------|------|
| `LevelEnterAnimationStepOneFinished` | `SequenceCount >= 1` | `UpdateSequenceState(FirstNHighlight, Count=1, **FirstNHighlightTailVisibility=NotVisible**)` |

> **blockerdda 变更**：新增 `FirstNHighlightTailVisibility=NotVisible`。非高亮子牌设为不可见（之前默认 Visible）。

### ② ShuffleOnMatch（`5050002`）— 消除后摇牌

| 事件 | 条件 | 动作 |
|------|------|------|
| `Attack` | Count>=1 AND DamageSourceType=8(Match) AND Visible AND NotLocked | `LockSelf(Common)` → `TransformSequence(Shuffle, FirstNHighlight, Count=1, **TailVisibility=NotVisible**, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow)` |

> **blockerdda 变更**：新增 `FirstNHighlightTailVisibility=NotVisible`。

### ③ UpdateSequenceOnTake（`5050004`）— 取牌后摇牌（高亮状态）

| 事件 | 条件 | 动作 |
|------|------|------|
| `AddingToBarByClick` / `AfterAttack` / `AutoMatchUse` | SequenceCountChange AND Count>=1 AND NotLocked AND Visible | `LockSelf` → `TransformSequence(Shuffle, FirstNHighlight, Count=1, **TailVisibility=NotVisible**, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow)` |

### ④ ShuffleOnTake（`5050003`）— 取牌后刷新（非高亮状态）

| 事件 | 条件 | 动作 |
|------|------|------|
| 同③ | 同③ BUT NOT Visible | `UpdateSequenceState(FirstNHighlight, Count=1, **TailVisibility=NotVisible**)` |

### ⑤ DestroyWhenEmpty（`5050005`）`Once=true`

| 事件 | 条件 | 动作 |
|------|------|------|
| `AddingToBarByClick` / `AfterAttack` / `AutoMatchUse` | `SequenceCount=0` | `PlayDestroyAnim` → `DestroyTile` |

### ⑥ DestroyWhenSequenceTileDestroyed（`5050006`）`Once=true`

| 事件 | 条件 | 动作 |
|------|------|------|
| `AfterAttack` | `SequenceCount=0` | `PlayDestroyAnim` → `DestroyTile` |

## 四、调控层

### 可见性 DDA
- 规则 ②③ 设置 `SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow`
- 摇牌后新子牌变为 Highlight 时触发 DDA

### TailVisibility 变更影响
- **之前**：非高亮子牌为 Visible（玩家可以看到但不可点）
- **之后**：非高亮子牌为 NotVisible（完全隐藏，增加随机性）

### 修复记录
- `b6a54cf`：修复老虎机第二张 Tile 点不动，unlock 后重新刷新 Clickable
- `684fb73`：修复老虎机白板问题（TileView）

## 五、视图层

| 模块 | 职责 |
|------|------|
| `SlotMachineTileController.cs` | 老虎机控制 |
| `SlotMachineTransformSequenceViewAction.cs` | 摇牌动画（blockerdda 重构） |
| `SlotMachineTileView.cs` | 视图（修复 Clickable 刷新） |

## 六、可见性 & 选中规则

| 状态 | 子牌可见性 | 可交互 |
|------|-----------|--------|
| 进场 | FirstNHighlight(1) + Tail=NotVisible | 仅高亮子牌可点 |
| 摇牌后 | 新子牌高亮，旧子牌 NotVisible | 同上 |
| 非高亮状态 | FirstNHighlight(1) + Tail=NotVisible | 仅刷新不摇 |
| 序列空 | 销毁 | — |

## 七、关联笔记

- [[障碍牌-CardBox]]
- [[障碍牌-SuitCase]]
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
