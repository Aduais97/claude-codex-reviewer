"""Scene assembly (SPEC §6.1): xfade concat of composited scene
INTERMEDIATES into the finished reel — the single delivery encode happens
here (M11). Un-signed composite reviews get a burned-in DRAFT bar so an
unreviewed reel cannot be mistaken for a publishable one (M2).
"""

from .base_motion import ff, duration_of
from .compose import DELIVERY


def concat_xfade(clips, out_path, transition="fade", tdur=0.3, draft=True):
    args = []
    for c in clips:
        args += ["-i", c]
    fc, prev, offset = [], "0:v", 0.0
    for i in range(1, len(clips)):
        offset += duration_of(clips[i - 1]) - tdur
        fc.append(f"[{prev}][{i}:v]xfade=transition={transition}"
                  f":duration={tdur}:offset={offset:.3f}[x{i}]")
        prev = f"x{i}"
    if draft:
        fc.append(f"[{prev}]drawbox=x=0:y=ih-16:w=iw:h=16:color=red@0.55:t=fill[vd]")
        prev = "vd"
    if not fc:  # single clip, publishable — pure remux would skip the draft bar
        fc.append(f"[0:v]null[vn]")
        prev = "vn"
    args += ["-filter_complex", ";".join(fc), "-map", f"[{prev}]"]
    return ff(args + DELIVERY + [out_path],
              f"assemble {len(clips)} scene(s){' DRAFT' if draft else ''}")
