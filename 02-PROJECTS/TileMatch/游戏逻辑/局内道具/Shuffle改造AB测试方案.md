---
title: Shuffle改造AB测试方案
type: analysis
tags:
  - TileMatch
  - 游戏逻辑
  - Shuffle
  - AB测试
status: finalized
date: 2026-07-02
cat_order: 007
---

# Shuffle 改造 AB 测试方案

## 背景

原版 Shuffle 道具只帮助最右侧 1 种类型的盲区牌，导致玩家在多类型盲区场景下体验不佳。本方案对 Shuffle 选牌算法进行改造，并通过 AB 测试验证改造效果。

## 原版问题分析

### 原版行为

- Shuffle 仅对最右侧的 1 种类型进行盲区消除辅助
- 当 Bar 中存在多种类型的盲区牌时，无法有效改善局面

### 盲区分析

| 场景 | 原版表现 | 问题 |
|------|----------|------|
| 单类型盲区 | 帮助消除 | 正常 |
| 多类型盲区 | 仅帮最右侧 1 种 | 其余类型仍无法消除 |
| 混合盲区 | 效果有限 | 玩家体验差，道具感知价值低 |

## 改造方案：多类型优先配对算法

### 选牌排序规则

改造后的 Shuffle 选牌算法引入多类型优先配对策略：

```
排序优先级：needCount ASC → nonHighlightCount DESC
```

| 排序字段 | 方向 | 说明 |
|----------|------|------|
| `needCount` | ASC（升序） | 需要的牌数少的类型优先处理，快速消除 |
| `nonHighlightCount` | DESC（降序） | 非高亮牌数多的类型优先处理，覆盖更多盲区 |

### 算法流程

1. 收集 Bar 中所有需要消除的类型及其需求数
2. 按 `needCount ASC, nonHighlightCount DESC` 排序
3. 依次为每种类型寻找配对牌
4. 多类型并行消除，提升整体效果

## 概率梯度 + 保底机制

### 设计目标

避免 Shuffle 过于强大（降低难度）或过于弱小（道具无感），通过概率梯度平滑过渡。

### remainingSlots 阈值梯度

根据 Bar 剩余槽位（`remainingSlots`）占比，划分 4 个梯度区间：

| remainingSlots 占比 | Shuffle 帮助概率 | 说明 |
|---------------------|------------------|------|
| **0%**（Bar 满） | 最高 | 紧急情况，最大力度帮助 |
| **0% ~ 30%** | 高 | 接近危险，高概率触发 |
| **30% ~ 70%** | 中 | 正常区间，中等概率 |
| **70% ~ 100%** | 低 | 空间充足，低概率帮助 |

```
概率梯度示意：

帮助概率
  ↑
  │  ████
  │  ████  ████
  │  ████  ████  ████
  │  ████  ████  ████  ████
  └─────────────────────────→ remainingSlots 占比
     0%   30%   70%  100%
```

### 同关卡保底步长

- 同一关卡内，`shuffleUseCount` 每次使用后保底步长递增 **20%**
- 即每次使用 Shuffle 后，下次触发帮助的概率提升 20%
- 防止玩家连续使用 Shuffle 都无法获得有效帮助

```
第1次 Shuffle：基础概率 P
第2次 Shuffle：P × 1.2
第3次 Shuffle：P × 1.44
...
```

## AB 测试设计

### 分组方案

| 组别 | 策略 | 说明 |
|------|------|------|
| **对照组（A组）** | 一直帮 | 原版逻辑，每次 Shuffle 都最大化帮助 |
| **测试组（B组）** | 概率梯度 + 保底 | 改造逻辑，按梯度概率 + 保底步长 |

### 核心指标

| 指标 | 说明 | 期望方向 |
|------|------|----------|
| 关卡通关率 | 使用 Shuffle 后的通关率 | B组 ≥ A组 |
| Shuffle 使用次数 | 单关卡平均使用次数 | B组 ≤ A组 |
| 道具购买转化率 | Shuffle 相关购买 | B组 > A组 |
| 玩家留存率 | 次日/7日留存 | B组 ≥ A组 |
| 关卡流失率 | 使用 Shuffle 后仍放弃的比率 | B组 < A组 |

### 埋点方案

| 埋点事件 | 参数 | 触发时机 |
|----------|------|----------|
| `shuffle_trigger` | groupId, levelId, remainingSlots, shuffleUseCount | 玩家点击 Shuffle |
| `shuffle_result` | helpedTypes, matchCount, isFullHelp | Shuffle 执行完成 |
| `shuffle_level_end` | levelId, result(win/lose), totalShuffleCount | 关卡结束 |
| `shuffle_purchase` | itemId, price, groupId | 购买 Shuffle 道具 |

### 决策标准

| 条件 | 决策 |
|------|------|
| B组通关率 ≥ A组 **且** 留存率 ≥ A组 | 全量上线改造方案 |
| B组通关率显著 > A组 **但** 留存率 < A组 | 调整概率梯度参数后重新测试 |
| B组通关率 < A组 | 放弃改造，保留原版逻辑 |
| B组购买转化率显著提升 | 优先上线改造方案 |

## 关联

- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]]文档

- [[分析-局内道具逻辑梳理]] - 局内道具完整架构与逻辑分析
