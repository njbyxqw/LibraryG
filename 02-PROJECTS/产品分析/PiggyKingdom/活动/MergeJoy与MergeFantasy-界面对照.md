---
title: Piggy Kingdom Merge Joy 与 Merge Fantasy 界面对照
date: 2026-11-19
type: research
status: current
lifecycle: current
tags: [产品分析, PiggyKingdom, Merge, UI]
---

# Merge Joy 与 Merge Fantasy 界面对照

实拍确认 Joy 的主界面是浮在压暗背景上的大型框式弹窗，音乐舞台与棋盘装在同一块紫金面板内。Fantasy 是全屏农场，棋盘下方的葡萄地块和厨师火鸡直接融入场景。Joy 截图显示 `Finished`，仅据此图无法核定轮次及开场态。Fantasy 的葡萄与制作派画面匹配场景 11。Android 2.7.3 默认相邻窗口及不同设备的开放证据见 [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy与MergeFantasy-活动排期|活动排期]]。

| 界面 | Merge Fantasy · 农场主题 | Merge Joy · 音乐舞台主题 |
|---|---|---|
| 主界面外壳 | 全屏农场场景。顶部是木牌标题和倒计时，中间为目标条与 7 列棋盘，底部是厨师火鸡、葡萄地块和工具余额。 | 大型紫金框式弹窗，面板四周可见压暗背景。上半部用红色标题和蓝幕舞台，吉他、鼓组、麦克风营造主题，下半部承载 6 列棋盘。 |
| 棋盘可见尺寸 | 实拍 7 列 × 7 行，合计 49 格，含覆盖格。 | 结束态实拍 6 列 × 8 行，合计 48 格，含底部一行与覆盖格。 |
| 棋盘周边 | 图鉴入口和主链目标在棋盘上方。葡萄地块和火鸡位于棋盘外，可直接作为操作对象。 | 目标条压在舞台下沿，棋盘上方显示合成领奖提示，盘内覆盖层采用金色音符。暂存物品气泡挂在棋盘下方正中，截图数字为 12。 |
| Progress 礼包 | 入口在右上。打开后棋盘留在背后并压暗，红金弹窗左列显示 `Use Tools!` 的累计消耗，中、右列为免费与 VIP。 | 入口嵌在舞台右侧，截图显示 `Finished`。包内场景 28 指定紫色版 `MergePassPanel_9`，任务列展示待解锁目标物，共 10 档。音乐主题截图的礼包展开态尚缺。 |
| 帮助 | 全屏压暗棋盘。4 段依次为通关、点植物采集、制作派、收集物品领奖。第三段随场景变化。 | 帮助文案为 3 段，通关、取得物品、收集目标物。独立帮助页会加载主题插图、资源和礼盒图，实际排版待实拍。 |

Fantasy 实拍 Progress 的 5/10/15 工具档显示免费工具各 ×1，VIP 分别 ×2、×3、×5，与备用 `MergePassConfig_1` 前三档奖励吻合。截图报价为 PHP 265.00，属于该样本。此前拼图用了默认 `MergePassConfig` 示意金币或骰子奖励。

## BP 进度与奖励

| 对比项 | Merge Joy | Merge Fantasy |
|---|---|---|
| 任务列 | `Unlock this item`。首次解锁主链 Lv.2–Lv.11 的指定物品，各解锁一档，共 10 档。 | `Use Tools!`。累计消耗工具推进 15 档，起档 5，末档 300。 |
| 免费轨合计 | 50 个 Joy 活动资源。 | 45 把 Fantasy 工具。 |
| 活动资源型 VIP | `MergePassConfig_1` 前三档为 2、3、5，后半段分量更大。满档付费轨合计 200 个 Joy 活动资源。 | 同表前三档同为 2、3、5，200 把工具分散在 15 档。用户实拍对上前三档。 |
| 混合奖励型 VIP | 默认 `MergePassConfig` 的满档付费轨含 3,000 金币，以及骰子、道具和卡牌奖励。前三档为 500 金币、2 个骰子、300 金币。 | 同表也含 3,000 金币及混合奖励。前三档为 500 金币、1 个骰子、200 金币。 |
| 商品 | 两套包内表均指向 `shopId=93`。音乐主题的实际售价及命中表待实拍。 | 同一商品。用户截图显示 PHP 265.00。 |

棋盘行数按截图可见范围计数。帮助以主要文案段落计数。VIP 合计为对应包内表的全部付费档奖励，独立于免费轨，获得每档仍需满足该档条件。

| Joy 实拍 | Fantasy 实拍 |
|---|---|
| [音乐舞台主界面 · Finished](https://chatgpt.com/library?file_id=libfile_fde3_f-53e3dac9e04c8191a11fd5a2a0460834_c84987d778ec81918f4b532d85214c2c&account_id=personal) | [农场主界面](https://chatgpt.com/library?file_id=libfile_fde3_f-f6a633042b7881918497425f5692f861_c84987d778ec81918f4b532d85214c2c&account_id=personal) · [Progress 礼包](https://chatgpt.com/library?file_id=libfile_fde3_f-0542e08ff3c08191950730c86a1b0f55_c84987d778ec81918f4b532d85214c2c&account_id=personal) · [帮助页](https://chatgpt.com/library?file_id=libfile_fde3_f-22a4b51c243c819195b2b51df2f08e83_c84987d778ec81918f4b532d85214c2c&account_id=personal) |

[[02-PROJECTS/产品分析/PiggyKingdom/assets/merge-interface/merge-joy51-fantasy42.webp|早期配置示意图]]

## 证据路径

- 帮助文案核对 `language_english` 的 `mergemini_guide_step1–3`、`mergeani_guide_step1–4` 和场景 11 变体。Joy 帮助页的主题资源加载见 `MergeminiGuideView_Asm.SetSceneTheme`（`0x060015A1`）。
- BP 核对 `MergePassConfig` 与 `MergePassConfig_1` 的 `activityType` 37、45。运行时分别由 `MergePassDM.OnMergeItemUnlocked`（`0x060015BD`）和 `OnMergeTokenConsumed`（`0x060015BE`）推进。

- 主界面入口对照来自 Android 2.7.3 的 `Hot.Scripts.dll`。Joy 的 `M3Client.MergeminiActivity.ShowMergeminiGame`（`0x06001F39`）在调用 `UIManager.Open<MergeminiGameView_Asm>` 前将 `true` 传给 `MainView.PauseAndHideUIElements`。Fantasy 的 `ShowMergeaniGame`（`0x06001F02`）同样隐藏首页界面。外框、底幕和留边以主题 Prefab 或实拍为准。

- 原始 Progress 资源在 `06-PRODUCT-ASSETS/PiggyKingdom/2.7.3/05-Runtime/20261119-interface/bundles/`，来自 MuMu 实例 1「产品分析」的只读磁盘样本。原 Prefab 为 `MergePassPanel_9` 和 `MergePassPanel_3`。`ui_mergepass_v1` 的 SHA-256 为 `b839fe346ce3eafe70140d794d24995cc73960677429d0f44b3f741328b7b88d`，`merge_common_ui_v1` 为 `24d58d1c425e8a4383358a0ac62d4773d2f0efde4169991e064f9b43564a0732`。
- 小麦与镰刀分别来自包内 `prefabs/levelrewards/collect_nearby_mergemini` 与 `collect_nearby_mergeani` 的资源依赖。在 `UnityDataAssetPack.apk` 内成员末段分别为 `0ef998fd7cf24419eb9152cd3ba924ac` 和 `da49dd5d9f7284819bad6c9ef9320377`。默认排期、场景、文案与奖励表见 [[02-PROJECTS/产品分析/PiggyKingdom/资源路径索引#Merge 系列活动清单（2026-11-19）|资源路径索引]]。
