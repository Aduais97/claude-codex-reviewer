#!/usr/bin/env python3
"""File Oct-Nov 2026 HOTC raw guard logs + media from the Drive export into the
canonical Operations tree. Idempotent (skips same-size existing files).

Drive day folder -> TREE/<month>/<week>/<ops_day>/
  - Untitled document.docx -> Raw Guard Log.docx
  - all other files (media) copied flat into the day folder
"""
import os, json, glob, shutil, re

HOME = os.path.expanduser('~')
TREE = os.path.join(HOME, 'Desktop/ASG/Operations/Clients/HOTC/2026')
STAGE = os.path.join(HOME, 'Desktop/Dev/Claude/scripts/hotc/data/hotc_octnov2026')

DAY_RE = re.compile(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) \d+')

def drive_day_dir(src):
    """Outermost ancestor dir named like a day folder (child of a Week folder)."""
    parts = src.split(os.sep)
    for i, p in enumerate(parts):
        if p.startswith('Week ') and i + 1 < len(parts) and DAY_RE.match(parts[i + 1]):
            return os.sep.join(parts[:i + 2])
    raise ValueError('no day dir for ' + src)

def copy(src, dst):
    if os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src):
        return False
    shutil.copy2(src, dst)
    return True

def main():
    total_files = copied = 0
    for mapf in sorted(glob.glob(os.path.join(STAGE, '*', '_daymap.json'))):
        for day in json.load(open(mapf)):
            src = day['src']
            ddir = drive_day_dir(src)
            out = os.path.join(TREE, day['month'], day['week'], day['ops_day'])
            os.makedirs(out, exist_ok=True)
            n_copied = 0
            for root, _dirs, files in os.walk(ddir):
                for f in files:
                    if f.startswith('.'):
                        continue
                    sp = os.path.join(root, f)
                    name = 'Raw Guard Log.docx' if f == 'Untitled document.docx' else f
                    total_files += 1
                    if copy(sp, os.path.join(out, name)):
                        n_copied += 1
            copied += n_copied
            print(f"{day['ops_day']:<28} -> {day['month']}/{day['week']}  ({n_copied} new)")
    print(f'\n{copied} files copied ({total_files} seen).')

if __name__ == '__main__':
    main()
