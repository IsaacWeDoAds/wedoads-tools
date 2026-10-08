#!/usr/bin/env python3
"""Place the lf01 layers on Nishant's Palmier timeline (60 fps) from palmier_plan.json + the rendered clips.
   python3 palmier_place.py montage      insert the cold open at frame 0 (ripples his V1/A1 by 200 frames) — run FIRST, once
   python3 palmier_place.py broll        library/news/capture b-roll on a "Broll" track
   python3 palmier_place.py generated    Omni windows + Veo/anime shots on a "Generated" track (zoom-matched Omni)
   python3 palmier_place.py graphics     cards + fulls on "Cards", alpha type windows on "Type" (needs the renders)
   python3 palmier_place.py sfx          the 220 cues on SFX lanes (+ volumes, bed fades) and the pre-roll sfx
   python3 palmier_place.py zoom         scale/position keyframes on his clips (the jump-cut zoom layer)
   python3 palmier_place.py status       what is on the timeline now
Frames: plan frames are CUT frames at 30 fps → timeline = OFFSET + 2*f, OFFSET = 200 once the montage is in.
He places the GENERATED clips (Omni / Veo / anime) himself; palmier_align.py lines them up afterwards."""
import json, os, sys, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palmier import Palmier
P = Palmier()
ROOT = os.path.abspath(".")
plan = json.load(open("work/lf01/work/palmier_plan.json"))
STATE_F = "work/lf01/work/palmier_state.json"
state = json.load(open(STATE_F)) if os.path.exists(STATE_F) else {"offset": 0, "media": {}, "tracks": {}}
save = lambda: json.dump(state, open(STATE_F, "w"), indent=1)
OFF = lambda: state["offset"]
T = lambda f: OFF() + 2 * f
RENDER_VER = os.environ.get("RENDER_VER", "v4")
def _try_link(a, b):
    try: os.link(a, b); return True
    except OSError: return False   # exFAT / cross-device: no hardlinks
def render_file(name):
    """out/lf01/palmier/<name> → a versioned hardlink Palmier has never seen (new asset, fresh metadata)"""
    src = f"out/lf01/palmier/{name}"; vdir = f"out/lf01/palmier/{RENDER_VER}"; os.makedirs(vdir, exist_ok=True)
    dst = f"{vdir}/{name}"
    if not os.path.exists(dst):
        if not os.path.exists(src): raise FileNotFoundError(src)
        (lambda: __import__('shutil').copy2(src, dst))() if not _try_link(src, dst) else None
    return dst
def media(path, folder):
    """import once (referenced in place), remember the id"""
    path = os.path.abspath(path)
    if path in state["media"]: return state["media"][path]
    r = P.call("import_media", {"source": {"path": path}, "folder": folder})
    mid = r.get("mediaRef") or r.get("id"); state["media"][path] = mid; save(); return mid
def add_track(entries, name, kind="video"):
    """one add_clips call without trackIndex → Palmier creates ONE new track for the batch; name it"""
    out = []
    for i in range(0, len(entries), 40):
        r = P.call("add_clips", {"entries": entries[i:i + 40]} if i == 0 else {"entries": [dict(e, trackIndex=state["tracks"][name]["index"]) for e in entries[i:i + 40]]})
        out += r.get("clips", [])
        if i == 0:
            ct = (r.get("createdTracks") or [{}])[0]
            tl = P.call("get_timeline", {})
            tr = next((t for t in tl["tracks"] if t.get("label") == ct.get("label") and t["type"] == kind), tl["tracks"][ct.get("index", 0)])
            state["tracks"][name] = {"trackId": tr["trackId"], "index": tr["index"]}
            P.call("manage_tracks", {"set": [{"trackId": tr["trackId"], "name": name}]}); save()
            # indexes shift after a new track: re-read for the remaining batches
            tl = P.call("get_timeline", {}); state["tracks"][name]["index"] = next(t["index"] for t in tl["tracks"] if t["trackId"] == tr["trackId"]); save()
    print(f"  {name}: {len(out)} clips")
    return out
def clip_entry(mid, start_f, dur_f, src_from_f=None, audio=False):
    e = {"mediaRef": mid, "startFrame": T(start_f), "includeAudio": audio}
    if src_from_f is not None: e["source"] = [round(src_from_f / 30, 4), round((src_from_f + dur_f) / 30, 4)]
    else: e["endFrame"] = T(start_f + dur_f)
    return e

cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
# identity guard: the MCP edits whatever project is open — refuse to touch a timeline that is not his lf01 trim
_seg = json.load(open("work/lf01/work/segments.json"))
_tl = P.call("get_timeline", {}); _v1 = next((t for t in _tl["tracks"] if t.get("label") == "V1"), None)
_n = len([c for c in (_v1 or {}).get("clips", []) if c["mediaRef"] == _seg.get("sourceRef")])
if cmd != "status" and (_v1 is None or _n != len(_seg["segments"])):
    sys.exit(f"REFUSED: the open Palmier timeline has {_n} clips of the lf01 take (map has {len(_seg['segments'])}) — another project or a re-trim is open; rebuild the map or reopen lf01 first")
if cmd == "montage":
    assert state["offset"] == 0, "montage already inserted"
    mid = media(render_file("montage.mp4"), "lf01/render")
    tl = P.call("get_timeline", {}); v1 = next(t for t in tl["tracks"] if t.get("label") == "V1")
    r = P.call("insert_clips", {"trackIndex": v1["index"], "atFrame": 0, "entries": [{"mediaRef": mid, "durationFrames": plan["PRE"] * 2, "includeAudio": True}]})
    state["offset"] = plan["PRE"] * 2; save()
    print("montage inserted at 0 → his cut now starts at", state["offset"], json.dumps(r)[:200])
elif cmd == "broll":
    # library / news / capture b-roll (generated clips have their own step) on one track under the graphics
    ents = []
    for sh in plan["broll"]:
        if any(k in sh["src"] for k in ("/gen/", "/omni/")): continue
        ents.append(clip_entry(media(f"public/{sh['src']}", "lf01/broll"), sh["from"], sh["to"] - sh["from"], sh["srcFrom"]))
    ents.sort(key=lambda e: e["startFrame"]); add_track(ents, "Broll")
elif cmd == "generated":
    # Omni behind-the-head windows + Veo / anime shots, from the readable staged copies (his library folders)
    import glob
    staged = glob.glob("work/lf01/palmier_media/omni/*.mp4") + glob.glob("work/lf01/palmier_media/generated/*.mp4")
    def staged_for(src):
        b = os.path.basename(src)
        key = {"maze-c2_30": "veo-maze", "server-c2_30": "veo-server", "puppet-c2_30": "veo-puppets", "anime-desk-c2_30": "anime-desk", "anime-hours-c1_30": "anime-10000",
               "anime-mentor-c1_30": "anime-mentor", "anime-meetings-c1_30": "anime-meetings", "anime-fork-c1_30": "anime-fork", "anime-intern-c1_30": "anime-ai-as"}.get(b.replace(".mp4", ""))
        if key is None and "_1080" in b: key = "omni-" + b.split("_")[0]
        if key is None: key = b.replace(".mp4", "")   # v10 Omni clips are staged under their own conformed name
        return next((f for f in staged if os.path.basename(f).startswith(key)), None) if key else None
    ents, omni_rows = [], []
    # Omni clips retired (6 Sep) — only the Veo / anime shots are placed
    for sh in plan["broll"]:
        if "/gen/" not in sh["src"]: continue
        f = staged_for(sh["src"])
        if not f: continue
        ents.append(clip_entry(media(f, "lf01/generated"), sh["from"], sh["to"] - sh["from"], sh["srcFrom"]))
    order = sorted(range(len(ents)), key=lambda i: ents[i]["startFrame"])
    clips = add_track([ents[i] for i in order], "Generated")
    # the Omni windows sit where the face would be: give them the face's zoom keyframes so the switch is invisible
    ox, oy = 962 / 1920, 400 / 1080
    by_start = {c["frames"][0]: c["id"] for c in clips}
    n = 0
    for o in omni_rows:
        cid = by_start.get(T(o["from"]))
        seg = next((z for z in plan["zoom"] if z["from"] <= o["from"] < z["from"] + z["len"]), None)
        if not cid or not seg: continue
        ks = [(k[0] + seg["from"] - o["from"], k[1]) for k in seg["keys"] if o["from"] <= k[0] + seg["from"] < o["to"]]
        if not ks: continue
        pts = [(0, ks[0][1])] + [(k[0], k[1]) for k in ks if k[0] > 0]
        P.call("set_keyframes", {"clipId": cid, "property": "scale", "keyframes": [[p[0] * 2, p[1], p[1], "linear"] for p in pts]})
        P.call("set_keyframes", {"clipId": cid, "property": "position", "keyframes": [[p[0] * 2, ox - ox * p[1], oy - oy * p[1], "linear"] for p in pts]})
        n += 1
    print(f"  zoom-matched {n} Omni windows")
elif cmd == "graphics":
    # cards + fulls (opaque) on "Cards"; type (alpha) on "Type" above; then order Type > Cards > Generated > Broll > his V1
    ents = []
    for w in plan["cards"]: ents.append(clip_entry(media(render_file(f"card_{w['from']:06d}.mp4"), "lf01/render"), w["from"], w["to"] - w["from"], 0))
    for w in plan["fulls"]: ents.append(clip_entry(media(render_file(f"full_{w['from']:06d}.mp4"), "lf01/render"), w["from"], w["to"] - w["from"], 0))
    ents.sort(key=lambda e: e["startFrame"]); add_track(ents, "Cards")
    ents = [clip_entry(media(render_file(f"type_{w['from']:06d}.mov"), "lf01/render"), w["from"], w["to"] - w["from"], 0) for w in plan["types"]]
    add_track(ents, "Type")
    want = [n for n in ["Type", "Cards", "Generated", "Broll"] if n in state["tracks"]]
    P.call("manage_tracks", {"reorder": [{"trackId": state["tracks"][n]["trackId"], "to": i} for i, n in enumerate(want)]})
    tl = P.call("get_timeline", {})
    for n in want: state["tracks"][n]["index"] = next(t["index"] for t in tl["tracks"] if t["trackId"] == state["tracks"][n]["trackId"])
    save(); print("order:", [(t.get("label"), t["type"]) for t in tl["tracks"]])
elif cmd == "sfx":
    cues = plan["cues"]
    # lanes: greedy interval colouring so no two cues overlap on a lane (Palmier overwrites on the same track)
    lanes = []
    for c in sorted(cues, key=lambda c: c["at"]):
        a, b = T(c["at"]), T(c["at"] + c["dur"])
        for L in lanes:
            if L["end"] <= a: L["cues"].append(c); L["end"] = b; break
        else: lanes.append({"cues": [c], "end": b})
    print(f"{len(cues)} cues → {len(lanes)} lanes")
    placed = []
    for i, L in enumerate(lanes):
        ents = []
        for c in L["cues"]:
            mid = media(f"public/{c['src']}", "lf01/sfx")
            ents.append({"mediaRef": mid, "startFrame": T(c["at"]), "source": [round(c["startFrom"] / 30, 4), round((c["startFrom"] + c["dur"]) / 30, 4)]})
        clips = add_track(ents, f"SFX{i+1}", "audio")
        for c, cl in zip(L["cues"], clips): placed.append((c, cl["id"]))
    # pre-roll sfx (shutters, reversed hit, tension strings) at 0 on its own lane
    mid = media(render_file("preroll_sfx.wav"), "lf01/render")
    add_track([{"mediaRef": mid, "startFrame": 0}], "Preroll", "audio")
    print("placed; run sfxfix for levels and fades")
elif cmd == "typetrack":
    # the alpha type windows as ProRes 4444 (out/lf01/palmier/v3) — Palmier's compositor cannot decode Animation/qtrle
    ents = [clip_entry(media(render_file(f"type_{w['from']:06d}.mov"), "lf01/render"), w["from"], w["to"] - w["from"], 0) for w in plan["types"]]
    add_track(ents, "Type")
    want = [n for n in ["Type", "Cards", "Generated", "Broll"] if n in state["tracks"]]
    P.call("manage_tracks", {"reorder": [{"trackId": state["tracks"][n]["trackId"], "to": i} for i, n in enumerate(want)]})
    tl = P.call("get_timeline", {})
    for n in want: state["tracks"][n]["index"] = next(t["index"] for t in tl["tracks"] if t["trackId"] == state["tracks"][n]["trackId"])
    save(); print("order:", [(t.get("label"), t["type"]) for t in tl["tracks"] if t["type"] == "video"])
elif cmd == "reorder":
    # Type > Cards > Generated > Broll > his V1 — add_clips creates each new track on TOP, so every native re-place
    # must re-assert this (6 Sep: a b-roll re-place after graphics buried the text track under the cutaways)
    # only the Type track is pinned (index 0); Nishant arranges Cards / Generated / Broll himself (shots never overlap)
    if "Type" in state["tracks"]: P.call("manage_tracks", {"reorder": [{"trackId": state["tracks"]["Type"]["trackId"], "to": 0}]})
    tl = P.call("get_timeline", {})
    for n in [n for n in ["Type", "Cards", "Generated", "Broll"] if n in state["tracks"]]:
        state["tracks"][n]["index"] = next(t["index"] for t in tl["tracks"] if t["trackId"] == state["tracks"][n]["trackId"])
    save(); print("order:", [(t.get("label"), t["type"]) for t in tl["tracks"] if t["type"] == "video"])
elif cmd == "preroll":
    # the pre-roll SFX bed alone (the sfx command places it last; re-add it here if that step failed)
    mid = media(render_file("preroll_sfx.wav"), "lf01/render")
    add_track([{"mediaRef": mid, "startFrame": 0}], "Preroll", "audio"); save()
elif cmd == "droptrack":
    # remove ONE of my tracks by name (e.g. Type) before re-placing it from a new render version
    name = sys.argv[2]; tr = state["tracks"].pop(name, None)
    if tr: P.call("manage_tracks", {"remove": [{"trackId": tr["trackId"]}]}); save(); print("removed", name, tr["trackId"])
    else: print("no such track in state:", name)
elif cmd == "reset":
    # remove every track this script created and the old montage, so a regenerated register can be placed cleanly
    tl = P.call("get_timeline", {})
    mine = [t for t in tl["tracks"] if t.get("label") not in ("V1", "A1")]
    if mine: P.call("manage_tracks", {"remove": [{"trackId": t["trackId"]} for t in mine]})
    if state["offset"]:
        tl = P.call("get_timeline", {}); v1 = next(t for t in tl["tracks"] if t.get("label") == "V1")
        P.call("ripple_delete_ranges", {"trackIndex": v1["index"], "units": "frames", "ranges": [[0, state["offset"]]]})
        state["offset"] = 0
    state["tracks"] = {}; save()
    tl = P.call("get_timeline", {}); print("reset →", [(t.get("label"), t["type"], len(t.get("clips", []))) for t in tl["tracks"]], "total", tl["totalFrames"])
elif cmd == "sfxfix":
    # volumes + fades per SFX clip, fades clamped to the clip (Palmier refuses fades longer than the clip)
    cues = plan["cues"]
    by_start = {}
    for c in cues: by_start.setdefault(T(c["at"]), []).append(c)
    tl = P.call("get_timeline", {})
    sfx_tracks = [t for t in tl["tracks"] if t["type"] == "audio" and t.get("label") != "A1"]
    groups = {}
    for t in sfx_tracks:
        for cl in t.get("clips", []):
            a, b = cl["frames"]; cands = by_start.get(a, [])
            c = min(cands, key=lambda c: abs(2 * c["dur"] - (b - a))) if cands else None
            if not c: continue
            db = round(20 * math.log10(max(c["vol"], 1e-3)), 1)
            fi, fo = (min(24, (b - a) // 3), min(48, (b - a) // 2)) if c["fade"] else (0, 0)
            while fi + fo >= b - a and (fi or fo): fi = max(0, fi - 2); fo = max(0, fo - 2)
            groups.setdefault((db, fi, fo), []).append(cl["id"])
    for (db, fi, fo), ids in groups.items():
        for j in range(0, len(ids), 60):
            args = {"clipIds": ids[j:j + 60], "volumeDb": db}
            if fi or fo: args.update({"fadeInFrames": fi, "fadeOutFrames": fo, "fadeInInterpolation": "smooth", "fadeOutInterpolation": "smooth"})
            P.call("set_clip_properties", args)
    print("volumes/fades set on", sum(len(v) for v in groups.values()), "clips in", len(groups), "groups")
elif cmd == "zoom":
    # scale/position keyframes per clip of his V1 (clip-relative frames at 60 fps); origin = his face (962,400)
    ox, oy = 962 / 1920, 400 / 1080
    n = 0
    for z in plan["zoom"]:
        if not z.get("clipId"): continue
        keys = z["keys"]
        # breakpoints only: keep points where the slope changes (+ ends), at 60 fps
        pts = [(0, keys[0][1])]
        for k in range(1, len(keys) - 1):
            d0 = keys[k][1] - keys[k - 1][1]; d1 = keys[k + 1][1] - keys[k][1]
            if abs(d1 - d0) > 1e-4: pts.append((keys[k][0], keys[k][1]))
        pts.append((keys[-1][0], keys[-1][1]))
        if len(pts) > 120: pts = pts[::2]
        sc = [[p[0] * 2, p[1], p[1], "linear"] for p in pts]
        po = [[p[0] * 2, ox - ox * p[1], oy - oy * p[1], "linear"] for p in pts]
        P.call("set_keyframes", {"clipId": z["clipId"], "property": "scale", "keyframes": sc})
        P.call("set_keyframes", {"clipId": z["clipId"], "property": "position", "keyframes": po})
        n += 1
    print(f"zoom keyframes on {n} clips")
else:
    tl = P.call("get_timeline", {})
    print("offset", state["offset"], "| tracks:", [(t.get("label"), t["type"], len(t.get("clips", []))) for t in tl["tracks"]])
