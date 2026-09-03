---
tags:
  - TileMatch
  - Git
  - 配置
type: note
status: finalized
date: 2026-06-26
cat_order: 001
---

# 记录 - gitignore 本地忽略配置

## 背景

WorkBuddy 工具在 TileMatch 项目中运行后会产生 `.workbuddy/`、`workbuddy_archives/`、`automation-*/` 等产物目录，导致 `git status` 频繁变脏。需要配置忽略规则，同时不将这些忽略规则提交到远程仓库。

## 操作记录

### Step 1: 恢复 .gitignore 到 committed 版本

此前误将 WorkBuddy 忽略规则写入了 `.gitignore`（会被提交到远程），需要恢复到已提交版本：

```bash
git restore .gitignore
```

- 将 `.gitignore` 恢复到最近一次 commit 的版本
- 移除了误加的 WorkBuddy 相关忽略规则

### Step 2: 迁移忽略规则至 .git/info/exclude

Git 支持 `.git/info/exclude` 作为本地生效的忽略配置，**不会被提交到远程仓库**，正好满足需求。

将 WorkBuddy 忽略规则从 `.gitignore` 迁移至 `.git/info/exclude`：

```
路径: .git/info/exclude
作用范围: 仅本地仓库生效
是否提交: 否（.git/ 目录不入库）
```

### Step 3: 初版 exclude 规则问题

初版 `exclude` 包含通配规则：

```
*.md
```

**问题**：`*.md` 会递归忽略仓库中所有 `.md` 文件，导致项目子目录中的合法 `.md` 文件（如设计文档、README 等）也被忽略，造成误伤。

**处理**：已删除该规则。

### Step 4: 最终 exclude 规则

经过迭代，最终 `.git/info/exclude` 规则如下：

```gitignore
# WorkBuddy 产物
.workbuddy/
.codebuddy/
workbuddy_archives/
automation-*/

# 日志文件
client/fbg.log

# 本地编辑器扩展（不提交）
client/Assets/Editor/
client/Assets/Editor.meta
```

### 规则说明

| 规则 | 忽略目标 | 说明 |
|------|----------|------|
| `.workbuddy/` | WorkBuddy 工作目录 | 工具运行产物 |
| `.codebuddy/` | CodeBuddy 工作目录 | 工具运行产物 |
| `workbuddy_archives/` | 归档目录 | 历史归档产物 |
| `automation-*/` | 自动化任务目录 | 自动化任务产物 |
| `client/fbg.log` | 日志文件 | 运行时日志 |
| `client/Assets/Editor/` | 本地编辑器扩展 | Unity 本地编辑器扩展，不提交 |
| `client/Assets/Editor.meta` | Editor 目录的 meta 文件 | Unity meta 文件，配套忽略 |

## 最终验证

```bash
git status
```

**结果**：`git status` 不再因 WorkBuddy 产物变脏，工作区干净。

## 经验总结

| 要点 | 说明 |
|------|------|
| 本地忽略用 `.git/info/exclude` | 不入库，仅本地生效 |
| 避免使用 `*.md` 等宽泛通配 | 会递归匹配，误伤子目录文件 |
| 本地编辑器扩展可放入 exclude | 不影响团队其他成员 |
| 定期检查 `git status` | 确认忽略规则生效，无遗漏 |

## 关联

- [[_MOC|TileMatch 知识库 MOC]]

文档

- [[规范-本地扩展开发|本地扩展开发规范]] - 本地编辑器扩展开发规范（对应 `client/Assets/Editor/` 忽略项）
