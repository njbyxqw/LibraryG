---
title: 多 Agent 任务上下文与交接规范
date: 2026-09-18
type: spec
status: current
lifecycle: current
priority: high
scope: local-personal-codex
source: "用户 2026-09-18 明确确认；基于现有 LG 工作流、TS/MT Git 现场与 Codex/Obsidian MCP 实测。"
tags: [LibraryG, Codex, Agent, Task, Worktree, Context, MCP]
---

# 多 Agent 任务上下文与交接规范

> 本文是 TS / MT 多 Agent 协作的唯一 current 入口。它只定义任务、上下文、交接和 Worktree 的最小协议；知识归属、Daily 和项目事实仍以现有 finalized 规范为准。

## 最小模型

```text
Task 卡 → 最小 Context → Worktree / 执行 → Artifact → Task 卡更新 → Proposal / Promote
```

- **LG**：长期知识、规范、决策、项目索引和 INBOX；不是运行时 scratchpad。
- **TS / MT**：当前代码、配置和实现事实；当前代码优先于 LG 历史记录。
- **Task**：唯一可恢复的交接载体；不以聊天记录或 Agent Memory 交接。
- **Artifact**：可审阅的 diff、branch/commit、验证记录或正式文档链接。
- **Agent Runtime**：会话、临时分析与 Worktree；不写成长期开箱即用的事实。

## 读取：只加载足够的上下文

1. 只读项目 `AGENTS.md` 中的团队约束，再读本机忽略的 `.agent/PROJECT.md`，确认项目根、Unity 根、事实优先级和禁止项。
2. 读取 Task 卡中列出的 `related_knowledge`、`related_code` 与验收条件。
3. 只有任务需要时，才从项目 MOC、LG MOC 或专题文档继续检索。
4. 不把 HOME、全部 Daily、完整 Memory、全部规则或历史聊天作为默认 Context。

项目 `AGENTS.md` 是团队公共文件，只能作为约束来源，未经用户逐次明确授权不得修改。`.agent/PROJECT.md` 是个人、本机的高信号项目地图；动态进度留在 Task 卡、Git 和当前代码中，不建立独立 `STATE.md`。

## Task 与 Artifact

Task 卡放在 `00-INBOX/` 根目录，仍使用既有六种状态：`讨论 / 方案 / 待办 / 进行中 / 阻塞 / 完成`。

除现有最小字段外，复杂任务补充：

```yaml
id: TS-123
project: TS | MT | 跨项目
scope:
related_knowledge: []
related_code: []
base_ref:
worktree:
artifact:
writeback_target: none | proposal | <LG path>
```

正文使用：`目标与范围`、`已确认事实`、`开放问题`、`交付与验收`、`执行记录 / Artifact`、`下一步`、`关联`。Task 卡只保存结论、证据和链接，不复制长分析或完整会话。

接手 Agent 的首轮只做只读 preflight：核对 Task、基线、脏改动、相关事实与验收条件。发生前提冲突、范围扩大或无关脏改动时，停止修改并回报。

## Worktree

- TS / MT 的代码修改任务默认使用 Codex Desktop 托管 Worktree；纯查询、SQL、方案和 LG 文档任务不创建 Unity Worktree。
- Worktree 从用户确认的 base ref / SHA 创建；不得默认携带人工主目录的未提交改动。
- Codex 托管 Worktree 默认是 detached HEAD。需要保留时再显式建立 `codex/<task-id>` 分支。
- 交付默认是 diff + 验证记录；commit / push 仍须用户明确授权。
- Unity 的 `Library`、`Temp`、`Logs`、`obj` 与 `.vs` 必须保持每个 Worktree 独立。`.worktreeinclude` 仅复制明确必需、可安全复制的忽略文件，绝不复制缓存、密钥或机器状态。
- 人工开发目录不作为 Agent 并行修改目标；同一分支不能同时 checkout 于两个 Worktree。

## LG 写回与 MCP

### 默认权限

| 动作 | 默认 |
|---|---|
| MOC / 项目知识 / INBOX 的读取与检索 | 允许 |
| 新建 INBOX Task 或 Proposal | 仅用户显式触发 |
| 修改已有 Task | 仅任务负责 Agent，且保留 Artifact / 状态依据 |
| 修改正式知识区 | 先 Proposal，人工确认后 Promote |
| 移动、删除、批量重写、Git commit/push | 用户明确确认 |

MCP 只是统一接口，不是文件权限墙。技术上要限制写入，执行 Agent 还必须没有 LG 正式知识区的直接写权限。

当前 Obsidian Local REST API with MCP 的接入仅开放 `vault_read` 与 `search_simple`。它使用本机 loopback 和 API key；`vault_patch`、写入、移动、删除和命令执行工具均不在 Codex 工具白名单中。检索先以 MOC 路由限定范围，再使用 `search_simple`；只有需要稳定的项目摘要时才考虑补充 `lg context`。

`search_simple` 的 Codex 输出上限为 1200 tokens，`vault_read` 为 4000 tokens。搜索必须先带项目或主题限定词；拿到路径后再用 `vault_read(path, target)` 精读，避免一次搜索把大量命中灌入 Context。

## 旧材料与过渡

- [[02-PROJECTS/Agent/工作流/指南-LGChat与本地执行协作|LG、Chat 与本地执行协作实用指南]] 与 [[02-PROJECTS/Agent/工作流/协议-LGChat与本地执行协作|LG、Chat 与本地执行协作协议]] 保留原文，改为 historical 追溯材料；不再作为执行入口。
- 原始版本可由本次改造前 Git revision `6d7d160a31ff65b2de2fe0eb3914c8a9d4d62d15` 恢复；本次不删除任何旧文档。
- 3–5 个真实任务后复核：首次正确 Context 所需轮次、重复检索、错误写回、Worktree 清理和交接恢复率。只保留经实际任务证明有价值的字段或自动化。

## 关联

- [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]]
- [[02-PROJECTS/Agent/工作流/规范-本机项目执行与LG知识库桥接|本机项目执行与 LG 知识库桥接规范]]
- [[02-PROJECTS/Agent/工作流/规范-多项目工作流与复现|多项目工作流与复现规范]]
- [[02-PROJECTS/Agent/工作流/INBOX对话工作区工作流|INBOX 对话工作区工作流]]
