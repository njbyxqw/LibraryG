---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：CandyBottle 糖果瓶（5170）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5170` | |
| Group | `Blocker` | |
| MatchCount | `0` | 不可点击匹配 |
| 尺寸 | 1×1 Fixed | |
| 血量 | **3** | `Life: {"0": 3}` |
| 伤害源 | `8`（Match） | 消除匹配时造成范围伤害 |

## 二、数据层

- 无序列容器，无子牌体系
- 标准 Blocker：受 Match 攻击扣血
- **独特机制**：血量降到 ≤1 时触发 `SelectAndTransformTiles` — 将周围 Tile 随机转换为同花色
- HasSeen 机制：DDA 交换时 **Swap 互换**，洗牌时 **Rebuild 重建**

## 三、逻辑层：5 条 ECA

### ① HandleMatchAttack（`5170001`） `StopPolicy=1`

| 项目 | 内容 |
|------|------|
| 事件 | `Attack`（TargetSelector=1） |
| 条件 | `Lives>=2` AND `DamageSourceType=8`（Match）AND `VisibilityState=4` |
| 动作 | `HandleAttack` — 扣除 1 点血量 |

> **StopPolicy=1**：此行为命中后，同一事件的其他 CandyBottle 行为不再执行。Lives>=2 时只扣血，不触发变形。

### ② SelectAndTransformWhenLifeLow（`5170002`） `Once=true`

| 项目 | 内容 |
|------|------|
| 事件 | `Attack` |
| 条件 | `Lives<=1` AND `DamageSourceType=8` AND `VisibilityState=4` |
| 动作 | **`SelectAndTransformTiles`** → `PlayDestroyAnim(AutoDestroy=true)` |

> **核心机制**：血量降到 1 或以下的当次攻击，不执行 HandleAttack，而是触发 SelectAndTransformTiles 将周围牌转化为同花色，然后自毁。

### ③ TileDestroyed（`5170003`） `Once=true`

| 项目 | 内容 |
|------|------|
| 事件 | `TileDestroyed`（TargetSelector=1, SourceSelector=1） |
| 条件 | — |
| 动作 | `DestroyTile` — 最终销毁 |

### ④ AutoDestroy Candidate（`5170005`）— 保底候选注册

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeCandidateCheck` |
| 条件 | `BoardHasAtMostInteractableTile(0)` AND `BoardHasAtMostLockedTile(0, Destroy, Highlight)` AND `Lives>=1` |
| 动作 | `RegisterBlockerGuaranteeCandidate(GuaranteeKey="Tile.CandyBottle.AutoDestroyWhenNoInteractableTiles")` |
| 触发事件 | `LevelEnterAnimationStepOneFinished` / `AddingToBarByClick` / `AutoMatchUse` / `ApplicationPendingEnd` |

> ⚠️ 与 Clock/Volcano 不同：CandyBottle 的保底候选**没有 VisibilityState=4 条件**（可见性不限）。

### ⑤ AutoDestroyWhenNoInteractableTiles（`5170004`） `Once=true` — 保底执行

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeSelected`（TargetSelector=Self） |
| 条件 | `BlockerGuaranteeKeyEquals("Tile.CandyBottle.AutoDestroyWhenNoInteractableTiles")` |
| 动作 | **`SelectAndTransformTiles`** → `PlayDestroyAnim` → `DestroyTile` |

> **关键差异**：保底销毁时**也会触发 SelectAndTransformTiles**（与自然死亡一致），不像 Volcano 保底跳过特殊技能。

## 四、调控层

### HasSeen 机制（blockerdda 变更）

| 场景 | 行为 |
|------|------|
| DDA 交换 | `ExchangeHasSeenWith()` **Swap 互换** |
| 洗牌 | `RebuildHasSeenFromCurrentVisibility()` **重建** |

### 保底机制（blockerdda 变更）

- **两阶段**：`BlockerGuaranteeCandidateCheck` → `BlockerGuaranteeSelected`
- **与自然死亡一致**：保底销毁也执行 `SelectAndTransformTiles`（区别于 Volcano）
- **无 VisibilityState 限制**：候选注册不需要可见（区别于 Clock/Volcano）

## 五、视图层

| 血量 | 外观 |
|------|------|
| 3 | 完整糖果瓶 |
| 2 | 轻微裂痕 |
| 1 | 即将破碎 → **变形触发** |
| 0 | 变形动画 → 周围牌变色 → 消失 |

## 六、可见性 & 选中规则

| 状态 | 规则 |
|------|------|
| 被遮挡 | 不可交互 |
| 可见（VisibilityState=4） | 被 Match 攻击扣血 |
| Lives≤1 Match 攻击 | 触发 SelectAndTransformTiles → 自毁 |
| 死局保底 | 棋盘无交互牌时强制销毁（也触发 SelectAndTransformTiles） |

## 七、关联笔记

- [[障碍牌-类型全览]]
- [[障碍牌-Volcano]]
- [[障碍牌-Clock]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
