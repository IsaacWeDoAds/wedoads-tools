# Long-form from raw, built in HyperFrames (lf02, Oct 2026)

When there is no Palmier pre-cut, cut from the raw takes and build the whole video as a HyperFrames project.
lf02 ("How I edit all my videos with Claude", 16:22) shipped this way; this is what it settled.

## The cut (as data)
- `edl.py`: a list of `(id, clip, a, b, register, opts)` + `DROP` ranges + `HEAD_FIX`/`TAIL_FIX` keyed by piece
  id. Edges are decided by the `shortform-cutaway` v2 rules (envelope release tails, onset heads, island guard,
  no re-join across a drop, micro-fades). `b` = the last word's release, never a word start (15 words were cut
  in v1 by that one mistake).
- Long takes drift: verify every piece against isolated-window ASR (`isowords.py`), then sweep every edge
  (`edge_sweep.py`), probe each doubt (`probe.py`), and listen back around every join (`listen_back.py`).
- Screen recordings shot alongside the camera lock to it by audio cross-correlation (lag per file).

## Registers (16:9)
| | what | rules |
|---|---|---|
| F | face full frame | emphasis lockups (serif lead + heavy caps key word) in the lane he is NOT facing; static 1.00/1.12 on same-take jump cuts |
| S | screen | white grid paper; the recording in a rounded card at **full width** (x420–1880), only the Dock / Chrome bookmark bar cropped, no zoom, no push-in; his face in a **9:16 card** (352×626) on the side he faces, zoomed out to the camera's full height |
| D | paper drawer | face card is the drawer on the side he faces (lf02: LEFT, x0–648 = 9 grid squares); graphics authored in a 1240 lane and shifted by 648; slides out/in in 10 f |
| P | full page | one idea on paper; entries alternate slide-R / dissolve / slide-L / dissolve, hard cut out |
| B | b-roll | his own footage full frame; pick moments that show the edit's own type (a card on screen), not a plain shot |

Registers hard-cut. Graphics land on spoken words (a word resolver that prefers WhisperX times and falls back
to the isolated-window time when they disagree by > 1 s).

## Sound
- Every dialogue cut: `data-fade-in="0.015"` / `data-fade-out="0.025"` (not on source-contiguous joins, not
  on a section edge inside a piece).
- SFX by what moves, variants rotated, peak-aligned from a catalog, ≤ 1 transient per 0.22 s; he asked for
  the whole kit −4 dB after the first pass.
- A hook music bed when asked: catalog search by mood → a model listens and scores → ducked on the cut's
  speech envelope (−10 dB gaps / −17.5 dB under speech) → baked to `assets/music/hookbed.wav`.

## Build + render
- Generator (`build.py`) writes `index.html` + one sub-composition per scene window; every timed element is a
  record `{f0, n, ms, fmt}` so the same data writes the full root and any section root.
- Card frames are **timed plates behind** the video — never style an untimed wrapper.
- Export in ~90 s sections (boundaries where no host spans, or a host starting one frame early with a
  dropped preroll frame), cached by content hash; stitch with exact frame counts; audio as PCM per section,
  one limiter, one AAC encode; the −14 LUFS copy measured on the encoded file.
- The Studio preview can show a ready video unpainted on a 300-clip timeline; trust rendered stills.

## Review
Contact sheets of every scene (mid + settled state) + every 6th screen beat → a different model (Fable)
reviews → check each finding on full-res frames (it once sampled 0.08 s before a label landed) → fix the real
ones → re-render only the touched sections.
