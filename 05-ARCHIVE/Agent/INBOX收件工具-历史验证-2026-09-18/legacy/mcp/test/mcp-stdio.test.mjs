import assert from "node:assert/strict";
import { mkdtemp, readdir, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { Client } from "@modelcontextprotocol/client";
import { StdioClientTransport } from "@modelcontextprotocol/client/stdio";

function validInput() {
  return {
    title: "MCP 协议测试",
    state: "方案",
    target: "TS",
    next_owner: "Codex",
    next_action: "查当前实现。",
    conclusion: "先确认当前实现是否符合方案。",
    facts_to_verify: ["入口是否存在。"],
    related_links: ["[[02-PROJECTS/TileScape/_MOC]]"]
  };
}

test("历史 MCP stdio 只暴露建卡工具，并只写临时 INBOX", async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), "libraryg-inbox-test-"));
  const client = new Client({ name: "libraryg-inbox-test", version: "0.1.0" });
  const fixturePath = path.join(process.cwd(), "legacy", "mcp", "fixtures", "stdio-fixture.mjs");
  const transport = new StdioClientTransport({ command: process.execPath, args: [fixturePath, root], stderr: "pipe" });

  try {
    await client.connect(transport);
    const { tools } = await client.listTools();
    assert.deepEqual(tools.map((tool) => tool.name), ["create_inbox_task"]);

    const result = await client.callTool({ name: "create_inbox_task", arguments: validInput() });
    assert.equal(result.isError, undefined);
    assert.match(result.content[0].text, /MCP 协议测试/);
    assert.deepEqual(await readdir(root), [result.structuredContent.relative_path]);
    assert.match(result.structuredContent.relative_path, /^\d{4}-\d{2}-\d{2} - MCP 协议测试\.md$/u);
  } finally {
    await client.close();
    await rm(root, { recursive: true, force: true });
  }
});
