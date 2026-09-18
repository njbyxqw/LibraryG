import { createServer } from "node:http";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";

import { InboxTaskValidationError } from "../../../src/inbox-task.mjs";
import { createDeduplicatingTaskCreator } from "./task-receipt.mjs";

const MAX_REQUEST_BYTES = 24_000;
const TOOL_NAME = "create_inbox_task";

export function renderWebMcpProbePage() {
  const inputSchema = {
    type: "object", additionalProperties: false,
    required: ["title", "state", "target", "next_owner", "next_action", "conclusion"],
    properties: {
      title: { type: "string", minLength: 1, maxLength: 80 },
      state: { type: "string", enum: ["讨论", "方案", "待办", "进行中", "阻塞", "完成"] },
      target: { type: "string", enum: ["LG", "MT", "TS", "跨项目"] },
      next_owner: { type: "string", enum: ["Chat", "Codex", "用户"] },
      next_action: { type: "string", minLength: 1, maxLength: 500 },
      conclusion: { type: "string", minLength: 1, maxLength: 8000 },
      facts_to_verify: { type: "array", maxItems: 20, items: { type: "string", maxLength: 500 } },
      related_links: { type: "array", maxItems: 20, items: { type: "string", maxLength: 500 } }
    }
  };
  return `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>LibraryG INBOX — WebMCP 能力探针</title>
<style>body{font:16px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:720px;margin:48px auto;padding:0 20px;color:#18212f}code{background:#f0f2f5;padding:2px 5px;border-radius:4px}.ok{color:#087b39}.no{color:#b42318}</style>
<h1>LibraryG INBOX 能力探针</h1><p>此页只注册一个工具：<code>${TOOL_NAME}</code>。服务处于测试模式，写入固定临时目录，绝不写入 LibraryG 的 <code>00-INBOX</code>。</p><p id="api">正在检测 WebMCP…</p><p id="tool">工具尚未注册。</p><p id="result">尚未创建测试卡。</p>
<script type="module">
const api=document.querySelector('#api'),tool=document.querySelector('#tool'),status=document.querySelector('#result');const inputSchema=${JSON.stringify(inputSchema)};
if(!document.modelContext||typeof document.modelContext.registerTool!=='function'){api.textContent='当前内置浏览器未提供 document.modelContext。';api.className='no';}else{api.textContent='检测到 document.modelContext。正在注册唯一工具…';api.className='ok';try{await document.modelContext.registerTool({name:'${TOOL_NAME}',title:'创建测试 INBOX 任务卡',description:'仅当用户明确要求整理进 INBOX 时调用。此为测试工具，只会在固定临时目录创建一张测试任务卡；不能读取、修改、删除任何现有内容，也不能选择路径。重复调用相同任务只返回首次结果。',inputSchema,annotations:{readOnlyHint:false,consequentialHint:true,untrustedContentHint:false},execute:async(input,{signal}={})=>{const accepted=window.confirm('确认创建测试 INBOX 卡？\\n\\n标题：'+input.title+'\\n状态：'+input.state+'\\n目标：'+input.target+'\\n\\n它只会写入临时测试目录。');if(!accepted){status.textContent='已取消：未创建测试卡。';status.className='no';throw new Error('用户取消创建测试卡。');}status.textContent='正在创建测试卡…';status.className='';try{const response=await fetch('/v1/create-inbox-task',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(input),signal});const output=await response.json();if(!response.ok)throw new Error(output.error||'创建测试卡失败。');status.textContent=(output.reused?'未重复创建，返回已有测试卡：':'测试卡已创建：')+output.relativePath;status.className='ok';return output;}catch(error){status.textContent='创建失败：'+(error?.message||String(error));status.className='no';throw error;}}});tool.textContent='唯一工具已注册。每次建卡将由本机页面再次确认。';tool.className='ok';}catch(error){tool.textContent='工具注册失败：'+(error?.message||String(error));tool.className='no';}}
</script>`;
}

async function readJson(request) {
  const chunks = []; let size = 0;
  for await (const chunk of request) { size += chunk.length; if (size > MAX_REQUEST_BYTES) throw new InboxTaskValidationError("请求正文超过长度上限。"); chunks.push(chunk); }
  try { return JSON.parse(Buffer.concat(chunks).toString("utf8")); } catch { throw new InboxTaskValidationError("请求正文必须是 JSON。"); }
}
function sendJson(response, statusCode, value) { response.writeHead(statusCode, { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" }); response.end(JSON.stringify(value)); }

/** D1 only: root is process-controlled, never available in the tool schema. */
export function createWebMcpProbeServer({ root }) {
  if (!root) throw new Error("D1 probe requires a fixed temporary root.");
  const createTask = createDeduplicatingTaskCreator({ root });
  return createServer(async (request, response) => {
    const url = new URL(request.url, "http://127.0.0.1");
    if (request.method === "GET" && url.pathname === "/") { response.writeHead(200, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" }); response.end(renderWebMcpProbePage()); return; }
    if (request.method === "POST" && url.pathname === "/v1/create-inbox-task") {
      if (!request.headers["content-type"]?.startsWith("application/json")) { sendJson(response, 415, { error: "只接受 application/json。" }); return; }
      try { sendJson(response, 201, await createTask(await readJson(request))); } catch (error) { sendJson(response, error instanceof InboxTaskValidationError ? 400 : 500, { error: error.message || "创建测试卡失败。" }); }
      return;
    }
    sendJson(response, 404, { error: "未找到接口。" });
  });
}

/** Historical probe uses a separate port so it cannot be mistaken for production. */
export async function startWebMcpProbe({ port = 38743 } = {}) {
  const root = await mkdtemp(path.join(tmpdir(), "libraryg-webmcp-probe-"));
  const server = createWebMcpProbeServer({ root });
  await new Promise((resolve, reject) => { server.once("error", reject); server.listen(port, "127.0.0.1", () => { server.off("error", reject); resolve(); }); });
  return { server, root, url: `http://127.0.0.1:${port}/` };
}
export { TOOL_NAME };
