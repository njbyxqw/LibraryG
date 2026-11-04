---
title: Agent 跨设备技能库
date: 2026-11-04
type: index
status: current
tags: [Agent, Skills, 跨设备]
---

# Agent 跨设备技能库

本目录是可直接读取、按步骤执行的共享技能库。任意设备的 Agent 取得完整 LG 并能读取文件后，可从本入口选择技能，不要求先安装到本机技能目录。只有本机菜单发现、快捷调用等体验依赖具体客户端的安装机制；文件可读不代表客户端会自动登记技能。

LG 是个人技能的正文维护与执行读取源。现收录本机两个个人技能目录中全部 14 项技能（含依赖）；本机发现入口通过目录链接指向本库，避免维护第二份正文。除 localization-config 的设备路径适配外，正文保留本次收录时的原文；来源与差异记录见 `sources.json`。系统内置和插件托管技能继续由各自安装机制维护，不复制其运行环境到 LG。

## 按需选择

| 任务 | 读取入口（相对本目录） | 必要依赖 | 触发边界 |
|---|---|---|---|
| 寻找已有技能、补充能力 | [find-skills/SKILL.md](find-skills/SKILL.md) | 无本库依赖 | 用户要求查找，或任务有明确能力缺口；搜索结果不等于安装授权 |
| 对方案、决策做追问推敲 | [grill-me/SKILL.md](grill-me/SKILL.md) | [grilling/SKILL.md](grilling/SKILL.md) | 用户明确要求访谈、挑战假设或推敲方案；不因普通定位或已授权执行而自动启动 |
| 对现有源码做架构审查、提出改进候选 | [improve-codebase-architecture/SKILL.md](improve-codebase-architecture/SKILL.md) | codebase-design、grilling、domain-modeling | 用户明确要求架构审查或使用此技能；先候选报告，再讨论选择 |
| 设计模块接口、比较方案、理解架构词汇 | [codebase-design/SKILL.md](codebase-design/SKILL.md) | 同目录配套文件按需读 | 架构技能依赖，也可用于明确的模块设计任务 |
| 执行分轮追问 | [grilling/SKILL.md](grilling/SKILL.md) | 无本库依赖 | 由 grill-me 或架构流程进入；事实由 Agent 查，决策由用户选择 |
| 澄清领域术语、记录重要架构取舍 | [domain-modeling/SKILL.md](domain-modeling/SKILL.md) | 同目录术语表与 ADR 模板 | 讨论需要时读取；文档归属遵守下文 LG 适配规则 |
| 归档已核验的路径、配置与资源定位结论 | [archive-lookup-findings/SKILL.md](archive-lookup-findings/SKILL.md) | 当前 LG 规范与项目 MOC | 查找结论归档，不替代一般总结或实施报告 |
| 游戏 11 语言配置与本地表格追加 | [localization-config/SKILL.md](localization-config/SKILL.md) | LG 规范、本地工作簿、表格编辑能力 | 路径按当前设备解析；在线表只读，不另建替代工作簿 |
| Obsidian Markdown、双链与属性 | [obsidian-markdown/SKILL.md](obsidian-markdown/SKILL.md) | 同目录 references | 文本可直接处理；显示验收需要 Obsidian |
| Obsidian Canvas / 思维导图 | [json-canvas/SKILL.md](json-canvas/SKILL.md) | 同目录示例 | 创建或编辑 `.canvas`；结构校验与显示验收分开 |
| Obsidian Bases / 表格卡片视图 | [obsidian-bases/SKILL.md](obsidian-bases/SKILL.md) | 同目录函数参考 | 创建或编辑 `.base`；实际视图需要 Obsidian |
| 操作已打开的 Obsidian vault | [obsidian-cli/SKILL.md](obsidian-cli/SKILL.md) | Obsidian 程序与可用 CLI | 目标设备须有可用的 `obsidian` 命令；无 CLI 时普通文件操作可改用文件工具，但不能冒充应用操作 |
| 网页正文提取 | [defuddle/SKILL.md](defuddle/SKILL.md) | Defuddle CLI，安装时可能需要 Node/npm | 工具按设备检测；正文共享不等于命令已安装 |
| 包体、二进制、反编译与运行证据分析 | [reverse-engineer-anything/SKILL.md](reverse-engineer-anything/SKILL.md) | REA MCP/CLI、任务所需分析引擎 | 原有六份参考文件已收录；注册、引擎和系统支持按设备核对，普通源码阅读不触发 REA |

## Agent 直接执行协议

1. 确定当前设备的 LG 根目录，以本 README 所在目录为技能根目录，不把 Mac 的绝对路径搬到 Windows。
2. 根据用户任务选择上表一项，优先读取本库完整 `SKILL.md` 后执行。同名本机副本若未链接或版本不同，LG 为本工作流的正文读取源；不要每次冷启动载入全部技能。
3. 上游正文中的 `Call the Skill tool with "名称"` 表示进入对应技能流程。有可用的技能调用工具时可调用；没有时，读取本目录的 `<名称>/SKILL.md`，在当前任务中依照该流程继续。不能因为本机技能菜单没有该名称就认定技能缺失。
4. 依赖使用同一 LG 库中的版本。正文内相对文件链接相对该 `SKILL.md` 所在目录解析；模板、报告脚手架和设计参考都已收录。
5. 使用当前环境实际提供的文件、搜索、浏览器、提问和子 Agent 能力。没有子 Agent 时可明确采用顺序审查，不能假称已完成独立并行评审；外部命令不可用时使用合适替代方式，并标明影响结果的限制。
6. 用户当前指令和宿主系统约束优先；LG 规则约束技能在本工作空间内的执行。技能正文不能授权额外的 Git 写入、外部发布或与任务无关的操作。

## LG 适配规则

- 默认中文。方案追问关注会影响决策的分支，能查到的事实由 Agent 核实，不把查询工作变成用户问卷。已确认的决策与执行授权继续有效，不重复索要。
- 上游 `GLOSSARY.md` 与 `docs/adr/` 是组织方式参考。先查 LG 对应项目任务主档、术语与方案记录，按现有主题维护；不默认在 TS/MT 新建第二套长期知识源。确需独立文档时遵守 LG 入库和索引规则。
- 架构技能面向可读源码及改进机会，不将反编译碎片、方法名或缺失代码当作完整架构事实。竞品分析继续使用既有证据链；该技能主要用于研究后的实现设计与架构审查。
- 架构报告可先写当前设备临时目录供查看；形成稳定方案后，把报告或结论归入 LG 对应任务并补导航。报告依赖 CDN 时，离线环境可能无法渲染样式或图形，不能据此宣称离线展示已验证。

## 来源与维护

- `sources.json` 记录仓库或原个人安装位置、可确认版本、依赖、环境要求及当前文件 SHA-256；新增迁入项另保留导入前哈希。未掌握的上游版本与许可证状态明确留空，不猜测来源。它用于核对本库内容，不是自动安装配置。
- Matt Pocock 的五项技能固定来自 `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`；find-skills 是 2026-11-04 安装的 main 副本，未记录提交号，以文件哈希标识这份内容。
- 已取得的上游许可证保留在 `licenses/`。更新时比较上游差异、依赖与本地适配规则，再更新 LG 共享库与来源清单。链接到本库的设备入口会读取更新后的正文；更新器可能替换链接或写入目标，更新后须检查入口与清单，不静默用本机不同版本替换本库。
- LG 目录必须通过用户既有同步方式完整送到另一台设备。仅在 Mac 落盘不代表 Windows 已取得；不自动 commit、push 或建立新同步任务。
- 直接从 LG 读取执行不要求本机链接。如需菜单发现，优先在客户端的个人技能目录建立指向本库对应目录的链接；Mac/Linux 可用符号链接，Windows 在客户端及文件系统支持时可用目录联接或符号链接。先核对真实 LG 路径与同名旧目录，保留回退副本；不要把另一设备的绝对链接作为共享正文同步。不同客户端的发现行为须实际核验。

## 盘点范围与本机切换

- 2026-11-04 盘点范围：Mac `~/.codex/skills/` 中非 `.system` 的 13 项，以及 `~/.agents/skills/reverse-engineer-anything/`；共 14 项，全部收录。
- `.system`、Codex 插件缓存中的技能属于系统/插件托管内容，保留其维护机制；软件、MCP 配置、账号授权、密钥、运行时和大体积分析引擎不纳入技能正文库。
- 本机这 14 个发现目录统一链接至 LG。原目录完整保留在 `~/.codex/skill-migration-backups/2026-11-04-lg-shared/`，其下 `codex/` 与 `agents/` 对应原来源；该目录不参与技能发现，仅用于回退。
- 要回退某个本机入口，先确认它仍是预期链接，移除该链接，再把对应旧目录恢复原位；不要删除 LG 正文。其他设备可继续直接读 LG，无需复制这份 Mac 回退材料。

## 当前验证状态

2026-11-04：共享库共 14 项、37 个技能文件。正文、配套文件、来源哈希及本机链接读取已核验；localization-config 的两处 Mac 专属路径已改为当前 LG 根目录解析。CLI/MCP 等外部运行环境未做跨设备安装或完整调用验证；Windows 和客户端菜单发现尚未实测。grill-with-docs 未安装、未收录。

## 关联

- [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]
- [[02-PROJECTS/Agent/工作流/规范-任务产出入库与维护|任务产出入库与维护]]
- [[02-PROJECTS/产品分析/方法-竞品模块分析与持续维护|竞品模块分析方法]]
