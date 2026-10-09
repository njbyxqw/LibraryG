---
title: Chuzzle 知识库 MOC
date: 2026-10-09
type: index
status: current
lifecycle: current
project: Chuzzle
tags: [Chuzzle, Unity, MOC, 关卡编辑器]
source: "ChuzzleDemo 当前工作区静态整理；运行时与 Unity 人工验收另行记录"
---

# Chuzzle 知识库 — 总入口

> ChuzzleDemo 的项目事实、代码导航、编辑器状态与持续整理任务入口。当前只沉淀已核实的目录、程序集、设计文档和历史实施记录；未执行的 Unity 验收不视为功能完成。

## 快速入口

| 需求 | 入口 |
|---|---|
| 项目定位、范围与当前边界 | [[02-PROJECTS/Chuzzle/_项目概览|项目概览]] |
| 运行时、程序集和主要目录 | [[02-PROJECTS/Chuzzle/代码框架/代码框架总览|代码框架总览]] |
| 关卡配置加载与程序化生成 | [[02-PROJECTS/Chuzzle/代码框架/梳理-关卡配置加载与生成-2026-10-09|配置加载与生成静态审计]] |
| 记录、回放、恢复与测试文件 | [[02-PROJECTS/Chuzzle/代码框架/梳理-记录回放恢复与测试地图-2026-10-09|记录回放恢复与测试地图]] |
| 显示层重构的当前代码对照 | [[02-PROJECTS/Chuzzle/代码框架/梳理-显示层重构现状静态对照-2026-10-09|显示层重构现状静态对照]] |
| 设计文档与当前代码差异 | [[02-PROJECTS/Chuzzle/代码框架/梳理-设计合同与当前代码差异-2026-10-09|设计合同与当前代码差异]] |
| 项目 Docs 与关卡编辑器资料 | [[02-PROJECTS/Chuzzle/参考/Docs与编辑器索引|Docs 与编辑器索引]] |
| 后续补充、验收和 Bug 整理 | [[02-PROJECTS/Chuzzle/任务/任务-项目资料完善与验收|项目资料完善与验收任务]] |

## 当前项目框架

- **执行仓库**：`/Users/dean/ChuzzleDemo`；当前整理时为 `dev @ c2be0d58`。分支与提交只说明本次静态快照，后续代码任务需重新确认。
- **玩法核心**：整行或整列循环移动的消除玩法；具体玩家合同以项目 `Docs/02-整体方案概述/00-产品范围与玩家规则.md` 为准。
- **运行时**：`Config`、`DomainEvent`、`Logic.Interface`、`Logic.GameLogic`、`Logic.LevelLogic`、`Game`、`Application`、`View`、`GameRecord` 等独立程序集。
- **编辑器**：`Assets/Game/Chuzzle/Editor/LevelEditor/` 包含关卡编辑、试玩和 Bot 评估；详细状态见 [[02-PROJECTS/Chuzzle/参考/Docs与编辑器索引|Docs 与编辑器索引]]。

## 当前事实与验证边界

| 范围 | 当前结论 | 边界 |
|---|---|---|
| 项目目录、程序集、场景与 Docs 分类 | 已静态核对 | 不代表编译或 Play Mode 通过 |
| 编辑器迁移记录 | 有历史实施与编译记录 | 历史记录不是今天的运行验证 |
| 编辑、试玩、Bot 的真实交互 | 待按场景手工验收 | 需在 Unity 中执行并保留复现信息 |
| 细节资料整理 | 已拆入任务主档 | 需按每项来源补充，不凭文件名或旧方案推断 |

## 待办

- [ ] 按 [[02-PROJECTS/Chuzzle/任务/任务-项目资料完善与验收|任务主档]] 逐项补齐运行时调用链、编辑器验收与测试地图。
- [ ] 新报编辑器问题先登记复现、关卡文件、预期/实际与验证状态，再决定是否进入修复。

## 关联

- [[HOME|LibraryG 主入口]]
- [[AI总MOC|AI 总 MOC]]
- [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护规范]]
- [[02-PROJECTS/Agent/工作流/方案-WorkBuddy日志知识闭环自动化实施|WorkBuddy 交接规范]]
