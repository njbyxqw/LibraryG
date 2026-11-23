---
title: Piggy Kingdom Merge Joy 与 Merge Fantasy 活动排期
date: 2026-11-19
type: research
status: current
lifecycle: current
aliases: [Merge Joy 与 Merge Fantasy 排期, Piggy Kingdom 二合活动排期]
tags: [产品分析, PiggyKingdom, Merge, 活动排期]
---

# Merge Joy 与 Merge Fantasy 活动排期

**包内默认是四周一个循环，按周依次为 Joy → Fantasy → Joy → 两者均无默认场次。** 两个玩法的单轮窗口都是周一 16:00 开启，下一周周一 15:29:59 截止。时间统一为 UTC+8。此规律来自 Android 2.7.3 / 203 的客户端排期计算。

**服务器缓存已确认有覆盖。** 11 月 18 日 20:07，「产品分析」模拟器收到的活动开放记录是 **Merge Wonders 第 77 轮，11/16 16:00–11/30 15:29:59**。同一批缓存里 Joy 与 Fantasy 的开关均为关闭，且无服务端轮次记录。这条 Wonders 记录横跨包内默认的 Fantasy 42 和 Joy 52 两段窗口。对其他账号和地区的实际上线时间仍需另取记录。

## 近期日期

以下场次均为包内推演。每行从首日 16:00 至末日 15:29:59。

Joy 51 与 Fantasy 42 的界面与奖励预览见 [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy与MergeFantasy-界面对照|界面对照]]。

| 日期（UTC+8） | 默认玩法与轮次 | 包内明确指定的场景 | 服务器记录对照 |
|---|---|---|---|
| 10/12–10/19 | Joy 49 | 场景 26（配置 ID 1026） | 10/13 有玩家提及 Joy，未取得其账号的期号与起止时间。 |
| 10/19–10/26 | Fantasy 41 | 场景 10，图鉴为南瓜点心、蜡烛、幽灵 | 待采样 |
| 10/26–11/02 | Joy 50 | 场景 27（配置 ID 1027） | 待采样 |
| 11/02–11/09 | 两者均无默认场次 | — | 待采样 |
| 11/09–11/16 | Joy 51 | 场景 28（配置 ID 1028） | 待采样 |
| 11/16–11/23 | Fantasy 42 | 场景 11，图鉴为葡萄酒、木餐具、派 | 11/18 样本只有同组的 Wonders 77，Fantasy 开关为关闭。 |
| 11/23–11/30 | Joy 52 | 默认场景表无显式轮次映射 | 11/18 缓存的 Wonders 77 窗口覆盖本周。Joy 是否另有下发待刷新。 |
| 11/30–12/07 | 两者均无默认场次 | — | 待采样 |
| 12/07–12/14 | Joy 53 | 无显式映射 | 待下发 |
| 12/14–12/21 | Fantasy 43 | 无显式映射 | 待下发 |
| 12/21–12/28 | Joy 54 | 无显式映射 | 待下发 |

10/13 的公开玩家反馈日期落在 Joy 49 的默认窗口内，可用来定位旧样本。用户近期见过 Joy 与 Fantasy 两项活动，看到的日期和期号待对照。图鉴主题对应关系见 [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeFantasy/逻辑与配置-2.7.3#7. 主题变化与“本期”确认边界|Fantasy 场景与图鉴]]。[10/13 玩家评论](https://www.appbrain.com/app/piggy-kingdom/com.olleyo.piggy.king.free)

## 排期取值与验证

| 玩法 | 默认首段（UTC+8） | `interval` | 两次开场相隔 |
|---|---|---:|---:|
| Merge Joy · `mergemini` | 2024-12-09 16:00 至 12-16 15:29:59 | 606601 秒 | 14 天 |
| Merge Fantasy · `mergeani` | 2023-09-25 16:00 至 10-02 15:29:59 | 1816201 秒 | 28 天 |

`ActivityPlanConfigProvider.ToOpenItem`（ARM RVA `0x2CD0468`）用 `end - start + interval` 算周期。在本文日期范围内，默认轮次为 `floor((当前时间 - 首段开始 + interval) / 周期) + 1`，起止时间各加 `(轮次 - 1) × 周期`。冷却期内函数可能已经返回下一轮窗口，仍须比较返回的开始时间与当前时间。包内 `ActivityPlanConfig`、`_1`、`_2` 的两条记录一致。

运行样本的 AutoP 缓存指定 `eventplan_config=ActivityPlanConfig`、`eventtemplate_config=ActivityTemplateConfig_1`。两项玩法的 `_on=false`、`_config=null`、`_start={}`。开放记录缓存的同组五个玩法中仅有 `merge2`，原始字段为 `round=77, start_time=1794816000, end_time=1796023799, status=1`。同一天按包内默认计算，Wonders 会落在第 104 轮、仅开到 11/23。因此 AutoP 选中默认表的名字，也可以同时存在独立下发的开场窗口。账号本地五个玩法的 `st`、`et` 都为 0，Wonders 的服务器排期也不能等同于该账号已进入活动。

包内模板把 Joy、Fantasy、Wonders、Adventure 和 Feed 放在同组 `group=11`。客户端的同组选取路径会检查开关、解锁与候选开放窗口。12 月以后本文只推演默认窗口，逐期主题和服务器覆盖留待新样本确认。

## 证据入口

- 包内表位于 [[02-PROJECTS/产品分析/PiggyKingdom/资源路径索引#Merge 系列活动清单（2026-11-19）|Merge 系列证据路径]] 的默认配置目录。算法关键地址为 `0x2CD0AAC–0x2CD0AE8`（周期和轮次计算）与 `0x2CD0B24–0x2CD0BFC`（平移开始与结束时间）。同组选取入口是 `ActivityMngr.EnumValidActivityInGroup`（`0x31B3404`）。
- 模拟器来源为 `06-PRODUCT-ASSETS/PiggyKingdom/2.7.3/05-Runtime/20261118-merge/decoded/` 下的 `M3.M3AutoPInfo_FIXK.json`、`M3.M3SystemOpenInfo_FIXK.json`、`ActivityUserInfo_FIXK.json`。样本为 2026-11-18 20:07:37（UTC+8）同批逐文件读取，非原子抓包。开放记录的原件 SHA-256 为 `a1e4df4813261ba199416849f61f643226e8aaa0a84817f34bcc4f5ce91fff39`。
- 11/19 复采时「产品分析」实例未在线，MuMu 后台启动返回 `-503 mainnx connect failed`，因此服务器侧结论停在 11/18 已留存的缓存。
