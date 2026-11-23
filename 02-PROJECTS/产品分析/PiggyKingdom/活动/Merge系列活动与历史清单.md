---
title: Piggy Kingdom Merge 系列活动与历史清单
date: 2026-11-19
type: research
status: current
lifecycle: current
aliases: [Piggy Kingdom 二合活动清单, Merge Joy, Merge系列历史]
tags: [产品分析, PiggyKingdom, Merge, 活动]
---

# Piggy Kingdom Merge 系列活动与历史清单

在 Android `2.7.3 / 203` 包内，活动模板和默认排期共同收录了 **5 个 Merge 玩法入口**。Merge Joy 对应 `mergemini`，Merge Fantasy 对应 `mergeani`，各有自己的棋盘和主题轮次。Milk Farm、Chick Feast、Piggy Spa 则是同一个喂养活动在不同场景使用的三种标题。公开资料还留下了 2024 年的水下 Merge Wonders，以及 2026 年的 Labor Day Woodland Merge 宣传卡。

## 玩法与主题库存

| 游戏内英文名 | 活动标识 · 默认配置 | 玩法识别点 | 包内场景与明确指定的轮次 |
|---|---|---|---|
| **Merge Joy** | `mergemini` · `MergeMiniConfig` | 放置物品，在棋盘上二合推进奖励 | `scenes_new` 有 28 个场景，其中 27 个配置指定轮次 25–51。场景 2 未填轮次。旧 `scenes` 有 25 个场景。 |
| **Merge Fantasy** | `mergeani` · `MergeAniConfig` | 用工具采集、二合，推进解云、开地及动物支链 | `scenes_new` 有 9 个场景，覆盖轮次 34–42。旧表有 7 个场景。图鉴主题线索包括薰衣草与羊毛、马戏团、珊瑚与宝藏、南瓜与幽灵等。[[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeFantasy/逻辑与配置-2.7.3#7. 主题变化与“本期”确认边界\|9 个场景的图鉴品类]] |
| **Merge Wonders** | `merge2` · `MergeConfig` | 开箱获得物品，以二合产物推进任务 | 3 个场景合计覆盖轮次 26–80。2024 年版本说明提到水下主题，尚无法对应到场景编号。 |
| **Merge Adventure** | `mergedig2` · `MergeDig2Config` | 用镐挖出物品，合成拿钥匙进入下一阶段 | 1 个场景配在轮次 26、28、30、32、36、40。包内还有 `MergeDigConfig`，与 `MergeDig2Config` 的同名字段中只有棋盘表有差异。现有排期只列 `mergedig2`。 |
| **Milk Farm / Chick Feast / Piggy Spa** | `mergefeed` · `MergeFeedConfig` | 点动物喂养以取得新物品，再继续合成。通用提示使用 Merge Feed。 | 轮次 1 对应场景 1 Milk Farm，轮次 2 对应场景 2 Chick Feast，轮次 3 对应场景 3 Piggy Spa。 |

Merge Joy 的轮次可用来定位历史截图和素材。轮次 25、26、27 分别指向场景 3、4、1，轮次 28–51 依次指向场景 5–28。场景 23–28 的表内 ID 为 1023–1028。英文文本确认了统一入口标题，逐个场景的玩家可见主题名仍待取证。

喂养玩法另有 `mergefeed_title_4` 等文案键，缺少对应的英文文本和场景行。第四个主题的名字及上线情况未知。

**Merge Progress**（`mergepass`，付费项显示为 Merge Pass）是随部分 Merge 玩法出现的双轨进度，**Merge Master** 是排行标题。默认排期未为两者列出独立 Merge 场次。[App Store 内购列表](https://apps.apple.com/us/app/piggy-kingdom-match-3-games/id1635337354)

## 找到的公开记录

| 日期或版本 | 可确认的记录 | 来源 |
|---|---|---|
| 2024-11 · Android 1.8.6、1.8.9 | 两个版本的更新说明都称 **Merge Event**，1.8.9 还提到新增活动头像框。文案未给出具体玩法名。 | [版本更新说明存档](https://piggy-kingdom.apk.watch/1.6.0)，对应包的镜像上传日为 11-21、11-29 |
| 2024-12 · Android 1.9.1 | 更新说明明确写出 **Merge Wonders** 及水下主题。 | [版本更新说明存档](https://piggy-kingdom.apk.watch/1.6.0)，对应包的镜像上传日为 12-14 |
| 2025-03-08、2025-04-28 | 两个玩家上传的视频均以 Piggy Kingdom **Merge Wonders** 标记。日期为投稿日，轮次未核。 | [3 月投稿](https://www.youtube.com/watch?v=d2qRsUXBZxI) · [4 月投稿](https://www.youtube.com/watch?v=nywYPlkh1uY) |
| 2026-04-27 | 玩家反馈提到 **Merge Joy** 活动的结算问题。 | [4 月玩家反馈](https://outagedown.com/game/piggy-kingdom-match-rescue) |
| 2026-09 · Google Play 活动卡 | **Labor Day Woodland Merge** 显示 09/20 结束。年份采用商店快照的 2026 年 9 月上下文，活动入口与场景 ID 待核。 | [Google Play 游戏页](https://play.google.com/store/apps/details?hl=en-US&id=com.olleyo.piggy.king.free)，活动卡来自历史搜索快照 |
| 2026-10-13 | 玩家评论再次明确提到 **Merge Joy**。 | [10 月玩家评论](https://www.appbrain.com/app/piggy-kingdom/com.olleyo.piggy.king.free) |

## 排期线索与来源

Merge Joy 与 Merge Fantasy 的默认轮次已按客户端计算更新，并与 11/18 模拟器服务器缓存逐项对照。见 [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy与MergeFantasy-活动排期|Merge Joy 与 Merge Fantasy 活动排期]]。

以下为 `2.7.3` 包内三套默认排期一致的首段窗口，时间为 UTC。五项都配置为重复，归入组 11、首页位置 1。用这些日期定位旧版本或截图时，需要另取实际开服记录。场景轮次只在各自活动的配置中解释。

| 活动 | 包内默认排期的首段窗口 |
|---|---|
| `mergeani` | 2023-09-25 08:00:00 至 2023-10-02 07:29:59 |
| `merge2` | 2024-11-25 08:00:00 至 2024-12-02 07:29:59 |
| `mergemini` | 2024-12-09 08:00:00 至 2024-12-16 07:29:59 |
| `mergedig2` | 2024-12-16 08:00:00 至 2024-12-23 07:29:59 |
| `mergefeed` | 2026-08-10 08:00:00 至 2026-08-17 07:29:59 |

包内清单依据英文文本、活动模板、活动排期、远端选表键及各活动默认配置交叉核对。现有本机样本的五个玩法均无有效开放起止时间，因此实际首发时间、地区或账号覆盖、每期主题仍需历史截图或开放期采样。精确文件入口见 [[02-PROJECTS/产品分析/PiggyKingdom/资源路径索引#Merge 系列活动清单（2026-11-19）|Merge 系列证据路径]]。

## 关联

- [[02-PROJECTS/产品分析/PiggyKingdom/_MOC|Piggy Kingdom 产品入口]]
- [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeFantasy/README|Merge Fantasy 功能档案]]
