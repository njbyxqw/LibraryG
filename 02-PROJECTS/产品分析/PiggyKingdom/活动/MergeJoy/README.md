---
title: Piggy Kingdom Merge Joy 功能档案
date: 2026-11-24
type: index
status: current
lifecycle: current
tags: [产品分析, PiggyKingdom, MergeJoy, 交接]
---

# Merge Joy 参考入口

本档案供TS需求对话及后续拆解复用。代码样本为Android 2.7.3／203原包；资源包括既有缓存和2026-11-24官方静态下载，不能把所有素材说成随原包发布。未执行游戏操作或TS实现。

| 入口 | 用途 |
|---|---|
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/数值配置参考-2.7.3\|数值配置参考与Docs同步稿]] | 按字段列发射口供应、两版棋盘数量与逐格配置、12级主链、奖励链、首次礼包、两版BP及预算；保留原始ID、奖励类型与输入SHA256。TS参考资料目录已有数值一致的阅读副本。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/逻辑与配置-2.7.3\|详细逻辑与配置]] | 投放、四向解覆盖、主链、奖励链、BP、终奖留场和退出结算；有方法token／IL偏移及未知边界 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/详细内容与配置参考-2.7.3\|完整数值表]] | 既有主链、直接礼包、两版BP完整奖励与棋盘逐格表，配合主档新增证据阅读 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/数值分层与选表-2.7.3\|合成链、BP与配置分层分析]] | 按发射口、棋盘预置、奖励来源拆分：39件主链＋5件奖励链预置；12级主链、两条5级奖励链、5档进度礼包、两版10档BP。主玩法2套表的升级与奖励相同，预置等值1501／1309；人群阈值未确认。 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/完成到期与结算-2.7.3\|完成与结算专题]] | 最后机会精确条件、BP补领过滤及空列表、暂存与固定1拳套补偿、解锁统计和TS定稿依据 |
| [资源图册](资源图册-2.7.3.html) | 音乐28／秋季29主链、覆盖、场景、UI、入口、通用奖励链与BP，原始资源拼排，非实拍 |
| [[02-PROJECTS/产品分析/PiggyKingdom/活动/MergeJoy/尺寸与界面说明-2.7.3\|秋日界面复刻与尺寸]] | 图册新增区域点击说明、原始实拍对照、Play／气泡状态及尺寸开关；原图px与Prefab UI单位分别列出 |
| [273张Sprite ZIP](assets/package-reference/reference-sprites.zip) | 按Bundle＋path ID保留重名资源，可逐张查看；约12MB |
| [来源清单](assets/package-reference/source-manifest.json) | 15输入Bundle、下载时间、对象ID、完整本地SHA256与清单31位MD5前缀校验 |
| [代码证据](assets/package-reference/code-evidence-index.json) | 本轮降级工具、同构建DLL身份、核心方法、关卡奖励链与浮点常量复算 |
| [配置对照](assets/package-reference/configuration-reference.json) | 原包28场景与缓存30场景；物品、奖励、棋盘等完全相同，仅新增52／53轮映射 |
| [Prefab引用](assets/package-reference/prefab-reference.json) | 主／帮助／结束、BP3／9和场景前后景等15根、247节点及组件 |
| [既有用户实拍](assets/20261123-user-screenshots/provenance.json) | 六图原件，拍摄版本和期号未知 |

图册已改为**单文件HTML（约3.08MB）**：51张唯一图片压缩后内嵌并复用，样式和交互也内嵌。单独复制HTML即可离线查看复刻、原始实拍对照、尺寸与全部资源图；PNG素材ZIP、Markdown正文和来源JSON仍为独立附件。网页图片保留原分辨率与透明度，主要采用WebP质量88压缩；原始PNG及ZIP未改动。

## 另一对话先读的规则

1. 底部角标是`coins＋暂存件数`，暂存后进先出优先；暂存为空才花1资源生成主链Lv.1，满盘不扣。
2. 10000全覆盖靠合成目标格的四向邻接一次解除；11000半覆盖要拖同级棋子入格二合。两层不由一次邻接事件连破。
3. 默认一张6×8盘面、一条12级主链，无8阶段或Fantasy式纵向移盘。主题表是跨轮内容。
4. Lv.7以上每次合成都产`itemRewards`，放不下进暂存；主链直接等级奖只给首次解锁。Lv.12另有逐点排11件的静态分支，尚缺操作差分，勿直接据此预算TS产出。
5. BP按Lv.2～11解锁推进10档，不消耗目标棋子；已达标后购买可领付费轨。结束自动补领过滤Joy活动资源。
6. 领终奖后留盘、隐藏Play；真正退出只补可视盘面顶层可兑现奖励物，不补暂存或自动合低级物。终奖已领且coins>0时固定换1个拳头，非按余额逐个换。

## 实现顺序建议

以下是另一对话使用研究的顺序，不代表TS方案已获确认：

- Step1：读逻辑第4、5节，先定TS资源模型、底部入口、两层覆盖和棋盘尺寸，区分竞品事实与TS取舍。
- Step2：对照第6、7节与主链／奖励链图，确定等级、首次／重复奖励、BP和总经济预算；暂不依赖未实测的Lv.12额外分支。
- Step3：按第8节决定TS终奖留场、到期、补领及余资源处理，明确暂存和异常防重的验收。
- Step4：用图册和Prefab索引排UI与成套主题，回填原需求的受影响项，再制定程序实现与验收；本任务不直接改TS需求取舍。

## 验证边界

本轮REA连接关闭，改用本机PEReader／已有Obfuz静态恢复、Capstone和UnityPy，均取得实际解析产物，无新增REA ID。代码地址属原包ARMv7；11/24设备ARM64仅用于外部配置采样。未实购、未做当前开放期选择与连续游戏差分，未验证崩溃中断防重。报告附件未commit／push，未声称跨设备已同步。

## 关联

- [[02-PROJECTS/产品分析/PiggyKingdom/_MOC|Piggy Kingdom产品入口]]
- [[02-PROJECTS/TileScape/游戏逻辑/需求-MergeJoy参考下的二合功能修改|TS需求对话对应文档]]
