---
title: Home DLC 与 Endless 最大关卡更新流程梳理
date: 2026-08-20
type: analysis
status: current
project: TileScape
lifecycle: current
verification: static-analysis-runtime-pending
tags: [TileScape, DLC, HomeScene, Endless, 最大关卡, 重启]
source: "TS 当前工作区静态代码；用户确认的流程目标另行标注"
---

# Home DLC 与 Endless 最大关卡更新流程梳理

> 范围：HomeScene 章节 DLC、启动门禁、关卡入口、画廊，以及 Endless 结束后同步最大关卡并要求重启的当前行为。
>
> 验证边界：2026-08-20 对 TS 当前工作区的静态代码梳理；未做 Unity 真机、CDN 或服务器联调验证。

## 当前已实现规则

### 章节 DLC

- 启动阶段由 `HomeHubDlcModule.CollectApplicationLoadingRequireDownloadableIds` 收集当前 Home 章节及 `ChapterDLCLoadingPreLevel` 窗口内的必需 Package；Loading Gate 成功前不能进入 Home。
- 每次回到 Home 都执行 `FlowItemHomeDlcPreLevelDownload`，仅以普通进度 `ILeveledGame.CurrentLevel()` 计算临近章节地图包，并以 Low 优先级后台预下载；无尽虚拟关卡号不参与计算。
- 关卡按钮是地图 Package 的前台门禁入口：当前关卡所属章节未 Ready 时下载并阻止本次进入；章节最后一关还会检查下一章节。下载成功后需再次点击。
- 章节解锁 Flow 不下载资源；下一章节地图未 Ready 时直接结束，避免加载未就绪资源。画廊封面可占位，主动预览缺图时走前台下载。

### Endless 最大关卡同步与重启

- `TileMatch.Init` 会请求一次服务器最大关卡；结果只持久化到 `Profile.MaxLevelId`，不会改变本次运行 `EffectiveMaxLevelId`。
- Endless 的 `Succeeded`、`QuitFailed`、`GiveUpReviveFailed` 结束状态都会再次请求服务器最大关卡；普通关卡结束不请求。
- 若该次 Endless 请求得到的最大关卡大于 `EffectiveMaxLevelId`，会置 `_requiresNewLevelRestart = true`。
- 此状态下玩家下一次调用 `OpenGotoGamePanel` 不会打开进关面板，而是显示不可关闭、不可取消的重启提示；确认后保存 Profile、写入 `HomeEndlessExitUnlockBridge` 并执行 `UtilsLoading.Restart(false)`。
- 下次冷启动以新的 `Profile.MaxLevelId` 初始化 `EffectiveMaxLevelId`。若玩家曾在 Endless 且普通进度小于新的有效最大关卡，则清空 Endless 进度、保留桥接的已完成普通关卡，并在 Home Flow 尝试展示下一章节解锁。

## 关键调用链

```text
Endless 结束
  TileMatch.ForwardGameState()
    RequestServerMaxLevelAfterEnd()
      RequestServerMaxLevel(..., markRestartWhenBoundaryAdvances: true)
        RecordServerMaxLevelForNextLaunch()
        HasPendingMaxLevelForNextLaunch -> _requiresNewLevelRestart = true

玩家尝试开始下一关
  TabBarHome.TryOpenCurrentLevelAsync()
    IHomeScene.TryEnterLevelAsync()  // DLC Ready 门禁
    ILeveledGame.OpenGotoGamePanel()
      _requiresNewLevelRestart -> GameMain.OpenNewLevelRestartNotice()
      确认 -> SaveToLocal -> HomeEndlessExitUnlockBridge.SetPending -> UtilsLoading.Restart(false)

重启后
  TileMatchDataCenter.ValidateAgainstCurrentConfig()
    新 EffectiveMaxLevelId 生效
    EndlessIndex > 0 且 CurrentLevelIndex < EffectiveMaxLevelId
      -> SetPending(CurrentLevelIndex) 并清空 EndlessIndex
  HomeSceneController / Home Flow
    消费桥接状态 -> FlowItemHomeEndlessExitChapterUnlock
```

## 已确认情景：最大关卡 400，玩家完成 399 后服务器配置上调

假设服务器新值为 `N`，且 `N > 400`：

1. 玩家正在第 399 关时，即使先收到服务器结果，本次运行的 `EffectiveMaxLevelId` 仍为 400；结果只写入 `Profile.MaxLevelId = N`。启动请求本身不标记重启。
2. 玩家完成第 399 关后，普通进度变为 400，仍可正常进入并完成第 400 关；普通关卡结束不会触发新的最大关卡请求或重启提示。
3. 第 400 关完成后，普通进度为 400；在不重启的当前运行中，下一关仍按旧边界进入 Endless。
4. 第一局 Endless 结束后会请求服务器。若此时响应仍为 `N > 400`，则设定重启标记；玩家下一次点击进关，先通过当前 Home DLC 门禁，再被重启提示拦截，无法继续进入旧 Endless。
5. 确认重启后，启动门禁按普通进度 400 与新章节窗口收集 DLC。资源 Ready 后进入 Home；冷启动清空 Endless 进度并触发从 400 所在章节到下一章节的解锁流程。

## 与已确认目标的差异

| 项目 | 当前代码 | 此次讨论确认的目标 |
|---|---|---|
| 最大关卡检测 | 初始一次；每次 Endless 结束一次 | 保持每次 Endless `lv_end` 检测 |
| 生效方式 | 仅下次冷启动改变普通/Endless 边界 | 重启后统一生效 |
| 提示时机 | 下次打开进关面板 | 初版等同于下一关前；可配置延迟关数 |
| 取消行为 | 提示框无取消、无关闭 | 初版可保持强制重启；循环/延迟需要显式配置 |
| DLC 下载 | 重启后 Loading Gate 与 Home 门禁处理 | 同左，不在 Endless 运行中热切章节 |

> 待验证：当前最大关卡请求为异步回调；若玩家在回调完成前已打开下一关，首次 Endless 仍可能先被打开。需要真机/联调确认回调到达时序。

## 关键文件

- `Assets/Game/TileV2/Scripts/Entry/TileMatch.cs`
- `Assets/Game/TileV2/Scripts/DataCenter/TileMatchDataCenter.Level.cs`
- `Assets/Game/TileV2/Scripts/DataCenter/TileMatchDataCenter.Flow.cs`
- `Assets/Scripts/GameMain.cs`
- `Assets/Module/HomeHub/HomeScene/Scripts/DLC/DLC.md`
- `Assets/Module/HomeHub/HomeScene/Scripts/DLC/HomeHubDlcModule.cs`
- `Assets/Module/HomeHub/HomeScene/Scripts/Flow/Item/FlowItemHomeEndlessExitChapterUnlock.cs`

## 关联

- [[02-PROJECTS/TileScape/_MOC|TileScape 知识库 MOC]]
- [[02-PROJECTS/TileScape/参考/快速定位与资源替换索引|TileScape 快速定位与资源替换索引]]
- [[01-DAILY/2026-08-20|2026-08-20 工作日志]]
