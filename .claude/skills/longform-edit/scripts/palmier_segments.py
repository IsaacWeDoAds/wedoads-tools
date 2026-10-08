"""Rebuild work/lf01/work/segments.json from the LIVE Palmier V1 — his current trim is the ground truth.
Every re-trim he makes moves every source-anchored cue; run this before gen_data.py whenever V1 changed.
Cut frame (30 fps) = (timelineFrame - OFFSET) / 2; source seconds = trimStartFrame / 60 (project-fps units)."""
import json, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import palmier as pm
P = pm.Palmier() if hasattr(pm, "Palmier") else pm
tl = P.call("get_timeline", {}); assert tl["fps"] == 60, tl["fps"]
v1 = next(t for t in tl["tracks"] if t.get("label") == "V1")
clips = sorted(v1["clips"], key=lambda c: c["frames"][0])
src_ref = collections.Counter(c["mediaRef"] for c in clips).most_common(1)[0][0]
mine = [c for c in clips if c["mediaRef"] == src_ref]
OFFSET = mine[0]["frames"][0]                     # the montage sits before his first source clip
starts = [round((c["frames"][0] - OFFSET) / 2) for c in mine]
end = round((mine[-1]["frames"][1] - OFFSET) / 2)
segs = []
for i, c in enumerate(mine):
    f0 = starts[i]; f1 = starts[i + 1] if i + 1 < len(mine) else end
    srcS = c["trimStartFrame"] / 60
    segs.append({"from": f0, "len": f1 - f0, "srcS": round(srcS, 4), "srcE": round(srcS + (f1 - f0) / 30, 4),
                 "tl": c["frames"], "clipId": c["id"], "audioId": (c.get("audio") or {}).get("id")})
out = {"segments": segs, "total": end, "fps_timeline": 60, "source": "C0937.MP4", "offset": OFFSET, "sourceRef": src_ref}
old = json.load(open("work/lf01/work/segments.json"))["segments"] if os.path.exists("work/lf01/work/segments.json") else []
json.dump(out, open("work/lf01/work/segments.json", "w"), indent=0)
oldby = {s.get("clipId"): s for s in old}
moved = sum(1 for s in segs if s["clipId"] in oldby and oldby[s["clipId"]]["from"] != s["from"])
print(f"V1: {len(mine)} source clips (+{len(clips)-len(mine)} other), offset {OFFSET}, cut total {end}f = {end/30:.1f}s | vs old map: {len(old)} clips, {moved} moved, {len(set(oldby)-{s['clipId'] for s in segs})} gone, {sum(1 for s in segs if s['clipId'] not in oldby)} new")
