"""Replace only the re-rendered type windows on the Type track (indexes in work/lf01/work/type_rerender.json):
remove the old clip at that start frame, import the new versioned file, add it back on the same track.
   RENDER_VER=v6 python3 palmier_retype.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import palmier as pm
P = pm.Palmier() if hasattr(pm, "Palmier") else pm
plan = json.load(open("work/lf01/work/palmier_plan.json"))
STATE_F = "work/lf01/work/palmier_state.json"; state = json.load(open(STATE_F))
RENDER_VER = os.environ.get("RENDER_VER", "v6")
OFF = state["offset"]; T = lambda f: OFF + 2 * f
sel = json.load(open("work/lf01/work/type_rerender.json"))
if isinstance(sel, list): sel = {"types": sel, "fulls": []}
tl = P.call("get_timeline", {})
def _try_link(a, b):
    try: os.link(a, b); return True
    except OSError: return False   # exFAT / cross-device: no hardlinks
def render_file(name):
    src = f"out/lf01/palmier/{name}"; vdir = f"out/lf01/palmier/{RENDER_VER}"; os.makedirs(vdir, exist_ok=True)
    dst = f"{vdir}/{name}"
    if not os.path.exists(dst): (lambda: __import__('shutil').copy2(src, dst))() if not _try_link(src, dst) else None
    return dst
def media(path):
    path = os.path.abspath(path)
    if path in state["media"]: return state["media"][path]
    r = P.call("import_media", {"source": {"path": path}, "folder": "lf01/render"})
    mid = r.get("mediaRef") or r.get("id"); state["media"][path] = mid; json.dump(state, open(STATE_F, "w"), indent=1); return mid
for kind, track, pat in (("types", "Type", "type_{:06d}.mov"), ("fulls", "Cards", "full_{:06d}.mp4")):
    idx = sel.get(kind) or []
    if not idx: continue
    tr = next(t for t in tl["tracks"] if t["trackId"] == state["tracks"][track]["trackId"])
    by_start = {c["frames"][0]: c for c in tr["clips"]}
    entries, removed = [], []
    for i in idx:
        w = plan[kind][i]; a, b = T(w["from"]), T(w["to"])
        for c in tr["clips"]:
            if c["frames"][0] < b and c["frames"][1] > a and c["id"] not in removed: removed.append(c["id"])
        entries.append({"mediaRef": media(render_file(pat.format(w["from"]))), "startFrame": a, "endFrame": b, "includeAudio": False, "trackIndex": tr["index"]})
    if removed: P.call("remove_clips", {"clipIds": removed})
    r = P.call("add_clips", {"entries": entries})
    tl = P.call("get_timeline", {}); tr = next(t for t in tl["tracks"] if t["trackId"] == state["tracks"][track]["trackId"])
    print(f"{track}: replaced {len(removed)}, added {len(r.get('clips', []))} from {RENDER_VER} → {len(tr['clips'])} clips on the track")
