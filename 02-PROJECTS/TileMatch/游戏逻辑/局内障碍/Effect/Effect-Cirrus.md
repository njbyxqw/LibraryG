---
tags: [TileMatch, 游戏逻辑, Effect牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 003
---

# Effect：Cirrus 云层 / Curtain 帷幕 / Mystery 神秘盒

---

# Cirrus 云层（40）

| 属性 | 值 |
|------|-----|
| EffectType | `40` |
| Priority | `7` |
| 尺寸 | 2×1 |
| 血量 | 2 |
| 透传 | ✅ |
| 初始状态 | `InitialState=1`（点击遮挡） |

## 逻辑层：3 条 ECA

### ① OnVisibilityChange — 去遮（`40001`） StopPolicy=1
| 事件 | 条件 | 动作 |
|------|------|------|
| StepTwoFinished / PrePropFinished / VisibilityChanged / 进Bar/自动/AfterAttack | Lives>=1 + VisibilityState=4 | `ChangeEffectClickOccluder(false)` |

### ② HandleTapAttack — 点击送Bar（`40002`）
| 事件 | 条件 | 动作序列 |
|------|------|---------|
| `Attack` | DamageSourceType=**1**(Tap) + ClickOccluder=false + Lives>=1 | PreCheckGameState → **LockTiles** → PlayDestroyAnim → **UnlockTiles** → **AddTilesToBar(TargetSelector=512)** → DestroyEffect |

> **唯一支持 Tap 点击的 Effect**。锁棋盘→播动画→解锁→Tile进Bar→云散。

## 视图层：CirrusEffectView

**实现接口**：`ITileViewCustomControl` + 领域事件

| 组件 | 作用 |
|------|------|
| `spine` (SkeletonAnimation) | Spine 模型（初始 disabled） |
| `particleBreak` | 破裂粒子 |
| `orderSkeletonRender` | 排序层 |

```
PlayDestroyAnim → PlayBreakAnimation（多阶段DOTween动画）:
  1. CaptureBreakAnimState: 保存左右Tile + spine原位置
  2. ApplyBreakSortingBoost: TileViews +1000 sorting + 启用spine
  3. MoveUpPhase: +0.02Y (0.001s)
  4. ScalePhase: ×1.1 (0.1s)
  5. SpreadPhase: 左右Tile平移0.3 + 旋转10° + 禁用spine + particleBreak
  6. RestoreBreakAnimState: 恢复原位

PlayDestroyAnimImmediate → particleBreak + 解锁 + 隐藏
```

---

# Curtain 帷幕（50）

| 属性 | 值 |
|------|-----|
| EffectType | `50` |
| Priority | `8` |
| 血量 | 1 |
| 透传 | ❌（默认） |
| 初始状态 | `InitialState=1` |
| 死局提示 | ❌ `CanJoinDeadlockHint=false` |

## 逻辑层：7 条 ECA — **唯一可切换开/闭的 Effect**

### 状态翻转逻辑

```
Attack(DamageSourceType=4)
  闭合(遮挡) ──────→ 打开(不遮挡)
  打开(不遮挡) ───→ 闭合(遮挡)
```

| 规则 | 行为 |
|------|------|
| **50001** | 首次可见→自动打开（仅一次，Blackboard防重入） |
| **50002** | 始终 HandleAttack |
| **50003** | `ClickOccluder=true` 被攻击 → `ChangeEffectClickOccluder(false)` 打开 |
| **50004** | `ClickOccluder=false` 被攻击 → `ChangeEffectClickOccluder(true)` 闭合 |
| **50007** | 死局且闭合 → **仅打开，不销毁** |

## 视图层：CurtainEffectView

| 组件 | 作用 |
|------|------|
| `spine` + `spineRender` | Spine 帷幕模型 |
| `hitParticle` | 击打粒子 |
| `ViewConfig.customEnterAnimDelayTime` | 入场延迟（基于Tile highlight） |

```
ChangeEffectClickOccluder:
  true(闭合) → SFX_curtain_switch + Spine "down"
  false(打开) → SFX_curtain_switch + Spine "up"

PlayCantClickAnimation → Spine "down_Click" + SFX_curtain_click_close

DoReduceEffect → SFX_curtain_break + hitParticle + Spine "End"
PlayDestroyAnim → 同 + DOVirtual.DelayedCall(延迟) → 释放

CustomEnterAnimDelay → 取决于 TileDataList 全部 Highlight
```

---

# Mystery 神秘盒（201）

| 属性 | 值 |
|------|-----|
| EffectType | `201` |
| Priority | `10`（最高） |
| 血量 | 1 |
| 处理点击 | ✅ `HandleClick=true` |
| 点击遮挡 | ✅ `IsClickOccluder=true` |
| 死局提示 | ❌ |

## 逻辑层：3 条 ECA — **唯一处理 EffectClick 的 Effect**

### ① EffectClick（`201001`）
| 事件 | 条件 | 动作序列 |
|------|------|---------|
| `EffectClick` | BarHasSpace(1) + Lives>=1 | PreCheckGameState → PlayClickAnimation → PlayDestroyAnim → DestroyEffect → **HandleForwardTileClick**（转发点击） → ReserveBarSpace |

> 盒子消失后转发点击到底层Tile，并预留Bar位置。不占Bar本身。

## 视图层：MysteryEffectView

| 组件 | 作用 |
|------|------|
| `spineAnimation` (SkeletonAnimation) | Spine `"Click"`(一次性) / `"Idle"`(循环) |
| `spineRender` (MeshRenderer) | 排序层 order+1 |
| `endParticle` | 打开粒子 |

```
PlayClickAnimation → base + PlayTileScaleAnimation
  → 每个TileView缩放 1.2×TileSize (0.08s, 延迟0.1s)

PlayCantClickAnimation → Spine "Click" (非WillDestroy状态)

ChangeColorState → WillDestroy: darkeningFactor=1.0; 否则: Spine "Idle" 循环

PlayDestroyAnim → SFX_mystery_break + 隐藏visualTransform
  → endParticle + DOVirtual.DelayedCall(0.45s) → 释放

PlayDestroyAnimImmediate → SFX_mystery_break + endParticle
```

---

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect牌-类型全览]]
