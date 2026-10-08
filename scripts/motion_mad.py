#!/usr/bin/env python3
"""Mean-absolute-frame-difference motion metric.

checkMotion()'s scene detector (gt(scene,0.008)) is built for browser tours that
scroll; it barely fires on element pops/fades inside a card and scored a working
design card at 0-1% (motion-gate-calibration). This is the calibrated
replacement: downscale to 160x100 grey, count frames where mean|Δ| > 0.35.

The STATIC-RUN length matters more than the percentage — Apple's own footage
never holds still for more than 3-5 frames.

  python3 scripts/motion_mad.py FILE [crop=w:h:x:y]
"""
import subprocess, sys
import numpy as np

f = sys.argv[1]
crop = sys.argv[2] if len(sys.argv) > 2 else None
vf = (f"{crop}," if crop else "") + "scale=160:100,format=gray"
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", vf,
                      "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                     capture_output=True).stdout
n = len(raw) // (160 * 100)
a = np.frombuffer(raw[: n * 160 * 100], np.uint8).reshape(n, 100, 160).astype(np.int16)
d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
moving = d > 0.35
pct = round(100 * moving.mean())
runs, cur, worst = [], 0, 0
for m in moving:
    if m:
        if cur: runs.append(cur)
        cur = 0
    else:
        cur += 1
if cur: runs.append(cur)
worst = max(runs) if runs else 0
verdict = "OK" if pct >= 30 and worst <= 12 else ("THIN" if pct >= 25 else "SLIDESHOW")
print(f"{f}")
print(f"  frames {n} · moving {pct}% · longest static run {worst} frames  [{verdict}]")
print(f"  (Apple reference: 33-50% moving, static runs 3-5 frames)")
