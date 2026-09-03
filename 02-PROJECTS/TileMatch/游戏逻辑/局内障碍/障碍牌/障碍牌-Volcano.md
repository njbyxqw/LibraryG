---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：Volcano 火山（5080）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5080` | |
| Group | `Blocker` | |
| MatchCount | `0` | 不可点击匹配 |
| 尺寸 | 1×1 Fixed | |
| 血量 | **3** | `Life: {"0": 3}` |
| 伤害源 | `8`（Match） | 消除匹配时造成范围伤害 |

## 二、数据层

- 无序列容器，无子牌体系
- 标准 Blocker：受 Match 攻击扣血 → 血归零时**喷发攻击**
- 独特机制：死亡时发射 `PrepareAttack(TargetFilter="Volcano", MaxTarget=3)` 攻击最多 3 个目标
- HasSeen 机制：DDA 交换时 **Swap 互换**，洗牌时 **Rebuild 重建**

## 三、逻辑层：4 条 ECA

### ① ReceiveDamage（`5080001`）

| 项目 | 内容 |
|------|------|
| 事件 | `Attack`（TargetSelector=1） |
| 条件 | `DamageSourceType=8`（Match）AND `Lives>=1` |
| 动作 | `HandleAttack` — 扣除 1 点血量 |

> 附近牌消除匹配时触发 Match 范围攻击，Volcano 在范围内则扣 1 血。

### ② DestroyLogicWhenLifeZero（`5080002`） `Once=true`

| 项目 | 内容 |
|------|------|
| 事件 | `Attack` |
| 条件 | `DamageSourceType=8` AND `Lives<=0` |
| 动作 | **`PrepareAttack(TargetFilter="Volcano", MaxTarget=3)`** → `PlayDestroyAnim` → `DestroyTile` |

> **核心差异**：血量归零时不是简单销毁，而是先发射 PrepareAttack——选择棋盘上最多 3 个 Volcano 目标进行攻击（连锁喷发）。

### ③ AutoDestroy Candidate（`5080004`）— 保底候选注册

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeCandidateCheck` |
| 条件 | `VisibilityState=4` AND `BoardHasAtMostInteractableTile(0)` AND `BoardHasAtMostLockedTile(0, Destroy, Highlight)` AND `Lives>=1` |
| 动作 | `RegisterBlockerGuaranteeCandidate(GuaranteeKey="Tile.Volcano.AutoDestroyWhenNoInteractableTiles")` |
| 触发事件 | `LevelEnterAnimationStepOneFinished` / `AddingToBarByClick` / `AutoMatchUse` / `ApplicationPendingEnd` |

### ④ AutoDestroyWhenNoInteractableTiles（`5080003`）— 保底执行

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeSelected`（TargetSelector=Self） |
| 条件 | `BlockerGuaranteeKeyEquals("Tile.Volcano.AutoDestroyWhenNoInteractableTiles")` |
| 动作 | `PlayDestroyAnim` → `DestroyTile` |

> ⚠️ 保底销毁时**不会**触发 PrepareAttack（与自然死亡不同）。保底只是为了释放格子。

## 四、调控层

### HasSeen 机制（blockerdda 变更）

| 场景 | 行为 |
|------|------|
| DDA 交换 | `ExchangeHasSeenWith()` **Swap 互换** |
| 洗牌 | `RebuildHasSeenFromCurrentVisibility()` **重建** |

### 保底机制（blockerdda 变更）

- **之前**：直接在多个事件上检查条件并执行
- **之后**：两阶段——`BlockerGuaranteeCandidateCheck` → 注册候选 → `BlockerGuaranteeSelected` → 执行
- **注意**：保底销毁不触发 PrepareAttack，与自然死亡行为不同

## 五、视图层

| 血量 | 外观 |
|------|------|
| 3 | 完整火山 |
| 2 | 轻微冒烟 |
| 1 | 即将喷发 |
| 0 | **喷发动画** → 消失 |

## 六、可见性 & 选中规则

| 状态 | 规则 |
|------|------|
| 被遮挡 | 不可交互 |
| 可见 | 被 Match 攻击扣血 |
| 血量归零 | **喷发攻击** → 销毁释放格子 |
| 死局保底 | 棋盘无交互牌时强制销毁（不喷发） |

## 七、关联笔记

- [[障碍牌-类型全览]]
- [[障碍牌-Clock]]
- [[障碍牌-CandyBottle]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
