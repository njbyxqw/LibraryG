import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { createInboxMcpServer } from "./mcp-server.mjs";

serveStdio(createInboxMcpServer, {
  onerror(error) {
    // stdout is reserved for MCP protocol messages.
    console.error(error.message);
  }
});
