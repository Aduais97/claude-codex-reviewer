"""Per-variant compositor (SPEC §6.4, §8 step 9).

Only the Pillow-RGBA text plate changes per variant; it is overlaid onto the
near-lossless intermediate. Scene-level composites re-emit INTERMEDIATE
(crf 12) so that delivery compression happens exactly once, in assemble.py
(M11). Text presets: fade_up and stagger_words via per-overlay timed alpha
fades — each staggered line is its own overlay input.
"""

import os
from PIL import Image, ImageDraw, ImageFilter

from . import CANVAS
from . import typeset, layout
from .base_motion import ff, INTERMEDIATE, duration_of

W, H = CANVAS
DELIVERY = ["-c:v", "h264_videotoolbox", "-b:v", "12M",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart"]


def line_plate(text, role, color_rgb, y_frac, shadow=False):
    """Full-canvas RGBA plate holding one centred tracked line at y_frac,
    auto-fit per M10 (shrink toward floor, else wrap to two lines)."""
    lines, scale = layout.fit_role(text, role, W)
    layout.assert_inside_type_safe(y_frac, role)
    plate = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    line_h = None
    for i, line in enumerate(lines):
        img, _ = typeset.set_line(line, role, W, color_rgb, scale)
        line_h = line_h or int(img.height * 0.92)
        x = (W - img.width) // 2
        y = int(y_frac * H) - img.height // 2 + i * line_h
        plate.alpha_composite(img, (x, y))
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sh.paste((0, 0, 0, 110), (0, 4), plate.split()[3])
        return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), plate)
    return plate


def composite(base, overlays, out_path, encode=None, audio=None):
    """overlays: list of dicts {png, t_in, fade, t_out?, rise?}.
    Each is looped, alpha-faded in at t_in (fade_up = slight downward-origin
    rise), and overlaid. encode defaults to INTERMEDIATE (M11) — pass
    DELIVERY only for a single-scene reel with no assembly step."""
    encode = encode or INTERMEDIATE
    # -t bound is load-bearing: looped PNG inputs are INFINITE streams —
    # without an explicit output duration the mux never stops (verified
    # runaway: 123MB / 213 CPU-min for a 3.2s clip).
    dur = duration_of(base)
    args = ["-i", base]
    fc, prev = [], "0:v"
    for i, ov in enumerate(overlays, start=1):
        args += ["-loop", "1", "-i", ov["png"]]
        t_in, fade = ov.get("t_in", 0.0), ov.get("fade", 0.35)
        chain = f"format=rgba,fade=t=in:st={t_in}:d={fade}:alpha=1"
        if ov.get("t_out") is not None:
            chain += f",fade=t=out:st={ov['t_out']:.2f}:d={fade}:alpha=1"
        fc.append(f"[{i}:v]{chain}[ov{i}]")
        rise = ov.get("rise", 0)
        y_expr = (f"'if(lt(t,{t_in}+{fade}),{rise}*(1-min((t-{t_in})/{fade},1)),0)'"
                  if rise else "0")
        fc.append(f"[{prev}][ov{i}]overlay=0:{y_expr}[v{i}]")
        prev = f"v{i}"
    args += ["-filter_complex", ";".join(fc), "-map", f"[{prev}]",
             "-t", f"{dur:.3f}"]
    if audio:
        args += ["-i", audio, "-map", f"{len(overlays) + 1}:a",
                 "-c:a", "aac", "-b:a", "192k"]
    return ff(args + encode + [out_path], os.path.basename(out_path))
