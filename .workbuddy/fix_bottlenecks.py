#!/usr/bin/env python3
"""Batch fix vault bottlenecks - with diff preview"""
from pathlib import Path
import re

VAULT = Path(r"D:\LibraryG")
TILEMATCH = VAULT / "02-PROJECTS" / "TileMatch"

fixes_applied = []
fixes_errors = []

# ===== 1. Add type: reference to 18 障碍牌 files =====
barrier_files = [
    "障碍牌-Butterfly", "障碍牌-CandyBottle", "障碍牌-CandyCube系列",
    "障碍牌-CardBox", "障碍牌-Clock", "障碍牌-Flip", "障碍牌-JokerFlip",
    "障碍牌-LightBulb", "障碍牌-Ore系列", "障碍牌-Rocket", "障碍牌-ShellBox",
    "障碍牌-SlotMachine", "障碍牌-SodaBox", "障碍牌-SuitCase", "障碍牌-Switch",
    "障碍牌-Thief", "障碍牌-TrafficLights", "障碍牌-Volcano"
]
barrier_dir = TILEMATCH / "游戏逻辑" / "局内障碍" / "障碍牌"

for bfile in barrier_files + ["报告-blockerdda分支调控逻辑变更排查"]:
    # Check main dir first, then barrier dir
    fpath = barrier_dir / f"{bfile}.md"
    if bfile == "报告-blockerdda分支调控逻辑变更排查":
        fpath = barrier_dir / f"{bfile}.md"
    if not fpath.exists():
        fixes_errors.append(f"NOT FOUND: {fpath}")
        continue
    
    content = fpath.read_text(encoding='utf-8-sig')
    # Insert type: reference after 'date:' line, or before '---' if no date
    if 'type:' not in content.split('---')[1] if '---' in content else False:
        fm_end = content.index('---', 4)
        fm = content[:fm_end + 3]
        # Find last non-empty line before second ---
        fm_lines = fm.split('\n')
        # Insert type before closing ---
        new_fm_lines = fm_lines[:-1] + ['type: reference'] + [fm_lines[-1]]
        new_fm = '\n'.join(new_fm_lines)
        new_content = new_fm + content[fm_end + 3:]
        
        # Show diff
        old_type_check = 'type:' in fm
        print(f"[FIX] {bfile}: add type: reference")
        fixes_applied.append(f"障碍牌/{bfile}: add type: reference")
        
        fpath.write_text(new_content, encoding='utf-8')
    else:
        print(f"[SKIP] {bfile}: already has type field")

# ===== 2. Fix 障碍牌-特殊机制.md =====
special_file = barrier_dir / "障碍牌-特殊机制.md"
if special_file.exists():
    content = special_file.read_text(encoding='utf-8-sig')
    if 'type:' not in content.split('---')[1]:
        fm_end = content.index('---', 4)
        fm = content[:fm_end + 3]
        fm_lines = fm.split('\n')
        new_fm_lines = fm_lines[:-1] + ['type: reference'] + [fm_lines[-1]]
        new_fm = '\n'.join(new_fm_lines)
        new_content = new_fm + content[fm_end + 3:]
        print(f"[FIX] 障碍牌-特殊机制: add type: reference")
        fixes_applied.append("障碍牌/障碍牌-特殊机制: add type: reference")
        special_file.write_text(new_content, encoding='utf-8')

# ===== 3. Fix cat_order issues =====
# 3a. 游戏逻辑\局内道具\Shuffle改造AB测试方案.md: cat_order 7 -> 007
shuffle_file = TILEMATCH / "游戏逻辑" / "局内道具" / "Shuffle改造AB测试方案.md"
if shuffle_file.exists():
    content = shuffle_file.read_text(encoding='utf-8-sig')
    if 'cat_order: 7\n' in content:
        content = content.replace('cat_order: 7\n', 'cat_order: 007\n')
        shuffle_file.write_text(content, encoding='utf-8')
        print(f"[FIX] Shuffle改造AB测试方案: cat_order 7 → 007")
        fixes_applied.append("cat_order: Shuffle改造AB测试方案 7→007")

# 3b. 编辑器\报告-单牌块牌底配置功能实现记录-v1.md: cat_order 12 -> 012
paidi_file = TILEMATCH / "编辑器" / "报告-单牌块牌底配置功能实现记录-v1.md"
if paidi_file.exists():
    content = paidi_file.read_text(encoding='utf-8-sig')
    if 'cat_order: 12\n' in content:
        content = content.replace('cat_order: 12\n', 'cat_order: 012\n')
        paidi_file.write_text(content, encoding='utf-8')
        print(f"[FIX] 报告-单牌块牌底配置: cat_order 12 → 012")
        fixes_applied.append("cat_order: 单牌块牌底 12→012")

# 3c. Fix duplicate cat_order in 编辑器/
# 复盘-牌底笔刷功能开发.md: cat_order 001 → 002 (or swap with 规范-本地扩展开发)
fupan_file = TILEMATCH / "编辑器" / "复盘-牌底笔刷功能开发.md"
guifan_local_file = TILEMATCH / "编辑器" / "规范-本地扩展开发.md"
if fupan_file.exists() and guifan_local_file.exists():
    fupan_content = fupan_file.read_text(encoding='utf-8-sig')
    # Check current values
    if 'cat_order: 001' in fupan_content:
        fupan_content = fupan_content.replace('cat_order: 001', 'cat_order: 002')
        fupan_file.write_text(fupan_content, encoding='utf-8')
        print(f"[FIX] 复盘-牌底笔刷: cat_order 001 → 002")
        fixes_applied.append("cat_order: 复盘-牌底笔刷 001→002")
    elif 'cat_order: 002' in fupan_content:
        print(f"[SKIP] 复盘-牌底笔刷: already 002")

# 3d. Fix duplicate cat_order in 游戏逻辑/其他/
# 分析-AssignTileTypeByDepth分池打乱策略-v1.md and 分析-死局逻辑与改进方案-v1.md both have 003
siju_file = TILEMATCH / "游戏逻辑" / "其他" / "分析-死局逻辑与改进方案-v1.md"
if siju_file.exists():
    content = siju_file.read_text(encoding='utf-8-sig')
    if 'cat_order: 003' in content:
        content = content.replace('cat_order: 003', 'cat_order: 004')
        siju_file.write_text(content, encoding='utf-8')
        print(f"[FIX] 分析-死局逻辑: cat_order 003 → 004")
        fixes_applied.append("cat_order: 死局逻辑 003→004")

# ===== 4. Fix _MOC BUG chapter path-style links =====
moc_file = TILEMATCH / "_MOC.md"
if moc_file.exists():
    content = moc_file.read_text(encoding='utf-8-sig')
    old1 = '[[游戏逻辑/BUG/BUG-临时汇总|临时汇总'
    new1 = '[[BUG-临时汇总|临时汇总'
    old2 = '[[游戏逻辑/BUG/BUG-AssignTileTypeByDepth-单花色越界崩溃-v1|单花色越界崩溃]]'
    new2 = '[[BUG-AssignTileTypeByDepth-单花色越界崩溃-v1|单花色越界崩溃]]'
    
    if old1 in content and old2 in content:
        content = content.replace(old1, new1)
        content = content.replace(old2, new2)
        moc_file.write_text(content, encoding='utf-8')
        print(f"[FIX] _MOC.md: BUG chapter 2 path-style links → basename")
        fixes_applied.append("_MOC: 2 path-style links fixed")
    else:
        print(f"[SKIP] _MOC BUG links: already fixed or not found")
        if old1 not in content:
            print(f"  old1 not found")
        if old2 not in content:
            print(f"  old2 not found")

# ===== 5. Clean HOME.md workbuddy_sync references =====
home_file = VAULT / "HOME.md"
if home_file.exists():
    content = home_file.read_text(encoding='utf-8-sig')
    if 'workbuddy_sync' in content:
        # Line 62 area
        content = content.replace(
            '3. **同步**: 确保重要的笔记标记了 `workbuddy_sync: true`',
            '3. **同步**: 确保工作产出已记录到每日日志中'
        )
        # Line 72 area
        content = content.replace(
            '| 每日笔记 | `04-TEMPLATES/tp-daily.md` | 日常工作记录 | `date`, `workbuddy_sync` |',
            '| 每日笔记 | `04-TEMPLATES/tp-daily.md` | 日常工作记录 | `date`, `tags` |'
        )
        home_file.write_text(content, encoding='utf-8')
        print(f"[FIX] HOME.md: 2 workbuddy_sync references cleaned")
        fixes_applied.append("HOME.md: workbuddy_sync ×2 cleaned")
    else:
        print(f"[SKIP] HOME.md: no workbuddy_sync found")

# ===== 6. Clean HOME-冷启动指南.md workbuddy_sync =====
lengqidong_file = VAULT / "HOME-冷启动指南.md"
if lengqidong_file.exists():
    content = lengqidong_file.read_text(encoding='utf-8-sig')
    if 'workbuddy_sync' in content:
        # Find and remove the workbuddy_sync line (only report if actually changed)
        lines = content.split('\n')
        new_lines = []
        changed = False
        for line in lines:
            if 'workbuddy_sync' in line and '废弃' not in line:
                new_lines.append(line.replace('`workbuddy_sync: true`', '~~`workbuddy_sync: true`（已废弃）~~'))
                changed = True
            else:
                new_lines.append(line)
        if changed:
            content = '\n'.join(new_lines)
            lengqidong_file.write_text(content, encoding='utf-8')
            print(f"[FIX] HOME-冷启动指南: workbuddy_sync → 标记为已废弃")
            fixes_applied.append("HOME-冷启动指南: workbuddy_sync marked deprecated")
        else:
            print(f"[SKIP] HOME-冷启动指南: workbuddy_sync already deprecated")
    else:
        print(f"[SKIP] HOME-冷启动指南: no workbuddy_sync")

# ===== 7. Add [[_MOC]] backlinks to docs missing them (dynamic detection) =====
# Mirror scan_vault_v2.py reverse-MOC check: any TileMatch doc (non-_trash, non-_) that
# links to no _MOC (top-level or sub-MOC) gets a backlink appended. Replaces the former
# hardcoded 12-file list so new docs are auto-covered every run.
def _has_moc_backlink(content):
    for m in re.finditer(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content):
        if '_MOC' in m.group(1).strip():
            return True
    return False

for fpath in sorted(TILEMATCH.rglob("*.md")):
    rel = str(fpath.relative_to(VAULT))
    if '_trash' in rel:
        continue
    if fpath.stem.startswith('_'):
        continue
    try:
        content = fpath.read_text(encoding='utf-8-sig')
    except:
        continue
    if _has_moc_backlink(content):
        continue

    label = str(fpath.relative_to(TILEMATCH))
    if '## 关联' in content:
        content = content.replace('\n## 关联', '\n## 关联\n\n- [[_MOC|TileMatch 知识库 MOC]]')
    else:
        content = content.rstrip() + '\n\n---\n\n## 关联\n\n- [[_MOC|TileMatch 知识库 MOC]]\n'
    fpath.write_text(content, encoding='utf-8')
    print(f"[FIX] {label}: added [[_MOC]] backlink")
    fixes_applied.append(f"MOC backlink: {label}")

# ===== Summary =====
print(f"\n{'='*60}")
print(f"TOTAL FIXES: {len(fixes_applied)}")
print(f"ERRORS: {len(fixes_errors)}")
if fixes_errors:
    for e in fixes_errors:
        print(f"  ERROR: {e}")
