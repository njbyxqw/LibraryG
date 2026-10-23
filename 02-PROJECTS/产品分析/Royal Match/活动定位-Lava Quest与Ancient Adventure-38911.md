---
title: Royal Match 38911 Lava Quest 与 Ancient Adventure 活动规则
date: 2026-10-21
type: product-analysis
status: current
lifecycle: current
tags:
  - 产品分析
  - RoyalMatch
  - 活动系统
  - 连胜活动
  - REA
aliases:
  - Lava Quest 与 Ancient Adventure
  - Lava Quest 规则
  - Ancient Adventure 规则
---

# Royal Match 38911 Lava Quest 与 Ancient Adventure 活动规则

> [!summary] 本轮结论
> - **Lava Quest**：玩家主动开始一轮挑战，与 99 名历史数据模拟玩家组成 100 人局；连续首过 7 关即获胜，任何一关最终失败都会结束本轮。获胜者均分 10,000 金币奖池，客户端按 10 金币粒度向上取整；失败后当前公开规则为等待 30 分钟再试。
> - **Ancient Adventure**：以过关自动进入并推进的个人连胜路线。38911 同时保留单阶段和三阶段实现：单阶段为 7 步；三阶段依次为 5、7、10 步。失败把**当前阶段**进度归零，已完成阶段不回退；阶段结束可直接领取阶段奖，也可进入 12 张牌的 Heist 奖励玩法。
>
> 当前公开帮助页给出玩家可见规则；阶段结构、失败处理、奖励计算和 Heist 规则来自 38911 客户端静态代码。当前账号实际命中哪套 Ancient Adventure 实验、精确奖励值和档期仍由服务端配置决定。

## 一、规则证据口径

| 证据层 | 本文用途 |
|---|---|
| Royal Match 官方帮助页 | 当前玩家可见的时长、解锁、进入方式、人数、重试与基础奖励规则 |
| 38911 IL2CPP 静态代码 | 状态机、步数、失败归零、阶段切换、奖励计算、Heist 处理 |
| 服务端模型与本地持久化结构 | 能够下发和保存的数据范围；不等于当前账号实际配置 |
| 用户运行观察 | Lava Quest / Ancient Adventure 在周中、周末档位轮换；本文不据此推断固定星期 |

官方页面：

- [Lava Quest - Royal Match Help Center](https://dreamgames.helpshift.com/hc/en/3-royal-match/faq/187-lava-quest/)
- [Ancient Adventure - Royal Match Help Center](https://dreamgames.helpshift.com/hc/en/3-royal-match/faq/560-ancient-adventure/)

以下代码路径均相对于：

`06-PRODUCT-ASSETS/RoyalMatch/38911/04-ReverseEngineering/IL2CPP_Static/cpp2il-diffable-cs/DiffableCs/Assembly-CSharp/`

## 二、Lava Quest

### 2.1 玩家规则卡

| 项目 | 规则 |
|---|---|
| 解锁条件 | 等级 66 及以上 |
| 进入方式 | 在活动入口点击 **Start**；需要联网 |
| 每轮目标 | 连续首过 7 个关卡 |
| 参赛规模 | 玩家本人 + 99 名模拟玩家，共 100 人 |
| 对手性质 | 不是实时对战；使用曾挑战相同 7 关玩家的历史数据构造比赛过程 |
| 胜利条件 | 完成第 7 次连续胜利；内部从 Step 1 推进到 `SuccessStep = 8` |
| 失败条件 | 任一关最终失败或活动记录到关卡中途退出；内部写入 `FailStep = 9` |
| 单轮时限 | 当前公开规则为 24 小时；若总活动先结束，也会提前终止本轮 |
| 奖励 | 所有完成 7 关的胜者均分 10,000 金币奖池 |
| 失败后重试 | 当前公开规则为等待 30 分钟后可开始新一轮 |
| 成功后 | 当前轮完成并领取奖励；客户端将该服务端活动标记为已领取，不再重复加入同一轮 |

### 2.2 一轮挑战的状态流

```text
入口点击 Start
  → 请求加入并取得模拟分组
  → Finding Players
  → Step 1
      ├─ 过关：Step + 1，并播放本步淘汰表现
      ├─ 最终失败/中途退出：Step 9，本轮失败
      └─ 到 Step 8：本轮成功
  → 成功领取金币 / 失败进入冷却
```

客户端固定常量为：

```text
InitialStep = 1
TotalStepCount = 7
SuccessStep = 8
FailStep = 9
```

- `EnteredLevel()` 在进入有效关卡时写入“正在关卡中”。
- `WonLevel()` 清除该标记并推进一步。
- `FailedLevel()` 清除该标记并直接写入失败终态。
- `CheckIfQuitInGame()` 和无法恢复关卡的处理，会把仍处于关卡中的异常退出视为失败。
- 活动管理器只接收关卡最终的 Win / Fail 结果，没有“使用关卡内续步即单独判负”的规则；因此购买续步后最终过关，活动侧仍收到胜利，真正放弃或结算失败才会断连胜。

### 2.3 模拟分组与淘汰表现

加入请求会发送玩家当前 `Level` 和 `LeagueLevel`，服务端返回：

| 字段 | 作用 |
|---|---|
| `Scenario` / `ScenarioId` | 选择本轮历史模拟场景 |
| `StepUserCounts[]` | 每一步仍留在比赛中的人数，用于人数下降和卡片跌落表现 |
| `WinnerCount` | 不含玩家本人的其他胜者数 |
| Leader/Profile 数据 | 显示模拟参赛者姓名、头像、头像框及游客/Facebook 资料 |

因此界面上的“多人同时推进、逐步落入岩浆”是按服务端历史场景播放，并不代表 100 人正在实时同步游玩。

### 2.4 奖金结算

公开规则为 10,000 金币由完成挑战的玩家均分。38911 的实际发奖方法为：

```text
总胜者数 = 服务端 WinnerCount + 玩家本人
基础份额 = 10000 / 总胜者数（整数除法）
个人金币 = 基础份额向上取整到 10 的倍数
```

示例：

| 总胜者数 | 个人金币 |
|---:|---:|
| 1 | 10,000 |
| 2 | 5,000 |
| 3 | 3,340 |
| 6 | 1,670 |

所以玩家看到的是“均分奖池”，客户端发放时还做了一次 10 金币粒度的向上取整。

### 2.5 时限、冷却与可加入条件

可加入不仅取决于图标是否出现，还要求：

- 账号达到等级 66；
- 服务端活动已开启且未被后台关闭；
- 当前没有未结束、未领取的 Lava Quest；
- 冷却已经结束；
- 活动剩余时间足够开始下一轮；
- 网络可用，并能取得分组信息；
- 当前仍有可游玩的主线或联盟关卡。

失败或超时后会保存 Cooldown End Date。当前官方值是 30 分钟；包内存在一份旧的本地兜底配置，但持续时间参数与当前公开规则不一致，应视为被服务端覆盖或不再直接使用，不能当作线上生效值。

### 2.6 规则定位

| 模块 | 路径/方法 |
|---|---|
| 核心管理器 | `Royal/Player/Context/Units/LavaQuestManager.cs` |
| 持久化进度 | `Royal/Player/Context/Data/Persistent/LavaQuestProgress.cs` |
| 配置 | `Royal/Player/Context/Data/LavaQuest/LavaQuestConfig.cs` |
| 分组返回 | `Royal/Infrastructure/Services/Backend/Protocol/EnterLavaQuestResponse.cs`、`LavaQuestUserGroupInfo.cs` |
| 奖励计算 | `LavaQuestManager.GetInventoryPackage()`，原生地址 `0x01CB6EF4` |
| 关键埋点 | `LavaQuestEnter`、`LavaQuestFinish`、`LavaQuestClaim` |

## 三、Ancient Adventure

### 3.1 玩家规则卡

| 项目 | 规则 |
|---|---|
| 解锁条件 | 等级 66 及以上 |
| 进入方式 | 过关时自动开始/加入，不需要像 Lava Quest 一样先点击 Start 组队 |
| 核心目标 | 持续首过关卡，沿当前 Adventure 路线推进 |
| 对抗性质 | 个人进度活动，没有玩家分组或实时排行榜 |
| 单轮时限 | 当前公开规则为 24 小时 |
| 失败 | 当前 Step 归零；单阶段版本相当于整段从头开始，多阶段版本只重置当前 Stage |
| 重试 | 失败后可立即重新开始，不设 30 分钟冷却 |
| 奖励 | 可含中途 Step Reward、Stage Reward、金币和 Seasonal Card Collection 卡包；精确数值由服务端配置 |
| 完成 | 单阶段或全部三阶段完成后，写入 `FinishedStage = 4` |

### 3.2 单阶段版本

38911 的 `IsAncientAdventureOneStaged` 实验会启用单阶段活动：

- 进入时逻辑 Stage 直接设为 2；
- Stage 2 的目标步数固定为 **7**；
- 每次胜利 Step +1；
- 任一关最终失败时 Step 归零，因此需要重新完成 7 连胜；
- 完成后 Stage 直接写为 4，活动结束；
- UI 层通过 `GetUiStageForOneStageEvent()` 映射为 Stage 3 主题表现，因此“逻辑 Stage 2”和“画面使用第三阶段资源”并不矛盾。

当前官方帮助页用“失败后从 Adventure 开头重新开始”的口径描述活动，与这套单阶段规则一致。

### 3.3 三阶段版本

客户端仍保留完整三阶段实现：

| 阶段 | 需要连续胜利 | 失败后 |
|---:|---:|---|
| Stage 1 | 5 关 | 当前阶段 Step 归零，已完成阶段不受影响 |
| Stage 2 | 7 关 | 当前阶段 Step 归零，Stage 1 仍保持完成 |
| Stage 3 | 10 关 | 当前阶段 Step 归零，Stage 1、2 仍保持完成 |

完整路线需要累计通过 22 关，但不是要求一次性 22 连胜；每个 Stage 是一段独立连胜检查点。

阶段转换规则：

```text
当前阶段达到目标 Step
  → 领取阶段结算奖励，或进入 Heist
  → Stage + 1
  → Step = 0
  → 清空当前阶段最高 Step 与失败动画状态
  → Stage 3 结束后写入 Stage 4，活动完成
```

### 3.4 胜负、退出与进度保存

- `ProceedNextStep()` 在胜利后把 Step 加 1。
- 达到配置中的中途奖励步数时，奖励会直接加入库存，并记录已到达的最高 Step。
- `FailStep()` 明确执行 `SetStep(0, shouldSave: true, shouldSync: false)`，即把当前阶段进度归零。
- 失败时会保存 Step Up/Fail 动画数据；如果本来就在 Step 0，则不再额外播放一次下坠动画。
- 关卡退出检查会消费“中途退出”标志并调用 `FailedLevel()`，因此退出、崩溃后无法恢复的关卡同样会断掉当前阶段连胜。
- 与 Lava Quest 相同，活动层只看关卡最终 Win / Fail；关卡内购买续步本身没有独立判负分支。

### 3.5 奖励结构

服务端配置可定义：

| 层级 | 字段 | 规则意义 |
|---|---|---|
| 活动 | `v`、`s[]`、`os` | 配置版本、三阶段配置、单阶段配置 |
| Stage | `sgr` | 该阶段最终奖励 |
| Stage | `str[]` | 指定 Step 到达时的中途奖励 |
| Stage | `hd[]` | Heist 三档卡片数量和金币值 |
| Step Reward | `st`、`r` | 奖励触发步数与奖励内容 |
| Heist | `oc`、`cr` | 每档卡片数量与对应金币奖励 |

规则特点：

- 中途 Step Reward 在到达相应步数时自动领取，不需要等整个阶段完成。
- 未启用 Heist 时，阶段完成后直接领取配置的 Stage Reward。
- 启用 Heist 时，阶段完成会转入 Heist，再由翻牌结果决定本阶段金币奖励。
- 奖励可以包含普通物品和 Seasonal Card Collection 卡包。
- `EventRewardOverrider` 可按活动或账号覆盖 Step Reward，因此包内结构不能反推出当前线上精确数值。

### 3.6 Heist 规则

Heist 是 Ancient Adventure 的可选阶段结算玩法：

1. 界面生成 **12 张隐藏卡片**。
2. 奖励分为低、中、高三档；每档的卡片数量和金币额来自该 Stage 的 `hd[]` 配置。
3. 客户端使用活动与进度派生的 Seed 预先打乱卡片，牌面排列在开始选择前已经确定，并非点击后临时算结果。
4. 玩家逐张翻牌；当任意一档累计翻出 **3 张**时，Heist 立即完成。
5. 玩家获得该档配置的金币奖励。
6. 已选择卡片和完成状态都会持久化，因此掉线重进可恢复当前 Heist。

客户端为三个奖励档分别记录翻出次数，并在领奖埋点中上报 `heistLowestCount`、`heistMediumCount`、`heistHighestCount`。当前账号是否启用 Heist 由 `IsAncientAdventureHeistEnabled` 实验结果决定。

### 3.7 时限、重新开始与实验

- 结束状态有 `TimeFinished = 0`、`Completed = 1`、`Restart = -1`。
- 24 小时到期或服务端总活动结束会终止本次 Adventure。
- 失败后可立即从当前段 Step 0 再走，不进入冷却。
- 单阶段/多阶段和是否启用 Heist 都会在进入活动时固化到本地进度，避免同一轮中途切换实验导致结构改变。
- 客户端含新老用户两组相关实验 ID（146/147、152/153），但实验分流条件和当前线上比例不在包内。

### 3.8 规则定位

| 模块 | 路径/方法 |
|---|---|
| 核心管理器 | `Royal/Player/Context/Units/AncientAdventureManager.cs` |
| 公共状态机 | `Royal/Player/Context/Units/AncientAdventure/AncientAdventureCommonModel.cs` |
| 持久化进度 | `Royal/Player/Context/Data/Persistent/AncientAdventureProgress.cs` |
| 配置 | `Royal/Player/Context/Data/AncientAdventure/AncientAdventureConfig.cs`、`AncientAdventureStage.cs` |
| 阶段步数 | `GetStepCount()`：Stage 1/2/3 = 5/7/10，原生地址 `0x01BA7200`、`0x01BA6DD8` |
| 失败归零 | `AncientAdventureCommonModel.FailStep()`，原生地址 `0x01BA7224` |
| 推进一步 | `ProceedNextStep()`，原生地址 `0x01BA7290` |
| 切换阶段 | `ProceedNextStage()`，原生地址 `0x01BA78E8` |
| Heist | `Royal/Scenes/Home/Ui/Dialogs/AncientAdventure/AncientAdventureHeistController.cs` |
| 关键埋点 | `AncientAdventureFinish`、`AncientAdventureClaim` |

## 四、配置、数值、分组与关卡调控

### 4.1 可分析深度

| 范围 | 38911 静态包可确认 | 仍需运行时/服务端 |
|---|---|---|
| 配置结构 | 字段、层级、读取与覆盖链 | 当前档期实际下发内容 |
| 固定数值 | 解锁等级、目标步数、成功/失败状态、奖励计算公式 | 活动时长、冷却、分步人数、Ancient 奖励数字等动态值 |
| 分组 | Lava 请求字段、分组返回字段、客户端如何生成展示身份 | 服务端如何选历史样本、是否使用请求体外的账号画像 |
| 关卡关联 | 进入、胜利、失败、退出和恢复失败的完整回调链 | 运行时异常路径是否被服务端二次修正 |
| 难度调控 | 可检查两活动是否直接调用棋盘、步数、生成权重或 DDA | 服务端或全局关卡系统独立存在的调控策略 |

结论口径：**活动规则和客户端执行逻辑可以高置信还原；服务端分组算法与当前账号实际配置不能仅靠 APK 定案。**

### 4.2 Lava Quest 配置与分组协议

客户端配置模型 `LavaQuestConfig` 只有四个字段：

| 字段 | 含义 | 来源/边界 |
|---|---|---|
| `v` | 配置版本 | 服务端下发 |
| `d` | 单轮持续时间，秒 | 服务端可覆盖 |
| `c` | 失败后的冷却时间，秒 | 服务端可覆盖 |
| `r` | 奖励物品 | 当前公开规则对应 10,000 金币奖池 |

`LavaQuestInfo` / `GetLavaQuestInfoResponse` 会下发 `ServerEventId`、剩余时间、配置版本和 JSON 配置；客户端据此更新本轮结束时间和本地配置。包内虽有一份 `d=300000`、`c=50000` 的兜底 JSON，但与当前公开的 24 小时/30 分钟不一致，不能作为当前线上值。

玩家点击 Start 时，`EnterLavaQuestRequest` 请求体明确只有：

```text
Level
LeagueLevel
```

`EnterLavaQuestResponse` 返回服务端活动 ID 和 `LavaQuestUserGroupInfo`：

| 返回字段 | 客户端用途 |
|---|---|
| `Scenario` / `ScenarioId` | 选择和持久化本轮历史模拟场景 |
| `StepUserCounts[]` | 驱动每一步剩余人数和淘汰动画 |
| `WinnerCount` | 计算玩家最终分到的金币 |

所以能确定的是：

- 请求体没有显式发送胜率、连胜、付费、失败次数或棋盘难度，只发送当前 `Level` 和 `LeagueLevel`；
- 这不排除服务端在认证上下文中读取其他账号资料，但 APK 无法证明它具体用了哪些指标；
- 服务端返回的是“场景 + 每步人数 + 最终胜者数”，客户端负责保存并播放；
- Facebook 玩家资料返回后，客户端会为展示对象组合 Facebook ID、本地随机用户名、头像和头像框；不足部分由 Guest 资料补齐，因此展示身份不等同于实时对手。

### 4.3 Ancient Adventure 配置层级

Ancient 使用公共配置和账号配置两层：

- `AncientAdventureInfo` 下发服务端活动 ID、剩余时间、公共配置版本和 JSON；
- `GetAncientAdventureInfoResponse.AncientAdventureUserConfig` 下发账号实际命中的用户配置；
- 客户端再根据单阶段/多阶段、Heist 和 Reward Overrider 实验决定最终表现。

配置结构为：

```text
AncientAdventureConfig
  v    配置版本
  s[]  三阶段配置
  os   单阶段配置

AncientAdventureStage
  sgr  阶段结算奖励
  str[] 中途步数奖励
  hd[] Heist 奖励档
```

其中 `StepRewardData = (st, r)`，表示触发步数与奖励；`HeistData = (oc, cr)`，表示某档卡片数量与金币值。阶段目标 5/7/10、单阶段 7、失败归零和三张同档牌结算属于客户端规则；每个 `sgr`、`str[]`、`hd[]` 的当前数值则需要账号响应才能确认。

### 4.4 与关卡结算的回调链

两项活动都通过中央 `EventsHelper` 接收普通关卡结果：

```text
GameManager.StartGame
  → EventsHelper.EnteredLevel()
  → Lava / Ancient 记录进入关卡

UserManager.LevelEnd / UpdateEventsOnLevelWin
  ├─ 最终胜利 → EventsHelper.WonLevel()
  └─ 最终失败 → EventsHelper.FailedLevel()

关卡无法恢复或检测到中途退出
  → EventsHelper.WontRestoreLevel() / CheckIfQuitInGame()
  → 按失败处理，断开当前连胜
```

细节边界：

- Lava 胜利时 Step +1，失败写入 Step 9；Ancient 胜利推进当前阶段，失败执行 `Step = 0`；
- 使用金币续步不会直接触发活动失败，活动只接收最终 Win / Fail；
- Side Progression 关卡不会走两项活动的通用推进回调；Lava 的 `OnSideProgressionLevelWin()` 只记录一个后续 UI 展示标志，不增加 Step，Ancient 也没有对应的进度增加入口；
- 因而当前静态证据支持：主线/联盟的普通关卡结算计入连胜，支线关卡不计入。

### 4.5 是否直接调控关卡难度

对两个活动管理器的静态引用边界检查中，能找到的是 Prelevel 面板、关卡进入/结算、失败警告、活动弹窗、奖励、存档、通知和埋点；没有找到它们直接写入以下系统的调用边：

- 棋盘布局或关卡数据；
- 初始步数、剩余步数或续步价格；
- Tile/障碍生成权重和随机种子；
- 关卡难度标签或 DDA 参数。

因此更准确的结论是：**Lava Quest 和 Ancient Adventure 在客户端属于“观察关卡最终结果并推进活动”的上层系统，未发现它们直接改变局内难度。** 这不等于 Royal Match 没有全局 DDA，也不能排除服务端依据账号数据决定活动资格或历史场景；只能说明 38911 中没有找到“这两个活动 → 棋盘/步数/生成参数”的直接链路。

### 4.6 进一步抓取的最小字段集

若要把动态数值补齐，优先记录：

| 活动 | 响应/数据 | 可补齐内容 |
|---|---|---|
| Lava | `LavaQuestInfo.Config` | 实际 `d`、`c`、`r` |
| Lava | `EnterLavaQuestResponse.LavaQuestUserGroupInfo` | 本轮 Scenario、7 步人数曲线、WinnerCount |
| Ancient | `AncientAdventureInfo.Config` | 公共活动版本和时限配置 |
| Ancient | `AncientAdventureUserConfig` | 单/三阶段实际配置、Step/Stage 奖励、Heist 三档数值 |
| Ancient | 本地实验与进度 | 是否启用 One Staged、Heist、Reward Override |

## 五、目前仍由运行时决定的信息

| 信息 | 为什么静态包不能定案 | 最合适的验证方式 |
|---|---|---|
| Ancient 当前是单阶段还是三阶段 | 由账号实验和服务端配置决定 | 同账号活动界面 + `GetAncientAdventureInfo` 响应 |
| Ancient 是否启用 Heist | 独立实验标志 | 完成一个 Stage 或读取账号进度标志 |
| Ancient 每一步/每阶段奖励 | 服务端用户配置且可被 Reward Overrider 覆盖 | 活动配置响应 + 实际领奖响应 |
| Heist 三档卡数与金币 | 位于 `hd[]` 服务端配置 | 抓取配置或完整翻牌样本 |
| Lava 每步模拟存活人数 | 每轮 `StepUserCounts[]` 不同 | `EnterLavaQuest` 响应 |
| 两项活动的实际档期 | 客户端没有固定星期表 | 连续档期的 ServerEvent/UpcomingEvents 响应 |

## 六、验证边界

- 本轮只分析用户提供的 38911 XAPK，没有安装、运行或修改样本。
- REA MCP 已确认目标 `libil2cpp.so` 的身份；本机未配置 Ghidra/IDA 深度提供器，所以方法级规则来自同一二进制已生成的 Cpp2IL ARM64 反汇编与差分 C#，不是运行时 Hook 结果。
- 官方帮助页反映当前公开玩家规则；服务端仍可按活动批次、账号和实验覆盖客户端兜底配置。
- “周中/周末轮换”保留为用户运行观察，本文不把它扩展为固定星期或永久排期结论。
- `NotificationTags` 中 Lava 21、Ancient 38 是通知标签编号，不是活动枚举 ID。

## 关联

- [[02-PROJECTS/产品分析/Royal Match/活动清单与简述-38911|活动清单与简述]]
- [[02-PROJECTS/产品分析/Royal Match/系统活动关卡与主场景框架-38911|系统活动、关卡与主场景框架]]
- [[02-PROJECTS/产品分析/Royal Match/资源与逻辑分析总览-38911|资源与逻辑分析总览]]
- [[02-PROJECTS/产品分析/_MOC|产品分析 MOC]]
