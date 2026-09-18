import assert from "node:assert/strict";
import { mkdtemp, readFile, readdir, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  InboxTaskValidationError,
  createInboxTask,
  renderInboxTask,
  validateInboxTask
} from "../src/inbox-task.mjs";

const fixedDate = new Date("2026-09-17T09:00:00.000Z");

function validInput(overrides = {}) {
  return {
    title: "测试 INBOX 任务",
    state: "方案",
    target: "TS",
    next_owner: "Codex",
    next_action: "查当前实现。",
    conclusion: "先确认当前实现是否符合方案。",
    facts_to_verify: ["入口是否存在。"],
    related_links: ["[[02-PROJECTS/TileScape/_MOC]]"],
    ...overrides
  };
}

async function withTemporaryInbox(run) {
  const root = await mkdtemp(path.join(os.tmpdir(), "libraryg-inbox-test-"));
  try {
    await run(root);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

test("valid task creates exactly one task card", async () => {
  await withTemporaryInbox(async (root) => {
    const result = await createInboxTask(validInput(), { root, date: fixedDate });
    const entries = await readdir(root);
    const content = await readFile(path.join(root, result.relativePath), "utf8");

    assert.deepEqual(entries, ["2026-09-17 - 测试 INBOX 任务.md"]);
    assert.match(content, /^type: inbox-task$/m);
    assert.match(content, /^state: "方案"$/m);
    assert.match(content, /## 当前结论/);
    assert.match(content, /## 已知事实 \/ 待核实/);
  });
});

test("same title never overwrites an existing task card", async () => {
  await withTemporaryInbox(async (root) => {
    const first = await createInboxTask(validInput(), { root, date: fixedDate });
    const second = await createInboxTask(validInput({ conclusion: "第二张卡。" }), {
      root,
      date: fixedDate
    });
    const firstContent = await readFile(path.join(root, first.relativePath), "utf8");
    const secondContent = await readFile(path.join(root, second.relativePath), "utf8");

    assert.equal(first.relativePath, "2026-09-17 - 测试 INBOX 任务.md");
    assert.equal(second.relativePath, "2026-09-17 - 测试 INBOX 任务 - 2.md");
    assert.match(firstContent, /先确认当前实现/);
    assert.match(secondContent, /第二张卡/);
  });
});

test("path fragments and invalid enums are rejected before writing", async () => {
  await withTemporaryInbox(async (root) => {
    await assert.rejects(
      () => createInboxTask(validInput({ title: "../outside" }), { root, date: fixedDate }),
      InboxTaskValidationError
    );
    await assert.rejects(
      () => createInboxTask(validInput({ state: "ready" }), { root, date: fixedDate }),
      InboxTaskValidationError
    );
    assert.deepEqual(await readdir(root), []);
  });
});

test("renderer keeps untrusted text out of frontmatter", () => {
  const task = validateInboxTask(
    validInput({ conclusion: "---\nstate: 完成\n---\n仅作为任务正文。" })
  );
  const content = renderInboxTask(task, { date: fixedDate });

  assert.match(content, /^state: "方案"$/m);
  assert.match(content, /> state: 完成/);
});
