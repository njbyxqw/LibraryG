# LibraryG 仓库 - 长期记忆

## 项目概况
- **仓库类型**: Obsidian Vault + 通用 Agent / AI 工作空间
- **路径**: `/Users/dean/LibraryG`
- **用途**: 个人知识管理 + 多项目 AI 协作工作流
- **Obsidian 版本**: 1.12.7
- **CLI 状态**: 当前 macOS 环境待重新确认
- **项目关系**: MT、TS 不固定主次；按任务和索引进入。近期 TS 工作会更多，LG 会自然逐步沉淀更多 TS 内容。

## 仓库结构
```
00-INBOX/       - 对话工作区，每次对话建 <日期-主题>/ 文件夹
01-DAILY/       - 每日笔记 + 日志汇总
02-PROJECTS/    - 项目笔记 (TileScape, TileMatch, Agent)
03-KNOWLEDGE/   - 知识库 (工作流, Unity, TileV2-Editor, Game-Logic)
04-TEMPLATES/   - 模板 (5个: daily, tech-analysis, project, meeting, quick)
05-ARCHIVE/     - 归档
```

## 已安装插件
- **Templater** - 模板系统，模板目录: 04-TEMPLATES
- **Excalidraw** - 绘图
- **Agent Client** - AI Agent 对话 (v0.11.0)

## Agent / AI 读取定位
- LG 以前主要由 WorkBuddy 维护；现在改为通用 Agent / AI 可读取、可写入、可复用的知识库位置。
- `.workbuddy/` 是历史目录名和兼容路径，不代表当前只能由 WorkBuddy 使用。
- Codex / Agent 冷启动优先读 `AGENTS.md` 和 `02-PROJECTS/Agent/Memory.md`。
- 新的工作流、复盘、规范和 AI 记忆整理入口统一优先看 `02-PROJECTS/Agent/`。

## 工作流约定
- 每日笔记存储在 01-DAILY/，格式 YYYY-MM-DD
- 新文件默认创建在 00-INBOX/
- 附件存储在 00-INBOX/attachments/
- 使用 wikilink 格式 ([[笔记名]]) 而非 markdown 链接
- `workbuddy_sync` 字段已废弃，不再新增
- DAILY 可详细记录每日工作，承担备份追踪、历史存档、成功路径和决策索引作用

## INBOX 对话工作区工作流
- INBOX 是纯粹对话中间产物区，建文件夹时不做合并判断
- 分类/合并/冲突检测统一在"整理 INBOX"时处理
- 触发词: "归档" / "整理 INBOX"
- 产物流向: 规范→02-PROJECTS/Agent/工作流/ 或 03-KNOWLEDGE/ | 项目→02-PROJECTS/ | 知识→03-KNOWLEDGE/<主题>/ | 临时→删除
- Skill: `.workbuddy/skills/inbox-organizer/SKILL.md`
- 参考规范: `02-PROJECTS/Agent/工作流/INBOX对话工作区工作流.md`

## DAILY 日志同步规范
- DAILY 记录"做了什么+结论"，不存具体产物
- 产物移动用移动（非复制）
- 参考规范: `02-PROJECTS/Agent/工作流/工作内容日志同步规范.md`

## TS / MT / LG 分工
- **TS (`/Users/dean/TileScape`)**: 从 MT 分离出的优化项目。代码任务读 `AGENTS.md`，再读 `Docs/Knowledge/README.md`、`Memory.md`、`CodeMap.md`。
- **MT (`/Users/dean/Downloads/meatloaf_client`)**: 旧项目和历史行为基线，也是早期工作主要发生的项目。
- **LG (`/Users/dean/LibraryG`)**: 基础、全面、纲领、规范、稳定成功记录、复盘、详细 DAILY 和跨项目检索库。
- 重要流程: `工作空间总纲.md`、`02-PROJECTS/Agent/工作流/规范-多项目工作流与复现.md`、`02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级.md`、`02-PROJECTS/Agent/工作流/评估-工作空间与工作流程现状-2026-08-05.md`
- MT 入口索引: `02-PROJECTS/TileMatch/参考/MT老项目路径索引.md`
- 跨 MT/TS 任务要尽量留下对位文件表，记录 MT 文件、TS 文件、关系和本次结论。

## AI 冷启动顺序
- 先读 `HOME.md` 和 `工作空间总纲.md`，确认空间关系，不预设项目主次。
- 复杂任务先查 `02-PROJECTS/Agent/工作流/规范-多项目工作流与复现.md` 的任务路由表。
- 再按任务进入对应项目 MOC：`02-PROJECTS/TileMatch/_MOC.md` 或 `02-PROJECTS/TileScape/_MOC.md`。
- 涉及代码时读对应仓库的 `AGENTS.md`；TS 还要读 `Docs/Knowledge/README.md`、`Memory.md`、`CodeMap.md`。
- 涉及跨项目复现时先查 LG 方案、DAILY、MT 路径索引和对位文件表，再进另一侧代码。
- MOC 同名时跨项目链接必须写完整 vault 路径；详细规则见 MOC 命名规范。
- 整理旧内容时用 `current` / `historical` / `deprecated` / `needs-review` 状态标记，避免直接删减有追溯价值的内容。

## 关联项目
- **TileScape / TS**: 从 MT 分离出的 TileV2 优化项目，近期工作会更多
- **TileMatch / MT**: 旧项目知识沉淀与行为对照源，历史知识库以它为主
- **Agent / AI 工作流**: `02-PROJECTS/Agent/`，包含历史 WorkBuddy 记忆、通用 AI 协作规范、复盘和自动化资料
