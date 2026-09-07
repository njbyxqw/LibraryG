---
title: 执行反馈：三工作空间 AI 工作流规范全量审查
date: 2026-09-04
type: report-plan
status: feedback-ready
priority: critical
projects: [LibraryG, TileScape, TileMatch]
source: "任务包-三工作空间AI工作流规范全量审查-2026-09-04 的只读审查执行反馈；由 WorkBuddy 执行、待 Codex 验收"
verification: "只读静态审查；未修改 TS / MT 任何文件，未 commit / push"
tags: [LibraryG, AI工作流, 规范审查, 执行反馈, TileScape, TileMatch]
---

# 执行反馈：三工作空间 AI 工作流规范全量审查

> [!important] 审查方式与边界
> - 本轮为**只读静态审查**：仅读取 LG / TS / MT 三个工作空间的规范、索引、MOC 与 Docs，未修改、移动、删除、重命名任何文件。
> - **未修改 TS / MT 任何团队文件**（`AGENTS.md`、`.cursor/rules`、`Docs/`、`Docs/Knowledge/`），未改 Git 配置，未 commit / push。
> - 不依据文件修改时间、Git 提交或未跟踪文件推断个人工作事实。
> - 每条结论附：工作空间 · 精确路径 · 标题/章节或行文锚点 · 分类与判断边界。

---

## 〇、总体结论（先看这里）

| 判断 | 结论 |
|---|---|
| 核心边界是否一致 | **无冲突**。LG 规范与 TS / MT 已检查材料中，`LG 是唯一知识库与规范源；TS / MT 默认只读、可读可检索、默认不写` 的边界没有冲突；TS 根 `AGENTS.md` 为项目规则索引，LG 回链声明位于 `Docs/Knowledge/README.md`。 |
| 是否有本地规范被误作个人规范源 | **无**。TS 的 `Docs/Knowledge/README.md`、MT 的 `client/AGENTS.md` 均主动声明 LG 是唯一规范源，未发现冲突表述。 |
| 是否有 P0（阻断级）问题 | **无**。未发现会阻断冷启动、误导 AI 进入错误规范源、或导致数据破坏的问题。 |
| 待修订项 | **1 项 P1 + 2 项 P2**，全部为 LG 侧修订，见第六节。 |
| TS / MT 是否需要改动 | **不需要**。所有修复均在 LG 侧完成，无需触碰团队文件。 |

---

## 一、三个工作空间的证据清单

### A. LibraryG 规范源（14 项必读，全部已读）

| # | 文件 | 角色 | 关键证据（锚点） |
|---|---|---|---|
| 1 | `AGENTS.md` | `canonical` | 根冷启动入口；「工作空间地图」表明确 LG 主控知识库、MT/TS 执行空间；「优先读取」列出 7 项。 |
| 2 | `AI总MOC.md` | `routing` | 默认必读三项、规则分层、任务路由表（含「项目 AI 记忆同步」指向 TS/MT 同步文档）。 |
| 3 | `HOME.md` | `routing` | 全库导航；「工作流」行列出规范入口。**发现歧义链接见 P2-1。** |
| 4 | `工作空间总纲.md` | `canonical` | LG 唯一源、三空间边界、知识库规则。 |
| 5 | `02-PROJECTS/Agent/Memory.md` | `canonical` | 路径速查、冷启动顺序、LG 稳定协议、文档归属、用户偏好、Git 约束、MOC 约定、状态标记。 |
| 6 | `02-PROJECTS/Agent/工作流/_MOC.md` | `routing` | 路由表分「规范与当前入口 / 报告与计划 / 实施任务包 / 历史与休眠」。**状态未更新见 P2-2。** |
| 7 | `…/规范-任务产出入库与维护.md` | `canonical` | 核心原则、入库路径判断、三类任务、LG 唯一源、项目 Docs 默认只读。 |
| 8 | `…/规范-本机项目执行与LG知识库桥接.md` | `canonical` | 2026-09-04 新建；唯一来源与分工表、读取顺序、Docs 读写边界、三类任务落点、禁止项。与任务边界完全一致。 |
| 9 | `…/规范-MOC命名与导航层级.md` | `canonical` | 核心原则（含「项目 MOC 优先」）、推荐层级、命名/链接规则、当前 MOC 登记。 |
| 10 | `…/规范-多项目工作流与复现.md` | `canonical` | 核心原则、推荐读取顺序、任务路由表、对位文件表。 |
| 11 | `…/规范-AI协作注意事项.md` | `canonical` | 只读分析型 AI 边界、结论状态（已确认/已审计/待验证/无证据）。 |
| 12 | `…/规范-任务知识沉淀闭环与自动巡检.md` | `canonical` | 四道门、分类落点、收尾清单、自动巡检、规则统一性检查。 |
| 13 | `…/INBOX对话工作区工作流.md` | `needs-review` | 2026-07-01；产物分类判断表落点与当前落地约定冲突，见 P1。 |
| 14 | `03-KNOWLEDGE/_MOC.md` + `02-PROJECTS/TileMatch/_MOC.md` + `02-PROJECTS/TileScape/_MOC.md` | `routing` | 三个 MOC 均已接入，路由完整；`03-KNOWLEDGE/_MOC.md` 已把空文件 `Unity.md` 登记为 `needs-review` 且「不进入任何 MOC 导航」。 |

### B. TileScape 执行与事实来源（已读）

| 文件 | 角色（本地） | 关键证据 |
|---|---|---|
| `TileScape/AGENTS.md`（40 行） | 本地路由索引 | 仅索引；规则源 `.cursor/rules`、技能源 `.cursor/skills`；明确「`.cursor` 是唯一维护源、不写绝对路径」。 |
| `TileScape/.cursor/rules/agent-habits.mdc`（71 行） | 团队代码约束 | 不擅自改码、多方案对比、dotnet 受控编译等本地协作习惯。 |
| `TileScape/Docs/Knowledge/README.md` | 事实来源 + 边界声明 | **明确「本目录不是独立知识库或规范源；LibraryG 是唯一知识库与规范源」**——与 LG 一致，无冲突。 |
| `Docs/Knowledge/Memory.md` / `CodeMap.md` / `TaskIndex.md` | 本地执行索引 | 均为本地事实来源；CodeMap 承载代码定位与文件地图。 |
| `Docs/Knowledge/Governance.md` | 本地治理说明 | 明确「参考 LG 的 Memory / MOC / INBOX / DAILY」——无冲突。 |
| `Docs/Knowledge/Local/`（Inbox/Archive）+ `Module/TileV2.md` | 本地暂存/模块事实 | Local 受 gitignore 保护；Module/TileV2 为项目模块事实。 |

### C. TileMatch / MT 执行与事实来源（已读）

| 文件 | 角色（本地） | 关键证据 |
|---|---|---|
| `Downloads/meatloaf_client/client/AGENTS.md`（165 行） | 本地路由 + 代码约束 | **首段即声明「LibraryG 是唯一知识库与规范源；涉及查找/归档/历史/资源定位/跨项目/入库/自动化时先读 LG AGENTS.md、AI总MOC、02-PROJECTS/TileMatch/_MOC」**。含 C#/Unity 编码规则、受控 dotnet build、规则/skill 索引。 |
| `client/.cursor/rules/agent-habits.mdc`（72 行） | 团队代码约束 | 与 TS 版本基本一致的本地代码习惯。 |
| `02-PROJECTS/TileMatch/参考/MT老项目路径索引.md` | LG 侧索引 | 基础路径、TileV2 对照入口、MT 独有入口、使用规则。 |
| `02-PROJECTS/TileMatch/参考/同步-项目AI记忆与源码旁文档-2026-09-03.md` | LG 侧同步记录 | 登记 MT AI 记忆与源码旁文档到 LG；明确「源码旁文档设计结论不得直接写成通用 Knowledge」。 |

---

## 二、跨工作空间统一矩阵（9 环节）

| 工作流环节 | LG 当前规范/入口 | TS 当前事实入口 | MT 当前事实入口 | 一致性 | 缺口或风险 |
|---|---|---|---|---|---|
| 冷启动读取 | `AGENTS.md` → `AI总MOC.md` → 项目 `_MOC.md` → 专题规范（桥接规范 §读取顺序） | `AGENTS.md`（40 行索引）→ `.cursor/rules/agent-habits.mdc`、`Docs/Knowledge/*` | `client/AGENTS.md`（首段声明 LG 唯一源）→ `.cursor/rules` | ✅ 一致 | HOME.md `Unity` 歧义链接（P2-1） |
| 新建持续任务 | LG `任务-<主题>.md` 起始即建（桥接规范 §三类任务落点） | 不建本地任务档案 | 不建本地任务档案 | ✅ 一致 | 无 |
| 活索引 / 快速查找 | 项目 MOC 活索引（`参考-关卡资源路径速查`、`参考/快速定位与资源替换索引`） | `Docs/Knowledge/` 索引 + LG 参考索引 | LG `参考/关卡资源路径速查` + `MT老项目路径索引` | ✅ 一致 | 无 |
| 零碎任务 / INBOX | 默认对话；跨回合用 LG `00-INBOX/` | 不写个人 INBOX | 不写个人 INBOX | ⚠️ 基本一致 | INBOX 工作流落点表旧约定（P1） |
| 项目 Docs 读取与检索 | 必须可读可检索（桥接规范 §Docs 读写边界） | `Docs/Knowledge/` + 源码旁 Markdown | `Docs/` + 源码旁 Markdown | ✅ 一致 | 无 |
| 项目 Docs 写入边界 | 默认不写；例外需用户要求 + 回链 LG 主档 | README 声明「非独立规范源」 | 同步文档声明「源码旁结论不得写成通用 Knowledge」 | ✅ 一致 | 无 |
| 稳定结论 / Daily / MOC | LG 唯一落点（任务产出入库、沉淀闭环） | 本地不写个人 Daily/MOC | 本地不写个人 Daily/MOC | ✅ 一致 | `_MOC` 任务包状态未更新（P2-2） |
| 跨项目对位与代码事实 | LG 对位文件表 + `规范-多项目工作流与复现` + `MT老项目路径索引` | 代码事实优先；`Docs/Knowledge/CodeMap` | 历史基线；`client/AGENTS.md` + 路径索引 | ✅ 一致 | 无 |
| WorkBuddy 执行与 Codex 验收 | LG 任务包 → WorkBuddy 执行 → Codex 验收（沉淀闭环 §收尾） | 无（纯执行空间） | 无（纯执行空间） | ✅ 一致 | 无 |

---

## 三、三类结论（已确认 / 待确认 / 无证据）

### 已确认（有精确路径与行文锚点支撑）

1. **LG 唯一规范源边界一致**：`AGENTS.md`、`工作空间总纲.md`、`Memory.md`、`规范-本机项目执行与LG知识库桥接.md`、`规范-任务产出入库与维护.md` 五份 canonical 文件均表述「LG 唯一源、TS/MT 默认只读」，无冲突。
2. **TS 本地材料正确声明边界**：`TileScape/Docs/Knowledge/README.md` 明确「本目录不是独立知识库或规范源；LibraryG 是唯一知识库与规范源」。
3. **MT 本地材料正确声明边界**：`client/AGENTS.md` 首段声明 LG 唯一源并给出「先读 LG AGENTS.md → AI总MOC → TileMatch/_MOC」回链顺序。
4. **三个项目 MOC 已接入**：`03-KNOWLEDGE/_MOC.md`、`02-PROJECTS/TileMatch/_MOC.md`、`02-PROJECTS/TileScape/_MOC.md` 均已建立并互相回链，路由完整。
5. **HOME.md 存在 Unity 歧义链接**：`HOME.md:249` 同时存在 `[[03-KNOWLEDGE/Unity/Unity 开发笔记|Unity 开发]]` 与 `[[03-KNOWLEDGE/Unity|Unity 速查]]`，后者可解析到空文件 `03-KNOWLEDGE/Unity.md`（0 字节，2026-08-05）或目录 `03-KNOWLEDGE/Unity/`，构成歧义与重复路由。
6. **`_MOC.md` 任务包状态滞后**：`02-PROJECTS/Agent/工作流/_MOC.md`「实施任务包」区仍标「知识库内容归属与 MOC 路由整理 | current（执行中 / 待验收）」，而该任务包已于 2026-09-03 执行并验收完毕。

### 待确认（需用户或 Codex 裁决）

1. **INBOX 工作流落点冲突**：`02-PROJECTS/Agent/工作流/INBOX对话工作区工作流.md`（2026-07-01）产物分类判断表写「规范/流程文档 → `03-KNOWLEDGE/工作流/`」，而当前实际落地为 `02-PROJECTS/Agent/工作流/`（见 `规范-任务产出入库与维护.md`、`Agent/工作流/_MOC.md`）。**需确认以哪份为准，或将该旧文档降级为 historical。**

### 无证据

1. **未发现任何 TS / MT 本地文件把「个人任务档案 / 个人 Daily / 个人 MOC / 个人规范」误写入团队文件**。
2. **未发现 `AI总MOC` / Agent 工作流 MOC 把报告、计划或任务包误作默认规范入口**（`_MOC.md` 已明确分「规范 / 报告与计划 / 实施任务包 / 历史与休眠」四区，报告仅作追溯）。
3. **未发现断链导致冷启动死路**（除 HOME.md 的 Unity 歧义外，其余关键入口路径均存在）。

---

## 四、规范角色清单与历史/任务包状态问题

### 角色清单（LG 侧 16 个文件 / 14 项必读条目）

| 角色 | 数量 | 文件 |
|---|---|---|
| `canonical` | 9 份 | `AGENTS.md`、`工作空间总纲.md`、`Memory.md`、`规范-任务产出入库与维护.md`、`规范-本机项目执行与LG知识库桥接.md`、`规范-MOC命名与导航层级.md`、`规范-多项目工作流与复现.md`、`规范-AI协作注意事项.md`、`规范-任务知识沉淀闭环与自动巡检.md` |
| `routing` | 6 份 | `AI总MOC.md`、`HOME.md`、`Agent/工作流/_MOC.md`、`03-KNOWLEDGE/_MOC.md`、`02-PROJECTS/TileMatch/_MOC.md`、`02-PROJECTS/TileScape/_MOC.md` |
| `needs-review` | 1 份 | `INBOX对话工作区工作流.md` |

> 注：必读条目共 14 项，其中第 14 项含 3 个 `_MOC.md` 文件，故文件总数为 16 个（9 canonical + 6 routing + 1 needs-review）。

### 历史 / 任务包状态问题

| 问题 | 位置 | 建议 |
|---|---|---|
| 已执行任务包仍标「进行中」 | `02-PROJECTS/Agent/工作流/_MOC.md`「实施任务包」区 | 将「知识库内容归属与 MOC 路由整理」状态改为 `completed（已执行 / 已验收）`，或移入「报告与计划」区归档。 |
| 旧 INBOX 工作流落点约定过时 | `INBOX对话工作区工作流.md`（2026-07-01） | 降级为 `historical`，或更新落点表以对齐 `02-PROJECTS/Agent/工作流/`。 |

---

## 五、推荐的 LG-only 修订任务清单

> [!note] 原则
> 以下所有修订均在 LG 工作空间内完成，**不触碰 TS / MT 任何团队文件**。

### P1（重要，规范冲突，应优先修复）

- **P1-1 修复 INBOX 对话工作区工作流的落点表**
  - 目标：`02-PROJECTS/Agent/工作流/INBOX对话工作区工作流.md`
  - 问题：产物分类判断表「规范/流程文档 → `03-KNOWLEDGE/工作流/`」与当前实际落地 `02-PROJECTS/Agent/工作流/` 冲突，会误导 AI 把规范流程文档落到错误目录。
  - 建议：将落点改为 `02-PROJECTS/Agent/工作流/`；或将该文档整体降级为 `historical` 并在 `_MOC.md` 中移入「历史与休眠」区。

### P2（次要，歧义 / 状态，可择期修复）

- **P2-1 清理 HOME.md 的 Unity 歧义链接**
  - 目标：`HOME.md:249`
  - 问题：`[[03-KNOWLEDGE/Unity|Unity 速查]]` 与 `[[03-KNOWLEDGE/Unity/Unity 开发笔记|Unity 开发]]` 重复，且前者可解析到 0 字节空文件 `03-KNOWLEDGE/Unity.md`。
  - 建议：删除歧义链接 `[[03-KNOWLEDGE/Unity|Unity 速查]]`，仅保留 `[[03-KNOWLEDGE/Unity/Unity 开发笔记|Unity 开发]]`；空文件 `Unity.md` 维持 `needs-review` 登记（已在 `03-KNOWLEDGE/_MOC.md` 处理，不删除不覆盖）。

- **P2-2 更新 `_MOC.md` 实施任务包状态**
  - 目标：`02-PROJECTS/Agent/工作流/_MOC.md`「实施任务包」区
  - 问题：「知识库内容归属与 MOC 路由整理」仍标 `current（执行中 / 待验收）`。
  - 建议：改为 `completed（已执行 / 已验收）`。

---

## 六、不修改 TS / MT 团队文件的声明

本轮审查**未修改、未移动、未删除、未重命名** TileScape 与 TileMatch 两个工作空间下的任何文件，包括但不限于：

- `TileScape/AGENTS.md`、`TileScape/.cursor/rules/agent-habits.mdc`、`TileScape/Docs/**`、`TileScape/Docs/Knowledge/**`
- `meatloaf_client/client/AGENTS.md`、`meatloaf_client/client/.cursor/rules/agent-habits.mdc`、`meatloaf_client/**`

也未修改任何 Git 配置、未执行 commit 或 push。所有修订建议均落在 LG 工作空间内。

---

## 关联

- [[AI总MOC|AI 总 MOC]]
- [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]
- [[02-PROJECTS/Agent/工作流/规范-本机项目执行与LG知识库桥接|本机项目执行与 LG 知识库桥接规范]]
- [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]]
- [[03-KNOWLEDGE/_MOC|通用知识 MOC]]
- [[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]]
- [[02-PROJECTS/TileScape/_MOC|TileScape MOC]]
