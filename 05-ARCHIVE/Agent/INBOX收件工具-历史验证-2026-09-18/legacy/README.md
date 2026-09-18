# 历史验证模块

这些文件不属于当前生产收件链路，只保留验证和追溯价值：

- `mcp/`：旧 MCP stdio 适配；当前未接入外部私有连接或 tunnel。
- `webmcp-probe/`：D1/D2 临时目录探针；写入系统临时目录，不写真实 `00-INBOX/`。

当前生产入口仅为 [[02-PROJECTS/Agent/工具/INBOX收件工具/README|INBOX 收件工具]] 中的 `npm run serve:webmcp-inbox`。历史测试脚本与其 MCP 依赖已于 2026-09-18 从生产工具移除；本目录只作原件追溯。
