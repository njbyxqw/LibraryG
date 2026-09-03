---
type: report
tags: [TileMatch, Rocket, RocketVL]
status: finalized
date: 2026-06-25
cat_order: 003
---

# RocketVL — 火箭牌闪电球视觉替换 完整存档

**存档日期**: 2026-06-25  
**功能状态**: ✅ 已实现，待清理调试日志  
**代码版本**: 基于 `e83f832fe7` 后续修改

---

## 一、功能概述

### 1.1 核心目的

在**编辑器测试模式**下，将火箭牌的视觉效果从「火箭粒子飞行+爆炸」替换为「闪电球闪电击中效果」。

### 1.2 触发条件

- 编辑器输入 `3`（RocketMode=3）
- 仅影响**视觉表现**，不影响逻辑层（链式攻击逻辑不变）

### 1.3 视觉效果变化

| 维度 | 原版（RocketMode=0/1） | RocketVL（RocketMode=3） |
|------|------------------------|--------------------------|
| **飞行特效** | 火箭粒子飞行 | ❌ 无 |
| **击中特效** | 爆炸动画 | ✅ 闪电击中（eff_Lightning01） |
| **音效** | 火箭音效 | ✅ 随机闪电音效（SFX_lightning1~5） |
| **触觉反馈** | 有 | ✅ 保留（Light 级别） |
| **牌面打破** | 有 | ✅ 保留 |

---

## 二、涉及文件清单

### 2.1 新建文件（2 个）

| 文件 | 作用 | 状态 |
|------|------|------|
| `GameCore/View/GameView/Views/ViewActions/RocketVLLighting/RocketVLLightningViewAction.cs` | 接收 `ChainedAttackActionData`，展平所有 Wave 目标，逐牌播放闪电击中效果 | ✅ |
| `GameCore/View/GameView/Views/ViewActions/RocketVLLighting/RocketVLLightningViewActionController.cs` | Controller 壳子，返回 `RocketVLLightningViewAction` 实例 | ✅ |

### 2.2 修改文件（7 个）

| 文件 | 改动 | 状态 |
|------|------|------|
| `GameCore/View/Interface/ICustomViewActionController.cs` | 枚举加 `RocketVLLighting` | ✅ |
| `GameCore/View/GameView/TileMatchViewController.cs` | `DataBridge` 属性 `internal` → `public` | ✅ |
| `GameCore/View/GameView/TileMatchViewController.ViewActions.cs` | 注册 `RocketVLLightningViewActionController` 到 `_viewActions` 字典 | ✅ |
| `Config/Game/CustomData.cs` | 加 `RocketMode` 字段 + `SetRocketMode()` 方法 | ✅ |
| `GameCore/Logic/GameLogic/Module/Statistic/DataBridge.cs` | 加 `RocketMode` 字段（默认 0） | ✅ |
| `GameCore/Application/ActionInvoker/Implementation/PrepareChainedAttackActionInvoker.cs` | 新增 `ResolveControllerType()`：mode==3 → `RocketVLLighting` | ✅ |
| `Editor/LevelEditor/Script/Views/TestControlView/TestControlView.cs` | 输入 `3` → `SetRocketMode(3)`；OnPlayBtnClick 传值 | ✅ |

---

## 三、核心代码详解

### 3.1 `RocketVLLightningViewAction.cs`

**路径**: `Assets/Game/TileV2/Scripts/GameCore/View/GameView/Views/ViewActions/RocketVLLighting/RocketVLLightningViewAction.cs`

#### 3.1.1 核心流程

```csharp
public override async UniTask DoAction(object data)
{
    // 1. 展平数据：将 ChainedAttackActionData.Waves 展平为 _flattenedTargets
    if (!TryFlattenData(data))
    {
        return;
    }

    // 2. 逐牌播放闪电击中效果（并行）
    List<UniTask> tasks = new List<UniTask>();
    for (var index = 0; index < _flattenedTargets.Count; index++)
    {
        var tileData = _flattenedTargets[index];
        var tileView = TileMatchViewController.Instance.GetTileView(tileData.Id);
        tasks.Add(PlayOneShotEffect(index, tileData, tileView));
    }

    // 3. 等待所有特效完成
    await UniTask.WhenAll(tasks);

    // 4. 最终延迟（让特效完全播放）
    await DOVirtual.DelayedCall(ViewConfig.finalDelay, () => { })
        .SetLink(TileMatchViewController.Instance.gameObject)
        .ToUniTask(...);
}
```

#### 3.1.2 数据展平逻辑

```csharp
private bool TryFlattenData(object data)
{
    _flattenedTargets = new List<TileData>();

    // 支持两种数据源
    if (data is ChainedAttackActionData chainedData)
    {
        FlattenWaves(chainedData.Waves);
        return true;
    }

    if (data is PrepareAttackActionData prepareAttackData)
    {
        for (int i = 0; i < prepareAttackData.Targets.Count; i++)
        {
            if (prepareAttackData.Targets[i] != null)
            {
                _flattenedTargets.Add(prepareAttackData.Targets[i]);
            }
        }
        return _flattenedTargets.Count > 0;
    }

    return false;
}

private void FlattenWaves(List<AttackWaveData> waves)
{
    for (int wi = 0; wi < waves.Count; wi++)
    {
        var wave = waves[wi];
        for (int ti = 0; ti < wave.Targets.Count; ti++)
        {
            var tile = wave.Targets[ti].Tile;
            if (tile != null)
            {
                _flattenedTargets.Add(tile);
            }
        }
    }
}
```

#### 3.1.3 单牌特效播放

```csharp
private async UniTask PlayOneShotEffect(int index, TileData tileData, TileView tileView)
{
    // 1. 延迟：根据索引错开播放（避免所有特效同时播放）
    await DOVirtual.DelayedCall(ViewConfig.shotDelayInterval * index, () => { })
        .SetLink(tileView.gameObject)
        .ToUniTask(...);

    if (!tileView)
    {
        return;
    }

    // 2. 高亮牌面
    tileView.SetAutoChangeHighlight(false);
    tileView.SetHighlight(true, true);
    tileView.SetSortingOrder(-100);

    // 3. 播放闪电特效
    PlayLightEffects(tileView);

    // 4. 延迟后播放牌面打破效果
    await DOVirtual.DelayedCall(ViewConfig.shotEffectDelay, () => { })
        .SetLink(tileView.gameObject)
        .ToUniTask(...);

    tileView.PlayBreakEffect();

    // 5. 发布 TileDestroyed 事件（触发后续逻辑）
    DomainEventBus.PublishForEnumKey(EventType.TileDestroyed, tileData.Id);
}
```

#### 3.1.4 闪电特效播放

```csharp
private void PlayLightEffects(TileView tileView)
{
    if (!tileView)
    {
        return;
    }

    // 1. 注册/播放闪电粒子
    if (!ParticlesController.ContainsParticle(_lightEffectName))
    {
        GameObject effectGameObject = TileResourceHub.LoadAsset<GameObject>(_lightPrefabPath);
        effectGameObject.gameObject.SetActive(false);
        ParticlesController.RegisterParticle(_lightEffectName, effectGameObject);
    }

    // 2. 随机音效
    int randomIndex = TileMatchViewController.Instance.ViewRandomService.Range(1, 6);
    string soundName = $"SFX_lightning{randomIndex}";
    TileMatchViewController.Instance.Proxy.SoundSystemPlaySound(soundName);

    // 3. 触觉反馈
    HapticsHub.Instance.DoHaptic(HapticsTypes.Light);

    // 4. 播放粒子
    var lockEffect = ParticlesController.PlayParticle(_lightEffectName);
    lockEffect.SetPosition(tileView.VisualTransform.position).SetDuration(2.0f);
}
```

#### 3.1.5 配置参数

```csharp
private static readonly LightingViewActionConfig ViewConfig = new();

private readonly string _lightEffectName = "WinStreakLight";
private readonly string _lightPrefabPath = "Assets/Game/TileV2/Res/Game/GameCore/Prop/WinStreak/Prefab/eff_Lightning01.prefab";
```

**`LightingViewActionConfig` 参数**：

| 参数 | 值 | 说明 |
|------|-----|------|
| `shotDelayInterval` | 0.1s | 每张牌特效播放间隔 |
| `shotEffectDelay` | 0.18s | 闪电击中后到牌面打破的延迟 |
| `finalDelay` | 0.5s | 所有特效完成后的最终延迟 |

---

### 3.2 `PrepareChainedAttackActionInvoker.cs`

#### 3.2.1 路由逻辑

```csharp
public override async UniTask ProcessAsync(ActionResult actionResult, CancellationToken cancellationToken)
{
    if (actionResult.Data is ChainedAttackActionData data && data.Data is TileData tileData)
    {
        // 1. 解析 Controller 类型
        var controllerType = ResolveControllerType(tileData);

        // 2. 如果解析到特定 Controller，使用它
        if (controllerType != CustomViewActionControllerType.NotDefined)
        {
            var controller = ViewController.GetViewActionController(controllerType);
            if (controller != null)
            {
                await controller.DoAction(data).AttachExternalCancellation(cancellationToken);
            }
        }

        // 3. 发布 AfterAttack 事件
        DomainEventBus.PublishForEnumKey(EventType.AfterAttack);
    }

    await Task.CompletedTask;
}

private CustomViewActionControllerType ResolveControllerType(TileData tileData)
{
    bool isRocket = tileData.TileType == TileType.Rocket;
    bool isGameView = ViewController is TileMatchViewController;
    int rocketMode = 0;
    
    // 从 DataBridge 获取 RocketMode
    if (isGameView)
    {
        var tileMatchVC = (TileMatchViewController)ViewController;
        var db = tileMatchVC.DataBridge;
        rocketMode = db != null ? db.RocketMode : -1;
    }
    
    // RocketMode=3 → 路由到 RocketVLLighting
    if (isRocket && rocketMode == 3)
    {
        return CustomViewActionControllerType.RocketVLLighting;
    }

    // 其他情况：使用默认路由
    var fallback = ViewController.GetViewActionControllerType(tileData.TileType, ActionType);
    return fallback;
}
```

#### 3.2.2 路由决策树

```
PrepareChainedAttackActionInvoker.ProcessAsync()
  │
  ├─ 解析 Controller 类型: ResolveControllerType(tileData)
  │   │
  │   ├─ 是否火箭牌? (tileData.TileType == Rocket)
  │   │   └─ 是 → 读取 DataBridge.RocketMode
  │   │       ├─ RocketMode == 3 → RocketVLLighting ✅
  │   │       └─ RocketMode == 0/1 → 默认路由（Rocket 普通视图）
  │   │
  │   └─ 否 → 默认路由（根据 TileType 和 ActionType）
  │
  ├─ 获取 Controller 实例
  ├─ 执行 Controller.DoAction(data)
  └─ 发布 AfterAttack 事件
```

---

## 四、数据流详解

### 4.1 完整数据流

```
编辑器输入 3
  │
  ├─ OnRocketEditorEnd: LevelEditorData.SetRocketMode(3)
  │   └─ IsRocket=true, RocketMode=3
  │
  ├─ OnPlayBtnClick: CustomData.SetRocketMode(3)
  │   └─ CustomData.RocketMode=3, IsCanShowRocket=true
  │
  ├─ GameUILogic.SetCustomData(customData)
  │
  ├─ ──── 场景加载 ────
  │
  ├─ TileMatchGame.InitializeGame(customData)
  │   └─ _customData = customData
  │
  ├─ InitializeDataBridge()
  │   └─ UpdateDataBridgeIfNeeded(): Trial 模式从 CustomData 更新
  │       └─ DataBridge.RocketMode = 3
  │
  ├─ TileMatchApplication 初始化
  │   └─ ViewController.DataBridge = DataBridge(RocketMode=3)
  │
  ├─ ──── 游戏进行中 ────
  │
  ├─ 火箭牌消除 → PrepareChainedAttackAction（逻辑层）
  │   └─ ChainedAttackActionData { TileType.Rocket, Waves=[...] }
  │
  ├─ PrepareChainedAttackActionInvoker.ProcessAsync()
  │   ├─ ResolveControllerType(): DataBridge.RocketMode=3 → RocketVLLighting
  │   ├─ RocketVLLightningViewActionController.GetNewAction()
  │   └─ RocketVLLightningViewAction.DoAction(ChainedAttackActionData)
  │       ├─ TryFlattenData: 展平所有 Wave.Targets → _flattenedTargets
  │       ├─ 对每张目标牌（间隔 0.1s）:
  │       │   └─ PlayOneShotEffect(index, tileData, tileView)
  │       │       ├─ 延迟: 0.1s × index
  │       │       ├─ tileView.SetHighlight(true)
  │       │       ├─ PlayLightEffects: 闪电特效 + 音效 + 触觉
  │       │       ├─ 延迟 0.18s
  │       │       ├─ tileView.PlayBreakEffect()
  │       │       └─ DomainEventBus.Publish(TileDestroyed)
  │       │
  │       ├─ UniTask.WhenAll → 等待全部完成
  │       ├─ 延迟 0.5s (finalDelay)
  │       └─ Done（AfterAttack 由 Invoker 发布）
```

### 4.2 关键数据传递节点

| 节点 | 数据类型 | 说明 |
|------|----------|------|
| 编辑器 | `LevelEditorData.RocketMode=3` | 用户输入触发 |
| Trial 模式 | `CustomData.RocketMode=3` | 传递到游戏逻辑 |
| 场景加载 | `DataBridge.RocketMode=3` | 逻辑层存储 |
| 视觉路由 | `CustomViewActionControllerType.RocketVLLighting` | Invoker 决策 |
| 视觉执行 | `ChainedAttackActionData` | 传递到 ViewAction |

---

## 五、视觉效果时间轴

### 5.1 单张牌的时间轴

```
T+0.00s: 开始处理第 N 张牌
  └─ 延迟: 0.1s × index（错开播放）

T+0.00s + delay: 高亮牌面
  ├─ tileView.SetHighlight(true, true)
  └─ tileView.SetSortingOrder(-100)

T+0.00s + delay: 播放闪电特效
  ├─ 注册/播放 eff_Lightning01 粒子
  ├─ 随机音效 SFX_lightning1~5
  └─ 触觉反馈 HapticsTypes.Light

T+0.18s: 播放牌面打破效果
  └─ tileView.PlayBreakEffect()

T+0.18s: 发布 TileDestroyed 事件
  └─ DomainEventBus.PublishForEnumKey(EventType.TileDestroyed, tileData.Id)

T+0.18s~: 牌面消除完成
```

### 5.2 多张牌的并行播放

```
牌1: T+0.00s 开始 → T+0.18s 完成
牌2: T+0.10s 开始 → T+0.28s 完成
牌3: T+0.20s 开始 → T+0.38s 完成
...
所有牌完成后: T+X.XXs + 0.5s (finalDelay) → Done
```

---

## 六、配置与调试

### 6.1 编辑器配置

**文件**: `Editor/LevelEditor/Script/Views/TestControlView/TestControlView.cs`

```csharp
// 输入 3 → 设置 RocketMode=3
if (input == 3)
{
    LevelEditorData.SetRocketMode(3);
}

// 点击 Play 按钮时传递
OnPlayBtnClick()
{
    CustomData.SetRocketMode(LevelEditorData.RocketMode);
    // ... 其他逻辑 ...
}
```

### 6.2 调试日志

**当前状态**: ✅ 调试日志已添加，待清理

| 文件 | 日志内容 |
|------|----------|
| `PrepareChainedAttackActionInvoker.cs` | `[RocketVL] PrepareChainedAttackInvoker hit, TileType={...}` |
| `PrepareChainedAttackActionInvoker.cs` | `[RocketVL] Resolved controllerType={...}` |
| `PrepareChainedAttackActionInvoker.cs` | `[RocketVL] Resolve: isRocket={...}, rocketMode={...}` |
| `PrepareChainedAttackActionInvoker.cs` | `[RocketVL] ROUTING TO RocketVLLighting!` |
| `PrepareChainedAttackActionInvoker.cs` | `[RocketVL] Fallback to: {...}` |
| `RocketVLLightningViewAction.cs` | `[RocketVL] RocketVLLightningViewAction.DoAction ENTERED!` |
| `RocketVLLightningViewAction.cs` | `[RocketVL] TryFlattenData returned false` |
| `RocketVLLightningViewAction.cs` | `[RocketVL] Flattened {N} targets` |
| `RocketVLLightningViewAction.cs` | `[RocketVL] No targets, exiting` |
| `RocketVLLightningViewAction.cs` | `[RocketVL] All effects completed` |
| `RocketVLLightningViewAction.cs` | `[RocketVL] DoAction DONE` |

**清理建议**: 功能验证完成后，移除所有 `[RocketVL]` 前缀的调试日志。

---

## 七、当前状态与待办

### 7.1 已完成

- [x] RocketMode=3 路由到 RocketVLLighting
- [x] 闪电击中特效正常播放
- [x] 球体动画已移除，仅保留闪电打牌
- [x] 音效随机播放（SFX_lightning1~5）
- [x] 触觉反馈正常
- [x] 牌面打破效果正常
- [x] 正常运行火箭模式（0/1）不受影响

### 7.2 待办事项

- [ ] 清理调试日志（所有 `[RocketVL]` 日志）
- [ ] 性能测试：大量牌同时消除时的帧率
- [ ] 真机测试：iOS/Android 特效表现
- [ ] 编辑器文档更新：说明 RocketMode=3 的用途

---

## 八、常见问题

### 8.1 为什么 RocketVL 只在编辑器生效？

**设计意图**: RocketVL 是**编辑器测试功能**，用于验证闪电球视觉效果。正式游戏中不使用 RocketMode=3。

**如果要在正式游戏中使用**: 需要从服务器配置或玩家设置中传递 `RocketMode` 到 `DataBridge`。

### 8.2 为什么闪电特效使用 WinStreak 的资源？

**资源复用**: `eff_Lightning01.prefab` 原本用于连胜闪电球，RocketVL 直接复用该资源，避免重复制作特效。

**路径**: `Assets/Game/TileV2/Res/Game/GameCore/Prop/WinStreak/Prefab/eff_Lightning01.prefab`

### 8.3 为什么需要修改 `DataBridge` 的访问权限？

**跨程序集访问**: `PrepareChainedAttackActionInvoker` 在 Application 层，`TileMatchViewController.DataBridge` 在 View 层，需要 `public` 访问权限。

---

## 九、文件依赖关系

### 9.1 编译依赖

```
RocketVLLightningViewAction.cs
  ├─ 依赖: BaseViewAction
  ├─ 依赖: LightingViewActionConfig
  ├─ 依赖: ParticlesController
  ├─ 依赖: TileResourceHub
  └─ 依赖: DomainEventBus

RocketVLLightningViewActionController.cs
  └─ 依赖: BaseViewActionController

PrepareChainedAttackActionInvoker.cs
  ├─ 依赖: CustomViewActionControllerType.RocketVLLighting
  ├─ 依赖: DataBridge.RocketMode
  └─ 依赖: ViewController.GetViewActionController()

DataBridge.cs
  └─ 新增: RocketMode 字段

CustomData.cs
  └─ 新增: RocketMode 字段 + SetRocketMode() 方法
```

### 9.2 运行时依赖

```
编辑器输入
  ↓
CustomData (传递 RocketMode)
  ↓
DataBridge (存储 RocketMode)
  ↓
PrepareChainedAttackActionInvoker (读取 RocketMode)
  ↓
RocketVLLightningViewActionController (创建 ViewAction)
  ↓
RocketVLLightningViewAction (执行视觉效果)
```

---

## 关联

- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]]

- [[分析-RocketV2完整逻辑-v2（重构版）]]
- [[分析-RocketV2技术实现-v1]]
- [[分析-关卡连胜与闪电球逻辑-v1|关卡连胜与闪电球逻辑]]
