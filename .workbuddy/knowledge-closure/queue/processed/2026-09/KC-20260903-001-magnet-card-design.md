---
schema_version: 1
id: KC-20260903-001-magnet-card-design
status: ready
risk: low
projects: [LibraryG, TileScape, TileMatch]
created_at: 2026-09-03T00:00:00+08:00
producer: Codex
source_evidence:
  - kind: user_confirmation
    ref: "当前对话 2026-09-03"
    summary: "新增一种磁铁特殊牌；开局按每关配置的组数随机选花色并替换；点击一张后飞往弃牌区，再吸另外两张到手牌区完成消除。"
    verification: confirmed
  - kind: static_code
    ref: "TileScape/Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Module/LevelRocket/Strategy/RocketNormalStrategy.cs"
    summary: "现有火箭初始化按 TileType 分组、随机挑选并通过 TileService.ModifyTile 转换；组数按三张牌计算。"
    verification: static-confirmed
  - kind: static_code
    ref: "TileScape/Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Prop/AutoMatchProp.cs"
    summary: "现有自动匹配道具一次将 3 张目标牌加入 Bar；不能直接表达点击牌进 OverBar、其余两张进 Bar 的三牌联动。"
    verification: static-confirmed
  - kind: historical_code
    ref: "TileMatch/Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Prop/LightingProp.cs；LightingViewAction.cs"
    summary: "历史连胜闪电球以 WinStreakTimes 限制最多 4 组，每组 3 张；仅作组数概念参考。"
    verification: static-confirmed
---

# 磁铁牌元素方案归档与导航

## 执行边界

- 仅执行本包 actions；不得自行补充内容或改变归类。
- 不修改 TileScape / TileMatch 代码、资源、配置或 Git 状态。
- 任一前置条件不满足时，停止后续写入并转 `needs-review`。

## Actions

### A1

- operation: `create_document`
- target: `03-KNOWLEDGE/Game-Logic/设计-磁铁牌元素-v1.md`
- anchor: `目标文件本身`
- precondition: `目标不存在；全库尚未出现 <!-- kc:KC-20260903-001-magnet-card-design:A1 -->`
- verify: `文件含完整 frontmatter、来源、状态、关联和唯一幂等标记；内部 wikilink 目标存在`
- rollback: `保留报告；人工删除本 action 创建的文档`

```markdown
---
title: 磁铁牌元素方案 v1
date: 2026-09-03
type: design
projects: [TileScape, TileMatch]
domain: TileV2 Game Logic
status: needs-review
lifecycle: draft
working_branch: level_trial
source: 用户需求说明；TileScape 当前静态代码；TileMatch 历史连胜闪电球逻辑
verification: static-analysis-pending-runtime
tags: [TileV2, 元素牌, 磁铁牌, Trial, LevelEditor, ECA]
---

# 磁铁牌元素方案 v1

<!-- kc:KC-20260903-001-magnet-card-design:A1 -->

## 已确认需求

- 新增一种可在关卡内放置与试跑的特殊牌，暂称 `Magnet`；参考金牌或火箭牌的局内载体与开局改牌路径。
- 开局按关卡配置的组数，随机选择普通花色牌并替换成磁铁牌。
- 玩家点击任一磁铁牌后：被点牌播放飞往弃牌区（OverBar）的表现；一次磁铁效果再将另外两张磁铁牌吸至手牌区（Bar），完成匹配消除。
- 组数由每关配置，服务于 `level_trial` 分支中的 LevelEditor + Trial 验证；不新建独立运行时或固定实验关文件。

## 当前设计口径

| 维度 | 方案 | 依据 / 说明 |
| --- | --- | --- |
| 元素载体 | 独立、可点击的特殊 `Tile`，而非覆盖普通牌的 `Effect` | 它需要自身点击、专属动画和三张联动状态；火箭是最近的开局改牌参照。 |
| 一组定义 | 暂按 3 张同一普通花色牌替换为 3 张磁铁牌 | 当前三消与历史闪电球均以 3 为一组；需产品确认“组”是否另有定义。 |
| 开局改牌 | 基于火箭初始化的“按 TileType 分组 → 随机选候选 → `TileService.ModifyTile`”思路，按配置循环选组 | 不继承火箭的固定 3 组、可用门槛或 `WinStreakTimes` 规则。 |
| 点击后逻辑 | 专用原子操作：锁定本组 3 张，记录随机结果；点击牌走 OverBar 视觉，另外 2 张走 Bar；统一触发匹配与状态结算 | 现有 `AutoMatchProp` 是一次向 Bar 加 3 张，不能直接表达该序列。 |
| 随机边界 | 仅决定“哪些完整磁铁组被转化 / 被触发”；同组剩余两张必须与点击牌绑定，避免跨组误吸 | 随机结果必须进入录像 / 重连所需记录，保证可复现。 |
| 关卡数据 | 每关新增磁铁组数；编辑器暴露可填写、保存、加载、Trial 读取的参数 | 不先做通用试跑工具。 |

## 待确认事项（阻断实现）

1. 被点击磁铁牌进入 OverBar 后，如何与另两张 Bar 内牌构成“三消”：是 OverBar 牌也计入本次匹配，还是三张均应最终进入 Bar（仅视觉上先飞弃牌区）？
2. “随机触发一次”是随机挑选已生成的一个完整磁铁组，还是点击的那组必定触发、随机仅用于开局选花色？本稿暂按后者。
3. 每关配置不足以生成完整 3 张同花色组时：降级为可生成的组数、整关不生成，还是报关卡校验错误？
4. 火箭、闪电、风车、局内磁铁、自动匹配、撤回等道具命中磁铁牌时，分别是普通取牌、摧毁、不可选，还是触发磁铁效果？
5. 是否要求机器人跑关、录像/重连和正式局中的 DDA 均支持；本次 Trial 最小闭环可先验证真实局内逻辑和表现，后续再扩范围。

## 实现工作拆分（待确认后）

1. 新增 TileType、TileConfig、Prefab / TileView 和 LevelEditor 类型展示；确认 `MatchCount`、可点击性及 TileGroup。
2. 新增每关磁铁组数配置与加载数据；在 Board 初始化阶段复用火箭式候选筛选，生成完整三张组并写入组关联信息。
3. 在 `TileClicked` 链路接入专用 ECA Action / 服务：验证目标、锁定同组牌、处理棋盘 / Bar / OverBar 状态、写入记录并触发匹配检查。
4. 以 ActionResult 驱动专用 ViewAction：点击牌飞往 OverBar，另外两张依次吸到 Bar，按确认后的口径播放匹配消除。
5. 补齐关卡校验、道具交互表、回放/重连、机器人和 Trial 验证关。

## 参考依据

- TileScape 开局火箭改牌：`Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Module/LevelRocket/Strategy/RocketNormalStrategy.cs`。
- TileScape 金牌初始化与 Board 接入：`Module/LevelGoldTile/LevelGoldTilesInit.cs`、`Entity/Board.cs`。
- TileScape 自动匹配：`GameLogic/Prop/AutoMatchProp.cs`，其目标数固定为 3 并直接进 Bar。
- TileScape ECA 点击入口：`Config/Behaviours/Event/EventType.cs` 的 `TileClicked` 与 `Behaviours/Action/Implementation/ForwardTileClickAction.cs`。
- TileMatch 历史连胜闪电球：`LightingProp.cs`、`LightingViewAction.cs`；连胜组数为 `min(4, WinStreakTimes)`，每组 3 张，仅作概念参考。

## 关联

- [[03-KNOWLEDGE/Game-Logic/任务-元素牌开发|元素牌开发任务]]
- [[02-PROJECTS/TileScape/_MOC|TileScape MOC]]
- [[02-PROJECTS/TileMatch/_MOC|TileMatch MOC]]
```

### A2

- operation: `moc_append`
- target: `03-KNOWLEDGE/_MOC.md`
- anchor: `## 关联`
- precondition: `目标存在；锚点唯一；A1 已成功；尚未出现 <!-- kc:KC-20260903-001-magnet-card-design:A2 -->`
- verify: `幂等标记唯一；链接目标存在`
- rollback: `保留报告；人工删除本 action 的标记块`

```markdown
<!-- kc:KC-20260903-001-magnet-card-design:A2 -->
- [[03-KNOWLEDGE/Game-Logic/设计-磁铁牌元素-v1|磁铁牌元素方案 v1]] — 按关卡组数随机替换、点击后三张联动消除的设计稿；存在待确认的 OverBar / 三消语义。
```

### A3

- operation: `daily_append`
- target: `01-DAILY/2026-09-03.md`
- anchor: `## TileScape`
- precondition: `目标存在；锚点唯一；A1 与 A2 已成功；尚未出现 <!-- kc:KC-20260903-001-magnet-card-design:A3 -->`
- verify: `幂等标记唯一；今日索引与 TileMatch、TileScape、LibraryG 三个项目节存在`
- rollback: `保留报告；人工删除本 action 的标记块`

```markdown
<!-- kc:KC-20260903-001-magnet-card-design:A3 -->
### 磁铁牌元素方案（待确认）

- 做了什么：根据用户需求形成磁铁牌的初版需求卡，并生成 WorkBuddy 文档闭环任务包。
- 关键结论：采用独立特殊 Tile + 开局按配置组数改牌；点击后需要专用三牌联动，而不能直接复用“自动匹配道具一次进 Bar 三张”的语义。
- 产出 / 路径：[[03-KNOWLEDGE/Game-Logic/设计-磁铁牌元素-v1|磁铁牌元素方案 v1]]；`.workbuddy/knowledge-closure/queue/ready/KC-20260903-001-magnet-card-design.md`。
- 来源依据：用户 2026-09-03 需求；TS 火箭初始化、金牌初始化、自动匹配静态代码；MT 历史连胜闪电球代码。
- 后续入口：确认 OverBar 与三消的结算口径、随机范围和道具交互表后，进入 `level_trial` 的元素实现。
```

## 预期结果

- WorkBuddy 仅创建一份 `needs-review` 的磁铁牌设计稿、补充通用知识 MOC 入口和当日 TileScape 日志。
- 任何实现口径不由 WorkBuddy 自行决定；代码开发仍需在用户确认待决项后另行执行。
