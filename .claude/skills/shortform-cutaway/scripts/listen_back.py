#!/usr/bin/env python3
"""listen_back.py — the assembled-cut listen-back (v2, Oct 2026). Assembles the cut's audio exactly as it will
play, transcribes 4.4 s around EVERY join with a fresh decoder, and flags a 2-3 word phrase that repeats within
6 words (a doubled take across a join) — plus prints what is actually heard, so a clipped word ("using AI" ->
"using") or a fumble left in ("or a Claude or a Claude") is visible in one pass.

The right ALARM, never the diagnosis: Whisper reconstructs across a splice and localises a fold to the wrong side.
Confirm every hit with probe.py on the raw source + the envelope (envtools.py AUDIO.wav T).

Usage: listen_back.py cut.json [--all]      (needs OPENAI_API_KEY; --all prints every join, default prints hits)
"""
import concurrent.futures as cf, json, re, sys, wave
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from probe import key, tx

C = json.load(open(sys.argv[1])); P = C["pieces"]
w = wave.open(C["audio"]); sr = w.getframerate(); ch = w.getnchannels()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
if ch > 1: x = x.reshape(-1, ch).mean(1).astype(np.int16)
cut, starts, t = [], [], 0.0
for p in P:
    n = round(p.get("dur", p["b"] - p["a"]) * sr); starts.append(t)
    cut.append(x[int(p["a"] * sr):int(p["a"] * sr) + n]); t += n / sr
cut = np.concatenate(cut); K = key()
LEGIT = {"you can see", "as you can", "you can", "all the", "of the", "the same", "and the", "this is"}


def job(i):
    t0 = starts[i]
    return i, tx(cut[int(max(0, t0 - 2.2) * sr):int((t0 + 2.2) * sr)], sr, "whisper-1", K)


hits = 0
with cf.ThreadPoolExecutor(8) as ex:
    for i, txt in ex.map(job, range(1, len(P))):
        ws = re.findall(r"[a-z0-9']+", txt.lower()); rep = None
        for n in (3, 2):
            seen = {}
            for k in range(len(ws) - n + 1):
                g = " ".join(ws[k:k + n])
                if g in seen and k - seen[g] <= 6 and g not in LEGIT: rep = g; break
                seen.setdefault(g, k)
            if rep: break
        tl = starts[i]
        if rep: hits += 1
        if rep or "--all" in sys.argv:
            print(f"{'REPEAT' if rep else '      '} {P[i]['id']:6} @{int(tl // 60)}:{tl % 60:05.2f} {('[' + rep + ']') if rep else ''} | {txt}", flush=True)
print(f"{hits} joins with a repeated phrase of {len(P) - 1} — most are legit parallels ('the latest video, the latest vlog'); "
      f"probe the rest", file=sys.stderr)
