---
title: BettaSDK 配置 Schema
date: 2026-09-18
type: knowledge
status: finalized
lifecycle: current
priority: high
project: 跨项目
tags: [LibraryG, 03-KNOWLEDGE, 底层框架, BettaSDK, 跨项目]
source: "Packages/BettaSDK/Core/Config/BettaSDKConfig.cs、Service/Config/ServiceConfig.cs 完整源码逐读（工作区版本，2026-09-18）"
verification: "字段清单为源码原文；未做运行时验证"
---

# BettaSDK 配置 Schema

> SDK 有两套配置：`BettaSDKConfig`（ScriptableObject，进 `Resources/Config/BettaSDKConfig`）和 `ServiceConfig`（JSON，进 `Resources/Config/ServiceConfig`）。
> 前者管 SDK 全局（版本/API/加密/支付/性能/平台），后者管第三方服务（各渠道 key/id/placement）。

---

## 一、BettaSDKConfig（ScriptableObject）

`[CreateAssetMenu(menuName = "Betta/BettaSDKConfig")]`，单例从 `Resources.Load<BettaSDKConfig>("Config/BettaSDKConfig")` 读。

### 基础

| 字段 | 类型 | 说明 |
|---|---|---|
| `version` | `VersionStatus` | RELEASE=0 / DEBUG=1，**切换整套配置环境的总开关** |
| `uiResourceVariant` | `UIResourceVariant` | Auto=0 / Phone=1 / Pad=2，UI 资源变体 |
| `AppId` | `string`（只读） | 按平台返回 `appIdAndroid` / `appIdIOS` |
| `APIUrl` | `string`（只读） | 按 version 返回 `apiUrlRelease` / `apiUrlDebug` |
| `APISecret` | `string` | 按 version 读写 |
| `APITimeout` | `int` | 按 version，默认 15s |
| `ResUrl` | `string`（只读） | 按 version |
| `BuildAppBundle` | `bool`（只读） | 按 version 返回是否打 AppBundle |

### Server（Release / Debug 各一份）

| 字段 | 类型 |
|---|---|
| `appIdAndroid` / `appIdIOS` | string |
| `apiUrlRelease` / `apiSecretRelease` / `apiTimeoutRelease` / `resUrlRelease` | string/string/int/string |
| `apiUrlDebug` / `apiSecretDebug`（默认 `"foobar"`）/ `apiTimeoutDebug` / `resUrlDebug` | string/string/int/string |

### 广告

| 字段 | 类型 | 默认 |
|---|---|---|
| `AdRewarded` | bool | true |
| `AdInterstitial` | bool | true |
| `AdBanner` | bool | false |
| `EnableAppsFlyerUDL` | bool | true（AppsFlyer 统一深链） |

### 支付

| 字段 | 类型 |
|---|---|
| `supportedPurchaseChannelType` | `SupportedPlatformType` |
| `enjoyPayConfig` | `EnjoyPayConfig` |
| `appchargeConfig` | `AppchargeConfig` |

### 加密 / 保护

| 字段 | 类型 | 默认 |
|---|---|---|
| `EncryptKey` | string | 16 位加密 key |
| `EnableDllProtection` | bool | true（HybridCLR DLL 加密） |
| `EnableMetadataProtection` | bool | true（IL2CPP Metadata 加密） |
| `EnableRuntimeProtection` | bool | true（运行时保护） |
| `EnablePerformanceMonitor` | bool | false（性能监测） |

### Android / iOS 平台

| 字段 | 类型 | 说明 |
|---|---|---|
| `AndroidKeyStoreUseConfiguration` / `Path` / `Pass` / `Alias` / `AliasPass` | bool/string… | Android 签名配置 |
| `DebugBuildAppBundle` / `ReleaseBuildAppBundle` | bool | 是否打 AppBundle |
| `iOSAddPushNotification` / `iOSAddSignInWithApple` / `iOSAddGameCenter` | bool | iOS Capabilities |
| `iOSAppUsesNonExemptEncryption` | bool | 写 Info.plist `ITSAppUsesNonExemptEncryption` |

### Facebook 权限 / URL

| 字段 | 类型 | 默认 |
|---|---|---|
| `kUserPermissionLoginToken` | bool | true |
| `kUserPermissionBasicInfo` | bool | true |
| `kUserPermissionPublish` | bool | false |
| `kUserPermissionFriendList` | bool | false |
| `EmailURL` / `AppStore` / `GooglePlay` / `PrivacyPolicyURL` / `TermofUseURL` | string | 各类 URL |

### 其他

| 字段 | 类型 | 说明 |
|---|---|---|
| `HotUpdates` | `string[]`（`[HideInInspector]`） | 热更列表 |
| `TrackingDescriptions` | `StringPair[]` | iOS 追踪权限文案 |
| `ModuleInfos` | `ModuleInfo[]` | 模块信息（Macro/Debug/Release/AsmDef/AsmRef/File/Directory） |

## 二、支付子配置

### EnjoyPayConfig

| 字段 | 类型 |
|---|---|
| `merchantsIdDev` / `appIdDev` / `privateKeyDev` | string |
| `merchantsIdRelease` / `appIdRelease` / `privateKeyRelease` | string |
| `androidAvailableCountryCode` / `iOSAvailableCountryCode` | `string[]`（ISO 3166-1 alpha-2，如 `["RU","KZ"]`） |
| `clientReturnUrl` | string |

### AppchargeConfig

| 字段 | 类型 |
|---|---|
| 沙盒：`urlSandBox` / `mainKeySandBox` / `publisherTokenSandBox` / `checkoutPublicKeySandBox` / 国家码数组 / `clientReturnUrlSandBox` | string/string[] |
| 正式：`url` / `mainKey` / `publisherToken` / `checkoutPublicKey` / 国家码数组 / `clientReturnUrl` | string/string[] |
| `unsupportedMaxConfigPrice` | float（默认 0.8，≤ 该值的商品不算 AppCharge 支持商品） |

### ModuleInfo

| 字段 | 类型 |
|---|---|
| `Macro` | string（关联宏） |
| `Debug` / `Release` | bool |
| `AsmDef` | string |
| `AsmRef` | `string[]` |
| `File` / `Directory` | `string[]` |

## 三、ServiceConfig（JSON）

`Resources/Config/ServiceConfig`，加载后 `UtilsEncryption.DecodeString` 解密 → `JsonConvert.DeserializeObject`。

基类：`ServiceConfigBase { string name; bool isUse = true; }`，`isUse=false` 跳过该服务。

| 配置类 | name 常量 | 字段 |
|---|---|---|
| `ServiceConfigAdmob` | `Admob` | `appIdIOS` / `appIdAndroid` |
| `ServiceConfigMax` | `Max` | `appId` / `interstitialPlaceIOS·Android` / `rewardedPlaceIOS·Android` / `bannerPlaceIOS·Android` |
| `ServiceConfigAppsFlyer` | `AppsFlyer` | `devKey` / `iOSAppID` / `purchaseId` / `roi360` |
| `ServiceConfigFacebook` | `Facebook` | `appId` / `clientToken` |
| `ServiceConfigGoogle` | `Google` | `clientIdAndroid` / `clientIdReleaseAndroid` / `clientIdIOS` / `webClientId` |
| `ServiceConfigGoogleGame` | `GoogleGame` | `appId` |
| `ServiceConfigAIHelp` | `AIHelp` | `appId` / `domain` / `appIdIOS` / `appIdAndroid` |
| `ServiceConfigTA` | `TA` | `appId` / `appIdRelease` / `serverUrl` |
| `ServiceConfigFirebase` | `Firebase` | （无额外字段） |
| `ServiceConfigApt` | `Apt` | `appId` |

## 四、复刻要点

1. **两套配置职责分明**：`BettaSDKConfig` = SDK 自己（版本/加密/性能），`ServiceConfig` = 第三方渠道（key/id）。
2. **`version` 是环境总开关** —— 一个 `VersionStatus` 切全部 Release/Debug 配置，业务层取配置时统一走 `Instance.APIUrl` 这类只读属性，不直接摸字段。
3. **`ServiceConfig` 是加密 JSON** —— 落盘前用 `UtilsEncryption` 编码，读时 `DecodeString`。复刻时若不需要加密，可省去这步直接读明文 JSON。
4. **字段都有 `#if DEBUG || DEVELOPMENT_BUILD` 的 Header 标注** —— 正式构建里这些 Header 不显示，纯编辑器可读性优化，不影响序列化。
