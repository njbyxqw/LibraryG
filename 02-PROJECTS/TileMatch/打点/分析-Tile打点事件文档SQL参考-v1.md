---
title: Tile打点事件文档 SQL 参考
tags: [TileMatch, 打点, SQL, analytics_events]
type: reference
status: finalized
version: v1
date: 2026-06-08
cat_order: 002
---

# Tile 打点事件文档 — SQL 参考

> 专供后续写 SQL 使用的结构化文档。包含事件总览、公共参数、9 大模块、SQL 写作注意事项。

---

## 一、打点系统架构

### 1.1 四通道架构

| 通道 | 用途 | SDK |
|------|------|-----|
| ThinkingAnalytics (TA) | 业务事件分析 | 数数科技 |
| AppsFlyer (AF) | 市场归因 | AppsFlyer |
| Firebase | 业务事件 + 归因 | Firebase |
| Facebook (FB) | 市场归因 | Facebook SDK |

### 1.2 调用链

```
BI（门面）
  └─ ServiceHub（路由）
       └─ IServiceTrack 实现
            ├─ TAServiceTrack
            ├─ AFServiceTrack
            ├─ FirebaseServiceTrack
            └─ FBServiceTrack
```

### 1.3 事件分布

- 约 70+ 个事件，分布在 50+ 个 C# 文件中
- 业务事件走 Firebase + TA
- 市场归因事件走 AF + FB + Firebase
- 关卡打点由 `TaDataManager` 集中管理
- 活动打点分散在各 Activity 类中

---

## 二、公共参数

### 2.1 用户属性（v_user_48）

TA 用户属性表，约 130 行 × 16 列。

### 2.2 事件公共字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `#account_id` | String | 账号 ID |
| `#user_id` | String | 用户 ID |
| `#event_name` | String | 事件名 |
| `#event_time` | DateTime | 事件时间 |
| `#country_code` | String | 国家代码 |
| `#app_version` | String | 应用版本 |
| `#zone_offset` | Int | 时区偏移 |
| `is_test` | Boolean | 是否测试用户 |

### 2.3 SQL 时间过滤模板

```sql
-- 日期分区
WHERE ${PartDate:date1}
-- 时区修正 + 时间范围
AND date_add('minute', cast((cast('${timezone}' as int) - if("#zone_offset" is null, 0, "#zone_offset")) * 60 as integer), "#event_time") ${Time:time1}
-- 测试用户过滤
AND e.is_test = false
-- 国家过滤
AND e."#country_code" <> 'CN'
```

---

## 三、9 大模块事件总览

### 3.1 基础模块

| 事件名 | 触发时机 | 关键参数 |
|--------|---------|---------|
| `lv_start` | 关卡开始 | lv_id, level_enter_num, level_type |
| `lv_end` | 关卡结束 | lv_id, levelend, lv_time, card_left, card_total |
| `lv_revive` | 关卡复活 | lv_id, revive_type, revive_times_cur |
| `add_moves_show` | 复活弹窗 | card_left, card_total, revive_times_cur |
| `prop_used` | 道具使用 | prop_type, deadlock_times, is_deadlock |

### 3.2 广告模块

| 事件名 | 触发时机 | 关键参数 |
|--------|---------|---------|
| `ad_show` | 广告展示 | ad_type, ad_placement |
| `ad_click` | 广告点击 | ad_type, ad_placement |
| `ad_close` | 广告关闭 | ad_type, close_type |

### 3.3 支付模块

| 事件名 | 触发时机 | 关键参数 |
|--------|---------|---------|
| `purchase` | 完成支付 | product_id, price, currency |
| `gift_show` | 礼包展示 | gift_type |

### 3.4 物品产销模块

| 事件名 | 触发时机 | 关键参数 |
|--------|---------|---------|
| `report_item` | 物品变动 | item_id, change_method, change_amount |

### 3.5 其他模块

- UI 交互模块：`ui_open`, `ui_close`
- 教程模块：`tutorial_step`
- 活动模块：各 Activity 类自定义事件
- DDA 模块：`control_times`, `exp_hard`
- 连胜模块：`streak_will_3`, `streak_will_4`, `streak_rate`

---

## 四、SQL 写作注意事项（关键）

> ⚠️ 以下问题在写 SQL 时必须注意，否则会导致计算结果错误。

### 4.1 参数实际类型与设计不符

| 参数 | 设计类型 | 实际上报类型 | 影响 |
|------|---------|-------------|------|
| `lv_id` | int | **String (VARCHAR)** | ORDER BY 产生字典序，需 CAST |
| `level_type` | int | **String** | 比较时需注意类型转换 |
| `level_enter_num` | int | **String** | 比较时需注意类型转换 |

**SQL 修正**：
```sql
-- 排序时强制转换
ORDER BY CAST(lv_id AS INT)

-- 区间过滤时强制转换
WHERE CAST(lv_id AS INT) BETWEEN 1 AND 200
```

### 4.2 level_enter_num 首次进入为 0

**设计**：首次进入应上报 `level_enter_num = 1`  
**实际**：首次进入上报为 `0`

**SQL 修正**：
```sql
-- 首次尝试相关指标需 +1 修正
WHERE CAST(level_enter_num AS INT) = 0  -- 首次进入
-- 或
WHERE CAST(level_enter_num AS INT) + 1 = 1  -- 首次进入
```

### 4.3 energyvalue 体力值

体力未满时上报为 `0`，不是真实体力值。SQL 中不能直接用于计算平均体力。

### 4.4 ui_close 的 close_type

`ui_close` 事件的 `close_type` 实际上报为 `open_type`（参数名错误）。

### 4.5 gift_show 打点缺失

目前只有首充礼包有 `gift_show` 打点，尝试礼包/BP/付费岛均缺失。

### 4.6 report_item 的 change_method

`report_item` 的 `change_method` 在测试中未上报。

---

## 五、关卡打点字段速查（TaDataManager）

### 5.1 lv_start 事件

| 字段 | 说明 | 备注 |
|------|------|------|
| lv_id | 关卡 ID | VARCHAR，排序需 CAST |
| level_enter_num | 进入次数 | 首次=0，需+1 |
| level_type | 关卡类型 | VARCHAR |
| energyvalue | 体力值 | 未满时=0 |

### 5.2 lv_end 事件

| 字段 | 说明 | 备注 |
|------|------|------|
| lv_id | 关卡 ID | VARCHAR |
| levelend | 结束原因 | 1=成功, 2=失败, 4=退出, 5=闪退, 6=保底胜利 |
| lv_time | 关卡用时（秒） | |
| card_left | 剩余牌数 | |
| card_total | 总牌数 | |
| gold_num_claim | 金币采集数 | |
| level_shuffle_num | 洗牌次数 | |
| level_hint_num | 提示次数 | |
| level_remove_num | 移牌次数 | |
| level_addslotnum | +1 次数 | |
| level_removeone_num | 撤回次数 | |
| exp_hard | 期望难度 | |
| control_times | DDA 调控次数 | |
| control_times_progress_25/50/75/100 | 各进度 DDA 次数 | |
| deadlock_times | 死局次数 | |
| revive_times_cur | 当前复活次数 | |
| failed_times | 失败次数 | |
| revive_times | 总复活次数 | |

### 5.3 LevelFinishReason 枚举

```csharp
public enum LevelFinishReason
{
    None = 0,
    Success = 1,           // 正常通关
    Fail = 2,              // 放弃复活失败
    Quit = 4,              // 主动退出
    Crash = 5,             // 闪退
    GuaranteeSuccess = 6,  // 保底胜利
}
```

---

## 六、数据表说明

### 6.1 主要查询表

| 表名 | 说明 | 使用场景 |
|------|------|---------|
| `ta.v_event_48` | 事件表 | 所有打点事件查询 |
| `ta.v_user_48` | 用户属性表 | 用户属性关联 |

### 6.2 JOIN 方式

```sql
FROM ta.v_event_48 e
JOIN ta.v_user_48 u
  ON e."#account_id" = u."#account_id"
```

---

## 关联

- [[_MOC|TileMatch 知识库 MOC]]



- [[报告-Tile打点事件梳理_2026-06-08]]
- [[分析-Tile打点解析-v1]]
- [[报告-关卡难度分析SQL_完整版_2026-07-03]]
