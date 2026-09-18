import { mkdir, open, readFile, rename, rm } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import path from "node:path";

const VERSION = 1;

export async function readReceiverSettings(settingsFile) {
  try {
    const parsed = JSON.parse(await readFile(settingsFile, "utf8"));
    if (parsed?.version !== VERSION || typeof parsed.automaticEnabled !== "boolean") throw new Error("invalid settings");
    return parsed;
  } catch (error) {
    if (error?.code === "ENOENT") return { version: VERSION, automaticEnabled: true };
    throw new Error("自动建卡设置损坏，已暂停启动以避免非预期写入。");
  }
}

export async function writeReceiverSettings(settingsFile, automaticEnabled) {
  const directory = path.dirname(settingsFile);
  await mkdir(directory, { recursive: true, mode: 0o700 });
  const temporary = path.join(directory, `.${randomUUID()}.settings.tmp`);
  const handle = await open(temporary, "wx", 0o600);
  try {
    await handle.writeFile(`${JSON.stringify({ version: VERSION, automaticEnabled }, null, 2)}\n`, "utf8");
    await handle.sync();
  } finally { await handle.close(); }
  try { await rename(temporary, settingsFile); } finally { await rm(temporary, { force: true }); }
  return { version: VERSION, automaticEnabled };
}
