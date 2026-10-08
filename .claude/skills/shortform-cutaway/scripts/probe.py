#!/usr/bin/env python3
"""probe.py — verbatim micro-probes: transcribe short UNPADDED windows with two engines and a disfluency prompt.
Use it to CHOOSE between two hypotheses the envelope has already bracketed ("is 10.2-11.8 a restart?",
"does the piece end inside 'free'?"). Not for discovery: short windows hallucinate, and silence-PADDED short
windows hallucinate repeats ("You're in. You're in."), so never pad, and keep windows 1.5-3 s.

Usage: probe.py AUDIO.wav T0 T1 [T0 T1 ...]      (needs OPENAI_API_KEY in the environment or a .env/.env.local)
Prints, per window: whisper-1 | gpt-4o-transcribe.
"""
import io, json, os, sys, urllib.request, uuid, wave
from pathlib import Path
import numpy as np


def key():
    if os.environ.get("OPENAI_API_KEY"): return os.environ["OPENAI_API_KEY"]
    for f in (".env.local", ".env"):
        if Path(f).exists():
            for l in open(f):
                if l.startswith("OPENAI_API_KEY="): return l.split("=", 1)[1].strip().strip('"')
    sys.exit("set OPENAI_API_KEY")


PROMPT = "Umm, so, I- I'll, the the, uh, verbatim with repeats and false starts."


def tx(seg, sr, model, k):
    seg = np.clip(seg.astype(np.float32) * 2.0, -32768, 32767).astype(np.int16)
    buf = io.BytesIO(); ww = wave.open(buf, "wb"); ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(sr); ww.writeframes(seg.tobytes()); ww.close()
    b = uuid.uuid4().hex
    f = lambda n, v: f"--{b}\r\nContent-Disposition: form-data; name=\"{n}\"\r\n\r\n{v}\r\n"
    body = (f("model", model) + f("language", "en") + f("prompt", PROMPT)
            + f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\nContent-Type: audio/wav\r\n\r\n").encode() + buf.getvalue() + f"\r\n--{b}--\r\n".encode()
    r = urllib.request.Request("https://api.openai.com/v1/audio/transcriptions", data=body,
                               headers={"Authorization": f"Bearer {k}", "Content-Type": f"multipart/form-data; boundary={b}"})
    return json.loads(urllib.request.urlopen(r, timeout=120).read())["text"]


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) % 2: sys.exit(__doc__)
    w = wave.open(sys.argv[1]); sr = w.getframerate(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    if ch > 1: x = x.reshape(-1, ch).mean(1).astype(np.int16)
    k = key(); a = sys.argv[2:]
    for i in range(0, len(a), 2):
        t0, t1 = float(a[i]), float(a[i + 1]); seg = x[int(t0 * sr):int(t1 * sr)]
        print(f"{t0:.2f}-{t1:.2f} | w1: {tx(seg, sr, 'whisper-1', k)} | 4o: {tx(seg, sr, 'gpt-4o-transcribe', k)}", flush=True)
