---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：Butterfly 蝴蝶（5020）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5020` | |
| Group | `Blocker` | |
| MatchCount | `0` | 不可点击匹配 |
| 尺寸 | 1×1 Fixed | |
| 血量 | **1** | `Life: {"0": 1}` |
| 点击行为 | 可点击（不进 Bar） | `SourceSelector=25` |

## 二、数据层

- 无序列容器，无子牌体系
- 无保底机制（Butterfly **不参与死局保底**）
- HasSeen 机制：DDA 交换时 **Swap 互换**，洗牌时 **Rebuild 重建**

## 三、逻辑层：2 条 ECA

### ① TileClicked（`5020001`）— 点击触发链式攻击

| 项目 | 内容 |
|------|------|
| 事件 | `TileClicked`（TargetSelector=1, **SourceSelector=25**） |
| 条件 | `OverBarHasSpace(3)` AND `Lives>=1` |
| 动作 | **EmitEvent(Attack, TST=2, DST=1)** → **CreateTile("ButterFly", CountMatch=1, CreatePosition="OverBar")** → EmitEvent(Attack, TST=1, DST=4) → EmitEvent(Attack, TST=4, DST=2) → `DestroyTile` |

三次 Attack 详情：

| Attack | TargetSelectorType | DamageSourceType | 含义 |
|--------|-------------------|-----------------|------|
| 1 | 2 | 1（Tap） | Tap 范围伤害 |
| 2 | 1 | 4（AddToBar） | AddToBar 范围伤害 |
| 3 | 4 | 2（AoE） | 大范围伤害 |

> **核心机制**：点击蝴蝶 → 发射三次范围攻击 → 在弃牌区生成一张新的 Butterfly → 蝴蝶自毁。
> 
> **弃牌区空间要求**：`OverBarHasSpace(3)` — 需要 3 个弃牌区空位（为生成的蝴蝶预留空间）。
> **CreatePosition="OverBar"**：新蝴蝶生成在弃牌区，可被拾取进 Bar。

### ② TileDestroyed（`5020002`） `Once=true`

| 项目 | 内容 |
|------|------|
| 事件 | `TileDestroyed`（TargetSelector=1, SourceSelector=1） |
| 条件 | — |
| 动作 | `DestroyTile` — 最终销毁 |

## 四、调控层

### HasSeen 机制（blockerdda 变更）

| 场景 | 行为 |
|------|------|
| DDA 交换 | `ExchangeHasSeenWith()` **Swap 互换** |
| 洗牌 | `RebuildHasSeenFromCurrentVisibility()` **重建** |

### 无保底机制

Butterfly **不参与死局保底**。与 Clock/Volcano/CandyBottle 等不同，Butterfly 没有 `BlockerGuaranteeCandidateCheck` 行为。

**设计原因**：Butterfly 可点击且能自毁，不需要额外的保底保护。

## 五、视图层

| 模块 | 职责 |
|------|------|
| Spine 动画 | 点击 → 蝴蝶飞舞 → 攻击特效 → 消失 |
| 新蝴蝶生成 | OverBar 位置创建新 Butterfly Tile |

## 六、可见性 & 选中规则

| 状态 | 规则 |
|------|------|
| 被遮挡 | 不可见不可点 |
| 可见 | 可点击 → 3 次攻击 + 生成新蝴蝶 + 自毁 |
| 弃牌区满 | 无法点击（OverBarHasSpace 检查） |
| 死局 | 无保底（Butterfly 不参与自动销毁） |

## 七、关联笔记

- [[障碍牌-Rocket]]（同样的三阶段 Attack 模式）
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
