---
title: TF Rescue Mission与七日任务：开启前计数
date: 2026-11-25
type: product-analysis
status: current
verification: static-native-verified
tags: [产品分析, TileFamily, RescueMission, WeeklyMission, 任务计数]
---

# Rescue Mission与七日任务：开启前计数

**活动整体尚未开启时，先前通关不会计入这期任务，开启后也不会补记。** 活动已经在后台开启、只是玩家没有点击入口时，符合任务条件的行为可以正常累计。结论基于 TF 2.12.0／21200 原包 ARM64，未做设备前后差分。

## 状态与行为

正式开启关卡配置为 **120关**：2026-11-04 initial-config的`config_server_activity_dup.csv`中，`rescue_mission_01`至`rescue_mission_08`及`weekly_mission_01/02`的`StartLevel`均为120，`PreviewLevel`为空。这里是配置的关卡门槛，不等于任意时刻达到该关卡立即开启，还须通过活动排期与其他启动条件；未新采2026-11-25线上配置。

| 场景 | 通关任务计数 | 依据与边界 |
|---|---|---|
| 尚未达到活动条件、未创建本期活动 | 不累计到本期 | 尚未初始化本期任务；新任务进度为0 |
| 活动处于 NOTENABLE／PREVIEWING／INACTIVE | 不更新 | 实际写入入口要求 ACTIVE=10，其余状态退出 |
| 活动已 ACTIVE，尚未打开活动页或看过开场动画 | 可以累计 | 任务更新不检查页面是否打开或开场动画标记 |
| 活动已 ACTIVE，后续某天／阶段尚未解锁 | 已生成且匹配的任务可累计 | 更新遍历本期任务字典，不以当前页签／StageIndex筛掉后续任务；领取／展示解锁另行判断 |
| TIMEOUT／CLOSED | 不更新 | 同一 ACTIVE 门禁 |

“任务目标完成10关”只作例子，不表示本批所有任务均配置为10。若本期尚未开启时打了10关，随后正式开启，该通关任务从0开始；之后再完成1次符合条件的通关，计为1，而非11。

## 实现区分

本版本同时有 `RescueMissionLiveEvent` 与 `WeeklyMissionLiveEvent`。Rescue 的初始化可见4阶段路径；Weekly 另有按日期锁页签、每日任务校验与替换机制。不能仅凭玩家可见“救援／七日任务”名称把它们视为同一内部类。本次一并核对两条实现，活动状态门禁与普通事件增量计数结论一致。

普通通关类的未开启计数结论不直接推广到所有任务：合成等进度型任务存在 `UpdateMergeTaskProgress`／`GetMissionTaskProgress` 的同步读取，登录天数也有独立初始化。应逐类型核对，不能用通关的规则断言所有目标一律无同步或补值。

## 最短证据链

本机根：`D:\LibraryG\06-PRODUCT-ASSETS\TileFamily\2.12.0\`。下表方法均为同构建ARM64地址；代码语义由原始指令、metadata与配置联合核对。

| 环节 | 方法／地址 | 已核逻辑 |
|---|---|---|
| 通关行为输入 | `ToyActivityV2ControllerDependency.SendData` `0x674ce98` | 成功路径检查 `LevelPlayCount==1`，发送 MissionId=5001、TargetNumber=1、DataType=Increase(0)；另外两条成功难度路径发送5002与5029，均为+1 |
| 常量复核 | 原生只读地址 `0x151a7b8`／`0x1519868`／`0x151a9e0` | 连续两个int分别为 `(5001,1)`／`(5002,1)`／`(5029,1)`，不是玩家历史累计关数 |
| Rescue事件门禁 | `<UpdateMissionData>d__67.MoveNext` `0x65e79b8` | `0x65e7a10` 比较当前状态与10，非10退出，符合才调用实际写入 |
| Weekly事件门禁 | `<UpdateMissionData>d__82.MoveNext` `0x65d65f0` | `0x65d6648` 同样比较10，非10退出 |
| 状态值 | metadata `LiveEventState` 字段默认值 | 解码为NOTENABLE=0、PREVIEWING=5、ACTIVE=10、INACTIVE=20、TIMEOUT=30、CLOSED=40 |
| Rescue实际写入 | `UpdateMissionData` `0x65dec9c` | 遍历MissionDupInfos，匹配MissionId与可选来源；Increase将TargetNumber加到MissionNumber，再检查目标完成 |
| Weekly实际写入 | `UpdateMissionData` `0x65cdc20` | 同类字典遍历与增量／覆盖分支；未以页签日期限制普通任务写入 |
| 新任务初始化 | `MissionListConfig.CreateMissionData` `0x65ea1a8` | `0x65ea4fc` 同时将State与MissionNumber清零 |
| 任务语义 | `decoded/initial-config/Config/config_mission_list.csv` | 5001说明为“获得n局首胜”，表头说明“活动期间内进行统计”；不能把失败、任意重打均写成必计 |

原始证据位于 `04-ReverseEngineering/rescue-*.txt`、`rescue-calls.json`、`rescue-source-xrefs.json`；提取与校验入口 `rescue-extract.py`、`rescue-source-xrefs.py`、`rescue-audit.py`。`rescue-audit.json`保存输入哈希、枚举原值、通关常量和四项指令断言结果。

## 来源与验证边界

- 同构建ARM64 SHA256：`c9a2163af064d82b4542ea73810470c4abb072a1477cd48e83395f382679a3af`，本次重新计算与既有样本一致；metadata身份见资源索引。
- 配置沿用2026-11-04保存的initial-config；不代表2026-11-25线上所有账号仍采用相同任务组或排期。
- REA本次读取ELF与哈希成功，伪代码返回provider_unavailable；使用既有metadata及Capstone／pyelftools复核原始指令。未执行目标代码、改账号、改时或实机通关。
- 已核普通通关输入→状态门禁→进度写入→新建归零；未证明具体当前账号处于何种状态，也未完成所有任务类型、替换任务和跨版本迁移的穷尽验证。

## 关联

- [[02-PROJECTS/产品分析/Tile Family/_MOC]]
- [[02-PROJECTS/产品分析/Tile Family/活动系统与清单-2.12.0]]
- [[02-PROJECTS/产品分析/Tile Family/资源路径索引]]
- [[02-PROJECTS/产品分析/PiggyKingdom/活动/RescueMission/开启前计数-2.7.3]]
