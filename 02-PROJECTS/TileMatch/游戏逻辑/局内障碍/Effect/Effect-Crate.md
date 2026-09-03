---
tags: [TileMatch, 游戏逻辑, Effect牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 006
---

# Effect：Crate 木箱

## 基础属性

| 属性 | 值 |
|------|-----|
| EffectType | `20` |
| Priority | `6` |
| 尺寸 | 1×1（Fixed） |
| 血量 | 1 |
| 透传伤害 | ❌ |
| 遮挡 | ✅ `IsOccluder: true` |
| 配置文件 | `EffectConfig/Crate.json` |

---

## 数据层

- **DamageSourceType=`4`**：仅 AddToBar 消除能敲碎木箱
- 单层护盾，1 次攻击即碎
- 遮挡底层 Tile 点击

---

## 逻辑层：4 条 ECA

### ① HandleAttack（`20001`）
| 事件 | 条件 | 动作 |
|------|------|------|
| `Attack` | DamageSourceType=4 + Lives>=1 | `HandleAttack` |

### ② Destroy有命（`20002`） StopPolicy=1
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectDestroyed` | Lives>=1 | `PlayDestroyAnim` → `DestroyEffect` |

### ③ Destroy没命（`20003`） StopPolicy=1
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectDestroyed` | Lives<=0 | `DestroyEffect` |

### ④ 死局自毁（`20004`）
| 事件 | 条件 | 动作 |
|------|------|------|
| 进场/进Bar/道具用完/自动消除 | 棋盘无可交互+无锁定+Lives>=1 | `ChangeEffectState(2)` → `PlayDestroyAnim` → `DestroyEffect` |

---

## 视图层：CrateEffectView

| 组件 | 名称 | 作用 |
|------|------|------|
| 粒子 | `crateParticle` | 木箱破碎粒子 |

### 关键逻辑

```
ChangeEffectLives(delta<0) → DoReduceEffect
  → 隐藏图标
  → SFX_crate_break + crateParticle缩放至TileSize

PlayCantClickAnimation → DOTween DOShakePosition(0.08s, 0.05强度)

PlayDestroyAnim → 同DoReduceEffect + 释放事件
```

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
