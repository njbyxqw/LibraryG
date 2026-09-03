---
title: 分析-RocketV2技术实现-v1
date: 2026-06-24
type: analysis
status: finalized
version: v1
tags: [TileMatch, 游戏逻辑, Rocket]
cat_order: 002
---

# RocketV2 技术实现详解

> 火箭牌 V2 重构的技术实现文档，包含代码级详细分析

---

## 一、概述

RocketV2 重构（提交 `e83f832fe7`，2026-06-24 10:58）涉及 44 个文件变更，2655 insertions，198 deletions。

核心改进：
1. 生成策略从 `RocketNormalStrategy` 改为 `RocketDepthStrategy`
2. `PrepareChainedAttackAction` 替代旧的 `PrepareAttack`，逻辑层预计算所有波次
3. `RocketPrimaryTargetFilter` 让主波 Rocket 与普通牌同权重
4. `RocketChainTargetFilter` 链式波优先普通牌，不足兜底火箭

---

## 二、生成规则优化

### 2.1 RocketDepthStrategy 深度分桶

**文件**: `RocketDepthStrategy.cs`

**核心逻辑**:
```csharp
// 深度分桶算法
int depth = tileData.Depth;
int bucket = depth / DEPTH_BUCKET_SIZE;  // BUCKET_SIZE = 5
float rocketProbability = GetRocketProbabilityByBucket(bucket);

// 连胜动态调节
if (winStreak > 3)
{
    rocketProbability *= 1.2f;  // 连胜时提高火箭概率
}
```

**配置常量**:
| 常量 | 值 | 说明 |
|------|-----|------|
| `BASE_ROCKET_COUNT` | 3 | 基础火箭生成数量 |
| `ROCKET_INCREMENT_THRESHOLD` | 5 | >28 组时每多 5 组 +1 火箭 |
| `DEPTH_BUCKET_SIZE` | 5 | 深度分桶大小 |

### 2.2 Highlight 兜底

当深度分桶后火箭数量不足时，使用 Highlight 牌兜底：
```csharp
int needed = targetRocketCount - generatedRocketCount;
if (needed > 0)
{
    List<TileData> highlightTiles = GetHighlightTiles();
    // 优先选择深度浅的 Highlight 牌转换为火箭
}
```

---

## 三、Lucky Rocket（幸运火箭）

### 3.1 概率映射表

**文件**: `LevelRocketData.cs`

```csharp
public int GetRocketLuckyProbability()
{
    // 返回 0-100 的概率值
    return RocketLuckyProbability;
}
```

**数据流**:
```
LevelRocketData.GetRocketLuckyProbability()
  → DataBridge.RocketLuckyProbability
  → Action 传递
  → RocketVLLightningViewAction
```

### 3.2 录像兼容

Lucky Rocket 的概率计算在逻辑层完成，录像回放时使用相同的随机数种子，确保录像兼容。

---

## 四、Chain Rocket（链式攻击）

### 4.1 触发条件

```csharp
if (rocketCount >= CHAIN_ROCKET_THRESHOLD)  // THRESHOLD = 2
{
    // 触发链式攻击
    PrepareChainedAttackAction();
}
```

### 4.2 波次规则

**文件**: `PrepareChainedAttackActionInvoker.cs`

```csharp
public async Task ProcessAsync(ChainedAttackActionData data)
{
    // 主波：RocketPrimaryTargetFilter（与普通牌同权重）
    List<TileData> primaryTargets = FilterPrimaryTargets(data);
    
    // 链式波：RocketChainTargetFilter（优先普通牌，不足兜底火箭）
    for (int wave = 1; wave <= data.ChainCount; wave++)
    {
        List<TileData> chainTargets = FilterChainTargets(data, wave);
        // 执行攻击
    }
}
```

### 4.3 目标筛选

**RocketPrimaryTargetFilter**:
- 普通牌权重 = 1.0
- 火箭牌权重 = 1.0（同权重，随机选）

**RocketChainTargetFilter**:
- 普通牌权重 = 1.0
- 火箭牌权重 = 0.5（优先普通牌）

---

## 五、RocketVL 闪电球视觉替换

### 5.1 方案

编辑器 Rocket 输入框输入 3 → 火箭牌使用闪电球视觉特效（RocketVL）

**火箭攻击逻辑不动，仅换视觉层**

### 5.2 新建文件

1. `RocketVLLightningViewAction.cs`
   - 接收 `ChainedAttackActionData`
   - 展平所有 Wave 目标为 `List<TileData>`
   - 分 2 组播放闪电球动画 + 闪电击中特效

2. `RocketVLLightningViewActionController.cs`
   - Controller 壳子

### 5.3 修改文件（10 个）

| 文件 | 改动 |
|------|------|
| `ICustomViewActionController.cs` | 枚举加 `RocketVLLighting` |
| `CustomData.cs` | 加 `RocketMode` 字段 + `SetRocketMode()` |
| `DataBridge.cs` | 加 `RocketMode` 字段（默认 0） |
| `TestControlView.cs` | `OnRocketEditorEnd` 识别 mode=3 |
| `LevelEditorData.cs` | 加 `RocketMode` 字段 |
| `LevelEditorConfig.cs` | 加 `RocketMode` 字段 |
| `LevelEditorConfigWriter.cs` | 写 `RocketMode` 到 JSON |
| `TileMatchViewController.ViewActions.cs` | 注册 `RocketVLLightningController` |
| `TileMatchGame.RecordController.cs` | Trial 模式传 `RocketMode` 到 DataBridge |
| `PrepareChainedAttackActionInvoker.cs` | mode==3 路由到 `RocketVLLighting` |

### 5.4 数据流

```
编辑器输入 3 
  → LevelEditorData.RocketMode=3 
  → CustomData.SetRocketMode(3)
  → RecordController 
  → DataBridge.RocketMode=3
  → PrepareChainedAttackActionInvoker.ProcessAsync()
    → ResolveControllerType() 检测 mode=3 
    → RocketVLLighting
    → RocketVLLightningViewAction.DoAction(ChainedAttackActionData)
      → 展平 Waves 
      → 2 组闪电球动画 
      → AfterAttack
```

---

## 六、测试验收清单

### 6.1 生成规则

- [ ] 深度分桶正确（不同深度牌的火箭概率）
- [ ] 连胜动态调节正确（winStreak > 3 时概率提高）
- [ ] Highlight 兜底正确（火箭数量不足时转换 Highlight）
- [ ] 基础火箭数量 = 3
- [ ] >28 组时每多 5 组 +1 火箭

### 6.2 Lucky Rocket

- [ ] 概率映射表正确
- [ ] 数据流贯通（LevelRocketData → DataBridge → Action）
- [ ] 录像兼容（回放时概率一致）

### 6.3 Chain Rocket

- [ ] 触发条件正确（rocketCount >= 2）
- [ ] 波次规则正确（主波 + 链式波）
- [ ] 目标筛选正确（主波同权重，链式波优先普通牌）
- [ ] 事件抑制正确（链式攻击时抑制重复事件）

### 6.4 RocketVL

- [ ] 编辑器输入 3 正确触发 RocketVL
- [ ] 闪电球动画正确播放（2 组）
- [ ] 闪电击中特效正确
- [ ] 球体动画已移除

---

## 七、涉及文件清单

### 7.1 核心文件

- `RocketDepthStrategy.cs` — 深度分桶生成策略
- `PrepareChainedAttackActionInvoker.cs` — 链式攻击调用器
- `RocketPrimaryTargetFilter.cs` — 主波目标筛选
- `RocketChainTargetFilter.cs` — 链式波目标筛选
- `LevelRocketData.cs` — 火箭配置数据
- `DataBridge.cs` — 数据桥接

### 7.2 View 层文件

- `RocketVLLightningViewAction.cs` — 闪电球视觉动作
- `RocketVLLightningViewActionController.cs` — 闪电球控制器
- `TileMatchViewController.ViewActions.cs` — View 层注册

### 7.3 编辑器文件

- `TestControlView.cs` — 编辑器测试控制
- `LevelEditorData.cs` — 编辑器数据
- `LevelEditorConfig.cs` — 编辑器配置
- `LevelEditorConfigWriter.cs` — 配置写入

---

## 关联

- [[分析-RocketV2完整逻辑-v2（重构版）|RocketV2 完整逻辑]] — 配套分析文档
- [[报告-RocketVL闪电球视觉替换|RocketVL 闪电球视觉替换]] — 相关视觉改造方案
- [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑分析]] — 高层综述
- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]] — 项目总入口
