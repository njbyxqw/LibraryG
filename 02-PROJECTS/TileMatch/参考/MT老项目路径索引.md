---
title: MT 老项目路径索引
date: 2026-08-05
type: reference
status: finalized
priority: high
cat_order: 020
tags: [TileMatch, Meatloaf, MT, 路径索引, 迁移对照]
---

# MT 老项目路径索引

> 本文记录 MT 老项目在当前机器上的关键路径，用于和 TS 做行为对照、方案复现和历史追溯。MT 和 TS 项目之间不固定主次；本索引只负责快速定位旧项目入口，避免每次重新找路径。

---

## 基础路径

| 项 | 路径 | 说明 |
|---|---|---|
| MT 工作空间 | `/Users/dean/Downloads/meatloaf_client` | 老项目根目录 |
| MT Unity Client | `/Users/dean/Downloads/meatloaf_client/client` | 主要 Unity 工程 |
| MT Agent 入口 | `/Users/dean/Downloads/meatloaf_client/client/AGENTS.md` | 进入 MT 代码任务前优先读取 |
| MT 记忆 | `/Users/dean/Downloads/meatloaf_client/.workbuddy/memory/` | 少量历史 memory |
| LG 中 MT 知识库 | `02-PROJECTS/TileMatch/` | MT/TileMatch 逻辑、工具、复盘、报告沉淀 |

---

## TileV2 对照入口

| 领域 | MT 路径 | TS 对位路径 | 备注 |
|---|---|---|---|
| TileV2 根 | `/Users/dean/Downloads/meatloaf_client/client/Assets/Game/TileV2` | `/Users/dean/TileScape/Assets/Game/TileV2` | 两边大量代码同源 |
| 配置 | `Assets/Game/TileV2/Config` | `Assets/Game/TileV2/Config` | 表配置、关卡配置、障碍配置 |
| 配置源码 | `Assets/Game/TileV2/Scripts/Config` | `Assets/Game/TileV2/Scripts/Config` | 配置结构与加载逻辑 |
| 玩法入口 | `Assets/Game/TileV2/Scripts/Entry` | `Assets/Game/TileV2/Scripts/Entry` | TS 已有更多接口化/生命周期改造 |
| 棋盘核心 | `Assets/Game/TileV2/Scripts/GameCore/Logic` | `Assets/Game/TileV2/Scripts/GameCore/Logic` | 局内规则、实体、服务、ECA |
| 表现层 | `Assets/Game/TileV2/Scripts/GameCore/View` | `Assets/Game/TileV2/Scripts/GameCore/View` | 动画、输入、TileView、ViewController |
| 记录/回放 | `Assets/Game/TileV2/Scripts/GameRecord` | `Assets/Game/TileV2/Scripts/GameRecord` | 重连、回放、记录控制 |
| 编辑器 | `Assets/Game/TileV2/Editor` | `Assets/Game/TileV2/Editor` | LevelEditor、LevelBot、TileTypeEditor |
| 资源 | `Assets/Game/TileV2/Res` | `Assets/Game/TileV2/Res` | UI、局内、音效、动画资源 |
| Excel 源 | `Assets/Game/TileV2/ExcelConfig` | `Assets/Game/TileV2/ExcelConfig` | 表源文件 |

---

## MT 独有 / 旧架构常见入口

| 领域 | MT 路径 | 用途 |
|---|---|---|
| Proxy | `Assets/Game/TileV2/Scripts/Proxy` | 旧项目外部系统代理实现 |
| Proxy 接口 | `Assets/Game/TileV2/Scripts/Proxy.Interface` | Item、Sound、UIData 等旧接口 |
| UI 逻辑 | `Assets/Game/TileV2/Scripts/UILogic` | 旧 UI 流程、旧 Data、GameUILogic |
| 关卡编辑器本地工具 | `Assets/Game/TileV2/Editor/LevelEditor` | 旧编辑器实现对照 |
| LevelBot | `Assets/Game/TileV2/Editor/LevelBot` | 跑关机器人旧实现 |

---

## 使用规则

- 做 MT / TS 对照时，先查 LG 中已有专题文档和工作记录，再进入代码路径。
- 对同源代码，优先记录“行为是否等价”和“生命周期/架构差异”，不要机械逐字复制。
- 如果在 MT 找到可复用方案，回写到 LG 对应专题；如果只是一段临时定位，写入 DAILY 即可。
- 历史 Windows 路径保留在旧文档中可以作为历史信息；当前机器以本文路径为准。

---

## 对位文件表模板

```markdown
| 领域 | MT 文件 | TS 文件 | 关系 | 结论 |
|---|---|---|---|---|
|  | `...` | `...` | 同源 / 已重构 / 缺失 / 产品差异 |  |
```

---

## 关联

- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]]
- [[02-PROJECTS/TileScape/_MOC|TileScape 知识库 MOC]]
- [[规范-多项目工作流与复现|多项目工作流与复现]]
