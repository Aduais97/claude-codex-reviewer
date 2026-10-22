"""Base motion -> near-lossless intermediate, once per scent (SPEC §6.4, M11).

Crop to 9:16 FIRST, then zoompan — never squash. The intermediate is
libx264 crf 12 (near-lossless); delivery compression happens exactly once,
in compose.py. Pure-type beds are the only RENDERABLE-NOW base today.
"""

import os, time, json, subprocess
from PIL import Image, ImageDraw, ImageFilter

from . import CANVAS, FPS
from . import assets_gate, palette

W, H = CANVAS
INTERMEDIATE = ["-c:v", "libx264", "-preset", "slow", "-crf", "12",
                "-pix_fmt", "yuv420p"]


def ff(args, desc=""):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-y"] + args
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    ok = r.returncode == 0
    print(f"  [{'OK' if ok else 'FAIL'} {time.time()-t0:.1f}s] {desc}")
    if not ok:
        for line in r.stderr.strip().split("\n")[-4:]:
            print(f"    ! {line}")
    return ok


def duration_of(path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json",
                        "-show_format", path], capture_output=True, text=True)
    return float(json.loads(r.stdout)["format"]["duration"])


def pure_type_bed(out_path, dur, bg_token="ember_espresso", vignette=True):
    """RENDERABLE-NOW bed: flat brand dark + gentle vignette. No assets."""
    color = palette.TOKENS[bg_token].replace("#", "0x")
    vf = "vignette=PI/5" if vignette else "null"
    return ff(["-f", "lavfi", "-i", f"color=c={color}:s={W}x{H}:r={FPS}",
               "-vf", vf, "-t", str(dur)] + INTERMEDIATE + [out_path],
              f"pure_type bed ({bg_token}, {dur}s)")


def light_sweep_png(path, width_frac=0.22):
    """Soft diagonal rose_gold_highlight band for blend=screen sweeps."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    band = int(W * width_frac)
    r, g, b = palette.rgb("rose_gold_highlight")
    for i in range(band):
        a = int(90 * (1 - abs(i - band / 2) / (band / 2)))
        d.line([(i, 0), (i - H // 3, H)], fill=(r, g, b, a))
    img = img.filter(ImageFilter.GaussianBlur(18))
    img.save(path)
    return path


def still_motion(src, out_path, dur, zoom=(1.0, 1.06), pan=0.0,
                 grade=True, purpose="draft"):
    """Ken Burns push_in on a real still -> intermediate. Asset-gated."""
    palette.assert_not_hero(purpose)
    src = assets_gate.assert_source_ok(src)
    frames = int(dur * FPS)
    z0, z1 = zoom
    z_rate = (z1 - z0) / max(frames, 1)
    frac_s = max(0.01, 0.5 - pan / 2)
    # crop to 9:16 FIRST (SPEC §4.4), then zoompan
    crop = f"crop='min(iw,ih*{W}/{H})':'min(ih,iw*{H}/{W})'"
    zp = (f"zoompan=z='if(eq(on,0),{z0:.3f},min(zoom+{z_rate:.7f},{z1:.3f}))'"
          f":x='(iw-iw/zoom)*({frac_s:.4f}+{pan:.4f}*on/{frames})'"
          f":y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}")
    warm = (",colortemperature=4600,colorbalance=rm=0.04:bm=-0.03,vignette=PI/5"
            if grade else "")
    return ff(["-loop", "1", "-i", src, "-vf", f"{crop},{zp}{warm},format=yuv420p",
               "-t", str(dur)] + INTERMEDIATE + [out_path],
              f"still_motion {os.path.basename(src)} ({dur}s)")
