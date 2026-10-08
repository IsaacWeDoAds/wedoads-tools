#!/usr/bin/env python3
"""measure_take.py — hair top / chin / head-cx as DISTRIBUTIONS across a whole take.

Why this exists: a fit calibrated on three frames that happen to agree centres those
three frames and leaves the subject visibly off for the rest of the reel. That shipped
once and was caught in review. Sample the midpoint of EVERY kept clip instead.

    python3 measure_take.py TAKE.mp4 --beats work/reelNN/work/beats.txt
    python3 measure_take.py TAKE.mp4 --every 1.5        # no beats file yet
    python3 measure_take.py TAKE.mp4 --beats b.txt --card 1008x1050 --headroom 0.11

beats.txt is `start end label` per line (seconds), '#' comments allowed.

Outputs per-frame rows, the weighted medians, and — when --card is given — the SOLVED
fit {scale, dx, dy} plus the tightest-frame headroom assertion.

Detector caveats this encodes (all cost real time before they were written down):
  * Haar's box BOTTOM is not the chin. We never use it; chin comes from the skin scan
    and should still be eyeballed on a grid crop.
  * Haar's box TOP is not the hairline either. The offset is per-take, so we report
    BOTH a direct dark/bright-row hairline scan and the box offset, and tell you which
    one to trust based on the background's contrast against hair.
  * A dark-row scan is useless when the background is as dark as the hair (dim
    corridor). We measure background luma behind the head and warn.
  * Background passers-by register as hair. Hits outside the head's x-band are dropped.
  * Rotation side-data lies to OpenCV. We decode with -noautorotate and report the
    frame size actually returned, so a mis-tagged clip is obvious immediately.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

try:
    import cv2
except ImportError:
    sys.exit("needs opencv-python:  pip install opencv-python")


def probe(src):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,duration,side_data_list", "-of", "json", src],
        capture_output=True, text=True).stdout
    st = json.loads(out)["streams"][0]
    rot = 0
    for sd in st.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = sd["rotation"]
    return int(st["width"]), int(st["height"]), float(st.get("duration") or 0), rot


def grab(src, t, w, h):
    """Raw pixels, rotation metadata deliberately ignored — see module docstring."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-noautorotate", "-ss", f"{t:.3f}", "-i", src,
         "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24",
         "-vf", "scale=in_range=pc:out_range=tv", "-"],
        capture_output=True).stdout
    if len(raw) != w * h * 3:
        return None
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3)


def measure_frame(img, det):
    h, w, _ = img.shape
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    boxes = det.detectMultiScale(grey, 1.1, 5, minSize=(120, 120))
    boxes = [b for b in boxes if 150 <= b[2] <= 340]          # reject bad detections
    if not boxes:
        return None
    x, y, bw, bh = max(boxes, key=lambda b: b[2])
    cx = x + bw // 2
    band = slice(max(0, cx - bw // 2), min(w, cx + bw // 2))

    # background luma above the head — decides whether a hairline scan is trustworthy
    bg = float(grey[max(0, y - 220):max(1, y - 120), band].mean())

    # hairline: first row above the box whose luma departs from the background
    hair = None
    col = grey[:, band]
    for r in range(max(0, y - 260), y):
        if abs(float(col[r].mean()) - bg) > 18:
            hair = r
            break

    # chin: last contiguous skin row below the box centre (r>g>b, r-b>18)
    b, g, r = img[:, band, 0].astype(int), img[:, band, 1].astype(int), img[:, band, 2].astype(int)
    skin = ((r > g) & (g > b) & (r - b > 18)).mean(1)
    chin = None
    for row in range(min(h - 1, y + bh + 320), y + bh // 2, -1):
        if skin[row] > 0.30:
            chin = row
            break

    return dict(box_top=int(y), box_bottom=int(y + bh), cx=int(cx), bg=round(bg, 1),
                hair=None if hair is None else int(hair),
                chin=None if chin is None else int(chin))


def wmedian(vals, weights):
    if not vals:
        return None
    order = np.argsort(vals)
    v, wts = np.array(vals)[order], np.array(weights, float)[order]
    c = np.cumsum(wts) / wts.sum()
    return float(v[np.searchsorted(c, 0.5)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--beats", help="start end label per line, seconds")
    ap.add_argument("--every", type=float, help="sample every N seconds instead")
    ap.add_argument("--fracs", default="0.2,0.4,0.6,0.8",
                    help="sample points within each beat")
    ap.add_argument("--card", help="split card as WxH, e.g. 1008x1050")
    ap.add_argument("--headroom", type=float, default=0.11,
                    help="target hair-top as a fraction of the card's visible height")
    ap.add_argument("--min-clear", type=float, default=90,
                    help="the tightest sampled frame must still clear this many px")
    a = ap.parse_args()

    w, h, dur, rot = probe(a.src)
    print(f"# {a.src}  {w}x{h}  {dur:.1f}s  rotation_side_data={rot}")
    if rot:
        print(f"# WARNING rotation side data = {rot}. Raw pixels are being measured as-is."
              f"\n#         LOOK at a frame before trusting anything below.")

    samples = []
    if a.beats:
        fr = [float(x) for x in a.fracs.split(",")]
        for line in open(a.beats):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            s, e, *lab = line.split()
            s, e = float(s), float(e)
            for f in fr:
                samples.append((s + (e - s) * f, e - s, " ".join(lab)))
    else:
        step = a.every or max(1.0, dur / 24)
        t = step / 2
        while t < dur:
            samples.append((t, step, ""))
            t += step

    det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    rows = []
    for t, weight, lab in samples:
        img = grab(a.src, t, w, h)
        if img is None:
            continue
        m = measure_frame(img, det)
        if not m:
            continue
        m.update(t=round(t, 2), weight=weight, label=lab)
        rows.append(m)
        print(f"  {t:7.2f}s  hair {str(m['hair']):>5}  chin {str(m['chin']):>5}  "
              f"cx {m['cx']:>4}  boxTop {m['box_top']:>4}  bg {m['bg']:>5}  {lab}")

    if not rows:
        sys.exit("no faces detected — check the rotation flag and LOOK at a frame")

    hairs = [(r["hair"], r["weight"]) for r in rows if r["hair"] is not None]
    chins = [(r["chin"], r["weight"]) for r in rows if r["chin"] is not None]
    cxs = [(r["cx"], r["weight"]) for r in rows]
    offs = [r["box_top"] - r["hair"] for r in rows if r["hair"] is not None]

    hair_med = wmedian([v for v, _ in hairs], [x for _, x in hairs])
    chin_med = wmedian([v for v, _ in chins], [x for _, x in chins])
    cx_med = wmedian([v for v, _ in cxs], [x for _, x in cxs])
    hair_min = min(v for v, _ in hairs) if hairs else None

    bg_mean = float(np.mean([r["bg"] for r in rows]))
    print(f"\n# background luma behind head ≈ {bg_mean:.0f}")
    if bg_mean < 70:
        print("# WARNING dark background — the hairline scan is UNRELIABLE on this take.\n"
              f"#         Use the box offset instead: boxTop − {int(np.median(offs)) if offs else '???'}")

    print(f"\nhair top   median {hair_med}   min {hair_min}   max {max(v for v,_ in hairs)}")
    print(f"chin       median {chin_med}")
    print(f"head cx    median {cx_med}   range {min(v for v,_ in cxs)}–{max(v for v,_ in cxs)}")
    print(f"boxTop − hair offset  median {int(np.median(offs)) if offs else 'n/a'}")

    spread = max(v for v, _ in hairs) - hair_min
    if spread > 120:
        print(f"\n# NOTE hair top spreads {spread}px across the take. Check whether it DRIFTS "
              f"monotonically (settle/walk → fit the median, or carry two fits) or SWAYS.")

    if a.card:
        cw, ch = (int(x) for x in a.card.lower().split("x"))
        floor = (cw / 2) / cx_med
        s = max(1.0, round(floor + 0.0005, 3))
        dx = round(cw / 2 - cx_med * s)
        dy = round(a.headroom * ch - hair_med * s)
        tight = hair_min * s + dy
        print(f"\n# card {cw}x{ch}, headroom {a.headroom:.0%} = {a.headroom*ch:.0f}px")
        print(f"# dx<=0 scale floor = (cw/2)/cx = {floor:.4f}")
        print(f"FACE_FIT = {{ scale: {s}, dx: {dx}, dy: {dy} }}")
        print(f"# tightest sampled frame (hair {hair_min}) lands at card y{tight:.0f} "
              f"— {'OK' if tight >= a.min_clear else 'FAIL, raise dy'} "
              f"(floor {a.min_clear:.0f})")
        print(f"# chin lands at card y{chin_med * s + dy:.0f} of {ch}")

    print("\n# Caption band: CAPTION_FACE_Y = max(chin + 180, handTop + 96) — measure handTop "
          "separately; this script does not detect hands.")


if __name__ == "__main__":
    main()
