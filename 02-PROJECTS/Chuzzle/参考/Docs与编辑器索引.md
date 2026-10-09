---
title: Chuzzle Docs 与编辑器索引
date: 2026-10-09
type: reference
status: current
lifecycle: current
project: Chuzzle
tags: [Chuzzle, Docs, 编辑器, LevelEditor, LevelBot]
source: "ChuzzleDemo/Docs 与 Assets/Game/Chuzzle/Editor 静态目录整理"
verification: "static-review; editor runtime pending"
---

# Chuzzle Docs 与编辑器索引

## Docs 路由

| 仓库目录 | 内容 | 使用边界 |
|---|---|---|
| `Docs/01-竞品分析/` | Jex、PiggyMatch、TileScape 的玩法分析 | 参考材料，不替代 Chuzzle 当前实现 |
| `Docs/02-整体方案概述/` | 产品范围、统一语言、运行时边界、领域模型、记录/恢复、完成门禁 | 当前设计合同的优先入口；仍需按代码核对时效 |
| `Docs/03-详细落地方案/` | 玩法从冻结边界到验收的分阶段方案 | 设计/实施依据，不能凭文件存在认定已实现 |
| `Docs/04-落地实施/` 与 `05-落地实施细项/` | 实施提示、阶段记录和验收 | 历史实施过程，需标明对应日期与验证范围 |
| `Docs/06-后续处理/` | 显示层、程序化关卡、Booster、掉落、全局花色等后续主题 | 待核实的计划、讨论与部分实施记录混存 |
| `Docs/编辑器/` | 关卡编辑器迁移、试玩、Bot、设计方案与复盘 | 编辑器工作的首选资料入口 |

## 编辑器代码地图

| 范围 | 路径 | 当前定位 |
|---|---|---|
| 关卡编辑器 | `Assets/Game/Chuzzle/Editor/LevelEditor/` | 场景、编辑面板、命令、保存、验证、试玩接线 |
| 试玩 | `.../LevelEditor/Script/Dependency/EditorTrialLauncher.cs`、`EditorTrialController.cs` | 从编辑场景创建独立试玩并负责返回/清理 |
| Bot | `Assets/Game/Chuzzle/Editor/LevelBot/` | 参数、单局运行、批次控制、统计、输出与断点恢复 |
| 编辑关卡数据 | `Assets/Game/Chuzzle/Editor/LevelConfig/Levels/` | 编辑器使用的关卡组；与正式运行时配置边界需按操作确认 |
| 辅助校验 | `ChuzzleBoardPresentationValidator.cs`、`LevelConfigValidator.cs`、`LevelDiagnostic.cs` | 编辑期检查工具 |

## 已登记的编辑器状态

| 项目 | 状态 | 来源与边界 |
|---|---|---|
| 编辑器迁移 01–15 | 历史记录称已按计划实施 | `Docs/编辑器/ChuzzleEditor迁移记录.md`；不等于当前 Unity 运行验收 |
| 编辑、保存、目录、花色/目标、棋盘/入口、模板 | 静态接线已记录，运行待验收 | 历史记录明确未完成真实鼠标/键盘验收 |
| 全手绘试玩返回 | 静态接线已记录，运行待验收 | 需 Play Mode、视觉与返回验证 |
| Bot、统计、CSV、续跑 | 静态接线已记录，运行待验收 | 需真实跑关、固定种子、输出失败与恢复验证 |
| P006：Undo / Redo 队列 | 未修复继承限制 | 首次 Redo、全部 Undo 后新增命令和计数限制均需复现与定界 |
| P005：类型显示素材 | 来源缺口 | 624 条显示配置仅 1 张可加载；灰色“图像缺失”不是素材恢复完成 |

## Bug 记录约定

后续编辑器 Bug 统一先写入 [[02-PROJECTS/Chuzzle/任务/任务-项目资料完善与验收#编辑器-Bug-登记|任务主档的 Bug 登记]]，至少包含：复现步骤、使用场景与关卡文件、预期/实际、Console 或截图、稳定复现性、验证状态。确认可复用的根因或修复，再单独沉淀专题文档。

## 关联

- [[02-PROJECTS/Chuzzle/_MOC|Chuzzle MOC]]
- [[02-PROJECTS/Chuzzle/代码框架/代码框架总览|代码框架总览]]
- [[02-PROJECTS/Chuzzle/任务/任务-项目资料完善与验收|项目资料完善与验收任务]]
