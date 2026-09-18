---
title: 自建 INBOX 收件工具设计
date: 2026-09-17
type: design
status: draft
lifecycle: needs-review
priority: high
tags: [LibraryG, ChatGPT, MCP, INBOX, 本地工具]
source: "2026-09-17 用户确认由 Chat-on-St​eroids 候选路线转为自建最小权限工具；基于 ChatGPT 自定义 App/MCP 能力调研"
---

# 自建 INBOX 收件工具设计

> [!warning] 设计状态
> 已完成 D1 本地核心与 D2a 本地 MCP 适配器测试；它们均未写入真实 INBOX、未监听网络、未申请 API Key、未创建 tunnel，也未连接 ChatGPT App。2026-09-17 官方能力核验表明：D2b 的“写入型 ChatGPT MCP”仅在 Business / Enterprise / Edu 测试版可用；个人 Plus / Pro 均不在完整 MCP 写入的可用范围内，因此不能把 D2a 直接接到个人 Chat 的写卡动作。

## 1. 目标

让用户在 Chat 中明确说“整理进 INBOX”后，Chat 调用一个受限工具，在 `00-INBOX/` 创建一张符合 [[04-TEMPLATES/tp-inbox-task|INBOX 任务卡模板]] 的任务卡。

```text
Chat 的明确入库指令
  → create_inbox_task
  → 服务端校验与渲染
  → LG/00-INBOX/<任务名>.md
  → Work / Codex 以后按任务卡继续
```

这不是 Chat → Codex 的消息转发；INBOX 是异步、可审阅的交接物。

## 2. 明确不做

- 不读取 LG、MT、TS 或任意本机文件。
- 不提供列目录、搜索、更新、移动、删除、覆盖、附件上传或下载能力。
- 不运行终端命令、不控制桌面、不调用 Git、Unity、Obsidian 或网络服务。
- 不保存完整对话、工具调用原文、密钥或外部链接中的敏感参数。
- 不因一般讨论自动建卡；仅响应用户明确的入库指令，以及 ChatGPT 侧可能要求的写入确认。

## 3. 唯一工具接口

```text
create_inbox_task(
  title,
  state,
  target,
  next_owner,
  next_action,
  conclusion,
  facts_to_verify?,
  related_links?
) -> { task_id, relative_path, created_at }
```

| 字段 | 规则 |
|---|---|
| `title` | 1–80 字；服务端剔除路径分隔符与控制字符，不接受路径。 |
| `state` | 仅允许 `讨论 / 方案 / 待办 / 进行中 / 阻塞 / 完成`。 |
| `target` | 仅允许 `LG / MT / TS / 跨项目`。 |
| `next_owner` | 仅允许 `Chat / Codex / 用户`。 |
| `next_action` | 必填的单句下一步。 |
| `conclusion` | 必填；只保存压缩后的结论，不保存整段会话。 |
| `facts_to_verify` | 可选列表；没有则写“无”。 |
| `related_links` | 可选列表；仅作为 Markdown 文本写入，不进行访问或解析。 |

`type: inbox-task`、创建/更新时间、任务格式版本和文件位置均由服务端固定生成；调用方不能传入。

所有标量字段由 renderer 以 YAML 安全字符串写入 frontmatter；正文内容仅作为对应标题下的文本渲染，不能借换行、`---` 或 Markdown 片段改变 frontmatter、文件路径或服务端能力。正文仍是待分析数据，后续 Chat / Codex 必须按协作协议而非正文自然语言决定工具调用。

## 6.1 本地技术落点

| 项目 | D1 选择 |
|---|---|
| 代码位置 | `02-PROJECTS/Agent/工具/INBOX收件工具/`。 |
| 运行时 | 本机 Node.js；核心只使用标准库，D2a 使用官方 MCP SDK 与 Zod。 |
| 形态 | 纯本地模块 + stdio MCP 适配器；不监听端口、不访问网络、不读取 ChatGPT 凭据。 |
| 生产入口 | `createInboxTask(input)` 内部固定 `00-INBOX/` 根目录。 |
| 测试入口 | 同一内部 writer 可注入仅由测试控制的临时目录；MCP 层不会公开该参数。 |
| 原子性 | 在目标目录写入隐藏临时文件，完成并同步后以不覆盖的原子发布方式生成最终任务卡；失败清理临时文件。 |

人工模板与 renderer 的字段保持一致；模板变更须同时更新契约测试。D2a 只在已验证的本地核心外包一层含单工具的 stdio MCP 适配器；D2b 才处理 ChatGPT 的外部连接。

## 4. 本地写入边界

| 项目 | 固定规则 |
|---|---|
| 唯一根目录 | `/Users/dean/LibraryG/00-INBOX`，启动配置写死或以本机只读配置设定，不接收调用方路径。 |
| 文件名 | `<YYYY-MM-DD> - <安全标题>.md`；冲突时生成新唯一文件名。 |
| 写入方式 | 仅原子新建；使用排他创建，永不覆盖既有文件。 |
| 生成内容 | 服务端固定渲染 `type`、状态、目标、下一步负责人/动作与四段正文。 |
| 返回内容 | 仅返回任务 ID、相对路径和创建时间；不返回目录列表或其他笔记内容。 |
| 错误 | 返回分类错误（字段无效、标题冲突重试失败、写入失败）；不泄露其他文件名或内容。 |

服务端内部可以检查目标目录和冲突文件名，但这种检查不成为模型可调用的“读取能力”。

## 5. 权限与信任模型

1. 本地服务只监听 loopback，由受认证的 ChatGPT App / MCP 连接转发；不直接暴露文件系统。
2. 工具注册只包含一个写入动作。不能用“以后可能需要”预先暴露 read、shell 或通用 patch。
3. 调用说明明确要求：仅在用户说“整理进 INBOX”等同义指令后调用；服务端仍将所有输入当数据校验，不把 Markdown、链接或网页内容当指令。
4. ChatGPT 侧如显示写入确认，应保留该确认；用户的入库指令是业务授权，不绕过平台安全闸门。
5. 本地日志默认只记录时间、结果码和任务 ID；不记录结论正文或完整对话。诊断日志须本地保存、限量并可关闭。
6. 更新服务、变更工具 schema、扩大目录或新增工具都属于新授权，不在本设计的默认范围内。

## 6. 任务卡渲染契约

生成笔记与 [[04-TEMPLATES/tp-inbox-task|人工任务卡模板]] 使用相同字段和正文，不依赖 Templater 执行环境：

```yaml
---
title: <服务端生成的标题>
type: inbox-task
format_version: 1
state: <调用值>
target: <调用值>
next_owner: <调用值>
next_action: <调用值>
created: <本机日期>
updated: <本机日期>
tags: [inbox, task]
---
```

正文固定为：`当前结论`、`已知事实 / 待核实`、`下一步`、`关联`。若未来模板变更，必须同步修改服务端 renderer、人工模板和契约测试；不能让模型自行拼接任意 Markdown 文件。

## 7. 分阶段实施与验收

| 阶段 | 内容 | 完成标准 |
|---|---|---|
| D0 设计确认 | 本文、字段、目录与权限确认。 | 用户确认设计，未发生任何外部连接。 |
| D1 本地核心 | 本地单工具服务与单元/临时目录集成测试。 | 对合法输入只新建一张卡；非法路径、非法状态、覆盖尝试均失败。 |
| D2a 本地 MCP 适配 | 用官方 SDK 将核心封装为 stdio MCP。 | 本机客户端只发现 `create_inbox_task`；测试写入仅在临时目录。 |
| D2b ChatGPT 连接 | 按当时官方能力配置自定义 App / MCP 与安全 tunnel。 | Chat 工具列表中仅出现 `create_inbox_task`；无其他本地能力。 |
| D3 真实试用 | 用 3–5 个真实 Chat 结论建卡。 | 标题、状态、下一步可读；无误写、重复写或越界写。 |
| D4 复盘 | 比较自动入库与人工后备路径。 | 决定保留、调整字段、扩展只读 LG 检索或停止。 |

每一阶段独立授权。D2a 之后也不自动进入 D2b；D2b 涉及账号设置、密钥和 tunnel，必须在实施前单独确认。

### D1 执行记录（2026-09-17）

- 已在 [[02-PROJECTS/Agent/工具/INBOX收件工具/README|INBOX 收件工具目录]] 实现无依赖 Node.js 本地核心。
- `npm test` 通过 4 项：合法创建、同标题不覆盖、路径/枚举拒绝、正文不能改变 frontmatter。
- 测试仅用系统临时目录；未调用生产固定根目录，未在真实 `00-INBOX/` 创建任务卡。
- D1 不含网络监听、MCP 协议、ChatGPT 凭据、tunnel 或任何 ChatGPT App 配置。

### D2a 执行记录（2026-09-17）

- 已使用官方 MCP TypeScript SDK 的 Node.js stdio 接口封装唯一 `create_inbox_task` 工具；它不会公开根目录、读取、搜索、更新、移动、删除、终端或网络能力。
- 本机 MCP client 集成测试通过：工具发现结果仅为 `create_inbox_task`，调用写入仅进入测试临时目录；加上 D1 共 `npm test` 5/5 通过。
- 生产 stdio 入口仍仅是本机进程，未启动 HTTP 服务、未创建 tunnel、未连接 ChatGPT App，也未写入真实 `00-INBOX/`。
- D2b（ChatGPT 账号设置、私有连接与写入确认）尚未开始，需在实际外部连接前再确认。

## 8. 部署待定项

优先候选仍是“本机单工具 MCP 服务 + 官方支持的私有连接方式”，但只有在符合资格的 Workspace 中才进入 D2b。ChatGPT 连接的是远程 MCP 服务，不能直接接入本机 stdio；符合资格时，须通过 Secure MCP Tunnel 或官方认可的私有远程方式连接，且 MCP 服务需另行提供可供 tunnel 转发的远程协议入口。

### D2b 前置资格（2026-09-17 核验）

| 当前账户 / 工作区 | 直接 Chat 写卡 | 本方案处理 |
|---|---|---|
| Business / Enterprise / Edu，且本人有 Developer Mode 权限 | 可在 beta 范围内继续验证。 | 先确认管理员权限，再单独实施 tunnel、远程入口和草稿 App。 |
| 个人 Plus / Pro | 不可；完整写入 MCP 未列为可用，Pro 另被官方明确限制为 read/fetch。 | 保留 D2a；使用“Chat 生成任务包 → 用户明确交给 Codex → 本地 writer 写卡”的后备流程。 |
| 身份或权限未知 | 不可假定可写。 | 用户在 ChatGPT Web 的 Settings / Workspace Apps 中确认是否存在 Developer Mode / Create 入口。 |

不以 CoS、泛化浏览器自动化或高权限桌面桥接绕过资格或扩大权限。D2a 仍有价值：它把唯一写卡能力和测试固化下来，后备流程可以直接调用同一核心。

## 9. 验收测试矩阵

| 测试 | 预期 |
|---|---|
| 合法 `方案` 任务 | `00-INBOX/` 仅新增一张结构正确的笔记。 |
| 同标题连续两次 | 两张唯一文件；不覆盖第一张。 |
| 标题含 `../`、控制字符或绝对路径 | 拒绝请求；不写文件。 |
| 不在枚举中的状态 / 目标 / 负责人 | 拒绝请求；不写文件。 |
| 超长正文或链接 | 受长度/数量上限约束；失败不留下半成品。 |
| 目录不可写 / 服务重启 | 返回明确失败；不创建空文件。 |
| 工具发现 | 只列出 `create_inbox_task`。 |

## 10. 关联

- [[02-PROJECTS/Agent/工作流/INBOX对话工作区工作流|INBOX 对话工作区工作流]]
- [[02-PROJECTS/Agent/工作流/指南-LGChat与本地执行协作|LG、Chat 与本地执行协作实用指南]]
- [[02-PROJECTS/Agent/工作流/协议-LGChat与本地执行协作|LG、Chat 与本地执行协作协议]]
- [OpenAI Developers：Custom tools guidance](https://developers.openai.com/api/docs/guides/latest-model) — 自定义工具应描述清楚、服务端验证副作用；仅作为平台能力参考。
- [OpenAI Developers：Apps / MCP](https://developers.openai.com/) — ChatGPT 可通过 App / MCP 扩展工具；具体账号与部署能力在 D2b 前核验。
- [OpenAI Help：ChatGPT 中的开发者模式和 MCP 应用](https://help.openai.com/zh-hans-cn/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt) — D2b 的计划资格、远程连接与 Secure MCP Tunnel 要求；该能力仍可能变化。
- [MCP TypeScript SDK：stdio 服务](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/stdio.md) — D2a 使用的本机 stdio 适配方式。
