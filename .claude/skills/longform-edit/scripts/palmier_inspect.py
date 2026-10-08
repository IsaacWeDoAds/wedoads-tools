"""Save composited timeline frames: python3 palmier_inspect.py 52246 52750 ... → out/lf01/palmier/inspect/f<frame>.png"""
import sys, os, shutil, json, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import palmier as pm
P = pm.Palmier() if hasattr(pm, "Palmier") else pm
os.makedirs("out/lf01/palmier/inspect", exist_ok=True)
for a in sys.argv[1:]:
    f = int(a); r = P.call("inspect_timeline", {"startFrame": f, "endFrame": f + 1, "maxFrames": 1})
    out = f"out/lf01/palmier/inspect/f{f:06d}.png"
    if isinstance(r, str) and os.path.exists(r): shutil.move(r, out); print(f, "saved (path)", out); continue
    if isinstance(r, list): r = next((x for x in r if isinstance(x, dict) and x.get("image")), r[0] if r else {})
    if isinstance(r, dict) and r.get("image") and os.path.exists(r["image"]): shutil.move(r["image"], out); print(f, "saved", out); continue
    if isinstance(r, dict):
        img = None
        for c in (r.get("content") or []):
            if c.get("type") == "image": img = c.get("data")
        if img is None and r.get("image"): img = r["image"]
        if img is None and r.get("path") and os.path.exists(r["path"]): shutil.move(r["path"], out); print(f, "saved (dict path)", out); continue
        if img:
            open(out, "wb").write(base64.b64decode(img)); print(f, "saved", out, os.path.getsize(out)); continue
    print(f, "unexpected result:", str(r)[:300])
