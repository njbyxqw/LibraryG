---
title: MEMORY-项目级-原始存档
date: 2026-07-08
type: archive
status: active
tags: [WorkBuddy, MEMORY, 存档]
---

# MEMORY 项目级原始存档（append-only）

> **来源**：`meatloaf_client01\.workbuddy\memory\MEMORY.md`
> **规则**：每次蒸馏/清理时，将当期完整内容作为新切片追加到末尾。每个切片标注时间、编号、事件、原因、精简前后变化。
> **Obsidian 字符上限**：经查 Obsidian 为纯 Markdown 编辑器，单篇无字符上限，持续追加无压力。

---

## [2026-07-08] #001 首次蒸馏

**事件**：项目级 MEMORY 首次蒸馏（Task B · 知识库整理完成后的第二步）
**原因**：严重超限（206行/约15k字符，限制3k），「项目资料库索引」全表与 Obsidian [[_MOC]] 重复
**精简前后**：206行/15k → 77行/2,445字符；删 100+ 行重复索引表格 + 压缩 Notion/备份/文档规则为摘要

### 蒸馏前原文

# 项目约定

## Obsidian 优先知识库管理规则（最高优先级）

> Obsidian 是 TileMatch 项目的**唯一权威知识库**。所有文档、分析、报告必须以 Obsidian 为单一源。

### 核心原则
1. **单一源**：所有知识文档只存在于 `D:\LibraryG\02-PROJECTS\TileMatch\` 下，禁止在 `D:\meatloaf_client01\` 或其他位置生成归档文档
2. **MCP 优先**：对 vault 的读写操作优先使用 Obsidian MCP 工具（`mcp__obsidian-mcp__*`），仅在 MCP 不可用时降级为文件系统操作
3. **索引联动**：每次新增/修改/删除文档后，必须同步更新 `_MOC.md` 索引和本文件的「项目资料库索引」表
4. **规范先行**：所有文档必须遵循 `[[规范-知识库文档分类标准]]` 的命名、frontmatter、分类要求
5. **健康检查**：每周一自动化执行 vault 健康检查（断链/frontmatter/索引同步/命名合规），手动触发时用 Grep + Glob 扫描

### 操作优先级
| 场景 | 工具 | 说明 |
|------|------|------|
| 读取/搜索 vault 内容 | `mcp__obsidian-mcp__search_vault` / `mcp__obsidian-mcp__read_note` | MCP 优先 |
| 创建新笔记 | `mcp__obsidian-mcp__create_note` | 自动放置到正确目录 |
| 编辑现有笔记 | `mcp__obsidian-mcp__update_note` | 支持 replace/insert 模式 |
| 批量扫描/统计 | `Grep` + `Glob` 工具 | MCP 不适合批量操作时使用 |
| 健康检查 | `Grep` + `Glob` + `Bash(wc)` | 定期/手动触发 |

### 知识库健康标准
- ✅ 零断链（所有 `[[]]` wikilink 指向的文件存在）
- ✅ 100% frontmatter 合规（title/date/type/status/tags 五字段齐全）
- ✅ _MOC.md 索引与实际文件 1:1 对应
- ✅ 文件命名符合分类标准（规范-/报告-/分析-/笔记-前缀）
- ✅ 零污染（无内容被错误覆盖）

## Notion 同步规则（Obsidian → Notion 单向云镜像，实施中）

> 2026-07-06 用户决定：因熟悉 Notion 且需离机安全，**把 Obsidian 当前版本单向同步到 Notion 作为云副本**；私人 git 暂缓（用户需时间学 git）。Obsidian 仍是单一源，Notion 仅为只读镜像。

- **方向**：Obsidian（单一源）→ 单向同步 → Notion（云镜像 / 离机副本）
- **现状**：Notion connector 当前 disconnected，无 notion MCP 工具，当前无法直接推送；待用户重连 connector 或提供 Notion integration token + 父页面
- **令牌/工作量评估**：见当日日志「Notion 同步决策」；大文件（关卡文件变更追踪 7514 行）需分批 block，推荐 Python 脚本方案省 token
- **原则**：同步为单向镜像，不在 Notion 反向编辑；wikilink/反链在 Notion 不原样保留（转纯文本或 Notion 链接）
- **标签体系（历史参考）**：Rocket(pink)、文件迁移(blue)、白盒关卡(green)、曲线优化(yellow)、备份梳理(orange)、编辑器(purple)、打点(red)、游戏逻辑(gray)

## Git / 提交硬规则（2026-07-06 确立，最高优先级）

> ⚠️ **范围澄清（2026-07-06 用户纠正）**：「禁止自动 commit」**仅针对 `D:\meatloaf_client01` 的公用 git**；用户的**私人 git 在明确授权下可以 commit**。

1. **`meatloaf_client01` 公用 git：禁止任何自动化 / 脚本自动 commit / push**（含周度自动化、Python/Bash 脚本、AI 自主行为）。**绝对不允许。**
2. **私人 git：可在用户显式授权下 commit / push**（如"提交一下""备份到私人 git"）；授权后先展示待 commit 内容再执行。
3. `.workbuddy/memory`（AI 本地工作记录）**默认不进 git**，保持 gitignored；仅当用户单独明确指示时才可纳入。
4. Unity 代码（`D:\meatloaf_client01\Claw` 等）一般存本地或 gitignore，是否进版本控制由用户决定。
5. 任何 git 写操作（无论哪个仓库）均**先展示待 commit 内容**供确认，再执行。

## 备份与维护现状（2026-07-06 评估 + 2026-07-06 用户纠正）

| 路径 | Git | 远程 | 云同步 | 状态 |
|------|-----|------|--------|------|
| `D:\meatloaf_client01`（Unity 代码） | ✅ | ✅ gitlab | ❌ | 按用户习惯保持本地/远程，不强制 |
| `D:\meatloaf_client01\.workbuddy\memory` | ❌ gitignored（**有意**） | ❌ | ❌ | ✅ 本地工作记录，按规则不进 git |
| `D:\LibraryG`（Obsidian vault = 优先知识库） | ❌ | ❌ | ❌ | 🔴 **零备份，需用户确认方案后处理** |

- **备份方向**（待用户确认，详见对话）：考虑用户的**私人 git** 作为远端；可选项含 LibraryG 单独 git 仓库手动 push / 文件级 robocopy 到第二磁盘或云 / Obsidian Sync 等
- **状态**：离机安全方案已定 → **Obsidian → Notion 单向云镜像**（实施中，待重连 connector）；私人 git 暂缓（用户需时间学 git，授权后可 commit）

## 文档生成规则
- **目标路径**：生成归档文档（梳理报告、逻辑分析等）时，直接 `Write` 到 Obsidian 仓库：
  `D:\LibraryG\02-PROJECTS\TileMatch\[分类]\[文件名].md`
- **Frontmatter**：生成时自动加上：
  ```yaml
  ---
  tags: [TileMatch, 分类标签]
  status: draft
  date: YYYY-MM-DD
  ---
  ```
- **分类目录**：编辑器 → `编辑器/`，打点 → `打点/`，游戏逻辑 → `游戏逻辑/`，Rocket → `Rocket/`
- **禁止生成到**：不再生成文档到 `D:\meatloaf_client01\` 下（避免两处不同步）

## 文档存档规则
- **触发词**：用户说"整理文档""存档""日志""同步""归档""存一下"等 → 生成的 .md 文件为归档文档
- **归档文档**：一旦标记为归档，非必要不修改；Notion 同步已暂停，归档仅存于 Obsidian（单一源）
- **日志标记**：当天 `memory/YYYY-MM-DD.md` 必须在"输出"小节中用 `生成 \`xxx.md\`` 格式标记所有归档文档，供自动化检测
- **资料库索引联动**：每次生成归档文档后，更新 Obsidian `_MOC.md` 和 `MEMORY.md` 索引表

## 项目资料库索引

> 知识库已迁移至 Obsidian，以后只维护 Obsidian 里的笔记。
> 路径：`02-PROJECTS/TileMatch/`，入口：`[[_MOC]]`
> AI 需要时用 Grep 搜索 Obsidian 仓库里带对应 tag 的笔记。
> ⚠️ 此段以下原包含 22 条概念速查 + 编辑器/打点/游戏逻辑/Rocket/工具/障碍牌/Effect 全分类表格（~100行），在蒸馏中被精简为 8 条核心速查。原文详细表格见蒸馏前 git 历史或此存档早期版本。