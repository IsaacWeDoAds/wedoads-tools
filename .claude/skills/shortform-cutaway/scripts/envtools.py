# Envelope tools: a 10 ms RMS envelope (dB) of a mono WAV, and the edge finders the cut rules use.
# Every edge decision in v2 is made on the ENVELOPE, never on an ASR word end (ASR ends run early on decays,
# WhisperX starts can run ~0.4 s late, and either can drift on long takes).
#   from envtools import env, thr, speech_end, onset_before, release_after, islands, quiet
#   (all take the WAV path first; extract with: ffmpeg -i SRC -vn -ac 1 -ar 16000 audio.wav)
import wave
from functools import lru_cache
import numpy as np


@lru_cache(None)
def env(path):
    """10 ms RMS envelope in dB (index k = time k/100 s)"""
    w = wave.open(str(path))
    sr, ch = w.getframerate(), w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if ch > 1: x = x.reshape(-1, ch).mean(1)
    hop = sr // 100; n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)


@lru_cache(None)
def floor(path):
    e = env(path); return float(np.percentile(e, 8)), float(np.percentile(e, 80))


def thr(path):
    """speech threshold: 45 % of the way from the room-tone floor to typical speech"""
    f, s = floor(path); return f + 0.45 * (s - f)


def speech_end(path, t, look=0.6):
    """first time after t where energy stays under threshold for 120 ms (a word's release)"""
    e = env(path); th = thr(path); i = int(t * 100); j = min(len(e), int((t + look) * 100))
    for k in range(i, j):
        if (e[k:k + 12] < th).all(): return k / 100
    return j / 100


def speech_start(path, t, look=0.4):
    """last time before t where energy was under threshold for 120 ms (a conservative onset)"""
    e = env(path); th = thr(path); i = int(t * 100); j = max(0, int((t - look) * 100))
    for k in range(i, j, -1):
        if (e[k - 12:k] < th).all(): return k / 100
    return j / 100


def onset_before(path, t, look=0.5, q=3):
    """walk back from t (a word start) through voiced frames; the onset is where >= q*10 ms sit below thr-6 dB.
    Use it to (a) find a word whose WhisperX start is late and (b) cap a tail before the NEXT word's real onset."""
    e = env(path); th = thr(path) - 6; i = int(t * 100); j = max(0, int((t - look) * 100)); run = 0
    for k in range(i, j, -1):
        run = run + 1 if e[k] < th else 0
        if run >= q: return (k + q) / 100
    return j / 100


def release_after(path, t, look=0.5, q=3):
    """walk forward from t (a word end) through its decay; the release is where >= q*10 ms sit below thr-6 dB"""
    e = env(path); th = thr(path) - 6; i = int(t * 100); j = min(len(e), int((t + look) * 100)); run = 0
    for k in range(i, j):
        run = run + 1 if e[k] < th else 0
        if run >= q: return (k - q + 1) / 100
    return j / 100


def islands(path, a, b, gap=0.07):
    """voiced islands in [a, b] separated by >= gap of quiet -> [(s, e)]. A short island right before a kept
    word is usually a 'hm' or a false-start syllable: never let a head reach back over one."""
    e = env(path); th = thr(path) - 6; out = []; cur = None; quiet_n = 0; g = int(gap * 100)
    for k in range(int(a * 100), int(b * 100)):
        if e[k] >= th:
            if cur is None: cur = [k, k]
            cur[1] = k; quiet_n = 0
        else:
            quiet_n += 1
            if cur is not None and quiet_n >= g: out.append((cur[0] / 100, (cur[1] + 1) / 100)); cur = None
    if cur is not None: out.append((cur[0] / 100, (cur[1] + 1) / 100))
    return out


def quiet(path, t, win=0.06):
    """the quietest 10 ms within +-win of t -> (time, dB). Snap a cut that lands on voice to the valley."""
    e = env(path); i0, i1 = max(0, int((t - win) * 100)), int((t + win) * 100) + 1
    k = i0 + int(np.argmin(e[i0:i1])); return k / 100 + 0.005, float(e[k])


def ascii_env(path, cut, lo=None, hi=None):
    """one char per 20 ms: '#' > thr+12, '+' > thr+4, '.' > thr, ' ' quiet; '|' marks the cut"""
    e = env(path); th = thr(path); lo = cut - 0.8 if lo is None else lo; hi = cut + 0.8 if hi is None else hi
    s = ""
    for k in range(int(lo * 100), int(hi * 100), 2):
        if abs(k / 100 - cut) < 0.01: s += "|"; continue
        v = max(e[k], e[k + 1]); s += "#" if v > th + 12 else ("+" if v > th + 4 else ("." if v > th else " "))
    return f"{lo:8.2f} {s} {hi:.2f}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3: sys.exit("usage: envtools.py AUDIO.wav CUT_SECONDS [LO HI]   -> ASCII envelope around a cut")
    a = sys.argv; print(ascii_env(a[1], float(a[2]), *(float(x) for x in a[3:5])))
