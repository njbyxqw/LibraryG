---
tags: [TileMatch, 游戏逻辑, 障碍牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 004
---

# 障碍牌：Ore 矿石 + Pickaxe 镐子

## 关系

> Ore（矿石）和 Pickaxe（镐子）是配对的障碍体系。矿石本身不可交互，需要点击对应等级的镐子来敲碎。

## 变体

| 镐 | TileType | 对应矿石 | Ore TileType | 尺寸 |
|------|----------|---------|-------------|------|
| Pickaxe1 | 5187 | Ore1 | 5190 | 镐:1×1 / 矿:3×3 |
| Pickaxe2 | 5188 | Ore2 | 5191 | 镐:1×1 / 矿:3×3 |
| Pickaxe3 | 5189 | Ore3 | 5192 | 镐:1×1 / 矿:3×3 |

## 基础属性

| | Pickaxe | Ore |
|------|---------|-----|
| Group | Blocker | Blocker |
| MatchCount | `3`（可点击） | `0` |
| 尺寸 | 1×1 | 3×3 |
| 洗牌 | ✅ | ❌ `Shufflable=false` |

## 核心机制

> 点击镐 → 进 Bar（MatchCount=3）→ 攻击对应等级的矿石 → 矿石破碎。

- Ore 不可洗牌（`Shufflable=false`），固定在棋盘上
- 必须用同等级的镐（1对1，2对2，3对3）

## 关联
- [[局内障碍知识库_MOC]]
- [[障碍牌-类型全览]]
