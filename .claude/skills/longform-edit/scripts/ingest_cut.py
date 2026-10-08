#!/usr/bin/env python3
"""Ingest Nishant's own cut (from Palmier) and rebuild the cut↔source map so every source-anchored
cue (shots, stamps, emphasis, Omni) lands on his timeline.

  python3 work/lf01/work/ingest_cut.py HIS_CUT.mp4

1. conform video → public/broll/lf01/cut.mp4 (1920x1080 CFR 30, 8-bit) and audio → cut.wav
2. WhisperX (language=en) on his audio → words
3. match his words to the SOURCE word list (work/lf01/work/lf01_wx_en.json) by sequence alignment
4. runs of matched words with a near-constant (cut − source) offset become segments
   → work/lf01/work/segments.json  {from,len,srcS,srcE}  (cut frames ↔ source seconds)
5. report coverage; unmatched stretches are listed so they can be checked by ear.
"""
import sys, os, json, subprocess, re, difflib
SRC = sys.argv[1]; FPS = 30
os.makedirs("public/broll/lf01", exist_ok=True)
info = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height,r_frame_rate:format=duration","-of","csv=p=0",SRC],capture_output=True,text=True).stdout
print("his export:", info.strip().replace("\n"," "))
subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-vf","scale=1920:1080:flags=lanczos,fps=30,format=yuv420p","-c:v","libx264","-preset","fast","-crf","16","-an","public/broll/lf01/cut.mp4"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-vn","-ac","2","-ar","48000","-c:a","pcm_s16le","public/broll/lf01/cut.wav"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-vn","-ac","1","-ar","16000","-c:a","pcm_s16le","work/lf01/work/hiscut_16k.wav"],check=True)
nf = int(subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-count_frames","-show_entries","stream=nb_read_frames","-of","csv=p=0","public/broll/lf01/cut.mp4"],capture_output=True,text=True).stdout.strip().strip(","))
ad = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","public/broll/lf01/cut.wav"],capture_output=True,text=True).stdout.strip())
print(f"conformed: {nf} frames = {nf/FPS:.2f}s video, {ad:.2f}s audio  (A/V Δ {nf/FPS-ad:+.3f}s)")
# 2. transcribe + align his cut
code = '''
import json, whisperx, sys
audio = whisperx.load_audio("work/lf01/work/hiscut_16k.wav")
m = whisperx.load_model("medium", "cpu", compute_type="int8", language="en")
res = m.transcribe(audio, batch_size=8, language="en")
ma, meta = whisperx.load_align_model(language_code="en", device="cpu")
al = whisperx.align(res["segments"], ma, meta, audio, "cpu", return_char_alignments=False)
words = [{"s": round(w["start"],3), "e": round(w["end"],3), "w": w.get("word","")} for s in al["segments"] for w in s.get("words",[]) if "start" in w]
json.dump(words, open("work/lf01/work/hiscut_wx.json","w"))
print(len(words), "words", file=sys.stderr)
'''
subprocess.run([os.path.expanduser("~/wx-env/bin/python"),"-c",code],check=True,env={**os.environ,"OMP_NUM_THREADS":"6"})
H = json.load(open("work/lf01/work/hiscut_wx.json")); S = json.load(open("work/lf01/work/lf01_wx_en.json"))
norm = lambda w: re.sub(r"[^a-z0-9]","",w.lower())
ht = [norm(w["w"]) for w in H]; st = [norm(w["w"]) for w in S]
sm = difflib.SequenceMatcher(None, ht, st, autojunk=False)
pairs = []   # (his_word_idx, src_word_idx)
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag == "equal":
        pairs += [(i1+k, j1+k) for k in range(i2-i1)]
print(f"matched {len(pairs)} of {len(H)} words in his cut ({100*len(pairs)/max(1,len(H)):.0f}%)")
# 4. segments from runs with a stable offset
segs = []; cur = None
for hi, si in pairs:
    off = H[hi]["s"] - S[si]["s"]
    if cur and abs(off - cur["off"]) < 0.12 and si > cur["si_last"]:
        cur["hi_last"] = hi; cur["si_last"] = si; cur["off"] = 0.8*cur["off"] + 0.2*off
    else:
        if cur: segs.append(cur)
        cur = {"hi_first": hi, "hi_last": hi, "si_first": si, "si_last": si, "off": off}
if cur: segs.append(cur)
segs = [g for g in segs if g["hi_last"] - g["hi_first"] >= 2]
out = []
for k, g in enumerate(segs):
    # cut span: from this run's first word (minus a little) to the next run's start
    c0 = H[g["hi_first"]]["s"] - 0.10 if k == 0 or True else 0
    c0 = max(0.0, c0 if k == 0 else (H[g["hi_first"]]["s"] + H[segs[k-1]["hi_last"]]["e"]) / 2)
    c1 = (H[g["hi_last"]]["e"] + H[segs[k+1]["hi_first"]]["s"]) / 2 if k+1 < len(segs) else nf / FPS
    f0 = int(round(c0 * FPS)); f1 = int(round(c1 * FPS))
    out.append({"from": f0, "len": max(1, f1 - f0), "srcS": round(c0 - g["off"], 3), "srcE": round(c1 - g["off"], 3)})
json.dump({"fps": FPS, "total": nf, "segments": out, "source": os.path.basename(SRC)}, open("work/lf01/work/segments.json","w"), indent=0)
cov = sum(s["len"] for s in out) / nf
print(f"segments: {len(out)}  coverage {100*cov:.1f}% of his cut  total {nf} frames")
un = [(H[i]["s"], H[i]["w"]) for i in range(len(H)) if i not in {p[0] for p in pairs}]
print(f"unmatched words in his cut: {len(un)}" + (" — first few: " + ", ".join(f"{t:.1f}s {w}" for t, w in un[:12]) if un else ""))
