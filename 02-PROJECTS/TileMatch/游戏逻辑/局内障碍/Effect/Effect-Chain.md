---
title: Effect-Chain 锁链
type: analysis
tags: [TileMatch, 游戏逻辑, Effect牌]
status: draft
date: 2026-07-01
cat_order: 002
---

# Effect：Chain 锁链

## 基础属性

| 属性 | 值 |
|------|-----|
| EffectType | `60` |
| Priority | `5` |
| 尺寸 | 1×1（Fixed） |
| 透传伤害 | ❌ |
| 配置文件 | `EffectConfig/Chain.json` |

---

## 数据层

- **作用**：链接两个 Tile，攻击一端时传递到另一端
- 无血量机制（无 `Life` 字段）
- 无遮挡（无 `IsOccluder`）

---

## 逻辑层：1 条 ECA

### HandleAddToBarAttack（`60001`）

| 事件 | 条件 | 动作 |
|------|------|------|
| `Attack`（TargetSelector=1） | — | 链接攻击传递 |

> Chain 不阻挡攻击，而是**转发**攻击到链接的另一端 Tile。

---

## 视图层：ChainEffectView

| 组件 | 名称 | 作用 |
|------|------|------|
| 粒子 | `hitParticle` | 断链时击中粒子 |
| Animator | `animator` | 已声明未使用 |
| Spine | `spine` + `spineRender` | 锁链模型 |

### 关键逻辑

```
ChangeEffectLives → DoReduceEffect
  → 播放 SFX_chain_break
  → life==0 → hitParticle 缩放至 TileSize

PlayCantClickAnimation → Spine "click" + SFX_chain_click

PlayDestroyAnim → SFX_chain_break + hitParticle + 释放事件
```

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
