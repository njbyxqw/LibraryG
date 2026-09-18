import assert from "node:assert/strict";
import test from "node:test";

import { renderWebMcpInboxPage } from "../src/webmcp-inbox-page.mjs";

test("生产页面不把真实写入描述为临时测试", () => {
  const page = renderWebMcpInboxPage();
  assert.match(page, /自动建卡：已开启/);
  assert.match(page, /暂停自动建卡/);
  assert.match(page, /\/v1\/inbox-settings/);
  assert.match(page, /固定 00-INBOX 目录/);
  assert.match(page, /保底：从 Chat 交接包创建/);
  assert.match(page, /parseHandoff/);
  assert.match(page, /create-pasted/);
  assert.match(page, /create-from-clipboard/);
  assert.match(page, /navigator\.clipboard\?\.readText/);
  assert.doesNotMatch(page, /window\.confirm/);
  assert.doesNotMatch(page, /测试任务卡/);
});
