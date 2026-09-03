# WorkBuddy 知识闭环运行目录

当前执行依据：[[02-PROJECTS/Agent/工作流/方案-WorkBuddy日志知识闭环自动化实施|WorkBuddy 日志知识闭环自动化实施方案]]。

## 允许的状态流转

`ready → processing → processed/YYYY-MM`  
`ready / processing → needs-review`  
`processing → failed`

只处理 `queue/ready/` 内 `status: ready` 且 `risk: low` 的任务包。不得修改 MT / TS 业务代码、移动/删除历史资料、commit 或 push。

## 运行前读取

1. `AGENTS.md`
2. `AI总MOC.md`
3. `02-PROJECTS/Agent/工作流/方案-WorkBuddy日志知识闭环自动化实施.md`
4. `02-PROJECTS/Agent/工作流/规范-任务知识沉淀闭环与自动巡检.md`
5. `02-PROJECTS/Agent/工作流/工作内容日志同步规范.md`

模板位于 `templates/`；报告写到 `reports/YYYY-MM/`。没有有效任务包时，仅生成 `report_only` 状态报告，不得补写猜测内容。
