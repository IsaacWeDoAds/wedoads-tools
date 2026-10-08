---
name: take-geometry
description: "MANDATORY first measurement on any new talking-head take — sample every kept clip, measure hair-top / chin / head-cx as DISTRIBUTIONS, then SOLVE the split-card fit and the clear caption bands from those numbers instead of nudging. Covers the headroom rule, the dx≤0 scale floor, drifting and swaying takes, the detectors that lie (Haar box bottom, dark-pixel scans, rotation metadata), and the alpha-channel face guard. Use before laying out ANY graphics on a new take, and whenever text lands on a face or a card crops hair."
---

# TAKE GEOMETRY — measure the take, then solve the layout

> **THE JOB:** before a single graphic is placed, know where his face, hair and hands actually are
> across the WHOLE take — as distributions, not as one frame — and derive the split-card fit and
> the clear text bands arithmetically. Every layout rejection in this project traces back to a
> number that was guessed or sampled too thinly.

**Nothing transfers between takes.** Reel 26 was a wider framing than reel 25 and *nothing* from
reel 25 carried. Measure every time.

## The two hard rules this serves

1. **Text/graphics live inside the IG safe zone**: below y=220 (top UI band), above y=1470 (bottom
   450 UI band), 35px side margins, ~100px clear on the right for the icon stack. Imagery may
   cross; TEXT may not.
2. **Text must NEVER cover his face in ANY frame.** A ~6-frame flash counts as a defect. Hair-top
   grazes pass; eyes/nose/mouth never do. When no face-clear spot exists, **drop the element**
   rather than overlap it.

## Step 1 — sample correctly

**Sample the midpoint of EVERY kept clip, not 3 frames.** Three frames that happen to agree will
calibrate a fit that is visibly wrong for most of the reel — that shipped, and he caught it and
pointed at the rule.

- ~20 frames minimum, spanning **every register** the fit will be used in.
- **Duration-weight** the samples, target the **median**.
- Sanity-check the extremes: at both sway ends the face must still read in-card.
- If the take **drifts**, say so and handle it (below). Reel 35's hair top moved y600 → y760 over
  70s as he settled; one number is wrong for that take.

Run `scripts/measure_take.py` (see below). Record hair top, chin, head-cx, and hand top per frame.

## Step 2 — the detectors that lie

| Detector | How it lies | What to do |
|---|---|---|
| **Haar face box bottom** | Is NOT the chin. A scan for "lowest dark row below the box" found a navy jacket collar and put the chin 130px too low | Judge the chin on a drawn-grid crop, not on a dark-row scan |
| **Haar box top** | Is not the hairline either; the offset is per-take. `boxTop − 145` held for reels 38/47, not for 48 | Derive the offset per take, or scan pixels when the background allows |
| **Dark-pixel hair scan** | Useless when the background is as dark as his hair (a dim corridor). Works when the wall behind him is bright | Check the background first; on a dark backdrop use the box offset + a guide line |
| **Passers-by** | A background person's hair registered as a y592 hit | Reject hits far from the head's x-band |
| **Rotation metadata** | iPhone side data survives ffmpeg re-encodes and lies to cv2/trackers; horizontal footage gets tagged −90, and the phone can flip mid-clip | Extract raw pixels with `-noautorotate` and **LOOK**. Bake with `-display_rotation 0` + transpose. The fix is 0° or 180°, never 90° |
| **Full-range colour** | Source is often `yuvj420p`; a scan on the wrong range shifts every threshold | `scale=in_range=pc:out_range=tv` before scanning |
| **Detector false starts** | Two detectors mis-found the head before a nose-verified grid crop settled it | Confirm on a drawn-grid crop; reject boxes outside 150–340px wide |

## Step 3 — solve the split-card fit (never nudge)

With footage scaled by `s` and offset `(dx, dy)` inside the card: `card_y = source_y·s + dy`.

**Horizontal — pin his HEAD's x, not the frame's.** He is rarely centred in his own frame (head-cx
has measured 448 to 596 against a 540 frame centre):

```
dx = cardWidth/2 − HEAD_CX·s        // card half-width (504), NOT (cardW − canvasW·s)/2
```

**Vertical — target HEADROOM. Do NOT centre the face.** Centring reads as a ceiling shot: a head
centred in a tall card leaves as much air above the hair as chin-to-shoulders below, and the eye
reads the air as waste. He rejected face-centring twice in the same words ("minimal headspace
above, the face is getting cut").

```
dy = HEADROOM − hairTop·s           // HEADROOM ≈ 11% of the card's VISIBLE height
```

Then **assert the TIGHTEST sampled frame still clears ~90px** so no frame ever crops his hair.

**The scale floor.** `dx ≤ 0` is required or the card's left edge shows background:

```
s ≥ (cardWidth/2) / HEAD_CX
```

Check the floor before picking `s`, and **prefer the lowest scale the floor allows** — in-card sway
amplitude is `sway·s`, so a low `s` both avoids upscaling his face and shrinks the wobble. `s = 1.0`
whenever the floor permits it.

**Measure the hair top off the RENDERED CARD, not off whole-take source medians.** This was wrong
by 176px on the first attempt: a take-wide median mixes in the full-frame beats where he sits much
higher, but the split registers use a different, lower subset. Keep both numbers, separately.

Derive the constants in code (`FACE_FIT_SCALE`, `FACE_FIT_DX/DY`) so re-measuring re-solves the
framing instead of requiring new nudges. Feed the same `{scale, dx, dy}` into the split→full
transition as its `fromFit` so the grow lands exactly on the full-frame framing.

### Special cases

- **A drifting take** (he settles lower over time): frame to the EARLY clips' hair and verify the
  late ones still fit, or split the reel into two fits.
- **A walking take**: bands drift ±97px. Fit the **median**, never a frame.
- **Two shot sizes in one take** (hook shot closer than the body): ONE fit crops his hair in the
  hook or leaves the body swimming. Carry **two fits** — `FIT_HOOK` and `FIT_BODY`.
- **A punched full-frame register**: the punch must not expose a frame edge —
  `|tx| ≤ 540 − 540/k` and `|ty| ≤ 960 − 960/k`.
- **Scaling a full-frame face beat**: scale **about the chin**, not the centre — 1.10 about the chin
  crops dead ceiling without pushing the chin into the caption band.

## Step 4 — derive the caption bands

Compute, don't type pixels:

```
CAPTION_FACE_Y = max(chin + 180, handTop + 96)
```

Then check the result against the take:

- **Hands are the usual blocker.** Gesture-heavy takes hold y1050–1700 all reel; a mic or lav at
  chest height rides y900–1300. On several takes there is **no clear band below the face at all**,
  and every full-frame caption must live in the headroom band (y230–560) over a top scrim.
- **A tight top band forces the layout.** With IG chrome at 192 and hair at y545, the top band is
  only ~315px — a 4-row ledger will not fit; it becomes a 2×2 block.
- **Punch-in shrinks the band.** At 1.12 a hair top of y520 rises to y467, which still clears a
  ONE-line caption block but not a two-line one. Keep captions single-line under a punch.
- **A phase-varying take needs per-window bands.** When he leans in, hair can rise from y735 to
  y360 — the top band is then only safe in specific windows, and each element must be checked
  against its OWN window, not the take median.
- **Ink is invisible over video.** Anything in a band over footage is white-on-scrim.

## Step 5 — enforce with the alpha guard, not with your eyes

`scripts/face_guard.py` renders the graphics-only (transparent) composition, reads the **alpha
channel**, and asserts zero opaque graphic pixels inside the face band per beat.

```bash
python3 scripts/face_guard.py OVERLAY.mov --top 442 --bottom 1111 [--max-coverage 0.85]
```

It catches what a contact sheet cannot: a stamp hanging 10px into the band, a text stack
overflowing onto hair, and the **one-frame register seam** where a face card rendered while its
paper background was still gated behind `if (p <= 0.001) return null` — one frame of opaque black
across his face (231k opaque px at y880–1109).

Two traps in writing that guard:
- **Do not detect the face by dark pixels** — caption drop-shadows read as dark and false-positive
  as hair. Use the graphics layer's alpha; it answers the actual question.
- A full-frame MG beat is ~100% opaque by design. **Skip** frames whose alpha coverage exceeds ~85%.

**The guard cannot see a crossfade.** At a register seam nothing is opaque, so an opaque-pixel guard
misses it entirely — which is one of the reasons registers hard-cut (`split-screen`).

## Step 6 — write it down

Every take's numbers go in `data/takes.md` as a row. It is the single reason a re-render months
later does not re-measure from scratch — and the reason "nothing transfers" is provable rather than
a slogan.

## Related

`split-screen` consumes the fit and the bands. `caption-align` places runs inside the bands
this skill derives. `screen-capture` frames the other half of the split.
