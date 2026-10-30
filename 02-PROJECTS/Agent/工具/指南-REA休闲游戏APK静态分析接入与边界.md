---
title: REA 休闲游戏 APK 静态分析接入与边界
date: 2026-10-13
updated: 2026-10-21
type: guide
status: current
tags: [LibraryG, Agent, REA, APK, static-analysis]
source: "本机 REA 6.4.0 接入与环境预检"
---

# REA 休闲游戏 APK 静态分析接入与边界

## 当前状态

- REA 已登记为本机 Codex MCP：`npx -y rea-agents@6.4.0 mcp`。
- REA 操作技能已安装于 `~/.agents/skills/reverse-engineer-anything`；Codex 配置备份为 `~/.codex/config.toml.rea.backup`。
- REA 专用环境已就绪：Eclipse Temurin JDK `21.0.12.1`、`jadx-headless-mcp 0.7.1` 和 Apktool `3.0.3` 均已下载并校验。
- REA 的 `JAVA_HOME` 与 `REA_JADX_MCP_JAR` 已写入 `~/.codex/config.toml` 的专用 MCP 环境；`codex mcp list` 显示 REA 为 `enabled`。
- 已用用户授权的 Tile Kingdom 1.58 XAPK 完成首个目标级只读解析，归档与 Android/JADX 基础链路均已验证。
- 未接入 Ghidra/IDA；它们用于更深的原生代码分析，不是首轮 APK 静态检查的前置条件。

### 2026-10-19 现状复核

- Codex 仍将 `rea` 列为 `enabled`，当前会话暴露 170 个 `mcp__rea__*` 工具；`binary_session` 可响应，说明 MCP 服务已连接。
- 状态复核时没有打开分析目标：`open: false`，`analysis_provider_binding: null`；随后以用户提供的 `Tile+Kingdom_1.58_APKPure.xapk` 路径做最小只读测试。
- 原生深度分析 Provider 仍未就绪：Ghidra 未设置 `GHIDRA_INSTALL_DIR`，Hopper 启动器缺失，IDA 未配置；因此当前不能宣称可做原生函数反编译。
- REA 专用 JDK `21.0.12.1` 仍可用并包含 `jdk.compiler`；`REA_JADX_MCP_JAR` 仍指向存在的 `jadx-headless-mcp-0.7.1-all.jar`。
- 已新增 `/Users/dean/.local/share/rea/bin/apktool` 启动器，并在 `~/.codex/config.toml` 的 `[mcp_servers.rea.env]` 中配置 `REA_APKTOOL_COMMAND`；全新 REA 6.4.0 进程已识别 Apktool `3.0.3`，Evidence ID 为 `ev_b45ef63d905c310f16e7489bd4f5ed500a975176523a4b701123ea7618c06b40`。
- 已将 `REA_ADB_PATH` 指向 Unity 6000.0.60f1 自带的 `platform-tools/adb`；全新 REA 6.4.0 进程已识别 ADB `36.0.0-13206524`，该体检未连接设备、未启动 ADB server，Evidence ID 为 `ev_892f3f01ea5a97b524cda24a069794b4b7dc7a848923b145284e1b4cf587a4b8`。
- 配置备份为 `~/.codex/config.toml.rea-20261019-apktool-adb.backup`。本次新对话中的 REA 6.4.0 已把 `inspect_android_package`、`search_android_classes` 等 Android 静态工具报告为 `available`，并已用真实主 APK 完成目标级解析，基础链路验证通过。
- JEB 未在本机发现已安装客户端，默认端点 `http://127.0.0.1:8425/mcp` 不可达；JEB、IDA、Hopper 均属需要单独安装或授权的可选 Provider，不作为本次 APK 静态分析基础链路的完成门槛。
- 用户提供的 `/Users/dean/Desktop/琐碎/Tile+Kingdom_1.58_APKPure.xapk` 实际是 `944B` 的 macOS Finder Alias，不是 XAPK/ZIP 数据；`open_binary` 因此返回 `unsupported binary format`，系统 ZIP 清单同样无法读取。此结果只能证明“所给路径不是实际样本”，不能据此判定 REA 不支持真实 XAPK。后续应提供实际 `.xapk` / `.apk` 文件路径，或先在 Finder 中定位别名原件。
- 用户重新提供的真实样本现保存于 `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/00-Package/TileKingdom_1.58_APKPure.xapk`，约 `189MB`；REA 成功识别为 `zip`、完成 5 节点 / 4 子文件的归档图与完整性核对，无 integrity contradiction。XAPK 包含主包 `com.dreamloft.tilekingdom.apk`、ARM64 分包 `config.arm64_v8a.apk`、`manifest.json` 和 `icon.png`。
- REA 随后通过 `jadx-headless-mcp 0.7.1` 成功静态解析主 APK：包名 `com.dreamloft.tilekingdom`，版本 `1.58`（versionCode `133`），minSdk `24`，targetSdk `35`，Manifest 状态 `complete`，统计到 `30313` 个类与 `1886` 个资源。未执行签名验证、应用安装、运行时观察或玩法逻辑深挖。
- 主 APK 已通过 Apktool `3.0.3 --no-src` 解码到 `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/01-Decoded/APK`，约 `232MB`。Android `res/` 可直接查看；Unity 主要内容位于 `assets/aa/`（Addressables，约 `89MB`）和 `assets/bin/Data/`（Unity Data，约 `79MB`）。Addressables `catalog.json` 暴露 `1571` 个内部资源标识，包含章节、装修、活动、关卡、Tile、Booster、本地化等资源名；贴图/Prefab 仍封装在 Unity bundle / serialized assets 中，需 Unity 专用导出工具才能批量还原为独立 PNG、音频和 Prefab 数据。
- 已在隔离环境 `/Users/dean/.local/share/rea/unity-tools` 安装 UnityPy `1.25.4`，并配置复用脚本 `bin/export_unity_art.py`。对 `defaultlocalgroup_assets_all.bundle` 识别到 `79251` 个对象，其中 Sprite `1583`、Texture2D `1503`；按 `tile|chapter|bedroom|cozy|spooky|tropical|bomb|booster|level|event` 过滤后，将 `204` 张图片无失败导出到 `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/02-Art/PNG_Filtered_Sample`，报告为 `export-report.json`。
- 同一 UnityPy 环境已新增 `bin/export_unity_audio.py`。基础 `assets/bin/Data` 中识别并成功导出 `265` 个 AudioClip，全部还原为 WAV、失败 `0`，输出 `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/03-Audio/WAV_Export`，约 `279MB`；按时长初分为 `255` 个 SFX 与 `10` 个 Music，总时长约 `1858.81` 秒。分类只是便于浏览，不代表原项目 AudioMixer 分组。
- 已在 `/Users/dean/.local/share/rea/il2cpp-tools/Cpp2IL` 配置官方 Cpp2IL `2022.1.0-pre-release.21` macOS ARM64 版；下载件签名前 SHA-256 为 `6670ddb93f28d4e7f329251d2597d2abbc6ba23e46382f7ca7b5e437ec93606a`，与发布页一致，因 macOS 执行限制对本地副本补了 ad-hoc 签名。以 Unity `2021.3.45f2`、`libil2cpp.so` 与 `global-metadata.dat` 成功映射 `127372` 个方法定义，输出 `12403` 个 Diffable C# 文件（约 `55MB`）和带 Call Analyzer 的 ISIL/ARM64 指令转储（约 `395MB`）到 `/Users/dean/LibraryG/06-PRODUCT-ASSETS/TileKingdom/1.58/04-ReverseEngineering/IL2CPP_Static`。
- Tile Temple 活动抽样已验证静态逻辑可读到方法内部：`TileTempleAddon` 组合 `PlayerEliminationAddon`、`LevelScoringAddon`、`RewardAddon`；参与时订阅 `ScoreChanged`，只有关卡特性 `IsTileTempleActive` 时才触发淘汰模拟；`CanReward` 要求尚未领奖且淘汰模块判定获胜；奖励取 `RewardAddon.GetFirstRewardAt(0)`；单实例胜利次数小于 `2` 才允许再次参与；胜利时累计实例胜场。其 UI/状态层包含 EventStarted、Info、Load、主界面、Reward，并有完成/失败埋点类。以上为静态二进制证据，不等同于运行时远端配置或实际活动参数。
- Tile Temple 的专属 Addressables 目录项指向独立 `tiletempleevent_assets_all_*.bundle`，该 bundle 未随本次基础 APK 落盘，推测属于远端内容；因此本地包可恢复框架、状态、字段和方法逻辑，但“每阶段淘汰人数、最大获胜人数、奖励内容”等序列化实例值仍需取得对应远端 bundle、配置响应或运行时证据后才能确认。

## AI 通用配置入口

面向其他机器和其他 AI 的独立安装说明见：[[02-PROJECTS/Agent/工具/手册-REA MCP通用配置与验收（AI执行版）|REA MCP 通用配置与验收手册（AI 执行版）]]。该手册不继承本文的本机路径、当前状态或历史 Evidence。
## 使用范围

本文限于安装包静态工具接入。长期竞品调研已扩展到应用运行后的私有存储、配置与下载资源，完整方法见 [[02-PROJECTS/产品分析/方法-竞品模块分析与持续维护|竞品模块分析与持续维护]]；Windows 实际可用工具与本页历史 Mac 环境分开核验，不能以静态流程“不会运行样本”的边界代替用户另行授权的运行采集范围。

仅处理本人拥有或已获授权的 APK，用于竞品体验拆解、包结构、Manifest、资源、SDK 与可见玩法逻辑的静态研究。

不用于绕过付费、授权、反作弊、加密保护，或提取、传播受限制内容。不会安装、运行或修改样本 APK。

## 标准分析交付结构

REA 竞品 APK 分析默认不是“解包完成即结束”，而是围绕资源使用与逻辑关系交付：

| 维度 | 最低交付 |
|---|---|
| 图片 | Sprite/Texture/Atlas 清单、所在 bundle、Prefab/UI 消费者、触发界面、材质依赖与可替换入口 |
| 动效 | Animator/AnimationClip、ParticleSystem、Spine/Tween 的控制组件、动画名、触发条件和材质/Shader/骨骼依赖 |
| 音效 | AudioClip、SoundKey、调用方法、触发事件、循环/一次性和 Mixer/配置绑定；不能只按文件名猜用途 |
| 逻辑 | 功能入口、状态流、核心数据、判定、奖励、失败、埋点和远端配置边界 |
| 引用链 | 尽量形成 `资源 → Prefab/组件 → 控制逻辑 → 触发条件 → 表现结果` 的最短可复用链 |
| 验证状态 | 明确标注静态确认、静态推断、运行时确认、远端缺失和工具未恢复 |

只有文件库存而未找到消费者时，写作“已提取/已定位”；找到组件和触发条件后才写作“已对位”；只有实际运行观察后才写作“运行时已验证”。

## 首个样本流程

1. 用户提供 APK 的本机路径，并确认其来源和分析授权。
2. 先检查路径是否为真实 APK/XAPK 文件而非 Finder Alias；XAPK 应能识别为 ZIP 容器。再仅做包信息、Manifest、资源与依赖概览；样本不复制入 LibraryG。
3. 需要 Java/Kotlin 代码检索时，使用 REA 的 Android 静态分析工具；需要解码 `resources.arsc` 或 XML 资源时，使用已校验的 Apktool JAR。
4. Unity 美术资源优先从 Addressables bundle 用隔离的 UnityPy 导出；先按资源名小批量筛选，保留 JSON 报告和 path ID，避免把 Texture2D 与 Sprite 的重复导出误判为不同原画。
5. Unity 音频同时检查 Addressables bundle 和 `assets/bin/Data` 的 AudioClip；若 `AudioClip.m_Resource` 指向 `resources.resource` 等流式侧车，必须将主 Unity 文件与侧车一并交给 UnityPy，不能把单文件解码失败误判为音频缺失。共享脚本 `export_unity_audio.py` 支持可重复的 `--resource` 参数。导出时保留原名称、path ID、时长、声道、采样率和 JSON 报告；按时长生成的 Music/SFX 目录仅是浏览分类，不能据此推断实际播放总线。
6. IL2CPP 逻辑以 `global-metadata.dat`、目标架构 `libil2cpp.so` 和准确 Unity 版本配对；先输出 Diffable C# 做类/字段/方法索引，再按具体问题查 ISIL/原生指令。Cpp2IL 的 `NotImplemented` 或匿名地址调用必须保留为未完全恢复，不强行翻译成源码事实。
7. 将结论按游戏或专题归入 `02-PROJECTS/` 对应知识路径，并在当日 Daily 写清样本、证据边界和未验证项。

## 使用要点

- 新开一个 Codex 对话后，REA MCP 才会从新配置载入。
- JDK、JADX 与 Apktool 均存放于 `~/.local/share/rea/`，不会改变系统默认 Java 或写入项目目录。
- 优先从静态可证据化内容开始；动态行为、远端配置和真实付费链路必须标为待设备/网络验证。
- 对比分析只记录机制与实现线索，不把反编译结果当作运行时事实。

## 关联

- [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]
- [[02-PROJECTS/产品分析/_MOC|产品分析 MOC]]

