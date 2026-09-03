---
tags: [TileMatch, 游戏逻辑, Effect牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 004
---

# Effect：Cloud 云朵 / GiftBox 礼盒

---

## Cloud 云朵（90）

| 属性 | 值 |
|------|-----|
| EffectType | `90` |
| Priority | `4` |
| 血量 | 1 |
| 遮挡 | ✅ |
| 透传 | ❌ |
| 伤害源 | `64`（特殊） |

### 逻辑层：4条ECA

**① OnVisibilityChange（`90001`）** — 核心
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectVisibilityChanged` / 进场 / AfterAttack / AutoMatch | VisibilityState=4 + Lives>=1 | `ChangeEffectLives(-1)` → `DestroyEffect` |

> 底层 Tile 完全可见 → 云自动-1 命→自毁。**无法被常规攻击打掉**。

### 视图层：CloudEffectView

| 组件 | 作用 |
|------|------|
| `cloudParticle` | 飘散粒子 |
| `animation` (Legacy) | `"CloudBlock_End"` 消散动画 |
| `ViewConfig.destroyAnimationDelayTime` | 销毁动画延迟 |

```
ChangeEffectLives(delta<0) → DoReduceEffect
  → SFX_cloud_break + cloudParticle
  → Animation.Play("CloudBlock_End")

PlayDestroyAnim → DOVirtual.DelayedCall(延迟) → 释放事件
```

---

## GiftBox 礼盒（100）

| 属性 | 值 |
|------|-----|
| EffectType | `100` |
| Priority | `9`（最高） |
| 血量 | 1 |
| 遮挡 | ✅ |
| 透传 | ❌ |
| 伤害源 | `64` |

### 逻辑层：3条ECA

**② OnVisibilityChange（`100002`）**
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectVisibilityChanged` / 进场 / AfterAttack / AutoMatch | VisibilityState=4 + Lives>=1 | `ChangeEffectLives(-1)` → `PlayDestroyAnim` → `DestroyEffect` |

**③ 无条件销毁（`100003`）** — 无 Lives 条件！EffectDestroyed 触发即执行。

### 视图层：GiftBoxEffectView

| 组件 | 作用 |
|------|------|
| `giftBoxParticle` | 礼物粒子 |
| `spine` (SkeletonAnimation) | Spine `"animation"` 开盒动画 |
| `ViewConfig.destroyAnimationDelayTime` | 延迟配置 |

```
PlayDestroyAnim → SFX_giftbox_break + Spine "animation" + giftBoxParticle
  → 无 CustomEnterAnimDelay（不同于 Cloud）
```

---

### Cloud vs GiftBox 对比

| | Cloud | GiftBox |
|------|-------|--------|
| 销毁动画 | Legacy Animation "CloudBlock_End" | Spine "animation" |
| 粒子 | cloudParticle | giftBoxParticle |
| 声音 | SFX_cloud_break | SFX_giftbox_break |
| 延迟 | DOVirtual.DelayedCall | 配置延迟 |
| 无Lives销毁 | ❌ 仅2条 | ✅ 无条件触发 |

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
