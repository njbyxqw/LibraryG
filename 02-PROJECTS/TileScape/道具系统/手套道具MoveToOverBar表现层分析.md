---
title: 手套道具 MoveToOverBar 表现层分析
tags: [TileScape, 道具, 表现层, MoveToOverBar, 手套]
type: tech-analysis
status: historical
lifecycle: historical
source: "origin/main ae41b0e；基于 feat-new_movetooverbar_prop 的静态历史审计"
date: 2026-08-10
---

# 手套道具 MoveToOverBar 表现层分析

> 分支 `feat-new_movetooverbar_prop` 手套道具拿牌功能的完整表现层梳理。
> 涵盖 4 条提交（`3b09e8bbb` → `ff53defc7`）的表现层改动、需求对齐、0.1s 停留补丁。

---

## 需求背景

手套道具（MoveToOverBar）的核心表现需求：

1. 道具图标从道具按钮位置**飞砸曲线**砸到目标牌上
2. 图标砸到后**消失**
3. 被选中的牌**提到最上层**（sortingOrder 提升到 100）
4. 选中牌在最上层**短暂停留 0.1s**
5. 停留结束后，选中牌一起**飞到弃牌区**（OverBar）

---

## 提交时间线

| # | Commit | 描述 | 表现层重点 |
|---|--------|------|-----------|
| 1 | `3b09e8bbb` | 手套道具修改初版提交 | 全部表现层文件首次落地 |
| 2 | `5b648e277` | 手套直接触发金牌收集 | 调整 Selection 逻辑，测试契约更新 |
| 3 | `1fbf4db8f` | 新增事件 MoveToOverBarUse 引用 | 25 个 JSON 配置接入事件 |
| 4 | `ff53defc7` | 修复翻转牌 Bug | Flip/JokerFlip 序列牌缩放恢复 |

---

## 表现层分 4 层（12 个 C# 文件 + 33 个 JSON）

### ① UI 表现层（UIGamePanel）— 核心改动 +473 行

| 文件 | 改动量 | 职责 |
|------|--------|------|
| `TileGamePanelPropPresentation.cs` | +345 | 飞行图标创建、弧线动画、选中牌三态快照管理 |
| `TileGamePanelPropUseFlow.cs` | +118 | 流程编排：准备→消耗→表现→执行→提交/回滚 |
| `TileGamePanelPropButton.cs` | +2 | 暴露图标 Sprite 和 Transform |
| `TileGamePanelPropController.cs` | +8 | 暴露图标供飞行动画使用 |

**PropPresentation.cs（核心文件）要点：**

- 新增 `MoveToOverBarPropPresentationConfig` 静态配置：
  - 飞行时长 0.45s、缩放 5x、弧高 0.3、排序 30000
  - 选中牌 sortingOrder = 100
  - **停留时长 0.1s**（补丁新增）
- 新增 `PlayMoveToOverBar` 方法：创建飞行 Icon（Image + Canvas override sorting），从道具按钮位置用 DOTween `DOPath` CatmullRom 弧线飞向目标牌
- 新增 `MoveToOverBarTilePresentationScope` 内部类：管理选中牌的三态快照（排序层级、PresentationMode、背景可见性），支持成功保留 / 失败回滚
- 回调签名 `Action` → `Func<bool>`，表现层需知道执行结果决定提交 / 回滚
- 移除旧的 Remove Spine 动画

### ② View 表现层（GameView + Headless 双实现）

| 文件 | 改动 | 职责 |
|------|------|------|
| `TileMatchViewController.cs` (+17×2) | `RefreshEffectBinding`：手套选牌后重新绑定 Effect→TileView |
| `BoardView.cs` (+11×2) | `KeepDetachedEffectOnBoard`：Effect 中牌全被拿走后空 EffectView 留在棋盘 |
| `OverBarCellView.cs` (×2) | 移除 `allowBeyondDefaultMax` 限制，OverBar 不再受 `_maxStack` 上限约束 |
| `ITileMatchViewController.cs` (+2) | 接口声明 `RefreshEffectBinding` |

### ③ 翻转牌 Bug 修复（ff53defc7）

| 文件 | 改动 | 说明 |
|------|------|------|
| `FlipTileView.cs` (+27) | `RestoreReleasedSequenceTileScale` | 手套拿走翻转牌某一张后，剩余序列牌恢复棋盘完整缩放 |
| `JokerFlipTileView.cs` (+27) | 同上 | Joker 翻转牌同样处理 |

### ④ 配置层（33 个 JSON）

- 25 个 EffectConfig/TileConfig 新增 `MoveToOverBarUse` 事件引用
- 8 个 ShellBox 方向配置新增

---

## 核心设计要点

### 1. 动画方案

从旧的 Spine Remove 动画改为**动态创建飞行图标**（Runtime GameObject + Image + override Canvas），DOTween 三段动画：

```
放大(0→5x, 0.1s) → 弧线飞行(CatmullRom, 0.35s) → 缩小消失(5x→0, 0.1s)
```

### 2. 事务性表现

`Func<bool>` 回调让表现层能根据逻辑执行结果做：
- **成功**：提交（保留牌恢复排序）
- **失败**：回滚（全部恢复原状）

保证视觉与逻辑一致。

### 3. 三态快照

每张选中牌通过 `MoveToOverBarTilePresentationScope` 保存：
- 排序层级（SortingOrder）
- PresentationMode
- 背景可见性（BackgroundVisible）

确保恢复时精确还原。

---

## 需求对齐分析

| 需求步骤 | 当前实现 | 状态 |
|---------|---------|------|
| 1. 图标飞砸曲线砸到目标牌 | DOPath CatmullRom 弧线 0.45s | ✅ 已有 |
| 2. 图标消失 | DOScale(0) 0.1s 缩小 | ✅ 已有 |
| 3. 选中牌提到最上层 | ApplyMoveToOverBarPresentation sortingOrder=100 | ✅ 已有 |
| 4. 停留 0.1s | **原缺失** | ✅ **已补** |
| 5. 飞到弃牌区 | 逻辑层 AddToOverBar → View PlayAddToOverBarAnim | ✅ 已有 |

**差距仅 1 处**：飞行图标消失后、选中牌提到上层后缺 0.1s 停留。牌飞到弃牌区的动画已由逻辑层 `ActionResult.AddToOverBar` → `OverBarView.PlayAddToOverBarAnim` 覆盖，表现层不需要额外处理。

---

## 0.1s 停留补丁

**文件**：`TileGamePanelPropPresentation.cs`（+8 行）

### 改动清单（5 处）

| # | 位置 | 改动 |
|---|------|------|
| 1 | Config | 新增 `SelectedTileHoldDuration = 0.1f` |
| 2 | 字段 | 新增 `_presentationApplied` flag |
| 3 | OnComplete | 飞行图标销毁 → `ApplyMoveToOverBarPresentation()`（选中牌提到上层）→ `DelayedCall(0.1f, Complete)` |
| 4 | Complete | Apply 条件加 `!_presentationApplied` 跳过重复 Apply，避免 0.1s 停留期间选中的牌被先撤销再重新应用造成闪烁 |
| 5 | Cancel | 重置 flag |

### 新时序

```
飞行动画 0.45s
  → 图标消失
  → 选中牌提到上层 (sortingOrder=100)
  → 停留 0.1s (DelayedCall)
  → Complete: 执行逻辑层拿牌
  → 牌飞到弃牌区动画 (View 层 PlayAddToOverBarAnim)
  → 成功提交 / 失败回滚
```

---

## 3 张选中牌排序现状

当前 3 张选中牌**都设 `SelectedTileSortingOrder = 100`**，彼此完全相同。

`SetSortingOrder(100)` 内部展开：
- icon = 299
- background = 298
- effects = 300+

3 张牌之间没有相对渲染差异——位置不重叠时无影响。但如果希望 3 张牌有明确叠加顺序（比如后选的盖在先选上面），需要改成递增（100/101/102）。**此项待确认是否需要修改。**

---

## 关键文件路径

| 层 | 文件 |
|----|------|
| UI 表现层 | `Assets/Game/TileV2/Scripts/UI/UIGamePanel/TileGamePanelPropPresentation.cs` |
| UI 流程 | `Assets/Game/TileV2/Scripts/UI/UIGamePanel/TileGamePanelPropUseFlow.cs` |
| UI 控制 | `Assets/Game/TileV2/Scripts/UI/UIGamePanel/TileGamePanelPropController.cs` |
| UI 按钮 | `Assets/Game/TileV2/Scripts/UI/UIGamePanel/TileGamePanelPropButton.cs` |
| View 接口 | `Assets/Game/TileV2/Scripts/GameCore/View/Interface/ITileMatchViewController.cs` |
| View GameView | `Assets/Game/TileV2/Scripts/GameCore/View/GameView/TileMatchViewController.cs` |
| View Headless | `Assets/Game/TileV2/Scripts/GameCore/View/Headless/TileMatchViewController.cs` |
| BoardView G | `Assets/Game/TileV2/Scripts/GameCore/View/GameView/Views/Board/BoardView.cs` |
| BoardView H | `Assets/Game/TileV2/Scripts/GameCore/View/Headless/Views/Board/BoardView.cs` |
| OverBarCell G | `Assets/Game/TileV2/Scripts/GameCore/View/GameView/Views/OverBar/OverBarCellView.cs` |
| OverBarCell H | `Assets/Game/TileV2/Scripts/GameCore/View/Headless/Views/OverBar/OverBarCellView.cs` |
| FlipTileView | `Assets/Game/TileV2/Scripts/GameCore/View/GameView/Views/Tile/Flip/FlipTileView.cs` |
| JokerFlipTileView | `Assets/Game/TileV2/Scripts/GameCore/View/GameView/Views/Tile/JokerFlip/JokerFlipTileView.cs` |
| Logic Selection | `Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Prop/MoveToOverBarSelection.cs` |
| Logic Prop | `Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Prop/MoveToOverBarProp.cs` |

---

## 相关文档

- [[_MOC|TileScape 知识库 MOC]]
- [[代码框架/代码框架总览|代码框架总览]]
- [[_项目概览|项目概览]]
