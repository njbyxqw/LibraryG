import assert from "node:assert/strict";
import test from "node:test";

import { TOOL_NAME, renderWebMcpProbePage } from "../src/webmcp-probe-server.mjs";

test("D1 页面只声明最终建卡工具，不含额外读写能力", () => {
  const page = renderWebMcpProbePage();
  assert.match(page, new RegExp(`name:'${TOOL_NAME}'`));
  assert.match(page, /document\.modelContext\.registerTool/);
  assert.match(page, /consequentialHint:true/);
  assert.match(page, /window\.confirm/);
  assert.match(page, /id="result"/);
  assert.match(page, /output\.reused/);
  assert.match(page, /\/v1\/create-inbox-task/);
  assert.doesNotMatch(page, /inbox_receiver_status/);
  assert.doesNotMatch(page, /getInboxTasks/);
  assert.doesNotMatch(page, /\/Users\/dean\/LibraryG\/00-INBOX/);
  assert.doesNotMatch(page, /root:/);
});
