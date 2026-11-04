---
name: localization-config
description: Create and maintain TileMatch-style multilingual localization rows when the user asks for game localization, multilingual copy, translation configuration, or invokes $localization-config. Preserve the fixed 11-language schema and append completed rows to the established local workbook. Do not use for generic software locale debugging or code-only internationalization work.
---

# Localization Config

Produce localization content in the user's established format and keep the local workbook current.

## Stable sources

- Resolve the current device's LibraryG root from the active workspace and its `AGENTS.md`. When reading this shared copy, resolve symlinks first, then ascend four levels from the directory containing `SKILL.md` to reach the vault root. Do not reuse another device's absolute path.
- Workflow specification, relative to that root: `02-PROJECTS/TileMatch/参考/规范-多语言配置任务与本地工作表.md`
- Local append-only workbook, relative to that root: `02-PROJECTS/TileMatch/参考/附件/多语言配置工作表.xlsx`
- Online reference sheet: `https://docs.google.com/spreadsheets/d/1SM3zfMYbMUhxzCw9mETgAQV0wkld9uQlDaJnZjT1rBE/edit?gid=951765346#gid=951765346`

Read the workflow specification before handling a localization task when the file is available. Treat the online sheet as read-only: it may be consulted for existing terminology or context, but must never be edited.

## Required schema

Keep this exact field order:

`en`, `zh`, `zht`, `fr`, `de`, `ja`, `ko`, `pt`, `es`, `it`, `ru`

These columns are English, Simplified Chinese, Traditional Chinese, French, German, Japanese, Korean, Portuguese, Spanish, Italian, and Russian.

Do not add, remove, rename, or reorder columns unless the user explicitly changes the schema.

## Workflow

1. Use the supplied English content as `en`, then preserve placeholders, markup, escape sequences, numbers, and game-specific terminology in every translation.
2. Translate for natural in-game usage rather than mechanically mirroring source syntax. Do not invent missing product context; flag material ambiguity briefly.
3. Return the completed rows in a compact table or tab-separated block using the exact schema order. Follow an explicit output format from the user when provided.
4. Append one row per configuration item to the first empty row of the local workbook. Preserve existing rows, formatting, sheet structure, and column order. Use the spreadsheet workflow for `.xlsx` edits and verify the saved result.
5. If the workbook or specification is unavailable, still provide the localization output and clearly report that the local append was not completed. Do not create a competing replacement workbook elsewhere.

Do not commit or push LibraryG changes without explicit user authorization.
