---
title: BettaSDK 能力注入 ImplementHub
date: 2026-09-18
type: knowledge
status: finalized
lifecycle: current
priority: high
project: 跨项目
tags: [LibraryG, 03-KNOWLEDGE, 底层框架, BettaSDK, 跨项目]
source: "Packages/BettaSDK/Hub/Implement/ImplementHub.cs 完整源码逐读（工作区版本，2026-09-18）"
verification: "代码为源码原文，可 100% 复刻；仅依赖 Singleton 基类"
---

# 能力注入 ImplementHub

> `ImplementHub` 是 BettaSDK 的**依赖注入容器**：把 `Betta.Interface` 里定义的接口，映射到具体实现，业务层通过 `Get<T>()` 取用。
> 它是 `Interface.ImplementManager.IImplementManager` 的唯一实现，仅依赖 `Singleton` 基类，191 行，**可 100% 复刻**。

---

## 一、核心设计

- 用 `Dictionary<Type, ImplementationBucket>` 存「接口类型 → 实现桶」。
- 每个 `ImplementationBucket` 分**两个槽**：
  - **default 槽**：无名字的默认实现（最多一个）。
  - **named 槽**：`Dictionary<string, object>` 具名实现（`StringComparer.Ordinal` 精确匹配，可多个）。
- 复刻要点：**default 与 named 互斥于同一个接口的注册语义**，重复注册直接抛异常，不做静默覆盖。

## 二、完整源码

```csharp
using System;
using System.Collections.Generic;
using Interface.ImplementManager;

namespace BettaSDK
{
    public sealed class ImplementHub : Singleton<ImplementHub>, IImplementManager
    {
        private sealed class ImplementationBucket
        {
            public object DefaultImplementation;
            public bool HasDefaultImplementation;
            public Dictionary<string, object> NamedImplementations;

            public bool TryGet(string name, out object implementation)
            {
                implementation = null;

                if (string.IsNullOrEmpty(name))
                {
                    if (!HasDefaultImplementation) return false;
                    implementation = DefaultImplementation;
                    return implementation != null;
                }

                if (NamedImplementations == null) return false;
                return NamedImplementations.TryGetValue(name, out implementation) && implementation != null;
            }

            public bool HasAny()
            {
                return HasDefaultImplementation || (NamedImplementations != null && NamedImplementations.Count > 0);
            }
        }

        private readonly Dictionary<Type, ImplementationBucket> _implementations = new();
        private bool _initialized;

        protected override void InitFirst()
        {
            if (_initialized) return;
            _initialized = true;
        }

        protected override void OnDestroy()
        {
            _implementations.Clear();
            _initialized = false;
        }

        public T Get<T>() where T : class
        {
            if (!TryGet<T>(out var implementation)) return null;
            return implementation;
        }

        public bool TryGet<T>(out T implementation, string name = "") where T : class
        {
            implementation = null;
            var type = typeof(T);
            if (!_implementations.TryGetValue(type, out var bucket) || bucket == null) return false;
            if (!bucket.TryGet(name, out var impl)) return false;
            implementation = (T)impl;
            return implementation != null;
        }

        public bool IsRegistered<T>() where T : class
        {
            var type = typeof(T);
            return _implementations.TryGetValue(type, out var bucket) && bucket != null && bucket.HasAny();
        }

        public void Register<TInterface>(TInterface instance, string name = "") where TInterface : class
        {
            if (instance == null)
                throw new ArgumentNullException(nameof(instance),
                    $"Cannot register null implementation for {typeof(TInterface).Name}");

            var interfaceType = typeof(TInterface);

            if (!_implementations.TryGetValue(interfaceType, out var bucket) || bucket == null)
            {
                bucket = new ImplementationBucket();
                _implementations.Add(interfaceType, bucket);
            }

            if (string.IsNullOrEmpty(name))
            {
                if (bucket.HasDefaultImplementation)
                    throw new InvalidOperationException(
                        $"Default implementation for {interfaceType.Name} is already registered.");
                bucket.DefaultImplementation = instance;
                bucket.HasDefaultImplementation = true;
                return;
            }

            if (bucket.NamedImplementations == null)
                bucket.NamedImplementations = new Dictionary<string, object>(StringComparer.Ordinal);

            if (!bucket.NamedImplementations.TryAdd(name, instance))
                throw new InvalidOperationException(
                    $"Named implementation '{name}' for {interfaceType.Name} is already registered.");
        }

        public void UnRegister<T>(T instance) where T : class
        {
            if (instance == null)
                throw new ArgumentNullException(nameof(instance),
                    $"Cannot unregister null implementation for {typeof(T).Name}");

            var interfaceType = typeof(T);

            if (!_implementations.TryGetValue(interfaceType, out var bucket) || bucket == null)
                throw new InvalidOperationException(
                    $"Implementation for {interfaceType.Name} is already unregistered.");

            var removed = false;
            if (bucket.HasDefaultImplementation && ReferenceEquals(bucket.DefaultImplementation, instance))
            {
                bucket.DefaultImplementation = null;
                bucket.HasDefaultImplementation = false;
                removed = true;
            }
            else if (bucket.NamedImplementations != null)
            {
                string keyToRemove = null;
                foreach (var pair in bucket.NamedImplementations)
                {
                    if (!ReferenceEquals(pair.Value, instance)) continue;
                    keyToRemove = pair.Key;
                    removed = true;
                    break;
                }
                if (removed) bucket.NamedImplementations.Remove(keyToRemove);
            }

            if (!removed)
                throw new InvalidOperationException(
                    $"Implementation for {interfaceType.Name} is already unregistered.");

            if (!bucket.HasAny()) _implementations.Remove(interfaceType);
        }
    }
}
```

## 三、使用三铁律

| 铁律 | 说明 |
|---|---|
| 先注册后取用 | `Get<T>()` 取不到时返回 `null`（不抛异常），调用方必须判空 |
| default 唯一 | 同一接口 default 实现只能注册一个，重复注册抛 `InvalidOperationException` |
| named 精确匹配 | 具名实现用 `StringComparer.Ordinal`，大小写敏感 |

```csharp
// 注册（实现方，通常集中在模块初始化处）
ImplementHub.Instance.Register<IAudioSystem>(new AudioSystemImpl());
ImplementHub.Instance.Register<IAudioSystem>(new AudioSystemPadImpl(), "pad"); // 具名

// 取用（业务方）
var audio = ImplementHub.Instance.Get<IAudioSystem>();
var padAudio = ImplementHub.Instance.Get<IAudioSystem>();      // 仍是 default
var padAudio2 = ImplementHub.Instance.TryGet<IAudioSystem>(out var a, "pad"); // 取具名
```

## 四、复刻要点

1. **泛型约束 `where T : class`** —— 只收引用类型，接口天然满足。
2. **`Singleton<T>` 基类**要求 `T : new()`，`ImplementHub` 有 public 无参构造，满足。
3. **`UnRegister` 用 `ReferenceEquals`** 按引用匹配，不是 `Equals`，避免被重载的相等比较干扰。
4. **桶为空时整体移除** —— 反注册最后一个实现后，接口类型从字典删除，`IsRegistered` 返回 false。
5. 若脱离 `Singleton` 单独复刻，只需把 `InitFirst`/`OnDestroy` 换成普通构造/析构即可。
