---
title: Activity DLC 现状与设计差异
date: 2026-08-26
type: audit
status: current
lifecycle: static-audit
verification: code-and-config-static-only
tags: [TileScape, Activity, DLC, static-audit]
source: "TS feature-activityDLC @ 381f19f53、当前工作区静态代码与配置；未运行 Unity、构建、CDN 或真机验证"
---

# Activity DLC 现状与设计差异

> 本文记录当前 `feature-activityDLC` 的已实现能力和与 [[02-PROJECTS/TileScape/游戏逻辑/设计-活动DLC扩展框架-2026-08-25|活动 DLC 扩展框架]] 的差异；设计稿不等同于已实现规则。

## 已确认的当前能力

- 首充礼包是当前 DLC 试点；`Activity.{activityName}.{themeKey}` 经 `activitydlcmap.bytes` 映射 Package，无映射或空 Package 时回退为基础包活动。
- 进入 Home 时，距既有活动 `openLevel` 不超过 10 关的未 Ready 活动会以 Low 优先级、最多重试两次请求资源。
- 展示资格为 `IsActive` 且全部 Package Ready；未 Ready 时入口、面板和商店 Banner 均不展示，下载完成或 Package 状态变更后刷新活动 UI。
- Application Loading Gate 的活动 Package 收集能力已预留，但当前 `GameMain` 未启用逐活动 Loading 门禁。

## 与设计稿的关键差异

| 设计能力 | 当前结论 |
|---|---|
| 通用活动索引、投递形态、版本、请求节点和优先级 | 未实现；当前仅有映射键和 Package 列表，开启关沿用既有活动配置。 |
| 独立请求节点和跨活动排序/功能提权 | 未实现；预下载阈值固定为开启前 10 关。 |
| 每关或每次 Loading 重试、前台 High 下载和失败交互 | 未实现；目前仅再次进入 Home 时重新扫描，`EnsurePresentationAsync` 未 Ready 时直接失败。 |
| 版本包切换、预告入口、弹窗额度/去重和入口排序动画 | 未实现。 |

## 关键路径

- `Assets/Module/Activity/Core/ActivityModule.cs`：进入 Home 时机。
- `Assets/Module/Activity/Core/DLC/ActivityModule.Dlc.cs`：DLC 事件、后台请求与 UI 刷新。
- `Assets/Module/Activity/Core/DLC/ActivityDlcCoordinator.cs`：Package 解析、Ensure、代次与生命周期。
- `Assets/Module/Activity/Core/DLC/ActivityDlcNeedSet.cs`：映射键与基础包回退。
- `Assets/Module/Activity/Core/Entity/ActivityBase.cs`：展示 Ready 门禁。
- `Assets/Module/Activity/Core/Config/Data/activitydlcmap.bytes`：运行时映射；`*.json~` 只用于可读核对。

## 验证边界

- EditMode 测试代码覆盖映射、Ready 门禁、Low 请求、重试参数、代次失效和“开启前 10 关”规则，但本轮未执行。
- 未验证资源 Manifest/闭包、CDN、全新安装、缓存、断网、取消或失败恢复。

## 关联

- [[02-PROJECTS/TileScape/游戏逻辑/设计-活动DLC扩展框架-2026-08-25|活动 DLC 扩展框架]]：目标设计与待实施边界。
- [[02-PROJECTS/TileScape/游戏逻辑/梳理-HomeDLC与Endless最大关卡更新流程-2026-08-20|Home DLC 与 Endless 最大关卡更新流程]]：Home 章节 DLC 的既有链路。
