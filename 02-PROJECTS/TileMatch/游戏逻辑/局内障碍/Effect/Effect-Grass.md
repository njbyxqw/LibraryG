---
title: Effect-Grass 草丛
type: analysis
tags: [TileMatch, 游戏逻辑, Effect牌]
status: draft
date: 2026-07-01
cat_order: 010
---

# Effect：Grass 草丛

## 基础属性

| 属性 | 值 |
|------|-----|
| EffectType | `70` |
| Priority | `2` |
| 尺寸 | 1×1（Fixed） |
| 血量 | 2 |
| 透传伤害 | ❌ |
| 配置文件 | `EffectConfig/Grass.json` |

---

## 数据层

- **DamageSourceType=`2`**：特殊伤害源
- **NeighborIsEmpty(type=16, layer=2)**：邻居格被清除后自动枯萎

---

## 逻辑层：4 条 ECA

### ④ 自动销毁（`70004`）— 独有机制

| 事件 | 条件 | 动作 |
|------|------|------|
| 进场/进Bar/道具/自动 | **ANY**：( `NeighborIsEmpty(16, layer=2)` **OR** `BoardHasAtMostInteractableTile(0)` ) + Lives>=1 + Board无锁定 | `ChangeEffectState(2)` → `PlayDestroyAnim` → `DestroyEffect` |

> 邻居 Tile 被消除 → 草丛失去依附 → 自动枯萎。

---

## 视图层：GrassEffectView

| 组件 | 作用 |
|------|------|
| `hitParticle` | 击打粒子 |
| `spine` + `spineRender` | Spine 草丛模型 |
| `_originalLife = 2` | |

```
ChangeEffectLives(ignore delta) → DoReduceEffect
  → SFX_lawn_break + hitParticle
  → life==1: Spine "B_Idle" (萎靡状态)

PlayCantClickAnimation:
  → life==1: Spine "B_Click" (点击枯萎)
  → life==2: Spine "A_Click" (点击完整)

SetSortingOrder → spineRender order+2
```

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
