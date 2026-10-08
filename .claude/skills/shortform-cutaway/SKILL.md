---
name: shortform-cutaway
description: "v2 (Oct 2026). The ROUGH-CUT editor for talking-head takes — 9:16 shorts first, and the same edge rules power long-form cuts. Turns a raw camera ramble (redo takes, pauses, restarts, talking to the AI) into a tight, flowing cut: WhisperX forced alignment finds the words → the model picks the red thread (one clean take per beat) → every EDGE is then decided on the audio envelope (release-based tails, onset-based heads, no cut back over a 'hm', micro-fades at every real cut) → an edge sweep + the cut-audit skill prove it before anything is styled. Use for 'remove the silences', 'make the rough cut', 'cut this', 'make it flow', 'punchy version', and whenever a cut sounds abrupt, clips a word, or keeps a fumble. Does NOT do captions/music/grade/reframe (= shortform-finish)."
---

# SHORTFORM CUTAWAY v2 — the rough-cut editor

> **THE JOB:** WhisperX tells you which words were said → the model arranges the clean takes into a red
> thread → the builder cuts on the **audio envelope**, not on the ASR's word times → every edge is swept and
> audited before styling. Output = a cut list (`cut.json`) + a matching MP4, which lands in any editor.

Stage 1 of the pipeline. Stage 2 (reframe, type, sound) is `shortform-finish`. Between them sits the
**`cut-audit`** skill — never skip it.

## What changed in v2 (and why — every line is a real miss)

| v1 rule | what shipped | v2 rule |
|---|---|---|
| tail = WhisperX end + 0.06 | "edited using [AI]", "absolutely [free]" lost their last syllable | tail = envelope **release** + 0.06, capped before the NEXT word's **envelope onset** − 0.03 |
| head = WhisperX start − 0.04 | onsets of "in", "canvas", "These" cut (WhisperX started 0.4 s late) | head = the envelope onset found by walking back from the word |
| head searches back for 120 ms of quiet | it walked over a separate "hm" and played it | never reach back over a separate voiced island (`islands()`) |
| beat END written by eye | 15 of ~200 ENDs were the START of the last word → that word dropped | END = the last word's release; the builder warns when an END sits on a word start or inside a word |
| gaps measured on word times | an under-run word end invented a "silence" inside "Free Gemini access" | split a beat only where the **envelope** is silent > GAP |
| contiguous pieces re-join | a dropped "not—" fragment came back | never re-join across a dropped word |
| hard cuts, raw | a click at cuts that land on voice | 15 ms fade-in / 25 ms fade-out on every real cut (skip source-contiguous joins) |
| trust WhisperX everywhere | on a 23-min take it drifted 15 s; the cut played the wrong audio | on long takes, verify every piece with isolated-window ASR (`isowords.py`) |

---

## ⭐ FIRST RUN — which editor do you use?

Ask once. The cut math is identical; only the landing differs.

- **(a) DaVinci Resolve** — `build_wx.py` (v1) still emits Resolve `clip_infos`; for v2 edges, convert
  `cut.json` pieces (`a`, `dur` seconds) to frames at your source FPS.
- **(b) Premiere Pro** — write `cut.json` pieces as a CMX3600 EDL / FCP7 XML (one event per piece).
- **(c) Remotion** — each piece → a `<Sequence>` of an `<OffthreadVideo>` trimmed with `startFrom`/`endAt`;
  apply the fades with `interpolate` on volume.
- **(d) HyperFrames** — each piece → a `<video class="clip">` with `data-start` (timeline), `data-media-start`
  (= `a`), `data-duration`, `data-has-audio="true"`, and `data-fade-in="0.015"` / `data-fade-out="0.025"`
  where the piece says `fade_in`/`fade_out`. Hard cuts between registers are just consecutive clips.
- **(e) Claude-Code-only (ffmpeg)** — render each piece with `-ss a -t dur`, `afade` in/out where flagged,
  reframe in the same pass (`crop=ih*9/16:ih,scale=1080:1920,fps=30`), concat with a re-encode (CFR!).
  Drive the loop from Python, not a bash `while read`.

> Default to **(e)** if they don't know.

---

## SETUP (once)

WhisperX needs **Python ≤ 3.12** + torch:
```bash
python3.11 -m venv ~/wx-env && ~/wx-env/bin/pip install whisperx
export HF_HOME=~/wx-cache        # model cache (a faster-whisper model + a ~360 MB alignment model)
```
The v2 scripts need only `numpy` (and `OPENAI_API_KEY` for `probe.py` / `isowords.py` / `listen_back.py`).

## WHY WhisperX — and why it is still not enough
A "silence" is a stretch where **no word is said**, not a waveform dip, so the cut is driven by words.
faster-whisper only guesses word times; WhisperX force-aligns them with a phoneme model — good enough to
know **which** words are where. But its **ends** run early on decays and its **starts** can run late, and on
long takes it can drift by seconds. So v2 uses WhisperX for *what was said*, and the **envelope** for *where
to cut*.

---

## THE METHOD

```bash
WORK=~/cut && mkdir -p "$WORK"; SRC=/path/to/CLIP.MP4
# 1. audio: mono WAV for the envelope tools, mp3 for WhisperX
ffmpeg -y -i "$SRC" -vn -ac 1 -ar 16000 "$WORK/a.wav"
# 2. words
HF_HOME=~/wx-cache OMP_NUM_THREADS=4 ~/wx-env/bin/python scripts/whisperx_align.py "$WORK/a.wav" "$WORK/wx.json"
#    long take (> ~5 min) or a multi-take ramble? also: python3 scripts/isowords.py "$WORK/a.wav" "$WORK/iso.json"
# 3. EDITOR step (the model): read the words, write beats.txt — the RED THREAD (below)
# 4. build on the envelope
python3 scripts/build_wx2.py "$WORK/a.wav" "$WORK/wx.json" beats.txt 0.30 30 > "$WORK/cut.json"
#    read every WARN line it prints; fix beats.txt and rebuild until none are left
# 5. sweep every edge
python3 scripts/edge_sweep.py "$WORK/cut.json" "$WORK/wx.json" [--iso "$WORK/iso.json"]
# 6. settle each doubtful flag in one call (unpadded 1.5–3 s windows, two engines):
python3 scripts/probe.py "$WORK/a.wav" 10.1 12.9 57.6 58.5
# 7. listen to the assembled cut around every join
python3 scripts/listen_back.py "$WORK/cut.json"
# 8. run the cut-audit skill's gates (stretched words, repeat_scan, per-burst probes), then land it (FIRST RUN)
```
`python3 scripts/envtools.py a.wav 57.9` prints an ASCII envelope around any cut — the fastest way to see
whether a word is whole (`#` loud, `+` voiced, `.` near threshold, space = quiet, `|` = the cut).

### Step 3 — THE RED THREAD (only the model can do this)
Write `beats.txt`, one beat per line `START END label`, so the story moves: **hook → what it is → how → result
→ value → CTA → (fun button).**
- **One clean take per beat.** People redo lines until right → the **later take usually wins** — but a
  later take can be a *prefix* of a restart ("or a Cl— or a Claude Pro"): probe before you trust it.
- **END = where the last kept word RELEASES**, not where the next word starts. Copying the next word's start
  (or the last word's start) is how 15 last words got cut in one edit. `build_wx2` warns; obey the warning.
- **Drop:** false starts, restarts, doubles, pointing shots, pure meta ("is this recording?"), ums, the "hm"
  before a line. **Keep** the real content and the speaker's own opinions.
- **A sentence's internal pause is not a silence to cut.** Cutting a 0.2 s emphasis pause reads as a jarring
  jump; tighten only a genuinely halting delivery, and only where the face is small or hidden.
- **Honour to-camera direction** ("you can cut here" is often the fun ending).
- **Fix the order** so it reads as one thought (the cleanest hook first even if recorded last).
- **GAP** (envelope silence that splits a beat): 0.30 punchy short-form · 0.45 long-form. Real inter-beat
  gaps in a natural delivery are ≥ 0.6 s; anything flagged in the 0.3–0.5 band deserves a listen.

### Long takes (> 5 min, or several takes in one file)
- Run `isowords.py` and `edge_sweep.py --iso`. When WhisperX and the isolated words disagree by > 1 s on a
  word, trust the isolated time for **where** and the envelope for **the edge**.
- Keep the cut **as data** (a Python list of `(id, source, a, b, register, opts)` plus `DROP` ranges and
  `HEAD_FIX`/`TAIL_FIX` keyed by piece id) so every decision is reviewable and every rebuild reproduces it.
- Screen recordings shot alongside the camera lock to it by cross-correlating their audio envelopes
  (corr ≈ 0.9 is a lock); store the lag per file.

---

## ⛔ DEAD ENDS (do not repeat)
1. **Whisper segments as the silence cutter** — they smooth over think-pauses.
2. **Tight amplitude margins / fixed-dB silencedetect** — clip "This", "ASAP"; fail when mic distance varies.
3. **faster-whisper word times for edges** — mistimed around pauses.
4. **WhisperX word times for edges** (v1) — ends early, starts late; see the v2 table.
5. **Trusting a clean transcript** — ASR de-duplicates an immediate repeat; five transcripts once called a
   doubled line clean. The envelope + `repeat_scan` + per-burst probes catch it (`cut-audit`).
6. **Padded short probes** — silence-padding makes Whisper loop and "hear" repeats that are not there.
7. **Re-joining neighbours blindly** — a dropped fragment comes back.

> **Not the cause (don't chase):** the NLE, the FPS, or "use Gemini to find the silences".

Scripts: **`build_wx2.py`** (the builder) · `envtools.py` · `edge_sweep.py` · `probe.py` · `isowords.py` ·
`listen_back.py` · `whisperx_align.py`. Kept for reference: `build_wx.py` (v1), `build_cut.py`,
`build_wordcut.py`, `build_clipinfos.py`, `flow_cut.py`; aids: `motion_score.py`, `storyboard.sh`.

## SCOPE
**DOES:** take selection · word alignment · envelope-exact edges · micro-fades · edge sweep · probes ·
listen-back · a cut list for any editor + an MP4.
**DOES NOT (→ `shortform-finish`):** captions · type · music · SFX · grade · reframe / punch-ins.
