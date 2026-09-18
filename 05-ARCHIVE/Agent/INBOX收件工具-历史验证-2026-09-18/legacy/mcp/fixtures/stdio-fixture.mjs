import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { createInboxTask } from "../../../src/inbox-task.mjs";
import { createInboxMcpServer } from "../src/mcp-server.mjs";

const root = process.argv[2];
if (!root) {
  throw new Error("测试夹具需要临时 INBOX 根目录。");
}

serveStdio(
  () => createInboxMcpServer({
    writeTask(input) {
      return createInboxTask(input, { root });
    }
  }),
  {
    onerror(error) {
      console.error(error.message);
    }
  }
);
