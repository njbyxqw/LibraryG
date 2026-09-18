// Serialized into the local page as well as exercised directly by tests.
export function parseHandoff(value) {
  let text = value.trim();
  if (!text) throw new Error('请先粘贴任务交接包。');
  const fence = String.fromCharCode(96).repeat(3);
  if (text.startsWith(fence)) {
    const lines = text.split(/\r?\n/);
    if (!/^```(?:json)?$/i.test(lines[0].trim()) || lines.at(-1).trim() !== fence) {
      throw new Error('请复制完整的 JSON 代码块。');
    }
    text = lines.slice(1, -1).join('\n');
  }
  let input;
  try { input = JSON.parse(text); } catch { throw new Error('任务交接包必须是 JSON；请只复制代码块内容。'); }
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('任务交接包必须是一个对象。');
  return input;
}

export const CHAT_INSTRUCTIONS = `当我明确说“整理进 INBOX”时，把本次已确认结论整理成一张任务卡。仅讨论的内容用“讨论”，已形成方案用“方案”，明确安排执行用“待办”。不要把未确认假设写成事实。
如果本对话确实具有 create_inbox_task 工具，调用一次，只有收到成功回执才能说已入库；失败后不要自动重试。
没有该工具时，只输出下面格式的 JSON 代码块，明确说“待导入本地”，不要生成下载文件或声称已写入 INBOX。
{
  "title": "简短标题（不含路径斜杠）",
  "state": "方案",
  "target": "LG",
  "next_owner": "用户",
  "next_action": "下一步",
  "conclusion": "完整方案：目标、范围、关键决策、验收要求；保留未决问题",
  "facts_to_verify": [],
  "related_links": []
}
state 仅选：讨论、方案、待办、进行中、阻塞、完成；target 仅选 LG、MT、TS、跨项目；next_owner 仅选 Chat、Codex、用户。conclusion 最多 8000 字符，超出先说明，不静默截断。不得添加其他字段。创建任务卡不代表授权自动执行项目修改。`;
