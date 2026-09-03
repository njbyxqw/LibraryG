---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：SodaBox 苏打盒（5120/5121）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5120`(H) / `5121`(V) | 水平/垂直方向 |
| Group | `Blocker` | |
| MatchCount | `0` | 不可点击匹配 |
| 尺寸 | 3×2 / 2×3 Fixed | 大尺寸障碍 |
| 血量 | **6** | `Life: {"0": 6}` |
| 伤害源 | `4`（AddToBar） | 进 Bar 时造成范围伤害 |

## 二、数据层

- 无序列容器，无子牌体系
- 大尺寸 Blocker：3×2（水平）或 2×3（垂直），占据 6 格
- 与 CardBox 同为 6 血，但**没有 StayAlive 机制**（0 血直接死）
- HasSeen 机制：DDA 交换时 **Swap 互换**，洗牌时 **Rebuild 重建**

## 三、逻辑层：4 条 ECA

### ① HandleAddToBarAttack（`5120001`）

| 项目 | 内容 |
|------|------|
| 事件 | `Attack`（TargetSelector=1） |
| 条件 | `DamageSourceType=4`（AddToBar） |
| 动作 | `HandleAttack` — 扣除 1 点血量 |

> 任意牌进 Bar 时触发 AddToBar 范围攻击，SodaBox 在范围内则扣 1 血。**没有 Lives 前置条件**，0 血时仍可能收到攻击事件。

### ② Destroy（`5120002`） `Once=true` `StopPolicy=1`

| 项目 | 内容 |
|------|------|
| 事件 | `Attack` |
| 条件 | `DamageSourceType=4` AND `Lives<=0` |
| 动作 | `PlayDestroyAnim(AutoDestroy=false)` → `DestroyTile` |

> **StopPolicy=1**：此行为命中后同事件其他行为不再执行，确保 0 血时只销毁不再扣血。

### ③ AutoDestroy Candidate（`5120005`）— 保底候选注册

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeCandidateCheck` |
| 条件 | `BoardHasAtMostInteractableTile(0)` AND `BoardHasAtMostLockedTile(0, Destroy, Highlight)` AND `Lives>=1` |
| 动作 | `RegisterBlockerGuaranteeCandidate(GuaranteeKey="Tile.SodaBoxHorizontal.AutoDestroyAgainstStuckInGame")` |
| 触发事件 | `LevelEnterAnimationStepOneFinished` / `AddingToBarByClick` / `AutoMatchUse` / `ApplicationPendingEnd` |

> ⚠️ 没有 `VisibilityState=4` 条件：即使被遮挡，只要棋盘无交互牌就注册保底候选。

### ④ AutoDestroyAgainstStuckInGame（`5120004`）— 保底执行

| 项目 | 内容 |
|------|------|
| 事件 | `BlockerGuaranteeSelected`（TargetSelector=Self） |
| 条件 | `BlockerGuaranteeKeyEquals("Tile.SodaBoxHorizontal.AutoDestroyAgainstStuckInGame")` |
| 动作 | `ChangeEffectState(TargetState=2)` → `PlayDestroyAnim` → `DestroyTile` |

> 保底销毁前先 `ChangeEffectState(2)` — 切换视觉效果，然后播放销毁动画。

## 四、调控层

### HasSeen 机制（blockerdda 变更）

| 场景 | 行为 |
|------|------|
| DDA 交换 | `ExchangeHasSeenWith()` **Swap 互换** |
| 洗牌 | `RebuildHasSeenFromCurrentVisibility()` **重建** |

### 保底机制（blockerdda 变更）

- **两阶段**：`BlockerGuaranteeCandidateCheck` → `BlockerGuaranteeSelected`
- **无 VisibilityState 限制**：即使被遮挡也可注册保底候选（区别 Clock/Volcano）
- **ChangeEffectState(2)**：保底执行时切换外观状态

## 五、视图层

| 血量 | 外观 |
|------|------|
| 6→5 | 完整苏打盒 |
| 4→3 | 轻微晃动 |
| 2→1 | 即将破碎 |
| 0 | 爆炸动画 → 消失 |

## 六、可见性 & 选中规则

| 状态 | 规则 |
|------|------|
| 被遮挡 | 不可交互（但仍可被保底候选注册） |
| 可见 | 被 AddToBar 攻击扣血 |
| 血量归零 | 销毁释放 6 格 |
| 死局保底 | 棋盘无交互牌时强制销毁 |

## 七、关联笔记

- [[障碍牌-CardBox]]（同为 6 血，但机制不同）
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
