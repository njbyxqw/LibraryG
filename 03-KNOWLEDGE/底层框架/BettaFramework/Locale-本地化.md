---
title: Locale 本地化
date: 2026-09-18
type: knowledge
status: finalized
lifecycle: current
priority: high
project: 跨项目
tags: [LibraryG, 03-KNOWLEDGE, 底层框架, BettaFramework, Locale, 本地化, 跨项目]
source: "Packages/BettaFramework/Scripts/Runtime/Locale/*.cs 全部 4 文件逐文件深读（工作区版本，2026-09-18）"
verification: "类结构/方法签名/语言表为源码原文；加载链路为源码阅读推断；未做运行时验证"
---

# Locale 本地化

> BettaFramework 的本地化系统：语言表 → 资源加载（JSON/Protobuf 双格式）→ 运行时切换 → 字体/材质分发。
> 4 文件 / 651 行。复刻度约 95%（依赖 BettaSDK 的 `ResourceHub` / `UtilsEncryption` / `UtilsLog`，以及 Newtonsoft / ProtoBuf）。

---

## 一、文件与类型

| 文件 | 关键类型 | 职责 |
|---|---|---|
| `Locale.cs` | `Locale`（static）、`LanguageInfo`、`IOnLocaleRegionChange` | 语言码表 + 资源定位 + 资产加载 |
| `LocaleManager.cs` | `LocaleManager`（static）、`EventLocaleChanged` | 运行时管理器：切换/缓存/字体 |
| `LocaleAsset.cs` | `LocaleAsset` | 词条缓冲（JSON / Proto 双构造） |
| `LocaleStringRow.cs` | `LocaleStringRow` | Protobuf 词条契约 |

---

## 二、语言码表（`Locale.Languages`）

```csharp
public class LanguageInfo
{
    public SystemLanguage Language;   // Unity 枚举
    public readonly string Describe;   // 显示名
    public readonly string Code;       // ISO 通用
    public readonly string CodeIOS;    // iOS
    public readonly string CodeAndroid;// Android
    public LanguageInfo(SystemLanguage l, string c, string ci, string ca, string d) { ... }
}
```

支持 18 种语言（`Dictionary<SystemLanguage, LanguageInfo>`）：

| SystemLanguage | Code | iOS | Android | 描述 |
|---|---|---|---|---|
| Chinese / ChineseSimplified | `zh` | `zh-Hans` | `zh-rCN` | 简体中文 |
| ChineseTraditional | `zht` | `zh-Hant` | `zh-rTW` | 繁體中文 |
| English | `en` | `en` | `en` | English |
| Dutch | `nl` | `nl` | `nl` | Nederlands |
| French | `fr` | `fr` | `fr` | Français |
| German | `de` | `de` | `de` | Deutsch |
| Indonesian | `id` | `id` | `in` | Bahasa Indonesia |
| Italian | `it` | `it` | `it` | Italiano |
| Japanese | `ja` | `ja` | `ja` | 日本語 |
| Korean | `ko` | `ko` | `ko` | 한국어 |
| Portuguese | `pt` | `pt` | `pt-rBR` | Português |
| Russian | `ru` | `ru` | `ru` | Русский |
| Spanish | `es` | `es` | `es` | Español |
| Thai | `th` | `th` | `th` | ภาษาไทย |
| Turkish | `tr` | `tr` | `tr` | Türkçe |
| Vietnamese | `vi` | `vi` | `vi` | Tiếng Việt |
| Faroese | `fa` | `fa` | `fa` | فارسی |

> `GetLanguageInfo` 对未登记语言回退 `LanguageDefault`（`English`）。`LanguageDefault = SystemLanguage.English`。

### 支持语言集合

```csharp
public static readonly List<SystemLanguage> Supported = new();
public static void Init(List<SystemLanguage> supportedLanguages);  // 去重填充
public static bool IsSupport(SystemLanguage language);
```

---

## 三、Locale（资源定位与加载）

```csharp
public static class Locale
{
    public const string GroupLoading = "loading";   // 预置分组常量
    public const string GroupMain    = "main";

    public static string GetLanguageCode(SystemLanguage language);  // 取 Code
    public static string GetLanguageDesc(SystemLanguage language);  // 取描述
    public static LocaleAsset LoadAsset(string region, string group);
}
```

### `LoadLocaleTextAsset`（资源定位规则）

| 情况 | 路径 |
|---|---|
| `groupInfo.buildIn`（内置） | 从 `groupInfo.path` 拆出 `Resources/` 之后的部分，`Resources.Load<TextAsset>($"{basePath}/{region}")`（无扩展名逻辑路径） |
| 非内置 + JSON | `ResourceHub.LoadAsset<TextAsset>($"{groupInfo.path}/{region}{.json}")` |
| 非内置 + Protobuf | `ResourceHub.LoadAsset<TextAsset>($"{groupInfo.path}/{region}{.bytes}")` |

> 扩展名由 `ConfigRuntimeConst.RuntimeFormat`（`ConfigDataFormat.Json` / `ProtobufNet`）决定；`ConfigRuntimeConst` 是 const，编译器折叠分支，保留双路径以便改常量后重编可用。

### `LoadAsset` 处理分支

```
LoadLocaleTextAsset → null 则返回 null
  ├─ ProtobufNet 格式 → 读 ta.bytes → new LocaleAsset(bytes)
  └─ JSON 格式 → ta.text；若 groupInfo.encrypt → UtilsEncryption.DecodeString(text)
                  → new LocaleAsset(text)
```

---

## 四、LocaleAsset（词条缓冲）

```csharp
public class LocaleAsset
{
    private class Node { public string key; public string value; }   // JSON 中间结构
    private readonly Dictionary<string, string> _buffer = new();

    public LocaleAsset(string json);        // JSON：List<Node> 反序列化 → _buffer
    public LocaleAsset(byte[] protoBytes);  // Proto：List<LocaleStringRow> 反序列化 → _buffer
    public bool TryGetValue(string key, out string text);
    public void Release();                  // _buffer.Clear()
}
```

- JSON 反序列化用 `Newtonsoft.Json.JsonConvert.DeserializeObject<List<Node>>`
- Proto 用 `ProtoBuf.Serializer.Deserialize<List<LocaleStringRow>>`
- 重复 key 会 `Debug.LogError($"key repeated:{kv.key}")`，但**后写覆盖前值**（`_buffer[kv.key] = kv.value`）

---

## 五、LocaleStringRow（Protobuf 契约）

```csharp
[ProtoContract]
public sealed class LocaleStringRow
{
    [ProtoMember(1)] public string Key { get; set; }
    [ProtoMember(2)] public string Value { get; set; }
}
```

> 这是词条表的 Protobuf 序列化契约，与 JSON 的 `{key,value}` 结构一一对应。

---

## 六、LocaleManager（运行时管理器）

```csharp
public static class LocaleManager
{
    private const string CacheKey = "locale_region";     // PlayerPrefs 缓存键
    private static readonly Dictionary<SystemLanguage, Dictionary<string, LocaleAsset>> TextDict;   // 语言 → 分组 → 资产
    private static readonly List<IOnLocaleRegionChange> ActiveComponents;                            // 切换时刷新的组件
    private static readonly Dictionary<string, Material> CacheMaterials;
    private static readonly Dictionary<SystemLanguage, TMP_FontAsset> CacheFonts;
    private static SystemLanguage _language = Locale.LanguageDefault;
    public static SystemLanguage Language { get; set; }  // 编辑器非 Play 态返回 English

    public static void Init();                           // 读配置 → 决定初始语言 → 加载 buildIn 分组
    public static bool SetLanguage(SystemLanguage);      // 切换
    public static bool LoadConfig(SystemLanguage, string group);
    public static void UnLoadConfig(SystemLanguage, string group = default);
    public static bool HasKey(string key, string group = "main", SystemLanguage language = Unknown);
    public static string GetText(string key, string group = "main", SystemLanguage language = Unknown);
    public static TMP_FontAsset GetFont();
    public static Material GetFontMaterial(string material, string suffix = "");
    public static void Register(IOnLocaleRegionChange) / UnRegister(IOnLocaleRegionChange);
}
```

### Init 流程

```
Locale.Init(config.languages)                       # 填 Supported
PlayerPrefs 有 cache → TryParse → MatchLanguage(cache)
无 cache             → MatchLanguage(primaryLanguage==Unknown ? systemLanguage : primaryLanguage)
PlayerPrefs.SetString(CacheKey, Language)
遍历 config.localeGroups，buildIn 的 → LoadConfig(Language, name)
```

`MatchLanguage`：`IsSupport(language)` 则返回，否则回退 `LanguageDefault`。

### SetLanguage（切换）流程

```
Language == language → return false（已加载）
!IsSupport → return false
遍历当前语言的 TextDict 分组 → LoadConfig(newLanguage, group)（失败即中断 return false）
UnLoadConfig(oldLanguage)
Language = newLanguage
PlayerPrefs.SetString(CacheKey, ...)
遍历 ActiveComponents → OnLocaleRegionChange()
UtilsEvent.Send(new EventLocaleChanged(language))    # BettaSDK 事件
```

> `EventLocaleChanged` 是 `readonly struct : IEvent`（BettaSDK 事件契约），供全局订阅语言变更。

### GetText（核心取值）

```
language==Unknown → language = Language
text = $"{code}_{group}_{key}"                       # 默认返回（未命中时的兜底标识）
TextDict[language][group] 未命中 → UNITY_EDITOR 非 Play 态惰性 LoadConfig
cfg.TryGetValue(key, out t) → text = t
return text.Replace("\\n", "\n")                     # 转义换行还原
```

> **编辑器非 Play 态**会惰性 `LoadConfig` 兜底（保证 Inspector 预览可见）；Play 态未命中直接返回 `{code}_{group}_{key}` 兜底串。

### 字体 / 材质分发

```
GetFont(): CacheFonts 缓存，Resources.Load<TMP_FontAsset>($"Fonts/{code}/{code}")
GetFontMaterial(material, suffix=""):
   material 空 → GetFont().material
   materialFullName = $"{code}-{material}{suffix}"  → 缓存/加载
   失败回退 → Resources.Load($"Fonts/{code}/{code}-{material}")
   再失败 → GetFont().material
```

---

## 七、配置（BettaFrameworkConfig 侧）

```csharp
public SystemLanguage primaryLanguage = SystemLanguage.Unknown;   // 主语言（Unknown=跟随系统）
public List<SystemLanguage> languages = new() { SystemLanguage.English };
public LocaleGroupInfo[] localeGroups;                            // 分组配置

[Serializable]
public class LocaleGroupInfo
{
    public bool buildIn;        // 是否内置（Resources 加载）
    public bool encrypt;        // 是否加密（JSON 轨）
    public string name;         // 分组名（如 "main" / "loading"）
    public string path;         // 资源路径
    public string googleSheet;  // GoogleSheet 来源（编辑器抓取用）
}
```

`BettaFrameworkConfig.Instance` 从 `Resources.Load<BettaFrameworkConfig>("Config/BettaFrameworkConfig")` 取。

---

## 八、复刻要点与坑

1. **`UtilsEncryption.DecodeString` / `ResourceHub.LoadAsset` / `UtilsLog` / `UtilsEvent` 都来自 BettaSDK**，复刻需替换或复用。
2. **资源路径约定**：JSON 轨为 `{path}/{region}.json`，Proto 轨为 `{path}/{region}.bytes`；内置轨走 `Resources/{path}/{region}`（无扩展名）。工程侧不参与 `.json~` / `.bytes~` 副轨解析。
3. **`GetText` 未命中的兜底串 `{code}_{group}_{key}`** 是有意设计，方便排查缺词条，不是 bug。
4. **`SetLanguage` 是"先加载新语言全部成功才卸载旧语言"**，中途失败保留旧语言。
5. **语言切换触发两类通知**：`IOnLocaleRegionChange`（组件级，`UIText` 等注册）与 `EventLocaleChanged`（全局事件，`UtilsEvent`）。
6. **重复 key 后写覆盖**，仅告警不报错。

---

## 关联

- [[03-KNOWLEDGE/底层框架/BettaFramework/框架总览|框架总览]] — 本模块定位与 `BettaFrameworkRoot.Init` 链路
- [[03-KNOWLEDGE/底层框架/BettaSDK/SDK总览|BettaSDK 分册]] — `ResourceHub` / `UtilsEncryption` / `UtilsLog` / `UtilsEvent`
- [[03-KNOWLEDGE/底层框架/BettaInterface/契约总览|BettaInterface 契约]] — `ILogger` / `IUIBase` 等契约
