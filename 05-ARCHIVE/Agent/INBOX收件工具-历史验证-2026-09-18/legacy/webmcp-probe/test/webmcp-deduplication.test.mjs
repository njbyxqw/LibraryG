import assert from "node:assert/strict";
import test from "node:test";
import { mkdtemp, readdir, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";

import { createDeduplicatingTaskCreator } from "../src/task-receipt.mjs";

const task = {
  title: "D2 重复调用测试", state: "方案", target: "LG", next_owner: "用户",
  next_action: "确认重复调用不会建第二张卡", conclusion: "同一受限任务输入只能创建一张卡。"
};

test("D2 相同任务在同一探针进程只创建一次", async () => {
  const root = await mkdtemp(path.join(tmpdir(), "libraryg-webmcp-dedup-"));
  try {
    const createTask = createDeduplicatingTaskCreator({ root });
    const first = await createTask(task);
    const replay = await createTask({ ...task });
    assert.equal(first.reused, false);
    assert.equal(replay.reused, true);
    assert.equal(replay.taskId, first.taskId);
    assert.deepEqual(await readdir(root), [first.relativePath]);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
