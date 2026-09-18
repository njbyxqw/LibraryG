---
title: 任务包：三工作空间 AI 工作流规范全量审查
date: 2026-09-04
type: audit-task
status: completed
lifecycle: historical
archived: 2026-09-18
priority: critical
projects: [LibraryG, TileScape, TileMatch]
risk: low
source: "用户 2026-09-04 授权：全面审查并梳理 AI 工作流相应规范与文档；WorkBuddy 拥有 LG、TS、MT 三个独立工作空间。"
verification: "只读审查；由 Codex 汇总、规划与验收"
tags: [LibraryG, WorkBuddy, AI工作流, 规范审查, TileScape, TileMatch]
---

# 任务包：三工作空间 AI 工作流规范全量审查

## 一、审查目标

建立一份可执行、可维护的 AI 工作流规范地图，回答四个问题：

1. 哪些文档是 LG 的当前规范源，哪些只是报告、计划、历史材料或任务工作区？
2. AI 在 LG、TS、MT 三个工作空间各自应该读什么、检索什么、允许写什么？
3. 是否存在规则冲突、重复、失效入口、误导性本地规范或未接入的关键规则？
4. 如何在**不修改 TS / MT 团队文件**的前提下，让本机 AI 始终以 LG 为知识库与规范源，并能读取/检索项目 Docs 和代码事实？

> [!important] 已确认边界
> LG 是唯一知识库与规范源。TS / MT 是项目执行空间和事实来源；其 `AGENTS.md`、`.cursor/rules`、`Docs/`、`Docs/Knowledge/` 默认只读、可检索，不写入个人任务档案、个人 Daily、个人 MOC、个人规范或个人执行记录。

## 二、执行规则（WorkBuddy）

- 三个工作空间均只读审查；不得修改、移动、删除、重命名文件，不得改 Git 配置、commit 或 push。
- 不依据文件修改时间、Git 提交或未跟踪文件推断个人工作事实。
- 不全盘摘录正文；只记录与 AI 入口、规则、知识落点、任务创建、Docs 读写边界、Daily、INBOX、MOC 和自动化有关的证据。
- 每条结论必须附：工作空间、精确路径、标题/章节或行文锚点、分类与判断边界。
- 因三个工作空间独立，分别完成下列 A/B/C 审查；最终在 **LG 工作空间** 创建统一执行反馈。若无法跨工作空间写文件，则将三份结构化结果交回本任务，由 Codex 写入 LG。

## 三、A：LibraryG 规范源审查

### 必读范围

1. `AGENTS.md`
2. `AI总MOC.md`
3. `HOME.md`
4. `工作空间总纲.md`
5. `02-PROJECTS/Agent/Memory.md`
6. `02-PROJECTS/Agent/工作流/_MOC.md`
7. `02-PROJECTS/Agent/工作流/规范-任务产出入库与维护.md`
8. `02-PROJECTS/Agent/工作流/规范-本机项目执行与LG知识库桥接.md`
9. `02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级.md`
10. `02-PROJECTS/Agent/工作流/规范-多项目工作流与复现.md`
11. `02-PROJECTS/Agent/工作流/规范-AI协作注意事项.md`
12. `02-PROJECTS/Agent/工作流/规范-任务知识沉淀闭环与自动巡检.md`
13. `02-PROJECTS/Agent/工作流/INBOX对话工作区工作流.md`
14. `03-KNOWLEDGE/_MOC.md`、`02-PROJECTS/TileMatch/_MOC.md`、`02-PROJECTS/TileScape/_MOC.md`

### 输出内容

为每个文件标记一种角色：

| 角色 | 定义 |
|---|---|
| `canonical` | 当前 AI 必须遵守的 LG 规范或稳定入口。 |
| `routing` | 只负责把任务导向规范/项目/索引。 |
| `reference` | 按需读取的说明或专题资料。 |
| `report-plan` | 审查、报告、计划、任务包；不作为默认规则。 |
| `historical-dormant` | 历史同步、旧 WorkBuddy、废弃流程或仅追溯材料。 |
| `needs-review` | 当前语义、入口、状态或归属不明确。 |

重点检查：

- 同一主题是否在多份 `canonical` 文件中给出冲突指令；
- `AI总MOC`、Agent 工作流 MOC 是否将历史/任务包误作当前默认入口；
- 已执行或已替代任务包是否仍显示为进行中；
- “LG 唯一源、项目 Docs 可读可检索但默认不写、持续任务起始即建 LG 主档”是否在关键入口间一致；
- MOC、HOME、总纲、规范之间是否存在断链、重复路由或无效路径。

## 四、B：TileScape 执行与事实来源审查

### 必读范围

1. `AGENTS.md`
2. `.cursor/rules/agent-habits.mdc`
3. `Docs/Knowledge/README.md`
4. `Docs/Knowledge/Memory.md`
5. `Docs/Knowledge/CodeMap.md`
6. `Docs/Knowledge/TaskIndex.md`
7. `Docs/Knowledge/Governance.md`
8. 与本次任务相关的项目 `Docs/` / 源码旁 Markdown（仅在以上索引指向时读取）。

### 输出内容

- 本地文件的角色：代码约束、事实索引、历史设计、团队交付文档或本地暂存；
- 哪些内容是 AI 执行时必须读取/检索的项目事实；
- 其中哪些表述若被当作个人规范，会与 LG 当前规范冲突；
- LG 对应的入口：TileScape MOC、Docs 索引、快速定位、代码框架、任务档案或 Daily；
- 本地文档中已有的 LG 链接是否存在、是否是事实引用而非要求改写团队文件；
- 不提出“修改 TS 规则/Docs 以同步个人规范”的解决方案，只提出 LG 侧桥接或本机 AI 行为建议。

## 五、C：TileMatch / MT 执行与事实来源审查

### 必读范围

1. `client/AGENTS.md`
2. `client/.cursor/rules/agent-habits.mdc`
3. `02-PROJECTS/TileMatch/_MOC.md` 与 `参考/MT老项目路径索引.md`（在 LG 工作空间核对其对应入口）
4. 项目内由 `AGENTS.md`、LG 路径索引或任务实际需要指向的代码/源码旁 Markdown。

### 输出内容

与 TileScape 相同，重点标识：本地代码约束和事实来源、LG 入口是否足够、任何可能把本地材料误作个人规范源的表述，以及 MT 作为历史行为基线时的读取边界。

## 六、跨工作空间统一矩阵

执行反馈必须包含下表：

| 工作流环节 | LG 当前规范/入口 | TS 当前事实入口 | MT 当前事实入口 | 一致性 | 缺口或风险 |
|---|---|---|---|---|---|
| 冷启动读取 |  |  |  |  |  |
| 新建持续任务 |  |  |  |  |  |
| 活索引 / 快速查找 |  |  |  |  |  |
| 零碎任务 / INBOX |  |  |  |  |  |
| 项目 Docs 读取与检索 |  |  |  |  |  |
| 项目 Docs 写入边界 |  |  |  |  |  |
| 稳定结论 / Daily / MOC |  |  |  |  |  |
| 跨项目对位与代码事实 |  |  |  |  |  |
| WorkBuddy 执行与 Codex 验收 |  |  |  |  |  |

## 七、允许与禁止的产出

允许在 LG 当前任务目录创建：

`05-ARCHIVE/Agent/2026-09-04-AI工作流全面审查/执行反馈-三工作空间AI工作流规范全量审查.md`

该反馈必须包括：

1. 三个工作空间的证据清单；
2. 上述统一矩阵；
3. `已确认 / 待确认 / 无证据` 三类结论；
4. 规范角色清单和历史/任务包状态问题；
5. 推荐的**LG-only**修订任务清单，按 P0/P1/P2 排序；
6. 不修改 TS/MT 团队文件的声明。

禁止：

- 在 TS / MT 任一文件中写入个人规范、个人任务、个人 Daily、个人 MOC 或执行反馈；
- 创建或修改项目代码、资源、配置、团队 Docs、Git 配置；
- 把审查发现直接当作已确认规则；
- 提交或推送任何仓库。

## 八、Codex 验收标准

WorkBuddy 回传后，Codex 将检查：

1. 三个工作空间的结论均有精确路径和证据边界；
2. 角色分类没有把报告/计划/任务包误标为默认规范；
3. 统一矩阵覆盖全部九个环节；
4. 建议均为 LG 或本机 AI 流程调整，不包含未授权的 TS/MT 团队文件改动；
5. 对关键入口做静态路径与链接核对；
6. 不以静态审查替代未来实际任务创建行为的验收。

## 关联

- [[AI总MOC|AI 总 MOC]]
- [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]
- [[02-PROJECTS/Agent/工作流/规范-本机项目执行与LG知识库桥接|本机项目执行与 LG 知识库桥接规范]]
- [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]]
