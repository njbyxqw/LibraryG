---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：LightBulb 灯泡（5100）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5100` | |
| Group | `Blocker` | |
| MatchCount | `0` | 不可点击匹配 |
| 尺寸 | 1×1 Fixed | |
| 血量（单只） | **1** | `Life: {"0": 1}` |
| **BatchStrategyType** | **`1`** | 批次共享血量（核心机制） |
| 伤害源 | `4`（AddToBar） | 进 Bar 时造成范围伤害 |

## 二、数据层

### Batch 批次机制

> LightBulb 是唯一使用 **Batch 批次系统** 的障碍牌。

| 概念 | 说明 |
|------|------|
| 批次血量 | 所有同批次灯泡**共享一个血量池**，不是各自独立扣血 |
| TopMember | 批次"队头"——只有队头执行关键操作，避免重复 |
| 成员死亡 | 血量降到阈值时，个别灯泡逐个熄灭 |
| 批次销毁 | 批次总血量为 0 时，整批灯泡一起销毁 |

### HasSeen 机制（blockerdda 变更）

| 场景 | 行为 |
|------|------|
| DDA 交换 | `ExchangeHasSeenWith()` **Swap 互换** |
| 洗牌 | `RebuildHasSeenFromCurrentVisibility()` **Rebuild 重建** |

## 三、逻辑层：8 条 ECA

### ① UpdateBatchState（`5100001`）— 进场批次初始化

| 项目 | 内容 |
|------|------|
| 事件 | `LevelEnterAnimationStepOneFinished` |
| 条件 | `BatchIsTopMember`（队头） |
| 动作 | `UpdateBatchState(BatchDisplayType="AllNHighlight")` |

> 只有队头灯泡执行。进场时将批次所有灯泡设为高亮可见。

### ② BatchHandleAttack（`5100003`）— 批次伤害处理

| 项目 | 内容 |
|------|------|
| 事件 | `Attack`（TargetSelector=1） |
| 条件 | `DamageSourceType=4`（AddToBar）AND `BatchIsTopMember` AND `BatchTotalLife>=1` AND `BatchVisibilityState=4` |
| 动作 | `BatchHandleAttack` — 从批次血量池扣 1 血 |

> 任意灯泡受到 AddToBar 攻击时，由队头代理从批次血量池扣除。

### ③ BatchMemberStateChange（`5100004`） `Once=true` — 成员死亡处理

| 项目 | 内容 |
|------|------|
| 事件 | `ChangeBatchLives`（批次血量变更事件） |
| 条件 | `BatchMemberIsDead` |
| 动作 | `BatchMemberStateChange` — 标记该成员死亡 |

> 批次血量降到阈值时，个别灯泡标记为死亡并播放熄灭动画。每个成员只触发一次。

### ④ DestroyBatch（`5100005`） `Once=true` — 整批销毁

| 项目 | 内容 |
|------|------|
| 事件 | `ChangeBatchLives` |
| 条件 | `BatchTotalLife=0` AND `BatchIsTopMember` |
| 动作 | `DestroyBatch` — 销毁整个批次 |

> 批次总血量为 0 时队头执行销毁。

### ⑤ BatchPlayDestroyAnim（`5100006`） `Once=true` — 批次销毁动画

| 项目 | 内容 |
|------|------|
| 事件 | `ChangeBatchLives` |
| 条件 | `BatchTotalLife=0` AND `BatchIsTopMember` |
| 动作 | `BatchPlayDestroyAnim(AutoDestroy=true)` |

> 所有灯泡一起播放销毁动画。

### ⑥ TileDestroyed（`5100007`） `Once=true`

| 项目 | 内容 |
|------|------|
| 事件 | `TileDestroyed`（TargetSelector=1, SourceSelector=1） |
| 条件 | — |
| 动作 | `DestroyTile` — 单只灯泡最终销毁 |

### ⑦ AutoDestroy Candidate（`5100009`）— 保底候选注册

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeCandidateCheck` |
| 条件 | `VisibilityState=4` AND `BoardHasAtMostInteractableTile(0)` AND `BoardHasAtMostLockedTile(0, Destroy, Highlight)` AND `Lives>=1` AND `BatchIsTopMember` AND **`NoSameTileTypeDestroying`** |
| 动作 | `RegisterBlockerGuaranteeCandidate(GuaranteeKey="Tile.LightBulb.AutoDestroyWhenNoInteractableTiles")` |
| 触发事件 | `LevelEnterAnimationStepOneFinished` / `AddingToBarByClick` / `AutoMatchUse` / `ApplicationPendingEnd` / **`BatchDestroySequenceCompleted`** |

> **独特条件**：`NoSameTileTypeDestroying` — 如果有其他灯泡正在销毁中，不注册保底候选（避免竞态）。`BatchDestroySequenceCompleted` 额外触发事件。

### ⑧ AutoDestroy（`5100008`） `Once=true` — 保底执行

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeSelected`（TargetSelector=Self） |
| 条件 | `BlockerGuaranteeKeyEquals("Tile.LightBulb.AutoDestroyWhenNoInteractableTiles")` |
| 动作 | `BatchPlayDestroyAnim(AutoDestroy=true)` — 整批播放销毁动画 |

> 保底执行时用 `BatchPlayDestroyAnim` 而非逐个销毁，确保批次一致性。

## 四、调控层

### HasSeen 机制（blockerdda 变更）

| 场景 | 行为 |
|------|------|
| DDA 交换 | `ExchangeHasSeenWith()` **Swap 互换** |
| 洗牌 | `RebuildHasSeenFromCurrentVisibility()` **Rebuild 重建** |

### 保底机制（blockerdda 变更）

- **两阶段**：`BlockerGuaranteeCandidateCheck` → `BlockerGuaranteeSelected`
- **批次安全**：`NoSameTileTypeDestroying` 防止批次销毁竞态
- **`BatchDestroySequenceCompleted`**：批次销毁完成后重新检查保底

## 五、Batch 血量示例

假设关卡放置了 5 只灯泡（同批次），配置总血量 = 10：

| 事件 | 批次血量 | 存活灯泡 | 说明 |
|------|---------|---------|------|
| 进场 | 10 | 5 只全亮 | — |
| 第 1 次 AddToBar | 9 | 5 只全亮 | 血量高，无成员死亡 |
| 第 2 次 AddToBar | 8 | 5 只全亮 | — |
| … | … | … | — |
| 第 9 次 AddToBar | 1 | 1 只 | 血量低，逐个熄灭 |
| 第 10 次 AddToBar | **0** | 0 | 整批销毁 |

> 具体死亡率由 Batch 系统内部阈值决定（如血量 ≤ 成员数则开始死亡）。

## 六、视图层

| 状态 | 外观 |
|------|------|
| 批次血量充足 | 全部灯泡亮起 |
| 血量降低 | 个别灯泡逐个熄灭（顺序由批次系统决定） |
| 批次血量=0 | 所有灯泡一起播放销毁动画 → 消失 |
| 死局保底 | 整批播放 BatchPlayDestroyAnim |

## 七、可见性 & 选中规则

| 状态 | 规则 |
|------|------|
| 被遮挡 | 不可交互 |
| 可见 | 被 AddToBar 攻击 → 批次血量池扣血 |
| 批次血量=0 | 整批销毁释放所有格子 |
| 死局保底 | 棋盘无交互牌 + 无同类型正在销毁 → 整批销毁 |

## 八、关联笔记

- [[障碍牌-Clock]]（同为 AddToBar 伤害源）
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
