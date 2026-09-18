import { startWebMcpInbox } from "./webmcp-inbox-server.mjs";

const { url } = await startWebMcpInbox();
console.log(`生产试用收件器已启动：${url}`);
console.log("生产模式：仅新建 /Users/dean/LibraryG/00-INBOX/ 任务卡；按 Ctrl+C 停止。");
