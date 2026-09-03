---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：Thief 小偷（5160）

## 一、基础属性

| 属性                                                             | 值         | 说明               |
| -------------------------------------------------------------- | --------- | ---------------- |
| TileType                                                       | `5160`    |                  |
| Group                                                          | `Blocker` |                  |
| MatchCount                                                     | `0`       | 不可点击匹配           |
| 尺寸                                                             | 1×1 Fixed |                  |
| 血量                                                             | **1**     | `Life: {"0": 1}` |
| Capabilities.CanExposeVisibleSequenceMembersAsTargets          | `true`    | 子牌暴露后可被选中        |
| Capabilities.CanPreRegulateHiddenSequenceTileBeforeEjectResult | `true`    | 弹出前预调控隐藏序列       |

## 二、数据层

### 序列配置
- 关卡 JSON 中通过 `SequenceCount` 或 `Sequences` 配置子牌
- 运行时动态追加子牌到 `LevelConfig.Tiles`，与容器共享 Position
- 子牌 `SequenceSource` 指向父级索引，`SequenceId` = 父 TileData.Id

### 花色去重
- Thief 是 **B 类容器**，无花色去重约束（序列内可出现同花色子牌）
- blockerdda 分支无变化（本来就是 None）

### HasSeen 机制（blockerdda 变更）

| 场景 | 之前 | 之后 |
|------|------|------|
| DDA 交换 | `RefreshSeenFromCurrentVisibility()` | `ExchangeHasSeenWith()` **Swap 互换** |
| 洗牌 | 同上 | `RebuildHasSeenFromCurrentVisibility()` **Rebuild 重建** |

## 三、逻辑层：6 条 ECA

### ① UpdateSequenceState（`5160001`）— 进场初始化

| 项目 | 内容 |
|------|------|
| 事件 | `LevelEnterAnimationStepOneFinished` |
| 条件 | `SequenceCount >= 1` |
| 动作 | `UpdateSequenceState(FirstNVisible, Count=0)` |

> **Count=0 表示全部**：Thief 进场时将所有子牌设为 Visible（不可交互），用户可以预览序列中有哪些牌。与 Flip（Count=1 只展示第一张）不同。

### ② EjectHeadToOverBarBeforeBarMatch（`5160002`）— Bar 匹配前弹出

| 项目 | 内容 |
|------|------|
| 事件 | `BeforeBarMatch` |
| 条件 | `SequenceCount>=1` AND `VisibilityState=4` AND `NotLocked` |
| 动作 | `EjectSequenceTo(EjectToPosition="OverBar", IgnoreOverBarCapacity=true, LockAllSequenceTilesDuringAction=true, **PreRegulateNextHiddenTile=true**)` |

> **核心机制**：每次 Bar 匹配前，自动弹出序列头牌到弃牌区（OverBar）。无视弃牌区容量限制（`IgnoreOverBarCapacity=true`）。
> 
> **blockerdda 关键新增**：`PreRegulateNextHiddenTile=true` — 弹出头牌后，自动对序列中下一个隐藏 Tile 执行 DDA 预调控（详见 [调控层](#四调控层preRegulate-预调控机制)）。

### ③ Guarantee Candidate（`5160006`）— 保底候选注册

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeCandidateCheck` |
| 条件 | `VisibilityState=4` AND `SequenceCount>=1` AND `BoardHasAtMostInteractableTile(0)` AND `BoardHasAtMostLockedTile(0, Destroy, Highlight)` AND `NotLocked` |
| 动作 | `RegisterBlockerGuaranteeCandidate(GuaranteeKey="Tile.Thief.GuaranteeWhenBoardHasNoAddToBar")` |
| 触发事件 | `LevelEnterAnimationStepOneFinished` / `AddingToBarByClick` / `AutoMatchUse` / `ApplicationPendingEnd` / **`AfterEjectSequenceToOverBar`** |

> **blockerdda 变更**：保底改为两阶段。额外触发事件 `AfterEjectSequenceToOverBar` — 每次弹出后都重新检查保底条件。

### ④ Guarantee Execute（`5160003`） `Once=true` — 保底执行

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeSelected`（TargetSelector=Self） |
| 条件 | `BlockerGuaranteeKeyEquals("Tile.Thief.GuaranteeWhenBoardHasNoAddToBar")` |
| 动作 | `EjectAllSequenceTo(EjectToPosition="OverBar", IgnoreOverBarCapacity=true)` |

> 死局时将所有剩余子牌一次性弹出到弃牌区，避免卡死。

### ⑤ Update After Eject（`5160004`）— 弹出后刷新序列

| 项目 | 内容 |
|------|------|
| 事件 | `AfterEjectSequenceToOverBar` / `AfterTileDestroyed` / `AfterBarMatch` |
| 条件 | `SequenceCount>=1` AND `VisibilityState=4` |
| 动作 | `UpdateSequenceState(FirstNVisible, Count=0)` — 刷新可见性 |

> 每次弹出/销毁/匹配后，刷新序列显示（重新展示剩余子牌）。

### ⑥ DestroyWhenEmpty（`5160005`） `Once=true` — 序列空销毁

| 项目 | 内容 |
|------|------|
| 事件 | `AfterEjectSequenceToOverBar` / `AfterTileDestroyed` |
| 条件 | `SequenceCount=0` AND `VisibilityState=4` |
| 动作 | `PlayDestroyAnim(AutoDestroy=true)` → `DestroyTile` |

> 所有子牌弹出完毕后，容器自动销毁。

## 四、调控层（blockerdda 分支核心变更）

### PreRegulate 预调控机制

> **这是 blockerdda 分支为 Thief/ShellBox 新增的调控能力**，在 blockerdda 报告中被遗漏。

```
EjectSequenceTo (PreRegulateNextHiddenTile=true)
  → SpecialActions.EjectSequenceToAction
    → SequenceRegulationService.TryRegulateNextHiddenBeforeEject()
      → 查找序列中下一个隐藏 Tile
        → TryExecuteHiddenBeforeEject(TileData)
          → DDA 预调控该 Tile
```

| 配置项 | 值 | 位置 |
|------|-----|------|
| `Capabilities.CanPreRegulateHiddenSequenceTileBeforeEjectResult` | `true` | TileConfig 全局能力 |
| `PreRegulateNextHiddenTile` | `true` | EjectSequenceTo Action 参数 |

**触发时机**：每次弹出头牌到 OverBar 时（规则 ②），在 `EjectSequenceTo` 执行后，自动检查序列中是否还有隐藏（NotVisible）的子牌，如有则执行 DDA 预调控。

**调控效果**：下一个隐藏子牌被 DDA 系统提前评估和调整，确保弹出后的游戏状态不会过于简单或困难。

### 保底机制（blockerdda 变更）

- **之前**：直接在事件上检查条件并执行
- **之后**：两阶段——`BlockerGuaranteeCandidateCheck` → 注册候选 → `BlockerGuaranteeSelected` → 执行
- **额外触发事件**：`AfterEjectSequenceToOverBar`（每次弹出后重新检查）

## 五、视图层

| 模块 | 文件 | 职责 |
|------|------|------|
| 控制器 | `ThiefTileController.cs` | 序列管理 + 弹出动画 |

## 六、可见性 & 选中规则

| 状态 | 子牌可见性 | 可交互 |
|------|-----------|--------|
| 被遮挡 | 不可见 | ❌ |
| 可见（VisibilityState=4） | FirstNVisible(全部) | ❌（Visible 不可交互，仅预览） |
| Bar 匹配前 | 头牌弹出到 OverBar | ✅ 弹出的牌可进 Bar |
| 死局保底 | 全部弹出到 OverBar | ✅ |
| 序列空 | 容器自动销毁 | — |

> **与其他序列容器的关键区别**：Thief 的子牌不是点击容器获取，而是在 Bar 匹配事件时**自动弹出**。玩家无法主动控制弹出时机。

## 七、关联笔记

- [[障碍牌-ShellBox]]（共享 PreRegulate 预调控机制）
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
