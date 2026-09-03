---
title: MEMORY-用户级-原始存档
date: 2026-07-08
type: archive
status: active
tags: [WorkBuddy, MEMORY, 存档]
---

# MEMORY 用户级原始存档（append-only）

> **来源**：`~/.workbuddy/MEMORY.md`
> **规则**：每次蒸馏/清理时，将当期完整内容作为新切片追加到末尾。当前用户级未超限，暂仅存档快照。

---

## [2026-07-08] #001 快照存档

**事件**：首次蒸馏中用户级 MEMORY 快照存档（未精简，仅备份）
**原因**：用户级 ~2.5k/4,000 字符未超限，暂不蒸馏
**变化**：无

### 当前原文

# 用户级记忆

## 🚨 Git / 提交硬规则（最高优先级）
> 范围（2026-07-06 用户纠正）：**「禁止自动 commit」仅针对 `meatloaf_client01` 公用 git**；**私人 git 在用户授权下可 commit**。
- `meatloaf_client01` 公用 git：**禁止任何自动化 / 脚本自动 commit / push**（周度自动化、Python/Bash、AI 自主行为一律不允许）
- 私人 git：用户显式授权（"提交一下"/"备份到私人git"）后可 commit/push，先展示待 commit 内容
- `.workbuddy/memory` 默认不进 git（gitignored），仅用户单独明确指示才纳入
- Unity 代码一般本地/gitignore，是否版本控制由用户决定
- 任何 git 写操作均先展示待 commit 内容再执行

## 工作环境
- **Obsidian 仓库**: D:\LibraryG (vault 名称: LibraryG)
- **Obsidian 版本**: 1.12.7, CLI 已启用
- **CLI 路径**: D:\Obsidian\Obsidian.exe (需 `export PATH="$PATH:/d/Obsidian"`)
- **主项目代码**: D:\meatloaf_client01\Claw (TileMatch, Unity/C#)

## Obsidian 工作流约定
- **定位**：Obsidian 是所有项目的优先知识库 / 单一源；Notion 作为 Obsidian 的**单向云镜像（离机副本）**，待重连后实施（2026-07-06 起）
- **MCP 优先**：vault 读写优先使用 Obsidian MCP 工具（`mcp__obsidian-mcp__*`），批量扫描用 Grep/Glob
- 每日笔记: 01-DAILY/YYYY-MM-DD.md
- 新文件默认: 00-INBOX/
- 模板目录: 04-TEMPLATES/ (5个模板: daily/tech-analysis/project/meeting/quick)
- 附件: 00-INBOX/attachments/
- 链接格式: Wikilink ([[ ]])
- 同步标记: frontmatter 中 `workbuddy_sync: true`
- WorkBuddy 记忆: .workbuddy/memory/ (MEMORY.md + 日期日志)
- **索引联动**：新增/修改文档后必须更新对应项目的 _MOC.md 和 MEMORY.md 索引
- **健康检查**：项目 vault 定期执行健康检查（断链/frontmatter/索引同步/命名合规）

## 沟通偏好
- 简洁中文，高度结构化输出
- 对比类内容用表格
- 先评估后实施，确认后执行
- "ok，执行吧" = 确认执行
- "存档/保存" = 触发文档保存
- 三句话总结获取核心信息
- **长回复输出偏好**：尽量在聊天里显示完整内容，不要把长文默认收进文档只给摘要；仅当内容确实过长（有客户端折叠风险）时，才落文档到 Obsidian，并**明确提醒用户"已存到 Obsidian：<路径>"**，同时在聊天里给出要点摘要
- **不要反复查找：找不到文件/路径/配置时直接问用户，不要绕弯子**
- **🚨 禁止私自用 Python 脚本批量改文件**：涉及文件内容修改必须先展示方案、用户确认后再执行；Python 脚本只能用于只读分析（扫描/统计/查找），不能写文件；如确需脚本辅助写文件，必须先打印 diff 供确认
- **MEMORY.md 清理约束**：超限清理/蒸馏时**保守合并、不删仍相关内容**；关键长期事实优先存 Obsidian 单一源而非只留 MEMORY；清理后简要告知用户删/合并了什么

## 已安装技能
- workbuddy-obsidian-workflow: Obsidian 仓库操作工作流
- obsidian-cli-official: Obsidian 官方 CLI (v1.12+, 115 命令)
- obsidian: Obsidian 直接读写 (vault = 普通文件夹)
