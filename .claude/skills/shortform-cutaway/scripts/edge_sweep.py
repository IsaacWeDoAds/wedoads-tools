#!/usr/bin/env python3
"""edge_sweep.py — check EVERY edge of a cut against both word lists and the envelope (v2, Oct 2026).
Built after a 16-min edit shipped with "edited using [AI]" and "absolutely [free]" cut off — every edge audit had
passed, because they only asked "is there speech at the edge?", never "is a word cut in half?".

Flags (judge each one by ear or with probe.py — some are deliberate, e.g. dropping a restart):
  CLIP-T / CLIP-H   a word straddles the piece's end / start
  MIDFLOW           the next source word follows the last kept word within 0.30 s and is not where the next
                    piece resumes -> the cut lands mid-phrase
  VOICE@END/START   the envelope is still above threshold at the edge (an audible chop unless faded)
  HEAD-ISLAND       a separate voiced fragment sits inside the head (a 'hm', a false-start syllable)
  TAIL-ISLAND       a short voiced fragment sits at the tail (the onset of a dropped restart)
  REPEAT            a 1-3 word phrase repeats inside the piece (a fumble left in) — reads --iso words if given

Usage: edge_sweep.py cut.json CLIP_wx.json [--iso ISO_words.json]
  cut.json from build_wx2.py ({"audio", "pieces": [{id, a, b, w1, ...}]}); words = [{s, e, w}].
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from envtools import env, thr, islands

C = json.load(open(sys.argv[1])); AUD = C["audio"]; P = C["pieces"]
WX = sorted(json.load(open(sys.argv[2])), key=lambda w: w["s"])
ISO = sorted(json.load(open(sys.argv[sys.argv.index("--iso") + 1])), key=lambda w: w["s"]) if "--iso" in sys.argv else None
E, TH = env(AUD), thr(AUD)
norm = lambda s: "".join(ch for ch in s.lower() if ch.isalnum())
COMMON = {"very", "the", "a", "and", "is", "that", "i", "it", "this", "so", "of", "to", "you", "are", "in", "all"}
flags = []
for i, p in enumerate(P):
    a, b = p["a"], p["a"] + p.get("dur", p["b"] - p["a"])
    nxt = P[i + 1] if i + 1 < len(P) else None; prv = P[i - 1] if i else None
    cont_t = nxt is not None and abs(nxt["a"] - b) < 0.06
    cont_h = prv is not None and abs(prv["a"] + prv.get("dur", prv["b"] - prv["a"]) - a) < 0.06
    for nm, W in (("wx", WX), ("iso", ISO or [])):
        for w in W:
            if w["e"] - w["s"] > 1.2: continue          # a stretched word is its own problem (cut-audit gate 1)
            if not cont_t and w["s"] < b - 0.04 and w["e"] > b + 0.06: flags.append((p, "CLIP-T", f"{nm} '{w['w']}' {w['s']:.2f}-{w['e']:.2f} vs end {b:.2f}"))
            if not cont_h and w["s"] < a - 0.06 and w["e"] > a + 0.04: flags.append((p, "CLIP-H", f"{nm} '{w['w']}' {w['s']:.2f}-{w['e']:.2f} vs start {a:.2f}"))
    w1 = p.get("w1", b)
    after = [w for w in WX if w["s"] >= w1 - 0.01]
    if after and not cont_t:
        resumes = nxt is not None and abs(nxt.get("w0", nxt["a"]) - after[0]["s"]) < 0.15
        if after[0]["s"] - w1 < 0.30 and not resumes:
            flags.append((p, "MIDFLOW", f"gap {after[0]['s'] - w1:.2f}s, next: '{' '.join(w['w'] for w in after[:6])}'"))
    kb, ka = int(b * 100), int(a * 100)
    if not cont_t and kb < len(E) and E[kb] > TH: flags.append((p, "VOICE@END", f"{E[kb] - TH:+.1f} dB over threshold"))
    if not cont_h and ka < len(E) and E[ka] > TH: flags.append((p, "VOICE@START", f"{E[ka] - TH:+.1f} dB over threshold"))
    isl = islands(AUD, a, b, 0.12)
    if len(isl) > 1 and not cont_h and isl[0][1] - isl[0][0] < 0.35: flags.append((p, "HEAD-ISLAND", f"{isl[0][0]:.2f}-{isl[0][1]:.2f} then {isl[1][0]:.2f}"))
    if len(isl) > 1 and not cont_t and isl[-1][1] - isl[-1][0] < 0.35: flags.append((p, "TAIL-ISLAND", f"{isl[-1][0]:.2f}-{isl[-1][1]:.2f} after {isl[-2][1]:.2f}"))
    iw = [x for x in (norm(w["w"]) for w in (ISO or WX) if a + 0.05 <= w["s"] <= b - 0.05) if x]
    hit = None
    for n in (3, 2, 1):
        for j in range(len(iw) - n):
            g = iw[j:j + n]
            if n == 1 and g[0] in COMMON: continue
            if any(iw[k:k + n] == g for k in range(j + n, min(j + n + 4, len(iw) - n + 1))): hit = " ".join(g); break
        if hit: break
    if hit: flags.append((p, "REPEAT", f"'{hit}' in: {' '.join(iw)[:120]}"))

for p, kind, msg in flags:
    print(f"{p['id']:6} {p['a']:8.2f} {kind:11} {msg}")
print(f"{len(flags)} flags over {len(P)} pieces — listen to every MIDFLOW/CLIP/REPEAT; probe.py settles a doubt in one call")
