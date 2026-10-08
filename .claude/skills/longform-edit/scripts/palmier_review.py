"""Composited review sheet straight from Palmier: source-second picks → timeline frames (via data.ts SEGMENTS +
offset) → inspect_timeline → labelled contact sheets in out/lf01/palmier/review/. Run after `graphics`.
   python3 palmier_review.py            # the standard 20 moments
   python3 palmier_review.py 5.0 46.5   # ad-hoc source seconds"""
import sys, os, shutil, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import palmier as pm
from PIL import Image, ImageDraw
P = pm.Palmier() if hasattr(pm, "Palmier") else pm
src = open("src/LF01/data.ts").read(); dec = json.JSONDecoder()
SEG = dec.raw_decode(src[src.index("export const SEGMENTS = ") + len("export const SEGMENTS = "):])[0]
OFFSET = json.load(open("work/lf01/work/palmier_state.json"))["offset"]
def s2tl(t):
    for s in SEG:
        if s["srcS"] <= t < s["srcE"]: return OFFSET + 2 * int(round(s["from"] + (t - s["srcS"]) * 30))
    return None
STD = [("montage", None, 200), ("intro box", 5.0, None), ("Anthropic lane", 13.0, None), ("AGI is here B", 41.8, None),
       ("AGI strip", 47.2, None), ("IQ B", 49.8, None), ("roadmap xl-B", 56.0, None), ("arc3 capture", 71.5, None),
       ("access R", 85.4, None), ("jobs-hl capture", 241.5, None), ("hiring strip", 291.2, None), ("creds hero", 364.2, None),
       ("CTA lane", 377.0, None), ("chapter 1", 489.6, None), ("Microsoft stamp + bets", 1147.5, None), ("EF stamp", 1175.4, None),
       ("creators two-up", 1364.8, None), ("LinkedIn/TikTok cloud", 1368.0, None), ("creators photo", 1373.2, None), ("recap", 1480.0, None)]
picks = [(f"{t}", float(t), None) for t in sys.argv[1:]] or STD
os.makedirs("out/lf01/palmier/review", exist_ok=True)
tiles = []
for name, t, tl in picks:
    f = tl if tl is not None else s2tl(t)
    if f is None: print(f"skip {name}: src {t} not in his cut"); continue
    r = P.call("inspect_timeline", {"startFrame": f, "endFrame": f + 1, "maxFrames": 1})
    if isinstance(r, list): r = next((x for x in r if isinstance(x, dict) and x.get("image")), {})
    img = r.get("image") if isinstance(r, dict) else None
    if not img or not os.path.exists(img): print(f"no frame for {name} @ {f}: {str(r)[:120]}"); continue
    out = f"out/lf01/palmier/review/f{f:06d}.png"; shutil.move(img, out)
    tiles.append((f"{name} · tl {f} ({f/60:.1f}s)" + (f" · src {t}" if t else ""), out)); print("saved", name, f)
# contact sheets, 3 x 3 per sheet at 640 px tiles
W = 640; cols = 3
for si in range(0, len(tiles), 9):
    chunk = tiles[si:si + 9]; rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W, rows * (W * 9 // 16 + 28)), (12, 12, 14)); d = ImageDraw.Draw(sheet)
    for i, (label, path) in enumerate(chunk):
        im = Image.open(path).convert("RGB"); im = im.resize((W, W * 9 // 16))
        x, y = (i % cols) * W, (i // cols) * (W * 9 // 16 + 28)
        sheet.paste(im, (x, y + 28)); d.text((x + 8, y + 7), label, fill=(240, 240, 240))
    p = f"out/lf01/palmier/review/sheet_{si // 9 + 1}.png"; sheet.save(p); print("sheet", p)
