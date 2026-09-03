---
tags: [TileMatch, 游戏逻辑, 障碍牌]
status: draft
date: 2026-07-15
type: reference
---

# 障碍牌：JokerFlip 王牌翻牌（5150）

## 一、基础属性

| 属性 | 值 | 说明 |
|------|-----|------|
| TileType | `5150` | |
| Group | `Blocker` | |
| MatchCount | `0` | |
| 尺寸 | 1×1 Fixed | |
| 血量 | 1 | |
| CoveredTileIgnoreVisible | `false` | |
| CustomTileController | `FlipTileController` | 与 Flip 共用 |
| Capabilities.CanExposeSequenceMembersToDeadlockHint | `false` | |
| EditorDefaults.Sequences | `[1001, -1]` | 预置 Joker + Random |

## 二、与 Flip 的区别

| 维度 | Flip | JokerFlip |
|------|------|----------|
| 序列内容 | 任意花色 | **Joker(1001) + 任意花色** |
| 花色去重（之前） | Prefer | Prefer |
| 花色去重（之后） | **Prefer（保留）** | **移除** |
| DDA 保护（之前） | 有 | 有 |
| DDA 保护（之后） | **移除** | **移除** |
| Behaviour 数 | 6 | 6（逻辑完全一致） |

> **blockerdda 分支关键变更**：JokerFlip 的花色去重被移除（Flip 保留）。这意味着 JokerFlip 序列内可能出现重复花色的子牌。

### Joker 万能牌机制
- Joker(1001) 可匹配任意花色
- 翻出后作为万能牌进 Bar，参与 3 消匹配

## 三、逻辑层：6 条 ECA

与 Flip 完全一致（BehaviourId 前缀为 `515` 而非 `511`），此处不再重复。

详见 [[障碍牌-Flip#三、逻辑层：ECA 行为引擎（6 条规则）]]

## 四、调控层变更

| 项目 | 之前 | 之后 |
|------|------|------|
| 花色去重 | Prefer | **None（移除）** |
| DDA 保护 | ProtectSequenceChildrenFromDda | **移除** |
| HasSeen (DDA) | RefreshSeen | **Swap 互换** |
| HasSeen (洗牌) | RefreshSeen | **Rebuild 重建** |

## 五、关联笔记

- [[障碍牌-Flip]]
- [[障碍牌-类型全览]]
- [[报告-blockerdda分支调控逻辑变更排查]]
- [[../局内障碍知识库_MOC]]
