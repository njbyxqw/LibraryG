---
title: 冷启动指南 — 从零重建工作流与知识库
date: 2026-07-08
type: spec
status: finalized
tags: [规范, 冷启动, 工作流, 知识库]
---

# 冷启动指南

> 换新设备后，按本文档从头建立完整的 Obsidian 知识库 + WorkBuddy 工作流。
> 读完这篇文章，你应该知道：目录怎么建、文档怎么写、自动化怎么配、AI 怎么用。

---

## 一、Vault 结构

```
D:\LibraryG\                         # Obsidian vault 根
├── HOME.md                          # 🔑 全库主入口 MOC（先看这个）
├── HOME-冷启动指南.md                # 本文件
│
├── 00-INBOX/                        # 对话中间产物（每次对话在此建临时文件夹）
├── 01-DAILY/                        # 每日工作日志
│   └── YYYY-MM-DD.md
├── 02-PROJECTS/
│   ├── TileMatch/                   # 三消游戏项目
│   │   ├── _MOC.md                  # 项目 MOC
│   │   └── ...（见下方 TileMatch 子结构）
│   └── WorkBuddy/                   # AI 工作档案
│       ├── 工作流/
│       └── WorkBuddy-MEMORY/
├── 03-KNOWLEDGE/                    # 通用知识（跨项目）
│   ├── Unity/
│   ├── TileV2-Editor/
│   └── Game-Logic/
├── 04-TEMPLATES/                    # 5 个模板
│   ├── tp-daily.md                 # 每日日志
│   ├── tp-meeting.md               # 会议记录
│   ├── tp-project.md               # 项目启动
│   ├── tp-tech-analysis.md         # 技术分析
│   └── tp-quick.md                 # 快速笔记
└── 05-ARCHIVE/                      # 过期文档归档
```

### TileMatch 项目子结构

```
02-PROJECTS/TileMatch/
├── _MOC.md                          # 项目总入口（type: index）
├── _项目概览.md                     # 项目基本信息（type: note）
├── 知识库/
│   ├── 规范-知识库文档分类标准.md    # 🔧 所有规则的权威来源
│   └── 规范-知识库健康检查.md
├── 游戏逻辑/
│   ├── Rocket/（火箭牌）
│   ├── 其他/（死局/跑关/牌局生成）
│   ├── 局内道具/（Shuffle/道具/风车）
│   ├── 局内障碍/
│   │   ├── 局内障碍知识库_MOC.md
│   │   ├── Effect/（16 种）
│   │   └── 障碍牌/（8 种）
│   └── 战前道具/（连胜闪电球）
├── 编辑器/
├── 打点/
├── 工具/（关卡数据分析/关卡文件追踪/_trash）
└── Git工作流/
```

---

## 二、文档规范·总纲

> 详细规则见 `[[02-PROJECTS/TileMatch/知识库/规范-知识库文档分类标准|分类标准]]`

### Frontmatter 必填字段

```yaml
---
title: "显示标题"         # 必填
date: YYYY-MM-DD          # 必填
type: spec|report|analysis|reference|note|index  # 必填，6 选 1
status: draft|finalized   # 必填，2 选 1
cat_order: NNN            # 必填，3 位补零，文件夹内 001 起连续
tags: [TileMatch, 子模块] # 必填
---
```

### type 快速判断

| type | 一句话 | 示例 |
|------|--------|------|
| `spec` | "必须这样做"的规则 | 分类标准、健康检查 |
| `analysis` | 代码逻辑深度分析，有推导过程 | RocketV2 逻辑、死局分析 |
| `report` | 工作成果总结 | 打点梳理、SQL 分析报告 |
| `reference` | 属性速查表，打开即查 | 障碍牌全览、Effect 全览 |
| `note` | 杂项记录/复盘/提案 | gitignore 配置、风车提需 |
| `index` | 导航页 | _MOC、顺序索引 |

### ⚠️ 禁止事项

- **type 只能用英文 6 种值**，禁止中文
- **status 只用 `draft` / `finalized`**，禁止中文（`已完成`、`完成`）
- **`workbuddy_sync` 字段已废弃**，不再使用

---

## 三、Wikilink 规则

| 场景 | 格式 | 示例 |
|------|------|------|
| TileMatch 内部 | 基名（仅文件名） | `[[分析-死局逻辑与改进方案-v1\|死局]]` |
| 跨项目（如 03-KNOWLEDGE） | vault-root 全路径 | `[[03-KNOWLEDGE/Unity/Unity 开发笔记\|Unity]]` |
| 指向 MOC | 基名 + `|别名` | `[[_MOC\|TileMatch 知识库 MOC]]` |

🚫 **禁止** `[[游戏逻辑/Rocket/xxx]]` 这种缺 `02-PROJECTS/TileMatch/` 前缀的路径链接——Obsidian 按 vault-root 解析，会断。

---

## 四、MOC 层级

```
HOME.md（vault 主 MOC）
  ├─ TileMatch/_MOC.md ──→ 58 篇文档（100% 覆盖）
  │    └─ 局内障碍知识库_MOC.md（子 MOC）
  ├─ WorkBuddy/WB-MEMORY_MOC.md（MEMORY 蒸馏存档）
  └─ 03-KNOWLEDGE/*（通用知识）
```

**规则**：
- vault 内**禁止两个 MOC 同名**。WorkBuddy MOC 已更名为 `WB-MEMORY_MOC.md`
- 每个 MOC 用 `aliases` 提供唯一别名
- HOME.md 是**重点维护对象**，新增项目/MOC 时必须登记

---

## 五、新建文档流程

1. 确定 `type` 和文件夹
2. 命名：`{前缀}-{主题}.md`（`spec`→规范-、`analysis`→分析-、`report`→报告-）
3. 分配 `cat_order`：文件夹内最大号 +1，三位补零
4. 写 frontmatter，末尾加 `## 关联`
5. 更新对应 `_MOC.md`
6. 追加 `知识库文档顺序索引.md` 的静态备份

---

## 六、WorkBuddy 自动化（2 个）

### 自动化 1：知识库同步与维护（主任务）

| 项 | 值 |
|----|-----|
| ID | `automation-1783910244457` |
| 频率 | 每周一 09:00 |
| CWD | `D:\LibraryG` |
| 流程 | **先同步（AI 读文件内容→参考 vault 同类→智能归位到正确目录）→ 导航检查（60%）→ 规范检查（40%）→ 合并报告** |
| 规则 | 只读/只复制，不自动修改文件，不 commit/push |

### 自动化 2（暂停）：Notion 同步

| 项 | 值 |
|----|-----|
| ID | `automation-1781245784822` |
| 状态 | **PAUSED**，待 Notion connector 重连 |

---

## 七、INBOX 对话工作流

```
对话开始 → INBOX/<日期-主题>/ 建临时文件夹
  ├─ 中间产物放这里
  └─ 对话结束：
      ├─ 规范 → 03-KNOWLEDGE/工作流/ 或 02-PROJECTS/<项目>/知识库/
      ├─ 知识 → 03-KNOWLEDGE/<主题>/
      ├─ 项目 → 02-PROJECTS/<项目>/
      └─ 日志 → 01-DAILY/YYYY-MM-DD.md
```

---

## 八、MEMORY 蒸馏

WorkBuddy 有两层 MEMORY 有字符上限：
- 项目级：`meatloaf_client01\.workbuddy\memory\MEMORY.md`（3,000 字符）
- 用户级：`~\.workbuddy\MEMORY.md`（4,000 字符）

**超限时蒸馏流程**：
1. 完整原文存档到 `Obsidian WorkBuddy-MEMORY/`（append-only）
2. 记录蒸馏日志（时间 + 事件 + 原因 + 变化）
3. 精简 MEMORY.md：保留核心规则 + 速查链接 → 详细内容点 Obsidian
4. **保守合并，不删仍相关内容**

---

## 九、Obsidian 插件

| 插件 | 用途 |
|------|------|
| Dataview | `_MOC.md` 仪表盘 + `知识库文档顺序索引.md` 动态表格 |
| Templater | 模板变量（`<% tp.date.now(...) %>`）|

---

## 十、健康检查标准

> 详细见 `[[02-PROJECTS/TileMatch/知识库/规范-知识库健康检查|健康检查规范]]`

| # | 检查项 | 权重 |
|---|--------|------|
| 1 | 断链扫描 | 25% |
| 2 | Frontmatter（六字段 + 值域） | 15% |
| 3 | _MOC 覆盖率 | 20% |
| 4 | cat_order 合规 | 15% |
| 5 | 链接路径风格 | 10% |
| 6 | 文件命名 | 10% |
| 7 | 零污染 | 5% |

---

## 十一、Obsidian MCP 工具优先级

| 操作 | 首选 | 降级 |
|------|------|------|
| 读笔记 | `mcp__obsidian-mcp__read_note` | `Read` |
| 搜 vault | `mcp__obsidian-mcp__search_vault` | `Grep` |
| 建笔记 | `mcp__obsidian-mcp__create_note` | `Write` |
| 编辑 | `mcp__obsidian-mcp__update_note` | `Edit` |
| 移动/改名 | `mcp__obsidian-mcp__move_note` | `Bash mv` |
| 批量扫描 | `Grep` + `Glob` | — |

---

## 关联

- [[HOME|返回主 MOC]]
- [[02-PROJECTS/TileMatch/知识库/规范-知识库文档分类标准|知识库分类标准]] — 所有规则的权威来源
- [[02-PROJECTS/TileMatch/知识库/规范-知识库健康检查|健康检查规范]] — 7 项指标
