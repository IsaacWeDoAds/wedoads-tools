# Building and shipping a vlog in HyperFrames

The reference build is `hyperframes/vlog3-edit/` (79 clips, 14:31, 60 fps). The toolkit is in
`work/vlog3/`: copy it and change the paths. Project setup traps (APFS + SSD symlinks, Studio owning
`index.html`, `check` hanging) are in hyperframes project setup.

## Toolkit (`work/vlog3/`)

| Script | Job |
|---|---|
| `hf_build.py` | first timeline from the Palmier cut: per-clip gains, punch geometry (do not re-run once Studio owns `index.html`) |
| `hf_transcribe.py` | per-clip WhisperX, timeline-time words + `cut.wav` (the dialogue mix as rendered) |
| `tl_frames.py` | grab any timeline time (applies the punch crop) with a 10% grid, for placing text |
| `hf_overlays.py` | every graphic as a sub-composition, from data |
| `place_text.py` | measured text placement → `text_offsets.json` |
| `hf_mount.py` | mounts graphics, SFX (peak-aligned, library) and music between markers in `index.html` |
| `hf_seams.py` | exact same-take continuity + one level per take |
| `hf_ripple.py` | cuts / extends / inserts on the original clock (`R(t)`) |
| `hf_grade.py` | bakes the grade into every source (`--revert` to undo) |
| `sfx_levels.py` | mixes the SFX stem against `cut.wav` and reports peaks next to the voice |
| `hf_testcut.py` | cuts timeline windows into a temporary `_test.html` for a short real render |
| `hf_export.py` | sectioned final export + stitch |

Regenerate with `hf_overlays.py && hf_mount.py`; the mount only replaces its own block, so his Studio
edits elsewhere in `index.html` survive.

## Colour grade: bake it, never per clip

`media-treatment` grades one `<video>` at a time with a live shader, and the shader starts a frame
late on every clip. In the render, the first frame after EVERY cut was ungraded (3–5 levels cooler;
one same-shot cut flashed). He saw *"a little blip between clips, like some transition effect."*

1. Approve the look on a few clips with the shader (warm-daylight 0.55 + vignette 0.12 + grain 0.10).
2. Snapshot the same timestamps graded and ungraded; fit a 33³ `.cube` from the pixel pairs
   (`grade/fit_look.py`, median error 0.4 levels). The cube holds **colour only**: it is fitted on
   centre pixels, so vignette and grain stay out of it and are added by ffmpeg. Night clips (shot
   after sunset, listed in `NIGHT` in `hf_grade.py`) get a weaker cube, 0.3/0.55 of the look.
3. Re-encode every used source **whole, `-copyts`**, with `lut3d` (tetrahedral, in 16-bit RGB) +
   `vignette=angle=PI/14` + `noise=c0s=4:c0f=t+u` (temporal luma grain). Encode with
   `h264_videotoolbox` High at 40 Mb/s, `-g 30`, BT.709 tags, audio copied. At 40 Mb/s the
   generation loss is invisible. Vlog 3's 34 sources came to 8.7 GB on the SSD. Verify frame
   counts, start times and channels match on every file, then repoint the clips
   (`assets/footage_graded/`).
4. ffmpeg's vignette dims the centre ~2%. `hf_grade.py` does not correct it yet; fold 1/0.982 into
   the LUT next time.
5. Grade the freeze stills with the same cube (keep the cutout's exact alpha).

## Render traps

- **Mono clip audio renders +3.0 dB hot** (stereo lands exact). Trim mono sources by −3 dB
  (`data-volume × 0.708`); verify with a test render against `cut.wav` (within 0.1 dB).
- Conformed iPhone files with 4 s GOPs freeze on seek: re-encode with `-g 30`.
- Many sub-compositions share one page: scope CSS and ids by composition, pass GSAP element refs.
- Overlapping `<audio>` on one track trips lint (`duplicate_audio_track`): lane them, with a 1 ms gap.
- There is no time-range render: `hf_testcut.py` cuts windows into a temporary root composition.

## Export: in sections

A one-shot export (Studio "Export" or `render`) of 82 clips + 171 audio tracks pre-extracts every
clip at once: memory went red, 70/82 ffmpeg extractions timed out, and the Mac crashed twice.

`python3 work/vlog3/hf_export.py [--workers 2] [--quality delivery] [--only N]`:
- ~100 s sections (at least 95 s, and the last one at least 40 s), with each boundary on a clip start,
  frame-exact, where no graphic spans the boundary. `--only N` re-renders one section.
- `--workers 2–3`, using ~2.5–3 GB and staying above 50% free
- about 50 min for 14:31
- video joined losslessly
- audio decoded per section to exact-length PCM, joined, and encoded once (no AAC gaps)

Traps:
- **A section can render one extra frame** (black, past its last clip). That puts a black flash at
  the join and shifts the picture one frame late from there on. Concat with a per-file `outpoint` of
  **exactly N/60**. Vlog 2's `N/60 − 0.5/60` left each section half a frame short: the stream went VFR
  and the picture led the audio by 42 ms by the end. Assert `total frames = round(duration × 60)` AND
  `avg_frame_rate = 60/1`.
- **HyperFrames peak-normalises the render's audio** when the mix reaches about −1 dBFS: the whole section comes
  out ~0.8 dB down, which is a level step at the join. Keep the timeline mix ≤ −3 dBFS sample peak, and limit to
  −1 dBTP only after the stitch.
- **Section re-basing must floor clip starts, in frames.** Rounding to the nearest 1e-4 s started clips a frame late
  on one section (`work/vlog2/hf_testcut.py` has the fix; the Vlog 3 copy still rounds).
- **A clip whose `data-media-start` sits exactly on a source-frame boundary** (59.94 fps on a 60 fps
  timeline) can show its first frame twice. Nudge those starts +0.25 frame (`work/vlog2/edl.py`, step 3b).
- After a reboot nvm's default Node is 20 and HyperFrames needs ≥22: put `<your Node 22+ bin>` first.
- Don't run Studio Export alongside a render. Two renders at once is what runs memory out. Other sessions
  render on this Mac too: `work/vlog2/hf_export.py` waits for ≥20% free memory before each section.
- **Section joins must avoid graphics hosts, not just clips and audio.** `hf_testcut` drops a graphic that
  starts before its window, so a note that crosses a join vanishes in the next section. Count
  `<div data-composition-src>` when picking joins.
- **Studio's live preview can show a blank picture with the audio running** on a heavy timeline (Vlog 2: 86
  clips, 63 graphics, 75 SFX). It is not in the render. Answer "it looks blank at 0:39" with a short real
  render of that window.

## Ship

Two files go to `<media-drive>/VideoEdits-out/<vlog>/`:
- **Master:** the render as it comes out, H.264 High, yuv420p, BT.709, ~22 Mb/s from `--quality
  delivery`, AAC 320k, `+faststart`. Its loudness is whatever the mix gives (Vlog 3: −19.9 LUFS,
  −1.0 dBTP); nothing is normalised.
- **YouTube copy (the upload):** video stream-copied from the master, audio at −14 LUFS, AAC 320k,
  measured on the encoded file. Two-pass loudnorm falls into "dynamic mode" when a plain gain change
  would push peaks past −1.5 dBTP, and then it pumps the speech (Vlog 3: −14.4). Do this instead
  (Vlog 2, `work/vlog2/hf_export.py`): a 4×-oversampled `alimiter` at (−2 dB − gain) shaves the few
  transients, then ONE linear gain, re-measured and corrected once (Vlog 2: −14.1 LUFS, −1.8 dBTP).

Before handing over, check the final file:
- frame count
- every section join: frame diffs, plus the max audio sample step for clicks
- a **per-frame** black scan: `ffmpeg -i F -vf scale=192:108,blackframe=amount=98:threshold=24 -f null -`.
  `blackdetect` only reports runs ≥2 s, and Vlog 3's master shipped with 7 single black frames, each the
  FIRST frame of a clip (m41–m46, m62, m69) that the renderer drew before the decode landed. The end
  card's first second is black by design
- a frame sheet of every graphic pulled from the final file
- frozen frames: test for EXACT repeats at 480p (mean diff < 0.15). A 64x36 threshold flags every
  locked-tripod shot because the grain averages out. Expect one single repeat per ~1001 frames (59.94 → 60).
