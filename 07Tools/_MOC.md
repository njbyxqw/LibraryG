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

## 关联

- [[HOME|LibraryG 主入口]]
- [[AI总MOC|AI 总 MOC]]
