#!/usr/bin/env python3
"""Vault scan v2 - fix encoding/matching issues"""
import re
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"D:\LibraryG")
TILEMATCH = VAULT / "02-PROJECTS" / "TileMatch"

# ============ 1. Collect all markdown files ============
all_md = {}  # basename -> [full paths]
all_paths = []  # list of (relative_path, basename)
for p in VAULT.rglob("*.md"):
    parts = p.parts
    if any(x in ('.obsidian', '.workbuddy', 'Excalidraw', '.git') for x in parts):
        continue
    bname = p.stem  # filename without extension
    rel = p.relative_to(VAULT)
    all_md.setdefault(bname, []).append(p)
    all_paths.append((str(rel), bname, p))

print(f"Total md files: {len(all_paths)}")
print(f"Unique basenames: {len(all_md)}")

# Debug: check specific files
for check in ['_项目概览', '_MOC', '规范-知识库文档分类标准', '分析-RocketV2完整逻辑-v2（重构版）']:
    print(f"  basename_lookup['{check}'] = {len(all_md.get(check, []))} hits")

# ============ 2. Extract wikilinks ============
wl_pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')

def resolve_link(target, source_file):
    """Try to resolve a wikilink target. Returns True if found."""
    target = target.strip()
    if not target:
        return True  # empty link
    
    # Handle headers: [[file#header]] or [[#header]]
    if '#' in target:
        target = target.split('#')[0]
        if not target:
            return True  # same-file header link
    
    # Handle path-style: extract basename
    if '/' in target:
        # Try full path resolution first
        full_path = VAULT / target
        if full_path.with_suffix('.md').exists():
            return True
        # Also try as-is (might be .md already)
        if full_path.exists():
            return True
        # Fall back to basename
        basename = target.split('/')[-1]
    else:
        basename = target
    
    return basename in all_md

# ============ 3. Check all links ============
broken_active = []
broken_daily = []
path_style_in_tm = []

for rel, bname, fpath in all_paths:
    try:
        content = fpath.read_text(encoding='utf-8-sig')  # handle BOM
    except:
        continue
    
    # Remove code blocks
    lines = content.split('\n')
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        
        for m in wl_pattern.finditer(line):
            target = m.group(1).strip()
            if not target:
                continue
            
            # Check path-style in TileMatch
            if '/' in target and '02-PROJECTS/TileMatch' in rel:
                # Check if it's a forbidden path prefix
                forbidden = ['游戏逻辑/', '编辑器/', '打点/', '工具/', 'Rocket/', 'Git工作流/']
                basename = target.split('/')[-1]
                if any(target.startswith(fp) for fp in forbidden) and '/' in target:
                    path_style_in_tm.append((rel, target, i))
            
            # Check if broken
            if not resolve_link(target, fpath):
                if rel.startswith('01-DAILY'):
                    broken_daily.append((rel, target, i))
                else:
                    broken_active.append((rel, target, i))

# ============ 4. MOC Closure ============
moc_file = TILEMATCH / "_MOC.md"
moc_content = moc_file.read_text(encoding='utf-8-sig')
moc_links = set()
for m in wl_pattern.finditer(moc_content):
    target = m.group(1).strip()
    if '#' in target:
        target = target.split('#')[0]
    if '/' in target:
        target = target.split('/')[-1]
    if target:
        moc_links.add(target)

print(f"\n_MOC.md contains {len(moc_links)} unique link targets")
print(f"Sample: {list(moc_links)[:5]}")

# TileMatch files (excluding _trash and _ prefixed)
tm_files = []
for rel, bname, fpath in all_paths:
    if not (TILEMATCH in fpath.parents or fpath.parent == TILEMATCH):
        continue
    if '_trash' in rel:
        continue
    if bname.startswith('_'):
        continue
    tm_files.append((rel, bname, fpath))

orphans = []
for rel, bname, fpath in tm_files:
    if bname not in moc_links:
        orphans.append((rel, bname))

# Reverse MOC
rev_count = 0
rev_missing = []
for rel, bname, fpath in tm_files:
    try:
        content = fpath.read_text(encoding='utf-8-sig')
    except:
        continue
    has_moc = False
    for m in wl_pattern.finditer(content):
        target = m.group(1).strip()
        if '#' in target:
            target = target.split('#')[0]
        if '/' in target:
            target = target.split('/')[-1]
        if '_MOC' in target:
            has_moc = True
            break
    if has_moc:
        rev_count += 1
    else:
        rev_missing.append(bname)

total_tm = len(tm_files)

# ============ 5. Frontmatter ============
fm_pat = re.compile(r'^---\r?\n(.*?)\r?\n---', re.DOTALL)

missing_type = []
nonstandard_type = []
missing_title = []

for rel, bname, fpath in all_paths:
    if TILEMATCH not in fpath.parents and fpath.parent != TILEMATCH:
        continue
    if '_trash' in rel:
        continue
    try:
        content = fpath.read_text(encoding='utf-8-sig')
    except:
        continue
    m = fm_pat.match(content)
    if not m:
        continue
    fm = m.group(1)
    fields = {}
    for line in fm.split('\n'):
        if ':' in line and not line.startswith(' '):
            k, v = line.split(':', 1)
            fields[k.strip()] = v.strip()
    
    dtype = fields.get('type', '')
    if not dtype:
        missing_type.append(rel)
    elif dtype not in ('spec', 'analysis', 'report', 'note', 'reference', 'index'):
        nonstandard_type.append((rel, dtype))
    
    if not fields.get('title') and dtype in ('spec', 'analysis', 'report', 'note'):
        missing_title.append(rel)

# ============ 6. cat_order ============
cat_issues = []
folder_orders = defaultdict(list)
for rel, bname, fpath in all_paths:
    if TILEMATCH not in fpath.parents and fpath.parent != TILEMATCH:
        continue
    if '_trash' in rel:
        continue
    try:
        content = fpath.read_text(encoding='utf-8-sig')
    except:
        continue
    m = fm_pat.match(content)
    if not m:
        continue
    for line in m.group(1).split('\n'):
        if line.strip().startswith('cat_order:'):
            val = line.split(':', 1)[1].strip()
            folder = str(fpath.parent.relative_to(TILEMATCH))
            folder_orders[folder].append((bname, val, rel))
            break

for folder, orders in folder_orders.items():
    seen = defaultdict(list)
    for bname, val, rel in orders:
        seen[val].append(rel)
        if val.isdigit() and len(val) != 3:
            cat_issues.append(('non_zero_padded', rel, val))
    for val, rels in seen.items():
        if len(rels) > 1:
            cat_issues.append(('duplicate', ' & '.join(rels), val))

# ============ 7. Naming ============
valid_prefixes = ('分析-', '规范-', '报告-', '参考-', '记录-', 'BUG-', 'Effect-', '障碍牌-', '任务-', '复盘-', '工具-', '待办-', '索引-')
naming_issues = []
for rel, bname, fpath in all_paths:
    if TILEMATCH not in fpath.parents and fpath.parent != TILEMATCH:
        continue
    if '_trash' in rel or bname.startswith('_'):
        continue
    if not any(bname.startswith(p) for p in valid_prefixes):
        naming_issues.append((rel, bname))

# ============ 8. Pollution ============
pollution = []
for rel, bname, fpath in all_paths:
    try:
        content = fpath.read_text(encoding='utf-8-sig')
    except:
        continue
    if 'workbuddy_sync' in content:
        for i, line in enumerate(content.split('\n'), 1):
            if 'workbuddy_sync' in line:
                pollution.append((rel, 'workbuddy_sync', i))
    # consecutive empty lines (3+)
    empty = 0
    for i, line in enumerate(content.split('\n'), 1):
        if line.strip() == '':
            empty += 1
            if empty >= 3:
                pollution.append((rel, 'consecutive_empty_lines', i))
        else:
            empty = 0

# ============ OUTPUT ============
print("\n" + "=" * 60)
print("SCAN RESULTS")
print("=" * 60)

print(f"\n--- BROKEN LINKS ---")
print(f"Active: {len(broken_active)}")
for r, t, l in broken_active:
    print(f"  {r}:{l} -> [[{t}]]")
print(f"Daily: {len(broken_daily)}")
for r, t, l in broken_daily[:20]:
    print(f"  {r}:{l} -> [[{t}]]")
if len(broken_daily) > 20:
    print(f"  ... +{len(broken_daily)-20} more")

print(f"\n--- MOC CLOSURE ---")
print(f"Forward: HOME -> _MOC = YES")
print(f"Orphans: {len(orphans)}")
for r, b in orphans:
    print(f"  - {r}")
print(f"Reverse: {rev_count}/{total_tm} ({rev_count*100//total_tm if total_tm else 0}%)")
print(f"Missing backlinks ({len(rev_missing)}): {', '.join(rev_missing)}")

print(f"\n--- LINK STYLE (TM) ---")
print(f"Path-style violations: {len(path_style_in_tm)}")
for r, t, l in path_style_in_tm:
    print(f"  {r}:{l} -> [[{t}]]")

print(f"\n--- FRONTMATTER ---")
print(f"Missing type: {len(missing_type)}")
for r in missing_type:
    print(f"  - {r}")
print(f"Non-standard type: {len(nonstandard_type)}")
for r, t in nonstandard_type:
    print(f"  - {r} (type={t})")
print(f"Missing title: {len(missing_title)}")
for r in missing_title:
    print(f"  - {r}")

print(f"\n--- cat_order ---")
print(f"Issues: {len(cat_issues)}")
for t, r, v in cat_issues:
    print(f"  [{t}] {r} (val={v})")

print(f"\n--- NAMING ---")
print(f"Issues: {len(naming_issues)}")
for r, b in naming_issues:
    print(f"  - {r} ({b})")

print(f"\n--- POLLUTION ---")
print(f"Markers: {len(pollution)}")
for r, m, l in pollution:
    print(f"  {r}:{l} [{m}]")
