#!/bin/zsh
# Swap the re-rendered comment-composer window onto the Type track and re-place the SFX lanes (the like cue moved
# to 373.5 s). Needs the JobMarket project IN FRONT in Palmier. ~1 minute.
set -e; cd "<project>"; export RENDER_VER=v12
python3 - <<'EOF'
import sys, json
sys.path.insert(0, "work/lf01/work"); import palmier as pm
P = pm.Palmier() if hasattr(pm, "Palmier") else pm
l = P.call("manage_project", {"action": "list"}); assert l["active"]["name"] == "JobMarket", f"active project is {l['active']['name']} — bring JobMarket to the front first"
EOF
RENDER_VER=v12 python3 work/lf01/work/palmier_retype.py | tail -1
for t in SFX1 SFX2 SFX3 SFX4 SFX5 SFX6 SFX7 SFX8 Preroll; do python3 work/lf01/work/palmier_place.py droptrack $t 2>/dev/null | grep -v "no such" || true; done
python3 work/lf01/work/palmier_place.py sfx | tail -1
python3 work/lf01/work/palmier_place.py sfxfix | tail -1
python3 work/lf01/work/palmier_place.py reorder | tail -1
setopt null_glob; rm -f out/lf01/palmier/review/*.png
python3 work/lf01/work/palmier_review.py 374.2 382.0 384.2 388.6 | tail -1
