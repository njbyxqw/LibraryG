---
tags: [TileMatch, 游戏逻辑, Effect牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 011
---

# Effect：Ice 冰块 1×1 + Ice2x2 冰块 2×2

---

## 对比

| 属性 | Ice 1×1 | Ice2x2 |
|------|---------|--------|
| EffectType | `30` | `200` |
| 尺寸 | 1×1 | 2×2 |
| 血量 | 3 | 4 |
| Priority | 1 | 1 |
| 父节点 | BoardView | Tile |
| TakeOverDestroy | ❌ | ✅ |
| ITileViewCustomControl | ❌ | ✅ |
| 入场动画 | ❌ | ✅ |

---

# Ice 冰块 1×1

## 数据层

- 挂在 `BoardView`（棋盘层），不挂 Tile
- **DamageSourceType=`4`**（AddToBar）

## 逻辑层：4 条 ECA（标准受击+销毁+死局）

## 视图层：IceEffectView

| 组件 | 作用 |
|------|------|
| Animator | `"3"`(阶段0) / `"3_2"`(阶段1) / `"2_1"`(阶段2) / `"doudong"`(抖动点击) |
| 粒子 | `hitParticle` + IceBreak1/IceBreak2（按名播放） |
| TransformFollower | 受伤时跟随 TileView |
| `_originalLife = 3` | |

```
ChangeEffectLives → DoReduceEffect
  → SFX_ice_break
  → life>0: SetIceObjectState(阶段) + 按名播放 IceBreak1/2
  → life==0: ClearTileFollower + hitParticle

PlayCantClickAnimation → Animator "doudong" + SFX_ice_click + AttachTileViewFollowers
```

---

# Ice2x2 冰块 2×2

## 视图层：Ice2x2EffectView

**实现接口**：`ITileViewCustomControl` + 领域事件（LevelViewInitialized, LevelEnterAnimationStepTwoFinished）

| 组件 | 作用 |
|------|------|
| `stageGameObject[5]` | 5阶段外观（0-4） |
| `reduceLifeParticle1/2/3` | 4→3/3→2/2→1 过渡粒子 |
| `deathParticle` | 最终死亡 |
| `smokeParticle` | 烟雾 |
| `_originalLife = 4` | |
| `_fallAsWhole = true` | 入场整块掉落 |

```
ChangeEffectLives(ignore delta) → DoReduceEffect
  → 阶段切换:
    life=3: SFX_bigice_break1 + reduceLifeParticle1 + smokeParticle
    life=2: SFX_bigice_break2 + reduceLifeParticle2 + smokeParticle
    life=1: SFX_bigice_break3 + reduceLifeParticle3 + smokeParticle
    life=0: SFX_bigice_break4 + deathParticle
  → life>0: SetIce2x2ObjectState 激活对应 stageGameObject

PlayCantClickAnimation → DOTween DOShakePosition + SFX_ice_click

入场动画 → OnEnterAnimationTick 控制整块掉落
SortingOrder: backSprite order-10, orderSprite2 +2, orderParticle4 +4, orderParticle5 +5
```

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
