# LibraryG Agent Instructions

本文件是 Codex 或其他 AI Agent 进入 LibraryG 时的根目录冷启动入口。

## 工作空间地图

| 空间 | 路径 | 定位 |
|---|---|---|
| LG / LibraryG | `/Users/dean/LibraryG` | 唯一知识库与规范源、Obsidian vault、长期记忆、工作记录 |
| MT / TileMatch 老项目 | `/Users/dean/Downloads/meatloaf_client` | 项目执行空间、旧项目、历史行为基线、对照来源 |
| TS / TileScape | `/Users/dean/TileScape` | 项目执行空间、从 MT 分离出的优化项目，承载迁移和重构 |

LG 是唯一知识库与规范源。项目之间不固定主次，但 TS / MT 只作为执行空间和事实来源；所有知识沉淀、维护规范、AI 读取协议和自动化规则均以 LG 为准。

## 子项目入口桥接

- LG 是所有工作空间的上层路由，不是仅在当前目录为 LG 时才读取的资料库。
- TS / MT 的 `AGENTS.md` 只提供项目执行入口和本地代码约束；对查找、归档、历史、资源定位、跨项目任务、知识入库和自动化必须先回到本文件，再进入对应项目 MOC。
- TS / MT 内的 AI 记忆、`Docs/Knowledge`、`.workbuddy/memory` 或源码旁 Markdown 不得作为独立规范源；若与 LG 规范冲突，先遵守 LG，并把差异记录回 LG。
- 子项目的当前代码事实优先于 LG 历史记录；发现差异时保留来源与状态，不覆盖或静默替换历史结论。

## 优先读取

1. `AI总MOC.md`
2. `HOME.md`
3. `工作空间总纲.md`
4. `02-PROJECTS/Agent/Memory.md`
5. 入库、归档、维护任务：`02-PROJECTS/Agent/工作流/规范-任务产出入库与维护.md`
6. 复杂跨项目任务：`02-PROJECTS/Agent/工作流/规范-多项目工作流与复现.md`
7. MOC 或导航问题：`02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级.md`

## 代码任务入口

- TS 代码任务：先读 `/Users/dean/TileScape/AGENTS.md`，再读 `/Users/dean/TileScape/Docs/Knowledge/README.md`、`Memory.md`、`CodeMap.md`。
- MT 代码或历史行为任务：先读 `/Users/dean/Downloads/meatloaf_client/client/AGENTS.md` 和 `02-PROJECTS/TileMatch/参考/MT老项目路径索引.md`。
- 跨 MT / TS 任务：中等以上任务要留下对位文件表，记录 MT 文件、TS 文件、关系和结论。

## 任务知识闭环（强制）

以下规则适用于所有有代码阅读、分析、实现、调研或方案产出的任务；不得在未完成检查前直接结束对话。

1. **先路由再检索**：先判定任务属于 MT、TS、跨项目或 LG；读取对应 MOC 与必要入口后，才在目标目录局部检索。不得只依赖对话上下文或全盘搜索。
2. **过程入 DAILY**：每次有实质进展，当日 `01-DAILY/YYYY-MM-DD.md` 按 `## TileMatch`、`## TileScape`、`## LibraryG` 分节追加“做了什么 + 关键结论 + 产出/路径 + 后续入口”。
3. **稳定结论必须归位**：游戏规则、机制、ECA、DDA、行为链路归入 LG 对应项目的 `游戏逻辑/`；代码定位、程序集职责、加载链路和文件地图归入 LG 项目 `代码框架/`、`参考/`。TS 仓库 `Docs/Knowledge/CodeMap.md` 可作为执行索引同步，但不能作为唯一长期来源；新增稳定文档必须挂到 LG 项目 MOC/索引。
4. **收尾自检**：回复“完成”前检查：是否更新 DAILY、是否新增或更新稳定文档、是否补 MOC/索引、是否写明来源与验证边界。没有稳定结论时，也要在 DAILY 明确写“仅完成定位/未形成可入库结论”。
5. **WorkBuddy 交接**：启用交接后，稳定结论必须选择“已直接入库 / 已生成 `ready` 任务包 / 无稳定结论”之一；仅把含来源、精确目标、正文、锚点与幂等标记的低风险任务包交给 WorkBuddy。 
6. **自动化不替代判断**：日检只能补漏和提出归档建议；不从团队提交、文件修改时间或推断中捏造个人工作记录。

详细标准与自动巡检见 `02-PROJECTS/Agent/工作流/规范-任务知识沉淀闭环与自动巡检.md`；WorkBuddy 任务包与验收流程见 `02-PROJECTS/Agent/工作流/方案-WorkBuddy日志知识闭环自动化实施.md`。

## 知识库规则

- LG 是唯一长期稳定来源：总纲、完整总结、稳定工作流、复盘、Daily、可检索记忆和自动化规则都沉淀到 LG。
- 项目目录只做执行：代码、资源、配置、快速入口、模块梗概、本地设计文档和任务上下文；其中稳定结论必须同步回 LG。
- Daily 可以详细记录，承担备份追踪、历史存档、成功路径和决策索引作用。
- 跨项目 wikilink 尽量写完整 vault 路径，尤其是 `_MOC.md`。
- 保留历史 WorkBuddy 材料。用 historical / deprecated 标注，不要直接删除有意义内容。

## 用户偏好

- 默认使用简洁中文，除非任务需要代码或精确英文术语。
- 输出要结构化、高信号；对比类内容优先用表格。
- 找不到文件、路径、配置时，合理检查后直接问，不要反复绕路。
- 不要自动 commit 或 push。任何 git 写操作都需要用户明确授权，并先展示待提交内容。
- 编辑要小步、克制、可核查；不要大规模覆盖或删减历史知识。

## 记忆位置

- 当前通用记忆：`02-PROJECTS/Agent/Memory.md`
- 历史 WorkBuddy 记忆归档：`02-PROJECTS/Agent/WorkBuddy-MEMORY/`
- 兼容记忆路径：`.workbuddy/memory/MEMORY.md`
