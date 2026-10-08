#!/usr/bin/env python3
"""Measure a Paper Drawer render against the reference numbers.

Per frame, finds the drawer seam (the top edge of the face card) by scanning
down the two 16-px edge strips for the first row that stops being plain paper.
Paper rows are bright and flat at the frame edge; the face footage is not.

  python3 measure_drawer.py OUT.mp4 [--seam 820]

Prints: resting seam y, the register runs (SPLIT / PAPER / FULL-FACE / MOVE)
with durations, the frame count of every drawer move, and the face share.
Reference (this tool on assets/style-refs/paper-drawer/): seam y820, moves read
8-9 f (the curve is 10 f; its first and last frames sit inside the 6 px rest
tolerance), split runs 4.3-5.1 s, paper runs 2.2-2.8 s, face on screen 62%.
Confetti or a card touching BOTH edges can fake a short MOVE inside a PAPER run.

A row is paper when EITHER edge strip is plain paper (a sticker may touch one
edge), face when both fail; flickers under 3 frames are merged away.
Limitation: a take with a flat near-white wall at one frame edge reads as
paper there. If the seam reads low, pass --edge-x 40 to move the strips inward.
"""
import argparse
import cv2
import numpy as np


def paper_rows(gray, edge_x, strip=16, luma=205, flat=7.0):
    left = gray[:, edge_x:edge_x + strip].astype(np.float32)
    right = gray[:, -edge_x - strip:gray.shape[1] - edge_x].astype(np.float32)
    lok = (left.mean(1) > luma) & (left.std(1) < flat)
    rok = (right.mean(1) > luma) & (right.std(1) < flat)
    # a sticker may touch ONE edge; the face card fails BOTH
    return lok | rok


def seam_of(gray, edge_x, start=300, run=8):
    ok = paper_rows(gray, edge_x)
    h = gray.shape[0]
    if not ok[start:start + 40].any():
        return 0                      # no paper at the top: face is full frame
    bad = 0
    for y in range(start, h):
        bad = bad + 1 if not ok[y] else 0
        if bad >= run:
            return y - run + 1
    return h                          # paper all the way down: drawer away


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--seam", type=int, default=820, help="expected resting seam y")
    ap.add_argument("--edge-x", type=int, default=0)
    a = ap.parse_args()

    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    seams = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        if g.shape[1] != 1080:
            g = cv2.resize(g, (1080, int(g.shape[0] * 1080 / g.shape[1])))
        seams.append(seam_of(g, a.edge_x))
    h = 1920
    tol = 6

    def label(s):
        if abs(s - a.seam) <= tol:
            return "SPLIT"
        if s >= h - 4:
            return "PAPER"
        if s == 0:
            return "FULL-FACE"
        return "MOVE"

    labels = [label(s) for s in seams]
    # merge flickers shorter than 3 frames into the preceding register
    for _ in range(2):
        runs, i = [], 0
        while i < len(labels):
            j = i
            while j + 1 < len(labels) and labels[j + 1] == labels[i]:
                j += 1
            runs.append((labels[i], i, j))
            i = j + 1
        for k, (lab, s, e) in enumerate(runs):
            if e - s + 1 < 3 and 0 < k < len(runs) - 1 and runs[k - 1][0] == runs[k + 1][0]:
                for q in range(s, e + 1):
                    labels[q] = runs[k - 1][0]
    runs, i = [], 0
    while i < len(labels):
        j = i
        while j + 1 < len(labels) and labels[j + 1] == labels[i]:
            j += 1
        runs.append((labels[i], i, j))
        i = j + 1

    rest = [s for s in seams if 0 < s < h - 4]
    if rest:
        vals, counts = np.unique(rest, return_counts=True)
        print(f"resting seam: y{int(vals[counts.argmax()])} (expected y{a.seam})")
    print(f"{'register':10s} {'start':>7s} {'end':>7s} {'dur':>6s}")
    for lab, s, e in runs:
        print(f"{lab:10s} {s / fps:7.2f} {(e + 1) / fps:7.2f} {(e - s + 1) / fps:6.2f}s"
              + (f"  ({e - s + 1} f)" if lab == "MOVE" else ""))
    moves = [e - s + 1 for lab, s, e in runs if lab == "MOVE"]
    split = [(e - s + 1) / fps for lab, s, e in runs if lab == "SPLIT"]
    paper = [(e - s + 1) / fps for lab, s, e in runs if lab == "PAPER"]
    face = sum(1 for l in labels if l in ("SPLIT", "FULL-FACE")) / max(1, len(labels))
    print(f"\nmoves: {len(moves)}  frames each: {moves}  (reference 8-9; curve is 10 f)")
    if split:
        print(f"split runs: {min(split):.1f}-{max(split):.1f}s  (reference 4.3-5.1, <=6)")
    if paper:
        print(f"paper runs: {min(paper):.1f}-{max(paper):.1f}s  (reference 2.2-2.8, <=3.5)")
    print(f"face on screen: {face:.0%}  (reference ~62%)")


if __name__ == "__main__":
    main()
