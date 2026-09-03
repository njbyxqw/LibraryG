# LibraryG

LibraryG 是跨 macOS / Windows 使用的 Obsidian 知识库，也是 TileMatch、TileScape 与 Agent 工作流的长期导航和归档入口。

## 开始使用

- 从 [[HOME|HOME]]、[[AI总MOC|AI 总 MOC]] 或 [[工作空间总纲|工作空间总纲]] 进入。
- 每次形成稳定结论时，记录到当日 `01-DAILY/`，并归入对应项目索引。
- 历史快照与不再活跃的材料放在 `05-ARCHIVE/`，不要直接丢弃。

## 跨设备约定

- Git 同步笔记、目录结构、项目索引与可共享的 Obsidian 语义配置。
- Git 同步用户级/项目级 Markdown 记忆和明确的 SQLite 工具数据；SQLite 运行时侧车文件不纳入版本控制。
- Git 不同步机器工作区、缓存、插件安装包和含密钥/本机状态的插件数据；这些内容由 `.gitignore` 管理。
- 文本文件统一使用 LF，避免 macOS 与 Windows 的换行差异制造无意义改动。

详细规则见 [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]]。
