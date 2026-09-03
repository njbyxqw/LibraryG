---
title: MOC 命名与导航层级规范
date: 2026-08-05
type: spec
status: finalized
priority: high
tags: [LibraryG, MOC, 导航, Obsidian, 工作流]
---

# MOC 命名与导航层级规范

> 本规范用于解决 MOC 重名、AI 检索误入、主 MOC 过度膨胀的问题。目标不是让所有 MOC 很短，而是让入口稳定、命名唯一、层级清晰、历史内容可保留。

---

## 核心原则

- **唯一可路由**：MOC 文件名或 alias 必须能明确指向一个项目/领域。
- **HOME 做路由**：`HOME.md` 是主入口，但只负责路由和高价值入口，不承载所有正文细节。
- **项目 MOC 做目录**：项目 `_MOC.md` 负责模块导航、常用入口、索引，不写成长篇正文。
- **子 MOC 做专题**：障碍、工具、MEMORY 等专题可以有子 MOC，但名称必须带领域前缀或唯一 alias。
- **历史不硬删**：遇到大 MOC 或旧 MOC，优先增加路由表和别名说明，不直接删减有意义内容。

---

## 推荐层级

```text
AI总MOC.md                       # AI 最短稳定入口
HOME.md                         # 全库主路由，只放项目入口和高价值入口
工作空间总纲.md                  # 空间关系和工作原则
02-PROJECTS/<项目>/_MOC.md       # 项目入口
02-PROJECTS/<项目>/<专题>/*MOC.md # 专题入口
02-PROJECTS/Agent/工作流/*       # 跨项目工作流、规范、导航规则
```

---

## 命名规则

| 层级 | 推荐文件名 | 说明 |
|---|---|---|
| AI 稳定入口 | `AI总MOC.md` | Codex / AI 任务优先读取的最短路由 |
| 全库主入口 | `HOME.md` | 唯一主路由 |
| 空间总纲 | `工作空间总纲.md` | 解释 MT / TS / LG / Obsidian 关系 |
| 项目 MOC | `02-PROJECTS/<项目>/_MOC.md` | 可以同名，但链接必须写完整路径 |
| 专题 MOC | `<专题名>_MOC.md` 或 `<项目>-<专题>_MOC.md` | 避免只有 `_MOC` 或过于泛化 |
| MEMORY MOC | `WB-MEMORY_MOC.md` | 历史 WorkBuddy 记忆入口，文件名已唯一，避免和项目 MOC 混淆 |

---

## 链接规则

- 从 `HOME.md` 指向项目 MOC 时，使用 vault-root 完整路径：`[[02-PROJECTS/TileScape/_MOC|TileScape MOC]]`。
- 项目内部指回本项目 MOC，可以使用 `[[_MOC|项目 MOC]]`，但跨项目禁止只写 `[[_MOC]]`。
- 子 MOC 应提供明确 alias，例如 `TileMatch 障碍系统 MOC`，减少 AI 只按文件名匹配时误入。
- 主 MOC 中同名入口必须带别名展示，不裸写 `[[_MOC]]`。

---

## MOC 内容边界

MOC 应优先包含：

- 项目/专题一句话定位；
- 快速入口；
- 模块分类；
- 高价值文档；
- 待补齐项；
- Dataview 或静态索引。

MOC 不宜承载：

- 完整技术方案正文；
- 大段工作过程；
- 每日流水；
- 大量重复摘录。

如果主 MOC 已经很庞大，优先做三件事：

1. 顶部增加“项目入口表”和“工作流入口表”。
2. 把长列表留在原处作为静态备份，不急删。
3. 新增专题 MOC 或索引页，再逐步把新内容挂到专题入口。

---

## 状态标记

旧文档、旧路径和旧方案不要急着删除。优先用状态标记表达当前可用性：

| 状态 | 含义 | 推荐用法 |
|---|---|---|
| `current` | 当前有效 | 当前仍作为执行依据的规范、入口、索引 |
| `historical` | 历史记录 | 旧环境路径、旧同步方案、历史报告，保留追溯价值 |
| `deprecated` | 已废弃 | 明确不应继续使用的字段、流程或方案 |
| `needs-review` | 待确认 | 可能过期但还没完成核验的文档 |

使用方式：

- 新文档可以在 frontmatter 增加 `lifecycle: current`。
- 历史文档不必批量改 frontmatter；可以在正文顶部加一句“当前状态”说明。
- 不确定时用 `needs-review`，不要直接删。
- 对入口文档、规范文档、MEMORY，优先保证状态准确。

---

## 当前 MOC 登记

| MOC | 路径 | 用途 |
|---|---|---|
| AI 总 MOC | `AI总MOC.md` | AI 最短稳定入口，负责把任务路由到 HOME、Memory、项目 MOC 和工作流规范 |
| HOME | `HOME.md` | 全库主路由 |
| 工作空间总纲 | `工作空间总纲.md` | 多空间职责边界 |
| TileMatch MOC | `02-PROJECTS/TileMatch/_MOC.md` | MT/TileMatch 项目入口 |
| TileScape MOC | `02-PROJECTS/TileScape/_MOC.md` | TS/TileScape 项目入口 |
| TileMatch 障碍系统 MOC | `02-PROJECTS/TileMatch/游戏逻辑/局内障碍/局内障碍知识库_MOC.md` | 障碍系统专题入口 |
| Agent MEMORY MOC | `02-PROJECTS/Agent/WorkBuddy-MEMORY/WB-MEMORY_MOC.md` | Memory 蒸馏与存档入口；目录名保留 WorkBuddy 历史来源 |

---

## 关联

- [[HOME|LibraryG 主入口]]
- [[工作空间总纲|工作空间总纲]]
- [[规范-多项目工作流与复现|多项目工作流与复现]]
