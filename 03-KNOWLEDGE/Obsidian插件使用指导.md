---
title: Obsidian 插件使用指导
date: 2026-07-08
tags:
  - obsidian
  - workflow
status: active
---

# Obsidian 插件使用指导

> 依据 `D:\LibraryG\.obsidian` 实际配置 + 仓库内真实使用痕迹整理，非凭空编写。版本截至 2026-07-08。

## 一、总览

| 插件 | 版本 | 类型 | 使用状态 | 一句话定位 |
|------|------|------|----------|------------|
| Dataview | 0.5.68 | 社区 | 🟢 高频使用 | 用 DQL 把 frontmatter 渲染成动态表格/仪表盘 |
| Templater | 2.20.6 | 社区 | 🟢 高频使用 | 文件创建时自动注入模板变量 |
| Excalidraw | 2.25.0 | 社区 | 🟡 已起步 | 手绘/流程图，当前 1 张图 |
| Local REST API (MCP) | 4.1.3 | 社区 | 🟢 基础设施 | 给 WorkBuddy/AI 提供 vault 读写接口（**含密钥，勿泄露**） |
| BuddyBridge | 1.0.13 | 社区 | ⚪ 未使用 | Obsidian 内直接对话 WorkBuddy/CodeBuddy |
| Smart Connections | 4.5.3 | 社区 | ⚪ 未使用 | 语义搜索/相关笔记推荐（尚未建索引） |
| Version History Diff | 2.3.8 | 社区 | ⚪ 按需 | 对比 Sync/File Recovery/Git 历史版本 |
| 核心 daily-notes / templates / canvas / properties / backlink / graph / bookmarks / file-recovery / sync / bases 等 | — | 核心 | 🟢 启用 | 见第九节 |

图例：🟢 已落地 / 🟡 初步 / ⚪ 已装未用

## 二、Dataview（v0.5.68，无自定义配置 → 全默认）

**用途**：把笔记的 frontmatter 属性当作数据库，用 DQL（类 SQL）渲染成动态表格。

**当前使用情况**（仓库内已有 6 个 DQL 块）：
- `02-PROJECTS/TileMatch/_MOC.md` — 4 个仪表盘查询：
  - 全部文档（按修改时间）：`TABLE type, status, date FROM "02-PROJECTS/TileMatch" WHERE type SORT file.mtime DESC`
  - 各分类文档数：`GROUP BY file.folder`
  - 最近更新 Top10：`SORT date DESC LIMIT 10`
  - 草稿待完善：`WHERE status = "draft"`
- `02-PROJECTS/TileMatch/知识库/知识库文档顺序索引.md` — 按 `cat_order` 排序展示全库顺序
- `02-PROJECTS/TileMatch/知识库/知识库编号方案_整合v1_2026-07-08.md` — 示例查询

**依赖的属性字段**：`type`、`status`、`date`、`cat_order`（来自 _MOC / 知识库笔记的 frontmatter）。只要这些字段保持规范，表格会自动更新。

**使用指导**：
1. 在任意笔记插入 ` ```dataview ` 代码块写 DQL。
2. 常用范式：`TABLE 字段 FROM "路径" WHERE 条件 SORT 字段 DESC LIMIT n`。
3. 统计数量：`TABLE length(rows) AS 数 GROUP BY 分组字段`。
4. 注意：Dataview 默认只读标准 Properties（YAML 属性），老式写法可能不被识别。

**注意事项**：
- 该插件是 `_MOC.md` 仪表盘和顺序索引的渲染依赖；禁用后这两页只剩静态备份（顺序索引页已保留无 Dataview 时的静态列表作为兜底）。
- 查询不渲染时，先确认插件已启用、且笔记 frontmatter 用了标准 Properties。

## 三、Templater（v2.20.6）

**用途**：文件创建时按模板自动注入变量（日期、标题、交互输入等），比核心 templates 更强（支持 JS、系统命令、用户脚本）。

**当前配置**：
- 模板目录：`04-TEMPLATES`
- 创建文件时自动触发：`trigger_on_file_creation: true`
- 生成后跳到光标位：`auto_jump_to_cursor: true`
- 系统命令：关闭（`enable_system_commands: false`，安全默认）
- Shell：`bash`
- 已登记 5 个模板（热键为空，靠命令面板/手动调用）

**5 个模板实际用法**：
| 模板 | 触发标签 | 关键变量 | 用途 |
|------|----------|----------|------|
| tp-daily | `daily` | `2026-07-08`、星期 | 每日笔记，底部提示 WorkBuddy 日志路径 |
| tp-tech-analysis | `tech-analysis` | `tp.file.title`、`tp.date.now` | 技术分析（背景/架构/决策表/迭代记录） |
| tp-project | `project` | `tp.file.title`、状态/优先级 | 项目概览（目标/里程碑/决策） |
| tp-meeting | `meeting` | `tp.date.now("YYYY-MM-DD HH:mm")` | 会议纪要（议题/行动项） |
| tp-quick | `inbox` | `tp.system.prompt(...)` 交互输入 | 快速捕获，状态 `unprocessed`，待整理 |

**使用指导**：
1. 新建笔记时若已开启「创建文件时触发」，会提示选模板；或命令面板搜 `Templater: Open insert template modal`。
2. 变量语法：`格式`、`Obsidian插件使用指导`；`null` 会弹窗让你输入。
3. 不要把 `04-TEMPLATES` 里的 `undefined` 片段当普通文本改，那是 Templater 指令。

**注意事项**：
- 与核心 `templates` 插件共存：本项目以 Templater 为主（核心 templates 也启用但基本不用）。
- `enable_system_commands: false` 是好的安全默认，保持。

## 四、Excalidraw（本机临时区）

**用途**：在 Obsidian 内画手绘图、流程图、架构图，可嵌入 Markdown 笔记。

**同步边界**：`Excalidraw/` 与仅用于该目录的 `路径图工作candy.canvas` 均为本机临时工作区，已排除出 Git；两台设备可各自保留不同内容。插件设置和可能的 API 凭据也不以共享库中的本节为依据。

**使用指导**：
1. 命令面板搜 `Excalidraw: Create a new drawing` 新建图；文件落在本机 `Excalidraw/`。
2. 临时图可在本机笔记中嵌入或链接；不要让需要跨设备访问的共享笔记依赖其中的文件。
3. 若图稿成为长期资料，先导出或整理为明确要共享的资源，再单独加入知识库。

## 五、Local REST API with MCP（v4.1.3，⚠️ 含密钥）

**用途**：在本地起一个 REST API + MCP server，让外部程序（WorkBuddy / AI 工具）读写你的 vault。仓库里 WorkBuddy 的 `obsidian-mcp` 连接器正是通过它工作的。

**当前配置**：
- 安全端口（HTTPS）：`27124`
- 不安全端口（HTTP）：`27123`，且 `enableInsecureServer: true`（已开启）
- `apiKey`：已生成（**敏感，见下方安全提醒**）
- 已内置 TLS 证书/私钥

**使用指导**：
- 一般无需手动操作；WorkBuddy 侧 `obsidian-mcp` 连接它即可用 `mcp__obsidian-mcp__*` 工具读写笔记。
- 若换机器/重装，需在 WorkBuddy 的 MCP 配置里填入这里的 `apiKey` 和端口。

**⚠️ 安全提醒（重要）**：
- `data.json` 内含 **明文 apiKey + RSA 私钥/证书**。任何拿到该文件的人都能读写你的整个 vault。
- **切勿把 `.obsidian/plugins/obsidian-local-rest-api/data.json` 提交到任何 git 仓库或同步到云端**（如已同步，建议轮换 apiKey：在插件设置里 Regenerate）。
- `enableInsecureServer: true` 意味着本地 27123 明文端口开放，仅在本机无风险；若在不信任的网络/多用户机器上，建议关闭不安全端口。

## 六、BuddyBridge（v1.0.13，桌面端）

**用途**：在 Obsidian 内直接与 WorkBuddy / CodeBuddy 多轮对话（流式响应），相当于把 AI 聊天搬进笔记软件。

**当前状态**：已安装，但仅 1 个名为「新对话」的空会话，尚未实际使用。

**使用指导**：
- 命令面板或侧栏打开 BuddyBridge，新建对话即可在 Obsidian 里问 WorkBuddy。
- 与 Local REST API 的区别：BuddyBridge 是「在 Obsidian 里聊天」；Local REST API 是「让 WorkBuddy 来操作 Obsidian」。两者互补。

## 七、Smart Connections（v4.5.3）

**用途**：本地向量模型给笔记做语义嵌入，写作时推荐相关笔记、支持语义搜索（无需 API key，隐私友好）。

**当前状态**：刚安装（`installed_at` 最近），**尚未生成嵌入索引**（仓库根无 `.smart-connections/` 文件夹），未实际使用。

**使用指导**：
1. 首次使用会在后台建立向量索引（笔记多时耗时几分钟）。
2. 命令面板搜 `Smart Connections` 打开面板，写作时右侧会显示相关笔记。
3. 默认用本地模型，无需配置即可用；如需更强效果可在设置里接入 API。

## 八、Version History Diff（v2.3.8）

**用途**：对比 Obsidian 核心 Sync、File Recovery，以及 Git 的版本历史差异。

**当前配置**：词级 diff（`word`）、相似度阈值 0.25、色盲友好配色、逐行输出（`line-by-line`）。

**使用指导**：
- 打开一篇笔记 → 命令面板搜 `Version History Diff` → 选要对比的历史源（Sync / File Recovery / Git）。
- 适合在误改后找回旧内容，或对比 Git 提交差异。

## 九、核心插件（启用 / 未启用摘要）

**已启用**（与本项目相关）：`daily-notes`、`templates`、`canvas`、`properties`、`backlink`、`outline`、`graph`、`tag-pane`、`bookmarks`、`file-recovery`、`sync`、`bases`、`word-count`、`note-composer`、`command-palette`、`page-preview`、`outgoing-link`、`editor-status`、`markdown-importer`。

**未启用**：`footnotes`、`slash-command`、`zk-prefixer`、`random-note`、`slides`、`audio-recorder`、`workspaces`、`publish`、`webviewer`。

> 说明：核心 `templates` 与社区 `Templater` 共存，实际以 Templater 为主。

## 十、异常 / 待清理项

1. **`hotkeys.json` 引用了 `mouse-tooltip-translator`**（Alt+8/9/0 翻译快捷键），但该插件**不在启用列表、也无插件目录** → 应为已卸载插件的残留热键。建议：在 Obsidian 设置 → 热键里清掉这几条，或重新安装该插件（如仍需划词翻译）。
2. **Smart Connections / BuddyBridge 已装未用**：如确定不用，可在社区插件里禁用以减负；Smart Connections 首次索引会占资源。
3. **Excalidraw AI 未配置 key**：AI 绘图功能当前不可用，需补 key 才生效。

---

生成说明：本指导依据 `.obsidian` 配置与仓库实际痕迹整理，非凭空编写；Local REST API 密钥已刻意不在此文档中明文展示。
