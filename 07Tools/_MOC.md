---
title: Tools 工具集 MOC
date: 2026-10-23
type: index
status: current
tags: [LibraryG, Tools, 工具集, MOC]
---

# Tools 工具集 MOC

LG 中跨项目工具仓库的导航入口。工具源码、依赖与运行结果仍留在各自仓库；此处记录定位、用途和验证边界。

## 工具仓库

| 工具 | 本机位置 | 用途 | 状态 |
|---|---|---|---|
| `common_tools` | `/Users/dean/common_tools` | 移动应用与 Unity 分析工具集 | 2026-10-23 静态浏览 README；未执行工具或样本 |
| `common_tools`（Windows） | `D:\common_tools` | 同一工具仓库的 Windows 执行副本 | 2026-10-27 SSH 克隆，提交 `e5faf0dc363a883d56d1683be17c5ba4583edc14`；Royal Match Il2CppDumper 已实跑成功 |

## common_tools 速览

来源：`/Users/dean/common_tools/README.md` 及各子目录 README；本次查看的本地提交为 `e5faf0dc`。下表是入口索引，具体参数以仓库文档为准。

| 目录 / 入口 | 主要用途 |
|---|---|
| `app_auto_unpack/` | APK、XAPK、AAB、IPA 解包；按需串接 AssetRipper、Il2CppDumper、Ghidra、JADX、LuaJIT 和静态地址分析 |
| `frida_tool/` | Android 设备操作、Frida 运行时采集、IL2CPP metadata dump 与内存查询 |
| `app_sandbox_tool/` | Android 应用沙盒导出、恢复及快照差异比较；设备操作需要 ADB 与 root |
| `apk_make_debuggable/` | 重建并重签可调试 APK / XAPK，产物需单独做设备安装验证 |
| `unity_assetbundle_tool/` | 调用 AssetRipper 查询 Bundle 内 Collections 与资源对象，输出 JSON |
| `analysis_results.py` | 保存已选分析结果、按指定字段比较 JSON；不重新执行分析阶段 |

仓库 README 中部分独立阶段与运行时方法标为“实现待验证”；各模块自述的离线测试数量也未在本次重跑。使用前先进入对应 README 确认输入、依赖、输出与覆盖行为。

## Windows 使用与验证边界

- 仓库来源：`git@gitlab.ftsview.com:Sparkwoods/Custom/Frontend/common_tools.git`。HTTPS 无可用非交互凭据；本机既有 SSH 身份可用。Mac 历史记录只是文档浏览，不能当作端到端已验收。
- 运行入口：`app_auto_unpack/stage_cli.py`，本机 Python 为 `D:\LibraryG\06-PRODUCT-ASSETS\_Tools\unity-analysis\Scripts\python.exe`。本次 `tool.check` 定位到内置 Windows Dumper/Ghidra；Dumper 对 Royal Match 38911 的二进制和 metadata 哈希绑定后成功产出 `dump.cs`、`il2cpp.h`、`script.json`、字符串表及 DummyDll。
- 本地兼容修复：`app_auto_unpack/provenance.py` 跨 `stat/fstat` 的比较不再混用 Windows `ctime` 语义；跨接口仍比设备号、文件号、大小、修改时间，同接口读前读后仍比完整身份，并保留 SHA256 检查。只有此文件有本地修改，未提交/推送；补丁在 CommonTools-Audit。4 项 provenance 回归通过；首次测试因默认临时目录权限失败，改用工作区临时目录后通过。
- `il2cpp_find_methods.py` 已读取 247,280 个有效方法条目；Ancient 关键词 1,205 条，分两页读取完毕，包含泛型容器，不等于 1,205 个业务方法。结果保留 `partial`：地址未绑定到运行内存，候选也未自动消歧。
- `frida_tool/scripts/android_cli.py app.inspect` 在 MuMu 返回 `partial`：设备 `ps` 列格式不符合工具预期。初次工具审计未启动 Frida；后续网络任务实际验证17.16.4：x86_64 MuMu 转译 ARM64 时 emulated attach 报错，native attach 只见桥接模块，0个业务Hook，不推断所有MuMu均不可用。依赖保留在LG工具目录；设备临时服务、文件与27043转发已清理。`app_sandbox_tool export` 会停止应用，本次未运行；配置通过Root SQLite只读查询补充。见[[02-PROJECTS/产品分析/Royal Match/资源路径索引#运行时证据|实际网络观测证据]]。
- Ghidra 初次因 JADX 的 Java 只有 JRE 而失败；随后将官方 Temurin JDK 21.0.12.1+1 下载到 `06-PRODUCT-ASSETS/_Tools/jdk21/temurin/` 并核对官方 SHA256，未更改系统 Java。`native.import_binary --analysis none` 已成功，工程为 AARCH64、image base `0x100000`、输入哈希一致；默认未进行全程序自动分析。定向伪代码结果与边界见产品证据索引。
- 执行证据：`D:\LibraryG\06-PRODUCT-ASSETS\RoyalMatch\38911\04-ReverseEngineering\CommonTools-Audit\`；产品结论见 [[02-PROJECTS/产品分析/Royal Match/资源路径索引|Royal Match 证据索引]]。仅能分析客户端包含或已下发到账号的数据，不能由工具存在推断可恢复全部服务器源码/配置。
- 定向方法体试跑：使用仓库内 Ghidra 加本地 `TargetedDecompile.java` 导出4个方法。解锁方法返回66；两个复杂方法存在明显PIC/不可达块告警，暂不作为可靠重建源码。当前尚未运行全量 `native.apply_il2cpp with-struct`，后续应补函数注册/签名/边界，再重导复杂方法；原始结果和质量判定均保留。

## 关联入口

- [[HOME|LibraryG 主入口]]
- [[AI总MOC|AI 总 MOC]]
