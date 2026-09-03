---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：Clock 时钟（5060）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5060` | |
| Group | `Blocker` | |
| MatchCount | `0` | 不可点击匹配 |
| 尺寸 | 1×1 Fixed | |
| 血量 | **3** | `Life: {"0": 3}` |
| 伤害源 | `4`（AddToBar） | 任意牌进 Bar 时造成 1 点伤害 |

## 二、数据层

- 无序列容器，无子牌体系
- 标准 Blocker：受攻击扣血 → 血归零销毁
- HasSeen 机制：DDA 交换时 **Swap 互换**，洗牌时 **Rebuild 重建**

## 三、逻辑层：4 条 ECA

### ① HandleAddAttack（`5060001`）

| 项目 | 内容 |
|------|------|
| 事件 | `Attack`（TargetSelector=1） |
| 条件 | `DamageSourceType=4`（AddToBar）AND `Lives>=1` |
| 动作 | `HandleAttack` — 扣除 1 点血量 |

> 任意牌被点击进 Bar 时触发 AddToBar 范围攻击，Clock 在范围内则扣 1 血。

### ② DestroyLogicWhenLifeZero（`5060002`） `Once=true`

| 项目 | 内容 |
|------|------|
| 事件 | `Attack` |
| 条件 | `DamageSourceType=4` AND `Lives<=0` |
| 动作 | `PlayDestroyAnim(AutoDestroy=false)` → `DestroyTile` |

> 血量归零的当次 Attack 事件中即触发销毁动画。

### ③ AutoDestroy Candidate（`5060005`）— 保底候选注册

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeCandidateCheck` |
| 条件 | `VisibilityState=4` AND `BoardHasAtMostInteractableTile(0)` AND `BoardHasAtMostLockedTile(0, Destroy, Highlight)` AND `Lives>=1` |
| 动作 | `RegisterBlockerGuaranteeCandidate(GuaranteeKey="Tile.Clock.AutoDestroyWhenNoInteractableTiles")` |
| 触发事件 | `LevelEnterAnimationStepOneFinished` / `AddingToBarByClick` / `AutoMatchUse` / `ApplicationPendingEnd` |

> **blockerdda 变更**：保底改为两阶段机制——先注册候选，等待 `BlockerGuaranteeSelected` 事件触发执行。

### ④ AutoDestroyWhenNoInteractableTiles（`5060004`）— 保底执行

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeSelected`（TargetSelector=Self） |
| 条件 | `BlockerGuaranteeKeyEquals("Tile.Clock.AutoDestroyWhenNoInteractableTiles")` |
| 动作 | `ChangeEffectState(TargetState=2)` → `PlayDestroyAnim` → `DestroyTile` |

> 当棋盘上无任何可交互 Tile 且无锁定 Tile 时，保底系统选择 Clock → 强制销毁释放格子。

## 四、调控层

### HasSeen 机制（blockerdda 变更）

| 场景 | 行为 |
|------|------|
| DDA 交换 | `ExchangeHasSeenWith()` **Swap 互换** |
| 洗牌 | `RebuildHasSeenFromCurrentVisibility()` **重建** |

### 保底机制（blockerdda 变更）

- **之前**：直接在多个事件上检查条件并执行
- **之后**：两阶段——`BlockerGuaranteeCandidateCheck` → 注册候选 → `BlockerGuaranteeSelected` → 执行

## 五、视图层

| 血量 | 外观 |
|------|------|
| 3 | 完整时钟 |
| 2 | 轻微破损 |
| 1 | 严重破损 |
| 0 | 销毁动画 → 消失 |

## 六、可见性 & 选中规则

| 状态 | 规则 |
|------|------|
| 被遮挡 | 不可交互 |
| 可见 | 被 AddToBar 攻击扣血 |
| 血量归零 | 销毁释放格子 |
| 死局保底 | 棋盘无交互牌时强制销毁 |

## 七、关联笔记

- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[障碍牌-Volcano]]
- [[../局内障碍知识库_MOC]]
