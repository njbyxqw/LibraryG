---
schema_version: 1
id: KC-20261009-001-chuzzle-detail-inventory
status: needs-review
risk: medium
projects: [Chuzzle, LibraryG]
created_at: 2026-10-09T00:00:00+08:00
producer: Codex
source_evidence:
  - kind: user_confirmation
    ref: "2026-10-09 当前对话"
    summary: "用户要求在 LG 新建 Chuzzle 项目框架，并将后续细节整理成 WorkBuddy 任务清单。"
    verification: confirmed
  - kind: static_review
    ref: "ChuzzleDemo/Assets/Game/Chuzzle/; ChuzzleDemo/Docs/"
    summary: "已确认顶层代码、Docs、编辑器与测试路径；细节调用链和 Unity 验收尚未完成。"
    verification: partial
---

# Chuzzle 项目细节整理与验收拆包

## 当前状态

`needs-review`，不得自动执行。

## 原因

以下事项需要解释当前代码、核对设计与实现差异，或运行 Unity 场景。它们不满足 WorkBuddy 仅处理“低风险、来源充分、正文固定”的写入条件。

## Codex 已完成的静态取证

1. 程序集依赖、Module → Game 生命周期：[[02-PROJECTS/Chuzzle/代码框架/梳理-运行时程序集与生命周期静态审计-2026-10-09|静态审计]]。
2. authored / 程序化关卡、元素目录与 Booster 规则加载：[[02-PROJECTS/Chuzzle/代码框架/梳理-关卡配置加载与生成-2026-10-09|配置加载与生成静态审计]]。
3. Record / Replay / Snapshot / Reconnect 和测试文件覆盖：[[02-PROJECTS/Chuzzle/代码框架/梳理-记录回放恢复与测试地图-2026-10-09|记录与测试地图]]。
4. 显示层文档—代码对照：[[02-PROJECTS/Chuzzle/代码框架/梳理-显示层重构现状静态对照-2026-10-09|显示层对照]]。
5. 设计合同差异：[[02-PROJECTS/Chuzzle/代码框架/梳理-设计合同与当前代码差异-2026-10-09|差异清单]]。

## 剩余 30% WorkBuddy 跟踪项

| ID | 工作项 | 执行前置 | 需要保留的证据 | 状态 |
|---|---|---|---|---|
| WB-C01 | Unity 刷新项目文件，核对 `Chuzzle.Game.csproj` 与真实 `Scripts/Entry/`，再记录编译 / Console 结果 | 可用 Unity Editor、明确 Unity 版本 | 刷新后路径差异、编译状态、Console 首个错误或通过截图 | needs-review |
| WB-C02 | 执行编辑器 P006、关卡编辑、试玩、Bot 的验收矩阵 | 指定场景、关卡文件、复现负责人 | 步骤、预期 / 实际、Console、截图 / CSV、Unity 版本 | needs-review |
| WB-C03 | 对已获得明确证据的结论执行固定正文入库 | 由 Codex 提供目标文档、完整正文、锚点、幂等标记 | 输入证据链接与写入后路径 | needs-review |

> [!warning]
> WB-C01 / WB-C02 需要 Unity 交互和判断，不能自动执行。WB-C03 只有在前两项形成来源充分、正文固定的输入后才可另拆为 `risk: low`、`ready` 包。

## 可转为 ready 的条件

每个跟踪项完成取证后，另建一个 `risk: low` 任务包，并明确提供：目标文件、唯一锚点、完整写入正文、幂等标记、来源与验证方式。不得修改本包后直接执行。

## 关联

- [[02-PROJECTS/Chuzzle/任务/任务-项目资料完善与验收|Chuzzle 项目资料完善与验收任务]]
- [[02-PROJECTS/Agent/工作流/方案-WorkBuddy日志知识闭环自动化实施|WorkBuddy 交接规范]]
