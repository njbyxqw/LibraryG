---
title: Tile Family（TF）产品分析 MOC
date: 2026-11-04
type: index
status: current
aliases: [TF, TileFamily, TF产品分析]
tags: [产品分析, TileFamily, MOC]
---

# Tile Family（TF）产品分析

用户于 2026-11-04 指定后续简称 **TF**。本档参考 RM 的系统与主场景框架、MV 的活动家族组织方法，TF 事实独立取证。

| 需求 | 文档 |
|---|---|
| 系统地图、主线与活动回流、与 RM/MV 对照 | [[02-PROJECTS/产品分析/Tile Family/系统框架与关键流程-2.12.0]] |
| 活动家族、37 个具体实现与下钻入口 | [[02-PROJECTS/产品分析/Tile Family/活动系统与清单-2.12.0]] |
| 活动解锁、排期、奖励与弹窗参数 | [[02-PROJECTS/产品分析/Tile Family/活动解锁排期与奖励配置-2.12.0]] |
| Rescue Mission／七日任务未开启计数 | [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/Rescue Mission与七日任务-开启前计数-2.12.0]]：通关只在ACTIVE累计，新建进度0；未点入口与整期未开启区分 |
| Jungle Quest／Treasure Quest：10000奖池、7步人数公式、参赛分段、R组调控与机器人 | [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/Jungle Quest与Treasure Quest-奖励调控与分组-2.12.0]] |
| 两种Quest关卡消耗：库存／免费／广告计分、复活扣款区别与奖金阶梯 | [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/Jungle Quest与Treasure Quest-关卡消耗口径与奖励影响-2.12.0]] |
| 广告总体策略、用户分层、插屏/RV、去广告及价格分配 | [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/广告策略与分配配置-2.12.0]] · [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/TileFamily_Ads_Strategy_2.12.0.html|HTML阅读版]] |
| Prop Favor道具礼包：五类20个候选、奖励全表、近期付费中位数选档、30关资格与局内触发 | [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/Prop Favor-道具礼包奖励定价与触发-2.12.0|详细正文]] · [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/TileFamily_Prop_Favor_2.12.0.html|HTML阅读版]] |
| 金币六档、道具金币与美元系数、DDA权重、20个Prop Favor及商城礼包对照 | [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/经济换算-金币道具与美元系数-2.12.0|换算分析]] · [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/TileFamily_Economy_Conversion_2.12.0.html|HTML阅读版]] |
| 通关结算激励视频：出现条件、300金币、分组与每日上限 | [[02-PROJECTS/产品分析/Tile Family/游戏逻辑/通关结算激励视频-2.12.0]] |
| 样本、工具、代码地址、运行快照与边界 | [[02-PROJECTS/产品分析/Tile Family/资源路径索引]] |

当前覆盖：2.12.0 / 21200 包体、Lua规则、关键ARM64调用、同版本MuMu缓存与部分结算实拍。125份配置密文已解码并完成重加密校验，已补副本解锁、排期、奖励与弹窗参数。广告专题已核U组/独立AB通道、U2付费召回的10天及库存门槛与购买重置、插屏节奏、设备/IAP拦截、RV双信号发奖和业务日界、509暂存区搬牌，以及MAX主备反馈/中价保存/失败重试；当前账号最终配置、广告实验权重、OrderMerge能量到账与重置、实际收益仍未知。主文档及本地HTML同步维护，后续按主题修订，不按轮次续尾。

上级：[[02-PROJECTS/产品分析/_MOC]]。

Prop Favor专题（2026-11-18）：沿用2.12.0及11月4日初始配置，已核5种定向礼包各4档（配置美元7.99/12.99/19.99/39.99）、完整奖励与59个相关SKU目录、Lua路由与3|20|50|0选价、页内Banner资格、附奖跳过和买后库存刷新；未采当前账号、未实购。图标及精简配置证据随报告保存，HTML为图片内嵌单文件；静态内容检查通过，浏览器视觉验收未完成。
