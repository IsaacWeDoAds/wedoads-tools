---
name: broll-style-edit
description: "The B-ROLL-LED format for the personal account — the fast Hinglish creator essay: ~1 shot/sec, talking head only 30–50% of screen time, b-roll from his own library literally illustrating each line, building two-tone captions in the black band below a square card, colour-register storytelling (past in B&W, blooming to colour on the payoff). Carries the card-format architecture, the standing copy rules, the listicle variant, and the account-separation rule. Use for any personal-account reel, any story/essay reel, and any reel where b-roll rather than a screen carries the picture."
---

# B-ROLL STYLE EDIT — the fast Hinglish creator essay

> **FIRST, ESTABLISH WHICH ACCOUNT.** Two grids with deliberately non-converging looks:
>
> | | the tools account | the personal account |
> |---|---|---|
> | subject | tools / tutorials | personal essays |
> | picture | screen recordings | his own real-life b-roll |
> | accent | `#F8F800` yellow | **blue family** (`#2D4BFF`) |
> | format | `split-screen` | this |
>
> **Never yellow on this account.** The separation rests on **accent colour and register**, not on
> density — both are dense now.

**A locked account doc outranks a named style reference.** When a request named the
split style while handing over the personal-account doc in the same message, the right move was to surface the
conflict and ask. He chose: **the locked doc wins.** `docs/personal-account-guidelines.md`
is the rulebook; this skill is the operating summary.

## The measured spec

**v1 of the guidelines doc was WRONG and produced two rejected reels** — it was written from a slow
lifestyle cohort. The account is the fast Hinglish creator-essay genre, referenced to
a high-volume creator-essay account. *"too fucking plain. No font change, nothing, how is this even an
edit."*

| | target | the rejected v1 |
|---|---|---|
| cuts/sec | **0.76–1.08** (avg shot 0.9–1.3s) | 0.28 |
| median shot | **0.9–1.3s** | ~2.9s, longest 6.7s |
| cuts in first 5s | **3–6** | 0 |
| cuts carrying SFX | **~1 in 4** | 0% |
| talking head | **30–50% of screen time** | ~100% |
| music bed | continuous — **but he adds it**; the edit ships SFX-only | none |

**A cut is a change of picture, not a graphic appearing.** And still no zoom at cuts — just more
cuts.

### Distrust the detectors on this style

That table has been measured wrong **twice**:
- A scene detector thresholded too high **missed cuts between visually similar setups** (two gym
  angles, two bathroom angles) — which is most of this style. It reported **half the real pace**,
  which is exactly the error that made v1 plain.
- A band-energy test counted **music-beat transients as SFX** and reported 3× the truth. With a
  continuous bed there is a transient near almost every cut.

**Settle any pace disagreement by sampling frames and counting shots BY HAND**, never by re-running
a detector.

## The card-format architecture (standing since 31 Aug 2026)

- **Talking head = native 1080×1080 SQUARE on PURE BLACK at y240.** No upscale, no blur. Canvas
  stays 9:16.
- **Landscape b-roll** → the same square-on-black. **Portrait b-roll** → full-bleed.
- **Captions in the black band BELOW the square** — block ≈ y1330–1562.

`cardkit.py` + `CardReel.tsx` encode this. **Don't regress them when copying.**

### Per-reel anchor crop is MANDATORY

His seat drifts through a single session: face cx **922 → 911 → 974 → 999** across four spans of the
same shoot. **Always re-measure on the cut parts, never inherit.** See `take-geometry`.

## The copy rules (six reels bounced on these in one review)

1. **Captions live in the black band below the card.** Never inside the card, never over the video.
   *"why is the text on top of the video when we have so much space below… add the text on the black
   area."* This also kills the entire face-collision problem class.
2. **No em dashes** — in video captions OR IG captions. *"It makes it feel like it's edited by an
   AI."* Use commas, colons, or a `|` row break.
3. **Kinship words translate fully.** *"Who the fuck knows what Tau is?"* — nana/dada →
   grandfather, mama/tau/chacha → uncle. The English-caption rule has **no exceptions** for kinship.
4. **Editor slates are never content.** His on-tape "this is reel number one/two" lines mark segment
   boundaries for the editor. Cut them, always.
5. **No "follow for more."** Both the serif closing hold and the spoken stinger were rejected.
   Reels end on the last content line + ~1s of energy-checked air.
6. **Titles are viewer-facing hooks HE words.** Rejected: "How I convinced my parents" (*"no one
   gives a fuck about how I convinced my parents"*), "My ₹20 lakh mistake", "Too much pressure?".
   Accepted direction — relatable second-person stakes: "If you feel pressure, watch this video",
   "Middle-class kid? Leave your friends", "Be delusional." **Get his words, or wait for approval,
   before export.**
7. **Caption sizes at the §16i spec** — body **82** / hook **86** px, yell **1.5×**. The 68/76 @1.35×
   version read as *"font is not good"*. `fit_scale` caps width AND rows AND block height so 2 rows
   never sink under IG's UI line.
8. **Max TWO rows per caption.** Three rows reach his face — hard rule.

### Scan for wrap defects mechanically

Simulate the flex wrap over every group and flag (a) an accent chunk split across rows, (b) an
orphan short word alone on row 2. Fix with `|` breaks in the generator. **18 defects were found this
way on one pass.**

Caption groups that **accumulate past ~4 words hit 3 rows** with a 1.5em emphasis chunk — split into
swap-groups instead.

## Devices

- **Captions BUILD** chunk by chunk on the word, big, **two-tone** with the stressed word in the
  accent.
- **Colour register: talking head in colour, the past in black & white, blooming to colour on the
  payoff.** The cheapest strong device there is.
- **B-roll must LITERALLY illustrate the line being spoken** — not mood, not abstraction.
- Landscape b-roll goes in at native size (`broll-select`); never upscaled.

## The listicle variant

For ranked-list reels he approved the reel-02b shape (doc §17, reference `src/Reel02b/`):

1. **One stable frame** — card y236 1008×630, caption-only lane y886–1046, full-width face card
   y1066+ with the headroom fit. Never redivide it mid-reel; captions never touch his head.
2. **Card sequencing per item: list first (~1.5s, a new row slides in), THEN the evidence capture.**
   The list opens as locked numbered slots — names appear only when spoken. The CTA recap with
   verdicts is the screenshot frame.
3. **Phone-readable list type (~64px names).** Shrink ornaments, not names.
4. **No pill/chip shapes** — facts are editorial text lines on the scrim, verdicts are
   square-cornered stamps. One big keyword pill at the CTA is the only rounded element allowed.
5. **Evidence is real page captures** keyed to cues; bot-walled sites get a typographic quote card,
   never a mock (`screen-capture`).

**Collab vs solo:** a collab reel posted to both grids may carry the tools account's yellow. On a
**solo** personal-account listicle the structure stands but the accent tokens must be **re-asked** (default: the account blue /
white). The two grids must never converge.

## Traps proven on this format

1. **Anaphora blinds ASR on the render.** Beats that deliberately repeat the same opening phrase
   collapsed into a hallucination loop when the assembled cut was re-transcribed. **Verify anaphoric
   cuts per-part in isolation** (each part decodes clean alone) plus onsets-vs-words; the
   whole-render transcript is unusable evidence there. See `cut-audit`.
2. **Whisper-hi hallucinates loops on quiet Hinglish; the EN model decodes it.** Spans that came
   back as "आप आप आप" were real quiet English/Hinglish speech. **Probe suspicious spans with BOTH
   language-forced models** before calling them noise.
3. **30fps lifestyle b-roll needs motion-scored in-points.** Catalogue in-points land on still
   moments → frozen-frame FAILs. Score windows by min-frame-diff (sequential grey decode, argmax of
   the window minimum) and pick in-points from that.
4. **Motion-score the CROPPED region for square inserts.** One clip froze because the people move at
   the frame edges, outside the centre 1080 crop — full-frame score 4.13, crop-region truth: a dead
   board. **Score with the crop applied and pick `(in_point, crop_x)` jointly.**
5. **Bake inserts in ffmpeg** (pre-composited square-over-blur + B&W + fps conform) so Remotion plays
   ONE video per insert — no decode contention, and the register is verifiable pre-render.
6. **Never decode part AAC for the VO** — cut sample-exact from the camera PCM per part. Priming
   samples drift **+56 ms over 9 parts**.

## Related

`broll-select` · `cut-audit` · `caption-align` · `take-geometry` · `sfx-design`.
Full rulebook: `docs/personal-account-guidelines.md` (777 lines) and
`docs/hinglish-creator-edit-style.md`.
