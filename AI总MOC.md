---
title: AI 总 MOC
date: 2026-09-03
type: index
status: finalized
lifecycle: current
priority: critical
tags: [LibraryG, AI, MOC, Obsidian, 知识库维护]
---

# AI 总 MOC

> 面向 Codex / AI 的最短稳定入口。做 LibraryG 相关任务时先读本页，再按任务进入下一级 MOC 或规范。不要默认全盘搜索。

---

## 默认必读

1. [[HOME|LibraryG 主入口]]
2. [[工作空间总纲|工作空间总纲]]
3. [[02-PROJECTS/Agent/Memory|Agent Memory]]

> 默认只读以上三项。涉及入库、MOC、跨项目、INBOX、WorkBuddy 或历史审计时，再按下方分层进入对应文档。

---

## 规则分层

| 层级 | 文档 | 何时读取 |
|---|---|---|
| Core | [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]] | 需要归档、入库、维护、沉淀稳定结论时 |
| Reference | [[02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级|MOC 命名与导航层级规范]] | 处理 MOC、链接、同名入口、导航层级时 |
| Reference | [[02-PROJECTS/Agent/工作流/规范-多项目工作流与复现|多项目工作流与复现]] | 涉及 MT / TS 对照、迁移、复现时 |
| Reference | [[02-PROJECTS/Agent/工作流/规范-多Agent任务上下文与交接|多 Agent 任务上下文与交接]] | 涉及 Task、最小 Context、Worktree、Artifact、MCP 或 Agent 交接时 |
| Reference | [[02-PROJECTS/Agent/工作流/工作内容日志同步规范|工作内容日志同步规范]] | 需要确认 Daily 详细格式时 |
| Reference | [[02-PROJECTS/Agent/工作流/规范-任务知识沉淀闭环与自动巡检|任务知识沉淀闭环与自动巡检]] | 做周期巡检、补漏审计或自动化前置检查时 |
| Reference | [[02-PROJECTS/Agent/工作流/INBOX对话工作区工作流|INBOX 对话工作区工作流]] | 整理 `00-INBOX/` 或处理临时产物时 |
| Reference | [[02-PROJECTS/Agent/工作流/规范-AI协作注意事项|AI 注意事项]] | 给只读分析型 AI 或外部 AI 任务设边界时 |
| Dormant | [[02-PROJECTS/Agent/工作流/方案-WorkBuddy日志知识闭环自动化实施|WorkBuddy 日志知识闭环自动化实施方案]] | 只有明确启用 WorkBuddy 交接时读取 |
| Historical | [[02-PROJECTS/Agent/工作流/DailyLogs同步流程|DailyLogs 同步流程]] | 追溯旧 Windows / WorkBuddy 日志同步方案时 |
| Historical | [[02-PROJECTS/Agent/工作流/知识库同步比对报告-2026-07-01|知识库同步比对报告]] | 追溯 2026-07-01 同步比对时 |
| Report | [[02-PROJECTS/Agent/工作流/报告-Obsidian链接完整性审计-2026-08-10|Obsidian 链接完整性审计报告]] | 追溯链接审计结果和历史修复依据时 |
| Report | [[02-PROJECTS/Agent/工作流/评估-工作空间与工作流程现状-2026-08-05|工作空间与工作流程现状评估]] | 追溯初始多项目工作空间判断时 |
| Report | [[02-PROJECTS/Agent/工作流/评估-LibraryG结构与AI读取稳定性-2026-08-10|LibraryG 结构与 AI 读取稳定性评估]] | 评估 LG 结构和 AI 读取稳定性时 |
| Report | [[02-PROJECTS/Agent/工作流/评估-LibraryG知识库Git化现状与使用规范-2026-09-03|LibraryG Git 化现状与使用规范]] | 评估跨设备 Git 同步边界、风险和日常流程时 |
| Report | [[02-PROJECTS/Agent/工作流/审查-知识库内容与任务产出流程-2026-09-03|知识库内容与任务产出流程审查]] | 审查内容归属、Daily、INBOX、MOC 与任务产出路径时 |
| Report | [[02-PROJECTS/Agent/工作流/评估-多项目工作空间协同阶段复盘-2026-08-26|多项目工作空间协同阶段复盘]] | 做阶段复盘或优先级重排时 |
| Plan | [[02-PROJECTS/Agent/工作流/计划-知识库维护降噪与Obsidian深化-2026-08-26|知识库维护降噪与 Obsidian 深化计划]] | 推进规则降噪和 Obsidian 深化时 |

---

## 任务路由

| 任务类型 | 入口 |
|---|---|
| LibraryG 入库 / 归档 / 维护 | [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]] |
| 在 TS / MT 执行任务、读取项目 Docs、创建个人任务档案 | [[02-PROJECTS/Agent/工作流/规范-本机项目执行与LG知识库桥接|本机项目执行与 LG 知识库桥接规范]] |
| 多 Agent 任务 / Worktree / Artifact 交接 | [[02-PROJECTS/Agent/工作流/规范-多Agent任务上下文与交接|多 Agent 任务上下文与交接规范]] |
| 可迁移 Unity / 编辑器 / 设计知识 | [[03-KNOWLEDGE/_MOC|通用知识 MOC]] |
| LG 工作流 / Daily / INBOX / MOC 维护 | [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]] |
| AI 注意事项 | [[02-PROJECTS/Agent/工作流/规范-AI协作注意事项|AI 注意事项]] |
| 任务收尾 / 自动巡检 | [[02-PROJECTS/Agent/工作流/规范-任务知识沉淀闭环与自动巡检|任务知识沉淀闭环与自动巡检]] |
| WorkBuddy 执行交接 | [[02-PROJECTS/Agent/工作流/方案-WorkBuddy日志知识闭环自动化实施|WorkBuddy 日志知识闭环自动化实施方案]] |
| MOC / 链接 / 导航问题 | [[02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级|MOC 命名与导航层级规范]] |
| LG 结构评估 | [[02-PROJECTS/Agent/工作流/评估-LibraryG结构与AI读取稳定性-2026-08-10|LibraryG 结构与 AI 读取稳定性评估]] |
| LG Git 同步评估 | [[02-PROJECTS/Agent/工作流/评估-LibraryG知识库Git化现状与使用规范-2026-09-03|LibraryG Git 化现状与使用规范]] |
| LG 内容与产出流程审查 | [[02-PROJECTS/Agent/工作流/审查-知识库内容与任务产出流程-2026-09-03|知识库内容与任务产出流程审查]] |
| 阶段复盘 / 工作空间协同评估 | [[02-PROJECTS/Agent/工作流/评估-多项目工作空间协同阶段复盘-2026-08-26|多项目工作空间协同阶段复盘]] |
| 维护降噪 / Obsidian 深化计划 | [[02-PROJECTS/Agent/工作流/计划-知识库维护降噪与Obsidian深化-2026-08-26|知识库维护降噪与 Obsidian 深化计划]] |
| Obsidian 链接审计 | [[02-PROJECTS/Agent/工作流/报告-Obsidian链接完整性审计-2026-08-10|Obsidian 链接完整性审计报告]] |
| TileMatch / MT 项目知识 | [[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]] |
| TileScape / TS 项目知识 | [[02-PROJECTS/TileScape/_MOC|TileScape MOC]] |
| 项目 AI 记忆同步 | [[02-PROJECTS/TileScape/参考/同步-项目AI记忆与Docs入口-2026-09-03|TS 项目 AI 记忆同步]] · [[02-PROJECTS/TileMatch/参考/同步-项目AI记忆与源码旁文档-2026-09-03|MT 项目 AI 记忆同步]] |
| 跨 MT / TS 复现 | [[02-PROJECTS/Agent/工作流/规范-多项目工作流与复现|多项目工作流与复现]] |
| Daily / 工作记录 | [[02-PROJECTS/Agent/工作流/工作内容日志同步规范|工作内容日志同步规范]] |
| 近期工作进度 / 待办 | [[01-DAILY/summaries/近期工作进度与待办-2026-08-20|近期工作进度与待办（08-05 至 08-25）]] |
| 近期任务归档状态 / 全量巡检 | [[01-DAILY/summaries/近期任务归档巡检-2026-09-07|09-07 巡检状态表]] · [[02-PROJECTS/Agent/工作流/计划-近期任务归档全量巡检-2026-09-07|专项计划]]（已完成首批逐任务对位，专项持续处理中） |
| INBOX 整理 | [[02-PROJECTS/Agent/工作流/INBOX对话工作区工作流|INBOX 对话工作区工作流]] |
| WorkBuddy 历史记忆 | [[02-PROJECTS/Agent/WorkBuddy-MEMORY/WB-MEMORY_MOC|WorkBuddy MEMORY 历史归档]] |

---

## 读取规则

- 先从本页和对应 MOC 逐级进入，只在定位后的目录内检索。
- 默认不把所有工作流文档都当必读；按“规则分层”触发读取。
- 遇到 `_MOC.md`、`_项目概览.md` 等同名文件，使用完整 vault 路径。
- 区分 `current`、`historical`、`deprecated`、`needs-review`，不要把旧方案或聊天推断写成正式规则。
- 形成可复用路径、代码逻辑、配置、资源、方案或稳定结论时，按入库规范更新 Daily、MOC 和必要索引；无新增事实的小任务不强行造文档。
