---
title: LibraryG 知识库
tags:
  - moc
  - home
updated: 2026-06-25
---

# LibraryG — WorkBuddy + Obsidian 工作流

> 个人知识管理 + AI 协作工作流。以 Obsidian 为知识载体，WorkBuddy 为 AI 执行引擎。

---

## 仓库结构

```
LibraryG/
├── 00-INBOX/        📥 快速捕获 — 未经整理的想法和笔记
├── 01-DAILY/        📅 每日笔记 — 日志、任务、工作记录
├── 02-PROJECTS/     📁 项目笔记
│   ├── TileMatch/      消除类游戏项目 (Unity/C#)
│   ├── TileScape/      消除类独立项目 (Unity/C#，TileV2 主干)
│   └── WorkBuddy/      自动化与工具链
├── 03-KNOWLEDGE/    📚 知识库
│   ├── Unity/          Unity 开发知识
│   ├── TileV2-Editor/  关卡编辑器
│   └── Game-Logic/     游戏逻辑分析
├── 04-TEMPLATES/    📋 模板 (5个)
├── 05-ARCHIVE/      🗄️ 归档
├── .workbuddy/      ⚙️ WorkBuddy 集成 (内部)
└── .obsidian/       🔧 Obsidian 配置
```

---

## 日常工作流

### 🌅 开始工作

1. **打开今日日记**: 在 Obsidian 中按 `Ctrl+1` 或点击左侧栏日历图标
2. **回顾**: 查看昨日日记和未完成任务
3. **规划**: 在今日日记中列出今日任务

> WorkBuddy 提示: 对 WorkBuddy 说 "打开今日笔记" 或 "回顾昨天的工作" 即可自动操作

### 💼 工作中

| 场景 | 操作 | 模板 |
|------|------|------|
| 记录工作进展 | 在今日日记中追加内容 | `tp-daily` |
| 分析代码/架构 | 新建技术分析笔记 | `tp-tech-analysis` |
| 开会讨论 | 新建会议记录 | `tp-meeting` |
| 快速记想法 | 在 00-INBOX 创建笔记 | `tp-quick` |
| 新项目立项 | 在 02-PROJECTS 创建项目笔记 | `tp-project` |

> WorkBuddy 提示: 对 WorkBuddy 说 "记录一条工作笔记：xxx" 或 "分析一下 xxx 模块的架构" 即可自动创建笔记

### 🌙 结束工作

1. **整理**: 将 00-INBOX 中的笔记归类到相应目录
2. **总结**: 在今日日记中补充工作记录和思考
3. **同步**: 确保工作产出已记录到每日日志中

> WorkBuddy 提示: 对 WorkBuddy 说 "存档今天的工作" 即可自动完成整理和同步

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

## WorkBuddy 集成

### 双向协作模型

```
┌─────────────────┐         ┌──────────────────┐
│   WorkBuddy     │         │     Obsidian     │
│   (AI 引擎)     │         │   (知识载体)      │
│                 │  写入 →  │                  │
│  .workbuddy/    │ ← 读取  │  00-INBOX/       │
│  memory/        │         │  01-DAILY/       │
│                 │  CLI →  │  02-PROJECTS/    │
│  Obsidian CLI   │         │  03-KNOWLEDGE/   │
└─────────────────┘         └──────────────────┘
```

### WorkBuddy 能做什么

- **读取笔记**: 搜索和读取仓库中的任意笔记作为上下文
- **创建笔记**: 在指定目录创建结构化笔记
- **追加内容**: 向今日日记或指定笔记追加内容
- **管理属性**: 设置/读取笔记的 frontmatter 属性
- **搜索**: 全文搜索或带上下文搜索
- **链接分析**: 查看反向链接、出链、孤立笔记

### 常用指令（对 WorkBuddy 说）

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

> CLI 路径: `D:\Obsidian\Obsidian.exe` (需添加到 PATH)

```bash
# 设置 PATH (bash 环境)
export PATH="$PATH:/d/Obsidian"

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

### TileMatch · 三消游戏
入口：[[02-PROJECTS/TileMatch/_MOC|项目 MOC]] · [[02-PROJECTS/TileMatch/_项目概览|项目概览]]

**游戏逻辑**
[[02-PROJECTS/TileMatch/游戏逻辑/局内障碍/局内障碍知识库_MOC|障碍系统 MOC]] · [[02-PROJECTS/TileMatch/游戏逻辑/Rocket/分析-RocketV2完整逻辑-v2（重构版）|火箭牌 V2]] · [[02-PROJECTS/TileMatch/游戏逻辑/其他/分析-死局逻辑与改进方案-v1|死局 deadlock]] · [[02-PROJECTS/TileMatch/游戏逻辑/其他/分析-障碍Tile生成与序列逻辑-v1|牌局生成]] · [[02-PROJECTS/TileMatch/游戏逻辑/局内道具/分析-局内道具逻辑梳理|局内道具]] · [[02-PROJECTS/TileMatch/游戏逻辑/战前道具/分析-关卡连胜与闪电球逻辑-v1|连胜闪电球]]

**编辑器**
[[02-PROJECTS/TileMatch/编辑器/分析-关卡编辑器界面与功能逻辑梳理-v1|编辑器架构]] · [[02-PROJECTS/TileMatch/编辑器/规范-本地扩展开发|本地扩展开发]] · [[02-PROJECTS/TileMatch/编辑器/分析-编辑器快捷键系统-v1|快捷键系统]]

**打点 & 数据**
[[02-PROJECTS/TileMatch/打点/报告-Tile打点事件梳理_2026-06-08|打点系统]] · [[02-PROJECTS/TileMatch/打点/报告-关卡难度分析SQL_完整版_2026-07-03|关卡难度 SQL]]

**知识库规范**
[[02-PROJECTS/TileMatch/知识库/规范-知识库文档分类标准|分类标准]] · [[02-PROJECTS/TileMatch/知识库/规范-知识库健康检查|健康检查]] · [[02-PROJECTS/TileMatch/知识库/知识库文档顺序索引|顺序索引]] · [[02-PROJECTS/TileMatch/知识库/知识库编号方案_整合v1_2026-07-08|编号方案]]

### WorkBuddy · AI 工作档案
入口：[[02-PROJECTS/WorkBuddy/WorkBuddy-MEMORY/WB-MEMORY_MOC|MEMORY 蒸馏 MOC]]

**工作流**
[[02-PROJECTS/WorkBuddy/工作流/工作内容日志同步规范|日志同步规范]] · [[02-PROJECTS/WorkBuddy/工作流/INBOX对话工作区工作流|INBOX 工作流]] · [[02-PROJECTS/WorkBuddy/工作流/DailyLogs同步流程|DailyLogs 同步]] · [[02-PROJECTS/WorkBuddy/工作流/知识库同步比对报告-2026-07-01|同步比对报告]]

**报告归档**
[[知识库文件污染事故总结_2026-07-03|知识库污染事故]] · [[复盘-牌底笔刷功能开发|牌底笔刷复盘]]

### 通用知识
[[03-KNOWLEDGE/Unity/Unity 开发笔记|Unity 开发]] · [[03-KNOWLEDGE/Unity|Unity 速查]] · [[03-KNOWLEDGE/TileV2-Editor/TileV2 编辑器概览|TileV2 编辑器]] · [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑]]

### 每日 & 模板
[[01-DAILY/|每日日志]]（24 篇） · [[01-DAILY/summaries/近期工作汇总-2026-07-01|近期工作汇总]]
模板：[[04-TEMPLATES/tp-daily|日记]] · [[04-TEMPLATES/tp-tech-analysis|技术分析]] · [[04-TEMPLATES/tp-project|项目]] · [[04-TEMPLATES/tp-meeting|会议]] · [[04-TEMPLATES/tp-quick|速记]]

---

## 配置详情

| 配置项 | 值 |
|-------|-----|
| Obsidian 版本 | 1.12.7 |
| CLI 状态 | 已启用 |
| 模板引擎 | Templater (community) |
| 模板目录 | `04-TEMPLATES/` |
| 日记目录 | `01-DAILY/` |
| 日记格式 | `YYYY-MM-DD` |
| 新文件位置 | `00-INBOX/` |
| 附件路径 | `00-INBOX/attachments/` |
| 链接格式 | Wikilink (`[[ ]]`) |
| WorkBuddy 记忆 | `.workbuddy/memory/` |

---

*最后更新: 2026-06-25 | 由 WorkBuddy 协助创建*
