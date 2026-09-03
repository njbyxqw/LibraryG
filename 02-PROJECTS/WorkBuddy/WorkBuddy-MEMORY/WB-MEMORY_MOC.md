---
title: WorkBuddy-MEMORY MOC
date: 2026-07-08
type: moc
status: active
tags: [WorkBuddy, MEMORY, MOC]
---

# WorkBuddy MEMORY 归档

> 本目录存放 WorkBuddy AI 的 MEMORY 蒸馏存档。
> 每次 MEMORY 超限清理时，原始全文和蒸馏记录在此归档，供历史回溯。

## 文件结构

| 文件 | 内容 | 模式 |
|---|---|---|
| [[MEMORY-蒸馏日志]] | 每次蒸馏/清理记录（事件+原因+变化） | append-only |
| [[MEMORY-项目级-原始存档（append）]] | 项目级 MEMORY 每次蒸馏前完整原文 | append-only |
| [[MEMORY-用户级-原始存档（append）]] | 用户级 MEMORY 每次蒸馏前完整原文 | append-only |

## 架构设计

| 文件 | 内容 | 状态 |
|---|---|---|
| [[设计-WorkBuddy-Agent-知识库体系架构策略\|架构策略]] | 工作流-Agent-知识库体系 5 维策略 | draft |

## 索引闭环

AI 查项目资料流程：
1. 读取 `meatloaf_client01\.workbuddy\memory\MEMORY.md` → 核心规则 + 速查链接
2. 速查指向 Obsidian `[[_MOC]]` 或 `[[知识库文档顺序索引]]`
3. 需要深度内容时用 `mcp__obsidian-mcp__search_vault` 或 `Grep` 搜索 vault
4. 蒸馏历史回溯 → 本目录原始存档
