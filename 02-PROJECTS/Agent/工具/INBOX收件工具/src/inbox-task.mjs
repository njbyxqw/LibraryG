import { randomUUID } from "node:crypto";
import { link, lstat, open, rm, unlink } from "node:fs/promises";
import path from "node:path";

export const DEFAULT_INBOX_ROOT = "/Users/dean/LibraryG/00-INBOX";
export const FORMAT_VERSION = 1;

const STATES = new Set(["讨论", "方案", "待办", "进行中", "阻塞", "完成"]);
const TARGETS = new Set(["LG", "MT", "TS", "跨项目"]);
const OWNERS = new Set(["Chat", "Codex", "用户"]);
const MAX_TITLE_LENGTH = 80;
const MAX_TEXT_LENGTH = 8_000;
const MAX_LIST_ITEMS = 20;
const MAX_LIST_ITEM_LENGTH = 500;

export class InboxTaskValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "InboxTaskValidationError";
  }
}

function requiredText(value, field, maxLength = MAX_TEXT_LENGTH, { allowNewlines = false } = {}) {
  if (typeof value !== "string") {
    throw new InboxTaskValidationError(`${field} 必须是文本。`);
  }

  const trimmed = value.trim();
  if (!trimmed) {
    throw new InboxTaskValidationError(`${field} 不能为空。`);
  }
  if (trimmed.length > maxLength) {
    throw new InboxTaskValidationError(`${field} 超过长度上限。`);
  }
  const forbiddenControls = allowNewlines
    ? /\u0000|[\u0001-\u0008\u000B\u000C\u000E-\u001F\u007F]/u
    : /\u0000|[\u0001-\u001F\u007F]/u;
  if (forbiddenControls.test(trimmed)) {
    throw new InboxTaskValidationError(`${field} 含有不允许的控制字符。`);
  }
  return trimmed;
}

function oneOf(value, field, allowed) {
  const normalized = requiredText(value, field, 20);
  if (!allowed.has(normalized)) {
    throw new InboxTaskValidationError(`${field} 不在允许值中。`);
  }
  return normalized;
}

function optionalList(value, field) {
  if (value === undefined || value === null) {
    return [];
  }
  if (!Array.isArray(value) || value.length > MAX_LIST_ITEMS) {
    throw new InboxTaskValidationError(`${field} 必须是不超过 ${MAX_LIST_ITEMS} 项的列表。`);
  }
  return value.map((item) => requiredText(item, field, MAX_LIST_ITEM_LENGTH));
}

function validateTitle(value) {
  const title = requiredText(value, "title", MAX_TITLE_LENGTH);
  if (/[\\/]/u.test(title) || title.includes("..")) {
    throw new InboxTaskValidationError("title 不能包含路径片段。");
  }
  return title;
}

export function validateInboxTask(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    throw new InboxTaskValidationError("任务必须是对象。");
  }

  const allowed = new Set(['title', 'state', 'target', 'next_owner', 'next_action', 'conclusion', 'facts_to_verify', 'related_links']);
  if (Object.keys(input).some(key => !allowed.has(key))) throw new InboxTaskValidationError('任务包含不支持的字段。');
  return {
    title: validateTitle(input.title),
    state: oneOf(input.state, "state", STATES),
    target: oneOf(input.target, "target", TARGETS),
    nextOwner: oneOf(input.next_owner, "next_owner", OWNERS),
    nextAction: requiredText(input.next_action, "next_action", 500),
    conclusion: requiredText(input.conclusion, "conclusion", MAX_TEXT_LENGTH, { allowNewlines: true }),
    factsToVerify: optionalList(input.facts_to_verify, "facts_to_verify"),
    relatedLinks: optionalList(input.related_links, "related_links")
  };
}

function yamlString(value) {
  return JSON.stringify(value);
}

function quoteBlock(value) {
  return value
    .split(/\r?\n/u)
    .map((line) => `> ${line}`)
    .join("\n");
}

function listBlock(items) {
  return items.length === 0 ? "- 无" : items.map((item) => `- ${item}`).join("\n");
}

function localDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function renderInboxTask(task, { date = new Date() } = {}) {
  const day = localDate(date);
  return `---
title: ${yamlString(task.title)}
type: inbox-task
format_version: ${FORMAT_VERSION}
state: ${yamlString(task.state)}
target: ${yamlString(task.target)}
next_owner: ${yamlString(task.nextOwner)}
next_action: ${yamlString(task.nextAction)}
created: ${day}
updated: ${day}
tags: [inbox, task]
---

# ${task.title}

## 当前结论

${quoteBlock(task.conclusion)}

## 已知事实 / 待核实

${listBlock(task.factsToVerify)}

## 下一步

- [ ] ${task.nextAction}

## 关联

${listBlock(task.relatedLinks)}
`;
}

async function assertExistingDirectory(root) {
  let entry;
  try {
    entry = await lstat(root);
  } catch {
    throw new InboxTaskValidationError("INBOX 根目录不存在或不可访问。");
  }
  if (!entry.isDirectory()) {
    throw new InboxTaskValidationError("INBOX 根路径不是目录。");
  }
}

function candidateFileName(day, title, attempt) {
  const suffix = attempt === 1 ? "" : ` - ${attempt}`;
  return `${day} - ${title}${suffix}.md`;
}

async function writeTemporaryFile(root, content) {
  const temporaryPath = path.join(root, `.${randomUUID()}.inbox-task.tmp`);
  const handle = await open(temporaryPath, "wx", 0o600);
  try {
    await handle.writeFile(content, "utf8");
    await handle.sync();
  } finally {
    await handle.close();
  }
  return temporaryPath;
}

/**
 * The root override is only for in-process tests. Future MCP code must call
 * this function without options, which fixes writes to DEFAULT_INBOX_ROOT.
 */
export async function createInboxTask(input, { root = DEFAULT_INBOX_ROOT, date = new Date(), taskId = randomUUID() } = {}) {
  const task = validateInboxTask(input);
  const resolvedRoot = path.resolve(root);
  await assertExistingDirectory(resolvedRoot);

  const day = localDate(date);
  const content = renderInboxTask(task, { date });
  const temporaryPath = await writeTemporaryFile(resolvedRoot, content);

  try {
    for (let attempt = 1; attempt <= 100; attempt += 1) {
      const fileName = candidateFileName(day, task.title, attempt);
      const finalPath = path.join(resolvedRoot, fileName);
      try {
        await link(temporaryPath, finalPath);
        await unlink(temporaryPath);
        return {
          taskId,
          relativePath: fileName,
          createdAt: date.toISOString()
        };
      } catch (error) {
        if (error?.code !== "EEXIST") {
          throw error;
        }
      }
    }
    throw new InboxTaskValidationError("同名任务过多，无法创建唯一文件。");
  } finally {
    await rm(temporaryPath, { force: true });
  }
}
