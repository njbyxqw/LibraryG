---
title: 分析-Tile打点解析-v1
date: 2026-06-08
type: analysis
status: finalized
version: v1
tags: [TileMatch, 打点, analytics_events]
cat_order: 001
---

# Tile 打点解析

> TileMatch 打点事件的完整解析，包含事件列表、字段说明、触发时机

---

## 一、打点系统概述

### 1.1 打点事件类型

TileMatch 的打点事件分为以下几类：

| 类型     | 说明       | 示例                                 |
| ------ | -------- | ---------------------------------- |
| 关卡事件   | 关卡生命周期相关 | `lv_start`, `lv_end`, `lv_revive`  |
| 道具事件   | 道具使用相关   | `prop_used`, `prop_get`            |
| 障碍事件   | 障碍Tile相关 | `obstacle_hit`, `obstacle_destroy` |
| 消除事件   | 消除相关     | `match`, `combo`                   |
| DDA 事件 | 难度调控相关   | `dda_adjust`, `dda_protect`        |
| 死局事件   | 死局相关     | `deadlock_times`, `is_deadlock`    |

### 1.2 打点数据流

```
游戏逻辑层
  → Entry/TileMatchGame.Logger.cs
  → TaDataManager.cs
  → analytics_events 表
  → TileAnalytics 后台
```

---

## 二、核心事件详解

### 2.1 lv_start（关卡开始）

**触发时机**: 关卡加载完成，玩家首次点击手牌区时

**字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `level_id` | int | 关卡 ID |
| `level_mode` | string | 关卡模式（normal/endless） |
| `timestamp` | long | 时间戳 |

### 2.2 lv_end（关卡结束）

**触发时机**: 关卡成功或失败时

**字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `level_id` | int | 关卡 ID |
| `result` | string | 结果（win/fail） |
| `duration` | long | 关卡时长（秒） |
| `deadlock_times` | int | 死局次数 |
| `deadlock_duration` | long | 死局总时长（秒） |

### 2.3 prop_used（道具使用）

**触发时机**: 玩家使用道具时

**字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `prop_type` | string | 道具类型 |
| `prop_count` | int | 道具数量 |
| `is_deadlock` | bool | 是否处于死局状态 |
| `deadlock_times` | int | 死局次数 |
| `deadlock_duration` | long | 死局持续时长（秒） |

### 2.4 match（消除）

**触发时机**: 手牌区发生消除时

**字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `match_count` | int | 消除组数 |
| `match_type` | string | 消除类型（normal/combo） |
| `tile_types` | string | 消除的 TileType 列表 |

---

## 三、打点事件文档 SQL 参考

**详见**: [[分析-Tile打点事件文档SQL参考-v1|Tile 打点事件文档 SQL 参考]]

**关键表**:
- `analytics_events` — 打点事件原始表
- `TileAnalytics_level_summary` — 关卡汇总表
- `TileAnalytics_prop_usage` — 道具使用表

---

## 四、打点代码位置

### 4.1 核心文件

| 文件 | 说明 |
|------|------|
| `Entry/TileMatchGame.Logger.cs` | 打点 Logger |
| `TaDataManager.cs` | 打点数据管理 |
| `TileMatchGameLogic.Event.cs` | 事件触发 |

### 4.2 打点流程

```csharp
// 示例：lv_end 打点
public void OnLevelEnd(LevelResult result)
{
    TaData taData = TaDataManager.GetCurrentTaData();
    taData.level_id = CurrentLevelId;
    taData.result = result;
    taData.duration = Time.time - _levelStartTime;
    taData.deadlock_times = InevitableDeathJudge.DeadlockCount;
    taData.deadlock_duration = InevitableDeathJudge.GetDeadlockDuration();
    
    TaDataManager.UploadTaData(taData);
}
```

---

## 五、常见问题

### 5.1 如何新增打点事件？

1. 在 `analytics_events` 表中新增字段（如果需要）
2. 在 `TaData` 类中新增字段
3. 在 `TileMatchGame.Logger.cs` 中新增打点逻辑
4. 在 `TaDataManager.cs` 中新增上传逻辑
5. 更新文档（`分析-Tile打点事件文档SQL参考-v1.md`）

### 5.2 如何查询打点数据？

**详见**: [[分析-Tile打点事件文档SQL参考-v1|Tile 打点事件文档 SQL 参考]]

**基本查询**:
```sql
SELECT 
    level_id,
    result,
    COUNT(*) as count
FROM analytics_events
WHERE event_name = 'lv_end'
GROUP BY level_id, result
```

---

## 关联

- [[分析-Tile打点事件文档SQL参考-v1|Tile 打点事件文档 SQL 参考]] — 配套 SQL 参考文档
- [[报告-Tile打点事件梳理_2026-06-08|Tile 打点事件梳理]] — 打点事件梳理报告
- [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑分析]] — 高层综述
- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]] — 项目总入口

---

## 变更记录

- 2026-06-08: 初始创建
- 2026-07-03: 恢复文件内容（从记忆重建）
