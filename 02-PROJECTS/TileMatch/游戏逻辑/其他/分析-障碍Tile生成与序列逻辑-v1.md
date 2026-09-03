---
title: "障碍Tile生成与序列逻辑"
date: 2026-07-20
type: analysis
status: finalized
version: v3
tags: [TileMatch, 游戏逻辑, 障碍Tile, 序列, 花色分配, V2分池, 深度排序, 洗牌道具, DDA]
cat_order: 002
---

# 障碍Tile生成与序列逻辑

> **完整覆盖**：从关卡 JSON 文件解析到 TileData 创建、花色分配（两套策略）、序列模型（父子关系 + 去重约束 + 容器类型）、洗牌道具（智能配对 + 序列保护 + Golden 跟随）、Board 初始化完整流程、Trap 藏牌 DDA 调控、Tile 显隐判定。
>
> **源码文件**（13 个核心文件）：`LevelConfig.cs` · `TileMatchGameLogic.EntityInitializer.cs` · `Board.cs` · `TileData.cs` · `Tile.cs` · `TileService.cs` · `AssignTileTypeStrategy.cs` · `AssignTileTypeByDepthStrategy.cs` · `SequenceData.cs` · `SequenceControl.cs` · `SequenceConstraintHelper.cs` · `ShuffleProp.cs` · `ShufflePropTargetFilter.cs` · `TrapRegulationStrategy.cs` · `SequenceDisplayService.cs` · `TransformSequenceAction.cs`
>
> **分池算法细节** 见独立文档 [[分析-AssignTileTypeByDepth分池打乱策略-v1|分池打乱策略]]。

---

## 一、完整初始化流程

### 1.1 入口：TileMatchGameLogic.EntityInitializer

```
GameData.InitializeFromContext()
  ├─ InitializeBoardData()     → BoardData(LevelConfig)
  ├─ InitializeBarData()       → BarData()
  ├─ InitializeOverBarData()   → OverBarData()
  ├─ InitializeSequenceData()  → SequenceData()
  ├─ InitializeComplexData()
  └─ InitializeBatchData()     → BatchData()

InitEntities()
  ├─ InitializeBoard()         → Board(LevelConfig) → AddLevelTiles → 所有 TileData → Tile
  ├─ InitializeBar()           → Bar
  ├─ InitializeOverBar()       → OverBar
  ├─ InitializeSequenceControl() → SequenceControl → 收集所有 SequenceId>0 的牌
  ├─ InitializeBatchControl()  → BatchControl
  └─ ResetRandomService()
```

### 1.2 Board.InitializeFromLevelConfig 详细流程

```csharp
// Board.cs:61-127
public void InitializeFromLevelConfig(TileMatchGameContext gameContext, IReadOnlyList<TileData> tileDataList)
{
    AddLevelTiles(gameContext, tileDataList);    // ① 遍历 tileDataList → CreateTile
    AddLevelEffect(gameContext);                  // ② 关卡预置 Effect
    UpdateAllIndexes();                           // ③ 计算 Grid 索引
    UpdateAllTileVisibility();                    // ④ 初次显隐计算
    UpdateAllEffectVisibility();

    // ⑤ 金牌/火箭替换（发生在分池分配之后，不受藏牌影响）
    if (isCanCollectGold)  ModifyTilesToGolden();
    if (isCanShowRocket)   ModifyTileToRocket();

    // ⑥ 重新计算索引 + 显隐（因为金牌/火箭改了 TileType）
    _boardData.RefreshCount();
    AddGoldenEffects(gameContext, tileDataList);  // 加 Golden Effect 装饰
    UpdateAllIndexes();
    UpdateAllTileVisibility();
    UpdateAllEffectVisibility();

    InvalidateCache();        // 使类型/分组/显隐缓存失效
    MarkAllTilesRegulated();  // 标记所有牌"已调控完成"
}
```

**关键时序保证**：花色分配（`AssignTileTypeStrategy` / `AssignTileTypeByDepthStrategy`）在 `tileDataList` 构建阶段完成 → 金牌/火箭替换发生在 Board 初始化期间 → Effect 最后挂载。Trap 藏牌花色在分池阶段已经写入 TileType，后续不覆盖。

### 1.3 TileData 构造

```csharp
// TileData.cs:178-196
public TileData(LevelTileConfig levelTileConfig)
{
    Id = EntityIdUtil.GetNextId();
    TileType = levelTileConfig.TileType;        // 花色/障碍类型
    Position = levelTileConfig.Position;          // Vector3Int 坐标
    Size = levelTileConfig.Size;                  // 占位大小
    Form = levelTileConfig.Form;                  // 形态
    Life = levelTileConfig.Life;                  // 生命值
    State = TileState.InBoard;                    // 初始 InBoard 状态
    FromRandom = levelTileConfig.FromRandom;      // 是否参与随机分配
    DefaultActiveIndex = levelTileConfig.DefaultActiveIndex;
    EntityVisibility = EntityVisibility.Highlight; // 初始全部 Highlight
    SetInPileIndex(-1);
    CalculateBounds();    // MinX/MaxX/MinY/MaxY 包围盒
    UpdateVisibility();   // 初次显隐计算
}
```

---

## 二、LevelConfig 关卡配置数据结构

### 2.1 LevelTileConfig（单张牌配置）

| 字段 | 类型 | 含义 |
|------|------|------|
| `TileType` | TileType | 牌的花色/类型（FromRandom 时为 Random） |
| `Position` | Vector3Int | 棋盘坐标 (x, y, z) |
| `Size` | Vector2Int | 占位尺寸 |
| `Form` | int | 形态编号 |
| `Life` | int | 生命值 |
| `FromRandom` | bool | 是否为随机分配花色的牌 |
| `SequenceCount` | int | 序列子牌数量（如 Flip=3） |
| `Sequences` | List\<int\> | 序列子牌预定义花色列表 |
| `SequenceSource` | int | 运行时动态追加的子牌指向父级索引（-1 = 非子牌） |
| `DefaultActiveIndex` | int | 默认激活索引 |

### 2.2 序列相关字段

```csharp
// LevelConfig.cs:68-84
[JsonProperty("SequenceCount")]  public int SequenceCount;          // 子牌数量
[JsonProperty("Sequences")]     public List<int> Sequences = new();  // 预定义花色
public int SequenceSource = -1;  // 运行时标记：指向父容器在 Tiles 列表中的下标
```

**序列牌两种生成模式**：

| 模式 | 使用字段 | 何时触发 |
|------|---------|---------|
| **SequenceCount > 0** | SequenceCount | 关卡文件预配置了数量，花色从 Random 池分配 |
| **Sequences.Count > 0** | Sequences | 关卡文件预定义了具体花色（可为 Random 占位） |

### 2.3 GetRandomTileCount / GetSequenceRandomTileCount

```csharp
// LevelConfig.cs:286-313
// GetRandomTileCount：
//   遍历 Tiles，计数 FromRandom=true 且 SequenceSource < 0（非运行时子牌）

// GetSequenceRandomTileCount：
//   遍历 Tiles，对每个容器：
//     - Sequences 列表中有 Random 的 → 计数
//     - SequenceCount > 0 → 全部计数
```

---

## 三、花色分配策略

### 3.1 策略选择

系统有两套花色分配策略，根据关卡配置决定使用哪个：

| 策略类 | 触发条件 | 文档 |
|--------|---------|------|
| `AssignTileTypeStrategy` | 默认（全部关卡） | 本节详述 |
| `AssignTileTypeByDepthStrategy` | `AssignTileTypeStrategy` 之后调用 | [[分析-AssignTileTypeByDepth分池打乱策略-v1|独立文档]] |

### 3.2 AssignTileTypeStrategy：步频交换算法

#### 3.2.1 入口 InvokeStrategy

```
入口
├─ count1 = GetRandomTileCount()         // FromRandom 普通牌
├─ count2 = GetSequenceRandomTileCount() // 序列子牌 FromRandom
├─ targetCount = count1 + count2
├─ InitializeTypeIndex(targetCount) → 步频交换生成花色索引列表
│   └─ GetBonusColors 或 GetColors → ShuffleTileType
│
└─ RandomizeTileTypeWithLevelConfig()
     ├─ 第一遍：遍历 tiles，FromRandom 且 SequenceSource < 0 → 顺序分配
     └─ 第二遍：遍历 tiles，处理序列容器
          ├─ SequenceCount > 0 → 追加子牌（prepareNextRandomType + TrackAssigned）
          └─ Sequences.Count > 0 → 展开子牌（Random 占位 → 从池中分配）
```

#### 3.2.2 GetColors：按组生成花色

```csharp
// AssignTileTypeStrategy.cs:210-237
for (int i = 0; i < tileCount; i++)
{
    // 每 3 个一组，花色序号递增
    // iconEnum 从 1 开始，超出 maxColorType 后回绕
    colors.Add(new RandomItem { ColorIndex = iconEnum - 1, RandomTime = randomTime });
    if (assignCount % 3 == 0) iconEnum++;
    if (iconEnum > maxColorType) iconEnum = 1;
}
// 结果：[0,0,0, 1,1,1, 2,2,2, ...] 每组 3 张
```

#### 3.2.3 ShuffleTileType：步频交换

```csharp
// AssignTileTypeStrategy.cs:173-208
for (int i = 0; i < colors.Count; i++)
{
    var targetIndex = i;
    var randomItem = colors[i];

    if (randomItem.RandomTime <= 0) { result.Add(randomItem.ColorIndex); continue; }

    // 从当前位置向后跳 1~randomStep 步，与目标位置花色交换
    var rm = _gameContext.RandomService.Range(1, randomStep);
    targetIndex += rm;
    randomItem.RandomTime--;
    targetIndex = Mathf.Min(targetIndex, colors.Count - 1);

    // 交换 colors[i] ↔ colors[targetIndex]
    colors[i] = colors[targetIndex];
    colors[targetIndex] = randomItem;
    result.Add(colors[targetIndex].ColorIndex);
}
```

| 参数 | 来源 | 含义 |
|------|------|------|
| `randomStep` | 难度表 `DiffStepTimeList` / `CustomData.RandomStep` | 步频，每步交换跳跃距离 |
| `randomTime` | 同上 | 每个花色最大可被交换次数 |

**效果**：不是 Fisher-Yates 全排列打乱，而是一种"有限次跳动交换"，保留了部分原始分组结构。

#### 3.2.4 RandomizeTileTypeWithLevelConfig：序列牌展开

这是首次分配花色时最复杂的步骤，处理 Sequence 容器子牌的展开：

```csharp
// AssignTileTypeStrategy.cs:44-137
// 第一遍：普通 FromRandom 牌 + 序列非子牌 → 直接取 typeIndex[typeIndex++] 赋值
foreach (var levelTileConfig in _gameContext.LevelConfig.Tiles)
{
    if (levelTileConfig.FromRandom && levelTileConfig.SequenceSource < 0)
    {
        levelTileConfig.TileType = tileTypes[types[typeIndex]].TileType;
        typeIndex++;
    }
}

// 第二遍：遍历全部 tiles，处理序列容器
for (int i = 0; i < initCount; i++)
{
    var tileConfig = _gameContext.LevelConfig.Tiles[i];

    // 模式 A：SequenceCount > 0（如 Flip 有 3 个子牌）
    if (tileConfig.SequenceCount > 0)
    {
        var usedTypes = PrefersDistinctTypes ? new HashSet<TileType>() : null;
        for (int index = 0; index < tileConfig.SequenceCount; index++)
        {
            PrepareNextRandomTypeForSequence(types, typeIndex, ..., usedTypes, tileConfig);
            newConfig.TileType = ResolveTypeByIndex(types[typeIndex]);
            newConfig.Position = tileConfig.Position;      // 共享容器位置
            newConfig.SequenceSource = i;                  // ← 指向父级下标
            list.Add(newConfig);                            // ← 运行时追加
            typeIndex++;
        }
    }

    // 模式 B：Sequences.Count > 0（预定义花色，可能含 Random）
    else if (tileConfig.Sequences.Count > 0)
    {
        foreach (var type in tileConfig.Sequences)
        {
            TileType tileType;
            if (type == Random)  // 占位符 → 从池中取
            {
                PrepareNextRandomTypeForSequence(types, typeIndex, ..., usedTypes, tileConfig);
                tileType = ResolveTypeByIndex(types[typeIndex]);
                typeIndex++;
            }
            else tileType = (TileType)type;  // 预定义花色

            TrackAssignedSequenceType(tileConfig, tileType, usedTypes);
            newConfig.Position = tileConfig.Position;
            newConfig.SequenceSource = i;
            list.Add(newConfig);  // 运行时追加
        }
    }
}
```

### 3.3 Bonus 关卡花色处理

```csharp
// AssignTileTypeStrategy.cs:239-316
// Bonus 关卡有 3 种花色（小/中/大），按 BonusConfigs 的 Count 分配
// 不够 → 从 BonusType=1 的类型补齐
// 多了 → 按优先级 {1,2,3} 递减
```

### 3.4 V2 分池打乱

> 完整分析见 [[分析-AssignTileTypeByDepth分池打乱策略-v1|分池打乱策略]]，核心要点在此摘要。

**规则**：视觉最上层 25% Tail 不打乱（贪心交替），其余 75% + 全部序列子牌合并 Shuffle（一次 Fisher-Yates）。

**提交 5885672785** 放宽了整除校验（只看总数不看各自）并合并了序列池。

---

## 四、序列模型

### 4.1 数据结构

#### SequenceData

```csharp
// SequenceData.cs
// 核心：Dictionary<long, List<long>> — Key=序列父级Id, Value=子牌Id列表
public class SequenceData
{
    private readonly Dictionary<long, List<long>> _sequenceIds = new();

    void AddSequences(long keyId, List<long> sequence);   // 批量添加
    void AddSequence(long keyId, long valueId);            // 单个添加
    void RemoveFromOneSequence(long keyId, long valueId);  // 移除子牌
    void ExchangeFromOneSequence(long keyId, long oldId, long newId); // 子牌置换
    void ExchangeInSameSequence(long keyId, long id1, long id2);     // 同序列交换位置
    void Sort(Comparer<long> comparer);                     // 按 SequenceIndex 排序
    List<long> GetSequence(long keyId);                     // 获取子牌Id列表
}
```

#### SequenceControl

```csharp
// SequenceControl.cs
public class SequenceControl : IEntity
{
    // 初始化：遍历所有 TileData，收集 SequenceId > 0 的牌
    void InitializeFromTileDataList(IReadOnlyList<TileData> tileDataList)
    {
        _sequenceData.Clear();
        for each tileData:
            if (tileData.SequenceId > 0)
                _sequenceData.AddSequence(tileData.SequenceId, tileData.Id);
        _sequenceData.Sort(按 SequenceIndex 排序);
    }

    // 移除单个子牌引用
    void RemoveTileReferenceFromSequence(TileData tileData);

    // 完全清理牌的所有序列状态
    void ClearTileSequenceState(TileData tileData)
    {
        tileData.SetSequenceId(-1);
        foreach EffectData on tile: 清除 SequenceId/SequenceIndex
    }

    // 销毁整个序列（父级被消除 → 所有子牌脱连）
    void RemoveSequenceSelf(TileData tileData)
    {
        var sequence = GetSequence(tileData.Id);
        foreach tileId in sequence:
            tile.SetSequenceId(-1);
            清除 EffectData 上的 SequenceId/SequenceIndex;
        _sequenceData.RemoveSequence(tileData.Id);
    }
}
```

### 4.2 TileData 序列相关字段

```csharp
// TileData.cs
public long SequenceId { get; private set; } = -1;     // 所属父级 Id（-1=普通牌）
public int SequenceIndex { get; private set; }          // 在序列中的顺位
public bool InPile { get; private set; }                // 是否参与 Pile（叠加判定）

// SetSequenceId / SetSequenceIndex 都会标记 _visibilityDirty
// SequenceId >= 0 时，显隐由 SequenceDisplayService 接管
```

### 4.3 序列显隐由 SequenceDisplayService 接管

```csharp
// TileData.cs:637-650, UpdateVisibility()
if (SequenceId >= 0)
{
    var displayService = ctx.SequenceDisplayService;
    var visibility = displayService.GetTileVisibility(SequenceId, Id, SequenceIndex);
    return displayService.ApplyTileVisibility(this, visibility);
}
```

**与普通牌的区别**：普通牌的显隐由 Grid Index（覆盖判定）驱动；序列子牌的显隐由容器自身的显示逻辑（如 Flip 的 FirstNHighlight）驱动。

### 4.4 运行时排序

SequenceData 通过 Comparer 按 SequenceIndex 排序，确保子牌在序列中按配置顺序排列。

---

## 五、序列约束：SequenceConstraintHelper

### 5.1 约束触发条件

```csharp
// SequenceConstraintHelper.cs:16-19
public static bool PrefersDistinctTypes(LevelTileConfig tileConfig)
{
    return tileConfig?.TileType == TileType.Flip;  // 仅 Flip 容器启用去重
}
```

**当前只有 Flip 类型启用序列内花色去重。** 其他容器（MagicBox、ShellBox×4、JokerFlip、Thief、CardBox、SuitCase）均不启用。

### 5.2 PrepareNextRandomTypeForSequence

在分配序列子牌花色时，尝试跳过与已分配子牌同色的花色：

```csharp
// 从 randomizedTypeIndices[currentRandomCursor+1..] 找第一个不在 usedTypes 中的花色
// 找到 → 与当前位置交换
// 找不到 → 记录警告，保留当前分配
```

### 5.3 TrackAssignedSequenceType

记录已分配的花色到 usedTypes，同时做重复检测：

```csharp
// 如果 PrefersDistinctTypes 且 tileType 不是 Default/Random
// 尝试 Add 到 usedTypes，如果 Add 失败（已存在）→ 警告日志
```

### 5.4 PreservesDistinctTypesOnSwap：洗牌交换保护

洗牌时两两交换的"合法性校验"：

```csharp
// 规则：交换后不能产生同序列内重复花色
public static bool PreservesDistinctTypesOnSwap(Tile tile1, Tile tile2, context)
{
    // 同序列内部交换 → 不会改变花色集合 → 总是允许
    if (sequenceId1 > 0 && sequenceId1 == sequenceId2) return true;

    // 跨序列交换：检查 tile2.TileType 进入序列1 是否合法
    //              且 tile1.TileType 进入序列2 是否合法
    return CanEnterSequence(tile2.TileType, sequenceId1, ...) &&
           CanEnterSequence(tile1.TileType, sequenceId2, ...);
}

// CanEnterSequence：遍历目标序列的所有兄弟牌，检查是否有同花色
```

### 5.5 CanTileJoinDDA：DDA 调控准入

```csharp
// 检查 tile 是否可以参与 DDA 调控
public static bool CanTileJoinDDA(Tile tile, context)
{
    if (!IsDDAEnabledForTile(tile, context)) return false;  // IsCanJoinDDA + Capabilities.CanJoinDDA
    if (tile.TileData.HasSeen) return false;                 // 玩家已见过 → 不能再调控
    return true;
}
```

---

## 六、序列容器类型全览

### 6.1 容器分类

| 类型 | Enum 值 | 类别 | 序列变换 | 去重约束 | 子牌数 | 显示模式 |
|------|---------|------|---------|---------|--------|---------|
| **Flip** | 5110 | A 类（FlipProfile） | Rotate 循环左移 | ✅ PrefersDistinctTypes | 3 | FirstNHighlight(1) 逐张暴露 |
| **CardBox** | 5140 | A 类 | 无 | ❌ | 3 | Life=6 护盾，打 0 血开盒 |
| **SuitCase** | 5130-5131 | A 类 | 无 | ❌ | 3 | 3x1/1x3 大格子，一次性暴露 |
| **MagicBox** | 5010 | B 类 | 无 | ❌ | 3 | — |
| **ShellBox** | 5030-5033 | B 类 | 无 | ❌ | 3 | — |
| **JokerFlip** | 5150 | B 类 | 无 | ❌ | 3 | — |
| **Thief** | 5160 | B 类 | 无 | ❌ | 3 | — |

### 6.2 Flip 详细行为

```
Flip 容器（3 个子牌，Rotate 模式）：
  点击容器上当前暴露的子牌 →
    TransformSequenceAction(Rotate) →
      队首子牌移到队尾 →
      新队首高亮（SequenceDisplayService.ApplyTileVisibility）

ECA 配置：
  Event: 子牌被消除
  Action: TransformSequence(Rotate × 1)
  子牌位置：3 张共享容器位置，SequenceDisplayService 控制各自显隐
```

### 6.3 CardBox 详细行为

```
CardBox 容器（3 个子牌，无变换）：
  容器本身有 Life=6 护盾 →
  每消除一张对应颜色牌 → 扣 1 血（Life--）→
  Life=0 → TransformSequence：FirstNVisible → FirstNHighlight → 子牌可点击

死局保护：场上无牌可交互时 → 自动破盒
```

### 6.4 SuitCase 详细行为

```
SuitCase 容器（3 个子牌，无变换，大格子 3×1 或 1×3）：
  容器占据 3 个格子 →
  脱盖条件触发 → FirstNVisible(全量) → 一次性暴露 3 张 → FirstNHighlight
```

---

## 七、洗牌道具完整逻辑

### 7.1 入口 ShuffleProp.Use()

```csharp
// ShuffleProp.cs:52-114
public bool Use()
{
    // ① 获取 ShuffleProp 专用 Filter
    _gameContext.TileTargetSelectService.GetCustomFilter(CustomTargetFilterType.ShuffleProp, out filter);

    // ② FilterTiles：从 Highlight + Visible + NotVisible 三层选牌
    var targets = filter.FilterTiles(...);

    // ③ 执行两两交换
    _gameContext.TileService.ExchangeTilePairsPosition(targets, RebuildFromCurrentVisibility);

    // ④ 重置调控标记
    foreach tile in targets: tile.TileData.UpdateCanJoinDDA(true);

    // ⑤ 记录游戏操作
    _gameContext.RecordController.AddMove(new TileMatchGameRecordUsePropMove(PropType));
}
```

### 7.2 Shufflable 判定

```csharp
// Tile.cs:516-540
internal bool Shufflable()
{
    if (LockState == LockState.Locked) return false;           // 锁定的牌不可洗
    if (!config.Capabilities.Shufflable) return false;         // 配置禁用
    if (TileGroup == Blocker && TileType != Rocket) return false; // 障碍牌不可洗（火箭除外）
    // Effect 检查（略）
    return true;
}
```

### 7.3 ShufflePropTargetFilter：智能配对策略

洗牌不是纯随机，而是有**定向配对优先级**：

```
Filter 流程：
① 分两组：highlightAllowTiles / notHighlightAllowTiles（含 Visible + NotVisible）

② 计算 Bar 中当前未完成消除的牌类型（lastUnmatchedTile）
   → shuffleToTopNeedCount = 还需要几张同花色牌来凑消组

③ 优先级配对（BuildPriorityTargetPairs）：
   如果存在 lastUnmatched：
   - 从 notHighlight 选出与 lastUnmatched 同花色的牌
   - 与 highlight 牌配对（优先找"交换后合法"的配对）
   - 最多配对 shuffleToTopNeedCount 对

④ 随机配对（BuildRandomPairs）：
   剩余未配对牌随机两两组合 → 优先找合法配对，找不到则强制配对

合法配对判定 → PreservesDistinctTypesOnSwap(tile1, tile2)
```

**设计意图**：如果玩家已经有未完成的消组在 Bar 里，洗牌道具会优先把相同的花色牌"洗到面上"，帮助玩家完成消除。

### 7.4 TileService.ExchangeTilePairsPosition：交换实现

```csharp
// TileService.cs:147-335
// 输入:tileList = [tile1, tile2, tile3, tile4, ...] 两两一组交换
// 关键步骤：
① 收集需要跟随交换的 Effect（Golden = 跟随牌；其他 Effect = 保持原位）
② ClearAllIndexes → 移除旧网格索引
③ 对每对 (tile1, tile2)：
   - 保存旧 position + sequenceId + sequenceIndex
   - Swap HasSeen（可见性记忆交换）
   - 分离 Golden Effect（跟随牌移）和其他 Effect（保持原位）
   - 设置新 position
   - 更新 SequenceData 中的映射（同序列交换 / 跨序列交换）
   - 设置新的 sequenceId + sequenceIndex
   - 清除旧 Grid Indexes → Add 新 Entity Index
④ UpdateAllIndexes + UpdateAllTileVisibility + UpdateAllEffectVisibility
⑤ RefreshTileDataByZ（按 Z 排序刷新）
⑥ RebuildAllHasSeenFromCurrentVisibility（因为模式是 RebuildFromCurrentVisibility）
```

### 7.5 Golden Effect 跟随

- `EffectType.Golden` 作为 `followTileEffectTypes`，交换时跟随牌移动
- 其他 Effect（非 Golden）保持原位不动
- Golden Effect 的 `SequenceID` 和 `SequenceIndex` 跟随牌同步更新

---

## 八、Tile 显隐判定

### 8.1 三种驱动模式

| 驱动模式 | 判定条件 | 算法 |
|---------|---------|------|
| **Grid Index** | InBoard + SequenceId < 0 + BatchId < 0 | MaxIndex>0 && MinIndex>0 = NotVisible；MaxIndex==0 && MinIndex==0 = Highlight；其余 = Visible |
| **SequenceDisplayService** | InBoard + SequenceId >= 0 | 由容器显示逻辑决定（如 Flip 的 FirstNHighlight） |
| **BatchDisplayService** | InBoard + BatchId >= 0 | 批次整体显示逻辑 |

### 8.2 Grid Index 计算（TileDepthComputer）

> 详细算法见 [[分析-AssignTileTypeByDepth分池打乱策略-v1#二、深度映射原理|分池打乱策略·深度映射]]。核心：Grid Index = 上层牌覆盖判定，Index>0 = 被遮挡 → NotVisible。

### 8.3 HasSeen 与 DDA 调控触发

```csharp
// TileData.cs:262-352
// Visibility 变化时：
// 如果从未见过 (HasSeen=false) 且 Visibility 从 NotVisible → Highlight（V2 含 Visible）
//   → _shouldRandomizeType = true     // 标记"需要在 DDA 中调控花色"
//   → CanTriggerRegulationThisVisibilityChange = true
// 同时 MarkSeen() = true
```

**HasSeen 交换**：洗牌时 `ExchangeHasSeenWith(tile1, tile2)` 交换两张牌的 HasSeen 状态 ← 这是"玩家已见过"记忆的正确转移。

---

## 九、DDA 调控：Trap 藏牌

### 9.1 分池阶段的藏牌

> 由 `AssignTileTypeByDepthStrategy` 的分池+Trap 路径执行，将 2 种花色藏到 NotVisible 深层位。详见 [[分析-AssignTileTypeByDepth分池打乱策略-v1#三、完整算法流程|分池算法 Trap 路径]]。

### 9.2 运行时的 Trap 调控

```csharp
// TrapRegulationStrategy.cs
// V2 DDA 策略：当牌变得可见时，选择"可见牌中该花色数量最少的暗牌"交换
public Tile TryExchangeTile(Tile target, TileMatchGameContext context)
{
    // ① 遍历 NotVisible 池
    // ② 过滤：Locked × / CanJoinDDA × / Blocker 非 Rocket × / Candy ×
    // ③ 统计各花色在 Bar + Visible + Highlight + OverBar(High/Vis) 中的数量
    // ④ 选数量最少的暗牌 → 实现"使每种花色分布更均匀"
}
```

---

## 十、关键文件索引

| 功能 | 文件 | 关键方法/行 |
|------|------|-----------|
| 关卡配置 | `Config/Level/LevelConfig.cs` | L68-84 序列字段; L286-313 计数 |
| 实体初始化 | `TileMatchGameLogic.EntityInitializer.cs` | `InitEntities()` → `InitializeBoard/InitializeSequenceControl` |
| 棋盘初始化 | `Entity/Board.cs` | L61-127 `InitializeFromLevelConfig` |
| Tile 数据层 | `Data/TileData.cs` | L178-196 构造; L636-716 `UpdateVisibility`; L637-650 序列显隐接管 |
| Tile 实体 | `Entity/Tile.cs` | L516-540 `Shufflable` |
| Tile 创建/交换 | `Services/TileService.cs` | L50-89 `CreateTile`; L147-335 `ExchangeTilePairsPosition` |
| 花色生成+步频 | `Module/LevelTileType/Strategy/AssignTileTypeStrategy.cs` | L139-171 `InitializeTypeIndex`; L173-208 `ShuffleTileType`; L44-137 `RandomizeTileType` |
| 分池打乱 V2 | `Module/LevelTileType/Strategy/AssignTileTypeByDepthStrategy.cs` | → 独立文档 |
| 深度计算 | `Module/LevelDepth/TileDepthComputer.cs` | `ComputeWeightedDepths` |
| 序列数据 | `Data/SequenceData.cs` | `Dictionary<long, List<long>>` |
| 序列控制 | `Entity/SequenceControl.cs` | L53-69 `InitializeFromTileDataList` |
| 序列约束 | `Services/SequenceConstraints/SequenceConstraintHelper.cs` | L26-69 去重; L94-112 交换保护; L114-127 DDA 准入 |
| 洗牌道具 | `Prop/ShuffleProp.cs` | L52-114 `Use` |
| 洗牌过滤 | `Filter/ShufflePropTargetFilter.cs` | L14-190 智能配对 |
| Trap 调控 | `Module/InLevelDDA/V2/Strategy/TrapRegulationStrategy.cs` | L18-67 `TryExchangeTile` |
| 序列显示 | `Services/SequenceDisplayService.cs` | — |
| 序列变换 | `Behaviours/Action/Implementation/TransformSequenceAction.cs` | L20 `TransformSequenceAction` |

---

## 关联

- [[分析-AssignTileTypeByDepth分池打乱策略-v1|AssignTileTypeByDepth 分池打乱策略]] — 分池算法完整分析（常量、流程、fallback、子方法、提交历史）
- [[工具-牌局生成深度显示-v1|牌局生成深度显示工具]] — Scene Gizmos + Console 统计
- [[分析-死局逻辑与改进方案-v1|死局逻辑与改进方案]] — 死局判定
- [[局内障碍知识库_MOC|局内障碍知识库]] — 障碍 Tile 全览
- [[_MOC|TileMatch 知识库 MOC]] — 项目总入口
