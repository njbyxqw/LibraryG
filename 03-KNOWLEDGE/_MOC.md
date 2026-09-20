---
title: 通用知识 MOC
date: 2026-09-03
type: index
status: finalized
lifecycle: current
priority: high
tags: [LibraryG, 03-KNOWLEDGE, MOC, 可迁移知识]
source: "2026-09-03 用户确认的知识归属与 MOC 路由规则；由任务包执行建立"
---

# 通用知识 MOC

> `03-KNOWLEDGE` 是**可迁移知识层**，不是项目文档的副本。本页是它的总入口，只路由"脱离单一项目仍可复用"的知识；项目事实的第一入口在 [[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]] 与 [[02-PROJECTS/TileScape/_MOC|TileScape MOC]]。

---

## 定位与判断规则

| 规则 | 说明 |
|---|---|
| 可放 | 跨项目已验证的共同机制、跨项目方法论，以及虽源自单一项目但明显可迁移的 Unity / 编辑器 / 设计方法。 |
| 不放 | 单项目专属的类、路径、配置值、功能实现、任务进度和项目事实正文。 |
| 提炼要求 | 允许从单一项目提炼，但必须写清"来源项目、适用范围、验证状态"，并回链项目事实。 |
| 写入顺序 | 先沉淀项目事实，确认具有复用价值后再提炼到 Knowledge；不得为了通用而复制项目原文。 |

---

## 按主题进入

| 主题 | 入口 | 状态 |
|---|---|---|
| 底层框架（跨项目） | [[03-KNOWLEDGE/底层框架/底层框架总览|底层框架总览]] · [[03-KNOWLEDGE/底层框架/BettaSDK/SDK总览|BettaSDK]] · [[03-KNOWLEDGE/底层框架/BettaFramework/框架总览|BettaFramework]] · [[03-KNOWLEDGE/底层框架/BettaInterface/契约总览|BettaInterface 契约]] | 新增（2026-09-18）：TS / MT 共用 submodule 同源；**以 TS 为基准**，MT 仅作参考。BettaInterface 契约层 + BettaFramework 核心机制 + BettaSDK 架构级均已细化到复刻级（静态扫描 + git 实测 + asmdef GUID 解析，未做运行时验证） |
| Unity / 架构方法 | [[03-KNOWLEDGE/Unity/Unity 开发笔记|Unity 开发笔记]] | Knowledge 候选（来源 TileMatch，TileScape 未验证） |
| 编辑器设计 | [[03-KNOWLEDGE/TileV2-Editor/TileV2 编辑器概览|TileV2 编辑器概览]] | 混合条目，待拆分事实与通用方法 |
| 游戏逻辑 | [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑分析]]、[[03-KNOWLEDGE/Game-Logic/任务-元素牌开发|元素牌开发任务]] | 项目事实汇总；跨 TS / MT 元素牌持续任务 |
| Obsidian / LG 工具 | [[03-KNOWLEDGE/Obsidian插件使用指导|Obsidian 插件使用指导]] | 工作流资料，待迁移到 Agent 工作流 |

---

## 当前条目状态

| 文件 | 当前判断 | 处理 |
|---|---|---|
| `Game-Logic/游戏逻辑分析.md` | 主要是 TileMatch 的 Rocket、DDA、死局等具体事实，不是可直接作为通用规则的正文。 | 保留原文件和所有链接；不作为项目 MOC 的优先入口，待提炼 / 迁移决策。 |
| `TileV2-Editor/TileV2 编辑器概览.md` | 混有 TileMatch 专属事实与可能可迁移的编辑器设计做法。 | 保留；后续拆分事实与通用方法。 |
| `Unity/Unity 开发笔记.md` | 源自 TileMatch，MVC、asmdef、LocalExtensions 等可形成可迁移方法，仍混有项目例子。 | 保留为 Knowledge 候选；来源 TileMatch，TileScape 未验证。 |
| `Obsidian插件使用指导.md` | LG vault 的操作与配置资料，属 Agent 工作流，不属通用项目知识。 | 本次不移动；待迁移到 Agent 工作流，正式入口见 [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]。 |
| `Unity.md` | 文件名 `Unity`，与 Knowledge 层语义错位；当前为空文件。 | **不进入任何 MOC 导航**；登记为 `needs-review`，不得删除或覆盖。 |
| `底层框架/`（BettaSDK 子目录 + BettaFramework 子目录 + BettaInterface 子目录） | 2026-09-18 新增。来源 TS / MT 共用 submodule；职责与链路为包内 README + 静态扫描，版本与挂载差异为 git 实测，asmdef 依赖为 GUID 实测解析。BettaInterface 已细化到逐接口签名（契约总览 + 上下清单）；BettaFramework 已细化到核心机制（框架总览 + UIManager / MessageDispatch / Locale / StateMachine）；BettaSDK 已细化到架构级（SDK总览 + 启动与生命周期 / 能力注入-ImplementHub / 第三方服务-ServiceHub / 配置Schema）。 | 保留。**已定基准：以 TS 工作区现状为准**（与 HEAD 的旧命名差异不追回），MT 仅作参考；版本对照表在任一侧升级 submodule 后复核。 |

> [!note]
> 上表 `Unity.md` 仅作 `needs-review` 登记，不作为活动导航入口。

---

## 关联

- [[AI总MOC|AI 总 MOC]]
- [[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]]
- [[02-PROJECTS/TileScape/_MOC|TileScape MOC]]
- [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]
- [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]]
- [[02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级|MOC 命名与导航层级规范]]
<!-- kc:KC-20260903-001-magnet-card-design:A2 -->
- [[03-KNOWLEDGE/Game-Logic/设计-磁铁牌元素-v1|磁铁牌元素方案 v1]] — 按关卡组数随机替换、点击后三张联动消除的设计稿；存在待确认的 OverBar / 三消语义。
