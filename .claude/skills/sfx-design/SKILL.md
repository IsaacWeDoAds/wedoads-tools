---
name: sfx-design
description: "Place sound effects so they LAND — schedule at event_frame minus the file's measured peak offset (not at its start), pick the sound by what is moving, and set volume for the FINAL domain using the measured mix + delivery gain. Carries the peak-offset table, the volume formula, the 522-entry house library, and the voice-subtracted residual check that actually proves a cue fired. Use whenever SFX are added, whenever a cue lands late, and whenever a mix clips after normalisation."
---

# SFX DESIGN — landing the hit, at the right level

> **SFX only in edits.** he adds music when posting. (The one exception is a format that
> specifies a bed — see `broll-style-edit`, where a continuous bed is structural but *he* still
> adds it.)

## 1. Schedule at the PEAK, not at the file start

An SFX file's transient does not sit at its start, so scheduling a cue at the visual event makes the
hit land **late**.

```
start_frame = event_frame − peak_offset
```

Measured at 60fps (re-measured with `astats` at native rate, unchanged):

| file | peak offset | file peak |
|---|---|---|
| `click.mp3` | **0.5 f** | −1.2 dBFS |
| `pop.wav` | **7.4 f** | −1.35 dBFS |
| `swish.mp3` | **14.5 f** | −15.7 dBFS |
| `swish2.mp3` | **15.5 f** | −16.1 dBFS |
| `transition.wav` | **10.3 f** | −0.85 dBFS |

Re-measure if the files change: decode to mono PCM, take `argmax(|x|)`, divide by the sample rate,
multiply by fps.

## 2. Pick the sound by what is MOVING, not by taste

| motion | sound |
|---|---|
| the frame travels (into or out of a full-frame graphic) | **whoosh** — length matched to the length of the move |
| something snapped in without moving | **click** |
| a toggle or a checkmark | **tick** |

**Dial whooshes down. They are always too loud.**

## 3. Volume — set it for the FINAL domain

Three things stack up between the `volume` prop and what the viewer actually hears:

1. **Remotion's mix lands SFX ~+5.2 dB above `20·log10(volume)`.** `pop.wav` at `volume={0.086}`
   measured **−17.5 dBFS** in the render, not −22.7. Treat `MIX_OFFSET_DB = 5.2` as a constant until
   re-measured.
2. **Delivery gain.** A phone-mic take sits around **−23.6 LUFS**, so reaching −14 adds **~+9.7 dB**
   to everything, SFX included.
3. **The files are hot.** `pop`, `click` and `transition` all sit within ~1.4 dB of full scale.

**So `0.45` on `pop.wav` is a transient ~9 dB ABOVE his loudest syllable** — and if loudnorm has
fallen into dynamic mode it pins every one of them to the ceiling regardless of what you set
(`render-ops`).

```
vol = 10 ^ ((target_final − delivery_gain − 5.2 − file_peak) / 20)
```

For a pop at **−10 dBFS in the finished file**: **≈0.066**. click ≈0.06 · transition ≈0.058 ·
swish ≈0.37 (its file is quiet). Rough rule of thumb: **~0.06–0.07 lands a pop at −10 dBFS; stamps
sit ~4 dB under his loudest word.**

**Verify on the delivered file**, in a window with no speech (the hook pop before his first word is
ideal):

```bash
ffmpeg -ss T -t 0.25 -i final.mp4 -af astats=measure_overall=Peak_level -f null -
```

### The measurement trap

**A numpy check that decodes with `-ac 1` SUMS the two channels** — an in-phase transient reads up
to **+6 dB too hot**, and voice "peaks" appear above 0 dBFS while `ebur128` says −1.6. Meter with
ffmpeg (`astats`, `volumedetect`, `ebur128=peak=true`) or decode the channels **separately**.

## 4. The house library

His own SFX folder is now the library: **`public/sfx/lib/<cat>/<slug>.wav`, 522 peak-measured
entries** (48k stereo PCM16; one-shots peak −1 dBFS, beds RMS −20 dBFS; multi-hit files sliced at
onsets into `-NN`). Each carries a `peak` (argmax) and an `onset`.

- Index: `docs/sfx-library.md` · TS map: `src/LF01/sfxlib.ts` · builder:
  `.claude/skills/longform-edit/scripts/sfx_lib.py`
- `peakAt(at, slug, vol)` schedules `start = at + 2 − peak·fps`; `bedAt` fades in/out.
- Reference levels against a voice RMS of −20.5 dBFS: **one-shots 0.22–0.4**, **chapter stacks ≤0.4
  each** (0.5+0.5+0.3 stacked hit +0.4 dBTP), **beds 0.14–0.3**.

## 5. Density

- **Split-format 9:16 reels: ~1.0 strong transient per second**, voice-forward (side/mid 0.10,
  no wide bed). Low ticks (vol ~0.13) on every 2nd caption-group swap in screen registers, on top of
  the register/graphic cues, hit that density.
- **B-roll-led reels: ~1 cut in 4 carries an SFX.** Do not measure this with a band-energy test —
  with a continuous music bed there is a transient near almost every cut, and one such test reported
  **3× the truth** (`broll-style-edit`).

## 6. Prove the cue actually fired — the residual check

**Envelope-vs-envelope comparison of AAC against PCM is useless** — it produced **113 false spikes
in 27 seconds**.

`sfx_check.py render.mp4 first_comp_frame` cross-correlates the render against `cut.wav` (which also
finds the **+42.7 ms AAC priming lag**), **subtracts the voice**, and lists residual events against
the scheduled cues. That is the only comparison that answers "did this cue land, and where".

## 7. Retime SFX whenever captions move

SFX cues and card boundaries were placed against the old caption frames and **drift with them**.
Retime them in the same pass as any caption regeneration (`caption-align`).

## Related

`render-ops` (loudnorm — SFX transients ride on a normalised voice, so a mix that is fine before
normalisation can clip after) · `mg-kit` · `split-screen` · `caption-edit` · `reel-review`.
