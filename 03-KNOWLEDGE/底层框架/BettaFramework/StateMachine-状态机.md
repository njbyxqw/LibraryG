---
title: StateMachine 状态机
date: 2026-09-18
type: knowledge
status: finalized
lifecycle: current
priority: high
project: 跨项目
tags: [LibraryG, 03-KNOWLEDGE, 底层框架, BettaFramework, StateMachine, 状态机, 跨项目]
source: "Packages/BettaFramework/Scripts/Runtime/SceneState/StateBase.cs + StateMachine.cs 逐文件深读（工作区版本，2026-09-18）"
verification: "类结构/方法签名为源码原文；未做运行时验证"
---

# StateMachine 状态机

> BettaFramework 的流程状态驱动基座。2 文件 / 169 行，**纯 C#、零 Unity 依赖，100% 可复刻**。

---

## 一、文件与类型

| 文件 | 关键类型 | 职责 |
|---|---|---|
| `StateBase.cs` | `StateBase`（abstract） | 状态基类：进入/执行/退出/切换 |
| `StateMachine.cs` | `StateMachine` | 状态机：注册/切换/驱动 |

---

## 二、StateBase（状态基类）

```csharp
public abstract class StateBase
{
    protected StateMachine _stateMachine;
    public int State { get; protected set; }        // 当前状态类型（子类在构造里赋值）
    private object _transitionObj = null;            // 切换传入的数据
    protected int _parentState = -1;                 // 从哪个状态切来
    protected int _toState = -1;                     // 切到哪个状态

    public void SetStateMachine(StateMachine stateMachine);   // 由 StateMachine.AddState 注入
    public void SetParentState(int parentState);
    public void SetToState(int toState);
    public void SetTransitionData(object obj);
    public void TransitionState(int stateEnum, object transitionObj = null);  // 转发 _stateMachine

    public virtual void WillEnter() {}                // 切换前钩子
    public virtual void WillExit() {}
    public abstract void OnEnter();                   // 进入（必须实现）
    public virtual void OnExecute() {}                // 执行（无参）
    public virtual void OnExecute(float deltaTime) {} // 执行（带 delta）
    public abstract void OnExit();                    // 退出（必须实现）
    public virtual void Release() {}                  // 释放

    public object TransitionObj { get; private set; }
}
```

> 语义约定：状态 A 切到 B 时调用 `_stateMachine.TransitionState(stateEnum, transitionObj)`，`transitionObj` 即传递数据。

---

## 三、StateMachine

```csharp
public class StateMachine
{
    public readonly Dictionary<int, StateBase> StateDic = new();
    public StateBase CurrentState { get; private set; }

    public void AddState(StateBase stateBase)   // StateDic.Add + SetStateMachine(this)
    public void RemoveState(int state)
    public void TryTransitionState(int stateEnum)   // 仅 WillExit + WillEnter，不切换
    public void TransitionState(int stateEnum, object transitionObj = null)
    public void OnExecute() / OnExecute(float deltaTime)
    public void OnExit()
    public void Release()
}
```

### `TransitionState`（核心切换）

```
TransitionState(stateEnum, transitionObj)
 ├─ CurrentState 非空：
 │    CurrentState.SetToState(StateDic[stateEnum].State)
 │    CurrentState.OnExit()
 │    parentState = CurrentState.State
 ├─ CurrentState = StateDic[stateEnum]
 ├─ CurrentState.SetParentState(parentState)
 ├─ CurrentState.SetTransitionData(transitionObj)
 ├─ CurrentState.OnEnter()
 └─ ExecuteCurrentState()          # 立即 OnExecute()
```

### `Release`（释放）

```
OnExit()                          # 当前状态 OnExit + 置 null
foreach StateDic.Values → state.Release()
StateDic.Clear()
```

---

## 四、复刻要点

1. **`State` 是 int 标识**（非泛型/枚举），由子类构造赋值，`StateMachine` 用 `Dictionary<int, StateBase>` 索引。
2. **切换即执行**：`TransitionState` 末尾立即 `OnExecute`，无需外部再驱动进入态；持续执行靠外部循环调 `OnExecute()` / `OnExecute(deltaTime)`。
3. **`TryTransitionState` 只做 Will 钩子**，不真正切换 —— 用于"预通知"场景。
4. **父状态追踪**：`_parentState` / `_toState` 记录切换前后，供状态内做返回/回退逻辑。
5. **零依赖**：整块可直接拷出，无任何 `using UnityEngine` 之外的耦合。

---

## 关联

- [[03-KNOWLEDGE/底层框架/BettaFramework/框架总览|框架总览]] — 本模块定位
- [[03-KNOWLEDGE/底层框架/BettaFramework/MessageDispatch-消息总线|MessageDispatch-消息总线]] — 状态切换常配合事件总线通知
