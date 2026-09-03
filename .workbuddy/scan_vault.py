#!/usr/bin/env python3
"""Vault comprehensive scan - read only analysis"""
import os
import re
import json
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"D:\LibraryG")
TILEMATCH = VAULT / "02-PROJECTS" / "TileMatch"

# ============ 1. Collect all markdown files and basenames ============
all_md_files = {}
for root, dirs, files in os.walk(VAULT):
    # Skip .obsidian, .workbuddy, Excalidraw
    parts = Path(root).parts
    if any(p in ('.obsidian', '.workbuddy', 'Excalidraw', '.git') for p in parts):
        continue
    for f in files:
        if f.endswith('.md'):
            fpath = Path(root) / f
            basename = f[:-4]  # without .md
            all_md_files[fpath] = basename

# Build basename -> filepath lookup
basename_lookup = defaultdict(list)
for fpath, bname in all_md_files.items():
    basename_lookup[bname].append(fpath)

# ============ 2. Extract all wikilinks from all files ============
wikilink_pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
code_block_pattern = re.compile(r'```[\s\S]*?```', re.MULTILINE)
inline_code_pattern = re.compile(r'`[^`]+`')

all_links = []  # (source_file, target_text, line_num)
broken_links = []  # (source_file, target_text, line_num)
path_style_links = []  # links with / in target (path-style)

for fpath, bname in all_md_files.items():
    try:
        content = fpath.read_text(encoding='utf-8')
    except:
        continue
    
    # Remove code blocks
    content_no_code = code_block_pattern.sub('', content)
    # Remove inline code
    content_no_code = inline_code_pattern.sub('', content_no_code)
    
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Skip code block lines
        if line.strip().startswith('```'):
            continue
        
        for m in wikilink_pattern.finditer(line):
            target = m.group(1).strip()
            all_links.append((str(fpath), target, i))
            
            # Check if path-style (contains /)
            if '/' in target:
                # Extract basename from path
                basename = target.split('/')[-1]
                rel_to_vault = fpath.relative_to(VAULT)
                path_style_links.append((str(rel_to_vault), target, i))
                # Still check if basename exists
                if basename not in basename_lookup:
                    broken_links.append((str(fpath.relative_to(VAULT)), target, i))
            else:
                # Direct basename
                if target not in basename_lookup:
                    broken_links.append((str(fpath.relative_to(VAULT)), target, i))

# ============ 3. MOC Closure ============
# Forward: HOME -> _MOC -> docs
moc_file = TILEMATCH / "_MOC.md"
home_file = VAULT / "HOME.md"

# Check HOME -> _MOC link
home_content = home_file.read_text(encoding='utf-8')
home_has_moc = '_MOC' in home_content

# Get all wikilinks from _MOC
moc_content = moc_file.read_text(encoding='utf-8')
moc_links = set()
for m in wikilink_pattern.finditer(moc_content):
    target = m.group(1).strip()
    if '/' in target:
        target = target.split('/')[-1]
    moc_links.add(target)

# Find orphans (files in TileMatch not linked from _MOC and not _MOC itself)
tilematch_files = {}
for fpath, bname in all_md_files.items():
    if TILEMATCH in fpath.parents or fpath.parent == TILEMATCH:
        tilematch_files[bname] = fpath

orphans = []
for bname, fpath in tilematch_files.items():
    if bname.startswith('_'):
        continue  # Skip _MOC, _项目概览 etc
    if bname not in moc_links:
        # Also check if it's in _trash
        rel = fpath.relative_to(TILEMATCH)
        if '_trash' in str(rel):
            continue
        orphans.append((str(rel), bname))

# Reverse: docs with [[_MOC]] backlink
reverse_moc_count = 0
reverse_moc_missing = []
for bname, fpath in tilematch_files.items():
    if bname.startswith('_'):
        continue
    if '_trash' in str(fpath.relative_to(TILEMATCH)):
        continue
    try:
        content = fpath.read_text(encoding='utf-8')
    except:
        continue
    # Check for [[_MOC]] or [[..._MOC...]] backlink
    has_moc_backlink = False
    for m in wikilink_pattern.finditer(content):
        target = m.group(1).strip()
        if '/' in target:
            target = target.split('/')[-1]
        if '_MOC' in target:
            has_moc_backlink = True
            break
    if has_moc_backlink:
        reverse_moc_count += 1
    else:
        reverse_moc_missing.append(bname)

total_tm_docs = len([b for b in tilematch_files if not b.startswith('_') and '_trash' not in str(tilematch_files[b].relative_to(TILEMATCH))])

# ============ 4. Link Style Check ============
# Path-style links in TileMatch area
path_style_in_tm = []
for src, target, line in path_style_links:
    if '02-PROJECTS/TileMatch' in src:
        path_style_in_tm.append((src, target, line))

# ============ 5. Frontmatter Check ============
fm_pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL)

fm_issues = []
for fpath, bname in all_md_files.items():
    if '_trash' in str(fpath.relative_to(VAULT)) if TILEMATCH in fpath.parents else False:
        continue
    try:
        content = fpath.read_text(encoding='utf-8')
    except:
        continue
    
    m = fm_pattern.match(content)
    if not m:
        continue  # No FM - skip for now, focus on docs that have FM
    
    fm_text = m.group(1)
    
    # Parse FM fields
    fm_fields = {}
    current_key = None
    for line in fm_text.split('\n'):
        if ':' in line and not line.startswith(' '):
            key, val = line.split(':', 1)
            fm_fields[key.strip()] = val.strip()
            current_key = key.strip()
    
    # Check type field
    doc_type = fm_fields.get('type', '')
    
    # Only check TileMatch docs (skip daily, templates, etc)
    if TILEMATCH in fpath.parents or fpath.parent == TILEMATCH:
        rel = fpath.relative_to(TILEMATCH)
        if '_trash' in str(rel):
            continue
        
        # Check for missing type
        if not doc_type:
            fm_issues.append(('missing_type', str(rel), bname))
        elif doc_type not in ('spec', 'analysis', 'report', 'note', 'reference', 'index', 'record', 'tool', 'bug-record', 'bug-log', 'task', 'guide', '参考'):
            fm_issues.append(('nonstandard_type', str(rel), f"type={doc_type}"))
        
        # Check for missing title
        if not fm_fields.get('title') and doc_type in ('spec', 'analysis', 'report', 'note'):
            fm_issues.append(('missing_title', str(rel), bname))

# ============ 6. cat_order Check ============
cat_order_issues = []
folder_orders = defaultdict(list)
for fpath, bname in all_md_files.items():
    if TILEMATCH not in fpath.parents and fpath.parent != TILEMATCH:
        continue
    rel = fpath.relative_to(TILEMATCH)
    if '_trash' in str(rel):
        continue
    try:
        content = fpath.read_text(encoding='utf-8')
    except:
        continue
    m = fm_pattern.match(content)
    if not m:
        continue
    fm_text = m.group(1)
    for line in fm_text.split('\n'):
        if line.strip().startswith('cat_order:'):
            val = line.split(':', 1)[1].strip()
            folder = str(fpath.parent.relative_to(TILEMATCH))
            folder_orders[folder].append((bname, val, str(rel)))
            break

# Check for duplicates and non-zero-padded
for folder, orders in folder_orders.items():
    seen = defaultdict(list)
    for bname, val, rel in orders:
        seen[val].append(rel)
        # Check zero-padding (should be 3 digits)
        if val.isdigit() and len(val) != 3:
            cat_order_issues.append(('non_zero_padded', rel, val))
    for val, rels in seen.items():
        if len(rels) > 1:
            cat_order_issues.append(('duplicate', ' & '.join(rels), val))

# ============ 7. Naming Check ============
naming_issues = []
valid_prefixes = ('分析-', '规范-', '报告-', '参考-', '记录-', 'BUG-', 'Effect-', '障碍牌-', '任务-', '复盘-', '工具-', '待办-')
for fpath, bname in all_md_files.items():
    if TILEMATCH not in fpath.parents and fpath.parent != TILEMATCH:
        continue
    rel = fpath.relative_to(TILEMATCH)
    if '_trash' in str(rel):
        continue
    if bname.startswith('_'):
        continue  # _MOC, _项目概览 etc are OK
    
    has_valid_prefix = any(bname.startswith(p) for p in valid_prefixes)
    if not has_valid_prefix:
        # Check if it's an index file
        if bname.startswith('索引-') or bname == '知识库文档顺序索引':
            pass  # index files are OK
        else:
            naming_issues.append(('no_prefix', str(rel), bname))

# ============ 8. Pollution Check ============
pollution_markers = ['workbuddy_sync', 'TODO:', 'FIXME:', 'PLACEHOLDER', '{{', 'XXX']
pollution_issues = []
for fpath, bname in all_md_files.items():
    try:
        content = fpath.read_text(encoding='utf-8')
    except:
        continue
    for marker in pollution_markers:
        if marker in content:
            # Check context - ignore if in code block
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if marker in line and not line.strip().startswith('```'):
                    # Skip if it's a legitimate use
                    if marker == '{{' and ('Excalidraw' in str(fpath) or 'template' in str(fpath).lower()):
                        continue
                    if marker == 'workbuddy_sync':
                        pollution_issues.append((str(fpath.relative_to(VAULT)), 'workbuddy_sync', i))
                    elif marker == 'TODO:' and line.strip().startswith('- [ ]'):
                        continue  # legitimate task
                    elif marker in ('TODO:', 'FIXME:', 'PLACEHOLDER', 'XXX'):
                        pollution_issues.append((str(fpath.relative_to(VAULT)), marker, i))
    
    # Check for consecutive empty lines (3+)
    empty_count = 0
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if line.strip() == '':
            empty_count += 1
            if empty_count >= 3:
                pollution_issues.append((str(fpath.relative_to(VAULT)), 'consecutive_empty_lines', i))
        else:
            empty_count = 0

# ============ OUTPUT ============
print("=" * 60)
print("VAULT COMPREHENSIVE SCAN REPORT")
print("=" * 60)

print(f"\nTotal markdown files: {len(all_md_files)}")
print(f"TileMatch docs (excl _trash): {total_tm_docs}")

print("\n" + "=" * 60)
print("1. BROKEN LINKS")
print("=" * 60)
# Separate active vs daily logs
active_broken = []
daily_broken = []
for src, target, line in broken_links:
    if '01-DAILY' in src:
        daily_broken.append((src, target, line))
    else:
        active_broken.append((src, target, line))

print(f"\nTotal broken links: {len(broken_links)}")
print(f"  Active docs: {len(active_broken)}")
print(f"  Daily logs: {len(daily_broken)}")

print("\n--- Active broken links ---")
for src, target, line in active_broken:
    print(f"  {src}:{line} -> [[{target}]]")

print("\n--- Daily log broken links (first 15) ---")
for src, target, line in daily_broken[:15]:
    print(f"  {src}:{line} -> [[{target}]]")
if len(daily_broken) > 15:
    print(f"  ... and {len(daily_broken) - 15} more")

print("\n" + "=" * 60)
print("2. MOC CLOSURE")
print("=" * 60)
print(f"\nForward: HOME -> _MOC link: {'YES' if home_has_moc else 'NO'}")
print(f"Orphans (not linked from _MOC): {len(orphans)}")
for rel, bname in orphans:
    print(f"  - {rel} ({bname})")

print(f"\nReverse MOC backlinks: {reverse_moc_count}/{total_tm_docs} ({reverse_moc_count*100//total_tm_docs if total_tm_docs else 0}%)")
print(f"Missing backlinks: {len(reverse_moc_missing)}")
if reverse_moc_missing:
    print(f"  (showing first 20): {', '.join(reverse_moc_missing[:20])}")
    if len(reverse_moc_missing) > 20:
        print(f"  ... and {len(reverse_moc_missing) - 20} more")

print("\n" + "=" * 60)
print("3. LINK STYLE (path-based in TileMatch)")
print("=" * 60)
print(f"\nPath-style links in TileMatch: {len(path_style_in_tm)}")
for src, target, line in path_style_in_tm:
    print(f"  {src}:{line} -> [[{target}]]")

print("\n" + "=" * 60)
print("4. FRONTMATTER ISSUES")
print("=" * 60)
missing_types = [x for x in fm_issues if x[0] == 'missing_type']
nonstandard_types = [x for x in fm_issues if x[0] == 'nonstandard_type']
missing_titles = [x for x in fm_issues if x[0] == 'missing_title']

print(f"\nMissing type: {len(missing_types)}")
for _, rel, bname in missing_types:
    print(f"  - {rel}")

print(f"\nNon-standard type: {len(nonstandard_types)}")
for _, rel, info in nonstandard_types:
    print(f"  - {rel} ({info})")

print(f"\nMissing title: {len(missing_titles)}")
for _, rel, bname in missing_titles:
    print(f"  - {rel}")

print("\n" + "=" * 60)
print("5. cat_order ISSUES")
print("=" * 60)
print(f"\nTotal issues: {len(cat_order_issues)}")
for issue_type, rel, val in cat_order_issues:
    print(f"  [{issue_type}] {rel} (cat_order={val})")

print("\n" + "=" * 60)
print("6. NAMING ISSUES")
print("=" * 60)
print(f"\nFiles without valid prefix: {len(naming_issues)}")
for _, rel, bname in naming_issues:
    print(f"  - {rel} ({bname})")

print("\n" + "=" * 60)
print("7. POLLUTION CHECK")
print("=" * 60)
# Deduplicate
unique_pollution = set()
for src, marker, line in pollution_issues:
    unique_pollution.add((src, marker, line))
print(f"\nTotal pollution markers: {len(unique_pollution)}")
for src, marker, line in sorted(unique_pollution):
    print(f"  {src}:{line} [{marker}]")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Broken links (active): {len(active_broken)}")
print(f"Broken links (daily): {len(daily_broken)}")
print(f"Orphans: {len(orphans)}")
print(f"Reverse MOC: {reverse_moc_count}/{total_tm_docs} ({reverse_moc_count*100//total_tm_docs if total_tm_docs else 0}%)")
print(f"Path-style links (TM): {len(path_style_in_tm)}")
print(f"Missing type: {len(missing_types)}")
print(f"Non-standard type: {len(nonstandard_types)}")
print(f"Missing title: {len(missing_titles)}")
print(f"cat_order issues: {len(cat_order_issues)}")
print(f"Naming issues: {len(naming_issues)}")
print(f"Pollution markers: {len(unique_pollution)}")
