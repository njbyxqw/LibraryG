---
title: TileScape 项目文档索引
date: 2026-08-04
tags:
  - tilescape
  - docs-index
type: index
status: finalized
project: TileScape
lifecycle: current
verification: index-only
priority: medium
cat_order: 020
---

# TileScape 项目文档索引（Docs/ + Doc/ 整理备注）

> 本文档是 `D:\TileScape\Docs\` 与 `D:\TileScape\Doc\` 下未迁移文档的**索引清单**。文档原文仍在项目内，仅做分类整理与价值备注；后续有需求再按主题迁移进知识库。

## 一、Docs/（项目设计 / 迁移文档，58 项）

### 1. 迁移总览 / 全局审计（7）
| 文档 | 备注 |
|---|---|
| `TILEV2_MIGRATION_LANDING_PLAN.md` | 迁移落地总计划 |
| `TILEV2_INTERFACE_MIGRATION_REPORT.md` | 接口迁移报告 |
| `TileV2_Migration_V1_Phase_Report.md` | V1 阶段报告 |
| `TileV2_NonMigrated_Content.md` | 未迁移内容清单 |
| `TileV2_Old_vs_Current_Exhaustive_Behavior_Audit.md` | 新旧行为穷举审计 |
| `Main_vs_Dev_Full_Code_Review_2026-08-01.md` | 主分支 vs dev 全量代码审查 |
| `DELETION_LOG.md` | 删除记录 |

### 2. 架构 / 接口设计（4）
| 文档 | 备注 |
|---|---|
| `R-018_Assembly_Dependency_Graph.mermaid` | 程序集依赖图（高价值） |
| `UIPageView_UITabBar_Component_Interface_Design.md` | UI 组件接口设计 |
| `Obfuz_Build_Entry_Points.md` | 混淆构建入口点 |
| `Obfuz_Symbol_Archive.md` | 混淆符号归档 |

### 3. 系统 / 模块设计（4）
| 文档 | 备注 |
|---|---|
| `FlyModule_System_Design.md` | Fly 模块系统设计 |
| `Scroll_Gesture_Routing_Runtime_Auto_Installation_Design.md` | 滚动手势路由自动安装设计 |
| `FontArt/`（3 篇） | UITextArt 设计/模板/工作流 |
| `UIManager_Lifecycle_Repair_Plan.md` | UIManager 生命周期修复 |

### 4. DataCenter 数据中心（5）
| 文档 | 备注 |
|---|---|
| `TileV2_DataCenter_Requirements_Derivation.md` | 需求推导 |
| `TileV2_DataCenter_Code_Driven_Implementation_Plan.md` | 代码驱动实现计划 |
| `TileV2_DataCenter_Behavior_Parity_Test_Matrix.md` | 行为对齐测试矩阵 |
| `TileV2_DataCenter_Phase6_Migration_Record.md` | Phase6 迁移记录 |
| `TileV2_DataCenter_Phase7_Migration_Record.md` | Phase7 迁移记录 |

### 5. 玩法机制迁移（8）
| 文档 | 备注 |
|---|---|
| `TileV2_Prop_Migration_Baseline.md` / `_Implementation_Plan.md` / `_Staged_Plan.md` | 道具迁移（基线/计划/分阶段） |
| `TileV2_Reward_Migration_Implementation_Plan.md` | 奖励迁移 |
| `TileV2_Condition_FunctionUnlock_Migration_Implementation_Plan.md` | 条件 FunctionUnlock 迁移 |
| `TileV2_Replay_UI_Migration_ImplementationPlan.md` | 回放 UI 迁移 |
| `TileV2_SimplePanels_UIFlow_MigrationPlan.md` | 简单面板 UI 流迁移 |
| `TileV2_UIGamePanel_UIManager_MigrationPlan.md` | UIGamePanel/UIManager 迁移 |

### 6. 新手引导 Tutorial（9）
| 文档                                                                                             | 备注                 |
| ---------------------------------------------------------------------------------------------- | ------------------ |
| `TileV2_Tutorial_NewFramework_Implementation_Plan.md` / `_Audit.md` / `_Developer_Tutorial.md` | 新框架迁移（计划/审计/开发者教程） |
| `TileScape_Tutorial_Requirements_Gap_Audit_2026-07-29.md`                                      | 需求缺口审计             |
| `TileScape_First_Main_Tutorial_Implementation_Plan_2026-07-29.md`                              | 首个主引导实现计划          |
| `TileScape_vs_Meatloaf_Tutorial_System_Design_Comparison_2026-07-28.md`                        | 新旧项目引导系统对比         |
| `Tutorial_Framework_Complexity_Audit_And_Optimization.md`                                      | 框架复杂度审计            |
| `Tutorial_Framework_Lean_Architecture_Implementation_Plan.md`                                  | 精简架构计划             |

### 7. 适配 / 性能 / 资源（6）
| 文档 | 备注 |
|---|---|
| `TileV2_Gameplay_Fixed_1080_Width_Adaptation_Plan.md` / `_Baseline.md` / `_Execution_Steps.md` / `_Validation.md` | 1080 固定宽度适配（4 篇） |
| `TileV2_Gameplay_Layout_Structure_Refactor_Plan.md` | 局内布局结构重构 |
| `TileScape_XAsset_Android_Bundle_Optimization_Audit.md` | Android Bundle 优化审计 |

### 8. 编辑器 / Bot（2 + 子目录）
| 文档 | 备注 |
|---|---|
| `TileV2_Editor_Bot_Headless_Migration_Implementation_Plan.md` | 实现计划 |
| `TileV2_Editor_Bot_Headless_Migration/`（12 文件） | adapt_manifest、baseline、headless-diff-classification、runtime_manifest、migration_acceptance_report、assembly_dependency_report、resource_reference_report 等 |

### 9. 分析 / 打点（3）
| 文档 | 备注 |
|---|---|
| `TileScape_Analytics_Full_Audit_2026-07-28.md` | 打点全量审计 |
| `TileScape_Analytics_Final_Review_Repair_Report_2026-07-28.md` | 终审修复报告 |
| `TileScape_Analytics_Blockers_Status_2026-07-29.md` | 阻塞项状态 |

### 10. 商业化（5）
| 文档 | 备注 |
|---|---|
| `TileScape_Ad_System_Capability_Migration_Implementation_Plan.md` / `_Record.md` | 广告系统迁移（计划/记录） |
| `TileScape_Trade_Purchase_Design_Review_2026-08-01.md` | 交易/购买设计评审 |
| `TileScape_Trade_Purchase_Fix_Plan_2026-08-01.md` / `_2026-08-03.md` | 交易/购买修复计划（两版） |

### 11. 配置 / Profile / UserLayer（3）
| 文档 | 备注 |
|---|---|
| `TileScape_GoogleDrive_Config_Profile_Full_Audit_2026-07-27.md` | 配置/Profile 审计 |
| `TileScape_UserLayer_Config_Completeness_Audit_And_Repair_Plan_2026-08-03.md` | UserLayer 配置完整性审计与修复 |
| `UserLayer_Full_Migration_Implementation_Plan.md` | UserLayer 全量迁移计划 |

## 二、Doc/（Meatloaf 源项目迁移过程记录，12 项）

> 多为**历史流水记录**（每日迁移报告），价值低于 Docs/ 的设计文档，一般不需迁移；仅保留索引备查。

| 文档 | 备注 |
|---|---|
| `Meatloaf_Dev_Delta_Migration_Stage0_2026-07-23.md` | 迁移 Stage0 |
| `Meatloaf_Dev_Delta_Migration_Manifest_2026-07-23.tsv` | 迁移清单（tsv） |
| `Meatloaf_Dev_Delta_Migration_Report_2026-07-23/24/25/26/30.md`（5 篇） | 每日迁移报告 |
| `Meatloaf_Dev_Delta_Content_Disposition_2026-07-25.md` | 内容处置说明 |
| `Meatloaf_Payment_Fulfillment_Risk_2026-07-24.md` | 支付履约风险 |
| `TileScape_Migration_Commit_Static_Review_2026-07-24.md` + `.dependency-graph.Mermaid` | 迁移提交静态审查 |
| `FoldableScreenAdaptationPlan.md` | 折叠屏适配计划 |

## 三、迁移优先级建议（后续有需求时参考）

- **高价值优先**（设计类，建议优先迁移）：R-018 程序集依赖图、Tutorial 新框架、DataCenter 需求推导、Trade/Purchase 设计评审、Ad 系统迁移、Fly 系统设计、UserLayer 计划
- **中价值**：玩法机制迁移各计划（Prop/Reward/Condition）、1080 适配、编辑器 Bot Headless
- **低价值/不迁移**：Doc/ 每日迁移报告、DELETION_LOG、Obfuz 构建细节

## 关联

- [[02-PROJECTS/TileScape/_MOC|TileScape 知识库 MOC]] — 项目总入口
- [[代码框架/代码框架总览|代码框架总览]] — 程序集/目录/关键类索引
