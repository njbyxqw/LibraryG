---
title: Effect-Golden 金砖
type: analysis
tags: [TileMatch, 游戏逻辑, Effect牌]
status: draft
date: 2026-07-01
cat_order: 009
---

# Effect：Golden 金砖

## 基础属性

| 属性 | 值 |
|------|-----|
| EffectType | `10` |
| Priority | `0`（最低） |
| 尺寸 | 1×1（Fixed） |
| 血量 | 4 |
| 透传伤害 | ❌ |
| 点击遮挡 | ❌ `IsClickOccluder: false` |
| 初始状态 | `InitialState=2` |
| 配置文件 | `EffectConfig/Golden.json` |

---

## 数据层

- **DamageSourceType=`4`**：AddToBar 攻击
- **VisibilityState=4**：必须可见才能被攻击
- **LevelCollect**：打碎时触发收集计数 `Golden` +1
- **不遮挡点击**：玩家可以同时点击底层 Tile

---

## 逻辑层：3 条 ECA

### ① HandleAttack（`10001`）
| 事件 | 条件 | 动作 |
|------|------|------|
| `Attack` | DamageSourceType=4 + VisibilityState=4 + Lives>=1 | `HandleAttack` |

### ② Destroy收集（`10002`）
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectDestroyed` | Lives>=1 | `PlayDestroyAnim` → **`LevelCollect(Key="Golden", Count=1)`** → `DestroyEffect` |

### ③ Destroy没命（`10003`）
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectDestroyed` | Lives<=0 | `DestroyEffect` |

---

## 视图层：GoldenEffectView

**实现接口**：`IBackgroundHiddenEffect`

| 组件 | 类型 | 作用 |
|------|------|------|
| `stageGameObjects[5]` | GameObject数组 | 5阶段外观（life 4→0） |
| `stageGoldIcon[5]` | GameObject数组 | 序列预览模式图标 |
| `stageGoldBackground[5]` | GameObject数组 | 可见模式背景 |
| `hitParticleA/B/C/D` | Particle | 各阶段击打粒子（stage 1-4） |
| `explodeParticle` | Particle | 最终销毁爆炸 |
| orderSprite2/3 | SpriteRenderer | 排序层 |

### 关键逻辑

```
_originalLife = 4

ChangeEffectLives(ignore delta) → DoReduceEffect
  → SFX_goldenTile_break
  → SetStageGameObjectState(生命值对应阶段)
    → 激活当前stageGameObject + stageGoldIcon + stageGoldBg
    → 播放对应阶段 hitParticle(A/B/C/D)
    → RefreshPresentation() 系统切换显示

RefreshPresentation:
  → entityVisible + backgroundVisible + previewActive
  → 决定显示 _curGoldIcon 还是 _curGoldBg

PlayDestroyAnim → explodeParticle + 释放事件
```

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
