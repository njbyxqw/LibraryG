---
title: Agent 工作流 MOC
date: 2026-09-03
type: index
status: finalized
lifecycle: current
priority: high
tags: [LibraryG, Agent, 工作流, MOC]
source: "2026-09-03 用户确认的知识归属与 MOC 路由规则；由任务包执行建立"
---

# Agent 工作流 MOC

> LG 的工作流、维护规范与 MOC / INBOX / Daily / 多项目复现的入口。规范和当前流程以 `current` 为准，报告仅作追溯，历史同步与 WorkBuddy 自动化方案不作为默认流程。

---

## 路由表

### 规范与当前入口（current）

| 需求 | 入口 |
|---|---|
| 任务产出与入库 | [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]] |
| 本机 TS / MT 执行与 LG 桥接 | [[02-PROJECTS/Agent/工作流/规范-本机项目执行与LG知识库桥接|本机项目执行与 LG 知识库桥接规范]] |
| MOC / 导航层级 | [[02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级|MOC 命名与导航层级规范]] |
| INBOX 整理 | [[02-PROJECTS/Agent/工作流/INBOX对话工作区工作流|INBOX 对话工作区工作流]] |
| Daily / 日志同步 | [[02-PROJECTS/Agent/工作流/工作内容日志同步规范|工作内容日志同步规范]] |
| 跨项目复现 | [[02-PROJECTS/Agent/工作流/规范-多项目工作流与复现|多项目工作流与复现规范]] |
| 知识沉淀闭环 / 自动巡检 | [[02-PROJECTS/Agent/工作流/规范-任务知识沉淀闭环与自动巡检|任务知识沉淀闭环与自动巡检]] |
| AI 协作注意事项 | [[02-PROJECTS/Agent/工作流/规范-AI协作注意事项|AI 协作注意事项]] |

### 协作草案（draft / needs-review）

| 需求 | 入口 | 状态 |
|---|---|---|
| Chat、LG 与本地执行的日常分工 | [[02-PROJECTS/Agent/工作流/指南-LGChat与本地执行协作|LG、Chat 与本地执行协作实用指南]] | draft |
| Chat → 本地核实 → Codex → LG 的执行边界 | [[02-PROJECTS/Agent/工作流/协议-LGChat与本地执行协作|LG、Chat 与本地执行协作协议]] | needs-review |

### 报告与计划（report / plan）

| 需求 | 入口 | 状态 |
|---|---|---|
| LG Git 化评估 | [[02-PROJECTS/Agent/工作流/评估-LibraryG知识库Git化现状与使用规范-2026-09-03|LibraryG Git 化现状与使用规范]] | report |
| LG 结构与 AI 读取稳定性 | [[02-PROJECTS/Agent/工作流/评估-LibraryG结构与AI读取稳定性-2026-08-10|LibraryG 结构与 AI 读取稳定性评估]] | report |
| 多项目协同阶段复盘 | [[02-PROJECTS/Agent/工作流/评估-多项目工作空间协同阶段复盘-2026-08-26|多项目工作空间协同阶段复盘]] | report |
| 初始工作空间评估 | [[02-PROJECTS/Agent/工作流/评估-工作空间与工作流程现状-2026-08-05|工作空间与工作流程现状评估]] | report |
| Obsidian 链接完整性审计 | [[02-PROJECTS/Agent/工作流/报告-Obsidian链接完整性审计-2026-08-10|Obsidian 链接完整性审计报告]] | report |
| 内容归属与任务产出审查 | [[02-PROJECTS/Agent/工作流/审查-知识库内容与任务产出流程-2026-09-03|知识库内容与任务产出流程审查]] | report |
| 维护降噪 / Obsidian 深化 | [[02-PROJECTS/Agent/工作流/计划-知识库维护降噪与Obsidian深化-2026-08-26|知识库维护降噪与 Obsidian 深化计划]] | plan |
| 近期任务逐项归档与全量巡检 | [[02-PROJECTS/Agent/工作流/计划-近期任务归档全量巡检-2026-09-07|近期任务归档全量巡检计划]] | scheduled，执行结果以计划勾选项及报告为准 |

### 实施任务包（implementation-task）

| 任务包 | 入口 | 状态 |
|---|---|---|
| 知识库内容归属与 MOC 路由整理 | [[02-PROJECTS/Agent/工作流/任务包-知识库内容归属与MOC路由整理-2026-09-03|知识库内容归属与 MOC 路由整理任务包]] | completed（已执行 / 已验收） |

### 历史与休眠（historical / dormant）

| 方案 | 入口 | 状态 |
|---|---|---|
| WorkBuddy 日志知识闭环自动化 | [[02-PROJECTS/Agent/工作流/方案-WorkBuddy日志知识闭环自动化实施|WorkBuddy 日志知识闭环自动化实施方案]] | dormant |
| DailyLogs 同步流程（旧 Windows / WorkBuddy） | [[02-PROJECTS/Agent/工作流/DailyLogs同步流程|DailyLogs 同步流程]] | historical |
| 2026-07-01 知识库同步比对 | [[02-PROJECTS/Agent/工作流/知识库同步比对报告-2026-07-01|知识库同步比对报告]] | historical |

> 历史与休眠方案仅作追溯，不作为默认流程。

---

## 关联

- [[AI总MOC|AI 总 MOC]]
- [[02-PROJECTS/Agent/Memory|Agent Memory]]
- [[03-KNOWLEDGE/_MOC|通用知识 MOC]]
- [[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]]
- [[02-PROJECTS/TileScape/_MOC|TileScape MOC]]
