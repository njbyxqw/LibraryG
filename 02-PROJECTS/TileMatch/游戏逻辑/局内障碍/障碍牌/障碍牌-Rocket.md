---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：Rocket 火箭牌（5000）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5000` | |
| Group | `Blocker` | |
| MatchCount | `3` | 可点击匹配进 Bar |
| 尺寸 | 1×1 Fixed | |
| 血量 | 1 | |
| 配置文件 | `TileConfig/Rocket.json` | |

## 二、数据层

- MatchCount=3：3 个同花色火箭牌可匹配消除
- 深度控制：`RocketDepthStrategy.cs` 决定生成深度
- DDA 交换时 HasSeen **Swap 互换**

## 三、逻辑层：5 条 ECA

### ① Rocket_TileClicked（`5000001`）

| 事件 | 条件 | 动作 |
|------|------|------|
| `TileClicked`（SourceSelector=25） | `BarHasSpace(1)` AND `Lives>=1` | EmitEvent(Attack, TST=2, DST=1) → EmitEvent(Attack, TST=1, DST=4) → EmitEvent(Attack, TST=4, DST=2) → `AddToBar(Click)` |

三次 Attack：
| Attack | TargetSelectorType | DamageSourceType | 含义 |
|--------|-------------------|-----------------|------|
| 1 | 2 | 1 | Tap 伤害 |
| 2 | 1 | 4 | AddToBar 伤害 |
| 3 | 4 | 2 | 范围伤害 |

### ② Rocket_BarChanged（`5000002`）

| 事件 | 条件 | 动作 |
|------|------|------|
| `BarChanged` | — | `BarMatch` |

### ③ Rocket_BarMatched（`5000003`）

| 事件 | 条件 | 动作 |
|------|------|------|
| `BarMatched` | — | `PrepareAttack(TargetFilter="Rocket", MaxTarget=6)` |

### ④ Rocket_Attack_When_Direct_TileDestroyed（`5000004`）`Once=true`

| 事件 | 条件 | 动作 |
|------|------|------|
| `TileDestroyed` | `StateEquals(1)` | `EmitEvent(Attack, TST=4, DST=2)` |

### ⑤ Rocket_TileDestroyed（`5000005`）`Once=true`

| 事件 | 条件 | 动作 |
|------|------|------|
| `TileDestroyed` | — | `DestroyTile` |

## 四、调控层

- 无序列容器，不涉及序列 DDA
- HasSeen 机制：DDA 交换时 Swap 互换

## 五、视图层

| 模块 | 文件 |
|------|------|
| 视觉特效 | `RocketViewAction.cs` |
| 闪电球 | `RocketVLLightingViewAction.cs` |

## 六、关联笔记

- [[分析-RocketV2完整逻辑-v2（重构版）]]
- [[报告-RocketVL闪电球视觉替换]]
- [[障碍牌-类型全览]]
- [[../局内障碍知识库_MOC]]
