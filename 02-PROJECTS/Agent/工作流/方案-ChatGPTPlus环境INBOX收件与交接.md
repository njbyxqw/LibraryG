---
title: ChatGPT Plus 环境的 INBOX 收件与交接方案
date: 2026-09-17
type: design
status: draft
lifecycle: needs-review
priority: high
tags: [LibraryG, ChatGPT-Plus, INBOX, Codex, 交接]
source: "2026-09-17 官方 ChatGPT MCP 能力核验；替代此前假定 Chat 可直接写本机 INBOX 的路线"
---

# ChatGPT Plus 环境的 INBOX 收件与交接方案

> [!warning] 已核验的能力边界
> 个人 Plus 不能使用完整、带写入动作的 ChatGPT MCP；Chat 也不能原生调用本机文件系统。因此“在 Chat 说一句整理进 INBOX，随后自动写本机文件”在当前产品条件下不可实现。此方案不尝试以 tunnel、浏览器自动化、第三方高权限插件或后台监听绕过该边界。

## 1. 重新定义目标

目标不再是“Chat 直接写本地文件”，而是让一次明确指令形成一个**可验证、最短、可跨界交接的任务包**，并把本地写入保持为单独、最小权限动作。

```text
Chat：用户说“整理进 INBOX”
  → Chat 输出 INBOX 任务包（不是完整聊天记录）
  → 用户复制该任务包
  → Codex 或本地收件快捷方式校验后新建 00-INBOX 任务卡
```

不可省略的是“用户把信息从云端 Chat 带到本机”的一次动作；它是 Plus 的产品边界，也是本方案保留的权限闸门。

## 2. 推荐路线：任务包 + Codex 收件

先不再开发新的桥接服务，先试用以下两步：

1. 在 Chat 中说 `整理进 INBOX`。Chat 只输出一个固定的 `INBOX 任务包`，不附带长解释。
2. 将任务包粘贴给 Codex，并说 `创建 INBOX 任务卡`。Codex 只调用本地 writer 新建一张卡；不读取项目、不开始执行任务。

任务包是唯一需要复制的内容，包含 `title`、`state`、`target`、`next_owner`、`next_action`、`conclusion`、`facts_to_verify`、`related_links`。它沿用 [[02-PROJECTS/Agent/工作流/方案-自建INBOX收件工具|自建 INBOX 收件工具]] 的固定枚举和 renderer 契约。

### Chat 输出约定

仅在用户明确触发后，Chat 输出如下 JSON 代码块，字段外不得插入解释：

```json
{
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

`intent` 只是交接标签，不能自行授权项目修改；Codex 仍需要用户的“创建 INBOX 任务卡”指令才可写入。

## 3. 三条路线的取舍

| 路线 | 是否适合 Plus | 人工动作 | 权限 / 维护成本 | 结论 |
|---|---|---:|---|---|
| Chat 直接写本机 INBOX | 否。 | 0 | 需要当前 Plus 不具备的写入 MCP。 | 排除。 |
| Chat 任务包 → Codex 收件 | 是。 | 复制、粘贴并触发一次。 | 无外部服务；writer 只新建任务卡。 | **先试用。** |
| Chat 页面扩展 → 本机 helper | 是。 | 点击一次“保存 INBOX”。 | 扩展可读取 Chat 页面；helper 只监听 `127.0.0.1` 并固定写入 INBOX。 | P1 试用后优先评估。 |
| Chat 任务包 → 本机快捷方式 | 是。 | 复制、按一次快捷键。 | 需本机剪贴板读取与快捷方式配置；仍不能由 Chat 自动触发。 | 备选，不优先。 |
| Chat-on-St​eroids / 浏览器桥接 | 技术上可能另行研究。 | 可减少交接。 | 高权限、维护与账号/平台风险。 | 当前不采用。 |
| 升级至 Business 等工作区 | 可能。 | 可接近直接调用。 | 订阅、管理员、远程 MCP/tunnel 与安全审查。 | 仅在其他业务需要时重评估。 |

## 4. 分阶段，不再预支实现

| 阶段 | 只做什么 | 进入条件 | 停止条件 |
|---|---|---|---|
| P0 前提核验 | 确认 Plus 无写入 MCP，记录替代边界。 | 已完成。 | 不启动外部连接。 |
| P1 任务包试用 | 用真实讨论生成 3–5 个任务包并由 Codex 写卡。 | 用户每次明确触发。 | 字段频繁缺失或复制成本不可接受。 |
| P2 复盘 | 统计遗漏字段、重复卡、从 Chat 到卡的操作摩擦。 | P1 有足够样本。 | 不能说明快捷方式是否值得。 |
| P3 可选页面收件器 | 仅在 P2 证实值得时，设计 ChatGPT 页面扩展 → 固定 writer 的单动作收件器。 | 用户单独确认浏览器扩展安装、Chat 页面读取与本机 helper。 | 不上传会话、不自动保存、helper 仅监听 `127.0.0.1`，只新建 INBOX 卡。 |

P1 不需要新服务、tunnel、ChatGPT App、浏览器扩展或系统权限改动。已有 D1/D2a writer 仅作为本地实现组件，P1 试用前也不要求新增功能。

### P3 的候选架构（仅设计，尚未授权实现）

```text
ChatGPT 网页中最后一条结构化任务包
  → 浏览器扩展显示“保存 INBOX”按钮
  → 用户点击一次
  → 扩展以本地随机令牌 POST 到 127.0.0.1 helper
  → 既有固定根目录 writer 校验并新建 00-INBOX 卡
```

扩展只匹配 ChatGPT 页面中的固定 JSON 任务包，不抓取整段历史，不注入提示词，不替 Chat 发送消息，也不处理其他网站。helper 不使用 Obsidian REST API、不需要云端 API key、不创建 tunnel，且不提供读、列、改、删、终端或项目访问。自动检测用户口令并直接写卡不作为第一版：先用可见按钮保留最后一次用户确认，避免 DOM 误判或页面结构变化导致误写。

这条架构参考了“Chat 页面扩展 + localhost helper + 本地 Obsidian 写入”的开源实践，但现有项目多数保存完整会话、写入范围较宽或平台/维护成熟度不足，不能直接采用。见第 7 节。

## 5. 验收标准

- Chat 产物不是整段对话，而是一份可独立理解的任务包。
- Codex 创建卡时仅新增 `00-INBOX/` 下的一张任务卡，永不覆盖、移动、删除或执行卡内任务。
- 三到五次真实试用后，再判断是否需要快捷方式；不以设计想象提前引入自动化。
- Chat 讨论、INBOX 建卡和项目实施是三次不同授权，不能互相推导。

## 6. GitHub 实践筛选（2026-09-17）

| 项目 | 与需求的关系 | 不直接采用的原因 |
|---|---|---|
| [Taan1el/save-to-obsidian](https://github.com/Taan1el/save-to-obsidian) | 最接近 P3：Chat 页面扩展经 localhost helper 写入 Obsidian；明确不自动保存。 | 目标是整段会话与通用 vault 文件夹；文档以 Windows 为主，项目规模与当前“单卡、单目录”需求不匹配。 |
| [peterspellward/chatbridge](https://github.com/peterspellward/chatbridge) | 可从 ChatGPT 页抓取最后一轮并通过本地 bridge 写入 Obsidian。 | 仅 4 个提交，需 Obsidian Local REST API 与 API key，写入项目/会话目录；权限面和成熟度不足。 |
| [trchopan/chatgpt-ux-navigator](https://github.com/trchopan/chatgpt-ux-navigator) | 支持在 Chat 页面保存回复到本地。 | 包含 prompt 注入、文件包含、WebSocket、编排器等远超收件需求的能力。 |
| [liyana31811/Codexless](https://github.com/liyana31811/Codexless) | 试图让普通 Chat 调用本地 Codex 工具。 | 自身文档仍要求 ChatGPT custom app / MCP 与 tunnel，并承认完整写入 MCP 依赖 Business / Enterprise / Edu；不解决 Plus 前提。 |
| [totec448-spec/chat-on-steroids](https://github.com/totec448-spec/chat-on-steroids) | 更全面的本地 Chat 桥接平台。 | 文件、命令、桌面、会话和 worker 面过大，不符合单一写卡工具。 |

结论：P3 若启动，优先自建约束极小的页面收件器，借鉴前两类的本地架构，不 fork 或安装它们。

## 7. 关联

- [[02-PROJECTS/Agent/工作流/INBOX对话工作区工作流|INBOX 对话工作区工作流]]
- [[02-PROJECTS/Agent/工作流/协议-LGChat与本地执行协作|LG、Chat 与本地执行协作协议]]
- [[02-PROJECTS/Agent/工作流/方案-自建INBOX收件工具|自建 INBOX 收件工具]]（本地 writer 组件，不再作为 ChatGPT Plus 直连方案）
- [OpenAI Help：ChatGPT 中的开发者模式和 MCP 应用](https://help.openai.com/zh-hans-cn/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt) — 当前计划资格及远程连接限制；能力可能变化。
