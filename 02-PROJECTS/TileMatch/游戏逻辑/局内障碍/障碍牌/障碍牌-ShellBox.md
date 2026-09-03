---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：ShellBox 贝壳 + MagicBox 魔法盒

## 一、基础属性

### ShellBox（8 方向变体）

| 变体 | TileType | 开口方向 | 可见内部 |
|------|----------|---------|---------|
| ShellBoxUp | 5030 | 上方（弹出 (0,-2)） | ✅ |
| ShellBoxDown | 5031 | 下方 | ✅ |
| ShellBoxLeft | 5032 | 左方 | ✅ |
| ShellBoxRight | 5033 | 右方 | ✅ |
| ShellBoxOpaqueUp | 5040 | 上方 | ❌ 不透明 |
| ShellBoxOpaqueDown | 5041 | 下方 | ❌ |
| ShellBoxOpaqueLeft | 5042 | 左方 | ❌ |
| ShellBoxOpaqueRight | 5043 | 右方 | ❌ |

### MagicBox

| 属性 | 值 |
|------|-----|
| TileType | 5010 |
| 弹出方向 | 上方 (0,2) |
| 可见内部 | ✅ |

### 共同属性

| 属性 | 值 |
|------|-----|
| Group | `Blocker` |
| MatchCount | `0` |
| 尺寸 | 1×1 Fixed |
| CoveredTileIgnoreVisible | `true` |
| SequenceDepthMode | `2` |
| 血量 | 1 |

## 二、数据层

### 花色去重（blockerdda 变更）
- **之前**：B 类容器，无去重约束
- **之后**：无变化（本来就是 None）

### HasSeen 机制
| 场景 | 之后 |
|------|------|
| DDA 交换 | Swap 互换 |
| 洗牌 | Rebuild 重建 |

## 三、逻辑层：4 条 ECA（以 ShellBoxUp 为例）

### ① TryToEjectCovered（`5030001`）— 尝试弹出子牌

| 事件 | 条件 | 动作 |
|------|------|------|
| `LevelEnterAnimationStepOneFinished` / `AfterTileDestroyed` / `AddingToBarByClick` / `AfterAttack` / `AutoMatchUse` | `SequenceCount>=1` AND `VisibilityState=4` AND `GridIsEmpty(LayerType=3, 检查 (0,-1)(0,-2)(1,-1)(1,-2))` | `EjectSequenceTo(Position=(0,-2), FullCover=true)` → `UpdateSequenceState(FirstNVisible, Count=1)` |

> 可见且目标格子空闲时，弹出子牌到棋盘。ShellBox 弹出后子牌为 Visible（不可交互），需等容器销毁后才变为可交互。

### ② TileDestroyedWhenNoCovered（`5030002`）`Once=true`

| 事件 | 条件 | 动作 |
|------|------|------|
| `AfterAttack` / `AutoMatchUse` | `SequenceCount=0` | `PlayDestroyAnim` |

### ③ UpdateStateWhenAttacked（`5030003`）

| 事件 | 条件 | 动作 |
|------|------|------|
| `AfterTileDestroyed` / `AddingToBarByClick` / `AfterAttack` / `AutoMatchUse` | `SequenceCount>=1` | `UpdateSequenceState` |

### ④ TileDestroyed（`5030004`）`Once=true`

| 事件 | 条件 | 动作 |
|------|------|------|
| `TileDestroyed` | — | `DestroyTile` |

### MagicBox 差异

| | ShellBox | MagicBox |
|------|---------|---------|
| 弹出方向 | 开口方向 | 固定向上 (0,2) |
| GridIsEmpty 检测 | 开口方向对应格 | (0,2)(0,3)(1,2)(1,3) |

## 四、调控层

### DDA 参与资格
- ShellBox/MagicBox 的子牌**无 DDA 保护**（B 类容器，从未有过）
- 子牌可参与 DDA 交换

### PreRegulate 预调控机制（blockerdda 新增）

> ShellBox 与 Thief 共享同一套预调控链路。

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

**触发时机**：ShellBox 可见且目标格子空闲时，弹出子牌到棋盘（规则 ①）。EjectSequenceTo 执行后，自动检查序列中是否还有隐藏子牌，如有则执行 DDA 预调控。

**与其他调控的区别**：
- ❌ 无 `SequenceVisibleDdaMode` 配置（不参与可见性 DDA）
- ❌ 无 `EnableDdaRegulationOnActivation`（不参与激活 DDA）
- ✅ 有 `PreRegulateNextHiddenTile`（弹出时预调控下一个隐藏子牌）

## 五、视图层

| 模块 | 职责 |
|------|------|
| `ShellBoxTileController.cs` | 贝壳控制：序列可见性管理、弹出动画 |
| `MagicBoxTileController.cs` | 魔法盒控制 |
| Spine | 开盖动画 + 子牌弹出粒子 |

## 六、可见性 & 选中规则

| 状态 | 子牌可见性 | 可交互 |
|------|-----------|--------|
| 被遮挡 | 不可见 | ❌ |
| 可见（VisibilityState=4） | 弹出到棋盘 FirstNVisible(1) | ❌（Visible 不可交互） |
| 容器销毁后 | 子牌变为普通 Tile | ✅ |
| 无子牌 | 容器自动销毁 | — |

> ShellBox vs ShellBoxOpaque：Opaque 版本内部子牌不可见（增加难度），但 ECA 逻辑完全相同。

## 七、关联笔记

- [[障碍牌-CardBox]]
- [[障碍牌-SlotMachine]]
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
