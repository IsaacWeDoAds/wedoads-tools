---
name: omni-restyle
description: "Restyle the creator's OWN footage with Omni Flash video-to-video — the named treatment vocabulary (Vox, documentary, paper-cutout, blueprint…), the identity-drift law (prompt the environment, never the person), the behind-the-head giant-type recipe, the slice-reveal format, and the measured output specs that cap how big a restyled clip may be placed. Use for restyle hooks, world-flip openers, behind-the-head typography, and any 'make this look like X' pass on real footage. NOT for generating footage from nothing — that is genvideo."
---

# OMNI RESTYLE — transform the world, never the person

> **THE LAW, measured both ways:**
>
> - **Changing the WORLD around him holds his face.** Background swaps and "add paper-cutout motion
>   graphics around him" both came back as him — wardrobe, lighting and gestures intact. On a "real"
>   register the output is effectively a **passthrough**: source and output frames match on face,
>   framing and hand position.
> - **Changing HIM drifts.** *"Change the t-shirt and relight warm"* returned a slimmer, smoother,
>   younger face with different hair — recognisably a *version* of him. Chaining a second edit onto
>   it **compounds** the drift.
>
> **So: prompt the environment, never the person.** Guard the face rule explicitly in the prompt
> (*"do not cover his face"*) and still check every frame.

This does not loosen the fabrication ban — **restyles of his own footage only**.

## Run it free in the app first

The Gemini app does the same edit **at no cost** and has returned a *better* result than the API
(duration near-exact, identity held). Use the API only when a run must be scripted or chained.
Cost-gate still applies to API calls: **~$0.10/s of output**.

Runner: `.claude/skills/genvideo/scripts/gen_omni_v2v.py PROMPT IN.mp4 OUT.mp4 [PREV_ID]`.
Mechanism: upload via Files API → poll to ACTIVE → `interactions.create` with
`{"type":"document","uri":file.uri}` + text. `previous_interaction_id` chains a refinement turn
(verified working). Needs **google-genai ≥ 2.0** — the system Python has drifted back to 1.60 before.

**Two concurrent `interactions.create` calls both died** with `APIConnectionError: Server
disconnected` — run sequentially, or with a small pool and back-off (3 parallel workers, ~90s per
clip, worked for a 24-clip batch in ~15 min).

## Measured output — and what it means for placement

Input 1080×1920 / 30fps → output is **always 720×1280, 24fps, AAC stereo 48k**. This is the
**model's** ceiling, not the API's: `response_format` accepts only `type` and `aspect_ratio`
(9:16 / 16:9), there is no resolution option, and pricing is quoted per second of 720p.

**A 1080-wide card would upscale it**, which the never-upscale rule forbids — so **restyled footage
caps at a 720px-wide card** (the reference reel's big card sits near 62% of frame width for exactly
this reason). Full-bleed hooks need that rule **bent deliberately, his call**.

Other measured behaviour:
- **10s input works.** App: 10.008s in → 10.005s out. The **API drifted +2.3%** on three of four 5s
  runs and −1% on the fourth — **retime with `setpts`** before any side-by-side with the original.
- **Audio is his real voice and the same words**, but re-encoded. RMS-envelope correlation vs
  source: light edits stay locked (+0.72 @ 10ms); heavy edits drift (+0.52 @ 210ms). On a 10s run
  sync was **410ms out across the first half and 0ms across the second** — **the transitions are
  where it slips**, so check the tail and the beat after each register change.
- **Pacing instructions get under-delivered.** Asked for a register change every 1.2s, it gave
  ~3.3s. Name **explicit timestamps** ("at 0.8s… at 4s…") instead of an interval — and still expect
  to be ignored.
- **Transitions come back as hard sweeps across frame, never crossfades** — which already satisfies
  the registers-hard-cut rule.

## The treatment vocabulary

He asked for a **named** visual vocabulary — "Vox style, documentary style etc." The
catalogue with paste-ready prompts is **`docs/omni-restyle-treatments.md`**:

| treatment | what it is | status |
|---|---|---|
| **Vox explainer** | newspaper wall, red marker circles, highlighter | |
| **Documentary evidence board** | corkboard, pinned photos, red string, 16mm grain | |
| **Paper-cutout craft** | | ✅ verified |
| **Blueprint schematic** | | ✅ verified |
| **Whiteboard marker** | closest to the notebook-and-marker language | |
| **Data room** | abstract glowing glass panels | ⚠ see below |
| **Cinematic relight** | | ⚠ see below |
| **Miniature diorama** | | |

**Every prompt opens with the same identity guard — keep it verbatim when writing new ones.** It is
the whole reason his face survives.

Two cautions:
- **Data room** panels must stay **abstract shapes**. Readable UI on them is a mocked screen
  recording, which is banned.
- **Cinematic relight** is the only treatment that touches light **on him** — the exact drift
  trigger. Test before trusting it.

## The hook rule: ONE flip, not a cycle

A register **cycle** is a *show-the-range* device — the reference reel needed it because that reel
was an ad for the tool. **A hook doesn't need to prove range; it needs one thumb-stopping moment,
and the transformation itself IS the event.** Open on the real room, flip once around **0.8s**, hold
the new world. This also dodges the model's habit of under-delivering pacing.

**The flip buys exactly ONE event** — the rest of the 0–5s density still comes from Remotion
(`split-screen`).

## Behind-the-head giant type

> *"we don't need text behind the head [via masks]… I have seen people generating motion graphics
> using Gemini Omni. Let's try a 5s sample."*

The sample nailed it first try: a huge white heavy grotesk word BEHIND him, his face hiding a letter,
hands occluding letters at 2.0s, a script lead-in upper-right, face/lighting/framing untouched. He
then approved every beat this way (**~$20 for 24 cues**).

**Recipe:** 5s source from the cut starting **1.2s before the cue word** → prompt =

1. *"keep the person… exactly as they are, do not cover his face"*
2. ONE typographic moment: the word, *"very large, heavy, white geometric sans-serif (Helvetica Black
   / Inter Black style)"*, a size phrase per weight (xl *"nearly the full frame width"* / l
   *"two-thirds"* / m *"half"*), *"placed BEHIND him so that his head, shoulders and hands occlude
   the letters"*
3. the lead-in *"in a white connected brush-script handwriting… upper right of his head, never
   touching his face"*
4. timing: *"pops in when he says X (about 1.2 seconds in), holds ~2.5s, gone by 4s"*
5. *"its layout, size, line breaks and position stay fixed once it has appeared (no re-typesetting,
   no second copy, no drifting duplicate)"*
6. a closing negative block: no captions / logos / other text / filters / crop / camera move

Integration rules:
- **Its audio is re-synthesised, not the source** (waveform corr ≈ 0.0). **Never use it** — the
  timeline keeps `cut.wav`.
- **The type pops ~0.2s EARLY.** Cut the clip in **only while the type is visible** (≈0.95s→3.8s of
  the clip = cue −7f … +78f) so **the pop itself hides the switch** from the 1080p face.
- Output is 1280×720 @ 24fps. He chose to **upscale** (Lanczos + unsharp → 1080p30) rather than card
  it — the never-upscale rule **bent deliberately, his call**, for ~2.8s windows.
- **Cues over a cutaway have no head to sit behind** → keep the lane lockup instead.
- Tail ghosts after ~4s are harmless (outside the cut-in window).

**QA every clip** with a 2fps sheet: the word spelled right (**Omni leaks gibberish**), the pop time,
and any identity drift; run a motion-envelope check vs source if the timing looks off.

**Production reality: 4 of 24 needed re-rolls (17%)** — a duplicated word sliding through
("basigs.", "day day."), a garbled doubled lead-in, a misspelling ("dolollar."), and one
re-typesetting mid-hold. Adding the fixed-layout clause **cut but did not eliminate** the leaks; one
cue took three rolls. **Budget for it.**

## The slice-reveal format

The "slice of another dimension" effect: the SAME take three times (real + two restyles), with a
**quad slice clipped out of the world layers**, its ends pinned to his real index fingertips.
Because all layers share the take, **the body continues across the seam — that continuity IS the
effect.** MediaPipe hand landmarks drive the quad automatically (the manual pen-mask route is 1–2
hours per reel).

- Track with the MediaPipe **tasks** API (`HandLandmarker` + `FaceDetector`, VIDEO mode) on the
  **conformed CFR** file. **Relabel hands by screen x** (handedness labels flip) and **pick faces by
  temporal nearest** — max-area selection grabs bogus wall boxes and cost a whole pass.
- Conform restyle layers with `setpts=PTS*(src_dur/gen_dur),fps=30`. The 24→30 dupes show up in a
  tblend QA scan as ~4 near-zero-diff frames inside full-frame world beats — **benign, don't chase
  them**.
- **THE FINAL LESSON, after five alignment iterations: each world layer gets ONE CONSTANT similarity
  transform for the whole reel** — scale = median of the tracked fit over its slice window,
  translation from eye-midpoint medians. **ANY per-frame transform or warp** (smoothed similarity,
  affine, homography, MLS bake — all tried, all rejected) makes the world inside the slice breathe
  and swim ("morphing", in his words), because the map keeps changing under the pixels. The
  reference works because its layers are **static-placed**. ~25px median face drift from a constant
  map IS the reference's own looseness — **accept it. Per-frame accuracy is a trap.**
- **The FACE is ONE rigid anchor (eye midpoint).** Pinning both cartoon eyes onto his real eye
  positions forces his eye spacing onto different cartoon proportions and smears the whole face.
  **Position the face, never stretch it** — a stylised face's internal geometry is part of the style.
- **VERIFY MOTION WITH CONSECUTIVE-FRAME STRIPS, not sampled stills.** Tile 8 adjacent frames
  (`select=between(n,F,F+7), tile=8x1`) cropped to the face. Swimming shows as tile-to-tile jumps —
  uniform sampling and every still check missed it **three review rounds in a row**.
- Align each restyle with a **multi-anchor similarity fit**, never the face box.

## Related

`genvideo` (generating footage from nothing; the Veo/Omni filter maps live there) ·
`asset-plan` (cost-gate before any call) · `broll-select` (the never-upscale rule this bends) ·
`split-screen` (hook density).
