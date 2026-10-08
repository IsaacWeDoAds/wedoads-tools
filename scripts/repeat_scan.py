#!/usr/bin/env python3
"""repeat_scan.py — catch a false-start/redo pair that ASR cannot hear.

Whisper COLLAPSES an immediate repeat ("Week 1 and… Week 1 and 2" transcribes as
one clean phrase), so a caption-sync check and a re-transcribe both pass while
the viewer plainly hears the stutter. This compares each speech burst against
the head of the next one with a DTW distance over log-mel frames: the same words
spoken twice score far above unrelated speech.

  python3 scripts/repeat_scan.py AUDIO_OR_VIDEO [threshold]

Measured on reel49ai: real repeats 0.83-0.91, unrelated control pairs ~0.66.
"""
import subprocess, sys
import numpy as np

SRC = sys.argv[1]
THR = float(sys.argv[2]) if len(sys.argv) > 2 else 0.78
SR = 16000
raw = subprocess.run(["ffmpeg","-v","error","-i",SRC,"-ac","1","-ar",str(SR),"-f","s16le","-"],
                     capture_output=True).stdout
a = np.frombuffer(raw, np.int16).astype(np.float32)/32768
H = 160
n = len(a)//H
db = 20*np.log10(np.sqrt((a[:n*H].reshape(n,H)**2).mean(axis=1))+1e-9)
fl = np.percentile(db, 5)
on = db > fl + 14
runs, s = [], None
for i, v in enumerate(on):
    if v and s is None: s = i
    if not v and s is not None: runs.append([s, i]); s = None
if s is not None: runs.append([s, len(on)])
m = []
for r in runs:                       # join only within-word gaps
    if m and r[0]-m[-1][1] < 8: m[-1][1] = r[1]
    else: m.append(r)
B = [(r[0]/100, r[1]/100) for r in m if (r[1]-r[0]) >= 30]

def logmel(t0, t1, nmel=26):
    x = a[int(t0*SR):int(t1*SR)]
    if len(x) < 512: return None
    N, Hh = 512, 160
    fr = [x[i:i+N]*np.hanning(N) for i in range(0, len(x)-N, Hh)]
    S = np.abs(np.fft.rfft(np.array(fr), axis=1))**2
    f = np.linspace(0, SR/2, S.shape[1]); mm = 2595*np.log10(1+f/700)
    ed = np.linspace(mm.min(), mm.max(), nmel+2); fb = np.zeros((nmel, S.shape[1]))
    for i in range(nmel):
        l, c, r2 = ed[i], ed[i+1], ed[i+2]
        fb[i] = np.clip(np.minimum((mm-l)/(c-l+1e-9), (r2-mm)/(r2-c+1e-9)), 0, None)
    M = np.log(S@fb.T+1e-10); return (M-M.mean(0))/(M.std(0)+1e-9)

def sim(A, Bm):
    if A is None or Bm is None: return 0.0
    D = 1-(A@Bm.T)/(np.linalg.norm(A,axis=1)[:,None]*np.linalg.norm(Bm,axis=1)[None,:]+1e-9)
    nn, mm2 = D.shape; C = np.full((nn+1, mm2+1), np.inf); C[0,0] = 0
    for i in range(1, nn+1):
        for j in range(1, mm2+1):
            C[i,j] = D[i-1,j-1]+min(C[i-1,j], C[i,j-1], C[i-1,j-1])
    return 1-C[nn,mm2]/(nn+mm2)

hits = []
for i in range(len(B)-1):
    (s1,e1),(s2,e2) = B[i], B[i+1]
    if s2-e1 > 2.5: continue
    L = min(e1-s1, e2-s2, 1.6)
    if L < 0.30: continue
    v = sim(logmel(s1,s1+L), logmel(s2,s2+L))
    if v >= THR:
        hits.append((s1,e1,s2,e2,v))
        print(f"  REPEAT  {s1:7.2f}-{e1:6.2f}  ->  {s2:7.2f}-{e2:6.2f}   sim {v:.3f}")
print(f"{len(B)} bursts · {len(hits)} repeat pair(s) at threshold {THR}")
sys.exit(1 if hits else 0)
