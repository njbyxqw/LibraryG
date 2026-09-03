---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：TrafficLights 红绿灯（5200/5201）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5200`(H) / `5201`(V) | 水平/垂直 |
| Group | `Blocker` | |
| MatchCount | `0` | 不可点击匹配 |
| 尺寸 | 3×1 / 1×3 Fixed | |
| 血量 | **3** | `Life: {"0": 3}` |
| 伤害源 | `8`（Match） | 消除匹配时造成范围伤害 |

## 二、数据层

- 无序列容器，无子牌体系
- 标准 Blocker：受 Match 攻击扣血 → 血量降到 ≤1 时销毁
- HasSeen 机制：DDA 交换时 **Swap 互换**，洗牌时 **Rebuild 重建**

## 三、逻辑层：5 条 ECA

### ① ReceiveDamage（`5200001`） `StopPolicy=1`

| 项目 | 内容 |
|------|------|
| 事件 | `Attack`（TargetSelector=1） |
| 条件 | `DamageSourceType=8`（Match）AND `Lives>=2` |
| 动作 | `HandleAttack` — 扣除 1 点血量 |

> **StopPolicy=1**：此行为命中后同事件其他行为不再执行。Lives>=2 时只扣血。

### ② DestroyWhenLifeZero（`5200002`） `Once=true`

| 项目 | 内容 |
|------|------|
| 事件 | `Attack` |
| 条件 | `DamageSourceType=8` AND `Lives<=1` |
| 动作 | `PlayDestroyAnim(AutoDestroy=true)` |

> **关键差异**：血量降到 ≤1 时即触发销毁（不是 ≤0）。Lives=3→2→1 时销毁，最多承受 2 次 Match 攻击。

### ③ TileDestroyed（`5200003`） `Once=true`

| 项目 | 内容 |
|------|------|
| 事件 | `TileDestroyed`（TargetSelector=1, SourceSelector=1） |
| 条件 | — |
| 动作 | `DestroyTile` — 最终销毁 |

### ④ AutoDestroy Candidate（`5200005`）— 保底候选注册

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeCandidateCheck` |
| 条件 | `VisibilityState=4` AND `BoardHasAtMostInteractableTile(0)` AND `BoardHasAtMostLockedTile(0, Destroy, Highlight)` AND **`OverBarHasAtMostInteractableTile(0)`** AND `Lives>=1` |
| 动作 | `RegisterBlockerGuaranteeCandidate(GuaranteeKey="Tile.TrafficLightsHorizontal.AutoDestroyWhenNoInteractableTiles")` |
| 触发事件 | `LevelEnterAnimationStepOneFinished` / `AddingToBarByClick` / `AutoMatchUse` / `ApplicationPendingEnd` |

> **独特条件**：`OverBarHasAtMostInteractableTile(0)` — 保底触发不仅要求棋盘无交互牌，**弃牌区也必须为空**。这是唯一有此限制的障碍牌。

### ⑤ AutoDestroyWhenNoInteractableTiles（`5200004`）— 保底执行

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeSelected`（TargetSelector=Self） |
| 条件 | `BlockerGuaranteeKeyEquals("Tile.TrafficLightsHorizontal.AutoDestroyWhenNoInteractableTiles")` |
| 动作 | `ChangeEffectState(TargetState=2)` → `PlayDestroyAnim` → `DestroyTile` |

## 四、调控层

### HasSeen 机制（blockerdda 变更）

| 场景 | 行为 |
|------|------|
| DDA 交换 | `ExchangeHasSeenWith()` **Swap 互换** |
| 洗牌 | `RebuildHasSeenFromCurrentVisibility()` **重建** |

### 保底机制（blockerdda 变更）

- **两阶段**：`BlockerGuaranteeCandidateCheck` → `BlockerGuaranteeSelected`
- **弃牌区联动**：`OverBarHasAtMostInteractableTile(0)` — 弃牌区还有牌时不触发保底
- **设计意图**：避免玩家弃牌区有牌可救场时，红绿灯被提前销毁

## 五、视图层

| 血量 | 外观 |
|------|------|
| 3 | 🟢 绿灯（完整） |
| 2 | 🟡 黄灯（警告） |
| 1 | 🔴 红灯（即将销毁） |
| 0 | 闪烁 → 消失 |

## 六、可见性 & 选中规则

| 状态 | 规则 |
|------|------|
| 被遮挡 | 不可交互 |
| 可见 | 被 Match 攻击扣血 |
| Lives≤1 | 触发销毁（最多 2 次攻击） |
| 死局保底 | 棋盘无交互牌 **+ 弃牌区为空** 时强制销毁 |

## 七、关联笔记

- [[障碍牌-Volcano]]（同为 Match 伤害源）
- [[障碍牌-SodaBox]]（同为大尺寸障碍）
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
