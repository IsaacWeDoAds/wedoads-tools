# The Hinglish creator-essay edit — measured off 3 reference reels

**Measured 11 Aug 2026** from three reels Nishant sent as the target. This is the genre reel 22
should have been cut in. Everything below is measured, not recalled.

| Ref | Subject | Length | Creator register |
|---|---|---|---|
| 1 | Oral-B toothbrush (sponsored) | 57.4s | product/routine montage |
| 2 | "MINDSET" — the year that changed things | 99.8s | personal story essay |
| 3 | "appreciate the people around you" | 79.5s | opinion essay (`hustlewithharman`) |

---

## 1. Pace — the single biggest gap

Scene-change detection (`select='gt(scene,0.28)'`):

| | cuts/sec | avg shot |
|---|---|---|
| ref 1 | **1.08** | 0.93s |
| ref 2 | **1.06** | 0.94s |
| ref 3 | **0.76** | 1.32s |
| **reel22 v1 (mine)** | **0.35** | 2.85s |

And mine flatters itself — 4 of those 14 detected "cuts" are graphics appearing. The real shot
count is **8 clips in 40s = 0.20/sec, avg shot 5.0s**. The references change picture **5× more
often**.

> `docs/personal-account-guidelines.md` §11.7 **bans** cuts faster than 0.4/sec and §4
> puts Mode B at 0.10–0.20/sec. The references run at 3–5× that ceiling. The doc and the target
> are not describing the same genre.

## 2. Talking head is the minority register

Estimated from the contact sheets: ref 1 ~30% talking head, ref 2 ~40%, ref 3 ~50%.
**Mine: ~90%** (36s of 40s on one locked framing).

The b-roll is not decoration — **each shot literally illustrates the line being spoken**. Ref 1
says "kisi ko coffee se" over a coffee pour, "kisi ko workout se" over three gym angles, "mere
toothbrush se" over the toothbrush. Ref 2 cuts to the car, the watch, the key, the driving POV,
his own old YouTube videos, the silver play button.

**Same action gets several angles cut together** (ref 1's bathroom sequence: side, front, close,
side, front — five shots of brushing teeth in ~5s).

## 3. Register split

- **Ref 3: talking head in COLOUR, all b-roll in BLACK & WHITE.** Clean, instantly readable
  "now" vs "illustration" split. Costs nothing and it is the most ownable device of the three.
- **Ref 2: blurred-self backdrop.** When a shot isn't 9:16 it is centred at native size over a
  blurred, scaled-up copy of itself. That is how they use landscape footage without upscaling it
  into the full frame.

## 4. Captions — a completely different system to what I built

All three:

- **Large.** Roughly 5–7% of frame height, not the 3.2% the guidelines specify.
- **They BUILD progressively.** A phrase accumulates word-group by word-group in place, then the
  whole line swaps. Ref 2's hook: `Kuch din` → `Kuch din PEHLE` → `Kuch din PEHLE maine tumhe
  apni` → (swap) `life` → `life ki kuch CHEEZE` → `life ki kuch CHEEZE dikhayi thi`.
- **Two-tone and two-typeface within one caption.** Connective words in white; the **stressed
  word in a colour, bold, and often italic or a different face**:
  - ref 1 → **teal/cyan**, accent word in an italic serif (`coffee`, `workout`, `toothbrush`)
  - ref 2 → **yellow**, accent word in heavy italic sans (`PEHLE`, `CHEEZE`, `5,000`, `MINDSET`)
  - ref 3 → **yellow** caps for stress, white italic serif for the rest
- **Romanised Hinglish**, tracking the spoken words closely — not a translated summary.
- Ref 3 varies it: loud two-tone treatment on the **hook**, then small plain white captions over
  the B&W body. The hook earns the big type; the body doesn't.

> §11.1 bans karaoke captions and §11.4 bans yellow. The references do both. §6's "one line per
> beat, ≤7 words, one font, white only" is not this genre.

## 5. Audio — the finding I'd have missed by eye

50ms RMS envelope over the whole reel:

| | noise floor (5th pct) | median | frames below −50 dB | LUFS | LRA |
|---|---|---|---|---|---|
| ref 1 | −30.7 dB | −18.4 | **0.0%** | −14.30 | 2.6 |
| ref 2 | −29.8 dB | −19.6 | **0.0%** | −14.62 | 3.8 |
| ref 3 | −29.9 dB | −19.0 | **0.0%** | −14.37 | 3.6 |
| **mine** | — | — | drops to **−65 dB** in every gap | −14.35 | 4.6 |

**There is never silence.** A continuous music bed sits ~11–16 dB under the voice and runs the
whole length. That bed is what makes a 1-second cut rate feel smooth instead of frantic — it is
load-bearing for the pace, not decoration.

My reel drops to −65 dB between clips, so every jump cut lands in a hole. Loudness is the one
thing I matched (−14.35 LUFS); the floor is what's wrong.

**SFX are selective, not per-cut.** Sharp onsets (>3.2× rise over 30ms) aligned within 120ms of
a cut: ref 1 **10%**, ref 2 **23%**, ref 3 **24%**. So roughly **one cut in four or five** gets a
hit — accents, not a whoosh on everything. Mine: 0%.

## 6. Ending

Ref 3 closes on a branded card — `HUSTLE with harman` in yellow caps + white italic serif — with
an **animated follow pill** that flips Follow → Following.

> §5d and §11.6 ban exactly this (no handle, no logo, no follow stinger). My own standing note
> follow end card says the opposite. The doc loses.

---

## 7. What this means for reel 22

The v1 edit is not a bad execution of this style — it is a faithful execution of a **different
and wrong** style. I followed the LOCKED guidelines doc literally, and that doc describes a slow,
graphics-free lifestyle genre (Tarini / Visha / Chloe) that is nothing like the reels above.

To rebuild in this genre reel 22 needs, at minimum:

1. **~35–40 shots, not 8.** Avg shot ~1s. From the 457-clip catalog, illustrating each line.
2. **A continuous music bed** at roughly −30 dB under a −18 dB voice, and no gap ever reaching
   silence.
3. **SFX on ~1 cut in 4**, peak-aligned.
4. **Big two-tone building captions** with a coloured stress word.
5. **A register split** — B&W b-roll against the colour talking head is the cheapest strong one.
6. **Only 36.7s of usable VO exists**, which caps the reel around 40s. The references run 57–100s.
   Reel 22 will stay short unless he shoots pickups.
