---
tags: [TileMatch, 游戏逻辑, Effect牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 015
---

# Effect：Pig 小猪护盾

## 版本差异

| 版本 | EffectType | 初始血量 | 视觉 |
|------|-----------|---------|------|
| Pig1 | 190 | 1 | A阶段（破碎） |
| Pig2 | 191 | 2 | B阶段（裂开） |
| Pig3 | 192 | 3 | C阶段（完好） |

**三者逻辑完全相同，仅初始血量不同。**

---

## 基础属性

| 属性 | 值 |
|------|-----|
| Priority | `3` |
| 尺寸 | 1×1（Fixed） |
| 透传伤害 | ❌ |
| 遮挡 | ✅ `IsOccluder: true` |
| 伤害源 | `8`（Match） |
| 配置文件 | `Pig1.json` `Pig2.json` `Pig3.json` |

---

## 数据层

- **DamageSourceType=`8`**：仅 Match 消除伤害
- 3 层血量配置：`Life: {"0": N}` N=1/2/3
- 死局自毁兜底

---

## 逻辑层：4 条 ECA

### ① HandleMatchAttack（`191001`）
| 事件 | 条件 | 动作 |
|------|------|------|
| `Attack` | DamageSourceType=8 + Lives>=1 | `HandleAttack` |

### ② Destroy有命（`191002`） StopPolicy=1
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectDestroyed` | Lives>=1 | `PlayDestroyAnim(AutoDestroy=false)` → `DestroyEffect` |

### ③ Destroy没命（`191003`） StopPolicy=1
| 事件 | 条件 | 动作 |
|------|------|------|
| `EffectDestroyed` | Lives<=0 | `DestroyEffect`（不播动画） |

### ④ 死局自毁（`191004`）
| 事件 | 条件 | 动作 |
|------|------|------|
| 进场/进Bar/道具/自动 | 棋盘无交互 + 无锁定 + Lives>=1 | `ChangeEffectState(2)` → `PlayDestroyAnim` → `DestroyEffect` |

---

## 视图层：PigEffectView

**最复杂的 Effect View** — 完整的 idle 循环状态机

| 组件 | 作用 |
|------|------|
| `spine` + `spineRender` | Spine 小猪模型 |
| `pigParticle3To2` | 3→2 血量过渡粒子 |
| `pigParticle2To1` | 2→1 血量过渡粒子 |
| `pigParticle1To0` | 1→0 死亡粒子 |

### Spine 动画状态机

```
血量=3 (C阶段)          血量=2 (B阶段)          血量=1 (A阶段)
  C_idle (静态)           B_idle (静态)           A_idle (静态)
  C_idle2 (随机)          B_idle2 (随机)          A_idle2 (随机)
  C_Click (点击)          B_Click (点击)          A_idle3 (随机)
                                                   A_Click (点击)
```

### Idle 循环系统

```
StartIdleLoop:
  → PlayStaticIdleWithRandomDuration
    → 设置 TimeScale 为随机 1~3 秒
    → OnIdleAnimationComplete → 等待 3~5 秒
      → PlayRandomIdleAnimation (随机选变体)
        → OnRandomIdleAnimationComplete → 等待 3~5 秒
          → PlayRandomIdleAnimation (循环)
```

### 关键逻辑

```
ChangeEffectLives(delta<0) → DoReduceEffect
  → SFX_piggy_break1/2 (根据life)
  → 播放对应过渡粒子 (3→2: 3To2 / 2→1: 2To1 / 1→0: 1To0)
  → UpdateIdleAnimationForLife (切换动画阶段)

PlayCantClickAnimation → 停止idle → 播放对应Click(A/B/C) → 完成后恢复idle

PlayDestroyAnim → 停止idle → SFX_piggy_break2 → pigParticle1To0

ChangeColorState(dark≥0.99) → StartIdleLoop
                        else → StopIdleLoop
```

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
