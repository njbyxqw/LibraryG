---
title: REA MCP 通用配置与验收手册（AI 执行版）
date: 2026-10-19
updated: 2026-10-19
type: guide
status: current
tags: [Agent, REA, MCP, setup]
source: "REA 与 OpenAI 官方配置文档"
---

# REA MCP 通用配置与验收手册（AI 执行版）

> [!important] 交给 AI 的任务目标
> 在用户授权范围内，为当前 AI 客户端完成 REA MCP 的安装、注册、重载与真实调用验收。不得引用其他机器的用户名、绝对路径、版本状态或 Evidence；所有路径和版本都必须在当前机器实时发现。

## 1. 先确定“完整”的范围

REA 核心 MCP 与分析 Provider 是两层：

| 层级 | 完成标准 | 是否必需 |
|---|---|---|
| REA 核心 | MCP 已注册，客户端重载后实际出现 REA 工具，至少一次状态调用成功 | 必需 |
| 目标 Provider | 当前任务所需的 JADX、Ghidra、IDA、Hopper、Apktool、ADB、Binwalk 等实际可用 | 按目标安装 |

不要为了“看起来完整”安装所有可选工具。静态 JavaScript、普通归档、Android、原生程序、固件和设备运行时各自需要不同 Provider；只补齐当前任务所需链路。

## 2. 环境预检

1. 确认操作系统、CPU 架构、当前 AI 客户端及其配置范围。
2. 检查 `node`、`npm`、`npx`。REA 当前支持 Node.js `22.x（>=22.19）`、`24.x（>=24.11）` 和 `26+`；不支持奇数版本 `23`、`25` 或预发布版。
3. 若 Node.js 不兼容或缺失，只报告精确问题和建议安装方式；REA 配置过程不得擅自升级 Node.js、npm、Homebrew、Java 或其他无关软件。
4. 若用户已安装 `rea`，优先复用；否则使用 `npx -y rea-agents@latest` 执行一次性命令。

```sh
command -v node
node --version
command -v npm
command -v npx
command -v rea
```

## 3. 首选安装流程

将 `<client>` 替换成真实客户端 ID，例如 `codex`、`claude_code`、`claude_desktop`、`cursor`、`gemini_cli`、`windsurf`、`opencode` 或 `vscode`。不确定时先查看当前版本帮助或运行不带客户端写入的交互式 setup，不要猜配置路径。

```sh
npx -y rea-agents@latest doctor --client <client> --json
npx -y rea-agents@latest setup --client <client> --dry-run --json
```

执行规则：

1. `doctor` 只读检查现状；`setup --dry-run` 只生成计划。
2. 向用户展示计划中的版本、写入路径、备份、Skill 变化和可选 Provider 操作。
3. 获得对应写入授权后，以完全相同的客户端范围应用：

```sh
npx -y rea-agents@latest setup --client <client> --yes
```

4. 不使用 `--all-detected`，除非用户明确要求配置所有检测到的客户端。
5. 不添加 `--install-hopper`，除非用户明确需要 Hopper 并批准该独立安装。
6. setup 会把持久 MCP 注册固定到本次解析出的精确 REA 版本，并安装匹配的操作 Skill；不要把持久配置长期写成 `@latest`。

## 4. 手动注册仅作后备

只有 setup 不支持目标客户端或明确失败时，才手动配置 STDIO MCP。先取得当前发布版本，把 `<PINNED_VERSION>` 替换成精确版本号。

Codex `~/.codex/config.toml` 示例：

```toml
[mcp_servers.rea]
command = "npx"
args = ["-y", "rea-agents@<PINNED_VERSION>", "mcp"]
startup_timeout_sec = 30
```

常见 JSON 客户端的结构示例：

```json
{
  "mcpServers": {
    "rea": {
      "command": "npx",
      "args": ["-y", "rea-agents@<PINNED_VERSION>", "mcp"]
    }
  }
}
```

实际键名和配置路径以当前客户端文档为准。修改前备份原文件，只增改 `rea` 条目，不覆盖其他 MCP、模型或权限配置。

## 5. 重载并验收核心 MCP

配置写入后必须重启或重新连接对应 AI 客户端；旧对话可能继续持有旧 MCP 进程。

重载后依次验证：

1. 当前会话实际出现 `mcp__rea__*` 工具。
2. 调用 `binary_session({})` 或当前版本提供的等价状态工具。
3. 只摘要记录服务版本、活动目标、Provider 和 `tool_availability`；不要原样输出超长能力目录。
4. `open: false` 仅表示尚未打开目标，不是故障。

只有配置文件存在、`doctor` 成功或 MCP 显示 enabled，都不足以证明当前会话已经连接；必须以真实 MCP 调用为最终依据。

## 6. 按任务补齐 Provider

| 目标 | 额外依赖 | 验收方式 |
|---|---|---|
| JavaScript / Electron / ASAR、普通归档 | 通常不需要原生反编译器 | 对用户授权的测试目标执行最小只读分析 |
| Android APK 代码 | 完整 JDK 17+，包含 `jdk.compiler`；`jadx-headless-mcp 0.7.1` JAR | `inspect_android_package` 成功返回包身份、Manifest 和类覆盖 |
| Android 资源 | 用户提供的可执行 Apktool 命令 | 若当前 REA 暴露 `inspect_apktool_client`，调用并确认可用 |
| Android 设备运行时 | 用户提供的 ADB；真实设备操作另需明确授权 | 先做不接触设备的客户端检查，再按授权连接设备 |
| 原生二进制 | 当前平台受支持的 Ghidra、IDA 或 Hopper | `rea providers --json` 加一个授权测试目标的最小打开/关闭 |
| 固件 | 对应平台上的 Binwalk 或 Unblob | 仅在固件任务中按 Provider 诊断补齐 |

缺少某个 Provider 只影响依赖它的操作，不代表 REA 核心安装失败。必须读取 `binary_session.result.tool_availability` 或 Provider 返回的具体 remediation，不能凭工具数量判断可用性。

## 7. Android / APK 配置模板

REA 不会替用户安装 Java、Android SDK、JADX、Apktool、ADB 或模拟器。需要 Android 静态分析时，先在用户授权下准备：

- 64 位完整 JDK 17 或更高版本；
- `jadx-headless-mcp-0.7.1-all.jar`；
- 可选的 Apktool 可执行命令；
- 仅运行时任务需要的 ADB。

把实时发现的绝对路径写入 REA MCP 的环境段；不存在或未验收的可选项不要写占位值：

```toml
[mcp_servers.rea.env]
JAVA_HOME = "/ABSOLUTE/PATH/TO/JDK"
REA_JADX_MCP_JAR = "/ABSOLUTE/PATH/TO/jadx-headless-mcp-0.7.1-all.jar"
REA_APKTOOL_COMMAND = "/ABSOLUTE/PATH/TO/apktool"
REA_ADB_PATH = "/ABSOLUTE/PATH/TO/adb"
```

如 Apktool 只有 JAR，可在用户选定的工具目录创建启动器，并将 `REA_APKTOOL_COMMAND` 指向该可执行文件：

```sh
#!/bin/sh
exec "/ABSOLUTE/PATH/TO/JDK/bin/java" \
  -jar "/ABSOLUTE/PATH/TO/apktool.jar" "$@"
```

写入后再次重载客户端。先验证 Java 版本、`jdk.compiler`、JAR 存在性、启动器执行权限及各工具自身的版本输出；最后用用户拥有或明确授权的真实 APK 做目标级验收。未执行目标级解析时，只能报告“Provider 预检通过”，不能报告“APK 分析链路已通过”。

## 8. 故障分流

| 观察 | 原因层级 | 正确处理 |
|---|---|---|
| 安装了 REA Skill，但没有 `mcp__rea__*` | 只有操作说明，MCP 未注册或未连接 | 运行 doctor 和 dry-run setup；不要重装分析引擎 |
| doctor 对齐，但当前会话无工具 | 客户端仍使用旧连接 | 重启 / reconnect / 新建会话，检查 MCP 启动日志 |
| `MCP tool call requires approval...` | AI 客户端策略在 REA 执行前拦截 | 走客户端审批；不要用重装 Provider 解决 |
| `provider_unavailable` | 当前操作缺少专属依赖 | 按返回的 remediation 只修该 Provider |
| shell 找不到 `rea`，但 MCP 正常 | CLI PATH 与 MCP 启动环境不同 | 检查实际 launcher；不要据此认定 MCP 损坏 |
| `open: false` | 当前没有活动目标 | 正常空闲状态 |
| 工具列表很长但操作不可用 | 工具已注册不等于 Provider 就绪 | 查看 operation-level availability |
| 重复调用仍失败 | 输入或前置条件未改变 | 停止重试，先解决原始阻塞项 |

## 9. 最终完成报告模板

AI 最终必须逐项报告，不得只说“REA 已配置完成”：

```text
REA 版本：<精确版本>
客户端与配置范围：<client + 配置文件或注册位置>
核心 MCP：<已注册 / 已重载 / 真实调用通过>
匹配 Skill：<已安装及版本来源>
本任务所需 Provider：<逐项列出已通过、未配置、不可用>
目标级验收：<测试目标、调用、结果；未执行则明确写未执行>
修改与备份：<实际文件和备份位置>
剩余边界：<需要用户批准、样本、商业软件或设备的事项>
```

完成判定：核心 MCP 真实调用通过，且用户当前任务依赖的 Provider 已完成真实最小验收。不得把静态分析写成运行时事实，也不得把可选商业 Provider 未安装描述为核心配置失败。

## 10. 官方参考

- [REA 安装与客户端配置](https://github.com/morluto/rea/blob/main/docs/installation.md)
- [REA Android 静态分析](https://github.com/morluto/rea/blob/main/docs/android-analysis.md)
- [REA CLI 与 Provider](https://github.com/morluto/rea/blob/main/docs/cli.md)
- [OpenAI Docs：Codex MCP 配置](https://learn.chatgpt.com/docs/extend/mcp)
- [OpenAI Docs：Codex `config.toml` 配置参考](https://learn.chatgpt.com/docs/config-file/config-reference)


