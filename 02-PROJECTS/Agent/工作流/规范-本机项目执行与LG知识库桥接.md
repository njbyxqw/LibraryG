---
title: 本机项目执行与 LG 知识库桥接规范
date: 2026-09-04
type: spec
status: finalized
lifecycle: current
priority: critical
scope: local-personal-codex
source: "用户 2026-09-04 明确确认：LG 是唯一知识库与规范源；TS / MT 团队规则与 Docs 默认只读，不承载个人知识库流程。"
tags: [LibraryG, Codex, 本机流程, TileScape, TileMatch, 知识库]
---

# 本机项目执行与 LG 知识库桥接规范

> 本规范仅约束当前用户的本机 AI / Codex 工作流，不修改 TS、MT 的业务代码、团队 Docs、项目 `AGENTS.md` 或 `.cursor/rules`。项目 `AGENTS.md` 只读作团队约束；本机忽略的 `.agent/PROJECT.md` 与 `.worktreeinclude` 才可作为个人 Agent 入口，且只包含项目地图和 Worktree 所需上下文，不复制 LG 规则或任务进度。

## 唯一来源与分工

| 空间 | 本机 AI 的使用方式 |
|---|---|
| LibraryG | 唯一知识库与规范源。任务档案、活索引、稳定结论、Daily、MOC、维护规范和个人 AI 工作流均写入此处。 |
| TileScape / TileMatch | 项目执行空间和当前代码事实来源。读取、局部检索代码与项目 Docs；默认不写入个人任务档案或知识库规范。 |

项目本地规则只提供代码约束和团队交付要求；与 LG 的个人知识库流程发生差异时，以 LG 为准，但不反向修改团队规则来“同步”个人流程。

## 本机 AI 的读取顺序

### 涉及任务创建、知识整理、归档、MOC、Daily、INBOX、跨项目或自动化

1. 先读 LG：`AGENTS.md` → `AI总MOC.md` → 对应项目 `_MOC.md`。
2. 再按任务读 LG 的入库、多项目或专题规范。
3. 需要项目事实时，进入 TS / MT 读取其 `AGENTS.md`、代码、`Docs/`、`Docs/Knowledge/` 和源码旁 Markdown。
4. 结论、任务主档、索引和 Daily 回写 LG；项目本地文档只作为来源或执行材料。

### 纯局部编码

只改一处代码、无任务档案或知识沉淀需求时，可以先按项目本地代码规则执行；一旦变为持续任务、需要方案/记录、形成稳定结论或需要跨项目对照，立即回到上述 LG 读取顺序。

## 项目 Docs 的读写边界

- **必须可读、可检索**：项目 `Docs/`、`Docs/Knowledge/`、源码旁 Markdown 可能包含当前设计、配置说明、交付材料或代码事实，不能因 LG 是知识库而跳过。
- **默认不写**：不在其中创建个人任务主档、个人 Daily、个人 MOC、个人知识库规范、个人执行反馈或验收记录。
- **例外**：用户明确要求随代码评审、项目交付或团队共享的文档时，才写项目 Docs；如关联持续任务，必须从该文档链接回 LG 主档案。

## 三类任务的落点

| 类型 | 主载体 | 项目本地材料 |
|---|---|---|
| 持续项目任务 | LG 对应项目领域的 `任务-<主题>.md`，从任务开始即建立。 | 只保留代码旁说明、交付文档或原始附件，并链接 LG 主档。 |
| 活索引 / 快速查找 | LG 对应项目的既有索引。 | 可读取项目 Docs、代码和配置作为来源；不新建个人本地索引副本。 |
| 零碎临时工作 | 默认对话；需要跨回合保存时使用 LG INBOX。 | 不因保存个人过程而新建项目 Docs。 |

## 禁止项

- 不为同步个人知识库流程修改 TS / MT 的业务代码、团队 Docs 或 `.cursor/rules`；项目 Agent 入口文件仅在用户明确启用时维护，并保持最小、可审阅。
- 不把项目 Docs 当作个人知识库或规范源，也不因其本地属性而拒绝读取/检索。
- 不用事后迁移替代任务创建时应走的 LG 主档案。
- 不自动 commit / push。

## 关联

- [[AI总MOC|AI 总 MOC]]
- [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]
- [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]]
- [[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]]
- [[02-PROJECTS/TileScape/_MOC|TileScape MOC]]
