---
title: BettaSDK 第三方服务 ServiceHub
date: 2026-09-18
type: knowledge
status: finalized
lifecycle: current
priority: high
project: 跨项目
tags: [LibraryG, 03-KNOWLEDGE, 底层框架, BettaSDK, 跨项目]
source: "Packages/BettaSDK/Service/ServiceHub*.cs、Service/Base/*.cs、Service/Config/*.cs 完整源码逐读（工作区版本，2026-09-18）"
verification: "代码片段为源码原文；机制为源码推导；未做运行时验证"
---

# 第三方服务 ServiceHub

> `ServiceHub` 是**第三方服务（广告/统计/登录/推送）的统一接入骨架**：配置驱动 + 编译期显式工厂，把 Max / AppsFlyer / Firebase / Facebook / Google / AIHelp / ThinkingAnalytics 等包装成统一的 `ServiceBase`。
> 核心特点：**不用反射**，靠 `ServiceDefine` 常量名 + `switch` 显式 `new`，接入一个新服务要同时改「配置类 + 工厂分支」。

---

## 一、服务基类 ServiceBase

```csharp
public abstract class ServiceBase
{
    private ServiceConfigBase _config;
    public string Name => _config != null ? _config.name : GetType().Name;
    public bool Initialise;
    public bool LogEnable;

    public virtual void Init() {}
    public virtual void Init(ServiceConfigBase config) { _config = config; }
    public virtual void Start() {}
    public virtual void Update(float timeDelta) {}
    public virtual void Release() {}

    protected void L(string str, params object[] args) { if (!LogEnable) return; UtilsLog.L($"[{Name}]{str}", args); }
    protected void W(string str, params object[] args) { if (!LogEnable) return; UtilsLog.W($"[{Name}]{str}", args); }
    protected void E(string str, params object[] args) { if (!LogEnable) return; UtilsLog.E($"[{Name}]{str}", args); }
}
```

生命周期钩子：`Init`（建连）→ `Start`（启动，可后置）→ `Update`（帧驱动）→ `Release`（释放）。

## 二、服务身份常量 ServiceDefine

```csharp
public static class ServiceDefine
{
    public const string Admob = "Admob";        // 备用广告渠道（当前主力是 Max）
    public const string Adjust = "Adjust";
    public const string AppsFlyer = "AppsFlyer";
    public const string Facebook = "Facebook";
    public const string Firebase = "Firebase";
    public const string Max = "Max";            // 广告聚合
    public const string MSSDK = "MSSDK";
    public const string Apple = "Apple";        // Apple 登录
    public const string Google = "Google";      // Google 登录
    public const string GoogleGame = "GoogleGame";
    public const string Apt = "AndroidPerformanceTuner";
    public const string AIHelp = "AIHelp";
    public const string TA = "ThinkingAnalytics"; // BI 打点
    public const string TASDK = "TASDK";
}
```

### 错误码与登录信息

```csharp
public static class ServiceError   // 统一错误码
{
    Success = 0, HasInProgress = 1, NetworkError = 2, UserCanceled = 3,
    ParameterError = 4, Unknown = 5, PluginMalformed = 6, NotSupported = 7,
    ChannelError = 8, NotInitialize = 9, NotLogin = 10, TokenExpired = 11,
    TargetNotFound = 12, Delayed = 13, NotReady = 14, AppleCredentialsRevoked = 15,
}

public static class ServicePermission  // 权限位
{ LoginToken = 1, BaseInfo = 2, Publish = 3, FriendList = 4 }

public class ServiceErrorInfo { int ErrorNumber; int ErrorCode; string ErrorMessage; }
public class ServiceLoginInfo { Id/Name/Token/Code/Email/Status/Permissions/TokenApple/CodeApple; }
```

## 三、配置 Schema（ServiceConfig）

`ServiceConfig` 是 JSON 资源（`Resources/Config/ServiceConfig`），加载后解密反序列化：

```csharp
public class ServiceConfig
{
    public const string ResPath = "Config/ServiceConfig";
    public static ServiceConfig Instance => _instance ??= Load();

    public static ServiceConfig Load()
    {
        var textAsset = Resources.Load<TextAsset>(ResPath);
        if (textAsset == null || string.IsNullOrEmpty(textAsset.text)) return null;
        var json = UtilsEncryption.DecodeString(textAsset.text);
        return JsonConvert.DeserializeObject<ServiceConfig>(json);
    }

    public ServiceConfigAdmob Admob;
    public ServiceConfigAppsFlyer AppsFlyer;
    public ServiceConfigTA TA;
    public ServiceConfigFirebase Firebase;
    public ServiceConfigFacebook Facebook;
    public ServiceConfigGoogle Google;
    public ServiceConfigGoogleGame GoogleGame;
    public ServiceConfigMax Max;
    public ServiceConfigAIHelp AIHelp;
    public ServiceConfigApt Apt;

    public Dictionary<string, ServiceConfigBase> Configs = new();
    public void Init()
    {
        Configs.Clear();
        _initConfig(Admob); _initConfig(AppsFlyer); _initConfig(TA);
        _initConfig(Firebase); _initConfig(Facebook); _initConfig(Google);
        _initConfig(GoogleGame); _initConfig(Max); _initConfig(AIHelp); _initConfig(Apt);
    }

    private void _initConfig(ServiceConfigBase config)
    {
        if (config == null) return;
        if (!config.isUse) return;                    // isUse=false 直接跳过
        if (string.IsNullOrEmpty(config.name)) { UtilsLog.W(...); return; }
        if (Configs.ContainsKey(config.name)) { Configs[config.name] = config; return; }
        Configs.Add(config.name, config);
    }
}
```

每个服务配置类都继承 `ServiceConfigBase { string name; bool isUse = true; }`，构造函数里写死 `name = ServiceDefine.Xxx`。

> 完整字段清单见 [[03-KNOWLEDGE/底层框架/BettaSDK/配置Schema|配置Schema]]。

## 四、工厂机制（ServiceHub.Init）

```csharp
public partial class ServiceHub : Singleton<ServiceHub>
{
    private readonly List<ServiceBase> _services = new();

    private T CreateService<T>(ServiceConfigBase config) where T : ServiceBase, new()
    {
        var service = new T();
        if (config == null) service.Init();
        else service.Init(config);
        _services.Add(service);
        if (service is IServiceTrack configData) _servicesData.Add(configData);  // 打点服务单列
        return service;
    }

    public void Init()
    {
        if (_initialized) return;
        _initialized = true;
        try { CultureInfo.DefaultThreadCurrentCulture = new CultureInfo("en", false); ServiceConfig.Instance.Init(); }
        catch (Exception ex) { UtilsLog.E("exceptions :" + ex.StackTrace); }

        foreach (var kv in ServiceConfig.Instance.Configs)
        {
            switch (kv.Key)
            {
                case ServiceDefine.AppsFlyer:  ServiceAppsFlyer = CreateService<ServiceAppsFlyer>(kv.Value); break;
                case ServiceDefine.Firebase:   ServiceFirebase = CreateService<ServiceFirebase>(kv.Value); break;
                case ServiceDefine.Max:        ServiceMax = CreateService<ServiceMax>(kv.Value); break;
                case ServiceDefine.TA:         ServiceThinkingAnalytics = CreateService<ServiceThinkingAnalytics>(kv.Value); break;
                case ServiceDefine.Facebook:   ServiceFacebook = CreateService<ServiceFacebook>(kv.Value); break;
#if PASSPORT_GOOGLE
                case ServiceDefine.Google:     ServiceGoogle = CreateService<ServiceGoogle>(kv.Value); break;
#endif
                case ServiceDefine.AIHelp:     ServiceAIHelp = CreateService<ServiceAIHelp>(kv.Value); break;
            }
        }

        try
        {
#if PASSPORT_APPLE
            if (ServiceApple.GetIOSAddSignInWithAppleState())
                ServiceApple = CreateService<ServiceApple>(null);
#endif
            ServiceDeepLink = CreateService<ServiceDeepLink>(null);
            ServiceGooglePlay = CreateService<ServiceGooglePlay>(null);
#if GameCenter || GoogleGameService
            ServiceGameService = CreateService<ServiceGameService>(null);
#endif
        }
        catch (Exception e) { UtilsLog.E($"Service initialise failed:" + e.StackTrace); throw; }

        ServiceMax?.Start();   // 等所有服务 Init 完，Max 最后启动

        // 预埋公共 BI 属性
        UserSetOnce(new Dictionary<string, object> { ["app_version_first"] = UtilsNative.GetAppVersionName() });
        UserSetOnce(new Dictionary<string, object> { ["app_build_first"] = UtilsNative.GetAppVersionCode() });
        UserSet(new Dictionary<string, object> { ["device_id"] = UtilsDevice.GetDeviceUniqueId() });
        UserSet(new Dictionary<string, object> { ["client_os"] = UtilsNative.Platform });
        UserSet(new Dictionary<string, object> { ["app_version"] = UtilsNative.GetAppVersionName() });
        UserSet(new Dictionary<string, object> { ["app_build"] = UtilsNative.GetAppVersionCode() });
        SetSuperProperties(new Dictionary<string, object> { ["app_build"] = UtilsNative.GetAppVersionCode() });

        Best.HTTP.Shared.HTTPManager.UserAgent = UtilsDevice.GetUserAgent();
        UtilsTimer.Instance.AddDelegate(Update);   // 挂进帧循环
    }

    private void Update(float timeDelta)
    {
        foreach (var service in _services) service.Update(timeDelta);
    }
}
```

### 复刻要点

1. **编译期显式工厂，非反射** —— 新服务要同时改 `ServiceConfig`（加字段+`_initConfig`）+ `switch` 加分支 + 建 `Service*` 类。这是有意为之（可读性 + 裁剪性，宏可去掉某渠道）。
2. **`CultureInfo("en")` 兜底** —— 防服务器交互受本地文化差异影响（小数点/日期格式）。
3. **`ServiceMax.Start()` 延后** —— Max 聚合依赖其他服务先就绪。
4. **`IServiceTrack` 单列到 `_servicesData`** —— 打点服务与普通服务分开，供 `TrackEvent` 广播。

## 五、打点分发（BI）

`ServiceHub.TrackBase.cs` 是打点（BI）统一入口，`_servicesData` 里的服务（实现 `IServiceTrack`）收到广播：

```csharp
public interface IServiceTrack
{
    string GetTrackID();
    void Track(string eventId, Dictionary<string, object> dict = null);
    void TrackAdRevenue(double revenue, string revenuePrecision, string network = null, ...);
    void TrackPurchase(PurchasePlatformType channel, decimal price, string currency, string productId, ...);
}
```

| 方法 | 分发对象 |
|---|---|
| `TrackEvent`（非市场打点） | Firebase + ThinkingAnalytics |
| `TrackEventMarket`（市场打点） | AppsFlyer + Facebook + Firebase |
| `UserAdd` / `UserSet` / `UserSetOnce` / `SetSuperProperties` | ThinkingAnalytics |
| `TrackAdRevenue` / `TrackPurchase` | 遍历 `_servicesData` 广播 |

> `SetCustomEventFieldsProvider` / `BuildEventFields` 是打点字段扩展点：业务层可注册 `Func<string, Dictionary<string,object>>` 按事件名注入自定义字段。

## 六、14 个 Service 实现

`Service/Services/` 下每个服务一个子目录：

| Service | 职责 | 对应第三方 |
|---|---|---|
| `ServiceMax` | 广告聚合 | AppLovin Max |
| `ServiceAppsFlyer` | 归因/市场打点 | AppsFlyer |
| `ServiceFirebase` | 打点/推送 | Firebase |
| `ServiceThinkingAnalytics` | BI 打点 | ThinkingAnalytics |
| `ServiceFacebook` | 登录/分享 | Facebook |
| `ServiceGoogle` | Google 登录 | Google Sign-In |
| `ServiceGooglePlay` | Google Play 服务 | Google Play |
| `ServiceGameService` | 成就/排行榜 | GameCenter / Google Play Games |
| `ServiceApple` | Apple 登录 | Sign in with Apple |
| `ServiceAIHelp` | 客服/社区 | AIHelp |
| `ServiceDeepLink` | 深链 | — |
| `ServiceNotifications` | 推送 | Unity Notifications |
| `ServiceBetta` | 自定义服务 | 内部 |
| `ServiceAppsFlyer` 之外的 `ServiceAdmob` 等 | 备用渠道 | — |

> 每个 `Service*` 的骨架一致：`new` → `Init(config)` 读配置建连 → 暴露给 Hub 调用。业务层通常不直接碰 `Service*`，而是通过对应 Hub（`AdHub`/`PassportHub`）间接使用。
