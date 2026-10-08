#!/usr/bin/env python3
"""Verify the sound layer of a windowed test render against the schedule.
   sfx_check.py <render.mp4> <first_comp_frame>
Decodes the render's audio and the voice track, aligns them (cut audio starts at composition frame PRE=100),
and reports (a) SFX events = 10 ms frames where the render exceeds the voice by >6 dB, merged, as composition
frames; (b) the expected cue frames from data.ts inside the window; (c) loudness / true-peak of the render."""
import sys, re, json, subprocess, numpy as np
PRE, FPS, SR = 100, 30, 48000
rend, a0 = sys.argv[1], int(sys.argv[2])
def dec(path, ss=None, t=None):
    cmd = ["ffmpeg", "-nostdin", "-v", "error"] + (["-ss", str(ss)] if ss else []) + ["-i", path] + (["-t", str(t)] if t else []) + ["-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, dtype=np.float32)
r = dec(rend)
n = len(r) / SR
# voice aligned to the render: render t  ↔  cut t = (a0 - PRE)/FPS + t
off = (a0 - PRE) / FPS
if off >= 0:
    v = dec("public/broll/lf01/cut.wav", ss=off, t=n)
else:
    v = np.concatenate([np.zeros(int(-off * SR), np.float32), dec("public/broll/lf01/cut.wav", t=n + off)])
m = min(len(r), len(v)); r, v = r[:m], v[:m]
# sample-accurate alignment (the render's AAC carries a priming offset): cross-correlate an 8 s voiced chunk
def lag_of(r, v):
    vo = np.where(np.abs(v) > 0.02)[0]
    if len(vo) < SR: return 0
    a = vo[0] + SR // 2; b = min(a + 8 * SR, len(v))
    if b - a < 2 * SR: return 0
    x, y = r[a:b] - r[a:b].mean(), v[a:b] - v[a:b].mean()
    nfft = 1 << int(np.ceil(np.log2(len(x) * 2)))
    cc = np.fft.irfft(np.fft.rfft(x, nfft) * np.conj(np.fft.rfft(y, nfft)), nfft)
    w = int(0.2 * SR)
    cand = np.concatenate([cc[:w], cc[-w:]])
    i = int(cand.argmax()); return i if i < w else i - 2 * w
lag = lag_of(r, v)
v = np.roll(v, lag); 
if lag > 0: v[:lag] = 0
elif lag < 0: v[lag:] = 0
voiced_mask = np.abs(v) > 0.01
g = float((r[voiced_mask] * v[voiced_mask]).sum() / ((v[voiced_mask] ** 2).sum() + 1e-9)) if voiced_mask.any() else 1.0
res = r - g * v
hop = SR // 100
k = m // hop
env = lambda x: 20 * np.log10(np.sqrt((x[: k * hop].reshape(k, hop) ** 2).mean(axis=1)) + 1e-7)
er, ev, es = env(r), env(v), env(res)
diff = er - ev
hot = es > -36
events, i = [], 0
while i < k:
    if hot[i]:
        j = i
        while j < k and (hot[j] or (j - i) < 10): j += 1
        events.append((a0 + i / 100 * FPS, (j - i) / 100, es[i:j].max(), (es[i:j] - ev[i:j]).max()))
        i = j
    else: i += 1
print(f"voice alignment lag {lag/SR*1000:+.1f} ms, gain {20*np.log10(g+1e-9):+.1f} dB; residual (render − voice) drives the events below")
print(f"render {rend}: {n:.1f}s, comp frames {a0}–{a0 + int(n * FPS)}")
lo = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", rend, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
I = re.findall(r"I:\s+(-?[\d.]+) LUFS", lo); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", lo); I = I[-1:] or ["?"]; TP = TP[-1:] or ["?"]
print(f"loudness I={I[0]} LUFS  true-peak={TP[0]} dBTP  (voice-only track is -17.6 LUFS)")
voiced = ev > -35
print(f"voice frames: {voiced.mean()*100:.0f}% of window; median render−voice over voiced frames {np.median(diff[voiced]):+.1f} dB (beds+sfx bleed)")
print(f"\n{len(events)} SFX events in the residual (comp frame, length s, peak dBFS, +dB over voice):")
for f, ln, pk, d in events: print(f"  f{f:7.0f}  {ln:4.2f}s  {pk:6.1f}  +{d:4.1f}")
ts = open("src/LF01/data.ts").read()
J = lambda name: json.loads(re.search(r"export const %s[^=]*= (\[.*?\])(?: as const)?;\n" % name, ts, re.S).group(1))
a1 = a0 + int(n * FPS)
exp = []
for s in J("SHOTS"):
    if a0 <= s["from"] + PRE < a1: exp.append((s["from"] + PRE, "glitch" if s["glitch"] else ("hero " + s["src"][5:] if s["src"].startswith("hero:") else s["kind"] + " " + s["src"].split("/")[-1][:22])))
for s in J("STAMPS"):
    if a0 <= s["from"] + PRE < a1: exp.append((s["from"] + PRE, "stamp " + s["text"][:24]))
for e in J("EMPH"):
    if a0 <= e["from"] + PRE < a1: exp.append((e["from"] + PRE, ("OMNI " if e.get("omni") else "lockup ") + e["text"]))
for h in J("HEROES"):
    for it in h["items"]:
        if a0 <= it["at"] + PRE < a1: exp.append((it["at"] + PRE, f"  item {h['id']}:{it['label'][:14]}"))
if a0 <= PRE < a1: exp.append((PRE, "CUT TO HIM (reversed hit lands)"))
for i in range(4):
    if a0 <= i * 25 < a1: exp.append((i * 25, "montage bite (shutter)"))
print(f"\n{len(exp)} expected cue frames in the window:")
for f, t in sorted(exp): print(f"  f{f:7d}  {t}")
