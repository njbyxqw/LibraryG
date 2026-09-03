---
title: LibraryG 知识库
tags:
  - moc
  - home
updated: 2026-08-05
---

# LibraryG — Agent / AI + Obsidian 工作流

> 个人知识管理 + 多 Agent / AI 协作工作流。以 Obsidian 为知识载体，LG 作为通用 AI 可读取、可写入、可检索的长期知识库。

---

## AI 必读

> AI 做 LibraryG 相关任务时，优先从 [[AI总MOC|AI 总 MOC]] 进入；按 MOC 逐级定位，不默认全盘搜索。

| 入口 | 用途 |
|---|---|
| [[AI总MOC|AI 总 MOC]] | AI 最短稳定入口 |
| [[02-PROJECTS/Agent/Memory|Agent Memory]] | 当前通用记忆 |
| [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护]] | 入库、归档、维护规则 |
| [[02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级|MOC 命名规范]] | 链接和导航规则 |

---

## 当前工作空间定位

入口：[[工作空间总纲|工作空间总纲]] — 先看这里理解 LibraryG、MT 老项目、TileScape、Obsidian 之间的职责边界。

| 空间 | 本机路径 | 定位 |
|------|----------|------|
| LibraryG | `/Users/dean/LibraryG` | 主控知识库 / 总纲空间 / Obsidian vault |
| MT 老项目 | `/Users/dean/Downloads/meatloaf_client` | 旧项目代码与历史行为源 |
| TileScape | `/Users/dean/TileScape` | 从 MT 分离出的优化项目，近期工作会更多 |
| Obsidian 配置 | `/Users/dean/LibraryG/.obsidian` | 知识浏览、双链、模板、Dataview |

---

## 仓库结构

```
LibraryG/
├── 工作空间总纲.md   🧭 多工作空间职责边界与信息流
├── 00-INBOX/        📥 快速捕获 — 未经整理的想法和笔记
├── 01-DAILY/        📅 每日笔记 — 日志、任务、工作记录
├── 02-PROJECTS/     📁 项目笔记
│   ├── TileMatch/      消除类游戏项目 (Unity/C#)
│   ├── TileScape/      消除类独立项目 (Unity/C#，TileV2 主干)
│   └── Agent/          AI 协作、工作流、记忆与自动化
├── 03-KNOWLEDGE/    📚 知识库
│   ├── Unity/          Unity 开发知识
│   ├── TileV2-Editor/  关卡编辑器
│   └── Game-Logic/     游戏逻辑分析
├── 04-TEMPLATES/    📋 模板 (5个)
├── 05-ARCHIVE/      🗄️ 归档
├── .workbuddy/      ⚙️ 历史 WorkBuddy 兼容区 / 当前 AI 记忆入口
└── .obsidian/       🔧 Obsidian 配置
```

---

## 日常工作流

### 🌅 开始工作

1. **打开今日日记**: 在 Obsidian 中按 `Ctrl+1` 或点击左侧栏日历图标
2. **回顾**: 查看昨日日记和未完成任务
3. **规划**: 在今日日记中列出今日任务

> AI 提示: 对当前协作 Agent 说 "打开今日笔记" 或 "回顾昨天的工作"，应优先读取 `01-DAILY/` 和本页索引。

### 💼 工作中

| 场景 | 操作 | 模板 |
|------|------|------|
| 记录工作进展 | 在今日日记中追加内容 | `tp-daily` |
| 分析代码/架构 | 新建技术分析笔记 | `tp-tech-analysis` |
| 开会讨论 | 新建会议记录 | `tp-meeting` |
| 快速记想法 | 在 00-INBOX 创建笔记 | `tp-quick` |
| 新项目立项 | 在 02-PROJECTS 创建项目笔记 | `tp-project` |

> AI 提示: 对当前协作 Agent 说 "记录一条工作笔记：xxx" 或 "分析一下 xxx 模块的架构"，应优先写入 Daily、INBOX 或对应项目目录。

### 🌙 结束工作

1. **整理**: 将 00-INBOX 中的笔记归类到相应目录
2. **总结**: 在今日日记中补充工作记录和思考
3. **同步**: 确保工作产出已记录到每日日志中

> AI 提示: 对当前协作 Agent 说 "存档今天的工作"，应按日志同步规范整理 INBOX、更新 Daily 和相关 MOC。

---

## 模板系统

| 模板 | 文件 | 用途 | 关键属性 |
|------|------|------|---------|
| 每日笔记 | `04-TEMPLATES/tp-daily.md` | 日常工作记录 | `date`, `tags` |
| 技术分析 | `04-TEMPLATES/tp-tech-analysis.md` | 代码/架构分析 | `category`, `status`, `source` |
| 项目概览 | `04-TEMPLATES/tp-project.md` | 项目跟踪 | `status`, `priority` |
| 会议记录 | `04-TEMPLATES/tp-meeting.md` | 会议笔记 | `attendees` |
| 快速笔记 | `04-TEMPLATES/tp-quick.md` | 临时想法 | `status: unprocessed` |

**使用方式**: 创建新笔记后，使用命令面板 (`Ctrl+P`) 搜索 "Templater: Insert template" 或使用 Templater 快捷键。

---

## Agent / AI 协作

### 双向协作模型

```
┌─────────────────┐         ┌──────────────────┐
│   Agent / AI    │         │     Obsidian     │
│   (执行与协作)   │         │   (知识载体)      │
│                 │  写入 →  │                  │
│  .workbuddy/    │ ← 读取  │  00-INBOX/       │
│  memory/        │         │  01-DAILY/       │
│                 │  CLI →  │  02-PROJECTS/    │
│  Obsidian CLI   │         │  03-KNOWLEDGE/   │
└─────────────────┘         └──────────────────┘
```

> `.workbuddy/` 是历史目录名，目前作为兼容的本地记忆入口保留；新的知识库规范、工作流和复盘统一放在 `02-PROJECTS/Agent/`。

### Agent / AI 能做什么

- **读取笔记**: 搜索和读取仓库中的任意笔记作为上下文
- **创建笔记**: 在指定目录创建结构化笔记
- **追加内容**: 向今日日记或指定笔记追加内容
- **管理属性**: 设置/读取笔记的 frontmatter 属性
- **搜索**: 全文搜索或带上下文搜索
- **链接分析**: 查看反向链接、出链、孤立笔记

### 常用指令（对当前 Agent / AI 说）

| 指令 | 效果 |
|------|------|
| "打开今日笔记" | 在 Obsidian 中打开/创建今日日记 |
| "记录工作笔记：xxx" | 追加内容到今日日记 |
| "搜索 xxx" | 在仓库中搜索关键词 |
| "创建技术分析：xxx" | 用技术分析模板创建笔记 |
| "存档今天的工作" | 整理 INBOX + 更新日记 |
| "回顾本周工作" | 读取本周日记并总结 |

---

## Obsidian CLI 速查

> 当前机器路径已从历史 Windows 环境迁移到 macOS。以下命令是旧 WorkBuddy/Obsidian CLI 设计稿，后续如需自动化执行，应先重新确认当前 Obsidian CLI 或插件能力；日常浏览与检索优先直接使用 Obsidian 打开 `/Users/dean/LibraryG`。

```bash
# 日记操作
obsidian daily                              # 打开/创建今日日记
obsidian daily:read                         # 读取今日日记内容
obsidian daily:append content="- [ ] 任务"  # 追加到今日日记

# 文件操作
obsidian create name="笔记名" content="# 标题"  # 创建笔记
obsidian read file="笔记名"                    # 读取笔记
obsidian append file="笔记名" content="内容"    # 追加内容
obsidian move file="笔记名" to="03-KNOWLEDGE/笔记名.md"  # 移动笔记
obsidian delete file="笔记名"                   # 删除笔记
obsidian open file="笔记名"                     # 在 Obsidian 中打开

# 搜索
obsidian search query="关键词"                 # 搜索笔记名
obsidian search:context query="TODO"           # 带上下文搜索

# 标签与属性
obsidian tags counts                          # 标签统计
obsidian property:set name="status" value="done" file="笔记名"  # 设置属性
obsidian properties file="笔记名"              # 列出所有属性

# 任务
obsidian tasks todo                           # 列出所有未完成任务
obsidian tasks daily todo                     # 今日日记中的任务

# 链接分析
obsidian backlinks file="笔记名"              # 反向链接
obsidian links file="笔记名"                  # 出链
obsidian orphans                              # 孤立笔记（无反链）
obsidian unresolved                           # 断链

# 仓库信息
obsidian vault                                # 仓库信息
obsidian files                                # 列出所有文件
obsidian folders                              # 列出所有文件夹
```

---

## 全库导航（主 MOC）

> ⚠️ **AI 做任务时先看这里**，按领域定位所需内容。所有链接均为文件路径，可直接点击。
> 🔰 **新设备？** → [[HOME-冷启动指南|冷启动指南]] — 从零重建工作流与知识库

### 项目入口

| 项目 | 入口 | 说明 |
|---|---|---|
| TileMatch / MT | [[02-PROJECTS/TileMatch/_MOC|项目 MOC]] · [[02-PROJECTS/TileMatch/_项目概览|项目概览]] | 历史工作主要沉淀区，旧项目逻辑与行为基线 |
| TileScape / TS | [[02-PROJECTS/TileScape/_MOC|项目 MOC]] · [[02-PROJECTS/TileScape/_项目概览|项目概览]] | 从 MT 分离出的优化项目，近期工作会更多 |
| Agent / LG 工作流 | [[02-PROJECTS/Agent/Memory|Agent Memory]] · [[02-PROJECTS/Agent/工作流/规范-多项目工作流与复现|多项目工作流与复现]] · [[02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级|MOC 命名规范]] · [[02-PROJECTS/Agent/工作流/评估-工作空间与工作流程现状-2026-08-05|工作空间现状评估]] | 跨项目规范、记忆、复盘和流程沉淀 |

### TileScape · TS
入口：[[02-PROJECTS/TileScape/_MOC|项目 MOC]] · [[02-PROJECTS/TileScape/_项目概览|项目概览]]

**代码冷启动**
`/Users/dean/TileScape/AGENTS.md` · `/Users/dean/TileScape/Docs/Knowledge/README.md` · `/Users/dean/TileScape/Docs/Knowledge/Memory.md` · `/Users/dean/TileScape/Docs/Knowledge/CodeMap.md`

**LG 侧索引**
[[02-PROJECTS/TileScape/代码框架/代码框架总览|代码框架总览]] · [[02-PROJECTS/TileScape/参考/Docs文档索引|Docs 文档索引]]

### TileMatch · MT
入口：[[02-PROJECTS/TileMatch/_MOC|项目 MOC]] · [[02-PROJECTS/TileMatch/_项目概览|项目概览]]

> 旧知识库以 MT 为主，是之前工作主要发生在 MT 上的自然结果；项目之间不固定主次，按任务和索引进入。

**代码入口**
[[02-PROJECTS/TileMatch/参考/MT老项目路径索引|MT 老项目路径索引]] · `/Users/dean/Downloads/meatloaf_client/client/AGENTS.md`

**游戏逻辑**
[[02-PROJECTS/TileMatch/游戏逻辑/局内障碍/局内障碍知识库_MOC|障碍系统 MOC]] · [[02-PROJECTS/TileMatch/游戏逻辑/Rocket/分析-RocketV2完整逻辑-v2（重构版）|火箭牌 V2]] · [[02-PROJECTS/TileMatch/游戏逻辑/其他/分析-死局逻辑与改进方案-v1|死局 deadlock]] · [[02-PROJECTS/TileMatch/游戏逻辑/其他/分析-障碍Tile生成与序列逻辑-v1|牌局生成]] · [[02-PROJECTS/TileMatch/游戏逻辑/局内道具/分析-局内道具逻辑梳理|局内道具]] · [[02-PROJECTS/TileMatch/游戏逻辑/战前道具/分析-关卡连胜与闪电球逻辑-v1|连胜闪电球]]

**编辑器**
[[02-PROJECTS/TileMatch/编辑器/分析-关卡编辑器界面与功能逻辑梳理-v1|编辑器架构]] · [[02-PROJECTS/TileMatch/编辑器/规范-本地扩展开发|本地扩展开发]] · [[02-PROJECTS/TileMatch/编辑器/分析-编辑器快捷键系统-v1|快捷键系统]]

**打点 & 数据**
[[02-PROJECTS/TileMatch/打点/报告-Tile打点事件梳理_2026-06-08|打点系统]] · [[02-PROJECTS/TileMatch/打点/报告-关卡难度分析SQL_完整版_2026-07-03|关卡难度 SQL]]

**知识库规范**
[[02-PROJECTS/TileMatch/知识库/规范-知识库文档分类标准|分类标准]] · [[02-PROJECTS/TileMatch/知识库/规范-知识库健康检查|健康检查]] · [[02-PROJECTS/TileMatch/知识库/知识库文档顺序索引|顺序索引]] · [[02-PROJECTS/TileMatch/知识库/知识库编号方案_整合v1_2026-07-08|编号方案]]

### Agent · AI 工作档案
入口：[[02-PROJECTS/Agent/Memory|Agent Memory]] · [[02-PROJECTS/Agent/WorkBuddy-MEMORY/WB-MEMORY_MOC|WorkBuddy MEMORY 历史归档]]

> `WorkBuddy-MEMORY` 是历史命名，保留用于追溯旧记录；现阶段按通用 Agent / AI 记忆区理解。

**工作流**
[[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护]] · [[02-PROJECTS/Agent/工作流/评估-LibraryG结构与AI读取稳定性-2026-08-10|LG 读取稳定性评估]] · [[02-PROJECTS/Agent/工作流/报告-Obsidian链接完整性审计-2026-08-10|Obsidian 链接审计]] · [[02-PROJECTS/Agent/工作流/规范-多项目工作流与复现|多项目工作流与复现]] · [[02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级|MOC 命名规范]] · [[02-PROJECTS/Agent/工作流/评估-工作空间与工作流程现状-2026-08-05|工作空间现状评估]] · [[02-PROJECTS/Agent/工作流/工作内容日志同步规范|日志同步规范]] · [[02-PROJECTS/Agent/工作流/INBOX对话工作区工作流|INBOX 工作流]] · [[02-PROJECTS/Agent/工作流/DailyLogs同步流程|DailyLogs 历史同步]] · [[02-PROJECTS/Agent/工作流/知识库同步比对报告-2026-07-01|同步比对报告]]

**报告归档**
[[知识库文件污染事故总结_2026-07-03|知识库污染事故]] · [[复盘-牌底笔刷功能开发|牌底笔刷复盘]]

### 通用知识
[[03-KNOWLEDGE/Unity/Unity 开发笔记|Unity 开发]] · [[03-KNOWLEDGE/Unity|Unity 速查]] · [[03-KNOWLEDGE/TileV2-Editor/TileV2 编辑器概览|TileV2 编辑器]] · [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑]]

### 每日 & 模板
[[01-DAILY/|每日日志]]（53 篇） · [[01-DAILY/summaries/近期工作进度与待办-2026-08-20|当前进度与待办]] · [[01-DAILY/summaries/阶段工作汇总-2026-07-02至2026-08-14|近期阶段汇总]] · [[01-DAILY/summaries/近期工作汇总-2026-07-01|上一阶段汇总]]
模板：[[04-TEMPLATES/tp-daily|日记]] · [[04-TEMPLATES/tp-tech-analysis|技术分析]] · [[04-TEMPLATES/tp-project|项目]] · [[04-TEMPLATES/tp-meeting|会议]] · [[04-TEMPLATES/tp-quick|速记]]

---

## 配置详情

| 配置项 | 值 |
|-------|-----|
| Obsidian 版本 | 1.12.7 |
| CLI 状态 | 当前 macOS 环境待重新确认 |
| 模板引擎 | Templater (community) |
| 模板目录 | `04-TEMPLATES/` |
| 日记目录 | `01-DAILY/` |
| 日记格式 | `YYYY-MM-DD` |
| 新文件位置 | `00-INBOX/` |
| 附件路径 | `00-INBOX/attachments/` |
| 链接格式 | Wikilink (`[[ ]]`) |
| AI 记忆入口 | `.workbuddy/memory/`（历史 WorkBuddy 目录名，当前按通用 Agent / AI 记忆入口使用） |

---

*最后更新: 2026-08-05 | 项目不固定主次；按任务与索引进入，LG 负责全面沉淀和检索*
