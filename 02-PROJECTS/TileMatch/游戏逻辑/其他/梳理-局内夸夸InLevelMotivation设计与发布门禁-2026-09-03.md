---
title: 局内夸夸 InLevelMotivation 设计与发布门禁
date: 2026-09-03
type: analysis
status: current
project: TileMatch
lifecycle: current
verification: "静态读取源码旁 Markdown；未核对当前代码实现、资源、Unity 场景或真机表现。"
priority: medium
cat_order: 150
tags: [TileMatch, TileV2, InLevelMotivation, 游戏逻辑, 发布门禁]
source: "/Users/dean/Downloads/meatloaf_client/client/Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Module/InLevelMotivation/in_level_motivation_cto_v3_design.md；in_level_motivation_implementation_status.md；in_level_motivation_final_design.md"
---

# 局内夸夸 InLevelMotivation 设计与发布门禁

> 本文只整理 MT 源码旁文档中的可追溯结论，作为后续查找、复现或迁移入口。它不是当前代码审计结果；实际实现以当前分支源码和 Unity 验证为准。

## 已确认文档状态

| 文档 | 状态 | 结论 |
|---|---|---|
| `in_level_motivation_cto_v3_design.md` | 当前唯一实现和验收基线 | V3 替代 V2 与 `final_design`，核心策略是复用现有异步结算权威点，Motivation 只消费事实，不接管棋盘事务。 |
| `in_level_motivation_final_design.md` | deprecated | 2026-07-20 已废弃，仅保留为历史决策记录；同步 ClickSettlement 和 44-byte Record Section 等设计不得继续采用。 |
| `in_level_motivation_implementation_status.md` | 实现状态记录 | 截至 2026-07-21，领域规则、旧流程接入、回放/重连协议和 GameView 表现链已落地；完整场景、回放/重连和真机性能仍需验收。 |

## V3 设计要点

| 范围 | 结论 |
|---|---|
| 业务边界 | `BarMatchAction` 是 Match 类反馈权威点；玩家根 `AddToBarAction` 同步尾部是 Reveal 类反馈权威点；Challenge/Perfect 复用既有 `SolutionHintService` 与 DarkTarget 事实。 |
| 不接管内容 | 不修改公共事件和 `ActionExecutionUnit` 语义，不新增棋盘事务，不复制 Deadlock 状态，不建立第二套 Solver 或 ECA。 |
| Challenge | 只跟随旧 DeadlockHint 的真实 Session 进入和正确暗牌目标消费；不因空位等于 3 本身播放。 |
| Replay / Reconnect | 重建逻辑状态和 DecisionSequence，但不播放表现、音效或重复正常 BI。 |
| FullBar / Combo | FullBar 使用当前 `Bar.CurrentCapacity`；FullBar 压制 Combo 时保留 Pending，后续补发最高档。 |
| Reveal | AHA / Thumb 只对 Player / ReplayPlayer 的根 Add 判定，AHA 压制 Thumb；判断使用逻辑未匹配手牌数和 Reservation，而不是等待 View 销毁。 |

## 发布门禁

| 门禁 | 当前状态 |
|---|---|
| 配置源 | 正式 `GlobalConstCfg` 字段和 ConfigOverride 数据仍需补齐；生成文件不能手改替代。 |
| 资源 / 文案 | Prefab 文案仍为英文贴图；若正式版本需要多语言，需补语言资源或改成本地化文本方案。 |
| 音效 | WAV 与 SoundConst 不等于可播放；正式 SoundCfg 条目仍需补齐。 |
| 场景表现 | 七个 Prefab、独立 View、目标牌 / Bar fallback 已接入；仍需实际分辨率下确认位置、层级和遮挡。 |
| 回放 / 重连 | Record v7 写入与读取需要按版本级单向迁移验收；`StartLv <= 0` 不能当协议回退开关。 |
| 性能 | 需在最大盘面记录 Reveal 与 DeadlockHint 路径耗时和 GC，对照功能关闭基线。 |

## 验证边界

- 已读：三份源码旁 Markdown 的设计状态、V3 产品口径、实现状态与发布门禁。
- 未验证：当前分支源码是否完全等于文档、Unity Editor 测试、真机性能、资源导入、SoundCfg、ConfigOverride 和线上实验配置。
- 使用要求：复用本结论前必须重新核对 MT 当前代码；迁移到 TS 前必须建立 MT / TS 对位文件表。

## 关联

- [[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]]
- [[02-PROJECTS/TileMatch/参考/同步-项目AI记忆与源码旁文档-2026-09-03|项目 AI 记忆与源码旁文档同步]]
- [[02-PROJECTS/TileMatch/参考/MT老项目路径索引|MT 老项目路径索引]]
- [[02-PROJECTS/Agent/工作流/规范-多项目工作流与复现|多项目工作流与复现]]
