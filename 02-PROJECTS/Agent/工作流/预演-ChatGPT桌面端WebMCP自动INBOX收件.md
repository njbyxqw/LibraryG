---
title: ChatGPT 桌面端 WebMCP 自动 INBOX 收件理论预演
date: 2026-09-17
type: preflight
status: draft
lifecycle: needs-review
priority: high
tags:
  - LibraryG
  - ChatGPT-Desktop
  - WebMCP
  - INBOX
  - preflight
source: "OpenAI 桌面端 Site Tools 官方说明；WebMCP Community Group Draft；尚未进行本机运行测试"
---

# ChatGPT 桌面端 WebMCP 自动 INBOX 收件理论预演

## 结论先行

“ChatGPT 桌面端对话 + 内置浏览器中的本机页面 + WebMCP”在技术链路上成立，但**尚不是已确认可用的个人 Plus 工作流**。

它只有同时通过下列硬门槛，才值得进入实现：

1. 内置浏览器中的本机页面实际暴露 `document.modelContext`，并能注册工具。
2. 当前 Plus 账号、所选模型和普通 Chat 会话能发现并调用该页面工具。
3. 本机地址满足 WebMCP 的 Secure Context 要求。
4. 每次建卡有可靠的用户授权边界；不能把模型传入的“用户说过整理进 INBOX”当作证明。
5. 工具页保持打开时，调用能只在受控测试目录创建卡片；随后才允许接到真实 `00-INBOX/`。

任一门槛失败，停止本路线，不用 custom MCP、tunnel 或 DOM 自动化去绕过；回到“浏览器扩展 + 本机显式确认”的候选方案。

## 目标与非目标

目标是：用户在 Chat 中明确说“整理进 INBOX”后，Chat 调用**唯一**的 `create_inbox_task` 工具，在固定目录新建一张任务卡。

不包含：读取仓库、列出/修改既有卡片、执行命令、写入 LG 其他目录、转交 Codex、自动启动 Work，或让模型选择写入根目录。

## 理论架构

```text
ChatGPT 桌面端的当前会话
  + 内置浏览器打开本机 INBOX 页面
      └─ 页面以 document.modelContext.registerTool 声明
         create_inbox_task（唯一工具）
              └─ ChatGPT 发现并请求调用
                   └─ 页面 handler 调用同源 /v1/inbox-tasks
                        └─ 仅监听 127.0.0.1 的 helper
                             └─ 复用固定规则 writer
                                  └─ 仅新建 LibraryG/00-INBOX/ 任务卡
```

页面没有任意文件权限；文件系统动作由 helper 和已有 writer 执行。生产模式的写入根目录固定在 helper 内部，绝不出现在工具参数中。

## 关键预演与判定

| 门槛 | 为什么会卡住 | 通过证据 | 失败后的决定 |
|---|---|---|---|
| H1：WebMCP API | 规范要求 Secure Context；官方未承诺本机 HTTP 页可用。 | 内置浏览器中 `document.modelContext` 存在，页面能注册工具。 | 不做 polyfill；先单独评估本机 HTTPS，未获批准不继续。 |
| H2：工具发现 | 官方仅称账号、模型和当前页面“支持时”可发现 Site Tools，未承诺 Plus。 | 地址栏出现工具箭头，且工具列表仅含本工具。 | 放弃桌面路线，不以 custom MCP 绕过。 |
| H3：普通会话调用 | 发现工具不等于正常 Chat 会话一定能调用。 | 用户在普通对话中触发一次受控测试调用。 | 保留网页扩展候选，不做生产代码。 |
| H4：授权可见性 | WebMCP handler 只收到参数，无法验证自然语言中的真实意图。`consequentialHint` 只是让客户端可选择确认的提示，不保证确认。 | 实测每次调用有清晰的 ChatGPT 确认；或用户另行确认接受本机页面的显式二次确认。 | 不允许“说一句话即静默写卡”。 |
| H5：测试隔离 | 首次成功也不应污染真实知识库。 | 同一工具在测试模式只能向临时目录写一张可删除测试卡；工具参数不能指定路径。 | 不连真实 `00-INBOX/`。 |
| H6：页面生命周期 | 官方说明工具仅属于当前打开页面，关页或离页就不可用。 | 固定打开的本机页能稳定保留工具。 | 若必须长期保持页面违反使用习惯，放弃本路线。 |
| H7：最小权限 | helper 若有读接口、可选路径或泛化命令，就超出需求。 | 只有建卡 POST；绑定 `127.0.0.1`；无列举、读取、删除和命令接口。 | 缩回单一写卡能力后再评审。 |

### 关于 localhost 与 Secure Context

WebMCP 规范把 API 标为 Secure Context，但没有在规范中保证 ChatGPT 内置浏览器对 `http://127.0.0.1` 或 `http://localhost` 的处理。常见浏览器对 localhost 的惯例不能替代实测。

因此 D1 先验证 API 是否存在；若不存在，不临时添加证书、代理或公网暴露。是否设计本机 HTTPS 是一个新的授权决策，而不是实现过程中顺手补的步骤。

### 关于“用户说过整理进 INBOX”

模型可以把 `intent: "用户已确认"` 放进参数，但页面与 helper 无法从这个字符串证明对话中真的发生过授权。工具描述也可能被误解或被页面内容诱导。

所以安全边界应为：工具标记 `consequentialHint: true`，并以平台实际呈现的确认作为首选；如果平台不确认，则改成用户点击本机页面的明确确认。后者会牺牲“完全一句话自动”，但不会伪造授权。

## 唯一工具契约

```text
name: create_inbox_task
annotations:
  readOnlyHint: false
  consequentialHint: true
  untrustedContentHint: false

input:
  title                 非空短标题
  state                 讨论 | 方案 | 待办 | 进行中 | 阻塞 | 完成
  target                LG | MT | TS | 跨项目
  owner                 Chat | Codex | 用户
  summary               任务结论或待办摘要
  proposal              可选方案正文
  acceptance_criteria   可选验收条件数组
  source_conversation   可选对话链接或标识

output:
  task_id
  created_at
  relative_path
```

输入使用严格 schema：未知字段、非法状态、空标题和过长正文均报错且零写入。`root`、`path`、`filename`、Shell、读取或删除能力均不在 schema 中。

首轮验证也不新增 `inbox_receiver_status` 等第二工具：仍只暴露最终名称 `create_inbox_task`，但 helper 以测试模式启动，内部写入临时根目录。模型无权切换测试/生产根目录。

## 分阶段执行，不提前越界

| 阶段 | 做什么 | 写入边界 | 继续条件 |
|---|---|---|---|
| D0：本预演 | 明确假设、硬门槛、失败出口。 | 无服务、无页面、无文件卡。 | 用户认可。 |
| D1：能力探针 | 本机极小页面注册唯一建卡工具，helper 固定测试根目录；完成一次可见调用。 | 仅临时目录的一张测试卡，不触及 LG `00-INBOX/`。 | H1–H6 全部有实证。 |
| D2：最小收件器 | 完善 schema、重复提交保护、错误呈现和测试。 | 仍是测试根目录。 | 连续多次测试无越权写入。 |
| D3：生产接线 | 将 helper 的固定根目录改为 LG `00-INBOX/`。 | 只新建任务卡。 | 用户单独确认真实写入与确认交互。 |
| D4：日常试用 | 以真实小任务观察摩擦、误触发、卡片质量。 | 固定 INBOX。 | 决定保留、调整或回退。 |

> [!info] 当前实现状态（2026-09-17）
> D1 的最小探针代码已就绪：`02-PROJECTS/Agent/工具/INBOX收件工具/src/webmcp-probe.mjs`。它只绑定 `127.0.0.1:38741`，每次启动在系统临时目录创建固定测试根目录，并仅注册 `create_inbox_task`。本地单元测试已覆盖单一工具声明与测试写卡边界；尚未启动服务、未在 ChatGPT 桌面端打开页面，因此 H1–H6 仍全是待验证状态。

> [!success] D1 首次实测（2026-09-17）
> 探针已在当前桌面应用内置浏览器打开，页面检测到 `document.modelContext`，并被浏览器发现为唯一 `create_inbox_task` 工具。随后以固定输入成功调用，返回 `taskId: 8bbe332f-147e-4dcb-a58a-1a083fa2d3f9` 与 `2026-09-17 - WebMCP 首次测试.md`；按 D1 设计，该卡只在本次进程的系统临时根目录。由此 H1、H2 和受控测试写卡路径获得实证。此次调用由当前 Codex 对话的浏览器工具适配层发起，不等同于确认“普通 Chat 自然语言可自动选择工具”，也未观察到面向用户的平台确认弹窗；H3、H4、H6 仍待单独验证。

> [!info] H4 的本地确认实现（待重启后实测）
> 历史探针曾在每次 `create_inbox_task` 调用前显示原生确认框，展示标题、状态、目标和“只写临时目录”；取消即抛错且零写入。该探针已于 2026-09-18 归档，不再提供 `npm run probe:webmcp` 运行入口；实现与测试保留在 [[05-ARCHIVE/Agent/INBOX收件工具-历史验证-2026-09-18/README|历史验证归档]]，仅供追溯。

> [!success] H4 第二次实测（2026-09-17）
> 重启后页面已显示“每次建卡将由本机页面再次确认”。调用 `create_inbox_task` 创建 `WebMCP 确认层测试` 时，用户确认看到了原生弹窗并选择确认；调用成功返回 `taskId: c15e063a-3bcb-4e73-94b9-c2c95472f8fd` 与 `2026-09-17 - WebMCP 确认层测试.md`，同样只在临时根目录。浏览器自动化侧未能读取该弹窗（`getJsDialog()` 为无），因此自动化不能代替或审计用户点击；但用户可见确认本身已获实证。

> [!success] H4 取消路径实测（2026-09-17）
> 随后触发 `WebMCP 取消确认测试`，用户在同一原生确认框选择取消。调用在 `fetch` 前以“用户取消创建测试卡”拒绝，未进入 helper 写卡接口。浏览器工具桥因未捕获的取消拒绝重置，未能在该轮枚举临时目录；因此“未调用写卡接口”有运行时错误和源码顺序证据，“临时目录绝对为空”未作独立枚举验证。这个边界足以说明生产设计应把页面确认作为唯一写卡闸门，且不得让工具调用绕过它。

> [!success] 自然语言整理到任务包实测（2026-09-17）
> 根据本对话已经形成的验证结论，当前助手将其归纳为标题、状态、目标、下一步、结论和待验证项，再调用同一工具；用户在页面确认后成功创建 `2026-09-17 - 桌面端 WebMCP INBOX 收件验证.md`（`taskId: c1f8d78a-bab1-4d00-98de-92d6192ddf6e`），仍仅在临时根目录。这证明“聊天结论 → 受限结构化任务包 → 用户页面确认 → 建卡”的链路完整。它不单独证明任意普通 Chat 会话会自行选择工具；工具选择规则和生产卡片质量仍需 D4 日常试用验证。

> [!info] D2 实现完成，待端到端验证（2026-09-17）
> 探针新增同进程重复提交保护：对验证后的任务字段生成内部摘要；相同输入再次到达 helper 时，不建第二张卡，而返回第一次的 `taskId`、相对路径和 `reused: true`。页面同时显示待创建、已创建、已取消、失败或“未重复创建”。`npm test` 7/7 通过，包含“相同输入只在临时根目录生成一张卡”的直接测试。该保护尚未跨进程持久化，重启后是否去重属于 D3 生产设计问题；运行中的旧探针也尚未加载 D2，需要重启后才做端到端重放测试。

> [!success] D2 端到端重放测试（2026-09-17）
> 用户重启探针后，对完全相同的 `WebMCP D2 重复提交验证` 连续两次在页面确认。第一次返回 `taskId: 0a7b6e28-14ac-44a4-abbf-2c178e5d83e4`、`relativePath: 2026-09-17 - WebMCP D2 重复提交验证.md`、`reused: false`；第二次返回相同 ID 和路径、`reused: true`。由此确认同进程重放不会新建第二张临时卡。跨进程重放仍未验证，也不应在未设计持久收据前接入真实 `00-INBOX/`。

## 失败决策树

```text
内置浏览器没有 document.modelContext / 工具箭头？
  → 停止桌面路线；不做 MCP/tunnel/DOM 绕过

工具被发现，但 Plus 普通会话不能调用？
  → 停止桌面路线；保留网页扩展候选

可以调用，但没有可靠确认？
  → 不做静默写卡；仅在用户接受页面二次确认时继续

测试目录能稳定建卡？
  → 再评审 D2，不能直接接真实 INBOX

测试中出现路径逃逸、重复写入或工具页不稳定？
  → 修复或放弃；不得进入 D3
```

## 与网页扩展候选的取舍

桌面 WebMCP 的优点是无需读取 ChatGPT 网页 DOM，也无需浏览器扩展权限；风险则集中在平台、账号、模型和本机页面支持尚未证实。网页扩展路线对平台 Site Tools 依赖更少，但需要维护页面 DOM 适配和扩展权限。

因此当前排序是：先用 D1 以极小代价验证桌面路线；验证失败即回退网页扩展，不把两条路线混合实现。

## 资料边界

- [OpenAI：在 ChatGPT 桌面应用中使用网站工具](https://help.openai.com/zh-hans-cn/articles/20001423-using-site-tools-in-the-chatgpt-desktop-app) — 证实内置浏览器的 Site Tools 机制及其页面/账号/模型依赖。
- [WebMCP Community Group Draft](https://webmachinelearning.github.io/webmcp/) — `document.modelContext`、工具注册、Secure Context 与工具注解的规范来源。
- [[方案-ChatGPTPlus自动INBOX收件器]] — 浏览器扩展默认候选与两条路线的上下文。

> [!warning] 验证边界
> 本文是理论推演，不证明任何本机页面、Plus 账号或模型已具备 WebMCP 能力，也没有创建、修改或测试真实 INBOX 任务卡。
