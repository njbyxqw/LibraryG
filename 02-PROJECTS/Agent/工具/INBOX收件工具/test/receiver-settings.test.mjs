import assert from "node:assert/strict";
import test from "node:test";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";

import { readReceiverSettings, writeReceiverSettings } from "../src/receiver-settings.mjs";

test("自动建卡默认开启，暂停状态跨重启保留", async () => {
  const directory = await mkdtemp(path.join(tmpdir(), "libraryg-receiver-settings-"));
  const settingsFile = path.join(directory, "settings.json");
  try {
    assert.equal((await readReceiverSettings(settingsFile)).automaticEnabled, true);
    await writeReceiverSettings(settingsFile, false);
    assert.equal((await readReceiverSettings(settingsFile)).automaticEnabled, false);
  } finally { await rm(directory, { recursive: true, force: true }); }
});
