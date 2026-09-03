---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：Flip 翻牌（5110）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5110` | |
| Group | `Blocker` | |
| MatchCount | `0` | 不可点击匹配 |
| 尺寸 | 1×1 Fixed | |
| 血量 | 1 | `Life: {"0": 1}` |
| CoveredTileIgnoreVisible | `false` | 子牌不覆盖可见性 |
| CustomTileController | `FlipTileController` | |
| SequenceDepthMode | `0` | 子牌渲染在 Tile 下方 |
| Capabilities.CanExposeSequenceMembersToDeadlockHint | `false` | 子牌不参与死局提示 |

## 二、数据层

### 序列配置
- 关卡 JSON 中通过 `SequenceCount` 或 `Sequences` 配置子牌
- 运行时动态追加子牌到 `LevelConfig.Tiles`，与容器共享 Position
- 子牌 `SequenceSource` 指向父级索引，`SequenceId` = 父 TileData.Id

### 花色去重（blockerdda 分支变更）

| 阶段 | 之前 | 之后（当前分支） |
|------|------|----------------|
| 初始分配 | Prefer 去重 | **Prefer 去重（保留）** |
| 洗牌 | Prefer 去重 | **Prefer 去重（保留）** |
| DDA 保护 | `ProtectSequenceChildrenFromDda=true` | **移除，子牌可参与 DDA** |

> Flip 是唯一保留花色去重约束的序列容器。JokerFlip/CardBox/SuitCase 的去重均已移除。

### HasSeen 机制（blockerdda 分支变更）

| 场景 | 之前 | 之后 |
|------|------|------|
| DDA 交换 | `RefreshSeenFromCurrentVisibility()` 按可见性刷新 | `ExchangeHasSeenWith()` **HasSeen 互换** |
| 洗牌 | 同上 | `RebuildHasSeenFromCurrentVisibility()` **按新位置重建** |

## 三、逻辑层：ECA 行为引擎（6 条规则）

### ① UpdateSequenceState（`5110001`）— 进场初始化

| 项目 | 内容 |
|------|------|
| 事件 | `LevelEnterAnimationStepOneFinished` |
| 条件 | `SequenceCount >= 1` |
| 动作 | `UpdateSequenceState(FirstNHighlight, Count=1, TailVisibility=NotVisible)` |

> 进场后高亮第 1 张子牌，其余设为 NotVisible。

### ② OnOtherTileClicked（`5110002`）— 别牌进 Bar 时翻转

| 项目 | 内容 |
|------|------|
| 事件 | `AddingToBarByClick` |
| 条件 | NOT SequenceCountChange AND Count>=2 AND Visible AND NotLocked AND Blackboard("HasBeenHighlighted"="true") |
| 动作 | `LockSelf` → `TransformSequence(Rotate, FirstNHighlight, Count=1, TailVisibility=NotVisible, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow)` |

> 只有已高亮过的 Flip 才会因别牌进 Bar 而翻转。Rotate = 循环左移 1 位。
> 翻转后触发 `SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow` DDA 调控。

### ③ RemoveFirstSequenceTile（`5110003`）— 取走子牌后轮转

| 项目 | 内容 |
|------|------|
| 事件 | `AfterAttack` / `AddingToBarByClick` / `AutoMatchUse` |
| 条件 | `SequenceCountChange` AND Count>=1 AND NotLocked |
| 动作 | `LockSelf(Common)` → `TransformSequence(Rotate, FirstNHighlight, Count=1, TailVisibility=NotVisible, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow)` |

### ④ SequenceTileClicked_LastCard（`5110004`）`Once=true` — 最后一张销毁

| 项目 | 内容 |
|------|------|
| 事件 | `AddingToBarByClick` / `AfterAttack` / `AutoMatchUse` |
| 条件 | `SequenceCount <= 1` |
| 动作 | `PlayDestroyAnim` → `UpdateSequenceState(FirstNHighlight, Count=1)` → `DestroyTile` |

### ⑤ DestroyWhenSequenceTileDestroyed（`5110005`）`Once=true` — 序列空时销毁

| 项目 | 内容 |
|------|------|
| 事件 | `AfterAttack` |
| 条件 | `SequenceCount = 0` |
| 动作 | `PlayDestroyAnim` → `UpdateSequenceState` → `DestroyTile` |

### ⑥ MarkFirstHighlight（`5110006`）— 标记首次高亮

| 项目 | 内容 |
|------|------|
| 事件 | `TileVisibilityChanged` / `LevelEnterAnimationStepOneFinished` |
| 条件 | `VisibilityState=4` AND NOT Blackboard("HasBeenHighlighted"="true") |
| 动作 | `SetBlackboard(HasBeenHighlighted=true)` |

> Blackboard 标记机制确保第一次高亮后的行为与后续区分（规则 ② 依赖此标记）。

## 四、调控层（blockerdda 分支新增/变更）

### 可见性 DDA 调控
- 翻转（规则 ②③）后设置 `SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow`
- 子牌从 NotVisible 变为 Highlight 且进入显示窗口时，触发 `SequenceRegulationService.TryRegulateVisibleReveal()`
- DDA 交换时 HasSeen **互换**（`TileExchangeHasSeenMode.Swap`），保持调控标记

### DDA 参与资格（变更）
- **之前**：Flip 子牌被 `IsProtectedFromDDA` 阻止参与 DDA
- **之后**：保护移除，`CanTileJoinDDA` 直接返回 true，子牌可被 DDA 交换

### 隐藏预调控
- `CanPreRegulateHiddenSequenceTileBeforeEjectResult` 需在 TileConfig Capabilities 中配置
- Flip 当前未配置此能力

## 五、视图层

| 模块 | 文件 | 职责 |
|------|------|------|
| 控制器 | `FlipTileController.cs` | 翻转动画 + 序列轮转驱动 |
| 视图动作 | `FlipViewAction.cs` | 牌面翻转 Spine 动画 |
| Headless | `View/Headless/Views/Tile/Flip/FlipTileView.cs` | 无渲染版本 |

## 六、可见性 & 选中规则

| 状态 | 规则 |
|------|------|
| 被遮挡 | 不可点击 |
| 可见（VisibilityState=4） | 可点击内部高亮子牌 |
| 子牌高亮 | 可进 Bar |
| 子牌 NotVisible | 不可见不可点 |
| 无子牌后 | 容器自动销毁 |

## 七、关联笔记

- [[障碍牌-类型全览]]
- [[障碍牌-JokerFlip]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
