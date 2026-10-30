---
title: Royal Match 活动逐项拆解 MOC
date: 2026-10-26
type: index
status: current
tags: [产品分析, RoyalMatch, 活动, MOC]
---

# Royal Match 活动逐项拆解

以 [[02-PROJECTS/产品分析/Royal Match/活动清单与简述-38911|38911 活动清单]] 为总范围。每个活动采用独立文件夹，按实际证据逐项推进，不提前为尚未分析的活动生成空文档。现有跨活动历史文档保留。

跨活动当前期限、未来开始字段与礼包/AB库存统一见 [[02-PROJECTS/产品分析/Royal Match/运营配置/排期与配置总览|运营配置总览]]；这里只作路由，不将配置库存提升为每个模块均已深度验证。

## 已建立独立档案

| 活动 | 入口 | 本轮进度 | 尚未完成 |
|---|---|---|---|
| Lava Quest | [[02-PROJECTS/产品分析/Royal Match/活动/Lava Quest/README|Lava Quest 详细拆解]] | 39781重验双期限、跨截止保留条件、清理例外和下一期准入；第五章已重整，含流程图 | 跨截止实际游玩/恢复响应、星期排期、服务端场景选择、库存到账 |
| Book of Treasure（Madness子类型） | [[02-PROJECTS/产品分析/Royal Match/活动/Book of Treasure/逻辑与配置-38911|数值与分层配置]] | 设备-1实读2203版两套25阶段；原生核验超级光球解锁分层、当前阶段档位保存及奖励覆盖；版本补取、前移48小时对照 | 全服分群、具体SLB组、完整奖励覆盖、真实跨期响应；39781未重验 |

## 其余中央活动队列

以下中央活动保留整体队列；Madness的Book子类型已单独建立上述档案，其余主题仍按现有覆盖状态推进，分组不代表固定优先级。

| 类别 | 活动 |
|---|---|
| 长期进度、通行证、通用 | League、Royal Pass、Weekly Pass、Madness、Super Booster、Invite Friends |
| 个人/团队竞争 | Kings Cup、Team Battle、Sky Race、Archery Arena、Team Tournament、Daily Lightning Rush、Propeller Rush、Robot Rivals、Clash of Champions、Royal World Cup |
| 连胜/阶段/短周期 | Pinata Party、Space Mission、Balloon Rise、Magic Cauldron、Dragon Nest、Duke's Fortune、Duke's Treats |
| 支线与独立玩法 | Hidden Temple、Train Journey、Ocean Odyssey、Puzzle Break、Ancient Adventure、Merge Smith、Short Expedition |
| 协作与商业化覆盖 | Team Treasure、Ladder Offer、Team Offer、Journey Offer、Starfall Offer |

Ancient Adventure 在 [[02-PROJECTS/产品分析/Royal Match/活动定位-Lava Quest与Ancient Adventure-38911#三、Ancient Adventure|既有主章节]] 持续维护：39781重验服务器期限、用户期失效及下一期准入；319→321配置正文一致、314→315截止约差24小时，3.2已重整。阶段连胜、防重复领奖、教程种子与洗牌主体仍按38911证据标注。剩余重点是服务端日历、跨期实际结算、教程池和奖励覆盖。队列表示尚未建立独立文件夹，不表示Ancient未分析；未另开重复主文档。

## 每个活动的交付结构

机制与配置主文档按主题持续修订：新证据先判断应补充、替换还是重排已有章节，合并重复内容并同步纠正旧结论。不因每次深挖新增文档或尾部章节；调查过程留 Daily/原始证据。仅当出现独立且稳定的专题边界时拆分文档。

1. `README.md`：玩家规则、核心判断、证据层级、当前结论与后续入口。
2. `逻辑与配置-<版本>.md`：资格、进入、状态流、关卡回调、配置/覆盖、数值、奖励、存储、异常与边界。
3. `资源与表现-<版本>.md`：Bundle → Prefab → 组件/字段 → 图片/动效/音效 → 场景触发；保留 path ID 和未对位项。
4. `证据与验证-<日期>.md`：样本身份、采集来源、文件哈希、已验证与未验证、复现方法。

大文件和原始证据放 `06-PRODUCT-ASSETS/RoyalMatch/<版本>/05-Runtime/<采集批次>/`。每个结论区分官方规则、历史静态、现场读取、资源序列化、推导和未知；不得把“缓存存在”升级为“现在生效”。

## 关联

- [[02-PROJECTS/产品分析/Royal Match/_MOC|Royal Match 产品 MOC]]
- [[02-PROJECTS/产品分析/方法-竞品模块分析与持续维护|模块分析与持续维护方法]]

- [[02-PROJECTS/产品分析/_MOC|产品分析 MOC]]
- [[02-PROJECTS/产品分析/Royal Match/活动清单与简述-38911|活动总清单]]
- [[02-PROJECTS/产品分析/Royal Match/资源路径索引|资源路径索引]]
