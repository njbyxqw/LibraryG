#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 CSV 第二列(lv_name)按"格式"分组，每组输出一个独立 CSV。
默认：[lv_id, lv_name] 两列。

可调项（改下面的 CONFIG 即可）：
  - INPUT_PATH : 源 CSV 路径
  - OUTPUT_DIR : 输出目录
  - MODE       : "literal"  后缀字面分组(每种后缀=1组)
                 "semantic" 语义家族分组(base/AB实验变体/子关变体/障碍变体/其他)
                 "two"      仅分 有后缀 / 无后缀
  - ENCODING   : 源文件编码（已确认 gb18030）
"""

import csv
import os
import re
from collections import defaultdict, OrderedDict

# ============================== CONFIG ==============================
INPUT_PATH = r"C:\Users\Administrator\Desktop\20260717_103150_64174_nwki3.csv"
OUTPUT_DIR = r"D:\meatloaf_client01\lvname_grouped"
MODE = "literal"          # literal | semantic | two
SRC_ENCODING = "gb18030"
OUT_ENCODING = "utf-8-sig"
# ===================================================================

COL_LV_ID = 0     # 第一列 lv_id (Level_ID)
COL_LV_NAME = 1   # 第二列 lv_name (Level)


def detect_group(name, mode):
    """根据 lv_name 与模式返回组名。"""
    name = name.strip()
    m = re.match(r"^(\d+)(.*)$", name)
    suffix = m.group(2) if m else name

    if mode == "two":
        return "base" if not suffix else "with_suffix"

    if mode == "semantic":
        if not suffix:
            return "01_主线(base)"
        if suffix.startswith("_tile"):
            return "04_障碍变体"
        if re.match(r"^_\d+$", suffix):
            return "03_子关变体"
        if suffix.startswith("_ab"):
            return "02_AB实验变体"
        return "05_其他"

    # literal（默认）
    return "base" if not suffix else suffix


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    groups = defaultdict(list)   # group -> list of (lv_id, lv_name)
    order = OrderedDict()        # 记录首次出现顺序
    total = 0

    with open(INPUT_PATH, "r", encoding=SRC_ENCODING, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)  # 跳过表头
        for row in reader:
            if len(row) <= COL_LV_NAME:
                continue
            lv_id = row[COL_LV_ID].strip()
            lv_name = row[COL_LV_NAME].strip()
            if not lv_name:
                continue
            total += 1
            g = detect_group(lv_name, MODE)
            if g not in order:
                order[g] = True
            groups[g].append((lv_id, lv_name))

    # 输出每个组一个 CSV
    written = []
    for g in order:
        rows = groups[g]
        # 文件名安全化：前缀 group_ + 组名(下划线保留)
        safe = re.sub(r"[^\w\-]", "_", g)
        fname = f"group_{safe}.csv"
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "w", encoding=OUT_ENCODING, newline="") as out:
            w = csv.writer(out)
            w.writerow(["lv_id", "lv_name"])
            w.writerows(rows)
        written.append((g, len(rows), fname))

    # 控制台汇总
    print(f"源文件: {INPUT_PATH}")
    print(f"模式: {MODE}   总条数: {total}   组数: {len(written)}")
    print(f"{'组名':<14}{'条数':>6}  文件")
    print("-" * 50)
    for g, cnt, fname in written:
        print(f"{g:<14}{cnt:>6}  {fname}")
    print(f"\n已写出到目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
