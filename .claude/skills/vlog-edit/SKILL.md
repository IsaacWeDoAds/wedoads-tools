---
name: vlog-edit
description: "Use when editing a day-in-the-life vlog for his main YouTube channel (16:9, his own DJI/iPhone footage), from the first cut to the export — including when he asks for text, typography, motion graphics, sound design, music or a colour grade on a vlog, and when a vlog cut shows jumps, repeated frames, clipped or half-finished lines, a blip at every cut, text on a messy background, or an export that runs out of memory. NOT for the essay-style long-form (longform-edit) and NOT for reels."
---

# VLOG EDIT — coverage first, type only when he asks

> **HIS OWN VLOG IS THE SPEC.** After a Vlog-3 cut built around an elaborate type system, he sent
> his own "A Day in My Life in Dubai" (12:08) as the reference: *"you'll understand the difference
> between what you have edited and how the vlog should have been done."*
>
> Reference build for everything below: **Vlog 3 in HyperFrames** (`hyperframes/vlog3-edit/`, its
> `BRIEF.md`, which records every decision and round of notes, and the toolkit in `work/vlog3/`). Paths are
> relative to ``. Copy that toolkit for the next vlog.
>
> `reel-edit` routes vlogs here. Of its pipeline, keep the asset plan, the cut audit, `sfx-design` and
> the independent Fable review. The reel deliverables (IG caption, DM PDF) don't apply: a vlog ships the
> two files under "Sound, music, grade, export".

## Pick the mode first

| He says | Mode | Read |
|---|---|---|
| nothing about text or graphics | **Coverage**: zero on-screen typography (his own vlog has none) | this file |
| "add text", "typography", "motion graphics", "sound design" on THIS vlog | **Treatment**: one design language of time cards, paper notes, handwriting, a freeze, light leaks, an end card | `references/treatment.md` |

Either way: **asset plan + rendered style frames first, his yes before the build** (`asset-plan`).
A treatment applies to that video only; the next vlog defaults back to coverage. If his words don't
clearly ask for text or graphics, it is coverage: ask, don't start a treatment.

**Put the mode question in the asset plan, every vlog.** Vlog 2 was built in coverage. He reviewed it in Studio and
said "there is no sound design, no typography", then asked for "more typography" on the treatment: a whole second build.
Show a style frame of each mode and let him pick before the cut is styled. Coverage still needs an audible SFX layer
(~7 cues/min at −20…−22 dBFS peaks); two transition whooshes read as "no sound design".

## The measured format (his own vlog)

Measured frame-by-frame across 120 scene cuts:

| | value |
|---|---|
| on-screen typography | **NONE.** No title card, timestamps, lower thirds or emphasis type. Opens **cold** on a POV shot of his feet |
| cut rate | **9.9 cuts/min** · median shot **2.45s** (mean 5.58s) |
| distribution | 14% <1s · 26% 1–2s · 22% 2–4s · 17% 4–8s · **21% over 8s** |

**Lots of very short inserts PLUS some long talking takes**, not a uniform pace. Interest comes from
**coverage**: every beat shot from several positions (tripod wide → handheld selfie → macro insert).
Rhythm devices without type: a recurring transition motif (elevator-mirror selfies), desaturated/B&W
frames as punctuation, burst montages at transitions (nine cuts in seven seconds).

**Cut cutaways in OVER continuing dialogue**, so the audio spine never breaks. **A muted cutaway must
never show him talking to camera** (5 of 25 inserts broke this once). Contact-sheet every insert.

**The constraint an edit cannot fix:** long locked-off single-angle takes cap the rhythm. He allows
**1.15× punch-ins** (1.3× rejected), one extra framing tier. **Flag "grab inserts as you go" before the
next shoot, not after.**

## Clean cuts: the first thing he notices

He watches for jumps. Every one of these was a note on Vlog 3. Full detail: `references/cut-cleanliness.md`.

- **A split inside one continuous take must be invisible:** the next piece starts *exactly* where
  the last one ends. Rounded in-points from Palmier replayed 2–9 frames at 19 splits ("it jumps").
- **One level per take.** Per-piece level matching put 6.5 dB steps on invisible seams.
- **Removing content inside one framing = a jump cut** → the far side gets the 1.15× punch-in.
- **Every cut point in silence**, frame-exact (60 fps), checked on the audio envelope. Never inside
  words that run together.
- **Finish the thought.** Before keeping a clip's out-point, read the source past it; a line that
  trails off ("…created multiple ones") gets extended until it lands.
- **Say it once or twice.** A topic he repeats ("the event", four times) keeps the setup and the
  payoff; cut the middle mentions. Cut fumbles and false starts.

## Sound, music, grade, export

- **SFX** (`sfx-design`, peak-aligned): sound the real actions and the big beats. Not every piece
  of text gets a sound (the shipped palette is in `references/treatment.md`). **Level: peaks −20 to
  −22 dBFS in the master**, where speech runs ~−19 LUFS and his syllables peak at −16 dBFS (median)
  and −7.5 (loud ones). That puts a cue about 5 dB under a normal syllable. His note on −13 dBFS was
  "too loud". Set levels on the master; the −14 LUFS copy lifts voice and SFX by the same gain.
- **Music is his, added at posting**, unless he asks. When he asks: bursts around the talking, never
  ducked, ~11 LU under the voice, silence on the story's turn. Library music only; check the
  licence before a monetised upload.
- **Colour grade: bake it into the footage. Never a live per-clip shader** on a many-clip timeline
  (one ungraded frame at every cut). See `references/hyperframes-pipeline.md`.
- **Export in sections** on his 18 GB Mac; a one-shot export of 80+ clips crashed it twice.
  **Ship two files:** the master and a −14 LUFS YouTube copy, which is the one he uploads. YouTube
  only turns loud videos down; it never lifts a quiet one.

## Common mistakes (all made on Vlog 3)

| Mistake | What he saw | Fix |
|---|---|---|
| Grade applied per clip in the editor | "a little blip between clips, like a transition" | bake a LUT into the sources |
| Trusted the imported in-points | "the cut jumps, it should be very clean" | exact continuity + one gain per take |
| Clip ended where the transcript said | "feels something got trimmed" / "the line doesn't make sense" | read the source past every out-point |
| Text placed by eye | "move it a little down onto the white wall" | measured placement on the plainest surface |
| Note anchored to the frame edge on a walking selfie | face grazed near the end of the hold | check the whole hold, dilated person mask |
| SFX matched to reel levels | "too loud, make them −7 dB" | −20…−22 dBFS peaks |
| Studio "Export" on the full project | memory red, Mac crashed | sectioned render |

## Where the rest lives

`references/treatment.md` (the text and graphics system, placement, face safety, end card) ·
`references/cut-cleanliness.md` (seams, levels, trims, finishing lines, Palmier traps) ·
`references/hyperframes-pipeline.md` (project setup, ripple edits, baked grade, mono trap, sectioned
export, deliverables). Memories: vlog3 dubai day, vlog location time cards,
hyperframes project setup, palmier clip placement, sfx peak alignment.
Siblings: `broll-select` (never upscale), `longform-edit` (the essay format, which DOES carry
type), `cut-audit`.
