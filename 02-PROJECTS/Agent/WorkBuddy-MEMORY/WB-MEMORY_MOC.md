---
title: WorkBuddy-MEMORY 历史归档 MOC
date: 2026-07-08
type: moc
status: historical
tags: [WorkBuddy, MEMORY, MOC, historical]
---

# WorkBuddy MEMORY 历史归档

> 本目录存放 WorkBuddy AI 的 MEMORY 蒸馏存档。
> 每次 MEMORY 超限清理时，原始全文和蒸馏记录在此归档，供历史回溯。
> 当前通用 Agent / AI 记忆入口已迁移到 [[02-PROJECTS/Agent/Memory|Agent Memory]]；本目录不作为新的执行规则入口。

## 文件结构

| 文件 | 内容 | 模式 |
|---|---|---|
| [[MEMORY-蒸馏日志]] | 每次蒸馏/清理记录（事件+原因+变化） | append-only |
| [[MEMORY-项目级-原始存档（append）]] | 项目级 MEMORY 每次蒸馏前完整原文 | append-only |
| [[MEMORY-用户级-原始存档（append）]] | 用户级 MEMORY 每次蒸馏前完整原文 | append-only |

## 架构设计

| 文件 | 内容 | 状态 |
|---|---|---|
| [[02-PROJECTS/Agent/设计-WorkBuddy-Agent-知识库体系架构策略|架构策略]] | 工作流-Agent-知识库体系 5 维策略 | draft |

## 索引闭环

AI 查项目资料流程：
1. 读取 `AGENTS.md`、`HOME.md`、`工作空间总纲.md`、[[02-PROJECTS/Agent/Memory|Agent Memory]]
2. 按任务进入 `02-PROJECTS/TileMatch/_MOC.md` 或 `02-PROJECTS/TileScape/_MOC.md`
3. 需要深度内容时搜索 vault 或进入对应项目代码仓库
4. 需要 WorkBuddy 历史版本时，再回溯本目录原始存档
