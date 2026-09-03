---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：SuitCase 行李箱（5130/5131）

## 一、基础属性

| 属性                       | 值                        | 说明   |
| ------------------------ | ------------------------ | ---- |
| TileType                 | `5130`(H) / `5131`(V)    |      |
| Group                    | `Blocker`                |      |
| MatchCount               | `0`                      |      |
| 尺寸                       | 3×1 / 1×3 Fixed          |      |
| 血量                       | 1                        |      |
| CoveredTileIgnoreVisible | `true`                   |      |
| CustomTileController     | `SuitCaseTileController` |      |
| SequenceLayoutType       | `1`                      | 特殊排列 |

## 二、数据层

### 花色去重（blockerdda 变更）

| 阶段     | 之前                             | 之后     |
| ------ | ------------------------------ | ------ |
| 初始分配   | Prefer                         | **移除** |
| 洗牌     | Prefer                         | **移除** |
| DDA 保护 | ProtectSequenceChildrenFromDda | **移除** |

### HasSeen 机制

| 场景     | 之后         |
| ------ | ---------- |
| DDA 交换 | Swap 互换    |
| 洗牌     | Rebuild 重建 |

## 三、逻辑层：4 条 ECA（当前分支最新）

### ① UpdateSequenceState（`5130001`）— 进场初始化

| 事件 | 条件 | 动作 |
|------|------|------|
| `LevelEnterAnimationStepOneFinished` | `SequenceCount >= 1` | `RefreshSequenceState(FirstNHighlight, Count=3, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow, SequenceRegulationEventPolicy=AllEvents, **EnableDdaRegulationOnActivation=true**)` |

> **blockerdda 变更**：新增 `EnableDdaRegulationOnActivation=true`。进场即激活 DDA 调控资格追踪。
> Count=3：一次性暴露 3 张子牌。

### ② CoverRemoveOnHighlight（`5130002`）— 高亮时脱盖

| 事件 | 条件 | 动作 |
|------|------|------|
| `TileVisibilityChanged` | `VisibilityState=4` AND `SequenceCount >= 1` | `RefreshSequenceState(FirstNHighlight, Count=3, SequenceVisibleDdaMode=VisibleOrEnterDisplayWindow, SequenceRegulationEventPolicy=AllEvents, **EnableDdaRegulationOnActivation=true**)` |

> 容器变为高亮时盖子脱落，3 张子牌全部暴露。

### ③ DestroyWhenEmpty（`5130003`）`Once=true`

| 事件 | 条件 | 动作 |
|------|------|------|
| `AddingToBarByClick` / `AfterAttack` / `AutoMatchUse` | `SequenceCount=0` | `PlayDestroyAnim` → `DestroyTile` |

### ④ DestroyWhenSequenceTileDestroyed（`5130004`）`Once=true`

| 事件 | 条件 | 动作 |
|------|------|------|
| `AfterAttack` | `SequenceCount=0` | `PlayDestroyAnim` → `DestroyTile` |

## 四、调控层（blockerdda 变更）

### Activation DDA（新增）
- 规则 ①② 设置 `EnableDdaRegulationOnActivation=true`
- 盖子脱落后子牌从 Visible→Highlight 时触发 DDA
- 通过 `InitializeActivationEligibility()` 追踪 3 个索引的调控资格

### DDA 参与资格
- **之前**：子牌被 `IsProtectedFromDDA` 阻止
- **之后**：保护移除，3 张子牌均可参与 DDA 交换

### 花色约束
- **之前**：3 张子牌花色尽量不重复（Prefer）
- **之后**：无约束，可能出现同花色子牌

## 五、视图层

| 模块 | 职责 |
|------|------|
| `SuitCaseTileController.cs` | 行李箱控制 + 盖子动画 |
| Spine | 盖子脱落动画 + 3 张子牌弹出 |
| 序列显示 | `SequenceLayoutType=1`：3 张一字排开 |

## 六、可见性 & 选中规则

| 状态 | 子牌可见性 | 可交互 |
|------|-----------|--------|
| 被遮挡（盖着） | FirstNHighlight(3) 但容器不可见 | ❌ |
| 容器高亮（脱盖） | 3 张全部 Highlight | ✅ 全部可点 |
| 序列空 | 销毁 | — |

## 七、关联笔记

- [[障碍牌-CardBox]]
- [[障碍牌-SlotMachine]]
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
