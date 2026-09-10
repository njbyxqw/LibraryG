---
title: DLC 全链路梳理与维护
date: 2026-09-08
type: task
status: in-progress
project: TileScape
lifecycle: current
verification: code-and-config-static-only-runtime-pending
cat_order: 030
tags: [TileScape, DLC, HomeScene, Endless, Activity, 长期任务]
source: "09-07 全链路基线 dev @ 8e730d376；09-08 Home 调度增量 dev @ 1e323e6e8 / 12e6620af；各节区分版本与静态验证范围"
---

# DLC 全链路梳理与维护

> 最新 Home 下载调度见 [[02-PROJECTS/TileScape/游戏逻辑/任务-DLC全链路梳理与维护#2026-09-08 Home 下载优化|2026-09-08 Home 下载优化]]；下方 09-07 基线保留历史。其他主题仍按各自来源版本解读。

## 背景、目标与范围

这是 DLC 的唯一长期任务主档。首轮把分散在 Home DLC、Endless 最大关卡、活动设计和 QA 中的说明按玩家旅程连起来，讲清“何时需要资源、何时能用、失败后怎么办”，后续直接更新本文，不按日期创建同题快照。

玩家安装后先得到基础资源，启动时补齐必要章节地图；进入 Home 后静默准备封面和临近地图。点击进关或历史画廊时仍需检查资源可用性。服务器提高最大关卡只提供新边界，不能代替地图和关卡配置。活动自身开启与资源可展示资格也分别判断。

本轮完成文字梳理、代码与配置静态复核、历史纠偏、LG 导航与 Daily。未来业务实现仅列建议，尚未授权执行。本轮不改 TS 代码、配置、资源、团队规则或源码旁 `DLC.md`；不提交、不推送、不创建定时自动化。长期任务保留为人工继续入口，不表示后台持续执行。

## 来源与版本

- 首轮核对时间：2026-09-07，Asia/Shanghai；2026-09-08 续做文档闭环，重新核对主仓库与下列嵌套库 HEAD 未变化。事实源为 `/Users/dean/TileScape` 的当前 `dev` 工作目录，HEAD 为 `8e730d376575e4cd67547fbdf60dcc2ee4b826d6`。有与 DLC 无关的用户未提交内容，本轮未修改。
- 底层嵌套库：`Packages/BettaSDK` 为 `d751f4f5740de568b3315d4986851c20ca527662`；`Packages/BettaFramework` 为 `5b74cd1e56b81e9690d89adac448fd7cae23200a`；两者本轮查看时工作区干净。
- 本文路径除 LG wikilink 外均相对 TS 根目录。主仓库 commit 不代表嵌套库版本，更新本文时应同时核对。
- 已对照 `/Users/dean/LibraryG` 与本任务工作树的 LG 入口、规范和 TileScape 文档；首轮读取时相关内容一致，初查两处均无同题主档与当日 Daily；落基线时原始 vault 已有另一任务新增的 9 月 7 日 Daily，续做时重新读取并保留其正文。
- `Assets/Module/HomeHub/HomeScene/Scripts/DLC/DLC.md` 是源码旁来源；2026-09-07 标注的 Ocean 迁移不是发布成功证据。其配置路径、占位图及启动选项等仍有漂移，冲突以当前代码和 `.bytes` 为准。
- 本轮按生成类型的 `ProtoMember` 字段号直接解码 `.bytes`，复核章节、提前窗口、活动/礼包映射及开启关卡；不是只读 `*.json~`。运行时格式由 `Packages/BettaFramework/Scripts/Runtime/Tool/ToolConfig/ConfigRuntimeConst.cs` 指定为 ProtobufNet；备份 JSON 不代表运行时数据。
- 原始需求来源：DLC 下载逻辑 (2)，任务 ID `01a01d59-195b-7660-971f-692b4eaa3867`（本任务收到的交接）；本轮按源码重新复核实现，历史用户目标按交接保留，不把交接摘要当当前代码证据。
- 历史来源为下方关联的 08-20 梳理、08-25 设计、08-26 审计，以及显式读取的本地 ignored 文档 `Docs/Knowledge/Local/Inbox/2026-09/Activity_DLC_QA_Functional_Test_Guide_2026-09-01.md`。历史“验收过”的说法不升级为本轮 dev 已运行验证。
- 证据边界：只做静态阅读、数据解码、文档路径与链接核查；未执行 Unity 编译/EditMode、资源构建、Player 构建、Jenkins、上传、CDN、服务端联调或真机验证。

## 先分清四种东西

| 对象 | 控制什么 | 不能据此推导什么 |
|---|---|---|
| 章节地图 Package | 地图 `.bytes`、Segment Prefab 及依赖能否加载 | 不代表封面、普通关卡配置或新 max 已就绪 |
| 章节 UI Package | Gallery / 解锁封面能否使用；未 Ready 用占位图 | 封面出现不代表地图可进入 |
| 普通关卡配置 | Levels → LevelGroup → 关卡文件可加载，另有既有动态关卡链路 | 不属于 Home 地图下载成功的必然结果 |
| 服务器 `maxLevel` | 候选普通/Endless 边界 | 不是资源包，也不是立即生效的服务器推送 |

所有实际 DLC 资源加载前，以 `CanUseAssets` / 底层 `CanUsePackageAssets` 为门禁。文件存在、下载百分比 100、已经发起请求都不能代替可用性校验；空 PackageId 的包体资源按可用处理。

## 2026-09-08 Home 下载优化

> [!important] 当前 Home 下载入口
> 本节取代下方 2026-09-07 基线中的协调器、两个 DLC Flow 与后台队列调度说明；旧正文保留供对照，不作当前调用入口。此次只增量复核 Home 下载优化及其相关门禁，活动构建配置等同期变化未在本节做完整复审。

**来源与范围**：TS 当前 `dev @ 1e323e6e85949ed46f6bf25c0fc6049540f70ce9`；关键提交 `12e6620af86653c09c8b78470c546aaef8fce8ba`，2026-09-08 16:30:02 +0800，提交标题“关卡地图/画廊主题 DLC 下载逻辑优化”。本轮约 20:31（Asia/Shanghai）读取当前工作目录，相关 Home/接口目录无未提交修改。底层会话/调度器另核对 `Packages/BettaSDK @ fd285b92795531ed70218697ef8ad90903ef86db`。不把提交作者工作记为本轮实现；本轮只读复核与 LG 文档维护。

### 职责拆分与真实路径

旧 `HomeHubDlcCoordinator`、`FlowItemHomeDlcBackgroundPreload`、`FlowItemHomeDlcPreLevelDownload` 及两个 Flow 注册点已删除。当前由 `HomeHubDlcModule` 构造一个共享队列和两个策略，按 Gallery UI、章节地图顺序放入 `IHomeDlcPreloader[]`：

- 组装与生命周期：`Assets/Module/HomeHub/HomeScene/Scripts/DLC/HomeHubDlcModule.cs`。
- 策略接口：`Assets/Interface/HomeScene/DLC/IHomeDlcPreloader.cs`；业务入口仍通过 `IHomeHubDlc.RequestHomePreloads`。
- UI 策略：`Assets/Module/HomeHub/HomeScene/Scripts/DLC/Preload/GalleryThemeDlcHandler.cs`，Id 为 `ThemeUI`。
- 地图策略：`Assets/Module/HomeHub/HomeScene/Scripts/DLC/Preload/ChapterMapDlcHandler.cs`，Id 为 `PreLevelMap`；同时承接启动收集、前台进关/Gallery 门禁及地图快照查询。
- 串行队列：`Assets/Module/HomeHub/HomeScene/Scripts/DLC/Download/HomeDlcBackgroundQueue.cs`，两策略共用实例，不各建下载队列。

模块中仍保留 `StartHomeBackgroundPreload`、`RequestCurrentLevelChapterPreload` 的定向转发方法；删除的是旧 Flow 及集中协调器，不能误写为所有原有业务方法均删除。

### 何时触发，哪些“回 Home”不触发

`Assets/Module/HomeHub/State/HomeSceneState.cs:OnEnter` 开始阶段即调用 `RequestHomePreloads`，发生在 `IHomeScene.EnterHome(TransitionObj)`、打开 UIMain 和初始化/执行 HomeFlow 之前。只提交后台请求、不等待下载，首次进 Home、普通关或无尽关返回 Home 都会重新评估；即便随后 HomeScene 准备失败，也已经尝试过两类预下载。

这里没有预下载“一次执行”标记。`_enterHomeReadyInvoked` 仅限制稍后的 UI/Flow 准备回调，不限制预下载；不能因名称相近混用两者语义。`RequestHomePreloads` 对两个策略分别 try/catch，一项抛异常仍运行另一项，下一次进入再次计算。没有按上次已评估跳过的持久标记。

Gallery 章节预览返回当前 Home，走 `Assets/Module/UIMain/Script/UIMainPanel.cs:RestoreCurrentHome → IHomeScene.EnterHome()`；这是场景内容恢复，不重新调用 HomeSceneState.OnEnter，因此不会额外触发统一预下载。该区别不影响先前已提交的后台任务继续执行。

### 候选、串行队列与重试

Gallery 策略仍遍历所有主题 UI Package，过滤空值、在候选内去重。地图策略仍读取已完成普通进度 `ILeveledGame.CurrentLevel()`，取当前 Home 章节起点到 `completed+ChapterDLCPreLevel` 的连续章节窗口（沿用既有 50 关配置）；无尽局数不扩大窗口。

两策略先提交候选，队列统一以 PackageId 去重，**执行单包时才再次 GetSnapshot 检查 CanUseAssets**。不要沿用旧稿“策略收集时已过滤全部 Ready”的实现描述。若排队期间前台已使地图 Ready，轮到它时直接跳过。队列串行调用 None + Low、`retryTimes:2`；没有前台提示，也不阻塞 Home 业务/动画。

GetSnapshot 或 Ensure 同步/异步异常在单包内捕获，失败不阻断后续包；finally 移除该包的 scheduled 标记，所以后续 Home 进入可再次提交。成功后也移除标记，下次可以作为候选再进入并被 Ready 检查跳过；这不等于重新下载。两个策略间也共享去重，避免同时候选造成重复后台请求。

前台 High 请求不等待 Home 业务队列轮到自己：它直接通过统一服务 Ensure。底层 `DownloadableContentManager` 按 Package 复用 ActiveDownloads 会话；`DownloadableContentDownloadScheduler` 仅调整等待项优先级、在当前 Lease 释放后选下一项，**不会抢占正在运行的 Low 下载**。若目标已在运行，前台加入该会话；如果仅在 Home 队列等待，前台可以先发起，后续后台执行时再看 Ready。

### 生命周期、保留的门禁语义

HomeSceneState.OnExit 不取消模块队列；进关或页面切换后，已提交任务仍由模块持有。只有 HomeHubDlcModule.Dispose 才清队列、取消 lifetime、解绑 PackageStateChanged；完成前台异步等待后也检查 disposed/取消，不能因晚到 Ready 继续进关/预览或提交后续地图预载。清队列与取消本模块等待不应笼统等同于取消其他订阅者共享的物理下载。

本次保留启动窗口 `completed+10+1` 的终点算法（配置提前 10 关），以及前台检查待进关和后一关、一次处理一个缺包、成功后本次仍不进关的语义；方法迁到 ChapterMapDlcHandler。Gallery 仍先 None/High，失败再加前台选项；有实际 DownloadedBytes 时需再次点击，零下载字节的成功可继续预览。模块释放期间新增加的晚到结果保护不改变正常成功路径。

### 测试来源、验收与下一步

原 `HomeHubDlcCoordinatorTests.cs` 重命名/调整为 `Assets/Module/HomeHub/HomeScene/Tests/Editor/HomeDlcHandlerTests.cs`。新增同目录 `HomeDlcPreloadTests.cs`、`HomeDlcConfigScope.cs`、`HomeDlcTestDoubles.cs`；`HomeProgressFlowContractTests.cs` 与 `ChapterUnlockDlcAssetAccessTests.cs` 相应调整旧 Flow 契约和接口假实现。

本轮静态阅读可看到测试意图包括：每次状态进入都先于场景准备请求、两策略异常隔离、同策略单包快照异常不丢后续候选、共享串行去重、失败下一次进入重试、异步异常继续、Dispose 取消/清队列、前台提前准备地图后后台跳过 Ready、前台晚到结果拒绝。测试源码存在不代表本轮已执行通过，状态测试也不能代替首次/普通/无尽三个真实玩家流程的设备证明。

- [x] 当前实现与提交差异静态复核；旧 Flow/协调器入口标为历史，主档与速查入口更新。
- [ ] 按实际交付需要运行相关 Editor 测试，验证首次/普通/无尽进 Home、Gallery 直接恢复、异常隔离、重复进入、Home 退出与模块 Dispose。
- [ ] 最新资源构建、Player、CDN 与真机下载结果仍未验证；本节不解决既有“新 max 缺图时不主动下载、不自动重应用”的需求差距。

下次查当前 Home 下载先读本节，再进 HomeSceneState、HomeHubDlcModule、两个 Handler 与共享队列；旧协调器/Flow 路径只用于 Git 历史追溯。本轮未修改 TS 代码、配置、资源、源码旁文档或团队规则，未 commit/push。

## 2026-09-07 基线实现链路：按玩家旅程阅读

### 1. 安装资源与章节映射

当前 Forest 是包体章节；Ocean、Candy、Desert、Ice、Garden 各有地图和 UI 两个 Package，共十个 Home Package。Endless 自身主题资源仍在包体。此处描述作者配置，不声称已检查实际安装包。

| 普通关卡范围 | 主题 | 地图 Package | UI Package |
|---|---|---|---|
| 1–50 | Forest | 空 | 空 |
| 51–100 | Ocean | `HomeHub.Theme.Ocean` | `HomeHub.Theme.OceanUI` |
| 101–200 | Candy | `HomeHub.Theme.Candy` | `HomeHub.Theme.CandyUI` |
| 201–300 | Desert | `HomeHub.Theme.Desert` | `HomeHub.Theme.DesertUI` |
| 301–400 | Ice | `HomeHub.Theme.Ice` | `HomeHub.Theme.IceUI` |
| 401–500 | Garden | `HomeHub.Theme.Garden` | `HomeHub.Theme.GardenUI` |

运行时章节表为 `Assets/Module/HomeHub/HomeScene/Config/Chapter/Data/chapter.bytes`；封面表为同目录 `chaptertheme.bytes`。地图读取 Chapter 的 `PackageId`、`AssetPathCfg`，封面读取 ChapterTheme 的 `PackageId`、`ThemeAreaCover`、`ThemeAreaCoverLoading`，不按路径是否含 `ResDLC` 猜归属。

DLC 地图位于 `Assets/Module/HomeHub/HomeScene/ResDLC/Theme/<Theme>/`，UI 位于同级 `<Theme>UI/<Theme>GalleryCover.png`。Forest 封面当前为 `Assets/Module/UIGallery/Texture/ForestGalleryCover.png`。所有当前章节表配置的占位图是 `Assets/Module/HomeHub/HomeScene/Res/Theme/Default/Default.png`，不再是源码旁说明中的 `Chatper.png`。

总 Package 配置的真实路径是 `Assets/Betta/Resources/Config/BettaDownloadableContentConfig.asset`。十个 Home Package 均指向 `HomeHubDLC`，`includeInPlayerForCopy=0`；Build 为 `Assets/Module/HomeHub/XAsset/HomeHubDLC.asset`。**共享 Build 表示共享清单与发布边界，并不表示请求一个包就下载整个 Build。** `Packages/BettaSDK/Hub/DownloadableContent/DownloadableContentPlan.cs:TryResolve` 先展开 Package 资产，再取主 Bundle 与依赖去重。物理下载量取决于实际 Manifest 的 Bundle 闭包和缓存，共包/共享依赖可能带来重叠。

发布需要匹配客户端的资源清单、Bundle 和可用下载地址；作者配置完整不能代替发布证明。源码旁文档提到的旧 iOS 构建也不能证明最新 Ocean 和封面调整已发布。本轮不触发发布；后续验证项见下文。

### 2. 启动：先补必要资源，再初始化业务

`Assets/Scripts/GameMain.cs` 的 `Start` 在 `PrepareBaseRuntime` 构造模块后收集 `IApplicationLoadingRequireDownloadableProvider` 声明，先等待 Gate，再执行 `InitializeModules` 与 `Init`。Provider 只声明 Package，不自行下载或提前创建活动 UI。

Home 由 `HomeHubDlcModule` 读取 `ILeveledGame.CurrentLevel()` 的已完成普通关卡数，协调器收集从当前 Home 章节起点到窗口终点连续覆盖的地图包。当前 `constconfig.bytes` 为 `ChapterDLCLoadingPreLevel=10`，代码终点为 `completed + 10 + 1`，含“接下来可玩的那一关”。不应只用 `completed+10` 做区间相交，否则在章节边界错一关。窗口越过末章时只保留已配置章节；空包跳过，按章节配置顺序去重。

`Assets/Module/ApplicationLoading/ApplicationLoadingRequireDownloadableGate.cs` 逐包以 Normal 优先级等待，选项为 `CheckNetwork | AlertOnFailure | NonDismissibleFailureNotice`。Loading 使用传入进度自行展示，不创建默认下载进度窗。

已有 Runtime Ready 可直接使用；重启后本地文件齐全但运行时状态未恢复时仍需校验。离线启动先尝试本地校验，只有可用才能继续；缺文件或校验失败不能放行。启动无网和下载失败提示都继承不可关闭标志，重试重新检查；生命周期取消或最终 Gate 失败不当作成功进入业务。

### 3. 进入 Home：后台下载不阻塞旅程

`FlowItemHomeDlcBackgroundPreload` 每次 Home Flow 执行时提交所有章节 UI 包的后台计划。`FlowItemHomeDlcPreLevelDownload` 每次回 Home 以普通完成进度提交地图计划，不使用无尽局数。

地图当前 `ChapterDLCPreLevel=50`，终点是 `completed+50`，从当前 Home 章节起点连续覆盖；与启动窗口的额外 `+1` 区别必须保留。UI 包与地图包共用协调器队列，跳过空包、重复、已 Ready 与已安排的请求，按队列顺序以 Low、`None`、`retryTimes:2` 执行。Flow 提交后立即结束，不等待下载，不显示确认、进度或失败弹窗。

成功只恢复资源可用状态，供后续入口使用；失败记录后退出当前队列任务，后续回 Home/业务事件可以再安排。Endless 中普通完成进度不随无尽局数增加，因此反复回 Home 可以重试同一窗口，不会自然扩大预取范围。协调器 Dispose 清队列、取消自己的等待；不能把一次回 Home 等同于模块销毁。

### 4. 点击关卡：缺一个包就停止本次进入

`TabBarHome → IHomeScene.TryEnterLevelAsync → IHomeHubDlc.EnsureCurrentLevelEntryAsync → HomeHubDlcCoordinator.EnsureLevelEntryAsync`。模块读取一次普通完成进度，以待进关和后一关的区间取得地图包。普通非末关通常是同一个包；章节末关涉及下一章。随后还按同一完成进度提交后台地图计划。

已 Ready 全部通过后才继续原进关逻辑。遇到第一个缺包，以 High、`CheckNetwork | AlertOnFailure | ImmediateNoNetworkNotice` 和 `DefaultNotice` 发起或加入下载；这里没有 `ConfirmDownload` 大小确认。离线且未 Runtime Ready 会立即提示无网。

只要这次点击进入缺包分支，即使下载成功也返回 false，玩家需再次点击。一次最多处理一个缺包；若当前章和下一章均缺，可能多次点击分别补齐。关闭下载进度窗只隐藏显示，不取消下载；下次点击可以重新观察同一下载。关闭无网/失败重试窗则结束该次前台等待或失败处理，本次不进关，后续点击可再试。High 优先级不能据此解释为一定中断已经执行的 Low 下载。

### 5. 画廊：封面和地图预览独立判断

Gallery 创建 Cell 不等待 UI 包；UI 未 Ready 就显示表中占位图，Home 后台准备封面。已完成章节的预览点击检查的是地图包，不能以封面显示正常判断可预览。

`GalleryChapterCompleteStateView` 对 Ready 地图直接预览；缺图时防重复点击并请求 `RequestGalleryPreviewChapterDownloadAsync`。该方法先用 High + `None` 静默 Ensure，不先弹网络提示。若成功且无实际下载字节（无 DownloadResult 或 `DownloadedBytes==0`），本次可以预览；若实际下载了字节，本次不预览，下次点击再进入。

第一次 Ensure 被取消则结束；其他失败才改用 High + 前台网络/失败提示选项再 Ensure，成功后的字节判定相同。Cell 显示 `Previous/loading` 旋转；完成后还核对 Cell 绑定章节未改变。重用 Cell 或页面退出不能让旧结果打开别的章节。此入口不使用关卡按钮的默认进度窗。

### 6. 章节解锁：展示前再守门，不负责下载

`FlowItemHomeChapterUnlock`、`FlowItemHomeEndlessExitChapterUnlock`、`UIChapterUnlock` 和 `HomeSceneController` 保护目标地图加载。`ChapterUnlockDlcAssetAccess` 分别判断地图可用性、封面选择：地图未 Ready 阻断切图；UI 包未 Ready 允许封面占位。异常路径可显示资源不可用提示，但这个提示本身不等于执行一次目标包 Ensure。

正常章末已由进关按钮预先检查下一章；解锁处是兜底。Flow/窗口不会主动下载缺地图，也不承诺下载后来完成会自动恢复这次已结束的解锁。地图 Ready 后才可加载章节配置与 Segment、重建地图；Endless 退出的桥接还需满足下面的新 max 应用条件。

### 7. Endless 与新 max：胜利返回时两阶段应用

当前链路已经不要求重启，但**不是每个 `lv_end` 都请求，也不是服务端一改值就立即应用**。

1. 玩家在胜利面板继续，`UIWinPanel.FinishAndClose` 先 `TryCompleteWinResult` 完成结算，再调用 `TryPrepareSuccessfulReturn`。
2. 只对 Endless 胜利来源或普通有效最大关卡胜利来源请求 `LoadConfigRequest(ConfigKey="maxLevel")`；普通非边界关、回放、Trial 不走此检查。失败/放弃/退出没有这条胜利继续触发。本轮读取的 `TileMatch.Init` 也没有旧文档所说的初始化服务器请求。
3. 返回值必须能解析为整数，经本地上限/策略校验后大于当前 `EffectiveMaxLevelId`，且覆盖下一普通关。通过后只存 pending，保留旧 max、下一关、完成进度、是否 Endless 与生命周期版本。回调完成后才关闭胜利面板、结束 Tile Flow 并发起返回 Home；请求失败或无新边界按现有回调继续返回。
4. `TileMatchSceneState.OnExit` 先 `ExitGame`，目标为 Home 时调用 `TryApplyPendingMaxLevel`。这是离开局内、进入 Home 的转换阶段，不是 Home 已显示后任意时刻热切。去其他场景则清 pending。
5. 应用时先取出并清 pending，再核对生命周期、旧 max、下一关及候选。下一普通关所属章节必须 `CanUseAssets`，并由 `TryValidateNormalLevelLoadable` 检查 Levels、LevelGroup 路径与实际关卡文件可加载。
6. `ApplyServerMaxLevel` 先成功构建新的 Endless 池，再更新有效 max、存档 max、清无尽索引并提交池。外层刷新派生缓存、保存 Profile、预取接下来关卡；Endless 胜利来源额外写 `HomeEndlessExitUnlockBridge`，供 Home Flow 展示 `UIChapterUnlock` 并重建地图。

任一步失败都保留旧有效边界并继续既有 Home 转换。**缺资源时不弹下载窗；pending 已清除，后台后来 Ready 不会自动重应用。** 下一次合适的胜利返回重新请求，届时条件齐全才可能成功。服务器 max 上调也不会帮客户端生成不存在的章节或普通关卡文件；这里只验证下一普通关可加载，不能概括为整个新范围已逐关验收。

### 8. 活动：当前已启用范围与设计分开

`CatalogLoader.LoadDlcMapRows` 合并两个实际目录：

- 活动：`Assets/Module/Activity/Activity/Config/Data/dlcmap.bytes`，配套 `main.bytes`。
- 礼包：`Assets/Module/Activity/Gift/Config/Data/dlcmap.bytes`，配套 `main.bytes`。

旧 `Assets/Module/Activity/Core/Config/Data/activitydlcmap.bytes` 不是当前有效路径。解析键仍是 `Activity.{activityName}.{themeKey}`；无映射、空列表或 `EnforceDlc=0` 返回基础包需要集。

| 对象 | 当前 openLevel | EnforceDlc | RequireOnStartup | 本轮配置结论 |
|---|---:|---:|---:|---|
| GiftFirstPay | 28 | 1 | 0 | Config + Theme.Default；总配置有对应两包，Build 为 GiftFirstPayDLC |
| GiftIceBreak | 28 | 1 | 0 | Config + Theme.Default；总配置有对应两包，Build 为 GiftIceBreakDLC |
| ActDailyBonus | 25 | 0 | 0 | 映射保留，当前 DLC 未启用，总 Package 配置未列签到两包 |
| ActGoldCard | 17 | 0 | 0 | 映射保留，当前 DLC 未启用，总 Package 配置未列金卡两包 |

这张表是仓库静态配置，不代表某账号当时已开启活动；仍受分层、时间、业务条件及运行时配置覆盖影响。Protobuf 中省略的整数标记按生成类型默认 0 解读。旧 QA 的首充/破冰 23 关、签到 DLC 开启与启动测试值 1 都不适用于当前配置。

进入 Home 时，活动模块扫描已初始化活动；距 openLevel 前 10 关或已越过 openLevel 且缺资源时后台准备，不要求活动已 Open，也不把礼包可购买资格作为该下载门槛。Preview/Open/Resume 事件也会触发检查，且这条事件路径不应用关卡距离筛选，不能再写“仅 EnterHome 请求”。

协调器按当前需要集逐包 Low + None、`retryTimes:2`，跳过 Ready，活动代次去重；一个包失败后仍可尝试后续包。常规请求不弹确认/进度/失败窗、不阻断其他基础功能。完成或 Package 状态改变会刷新展示资格，但不会直接强开面板。

`ActivityBase.CanPresent = IsActive(Open) + 全部需要包 CanUseAssets`；正式入口、Banner、强弹、开窗路径还受原业务规则约束。`EnsurePresentationAsync` 当前只检查资格，不会给未 Ready 活动发起前台 High 下载。DLC 缺失不会自行把 Open 改为 Finished。

启动能力已接入：`GameMain` 构造 ActivityModule 并参与 Provider 收集，不再有旧审计的 `startupGateEnabled=false` 全局禁用。需要同时满足映射启用、`RequireOnStartup!=0`、存档状态 **仅 Open**、未过期；收集 Default 主题需要集交 Gate。Preview 不合格。**当前四个映射标记全部为 0，所以当前配置不产生活动启动必需包；能力存在与当前启用必须分开。**

Finish/Close 通过提高活动代次使旧任务失效，停止后续包与旧结果恢复展示；并不保证当前底层物理下载立即停止。Dispose 才取消模块生命周期等待并解绑事件。后续 Home 或生命周期事件是常规重试入口，不是无限帧轮询。

### 9. 断网、失败、进度与生命周期的共同规则

`DownloadableContentRequestCoordinator` 统一组合策略。带 CheckNetwork 的离线请求先看 Runtime Ready；未开 ImmediateNoNetworkNotice 时可进一步本地校验。下载失败后若检测为断网，转无网提示；仍有网络则按 AlertOnFailure 显示失败重试。后台 None 直接返回结果，不套前台提示。

提示框的完整外壳是 `Assets/Betta.AOT/UI/Resources/UI/Notice/Prefab/UINotice.prefab`，控制器 `Assets/Betta.AOT/UI/UINotice.cs`。DLC 的 PromptNotice 与 ProgressNotice 都是继承该控制器的类型，定义在 `Assets/Module/DownloadableContent/DownloadableContentNoticePresenter.cs`；不能把内容 prefab 当完整弹窗。

| 用途 | 内容与文本 | 关闭规则 |
|---|---|---|
| 无网络 | 内容 prefab `Assets/Betta.AOT/UI/Resources/UI/Notice/Prefab/Content/UINoticeNetworkFailedContent.prefab`；正文 `str_id_NoNetwork` | 启动请求 CloseEnable=false；普通前台 true；重试按钮 `str_id_Retry`，CancelEnable=false |
| 下载失败 | 内容 prefab `Assets/Betta.AOT/UI/Resources/UI/Notice/Prefab/Content/UINoticResDownloadFailedContent.prefab`（实际拼写 UINotic）；正文 `str_id_ResourceLoading_Failed` | 同上；点击重试回到请求循环，关闭则不继续本次重试 |
| 默认下载进度 | 默认文字内容 prefab `Assets/Betta.AOT/UI/Resources/UI/Notice/Prefab/Content/UINoticeTextContent.prefab`；`str_id_ResourceLoading` 加百分比 | CloseEnable=true、OkEnable=false、CancelEnable=false；关闭仅停止进度展示 |

标题统一 `str_id_ResourceDownload`。系统还支持下载大小确认（`str_id_ResourceLoading` 加 MB、按钮 `str_id_Continue`），但当前上述 Home/活动调用没有启用 ConfirmDownload。文本经 `LocaleManager.GetText` 读取；当前运行时 `Assets/Betta/Res/Locale/en.bytes` 已解码核对，`en.json~` 是可读备份。英文分别为 Resource Download、Unable to load resources. No network connection!、Loading resources...、Resource download failed. 后接网络检查提示、Retry。Loading 原文没有 `{0}`，Presenter 走空格追加值的分支；具体换行表现未运行确认。

`UINotice.ApplyCloseMode` 同时控制 `Root/Background/btn_Close` 和 `Root/btn_FullPageClose`；`ApplyButtonMode` 独立控制取消/确认按钮。普通前台“可关闭”与启动“不可关闭”来自请求标记，并非内容 prefab 自带按钮。历史“回退关闭按钮修改”的对话不作当前文件状态证据；这里只描述本轮读到的代码，不声称执行过回退。

共享无网提示复用同一等待任务并抢先关闭已有失败提示；单个调用取消不等于共享弹窗立即销毁，`ShowNoNetworkRetryAsync` 使用独立共享等待。进度对象 Dispose 会关闭自己的窗口；失败提示等待取消、全局 UI 清理与底层共享下载取消不是同一件事。多调用方交叠时的关闭性、销毁后窗口残留、重复回调仍需运行验证，不能概括为所有取消都完全停止网络和 UI。

## 情境推演

这些是依据静态代码推演的预期，不是已跑过的用例。

- **资源已 Ready**：普通点击通过所需地图门禁；画廊已完成章节可立即预览；活动只有 Open 且原业务条件满足才恢复展示，不因 Ready 提前开启。
- **缺下一章地图**：已完成 99，点击进 100 时会检查 100 与 101，命中 Candy 缺包就下载并停留。本次成功后仍需再点；UI 封面是否 Ready 不改变地图门禁。启动完成进度 90 时窗口到 101，也会把 Candy 列为必要资源。
- **离线**：已校验资源仍可用；启动可以先恢复本地缓存 Ready，确实缺包时停在不可关闭重试提示。普通进关缺包时可关闭前台提示，Gallery 则先静默尝试，失败再提示；普通活动后台失败不因 DLC 强制拦住基础流程。
- **新 max 从 400 提高且 Garden 已 Ready**：普通 400 或 Endless 胜利继续请求，候选与下一关 401 配置验证成功后，在退出局内往 Home 的转换阶段应用，Endless 来源通过桥接尝试章节解锁，无需重启。
- **新 max 已到，但 Garden 后来才下完**：这次 pending 因地图未 Ready 被清除，仍使用旧边界。Home 后台把 Garden 下载完仅恢复资源可用性；下一次合适胜利返回再次请求才有机会应用，不会刚下载完就自动退出 Endless。
- **活动下载中结束**：Finish/Close 使旧代次失效，正在执行的包可能仍完成，但不能恢复已结束活动正式展示，也不继续旧任务的后续包。

## 已确认目标、实现差距与待确认项

| 目标 / 资料口径 | 当前静态事实 | 后续处理 |
|---|---|---|
| 用户历史目标：Endless 每关结束检查新 max | 当前仅胜利继续；普通有效最大关卡胜利也检查 | 明确是否将失败、放弃等所有最终 lv_end 纳入；不要把临时死亡/复活提示当最终结束 |
| 用户历史目标：缺资源弹窗，成功直接解锁 | 当前只挡应用并清 pending，无主动下载/完成后重应用 | 需规划安全返回节点、缺包 Ensure、失败返回与重新校验链路；尚未实现 |
| 新 max 不重启生效 | 已有两阶段实现及 Ready/配置门禁 | 保留该方向，不再以“必须重启”为现行要求；运行证据待补 |
| 活动扩展设计的预告、独立请求节点、版本包切换、功能提权及统一弹窗额度 | 当前映射/协调链未提供这些完整设计能力 | 设计稿继续有效作讨论来源；逐项确认需要后推进，不能整体称已实现 |
| 活动启动必要资源 | 能力接入、仅 Open 合格，但当前配置均未启用 | 产品是否需要启用及具体对象待确认；不自动恢复旧签到测试配置 |
| 当前 DLC 已可发布 | 只有代码/作者配置证据，最新 Ocean Manifest、Player、CDN 未核验 | 发布结论必须有对应版本产物与设备证据 |

## 实现顺序建议

以下只规划，不执行业务变更。

1. **Step1：固定需求边界。** 明确“每关结束”包含的最终结束类型、是否等待服务器返回、离线/取消是否允许继续 Endless。沿用当前胜利链作事实基线，避免把扩大触发范围误写成现状。
2. **Step2：设计一次安全的返回 Home 准备过程。** 保持结算先完成、局内资源退出后才应用边界；把候选 max、目标下一关、生命周期版本和失败策略串起来。缺地图时通过已有服务 Ensure；成功后重新验证目标和配置，不能直接复用下载前快照。处理重复点击、请求超时与过期回调。
3. **Step3：补齐成功与失败收口。** 资源齐全后原子应用 max、刷新缓存/保存，Endless 来源只登记一次桥接；取消/失败保留旧边界并给下一次明确重试入口。决定是否保留 pending 等待资源、或本次返回过程统一重试，避免与后台完成事件重复解锁。
4. **Step4：按需推进活动能力。** 先选择真实需启动阻塞的活动，再核对 EnforceDlc、RequireOnStartup、Package 内容和开放条件；预告、版本包、弹窗额度等分别立验收边界，不一次扩大到整个旧设计。
5. **Step5：发布与运行验证。** 更新受影响逻辑后针对性运行测试，再核验最新资源 Manifest/Bundle 闭包、Player 资源组成、发布目标与设备全新安装/缓存恢复。每层各记证据，最后回写本文进展、差距与 Daily。

## 阶段进展与待办验收

- [x] 首轮路由、同题去重、原始 LG 对照；当前工作目录与嵌套库版本核对。
- [x] 玩家旅程静态梳理：分包、启动、Home、进关、Gallery、解锁、max、活动、提示和生命周期。
- [x] 直接核对二进制配置，纠正活动路径/开关/开启关卡、封面路径与占位图。
- [x] 2026-09-08 建立唯一主档，补 MOC/速查/Docs 索引及历史范围提示；分别记录 9 月 7 日初稿与 9 月 8 日续做。
- [x] 2026-09-08 文档校验与原始 vault 入库完成：9 份文档经正常权限流程精确合入 `/Users/dean/LibraryG`，逐份回读一致；保留并发 SQL MOC 入口与巡检 Daily。新增/修改内容的 9 个内部链接目标、38 个明确来源路径核查通过，历史正文保留，文本差异无新增空白错误。此项仅代表文档入库，不代表业务实现或运行验证完成。
- [ ] 对以下用例补运行证据；本轮文档核查不代替通过记录。

| 验证项 | 验收关注点 |
|---|---|
| 全新安装与缓存恢复 | Forest/Ocean 分界、启动提前 10 关的 +1 边界、离线完整缓存能恢复 Ready；缺包不能进入业务 |
| Home 后台 | 50 关窗口与所有 UI 包、Ready/队列去重、失败后下次 Home 重试；无尽局数不扩大普通窗口 |
| 进关和 Gallery | 一次一个缺包、成功需再点；Gallery 零实际字节与有下载字节的区别；关闭进度不取消下载 |
| 解锁和 max | 普通边界胜利、Endless 胜利、失败退出分别检查；候选非法/配置缺失/地图未 Ready 时旧边界保留；应用与桥接只一次 |
| 后来才 Ready | 当前应不自动重应用 pending；若以后改为自动恢复，应更新事实描述与去重/生命周期用例 |
| 活动 | 首充/破冰 28 关与开前 10 关；签到/金卡基础包回退；临时启用 RequireOnStartup 时仅 Open 未过期入 Gate，Preview 不入 |
| 提示交叠与销毁 | 启动不可关闭、前台可关闭，共享无网与失败提示抢占、取消等待/关闭 UI/停止物理下载各自结果 |
| 最新发布闭包 | 每 Home Package 的实际 Bundle 与共享依赖、Ocean 最新清单、安装包组成、CDN 匹配；设备正常下载/断网/重试/缓存 |

## 下次继续入口

当前 Home 调度先读 [[02-PROJECTS/TileScape/游戏逻辑/任务-DLC全链路梳理与维护#2026-09-08 Home 下载优化|2026-09-08 Home 下载优化]]；不要按下方基线路径寻找已删除的协调器或 Flow。

先读本文“已确认目标、实现差距”与“阶段进展”，再核对 TS 当前分支/嵌套库/相关 diff；只重读改变的代码。默认下一步是收敛新 max 缺资源补齐流程的需求与方案，用户授权实现后才改业务。运行验收按实际交付需要推进，不要求用户逐项反馈所有清单。

09-07 基线源码入口（Home 协调器、两个 Flow 与旧测试已删除/重命名；当前路径见上方优化小节）：

- Home 调度：`Assets/Module/HomeHub/HomeScene/Scripts/DLC/HomeHubDlcCoordinator.cs`、同目录 `HomeHubDlcModule.cs`、两个 `FlowItemHomeDlc*.cs`。
- 启动/提示：`Assets/Scripts/GameMain.cs`、`Assets/Module/ApplicationLoading/ApplicationLoadingRequireDownloadableGate.cs`、`Assets/Module/DownloadableContent/DownloadableContentRequestCoordinator.cs`、同目录 `DownloadableContentNoticePresenter.cs`。
- 新 max：`Assets/Game/TileV2/Scripts/UI/UIWinPanel/UIWinPanel.cs`、`Assets/Game/TileV2/Scripts/Entry/TileMatch.cs`、同目录 `TileMatchSceneState.cs`、`Assets/Game/TileV2/Scripts/DataCenter/TileMatchDataCenter.Level.cs`。
- 解锁：`Assets/Module/HomeHub/HomeScene/Scripts/Flow/Item/FlowItemHomeEndlessExitChapterUnlock.cs`、同目录 `FlowItemHomeChapterUnlock.cs`、`Assets/Module/HomeHub/HomeScene/UI/UIChapterUnlock/Scripts/ChapterUnlockDlcAssetAccess.cs`。
- 活动：`Assets/Module/Activity/Core/DLC/ActivityModule.Dlc.cs`、同目录 `ActivityDlcCoordinator.cs`、`ActivityDlcStartupEligibility.cs`、`ActivityDlcNeedSet.cs`，以及 `Assets/Module/Activity/Core/Config/CatalogLoader.cs`、`Assets/Module/Activity/Core/Entity/ActivityBase.cs`。
- 现有测试入口（本轮未运行）：`Assets/Module/HomeHub/HomeScene/Tests/Editor/HomeHubDlcCoordinatorTests.cs`、`Assets/Module/DownloadableContent/Tests/EditMode/DownloadableContentRequestCoordinatorTests.cs`、`Assets/Module/Activity/Tests/EditMode/ActivityDlcStartupEligibilityTests.cs`。

## 关联

- [[02-PROJECTS/TileScape/_MOC|TileScape MOC]]
- [[02-PROJECTS/TileScape/参考/快速定位与资源替换索引|快速定位与资源替换索引]]
- [[02-PROJECTS/TileScape/参考/Docs文档索引|Docs 文档索引]]
- [[02-PROJECTS/TileScape/游戏逻辑/梳理-HomeDLC与Endless最大关卡更新流程-2026-08-20|Home/Endless 历史流程]]
- [[02-PROJECTS/TileScape/游戏逻辑/设计-活动DLC扩展框架-2026-08-25|活动扩展设计稿（保留设计状态）]]
- [[02-PROJECTS/TileScape/游戏逻辑/梳理-ActivityDLC现状与设计差异-2026-08-26|FirstPay 历史静态审计]]
- [[01-DAILY/2026-09-07|首轮整理日志]]
- [[01-DAILY/2026-09-08|续做与入库日志]]
