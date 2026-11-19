"""B1/B2 asset gate (SPEC §6.2 gate 1, §8 step 1).

Every source must have native short side >= 1080 and must not be one of the
two rejected AI clips (path or SHA-256). The render fails loudly rather than
upscale — the 480x848 clip silently blows up 2.25x into clean h264 otherwise.
"""

import os, json, hashlib, subprocess

MIN_SHORT_SIDE = 1080

BLACKLIST_SHA256 = {
    "799ff1f00f7a1c364902a50efae1732e4aa56c7188fd98ecb1f214f5ca88018d",  # 480x848
    "09e06ed2e62a52dec2c6046ee6cefbbc5afbb5e5af00d4ec780fbb7cc1aaae79",  # 848x480
}
BLACKLIST_PATH_FRAGMENTS = ("/Soeurs/reference/",)

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".heic", ".webp"}


class GateError(SystemExit):
    pass


def sha256_of(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def native_dims(path):
    if os.path.splitext(path)[1].lower() in IMAGE_EXT:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", path],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise GateError(f"ASSET GATE: cannot probe {path}")
    for s in json.loads(r.stdout).get("streams", []):
        if s.get("codec_type") == "video":
            return int(s["width"]), int(s["height"])
    raise GateError(f"ASSET GATE: no video stream in {path}")


def assert_source_ok(path):
    """Raise GateError unless `path` is a legal render source."""
    real = os.path.realpath(os.path.expanduser(path))
    if not os.path.exists(real):
        raise GateError(f"ASSET GATE: missing source {path}")
    for frag in BLACKLIST_PATH_FRAGMENTS:
        if frag in real:
            raise GateError(
                f"ASSET GATE: {path} is under a blacklisted path ({frag}) — "
                f"the rejected AI clips and their derivatives are banned (SPEC B2)")
    if sha256_of(real) in BLACKLIST_SHA256:
        raise GateError(
            f"ASSET GATE: {path} is a blacklisted AI clip by SHA-256 (SPEC B2)")
    w, h = native_dims(real)
    if min(w, h) < MIN_SHORT_SIDE:
        raise GateError(
            f"ASSET GATE: {os.path.basename(path)} is {w}x{h}; native short side "
            f"< {MIN_SHORT_SIDE}. Upscaling is banned (SPEC B2). Reshoot or exclude.")
    return real


# Scene readiness (SPEC §4.5): which scene types can render given the assets
# actually present in the movie definition.
SCENE_REQUIREMENTS = {
    "cold_open_hook":  ["macro_or_still"],
    "product_reveal":  ["styled_still"],
    "oil_ritual":      ["macro"],
    "scent_notes":     [],                       # pure type — RENDERABLE-NOW
    "sisters_duo":     [],                       # pure-type/logo variants only
    "claim_card":      [],                       # pure type for substantiated lines
    "firelight_mood":  ["styled_still_or_macro"],
    "range_teaser":    [],                       # pure-type/logo variants only
    "endcard_cta":     ["logo_asset"],
    "transition_beat": [],
}


def readiness_map(assets):
    have = {
        "styled_still": bool(assets.get("styled_still")),
        "logo_asset": bool(assets.get("logo_asset")),
        "macro": bool(assets.get("macro")),
    }
    have["macro_or_still"] = have["macro"] or have["styled_still"]
    have["styled_still_or_macro"] = have["macro_or_still"]
    return {
        scene: ("RENDERABLE-NOW" if all(have.get(r) for r in reqs)
                else "BLOCKED-ON-SHOOT")
        for scene, reqs in SCENE_REQUIREMENTS.items()
    }
