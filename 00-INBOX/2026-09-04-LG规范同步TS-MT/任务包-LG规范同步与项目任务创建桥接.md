---
title: 任务包：LG 规范同步与项目任务创建桥接
date: 2026-09-04
type: implementation-task
status: superseded
priority: critical
projects: [LibraryG, TileScape, TileMatch]
source: "用户 2026-09-04 明确确认：LG 是唯一知识库与规范源；TS / MT 必须同步 LG 最新规范"
verification: "WorkBuddy 静态检查 + Codex 实际任务创建验收"
tags: [LibraryG, TS, MT, 规范同步, 任务创建, AI, WorkBuddy]
---

# 任务包：LG 规范同步与项目任务创建桥接

> [!warning] 已替代，禁止执行
> 用户于 2026-09-04 明确：TS / MT 的 `AGENTS.md`、`.cursor/rules` 与项目 Docs 属于团队协作文件，个人知识库需求不得写入其中。本包原 Step 2、Step 3 的项目仓库修改不再授权执行。改用 [[02-PROJECTS/Agent/工作流/规范-本机项目执行与LG知识库桥接|本机项目执行与 LG 知识库桥接规范]]；项目 Docs 默认可读可检索、但不写入个人任务/规范。

## 一、目标与唯一原则

> **LG 是唯一知识库与规范源。TS、MT 是项目执行空间与代码事实来源。**

本任务的目标不是把 LG 的完整规范复制进两个项目，而是在 TS / MT 的 AI 冷启动入口建立强制桥接：凡涉及任务创建、知识入库、归档、MOC、Daily、INBOX、跨项目查找或自动化，必须先读取 LG 的**当前文件**，再返回项目执行。

本地规则只保留代码约束、技能入口和最短桥接，不得形成可替代 LG 的第二套知识库规范。

## 二、必须落实的行为

### 1. 新建任务门槛

当用户在 TS 或 MT 中说“新建任务 <主题>”时，AI 必须先判断：

| 情景 | 正确行为 |
|---|---|
| 持续项目任务 | 预计跨天、需要反复跟进背景/设计/进度/讨论/实现/验证。先读 LG 项目 MOC，在 `LibraryG/02-PROJECTS/<项目>/<领域>/任务-<主题>.md` 建立唯一主档案，再回项目写代码或本地材料。 |
| 活索引 / 快速查找 | 先进入 LG 项目 MOC 的对应索引，在已有索引中补条目；不在项目本地另建同类索引。 |
| 零碎临时工作 | 默认只留对话；只有需要跨回合保存的原始材料才使用 LG `00-INBOX/`。 |
| 纯局部编码 | 不必为一次小改动新建任务文档；但一旦形成持续任务或稳定结论，立即按以上规则进入 LG。 |

本地 `Docs/`、`Docs/Knowledge/Local/`、源码旁 Markdown 只能保存代码旁说明、团队交付文档或原始临时材料；如果关联持续任务，必须链接 LG 主档案，不能取代它。

### 2. 强制读取链

```text
TS / MT 项目入口
  → LG/AGENTS.md
  → LG/AI总MOC.md
  → LG 对应项目 _MOC.md
  → （按任务）LG 入库规范 / 多项目规范 / 项目专题 MOC
  → 回到 TS / MT 代码与本地执行索引
```

LG 最新文件即时生效；本地不得复制完整规则正文或以本地版本号替代读取 LG。

## 三、WorkBuddy 执行步骤

### Step 0：范围与保护

1. 只修改下列明确列出的 Markdown / 规则文件，不修改业务代码、资源、配置或 Git 历史。
2. 不 commit / push。
3. 写入前读取 LG `AGENTS.md`、`AI总MOC.md`、`02-PROJECTS/Agent/工作流/规范-任务产出入库与维护.md`。
4. 任何目标文件、锚点或路径不符时停止该项，报告 `needs-review`；不得临场发明第二套规则。

### Step 1：LG 建立规范桥接的正式入口

创建：

`/Users/dean/LibraryG/02-PROJECTS/Agent/工作流/规范-项目执行空间与LG规范同步.md`

必须写明：

- LG 唯一规范源，TS / MT 是执行空间与事实来源；
- 哪些任务必须先回 LG；
- 三类任务的创建与存放规则；
- 本地文档的允许范围和“必须回链 LG 主档案”的要求；
- LG 规则更新后，本地桥接只需保持指向当前 LG 文件，不复制规则正文；
- 静态同步检查和实际“新建持续任务”验收方式。

更新：

- `02-PROJECTS/Agent/工作流/_MOC.md`：在 `current` 路由表增加“TS / MT 规范同步与任务创建桥接”入口；
- `AI总MOC.md`：任务路由增加“TS / MT 项目任务创建、规范同步”入口；
- `02-PROJECTS/Agent/工作流/规范-任务产出入库与维护.md`：只补一条到该桥接规范的关联，不重复规则正文。

### Step 2：TileScape 入口桥接

修改目标：

1. `/Users/dean/TileScape/AGENTS.md`
2. `/Users/dean/TileScape/.cursor/rules/agent-habits.mdc`
3. `/Users/dean/TileScape/Docs/Knowledge/README.md`
4. `/Users/dean/TileScape/Docs/Knowledge/Governance.md`

写入要求：

- `AGENTS.md` 增加一个简短“LG 规范桥接”段落：其只说明本地是项目执行入口；任务创建、知识入库、归档、MOC、Daily、INBOX、跨项目任务和自动化必须先读取 LG 当前入口。LG 根目录从 TS 项目根按 `../LibraryG` 定位；不要在此复制 LG 规则正文。
- `agent-habits.mdc`（`alwaysApply: true`）增加“任务创建门槛”：用户提出新建持续任务或活索引时，先按 TS `AGENTS.md` 的 LG 桥接进入 LG，主档案写到 LG TileScape 路径；本地仅保留允许的执行材料。
- `README.md` 的“写入边界”增加“持续任务从开始在 LG 建主档”的句子；本地知识目录改为 LG 的执行索引，不表述为本地长期知识库。
- `Governance.md` 删除或改写“大型专题文档继续放在 Docs”的泛化规则：只有需团队评审/随代码交付的文档留在 Docs；项目稳定结论与任务主档案必须在 LG。把“任务收尾后提炼到 LG”改为“任务开始在 LG 建主档，收尾回写该主档”。

### Step 3：TileMatch / MT 入口桥接

修改目标：

1. `/Users/dean/Downloads/meatloaf_client/client/AGENTS.md`
2. `/Users/dean/Downloads/meatloaf_client/client/.cursor/rules/agent-habits.mdc`

说明：MT 的 `AGENTS.md` 已有“LG 是唯一知识库与规范源”的基础桥接；本步只补足新建任务门槛，不重写既有项目执行说明。

写入要求：

- `AGENTS.md` 明确：用户提出持续项目任务、活索引或知识整理时，先读 LG 当前入口和 `02-PROJECTS/TileMatch/_MOC.md`，在 LG 建主档/更新索引；纯局部编码例外不建任务文档。
- `agent-habits.mdc` 加入与 TS 等价的 `alwaysApply` 任务创建门槛；本地规则不得覆盖 LG。
- 从 MT `client` 项目根到 LG 的相对路径是 `../../../LibraryG`。若执行环境不满足该目录关系，停止并报告 LG 根路径不可用，不得回退为本地任务主档案。

### Step 4：现有本地误建任务的处理边界

本任务**不自动移动、删除或重命名**已在 TS / MT 本地创建的任务文档。

对用户指出的本次 TS 本地任务，WorkBuddy 只做以下准备：

1. 报告其精确路径、是否被 Git 跟踪、是否已有 LG 对应任务主档案；
2. 若用户确认它属于持续任务，后续单独任务包在 LG 建主档，并在本地文件顶部补 LG 主档链接；
3. 不依据文件修改时间猜测哪个文档是“刚创建的任务”。

## 四、验证与验收

### WorkBuddy 静态检查

1. TS / MT 两边的 `AGENTS.md` 与 `agent-habits.mdc` 都能找到 LG 桥接、任务创建门槛和“不以本地规范替代 LG”的表述。
2. TS `README.md` / `Governance.md` 不再把本地 Docs 描述为持续任务主档案或独立长期规范源。
3. LG 新规范可从 `AI总MOC → Agent 工作流 MOC` 到达。
4. 所有新增跨目录链接存在；不修改业务代码，不 commit/push。

### Codex 实际行为验收（必须）

在 TS、MT 各做一次全新任务创建情景，不使用既有对话上下文：

| 情景 | 预期结果 |
|---|---|
| TS：`新建任务 DLC 验收演练`，明确持续数天 | AI 先读 LG，并在 `LibraryG/02-PROJECTS/TileScape/游戏逻辑/` 建主档案；TS 仅在确需时建立并回链本地执行材料。 |
| MT：`新建任务 障碍机制对照验练`，明确持续数天 | AI 先读 LG，并在 `LibraryG/02-PROJECTS/TileMatch/游戏逻辑/` 建主档案。 |
| TS / MT：一次性小排查 | AI 不强造任务文档；若需保存原始材料，明确使用 LG INBOX。 |

任一情景仍把持续任务主档案默认建在 TS / MT 本地，则验收不通过，回到桥接规则修订，不以事后迁移作为通过条件。

## 五、禁止项

- 不在 TS / MT 复制完整 LG 规范正文、Daily、Memory、MOC 或 WorkBuddy 流程。
- 不用本地 `Docs/Knowledge`、`.workbuddy/memory` 或源码旁 Markdown 覆盖 LG 最新规则。
- 不移动、删除或覆盖现有任务文档。
- 不创建空的项目任务主档案来冒充验收通过。
- 不改业务代码、Git 配置、提交或推送。

## 六、WorkBuddy 回传格式

1. 每个修改文件的完整路径与变更摘要；
2. LG / TS / MT 各自桥接入口的摘录；
3. 静态检查结果、链接检查结果、未执行项；
4. 本地误建任务的候选清单（仅路径与跟踪状态，不作个人工作推断）；
5. 明确声明：未改业务代码，未移动/删除任务文档，未 commit/push。

## 关联

- [[AI总MOC|AI 总 MOC]]
- [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]
- [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]]
- [[00-INBOX/2026-09-03-知识库内容归属与MOC路由整理/AI任务规划-知识库后续治理|前序 AI 任务规划]]
