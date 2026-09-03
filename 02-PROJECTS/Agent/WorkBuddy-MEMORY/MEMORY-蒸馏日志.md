---
title: MEMORY-蒸馏日志
date: 2026-07-08
type: log
status: active
tags: [WorkBuddy, MEMORY, 蒸馏]
---

# MEMORY 蒸馏日志（append-only）

> **规则**：每次蒸馏/清理后追加一条记录，标注时间、编号、事件、原因、精简前后变化。

---

## [2026-07-08] #001 首次蒸馏

### 背景
- 项目级 MEMORY（`meatloaf_client01\.workbuddy\memory\MEMORY.md`）约 206 行 / ~15k 字符，远超 3,000 字符限制
- 系统多次因超限截断注入，影响 AI 上下文可用性
- 用户批准方案：项目级 + 用户级 MEMORY 纳入 Obsidian `WorkBuddy-MEMORY/` 管理

### 蒸馏动作

| 维度 | 蒸馏前 | 蒸馏后 | 限制 |
|---|---|---|---|
| 项目级 MEMORY | 206行/15k | 77行/2,445 | 3,000 |
| 用户级 MEMORY | 46行/2.5k | 不动 | 4,000 |

**项目级精简内容**：
- 删「项目资料库索引」全表（概念速查 22 条 + 编辑器/打点/游戏逻辑/Rocket/工具/障碍牌/Effect 全分类表格 ~100 行）
- 替换为极简核心速查 8 条 + 引导链接 `[[_MOC]]` / `[[知识库文档顺序索引]]`
- Notion/备份/文档规则压缩为摘要（50行→15行）
- Git 硬规则 + Obsidian 优先规则完整保留

**用户级**：未超限，仅存档快照，不做精简。

### 索引闭环
```
AI 查资料 → 读 MEMORY 核心速查 → 跳转 Obsidian [[_MOC]] / [[知识库文档顺序索引]]
         → mcp__obsidian-mcp__search_vault 或 Grep → 对应笔记
         → 需要历史版本 → [[MEMORY-项目级-原始存档（append）]]
```

### Obsidian 归档结构
```
02-PROJECTS/TileMatch/WorkBuddy-MEMORY/
├── _MOC.md                               — 归档索引 + 查资料流程
├── MEMORY-项目级-原始存档（append）.md     — 项目级 append-only 原文存档
├── MEMORY-用户级-原始存档（append）.md     — 用户级 append-only 原文存档
└── MEMORY-蒸馏日志.md                      — 本文件，每次蒸馏记录
```

### 后续维护
- 项目级 MEMORY 超限时：先存档原文到 append 文件 → 蒸馏精简 → 本日志追加记录
- 用户级 MEMORY 达 ~4,000 字符时触发首次蒸馏
- 蒸馏频率预估：每月 1-2 次（依赖项目变化量）
