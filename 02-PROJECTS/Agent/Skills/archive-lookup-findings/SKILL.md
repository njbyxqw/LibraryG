---
name: archive-lookup-findings
description: Archive verified, reusable project lookup findings from the current conversation. Use when the user says "整理对话", "归档本次查找", "沉淀定位结论", or asks to preserve discovered paths, localization keys, configuration locations, asset replacement entry points, or reference relationships for future lookup. Apply across projects; do not use for general meeting summaries or implementation reports.
---

# Archive Lookup Findings

## Workflow

1. Review the current conversation and archive each verified finding that fits the inclusion rules below.
2. Exclude items listed in the exclusion rules. Mark a retained uncertainty as **待验证**.
3. Use LibraryG as the primary archive. Read its `02-PROJECTS/Agent/Memory.md` and the active project MOC, then locate the matching project section under `02-PROJECTS/`.
4. Update or create the project-level lookup index in LibraryG. For TileScape, use `02-PROJECTS/TileScape/参考/快速定位与资源替换索引.md`; for another project, follow that project's MOC and naming convention. Update the project MOC when a new stable index is created.
5. Use an in-repository `Docs/` report only as a project-side execution reference when the user explicitly requests one; it is never the primary long-term archive.
6. Update an existing entry when it covers the same key, config, or asset; otherwise append a concise entry. Use project-relative paths.
7. Preserve the distinction between runtime references and definitions that exist only in backups, generated files, or unused resources.
8. Record a brief entry in the current LibraryG Daily when the archival task creates or materially updates a stable index, following the vault's Daily convention.
9. Report the entries added or updated and link the LibraryG record.

## Inclusion Rules

Archive these findings:

1. **Localization key**: definition file, actual runtime consumer, displayed meaning, parameter placeholders, and related keys. Archive an explicit “no runtime reference found” result too, including whether it exists only in a backup or generated resource.
2. **Configuration**: runtime data file, readable source/backup, generated type, loading API, primary consumer, ID/field meaning, trigger condition, and any important mismatch between comment and implementation.
3. **Resource or Prefab**: source asset path, consuming Prefab/UI/script, replacement entry point, dependency that must remain compatible (Sprite name, Animator, material, Spine data, etc.), and the smallest validation path.
4. **UI or feature entry**: Prefab path, controller/script path, public opening API, the concrete business callers, and nearby but easily confused UI/resources.
5. **Reference relationship**: a reusable chain such as `config → loader → presenter → Prefab`, or `asset → controller → UI`. Keep only the shortest chain that resolves future lookup.
6. **Negative/compatibility finding**: confirmed unused code/resource, backup-only definition, shared prefab impact scope, generated file restriction, or a known cross-system side effect.

Do not archive these by themselves:

- a raw search result without a conclusion;
- broad implementation analysis, design alternatives, or meeting discussion;
- one-off error logs, temporary paths, and transient test output;
- a fact already covered by an unchanged report entry;
- guesses that have not been checked against the workspace.

## Entry Format

Use the fields that apply:

```markdown
### `<name / key / asset>`

- **运行时路径 / 定义位置**：
- **实际引用**：
- **作用与触发条件**：
- **相近 key / 配置**：
- **资源替换入口 / 关联资源**：
- **结论与注意事项**：
```

Do not modify game code or resources while archiving unless the user separately asks for that change.
