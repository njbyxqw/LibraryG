---
title: DDAV3逻辑策略持续研究
date: 2026-09-11
type: analysis
status: complete
project: TileScape
verification: static-analysis; runtime-pending
tags: [TileScape, DDA, 持续研究]
---

# DDAV3 逻辑策略持续研究

## 总目标与授权范围

建立对 V3 当前行为可信、可解释的认识，判断它适合承担哪些调控目标，并形成有依据、可验证的迭代路线。

用户于 2026-09-11 接受六个研究目标，并要求参考已设置自动化持续推进和记录。当前范围是源码只读、分析、反例、研究文档及记录维护；不包含修改业务代码、资源、配置、提交或推送。必要验证可以先形成最小样本与对照设计，不将测试设计视为实际运行结果。

## 自动化接续

- 已有自动化：`06-00`，名称“五小时窗口提醒与 DDAV3 持续任务”，ACTIVE。
- 目标任务 ID：`01a080ef-a5b2-73b2-b0fc-40e550fe35f3`，与本次研究对话不是同一个任务。
- 原提示要求每次检查最新进度与目标，未达成继续，达成停止研究推进；缺必要信息或决策时明确等待。
- 本主档作为研究进度的唯一入口。原评估是版本基线，不直接代替当前进度。
- 不改已有提醒时间、提醒原文或目标任务；完成研究也不自行删除窗口提醒。

## 六个目标与完成标准

| 编号 | 目标 | 完成标准 | 当前状态 |
|---|---|---|---|
| G1 | 当前实现基线 | 入口、配置、揭牌、指标、候选、执行、统计和记录链路有源码依据，核对版本差异 | 静态产出完成：V3@cd3 基线链路与当前 `feat-winStreak` 的分支差异已记录；当前 checkout 不含 Slack V3 |
| G2 | 指标解释能力 | 梳理典型局面和反例，明确 FastNCD/HardSlack 适用范围与遗漏 | 静态产出完成：M01–M10 场景矩阵、指标边界和实际 DDA 触发拓扑已记录；棋盘样本未运行 |
| G3 | 调控正确性 | 对不换牌、误差改善、限幅、死区、多目标及无安全解给出可复核结论 | 静态产出完成：D01–D09 决策矩阵与确定行为已记录；真实牌面执行未验证 |
| G4 | 体验与业务策略 | 明确曲线意图、选择感、连消、失败/复活/道具收益的假设与对照方法 | 静态产出完成：六类体验对照假设已形成；玩家/运行数据未采集 |
| G5 | 迭代验证基础 | 配置、算法版本、回放、日志、测试和性能缺口及最小补齐项齐全 | 静态产出完成：配置/回放/随机流/统计/性能风险、日志和夹具方案及补齐建议齐全；独立 Slack 算法指纹/参数快照、回放、Unity 性能与 Layer A/B 执行仍待验证 |
| G6 | 分阶段路线 | 以依赖、收益、风险排序，写清每阶段范围、验证与退出条件 | 静态产出完成：三条路线、依赖与退出标准已记录；未实施 |

研究文档完成与算法运行有效性分别登记。只有六项目标对应产出齐全、关键未决项已说明依据/影响/处理方式，才能结束本研究；不能因已有摘要或达到某个运行窗口而标完成。若关键结论依赖运行数据而暂不可得，保留证据不足状态，不虚构结果。

## 当前版本与事实

- 原始基线：`DDA-V3-Test @ 9be729cb3223169ce85b4b0bf67b52314926a2f5`。
- 最近审计的 V3 版本：`DDA-V3-Test @ cd3aea16656814e0e226205c3c225c36a94deded`。
- 增量：`13c656c63` 修改 Slack 控制器和 DDA 合约测试；`cd3aea166` 为合并提交。
- 该区间只改变两个文件，未改变曲线数组、候选主排序、不换牌基准、步长执行方式或记录结构。
- 业务代码更新来自分支已有提交，不是本研究实施的修复。
- 当前 checkout（2026-09-14 16:04 UTC+8）：`feat-winStreak @ 3d1d339c7ac4010002ea02af190ed4f46c9c52a4`。它与 `DDA-V3-Test` 从共同基点分叉；`DDA-V3-Test` 仍是本地/远端引用，但 Slack V3 实现并未合入当前分支。R01–R08 是针对 V3 分支 `cd3aea166` 的历史代码事实，不得表述为当前 checkout 行为。

## 批次 R01：基线增量与深度成本评估

### 已确认变化

`InLevelDDAV2SlackController` 增加 `_depthThreeVisibleTypeCount`，在压力快照中记录深度 3 的可见不可点牌；虚拟目标也传入其真实深度。路线成本先使用高亮牌，再用低成本可见牌，再用深度 3 可见牌。

```text
成本 = 高亮可点使用数×1 + 低成本可见使用数×2 + 深度3可见使用数×3
GetVisibleRouteCost(depth) = max(2, depth)
```

当前统计深度仅接纳 1–3，因此实际可见成本为 2 或 3。高亮可点仍走成本 1。

证据：`Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Module/InLevelDDA/V2/InLevelDDAV2SlackController.cs` 的 PreparePressureSnapshot、ComputeMetrics、TryComputeRouteCost、GetVisibleRouteCost；对照 `9be729cb3..cd3aea166`。

新增 `VisibleRouteCost_UsesRealDepthAboveBaseUnlockCost`，覆盖深度 1/2/3 返回 2/2/3。它验证辅助函数映射，没有完整验证快照分类、路线组合选择和整局可解性。本轮没有执行该测试。

### 静态推演与限制

1. 若某最优路线只缺一张深度3可见牌，其他条件不变且没有替代路线，成本从2升为3，HardSlack在未触及截断时下降1。这能收紧此前偏乐观的估算。
2. 若两张所需可见牌共享覆盖牌，按每张分别计深度可能重复计入解锁成本。举例：两张 A 均被同一组两张覆盖牌遮住，模型可能计6；如果实际动作可以先移除两张覆盖牌再取得两张 A，则为4次取牌动作。该例需要构造真实合法棋盘确认，不能当作已复现缺陷。
3. 深度只提供覆盖数量信息，不能替代效果生命、锁定解除规则、消除释放容量和序列弹出状态模拟。新注释中的“真实成本”应理解为当前深度近似，不是路径证明。
4. 不换牌基准缺失与步长仅记录的问题在新版本仍存在。不能把“BUG修复”提交标题理解为原报告全部问题已修复。

### 本批结果

G1 基线已增量核对；G2 增加了新成本公式、修正收益和反例边界。未写业务代码，未运行 Unity、回放或 Profiler。

## 批次 R02：决策边界与候选排序（静态首轮）

### 版本与来源

- 核对时间：2026-09-12。
- TileScape 分支：`DDA-V3-Test`；HEAD：`cd3aea16656814e0e226205c3c225c36a94deded`，与 R01 核对版本一致。
- 对照范围：主档 HEAD 到当前 HEAD 的 DDA/Slack 路径无新增文件差异。
- 主要来源：`Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Module/InLevelDDA/V2/InLevelDDAV2SlackController.cs`（SelectExchangeTarget、CollectLegalCandidates、IsLegalCandidate、ApplyOutcomeControl、MovesPressureTowardTarget、IsBetterCandidate、ApplySelectedEvaluation）；参数同文件 `InLevelDDAV2SlackTuning`。
- 合约测试定位：`Assets/Game/TileV2/Tests/EditMode/DataCenter/MeatloafDeltaDdaContractTests.cs` 目前可见深度成本辅助函数契约；没有找到覆盖下列完整决策排序与边界组合的专门用例。本轮未执行测试。

### 决策矩阵（代码语义已确认；棋盘组合尚未运行）

| 情形 | 当前代码行为 | 证据状态与含义 |
|---|---|---|
| 当前误差落在 `DEAD_BAND=0.2` 内 | 若当前 HardSlack 未低于 `MinimumAllowedHardSlack`，立即以 `WithinDeadBand` 返回，不枚举候选；低于安全下界时绕过死区，继续尝试救场 | 已确认静态行为。死区不是绝对不换牌条件，安全救场优先 |
| 无合法隐藏候选 | 以 `NoLegalHiddenTile` 返回 | 已确认静态行为。合法性还要求未见、未锁定、仍在棋盘、可计入压力类型且序列约束允许 |
| 候选低于计划输/生存下界 | 该候选从排序中跳过；全部被跳过时返回 `OutcomeBoundaryRejectedAllCandidates` | 已确认静态行为。安全边界可能使系统宁可不换，也不选越界候选 |
| 多个候选比较 | 第一排序键是 `abs(candidate.HardSlack - target)`；接近并列时依次比较直接成组组数偏好、该花色可选隐藏牌数量、高亮花色数量；完全并列使用随机蓄水池选择 | 已确认静态行为。排序不是按候选能否改善当前误差方向优先；其余体验指标仅在目标距离并列时介入 |
| 达到步长上限 | `MAX_SLACK_DELTA=10`、紧急值 `5` 仅参与选中后的 `UsedFallback` 标记；当前代码没有以此过滤、截断或重新选择候选 | 已确认静态行为。“最大步长”在此版本不是硬限制；超限候选仍可被执行。需在 R02 后续确认其产品意图及真实指标可达性 |
| 所有候选都无法改善误差方向 | 仍会在安全下界内选取目标距离最小的候选；若其方向不符或变化超过上限，标记 `UsedFallback` | 已确认静态行为。Fallback 表示结果分类，不是另一次安全搜索或硬限幅 |

### 静态反例推演（不是已复现棋盘）

1. 假设当前 HardSlack=2、目标=1，合法候选的预测值分别为 0 和 2，两者距目标均为 1。代码会交给后续次级排序决定；没有显式优先选择朝目标移动的候选，因此次级成组/隐藏数量/高亮排序可能选择 HardSlack 仍为 2 的候选，最终 `UsedFallback=true`。这说明“距离目标优先”不等于“方向优先”；具体候选是否能由真实棋盘构造仍待验证。
2. 假设普通模式当前值高于目标，所有候选要么方向不对、要么跨过目标，但其中某候选仍是目标距离最近且满足最低安全值。代码会选择它；`MAX_SLACK_DELTA` 超限也只打标，不会拦截。以上是由排序/执行代码推导的决策语义，不代表已观察到玩家对局样本。
3. `ForcePlannedLose=false` 时 `ApplyOutcomeControl` 将最低 HardSlack 设为 0；因此困难曲线可以要求 0，但默认不会接受负值候选。若开启计划输，目标向 `-1` 渐变，最低允许值同步从 0 渐变至 -1。此策略配置当前写死在源码；本轮未切换开关或运行验证。

### 本批结果与边界

- G3 获得一组可从源码直接复核的候选排序、死区、安全筛选和步长语义；R02 尚未完成真实牌面矩阵，G2 共享覆盖、深度2/3、锁定效果及序列弹出场景仍为待构造项。
- 未修改 TileScape 源码、资源或配置；未编译、未运行 Unity/回放/玩家样本。
- 来源均为上述 HEAD 下的静态代码；反例数值为抽象候选指标示例，标记为推演而非测试结果。

### R02 增量：压力资源与换牌候选的资格边界

- `PreparePressureSnapshot` 对可见牌使用 `IsTileStateAndDepthEligibleForSlack`：深度须为 1–3，仍在棋盘且不处于销毁/入槽/匹配状态；锁定牌只有带 `LockSource.Destroy` 时排除。因此可见 `LockSource.Common` 锁牌在符合其他条件时仍可能进入路线压力计数。
- `CollectLegalCandidates` 则只扫 `NotVisible` 暗牌；`IsLegalCandidate` 对任何 `LockState.Locked` 都直接拒绝，并额外要求 `HasSeen=false`、仍在棋盘、可加入 DDA、并且跨序列交换后保持约束。
- `SequenceConstraintHelper` 当前只对 Flip 容器约束序列内 TileType 尽量不同；同一序列内部交换允许，跨序列时检查移入类型是否与目标序列的其他类型冲突。
- 因而“进入 HardSlack 压力快照的资源”和“本次可以被 DDA 换入的候选”不是同一集合。这是实现语义的确定差异；Common 锁牌何时解除、计入路线是否构成可用性高估，要结合具体锁行为/牌面确认，暂不定性为缺陷。
- `LockSource.Common` 本身没有单一生命周期：ECA `LockSelf/LockTiles` 与对应 `UnlockSelf/UnlockTiles` 可按行为配置成锁/解锁；`HandleForwardTileClickAction` 会在转发事务期间加锁、在 `CompleteTransaction` 回调中解锁；因此仅凭来源标记无法推导某张可见牌会在几步后恢复可点。该项应以具体行为链和触发时序为准。
- 这使得“计入压力但不作为本次换牌候选”不能直接推出指标错误：如果锁只保护尚未完成的短事务，路线估算可能合理；如果存在长期锁且没有可达解锁事件，则模型可能提前把锁牌当资源。两类样本必须分开验证。
- 候选评价按 `TileType` 去重：每种类型只计算一次 `ComputeMetrics(target, candidateType, ...)`，不把候选实体的位置、深度或具体序列身份传入指标函数；通过资格检查的同类型实体数量只作为平手次级键，最终再从该类型的合法实体列表里用随机索引选一个。故同类型不同位置/序列成员只要都合法，预测 HardSlack 相同，但其具体交换位置会变化。该实现语义已确认，实际玩家感知影响待样本验证。
- 执行层 `InLevelDDAV2Strategy.TryExchangeTileInternal` 调用 `TileService.ExchangeTilePairsPosition`，实际交换目标牌与选中实体的位置，并同步 `HasSeen` 和序列成员关系。因此不同位置实体虽然同花色预测值相同，交换后的牌面位置/序列布局可能不同；当前 Slack 评估比较即时虚拟目标花色，不逐个模拟这些实体位置带来的后续揭牌/序列状态。可确认的是预测粒度比执行状态更粗；是否造成后续调控差异需要构造同花色、不同位置候选的对照牌面。
- Flip 序列约束例外明确：同一 Flip 容器内交换允许（只改变顺序）；跨序列交换会检查两边目标 Flip 容器内其他成员是否已有即将移入的类型；目标不是 Flip 的序列不执行不同类型限制。`CanTileJoinDDA` 另检查 Tile 与类型配置的 DDA 许可及 `HasSeen`。
- 合约测试 `MeatloafDeltaDdaContractTests.PressureEligibility_AcceptsVisibleDepthBoundaryAndCommonLock` 与 `PressureEligibility_RejectsDeepDestroyLockedAndDestroyingTiles` 直接覆盖了静态资格谓词；它们没有覆盖交换候选筛选或完整路线可达性。本轮只读取测试代码，没有运行。
- 相关契约测试 `MeatloafDeltaSequenceConstraintContractTests` 覆盖同序列 Flip 允许交换、进入 Flip 时拒绝重复 sibling 类型、非 Flip 序列不限制重复类型；但未覆盖控制器综合选型。本轮只读取测试源码，没有运行。
- 来源：同一 HEAD 的 `InLevelDDAV2SlackController.cs`（PreparePressureSnapshot、CollectLegalCandidates、IsLegalCandidate、IsTileStateAndDepthEligibleForSlack、SelectExchangeTarget、SelectRandomCandidateTile）、`InLevelDDAV2Strategy.TryExchangeTileInternal`、`TileService.ExchangeTilePairsPosition`、`SequenceConstraintHelper.cs`（PreservesDistinctTypesOnSwap、CanTileJoinDDA、CanEnterSequence）、`LockActions.cs`、`HandleForwardTileClickAction.cs`；测试源 `MeatloafDeltaDdaContractTests.cs`、`MeatloafDeltaSequenceConstraintContractTests.cs`。

### R02 增量：HardSlack 下限造成的指标合并

- `freeSlot = F` 时，`maxFastNcd = F - HARD_SLACK_FLOOR = F + 2`。若完全无可行路线，代码直接以 `F+2` 作为 FastNCD；若存在路线但其 `rawBestNcd >= F+2`，也会被 `Math.Min` 截到 `F+2`。两种状态最终都会得到 `HardSlack=-2`。
- 例如 `F=3`，路线成本 5、6 或不存在路线，都会报告 `FastNCD=5, HardSlack=-2`；成本为 4 时则报告 `HardSlack=-1`。这不是新发现的实现变更，而是对既有截断公式的解释：`-2` 是“超出分辨范围/无估算路”的共同桶，不区分死局与仅需更高成本的路线，也不是死局证明。
- `SelectExchangeTarget` 的默认最低允许值为 0，故低于 0 的候选被淘汰；当前值若低于最低允许值则走 safety rescue。该筛选不恢复 `-2` 桶内被截掉的细节。
- 来源：`InLevelDDAV2SlackController.ComputeMetrics` 中 `maxFastNcd`、`rawBestNcd`、`fastNcd`、`hardSlack` 公式，以及 `SelectExchangeTarget` 的最低安全边界筛选。数值例是公式代入，不是实际棋盘测试；未运行测试。

## 下一批断点与执行顺序

### R02：G2/G3 决策反例矩阵（继续）

1. 先检查分支与 HEAD，只核对上次基线后的 DDA 相关变化。
2. 建立局面矩阵：即时一张成组、可见深度2/3、共享覆盖、普通锁/效果锁、弃牌可用、序列弹出前后。
3. 为每项记录模型输入、估算值、实际规则可能差异、源码与证据状态；优先构造可运行的小样本，但不得把复刻公式的脚本称为 Unity 测试。
4. 已确认：HardSlack=-2 会合并无可行路线与成本达到截断上限的路线；死区、安全下界、候选距离优先、步长仅打 `UsedFallback` 标记、压力统计牌与换牌候选资格集合不同；候选先按类型评价、执行再随机选择同类型实体；Flip 跨序列候选受 sibling 类型约束。位置不参与同花色即时评分，但执行会实际交换位置及序列成员，所以后续揭牌路径仍需作不同位置对照。下一步构造这组合法牌面，并补不换牌、等距、过冲、限幅和无安全解的输入—预测—结果表，分开记录代码确定行为与产品选择。

### R03：G5 回放与统计

追踪初始配置恢复、LevelDiff、算法分流、随机消费和操作重放；明确旧 V2 记录在 Slack 开关下的路径。区分逐目标、逐批与实际交换统计。

#### R03 首轮：DDA 配置快照与 Slack 运行开关

- 核对版本：`DDA-V3-Test @ cd3aea16656814e0e226205c3c225c36a94deded`；对照主档版本无新增源码提交。
- 录制入口 `TileMatchGame.RecordController` 取当前 DDA 类型及 V1/V2 配置，`BuildDDAV2RecordConfig` 记录旧 V2 阶段阈值、策略类型、概率、道具限制等字段；二进制由 `TileMatchGameRecorder.SetDDAConfigInfo` 写入 DDA marker/type 与对应配置负载。
- 重连/回放入口 `TileMatchGameLogic.InitInLevelDDA` 根据记录恢复 DDAType；若 V2 记录字段满足条件则 `RestoreFromRecord` 建立 V2 config，并将 `restoredFromRecord` 传给 `InLevelDDAV2ConfigSelector`，避免再依赖当前 Jungle 活动状态重算相关 prop-limit 覆盖。
- DDA 行为版本未随 DDA 配置负载单独记录。回放准入 `ShouldReplay` 检查关卡 ID（Game 模式）、关卡名和 Level MD5，不比较录制与当前 App/Build 版本；播放器的 move 只有 `Click`、`UseProp`、`StateChange`，按时间重发点击/道具输入，并非直接重放 DDA 选中的交换实体。因此历史输入在新代码下会重新运行当下 Slack 决策，跨代码版本不能据此当作历史 DDA 结果逐步精确复现。
- 与之不同，`ShouldReconnect` 明确要求 RecordVersion、CurrentGameVersion、CurrentGameBuildVersion 与当前一致。此门禁降低不同构建间恢复状态的风险，但 DDA 参数仍未形成独立快照/算法指纹，诊断旧记录时须依赖构建版本与对应源码。
- 不把缺少 Slack 快照扩大解释为完全无法重放：同构建记录、随机种子和同一逻辑代码是否可重复，仍取决于下游随机流与运行时顺序；这部分待追。
- `TileMatchGameLogic` 创建一个 `RandomService` 作为逻辑唯一随机流，建局时用记录中的 `LogicRandomSeed`（无记录则按 Trial/Bot 自定义种子，否则随机生成）；DDA Slack 候选平手蓄水池和同花色实体随机选择都调用同一 `GameContext.RandomService`。但构造、实体/牌型初始化、DDA 初始化完成后，构造函数末尾显式 `ResetRandomService()`，因此正常建局和 Replay/Reconnect 都从同一记录种子重新开始消费，不能仅凭牌型初始化消费推断 DDA 首次随机位点已漂移。
- Replay/Reconnect 的牌型初始化走 `ReconnectStrategy`，直接使用记录里的 `TileRandomResult`；普通新局按 DDA 类型走 `AssignTileType` 或 `AssignTileTypeByDepth`。这两条初始化路径不同，但都发生在末尾随机流重置之前；`TileRandomResult` 主要保证重连/回放的初始牌型，不能替代 DDA 运行时决定的交换实体记录。若 Slack 代码、调用顺序或额外随机消费者改变，即使种子相同，输入重放仍可能产生不同候选/实体结果；此处仍是静态条件分析，未做跨版本或运行时回放对照。
- 来源：`TileMatchGame.RecordController.cs`（配置快照）、`TileMatchGameRecorder.cs` / `TileMatchRecordController.Recorder.cs`（持久化入口）、`TileMatchGameRecordBinaryPersister.cs` / `TileMatchGameRecordBinaryLoader.cs`（二进制读写）、`TileMatchGameLogic.cs`（回放配置恢复）、`TileMatchRecordController.Replay.cs`（回放准入）、`TileMatchRecordController.Reconnector.cs`（重连版本准入）、`TileMatchGameRecordPlayer.cs`（输入重放）、`InLevelDDAV2Strategy.cs` 与 `InLevelDDAV2SlackController.cs`（静态 Slack 开关与运行决策）。本轮只做源码静态核对，未实际启动重连或回放。

#### R03 第二轮：随机流、初始牌面与统计口径（2026-09-13）

核对 HEAD 仍为 `cd3aea16656814e0e226205c3c225c36a94deded`，无新增提交；本轮使用 code-reviewer、obsidian-markdown 的既定流程，只读源码与更新研究记录。

**随机与初始恢复：**

- `TileMatchGameLogic.GetRandomSeed` 优先使用记录 LogicRandomSeed，其次使用 Trial/Bot 非零自定义种子，否则由 RandomService 随机生成。录制同时保存 logic/view 两种种子，逻辑和表现并非共用一个种子字段。
- `RandomService` 内部持有 `CustomRandom`。Reset 会用原始种子重建随机器；InitConfig 末尾、InitEntities 末尾以及构造流程 InitInLevelDDA/InitFatalDeathDetect 后都有 Reset。故“恢复初始牌型跳过发牌洗牌，必然导致局内随机偏移”的推断不成立：初始化阶段存在明确重置边界。
- `InitLevelConfigTileType` 在记录状态非 None 时走 ReconnectStrategy，按 TileRandomResult 恢复基础牌和序列成员花色；记录在建局后由 `_gameLogic.GetTileTypes()` 保存该列表。这是初始牌型列表，不是每次 DDA 交换对象的历史列表，也不是完整局中随机状态快照。
- Slack 的同分蓄水池选择、选中花色内部随机索引均使用 `_context.RandomService`。ShuffleProp/AutoMatchProp 等传递相同上下文随机服务，RocketNormalStrategy 也直接调用它。局内未见 DDA 独立随机流，不能把初始化重置理解为运行中各系统分流。
- CustomRandom 为显式状态递推；整数 Range(0,1) 仍会推进一次随机状态（Next(1) 调用 Next 后对1取模）。因此只有一个同花色合法实体时，SelectRandomCandidateTile 仍消耗随机数；若某次新规则让此交换直接被跳过，后续其他随机行为也可能错位。此为代码调用语义，未做完整牌局复现。

**可复现性判断：**

| 条件 | 判断 |
|---|---|
| 同版本、同初始牌型、同逻辑种子 | 是必要基础，不足以单独证明整局一致 |
| 再满足候选迭代顺序、事件/操作顺序和随机消费次数一致 | 可形成确定性重放的条件；本轮未验证这些条件在运行时始终成立 |
| 只修改同分规则或增加一次随机调用 | 即使曲线未改，也可能影响后续 DDA、道具或 Rocket 的随机结果 |
| 仅保存 Slack 曲线快照 | 不能解决算法控制流、候选遍历顺序和共用随机流变化 |
| 开发调参比较两个版本 | 应对照初始状态与完整操作轨迹；不能把种子相同当作其余随机结果均相同 |

建议先记录算法版本、有效配置及可诊断的随机调用序号，再决定是否分流。独立 DDA 随机流会改变历史随机消费契约，不宜作为无影响的小优化直接切换。

**统计口径已追至对外字段：**

| 计数 | 增量位置与粒度 | 解释 |
|---|---|---|
| Statistic._ddaRegulationCount | V2策略对每个通过入口并完成决策的目标加1 | 包括死区/无候选等未交换决策；不等同于真实交换 |
| 策略 _regulationDarkTimes | 每选中非空交换对象加1 | 逐目标真实交换数 |
| control_times | Board/Sequence 调控批次内有至少一个触发，批次结束记1；经 GetControlTimes 导出 | 批次尝试数，不是每一张牌的尝试数 |
| control_change_times | 同批至少一次真实交换，批次结束记1；经 GetControlChangeTimes 导出 | 发生过交换的批次数，不是换牌张数 |
| control_times_progress_* | Record 调控批次时，依据总牌与 Board+Bar+OverBar 剩余牌分桶 | 与 Slack 曲线仅用 Board 余量的进度不同 |

例如同批有3个合格目标、2次交换，则逐目标评估+3，逐目标交换+2，control_times+1，control_change_times+1。此为调用链代入，不是已执行测试。

进度差异示例：初始和统计总牌均为100，当前Board=74、Bar=5、OverBar=0，则 Slack进度为26%，调控统计进度为21%，落入首个0–25%区间。故不能直接把 control_times_progress_25 等字段对应到 Slack 的曲线分段；两个分母还可能因实体展开口径不同而进一步不同，应以实际初始化数据确认。

**主要源码证据：**

- `Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/TileMatchGameLogic.cs`：构造顺序、ResetRandomService、GetRandomSeed、RandomService 注册。
- 同目录 `TileMatchGameLogic.Config.cs`：InitConfig、InitLevelConfigTileType、GetTileTypes；`TileMatchGameLogic.EntityInitializer.cs`：InitEntities。
- 同目录 `Services/RandomService.cs`；`Assets/Game/TileShared/Scripts/Util/CustomRandom.cs`：Reset 与随机状态推进。
- 同目录 `Module/LevelTileType/Strategy/ReconnectStrategy.cs`；`Assets/Game/TileV2/Scripts/GameCore/Game/TileMatchGame.RecordController.cs`：初始花色恢复/记录。
- 同目录 `Module/InLevelDDA/V2/InLevelDDAV2SlackController.cs`、`InLevelDDAV2Strategy.cs`，以及 `Prop/ShuffleProp.cs`、`Prop/AutoMatchProp.cs`、`Module/LevelRocket/Strategy/RocketNormalStrategy.cs`：随机服务消费。
- 同目录 `Module/InLevelDDA/InLevelRegulationTimesRecorder.cs`、`Module/Statistic/Statistic.cs`、`Entity/Board.cs`、`Services/SequenceRegulationService.cs`、`TileMatchGameLogic.Logger.cs`；`Assets/Game/TileV2/Scripts/GameCore/Game/TileMatchGame.Logger.cs`：计数和导出。

**本轮收敛：**R03 的配置、准入、种子、初始结果恢复、随机消费和计数链已形成静态解释。尚不宣称同版本实际重放通过；运行顺序/确定性与性能证据仍缺。下一轮优先回到 R02 构建可复核场景矩阵，再推进 G4/G6，避免反复扩大静态检索而不收敛结论。

#### R03 下一断点

继续检查 replay 操作时间、棋盘随机结果与 DDA 重算的先后顺序，确认同构建可重复条件；补统计口径（尝试、真实交换、逐目标/逐步），并设计一组固定种子下的回放一致性对照。当前已确认：逻辑随机服务与 DDA 共流，但建局末尾重置使牌型初始化消费不直接改变 DDA 起始随机位点。

### R04：G4/G6 策略收敛

形成曲线与道具保护的对照矩阵，提出少量互斥策略选项及取舍；完成路线的退出标准。只有必须依赖用户产品选择时提问，同时继续不依赖该选择的分析。

## 批次 R04：场景矩阵与迭代选项（2026-09-13）

- 当前 HEAD 仍为 cd3aea166；形成 [[02-PROJECTS/TileScape/游戏逻辑/分析-DDAV3场景反例与迭代选项-2026-09-13|场景反例与迭代选项子文档]]，不覆盖原基线。
- G2/G3：补齐10类指标场景和9类决策边界的静态矩阵，明确输入、模型值、确定行为与真实棋盘待验证部分。
- G4/G6：形成6类体验对照、3条路线及退出标准。推荐先做保守曲线追踪；道具/复活保护和可行性保护分别作为后续选项，未授权实施。
- 研究进度：文档矩阵已完成，真实关卡样本与运行效果未完成；无业务代码修改、无Unity/测试运行。
- **下一批优先断点 R05**：从M01–M04核对真实点击、入槽、匹配的执行顺序，确认FastNCD动作成本与峰值占槽是否对应；再追M07弃牌取回资格。随后选择已有合法关卡样本，避免重复宏观静态清单。
- R03统计已有第二轮结论，后续仅补同构建运行顺序和首次分叉检查，不重复逐目标/逐批字段追踪。

## 批次 R05：入槽快照与弃牌可用性（2026-09-13）

- 用户要求继续并询问自动继续；已通过工具确认自动化06-00仍ACTIVE，提示已绑定本主档。按原窗口接续，不承诺两次窗口之间连续运行。本次没有改变计划。
- HEAD仍为cd3aea166。本轮只读源码，未执行Unity或测试。

### 已确认的动作顺序

`AddToBarAction.Execute` 先检查Bar.IsFull、点击锁定与已入槽等条件；随后处理非接管销毁的效果事件，Board.RemoveTile、OverBar.RemoveTile、Bar.AddTile，再调用Board.InvokeLevelDDA；之后锁定已入槽牌、更新Bar状态并派发AddingToBarByClick相关事件，最后检查满槽失败或成功。

Bar.AddTile内部已调用UpdateBarStatus，因此DDA不使用点击前的旧UnmatchedCount。UpdateBarStatus又通过各花色 `(数量-过滤数量)%MatchCount` 汇总未匹配计数，逻辑占槽与仍存在的牌实体数量不是同一个数。后续BarMatchAction负责解锁、寻找匹配、将匹配成员设为Matched并上Destroy锁，再发布匹配事件。

结论：评估样本应取DDA实际调用处的快照，不能直接使用动画结束后的实体列表或点击前空槽代入。未配对数按取余提前扣除完整组，表示逻辑容量语义；本轮不将这种分阶段处理定性为错误。效果事件的实际派发/排队时机仍需结合EventDispatchService进一步确认。

### 弃牌场景M07的边界收敛

Tile.Clickable允许InBoard或InOverBar状态，但还要求未锁定、类型可交互、效果不阻断点击以及达到Highlight可见性。AddToBarAction同时尝试从Board和OverBar移除，再加入Bar。因此满足条件的弃牌存在正常取回路径，不应把OverBar统一当作不可达资源。

Slack快照明确不把OverBar加入FastNCD，而成组计数包含OverBar全部符合其计数条件的牌。M07的差异因此有实际规则依据：若手里A×2，弃牌中唯一A确实可点且Bar未满，模型仍可能无A路线；反之，弃牌A若未高亮、被锁或效果阻断，也不能只凭成组数量称其可用。

这支持后续将弃牌细分为“当前可点”和“不可直接取回”再评估，尚不代表直接将全部弃牌加入成本公式即可正确。应核对OverBar格子/可见性以及点击事件配置；未构造真实关卡复现。

### 来源与下一断点

- `Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Behaviours/Action/Implementation/BarActions.cs`：AddToBarAction、BarMatchAction。
- `Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Entity/Bar.cs`：AddTile、UpdateBarStatus、GetUnmatchedCount。
- 同目录Tile.cs：Clickable；OverBar.cs：AddTile、RemoveTile及可见性更新。
- `Module/InLevelDDA/V2/InLevelDDAV2SlackController.cs`：PreparePressureSnapshot；相对根同为GameLogic。
- 下一批R06：核对普通牌TileClicked到AddToBar/BarMatch的ECA配置和事件调度，以及OverBar可见格位规则；选取能实现M01和M07的合法最小状态。不要将本次动作类追踪扩大为所有特殊Tile均按同一路径运行。

## 批次 R06：普通牌ECA、移动结束与弃牌栈（2026-09-13）

版本仍为cd3aea166；源码静态核对，未运行Unity或测试。

### 配置与时序已确认

- `Assets/Game/TileV2/Config/TileConfig/Normal.json` 的普通牌MatchCount=3。TileClicked行为先要求BarHasSpace(1)、LivesAtLeast(1)，按配置执行三次Attack事件再AddToBar(Click)；不是所有点击都无条件直接入槽。
- 同配置的BarMatch响应事件是BarChanged，而不是AddingToBarByClick。TileConfigLoader优先类型专属JSON，不存在时普通组回退Normal.json；本结论仅适用于使用该配置的普通牌，不覆盖全部特殊类型或线上资源覆盖。
- 图形与Headless的 `Views/Bar/BarCellContentContainer.cs` 均在移动完成后对Click类型发布BarChanged（携带牌ID）。BarMatchAction由此解锁并寻找匹配；BarMatchActionInvoker等待匹配动画后再发布TileDestroyed。故初始入槽、DDA评估、匹配确认与实体销毁是不同阶段。
- DomainEventBus.PublishForEnumKey直接遍历订阅者调用Handle；EventDispatchService也直接调用actor.ProcessEventOpportunity。ActionResult列表是结果收集，不能理解成所有逻辑动作都延后到表现执行。异步移动完成是另一条后续事件来源。
- 对回放的含义：仅复现输入顺序仍不足以证明一致，需检查BarChanged等完成事件与后续输入的相对顺序；Headless有相同事件入口，不代表实际时间顺序已验证相同。

### 新增指标口径差异：ReservedSpace

`BarHasSpaceCondition` 使用 `CurrentCapacity-UnmatchedCount-ReservedSpace` 判断是否至少有1格；Slack.ComputeMetrics使用 `max(0,CurrentCapacity-UnmatchedCount)`，没有扣ReservedSpace。

条件反例：若Capacity=7、UnmatchedCount=5、ReservedSpace=2，普通点击准入剩余0，不通过；Slack的F却为2。若另有模型成本1的路线，则H=1。此为公式与配置结合的静态反例：**未证明该预留状态与DDA实际调用同时可达**，暂不列为已复现缺陷。Bar.AddTile会释放该牌自己的预留，但不能由此推出所有其他预留也已清空。

下一步追ReserveBarSpaceAction的实际配置来源、释放和调控机会是否交叠，再决定是否需要扣除预留。不能未经生命周期验证直接改公式。

### M07弃牌栈的资格已细化

OverBarData按列存储，默认加入最少牌的一列，特定索引可覆盖选择；追加到列末，索引y=list.Count-1-index，故列末新牌为y=0。TileData.UpdateVisibility在InOverBar时将y<=0设为Highlight，其余设为Visible。OverBar移除后重算该列索引并刷新该列其他牌可见性。

因此M07应拆成两项：顶牌A且无锁/阻断效果、BarHasSpace通过时具备普通取回入口；被压在下方的A仅Visible，不能立即点击。FastNCD两者都不计入，成组计数却会计入符合计数条件的全部弃牌。只有顶牌样本才适合验证“遗漏即时资源”，下层样本须计算取回顺序，不可统一按成本1加入。

### 已选定的最小状态说明（非已运行样本）

- M01：普通配置A手牌2张、Board高亮可点A1张、至少1个点击可用槽、无效果/锁/预留；观察入槽后DDA快照、移动结束BarChanged、匹配和销毁四个节点。
- M07a：将第三张A置于OverBar某列y=0，其他条件同上；对照FastNCD漏计与合法点击取回路径。
- M07b：在该列A之上放另一张普通牌，使A的y=1；验证A不可立即点，取上层后转高亮。
- 当前是依据真实配置与索引规则确定的状态约束，未生成合法运行记录或实际执行。不得将“最小状态说明”写成“样本验证通过”。

### 源码证据与下一批

- `Assets/Game/TileV2/Config/TileConfig/Normal.json`；`Scripts/Config/Tile/TileConfigLoader.cs`（Scripts位于TileV2下）。
- GameLogic下 `Behaviours/Condition/Implementation/BarHasSpaceCondition.cs`、`Behaviours/Action/Implementation/BarActions.cs`、`Entity/Bar.cs`、`Data/OverBarData.cs`、`Data/TileData.cs`、`Entity/OverBar.cs`。
- `Assets/Game/TileV2/Scripts/DomainEvent/DomainEventBus.cs`；GameLogic下Services/EventDispatchService.cs。
- `Assets/Game/TileV2/Scripts/GameCore/View/GameView/Views/Bar/BarCellContentContainer.cs`及Headless对应文件；`GameCore/Application/ActionInvoker/Implementation/BarActionInvokers.cs`。
- **下一批R07**：只追ReservedSpace与DDA调用的实际交叠，随后把M01/M07最小状态对接既有测试/构造工具，明确可运行路径与缺项；避免再次重复宏观候选清单。

### R07：ReservedSpace 与 DDA 快照的事务交叠（2026-09-14）

- 版本：`DDA-V3-Test @ cd3aea16656814e0e226205c3c225c36a94deded`；分支仍为 `DDA-V3-Test`，未发现新提交。TileScape 工作区存在与本研究无关的未提交资源/临时文件，本轮未触碰。
- 当前 TileV2 配置检索中，`ReserveBarSpaceAction` / `ReleaseBarSpaceAction` 没有被 JSON 配置引用；唯一搜到的空间预留配置是 `Mystery.json` 的 `HandleForwardTileClick` Commit 阶段 `ReserveSpaceCount=1`。该结论限于仓库当前检索到的配置文件，不排除运行时动态配置。
- Mystery 点击事务先 Capture 目标槽位，播放销毁动画并销毁效果；Commit 阶段解析捕获槽位、给目标牌加 Common 锁、按配置预留 1 格，再发出 `HandleForwardTileClick` ActionResult。表现层完成回调进入 `CompleteTransaction` 后先释放该目标预留、解锁，再检查转发条件；目标仍可点时才发布原目标的 `TileClicked`。
- 普通 `AddToBarAction` 的顺序是移除 Board/OverBar 索引、调用 `Bar.AddTile`、再 `Board.InvokeLevelDDA`。`Bar.AddTile` 先按目标 ID 释放该牌自身的 reservation、更新 BarStatus；因此 Mystery 转发点击走正常入槽后，DDA 快照调用前同一目标的临时预留已经释放。按静态主路径，不能把 `Slack.ComputeMetrics` 未扣 ReservedSpace 直接认定为 Mystery 这次点击的误差。
- **跨事务交叠在结构上可达**：`HandleForwardTileClickActionInvoker.ProcessAsync` 等待 Mystery 的 ViewAction 完成后才在 `finally` 调用 `data.Complete()`；`MysteryViewAction` 的延迟/缩放等待合计约 0.63 秒。此期间 reservation 已存在且目标牌 Common 锁定。`TileMatchApplication.OnLogicEventResult` 为每个结果批次创建独立 `ActionExecutionUnit`；异步循环可同时启动多个 unit（每个 unit 内按序 await，不同 unit 之间没有全局串行锁）。`UIGamePanel` 根据 GameState 控制交互，未见其以 `Application.Pending` 禁用棋盘点击；`TileView` 的点击资格按单牌状态、锁和高亮检查。因此另一张合格牌可在窗口内触发自己的 TileClicked → AddToBar → Board.InvokeLevelDDA，而先前 Mystery 的 reservation 尚未释放。BarHasSpaceCondition 会扣全部 ReservedSpace，Slack 的 F 不扣；所以这种状态下两个容量口径确实可能不同。
- 上述结论证明了静态调用结构允许交叠，不证明玩家实际能稳定地在 0.63 秒窗口中触发第二次点击，也不证明由此必然令候选/结果变化；触控、动画、输入帧序及具体剩余槽位影响实际出现率和指标结果，均未运行验证。仅有 Mystery 一笔预留且另一点击准入仍通过时，可构造最小观察：先留出至少 2 个逻辑空位，完成 Mystery Commit 使 ReservedSpace=1，再点击另一张高亮普通牌；在第二次 `Board.InvokeLevelDDA` 处对照 `ReservedSpace=1` 与 Slack 使用的 `F=capacity-unmatched`。
- 现有 `MeatloafDeltaSchemaContractTests.Mystery_UsesCaptureCommitForwardClickTransaction` 只核对配置阶段、槽位解析策略和 reservation 数；`MeatloafDeltaForwardClickContractTests` 核对完成幂等及请求/解析 ID；`MysteryClickParityTests` 核对表现层点击可见性与事件。它们均未覆盖 reservation 生命周期与 DDA 快照的先后关系。本轮只读测试源码，未运行。
- 测试构造路径：EditMode 的 `MoveToOverBarPropTests.CreateContext` 可合成 `TileMatchGameContext`、逻辑服务、`Board`、`Bar`、`OverBar`、`SequenceControl` 与测试牌；`MeatloafDeltaSequenceConstraintContractTests.CreateSequenceContext` 用反射补 `BoardData`/`SequenceData` 并挂载 `Board`。`MeatloafDeltaDdaContractTests` 以反射测试控制器私有静态 helper。未搜到测试直接构造 `TileMatchGameLogic`；目前没有包含完整建局、动画等待、第二输入、DDA 调用的集成夹具。因而可先做上下文级时序/容量测试，真实输入交叠仍需运行时或更完整的集成测试。
- 本轮结论：R06 的容量口径差异不只是假设性的静态可达性问题——独立逻辑结果 unit 可在 Mystery reservation 保持期间继续处理另一输入，存在触发另一 DDA 的代码路径；但尚未实际触发或证明这会改变选牌/体验，因此仍是待运行验证风险，不定性为缺陷。
- 来源：`TileMatchApplication.AsyncEventLoop.cs`、`TileMatchApplication.cs`、`ActionInvoker/Implementation/HandleForwardTileClickActionInvoker.cs`、`View/GameView/Views/ViewActions/Mystery/MysteryViewAction.cs`、`TileMatchGameLogic.cs`、`TileView.cs`、`UIGamePanel.cs`、`EventDispatchService.cs`、`SequenceActions.cs`；前述 reservation/config 源码；`MoveToOverBarPropTests.cs`、`MeatloafDeltaSequenceConstraintContractTests.cs`、`MeatloafDeltaDdaContractTests.cs`。本轮仅静态检索和阅读测试源码，未运行。

#### R07 下一断点

把 M01、M07a、M07b 对接已有 `MoveToOverBarPropTests.CreateContext` 合成夹具，明确各状态需要补的 board occlusion/overbar 可见性/Bar计数，并列出 DDA 快照及 BarChanged 观测点；另外将 Mystery→第二次点击→DDA 的跨 unit 窗口写成可复现步骤。先完成夹具缺口与可行关卡样本盘点，再决定哪些能用上下文级测试覆盖、哪些必须进入 Unity 运行验证；本轮不修改或运行测试。

### R08：指标输入态与真实 DDA 触发拓扑（2026-09-14）

- 版本：分支 `DDA-V3-Test`，HEAD `cd3aea16656814e0e226205c3c225c36a94deded`；与 R07 相同，无新增 DDA 源码差异。TileScape 工作区的未提交文件保持原样。
- **修正样本含义：**R04 的 M01 “手牌 A×2、可见 A×1”是指标输入行，不等于一次点击必然触发控制器。普通点击走 `AddToBarAction`：先 `Board.RemoveTile(clicked)` 得到可见性更新产生的 `regulationList`，再从 OverBar 移除、加入 Bar，最后 `Board.InvokeLevelDDA(regulationList)`；若点击没有使任何牌变成可调控目标，`InvokeLevelDDA` 对空集合直接返回。故测试若要观察 DDA，必须安排顶部/覆盖牌 X 被拿走并揭出真正目标 A（或使用明确可触发的序列揭牌事件），再于实际快照验证目标在调用列表中。
- 可复核的 M01 触发态草图：Bar 初始放 A×2 与另一未成组牌 B；点击盖在目标 A 上的普通牌 X 后，X 入 Bar，使 7 格栏的 `UnmatchedCount=4`、模型 `F=3`，同时覆盖移除令 A 成为新可见/可调控目标。A 是此刻手牌可直接补成组的指标资源。必须以 `Board.RemoveTile` 返回集合与目标资格验证此草图；卡片生命周期、A 的可见性和 `HasSeen` 状态仍需构造/运行确认。
- M07a/b 应共享一个能触发 DDA 的揭牌几何，令新揭牌的另一张牌作为控制目标，再切换 OverBar 资源：M07a 把第三张 A 置于某列顶牌 `y=0`；M07b 将 A 放在 `y=1`、上方另放可点牌 `y=0`。两种状态的花色统计都看得到 A，但只有 M07a 的 A 能立即通过 `Tile.Clickable` 路径取回。顶牌/底牌次序可由 `OverBarData.UpdateOneCellIndexes` 按列追加次序验证。此对照只证明资源资格差异，不预设应将全部 OverBar 成本加进 FastNCD。
- 现有 `MoveToOverBarPropTests.CreateContext` 能合成逻辑服务与 Board/Bar/OverBar/SequenceControl，但它的简易 `CreateTile` 把牌放在不同 x、固定 y=1，随后 `board.AddTile(tile, false)`，不生成覆盖/揭牌关系；上下文里也未设置 `InLevelDDA`。`MeatloafDeltaSequenceConstraintContractTests.CreateSequenceContext` 只补 BoardData/SequenceData 与 Board/SequenceControl，同样不是完整 DDA 夹具。故测试可复用其实体和栏构造方式，但需要显式设置重叠几何/更新可见性/目标集合，并装配 V2 DDA 才能观测真实选择。
- 已静态盘点一个已跟踪的小型几何候选 `Assets/Game/TileV2/Editor/LevelConfig/Levels/new/2.json`：18 个牌位、无 Effects/Piles，在 `(6,7)` 存在 `z=0` 与 `z=2` 的共格牌；TileType 由三类候选分配。它可作为一个潜在的覆盖/揭牌几何来源，但注释为“不需连续引导”、`LevelId=0`，且本轮没有验证其运行可用性/实际顶层关系；不作为已选定或已验证的实验关卡。工作区另有未提交 Temp 牌面，本轮未读取或使用。
- 本批明确的观测点：点击 X 后 `regulationList` 是否含预期目标；DDA 入参时 `Bar.UnmatchedCount`、`ReservedSpace`、Board 可见 A 资格、OverBar 顶牌 y 与 `F`；决策返回的 Outcome/候选类型/实体 ID；随后实际点击 A 是否成组、点击底层 A 是否被拒绝且移除顶牌后变为可点。静态公式和结构之外不填“实际结果”。
- 来源：`GameLogic/Behaviours/Action/Implementation/BarActions.cs`、`Entity/Board.cs`（RemoveTile、InvokeLevelDDA、UpdateVisibilityInRegionAndCollectRegulation）、`Data/BoardData.cs`、`Services/SequenceRegulationService.cs`、`Entity/OverBar.cs`、`Data/OverBarData.cs`、`Entity/Tile.cs`、`Config/Tile/TileConfigLoader.cs`；测试 `MoveToOverBarPropTests.cs`、`MeatloafDeltaSequenceConstraintContractTests.cs`；候选关卡 `Levels/new/2.json`。仅静态追踪/数据盘点，未运行 Unity 或测试。

#### R08 下一断点

以 `Levels/new/2.json` 为只读几何候选，核实标准化加载后的顶层/可见目标与 TileType 池分配；并从测试装配链确认最小 V2 DDA fixture 所需的 services/config。随后将 M01/M07a/M07b 观察点落成运行步骤与预期日志字段。若候选文件不能提供可控目标，改用合成 LevelConfig 几何；暂不改牌面或测试代码。

### R09：研究基线与当前分支发生分流（2026-09-14）

- 当前检查：`feat-winStreak @ 3d1d339c7ac4010002ea02af190ed4f46c9c52a4`；共同基点为 `5ac5062261240cd5ad7e790fd5cda11834389525`。`DDA-V3-Test @ cd3aea16656814e0e226205c3c225c36a94deded` 仍有本地及远端引用，但它是分叉侧分支；未切换分支，也未触碰 TileScape 已有未提交文件。
- 对照共同基点两侧及 V3 基线到当前 HEAD 的 DDA 文件树：`feat-winStreak` 删除 `InLevelDDAV2SlackController.cs`（完整 Slack 候选/指标实现），并从 `InLevelDDAV2Strategy` 删除 Slack 分支、决策日志和诊断显示；当前 `TryExchangeTileInternal` 固定回到 `SelectStrategy()` 的 V2 概率档位，再执行所选策略。当前树中不再有 `FastNCD`、`HardSlack`、`SlackTuning` 或控制器符号。
- 当前策略还把 `_initialTotalTileCount` 固定为 `LevelConfig.Tiles.Count`，而 V3 基线取已建棋盘牌数并以配置数回退。这是显示统计来源变化；未评估会否影响非 Slack 功能。
- `MeatloafDeltaDdaContractTests` 在当前分支删除了 Slack 私有 helper 的深度资格、直接成组偏好和可见路线成本用例；保留的统计/事件契约不能作为 V3 指标回归覆盖。V3 控制器源码和该类契约仍可从 `DDA-V3-Test` ref 静态读取，但当前工作区不能据当前 assembly 执行这些测试。
- 结论：六目标研究的实际对象依旧明确为 `DDA-V3-Test @ cd3aea166`；当前 checkout 已不是该实现，故旧批次只作为 V3 分支分析有效。后续可继续通过分支引用做只读静态研究；若要 Unity/自动化运行验证，须先有包含 V3 实现的隔离可运行环境。本轮不擅自切分支或建 Git worktree。
- 来源：`git log --left-right DDA-V3-Test...HEAD`、共同基点 `5ac5062`；V3 与当前版本的 `InLevelDDAV2Strategy.cs`、V3 控制器文件树状态、`TileMatchGameLogic.cs`、`MeatloafDeltaDdaContractTests.cs`。全为提交树对照，未运行构建或测试。

#### R09 下一断点

继续从 `DDA-V3-Test` ref 读取源文件，不依赖当前 checkout 的 DDA 类；完成 R08 的候选几何/装配清单，并明确哪些只能在 V3 分支 Unity 环境验证。每轮继续核对当前分支指针与工作树，避免把两个分支的证据混写。

### R10：揭牌资格、随机牌池与夹具边界（2026-09-14）

- 版本：只读 `DDA-V3-Test @ cd3aea16656814e0e226205c3c225c36a94deded` 源码与受跟踪关卡文件；当前 checkout 仍是 `feat-winStreak @ 3d1d339c7`。未切分支，未改 TS 文件。
- `Levels/new/2.json` 的 18 个牌位都未显式写 `TileType`，其默认值为 `Random`；加载器保留随机标记，`GetRandomTileCount()` 计入这 18 张。关卡 `ElementsPerLevel=3`，随机分配策略先生成平衡类型索引再对全池洗牌，因此初始化后每类6张，但具体坐标类型不固定；不可把静态关卡直接指定成 M01 的 A/B/X 布局。
- `(6,7)` 的 `z=2` 覆盖 `z=0`。顶牌移除并刷新区域可见性后，底牌若此前未见且由 `NotVisible` 转为 `Highlight` 或 `Visible`，V2 会置 `CanTriggerRegulationThisVisibilityChange`；`Tile.ShouldRegulateType()` 对该标记走 `IsDDAEnabledForTile`，检查 `IsCanJoinDDA` 和对应 TileConfig 的 `Capabilities.CanJoinDDA`。因此该几何是实际调控目标的静态候选，但仍要满足初始化可见性、DDA 类型为 V2、牌型能力和运行时事件顺序。`Board` 会先更新可见性，再收集合格 Tile 到 regulationList；空列表会让 `InvokeLevelDDA` 提前返回。
- 牌型随机策略随后按 TileConfig 列表顺序为 `FromRandom` 槽位写入打乱后的平衡类型。候选关卡适合作为自然揭牌几何观察对象，不适合作为可控 A/B 指标反例的确定性牌面来源；M01/M07 的验证夹具应合成小型 LevelConfig 并固定牌型与重叠关系。
- 当前可复用 `MoveToOverBarPropTests.CreateContext` 的 GameContext、Board、Bar、OverBar、SequenceControl 与基础逻辑服务；新增夹具至少需配置 `LevelConfig`（明确固定 TileTypes/随机标记）、支持牌型能力的 `TileConfigs`、`RandomService`、V2 `InLevelDDA`、真实重叠 `BoardData`、开启可见性更新的牌移除路径，并设定 `TileMatchGameLogic.GameContext`。基础 builder 当前不挂 V2 DDA，合成牌位无重叠且添加时关闭可见性刷新，故不直接覆盖揭牌调控。
- 夹具可断言的首个静态预期：顶层移除后底层 tile 的 visibility 从 `NotVisible` 转为 `Highlight`/`Visible`；未见过且可加入 DDA 时进入本次 `regulationList`，并仅在列表非空时执行 V2 调控。M01/M07 场景还要按 R08 固定 Bar / OverBar 状态，并观察每个目标的 TryExchange 输入、触发标记和交换结果。
- 边界：以上是分支源码与关卡数据的静态闭环，不是运行结果。当前环境 checkout 不包含 V3 控制器，尚未跑 Unity 或测试；不得把构造条件表述成验证通过。

#### R10 下一断点

从 `DDA-V3-Test` 引用只读核对 `MoveToOverBarPropTests.CreateContext` 的每项依赖与 `InLevelDDAV2` 构造/挂载方式，整理成最小夹具装配表；区分可用 EditMode 上下文测试核对的可见性/目标收集，与必须在含 V3 实现的 Unity 环境核对的策略选择和表现时序。若没有可运行 V3 环境，先交付清晰的静态验证步骤与日志字段，不切换或创建 worktree。

### R11：V2 调控夹具的装配层级（2026-09-14）

- `MoveToOverBarPropTests.CreateContext` 可准确复用的基底为：`LevelConfig.Reset()`、按牌型建 `TileConfig` 字典、构造 `TileMatchGameContext`，反射初始化 `GameData.SequenceData`，调用 `BehaviourFactory.Initialize()`，注册 Random/EventDispatch/PendingDestroy/Effect 服务，设置 `Statistic`，构建并挂载 `Board(BoardData)`、`Bar`、`OverBar`、`SequenceControl`，最后设当前 `TileMatchGameLogic.GameContext`。构造牌时该测试用 `board.AddTile(tile, false)`，所以没有覆盖重叠揭牌刷新。
- `InLevelDDA` 构造签名为 `(context, InLevelDDAType.V2, v1Config, v2Config)`，V2 实例化 `InLevelDDAV2Strategy`；context 的 `SetInLevelDDA` 是 internal，测试已有同程序集路径调用其他 internal setter，可按相同方式挂载。
- V2 `TryExchangeTile` 的 Slack 候选路径核心依赖为 `Board`、`Bar`、`OverBar`、`TileConfigs`、`LevelConfig`、`RandomService`、`Statistic`；实际执行交换还走 `TileService.ExchangeTilePairsPosition`，产生的 ActionResult 由 `EventDispatchService.EnqueueResults` 分发。因此将验证拆两层更小：先只构造带重叠 BoardData 的上下文，测试移除顶牌后的可见性标记和 regulationList；然后补齐 `TileService` / `EventDispatchService`、V2 DDA 与具体 config，核对 FastNCD/HardSlack 的候选、决策及交换结果。第二层策略验证必须回到含 V3 控制器的 Unity 测试程序集。
- 装配表：必需数据为可固定牌型的 LevelConfig、TileConfigs（`MatchCount` 与 `Capabilities.CanJoinDDA` 明确）、真实坐标/层级、SequenceData；上下文组件为 RandomService、Statistic、Board/Bar/OverBar、SequenceControl 和全局 GameContext；策略交换阶段再补 TileService、EventDispatchService 和 `InLevelDDA(V2, v2Config)`。若只测目标收集，不必先模拟玩家点击或表现层异步，但需使用 `Board.RemoveTile(..., updateVisibility:true)` 的真实收集路径，并直接断言返回列表与 TileData 可见性标记。
- 当前 `feat-winStreak` checkout 不含 Slack 控制器，故本轮没有执行 EditMode 测试，也未构造 Unity 测试代码；装配信息是源代码盘点，不代表这些依赖已在测试中验证可以最小化。

#### R11 下一断点

将 R08 的 M01/M07 观察态改写成分层测试规格：Layer A 只验遮挡揭牌、DDA 资格与 regulationList；Layer B 在 V3 Unity 环境验 Slack 快照/策略/交换和 ECA 时序。明确逐步操作、每步断言字段及不能从静态源码得出的内容；继续使用分支 ref，只读且不改 TS 测试代码。

### R12：M01/M07 分层验证规格（静态方案）

- Layer A（可在 EditMode 上下文层验证）：先创建固定 A/B 类型配置和 V2 DDA，再把同格 `top X z=2`、`lower A z=0` 一次性加入，统一 `Board.UpdateAllIndexes()`、`UpdateAllTileVisibility()`，并调用 `TileMatchGameContext.InitializeSeenStateFromCurrentVisibility()` 重建最终初始 HasSeen；断言 A 为 `NotVisible` 且 `HasSeen=false`。以 `Board.RemoveTile(top, updateVisibility:true)` 移除 X，断言 A 转为 Highlight 或 Visible、`CanTriggerRegulationThisVisibilityChange=true`，并进入返回的 regulationList；把 A 的 `IsCanJoinDDA` 或 TileConfig `Capabilities.CanJoinDDA` 设为 false 作排除对照。记录可见性、HasSeen、trigger flag、regulationList tile IDs。Layer A 不调用 DDA 策略、不声称指标变化。
- Layer B（需 V3 Unity 测试环境）：按 R08 建立 M01 状态（Bar A×2+B×1，目标牌 X 覆盖 A，目标 A 是唯一揭牌调控对象；点击后 X 入 Bar 且 `UnmatchedCount=4`、容量7时预期 `F=3`），再对 M07a/M07b 只改变第三张 A 的 OverBar 堆叠位置 `y=0`/`y=1`。两者可共存于同一合成快照：X 用独立普通牌型且可点，OverBar 牌预置而不经本次点击入栏。每次以实际 AddToBar → regulationList → InvokeLevelDDA 顺序执行，固定随机种子并分别记录点击前后 Bar/OverBar/Board 状态。
- 观测项分为调用前事实、决策与结果：调用前记录目标 Tile ID/type/depth/visibility/HasSeen、Bar.UnmatchedCount/ReservedSpace/CurrentCapacity、Board 可见牌类型与 OverBar 各列 y；决策记录 SlackDDA 日志中的 source、curve、progress、targetHard、currentHard/currentPerceived、candidate 范围、selectedHard/selectedPerceived、strategy type、fallback、noSwapReason；结果检查目标与被选牌交换后的 Position、Board 可见性/HasSeen、ECA 返回和后续点击资格。V3 日志未包含候选实体 ID，需由 EditMode 断言交换坐标或受控临时测试记录补足。
- 可由静态结构确定的是上述调用入口、状态字段与日志字段存在；不能静态确定随机路径最终候选、预测指标、是否换牌、表现异步排序、M07a 是否能在给定完整局面中立即成组。这些必须运行固定种子用例。当前 checkout 没有 Slack 控制器，故此方案尚未执行。

#### R12 下一断点

回到 V3 分支源码逐项复核 M01 的普通点击是否能自然产生唯一揭牌 A、点击 X 的 Bar 变化与 regulationList 调用次序，以及 M07a/b 的目标资格是否与点击 X 的揭牌共存；若状态组合有冲突，改写最小状态规格而不改代码。之后整理本轮结果到 Daily，并保留运行验证边界。

### R13：M01/M07 共存与初始 HasSeen 重建（2026-09-14）

- 版本核对：当前 `feat-winStreak @ 3d1d339c7ac4010002ea02af190ed4f46c9c52a4`，V3 ref 仍为 `DDA-V3-Test @ cd3aea16656814e0e226205c3c225c36a94deded`，共同基点不变；分支与 HEAD 相比 R09–R12 未变。TileScape 当前未提交文件新增了部分 Tutorial/UI/配置相关变化；本轮继续不读取临时牌面、不触碰工作区文件。
- M01 和 M07a/b 的状态在静态层面可以共存：让被点击的普通 X 是独立牌型且覆盖唯一调控目标 A；Bar 预置 A×2+B×1；OverBar 单独预置第三张 A 顶牌或底牌。点击 X 后它以第四个未成组单位进入 Bar，目标 A 因遮挡移除而触发调控；OverBar A 不依赖本次点击入栏。容量7、当前无其他reservation时，`UnmatchedCount=4`、模型 `F=3`；若要研究实际玩家可达性，仍需证明此前形成的 OverBar 牌面来源与测试步骤，不把合成快照等同于自然局面。
- 修正 R12 夹具初始化：`TileData` 构造的默认索引会先按 Highlight 路径更新显隐并可能标记 `HasSeen`。正式初始化完成后，`TileMatchGameLogic.Event.Handle(LevelEnterAnimationStepOneFinished)` 调用 `InitializeSeenStateFromCurrentVisibility`；该方法对每张牌按最终可见状态重建 HasSeen，并清除临时触发标记。故夹具必须先完成完整遮挡几何与索引/可见性更新，再重建 HasSeen，最后才开始揭牌动作；不能先单独添加底牌并刷新造成其“被看见”。
- 推荐 Layer A 构造顺序：先按正式顺序建立 Context、类型与 TileData、Board（完整建牌后统一 `UpdateAllIndexes()` / `UpdateAllTileVisibility()`），再挂载 V2 DDA；执行 `context.InitializeSeenStateFromCurrentVisibility()`，断言底层 A 为 NotVisible/HasSeen=false、顶层 X 可点；最后调用真实 `Board.RemoveTile(X,true)` 并断言 A 的 visibility、trigger flag 和 regulationList ID。若该测试层没有正式初始化调用链，则必须显式注明用手工顺序近似，不能称完全等价。
- 来源：V3 ref 的 `TileData` 构造/`SetVisibility`/`RebuildHasSeenFromCurrentVisibility`、`Board.UpdateAllIndexes/UpdateAllTileVisibility/RemoveTile`、`TileMatchGameLogic.EntityInitializer.InitEntities`、`TileMatchGameLogic.Event`、`TileMatchGameContext.InitializeSeenStateFromCurrentVisibility`，以及 R08 所列普通点击、OverBar 与 Slack 指标源码。全部静态追踪；没有编辑或运行 TS 测试。

#### R13 下一断点

静态核对真实关卡初始化的 `InLevelDDA` 创建时点、随机牌型赋值、TileData 创建、Board 初始化、入场第一步 HasSeen 重建的先后关系；据此确认 Layer A 可复用正式顺序。若完整初始化依赖大量不相关服务，记录最小差异并将 Layer A 限定为数据层验证；Layer B 仍需含 V3 控制器的 Unity 环境。之后更新当日 Daily 和验证边界。

### R14：正式建局顺序与测试夹具对齐（2026-09-14）

- `TileMatchGameLogic` 构造顺序（V3 ref）：`InitializeContext → InitDataBridge/InitLevelDiff → InitConfig → InitEntities → SolutionHint/Prop/Events/PreProp → Statistic → InitInLevelDDA → FatalDeathDetect → ResetRandomService`。所以 V2 DDA 在 TileData 与 Board 初始化完成后才挂进 Context。
- `InitConfig` 内部先初始化 GameData，按 DDA 类型选择 `LevelTileTypeInit`（V2 正常新局使用 `AssignTileTypeByDepth`，回放/重连使用 Reconnect），再加载牌型配置、刷新 LevelConfig、生成 TileData、绑定批次并重置 RandomService。`InitEntities` 再建立 Board 并从所有 TileData 初始化棋盘，刷新索引/可见性，然后初始化 Bar、OverBar、Sequence/Batch；其末尾还会重置 RandomService。挂载 DDA 并初始化复杂度后，构造函数再次重置 RandomService。
- LevelEnterAnimationStepOneFinished 稍后调用 `InitializeSeenStateFromCurrentVisibility()`：这时 DDA 已存在，HasSeen 按当前最终显隐重建。它解释了为何 TileData 构造时短暂的默认可见状态不会成为本局揭牌资格的最终状态。
- 对 Layer A 的影响：最贴近正式路径的最小夹具应先完成类型、TileData、Board 与初始全量可见性，再挂载 V2 DDA、重建 Seen 状态，最后移除 X；DDA 要在后续揭牌刷新前存在。随机种子重置仅当测试涉及牌型池或策略随机选择时才需完整复刻，固定牌面 Layer A 可直接提供最终类型并把差异记为测试夹具简化。
- 来源：`TileMatchGameLogic.cs` 构造函数、`TileMatchGameLogic.Config.cs`、`TileMatchGameLogic.EntityInitializer.cs`、`Board.InitializeFromLevelConfig` / 更新索引与显隐、`TileMatchGameLogic.Event.cs` 以及 `TileMatchGameContext.InitializeSeenStateFromCurrentVisibility`，均读取 `DDA-V3-Test@cd3aea166`。这是调用顺序静态核对，不是测试执行证据。

#### R14 下一断点

把 R13/R14 的 Layer A 正式近似顺序逐步与现有 `CreateContext` 构造器比较，明确最少新增调用和不可达的 internal/private 边界；同时确认 TileConfig 能力设置与 Board 初始刷新实际 API，给出可复核的 fixture 步骤。若仍需完整 `TileMatchGameLogic` 初始化才能保证可信，应明确保留为运行环境缺口，而不为方便虚构简化路径等价性。完成后检查主档六目标是否已有足够文档产出，研究未完则继续登记下一断点。

### R15：Layer A 与现有测试构造器的最小差异（2026-09-14）

- `MoveToOverBarPropTests.CreateContext` 已暴露可复用的基础能力：Context 的 `SetServices/SetStatisticsData/SetBoard/SetBar/SetOverBar/SetSequenceControl/SetInLevelDDA` 等 internal setter 在该测试程序集可直接调用；测试还通过反射补 `GameData.SequenceData`。无需为了揭牌目标收集而引入完整 `TileMatchGameLogic`。
- 现有 builder 的主要差异只有牌位与时序：其 `CreateTile` 将牌放到不同 x、z=0，建牌循环执行 `board.AddTile(tile,false)`，既不生成覆盖关系，也不做最终的 `UpdateAllIndexes/UpdateAllTileVisibility` 和正式入场的 Seen 重建。Layer A 可复用 Context 和 service setup，添加自定义坐标 TileData；所有牌一次加入后显式更新索引与可见性，随后挂载 `InLevelDDA(V2)` 并调用 `InitializeSeenStateFromCurrentVisibility()`。
- 现有 TileConfig 的 `Capabilities.CanJoinDDA` 是 private set，默认 true；资格关闭对照可直接用 `TileData.UpdateCanJoinDDA(false)`（internal）而无需改配置文件，或提供经配置加载的 disabled TileConfig。为避免差异混淆，首轮优先对数据对象禁用并记录与正式 JSON 能力门槛的差异。
- 可复核 Layer A 步骤：用 `CreateContext(X,A)` 建基础 Context；移除 builder 预置牌并关闭可见性刷新，重建两张固定位置牌（X `(6,7,2)`、A `(6,7,0)`）后一次性加入；调用 Board 全量索引/显隐更新；挂载 V2 DDA；调用 Context Seen 重建；断言 X Highlight 且可点、A NotVisible 且 HasSeen=false；然后 `Board.RemoveTile(X,true)`，断言 A 新显、未见触发标记为真并出现在返回集合。第二次对照先在 A 上关闭 CanJoinDDA，再重复揭牌，要求 A 不进入集合。实际 API 可组成这个上下文级验证，但本轮未运行它。
- 边界：此序列忠实覆盖 Board 的几何、显隐与 DDA 目标资格；没有复现 `TileMatchGameLogic` 的 `InitConfig` 随机类型池、多个 RandomService 重置、ECA 点击准入、BarChanged 及表现回调。策略层仍须在含 V3 控制器环境验证。此处将 Layer A 定义为可独立验证的数据层契约，不声称覆盖玩家完整事件链。

#### R15 下一断点

检查 G1–G6 完成标准与现有文档产出，更新六目标状态表：把本轮确认的 Layer A 边界与 Layer B 运行缺口反映到相应目标；确认是否还存在可仅凭源码完成的重大缺口。之后形成下一批聚焦问题，或在所有静态研究目标达标时停止推进研究并保留提醒自动化。

### R16：G5 性能缺口的静态上界与测量项（2026-09-15）

- 版本仍为 `DDA-V3-Test@cd3aea166`；当前 `feat-winStreak@3d1d339c7`。分支与 HEAD 对比 R09–R15 无变化，故此处只读 V3 引用，不把结论扩展为当前 checkout 实际成本。
- 每个目标进入 `InLevelDDAV2SlackController.SelectExchangeTarget` 后都会调用 `PreparePressureSnapshot`：重新计算全 Board Tile 深度，遍历 Bar、OverBar、Board 建压力计数；之后遍历 NotVisible 候选并筛合法实体。对每个唯一候选类型分别跑 `ComputeMetrics`；每次指标计算会遍历 `_routeTypes` 求最低路线成本，并在有解时再遍历一次以统计正确选项。因此单目标成本包含一次全局深度/压力/候选扫描和至多 `候选花色数 × 2 × 路线花色数` 次路线评估。多目标 `regulationList` 由 `Board.InvokeLevelDDA` 逐个调用 `TryExchangeTile`；前一目标换位可能改变几何和可见性，所以每目标重算有正确性理由，不能简单假定整批可共用快照。
- 这是一项数据规模相关的性能测量要求，不是已证瓶颈。V3 中未见对应耗时采样或缓存命中统计；当前 feat checkout 没有 Slack 控制器，故无 profiler 数据。最小测量建议在 V3 Unity 环境按不同 Board 大小、隐藏候选类型数及单批目标数分层，记录每目标 Snapshot/Depth、Candidate、Metrics 耗时，候选/路线类型数、batch 目标数及总耗时 P50/P95/max；再决定是否优化，并保留换位后重新计算的正确性边界。
- G1–G6 静态文档产出盘点：G1 有分支版本/代码链路；G2 M01–M10 与指标反例、触发拓扑已整理；G3 D01–D09 决策边界已整理；G4 六类体验对照假设齐全；G5 回放、配置、随机、统计、性能风险、日志与夹具缺口均有静态证据和补齐建议；G6 三条路线和退出条件已有记录。按主档标准，依赖运行数据的结论保留“待验证”与影响，不虚构通过。本轮未发现还需额外静态检索才能补齐的主要研究问题，故**静态策略研究文档阶段收尾**；这不表示 DDA 运行验证完成。
- 尚未完成的执行验证统一留在 G1–G5 状态：当前 checkout 没有 V3 控制器；V3 Unity 环境下 Layer A/B 与回放/性能实验、玩家体验数据仍未取得。若以后获得 V3 可运行环境或新增业务数据，可按各目标下的观察方案开启验证工作；在此之前不继续重复静态检索。五小时提醒自动化保留。
- 来源：`Board.InvokeLevelDDA`、`InLevelDDAV2Strategy.TryExchangeTileInternal`、V3 `InLevelDDAV2SlackController.SelectExchangeTarget/PreparePressureSnapshot/CollectLegalCandidates/ComputeMetrics/TryComputeRouteCost`、`TileDepthComputer.ComputeAllTileDepths`。仅静态控制流与循环盘点，未测性能。

#### 静态研究收尾后的接续条件

静态策略整理的六项目标已完成并关闭本阶段研究推进。窗口提醒自动化继续按原时刻发送；后续只在用户明确恢复研究，或出现含 V3 控制器的可运行环境/新业务数据时继续相应运行验证，不重复扫描既有静态结论。

## 每轮记录协议

- 记录批次、代码版本、目标编号、来源文件、已确认结论、推演与待验证项。
- 更新本主档后同步 Daily；重要长分析可拆子文档并回链。
- 不重复把历史报告全文改写成新版本；在旧基线上显式标注适用范围并指向增量。
- 自动化没有新证据时不制造进展；按已有提醒要求发送窗口提醒，研究部分只汇报实际新结论或阻塞。

## 关联

- [[02-PROJECTS/TileScape/_MOC|TileScape MOC]]
- [[02-PROJECTS/TileScape/游戏逻辑/评估-DDAV3逻辑与实现策略-2026-09-11|首版评估：9be729cb3 基线]]
- [[01-DAILY/2026-09-11|当日记录]]
