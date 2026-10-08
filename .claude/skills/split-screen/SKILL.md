---
name: split-screen
description: "The signature 60-40 SPLIT-SCREEN reel format for the tools account — screen card on top, full-width face card below, a caption-only lane between. Carries the layout geometry and both variants (inset / full-bleed), the register grammar (hard cuts, the two sanctioned grow presets), MG density rules (3+ moving elements, furniture vs punch), the hook's first-5-seconds budget, stamps-not-pills, the Follow end card, and every layout rejection that produced them. Use for any 9:16 reel on the tools account that shows a screen, a tool, or a demo."
---

# SPLIT SCREEN — the house 9:16 format

> **THE FRAME IS STABLE; THE CARD CARRIES THE VARIETY.** The viewer's eyes never have to re-find
> his face. Novelty belongs in the card's *content*, never in the frame's architecture.

This was settled the hard way over three rounds on one reel:

| round | layout | verdict |
|---|---|---|
| v2 | novel carve-up (screen card + lane + narrow face column + side rail) | *"this division of space looks absolutely shit. don't ever use this."* |
| v3 | full-bleed alternating (face full-frame ⟷ evidence full-frame, hard cuts) | *"this is feeling clutter and the focus is shifting so frequently."* |
| **v4** | **the 60-40 split** | *"the 60-40 split looks much better."* **Shipped.** |

**Default to it.** Change only what the card SHOWS.

## Geometry

### Variant A — inset card (the classic)

```
CARD    x40  y100  1000×626        screen card, paper margin on 3 sides
LANE    y726 → y870                caption ONLY (~144–180px)
FACE    x36  y870  1008×1050       face card (or 1008×854 at y1066)
CONTENT_TOP  148 relative (y248 absolute)
```

### Variant B — full-bleed card (4 Sep 2026: *"I don't want the white border this time on top, left and right"*)

```
CARD_X 0 · CARD_TOP 0 · CARD_W 1080 · SHOT_H 726
LANE and FACE unchanged, so LANE_MID / CAPTION_Y still derive correctly
CONTENT_TOP becomes 248 ABSOLUTE (not 148)
```

With the card flush to y0, Instagram's username/Follow chrome lands **on** the card, so authored
card TEXT still starts below y240. Card **imagery** at y0 is fine. Any label bar moves to the
card's **bottom** edge — a top tab puts its text under IG chrome.

**The card frame must not animate on entry** in this variant. A `translateY`/`scale(0.96)` entrance
peels paper back into the corners — exactly the border he asked to remove. Put the slow lean on the
card's CONTENT and leave the frame rock solid.

`scripts/review_reel.py` takes `--card w:h:x:y`. Its motion crop defaults to the inset rectangle —
**pass `--card 1080:726:0:0` on the full-bleed variant** or it silently measures the wrong pixels.

### The safe band, and the lean that breaks it

Card **imagery** may span from y100; authored card **TEXT** must sit below y240.

`ScreenCard` drifts to `scale(1.025)` across each section, and a **centre-origin scale lifts
everything above the centre**:

```
y' = cardCentre + (y − cardCentre) × lean      // 413 + (240−413)×1.025 = 235.7
```

Content pinned at exactly 240 crosses the line **late in every beat**, by ~4px — invisible in a
mid-section still. **Pin at 248.** Do not "fix" it with `transformOrigin: 50% 0%`; that grows the
card downward into the caption lane.

**An external HTML asset needs a hard CLIP, not padding** — the asset scrolls its output upward and
drags text back through the band:

```css
.body{ position:absolute; left:0; right:0; top:152px; height:474px; overflow:hidden }
```

Delete the title-bar TEXT (traffic-light dots stay — chrome is furniture and may cross). Clipping
shortens the scroll window, so **add more real content** to keep the motion up.

Assert it: sample ~4 frames per section **including `frac 0.95`**, count bright pixels in
`g[168:238, 60:1020]`, and exclude sections whose card is a legitimately white screenshot.

## The lane is caption-only

The ~180px lane between the cards carries the **caption and nothing else**. A first pass that put a
source line, a chip AND the caption there rendered them on top of each other — the caption printed
straight through the chip.

Everything a shot wants to say goes **inside** the screen card as an overlay:
- `CardSource` — a strip across the card's top (site + date, repo + path) on a paper-to-transparent
  gradient; inverts to a dark wash over a dark-mode capture. Pads down by
  `CARD_TEXT_INSET = SAFE_TOP − SCREEN_Y + 10`.
- `CardStat` — the big number / pill across the card's foot on a transparent-to-paper gradient.

**Captions never touch his head** — the lane ends ≥20px above the face card. Text riding on the
hair line "looks bad" in any register.

## Register grammar

### Registers HARD CUT

**No opacity crossfade between registers, ever.** `SectionFade`-style wrappers cross-fade 5 frames
in / 4 out, so at every boundary the outgoing register is partly transparent, the incoming one too,
and **the base cut shows through both**. Three versions shipped with this before the cause was read
instead of guessed.

It survived several reels because it is *armed by content*: when adjacent registers are both paper
splits the fade blends identical paper. The moment they differ (dark terminal ↔ paper ↔ full capture
↔ full-frame face) every boundary flashes.

- Any register wrapper renders **opaque from its first frame to its last**.
- **When copying any pre-reel-35 `Final.tsx`, DELETE the SectionFade wrapper on sight** — same
  reflex as deleting `wave()`.
- In-beat STAGE swaps (site → terminal → score inside one card) also **replace, never blend**:
  unmount the old stage on an opaque background before the new one enters. A translucent veil leaves
  the previous stage's text ghosting through.
- Element ENTRANCES within a live register (springs, exp fades) are fine — they animate over their
  own register's background, not over another world.

**Cards must be opaque from frame one.** A `ScreenCard` opacity ramp of `Math.min(1, t*1.6)` with
`t = useEnter(0)` puts **one frame of bare paper at every register cut** — a flash the review gate
structurally cannot see, because it samples the boundary at +0.35s. `/watch`'s scene-change sampler
lands exactly on boundary frames, which is the only place this lives.

### No zoom at cuts (HARD RULE, twice-given)

> *"when there is zoom in and zoom outs between cuts, it looks bad, it shows that there is a cut.
> don't use this, i had asked you to add this to the memory earlier as well."*

- The base cut plays PLAIN: full-bleed `OffthreadVideo`, no scale/blur curves tied to segment
  boundaries. **Delete `wave()` wherever it is copied from.**
- **Do not inherit it from old reels.** Older `Final.tsx` files still contain it; copying "the latest
  shipped baseline" is how it came back. **The memory outranks the baseline code.**
- Slow drift NOT synchronised to cuts is fine. **The test: does anything change velocity on the
  exact frame of a cut?** Then it is banned.
- The one previously tolerated exception — an opening pull-back on the very first frame — was also
  dropped. Default to none.

### The two sanctioned transitions

Both are presets in `src/components/SplitToFull.tsx`. **Do not rebuild them.**

**split → full** (`useSplitToFull`):
```tsx
const t = useSplitToFull({ length, from: FACE_RECT, fromFit: FACE_FIT });
<div style={t.cardStyle}><OffthreadVideo style={t.innerStyle} … /></div>
```
1. **The un-zoom is not optional** — the card must land on *exactly* the next beat's full-frame
   framing or there is a visible pop. That is why it takes `fromFit`.
2. **Time the growth to LAND on the cut** so the next beat opens already full-bleed.
3. **Do not fade the paper out underneath it** — the growing card is what covers the paper; fading
   reveals the base footage through the card's edges.

**full → split** (`useFullToSplit`), `MOVE_START = sectionLength − MOVE_DUR`:
1. **What the shrinking card uncovers must be OPAQUE and already dressed** — kicker, title, rail
   already on it. Fading the screen card in underneath turned the whole top of the frame muddy grey
   for the length of the move.
2. **Full-frame display type must be GONE before the move starts** — the card's top edge travels
   down through the strip above his head, so his face rises into the words.

**The caption must clear the grow.** `CaptionLayer` is a single top-level layer and the `Split` is
what moves, so they are decoupled *by design* and **every grow drives the card up through a
stationary caption** unless something stops it. Seven frames of ink across his forehead and eyes
shipped this way.

```ts
const growOut = GROWS.has(reg.name)
  ? interpolate(frame, [reg.to - GROW_DUR - 2, reg.to - GROW_DUR + 4], [1, 0], {...})
  : 1;
const t = fadeIn(frame, cap.from, 6) * growOut;
if (t <= 0.01) return null;
```

Sample the grow window **every 4th frame** — `GROW_DUR` is only 16 frames and a mid-section sample
cannot see this class of bug at all.

Use the grow for **pacing** too: a 3s plain full-frame beat became ~1.5s by holding the split longer
and running the growth late, which is what killed a "this part looks plain" note.

## MG density

**Every section carries at least three moving elements, and the background is never truly static.**
A layer, not one hero graphic per beat. A correct cut with clean typography still reads "plain" —
this is the single most repeated rejection in the project.

### Furniture vs punch — the cue-gating rule

Splitting every card's elements is what fixes the "plain" note properly:

- **FURNITURE** — labels, list rows, chrome, counters. Lands at **section+2 to section+30**,
  regardless of the VO. (The gate samples at section+10, so at least half must be reading by then.)
- **PUNCH** — the tally, kicker, stamp or number that *answers* the spoken line. **Only this** is
  pinned to its word cue.

Five cards once shipped "plain" with 3+ elements each, because everything was cue-gated to
mid-section words and each card opened near-empty for 0.5–2s. **The register cuts at the section
boundary, so the viewer's eye arrives at frame 0.** Verify by sampling each section's FIRST second,
never its midpoint.

### Every register needs something moving on EVERY frame

The motion metric is mean luma difference over the card crop, so a 24px marker is invisible to it.
What carried one reel from 11–18% to 68–100%: a pulsing marker ring, a fill+sheen on the active
block, and a slow light sweep across the whole card on a 90f loop. See `screen-capture` for the
calibration table and the text-edge trick.

### The lane constraint

In the split, extra graphics go **inside the card**, in the **margin above it**, or **nowhere**.
A row of chips at y752 lands straight on the running caption.

- The hook's three chips become one in-card badge that swaps three times.
- A ladder graphic gets deleted when the card's own asset already animates it.
- A `−54%` ticker **replaces** the "by over half." caption in the lane rather than sitting under it
  — stronger than printing the words anyway.

**Ink graphics are invisible over video.** Anything in a full-frame face beat is white on a
translucent scrim, never the paper palette.

Build a per-reel kit of **frame-pure** primitives in `mg.tsx`, each taking `frame` as a **prop**
rather than calling `useCurrentFrame()`, so they compose inside `.map()` without breaking the Rules
of Hooks: `DotGrid` · `Rule` · `Chip` · `Ticker` · `Ring` / `Underline` · `Brackets` · `Bars` ·
`Marquee` · `Dots` · `Timer` · `OverStrip` · `Stack`.

## Stamps, not pills

> *"the pill design looks bad and is unreadable"* · *"the texts are overlapping the images"*

- Verdicts and labels are **solid rectangular stamps** — radius ~12, ink / red / green fill, white
  700-weight **≥34px** type. Never 999-radius pills.
- **A stamp gets its own clear band, structurally.** In a 1000×626 design card: imagery ends y≤510,
  stamps live y516–600, nothing behind them. In a Remotion screen card: a dedicated paper `ChipBand`
  (~92px, `#F1EFE9`, hairline top border) **below** the capture window — the capture shrinks, the
  text never floats on it. Docked bars attach to the capture's **bottom** edge (card-top is under IG
  chrome).
- **"Its own clear band" means STRUCTURAL, not a free corner.** Three stamps at
  `position:absolute; top:14px; right:26px` inside a *scrolling* terminal sat on the code they
  labelled as lines scrolled up under them — each read as clipped code for ~2.5s. **Make the label
  the block's own first row**, left-aligned above the code, with its height reserved in the layout.
- If a label is invisible in every sampled frame, **check stacking order** before assuming the cue
  is wrong — stamps placed as siblings *before* absolutely-positioned opaque panes never render.
- **No pill/chip shapes as design language.** Rounded-999 chips over b-roll "make it look AI
  generated and raw." Facts are editorial TEXT lines on a footer scrim.

## The hook — first 5 seconds

**A visual event every ~0.5s from 0 to 5s.** Budget one at least every 30 frames at 60fps. Viewers
decide to scroll inside the first seconds; a plain talking-head open loses them before the content
lands.

**The approved pattern — the split open:** open at **frame 0 already in the split** — b-roll or
capture playing in the screen card, his face lip-syncing in the face card, a brand lockup in-card
from the first beat ("add the logo at the start for credibility"), a stamp slam on the key VO word,
an in-card zoom bump, then the **card itself grows to full bleed** on the payoff word (never a hard
cut). ~8 events in 4s with the lane still caption-only.

**No bolted-on cold open.** Generated b-roll prepended as a standalone full-frame block before the
VO reads half-baked and was rejected — **hook b-roll belongs INSIDE the split card under the running
VO.**

**Withhold the payoff.** Density alone is not enough: skill/tool names and the finished "after"
result must not be legible in the first ~5s. Blur them (chip numbers crisp, names blurred). If
viewers can read the answer in the hook, they have no reason to watch.

An Omni restyle flip is a valid hook device but **buys exactly ONE event** — the rest of the density
still comes from Remotion. See `omni-restyle`.

## Type and lists

- On-screen lists must be **phone-readable first** — ~54–64px names. **Drop ornaments before
  dropping size.**
- Phone-scale floors: captions **≥78px**, in-card mono **≥36px**, display numbers are **150px**
  centrepieces. Graphics land ON the word, not seconds later.
- Name a tool with its **LOGO**, not just its name — reusable SVG marks in
  `src/components/Logos.tsx`, always paired with a wordmark. **A 40px mark in a corner chip is
  invisible on a phone**; when a brand is named in the VO, let the mark take the whole card, scrim
  the capture back, land the lockup centred at ~150px, and carry it into the next register so it
  gets seconds, not the half-second before the cut.
- Card content sequences **list → b-roll** per item: name the item big in the card, then the
  evidence takes it.

## The Follow end card (STANDING — every reel)

The closing "And don't forget to follow." line does **not** play as a full-frame talking head. It
becomes a 60-40 split: Follow→Following motion graphic on top (y0–768), face card below.

**Built — do not rebuild:** `src/components/FollowCta.tsx`. `<FollowCta startAt={f} />`, pinned so
the flip lands on the word (`startAt + 20` is the flip). Also registered as `FollowCtaSolo` for
transparent ProRes export.

- **Real numbers only** — his actual handle, posts, followers, following, and a real avatar crop.
  Never invent follower counts.
- **Tail air has a floor AND a ceiling: 0.5–0.9s of resolved "Following".** 1.05s read as "useless
  extra pause". Hit the band by moving the tap **earlier**, not by stretching the tail.
- **Check the source's last second BEFORE granting tail air.** On handheld takes the last thing he
  does is reach toward the camera to stop recording — a 1s tail once shipped him mid-reach. Sample
  the source after the final word, find where the reach starts to read, cap `TAIL_AIR` there.
- **Scale it into the card zone** — its inner card is 880px and self-centres, so at full size the
  handle and stats cross the x918 action rail. `transform: scale(0.85)` brings it to x166–914.
- **Headroom applies inside the cards too.** Compute the `objectPosition` crop, don't taste it:
  with the face band at source y600–1240 in a 1008px card, the scaled hair line is ≈560, so pick
  `crop = (560 − 120)/overflow` to land hair ~120px below the card top. One reel needed **58%** for
  the split card and **68%** for the follow card; the default 30% left ~370px of wall.

**He has had to ask for this twice.** It is part of finishing every reel.

## Related

`take-geometry` supplies `FACE_FIT` and the bands. `screen-capture` fills the card.
`caption-align` times the lane. `mg-kit` before building any new graphic. `sfx-design` and
`reel-review` close it out. Style reference: `docs/reel-edit-styles.md`.
