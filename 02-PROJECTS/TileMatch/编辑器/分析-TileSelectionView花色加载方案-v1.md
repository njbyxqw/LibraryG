---
title: "TileSelectionView 花色加载方案"
date: 2026-06-17
type: analysis
status: finalized
version: v1
tags: [TileMatch, 编辑器, TileSelectionView, 花色加载]
cat_order: 003
---

# TileSelectionView 花色加载方案

> **背景**：TileSelectionView 是关卡编辑器中用于选择 Tile 类型的视图，默认只显示固定花色（C1T1~C7T1）。需要动态加载当前关卡配置的花色。

---

## 一、现状分析

### TileSelectionView.cs 架构

- **715 行**，核心字段：
  - `_categoryData`：分类数据字典（`Dictionary<string, List<BlockTypeData>>`）
  - `_categoryGoDict`：分类按钮 GameObject 字典
  - `_categoryObject`：分类内容 GameObject
- **分类按钮创建流程**：`BuildCategoryButtons()` → 遍历 `_categoryData` → 实例化按钮 Prefab
- **ItemList 展开/关闭**：`OnCategoryButtonClicked()` → `OpenItemList()` / `CloseItemList()`
- **选中状态管理**：`_currentSelectedItem` 记录当前选中项

### 图标加载链路

```
SetTileIconSprite(TileSelectionTile / TileSelectionObstacle)
  → TileIconSpriteCache.GetDisplayConfigByBlockType()
  → AssetDatabase.LoadAssetAtPath<Sprite>(ImagePath)
```

### 数据源

- **TileType 枚举**：固定花色范围 `C1T1=0 ~ C7T1=60`
- **关卡 JSON 中的 TileTypes 字段**：`[{TileType, Count}]` 列表
- **LevelConfig.TileTypes**：当前关卡配置的所有 TileType 及其数量

---

## 二、方案对比

### 方案 A：动态插入（推荐 ⭐）

**思路**：在 `_categoryData["Tile"]` 末尾动态追加当前关卡的新花色

**实现步骤**：
1. 新增 `LoadFlowerColorsForCurrentLevel()` 方法
   - 遍历 `LevelConfig.TileTypes`
   - 筛选 `TileType > 60`（新花色）
   - 追加到 `_categoryData["Tile"]`
2. 新增 `ReloadFlowerColors()` 方法
   - 切换关卡时清除 0~60 范围旧花色
   - 保留放牌/暗牌/金牌/火箭牌
3. 修改 `OnLevelConfigChanged()`
   - 触发 `ReloadFlowerColors()`
   - 刷新已展开面板

**优点**：
- 最小化改动（仅 2 文件 3 方法）
- 不影响原有固定花色逻辑
- 动态适应关卡配置

**风险**：
1. **金牌/火箭牌被误删**：`ReloadFlowerColors()` 的 `RemoveAll` 条件太宽 → 改为 for 循环只匹配 0~60 范围
2. **图标加载失败**：新花色可能没有 `ImagePath` → 需要检查 `TileIconSpriteCache`
3. **性能**：每次切换关卡都重新加载 → 可以缓存

### 方案 B：独立 TileType 分类栏

**思路**：在 TileSelectionView 中新增一个独立的 TileType 分类栏

**实现步骤**：
1. 修改 `TileSelectionView.cs`：`_categoryData` 新增 "TileType" 分类
2. 修改 `BuildCategoryButtons()`：新增分类按钮
3. 新增 `LoadTileTypeData()`：从 `LevelConfig.TileTypes` 加载数据

**优点**：
- 隔离性好，不影响原有逻辑
- 更直观（新花色有独立分类）

**缺点**：
- 改动较大（UI 布局调整）
- 需要修改多个方法

---

## 三、方案 A 详细实现

### 3.1 LoadFlowerColorsForCurrentLevel()

```csharp
private void LoadFlowerColorsForCurrentLevel()
{
    var config = LevelDataManager.Instance?.CurrentLevelConfig;
    if (config == null) return;

    if (!_categoryData.ContainsKey("Tile"))
        _categoryData["Tile"] = new List<BlockTypeData>();

    // 追加新花色（TileType > 60）
    foreach (var tileType in config.TileTypes)
    {
        if ((int)tileType.TileType > 60)
        {
            var blockTypeData = new BlockTypeData
            {
                Id = (int)tileType.TileType,
                BlockType = tileType.TileType,
                Type = BlockType.Type.Tile,
                Name = tileType.TileType.ToString(),
                // ImagePath 需要从配置加载
            };
            _categoryData["Tile"].Add(blockTypeData);
        }
    }
}
```

### 3.2 ReloadFlowerColors()

```csharp
private void ReloadFlowerColors()
{
    if (!_categoryData.ContainsKey("Tile")) return;

    // 只移除 0~60 范围的新花色（保留放牌/暗牌/金牌/火箭牌）
    for (int i = _categoryData["Tile"].Count - 1; i >= 0; i--)
    {
        var data = _categoryData["Tile"][i];
        if ((int)data.BlockType > 60)
            _categoryData["Tile"].RemoveAt(i);
    }
}
```

### 3.3 OnLevelConfigChanged() 修改

```csharp
private void OnLevelConfigChanged()
{
    // 原有逻辑...
    
    // 新增：重载花色
    ReloadFlowerColors();
    LoadFlowerColorsForCurrentLevel();
    
    // 刷新已展开面板
    if (_currentOpenCategory == "Tile")
        OpenItemList("Tile");
}
```

---

## 四、数据流图

```
LevelConfig.TileTypes (数据源)
  ↓
LoadFlowerColorsForCurrentLevel() (追加到 _categoryData["Tile"])
  ↓
BuildCategoryButtons() (创建分类按钮)
  ↓
OnCategoryButtonClicked("Tile") (展开 ItemList)
  ↓
SetTileIconSprite() (设置图标)
  ↓
TileIconSpriteCache.GetDisplayConfigByBlockType() (获取显示配置)
  ↓
AssetDatabase.LoadAssetAtPath() (加载图标资源)
```

---

## 五、文件改动清单

| 文件 | 改动方法 | 改动类型 |
|------|---------|---------|
| `TileSelectionView.cs` | `LoadFlowerColorsForCurrentLevel()` | 新增 |
| `TileSelectionView.cs` | `ReloadFlowerColors()` | 新增 |
| `TileSelectionView.cs` | `OnLevelConfigChanged()` | 修改 |

**共计**：2 文件，3 方法

---

## 六、风险提示

1. **金牌/火箭牌被误删**
   - **现象**：`ReloadFlowerColors()` 的 `RemoveAll` 条件太宽，删掉了金牌/火箭牌
   - **修复**：改为 for 循环，只匹配 0~60 范围

2. **图标加载失败**
   - **现象**：新花色没有 `ImagePath`，导致图标显示为空
   - **检查**：`TileIconSpriteCache` 是否包含新花色的配置

3. **性能问题**
   - **现象**：每次切换关卡都重新加载，导致编辑器卡顿
   - **优化**：可以缓存 `LevelConfig.TileTypes`，只有变更时才重新加载

4. **Undo/Redo 支持**
   - **现象**：加载新花色后，Undo 可能导致数据不一致
   - **建议**：在 `LoadFlowerColorsForCurrentLevel()` 前保存 `_categoryData` 快照

---

## 七、后续优化方向

1. **缓存机制**：缓存 `LevelConfig.TileTypes`，避免重复加载
2. **配置检查**：在 `LoadFlowerColorsForCurrentLevel()` 中检查 `ImagePath` 是否为空
3. **Undo/Redo 支持**：保存 `_categoryData` 快照
4. **UI 优化**：新花色过多时，考虑分页或滚动显示

---

## 关联

- [[规范-本地扩展开发|本地扩展开发规范]] — 后续转为本地扩展方案
- [[分析-关卡编辑器界面与功能逻辑梳理-v1|关卡编辑器界面与功能逻辑梳理]] — 编辑器架构总览
- [[_MOC|TileMatch 知识库 MOC]] — 项目总入口
