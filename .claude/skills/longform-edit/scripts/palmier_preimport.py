"""Import the planned render files into Palmier in small groups (8, then a pause) so the app's indexer keeps up —
78 imports in one burst wedged the MCP (6 Sep 02:30). Uses the same state cache as palmier_place.py, so
`graphics` afterwards only adds clips. RENDER_VER must match the placement run."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import palmier as pm
P = pm.Palmier() if hasattr(pm, "Palmier") else pm
plan = json.load(open("work/lf01/work/palmier_plan.json"))
STATE_F = "work/lf01/work/palmier_state.json"; state = json.load(open(STATE_F))
RENDER_VER = os.environ.get("RENDER_VER", "v5")
def _try_link(a, b):
    try: os.link(a, b); return True
    except OSError: return False   # exFAT / cross-device: no hardlinks
def render_file(name):
    src = f"out/lf01/palmier/{name}"; vdir = f"out/lf01/palmier/{RENDER_VER}"; os.makedirs(vdir, exist_ok=True)
    dst = f"{vdir}/{name}"
    if not os.path.exists(dst): (lambda: __import__('shutil').copy2(src, dst))() if not _try_link(src, dst) else None
    return dst
ONLY = os.environ.get("ONLY", "all")   # all | type | fulls — a type-only re-place should not re-import the fulls
files = ([render_file(f"card_{w['from']:06d}.mp4") for w in plan["cards"]] + [render_file(f"full_{w['from']:06d}.mp4") for w in plan["fulls"]] if ONLY in ("all", "fulls") else []) \
      + ([render_file(f"type_{w['from']:06d}.mov") for w in plan["types"]] if ONLY in ("all", "type") else [])
todo = [f for f in files if os.path.abspath(f) not in state["media"]]
print(f"{len(files)} render files, {len(todo)} to import")
for i, f in enumerate(todo):
    path = os.path.abspath(f)
    for attempt in range(3):
        try:
            r = P.call("import_media", {"source": {"path": path}, "folder": "lf01/render"}); break
        except Exception as e:
            print("  retry", attempt, os.path.basename(f), str(e)[:80]); time.sleep(20)
    else: sys.exit(f"import failed: {f}")
    state["media"][path] = r.get("mediaRef") or r.get("id"); json.dump(state, open(STATE_F, "w"), indent=1)
    if (i + 1) % 8 == 0:
        print(f"  {i+1}/{len(todo)} imported, pausing"); time.sleep(6)
print("imports done:", len(todo))
