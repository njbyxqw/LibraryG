---
title: BettaSDK 总览
date: 2026-09-18
type: knowledge
status: finalized
lifecycle: current
priority: high
project: 跨项目
tags: [LibraryG, 03-KNOWLEDGE, 底层框架, BettaSDK, 跨项目]
source: "Packages/BettaSDK 工作区版本（2026-09-18）静态扫描 + 核心文件逐读 + asmdef/package.json 实测解析"
verification: "类职责/方法签名为源码原文；依赖为 asmdef/package.json 实测；未做运行时验证"
---

# BettaSDK 总览

> BettaSDK 是 Betta 框架的**能力实现层 + 第三方服务接入层**：单例基建、能力注入、第三方 SDK（Max/AppsFlyer/Firebase 等）封装、网络底座、支付桥接、玩家档案、资源加载。
> 它是 `Betta.Interface`（契约）的实现方之一、`BettaFramework`（UI/运行时）的上游。本目录按「照文档即可重建骨架」粒度整理，核心机制分册深挖，网络/支付等大体量模块只写职责与要点。

核心机制分册：
- [[03-KNOWLEDGE/底层框架/BettaSDK/启动与生命周期|启动与生命周期]]
- [[03-KNOWLEDGE/底层框架/BettaSDK/能力注入-ImplementHub|能力注入-ImplementHub]]
- [[03-KNOWLEDGE/底层框架/BettaSDK/第三方服务-ServiceHub|第三方服务-ServiceHub]]
- [[03-KNOWLEDGE/底层框架/BettaSDK/配置Schema|配置Schema]]

---

## 一、定位与体量

| 项 | 值 |
|---|---|
| UPM 包名 | `com.betta.unity.sdk` |
| asmdef 名 | `BettaSDK`（`autoReferenced: true`） |
| 命名空间 | `BettaSDK`（另有 `BettaSDK.Purchase` / `BettaSDK.Profile` 等子命名空间） |
| 自有代码体量 | 608 个 .cs ≈ 13.2 万行 |
| 内嵌第三方 | 2230 个 .cs（xasset / BestHTTP 等，见下） |
| Unity 版本 | 2022.3 |

**复刻边界**：SDK 依赖 Max / Firebase / AppsFlyer / AppleAuth / Google Play / xasset / BestHTTP 等第三方 + 内嵌源码包。这些**不可也不应复刻**，本文档只说明「接什么、怎么注册、配哪项」。

## 二、目录结构

```
BettaSDK/
├── BettaSDKRoot.cs            # 入口 MonoBehaviour（生命周期驱动）
├── BettaSDK.asmdef            # 引用 21 个程序集
├── package.json               # 依赖 6 个 UPM 包
├── Core/                      # 基础设施
│   ├── Singleton/             #   Singleton / SingletonMono
│   ├── Config/                #   BettaSDKConfig（ScriptableObject）
│   ├── Utils/                 #   UtilsTime/Device/Event/Encryption/File/Log/Timer/Zip 等
│   ├── Lattice/               #   运行时保护（DiffractionPattern/PhaseLattice/RuntimeProtectionBI）
│   ├── Protection/            #   加密混淆（BiochemistryHelix/MetabolicPathway，隐喻命名）
│   ├── PerformanceMonitor/    #   性能监测（聚合/告警/上报）
│   └── PerformanceTier/       #   性能档位
├── Hub/                       # 11 个能力 Hub（见下）
├── Service/                   # 第三方服务接入
│   ├── ServiceHub.cs          #   配置驱动 + 编译期工厂
│   ├── ServiceHub.Track*.cs   #   打点（BI）分发
│   ├── Base/                  #   ServiceBase / ServiceDefine
│   ├── Config/                #   ServiceConfig（JSON）
│   └── Services/              #   14 个第三方服务实现
├── Editor/                    # 编辑器扩展（Build/Config/Obfuz/Profile/Utils）
├── Packages/                  # 内嵌第三方源码（2230 个 .cs）
└── Tests/                     # 测试
```

## 三、11 个能力 Hub 职责速览

| Hub | 体量 | 职责 | 关键 API（节选） |
|---|---|---|---|
| `ImplementHub` | 191 行 | **能力注入容器**（接口→实现映射） | `Register<T>` / `Get<T>` / `UnRegister<T>` |
| `AdHub` | 431 行 | 广告（Max 聚合） | `Play` / `ShowBanner` / `IsReady` / `CanPlay` |
| `AudioHub` | 567 行 | 音频（2D/3D/音乐） | `PlayAudio2D` / `PlayAudio3D` / `PlayMusic` |
| `CdkHub` | 315 行 | CDK 兑换码 | `RequestRedeemGiftCode` / `IsAllowedGiftCodeFormat` |
| `HapticsHub` | 285 行 | 振动反馈（Android/iOS 分端） | `Play` / `Stop`（分端实现） |
| `PassportHub` | 1,837 行 | 登录（Apple/Google/Facebook） | `Login` / `Bind*` / `UnBind*` |
| `ProfileHub` | 4,607 行 | 玩家档案（本地+远程同步） | `GetProfile<T>` / `SaveToLocal` / `GetOrCreateProfile` |
| `PurchaseHub` | 6,411 行 | 支付（IAP/EnjoyPay/AppCharge） | `Checkout`（三方通道） |
| `ResourceHub` | 983 行 | 资源加载（xasset） | `LoadAsset<T>` / `LoadGameObject` / `LoadSprite` |
| `ServerHub` | 25,303 行 | 网络底座（HTTP + 协议 + 请求/响应） | 订单/好友/ABTest 等协议 |
| `UserHub` | 284 行 | 用户标签（AB 测试） | `Init` / `SetTag` / `GetUserTag` |

> `Social` 目录为空（0 文件），历史上预留，未落地。

## 四、依赖边界

### asmdef 引用（21 个程序集）

| 类别 | 程序集 |
|---|---|
| 本框架 | `Betta.Interface` |
| 第三方 SDK | `MaxSdk.Scripts` / `ThinkingAnalytics` / `AIHelp` / `AppsFlyer` / `AppleAuth` / `Google.Play.*` / `GoogleSignin` / `Unity.Purchasing` / `StompyRobot.SRDebugger` |
| 内嵌包 | `com.Tivadar.Best.HTTP` / `xasset` / `xasset.pad` |
| 运行时 | `HybridCLR.Runtime` / `Unity.TextMeshPro` / `Unity.Notifications.iOS/Android` / `Unity.SharpZipLib.Utils` / `Obfuz.Runtime` |

### package.json 依赖（6 个 UPM 包）

| 包 | 版本 | 用途 |
|---|---|---|
| `com.unity.nuget.newtonsoft-json` | 3.2.1 | JSON 序列化（ServiceConfig 等） |
| `com.unity.purchasing` | 5.1.2 | 内购 |
| `com.unity.mobile.notifications` | 2.4.2 | 推送 |
| `com.unity.editorcoroutines` | 1.0.0 | 编辑器协程 |
| `com.code-philosophy.hybridclr` | 8.7.0 | 热更 |
| `com.unity.sharp-zip-lib` | 1.4.0 | 压缩 |

## 五、复刻分档结论

| 模块 | 可复刻度 | 说明 |
|---|---|---|
| `Singleton` / `SingletonMono` | 100% | 无外部依赖，约 100 行 |
| `ImplementHub` | 100% | 仅依赖 `Singleton`，191 行，完整源码已录 |
| `ServiceHub` 工厂骨架 | 95% | 机制可抄，`Service*` 实体需第三方 SDK |
| `BettaSDKRoot` 生命周期 | 95% | 机制可抄，`UtilsNative`/`xasset` 需原生桥接 |
| `BettaSDKConfig` / `ServiceConfig` | 90% | 字段 schema 可抄，值需按项目填 |
| 各 Hub（Ad/Audio/CDK/...） | 索引级 | 职责+关键 API，实体依赖第三方 |
| `ServerHub` / `PurchaseHub` | 仅职责级 | 25k / 6k 行，网络协议与支付桥接不可复刻 |
| `Core/Lattice` + `Protection` | 不抄 | 反外挂/加密混淆，命名刻意隐喻化 |
