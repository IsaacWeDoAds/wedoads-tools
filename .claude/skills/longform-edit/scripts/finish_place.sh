#!/bin/zsh
# Last placement step for lf01 v10.1 — run when the JobMarket project is IN FRONT in Palmier (Nishant not editing
# another project). Removes the stale Type/Cards tracks, imports the v9 renders in paced groups, places Cards + Type,
# pins Type on top, and writes the composited review sheets.
set -e; cd "<project>"; export RENDER_VER=${RENDER_VER:-v9}
python3 - <<'EOF'
import sys, json
sys.path.insert(0, "work/lf01/work"); import palmier as pm
P = pm.Palmier() if hasattr(pm, "Palmier") else pm
l = P.call("manage_project", {"action": "list"}); assert l["active"]["name"] == "JobMarket", f"active project is {l['active']['name']} — bring JobMarket to the front first"
st = json.load(open("work/lf01/work/palmier_state.json")); seg = json.load(open("work/lf01/work/segments.json"))
tl = P.call("get_timeline", {}); v1 = next(t for t in tl["tracks"] if t.get("label") == "V1")
n = len([c for c in v1["clips"] if c["mediaRef"] == seg["sourceRef"]]); assert n == len(seg["segments"]), f"V1 has {n} clips, map {len(seg['segments'])}: rebuild the map first"
# my rendered-layer tracks = tracks whose clips reference render files (type_/full_/card_ in the media cache)
render_ids = {v for k, v in st["media"].items() if "/out/lf01/palmier/" in k and k.split("/")[-1].split("_")[0] in ("type", "full", "card")}
keep = {st["tracks"][k]["trackId"] for k in ("Broll", "Generated") if k in st["tracks"]}
stale = [t for t in tl["tracks"] if t["type"] == "video" and t.get("label") != "V1" and t["trackId"] not in keep and t.get("clips") and all(c["mediaRef"] in render_ids for c in t["clips"])]
if stale:
    P.call("manage_tracks", {"remove": [{"trackId": t["trackId"]} for t in stale]}); print("removed stale render tracks:", [(t.get("label"), len(t["clips"])) for t in stale])
for k in ("Type", "Cards"): st["tracks"].pop(k, None)
json.dump(st, open("work/lf01/work/palmier_state.json", "w"), indent=1)
EOF
ONLY=all python3 work/lf01/work/palmier_preimport.py | tail -1
python3 work/lf01/work/palmier_place.py graphics | tail -3 | cut -c1-160
python3 work/lf01/work/palmier_place.py reorder
setopt null_glob; rm -f out/lf01/palmier/review/*.png
python3 work/lf01/work/palmier_review.py 5.0 46.0 71.5 242.5 291.6 354.8 364.2 429.8 432.5 444.8 506 550.5 647.5 807 835 869 1146.5 1300 1323 1364.8 1373.2 1434 1458.5 | tail -4
