---
title: Tile Kingdom 1.58 Tile Temple 活动静态拆解
date: 2026-10-19
type: analysis
status: verified-static
tags:
  - 产品分析
  - 竞品
  - TileKingdom
  - 活动
  - IL2CPP
aliases:
  - Tile Kingdom Tile Temple 活动拆解
---

# Tile Kingdom 1.58 Tile Temple 活动静态拆解

> [!info] 证据边界
> 本文基于用户授权提供的 Tile Kingdom `1.58` XAPK、Unity 序列化资源与 ARM64 IL2CPP 静态恢复。文中的类、字段、明确调用和分支为静态证据；界面流向是由状态类及调用关系整理出的静态流程；服务端下发值、远端 Addressables 内容和实际运行表现均未验证。

## 样本与产出

| 项目 | 内容 |
|---|---|
| 包名 / 版本 | `com.dreamloft.tilekingdom` / `1.58`（133） |
| Unity 版本 | `2021.3.45f2` |
| C# 结构索引 | `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/04-ReverseEngineering/IL2CPP_Static/cpp2il-diffable-cs` |
| 指令与调用证据 | `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/04-ReverseEngineering/IL2CPP_Static/cpp2il-isil` |
| 美术样本 | `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/02-Art/PNG_Filtered_Sample` |
| 音频导出 | `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/03-Audio/WAV_Export` |
| 资源目录 | `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/01-Decoded/APK/assets/aa/catalog.json` |

## 活动分层

| 层 | 已确认组件 | 职责证据 |
|---|---|---|
| 活动入口 | `TileTempleAddon`、`TileTempleEventButton` | Addon 实现 `IHomeAddon`、`IAutoShow`、`IEventEntryData` 等接口；入口按钮继承通用社交活动按钮 |
| 状态流 | `TileTempleEventStartedState`、`TileTempleInfoState`、`TileTempleLoadState`、`TileTempleState`、`TileTempleRewardState` | 分别承载首次参与、说明、加载/结算模拟、主界面和领奖状态 |
| 关卡计分 | `LevelScoringAddon` | 观察关卡胜负，支持失败重置、失败扣分、连胜与困难关倍率开关 |
| 竞赛淘汰 | `PlayerEliminationAddon` | 保存剩余玩家、分步淘汰数组、当前淘汰数、失败标记和阶段 Step，并根据分数变化执行 `Simulate` |
| 奖励 | `RewardAddon` | 通过 `RewardId` 获取奖励容器；Tile Temple 读取索引 `0` 的首个奖励 |
| 展示 | `TileTempleScreenComponent`、`TileTempleLoadScreenComponent`、`TileTempleRewardScreenComponent` | 展示分数、剩余玩家、阶段台阶、头像推进/淘汰、奖励与结算动画 |
| 埋点 | `TileTempleCompletedTrackingEvent`、`TileTempleLoseTrackingEvent` | 完成事件包含胜负结果和奖励值；失败事件记录失败阶段 `tt_stage_fail` |

## 活动弹窗时机

> [!note] 实现口径
> 从产品体验看，下列界面属于“活动弹窗/活动面板”；但代码中的 `TileTempleEventStartedScreenComponent`、`TileTempleInfoScreenComponent`、`TileTempleLoadScreenComponent`、`TileTempleScreenComponent` 和 `TileTempleRewardScreenComponent` 都继承 `GameScreenComponent`，对应状态也继承普通 `ScreenState<T>`，并不是标准 `PopupComponent / PopupState<T>`。因此它们使用统一 Screen State Stack，但不自动具备标准弹窗的遮罩点击关闭逻辑。

### 时机总表

| 时机 | 前置条件 | 调用链 | 最终界面 | 是否自动 |
|---|---|---|---|---|
| 首次从活动入口进入 | 活动未参与，用户点击 Home 活动按钮 | `HomeState.ShowEvent` → `SocialEvent.IsParticipated == false` → `ShowEventStartedCommand.ShowStartScreen` → `TileTempleAddon.StartState` | `TileTempleEventStartedState` | 否，用户主动点击 |
| 点击首次参与按钮 | `SocialEvent.Participate()` 返回成功 | `EventStartedState.OnPlayClicked` → `TileTempleEventStartedState.OnParticipate` → `Push(TileTempleLoadState, redirect: true)` | 先加载/模拟页，关闭后构建 Home + Tile Temple 主界面 | 否，承接用户操作 |
| 已参与后手动进入 | 活动已参与，用户点击 Home 活动按钮 | `HomeState.ShowEvent` → `IHomeAddon` → `HomeState.ShowAddonState` → `TileTempleAddon.GetState()` | `TileTempleState` | 否，用户主动点击 |
| Tile Temple 关卡产生分数变化后回到 Home | 当前关卡带 `IsTileTempleActive`，淘汰模块尚未判定已输或已赢，`Simulate` 将 `NeedCheck` 置为真 | `OnScoreChanged` → `PlayerEliminationAddon.Simulate` → `NeedCheck = true` → Home 命令流水线中的 `AutoShowEventsCommand` → `ShowAddonState` | `TileTempleState` | 是 |
| 关卡失败并最终放弃续关 | 已参与事件中存在 `IForceShowOnLevelLose.ForceShowOnLevelLose == true` 的活动；Tile Temple 固定返回真 | `LevelLoseState.Lose` → `LevelState.Fail` → 查找首个强制展示活动 → 取其 `IHomeAddon.GetState()` → `Build(HomeState, 活动状态)` | Tile Temple 被选中时为 `TileTempleState`，替代普通 `LevelFailedState` 路径 | 是，失败强制展示 |
| 淘汰模拟结束且满足领奖 | `TileTempleAddon.CanReward()` 为真，即尚未领奖且淘汰赛已胜利 | `TileTempleState.StartSequence` → `PlaySimulation` 完成 → `CanReward` → `Push(TileTempleRewardState)` | `TileTempleRewardState` | 是，紧跟模拟结算 |
| 查看规则/奖励说明 | Tile Temple 主界面点击 Info | `TileTempleState.OnInfoClicked` → `Push(TileTempleInfoState)` | `TileTempleInfoState` | 否，用户主动点击 |

### 关后自动展示的核心标记

`TileTempleAddon.AutoShow` 并不是直接判断活动是否激活，而是直接返回 `PlayerEliminationAddon.NeedCheck`。

`NeedCheck` 的生命周期如下：

```text
带 Tile Temple 特性的关卡发生分数变化
  ↓
TileTempleAddon.OnScoreChanged
  ↓
PlayerEliminationAddon.Simulate
  ├─ 已经 IsLost：不再处理
  ├─ 已经 IsWon：不再处理
  └─ 其余情况：推进 Step/淘汰人数，并将 NeedCheck = true
  ↓
回到 Home 后 AutoShowEventsCommand 找到该活动
  ↓
HomeState.ShowAddonState → TileTempleState
  ↓
TileTempleScreenComponent.PlaySimulation
  ↓
演出后段将 NeedCheck = false
```

因此，自动展示的产品语义是“有一段尚未向玩家结算展示的淘汰进度”，而不是“每次回首页都展示活动”。`NeedCheck` 带 `[Save]`，说明它被纳入活动进度存档；这支持待展示状态跨界面保存，但实际落盘时点和重启后的恢复仍需运行验证。

### 首次参与后的界面串联

首次点击参与时，`EventStartedState.OnPlayClicked()` 先调用 `SocialEvent.Participate()`；只有返回成功才调用 Tile Temple 的 `OnParticipate()`。随后：

1. 压入 `TileTempleLoadState(addon, redirect: true)`；
2. Load State 阻塞输入，读取奖励数量和 `GetEliminationResult()`，播放加载/淘汰模拟；
3. 关闭 Load State 时，由于 `redirect == true`，不是普通 `Pop`，而是通过 `Build` 重建 `HomeState + TileTempleState`；
4. Tile Temple 主界面创建时直接启动 `StartSequence()`。

这条路径把“加入活动”“初始化模拟”“进入活动主界面”拆成三个连续状态，避免首次参与后直接落入一个尚未准备好数据的主界面。

### 失败时为什么会强制弹出

`TileTempleAddon.ForceShowOnLevelLose` 固定返回 `true`。在玩家于 `LevelLoseState` 中最终确认失败后：

1. 先执行 `LevelState.Fail()`，使活动计分/淘汰模块收到失败结果；
2. 从 `SocialEventManager.ParticipatedEvents` 中查找第一个实现 `IForceShowOnLevelLose` 且返回真的活动；
3. 若找到，则构建 `HomeState` 和该活动的 `IHomeAddon.GetState()`；
4. 若没有找到，才走普通 `LevelFailedState`。

因此 Tile Temple 的失败结算不是单纯等待首页自动弹出，而是在“放弃续关并确认失败”的路径中主动抢占普通失败结算。若同时存在多个强制展示活动，代码使用 `FirstOrDefault`；哪个活动先展示取决于已参与事件的枚举顺序，本地基础包无法确认远端实例顺序。

### 胜利后的奖励弹出

`TileTempleState.OnCreate()` 在完成界面订阅和 `Setup` 后调用 `StartSequence()`：

1. 先播放 `TileTempleScreenComponent.PlaySimulation()`；
2. 等待模拟完成，并让出一帧；
3. 调用 `TileTempleAddon.CanReward()`；
4. 只有 `IsRewarded == false && PlayerEliminationAddon.IsWon == true` 时，才压入 `TileTempleRewardState`；
5. Reward State 准备奖励表现时将 `IsRewarded` 置为真；关闭奖励页时会移除其下方的 `TileTempleState`，再弹出 Reward State，回到更下层界面。

这说明奖励页不是在分数变化瞬间弹出，而是必须等 Tile Temple 主界面的晋级/淘汰模拟播放完成后再出现。

### 首页自动展示的竞争关系

`AutoShowEventsCommand` 位于 Home 的 Command Executor 中。它从“已参与活动”获取实现 `IAutoShow` 的 Addon，要求候选同时可作为 `IHomeAddon`，且 `AutoShow == true`，再调用 `HomeState.ShowAddonState()`。

当前能确认：

- Tile Temple 只有 `NeedCheck == true` 时才进入自动展示候选；
- 命令一次保存并展示一个候选 Addon；
- Home 同时还有 Build、广告、评价、章节、Offer、未领奖励、活动开始等多类命令。

当前不能确认：

- 多个 `IAutoShow` 活动同时满足时的远端实例枚举顺序；
- Home 各命令在所有场景下的最终展示优先级，因为 Command Executor 会结合各命令的 `CanExecute`、异步执行和继续条件反复判断；
- Tile Temple 是否还配置了 `ShowEventStartedAddon` 从而在活动激活时主动弹首次介绍。该 Addon 属于远端活动组合，本地基础包只确认用户点击未参与活动入口时一定会进入 `StartState`。

## 已确认的具体逻辑

### 参与与计分驱动

1. `TileTempleAddon.OnParticipate()` 给 `LevelScoringAddon` 内部计分器订阅 `ScoreChanged`。
2. `OnScoreChanged(ScoreArgs)` 先检查当前关卡记录的 `LevelFeatures.IsTileTempleActive`。
3. 只有该特性激活时，才调用 `PlayerEliminationAddon.Simulate(args)` 推进淘汰模拟。
4. `OnEnd()` 解除 `ScoreChanged` 订阅，避免活动结束后继续响应分数变化。

因此可以确认：Tile Temple 并非每次普通得分都推进，而是由带 Tile Temple 特性的关卡结果驱动淘汰流程。

### 胜负、领奖与再次参与

| 判定 | 静态结果 |
|---|---|
| `HasWon()` | 直接返回 `PlayerEliminationAddon.IsWon` |
| `CanReward()` | `IsRewarded == false` 且 `PlayerEliminationAddon.IsWon == true` |
| `GetReward()` | `RewardAddon.GetFirstRewardAt(0)` |
| `IsLost()` | 活动过期，或 `PlayerEliminationAddon.IsLost` 为真 |
| `CanReparticipate()` | 当前活动实例累计胜利次数 `< 2` |
| 胜利收尾 | `OnEnd()` 在获胜时把实例胜利次数加 `1` |
| 客户端排名 | 获胜时为 `1`；否则为淘汰模块内部排名值 `+ 1` |

### 结算展示链路

- `TileTempleLoadState.OnCreate()` 先阻塞输入。
- 从 `TileTempleAddon.GetReward()` 取得奖励数量并交给加载界面 `Setup`。
- 从 `PlayerEliminationAddon.GetEliminationResult()` 取得本轮淘汰结果，再调用加载界面的 `PlaySimulation`。
- 主界面的 `PlaySimulation` 使用玩家分数、剩余人数、晋级分数、淘汰头像、晋级头像和阶段台阶做演出；并暴露 `ProfilesJump`、`PlatformBreak`、`TextCountCompleted` 三类表现事件。

## 尚不能确认的数值

`PlayerEliminationAddon` 已明确暴露以下字段，但本地基础包没有对应活动实例的完整序列化配置，因此不能填入具体值：

- `PlayersToEliminateArray`：各阶段淘汰人数数组；
- `MaxWinningPlayers`：最终允许获胜的玩家数；
- `PlayersLeft`、`Step`：当前进度存档；
- `RewardId` 与具体奖励容器；
- 计分倍率、失败扣分及活动时长等远端参数。

Addressables 目录项引用了独立的 `tiletempleevent_assets_all_92d842778bd9967c665102fd5ce6d59c.bundle`，但该文件未随基础 APK 落盘。需要在授权范围内取得对应远端 bundle、服务端配置响应或运行时证据，才能补齐上述数值与专属美术。

## 音效证据

基础 Unity Data 中共有 `265` 个 AudioClip，已全部无失败导出为 WAV。与 Tile Temple 直接同名的本地音效有：

| 名称 | 时长 | 静态用途线索 |
|---|---:|---|
| `sfx_tiletemple_platform_breaking` | 1.28 秒 | 对应主界面 `PlatformBreak` 事件与台阶破裂表现 |
| `sfx_tiletemple_profiles_moving` | 0.84 秒 | 对应 `ProfilesJump` 事件与玩家头像推进表现 |

此外，代码中的 `TileTempleState` 还持有 `platformBreakSoundKey`、`profilesJumpSoundKey`、`textCountSoundKey`、`ambienceSoundKey`，并维护一个 ambience AudioSource。基础包只凭同名 AudioClip 能直接对应前两项；计数声和环境声的具体资源绑定仍需 Prefab 或运行时配置证明。

整个音频包还覆盖局内 Tile 点击/落牌、炸弹、Chain/Ice/Grass/Honey/Jar/Curtain 等障碍、章节建设、Chef、Heist、Peril、Tile Tower、奖励、关卡成功/失败及 10 条长音乐。`Music` / `SFX` 目录是按 30 秒时长生成的浏览分类，不是原项目的 AudioMixer 分组。

## 可继续追查的问题

- `PlayerEliminationAddon.Simulate` 与 `GetEliminationResult` 的逐分支还原，可进一步解释每轮晋级/淘汰算法；
- `LevelScoringAddon` 的困难关、连胜和失败扣分如何共同影响活动分数；
- 专属 bundle 到手后，对照 Prefab、阶段数组、奖励配置和界面表现；
- 结合 Prefab 或运行时配置确认 Tile Temple 的计数声、环境声 key 与具体 AudioClip 绑定；
- 运行时仅用于验证静态推断，不把网络下发的单次配置误写成固定产品规则。

## 关联

- [[02-PROJECTS/产品分析/_MOC|产品分析 MOC]]
- [[02-PROJECTS/产品分析/Tile Kingdom/资源与逻辑分析总览-1.58|Tile Kingdom 1.58 资源与逻辑分析总览]]
- [[02-PROJECTS/产品分析/Tile Kingdom/资源路径索引|Tile Kingdom 资源路径索引]]
- [[02-PROJECTS/Agent/工具/指南-REA休闲游戏APK静态分析接入与边界|REA 休闲游戏 APK 静态分析接入与边界]]

