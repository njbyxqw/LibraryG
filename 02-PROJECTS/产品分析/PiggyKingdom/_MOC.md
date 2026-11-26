---
title: Piggy Kingdom 产品分析 MOC
date: 2026-11-18
type: index
status: current
lifecycle: current
aliases: [Piggy Kingdom MOC, Piggy产品分析]
tags: [产品分析, PiggyKingdom, MOC]
---

# Piggy Kingdom 产品分析

Joy定稿专项：[[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/完成到期与结算-2.7.3|完成、到期与结算]]，区分终奖留场、最后机会、BP补领过滤、棋盘奖励、暂存和固定余量补偿。

2.7.3 / 203：有限步数交换三消驱动区域建造；卡册、团队、排行与多类旁线和运营系统。当前样本走通首次启动、首关、首次建造及五个底部页签，中后期活动主要为包内库存。

| 入口 | 内容与状态 |
|---|---|
| [[02-PROJECTS/产品分析/PiggyKingdom/产品框架-2.7.3\|产品框架 2.7.3]] | 核心循环、首页和五页签、系统库存、经济与商业化、后续调研问题及来源边界 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/RescueMission/开启前计数-2.7.3\|Rescue Mission未开启计数]] | 未开启不接收任务事件；新轮归零并重建任务，已后台开启但未点入口可以累计。原包ARMv7静态核对。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/代码框架/活动配置与资源加载-2.7.3\|活动下发、缓存与跳关验证]] | 已取得实时成功响应：Joy关闭／Wonders开启。80→106后自动下载并进入Wonders棋盘；个人轮次105对位本地排期优先，窗口缓存77未等同实际场次。真机差异的服务端选择原因待证。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/PiggyPass/到期结算与弹窗-2.7.3\|Piggy Pass 到期弹窗]] | 未开启／零参与／免费或已购未领的数量与顺序；三种窗口原始资源拼图。代码及缓存资源已核，连续曝光待验证。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/Merge系列活动与历史清单\|Merge 系列活动与历史清单]] | 五个玩法入口、同玩法的换主题轮次及 2024–2026 年公开记录 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy与MergeFantasy-活动排期\|Merge Joy 与 Merge Fantasy 活动排期]] | 默认四周循环与 11/18 服务器缓存对照，含近期开场候选时间 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy与MergeFantasy-界面对照\|Merge Joy 与 Merge Fantasy 界面对照]] | Joy 舞台弹窗与 Fantasy 全屏农场的主界面实拍，含通行证与帮助对照 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/README\|Merge Joy资源与逻辑入口]] | 11/24取得音乐28／秋季29主题与273张Sprite；图册新增秋日界面复刻、区域说明、原图px与UI尺寸；投放、覆盖、通关倍率、BP与固定1拳头结算已静态核对。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/逻辑与配置-2.7.3\|Merge Joy规则与配置]] | 2.7.3方法体、配置和秋季六图；补齐暂存LIFO、首次／重复发奖、终奖留盘、BP资源过滤、余币固定1拳头；保留末级操作等实测缺口。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/详细内容与配置参考-2.7.3\|Merge Joy详细配置参考]] | 12级主链、两条5级奖励链、5个进度礼包、两版10档BP、6×8初始盘；资源来源、底部切换、Joy／Fantasy差异及结算边界。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/数值配置参考-2.7.3\|Merge Joy数值配置参考与Docs同步稿]] | 按配置字段与来源整理完整数值：投放、39＋5件预置、逐格棋盘、合成产物、首次礼包和两版BP；附输入SHA256，已同步到TS对应参考资料目录，未指定为TS正式配置。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/数值分层与选表-2.7.3\|Merge Joy合成链、BP与配置分层分析]] | 按发射口／39件主链与5件奖励链预置／其他奖励拆分数值，含12级主链、5档礼包及两版10档BP；主玩法2套表仅预置不同，BP2套表付费奖励不同。AP独立且开轮锁表，人群分层条件未确认。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeFantasy/README\|Merge Fantasy 功能档案]] | 活动规则、配置、证据与验证入口。2.7.3 样本开关关闭，实际开放期玩法待采样。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/PiggyKingdom_Framework_2.7.3.html\|图文阅读版]] | 10张实机配图内嵌，可独立打开，点击截图放大 |
| [[02-PROJECTS/产品分析/PiggyKingdom/资源路径索引\|资源与证据索引]] | 原包、解包、类型结构、运行截图和报告附件来源 |

## 当前边界

- 当前人工样本（11/25，跳53）：用户要求40→53，仅改UserInfo.level；启动可见53，保存回读53／金币5106／体力5／建造0。未点击启动赠礼、未填昵称或进入53关。[[02-PROJECTS/产品分析/PiggyKingdom/资源路径索引#当前样本：Level 53（2026-11-25，用户授权跳关）|53关备份与验证]]；下列40／106等均为历史样本。

- 历史人工样本（11/25，跳40）：实际起点为2关，仅改UserInfo.level为40；两次冷启动可见40，保存回读通过。游戏启动赠礼令金币1106→2106，昵称未填；第二次启动仍显示赠礼提示。[[02-PROJECTS/产品分析/PiggyKingdom/资源路径索引#历史样本：Level 40（2026-11-25，用户授权跳关）|备份、补丁与回读证据]]。下列106／80／200关均为历史样本。

- 首轮实机（11/18）：下一关Level 2；Castle建造1/8；Teams预告36关、Albums预告43关、小鸟形象入口预告57关；Shop已观察，未购买。
- 历史人工样本（11/24，重装后）：2.7.3／203 ARM64，主APK及资源分包与既有XAPK一致。先4→80，后按用户授权仅改80→106；106冷启动及保存回读通过，金币3206／体力5／建造2未人工调整。第二次106启动后已进入Wonders棋盘，尚未自然通关主线106。80关初次1206金币与昵称引导、11/20重装前200关均保留为历史，不当自然成长样本。[[02-PROJECTS/产品分析/PiggyKingdom/资源路径索引#人工关卡样本与回退|备份、字段与验证证据]]。
- 静态：53个非none活动／系统枚举，47个首页入口Prefab。均不等于当前开放活动数量。
- 配置与代码：框架初扫时只取得密文和Cpp2IL签名；Merge专题已解密33份相关配置并恢复同构建Hot.Scripts.dll，以CIL及受限算术VM模拟核对关键分支。此进展不等于其余活动均已完成消费者核验。
- 11/18 模拟器样本的 Merge Joy 与 Merge Fantasy 均关闭。同组服务器缓存有 Merge Wonders 77，11/16 16:00 至 11/30 15:29:59（UTC+8）。本地 Fantasy 的 scene1 与 MergeAniConfig 为初始化／回退值。
- 11/24实时验证：80关收到成功AutoP分段正文与终段，Joy=false、Wonders=true／106关和活跃天数1；106刷新后缓存仍相同，Wonders资源自动下载，第二次启动个人场次为105而服务器窗口缓存77。存在排期表先取的消费者分支；已有Joy ver64新主题表也不等于Joy被选中。真机对照版本／匹配账号尚缺，未确认AB分组或模拟器拦截。
- 后续优先核对功能开放顺序和活动对关卡回调的消费，再展开区域成本、旁线承接及商业化压力点。

## 关联

- [[02-PROJECTS/产品分析/_MOC|产品分析总入口]]
- [[02-PROJECTS/产品分析/方法-竞品模块分析与持续维护|竞品模块分析方法]]
