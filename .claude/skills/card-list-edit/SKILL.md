---
name: card-list-edit
description: "The curated-resource listicle — a borrowed or self-shot hook clip sells a promise, a white flash cuts to a flat background, then 6–8 REAL YouTube result cards hard-cut past at ~1 second each. No voice-over, no captions, no talking head, no 60-40 split: music and cards only. Use when the reel recommends a LIST of external things (videos, channels, tools, books, accounts) rather than explaining something he says on camera — 'drop 8 videos', 'best X to learn Y', 'save this list', or when he points at the card-list reference reels."
---

# CARD-LIST EDIT — the resource listicle

> **THE JOB:** the *list* is the content. He is not on camera, nobody speaks, and there are no
> captions. A promise line, then 6–8 real cards, each held about a second, hard-cut.

> Full measured spec, with every hex value and band: **`docs/reel-styles-cardlist.md`**.
> Reference files: `assets/style-refs/cardlist/ref1–4.mp4`. Measurements: `work/cardlist-study/`.

## When this format is right

The reel recommends **external things the viewer should go get** — YouTube videos, channels,
tools, books, accounts. If he explains something *in his own voice*, this is the wrong format;
route back to `reel-edit` and pick `split-screen` or `caption-edit`.

## The shape

```
[ HOOK 24% ]  [ flash 5f ]  [ CARD 1 ][ CARD 2 ] … [ CARD 8 ]  ← ends here, no end card
  clip + 1 line                ~0.97 s each, single-frame hard cut
```

**Target ref4's proportions** — hook 24% of runtime, **8 cards**, 0.97 s mean hold. It is the
densest of the four references and the only one that lands 8 items in 10 seconds. ref1 fits 6
in 8.8 s and is the flattest; don't copy ref1.

## The five rules that make it read

1. **The swap is ONE frame.** Measured across a swap: `0.6 → 19.7 → 0.6`. No crossfade, no
   slide, no scale-in. Consistent with the standing register crossfades banned rule.
2. **The card breathes, the type does NOT.** Card scales **1.00 → 1.04 across the hold** about
   its centre, then **hard-resets at the cut**. The label's bbox is pixel-identical across every
   frame of its hold. Static type against a moving card is the entire trick — ref1 has no
   push-in and is visibly the deadest reference.
3. **Something is always moving.** Either the card push-in or an animated background layer
   (ref3 runs particles, measured 0.41/frame against 0.00 for the flat backgrounds). Never both
   still.
4. **Real cards, never mocked.** These are screen captures of real YouTube results — thumbnail,
   duration badge, avatar, 2-line title, `channel · views · age`, kebab. Mocked UI is banned
   (banned fake screen edit style), and every capture goes through `screen-capture` plus
   the screen recordings carry pii scan before it lands in a card.
5. **Number the labels.** `1. Public Speaking` … `8. Leadership`. The count is what creates the
   "what's number 8" pull that holds the loop. Unnumbered category labels (ref1) lose it.

## Geometry — build at 1080×1920

| Element | y band | notes |
|---|---|---|
| Hook promise line (1 line) | **324–393** | centred, heavy geometric sans |
| Hook promise line (2 lines) | **279–410** | |
| Hook clip band | **432–1482** | full-bleed width, letterboxed — *not* full frame |
| List label | **423–509** | static, centred |
| Card box | **603–1347**, x **87–1029** | width 935–970 (≈87% of frame) |
| Description line (ref1 variant) | 1367–1443 | optional, 2 lines under the card |

All inside the instagram safe area audit band (text within y230–1574).

## Palette

```
Yellow  #F5EC06   keyword highlight · trigger word
Green   #2EF905   numbered serif label
White   #FCFBFC   body type
Blue    #7EA8FF   card offset shadow — right + bottom edges ONLY, 15px, no blur
Black   #000000   list background
Olive   #443F33   list background, ref1 variant
```

The card shadow is a **hard offset**, not a border: measured 4548 accent px in the right columns
and 6387 in the bottom rows against 200 and 342 on the left and top.

## The flash

Hook → list is bridged by a white bloom. **Default: 5 frames (0.17 s), peak mean-brightness
≈ 110.** The 8-frame full-white version (peak 253, held 2 frames) belongs only on a hook that
has already been warm-graded into it. A plain hard cut (ref1) also works but wastes the beat.

## Sound — read this before cutting

**This format is nothing but music, and he adds music at posting.** That inverts the standing
*SFX only in edits* rule and it is the one thing to settle up front:

- Get the **track or the BPM from him first**, and lay the swaps on the beat; or
- cut to a **0.97 s / 29-frame grid** (clean at ~124 BPM) and hand him the BPM to match.

The references are only *loosely* locked — swaps land 13–130 ms off the nearest onset. A true
beat-snap is the clearest available upgrade over them. Deliver at **−14.1 LUFS, peak ≤ −1.9 dBTP**
per loudnorm measure the encoded file.

## Two standing rules this format breaks — surface both, don't decide alone

1. **No end card.** All four references stop dead on the last card; our follow end card rule
   says close on the 60-40 FollowCta split. The end card costs ~1.5 s of a 10 s reel and kills
   the loop. **Recommendation:** drop it here and carry the CTA as the persistent top line
   (`Follow & Comment "Wow"`, trigger word in yellow curly quotes) — which also feeds the
   dm pdf with every final asset.
2. **Sourcing.** The reference hooks are other creators' clips. The *cards* are the point of the
   format and thumbnails-as-recommendation is ordinary editorial use, but the hook clip is the
   soft spot — **a 2.5 s self-shot hook removes it for free** and is the default I'd propose.

## Pipeline for this format

Most of the standard pipeline does not apply — there is no take, no transcript, no captions.

```
0. ASSET PLAN   `asset-plan`      the list itself: every video verified live (title, channel,
                                     view count, duration) — fact check vo claims applies to
                                     the CARDS. His YES on the list before any capture.
1. CAPTURE      `screen-capture`  real YouTube results, PII scan, one card per item
2. HOOK         his own clip, or `broll-select`
3. STYLE        this skill + `mg-kit` (reuse before building)
4. SOUND        settle the track/BPM first — see above
5. RENDER       `render-ops`      −14.1 LUFS
6. REVIEW GATE  `reel-review`     never skip; Fable 5 vision pass
```

**Skip:** `shortform-cutaway`, `cut-audit`, `take-geometry`, `caption-align` — no spoken
take exists to cut, measure or align.
