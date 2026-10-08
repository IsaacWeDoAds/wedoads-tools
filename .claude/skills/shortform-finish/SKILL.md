---
name: shortform-finish
description: "v2 (Oct 2026). STAGE-2 finishing pass — runs AFTER shortform-cutaway has locked (and cut-audit has proved) the cut. The styling layer: reframe, the zoom-out hook, static punch-ins on jump cuts, gated lens FX, the exponential text fade-in and authority-stack type, captions at phone-scale sizes, sound design peak-aligned and set at the right level, an optional ducked music bed, loudness delivered at −14 LUFS measured on the encoded file. Encodes the house rules learned the hard way: nothing animates across a cut, registers hard-cut, no constant push-ins on screen recordings, text never on the face. The cut is sacred — this skill never re-picks takes or moves cut points. Use for 'add a zoom', 'make it pop', 'add sound design', 'finish this short', 'the SFX are too loud', 'add music under the hook'."
---

# SHORTFORM FINISH v2 — the styling / animation stage

> **THE JOB:** make a LOCKED cut look and sound finished — framing, motion, type, captions, SFX, (music when
> asked), loudness. The cut itself is decided upstream; this skill never re-picks takes or moves cut points.

This skill teaches the **method**. Bring your own motion-graphics templates, SFX library and look.

## What changed in v2 (each from a real rejection)

| v1 | his verdict | v2 |
|---|---|---|
| punch-in/out **wave across cuts** | "shows that there is a cut" | **nothing animates across a cut.** Same-take jump cuts alternate a STATIC 1.00 / 1.12 framing; motion lives inside a shot, never on its edge |
| slow push-in on a still screen recording | "the constant zooming in looks odd. don't do that" | static framing; make the capture itself move (scroll, cursor) instead |
| SFX at file level | after the first full sound pass: "reduce the sound of SFX by 4 dB" | set levels from the formula below, then **trim the whole kit together** (−4 dB took it from "loud" to right) |
| one sound per kind | repetitive | 3–4 **variants per kind**, rotated; ≤ 1 transient per 0.22 s |
| no music ever | long-form: "no background music at the start — should be joyful / suspenseful" | SFX-only by default (he adds music on reels); a **ducked bed under a long-form hook** when asked (recipe below) |
| text at "readable" sizes | unreadable on a phone | measured floors: captions ≥ 78 px on 1080×1920, in-card mono ≥ 36 px |

---

## ⭐ FIRST RUN — which editor?
Ask once: **(a) Resolve** (Fusion graphs, BezierSpline keyframes) · **(b) Premiere** (keyframed Motion,
Essential Graphics) · **(c) Remotion** (`interpolate` everything) · **(d) HyperFrames** (HTML + GSAP; media
clips with `data-*` timing) · **(e) ffmpeg only**. Default: Remotion or HyperFrames for control, ffmpeg for
zero extra software.

## WORK ON A DUPLICATE — never the locked cut.

## REFRAME — check the source first
1080×1920 canvas. A vertical source fills at scale 1.0; a 16:9 source fill-scales (crops the sides).
For 16:9 long-form the same rules apply at 1920×1080.

---

## TECHNIQUE 1 — MOTION THAT NEVER CROSSES A CUT

### The zoom-OUT hook (opening only)
Scale `1.3 → 1.0`, front-loaded ease-out: `[0]=1.3 [6]=1.13 [14]=1.05 [26]=1.01 [40]=1.0` (24 fps). Motion
blur only during the move. **Center-lock** at 0.5,0.5 on anything that settles to ≤ 1.0 (an off-centre
pull-back exposes black). It starts on frame 0 of the first shot — it is the opening, not a transition.

### Jump cuts inside one take: STATIC punch alternation
Consecutive pieces from the same take alternate **1.00 / 1.12** framing (anchored on the face, from the
take-geometry measurements). Each side of the cut is still; the size change itself hides the jump.
**Never a zoom that is moving at the cut** — that is the rejected wave.

### Lens FX only DURING a move
Zoom blur / chromatic aberration peak during the fast part of the hook and return to 0 at rest. Never blur
the whole clip. Every zoom wants a whoosh (peak-aligned).

### Screen recordings
They must MOVE on their own (≥ 30 % of frames changing): one continuous creep scroll, a 96 px on-page
pointer moving with it. A still screen does not get an animated push-in to "keep it alive" — that reads as
odd; fix the capture instead. Long-form 16:9: show the **full screen width** in a rounded card on paper,
crop only the macOS Dock (bottom) or Chrome's bookmark bar (top), with the face in a 9:16 card beside it.
9:16 split-screen: zoom text-heavy captures 1.3–1.55 and frame with source x/y — a centre crop clips the
first letter of every line on left-aligned pages.

### Face on the side he looks toward
If he faces screen-right in the take, his face card goes LEFT and the graphics RIGHT, so he looks into them
(check every take — it is a property of the set, not a constant).

---

## TECHNIQUE 2 — EXPONENTIAL TEXT FADE-IN
Never linear. `opacity = 1 − e^(−k·t)` with a ~10 px rise and blur-to-sharp on the same ease-out; exit =
lift + blur-out. Remotion: `Easing.out(Easing.exp)`. GSAP: `power3.out` / `expo.out`.
**A graphic must be FULL in its first frame of use** when it carries the punch line — an end frame caught
mid-fade reads as a defect (a "FREE" that landed 0.5 s before the cut was caught grey).

## TECHNIQUE 3 — THE AUTHORITY STACK
Bold, tight tracking (≈ −0.04 em), words rise out of a soft fog and speed-ramp to a settle, lines stacked
with slight depth, exit = lift + blur-out. Give the "editor voice" a warm accent colour.

## CAPTIONS (when the format has them)
- Frames from the **source word times** mapped through the cut (never re-transcribe the rough cut); pin the
  repaired regions to the delivered audio.
- Display type, 1–3 words, ≥ 78 px on 1080×1920; never over the face (measure the take first — take-geometry).
- Every beat gets a caption (no 1-frame holes), and no caption run sits over measured dead air.
- Long-form: no running captions; emphasis lockups only, in the lane away from the face.

## ON-SCREEN ASSET RULES
0. **Look at the asset** before using it. 1. It appears **only while its line is said**, re-texted to the exact
words. 2. User images small, clustered in negative space, popped in ~3 frames apart, never over the face.
3. Re-text at the **source** and re-render. 4. **Parallax** over a zooming clip (graphic zooms slightly more).
5. Every animated element gets its own small SFX. Keep elements clustered — one zone for the eye.
6. **Registers hard-cut.** No opacity crossfade between registers (the base cut shows through both). The only
motion across a register edge is a slide that *is* the register change (a drawer, a page sliding in).
7. **Never text or graphics on the face.**

---

## TECHNIQUE 4 — SOUND DESIGN

**Pick the sound by what MOVES:** whoosh = a move (length matched to the move) · click/pop = a snap-in ·
tick = a toggle / a word landing · paper slide = a page or drawer · riser + hit (+ paper) = a chapter card ·
keyboard bed = typing (sized to the typed span, re-triggered every ~0.9 s) · readout ticks = a counter ·
shutter = a frame grab · a soft tech click = a cut into a screen beat. Not on plain b-roll cuts.

**Schedule at the PEAK:** `start = event − peak_offset` (decode, `argmax(|x|)`, ÷ sample rate). Keep a
catalog of every file's peak and onset; schedule from it, never by eye.

**Set levels for the FINAL domain:**
```
vol = 10 ^ ((target_final − delivery_gain − mix_offset − file_peak) / 20)
```
`delivery_gain` = the gain the loudness normalisation will add (a phone-mic take at −23.6 LUFS gains ~+9.7 dB
to reach −14); `mix_offset` = what your renderer adds (Remotion measured +5.2 dB over `20·log10(volume)`).
Library one-shots peak-normalised to −1 dBFS land well at **0.13–0.27** under a voice at data-volume 2.0;
whooshes 0.2–0.3; risers/hits ≤ 0.3. Then **listen to one full pass and trim the whole kit together** —
the creator's ear is the last stage (−4 dB was the fix on the first long-form pass).

**Variety:** 3–4 variants per event kind, rotated; ≤ 1 transient per 0.22 s (thin the rest).
**Prove it fired:** subtract the voice from the render (cross-correlate against the cut's own audio) and
list residual events against the schedule — envelope comparisons of AAC against PCM are useless.

### Music bed under a hook (only when asked)
1. Pick by brief, not by name: search a licensed catalog by mood (e.g. "curious upbeat tech intro, building
   anticipation"), then have a model *listen* to 5–8 candidates and score them against the brief — mood per
   section, does a lead melody fight speech, harsh stops. Take the one whose structure matches the hook
   (curious opening → driving → joyful).
2. Duck it on the cut's own speech envelope: ~**−10 dB vs voice in his gaps, −17.5 dB under speech**,
   attack 60 ms, release 350 ms. Bake the level into the file; play at volume 1.
3. Fade it out over ~2 s across the hook→body cut so it is gone ~1.5 s into the body.

### Reverb throw — `scripts/reverb_throw.sh`
The last moment of a clip blooms into a reverb tail (SoX Freeverb, wet-only). For depth at a cut.

## TECHNIQUE 5 — EDITOR TAKEOVER (optional)
"Let my editor explain" → a short MG explainer with a TTS voice → back to the speaker; text speech-synced.

---

## LOUDNESS + DELIVERY
- Master at whatever the mix gives, then a YouTube/IG copy at **−14 LUFS integrated, ≤ −1 dBTP**, measured
  **on the encoded file** (AAC overshoots a PCM loudnorm target): linear gain + an oversampled limiter,
  re-measure, iterate ≤ 3×.
- Every dialogue cut carries its micro-fade (from the cut list) — no clicks.

## HYPERFRAMES TRAPS (if you finish in HyperFrames)
- A `border` / `box-shadow` on an **untimed wrapper** shows on every frame of the edit. Put card frames on a
  **timed plate behind** the video (an ink rim + shadow, 2 px larger than the card).
- Audio fades: `data-fade-in` / `data-fade-out` on the media element; never on a section edge inside a piece.
- The Studio preview may show a live, ready `<video>` unpainted on a 300-clip timeline (the browser's
  player cap). Trust rendered frames, not preview screenshots.
- Long timelines: render in ~90 s sections (boundaries where no scene host spans), cache by content hash,
  stitch with exact frame counts. Make sound-variant rotation deterministic per cue, or one added cue
  invalidates every section's cache.

## AUDITION WORKFLOW
Render 4–5 alternatives per styled moment and compare. Place every created asset on the timeline.

## ⛔ NOT DONE UNTIL THE REVIEW GATE PASSES
Run **`reel-review`**: the deterministic script, then a **different model** (a vision reviewer) over sampled
frames from every section. Check every finding against full-res frames — the reviewer sometimes samples a
frame before a graphic lands — and fix every real blocker before the creator sees anything.

## SCOPE
**DOES:** reframe · hook zoom · static punch-ins · gated lens FX · text looks · captions · SFX + levels ·
music bed (on request) · loudness · delivery.
**DOES NOT (→ `shortform-cutaway`):** pick takes · move cut points · remove silences.
