import { parseHandoff, CHAT_INSTRUCTIONS } from "./handoff.mjs";
const TOOL_NAME = "create_inbox_task";

function toolSchema() {
  return {
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
}

export function renderWebMcpInboxPage() {
  return `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>LibraryG INBOX — WebMCP 收件器</title>
<style>body{font:16px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:720px;margin:48px auto;padding:0 20px;color:#18212f}code{background:#f0f2f5;padding:2px 5px;border-radius:4px}button{font:inherit;padding:7px 11px}.ok{color:#087b39}.no{color:#b42318}textarea{box-sizing:border-box;width:100%;min-height:170px;font:13px ui-monospace,SFMono-Regular,Menlo,monospace;padding:10px}.panel{margin-top:28px;padding:18px;border:1px solid #d9dee7;border-radius:8px}label{display:block;margin:10px 0 8px;font-weight:600}</style>
<h1>LibraryG INBOX 收件器</h1><p>此页只注册一个工具：<code>${TOOL_NAME}</code>。自动建卡开启时，只会新建 LibraryG 的 <code>00-INBOX</code> 任务卡。</p><p id="api">正在检测 WebMCP…</p><p id="tool">工具尚未注册。</p><p id="mode">正在读取自动建卡状态…</p><button id="toggle" type="button" disabled>暂停自动建卡</button><p id="result">尚未创建任务卡。</p><section class="panel"><h2>保底：从 Chat 交接包创建</h2><p>当 Chat 没有调用网站工具时，先在 Chat 点复制 JSON 交接包，再点下方按钮。此页只会在你点击按钮后读取一次剪贴板；不可用时仍可手动粘贴。</p><p><button id="create-from-clipboard" type="button">从剪贴板创建</button></p><label for="handoff">任务交接包</label><textarea id="handoff" spellcheck="false" placeholder='{"title":"…","state":"方案","target":"LG","next_owner":"用户","next_action":"…","conclusion":"…"}'></textarea><p><button id="create-pasted" type="button">使用已粘贴内容创建</button></p></section>
<section class="panel"><h2>给普通 Chat 的交接说明</h2><p>将下面说明复制到讨论方案的 Chat 对话中，再说“整理进 INBOX”。</p><textarea id="chat-instructions" readonly aria-label="Chat 交接说明"></textarea></section><section class="panel" id="receipt" hidden><h2>已落地，可交给执行端</h2><textarea id="execution" readonly aria-label="执行端读取指令"></textarea><p>复制这段指令到能够访问本机文件的执行对话中。当前收件器不会自动启动执行任务。</p></section>
<script type="module">
const api=document.querySelector('#api'),tool=document.querySelector('#tool'),mode=document.querySelector('#mode'),toggle=document.querySelector('#toggle'),status=document.querySelector('#result'),handoff=document.querySelector('#handoff'),createClipboard=document.querySelector('#create-from-clipboard'),createPasted=document.querySelector('#create-pasted'),inputSchema=${JSON.stringify(toolSchema())};let automaticEnabled=false, submitting=false;
document.querySelector("#chat-instructions").value=${JSON.stringify(CHAT_INSTRUCTIONS)};
function showReceipt(output){status.textContent="已创建任务卡："+output.absolutePath;status.className="ok";document.querySelector("#receipt").hidden=false;document.querySelector("#execution").value="请读取本机任务卡："+output.absolutePath+"\\n先复述目标、范围、待核实项及下一步，等待我确认后再修改项目。";}

function showMode(){mode.textContent=automaticEnabled?'自动建卡：已开启。明确触发后将写入并通知。':'自动建卡：已暂停。工具调用不会写入。';mode.className=automaticEnabled?'ok':'no';toggle.textContent=automaticEnabled?'暂停自动建卡':'恢复自动建卡';toggle.disabled=false;}
async function syncMode(){const response=await fetch('/v1/inbox-settings');const settings=await response.json();if(!response.ok)throw new Error(settings.error||'读取自动建卡状态失败。');automaticEnabled=settings.automaticEnabled;showMode();}
${parseHandoff.toString()}
async function createTask(input,{signal}={}){if(submitting)throw new Error('已有建卡请求处理中，请等待结果。');submitting=true;try{const response=await fetch('/v1/create-inbox-task',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(input),signal});const output=await response.json();if(!response.ok)throw new Error(output.error||'创建任务卡失败。');showReceipt(output);return output;}finally{submitting=false;}}
toggle.addEventListener('click',async()=>{toggle.disabled=true;try{const response=await fetch('/v1/inbox-settings',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({automaticEnabled:!automaticEnabled})});const settings=await response.json();if(!response.ok)throw new Error(settings.error||'更新自动建卡状态失败。');automaticEnabled=settings.automaticEnabled;showMode();}catch(error){status.textContent='更新自动建卡状态失败：'+(error?.message||String(error));status.className='no';toggle.disabled=false;}});
createPasted.addEventListener('click',async()=>{createPasted.disabled=true;try{status.textContent='正在创建任务卡…';status.className='';const output=await createTask(parseHandoff(handoff.value));showReceipt(output);}catch(error){status.textContent='创建失败：'+(error?.message||String(error));status.className='no';}finally{createPasted.disabled=false;}});
createClipboard.addEventListener('click',async()=>{createClipboard.disabled=true;try{if(!navigator.clipboard?.readText)throw new Error('当前浏览器不允许读取剪贴板；请改用手动粘贴。');handoff.value=await navigator.clipboard.readText();status.textContent='正在创建任务卡…';status.className='';const output=await createTask(parseHandoff(handoff.value));showReceipt(output);}catch(error){status.textContent='创建失败：'+(error?.message||String(error));status.className='no';}finally{createClipboard.disabled=false;}});
try{await syncMode();}catch(error){mode.textContent='自动建卡状态不可用：'+(error?.message||String(error));mode.className='no';}
if(!document.modelContext||typeof document.modelContext.registerTool!=='function'){api.textContent='当前内置浏览器未提供 document.modelContext；可使用下方粘贴入口。';api.className='no';}else{api.textContent='检测到 document.modelContext。正在注册唯一工具…';api.className='ok';try{await document.modelContext.registerTool({name:'${TOOL_NAME}',title:'创建 INBOX 任务卡',description:'仅当用户明确要求整理进 INBOX 时调用。自动建卡开启时，工具会直接新建一张固定 00-INBOX 目录任务卡，并在页面通知结果；不能读取、修改、删除任何现有内容，也不能选择路径。',inputSchema,annotations:{readOnlyHint:false,consequentialHint:true,untrustedContentHint:false},execute:async(input,{signal}={})=>{if(!automaticEnabled){status.textContent='自动建卡已暂停：未创建任务卡。';status.className='no';throw new Error('自动建卡已暂停。');}status.textContent='正在创建任务卡…';status.className='';try{const output=await createTask(input,{signal});showReceipt(output);return output;}catch(error){status.textContent='创建失败：'+(error?.message||String(error));status.className='no';throw error;}}});tool.textContent='唯一工具已注册。自动建卡开启时会写后通知。';tool.className='ok';}catch(error){tool.textContent='工具注册失败：'+(error?.message||String(error));tool.className='no';}}
</script>`;
}
