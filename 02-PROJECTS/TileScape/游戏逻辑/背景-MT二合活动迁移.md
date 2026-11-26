---
title: MT 二合活动迁移背景
date: 2026-11-23
updated: 2026-11-24
type: background
status: current
lifecycle: current
project: TileScape
verification: static-source-review; runtime-pending
tags: [TileScape, TileMatch, MT, MergeTwo, 二合活动, 迁移背景, 规则梳理]
aliases: [MT二合原始规则, 二合活动迁移背景]
source: "MT dev 静态源码与本地导出配置；本次对话整理；2026-11-23 用户确认 LG 主维护、项目 Docs 备份"
---

# MT 二合活动迁移背景

> **主要维护入口：LG。** 本文保存MT原始规则与流程，具体迁移及验证由程序执行。项目中的`Docs/ActivityMigration/MergeTwo/迁移背景.md`是2026-11-23本地备份，截至2026-11-24尚未提交，本轮Joy需求无需补交。后续仅在用户明确要求时同步，项目副本不独立维护。

> 11月24日仅整理维护边界与执行入口，未重做源代码调研。正文的V5.2决定、源版本及数值保留其历史口径；当前迁移进度与文档用途见[[02-PROJECTS/TileScape/参考/Docs文档索引#二合迁移文档用途与维护边界（2026-11-24）|项目文档索引]]，Joy功能范围见[[02-PROJECTS/TileScape/游戏逻辑/需求-MergeJoy参考下的二合功能修改|需求主档]]。

> 核对日期：2026-11-23。本文保存源端规则、业务流程、数据归属及定位依据，供产品讨论和程序迁移使用。具体实现、导表、资源处理与运行验收由程序执行，顺序与交付以现有迁移计划为准。

## 阅读入口

二合的核心闭环是“主线过关获取二合体力 → 发射与合成 → 收集阶段目标 → 阶段宝箱领奖与换盘”。图鉴、点赞返奖、排行榜、双轨 BP、商店及限时 Buff 共同围绕这条闭环运转。活动外围和棋盘玩法分别维护自己的状态，Item 系统维护真实余额。

| 要了解的问题 | 本文入口 | 后续执行入口 |
| --- | --- | --- |
| MT 原本有哪些功能 | [功能模块](#功能模块) | [当前活动迁移方案](../../../../TileScape_fresh/Docs/ActivityMigration/MergeTwo/活动迁移方案.md) |
| 进入、推进、退出和到期如何衔接 | [活动流程](#活动流程)、[到期与结算](#到期与结算) | 活动计划 A1、A2 |
| 六阶段、倍率、体力和商业化数值 | [规则与数值](#规则与数值) | 活动配置及 Item、Purchase 接入 |
| 状态由谁保存，恢复时依赖什么 | [数据与状态归属](#数据与状态归属) | [当前玩法迁移方案](../../../../TileScape_fresh/Docs/ActivityMigration/MergeTwo/玩法迁移方案.md)、活动方案的存档与生命周期章节 |
| 哪些源端功能在目标排除 | [迁移范围与既有决定](#迁移范围与既有决定) | [当前迁移总方案](../../../../TileScape_fresh/Docs/ActivityMigration/MergeTwo/二合迁移总方案.md) |
| 引导与弹窗为什么不能各自独立接入 | [界面与引导](#界面与引导) | [当前引导迁移方案](../../../../TileScape_fresh/Docs/ActivityMigration/MergeTwo/引导迁移方案.md) |
| 后续从哪里重新查代码 | [源码定位索引](#源码定位索引) | [当前公共接口方案](../../../../TileScape_fresh/Docs/ActivityMigration/MergeTwo/公共接口迁移方案.md) |

本文是背景快照，不承载实施进度，不把代码存在、旧测试记录或迁移计划中的预期结果视为本轮验收通过。

## 调研基线

| 项目 | 本次依据 |
| --- | --- |
| 源工程 | 当前环境的 `meatloaf_client01/client`，下文 MT 路径均相对该 Unity 工程根 |
| 源分支 | `dev` |
| 首轮调研提交 | `c07681bddb`，2026-11-23 |
| 本文整理时复核提交 | `538e3f128753fa7c438c3d72c3a381cd4da732b6`，2026-11-23 |
| 两次提交的相关差异 | 已比较活动、玩法、公开接口、二合首页入口、活动排期、Common 配置及活动 MergeTwoData；上述范围无提交差异 |
| Unity | 源端与目标本地版本均为 `6000.0.60f1` |
| 目标工程 | TileScape 当前工程；活动落点 `Assets/Module/Activity/MergeTwo`，玩法落点 `Assets/Game/MergeTwo` |
| 数值来源 | 源端本地导出 `Config/*.json~`、生成的 ConfigManager 和实际消费者；运行加载按配置格式选择 JSON 或 protobuf，并可应用配置覆盖 |
| 证据范围 | 源码、配置与既有设计的静态核对；本次未读取在线权威表、未确认真实账号的 AB 命中、未运行支付或完整活动链 |

**源选择存在版本边界。** V5.2 总控记录的计划源为 `meatloaf_client_copy/client`、`feat-dev_optimize`，本次实际调研源为上述 `dev` 工作区。本文没有修改程序迁移的源选择，也没有证明两条分支完全等价。程序开始前需确定正式源提交，并对本文涉及的规则、配置与接口做有界差异核对。

源端早期 README 中仍有“待接线”“待验收”等历史描述。定位时可用它找专题，判断当前实现需继续进入对应代码、配置和带版本的验收记录；存在差异时分别保留设计目标与实现事实。

## 活动流程

### 排期与预告

活动名为 `ActMergeTwo`。排期中的 `ruleId` 连接活动专表 Main，本地 Main 行为 `280101`；排期 ID、玩法规则 ID、活动期次是不同概念。

| 本地排期来源 | 预告门槛 preLevel | 开放门槛 openLevel | 其他要点 |
| --- | --- | --- | --- |
| 基础 activityconfig 中的 280100、280101 | 99999 | 99999 | 普通进度下不能将其视为开放配置 |
| activityconfig_ab104_b 中的 280100、280101 | 35 | 43 | 具体资格仍由活动框架与配置覆盖结果决定 |

AB104 B 的 280100 为 `cycleId=2`、`lateOpen=1`、`duration=863999`；280101 为 `cycleId=1`、`lateOpen=0`、`preTime=86400`。原配置的时间窗口分别从 2026-11-20 08:00:00、2026-11-19 08:00:00 开始，均写到 2026-11-30 07:59:59；这里只记录原始字段，不将其当作目标排期，也不另推时区。

预告有入口展示、时间／资格表示与频控。不能只复制 AB B 的等级，再省去配置覆盖、晚开或预告逻辑。[基础排期][C01]、[AB104 B 排期][C02]、[生命周期实现][S02]。

### 开启与首次进入

1. 活动框架开放本期，`OnOpen` 清理上一期玩法数据，重置 Buff、BP、弹窗、倍率、阶段、图鉴、点赞及排行相关状态，并发放本期开局体力。
2. 建立首页活动入口、更新各子模块红点，初始化机器人上下文，向公共待办队列提交活动流程。
3. 首次打开本期入口时展示开启介绍；后续打开可直接进棋盘。`StartPopupShown` 表示本期介绍已展示，不能混同于玩家生涯首次参与。
4. `IsFirstPeriod` 根据活动周期次数判断生涯首次；首次期的开启介绍有关闭限制，后续期允许关闭。
5. 打开主面板后，活动以当前阶段、地图、主链、合成等级上限及本期收纳键请求真实 Runtime。棋盘展示事实驱动引导及外围展示，不以窗口对象刚创建代替展示完成。

定位：`ActMergeTwo.OnOpen`、`OpenFromEntry`、`EnterBoard`、`OpenStageBoard`。[活动上下文][S01]、[生命周期][S02]、[阶段编排][S03]。

### 棋盘推进与换盘

玩家消耗体力发射，通过拖拽合成取得更高等级元素。首次收集事实同步到图鉴、BP 和排行解锁判断；合成点赞按元素配置产生，再推进点赞返奖及排行分数。

每个阶段只允许合成到本阶段配置的主链等级上限。活动检查该阶段所覆盖的主链等级是否全部收集，满足后请求解锁阶段宝箱；宝箱领取结果写入阶段领取标记，再执行换盘。判断依据是收集记录，不要求全部目标此刻仍摆在棋盘上。

正常换盘与“已领奖但换盘未完成”的重入恢复均由服务接管。`CurrentStage`、旧地图数据、阶段宝箱领取标记和收纳数据必须一致，不能只改活动阶段序号而丢弃旧棋盘。最后阶段没有下一张地图，走主链完成提示；主链完成和整期到期分别处理。[阶段编排][S03]、[服务换盘与恢复][S17]。

### 退出与重新进入

未到期退出后，可触发 BP 的退出活动展示；重新进入按本期当前阶段恢复棋盘。到期退出时，若尚有二合体力，先询问是否退出；确认后关闭 Runtime，再启动活动结算，不能在 Runtime 仍占用数据时读取并清理棋盘结算数据。

首页召回、体力提示、BP 展示与棋盘内部待办有各自条件。迁移时应保持“什么业务事实允许展示”，不能将所有弹窗都改为打开主界面时立即出现。[棋盘退出控制][S18]、[活动生命周期][S02]。

## 功能模块

| 模块 | 原始职责 | 主要输入与输出 | 定位 |
| --- | --- | --- | --- |
| Lifecycle | 排期状态、预告、开启、提醒、召回、到期与结算调度 | 周期时间、参与记录、频控 → 入口与窗口 | [S01]、[S02] |
| Gameplay | 主面板、发射、阶段目标、宝箱、换盘、主链完成 | Runtime 结果、阶段配置 → 领取状态与下一阶段 | [S03]、[S14] |
| 棋盘核心 | 地图与占位、拖拽、合成、腾位、发射器、元素产出、奖励和收纳 | 配置、命令、存档 → 玩法结果 | [S15]、[S16]、[S19] |
| 元素能力与效果 | Click、Drag、Merge、Replace、OutPut、Cover、StageBox、LuckyBox、Bonus；玻璃、冰冻、火苗和气泡等 | 元素类型、Function、Effect 配置 → 允许操作与结果 | [S19]、[S20] |
| Album | 收集点亮、逐元素奖励、整链奖励和红点 | 玩法收集记录 → 活动领取记录及奖励 | [S13] |
| Praise | 合成点赞、分档返奖、最高档循环 | Item 点赞余额、奖励档 → 棋盘回流奖励与领取位 | [S08] |
| Rank | 解锁、机器人分数刷新、排行展示与奖励 | 收集等级、点赞、机器人配置 → 排名快照 | [S09] |
| BattlePass | 主链收集任务、免费／付费奖励、购买、挽留和结算 | 收集状态、VIP 权益、领取位 → 待领奖与展示 | [S10]、[S11] |
| Gift | 钻石换体力、现金体力商品、购买订单与奖励交付 | 兑换档、商品、期次 → 体力到账 | [S04]、[S12] |
| EnergyBuff | 限时双倍体力、战前板展示、购买、主线难度贡献与保护状态 | 活动日、期限、付费分层、关卡 → 倍率与难度规则 | [S06]、[S07] |
| RewardReview | 阶段目标和宝箱奖励只读预览 | 阶段／宝箱配置 → 预览，不推进领奖 | `RewardReview/Scripts` |
| Tutorial 与 Prompt | 新手／功能引导、静置提示、遮罩、输入控制和恢复 | 主面板展示、棋盘操作、持久进度 → 引导演出 | [S14]、[S15]、[C08] |

其中棋盘同时有活动主发射器和元素自身的 OutPut 能力，不能把两者统称为“生成器”后使用同一套耗费、次数和恢复规则。普通 OutPut 当前实现包含固定／概率产出、独立剩余次数及耗尽行为，不能从历史参考资料额外补入冷却、轮次或付费加速。

## 规则与数值

### 六阶段与功能限制

| 阶段 | 地图 MapId | 本阶段主链最高等级 | 阶段宝箱 ElementId |
| --- | --- | --- | --- |
| 1 | 11.9-1 | 7 | 2001000 |
| 2 | 11.9-2 | 9 | 2001001 |
| 3 | 11.9-3 | 10 | 2001002 |
| 4 | 11.9-4 | 11 | 2001003 |
| 5 | 11.9-5 | 12 | 2001004 |
| 6 | 11.9-6 | 13 | 2001005 |

主链类型 `MainType=1`。上述等级是各阶段的上限；例如第二阶段检查前阶段上限之后的 8、9 级收集情况。[阶段配置][C03]、`AreStageTargetsCollected` 与 `ResolveStageMaxMergeLevel` [S03]。

活动还向玩法传递两项额外限制：幸运产物 `GeneratorLucky` 在阶段 ID 达到 `LuckyUnlockStage=2` 后允许；新增克隆／附泡 `BubbleCreation` 在 `stageId > 1` 时允许。这些只是附加许可，仍要满足各玩法自身条件。第一阶段禁止新增气泡不等于删除地图预置或恢复出来的已有气泡，也不等于禁止奖励收纳气泡。[阶段创建参数][S03]。

### 体力与三种倍率口径

| 项目 | 本地基线 | 语义 |
| --- | --- | --- |
| 二合体力 | Item 601 | Item 余额为实际权威 |
| 每期开局 | 3 | `PeriodStartEnergy=3`；生涯首次额外值当前为 0 |
| 普通主线成功 | 4 | `LevelEnergy=4`；Trial 排除，活动期及关卡上下文需有效 |
| 自然恢复 | 每 3600 秒 1 点，上限 30 | 30 是自然恢复上限，购买／发奖库存可以超过该值 |
| 过关 Buff | 1 倍或 2 倍 | 关卡开始捕获，成功时按捕获的期次、关卡与倍率交付 |
| 发射倍率 | 1、2、4、8 倍 | 控制棋盘发射档位，与主线奖励倍率分别维护 |
| 难度贡献 | 按付费分层与关卡尾号提供规则 | 属主线难度系统，与上面两种倍率不同 |

自然恢复通过 `ActivityRecoverable` 和活动起止窗口约束。预告或无有效期不应恢复；开局发奖期间临时暂停恢复结算，防止旧恢复基准给新一期多结算体力。[体力编排][S04]、[体力写入][S21]、[公共 Item 定义][C04]、[恢复窗口][S22]。

发射解锁条件为：1 倍常开；2 倍要求主链收集到 6 级；4 倍到 9 级；8 倍要求主链 10 级且当前体力至少 100。同一档全部条件需满足，并要求前面档位已解锁。条件失效时会回锁，所选倍率降为当前可用最高档，已提示档也会调整；它并非永久解锁权益。[倍率实现][S05]、[倍率配置][C05]。

发射还受队列、阶段领奖／换盘、主面板状态、棋盘故障、收纳物品等门禁约束。例如尚有奖励收纳物品时不能直接继续发射。空间不足、体力不足、配置不可用是不同结果，不能统一当作需要购买体力。[主面板][S14]。

### 图鉴与点赞

图鉴配置包含 `ElementType=1、2、4` 三条链。单元素点亮与整链完成使用玩法 CollectionData，单元素／整链领取使用活动 AlbumItemClaim、AlbumClaim；看到元素、已经领取元素奖励、整链收集完成是三种状态。[图鉴数据与领取][S13]、[图鉴配置][C06]。

点赞对应 Item 602，合成按材料元素的 Praise 配置产出。PraiseReward 当前 9 档的阶段需求依次为 `150、250、500、1000、1700、400、1650、300、500`。这些是逐档增量，实际门槛累计计算，不能直接按 TargetValue 的大小排序。最高档完成后，每新增 500 点可继续循环返奖，领取位和重复领取计数共同去重。[点赞奖励实现][S08]、[点赞配置][C07]。

点赞返奖包含棋盘元素，经过玩法奖励交付进入棋盘或同一期收纳。收纳气泡与带限时克隆效果的棋子气泡是不同系统，不能共用创建限制或结算规则。

### 排行与 BP

排行解锁条件为主链类型 1 收集到 5 级。Main 里 8001～8013 的机器人组数量合计 49，加玩家组成 50 人榜；这是本地机器人竞争实现，不能理解为 50 名真实玩家在线匹配。机器人在有效期内按配置刷新，后台暂停后停止刷新计时器，恢复时重新装配。RankInfos 保存快照及上一分数；RankReward 当前有名次 1～10 的奖励。[排行实现][S09]、[活动机器人生命周期][S01]。

BP 有 13 个任务与 13 档双轨奖励，任务对应主链元素 `2000100`～`2000112` 的收集状态，并非单独累加 BP 经验。免费／付费领取分别使用 ulong 位标记；付费资格以 Main.BattleVip 指定的 Item 604 为准，购买商品为 213。退出及到期均可能进入挽留流程；到期 BP 奖励过滤二合体力，具体流程见下一节。[BP 服务][S10]、[结算状态存储][S11]。

### 兑换商店与限时 Buff

| 体力兑换档 | 源端钻石消耗 | 得到体力 |
| --- | --- | --- |
| 1 | 300 | 10 |
| 2 | 900 | 20 |
| 3 | 1500 | 25 |
| 4 | 1900 | 30 |
| 5 | 2900 | 35 |
| 6 | 3900 | 40 |

兑换成功后推进档位，同日超过 6 档沿用末档；日界按 `TimeSeconds / 86400` 计算，不能自行改成设备本地零点。源端钻石 ID 为 2，商品消耗类型 10 表示现金购买引用，不是直接扣除 10 号普通道具。[兑换实现][S04]。

现金体力商品为 214／215／216，对应 60／150／400 体力。Buff 商品为 222／223，对应 1800／3600 秒。源 SKU、商品 ID、展示价格和实际到账须分别理解，目标不能照抄源 SKU。[礼包购买][S12]、[Buff 服务][S07]。

Buff 使用带期限 Item 603，有效时普通主线胜利体力翻倍。免费事件配置为活动第 `2、3、8、9、10` 天，持续 1200 秒，需玩家本期已进入过棋盘，同一日不能重复激活，持续时间不超过整期剩余时间。“活动第几天”按当前日桶减活动开始日桶再加 1 计算，不是精确经过若干个 24 小时。[Buff 活动编排][S06]。

Buff 还实现主线 V2 难度贡献：按近 30 日付费层 NR／LR／MR／MHR／HR／SR 和关卡尾号取规则。当前 NR／LR 匹配 5、9，MR／MHR 匹配 3、5、9，HR／SR 匹配 1、3、5、9；各行 `extraGrade=3、protectStart=1、protectStep=3`。活动提供规则并持久化保护上下文，具体难度运算和失败保护推进由主线系统消费，不应在迁移背景里把字段值直接等同于最终关卡难度。[难度贡献接口实现][S06]。

## 到期与结算

### 到期分流与操作权限

`CanMutateProgress` 允许正常 Opening，以及“WaitToClaim、SettlementStep 为 0、活动主面板仍打开”这一留场分支。留场不等于延期：`CanStartPurchase` 仍要求剩余时间大于 0；主线奖励和 Buff 也要求活动有效窗口。可以在棋盘内继续使用既有资源，不代表继续购买、恢复或领取主线新增体力。

从棋盘退出时，先停止当前 Runtime，再调用 `BeginSettlementFromBoard`。从棋盘外进入时，由活动 ToDo 直接接管结算。`NeedToWaitForClaim` 同时考虑活动结算、BP 购买、奖励展示和 BP 待领奖，旧期未收口时不能用新期覆盖。[活动权限][S01]、[生命周期结算][S02]、[退出控制][S18]。

### 持久化结算游标

| SettlementStep | 当前代码语义 | 关键条件 |
| --- | --- | --- |
| 0 | 尚未进入结算 | 到期留场可保留此值；开始结算后推进 |
| 1 | 排行结算 | 无榜单、已发完或无对应奖励可跳过；发奖结果不确定时保留 |
| 2 | BP 结算准备与挽留选择 | 优先处理可领取免费奖；是否展示补购取决于免费／付费待领奖及 VIP 状态 |
| 3 | BP 待领奖 | 继续处理允许领取的免费／付费奖励，完成后进入棋盘结算 |
| 4 | 棋盘剩余奖励 | 无活动 Runtime 时读取快照，分别展示有奖／无奖结束窗口；确认后推进 |
| 5 | 清理玩法数据 | 服务清理成功后结束旧期结算；重启仍需能恢复清理上下文 |
| 6 | 本期结算完成 | 可交回活动框架刷新状态及后续周期 |

这里是带条件跳转的状态机，不是每个玩家都固定看一遍“排行 → BP → 棋盘”弹窗。[生命周期调度][S02]、[结算存储][S11]。

排行 `RankRewardDeliveryState` 的当前语义为 0 未开始、1 已进入发奖但结果需确认、2 发放完成。代码在正式交付前先写 1，成功后写 2；若恢复时仍为 1，会保留结算并要求对账，不自动重发。这个保护针对特定来源，不代表所有奖励来源已具备完全相同的事务能力。

棋盘剩余奖励只查询配置 `SettlementChainTypes=[3,12]` 所选链，遍历当前地图、BubbleItemList 和 CarryItemList，按各元素剩余 OutPut 次数计算公共奖励；受限制的元素依规则跳过，内部元素产物不作为公共奖励直接发出。活动再次过滤二合体力 Item 601。BP 到期奖励也过滤 601，因此不能把“剩余棋子、体力、未领图鉴”全部统一折算补发。[棋盘结算计算][S23]、[结算过滤与确认][S11]。

图鉴未主动领取奖励不在当前这条到期自动补发链中。若产品决定改变这一行为，应单独确认，不能借迁移顺手补齐。

## 数据与状态归属

| 数据 | 当前权威位置 | 主要写入者与含义 |
| --- | --- | --- |
| 周期、配置、开始／结束时间 | 活动 Profile 的 ActivityData | 活动框架；与业务 State、稳定 PeriodId 分层 |
| 体力／点赞／Buff／BP 权益 | Item 601／602／603／604 | Item 与期限／权益系统；旧 Profile 同名字段不自动成为另一份余额权威 |
| 当前阶段、箱子领取 | MergeTwoData.CurrentStage、StageBoxClaimed | 活动消费真实宝箱领取和换盘结果后写入 |
| BP 免费／付费领取 | FreeClaimBits、PaidClaimBits | BP 交付链；ulong 位容量与索引不可随意改变 |
| 图鉴奖励领取 | AlbumClaim、AlbumItemClaim | 图鉴模块；与玩法 CollectionData 分别保存 |
| 点赞返奖 | PraiseRewardClaimBits、PraiseRewardRepeatClaimCount | 领取位＋最高档循环计数 |
| 排行 | RankInfos、RankRewardDeliveryState | 排行快照及到期交付状态 |
| 发射倍率 | ShootMultiplier、ShootAnnounced | 当前选择、解锁提示状态；不是永久权益 |
| 展示与频控 | StartPopupShown、MainChainFinishShown、BP 与 Lifecycle 字段、LastActivityExposureTime | 对应窗口实际展示及曝光逻辑 |
| Buff 事件与主线保护 | EnergyBuffEventStartTime、EnergyBuffEventDurationSeconds、EnergyBuffAttemptState | 限时事件锚点与难度保护快照；不能只迁 Buff 倒计时 |
| 结算 | SettlementStep、SettlementFromBoard、BattlePassRetainSettlement | 旧期可恢复游标、来源及 BP 挽留结算状态 |
| 玩法数据 | ProfileMergeTwo.DataDic 中的 MergeTwoGameData | 地图元素与唯一 ID、收集、收纳、气泡统计、发射器和静置提示等 |
| 引导进度 | ProfileMergeTwo.Tutorial | 引导组与保存点，生命周期独立于主面板对象 |

玩法模块当前以 `ActMergeTwo` 为独立存档键；活动收纳键为 `MergeTwo:` 加本期 PeriodId。不要把玩法保存键、收纳期次键、活动名、排期 ID 或规则 ID 统一替换成同一个字符串。[玩法模块注册][S24]、[阶段上下文][S03]、[活动 Profile][S25]、[玩法 Profile 根][S26]、[玩法数据结构][S27]。

跨期、换档或服务重建时，回调会核对原 Profile、PeriodId、Runtime 和服务归属。重启恢复依赖已经保存的领取位、地图和结算游标；仅禁用按钮无法代替这些检查。生成 Profile 必须从目标权威定义生成，不能手工修改生成字段来迁就编译。

## 界面与引导

活动外围窗口按 `Lifecycle、Gameplay、Album、BattlePass、Rank、Gift、EnergyBuff、RewardReview、Common` 分目录。首页活动／BP／Buff 入口还位于活动目录外。主面板内部通过 `MergeTwoMainToDoHub` 编排发射、领奖、倍率提示、换盘、子窗口和引导，运行资格会考虑窗口遮挡、场景状态、会话与退出状态。[主面板][S14]、[内部队列][S28]、[首页入口][S29]。

独立引导配置以 `MergeTwoMainShown` 等事件启动，包含点击／拖拽目标、遮罩、对话及保存点；Runtime 负责接入、换盘暂停和释放，主面板提供引导宿主。目标接入 Tutorial 时应保留事件事实、几何目标和业务等待关系，避免“窗口刚打开就开引导”或旧窗口回调推进新一期。[引导配置][C08]、[Runtime][S15]。

旧迁移文档提到的组件替换只是技术适配线索，是否需要转换应对照正式源 Prefab 和当前目标组件逐项核实。不能仅凭旧文本就假定源端所有按钮仍是同一种旧组件，也不能用“无 Missing Script”代替布局、遮挡、音效、点击和退出验收。

## 配置依赖

活动本地专表共 14 张，读取入口统一在活动 `Config` 上下文。程序需核对在线权威源、导出绑定及最终运行配置覆盖结果。[活动 ConfigManager][S30]。

| 表 | 当前本地行数 | 主要作用 |
| --- | --- | --- |
| Main | 1 | 规则、主链、机器人组、初始体力、商品与专属框 |
| GlobalConstCfg | 1 | 频控、体力、Buff 活动日、解锁与结算链 |
| StageConfig | 6 | 六阶段地图、上限、箱子及显示资源 |
| ShootMultiplier | 4 | 四个发射档位及解锁条件 |
| AlbumConfig | 3 | 图鉴链及整链奖励 |
| AlbumItemReward | 1 | 单元素奖励规则 |
| PraiseReward | 9 | 点赞档位及循环返奖 |
| RankReward | 10 | 排名奖励及展示 |
| BattlePass | 13 | 双轨奖励及任务引用 |
| Mission | 13 | 主链元素收集任务 |
| EnergyExchange | 6 | 钻石换体力档位 |
| EnergyShopItems | 3 | 现金体力商品 |
| EnergyBuffShopItems | 2 | 现金 Buff 时长商品 |
| EnergyBuffDifficulty | 6 | 付费层、尾号与难度保护参数 |

棋盘另有 Common、Element、Effect、Coder、Maps、Tutorial 配置。共享依赖包括活动排期及 AB、Item 与奖励转换、Purchase、Robot、PlayerInfo、Locale、Audio 和 XAsset。负奖励键如 `-3、-4` 需先经源奖励转换器解析，不能当作缺失的普通道具 ID。

Main 中 `FrameItemId=12029` 是二合专属头像框，`PeriodDiamondDisplayCount=10000` 是展示配置；展示数字不能代替逐条奖励汇总，也不能反向证明实际可领钻石总额。

## 迁移范围与既有决定

| 内容 | 源端现状 | 现有 V5.2 迁移决定 |
| --- | --- | --- |
| 二合本体 | 棋盘、六阶段、图鉴、点赞、排行、BP、体力商品及 Buff 已有实现 | 保留原规则、数值、界面及交互，在目标接缝适配 |
| Pinata 联动 | ActMergeTwo 实现 IPinataActivityProvider，以期次、窗口和体力 Item 向联动提供上下文 | 排除联动及其独占入口／配置，保留本体正常体力链 |
| FortuneCookie 联动 | 最高档体力商品购买成功后记录本期订单，供饼干 Offer 使用 | 排除该联动，保留本体购买交付和正常订单记录 |
| 二合专属道具 | 601 体力、602 点赞、603 Buff、604 BP 权益 | 保留能力，检查目标 ID 冲突，不当作不支持奖励替掉 |
| 二合专属头像框 | Main 引用 12029 | 保留资源与展示能力，检查目标冲突 |
| 不支持奖励 | 源奖励含目标未必支持的类型及转换键 | 先按源语义解析，再按每个原始奖励位置替换 100 钻；不能整包只补一次 |
| 钻石编号 | MT 为 2 | 现有目标计划按目标 1 映射，执行时核对目标定义 |
| 源 Docs 与 Reference | 含设计、历史验收与其他游戏参考 | 按需阅读；不整包当作运行资产迁入 |

联动依据：[Pinata Provider][S31]、[礼包购买服务][S12]。范围依据：[总控](../../../../TileScape_fresh/Assets/Game/MergeTwo/二合迁移总控.md)与[活动计划](../../../../TileScape_fresh/Assets/Module/Activity/MergeTwo/MergeTwo活动迁移.md)。本节记录既有决定，不新增迁移授权或改动执行顺序。

## 交给程序核实的事项

| 核实项 | 当前背景 | 需要带回的结果 |
| --- | --- | --- |
| 正式源版本 | 当前调研 dev 与旧计划源不同 | 实际源提交，以及规则／配置／接口的相关差异 |
| 目标排期与 AB | 源基础表 99999，AB104 B 为 35／43 | 目标权威行、实际生效分支、门槛、日界及晚开行为 |
| Item 与奖励语义 | 余额、期限、权益有各自宿主；存在负奖励转换键 | 实际映射、每个奖励位置差异、到账与展示一致性 |
| Buff 主线接入 | 体力翻倍与难度贡献是两套消费者 | 开局捕获、成功／失败／重玩、保护状态、跨期与 Trial 的真实行为 |
| 支付与补单 | BP、体力和 Buff 各有商品及期次上下文 | 有效 SKU、沙盒交付、重复回调、迟到／跨期订单处理 |
| 换盘与恢复 | 领奖位、旧图、收纳与新阶段需要一致 | 领奖后退出／重启、换盘中断、最后阶段再次进入 |
| 到期留场 | 可操作、可买、可恢复、可领奖不是同一个权限 | 棋盘内／外到期、带体力退出确认、重入后的实际分流 |
| 结算中断 | 有持久游标、排行不确定态及过滤规则 | 发奖前后中断、状态 1 对账、BP 挽留、棋盘清理恢复 |
| UI 与引导 | 共享主面板队列、展示事实及输入门禁 | 真实入口、新手与后续期、子窗口遮挡、换盘、关窗和后台恢复 |
| 投递与初始化 | 配置、服务、Profile、资源均有就绪顺序 | 生产创建链、目标真实构建和无缓存投递证据 |

这侧继续负责规则解释、源端差异分析、产品取舍整理及背景更新；程序执行迁移、导表、资源适配、编译和运行验证后，将结果与新发现回填到各自交付文档。若新发现改变玩家行为、奖励、期次、存档兼容或既有范围，应先同步具体差异，再调整对应设计，不能用技术适配默认改变规则。

## 源码定位索引

源码与执行计划链接按当前 Windows 的并列工作区布局解析：LG 为 LibraryG、源为 meatloaf_client01/client、目标为 TileScape_fresh。其他设备若目录名称或位置不同，按项目根重新定位，不直接套用本机链接；文件名、类型和方法仍可用于搜索。行号会随提交变化，索引以文件与符号为主。

| 主题 | 优先搜索的符号 | 依据 |
| --- | --- | --- |
| 活动注册与期次 | ActMergeTwo、OnOpen、NeedToWaitForClaim、CanMutateProgress | [活动上下文][S01] |
| 首进与结算 | OpenFromEntry、SelectReminder、OpenSettlementStep、FinishLifecycle | [生命周期][S02] |
| 阶段与恢复 | OpenStageBoard、AreStageTargetsCollected、OnStageBoxClaimed、CommitStage | [活动阶段][S03]、[玩法换盘][S17] |
| 体力交付 | OnPowerGameStateChanged、TryExchangePower、CapturePowerLevel、TryGrantLevelPower | [活动体力][S04]、[体力存储][S21] |
| 发射档位 | Prepare、Cycle、IsUnlocked | [倍率][S05] |
| Buff 与难度贡献 | CanStartEnergyBuffEvent、TryActivateEnergyBuffEvent、GetV2DifficultyRule | [Buff 编排][S06]、[Buff 服务][S07] |
| 点赞返奖 | PraiseRewardThreshold、TryDeliverPraiseReward | [点赞存储][S08] |
| 排行 | TryUnlock、RefreshRobotScores、GetPlayerRank | [排行控制][S09] |
| BP | ReadMissionCompletion、HasPendingClaims、TryPrepareBattlePassSettlement | [BP 服务][S10]、[结算存储][S11] |
| 商店与联动 | MergeTwoGiftPurchaseService、RecordHighestEnergyTierPurchase | [礼包服务][S12]、[Pinata][S31] |
| 图鉴 | MergeTwoAlbumDataSource、MergeTwoAlbumItemState | [图鉴数据][S13] |
| 主窗口与内部队列 | UIActMergeTwoMainPanel、MergeTwoMainToDoHub | [主面板][S14]、[队列][S28] |
| 玩法装配 | MergeTwoModule、MergeTwoRuns、MergeTwoRuntime、LogicSystem | [模块][S24]、[服务][S16]、[Runtime][S15]、[逻辑系统][S19] |
| 棋盘剩余奖励 | MergeTwoSettlementRewards.TryRead、CalculateRemaining | [结算计算][S23] |
| Profile 与数据键 | MergeTwoData、ProfileMergeTwo、MergeTwoGameData | [活动档][S25]、[玩法根][S26]、[玩法档][S27] |

[S01]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/ActMergeTwo.cs
[S02]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/ActMergeTwo.Lifecycle.cs
[S03]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/ActMergeTwo.Stage.cs
[S04]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/ActMergeTwo.Power.cs
[S05]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/MergeTwoShootMultiplier.cs
[S06]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/ActMergeTwo.EnergyBuff.cs
[S07]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/EnergyBuff/Scripts/Logic/MergeTwoEnergyBuffService.cs
[S08]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/MergeTwoProfileStore.Praise.cs
[S09]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/MergeTwoRankController.cs
[S10]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/BattlePass/Scripts/Logic/MergeTwoBattlePassService.cs
[S11]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/MergeTwoProfileStore.Settlement.cs
[S12]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Gift/Scripts/Logic/MergeTwoGiftPurchaseService.cs
[S13]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Album/Scripts/Data/MergeTwoAlbumData.cs
[S14]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Gameplay/Scripts/UIActMergeTwoMainPanel/UIActMergeTwoMainPanel.cs
[S15]: ../../../../meatloaf_client01/client/Assets/Game/MergeTwo/Scripts/Game/MergeTwoRuntime.cs
[S16]: ../../../../meatloaf_client01/client/Assets/Game/MergeTwo/Scripts/Services/MergeTwo.cs
[S17]: ../../../../meatloaf_client01/client/Assets/Game/MergeTwo/Scripts/Services/Service/MergeTwoStages.cs
[S18]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Gameplay/Scripts/UIActMergeTwoMainPanel/Board/MergeTwoMainBoardController.cs
[S19]: ../../../../meatloaf_client01/client/Assets/Game/MergeTwo/Scripts/Game/Logic/LogicSystem.cs
[S20]: ../../../../meatloaf_client01/client/Assets/Game/MergeTwo/Scripts/Game/Logic/Entity/Function/ElementFunctionRegistry.cs
[S21]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/MergeTwoProfileStore.Power.cs
[S22]: ../../../../meatloaf_client01/client/Assets/Scripts/Game/Module/ActivityItemRecoveryWindow.cs
[S23]: ../../../../meatloaf_client01/client/Assets/Game/MergeTwo/Scripts/Services/Service/MergeTwoSettlementRewards.cs
[S24]: ../../../../meatloaf_client01/client/Assets/Game/MergeTwo/Scripts/Services/MergeTwoModule.cs
[S25]: ../../../../meatloaf_client01/client/Assets/Scripts/Profile/ActivityProfile/MergeTwoData.cs
[S26]: ../../../../meatloaf_client01/client/Assets/Scripts/Profile/MergeTwoProfile/ProfileMergeTwo.cs
[S27]: ../../../../meatloaf_client01/client/Assets/Scripts/Profile/MergeTwoProfile/MergeTwoGameData.cs
[S28]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Gameplay/Scripts/UIActMergeTwoMainPanel/ToDo/MergeTwoMainToDoHub.cs
[S29]: ../../../../meatloaf_client01/client/Assets/Module/MainEntry/Entries/ActMergeTwo/UIActMergeTwoEntry.cs
[S30]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/Config/ConfigManager.cs
[S31]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Scripts/ActMergeTwo.Pinata.cs
[C01]: ../../../../meatloaf_client01/client/Assets/Activity/Activity/Config/activityconfig.json~
[C02]: ../../../../meatloaf_client01/client/Assets/Activity/Activity/Config/activityconfig_ab104_b.json~
[C03]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Config/stageconfig.json~
[C04]: ../../../../meatloaf_client01/client/Assets/Module/Common/Config/item.json~
[C05]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Config/shootmultiplier.json~
[C06]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Config/albumconfig.json~
[C07]: ../../../../meatloaf_client01/client/Assets/Activity/MergeTwo/Config/praisereward.json~
[C08]: ../../../../meatloaf_client01/client/Assets/Game/MergeTwo/Config/Tutorial/main.json~

## 关联

- [[02-PROJECTS/TileScape/_MOC|TileScape 知识库入口]]
- [[02-PROJECTS/TileScape/参考/快速定位与资源替换索引|路径与配置定位索引]]
- [[02-PROJECTS/TileScape/参考/Docs文档索引|项目 Docs 与 LG 主档关系]]
- [[02-PROJECTS/TileScape/参考/二合活动/01-调研报告-MergeFantasy|Merge Fantasy 竞品对照]]：用于另行讨论 TS 改造方向，不作为 MT 原始规则来源。
