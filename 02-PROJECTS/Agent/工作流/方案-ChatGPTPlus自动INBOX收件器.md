---
title: ChatGPT Plus 自动 INBOX 收件器设计
date: 2026-09-17
type: design
status: draft
lifecycle: needs-review
priority: high
tags: [LibraryG, ChatGPT-Plus, Chrome-Extension, INBOX, 本地自动化]
source: "2026-09-17 用户确认重设目标：Chat 形成方案后自动导出本地；GitHub 页面扩展与 localhost helper 实践调研"
supersedes: "[[02-PROJECTS/Agent/工作流/方案-ChatGPTPlus环境INBOX收件与交接]] 的手动任务包默认路线"
---

# ChatGPT Plus 自动 INBOX 收件器设计

> [!abstract] 一句话目标
> 在 **ChatGPT 网页版**中，用户明确说“整理进 INBOX”后，Chat 生成固定任务包；浏览器扩展只读取当前最后一轮，自动交给本机 helper 校验，并且仅在 `00-INBOX/` 新建一张任务卡。

> [!warning] 产品边界
> 这是浏览器页面收件器，不是 ChatGPT MCP：它不要求 Plus 获得写入型 MCP，不使用 tunnel，也不让 ChatGPT 直接拥有本机文件权限。若用户日常只使用 ChatGPT 桌面端而不使用 Chrome / Edge 网页版，此方案不适用。

> [!question] 桌面端候选（待验证，不替代本文默认方案）
> ChatGPT 桌面应用的内置浏览器新增了 Site Tools / WebMCP：若账号、模型和页面均支持，打开的网页可以向 ChatGPT 提供工具。因此可另行验证“本机 INBOX 页面在内置浏览器中提供唯一建卡工具”的路线。官方资料没有确认个人 Plus、普通 Chat 会话或 `localhost` 页面均可使用它；在实际发现工具箭头、完成一次隔离测试调用前，不把它列为可用能力。完整硬门槛见 [[预演-ChatGPT桌面端WebMCP自动INBOX收件]]。

### 与 Chat-on-St​eroids 的机制差异

| 项目 | Chat-on-St​eroids（CoS） | 桌面端 Site Tools / WebMCP 候选 |
|---|---|---|
| Chat 所在位置 | Chrome / Edge 的 ChatGPT 网页；CoS 自己的 Electron 只是本地控制台。 | ChatGPT 桌面应用 + 其内置浏览器。 |
| 工具如何被发现 | ChatGPT custom MCP app 经 tunnel 连接 CoS 的本机 MCP server。 | 当前打开的本机网页自行向内置浏览器声明 WebMCP site tool。 |
| 本地动作路径 | ChatGPT → tunnel → CoS Core → 文件 / 终端 / Desktop 等能力。 | ChatGPT → 当前网页的 `create_inbox_task` handler → 同源 localhost helper → 固定 writer。 |
| 浏览器伴侣 | Chrome extension 观察、自动化 ChatGPT DOM，并记录会话 / 工具关联。 | 不需要读取或抓取 ChatGPT 对话 DOM。 |
| Plus 前提 | 当前文档要求 Developer Mode 和 custom MCP apps；不适用于个人 Plus 的写入 MCP。 | 未知，必须实际验证 Site Tools 对账号、会话和 localhost 页面的支持。 |
| 权限面 | Core 含文件、patch、终端、会话、worker，另可启用 Desktop / Plugins。 | 设计上只有一个页面工具和一个固定目录的新建动作。 |

CoS 的扩展不会直接给 ChatGPT 文件权限；本地权限来自 CoS 的 Core MCP。扩展负责识别/配对 ChatGPT 网页会话、观察并自动化 DOM、记录消息和把实际工具结果关联回页面。CoS 官方也明确该浏览器自动化不是公开 ChatGPT API，且会本地记录会话内容；因此不作为本需求的权限模型。

### WebMCP 候选的精确链路

```text
ChatGPT 桌面应用的某个会话
  + 内置浏览器打开 http://127.0.0.1:<port>/inbox
      └─ 页面声明 site tool：create_inbox_task
          └─ ChatGPT 发现工具（地址栏箭头）
              └─ 用户说“整理进 INBOX”后，模型请求该工具
                  └─ 页面 handler 调同源 localhost API
                      └─ helper 校验任务包，只新建 00-INBOX 任务卡
```

网页本身不具有任意文件权限；实际写卡仍由同机 helper 完成。页面与 helper 可同源部署，因而无需浏览器扩展、跨网 tunnel 或 API key。模型发起工具调用仍会受 ChatGPT 的网站权限/确认机制约束。

首个验证仍只声明最终名称 `create_inbox_task`，不增加状态、读取或列表工具；但 helper 固定为测试模式，只能向临时目录创建一张可丢弃测试卡，工具参数不能选择根目录。只有在桌面端内置浏览器确实出现 Site Tools 箭头、当前对话能发现工具且用户确认边界清楚后，才评估生产接线。若任一前提不成立，回到本文默认的网页扩展方案。

## 1. 已确认需求

| 编号 | 需求 | 设计回应 |
|---|---|---|
| R1 | 方案讨论留在 Chat，避免为讨论消耗 Codex 工作额度。 | Chat 负责收敛方案；本机不参与讨论。 |
| R2 | 用户说“整理进 INBOX”后，不应再复制到 Codex。 | 页面扩展检测明确触发和任务包，自动发给本机 helper。 |
| R3 | 本地能力只能创建 `00-INBOX` 任务卡。 | helper 只有一个写入路由；固定根目录、只新建、永不覆盖。 |
| R4 | 任务卡不是自动执行授权。 | 任务卡的 `state`、`next_owner`、`next_action` 只记录后续入口；不触发 LG / MT / TS 读取或修改。 |
| R5 | 不保存整段聊天、不上传资料、不增加高权限工具。 | 扩展只提取最后一条有效任务包；helper 只绑定 `127.0.0.1`，无云端、无终端、无桌面控制。 |
| R6 | 长期可维护，页面变化时不能静默误写。 | 固定任务包协议、严格校验、消息指纹去重、失败可见、页面 fixture 回归测试。 |

## 2. 用户体验

### 正常路径

1. 用户在 ChatGPT 网页版完成讨论。
2. 用户发送：`整理进 INBOX`。
3. Chat 只回复一份固定 JSON 任务包。
4. 扩展确认“最后一个用户触发 + 最后一个完整助手任务包”成对出现。
5. helper 新建 `00-INBOX/YYYY-MM-DD - <标题>.md`。
6. 扩展显示“已保存：<相对路径>”。

用户不需要进入 Codex，也不需要复制粘贴。聊天、建卡、后续实施仍是三种独立授权。

### 不确定路径

任务包缺字段、Chat 仍在生成、页面结构无法可靠定位、helper 未运行、令牌不匹配或写入失败时：**不创建文件**。扩展显示原因，并提供“复制任务包”而非自动重试或保存整段会话。

## 3. Chat 任务包协议

只有用户明确触发后，Chat 才应在回复中仅输出一个 `json` 代码块：

```json
{
  "format_version": 1,
  "intent": "create_inbox_task",
  "title": "简短任务名",
  "state": "方案",
  "target": "LG",
  "next_owner": "Codex",
  "next_action": "核对当前实现与方案的差异。",
  "conclusion": "压缩后的当前结论。",
  "facts_to_verify": [],
  "related_links": []
}
```

允许值与 [[02-PROJECTS/Agent/工作流/方案-自建INBOX收件工具|本地 writer 契约]] 一致：

- `state`：`讨论 / 方案 / 待办 / 进行中 / 阻塞 / 完成`
- `target`：`LG / MT / TS / 跨项目`
- `next_owner`：`Chat / Codex / 用户`

扩展不相信自然语言解释，也不从普通 Markdown、附件、网页内容或历史消息中猜任务；它只接受最后一条助手消息内、恰好一个、通过 JSON schema 的代码块。

## 4. 架构与权限

```text
ChatGPT Web 当前对话
  └─ Chrome / Edge 扩展
       - 只读取 chatgpt.com 当前最后一轮
       - 不发送提示词、不控制浏览器、不保存历史
       - POST 结构化任务包
                ↓ 127.0.0.1 + 扩展专属随机令牌
       本机 INBOX helper
       - JSON schema + 触发/去重校验
       - 调用固定根目录 writer
                ↓
       /Users/dean/LibraryG/00-INBOX/<新任务卡>.md
```

### 浏览器扩展

- 最小 host permission：`https://chatgpt.com/*` 与 helper 的 `http://127.0.0.1:<固定端口>/*`；不请求 all-sites、下载、原生消息、浏览器控制、剪贴板或文件 URL 权限。
- 只观察当前活动 ChatGPT 标签页；不扫描其他标签、私密窗口、附件或上传内容。
- 触发条件为最后一条用户消息精确包含约定口令、其后最后一条助手消息含唯一有效任务包、并且回复已停止生成；等待短暂稳定窗口后再发一次。
- 对 `conversation_id + 用户消息指纹 + 助手任务包哈希` 去重。重载、页面切换和网络重试不能新建第二张卡。
- 只显示成功、失败和“复制任务包”反馈；不把完整任务正文写入扩展日志或同步存储。

### 本机 helper

- 只监听 `127.0.0.1` 固定端口；不监听局域网或公网，不使用 MCP、tunnel、Obsidian REST API 或云端 API key。
- 唯一动作是 `POST /v1/inbox-tasks`；无任务列表、文件读取、更新、删除、目录配置、shell 或插件接口。
- 请求必须同时满足：本机扩展来源、随机 bearer token、严格 schema、最大请求体和去重条件。失败信息不得暴露现有任务卡内容或目录列表。
- token 由首次本机设置生成，保存在用户私有配置中并排除 Git；扩展只持有该本机 token，不持有 OpenAI、Obsidian 或项目凭据。
- 复用现有 [[02-PROJECTS/Agent/工具/INBOX收件工具/README|INBOX writer]] 的校验、YAML 安全渲染、临时文件和不覆盖发布逻辑；目前的 MCP stdio adapter 不参与此架构。

## 5. 风险与防护

| 风险 | 防护 | 验收证据 |
|---|---|---|
| Chat 页面 DOM 改版 | 仅提取固定代码块；以保存的页面 fixture 测试；无法定位就不写。 | fixture 测试、可见失败提示。 |
| 模型输出错误 / 注入内容 | 任务包 schema、固定枚举、长度限制、服务端数据化渲染。 | 非法包零写入测试。 |
| 重复保存 | 成对消息指纹 + helper 幂等记录 + writer 不覆盖。 | 重试 / 刷新仅一张卡测试。 |
| 本机其他网页调用 helper | loopback、来源限制、随机 token、仅一个 POST。 | 缺 token / 错来源均拒绝。 |
| 扩展权限过宽 | 不采用现成全功能桥接；manifest 最小权限审查。 | manifest 审查清单。 |
| 用户误触发 | 只匹配明确口令与任务包；设置内可关闭“自动保存”，关闭时显示保存按钮。 | 自动 / 手动模式测试。 |

## 6. 实施阶段与闸门

| 阶段 | 范围 | 不做 | 进入闸门 | 验收 |
|---|---|---|---|---|
| D0 设计确认 | 本文、任务包格式、权限清单。 | 不写扩展/helper。 | 用户确认。 | 明确浏览器、触发词、自动/手动默认。 |
| D1 helper | 复用 writer，增加本机单 POST adapter 与临时目录协议测试。 | 不监听真实端口、不写真实 INBOX。 | D0 通过。 | 认证、schema、幂等、越界和零泄漏测试。 |
| D2 扩展 | Manifest V3、当前页任务包提取、手动“保存 INBOX”按钮与 fixture 测试。 | 不自动保存、不上传。 | D1 通过。 | 只申请最小权限；无效页面/包不发送。 |
| D3 联调试用 | 用户手动加载扩展、本机启动 helper，用测试对话建一张测试卡。 | 不处理真实任务、不启用自动模式。 | 用户单独确认安装扩展与本机监听。 | 可见成功、固定路径、无重复。 |
| D4 自动模式 | 在扩展设置中由用户开启“明确口令自动保存”。 | 不改为全自动会话归档。 | D3 连续稳定。 | 三次真实触发无错写、无重复。 |
| D5 复盘 | 3–5 个真实任务后的字段/摩擦/失败复盘。 | 不扩展为 LG 检索或项目执行器。 | D4 样本足够。 | 保留、降级为按钮或停止的明确决定。 |

## 7. 当前待用户确认的三个小决策

1. 使用 Chrome 还是 Edge 的 ChatGPT 网页版作为唯一载体？
2. 触发词是否固定为 `整理进 INBOX`，还是需要兼容 `转成待办`、`把方案留档`？
3. D2 默认先做“可见保存按钮”，D4 再开启自动；是否接受这个两段式安全上线？

## 8. 参考与关联

- [[02-PROJECTS/Agent/工作流/方案-ChatGPTPlus环境INBOX收件与交接|Plus 环境 INBOX 收件与交接方案]] — 已被本文细化，保留为能力决策记录。
- [[02-PROJECTS/Agent/工作流/方案-自建INBOX收件工具|自建 INBOX 收件工具]] — 复用其固定根目录 writer；MCP 部分不用于 Plus 自动收件。
- [[02-PROJECTS/Agent/工作流/INBOX对话工作区工作流|INBOX 对话工作区工作流]]
- [Taan1el/save-to-obsidian](https://github.com/Taan1el/save-to-obsidian) — 扩展→localhost helper 的收件结构参考，不直接采用。
- [peterspellward/chatbridge](https://github.com/peterspellward/chatbridge) — 最后一轮消息提取与本地写入结构参考，不直接采用。
- [OpenAI Help：ChatGPT 中的开发者模式和 MCP 应用](https://help.openai.com/zh-hans-cn/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt) — 说明为何本方案不选择 Plus 不支持的写入 MCP。
- [OpenAI Help：在 ChatGPT 桌面应用中使用网站工具](https://help.openai.com/zh-hans-cn/articles/20001423-using-site-tools-in-the-chatgpt-desktop-app) — 桌面端 WebMCP Site Tools 候选的官方说明，实际账号与本机页面可用性待验证。
