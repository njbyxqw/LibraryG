---
title: TileScape 知识库 MOC
tags: [TileScape, MOC]
type: index
status: finalized
date: 2026-08-04
aliases:
  - TileScape 知识库_MOC
---

# TileScape 知识库 — 总入口

> 本文档是 TileScape 知识库的导航中心。从上到下按「模块 → 子模块 → 具体文档」组织。

---

## 快速入口

- [[_项目概览|项目概览]] — TileScape 项目基本信息
- [[代码框架/代码框架总览|代码框架总览]] — 程序集职责 / 目录架构 / 关键类索引（含文件级检索索引 2026-08-20）
- [[道具系统/手套道具MoveToOverBar表现层分析|手套道具 MoveToOverBar 表现层分析]] — 表现层 4 层架构 / 需求对齐 / 0.1s 停留补丁
- [[参考/Docs文档索引|Docs 文档索引]] — Docs/ + Doc/ 未迁移文档分类清单

---

## 📊 知识库仪表盘（Dataview）

> 需安装并启用 Obsidian **Dataview** 社区插件后生效。启用后下方表格会自动统计 `02-PROJECTS/TileScape` 下的所有笔记。

### 全部文档（按修改时间）
```dataview
TABLE type, status, date
FROM "02-PROJECTS/TileScape"
WHERE type
SORT file.mtime DESC
```

### 各分类文档数
```dataview
TABLE length(rows) AS 文档数
FROM "02-PROJECTS/TileScape"
WHERE type
GROUP BY file.folder
```

### 最近更新（Top 10）
```dataview
TABLE date, status
FROM "02-PROJECTS/TileScape"
WHERE date
SORT date DESC
LIMIT 10
```

---

## 目录结构

```
02-PROJECTS/TileScape/
├─ _MOC.md              总入口（本文档）
├─ _项目概览.md         基本信息
├─ 代码框架/
│  └─ 代码框架总览.md   程序集 / 目录 / 关键类索引
├─ 道具系统/
│  └─ 手套道具MoveToOverBar表现层分析.md   表现层架构 / 需求对齐 / 0.1s补丁
└─ 参考/
   └─ Docs文档索引.md   Docs/ + Doc/ 未迁移文档分类清单
```

## 待办 / 后续扩展

- [x] Docs/ 与 Doc/ 文档整理备注（见 [[参考/Docs文档索引|Docs 文档索引]]）
- [x] 代码框架总览扩充文件级检索索引（第八~十二章：关键类→路径 / 模块明细 / View / 编辑器 / ECA）
- [ ] 按需迁移高价值设计文档（参考索引中的迁移优先级）
- [ ] 补充具体模块文档（如编辑器、DDA、打点）
