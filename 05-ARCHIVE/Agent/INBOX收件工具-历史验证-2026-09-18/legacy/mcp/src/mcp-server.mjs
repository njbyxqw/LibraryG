import { McpServer } from "@modelcontextprotocol/server";
import * as z from "zod/v4";
import { InboxTaskValidationError, createInboxTask } from "../../../src/inbox-task.mjs";

const states = ["讨论", "方案", "待办", "进行中", "阻塞", "完成"];
const targets = ["LG", "MT", "TS", "跨项目"];
const owners = ["Chat", "Codex", "用户"];

const inputSchema = z.object({
  title: z.string().min(1).max(80),
  state: z.enum(states),
  target: z.enum(targets),
  next_owner: z.enum(owners),
  next_action: z.string().min(1).max(500),
  conclusion: z.string().min(1).max(8_000),
  facts_to_verify: z.array(z.string().min(1).max(500)).max(20).optional(),
  related_links: z.array(z.string().min(1).max(500)).max(20).optional()
});

const outputSchema = z.object({
  task_id: z.string().uuid(),
  relative_path: z.string().min(1),
  created_at: z.string().datetime()
});

/**
 * The optional writer injection exists only for local protocol tests. The
 * production entrypoint uses the default writer, whose root is fixed in
 * inbox-task.mjs and cannot be supplied by an MCP caller.
 */
export function createInboxMcpServer({ writeTask = createInboxTask } = {}) {
  const server = new McpServer({
    name: "libraryg-inbox-task-writer",
    version: "0.1.0"
  });

  server.registerTool(
    "create_inbox_task",
    {
      title: "创建 LibraryG INBOX 任务卡",
      description:
        "仅在用户明确要求“整理进 INBOX”“转成待办”或“把方案留档”时调用。只会在固定的 LibraryG/00-INBOX 创建一张新任务卡；不会读取、列出、更新、移动或删除任何文件。",
      inputSchema,
      outputSchema
    },
    async (input) => {
      try {
        const result = await writeTask(input);
        const output = {
          task_id: result.taskId,
          relative_path: result.relativePath,
          created_at: result.createdAt
        };
        return {
          content: [
            {
              type: "text",
              text: `已创建 INBOX 任务卡：${output.relative_path}`
            }
          ],
          structuredContent: output
        };
      } catch (error) {
        const message = error instanceof InboxTaskValidationError
          ? error.message
          : "创建 INBOX 任务卡失败。";
        return { isError: true, content: [{ type: "text", text: message }] };
      }
    }
  );

  return server;
}
