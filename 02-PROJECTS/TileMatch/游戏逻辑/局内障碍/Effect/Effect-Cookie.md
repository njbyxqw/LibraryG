---
tags: [TileMatch, 游戏逻辑, Effect牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 005
---

# Effect：Cookie 饼干 / Jelly 果冻

---

# Cookie 饼干（120-121）

| 属性 | 值 |
|------|-----|
| EffectType | 120(H) / 121(V) |
| Priority | `6` |
| 尺寸 | 2×1 / 1×2 |
| 血量 | 2 |
| 透传 | ❌ |
| 遮挡 | ✅ |
| TakeOverDestroy | ✅ |
| 伤害源 | `4`（AddToBar） |

## 逻辑层：3 条 ECA

### 自动销毁（`120004`）
| 条件 | 动作 |
|------|------|
| **ANY**：( `CoveredCountAtMost(FullCover=true, Max=0)` **OR** `BoardHasAtMostInteractableTile(0)` ) + Lives>=1 | `PlayDestroyAnim` → `DestroyEffect` |

> FullCover=true, Max=0 = 覆盖的 2 格全部揭开后饼干自动碎裂。

### 视图层：CookieEffectView

**实现接口**：`ITileViewCustomControl` + 领域事件

| 组件 | 作用 |
|------|------|
| `cookieSpriteRenderer[]` | 阶段切换精灵 |
| `hitParticle` + `destroyParticle` | 击打/销毁粒子 |
| `_originalLife` | 根据 EffectData.Life 初始化 |
| `_enterAnimationPlaying` | 入场动画（2×1 块掉落） |

```
ChangeEffectLives(delta<0):
  → Life>=1: SFX_cookie_break1 + hitParticle
  → Life<=0: SFX_cookie_break2 + destroyParticle

PlayCantClickAnimation → DOTween DOShakePosition

SetObjectStateByLife(_originalLife - life) → spriteRenderer 阶段切换

ITileViewCustomControl: LockPosition=true, LockScale=false, LockSortingOrder=false
入场动画 → OnEnterAnimationTick 逐帧控制
```

---

# Jelly 果冻（180-183）+ JellyTransparent（170-173）

| 属性 | 值 |
|------|-----|
| EffectType | 170-183（8 方向） |
| Priority | `7` |
| 尺寸 | 1×2 |
| 血量 | 2 |
| 透传 | ❌ |
| TakeOverDestroy | ✅ |
| 初始状态 | `InitialState=1` |

## Jelly vs JellyTransparent

| | Jelly | JellyTransparent |
|------|-------|-----------------|
| 遮挡 | ✅ `IsOccluder` + `OcclusionMask` | ❌ |
| 可见性 | 一格不透明遮挡 | 两格透明可见 |
| 点击 | 不遮挡格可点 | `ClickMask` 控制 |

### OcclusionMask / ClickMask 示例（JellyDown）

```
OcclusionMask: [[1],[0]]  → 上格遮挡，下格可见
ClickMask:     [[1],[0]]  → 上格可点，下格不可点
```

## 逻辑层：2 条 ECA

### AutoDestroyWhenAllTilesDestroyed（`1xx002`）
| 事件 | 条件 | 动作 |
|------|------|------|
| 进场/进Bar/AfterAttack/自动/Tile销毁后 | `CoveredCountAtMost(FullCover=true, Max=1)` + Lives>=1 | `ChangeEffectState(2)` → `PlayDestroyAnim` → `DestroyEffect` |

> 底层 2 格只剩 ≤1 格有 Tile → 果冻自动融化。

## 视图层：JellyEffectView

**实现接口**：`ITileViewCustomControl` + 领域事件

| 组件 | 作用 |
|------|------|
| `centerRender` + `otherRender` | 中心/另一块瓦片 Transform |
| `centerUISprite` | 中心瓦片渲染 |
| `clickParticle` + `deathParticle` | 点击/销毁粒子 |
| `clickAnim` (Animator) | `"Click"` 抖动动画 |
| `endParticleTs` | 销毁粒子位置 |
| `_enterAnimationPlaying` | 入场动画 |

```
PlayCantClickAnimation → DoClickEffect:
  → SFX_link_break
  → 按名播放粒子 "Effect_Jelly_Click_" + EffectType
  → Animator "Click" + AttachTileViewFollowers

DoDeathEffect:
  → Jelly: SFX_jelly_break1 / JellyTransparent: SFX_jelly_break2
  → 按名播放粒子 "Effect_Jelly_End_" + EffectType

SortingOrder: 复杂方向映射
  Left/Right: normalOrder
  Up: centerRender special + other normal
  Down: centerRender normal + other special

GetTargetRenderTransform → 根据相对位置决定 attach 到 centerRender 还是 otherRender
入场动画 → OnEnterAnimationTick
```

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
