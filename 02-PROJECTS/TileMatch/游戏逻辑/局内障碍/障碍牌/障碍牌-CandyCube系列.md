---
tags: [TileMatch, 游戏逻辑, 障碍牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 003
---

# 障碍牌：CandyCube 糖果系列（收集型）

## 变体

| 障碍 | TileType | 尺寸 | 血量 | FixedSize |
|------|----------|------|------|-----------|
| CandyCube | 5070 | 2×2 | 1 | ✅ |
| CandyCube3x1H | 5091 | 3×1 | 1 | ✅ |
| CandyCube3x1V | 5090 | 1×3 | 1 | ✅ |
| CandyCubeNx1H | 5181 | 2~7×1 | 1 | ❌（可变） |
| CandyCubeNx1V | 5180 | 1×2~4 | 1 | ❌（可变） |

## 基础属性

| 属性 | 值 |
|------|-----|
| Group | **`Collectable`**（不是 Blocker） |
| MatchCount | `0`（不参与消除） |
| 血量 | 1 |
| 配置文件 | `TileConfig/CandyCube*.json` |

---

## 数据层

- **Group=Collectable**：CandyCube 不占据 Bar 槽位，不参与消除
- **FixedSize**：标准 CandyCube 固定尺寸；`Nx1` 版本为可变尺寸（关卡编辑器可拉伸）

---

## 逻辑层：2 条 ECA（全部变体共用）

### ① OnHighlight — 可见即收集（`xxx001`） `Once=true`

| 层级 | 内容 |
|------|------|
| **事件** | `TileVisibilityChanged` / `LevelEnterAnimationStepOneFinished` / `AfterAttack` / `AutoMatchUse` |
| **条件** | `VisibilityState = 4`（完全可见）且 `Lives >= 1` |
| **动作** | `PlayDestroyAnim(AutoDestroy=true)` — 自动销毁（收集） |

> **核心**：CandyCube 不需要攻击！只需将所有遮挡它的 Tile 清除，它变成可见（VisibilityState=4）→ 自动收集。

### ② TileDestroyed（`xxx002`） `Once=true`

| 层级 | 内容 |
|------|------|
| **事件** | `TileDestroyed` |
| **条件** | — |
| **动作** | `DestroyTile` — 最终销毁 |

---

## 可见性规则

| 状态 | 行为 |
|------|------|
| 被遮挡（VisibilityState<4） | 不可交互，不触发 |
| 完全可见（VisibilityState=4） | **自动 PlayDestroyAnim** → 收集完成 |

> 这是最简单的障碍：没有攻击逻辑，没有血量机制。只要暴露就自动收集。设计思路类似 "reach the target" 目标牌。

---

## 视图层

| 变体 | 视觉 |
|------|------|
| CandyCube | 2×2 糖果方块，可见→闪光消失 |
| CandyCube3x1 | 横向/纵向 3 连糖果 |
| CandyCubeNx1 | 可变长条糖果（编辑器可自由拉伸 2~7 格） |

---

## 关联
- [[Effect-Golden]]
- [[局内障碍知识库_MOC]]
- [[障碍牌-类型全览]]
