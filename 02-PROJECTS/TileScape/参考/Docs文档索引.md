---
title: TileScape 项目文档索引
date: 2026-09-03
tags:
  - tilescape
  - docs-index
type: index
status: finalized
project: TileScape
lifecycle: current
verification: index-only
priority: medium
cat_order: 020
---

# TileScape 项目文档索引（Docs/ + Doc/ 整理备注）

> 本文档是 `D:\TileScape\Docs\` 与 `D:\TileScape\Doc\` 下未迁移文档的**索引清单**。文档原文仍在项目内，仅做分类整理与价值备注；后续有需求再按主题迁移进知识库。

## Joy数值配置参考补充（2026-11-26）

- 用户明确要求按数值配置整理并同步到项目Docs；LG主档为[[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/数值配置参考-2.7.3|Merge Joy数值配置参考]]，解释与差分依据仍在[[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/数值分层与选表-2.7.3|数值分层与选表]]。
- TS副本：`Docs/ActivityMigration/MergeTwo/参考资料/MergeJoy-2.7.3/数值配置参考-2.7.3.md`；`Docs/ActivityMigration/MergeTwo/README.md`已补入口。数值第1～8节与LG相同，项目副本的来源和关联按团队阅读适配，不复制个人知识库结构；五份源配置摘要均保留。
- 本次只交付竞品数值参考，没有确定或写入TS正式玩法配置。核查文档数值、引用和副本一致性，未做游戏编译、实机投放、支付或人群分层实验；没有commit／push。本机`Docs/Knowledge/README.md`、`Memory.md`、`CodeMap.md`缺失，未从历史路径补造，按现有AGENTS与MergeTwo README定位。
- 下方11/24目录清单与提交状态保留原采样时间，不作为11/26当前文件清单；本轮未恢复其中缺失的旧需求或附件。

## 二合迁移文档用途与维护边界（2026-11-24）

本节只整理入口及已核状态，不把程序执行文档整套复制到LG。项目目录为`Docs/ActivityMigration/MergeTwo/`，核对提交`feat-merge@606d93905`；目录顶层有28份Markdown，其中26份已跟踪，`README.md`与`迁移背景.md`尚未提交。统计不含子目录中的竞品附件。

### 迁移背景是否需要提交

**本次Joy需求不需要补交`迁移背景.md`。** 它保存MT原始功能、六阶段规则、体力／奖励、进入退出与存档归属，属于规则背景；当前项目方案保存“怎样迁到TS、实际做了什么和验证了什么”，用途不同，但不需要为本轮Joy另维护一份背景全文。

- 规则背景主档为[[02-PROJECTS/TileScape/游戏逻辑/背景-MT二合活动迁移|MT二合活动迁移背景]]。项目文件是11月23日的本地备份，不是已提交交付物。
- 项目背景副本仍引用旧`Assets/.../MergeTwo活动迁移.md`等计划位置；本次局部检索未发现其他顶层迁移文档引用该副本，因此不提交它不会破坏现有迁移文档引用。
- 只有团队确实需要在仓库内独立查阅MT原始规则、且用户明确要求同步时，再校对背景副本、替换失效入口并提交。不自动删除现有本地副本。
- LG为背景和产品需求主档；项目文件非必要不改，指定同步时才更新。程序方案、实施记录和原始证据仍在项目内维护，LG保留用途索引、稳定结论与验证边界。

### 按用途阅读

以下文件名均相对上述项目目录。

| 类别 | 文档 | 主要回答的问题 |
|---|---|---|
| 当前结果概览 | `MergeTwo当前迁移报告.md` | 已迁入什么、剩余差异、奖励替代和缺失资源、各类验证覆盖到哪里；先读这一份了解进度 |
| 执行总方案 | `二合迁移总方案.md` | 源／目标基线、迁移范围、模块职责、实施依赖与历次决定；含历史记录，不能只看页首旧状态推断当前完成度 |
| 专项迁移方案 | `公共接口迁移方案.md`、`道具-奖励拓展.md` | 接口与UIEffect、物品／体力／奖励接入、共享能力和保留边界 |
| 专项迁移方案 | `玩法迁移方案.md`、`活动迁移方案.md`、`引导迁移方案.md` | 分别管理棋盘与存档核心，入口／BP／图鉴／生命周期等外围，以及教学配置／触发／恢复；和总方案合计六份方案 |
| 实施记录 | `活动Step1A4～Step4`、`玩法引导Step1`、`玩法Step2～Step3`、`引导Step2～Step3`对应实施记录 | 对应批次实际改动、交付文件、配置生成及验证，不作为新需求；有问题时按模块追查，共9份 |
| 已知问题 | `活动迁移问题.md` | 支付输入、字体及源资源缺失等影响与验收边界，以及用户后续修正的保留／排除范围 |
| 测试与修复记录 | `代码自动化测试首批记录.md`、`批量验证收口记录-20261123.md`、`140项差异收敛记录-20261124.md`、`全部失败修正记录-20261124.md` | 每批测试输入、失败与修复、复验结果；次数及用例有重叠，不能简单相加为总覆盖 |
| 专项修复记录 | `棋盘输入修复记录.md`、`Tips关闭引导修复记录.md`、`奖励代码收敛记录-20261124.md`、`多语言同步记录-20261123.md` | 输入、引导关闭、奖励与Tips收敛、多语言修正的原因、修改和验证范围 |
| 原始证据与清单 | `Evidence/`、`MergetwoMigrationReport.xlsx` | 日志、测试结果、哈希、引用与逐项奖励／缺图证据；Excel是指定批次快照，不替代后续修复记录 |
| 本轮产品改造 | `需求/MergeJoy/00-需求总览.md`、01～09模块、`参考资料/MergeJoy-2.7.3/` | Joy按模块说明需求、状态、配置、进度与验收；LG为主档，项目保留用户指定同步版本。11月24日新目录尚未提交，旧单篇`需求-MergeJoy参考下的二合功能修改.md`保留并指向新入口 |

### 当前应带到需求侧的信息

- 迁移报告结论仍为“有差异待验收”。支付商品输入与实际支付／补单、完整业务及设备验收不能由代码测试通过代替；Joy保留付费BP，旧三档体力直购不属于本版范围。
- 原迁移保留图鉴、六阶段换盘、恢复、兑换等，是迁移基线；Joy当前需求停用或修改这些功能，不能把“原先保留”理解成“新活动必须开放”。本版停用业务不等于删除通用玩法能力。
- 奖励替代、调试排期及旧引导不直接作为Joy正式内容。稳定产品要求已归入[[02-PROJECTS/TileScape/游戏逻辑/需求-MergeJoy参考下的二合功能修改|Joy需求主档]]，无需再复制程序实现细节。
- `606d93905`仅提交需求、图册和尺寸说明三份文件，原提交依赖未提交README及4份assets附件。11月24日按用户要求已在工作区去掉个人知识库关联及这些附件链接，三文件互相引用，说明原始素材包／完整JSON未包含；当前修改尚未提交。图册内嵌图片、尺寸数据及交互保留，后续不要求补交附件才能阅读。
- 项目交付文档聚焦需求、参考信息与资料范围，不展示LG路径、个人知识库结构或主档／同步关系。LG内部继续维护主档与来源；项目版本允许做面向团队的引用和措辞整理，不能因此另行改变产品规则。

推荐阅读顺序：了解进度先读当前迁移报告与活动迁移问题；做Joy评审读LG需求主档；需要实现细节再读对应专项方案；排查已改行为时再追实施记录及Evidence。原MT规则有疑问时回到LG背景主档。

### Joy模块需求暂存审阅与存放建议（2026-11-24）

以`HEAD=606d93905`的当前Git索引为准，暂存13个文件：`需求/README.md`、`需求/MergeJoy/00～09`共11个新增文件，另有图册引用清理和旧单篇需求的知识库引用清理。10份模块总分需求与LG一致，仅相对链接适配；没有混入游戏代码或运行资源。

尚有2处已跟踪文件的未暂存修改建议一并纳入：尺寸说明去除个人知识库与缺失附件链接；旧单篇增加新模块入口提示。后一文件为MM，索引中没有该提示。只提交当前暂存内容，尺寸说明仍保留两处缺失JSON链接及vault引用，旧单篇也未标明已被模块稿替代。补齐这两处修改后最终为14个文件，不是另加两份新文档。

| 内容 | 是否纳入本次需求提交 | 合适位置与理由 |
|---|---|---|
| 总览、9模块及需求目录索引 | 是 | `Docs/ActivityMigration/MergeTwo/需求/MergeJoy/`与`需求/README.md`；LG为主维护，项目为团队阅读副本 |
| 图册与尺寸说明 | 是 | 保持`参考资料/MergeJoy-2.7.3/`，图片和表格内嵌，需求模块引用它们 |
| 旧单篇需求及新版入口提示 | 本次保留并标明旧稿 | 根目录兼容旧链接；不继续维护第二套正文。若以后移入历史目录，需同时调整图册及尺寸说明的旧入口链接 |
| 未跟踪的根README | 否 | 内容仍含个人知识库路径、旧单篇主入口和原始附件下载，与当前交付方向不一致；所需导航已由`需求/README.md`提供，维护约定保留LG即可 |
| `assets/package-reference/`下ZIP与3份JSON | 否 | 4文件与LG竞品档案逐字节一致，约13.67MB；本次展示无需这些附件。原件保留LG产品分析档案，只有明确交付原始素材时才增补项目附件 |
| 未跟踪`迁移背景.md` | 否 | MT原始规则主档已在LG，项目副本有旧路径；本次Joy需求无依赖 |
| 根目录`TileScape_fresh.slnx` | 否，另案评估 | 本机161项目的解决方案，比已跟踪`TileScape.slnx`多14个MergeTwo／UIEffect／活动测试工程；不能当作完全重复文件，也不随文档提交。团队工程入口若需调整，应单独核对已有解决方案规范 |
| 根目录`fbg.log` | 否 | Facebook Game SDK初始化／退出日志，留本机排障，不属于需求或稳定知识 |

此轮仅评估归属与提交边界，未移动、删除、暂存或提交文件。旧根README、原始附件与背景副本是否清理本地文件另行处理，不由“不建议提交”推导为可以删除。

## 功能文档实例（2026-11-19）

以下两例核对自目前 Windows TS 工作区 `D:\TileScape_fresh` 的 Git 提交。

| 功能 | 团队文档入口 | 用途 |
|---|---|---|
| 二合迁移 | `Docs/MergeTwo_Requirements_Draft.md`（`6629a8359`） | 需求草案集中维护核心循环、术语、范围和 P01–P12 待定项。 |
| Flow 二期 | `Assets/Module/Flow/FlowDesignPhase2.md`、`Docs/Flow二期/`（`0e60bc9d4`） | 需求与设计、源码调研、落地方案、评审及分步实施验证各有入口，便于对照版本与接手。 |

该结构在竞品调研中的具体用法见 [[02-PROJECTS/产品分析/方法-竞品模块分析与持续维护#参照 TS Docs 组织功能档案|功能档案组织方法]]。

二合项目调研报告已按 `feat-MergeTwo` 需求草案准备，目标位置为 TS `Docs/MergeTwo/01-调研报告-MergeFantasy.md`。当前会话的 TS 仓库权限为只读，待放入团队 Docs。[[02-PROJECTS/TileScape/参考/二合活动/01-调研报告-MergeFantasy|01-调研报告-MergeFantasy]]

## SplashQuest 数值任务与交付副本

- TS `Docs/SplashQuest_Implementation_Plan.md`：活动项目交付副本；LG 持续主入口为 [[02-PROJECTS/TileScape/游戏逻辑/任务-钻石联盟每日三阶段改造]]，策划稿为 [[02-PROJECTS/TileScape/游戏逻辑/需求-钻石联盟每日三阶段活动]]。
- 数值状态（2026-11-16）：旧体系及 B1～V1.1 试算已归档，停止沿用；见 [[02-PROJECTS/TileScape/游戏逻辑/归档-SplashQuest旧数值体系问题与重设计交接-2026-11-16|旧数值体系问题与重设计交接]]。TS plan 与旧系数报告已同步历史状态。
- DDAV3 当前代码接缝与旧研究的适用边界见 [[02-PROJECTS/TileScape/游戏逻辑/任务-DDAV3逻辑策略持续研究#活动策略接入边界]]；源码仍是行为事实来源。

## DLC 当前入口与历史来源（2026-09-08）

- **当天 Home 增量**：[[02-PROJECTS/TileScape/游戏逻辑/任务-DLC全链路梳理与维护#2026-09-08 Home 下载优化|2026-09-08 Home 下载优化]]；dev @ `1e323e6e8` / `12e6620af` 已改为状态进入前置调度、两 Handler 与共享串行队列。旧 Flow/协调器只作历史路径，Editor 测试未在本轮执行。

- **唯一长期主档**：[[02-PROJECTS/TileScape/游戏逻辑/任务-DLC全链路梳理与维护|DLC 全链路梳理与维护]]。按玩家旅程维护当前实现、配置、需求差距与验证边界，不再新增日期快照。
- **源码旁说明**：TS `Assets/Module/HomeHub/HomeScene/Scripts/DLC/DLC.md`，2026-09-07 标注 Ocean 迁移；部分路径/配置/启动选项已与代码不同，以主档当前复核为准。本轮仅只读，不修改该文件。
- **本地 QA 来源**：TS `Docs/Knowledge/Local/Inbox/2026-09/Activity_DLC_QA_Functional_Test_Guide_2026-09-01.md`（ignored，使用显式路径）。其 Preview/Open 启动口径、23 关、签到启用和测试值均已漂移，不直接用于当前 dev 验收。
- **发布契约来源**：TS `Doc/DownloadableContentUsageGuide.md`；开头 2026-08-10“配置为空/全 Embedded”是历史快照。最新 Manifest、Player、CDN 与设备证据仍待核验。
- **历史 LG 材料**：[[02-PROJECTS/TileScape/游戏逻辑/梳理-HomeDLC与Endless最大关卡更新流程-2026-08-20|旧重启流程]]、[[02-PROJECTS/TileScape/游戏逻辑/梳理-ActivityDLC现状与设计差异-2026-08-26|FirstPay 试点审计]] 保留历史正文；[[02-PROJECTS/TileScape/游戏逻辑/设计-活动DLC扩展框架-2026-08-25|活动扩展框架]] 继续保留设计状态。

## 一、Docs/（项目设计 / 迁移文档，58+ 项，持续补充）

### 1. 迁移总览 / 全局审计（7）
| 文档 | 备注 |
|---|---|
| `TILEV2_MIGRATION_LANDING_PLAN.md` | 迁移落地总计划 |
| `TILEV2_INTERFACE_MIGRATION_REPORT.md` | 接口迁移报告 |
| `TileV2_Migration_V1_Phase_Report.md` | V1 阶段报告 |
| `TileV2_NonMigrated_Content.md` | 未迁移内容清单 |
| `TileV2_Old_vs_Current_Exhaustive_Behavior_Audit.md` | 新旧行为穷举审计 |
| `Meatloaf_TileScape_Full_Parity_Audit_2026-08-04.md` | MT / TS 全量对齐审计 |
| `Main_vs_Dev_Full_Code_Review_2026-08-01.md` | 主分支 vs dev 全量代码审查 |
| `DELETION_LOG.md` | 删除记录 |

### 2. 架构 / 接口设计（4）
| 文档 | 备注 |
|---|---|
| `R-018_Assembly_Dependency_Graph.mermaid` | 程序集依赖图（高价值） |
| `UIPageView_UITabBar_Component_Interface_Design.md` | UI 组件接口设计 |
| `Obfuz_Build_Entry_Points.md` | 混淆构建入口点 |
| `Obfuz_Symbol_Archive.md` | 混淆符号归档 |

### 3. 系统 / 模块设计（4）
| 文档 | 备注 |
|---|---|
| `FlyModule_System_Design.md` | Fly 模块系统设计 |
| `Scroll_Gesture_Routing_Runtime_Auto_Installation_Design.md` | 滚动手势路由自动安装设计 |
| `FontArt/`（3 篇） | UITextArt 设计/模板/工作流 |
| `UIManager_Lifecycle_Repair_Plan.md` | UIManager 生命周期修复 |

### 4. DataCenter 数据中心（5）
| 文档 | 备注 |
|---|---|
| `TileV2_DataCenter_Requirements_Derivation.md` | 需求推导 |
| `TileV2_DataCenter_Code_Driven_Implementation_Plan.md` | 代码驱动实现计划 |
| `TileV2_DataCenter_Behavior_Parity_Test_Matrix.md` | 行为对齐测试矩阵 |
| `TileV2_DataCenter_Phase6_Migration_Record.md` | Phase6 迁移记录 |
| `TileV2_DataCenter_Phase7_Migration_Record.md` | Phase7 迁移记录 |

### 5. 玩法机制迁移（8）
| 文档 | 备注 |
|---|---|
| `TileV2_Prop_Migration_Baseline.md` / `_Implementation_Plan.md` / `_Staged_Plan.md` | 道具迁移（基线/计划/分阶段） |
| `TileV2_Reward_Migration_Implementation_Plan.md` | 奖励迁移 |
| `TileV2_Condition_FunctionUnlock_Migration_Implementation_Plan.md` | 条件 FunctionUnlock 迁移 |
| `TileV2_Replay_UI_Migration_ImplementationPlan.md` | 回放 UI 迁移 |
| `TileV2_SimplePanels_UIFlow_MigrationPlan.md` | 简单面板 UI 流迁移 |
| `TileV2_UIGamePanel_UIManager_MigrationPlan.md` | UIGamePanel/UIManager 迁移 |

### 6. 新手引导 Tutorial（9）
| 文档                                                                                             | 备注                 |
| ---------------------------------------------------------------------------------------------- | ------------------ |
| `TileV2_Tutorial_NewFramework_Implementation_Plan.md` / `_Audit.md` / `_Developer_Tutorial.md` | 新框架迁移（计划/审计/开发者教程） |
| `TileScape_Tutorial_Requirements_Gap_Audit_2026-07-29.md`                                      | 需求缺口审计             |
| `TileScape_First_Main_Tutorial_Implementation_Plan_2026-07-29.md`                              | 首个主引导实现计划          |
| `TileScape_vs_Meatloaf_Tutorial_System_Design_Comparison_2026-07-28.md`                        | 新旧项目引导系统对比         |
| `Tutorial_Framework_Complexity_Audit_And_Optimization.md`                                      | 框架复杂度审计            |
| `Tutorial_Framework_Lean_Architecture_Implementation_Plan.md`                                  | 精简架构计划             |

### 7. 适配 / 性能 / 资源（6）
| 文档 | 备注 |
|---|---|
| `TileV2_Gameplay_Fixed_1080_Width_Adaptation_Plan.md` / `_Baseline.md` / `_Execution_Steps.md` / `_Validation.md` | 1080 固定宽度适配（4 篇） |
| `TileV2_Gameplay_Layout_Structure_Refactor_Plan.md` | 局内布局结构重构 |
| `TileScape_XAsset_Android_Bundle_Optimization_Audit.md` | Android Bundle 优化审计 |

### 8. 编辑器 / Bot（2 + 子目录）
| 文档 | 备注 |
|---|---|
| `TileV2_Editor_Bot_Headless_Migration_Implementation_Plan.md` | 实现计划 |
| `TileV2_Editor_Bot_Headless_Migration/`（12 文件） | adapt_manifest、baseline、headless-diff-classification、runtime_manifest、migration_acceptance_report、assembly_dependency_report、resource_reference_report 等 |

### 9. 分析 / 打点（3）
| 文档 | 备注 |
|---|---|
| `TileScape_Analytics_Full_Audit_2026-07-28.md` | 打点全量审计 |
| `TileScape_Analytics_Final_Review_Repair_Report_2026-07-28.md` | 终审修复报告 |
| `TileScape_Analytics_Blockers_Status_2026-07-29.md` | 阻塞项状态 |

### 10. 商业化（5）
| 文档 | 备注 |
|---|---|
| `TileScape_Ad_System_Capability_Migration_Implementation_Plan.md` / `_Record.md` | 广告系统迁移（计划/记录） |
| `TileScape_Trade_Purchase_Design_Review_2026-08-01.md` | 交易/购买设计评审 |
| `TileScape_Trade_Purchase_Fix_Plan_2026-08-01.md` / `_2026-08-03.md` | 交易/购买修复计划（两版） |

### 11. 配置 / Profile / UserLayer（3）
| 文档 | 备注 |
|---|---|
| `TileScape_GoogleDrive_Config_Profile_Full_Audit_2026-07-27.md` | 配置/Profile 审计 |
| `TileScape_UserLayer_Config_Completeness_Audit_And_Repair_Plan_2026-08-03.md` | UserLayer 配置完整性审计与修复 |
| `TileScape_UserLayer_MainThread_Performance_Optimization_Implementation_Plan_2026-08-04.md` | UserLayer 主线程性能优化实施计划 |
| `UserLayer_Full_Migration_Implementation_Plan.md` | UserLayer 全量迁移计划 |

### 12. 近期漏列补充（2026-08-04 之后）

| 文档 | 备注 |
|---|---|
| `DLC_Full_Impact_And_Compatibility_Audit_2026-08-11.md` | DLC 全量影响与兼容性审计；后续稳定结论优先看 LG 游戏逻辑下的 DLC 文档。 |
| `TileV2_Analytics_Meatloaf_Event_Field_Behavior_Parity_Audit_2026-08-06.md` | TileV2 打点事件字段行为与 MT 对齐审计。 |
| `TileV2_Analytics_Meatloaf_Parity_Audit_2026-08-06.md` | TileV2 打点与 MT 对齐审计。 |
| `TileScape_Local_Notification_Meatloaf_Alignment_Implementation_Plan_2026-08-06.md` | 本地通知与 Meatloaf 对齐实施计划。 |
| `TileScape_Three_Subrepositories_Current_vs_Dev_Function_Update_Report_2026-08-13.md` | 三个子仓库 current/dev 功能更新差异报告。 |
| `INTERFACE_REVIEW_REPORT.md` | 接口审查报告。 |

## 二、Doc/（Meatloaf 源项目迁移过程记录，12 项）

> 多为**历史流水记录**（每日迁移报告），价值低于 Docs/ 的设计文档，一般不需迁移；仅保留索引备查。

| 文档 | 备注 |
|---|---|
| `Meatloaf_Dev_Delta_Migration_Stage0_2026-07-23.md` | 迁移 Stage0 |
| `Meatloaf_Dev_Delta_Migration_Manifest_2026-07-23.tsv` | 迁移清单（tsv） |
| `Meatloaf_Dev_Delta_Migration_Report_2026-07-23/24/25/26/30.md`（5 篇） | 每日迁移报告 |
| `Meatloaf_Dev_Delta_Content_Disposition_2026-07-25.md` | 内容处置说明 |
| `Meatloaf_Payment_Fulfillment_Risk_2026-07-24.md` | 支付履约风险 |
| `TileScape_Migration_Commit_Static_Review_2026-07-24.md` + `.dependency-graph.Mermaid` | 迁移提交静态审查 |
| `FoldableScreenAdaptationPlan.md` | 折叠屏适配计划 |

## 三、迁移优先级建议（后续有需求时参考）

- **高价值优先**（设计类，建议优先迁移）：R-018 程序集依赖图、Tutorial 新框架、DataCenter 需求推导、Trade/Purchase 设计评审、Ad 系统迁移、Fly 系统设计、UserLayer 计划
- **中价值**：玩法机制迁移各计划（Prop/Reward/Condition）、1080 适配、编辑器 Bot Headless
- **低价值/不迁移**：Doc/ 每日迁移报告、DELETION_LOG、Obfuz 构建细节

## 关联

- [[02-PROJECTS/TileScape/_MOC|TileScape 知识库 MOC]] — 项目总入口
- [[02-PROJECTS/TileScape/参考/同步-项目AI记忆与Docs入口-2026-09-03|项目 AI 记忆与 Docs 入口同步]] — TS 项目内 AI 记忆、Docs/Knowledge 与 LG 边界
- [[代码框架/代码框架总览|代码框架总览]] — 程序集/目录/关键类索引
