import { createServer } from "node:http";
import path from "node:path";
import { DEFAULT_INBOX_ROOT, InboxTaskValidationError, createInboxTask } from "./inbox-task.mjs";
import { readReceiverSettings, writeReceiverSettings } from "./receiver-settings.mjs";
import { renderWebMcpInboxPage } from "./webmcp-inbox-page.mjs";

const MAX_REQUEST_BYTES = 24_000;
export const DEFAULT_SETTINGS_FILE = "/Users/dean/LibraryG/.inbox-receiver/settings.json";

async function readJson(request) {
  const chunks = [];
  let size = 0;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > MAX_REQUEST_BYTES) throw new InboxTaskValidationError("请求正文超过长度上限。");
    chunks.push(chunk);
  }
  try { return JSON.parse(Buffer.concat(chunks).toString("utf8")); } catch { throw new InboxTaskValidationError("请求正文必须是 JSON。"); }
}

function sendJson(response, statusCode, value) {
  response.writeHead(statusCode, { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" });
  response.end(JSON.stringify(value));
}

/** Production server: no root/path input, no read routes, no network exposure. */
export function createWebMcpInboxServer({ root = DEFAULT_INBOX_ROOT, settingsFile = DEFAULT_SETTINGS_FILE } = {}) {
  return createServer(async (request, response) => {
    const url = new URL(request.url, "http://127.0.0.1");
    if (request.method === "GET" && url.pathname === "/") {
      response.writeHead(200, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" });
      response.end(renderWebMcpInboxPage());
      return;
    }
    if (request.method === "GET" && url.pathname === "/v1/inbox-settings") {
      try { sendJson(response, 200, await readReceiverSettings(settingsFile)); } catch (error) { sendJson(response, 500, { error: error.message }); }
      return;
    }
    if (request.method === "POST" && url.pathname === "/v1/inbox-settings") {
      try {
        const input = await readJson(request);
        if (!input || typeof input.automaticEnabled !== "boolean") throw new InboxTaskValidationError("automaticEnabled 必须是布尔值。");
        sendJson(response, 200, await writeReceiverSettings(settingsFile, input.automaticEnabled));
      } catch (error) { sendJson(response, error instanceof InboxTaskValidationError ? 400 : 500, { error: error.message || "更新自动建卡设置失败。" }); }
      return;
    }
    if (request.method === "POST" && url.pathname === "/v1/create-inbox-task") {
      if (!request.headers["content-type"]?.startsWith("application/json")) { sendJson(response, 415, { error: "只接受 application/json。" }); return; }
      try {
        const settings = await readReceiverSettings(settingsFile);
        if (!settings.automaticEnabled) throw new InboxTaskValidationError("自动建卡已暂停；请在本机页面恢复后再试。");
        const result = await createInboxTask(await readJson(request), { root });
        sendJson(response, 201, { ...result, absolutePath: path.resolve(root, result.relativePath), reused: false });
      } catch (error) { sendJson(response, error instanceof InboxTaskValidationError ? 400 : 500, { error: error.message || "创建任务卡失败。" }); }
      return;
    }
    sendJson(response, 404, { error: "未找到接口。" });
  });
}

/** The only public local entry point. Keep it stable so Chat does not open a test page by mistake. */
export async function startWebMcpInbox({ port = 38741 } = {}) {
  const server = createWebMcpInboxServer();
  await new Promise((resolve, reject) => { server.once("error", reject); server.listen(port, "127.0.0.1", () => { server.off("error", reject); resolve(); }); });
  return { server, url: `http://127.0.0.1:${port}/` };
}
