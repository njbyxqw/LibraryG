---
title: UIManager 窗口生命周期
date: 2026-09-18
type: knowledge
status: finalized
lifecycle: current
priority: high
project: 跨项目
tags: [LibraryG, 03-KNOWLEDGE, 底层框架, BettaFramework, UIManager, 窗口系统, 跨项目]
source: "Packages/BettaFramework/Scripts/Runtime/UIManager/*.cs 全部 8 文件逐文件深读（工作区版本，2026-09-18）"
verification: "类结构/方法签名/状态集合为源码原文；行为语义为源码阅读推断；未做运行时验证"
---

# UIManager 窗口生命周期

> BettaFramework 的窗口系统核心。本模块共 8 文件 / 3239 行，是框架最大的一块。
> 关键特征：**分层 Canvas + 窗口栈 + 串行过渡队列 + 聚焦机制 + 原生屏幕适配**。

---

## 一、类层次与文件清单

```
IUIBase (Interface.UI)                 IUIWindow (Interface.UI)      IUIWindowAnimation (Interface.UI)
   ▲                                       ▲                              ▲
UIBase (abstract) ───────────────── UIWindow (abstract) ───────────────┘
   ▲
业务窗口（继承 UIWindow，实现 AssetPath）
```

| 文件 | 关键类型 | 行数 | 职责 |
|---|---|---|---|
| `UIBase.cs` | `UIBase`、`UIDefine`、`UIPrefabVariantPolicy` | ~200 | 窗口基类：资源加载、cell 子窗口管理 |
| `UIWindow.cs` | `UIWindow` | ~250 | 窗口：配置读取、动画、关闭入口 |
| `UICanvas.cs` | `UICanvas` | ~80 | 分层 Canvas（排序 + 分辨率适配） |
| `UIWindowConfig.cs` | `UIWindowConfig` | ~10 | 窗口配置组件（挂 prefab 根） |
| `UIWindowBg.cs` | `UIWindowBg` | ~60 | 遮罩背景（点击关闭） |
| `UIManager.cs` | `UIManager` | ~2414 | ★ 管理器：窗口栈/生命周期/聚焦/屏幕适配 |
| `UIScreenChangeCoordinator.cs` | `UIScreenChangeCoordinator` | ~200 | 屏幕变更稳定性协调器（状态机） |
| `Screen/ScreenResolution.cs` | `ScreenResolution`、`ScreenResolutionInfo`、`UILayoutOrientation`、`UICanvasMatchMode` | ~150 | 分辨率策略 |

---

## 二、UIBase（窗口基类）

```csharp
public abstract class UIBase : IUIBase
{
    protected abstract string AssetPath { get; }                          // 子类必须指定 prefab 路径
    protected virtual UIPrefabVariantPolicy PrefabVariantPolicy =>
        UIPrefabVariantPolicy.AdaptiveSinglePrefab;                        // 资源变体策略
    public RectTransform RectTransform { get; private set; }
    private readonly List<UIBase> _cells = new();                          // 子 cell 列表

    public virtual void OnOpen(params object[] args) { TryPrepareForOpen(); }
    public virtual void OnUpdate(long timeDelta) { /* 遍历 _cells */ }
    public virtual void OnClose() { /* Destroy RectTransform.gameObject */ }

    public T CreateCell<T>(Transform parent, params object[] args) where T : UIBase, new();
    public void DestroyCell(UIBase uiBase);
}
```

### 关键机制：资源加载三级回退（`Load`）

`UIBase.Load(assetPath, variantPolicy)` 按优先级尝试：

1. **`LoadFromHub`** — `ResourceHub.Exists` → `ResourceHub.LoadGameObject`（BettaSDK 的 AssetBundle 路径，运行时主通道）
2. **`LoadFromAssetDatabase`**（仅 `UNITY_EDITOR` 且 `!Application.isPlaying`）— `AssetDatabase.LoadAssetAtPath`（编辑器直读，需 `Assets/` 前缀）
3. **`LoadFromResources`** — `Resources.Load<GameObject>`（兜底）

`BuildAssetPathList` 处理 **Pad 资源变体**：当 `PrefabVariantPolicy == LegacyPadSuffix` 且 `UtilsDevice.UseLegacyPadUIResourceVariant` 为真时，会先尝试 `{fileName}_pad{ext}`，再回退原名。

> 加载成功后 `go.name = fileName`（去目录、去扩展名），保证运行时对象命名统一。

---

## 三、UIWindow（窗口）

```csharp
public abstract class UIWindow : UIBase, IUIWindow, IUIWindowAnimation
{
    public UIWindowConfig UIWindowConfig { get; private set; }
    public int  LayerOrder      => UIWindowConfig.layerOrder;      // 所属 Canvas 排序层
    public bool CanFocus        => UIWindowConfig.canFocus;
    public UIMaskType MaskType  => UIWindowConfig.maskType;
    public bool HideWhenPushed  => UIWindowConfig.hideWhenPushed;
    public string Name          => GetType().Name;
    protected virtual bool UseDefaultWindowAnimation => true;

    public override void OnOpen(params object[] args);
    public virtual void OnFocus(bool focus);
    public void Close(UIOperation closeType);
    public void Close(UIOperation closeType, Action completed);
    public virtual IEnumerator PlayOpenAnimation() / PlayCloseAnimation() / PlayResumeAnimation() / PlayHideAnimation();
    public virtual void ApplyCurrentScreen(NativeWindowMetrics current);
    public virtual void ApplyScreenChange(ScreenChangeInfo change);
}
```

### OnOpen 流程

1. `base.OnOpen` → `TryPrepareForOpen()`（加载 prefab，取 RectTransform）
2. 从 RectTransform 根取 `UIWindowConfig`；**缺失则 `AddComponent<UIWindowConfig>()` 兜底**（并告警）
3. `InitializeDefaultAnimation()`：若 `UseDefaultWindowAnimation`，取/加 `Animation` 组件，注册 4 个默认 clip（`open`/`close`/`resume`/`hide`，资源名 `UI/UIWindowOpen` 等）
4. `UIManager.Instance.GetCanvas(LayerOrder)` 拿到目标 Canvas，`SetParent(uiCanvas.transform, false)`

### 默认动画实现（`PlayAnimation`）

不用 `Animation.Play`，而是**手动逐帧采样**：`state.speed=0` → 每帧 `state.time = min(length, realtimeSinceStartup - startedAt)` → `Sample()`，直到 `state.time >= length`。关闭/隐藏用同一个 `Animation` 组件。

---

## 四、UICanvas / UIWindowConfig / UIWindowBg

### UICanvas（分层 Canvas）

```csharp
public class UICanvas : MonoBehaviour
{
    private Canvas _canvas;
    private CanvasScaler _scaler;
    // Awake: uiScaleMode = ScaleWithScreenSize
    public void ApplyWindowMetrics(NativeWindowMetrics metrics);   // 依据横竖屏选 resolutionInfo
    public void Init(Camera cam, int sortingOrder);               // worldCamera=uiCamera, planeDistance=10, sortingOrder, 命名 UICanvas_{order}
}
```

- 每个 `sortingOrder` 一个 Canvas，`UIManager.GetCanvas(order)` 缓存到 `Dictionary<int, UICanvas> _canvases`
- 默认层 `UIDefine.UISortingOrderDefault = 100`
- `_scaler.matchWidthOrHeight` 由 `ScreenResolutionInfo` 的 Phone/Pad 两种 matchMode 决定（`MatchWidth→0f`，`MatchHeight→1f`）

### UIWindowConfig（挂在 prefab 根的组件）

```csharp
public class UIWindowConfig : MonoBehaviour
{
    public int layerOrder = 100;                       // 所在 Canvas 层
    public bool canFocus = true;                       // 是否参与聚焦
    public UIMaskType maskType = UIMaskType.None;      // 遮罩类型（None/AutoClose...）
    public bool hideWhenPushed = true;                 // 被新窗口压栈时是否隐藏
}
```

### UIWindowBg（遮罩）

`Refresh(IReadOnlyList<IUIWindow> windows)` 从栈顶往下找第一个 `MaskType != None` 且 active 的窗口，把遮罩挂到它下面（`SetAsFirstSibling`）；`MaskType == AutoClose` 时点击遮罩触发 `UIManager.Close(window, UIOperation.Click)`。

---

## 五、UIManager 数据结构（完整状态集合）

```csharp
public class UIManager : SingletonMono<UIManager>, IUIManager, IApplicationModule
{
    public Camera uiCamera;

    // Canvas / 安全区
    private readonly Dictionary<int, UICanvas> _canvases;
    private readonly HashSet<UICanvas> _screenAdaptiveCanvases;             // 参与屏幕适配的额外 Canvas
    private readonly HashSet<UICanvas> _screenAdaptiveCanvasesPendingBatchApply;
    private readonly HashSet<UISafeArea> _safeAreas;
    private readonly HashSet<UISafeArea> _safeAreasPendingBatchApply;

    // 窗口状态集合（核心）
    private readonly List<IUIWindow> _openingWindows;                        // 正在 OnOpen 的窗口
    private readonly Dictionary<IUIWindow, UIOperation> _openingCloseRequests;// opening 期间的关闭请求
    private readonly List<IUIWindow> _windows;                               // 已打开窗口栈（顺序=层级）
    private readonly List<IUIWindow> _windowUpdateSnapshot;                  // OnUpdate 快照
    private readonly List<IUIWindow> _pendingActivationWindows;              // 等待屏幕 metrics 提交的窗口
    private readonly Dictionary<IUIWindow, UIOperation> _pendingWindowOpenTypes;
    private readonly HashSet<IUIWindow> _suspendedWindows;                   // 已挂起（SetActive(false)）
    private readonly HashSet<IUIWindow> _stackHiddenWindows;                 // 被压栈隐藏
    private readonly HashSet<IUIWindow> _queuedOpenWindows;                  // 排队打开
    private readonly HashSet<IUIWindow> _queuedResumeWindows;                // 排队恢复
    private readonly HashSet<IUIWindow> _transitionOpeningWindows;           // 过渡中打开
    private readonly HashSet<IUIWindow> _closingWindows;                     // 关闭中
    private readonly Queue<WindowTransitionRequest> _transitionQueue;        // 过渡队列
    private readonly Dictionary<IUIWindow, WindowInteractionState> _windowInteractionStates;
    private readonly Dictionary<IUIWindow, Action> _closeCompletionCallbacks;
    private readonly Dictionary<IUIWindow, PendingWindowScreenCallback> _deferredWindowScreenCallbacks;
    private readonly UIScreenChangeCoordinator _screenChangeCoordinator;
    private IUIWindow _focusedWindow;                                        // 当前聚焦窗口
    private Coroutine _transitionCoroutine;

    private UIWindowBg _uiWindowBg;
    // 重入/批处理护栏
    private bool _screenSignalsSubscribed;
    private bool _isApplyingScreenBatch;
    private bool _hasActiveScreenBatchMetrics;
    private NativeWindowMetrics _activeScreenBatchMetrics;
    private int _windowScreenCallbackDepth;
    private int _windowLifecycleDepth;
    private int _transitionQueueHoldDepth;
    private bool _isTransitionQueueRunning;
    private long _windowScreenApplyFailureVersion;
}
```

> 状态集合多达 12 组，是理解生命周期的关键。窗口在任一时刻归属其中一个或多个集合。

---

## 六、打开流程（`Open<T>`）

`Open<T>(UIOperation openType, string source, params object[] args)` 完整链路：

```
Open<T>
 ├─ 校验 openType ∈ {Click, Auto}（否则 ArgumentOutOfRangeException）
 ├─ EnsureScreenAdaptationRuntime()               # 订阅屏幕信号 + 刷新 coordinator target
 ├─ 查重 GetWindow<T>()：
 │    ├─ 命中且 closing → return null
 │    ├─ 命中且 pendingActivation / queuedOpen → return (T)window   # 已在开，直接返回
 │    ├─ 命中（已开）→ QueueWindowResume(window)                    # 拉回前台
 │    └─ 命中 opening → return（除非有 pending close 请求）
 ├─ new T()
 ├─ _openingWindows.Add(window)
 ├─ RunWindowLifecycle(() => { TryPrepareForOpen(); OnOpen(args); })
 │     # 异常则清理 + InvokeWindowClose + return null
 ├─ prepared==false → 清理 return null
 ├─ _openingWindows.Remove(window)；若有 opening 期间 close 请求 → 关闭 return null
 ├─ RectTransform==null → 关闭 return null
 ├─ ShouldDeferWindowActivation(...)?            # 屏幕适配未就绪时延迟
 │    └─ 是：SetActive(false) + _pendingActivationWindows.Add + 记录 openType，return window
 └─ QueueWindowOpen(window, openType) → 返回 window（成功时已在 _windows）
```

### `ShouldDeferWindowActivation`（屏幕适配延迟开关）

```csharp
return screenAdaptationActive &&
       (!hasCommittedWindowMetrics || isApplyingScreenBatch || hasPendingTarget);
```

即：屏幕适配激活且（首次尚未提交 metrics / 正在应用批 / 有 pending target）时，窗口先挂 `_pendingActivationWindows`，等 `CommitWindowMetrics` 后由 `ActivatePendingWindows` 统一激活。

### `QueueWindowOpenInternal`（实际入队）

1. `SetActive(false)` → 加 `_suspendedWindows`
2. 加 `_queuedOpenWindows` + `_transitionOpeningWindows`
3. `_transitionQueueHoldDepth++`（**暂停队列**，防止入队中途执行）
4. `EnqueueWindowTransition(Open)` + `FinalizeWindowOpen`（加 `_windows` + 派发 `OnWindowOpen` 事件 + 聚焦）
5. 检查 opening 期间的 close 请求
6. `finally`：`_transitionQueueHoldDepth--` + `StartWindowTransitionQueue()`

---

## 七、关闭流程（`Close`）

`Close(IUIWindow window, UIOperation closeType, Action completed)`：

```
Close(window, closeType, completed)
 ├─ window==null → completed?.Invoke() return
 ├─ RegisterCloseCompletion(window, completed)     # 合并 completion（多次 close 累加）
 ├─ opening / transitionOpening → 记录 _openingCloseRequests 延迟关闭
 ├─ pendingActivation → CloseWindowImmediately("while closing before activation")
 ├─ !_windows.Contains → InvokeCloseCompletion return
 ├─ !_closingWindows.Add(window) → return          # 已在关闭，忽略
 ├─ suspended / RectTransform==null / inactive → CloseWindowImmediately("hidden window")
 └─ EnqueueWindowTransition(Close)                 # 走动画关闭
```

`CloseWindowImmediately(window, closeType, context, invokeCompletion)` 是**所有路径的最终出口**：从全部 12 个状态集合移除 → `RestoreWindowInteraction` → 聚焦转移 → `InvokeWindowClose`（调 `window.OnClose`）→ 派发 `OnWindowClose` 事件 → `InvokeCloseCompletion`。

---

## 八、过渡队列（串行协程）

### 入队与调度

```csharp
private void StartWindowTransitionQueue()
{
    if (_transitionQueueHoldDepth > 0 || _isTransitionQueueRunning || _transitionQueue.Count == 0) return;
    _isTransitionQueueRunning = true;
    _transitionCoroutine = StartCoroutine(ProcessWindowTransitionQueue());
}

private IEnumerator ProcessWindowTransitionQueue()
{
    while (_transitionQueue.Count > 0)
    {
        var request = _transitionQueue.Dequeue();
        var transition = GetWindowTransition(request);       // Open→Show / Resume→Show / Close→Close
        var runner = RunWindowTransitionSafely(transition, request);
        while (runner.MoveNext()) yield return runner.Current;   // 串行驱动嵌套 IEnumerator
    }
    _transitionCoroutine = null;
    _isTransitionQueueRunning = false;
}
```

- `RunWindowTransitionSafely` 用 `Stack<IEnumerator>` 手动展开嵌套迭代器，逐个 `MoveNext`，异常时 `DisposeEnumerator` + 跳过当前过渡。
- 三种过渡类型（`WindowTransitionType`）：`Open` / `Resume` / `Close`。

### `ShowWindowWithTransition`（打开/恢复）

```
1. previous = FindTopStackWindow(window.LayerOrder, window)
2. CanTransitionBetween(previous, window)?   # 均 CanFocus 且同层
     → BlockWindowInteraction(previous)       # 加 CanvasGroup，禁交互
     → PlayWindowAnimation(previous, Hide)    # 播放压栈隐藏动画
     → HideWindowInStack(previous)            # 加 suspended+stackHidden，SetActive(false)
3. BlockWindowInteraction(window)
4. MoveWindowToFront(window)                  # _windows 移到末尾 + SetAsLastSibling
5. ResumeWindowForTransition(window, request) # 激活 + 屏幕回调 + 聚焦
6. PlayWindowAnimation(window, Open/Resume)
7. RestoreWindowInteraction(window)
```

### `CloseWindowWithTransition`（关闭）

```
1. BlockWindowInteraction(window)
2. PlayWindowAnimation(window, Close)
3. CloseWindowImmediately(window, closeType, "after close animation", false)
4. shouldResumeStack(window.CanFocus)?
     → resumeWindow = FindTopStackWindow(layerOrder)
     → BlockWindowInteraction(resumeWindow)
     → ResumeWindowForTransition(resumeWindow)
     → PlayWindowAnimation(resumeWindow, Resume)
     → RestoreWindowInteraction(resumeWindow)
finally: 兜底关闭 + 恢复 + _closingWindows.Remove + InvokeCloseCompletion
```

---

## 九、聚焦机制

```csharp
private IUIWindow FindTopFocusableWindow()
{
    for (int i = _windows.Count - 1; i >= 0; i--)        // 从栈顶往下
        if (IsWindowParticipating(window) && window.CanFocus)
            return window;
    return null;
}

private void SetFocusedWindow(IUIWindow target)
{
    // 校验 target 参与且 CanFocus，否则置 null
    if (ReferenceEquals(_focusedWindow, target)) return;
    previous = _focusedWindow; _focusedWindow = target;
    previous?.OnFocus(false);                            // 旧窗口失焦
    target?.OnFocus(true);                               // 新窗口聚焦（校验仍在 _windows）
}
```

- `IsWindowParticipating`：`_windows` 含 + 非 suspended + RectTransform 存在且 `activeInHierarchy`。
- `UIWindow.OnFocus(bool)` 内部派发 `MessageType.OnWindowFocus`（携带 `this` + focus）。
- 触发点：`FinalizeWindowOpen`、`HideWindowInStack`、`CloseWindowImmediately`、`Suspend`、`Resume`。

---

## 十、交互阻断（动画期间）

```csharp
private void BlockWindowInteraction(IUIWindow window)   // 加 CanvasGroup，interactable=false, blocksRaycasts=true
private void RestoreWindowInteraction(IUIWindow window) // 恢复原 interactable/blocksRaycasts
```

`_windowInteractionStates` 记录每个窗口被阻断前的 `CanvasGroup.interactable` / `blocksRaycasts`，动画结束恢复。用 `WindowInteractionState`（readonly struct）保存。

---

## 十一、屏幕适配（原生尺寸桥接）

### 信号订阅与批处理（`OnPreWillRenderCanvases`）

UIManager 在 `Awake` 里 `Canvas.preWillRenderCanvases += OnPreWillRenderCanvases`，每帧 Canvas 渲染前：

```
OnPreWillRenderCanvases
 ├─ 护栏：!subscribed || isApplyingScreenBatch || callbackDepth>0 || lifecycleDepth>0 → return
 ├─ UNITY_EDITOR: ObserveEditorGameViewMetrics()   # 编辑器 GameView 尺寸观察
 ├─ RefreshCoordinatorTarget()                    # 从 UtilsNative 取 pending/current 目标
 ├─ !HasTarget → RecoverPendingWindowsFromCommittedMetrics() return
 ├─ _screenChangeCoordinator.SampleUnitySurface(Time.frameCount, Screen.width, Screen.height)
 │     # 等比校验（AspectRatioTolerance=0.01）+ 稳定帧计数（StableFrameCountRequired=2）
 │     # 超时（TimeoutFrameCount=30）降级：直接用原生目标，防永久 inactive
 ├─ ConsumeTimeoutWarning() → 打日志
 └─ TryBeginApplying(out batchTarget)?
       ├─ IsInitial → ApplyInitialScreenState(metrics)
       └─ else       → ApplyQueuedScreenChanges(batchTarget)   # 逐 SequenceId 应用
```

### 关键数据结构：`UIScreenChangeCoordinator`

- 状态机：`Idle → WaitingUnity → Ready → Applying → Idle`
- `SetTarget(seqId, metrics)` / `SampleUnitySurface(frame, w, h)` / `TryBeginApplying` / `CompleteApplying`
- 稳定性判定：连续 `StableFrameCountRequired(2)` 帧宽高+宽高比一致才算 `Ready`；超过 `TimeoutFrameCount(30)` 帧降级 `Ready`
- `MetricsEqual` 比较 10 个字段（宽高/旋转/密度/四边 inset/物理 DPI）

### `ApplyCanvasAndSafeAreas`（核心应用）

```
UtilsDevice.ApplyWindowMetrics(metrics)          # 设备形态因子落定
ScreenResolution.Init(GetLayoutOrientation(metrics))   # 横竖屏 → 选 resolutionInfo
遍历 _canvases ∪ _screenAdaptiveCanvases → canvas.ApplyWindowMetrics
遍历 _safeAreas → safeArea.RefreshFromNativeWindow(metrics, true)
```

### `ActivatePendingWindows`（延迟窗口激活）

`CommitWindowMetrics` 后，把 `_pendingActivationWindows` 逐个 `QueueWindowOpenInternal(..., hasInitialScreenMetrics:true, ...)`。分批排空（`MaxPendingActivationPassesPerFrame=8` 防递归爆栈）。

> 这是「Android 首次启动 UI 永久 inactive」问题的防线：Canvas/SafeArea 失败仍激活窗口，用现有布局降级显示，仅标记 batch 失败。

---

## 十二、生命周期回调与事件派发

| 事件（`MessageType`） | 派发点 | 载荷 |
|---|---|---|
| `OnWindowOpen` | `FinalizeWindowOpen` | `(window.Name, openType)` |
| `OnWindowClose` | `CloseWindowImmediately`（wasOpened） | `(window.Name, closeType)` |
| `OnWindowFocus` | `UIWindow.OnFocus` | `(this, focus)` |

`OnUpdate`：`_windows` 快照遍历，`IsWindowParticipating` 且非 closing 才调 `window.OnUpdate(timeDelta)`，`timeDelta` = `(long)(deltaTime * 1000f)`（毫秒）。

---

## 十三、完整公开 API（UIManager）

| 方法 | 签名 | 说明 |
|---|---|---|
| 打开 | `T Open<T>(UIOperation openType, string source, params object[] args) where T:class,IUIWindow,new()` | 打开/复用/拉前台 |
| 关闭 | `void Close<T>(UIOperation) where T:class,IUIWindow,new()` | 按类型关 |
| 关闭 | `void Close(IUIWindow, UIOperation)` / `(IUIWindow, UIOperation, Action)` | 带完成回调 |
| 关闭全部 | `void CloseAll()` | 取消过渡后逐个立即关 |
| 挂起/恢复 | `void Suspend(IUIWindow)` / `void Resume(IUIWindow)` | 手动 SetActive 开关 |
| 查询 | `bool IsWindowOpen<T>()` | 是否已开 |
| Canvas | `UICanvas GetCanvas(int sortingOrder)` | 取/建分层 Canvas |
| 安全区 | `void RegisterSafeArea(UISafeArea)` / `UnregisterSafeArea` | 注册到适配集合 |
| 自适应 Canvas | `void RegisterScreenAdaptiveCanvas(UICanvas)` / `UnregisterScreenAdaptiveCanvas` | 额外参与适配 |
| 方向 | `void OrientationToPortrait()` / `OrientationToLandscape()` | 强制方向 |
| 生命周期 | `void Init(IImplementManager)` / `Release()` | IApplicationModule |
| 注入 | `void RegisterImplement(IImplementManager)` / `UnRegisterImplement` | 注入 IUIManager |
| 指标 | `NativeWindowMetrics GetInitialWindowMetrics()` | 取初始 metrics |

---

## 十四、复刻要点与坑

1. **窗口栈顺序 = `_windows` List 顺序**，`MoveWindowToFront` = 移到 List 末尾 + `SetAsLastSibling`，两层顺序必须一致。
2. **过渡队列是串行协程**，`_transitionQueueHoldDepth` 用于入队原子性（批量加多个过渡时暂停执行）。
3. **`SingletonMono` 依赖 BettaSDK**，复刻时需自带或替换为 Unity 原生单例。
4. **屏幕适配是最大耦合点**：`UtilsNative`（原生尺寸回调）/`UtilsDevice`（Pad 判定）都在 BettaSDK Native 层，无法纯抄，需自建等价桥接或复用 BettaSDK。
5. **`Resources` 资源约定**：`UICanvas`、`UIWindowBg` 需在 `Resources` 下；`UIWindowBg` 业务侧可覆盖（`Assets/Betta/Resources/UI/UIWindowBg` 优先）。
6. **`OnOpen` 内严禁再次打开/关闭窗口**（由 `_windowLifecycleDepth` / `_transitionQueueHoldDepth` 护栏保护），跨窗口操作走过渡队列。
7. **动画逐帧 `Sample()`** 而非 `Play()`，保证 close/hide 同组件不互相打断。

---

## 关联

- [[03-KNOWLEDGE/底层框架/BettaFramework/框架总览|框架总览]] — 本模块定位与依赖
- [[03-KNOWLEDGE/底层框架/BettaInterface/契约总览|BettaInterface 契约]] — `IUIBase` / `IUIWindow` / `IUIManager` / `UIOperation` / `UIMaskType` 定义
- [[03-KNOWLEDGE/底层框架/BettaSDK/SDK总览|BettaSDK 分册]] — `SingletonMono` / `ResourceHub` / `UtilsNative` / `UtilsDevice`
