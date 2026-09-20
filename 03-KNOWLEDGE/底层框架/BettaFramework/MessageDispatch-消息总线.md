---
title: MessageDispatch 消息总线
date: 2026-09-18
type: knowledge
status: finalized
lifecycle: current
priority: high
project: 跨项目
tags: [LibraryG, 03-KNOWLEDGE, 底层框架, BettaFramework, MessageDispatch, 消息总线, 跨项目]
source: "Packages/BettaFramework/Scripts/Runtime/Message/MessageDispatch.cs + MessageType.cs 逐文件深读（工作区版本，2026-09-18）"
verification: "类结构/方法签名为源码原文；dispatch 重入语义为源码阅读推断；未做运行时验证"
---

# MessageDispatch 消息总线

> BettaFramework 的事件总线。字符串 Key + 泛型委托，支持 0~3 参数。仅 480 行，**100% 可复刻**（唯一外部依赖是 `BettaSDK.Singleton`）。

---

## 一、文件与类型

| 文件 | 关键类型 | 职责 |
|---|---|---|
| `MessageType.cs` | `MessageType`（static class） | 框架内置消息 Key 常量 |
| `MessageDispatch.cs` | `IDelegateContainer`、`DelegateContainerBase<TDelegate>`、`DelegateContainer` / `DelegateContainer<T>` / `<T1,T2>` / `<T1,T2,T3>`、`MessageImplementation`、`MessageDispatch` | 总线实现 |

```
IDelegateContainer (interface)
   ▲
DelegateContainerBase<TDelegate> (abstract, TDelegate:class)     # 持有 List<TDelegate> CallBacks
   ├── DelegateContainer       : DelegateContainerBase<Action>
   ├── DelegateContainer<T>    : DelegateContainerBase<Action<T>>
   ├── DelegateContainer<T1,T2>: DelegateContainerBase<Action<T1,T2>>
   └── DelegateContainer<T1,T2,T3>: DelegateContainerBase<Action<T1,T2,T3>>

MessageImplementation    # 真正实现（Dictionary<string,object> 存容器）
MessageDispatch : Singleton<MessageDispatch>   # 门面，转发到 MessageImplementation
```

---

## 二、MessageType（内置 Key 常量）

```csharp
public static class MessageType
{
    public const string OnApplicationFocus   = "OnApplicationFocus";
    public const string OnApplicationPause   = "OnApplicationPause";
    public const string OnApplicationQuit    = "OnApplicationQuit";
    public const string OnClientBuildFetched = "OnClientBuildFetched";
    public const string OnWindowOpen         = "OnWindowOpen";
    public const string OnWindowClose        = "OnWindowClose";
    public const string OnWindowFocus        = "OnWindowFocus";
}
```

> 前三个是应用生命周期；后三个由 `UIManager` 派发。业务自定义 Key 直接传字符串即可，但约定统一放 `MessageType` 类保持跨项目一致。

---

## 三、DelegateContainer 系列（存储单元）

```csharp
public interface IDelegateContainer
{
    int Count { get; }
    void RemoveNullCallbacks();               // 压缩移除 null 槽位
}

public abstract class DelegateContainerBase<TDelegate> : IDelegateContainer where TDelegate : class
{
    public readonly List<TDelegate> CallBacks = new();
    public int Count => CallBacks.Count;

    public void RemoveNullCallbacks()
    {
        // 双指针压缩：把非 null 前移，再从尾部 RemoveAt 掉剩余 null
        var writeIndex = 0;
        for (var readIndex = 0; readIndex < CallBacks.Count; readIndex++)
        {
            var callback = CallBacks[readIndex];
            if (callback == null) continue;
            if (writeIndex != readIndex) CallBacks[writeIndex] = callback;
            writeIndex++;
        }
        for (var i = CallBacks.Count - 1; i >= writeIndex; i--)
            CallBacks.RemoveAt(i);
    }
}
```

> 存储用 `List`（非 HashSet/Delegate），因为同签名监听**允许重复添加**（不做去重）；移除用 `IndexOf` 精确匹配。

---

## 四、MessageImplementation（核心实现）

```csharp
public class MessageImplementation
{
    private readonly Dictionary<string, object> _containerDic;   // key → DelegateContainer
    private readonly List<string> _pendingRemovalKeys;           // 待压缩 key 列表
    private readonly HashSet<string> _pendingRemovalKeySet;      // 去重
    private int _dispatchDepth;                                  // 派发深度（重入护栏）
}
```

### Add（4 个重载，泛型分派到私有模板方法）

```csharp
public void AddEventListener(string messageKey, Action listener);
public void AddEventListener<T>(string messageKey, Action<T> listener);
public void AddEventListener<T1,T2>(string messageKey, Action<T1,T2> listener);
public void AddEventListener<T1,T2,T3>(string messageKey, Action<T1,T2,T3> listener);

private void AddEventListener<TDelegate, TContainer>(string messageKey, TDelegate listener)
    where TDelegate : class
    where TContainer : DelegateContainerBase<TDelegate>, new()
{
    if (listener == null) return;
    var container = GetOrCreateContainer<TContainer>(messageKey);
    container.CallBacks.Add(listener);
}
```

### Remove（关键：dispatch 中移除的处理）

```csharp
private void RemoveEventListener<TDelegate, TContainer>(string messageKey, TDelegate listener)
{
    if (listener == null) return;
    var container = GetContainer<TContainer>(messageKey);
    if (container == null) return;
    var callbacks = container.CallBacks;
    var index = callbacks.IndexOf(listener);
    if (index < 0) return;

    if (_dispatchDepth > 0)                         // ★ 派发中：置 null + 登记待处理
    {
        callbacks[index] = null;
        if (_pendingRemovalKeySet.Add(messageKey))
            _pendingRemovalKeys.Add(messageKey);
        return;
    }

    callbacks.RemoveAt(index);                       // 空闲：直接移除
    if (callbacks.Count == 0)
        _containerDic.Remove(messageKey);            // 空容器回收
}
```

### Dispatch（4 个重载 + 重入护栏）

```csharp
public void Dispatch(string messageKey)
{
    var container = GetContainer<DelegateContainer>(messageKey);
    if (container == null) return;
    BeginDispatch();
    try {
        var callbacks = container.CallBacks;
        for (var i = 0; i < callbacks.Count; i++)
        {
            var callback = callbacks[i];
            if (callback == null) continue;           // 跳过被移除的槽位
            callback();
        }
    }
    catch (Exception e) {
        Debug.LogError($"{nameof(MessageDispatch)} dispatch error, messageKey:{messageKey}\n{e.Message}\n{e.StackTrace}");
    }
    finally { EndDispatch(); }
}

private void BeginDispatch() { _dispatchDepth++; }
private void EndDispatch()
{
    _dispatchDepth--;
    if (_dispatchDepth == 0)
        ProcessPendingRemovals();                    // 回到最外层才统一压缩
}
```

### `ProcessPendingRemovals`（延迟压缩）

最外层派发结束时，遍历 `_pendingRemovalKeys`，对每个 key 调 `RemoveNullCallbacks()`，容器空则从 `_containerDic` 移除，最后清空 pending 集合。

---

## 五、MessageDispatch（门面）

```csharp
public class MessageDispatch : Singleton<MessageDispatch>
{
    private readonly MessageImplementation _implementation = new();
    // 4 组 × {AddEventListener / RemoveEventListener / Dispatch}，每组 0~3 参数
}
```

全部方法只是转发到 `_implementation`。用法：

```csharp
MessageDispatch.Instance.AddEventListener<Foo>("my_event", OnFoo);
MessageDispatch.Instance.Dispatch("my_event", fooArg);
MessageDispatch.Instance.RemoveEventListener<Foo>("my_event", OnFoo);
```

---

## 六、核心机制总结（复刻要点）

1. **字符串 Key + 泛型容器**：Key 命中后按容器泛型类型取回，`(TContainer)containerObj` 强转。同一 Key 不同签名互不冲突（存的是不同 `DelegateContainer` 实例）。
2. **派发中可安全增删监听**：`Remove` 在 `_dispatchDepth > 0` 时把槽位置 null + 登记，避免迭代中移除导致下标错乱；最外层 `EndDispatch` 统一压缩。
3. **嵌套派发**：`_dispatchDepth` 计数支持回调里再次 `Dispatch`；只有回到 0 才 `ProcessPendingRemovals`。
4. **单回调异常不中断派发**：每个 `callback()` 包在 for 循环内，但异常会**跳出整个 Dispatch 的 try**（后续监听不再执行），仅记录日志。复刻时如需"每个监听独立隔离"，需自行改为 per-callback try。
5. **`Singleton` 来自 BettaSDK**：替换为 Unity 单例或自行实现即可，其余逻辑零依赖。

---

## 关联

- [[03-KNOWLEDGE/底层框架/BettaFramework/框架总览|框架总览]] — 本模块定位
- [[03-KNOWLEDGE/底层框架/BettaFramework/UIManager-窗口生命周期|UIManager-窗口生命周期]] — `OnWindowOpen/Close/Focus` 的派发方
- [[03-KNOWLEDGE/底层框架/BettaSDK/SDK总览|BettaSDK 分册]] — `Singleton` 基类
