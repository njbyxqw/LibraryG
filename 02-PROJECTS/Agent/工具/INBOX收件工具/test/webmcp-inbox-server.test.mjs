import assert from "node:assert/strict";
import { mkdir, mkdtemp, readdir, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { createWebMcpInboxServer } from "../src/webmcp-inbox-server.mjs";

test("生产收件接口接受与粘贴交接包相同的受限字段", async () => {
  const directory = await mkdtemp(path.join(tmpdir(), "libraryg-webmcp-server-"));
  const inbox = path.join(directory, "00-INBOX");
  const settingsFile = path.join(directory, "settings.json");
  await mkdir(inbox);
  const server = createWebMcpInboxServer({ root: inbox, settingsFile });
  try {
    await new Promise((resolve, reject) => {
      server.once("error", reject);
      server.listen(0, "127.0.0.1", () => {
        server.off("error", reject);
        resolve();
      });
    });
    const port = server.address().port;
    const response = await fetch(`http://127.0.0.1:${port}/v1/create-inbox-task`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        title: "粘贴交接包测试",
        state: "方案",
        target: "LG",
        next_owner: "用户",
        next_action: "确认交接结果。",
        conclusion: "同一受限接口同时服务于 WebMCP 和粘贴入口。"
      })
    });

    const output = await response.json();
    assert.equal(response.status, 201, output.error);
    assert.deepEqual(await readdir(inbox), [output.relativePath]);
    assert.equal(output.absolutePath, path.join(inbox, output.relativePath));
    const settingsResponse = await fetch(`http://127.0.0.1:${port}/v1/inbox-settings`, {
      method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify({automaticEnabled:false})
    });
    assert.equal(settingsResponse.status, 200);
    const blocked = await fetch(`http://127.0.0.1:${port}/v1/create-inbox-task`, {
      method:'POST', headers:{'content-type':'application/json'}, body:'{}'
    });
    assert.equal(blocked.status,400);
    assert.match((await blocked.json()).error,/暂停/);
    assert.deepEqual(await readdir(inbox), [output.relativePath]);
  } finally {
    await new Promise((resolve) => server.close(resolve));
    await rm(directory, { recursive: true, force: true });
  }
});
