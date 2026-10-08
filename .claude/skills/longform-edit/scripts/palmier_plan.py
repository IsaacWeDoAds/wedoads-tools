#!/usr/bin/env python3
"""Turn data.ts (his cut) into the Palmier placement plan: what to RENDER (cards / fulls / type windows,
montage, pre-roll sfx) and what to place NATIVELY (b-roll, Omni, SFX cues, Veo audio, zoom keyframes).
Frames in the plan are CUT frames at 30 fps; palmier_place.py maps to the 60-fps timeline (×2, + montage)."""
import json, re, os
FPS = 30
ts = open("src/LF01/data.ts").read()
J = lambda name: json.loads(re.search(r"export const %s[^=]*= (\[.*?\])(?: as const)?;\n" % name, ts, re.S).group(1))
SHOTS, EMPH, STAMPS, HEROES, OMNI, CUES, SEG = J("SHOTS"), J("EMPH"), J("STAMPS"), J("HEROES"), J("OMNI"), J("CUES"), J("SEGMENTS")
TOTAL = int(re.search(r"TOTAL_FRAMES = (\d+)", ts).group(1))
PRE = int(re.search(r"PRE_FRAMES = (\d+)", ts).group(1))
MIN_GROW_LEN, GROW = 45, 12
hero_of = lambda src: next((h for h in HEROES if h["id"] == src[5:]), None) if src.startswith("hero:") else None
shot_at = lambda f: next((s for s in SHOTS if s["from"] <= f < s["to"]), None)

# ── render windows ──────────────────────────────────────────────────────────
cards = [{"from": s["from"], "to": s["to"], "src": s["src"]} for s in SHOTS if s["kind"] == "card"]
face_windows = cards + [{"from": s["from"], "to": s["to"], "src": s["src"]} for s in SHOTS if s["src"] == "hero:intro"]
fulls = [{"from": s["from"], "to": s["to"], "src": s["src"]} for s in SHOTS if s["kind"] == "full" and (s["glitch"] or hero_of(s["src"]) or "/site-" in s["src"])]
# type layer: frames where a stamp / non-omni lockup / lane hero is live AND the overlay mode is face/full AND no hero owns the frame
live = [False] * TOTAL
def mark(a, b):
    for f in range(max(0, a), min(TOTAL, b)): live[f] = True
for s in STAMPS: mark(s["from"], s["to"])
for e in EMPH:
    if not e.get("omni"): mark(e["from"], e["to"])
for h in HEROES:
    if h["kind"] == "lane": mark(h["from"], h["to"])
for f in range(TOTAL):
    if not live[f]: continue
    s = shot_at(f)
    if not s: continue
    next_is_face = not any(x["from"] == s["to"] for x in SHOTS)
    growing = s["kind"] == "card" and next_is_face and s["to"] - s["from"] >= MIN_GROW_LEN and f >= s["to"] - GROW
    mode = "face" if growing else s["kind"]
    if mode == "card" or (s["kind"] == "full" and hero_of(s["src"])): live[f] = False
# merge into windows (gap ≤ 15 frames joins)
types, f = [], 0
while f < TOTAL:
    if live[f]:
        a = f
        while f < TOTAL and (live[f] or (f - a < 1e9 and any(live[f:f + 16]))): f += 1
        types.append({"from": a, "to": f})
    else: f += 1

# ── native placements ───────────────────────────────────────────────────────
broll = [{"from": s["from"], "to": s["to"], "src": s["src"], "srcFrom": s["srcFrom"]} for s in SHOTS if s["kind"] == "full" and not s["glitch"] and not hero_of(s["src"]) and "/site-" not in s["src"]]
omni = [{"from": o["from"], "to": o["to"], "src": o["src"], "srcFrom": o["srcFrom"]} for o in OMNI]
veo_audio = []
for s in SHOTS:
    for key in ("maze-c2", "puppet-c2", "server-c2"):
        if key in s["src"]: veo_audio.append({"from": s["from"], "to": s["to"], "src": f"broll/lf01/gen/{key}_audio.wav", "srcFrom": s["srcFrom"], "vol": 0.45})

# ── zoom layer (port of faceScale in Final.tsx): per SEGMENT (= his clip) keyframes ─────────────
def face_scale(f):
    seg = next((i for i, sg in enumerate(SEG) if sg["from"] <= f < sg["from"] + sg["len"]), -1)
    if seg < 0: return 1.0
    sg = SEG[seg]
    flips = sum(1 for i in range(seg + 1) if SEG[i]["len"] >= 45)
    base = 1.0 if flips % 2 == 0 else 1.09
    push = min(0.05, max(0.0, 0.05 * (f - sg["from"]) / sg["len"])) if sg["len"] >= 180 else 0.0
    snap = 0.0
    def snapv(p, amp):
        d = f - p
        if 0 <= d < 24: return amp * (d / 4) if d < 4 else amp - (amp / 2) * ((d - 4) / 20)
        return 0.0
    for o in OMNI: snap = max(snap, snapv(o["from"] + 7, 0.06))
    for e in EMPH:
        if not e.get("omni"): snap = max(snap, snapv(e["from"], 0.05))
    return base + push + snap
zoom = []
for sg in SEG:
    a, b = sg["from"], sg["from"] + sg["len"]
    # sample the curve: every 4 frames plus every frame inside a snap, then compress runs of equal values
    pts = []
    last = None
    for f in range(a, b):
        v = round(face_scale(f), 4)
        if v != last or f == a: pts.append((f - a, v)); last = v
    if len(pts) > 400: pts = pts[::2]
    zoom.append({"clipId": sg.get("clipId"), "tl": sg.get("tl"), "from": a, "len": sg["len"], "keys": pts})

plan = {"PRE": PRE, "TOTAL": TOTAL, "cards": cards, "face_windows": face_windows, "fulls": fulls, "types": types, "broll": broll, "omni": omni, "veo_audio": veo_audio, "cues": CUES, "zoom": zoom, "segments": SEG}
json.dump(plan, open("work/lf01/work/palmier_plan.json", "w"), indent=0)
tsec = lambda L: sum(w["to"] - w["from"] for w in L) / FPS
print(f"render: cards {len(cards)} ({tsec(cards):.0f}s) · fulls {len(fulls)} ({tsec(fulls):.0f}s) · type windows {len(types)} ({tsec(types):.0f}s) · montage {PRE}f · preroll sfx")
print(f"native: b-roll {len(broll)} · omni {len(omni)} · sfx cues {len(CUES)} · veo audio {len(veo_audio)} · zoom keyframes on {len(zoom)} clips ({sum(len(z['keys']) for z in zoom)} keys)")
