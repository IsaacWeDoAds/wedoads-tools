#!/usr/bin/env python3
"""Build the house SFX library from Nishant's folder (5 Sep 2026).

  <media-drive>/sound effects new/  ->  public/sfx/lib/<category>/<slug>.wav  (48k stereo PCM16)
Every one-shot is peak-normalised to -1 dBFS; beds/loops are RMS-normalised to -20 dBFS; long
multi-hit files are ALSO sliced at onsets into <slug>_01.. so a single hit can be cued.
Per file we store the PEAK time (argmax |x|) so cues can be peak-aligned (sfx-peak-alignment).
Outputs: public/sfx/lib/catalog.json, src/LF01/sfxlib.ts (generated), docs/sfx-library.md
"""
import os, re, sys, json, subprocess, wave, shutil, unicodedata
import numpy as np
SRC = "<media-drive>/sound effects new"
ZIPX = "/private/tmp/claude-501/-Users-nishant-Video-Edits/b33cccbe-59cb-42cd-845e-f6510fc6a999/scratchpad/sfxzip"
OUT = "public/sfx/lib"
SR = 48000
AUDIO = (".mp3", ".wav", ".mp4", ".m4a", ".aif", ".aiff", ".flac", ".ogg")

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"\.(mp3|wav|mp4|m4a|aif|aiff|flac|ogg)$", "", s, flags=re.I)
    s = re.sub(r"^\d{6}_", "", s)                      # Epidemic catalogue number
    s = re.sub(r"- Epidemic Sound|- SFX Producer|\(youtube\)|\[FREE\]|Sound of Music|y2mate\.com -|@Sound Effect|_1080p(FHR)?|- Sound Effect \(HD\)|- Gaming Sound FX|- Free Sound FX|Sound Effects -", " ", s, flags=re.I)
    s = re.sub(r"^ES_", "", s)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    s = re.sub(r"-{2,}", "-", s)
    return s[:60]

# category rules (first match wins), applied to the lower-cased ORIGINAL name
RULES = [
  ("bed",     r"underscore|creepy_game|tension strings|anticipation|suspense piano|cinematic swell|space, weird|organic, wind|boosted mid|bass, resonant|deep voice whoosh|stopwatch|sprinkler|classroom|harmonica|hydraulic bell|mixer motor|siren"),
  ("riser",   r"riser|build up|rise into hit|reversed hit|reversed, dry|tape rewind|filter sweep|transition, fast|rise to hit|rise to 0|chopping"),
  ("impact",  r"bass drop|impact|slam|trailer hits|cinematic drum|short, deep|gritty|classic, |building block|vibrating low|drum"),
  ("glitch",  r"glitch|error|databend|feedback|noise, long|digital, computer|data load"),
  ("camera",  r"camera|shutter|flash|take photo|take picture"),
  ("whoosh",  r"whoosh|swoosh|swish|sword|fly by|axe|projectile|doppler|teleport|wind turbine"),
  ("paper",   r"paper|letter|envelope|tear|pencil|highlighter|magazine|books|wrapping|money, note|playing cards|scroll(?!\s*wheel)"),
  ("tech",    r"futuris|sci fi|scan|computer|ui data|text display|ticks, text|simple text|keyboard|typing|power up|device|hi-tech|select 21|data processing|mechanics, electronics"),
  ("ui",      r"ui|notification|alert|menu|pop|bell|ting|achievement|text message|marimba|boing|cartoon|smartphone|percusive"),
  ("click",   r"click|button|switch|mouse|trackpad|crank|mechanism|gizmo|gears|old, small"),
  ("foley",   r"coins|apple|chair|suitcase|run|sneakers|knife|chop|cutting|lemon|vacuum|flame|fire|water|rope|stretch|shot|taser|acid|slicing|spin|tiptoe|movement in hand|spacecraft|stress"),
  ("voice",   r"scream|pain|breathing|male|female"),
]
def category(name):
    n = name.lower()
    for cat, rx in RULES:
        if re.search(rx, n): return cat
    return "misc"
BED_LIKE = {"bed"}

def decode(path):
    """-> float32 stereo (n,2) at 48k"""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-f", "f32le", "-acodec", "pcm_f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    return x.reshape(-1, 2) if len(x) >= 2 else np.zeros((1, 2), np.float32)

def write(path, x):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    y = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((y * 32767).astype("<i2").tobytes())

def fade(x, fi=0.005, fo=0.02):
    n = len(x); a = int(fi * SR); b = int(fo * SR)
    if a and n > a: x[:a] *= np.linspace(0, 1, a)[:, None]
    if b and n > b: x[-b:] *= np.linspace(1, 0, b)[:, None]
    return x

def normalise(x, bed):
    m = np.abs(x).max() or 1.0
    if bed:
        rms = np.sqrt((x ** 2).mean()) or 1e-6
        g = 10 ** (-20 / 20) / rms
        return x * min(g, 0.99 / m)
    return x * (10 ** (-1 / 20) / m)

def measure(x):
    mono = np.abs(x).max(axis=1)
    peak_i = int(mono.argmax())
    thr = mono.max() * 0.5
    onset_i = int(np.argmax(mono >= thr))
    return round(peak_i / SR, 4), round(onset_i / SR, 4), round(len(x) / SR, 3)

def onsets(x, min_gap=0.45):
    """onset times (s) for a multi-hit file: 10 ms RMS envelope, rise > 14 dB over a 250 ms floor"""
    mono = x.mean(axis=1)
    hop = int(0.01 * SR)
    n = len(mono) // hop
    env = np.sqrt(np.maximum(1e-12, (mono[: n * hop].reshape(n, hop) ** 2).mean(axis=1)))
    db = 20 * np.log10(env + 1e-9)
    out, last = [], -10
    for i in range(3, n):
        floor = np.median(db[max(0, i - 25): i - 1])
        if db[i] > -32 and db[i] - floor > 14 and (i * 0.01 - last) > min_gap:
            out.append(i * 0.01); last = i * 0.01
    return out

def collect():
    files = []
    for root, _, names in os.walk(SRC):
        for nm in names:
            if nm.startswith("._") or not nm.lower().endswith(AUDIO): continue
            files.append(os.path.join(root, nm))
    for nm in os.listdir(ZIPX):
        if nm.lower().endswith(AUDIO): files.append(os.path.join(ZIPX, nm))
    return sorted(files)

def main():
    catalog = {}
    seen = set()
    for path in collect():
        name = os.path.basename(path)
        cat = category(name)
        sl = slug(name)
        while sl in seen: sl += "-b"
        seen.add(sl)
        x = decode(path)
        if len(x) < SR * 0.05: print("skip (empty):", name); continue
        bed = cat in BED_LIKE or len(x) / SR > 25
        y = fade(normalise(x.copy(), bed))
        rel = f"sfx/lib/{cat}/{sl}.wav"
        write("public/" + rel, y)
        peak, onset, dur = measure(y)
        catalog[sl] = {"src": rel, "cat": cat, "peak": peak, "onset": onset, "dur": dur, "bed": bed, "from": name}
        # slice multi-hit files (>2.5 s with >=3 onsets, one-shot categories only)
        if dur > 2.5 and cat in ("impact", "whoosh", "camera", "click", "ui", "riser", "glitch", "foley", "paper"):
            on = onsets(x)
            if len(on) >= 3:
                for k, t in enumerate(on[:12]):
                    a = max(0, int((t - 0.02) * SR))
                    b = int((on[k + 1] - 0.05) * SR) if k + 1 < len(on) else min(len(x), a + int(3.0 * SR))
                    b = min(b, a + int(3.0 * SR))
                    if b - a < SR * 0.12: continue
                    z = fade(normalise(x[a:b].copy(), False))
                    s2 = f"{sl}-{k+1:02d}"
                    rel2 = f"sfx/lib/{cat}/{s2}.wav"
                    write("public/" + rel2, z)
                    p2, o2, d2 = measure(z)
                    catalog[s2] = {"src": rel2, "cat": cat, "peak": p2, "onset": o2, "dur": d2, "bed": False, "from": f"{name} @ {t:.2f}s"}
        print(f"{cat:7s} {dur:7.2f}s peak@{peak:.3f} {sl}")
    json.dump(catalog, open(f"{OUT}/catalog.json", "w"), indent=1)
    # TS constants
    ts = ["// GENERATED by work/lf01/work/sfx_lib.py — the house SFX library (public/sfx/lib). Do not hand-edit.",
          "export type SfxEntry = { src: string; cat: string; peak: number; onset: number; dur: number; bed: boolean };",
          "export const SFX_LIB: Record<string, SfxEntry> = " + json.dumps({k: {kk: v[kk] for kk in ("src", "cat", "peak", "onset", "dur", "bed")} for k, v in catalog.items()}, indent=0) + ";"]
    open("src/LF01/sfxlib.ts", "w").write("\n".join(ts) + "\n")
    # index
    by = {}
    for k, v in catalog.items(): by.setdefault(v["cat"], []).append((k, v))
    md = ["# SFX library — `public/sfx/lib/`", "", f"Built {len(catalog)} files from `<media-drive>/sound effects new/` by `work/lf01/work/sfx_lib.py`.",
          "One-shots peak-normalised to −1 dBFS, beds RMS −20 dBFS, 48 kHz stereo PCM16. `peak` = seconds to the loudest sample",
          "(schedule a cue at `event − peak`), `onset` = first time the envelope reaches half the peak. Suffix `-NN` = a single hit sliced from a multi-hit file.", ""]
    for cat in sorted(by):
        md += [f"## {cat} ({len(by[cat])})", "", "| slug | dur | peak | from |", "|---|---|---|---|"]
        for k, v in sorted(by[cat]): md.append(f"| `{k}` | {v['dur']:.2f}s | {v['peak']:.3f} | {v['from']} |")
        md.append("")
    open("docs/sfx-library.md", "w").write("\n".join(md))
    print(f"\n{len(catalog)} entries -> {OUT}/catalog.json, src/LF01/sfxlib.ts, docs/sfx-library.md")
main()
