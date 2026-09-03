---
title: Agent Memory
date: 2026-08-05
type: memory
status: current
tags: [Agent, AI, LibraryG, MEMORY, 工作流]
---

# Agent Memory

> 这是 LG 当前通用 Agent / AI 长期记忆。它由旧 WorkBuddy MEMORY 蒸馏而来，面向 Codex、WorkBuddy 或其他 AI 协作工具使用。旧原文保留在 `02-PROJECTS/Agent/WorkBuddy-MEMORY/`，本文件只保留当前有效、可执行、可复用的规则。

---

## 路径速查

| 简称 | 路径 | 当前定位 |
|---|---|---|
| LG / LibraryG | `/Users/dean/LibraryG` | 主控知识库、Obsidian vault、长期记忆、Daily、规范、复盘、跨项目检索 |
| MT / TileMatch 老项目 | `/Users/dean/Downloads/meatloaf_client` | 旧项目、历史行为基线、旧代码来源 |
| TS / TileScape | `/Users/dean/TileScape` | 从 MT 分离出的优化项目，承载 TileV2 主干迁移和后续优化 |

项目之间不固定主次。旧知识库以 MT 内容居多是历史工作自然沉淀；后续 TS 内容增多也应随实际工作自然发生。

---

## 冷启动顺序

1. 先读 `AGENTS.md`、`AI总MOC.md`、`HOME.md`、`工作空间总纲.md`。
2. 再读本文件，确认当前路径、用户偏好和工作优先级。
3. 需要入库、归档或维护时，再读 `02-PROJECTS/Agent/工作流/规范-任务产出入库与维护.md`。
4. 复杂跨项目任务读 `02-PROJECTS/Agent/工作流/规范-多项目工作流与复现.md` 的任务路由表。
5. 按任务进入项目 MOC：
   - MT：`02-PROJECTS/TileMatch/_MOC.md`
   - TS：`02-PROJECTS/TileScape/_MOC.md`
6. 涉及代码时读对应仓库规则：
   - TS：`/Users/dean/TileScape/AGENTS.md`
   - MT：`/Users/dean/Downloads/meatloaf_client/client/AGENTS.md`
7. 涉及跨 MT / TS 复现时，先查 LG 方案、Daily、MT 路径索引和对位文件表，再进入另一侧代码。

## AI 读取 LG 稳定协议

- 先从 `HOME.md`、`工作空间总纲.md`、本文件和项目 `_MOC.md` 逐级定位，不默认全盘搜索。
- 明确任务域后，只在对应目录内局部检索；找不到再沿 MOC 上一级扩大范围。
- 遇到 `_MOC.md`、`_项目概览.md` 等同名入口，跨项目链接和引用必须写完整 vault 路径。
- 回答或写文档时说明依据文件；对话推断、草稿、旧方案不得写成正式规则。
- 任务形成可复用代码逻辑、路径、配置、资源或稳定结论时，按入库规范更新 Daily、MOC 和必要索引；纯小问答或无新增事实时不强行造文档。
- 周期巡检、自动化补漏或明显遗漏时，再按 [[02-PROJECTS/Agent/工作流/规范-任务知识沉淀闭环与自动巡检|任务知识沉淀闭环与自动巡检]] 检查：Daily、游戏逻辑/代码定位落点、MOC/CodeMap 导航和来源/验证边界。
- WorkBuddy 接管后，Codex 仍负责知识判断与取证；仅将含精确正文、目标、锚点、幂等标记和验证项的 `risk: low` 任务包放入 `.workbuddy/knowledge-closure/queue/ready/`。详见 [[02-PROJECTS/Agent/工作流/方案-WorkBuddy日志知识闭环自动化实施|WorkBuddy 日志知识闭环自动化实施方案]]。

---

## 工作空间原则

- **LG 是基础库**：可以存放基础、全面、纲领、详细、可检索的长文档。
- **项目目录偏执行**：项目内文档适合作为任务入口、模块梗概、局部设计和代码旁上下文。
- **Daily 可详细**：Daily 不是低价值流水账；它承担备份追踪、历史存档、成功路径和决策索引作用。
- **产出按价值入库**：形成可复用逻辑、路径、配置、资源、方案或稳定结论时，按 [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]] 判断归属、补来源状态、更新 MOC，并记录 DAILY；小任务保持低摩擦。
- **一边做深，一边复现**：MT 和 TS 有大量同源代码，不需要重复梳理；在一侧形成稳定方案和记录后，再在另一侧按记录复现。
- **保守整理历史**：旧路径、失败记录、旧同步方案、WorkBuddy 记录可能有追溯价值；优先标注状态，不直接删。

---

## 文档归属

| 内容 | 推荐位置 |
|---|---|
| 工作空间总原则、主入口、跨项目规则 | `HOME.md`、`工作空间总纲.md`、`02-PROJECTS/Agent/工作流/` |
| 当前通用 AI 记忆 | `02-PROJECTS/Agent/Memory.md` |
| Codex / Agent 冷启动说明 | `AGENTS.md` |
| WorkBuddy 历史原始记忆 | `02-PROJECTS/Agent/WorkBuddy-MEMORY/` |
| 每日详细过程、备份追踪、成功记录 | `01-DAILY/YYYY-MM-DD.md` |
| 临时对话材料和待整理草稿 | `00-INBOX/` |
| MT 旧逻辑和历史行为分析 | `02-PROJECTS/TileMatch/` |
| TS 项目知识和优化记录 | `02-PROJECTS/TileScape/` |
| 跨项目通用知识 | `03-KNOWLEDGE/` |

---

## 用户偏好

- 默认使用中文，简洁、结构化、高信号。
- 对比类内容优先用表格。
- 用户说“ok，执行吧”通常表示可以开始实施。
- 用户说“存档 / 保存 / 归档 / 整理 INBOX”通常表示需要把对话产物落到 LG。
- 长内容不要默认只给摘要；如内容太长需要落文档，应明确告诉用户保存路径，并在对话里给要点。
- 找不到文件、路径、配置时，合理检查后直接反馈并询问，不要反复绕路。
- 用户可能会手动改 LG 文档；遇到已有改动时要顺着现状整理，不要覆盖有意义内容。
- Unity / 真机运行时验收默认由用户按实际需要反馈。AI 不要求用户对每个验收项逐项回报；没有问题可以不反馈。只有高风险功能、需要把状态升级为“已验证”、或用户明确要求协助验收时，AI 才提供精简验收表并根据用户反馈更新文档。
- 用户很多 TS 工作是把 AI 作为需求辅助、代码定位、方案推演和局部实现工具使用，不是每项都按完整程序开发交付处理。不要默认把“运行时验证队列”提升为高优先级；仅当用户明确要交付、发布、验收、复盘问题，或功能风险会影响后续判断时，再主动收敛验收项。
- 当前 TS 协作的更高优先级是读取当前代码逻辑并沉淀为可复用知识：入口、调用链、配置来源、资源路径、运行时边界、与 MT 的行为差异。AI 应优先把“这套逻辑现在怎么工作”讲清楚、写清楚；验收只在需要交付确认或用户反馈异常时介入。

---

## Git 和写操作约束

- 不要自动 commit 或 push。
- 任何 git 写操作都需要用户明确授权，并先展示待提交内容。
- MT 公用 git 尤其严格：禁止 AI 自主 commit / push。
- `.workbuddy/memory` 默认不纳入 git，除非用户单独明确要求。
- 涉及批量改文件要谨慎；先说明方案，实际编辑应小步、可核查。

---

## Obsidian / MOC 约定

- LG 使用 wikilink：`[[...]]`。
- 跨项目链接必须尽量写完整 vault 路径，尤其是 `_MOC.md`，避免同名误入。
- `HOME.md` 是主路由，不承载所有细节。
- 项目 `_MOC.md` 负责项目入口和模块导航。
- 专题 MOC 应使用明确领域名或唯一 alias。
- MOC 过大时，优先增加路由表和专题索引，不直接删减历史列表。

---

## 状态标记

整理旧内容时优先用状态表达，不要急删：

| 状态 | 含义 |
|---|---|
| `current` | 当前有效 |
| `historical` | 历史记录，保留追溯价值 |
| `deprecated` | 已废弃，不应继续作为执行依据 |
| `needs-review` | 可能过期，待确认 |

---

## 关键入口

- [[HOME|LibraryG 主入口]]
- [[工作空间总纲|工作空间总纲]]
- [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]]
- [[02-PROJECTS/Agent/工作流/评估-LibraryG结构与AI读取稳定性-2026-08-10|LibraryG 结构与 AI 读取稳定性评估]]
- [[02-PROJECTS/Agent/工作流/规范-多项目工作流与复现|多项目工作流与复现]]
- [[02-PROJECTS/Agent/工作流/规范-MOC命名与导航层级|MOC 命名与导航层级规范]]
- [[02-PROJECTS/Agent/工作流/工作内容日志同步规范|工作内容日志同步规范]]
- [[02-PROJECTS/Agent/WorkBuddy-MEMORY/WB-MEMORY_MOC|WorkBuddy MEMORY 历史归档]]
- [[02-PROJECTS/TileMatch/参考/MT老项目路径索引|MT 老项目路径索引]]
- [[02-PROJECTS/TileScape/_MOC|TileScape MOC]]
- [[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]]
