#!/usr/bin/env python3
"""build_wx2.py — the v2 cut builder (Oct 2026). Same inputs as build_wx.py, but every EDGE is decided on the
audio envelope, because each of these shipped in a real edit with the v1 rules:
  * word ENDS from WhisperX run early on decays          -> "free" / "AI" / "gate" lost their last syllable
  * word STARTS from WhisperX can run ~0.4 s late         -> the onsets of "in", "canvas", "These" were cut
  * a beat END copied from a word's START drops that word -> 15 clipped last words in one 16-min edit
  * a head that searches back for 120 ms of quiet walks over a separate "hm" / false-start syllable
  * a gap measured on word times (not on audio) invents silences inside continuous speech
Rules: tail = envelope release + 60 ms, capped before the NEXT word's envelope onset; head = the envelope
onset (found by walking back from the word), never back over a separate voiced island; split a beat only
where the ENVELOPE is silent for > GAP; a cut that lands on voice slides to the quietest 10 ms within 60 ms.

Usage: build_wx2.py AUDIO.wav CLIP_wx.json beats.txt [GAP=0.30] [FPS=30] > cut.json
  AUDIO.wav  mono WAV of the source (ffmpeg -i SRC -vn -ac 1 -ar 16000 AUDIO.wav)
  beats.txt  one beat per line: START END label   (END = where the last kept word RELEASES, not where the
             next word starts; the builder warns when an END sits on a word start or inside a word)
Output: {"audio", "fps", "pieces": [{id, a, b, dur, text, w0, w1, beat, fade_in, fade_out}], "total"}
  fade_in/fade_out = true on every edge that is a real cut (not a source-contiguous join): apply a 15 ms
  fade-in / 25 ms fade-out there in your editor (HyperFrames: data-fade-in / data-fade-out) — no clicks.
stderr lists every piece and every warning. Then run edge_sweep.py and the cut-audit skill on the result.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from envtools import env, thr, speech_end, speech_start, onset_before, release_after, islands, quiet

AUD, WX, BEATS = sys.argv[1], sys.argv[2], sys.argv[3]
GAP = float(sys.argv[4]) if len(sys.argv) > 4 else 0.30
FPS = float(sys.argv[5]) if len(sys.argv) > 5 else 30.0
KEEP = 0.16
UMS = {"uh", "um", "umm", "uhh", "hmm", "mm", "err", "eh"}
E, TH = env(AUD), thr(AUD)
W = sorted(({"s": w["s"], "e": w["e"], "w": w["w"]} for w in json.load(open(WX))), key=lambda w: w["s"])
warn = []


def silent_run(a, b):
    best = cur = 0
    for v in E[int(a * 100):int(b * 100)] < TH:
        cur = cur + 1 if v else 0; best = max(best, cur)
    return best / 100


beats = []
for ln in open(BEATS):
    ln = ln.strip()
    if ln and not ln.startswith("#"):
        a, b, *r = ln.split(); beats.append((float(a), float(b), " ".join(r)))

pieces = []
for bi, (A, B, lab) in enumerate(beats):
    for w in W:   # the gate that would have caught the 15 clipped words
        if abs(w["s"] - B) <= 0.05: warn.append(f"beat {bi} END {B:.2f} sits on the START of '{w['w']}' ({w['s']:.2f}) — "
                                                f"if that word belongs to the beat, set END to its release (~{release_after(AUD, w['e']):.2f})")
        elif w["s"] < B - 0.05 < B + 0.05 < w["e"]: warn.append(f"beat {bi} END {B:.2f} falls INSIDE '{w['w']}' ({w['s']:.2f}-{w['e']:.2f})")
    ws = [w for w in W if A <= (w["s"] + w["e"]) / 2 <= B and w["w"].lower().strip(".,!?") not in UMS]
    if not ws: warn.append(f"beat {bi} {A:.2f}-{B:.2f}: no words"); continue
    runs, cur = [], [ws[0]]
    for w in ws[1:]:
        if silent_run(cur[-1]["e"], w["s"]) > GAP: runs.append(cur); cur = [w]
        else: cur.append(w)
    runs.append(cur)
    for k, r in enumerate(runs):
        s0, e0 = r[0]["s"], r[-1]["e"]
        prev = [w for w in W if w["e"] <= s0 - 0.01]; nxt = [w for w in W if w["s"] >= e0 + 0.01]
        lo = prev[-1]["e"] if prev else 0.0
        # head
        ia = min(speech_start(AUD, s0 + 0.02, 0.35) - 0.06, s0 - 0.06)
        floor_ = (release_after(AUD, max(lo - 0.02, 0)) + 0.02) if prev else 0.0
        ia = max(ia, s0 - KEEP - 0.12, floor_)
        on0 = onset_before(AUD, s0 + 0.02, 0.6)                      # WhisperX start late? find the real onset
        if s0 - 0.45 <= on0 - 0.04 < ia - 0.01 and on0 - 0.04 > floor_: ia = on0 - 0.04
        isl = [x for x in islands(AUD, ia, s0 + 0.02) if x[1] < s0 - 0.04 and x[1] - x[0] >= 0.05]
        if isl: warn.append(f"beat {bi}.{k}: skipped a separate voiced fragment {isl[-1][0]:.2f}-{isl[-1][1]:.2f} before '{r[0]['w']}'"); ia = isl[-1][1] + 0.03
        # tail
        ib = min(speech_end(AUD, e0, 0.7) + 0.06, e0 + 0.55)
        if nxt:
            on = onset_before(AUD, nxt[0]["s"] + 0.02)
            ib = min(ib, on - 0.03) if on > e0 + 0.05 else min(ib, nxt[0]["s"] - 0.04)
        # a cut on voice slides to the valley
        for which in ("a", "b"):
            t_ = ia if which == "a" else ib; i0 = int(t_ * 100)
            if 6 <= i0 < len(E) - 7 and E[i0] > TH - 3:
                m, db = quiet(AUD, t_, 0.06)
                if db < E[i0] - 3:
                    if which == "a": ia = m
                    else: ib = m
        pieces.append(dict(beat=bi, a=round(max(0.0, ia), 4), b=round(ib, 4), w0=s0, w1=e0, text=" ".join(w["w"] for w in r)))

# source-contiguous neighbours share ONE boundary (no audio played twice, none skipped) — but only when no source
# word lies between them: a deliberately dropped fragment must never be re-joined.
for p, q in zip(pieces, pieces[1:]):
    between = [w for w in W if p["w1"] < w["s"] < q["w0"]]
    if -0.5 < q["a"] - p["b"] < 0.35 and q["w0"] >= p["w1"] and not between:
        m, _ = quiet(AUD, (p["w1"] + q["w0"]) / 2, max(0.005, (q["w0"] - p["w1"]) / 2 - 0.005))
        p["b"] = q["a"] = round(m, 4)

t = 0.0
for i, p in enumerate(pieces):
    p["id"] = f"p{i:03d}"
    p["dur"] = round(round((p["b"] - p["a"]) * FPS) / FPS, 4)
    p["fade_in"] = not (i and abs(pieces[i - 1]["b"] - p["a"]) < 0.03)
    p["fade_out"] = not (i + 1 < len(pieces) and abs(p["b"] - pieces[i + 1]["a"]) < 0.03)
    t += p["dur"]
json.dump({"audio": AUD, "fps": FPS, "pieces": pieces, "total": round(t, 3)}, sys.stdout, indent=1)
print(f"# {len(pieces)} pieces, {t:.2f}s (GAP={GAP}s on the envelope)", file=sys.stderr)
for p in pieces:
    print(f"#  {p['id']} {p['a']:8.2f}-{p['b']:8.2f} ({p['dur']:4.1f}s) beat {p['beat']}  «{p['text'][:60]}»", file=sys.stderr)
for w in warn: print("WARN", w, file=sys.stderr)
