import { startWebMcpProbe } from "./webmcp-probe-server.mjs";

const { root, url } = await startWebMcpProbe();
console.log(`WebMCP D1 探针已启动：${url}`);
console.log(`测试根目录：${root}`);
console.log("仅 create_inbox_task 可用；按 Ctrl+C 停止。该目录不会写入真实 00-INBOX。");
