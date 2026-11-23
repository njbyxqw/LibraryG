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

2.7.3 / 203：有限步数交换三消驱动区域建造；卡册、团队、排行与多类旁线和运营系统。当前样本走通首次启动、首关、首次建造及五个底部页签，中后期活动主要为包内库存。

| 入口 | 内容与状态 |
|---|---|
| [[02-PROJECTS/产品分析/PiggyKingdom/产品框架-2.7.3|产品框架 2.7.3]] | 核心循环、首页和五页签、系统库存、经济与商业化、后续调研问题及来源边界 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/PiggyPass/到期结算与弹窗-2.7.3\|Piggy Pass 到期弹窗]] | 未开启／零参与／免费或已购未领的数量与顺序；三种窗口原始资源拼图。代码及缓存资源已核，连续曝光待验证。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/Merge系列活动与历史清单\|Merge 系列活动与历史清单]] | 五个玩法入口、同玩法的换主题轮次及 2024–2026 年公开记录 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy与MergeFantasy-活动排期\|Merge Joy 与 Merge Fantasy 活动排期]] | 默认四周循环与 11/18 服务器缓存对照，含近期开场候选时间 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy与MergeFantasy-界面对照\|Merge Joy 与 Merge Fantasy 界面对照]] | Joy 舞台弹窗与 Fantasy 全屏农场的主界面实拍，含通行证与帮助对照 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeFantasy/README|Merge Fantasy 功能档案]] | 活动规则、配置、证据与验证入口。2.7.3 样本开关关闭，实际开放期玩法待采样。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/PiggyKingdom_Framework_2.7.3.html|图文阅读版]] | 10张实机配图内嵌，可独立打开，点击截图放大 |
| [[02-PROJECTS/产品分析/PiggyKingdom/资源路径索引|资源与证据索引]] | 原包、解包、类型结构、运行截图和报告附件来源 |

## 当前边界

- 首轮实机（11/18）：下一关Level 2；Castle建造1/8；Teams预告36关、Albums预告43关、小鸟形象入口预告57关；Shop已观察，未购买。
- 当前人工样本（11/20）：实测从 Level 3 调整至 Level 200，两次冷启动显示及保存回读通过，金币／体力／建造值未人工调整。停在条款与昵称引导，尚未进入第 200 关对局或验证活动开放；不能当作自然成长样本。[[02-PROJECTS/产品分析/PiggyKingdom/资源路径索引#人工关卡样本与回退（2026-11-20）|备份、字段与验证证据]]。
- 静态：53个非none活动／系统枚举，47个首页入口Prefab。均不等于当前开放活动数量。
- 配置与代码：框架初扫时只取得密文和Cpp2IL签名；Merge专题已解密33份相关配置并恢复同构建Hot.Scripts.dll，以CIL及受限算术VM模拟核对关键分支。此进展不等于其余活动均已完成消费者核验。
- 11/18 模拟器样本的 Merge Joy 与 Merge Fantasy 均关闭。同组服务器缓存有 Merge Wonders 77，11/16 16:00 至 11/30 15:29:59（UTC+8）。本地 Fantasy 的 scene1 与 MergeAniConfig 为初始化／回退值。
- 后续优先核对功能开放顺序和活动对关卡回调的消费，再展开区域成本、旁线承接及商业化压力点。

## 关联

- [[02-PROJECTS/产品分析/_MOC|产品分析总入口]]
- [[02-PROJECTS/产品分析/方法-竞品模块分析与持续维护|竞品模块分析方法]]
