import { createHash } from "node:crypto";

import { createInboxTask, validateInboxTask } from "../../../src/inbox-task.mjs";

function receiptKey(input) {
  const task = validateInboxTask(input);
  return createHash("sha256").update(JSON.stringify(task)).digest("hex");
}

/**
 * D2 replay protection is deliberately local to one probe process. It derives
 * its key from validated task data, so no root, filename, or receipt ID is
 * exposed to the model or WebMCP schema.
 */
export function createDeduplicatingTaskCreator({ root }) {
  const receipts = new Map();
  return async (input) => {
    const key = receiptKey(input);
    const existing = receipts.get(key);
    if (existing) return { ...existing, reused: true };

    const created = await createInboxTask(input, { root });
    const result = { ...created, reused: false };
    receipts.set(key, result);
    return result;
  };
}
