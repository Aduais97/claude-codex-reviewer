"""Fan-out CLI (SPEC §8 steps 4 & 10).

  python3 -m soeurs_reels.cli movie.json

Loads the movie definition, prints the readiness map, runs every gate, and
renders all RENDERABLE-NOW variants: today that is the pure-type
`scent_notes` pipeline (notes ladder) crossed with substantiated
`claim_card` lines — N scents x M claims -> N*M draft reels, proving the
fan-out before the shoot lands (SPEC §8 step 4).
"""

import os, sys, json, tempfile

from . import CANVAS
from . import assets_gate, palette, layout, legal_gate, base_motion, compose, assemble

W, H = CANVAS


def build_scent_notes_clip(scent, workdir):
    """SPEC §4.5.4: notes ladder as staggered kinetic type on ember, plus the
    scent name (hook #1 Notes Ladder ends on it). RENDERABLE-NOW."""
    dur = 3.2
    bed = os.path.join(workdir, f"bed_notes_{scent['slug']}.mp4")
    if not base_motion.pure_type_bed(bed, dur):
        sys.exit("FATAL: bed render failed")

    color = palette.rgb("text_on_dark")
    ys = (0.30, 0.42, 0.54)
    overlays = []
    for i, note in enumerate(scent["notes"][:3]):
        png = os.path.join(workdir, f"note_{scent['slug']}_{i}.png")
        compose.line_plate(f"{note}.", "note_word", color, ys[i]).save(png)
        overlays.append({"png": png, "t_in": 0.30 + i * 0.55, "fade": 0.40,
                         "rise": 26})
    name_png = os.path.join(workdir, f"name_{scent['slug']}.png")
    compose.line_plate(scent["name"], "scent_name", color, 0.68).save(name_png)
    overlays.append({"png": name_png, "t_in": 2.05, "fade": 0.45, "rise": 30})

    clip = os.path.join(workdir, f"scene_notes_{scent['slug']}.mp4")
    if not compose.composite(bed, overlays, clip):
        sys.exit("FATAL: scent_notes composite failed")
    return clip


def build_claim_card_clip(claim_key, claim_text, scent, workdir):
    """SPEC §4.5.6: one confident substantiated line, pure type."""
    dur = 2.2
    bed = os.path.join(workdir, f"bed_claim_{claim_key}.mp4")
    if not base_motion.pure_type_bed(bed, dur):
        sys.exit("FATAL: bed render failed")
    png = os.path.join(workdir, f"claim_{claim_key}.png")
    compose.line_plate(claim_text, "claim_line", palette.rgb("text_on_dark"),
                       0.42).save(png)
    eyebrow = os.path.join(workdir, f"eyebrow_{scent['slug']}.png")
    compose.line_plate("PERFUME OIL · 10ML", "eyebrow_label",
                       palette.rgb("text_muted"), 0.52).save(eyebrow)
    clip = os.path.join(workdir, f"scene_claim_{claim_key}.mp4")
    overlays = [{"png": png, "t_in": 0.25, "fade": 0.35, "rise": 24},
                {"png": eyebrow, "t_in": 0.75, "fade": 0.35}]
    if not compose.composite(bed, overlays, clip):
        sys.exit("FATAL: claim_card composite failed")
    return clip


def main(movie_path):
    movie = json.load(open(movie_path))
    out_dir = os.path.expanduser(movie["render"]["out_dir"])
    os.makedirs(out_dir, exist_ok=True)
    workdir = os.path.join(tempfile.gettempdir(), "soeurs_reels_work")
    os.makedirs(workdir, exist_ok=True)

    # palette sanity (SPEC §4.2 legibility rules)
    problems = palette.check_legibility()
    if problems:
        sys.exit("PALETTE: " + "; ".join(problems))

    print("scene readiness (SPEC §6.2 gate 1):")
    ready = assets_gate.readiness_map(movie.get("assets", {}))
    for scene, state in ready.items():
        print(f"  {state:16s} {scene}")

    registry = dict(movie["gates"]["substantiation_registry"])
    registry["_house_names"] = movie["legal"].get("house_names", [])
    target = movie.get("publish_target", "organic")

    rendered = []
    for scent in movie["scents"]:
        scent["slug"] = scent["name"].lower().replace("'", "").replace(" ", "_")

        # gates 2-4+6 on the notes-ladder tokens (draft allowance surfaces
        # the pending tm_clearance instead of silently passing it)
        tokens = ([{"text": f"{n}."} for n in scent["notes"]]
                  + [{"text": scent["name"]}])
        pending = legal_gate.check_variant(tokens, scent, registry, target,
                                           allow_draft=True)
        for p in pending:
            print(f"  PENDING (draft only): {p}")

        notes_clip = build_scent_notes_clip(scent, workdir)

        for claim_key, claim_text in movie["claim_lines"].items():
            legal_gate.check_variant([{"text": claim_text,
                                       "claim_key": claim_key}],
                                     scent, registry, target, allow_draft=True)
            claim_clip = build_claim_card_clip(claim_key, claim_text, scent,
                                               workdir)
            draft = not legal_gate.composite_signed(movie)
            name = f"{'DRAFT_' if draft else ''}{scent['slug']}_notes_{claim_key}.mp4"
            out = os.path.join(out_dir, name)
            if assemble.concat_xfade([notes_clip, claim_clip], out, draft=draft):
                rendered.append(out)

    print(f"\nfan-out complete: {len(rendered)} reels -> {out_dir}")
    for r in rendered:
        print(f"  {os.path.basename(r)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
