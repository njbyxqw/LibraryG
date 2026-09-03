---
title: LibraryG 结构与 AI 读取稳定性评估
date: 2026-08-10
type: report
status: finalized
lifecycle: current
priority: high
tags: [LibraryG, 评估, AI读取, MOC, 知识库维护]
---

# LibraryG 结构与 AI 读取稳定性评估

> 本评估基于 `HOME.md`、`02-PROJECTS/Agent/Memory.md`、TileMatch / TileScape 项目 MOC、Agent 工作流规范目录。目标是判断当前 LG 是否容易被 AI 稳定读取，以及哪些设计会导致文档读不到或读偏。

---

## 总体判断

LG 当前已经有比较合理的三层结构：

| 层级 | 当前载体 | 评价 |
|---|---|---|
| 全库入口 | `HOME.md`、`工作空间总纲.md` | 方向正确，适合作为 AI 第一入口。 |
| 长期记忆 | `02-PROJECTS/Agent/Memory.md` | 已经能告诉 AI 路径、偏好、项目边界和冷启动顺序。 |
| 项目入口 | `02-PROJECTS/<项目>/_MOC.md` | TileMatch 较完整，TileScape 还偏轻。 |
| 流程规范 | `02-PROJECTS/Agent/工作流/` | 已覆盖 MOC、入库、Daily、INBOX、多项目复现。 |

结论：**基础设计可用，但还没有完全“抗 AI 误读”。** 主要风险来自入口重复、短链歧义、规则分散、旧规则残留、MOC 粒度不均。

---

## 主要问题

| 优先级 | 问题 | 影响 | 建议 |
|---|---|---|---|
| P1 | `_MOC.md`、`_项目概览.md` 等文件名在多个项目重复，项目内短链容易歧义。 | AI 或 Obsidian 可能跳到另一个项目的同名文件。 | 跨项目链接必须使用完整 vault 路径；项目内也建议对 `_MOC`、`_项目概览` 这类同名入口用完整路径。 |
| P1 | “AI 如何读 LG”规则分散在 `AGENTS.md`、`HOME.md`、`Memory.md`、多个工作流规范。 | AI 可能只读其中一个入口，漏掉入库或检索规则。 | 把冷启动读取协议固化进 `Memory.md` 和 `规范-任务产出入库与维护.md`。 |
| P1 | `HOME.md` 信息量偏大，既有工作流、项目入口、插件说明、历史 CLI。 | 首屏负担重，AI 容易在旧 CLI 或长列表里迷路。 | `HOME.md` 顶部增加“AI 必读 5 条”；历史 CLI 降级为历史参考。 |
| P2 | TileMatch MOC 很完整，但列表长；TileScape MOC 还很轻。 | TileMatch 容易读太多，TileScape 容易读不到具体模块。 | TileMatch 可增加专题路由表；TileScape 应继续补模块 MOC 或索引。 |
| P2 | `03-KNOWLEDGE` 是跨项目知识，但没有总 MOC。 | 通用知识只能靠 HOME 少量入口或搜索，容易漏。 | 新建 `03-KNOWLEDGE/_MOC.md` 或在 HOME 中明确通用知识路由。 |
| P2 | 旧 Windows/WorkBuddy 自动化内容仍在多个规范里出现。 | AI 可能误以为旧路径和旧 CLI 仍可执行。 | 保留历史，但统一标 `historical`，当前执行规则以 macOS 路径和 Memory 为准。 |
| P2 | `status` / `type` 在不同区域不完全统一。 | Dataview 和健康检查可能漏文档。 | 不强制全库一套字段，但每个区域要声明自己的字段规则。 |
| P3 | Daily 数量增长后缺少近期/主题索引。 | AI 做复盘时可能需要读太多 Daily。 | 定期生成周/月总结或主题索引，Daily 详细记录保留。 |

---

## 读不到文档的典型原因

1. **同名短链**：例如 `_MOC`、`_项目概览` 在多个项目重复。
2. **入口只挂在 HOME，未挂项目 MOC**：AI 进入项目 MOC 后看不到新文档。
3. **文档只在 Daily 里提到，没有稳定文档或索引**：后续只能靠日期回忆。
4. **草稿留在 INBOX**：没有进入项目目录或通用知识目录。
5. **旧规则和当前规则混在一起**：AI 不知道哪个是执行依据。
6. **通用知识没有专题 MOC**：只能搜索，不能沿导航进入。

---

## AI 读取 LG 的稳定协议

以后 AI 做 LibraryG 相关任务时，按以下顺序读取：

1. **冷启动固定读**：`AGENTS.md`、`HOME.md`、`工作空间总纲.md`、`02-PROJECTS/Agent/Memory.md`。
2. **任务归类**：判断任务属于 LG 工作流、TileMatch、TileScape、跨项目、Daily/INBOX、通用知识还是代码任务。
3. **读对应 MOC**：项目任务读对应项目 `_MOC.md`；工作流任务读 `02-PROJECTS/Agent/工作流/` 中相关规范。
4. **读稳定规范**：入库、MOC、Daily、INBOX、多项目复现任务必须读对应规范。
5. **局部检索**：只在已定位的目录内用关键词检索；找不到再沿 MOC 上一级扩大范围。
6. **禁止默认全盘搜索**：除非用户明确要求全库查找，或 MOC / Memory 路径失效。
7. **给出来源路径**：回答或改文档时说明依据来自哪些文件，不把未确认聊天内容当事实。
8. **任务结束入库**：稳定产物更新 MOC、Daily 和必要索引。

---

## 建议改进顺序

| 阶段 | 动作 | 收益 |
|---|---|---|
| 立即 | 把 AI 读取协议写入 `Memory.md` 和入库规范。 | 降低盲搜和漏读。 |
| 短期 | 在 `HOME.md` 顶部增加“AI 必读入口”。 | 冷启动更快。 |
| 短期 | 修正同名入口的短链，尤其跨项目 `_MOC`、`_项目概览`。 | 降低误跳项目。 |
| 中期 | 新建 `03-KNOWLEDGE/_MOC.md`。 | 通用知识可导航。 |
| 中期 | 为 TileScape 补模块级索引。 | TS 文档逐渐增多后不散。 |
| 长期 | 做定期健康检查：MOC 覆盖、断链、INBOX 残留、Daily 周总结。 | 长期可维护。 |

## 关联

- [[HOME|LibraryG 主入口]] — 全库主入口
- [[02-PROJECTS/Agent/Memory|Agent Memory]] — AI 冷启动记忆
- [[规范-任务产出入库与维护|任务产出入库与维护规范]] — 入库闭环
- [[规范-MOC命名与导航层级|MOC 命名与导航层级规范]] — MOC 与链接规则
- [[工作内容日志同步规范|工作内容日志同步规范]] — Daily 记录规则
