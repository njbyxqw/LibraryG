---
title: TileScape 打点字典工作簿索引
date: 2026-09-24
type: reference
status: current
project: TileScape
source: 02-PROJECTS/TileScape/参考/附件/TileScape打点.xlsx
source_snapshot_sha256: 5c73915a201aac3452eff5fe860616da69315fcd0b4de0c835c3187222664814
verification: 静态读取工作簿；运行 SQL 前须在当前 TA 环境和当前客户端代码复核表名、字段类型、事件覆盖与版本范围。
tags: [TileScape, 打点, 埋点, ThinkingData, TA, SQL]
---

# TileScape 打点字典工作簿索引

> 用于 SQL 和代码逻辑定位的活入口。权威事件/属性明细保留在 [[#原始工作簿与更新规则|原始工作簿]]；LG 记录检索路径与使用边界，不维护容易过期的逐事件副本。

## 原始工作簿与更新规则

- LG 内权威附件：![[02-PROJECTS/TileScape/参考/附件/TileScape打点.xlsx]]
- 导入来源：`/Users/dean/Downloads/TileScape打点.xlsx`；原文件未移动或删除。
- 本次静态快照：SHA-256 `5c73915a201aac3452eff5fe860616da69315fcd0b4de0c835c3187222664814`（2026-09-24 读取）。这是本次读取锚点，不是工作簿的版本号。
- 后续从本页点击附件，使用 Excel、Numbers 或 LibreOffice 编辑并保存到 LG 内的同一文件；若变动影响 Sheet 路由、公共字段、核心事件或版本边界，再同步修订本页和当天 Daily。
- 表内“状态 / 测试结果 / 测试备注”属于历史设计与验收线索，不能替代当前代码、TA 查询或设备验证。

## 快速路由

| 想查什么 | 优先 Sheet | 使用要点 |
|---|---|---|
| Adjust/FB/投放与收入回传 | `投放相关事件` | 查 `session`、`purchase`、`ad_revenue`、新用户购买与关卡阶梯；先确认目标渠道。 |
| 用户画像、分层、AB | `用户属性` | 读取属性含义、更新方式和计算口径；历史 cohort 不可直接用当前快照属性回推。 |
| 全事件字段和系统预置字段 | `公共参数` | 同时包含业务公共参数与 SDK 预置字段（如账号、设备、时区、事件时间）；先判字段层级。 |
| 启动、推送、归因、性能、运行保护 | `基本模块` | 含 `launch_flow`、`push`、`game_exit`、`home_enter`、性能汇总与运行保护类事件。 |
| UI、引导、区域和 DLC | `基础功能` | 查 `ui_open`、`ui_close`、`start_guide`、`end_guide`、`dlc_start`、`dlc_complete`、`dlc_fail`。 |
| 广告播放、展示、收入 | `广告` | `applovin_ad_revenue_impression_level`、`ad_result`、`ad_click`、`ad_entrance`、`ad_play`、`ad_ecpm_fetch` 分用途查询。 |
| 物品产销 | `产销` | 以 `report_item` 和变化类型、物品、数量、来源/子来源字段建立口径。 |
| 礼包展示、点击、购买 | `支付` | 按 `gift_show`、`gift_click`、`trackrevenue`、`purchase` 等漏斗节点及位置/商品字段查。 |
| 关卡尝试、结局、复活和道具 | `关卡` | 当前关卡事件与字段主入口，见下节。 |
| 新增或版本化需求 | `新增需求` | 仅作变更线索；用当前实现和正式事件块确认最终口径。 |

## 关卡 SQL / 逻辑常用入口

`关卡` Sheet 已登记 `lv_start`、`lv_end`、`lv_revive`、`add_moves_show`、`prop_used`、`lv_start_reconnect`、`level_loading`。查一条关卡链路时，应一起确认事件时机、公共参数继承、`lv_id` / `lv_name`、关卡类型、尝试/进关方式、结果和复活/道具字段的含义。

不要仅以事件时间相邻就推断属于同一局。需要关卡级漏斗或复活归因时，先用该表确认可用的局次与状态字段，再对当前 TA 数据抽样验证事件顺序与覆盖。

## 与现有 TA SQL 基础的关系

[[02-PROJECTS/TileScape/参考/参考-TA游戏分析SQL基础-2026-09-08|TA 游戏分析 SQL 基础]]记录的是已使用过的查询口径和骨架；本页提供“事件/属性应如何查”的工作簿入口。两者都不替代本次查询前对当前 TA 表/视图、字段类型、分区、时区和观察窗口的复核。

工作簿为层级行结构：事件起始行之后的连续属性行同属该事件。编写 SQL 或定位上报代码时，应读取完整事件块及其备注，不能只摘取事件名或首个属性。

## 关联

- [[02-PROJECTS/TileScape/参考/参考-TA游戏分析SQL基础-2026-09-08|TA 游戏分析 SQL 基础]]
- [[02-PROJECTS/TileScape/参考/分析-新用户关卡风险与首次挫败监控方案-2026-09-08|新用户关卡风险与首次挫败监控方案]]
- [[02-PROJECTS/TileScape/_MOC|TileScape 知识库 MOC]]
