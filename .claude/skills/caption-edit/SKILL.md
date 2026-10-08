---
name: caption-edit
description: "The 'just a basic edit' format — the take stays WHOLE and uncut, full frame, no 60-40 split, no crop or reframe. Captions and typography from frame one, stamps in the clear top band, SFX, and a compact Follow strip instead of the split end card. Also covers the 'mostly raw' variant where visuals cut away over uncut audio. Use when he asks for a basic edit, says 'no cuts needed', 'keep it mostly raw', 'just add captions', or when the SHOT itself is the content (a two-shot, a walking take, a locked-off camera)."
---

# CAPTION EDIT — overlay only, the take stays whole

> **THE JOB:** the shot he chose IS the content. Do not split it, crop it, punch into it, or cut it.
> Everything you add rides on top.

> *"I want just a basic edit. Add captions and some typography from the start itself. Add some sound
> effects, and when I'm talking about the skills, don't convert it into the 60-40 thing. I just want
> you to add the skill at the top without cropping down or moving the whole video. It can come as an
> overlay, and that is it."* — then, mid-edit: *"No cuts needed."*

## Why this format exists

Two situations produce it, and both are about the footage:

1. **The shot is the content** — two people on a bench with a phone. A split card or a punch-in
   breaks the frame he chose, and on a locked-off camera the pauses are short enough that jump cuts
   read as errors.
2. **"Mostly raw"** — a walking handheld take where every cut jumps the background. On one reel
   there was **3.4s of true dead air in 162s**; five jump cuts to save 2% of runtime would have read
   as errors, not style.

## The shape

- **ONE uncut `OffthreadVideo`**, full frame, `objectFit: cover`, **never scaled**.
- **Two overlay bands, both measured per take** (`take-geometry`):
  - a **caption plate** in the clear band (under the chins on a two-shot) — black plate, 78px white
    700 display type, amber emphasis;
  - a **top band of solid stamps** in the clear headroom.
- **"Typography from the start" = something on frame one.** A top stamp naming what the viewer is
  about to see, landing on the first pop, gone the instant the source's own event takes over.
- **"The skill at the top" = a full lockup**, not a chip: the brand mark + wordmark at
  household-brand size, the skill as a mono chip beneath it, one chip per capability, **each popping
  ON its spoken word**.

## The Follow close

The standing 60-40 Follow end card is **NOT used** here. Instead the Follow→Following flip rides the
**top band as a compact strip** (avatar · handle · button) over a ~0.4s last-frame hold.

**With more than one person on camera, BOTH accounts get a strip**, tapped a beat apart. Real
numbers only — never invent a follower count.

## SFX

Pops on stamps at **~4 dB under his loudest word**. `pop.wav` and `transition.wav` are **hot files**
— use **0.25 / 0.2** volume, not 0.5. A swish on any source-baked element's arrival and exit, a
click per Follow tap. See `sfx-design`.

## The "mostly raw" variant — cutaways over uncut audio

Mount ONE continuous `OffthreadVideo` for the whole VO and paint the evidence beats on top as
overlays. **Cutting to a card and back never moves the audio.**

**The measured target: ~10% of the reel in cutaways.** One reel ran four cutaways, 16s of 162s; he
is on screen the other 90%. That is what "mostly raw" should measure out to.

### The trap this shape creates — frozen frames

**A 900×900 card is only ~39% of a 1080×1920 frame**, so when the card's content holds still the
WHOLE frame holds still and the review gate fails it (tblend difference, YAVG < 0.30). One version
had freezes of 0.75s and **1.48s**.

Fixes, in order of effect:

1. **Make the ground move enough to SEE.** A `#14151A` grid drifting 0.55px/frame is invisible to
   the eye *and* to the check. **`#1E2029` at 1.6px/frame on two axes** fixed every freeze at once —
   and it kills the dead-black feeling around the card.
2. **Speed up a step-based capture** — a replay at 1.6× went 20% → 34% card motion.
3. **Stage a drawn card** rather than landing it whole: furniture on frame one, only the numbers
   cued (`split-screen`'s furniture-vs-punch rule), and give filled bars a slow moving stripe so
   they are never a still object.
4. **A number waiting for its cue must render NOTHING.** Parked at "0.0%" it reads as a real score
   of zero — a different and wrong claim.

## What "basic" does NOT mean

**A locked-off take is not automatically this format.** If he names the Tharun look, says "same
editing language as those desk reels", or wants punch-ins and graphics living in the shot, that is
`layered-head-edit` — a full-frame head that CUTS. This skill is for the take that stays whole.

**Do not read "basic" as "skip the pipeline."** The review gate, the caption pause audit and the
audio-offset check all still run. Skip only what he named: the split, the crop, the cuts.

## Related

`take-geometry` for the bands (a two-shot needs both heads cleared; a walking take drifts).
`caption-align` for run construction and the pause audit. `sfx-design`. `reel-review`.
Sibling formats: `split-screen`, `broll-style-edit`, `vlog-edit`.
