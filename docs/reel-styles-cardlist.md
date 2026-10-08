# Card-list reel — the measured spec

> Saved 9 Sep 2026. Learned from 4 reference reels Nishant supplied (`SaveClip.App_AQ*.mp4`,
> saved to `assets/style-refs/cardlist/ref1–4.mp4`). Every number below is **measured off the
> actual files** — per-frame RGB diffs, band decomposition, EBU R128, spectral-flux onsets —
> not estimated. Source measurements: `work/cardlist-study/`.

**What it is:** a curated-resource listicle. A borrowed hook clip sells a promise, a flash
cuts to a flat background, and then 6–8 **real YouTube cards** hard-cut past the viewer at
~1 second each. No voice-over. No captions. Music only.

**This is a new format for the repo.** It is not a variant of the 60-40 split — it shares
none of its parts. Route to it explicitly.

---

## 0. The measurements

| | ref1 | ref2 | ref3 | ref4 |
|---|---:|---:|---:|---:|
| Duration | 8.77 s | 12.28 s | 12.98 s | 10.38 s |
| Hook length | 2.90 s | 4.83 s | 3.73 s | 2.50 s |
| Hook as % of runtime | 33% | 39% | 29% | **24%** |
| Cards | 6 | 6 | 7 | **8** |
| Mean card hold | 0.95 s | 1.15 s | 1.20 s | 0.97 s |
| Hold range | 0.80–1.13 | 0.96–1.24 | 0.96–1.37 | 0.87–1.03 |
| Background | olive `#443F33` | `#000000` | `#000000` + particles | `#000000` |
| Label colour | white | white + yellow | — (CTA line) | green `#2EF905` |
| Card theme | YouTube **light** | YouTube dark | YouTube dark | YouTube dark |
| Card push-in | **none** | yes | (bg animated) | yes |
| Hook→list transition | hard cut | 5-frame flash | 8-frame white flash | 5-frame flash |
| Integrated loudness | −14.1 LUFS | −14.1 LUFS | −14.1 LUFS | −14.1 LUFS |
| LRA | 4.3 LU | 3.0 LU | 1.9 LU | 2.5 LU |
| True peak | −4.2 dBTP | −1.9 dBTP | −3.1 dBTP | −3.1 dBTP |

All four: 720×1280, 30 fps, H.264. Resolution is the download's, not the design's — build at
1080×1920 and every geometry below scales ×1.5 from the measured 720-wide values.

### Four findings that matter

**1. There are no scene cuts.** ffmpeg's scene detector at 0.25 returns **zero** cuts in all
four files. Every "cut" you feel is a *card swap on a static background* — the frame never
changes shot, only its contents. This is why the format is cheap to build and why it reads
as fast without being fast.

**2. The swap is a single-frame hard cut.** Frame-exact diff across a swap (ref4, f101):
baseline `0.6` → `19.7` → `0.6`. No crossfade, no slide, no scale-in. One frame.
This matches the house rule already on file — registers hard-cut, never crossfade.

**3. The card breathes; the type does not.** Within one hold the card grows
**w 613 → 631 px over 24 frames** (≈ **scale 1.00 → 1.04, +4%/s**), scaling about its centre,
then **resets hard at the next cut**. The label's bounding box over the same span is
*pixel-identical* (`y283-339 x170-547` at f102, f115 and f128). Static type, moving card —
that contrast is the whole trick. ref1 has no push-in at all and is visibly the flattest of
the four.

**4. It is music-led, and the cadence is only loosely locked to it.** No speech anywhere:
LRA 1.9–4.3 LU with zero silence gaps is a continuous compressed music bed. Card changes land
**13–130 ms** from the nearest spectral-flux onset (median ≈ 60–90 ms) — referenced to the
music, eyeballed rather than snapped. Tightening that to a true beat grid is the single
clearest upgrade available over the references.

---

## 1. Structure

```
[ HOOK 24–39% ]  [ flash 0–8f ]  [ CARD 1 ][ CARD 2 ] … [ CARD N ]  ← ends here
   borrowed clip                  ~1.0 s each, hard cut between
   + 1 promise line               static label + real YouTube card
```

**Aim for ref4's proportions**: hook 24%, 8 cards, 0.97 s mean hold. It is the densest of the
four and the only one that gets 8 items into 10 seconds.

**The reel ends on the last card.** No outro, no end card, no follow split. The CTA lives as
a *persistent top line* during the list (ref2, ref3) or is left to the IG caption (ref1, ref4).
→ **This contradicts our standing `follow-end-card` rule.** See §7.

---

## 2. The hook

| Element | Measured (720×1280) | Build at 1080×1920 |
|---|---|---|
| Promise line, 1 line | y 216–262 | y **324–393** |
| Promise line, 2 lines | y 186–273 | y **279–410** |
| Clip band top | y 288–313 | y **432–470** |
| Clip band bottom | y 963–988 | y **1445–1482** |
| Clip width | full-bleed 0–719 | full-bleed |

The clip sits in a **letterboxed mid band ~975 px tall** on black — it is *not* full-frame.
Roughly a third of the frame above it and a third below stay empty black. That dead space is
what makes the single type line read.

**Typography:** heavy geometric sans (Poppins / Montserrat Bold), centred, tight leading.
Two treatments seen:
- **Plain white**, stating a trade: `8 videos = 8 skills`, `6 videos = 6 skills`
- **Yellow keyword + white remainder**: `**Communication skill** is most important in every field…`

Both are *promises of a payoff*, never a description of the video. Keep to ≤ 8 words.

**The hook clip in all four refs is someone else's footage** — a stranger at a podium, a TEDx
speaker, a stock-looking desk shot. Nishant already shoots his own; a 2.5-second self-shot
hook removes the sourcing question entirely and is the one change I'd make by default. Flagged,
not decided — see §7.

---

## 3. The list register

| Element | Measured (720×1280) | Build at 1080×1920 |
|---|---|---|
| Label band | y 282–339 | y **423–509** |
| Label band (ref1 variant) | y 340–364 | y 510–546 |
| Card box | y 402–898, x 58–686 | y **603–1347**, x **87–1029** |
| Card width | 623–648 (86–90% of frame) | **935–970** |
| Description line 1 (ref1) | y 911–934 | y 1367–1401 |
| Description line 2 (ref1) | y 940–962 | y 1410–1443 |

Everything lands inside the `instagram-safe-area-audit` band (text within y230–1574 at 1080×1920).
The card bottom at y1347 clears it comfortably.

### The three label treatments

1. **Numbered green serif** (ref4) — `1. Public Speaking`, `2. Body Language`. High-contrast
   bold serif in `#2EF905` on black. The number does the counting so the viewer knows the
   list's length. **Best of the three** — it creates the "wait, what's number 8" pull.
2. **Category + description** (ref1) — bold white sans label *above* the card, plus a 2-line
   bold white sentence *below* it: `how to keep going without waiting for motivation`.
   Densest, most useful, slowest.
3. **Persistent CTA only** (ref2, ref3) — no per-card label; one fixed line at the top all
   the way through: `Follow & Comment "Wow"` / `Follow and Coment "Link"` with the trigger
   word in yellow inside curly quotes. (`Coment` is misspelled in the original — don't copy that.)

Treatments 1 and 3 can combine; ref4 leaves the CTA to the caption, which is why it fits 8 cards.

### The card

A **real YouTube result card**, not a mock. Thumbnail 16:9 with the duration badge bottom-right,
then the title row: circular channel avatar, 2-line title, `channel · views · age` metadata,
and the `⋮` kebab. Light theme in ref1, dark theme in the other three.

**Accent:** a hard offset drop-shadow in cornflower blue `#7EA8FF`, **10 px** (15 px at 1080),
on the **right and bottom edges only** — no blur, no top or left edge. Verified: 4548 accent
px in the right columns and 6387 in the bottom rows, against 200 and 342 on the left and top.

This is a screen capture of a real search result, not a rebuilt component — which puts it under
the house `screen-capture` rules and the `screen-recordings-carry-pii` scan.

---

## 4. Motion

| Layer | Behaviour |
|---|---|
| Card | scale **1.00 → 1.04** across the hold, about its centre; **hard reset** at each cut |
| Label | **completely static** — no drift, no fade, no pop |
| Background | flat and dead-still (ref1/2/4) **or** a subtle particle layer (ref3, measured diff 0.41/frame vs 0.00) |
| Cut | 1 frame, no crossfade |

Something must always be moving: either the card push-in or an animated background. ref1 has
neither and is the flattest reference of the four — don't copy ref1's stillness.

---

## 5. The flash transition

Hook → list is bridged by a short white bloom, measured as mean-frame-brightness:

- **ref3** (strongest): `136 → 157 → 173 → 206 → 253` (full white, held 2 frames) `→ 156 → 56`.
  8 frames, 0.27 s. Preceded by a warm orange wash over the last ~0.6 s of the hook.
- **ref2 / ref4** (lighter): peak ≈ 105–112, 5 frames, ≈ 0.17 s.
- **ref1**: none — a plain hard cut.

Use the 5-frame version by default; save the full-white 8-frame bloom for a hook that has
already been warm-graded into it.

---

## 6. Colour and sound

```
Yellow  #F5EC06   keyword highlight, trigger word
Green   #2EF905   numbered serif label
White   #FCFBFC   body type
Blue    #7EA8FF   card offset shadow (right + bottom, 10px@720 / 15px@1080)
Black   #000000   list background (3 of 4)
Olive   #443F33   list background (ref1 variant)
```

**Sound:** deliver at **−14.1 LUFS integrated, true peak ≤ −1.9 dBTP** — which is exactly
where our `loudnorm-measure-the-encoded-file` rule already puts every reel. Continuous music
bed, no VO, no SFX, no silence.

---

## 7. Two decisions this format forces

**1. It ends on the last card — our standing rule says close on the `FollowCta` split.**
All four references simply stop on the final card. Adding our end card costs ~1.5 s of a
10-second reel and breaks the "list ends, loop restarts" pull that makes these rewatch. My
recommendation: **drop the end card for this format only** and carry the CTA as the persistent
top line (ref2/ref3 treatment), which also feeds the trigger-word DM asset. Nishant's call.

**2. The whole format is music, and he adds music at posting.** Our standing rule is *SFX only
in edits — Nishant adds music when posting*. Here there is nothing but music: the ~1 s cadence
is the music's cadence. If I cut to a blind 1.0 s grid and he lays a 90 BPM track over it, the
swaps will drift against the beat. Either he names the track first, or I cut to a
**0.97 s (≈29-frame) grid** that divides cleanly at 124 BPM and hand him the BPM to match.

Also worth stating plainly: the references are built on other people's material — found hook
clips and other channels' thumbnails. Thumbnails-as-recommendation is ordinary editorial use
and the cards are the *point* of the format. The hook clip is the soft spot, and a self-shot
hook removes it for free.
