#!/usr/bin/env python3
"""isowords.py — isolated-window word timestamps for a whole take (v2, Oct 2026). Ground truth for WHICH words
are WHERE on long takes. On a 23-min take WhisperX drifted 15 s at one point (the cut played the wrong audio) and
4 s at another (three false starts collapsed). A fresh decoder every 5 s cannot carry drift across a pause.

whisper-1 verbose_json words on 5 s windows every 3 s; a word is kept from the window where it starts in the
first 3 s. ~1.7x the audio minutes in API time (cents per hour of footage), run in parallel.
Use the result to (1) check each piece's words (edge_sweep.py --iso), (2) anchor graphics: when WhisperX and
these times disagree by > 1 s on a word, trust these for WHERE, and the envelope for the exact edge.

Usage: isowords.py AUDIO.wav OUT_iso.json [T0 T1]      (needs OPENAI_API_KEY)
"""
import concurrent.futures as cf, io, json, sys, urllib.request, uuid, wave
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from probe import key

w = wave.open(sys.argv[1]); sr = w.getframerate(); ch = w.getnchannels()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
if ch > 1: x = x.reshape(-1, ch).mean(1).astype(np.int16)
T0 = float(sys.argv[3]) if len(sys.argv) > 4 else 0.0
T1 = float(sys.argv[4]) if len(sys.argv) > 4 else len(x) / sr
K = key()


def words(t):
    seg = np.clip(x[int(t * sr):int((t + 5) * sr)].astype(np.float32) * 2.0, -32768, 32767).astype(np.int16)
    buf = io.BytesIO(); ww = wave.open(buf, "wb"); ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(sr); ww.writeframes(seg.tobytes()); ww.close()
    b = uuid.uuid4().hex
    f = lambda n, v: f"--{b}\r\nContent-Disposition: form-data; name=\"{n}\"\r\n\r\n{v}\r\n"
    body = (f("model", "whisper-1") + f("language", "en") + f("response_format", "verbose_json") + f("timestamp_granularities[]", "word")
            + f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\nContent-Type: audio/wav\r\n\r\n").encode() + buf.getvalue() + f"\r\n--{b}--\r\n".encode()
    r = urllib.request.Request("https://api.openai.com/v1/audio/transcriptions", data=body,
                               headers={"Authorization": f"Bearer {K}", "Content-Type": f"multipart/form-data; boundary={b}"})
    for attempt in range(3):
        try:
            out = json.loads(urllib.request.urlopen(r, timeout=120).read()).get("words", [])
            return [{"s": round(t + v["start"], 2), "e": round(t + v["end"], 2), "w": v["word"]} for v in out
                    if v["start"] < 3.0 or t + 5 >= T1]
        except Exception as e:
            err = e
    print(f"window {t:.1f} failed: {err}", file=sys.stderr); return []


starts = [round(T0 + 3 * i, 2) for i in range(int((T1 - T0) // 3) + 1)]
with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(words, starts))
W = sorted((w for r in res for w in r), key=lambda w: w["s"])
json.dump(W, open(sys.argv[2], "w"), ensure_ascii=False)
print(f"{len(W)} isolated-window words over {T1 - T0:.0f}s ({len(starts)} windows)", file=sys.stderr)
