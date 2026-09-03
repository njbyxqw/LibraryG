---
tags: [TileMatch, 游戏逻辑, Effect牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 016
---

# Effect：Stone 石板

## 基础属性

| 属性 | 值 |
|------|-----|
| EffectType | `80` |
| Priority | `3` |
| 尺寸 | 1×1（Fixed） |
| 血量 | 2 |
| 透传伤害 | ❌ |
| 遮挡 | ✅ `IsOccluder: true` |
| 配置文件 | `EffectConfig/Stone.json` |

---

## 数据层

- **DamageSourceType=`8`**：仅 Match 消除攻击
- **OverBarHasAtMostInteractableTile(0)**：死局自毁时额外检查头顶弃牌区

---

## 逻辑层：4 条 ECA

### ① HandleMatchAttack（`80001`）
| 事件 | 条件 | 动作 |
|------|------|------|
| `Attack` | DamageSourceType=8(Match) + Lives>=1 | `HandleAttack` |

### ② Destroy有命（`80002`） StopPolicy=1
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectDestroyed` | Lives>=1 | `PlayDestroyAnim` → `DestroyEffect` |

### ③ Destroy没命（`80003`） StopPolicy=1
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectDestroyed` | Lives<=0 | `DestroyEffect` |

### ④ 死局自毁（`80004`）← 唯一含 `OverBar` 检查
| 事件 | 条件 | 动作 |
|------|------|------|
| 进场/进Bar/道具用完/自动消除 | `BoardHasAtMostInteractableTile(0)` + `BoardHasAtMostLockedTile(0)` + **`OverBarHasAtMostInteractableTile(0)`** + Lives>=1 | `ChangeEffectState(2)` → `PlayDestroyAnim` → `DestroyEffect` |

> 多层布局时，头顶层也清空才自毁。

---

## 视图层：StoneEffectView

| 组件 | 名称 | 作用 |
|------|------|------|
| 粒子 | `stoneParticle` | 碎石粒子 |
| 精灵数组 | `stoneSpriteRenderer[]` | 2阶段（完整→碎裂） |
| 私有字段 | `_originalLife = 2` | 记录初始血量 |

### 关键逻辑

```
ChangeEffectLives(delta<0)
  → DoReduceEffect
    → SFX_stone_break + stoneParticle
    → SetObjectStateByStage(_originalLife - 剩余)
      → stage 0: 完整石板
      → stage 1: 碎裂石板

PlayCantClickAnimation → base(无动画) + SFX_stone_click

SetSortingOrder → stoneSpriteRenderer[] order+1
```

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
