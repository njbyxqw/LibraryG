---
title: TileScape 知识库 MOC
tags: [TileScape, MOC]
type: index
status: finalized
project: TileScape
lifecycle: current
date: 2026-09-03
aliases:
  - TileScape 知识库_MOC
---

# TileScape 知识库 — 总入口

> 本文档是 TileScape 知识库的导航中心。从上到下按「模块 → 子模块 → 具体文档」组织。

---

## 任务路由

| 需求 | 入口 |
|---|---|
| 项目概览 | [[02-PROJECTS/TileScape/_项目概览|项目概览]] |
| 代码框架 | [[代码框架/代码框架总览|代码框架总览]] |
| Docs 索引 | [[参考/Docs文档索引|Docs 文档索引]] |
| 项目 AI 记忆 / Docs 入口 | [[参考/同步-项目AI记忆与Docs入口-2026-09-03|项目 AI 记忆与 Docs 入口同步]] |
| 快速定位 / 资源替换 | [[参考/快速定位与资源替换索引|快速定位与资源替换索引]] |
| 新用户关卡风险 / SQL 设计 | [[参考/分析-新用户关卡风险与首次挫败监控方案-2026-09-08|新用户关卡风险与首次挫败监控方案]] |
| GM 模块 | [[GM工具/_MOC|GM 工具 MOC]] |
| 游戏逻辑 | 见下方「游戏逻辑」节（无独立 MOC，逐条列于本文档） |
| 跨项目持续任务 | [[03-KNOWLEDGE/Game-Logic/任务-元素牌开发|元素牌开发任务]]：TS 当前实现、MT 历史机制对位 |
| 可迁移知识 | [[03-KNOWLEDGE/_MOC|通用知识 MOC]] |

---

## 快速入口

- [[02-PROJECTS/TileScape/_项目概览|项目概览]] — TileScape 项目基本信息
- [[代码框架/代码框架总览|代码框架总览]] — 程序集职责 / 目录架构 / 关键类索引
- [[代码框架/梳理-GM工具注册与扩展链路-2026-08-26|GM 工具注册与扩展链路]] — `MODULE_GM` 门控、注册中心、面板执行与后续新增工具边界
- [[GM工具/_MOC|GM 工具]] — 新增与使用规则、具体 GM 工具说明与验证边界
- [[参考/Docs文档索引|Docs 文档索引]] — Docs/ + Doc/ 未迁移文档分类清单
- [[参考/同步-项目AI记忆与Docs入口-2026-09-03|项目 AI 记忆与 Docs 入口同步]] — TS `AGENTS.md`、`Docs/Knowledge`、`.workbuddy/memory` 与 LG 的入口边界
- [[参考/快速定位与资源替换索引|快速定位与资源替换索引]] — 多语言、配置、UI 与资源替换入口
- [[规范-多项目工作流与复现|多项目工作流与复现]] — MT / TS 同源代码下的记录、对照与复现闭环

## 游戏逻辑

- [[02-PROJECTS/TileScape/游戏逻辑/分析-DDAV3场景反例与迭代选项-2026-09-13|DDAV3 场景反例与迭代选项]] — 静态场景矩阵、体验假设、三条迭代路线及退出标准。

- [[02-PROJECTS/TileScape/游戏逻辑/任务-DDAV3逻辑策略持续研究|DDAV3 逻辑策略持续研究]] — 六个研究目标、版本增量、证据状态与自动化续跑断点。

- [[02-PROJECTS/TileScape/游戏逻辑/评估-DDAV3逻辑与实现策略-2026-09-11|DDAV3 逻辑与实现策略评估]] — DDA-V3-Test @ 9be729cb3：Slack 指标、曲线、选牌与静态评估；运行效果待验证。

- [[02-PROJECTS/TileScape/游戏逻辑/任务-DLC全链路梳理与维护|DLC 全链路梳理与维护]] — 唯一持续任务：启动/Home/画廊/解锁/Endless/活动全链路、当前配置、差距与验收入口

- [[游戏逻辑/设计-活动DLC扩展框架-2026-08-25|活动 DLC 扩展框架]] — 活动内容按基础包 / DLC 投递、请求下载校验开启链路与展示门禁的讨论稿
- [[游戏逻辑/设计-风车Shuffle单组保底-v1|风车 Shuffle 单组保底]] — 局内风车道具：仅定向保证一个牌型可补齐，其余随机换位
- [[游戏逻辑/梳理-局内四道具表现与逻辑-v1|局内四道具表现与逻辑]] — 撤回、风车、手套、磁铁的玩家表现与底层行为
- [[游戏逻辑/梳理-新增障碍元素开发流程-2026-09-08|新增障碍元素开发流程]] — 新增 Blocker 障碍的逻辑 / 资源 / 落地三段式流程（元素牌开发任务执行手册）
- [[道具系统/手套道具MoveToOverBar表现层分析|手套 MoveToOverBar 表现层历史审计]] — `feat-new_movetooverbar_prop` 的提交、表现层与 0.1s 停留补丁；非当前代码结论
- [[02-PROJECTS/TileScape/游戏逻辑/梳理-HomeDLC与Endless最大关卡更新流程-2026-08-20|Home DLC 与 Endless 最大关卡更新流程]] — 2026-08-20 历史重启链路；当前行为以 DLC 长期主档为准
- [[游戏逻辑/梳理-Home章节解锁镜头预览流程-2026-08-21|Home 章节解锁镜头预览流程]] — 新章节末关预览、停留与首关回程镜头链路
- [[02-PROJECTS/TileScape/游戏逻辑/梳理-ActivityDLC现状与设计差异-2026-08-26|Activity DLC 现状与设计差异]] — 2026-08-26 FirstPay 试点历史静态对照；当前范围以 DLC 长期主档为准
- [[游戏逻辑/审计-音效实际使用与未接入项-2026-08-12|音效实际使用与未接入项审计]] — 已接入、替代和未接入音效的历史静态审计

## 代码与配置定位

- [[代码框架/梳理-音效配置与播放链路-2026-08-24|音效配置与播放链路]] — AudioCfg、配置音量覆盖规则与 MT 对照
- [[游戏逻辑/梳理-Home普通关云层推进与镜头表现-2026-08-24|Home 普通关云层推进与镜头表现]] — Forest 1-50 节点、云层、角色与镜头表现，以及目标解锁节奏
- [[游戏逻辑/梳理-解锁动画时机调整-2026-08-24|解锁动画时机调整]] — 主界面关卡按钮、结算新障碍、局内道具教程解锁的飞行、特效与切换时序

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

### 待验证 / 待反馈
```dataview
TABLE type, status, verification, date
FROM "02-PROJECTS/TileScape"
WHERE contains(string(verification), "pending") OR contains(string(status), "needs")
SORT date DESC
```

### 代码逻辑沉淀
```dataview
TABLE type, status, verification, date
FROM "02-PROJECTS/TileScape"
WHERE type = "game-logic" OR type = "analysis" OR type = "tool"
SORT date DESC
```

### 设计草稿
```dataview
TABLE status, verification, date
FROM "02-PROJECTS/TileScape"
WHERE status = "draft"
SORT date DESC
```

### 属性约定

| 字段 | 用途 |
|---|---|
| `project` | 固定项目归属，便于跨项目检索时过滤。 |
| `type` | 文档类型：`index`、`reference`、`game-logic`、`analysis`、`spec`、`guide`、`tool` 等。 |
| `status` | 文档当前状态：`current`、`finalized`、`draft`、`needs-review` 等。 |
| `lifecycle` | 生命周期：`current`、`draft`、`historical`、`deprecated`。历史材料只标注，不直接删除。 |
| `verification` | 证据边界：静态梳理、已实施但待运行反馈、纯讨论稿等。 |

---

## 目录结构

```
02-PROJECTS/TileScape/
├─ _MOC.md              总入口（本文档）
├─ _项目概览.md         基本信息
├─ 代码框架/
│  └─ 代码框架总览.md   程序集 / 目录 / 关键类索引
│  └─ 梳理-GM工具注册与扩展链路-2026-08-26.md  GM 注册、面板与扩展边界
├─ GM工具/
│  └─ _MOC.md          新增规则与具体工具入口
│  └─ 规范-GM工具新增与使用规则.md
│  └─ 工具-屏蔽关卡动更开关.md
├─ 参考/
│  └─ Docs文档索引.md   TS 仓库 Docs/ + Doc/ 索引
│  └─ 快速定位与资源替换索引.md  路径、引用与资源替换入口
├─ 游戏逻辑/
│  └─ 设计-风车Shuffle单组保底-v1.md  风车单组保底规则
│  └─ 梳理-局内四道具表现与逻辑-v1.md  四道具表现与实际逻辑
│  └─ 梳理-HomeDLC与Endless最大关卡更新流程-2026-08-20.md  DLC 与 Endless 更新链路
│  └─ 梳理-Home章节解锁镜头预览流程-2026-08-21.md  章节解锁镜头预览链路
│  └─ 设计-活动DLC扩展框架-2026-08-25.md  活动 DLC 分包、门禁与展示设计讨论稿
```

## 待办 / 后续扩展

- [x] Docs/ 与 Doc/ 文档整理备注（见 [[参考/Docs文档索引|Docs 文档索引]]）
- [x] 多项目工作流与复现规范（见 Agent 工作流）
- [ ] 按需迁移高价值设计文档（参考索引中的迁移优先级）
- [ ] 补充具体模块文档（如编辑器、DDA、打点）

## 打点与 SQL

- [[02-PROJECTS/TileScape/参考/参考-TA游戏分析SQL基础-2026-09-08|TA 游戏分析 SQL 基础]] — 当前常用 TA 数据源、事件语义、时间与新用户口径、查询骨架、筛选和复核清单。
- [[02-PROJECTS/TileScape/参考/分析-新用户关卡风险与首次挫败监控方案-2026-09-08|新用户关卡风险与首次挫败监控方案]] — 新用户关卡风险、首次挫败、复活和重试的分析设计。
