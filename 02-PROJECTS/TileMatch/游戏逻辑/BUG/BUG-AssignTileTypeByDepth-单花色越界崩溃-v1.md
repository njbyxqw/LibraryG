---
title: BUG-AssignTileTypeByDepth-单花色越界崩溃-v1
tags: [BUG, AssignTileTypeByDepth, 崩溃, 花色分配, 边界条件]
status: finalized
type: bug-record
date: 2026-07-24
---

# BUG：AssignTileTypeByDepth 单花色关卡越界崩溃

## 概要

关卡只配置 1 种花色时，`AssignTileTypeByDepthStrategy` 在 `RandomizeTileTypeWithLevelConfig` 中抛出 `ArgumentOutOfRangeException`，导致游戏初始化崩溃。

## 复现条件

- 关卡 `LevelConfig.TileTypes` 仅包含 **1 种花色**（花色数量 < 3）
- 触发 `GetTileTypeListForNonBonus` 的 MinElements 保护逻辑

## 崩溃栈

```
ArgumentOutOfRangeException: Index was out of range.
  at AssignTileTypeByDepthStrategy.RandomizeTileTypeWithLevelConfig (line 753)
  at AssignTileTypeByDepthStrategy.InvokeStrategy (line 85)
```

崩溃行（`AssignTileTypeByDepthStrategy.cs:753`）：

```csharp
levelTileConfig.TileType = tileTypes[types[typeIndex]].TileType;
```

## 根因分析

### 问题链路

```
TileTypes = [花色A]（1种）
    ↓
GetTileTypeListForNonBonus():
    levelConfigCount = 1
    levelConfigCount < MinElements(3) → 尝试补到 3
    adjust = 1 - 3 = -2
    levelConfigCount = 1 - (-2) = 3   ← out 参数被改成 3
    但 3 >= fullList.Count(1) → return fullList  ← 实际只返回 1 个元素！
    ↓
tileTypeCount = 3（out 参数），tileTypeList.Count = 1  ← 不一致！
    ↓
types 按 tileTypeCount=3 生成花色索引：[0, 0, 0, 1, 1, 1, 2, 2, 2, ...]
    ↓
RandomizeTileTypeWithLevelConfig:
    tileTypes[types[0]] → tileTypes[0] ✓
    tileTypes[types[1]] → tileTypes[1] ✗ → 越界崩溃
```

### 问题代码（`GetTileTypeListForNonBonus`，第 91-123 行）

```csharp
private List<TileTypeConfig> GetTileTypeListForNonBonus(out int levelConfigCount)
{
    var fullList = _gameContext.LevelConfig.TileTypes;
    levelConfigCount = fullList.Count;  // = 1
    // ...
    int adjust = excel.v2ElementAjust;  // 假设 = 0
    if (adjust < 0) adjust = 0;
    if (levelConfigCount - adjust < MinElements)  // 1 - 0 < 3 → true
    {
        adjust = levelConfigCount - MinElements;  // adjust = -2
    }
    levelConfigCount -= adjust;  // = 1 - (-2) = 3

    if (levelConfigCount >= fullList.Count)  // 3 >= 1 → true
    {
        return fullList;  // ← 只返回 1 个元素！out 参数却是 3
    }
    // ...
}
```

**问题**：当花色数不足 3 时，代码试图通过调整 `adjust` 把 `levelConfigCount` 补到 3，但 `levelConfigCount >= fullList.Count` 判定直接短路返回原始列表，导致 **out 参数与返回列表长度不一致**。

## 影响范围

- 只影响花色数 < 3 的关卡（生产环境极少见，测试关卡可能遇到）
- Bonus 关卡不受影响（走 Bonus 分支，固定 3 花色）
- 走 `InitializeTypeIndexByDepth`（非 Original）分池路径的关卡不受影响，因为它显式按 `targetCount` 分配列表长度

## 关联

- [[_MOC|TileMatch 知识库 MOC]]

文档

- [[分析-AssignTileTypeByDepth分池打乱策略-v1|AssignTileTypeByDepth 分池打乱策略]] — 完整算法流程
- `AssignTileTypeByDepthStrategy.cs` — 源码文件

## 相关提交历史

无（此为首次发现）
