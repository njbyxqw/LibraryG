---
title: 验收：MOC 使用情景静态验证
date: 2026-09-03
type: 验收
status: accepted
lifecycle: historical
archived: 2026-09-18
source: "AI任务规划-知识库后续治理.md · P2"
tags: [LibraryG, P2, MOC, 验收, 链接验证]
---

# 验收：MOC 使用情景静态验证（P2）

> 按 `AI任务规划-知识库后续治理.md` 的 P2 节，由 WorkBuddy 对 5 个使用情景做**静态链路核对**。只按给定情景逐级走链接并记录结果，不按文件名全库搜索，不改任何文件，不增删入口。

## 验收结论总览

| 情景 | 结果 |
|---|---|
| 1 查 TileMatch 障碍机制 | ✅ 链路完整，无断点，无误入 |
| 2 查 TileScape GM 工具 | ✅ 链路完整，无断点 |
| 3 查 TileScape 文档/资源位置 | ✅ 链路完整，无断点 |
| 4 查可迁移 Unity/编辑器方法 | ⚠️ 主链路可达，含 2 处误入风险（见下） |
| 5 查 LG 维护 / INBOX 规则 | ✅ 链路完整，无断点 |

链接存在性：本验证涉及的全部跨目录/带路径链接目标文件均存在；全部裸文件名链接各只有 1 个匹配，无重名歧义。

---

## 情景 1 — 查 TileMatch 障碍机制

预期路径：`AI总MOC → TileMatch MOC → 局内障碍知识库 MOC → 具体障碍文档`

实际经过：
1. `AI总MOC.md` 任务路由 → `[[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]]` ✅
2. `TileMatch/_MOC.md` 任务路由「障碍模块」→ `[[局内障碍知识库_MOC|局内障碍知识库 MOC]]` ✅（快速入口区另有同名入口）
3. `游戏逻辑/局内障碍/局内障碍知识库_MOC.md` → 具体障碍文档：`[[障碍牌-类型全览]]`、`[[障碍牌-Rocket]]`、`[[Effect牌-类型全览]]` 等 ✅

链接核对：
- `局内障碍知识库_MOC` → 唯一 `02-PROJECTS/TileMatch/游戏逻辑/局内障碍/局内障碍知识库_MOC.md`
- `障碍牌-类型全览` / `障碍牌-Rocket` → 唯一 `.../局内障碍/障碍牌/`
- `Effect牌-类型全览` → 唯一 `.../局内障碍/Effect/`

结论：无断点、无重名、无误入历史资料。

---

## 情景 2 — 查 TileScape GM 工具

预期路径：`AI总MOC → TileScape MOC → GM 工具 MOC → 具体工具/规则`

实际经过：
1. `AI总MOC.md` 任务路由 → `[[02-PROJECTS/TileScape/_MOC|TileScape MOC]]` ✅
2. `TileScape/_MOC.md` 任务路由「GM 模块」→ `[[GM工具/_MOC|GM 工具 MOC]]` ✅（快速入口区另有同名入口）
3. `TileScape/GM工具/_MOC.md` → `[[规范-GM工具新增与使用规则]]`、`[[工具-屏蔽关卡动更开关]]` ✅

链接核对：三处目标文件均存在（`GM工具/_MOC.md`、`规范-GM工具新增与使用规则.md`、`工具-屏蔽关卡动更开关.md`）。

结论：无断点、无误入。

---

## 情景 3 — 查 TileScape 文档或资源位置

预期路径：`AI总MOC → TileScape MOC → Docs 索引或快速定位索引`

实际经过：
1. `AI总MOC.md` 任务路由 → `TileScape MOC` ✅
2. `TileScape/_MOC.md` 任务路由「Docs 索引」→ `[[参考/Docs文档索引]]`、「快速定位/资源替换」→ `[[参考/快速定位与资源替换索引]]` ✅
3. `TileScape/参考/Docs文档索引.md`、`TileScape/参考/快速定位与资源替换索引.md` 均存在，且各自回链 `TileScape 知识库 MOC` ✅

结论：无断点、无误入。

---

## 情景 4 — 查可迁移 Unity / 编辑器方法 ⚠️

预期路径：`AI总MOC → 通用知识 MOC → 对应 Knowledge 条目 → 来源项目 MOC`

实际经过：
1. `AI总MOC.md` 任务路由「可迁移 Unity/编辑器/设计知识」→ `[[03-KNOWLEDGE/_MOC|通用知识 MOC]]` ✅
2. `03-KNOWLEDGE/_MOC.md` 按主题进入 → `[[03-KNOWLEDGE/Unity/Unity 开发笔记]]`、`[[03-KNOWLEDGE/TileV2-Editor/TileV2 编辑器概览]]` ✅
3. `03-KNOWLEDGE/_MOC.md` 关联区回链 → `[[02-PROJECTS/TileMatch/_MOC]]`、`[[02-PROJECTS/TileScape/_MOC]]` ✅

链接核对：四个 Knowledge 条目文件均存在。主链路可达、无断点。

发现的误入风险（均为语义/旁路层面，非链接断裂，均属 P1 待决项）：

1. **「按主题进入」含 2 条非可迁移条目**：通用知识 MOC 的「按主题进入」表里，「游戏逻辑」（指向 `游戏逻辑分析`，实为项目事实汇总）与「Obsidian / LG 工具」（指向 `Obsidian插件使用指导`，实为工作流资料）2 条，按 MOC 自身「只路由可迁移知识」的定位本不该作为入口。但二者状态列已明确标注「待提炼 / 待迁移」，属于已知过渡态，不是链接错误。
2. **HOME 存在 Unity 空文件旁路入口**：`HOME.md:249` 有 `[[03-KNOWLEDGE/Unity|Unity 速查]]`，指向 `03-KNOWLEDGE/Unity`。该路径同时对应「空文件 `Unity.md`」与「目录 `Unity/`」，存在解析歧义，是 `Unity.md` 空文件问题的实际来源之一。通用知识 MOC 已正确地把 `Unity.md` 排除在导航之外（仅在状态表登记 `needs-review`），但 HOME 的旁路入口仍指向它。

结论：主链路 ✅，但 `Unity.md` 空文件问题与「非可迁移条目占用 Knowledge 入口」问题，需 P1 逐文件规划时决策（HOME 的 Unity 速查改指向、Knowledge 入口表是否精简）。

---

## 情景 5 — 查 LG 维护或 INBOX 规则

预期路径：`AI总MOC → Agent 工作流 MOC → 对应 current 规范`

实际经过：
1. `AI总MOC.md` 任务路由「LG 工作流/Daily/INBOX/MOC 维护」→ `[[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]` ✅
2. `Agent/工作流/_MOC.md` 「current」7 条规范入口 ✅
3. 7 条规范文件均存在：任务产出入库、MOC 命名与导航、INBOX 对话工作区、工作内容日志同步、多项目工作流与复现、任务知识沉淀闭环与自动巡检、AI 协作注意事项 ✅

结论：无断点、无误入。

---

## 边界与未执行项

- 未修改、移动、删除任何文件；未增删任何 MOC 入口。
- 未验证 Obsidian Dataview / Canvas 动态渲染（按要求排除）。
- 本次仅覆盖 P2 五情景；P1（逐文件归属规划）、P3（拆分迁移）需 AI 先出方案并待用户确认，不在本轮执行。

## 后续动作建议（交 AI / Codex 决策）

1. HOME.md:249 的 `[[03-KNOWLEDGE/Unity|Unity 速查]]` 改指向 `[[03-KNOWLEDGE/Unity/Unity 开发笔记]]`，或确认空文件 `Unity.md` 的去留。
2. 通用知识 MOC「按主题进入」表是否精简为仅「可迁移知识」条目，把「游戏逻辑」「Obsidian/LG 工具」移出，仅保留状态表登记。

## 关联

- [[05-ARCHIVE/Agent/2026-09-03-知识库内容归属与MOC路由整理/AI任务规划-知识库后续治理|AI 任务规划（P2）]]
- [[03-KNOWLEDGE/_MOC|通用知识 MOC]]
- [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]
