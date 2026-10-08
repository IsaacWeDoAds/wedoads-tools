#!/usr/bin/env python3
"""face_guard.py — assert no graphic ever covers Nishant's face.

Reads the ALPHA channel of a graphics-only (transparent) render and fails if any
opaque graphic pixel lands inside the measured face band on a frame where the
face is actually visible.

Two traps this deliberately avoids (both cost real time on earlier reels):

  * Do NOT detect the face by dark pixels — caption drop-shadows read as dark
    and false-positive as "hair". The alpha of the GRAPHICS layer answers the
    real question: "is there a graphic here".
  * A full-frame MG beat is ~100% opaque by design. Frames whose alpha coverage
    is above --max-coverage are register changes that hide the face on purpose,
    and are skipped rather than flagged.

Usage:
  face_guard.py OVERLAY.mov --top 442 --bottom 1111 [--max-coverage 0.85]
                            [--alpha 40] [--tolerance 0]
"""
import argparse
import json
import subprocess
import sys

import numpy as np

W, H = 1080, 1920


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("overlay")
    ap.add_argument("--top", type=int, required=True, help="face band top (px)")
    ap.add_argument("--bottom", type=int, required=True, help="face band bottom (px)")
    ap.add_argument("--left", type=int, default=0)
    ap.add_argument("--right", type=int, default=W)
    ap.add_argument("--alpha", type=int, default=40, help="alpha above this = opaque")
    ap.add_argument("--max-coverage", type=float, default=0.85)
    ap.add_argument("--tolerance", type=int, default=0, help="allowed opaque px")
    ap.add_argument("--json", dest="json_out")
    args = ap.parse_args()

    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", args.overlay,
         "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
        stdout=subprocess.PIPE,
    )
    assert proc.stdout is not None

    frame_bytes = W * H * 4
    violations = []
    skipped = 0
    n = 0
    while True:
        buf = proc.stdout.read(frame_bytes)
        if len(buf) < frame_bytes:
            break
        a = np.frombuffer(buf, dtype=np.uint8).reshape(H, W, 4)[:, :, 3]
        opaque = a > args.alpha
        coverage = float(opaque.mean())
        if coverage <= args.max_coverage:
            band = opaque[args.top:args.bottom, args.left:args.right]
            hits = int(band.sum())
            if hits > args.tolerance:
                ys, xs = np.nonzero(band)
                violations.append({
                    "frame": n,
                    "opaque_px": hits,
                    "coverage": round(coverage, 4),
                    "y_range": [int(ys.min()) + args.top, int(ys.max()) + args.top],
                    "x_range": [int(xs.min()) + args.left, int(xs.max()) + args.left],
                })
        else:
            skipped += 1
        n += 1
    proc.wait()

    print(f"frames checked: {n - skipped}   full-frame MG skipped: {skipped}")
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(violations, fh, indent=2)

    # A guard that inspected nothing must never report PASS — an unreadable or
    # missing render would otherwise look identical to a clean reel.
    if n == 0:
        print("FAIL — decoded 0 frames; the overlay render is missing or unreadable")
        return 2
    if n - skipped == 0:
        print("FAIL — every frame was skipped as full-frame MG; check --max-coverage")
        return 2

    if not violations:
        print(f"PASS — no graphic inside the face band y{args.top}–{args.bottom}")
        return 0

    print(f"FAIL — {len(violations)} frame(s) put a graphic on the face:")
    for v in violations[:25]:
        print(f"  f{v['frame']:5d}  {v['opaque_px']:7d}px  "
              f"y{v['y_range'][0]}–{v['y_range'][1]}  x{v['x_range'][0]}–{v['x_range'][1]}")
    if len(violations) > 25:
        print(f"  … and {len(violations) - 25} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
