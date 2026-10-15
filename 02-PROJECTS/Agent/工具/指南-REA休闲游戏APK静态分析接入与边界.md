---
title: REA 休闲游戏 APK 静态分析接入与边界
date: 2026-10-13
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
- 当前仍未对任何 APK 做实际解析。
- 未接入 Ghidra/IDA；它们用于更深的原生代码分析，不是首轮 APK 静态检查的前置条件。

## 使用范围

仅处理本人拥有或已获授权的 APK，用于竞品体验拆解、包结构、Manifest、资源、SDK 与可见玩法逻辑的静态研究。

不用于绕过付费、授权、反作弊、加密保护，或提取、传播受限制内容。不会安装、运行或修改样本 APK。

## 首个样本流程

1. 用户提供 APK 的本机路径，并确认其来源和分析授权。
2. 先仅做包信息、Manifest、资源与依赖概览；样本不复制入 LibraryG。
3. 需要 Java/Kotlin 代码检索时，使用 REA 的 Android 静态分析工具；需要解码 `resources.arsc` 或 XML 资源时，使用已校验的 Apktool JAR。
4. 将结论按游戏或专题归入 `02-PROJECTS/` 对应知识路径，并在当日 Daily 写清样本、证据边界和未验证项。

## 使用要点

- 新开一个 Codex 对话后，REA MCP 才会从新配置载入。
- JDK、JADX 与 Apktool 均存放于 `~/.local/share/rea/`，不会改变系统默认 Java 或写入项目目录。
- 优先从静态可证据化内容开始；动态行为、远端配置和真实付费链路必须标为待设备/网络验证。
- 对比分析只记录机制与实现线索，不把反编译结果当作运行时事实。

## 关联

- [[02-PROJECTS/Agent/工作流/_MOC|Agent 工作流 MOC]]

