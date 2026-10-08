---
name: layered-head-edit
description: "Use when he asks for the Tharun look, 'those two desk reels', 'same editing language as the reference', or any 9:16 talking-head reel where the graphics should live IN the shot (type behind his head, labels on props, icons beside his hand, cards sliding in behind him) with flash-cut register changes and a scoreboard graphic that returns after every list item. Also when a full-frame talking head must CUT (punch-ins, second angle) rather than stay whole. Not for screen-demo reels that want the 60-40 split, and not for 'just captions'."
---

# LAYERED HEAD EDIT — the Tharun desk grammar

> **THE JOB:** the talking head stays full frame and everything lands *in his world* — behind his
> head, on the desk, beside his hand — punctuated by 2-frame flashes, with one scoreboard graphic
> that comes back after every list item. The frame changes size by hard cut, never by zoom.

**Two negotiations this skill closes, both from the no-skill baseline:**

- *"A named reference isn't automatically a layout brief, so I default to the house system."*
  When he says "same editing language" it **is** the layout brief. This skill is that brief.
- *"I can't sample the reels."* You can. They are at `assets/style-refs/tharun-desk/` with 4 fps
  dense sheets. Sample them before building (`sample-named-reference-first`). The measured
  evidence is `docs/tharun-desk-edit-style.md`; the numbers below come from it.

**Do not route this to `caption-edit`.** That format keeps the take whole and rides overlays in a
top band. This one cuts at ~0.5/s and puts graphics *in the shot*. Do not route it to
`split-screen` either: no card-above-face, no caption lane.

## The shape, in order

### 1. Base — full-frame head, hard-cut shot sizes

- One take, full frame, `objectFit: cover`. **Three crops, hard-cut on word edges:** base
  (face ≈ 40% of frame width, centre y ≈ 0.39 H), punch-in **1.35×**, and, if he shot one, a
  second angle. A punch-in is a cut to a fixed tighter crop, never a scale curve
  (`no-zoom-at-cuts`).
- Pace **0.45–0.55 cuts/s** (median shot 1.1–1.5 s). No hold longer than ~5 s without a
  graphic event. First 5 s: ≥1 cut and a type event every ~0.4 s — density comes from labels
  popping, not only from cuts (`hook-density-first-5-seconds`).
- Talking head on screen ~60% of the runtime; the rest is the registers below.

### 2. Graphics in the shot's space — four placements

| placement | how | reference |
|---|---|---|
| **behind the head** | person matte (MediaPipe selfie segmentation, feathered — the slice-reveal recipe) so the type sits between him and the room; his hair/shoulders occlude the letters, the letters never cover the face. Fallback: Omni behind-the-head v2v (`omni-behind-head-type`, ~$0.50/beat, his cost gate) | B "3 SKILLS", "CAPABLE YOU ARE", "FOCUS 10–14 HOURS"; A newspaper card, PROJECT cards |
| **on the props** | if he shot with counters (chips, cards, objects), light them in sequence and draw numerals above them on the "in order" line; the object he moves is the progress marker | A 25.5–28.5 |
| **beside the hand** | icon chips pop at the gesture on the spoken concept, one per noun, and stay | A 41–44, B 2.25, 18–19 |
| **cards sliding in behind him** | a card enters from the frame edge *behind* the matte, holds 1.5 s, exits on the next phrase | A 6.25 newspaper, 26–28 project cards |

**Face rule holds:** occluded-by-head is allowed, drawn-over-face is not. Run the alpha guard.

### 3. The accumulator — one scoreboard graphic, returns after every list item

Build ONE full-frame MG world for the list (A: purple 3D coin between glowing hands, the row of
earned coins beneath; B: a glowing node with satellites on a starfield). After each item:
white flash → the world → the new item spins/flies in and takes its label → the row/map shows
everything earned so far → hard cut back. **1.5–2.3 s per visit**, a slow dolly inside the
world, never static. This is the structural spine of a list reel in this format; without it the
reel is a caption edit with flashes.

### 4. The demo register (tools account) — grid paper, real recordings, neon stamps

Near-white paper (`#F7F7F7`) with a faint grey grid; a rounded dark device frame carrying a
**real** screen recording (`screen-capture`, ≥30% motion; mocked recordings banned); cards
**stack and slide** rather than cut; one **neon stamp per spoken word** under the card — black
condensed caps on a house-yellow `#F8F800` block, slight rotation, rectangular
(`stamps-not-pills`). Caption may ride inside the card's bottom edge on game demos.

### 5. Captions — accumulating lockups with a hero word

- **Voice:** heavy geometric grotesk (Inter/SF Pro Display Bold class), pure white, soft dark
  shadow, **no plate, no accent colour, no karaoke**. Sentence case, punctuation kept.
- **Size (1080×1920):** regular word em ≈ **110 px**; two-size lockup = small line ≈ 65 px over
  a **hero word ≈ 180–190 px** (~1.7×). Hero = the noun/number he lands on ("acquired",
  "complex", "weeks", the tool name).
- **Entry:** each word pops ON its onset and **stays**; the phrase accumulates ("you're" →
  "you're seriously" → "…missing out."); it clears on the next phrase's first word. Data shape:
  runs are phrases, words carry onsets, one optional `hero` flag per run.
- **Position:** chest band, centre **y ≈ 1300** on a desk shot (below the chin, above the desk
  edge); the top band when the shot is framed low; left of centre beside the gesturing hand on
  a few beats. Measure the bands per take (`take-geometry`) — the reference moves them.
- Personal-account variant (B): SF Pro Semibold class, em ≈ 60 px, 1–3 words replacing, centre
  y ≈ 1040.

### 6. Display voices

- **Grunge condensed caps** — eroded heavy condensed caps, white, cap height 175–255 px, with a
  33–38 px light-sans kicker ("Don't Ignore These / 3 SKILLS", "spend / 30 MINS / everyday").
  Titles sit above the head (centre y ≈ 270–430) and partly behind the hair. Numbers count up
  on the spoken numbers ("18" → "18 19" → "18 19 20").
- **Neon stamp** — "Comment" 64 px sans-bold + the trigger word 190 px condensed caps in curly
  quotes on the yellow block. Tools account only.
- **Neon caps on black** — an interstitial that builds one line per spoken word over ~1 s
  ("REAL BACKEND / and / DEPLOYMENT").
- **Label + curved arrow** — a hand-drawn arrow from a label to the thing it names (the photo,
  the person, the card).

### 7. Register punctuation — measured, at 30 fps

| device | spec | use |
|---|---|---|
| **white flash** | 2 frames `#FFFFFF` (optionally 1 half-white lead frame), then the new register hard | every face ↔ MG / demo boundary |
| **blink** | 1 frame **inverted** + 1 frame **black**, then the new register | on an emphasis word that ends a phrase ("simple logic", "till now") |
| **strobe** | after a flash, alternate red-multiply / normal every 2–3 frames for ~0.5 s with a ⚠️ + "PROBLEM"-class stamp | the one alarm beat |
| **wash → white** | desaturate to ~70% white over 3 frames, 1 white frame | the CTA landing |
| **smoke / cloud wipe** | the MG world's own cloud layer rolls over the face for ~0.4 s | entering the accumulator |

These are hard cuts with a punctuation frame — not crossfades (`register-crossfades-banned`).
**Every flash carries an SFX hit.**

**Budget — not every boundary is punctuated.** A punctuates 12 of its 41 cuts (≈ one per 7 s);
B about one per 8 s. The rule that falls out of the timestamps:

- **flash IN, plain cut OUT.** Every entry into the accumulator world is punctuated (white flash
  for the coin world, the smoke roll for the starfield); every return to the face is a plain hard
  cut. Demo cards enter and leave on plain cuts.
- punctuated as well: the hook's photo/paper cards, the blink on an emphasis word, the CTA wash,
  the alarm strobe, the end card.
- not punctuated: punch-ins, shot-size changes, card-to-card slides, the second angle.

Three punctuations per list item is the over-application the with-skill test produced; one per
item (the entry into the world) is the reference.

### 8. Hook recipe (0–5 s)

Open on the face already talking with the first caption word; the title/hero lockup lands at
~0.25 s behind the hair; a number counts up on the spoken numbers; icon chips pop at ~2.25 s;
first register cut at 3.4–4.4 s to the promise (the subject's photo with a label + arrow and a
selective-colour reveal, or the accumulator world). Withhold the list itself — names blurred or
absent until each is spoken.

### 9. CTA, share beat, close

- **CTA:** the neon "Comment "WORD"" stamp under the demo card and again on the face near the
  end (tools); or the wash-to-white + glowing grunge word on his chest (personal). Real trigger
  word, real doc.
- **Share beat (optional):** the reel shrinks into a phone DM composer typing the share line —
  the `cta-comment-composer` pattern in DM form.
- **Close:** the reference ends on a title card; the house ends on the **Follow close** — in this
  full-frame format it rides as the compact top-band strip over a ~0.4 s hold (`caption-edit`'s
  idiom), real numbers only. If the script ends on a "90 DAYS"-class line, the grunge title card
  can precede the strip.

### 10. Sound

SFX only — he adds the bed. But the grammar needs: a whoosh/impact on **every** flash and
blink, a pop per caption hero word and per icon chip, a slide on every card entry/exit, a click
on the Follow tap. Peak-aligned (`sfx-design`); target −14 LUFS, ≤ −1 dBTP on the encoded file.

## Account mapping

| | tools account | personal account |
|---|---|---|
| palette | A: white captions, house yellow stamps, purple MG world, grid-paper demos | B: white captions, grunge caps, dark starfield MG, red alarm, **no yellow** |
| conflict to surface | none | the locked personal-account doc (square card on black, captions in the black band) — quote the section and ask which wins before styling |

## Pipeline hooks

- **Asset plan** must list: the matte source (segmentation or Omni), which lines get
  behind-head type, the prop beats he shot, every real recording for the demo register, and the
  accumulator world's design. Get his yes.
- **Cut:** `shortform-cutaway` decides takes; this skill decides crops. Mark punch-ins on word
  edges in the cut data, not as scale curves.
- **Captions:** `caption-align` word onsets → phrase runs with `hero` flags; run the pause audit.
- **Review gate:** the alpha face guard must be told the blink's inverted frame is legal; the
  card-motion check runs on the accumulator visits (they dolly, so they pass); still-sample the
  2-frame flashes to prove they exist — scene sampling lands on them, mid-beat stills do not.

## Quick reference

| thing | number |
|---|---|
| cuts | 0.45–0.55 /s · median 1.1–1.5 s · max hold ~5 s |
| crops | base face 40% W · punch 1.35× · hard cut |
| caption | em 110 px · hero 180–190 px · centre y 1300 · white, no plate |
| grunge display | cap 175–255 px · kicker 33–38 px · above/behind the head |
| stamp | yellow block, black condensed caps · "Comment" 64 px + word 190 px |
| accumulator visit | 1.5–2.3 s · after every item · slow dolly |
| white flash | 2 frames · blink 1 invert + 1 black · strobe 2–3 f alternation ×0.5 s |
| punctuation budget | ≈ 1 per 7 s · flash IN to the MG world, plain cut OUT · demo cards plain |
| 50-50 stack (B) | card y 0–916 · head translated +500 px, not scaled · caption y ≈ 955 |
| talking head | ~60% of runtime |

## Common mistakes

- Routing to `caption-edit` because the take is locked-off. The reference cuts; so does this.
- Captions on an ink plate with an amber word, 3-word runs replacing each other. Wrong voice:
  white, no plate, accumulating, hero at 1.7×.
- Everything in a top band. Nothing is "beside him"; it is behind him, on the desk, at the hand.
- Register changes with no punctuation frame, or with a crossfade.
- Punctuating every boundary (three per list item). Flash in, cut out; ~1 per 7 s.
- No accumulator. A list reel here without the returning scoreboard is a caption edit.
- Animated zooms standing in for the punch-ins.
- A flash long enough to read as a white card (>3 frames), or a blink with the invert held.


## Build notes from the first reel in this format (reel60, 14–15 Sep 2026)

What the first build got wrong, and the numbers that fixed it — apply these before the first render.

- **Recentre before you punch.** His head is rarely on the frame's centre line (cx 468 on a 540
  frame). Base crop = the smallest scale that lets the head sit at x540 with no edge showing
  (`s ≥ 540 / HEAD_CX`, 1.16 on reel60), translate after the scale-about-the-chin. Punches on a
  handheld take must be **1.5×**: 1.12 and 1.2 vanished inside his own sway and read as "the head
  never cuts".
- **Type behind the head = MediaPipe selfie segmenter + a CSS mask, not a second video.** Model at
  `work/reel60/work/matte/selfie_segmenter.tflite` (250 KB, 8 ms/frame at 540×960); its single
  confidence mask IS person confidence. Write RGBA PNGs with alpha = background for the lockup
  windows only (391 frames = 13 MB), then `mask-image` the TYPE layer, `mask-size` = 1080k×1920k
  and `mask-position` = the transformed frame's top-left, so one video decode carries everything.
  Put the numeral band **in the hair line** (numeral bottom ≈ hair top + 60–120 px); above it the
  matte has nothing to hide, too low and the word is swallowed when he leans in.
- **Logo tiles are 240 px** (mark 140, name 48) and live in the **left column only**
  (x140; y430/720/1010): at 1.5× the face box spans x273–813, so a right-column tile either
  touches the ear or puts its name under the x918 rail. 130 px chips read as "tiny dots".
- **SFX = the house classics** (swish → transition on every flash, pop on stamps/tiles/coin
  landings, click on keystrokes and the Follow tap). Library one-shots (bubble pops, notifications,
  glitches, keyboard beds) were rejected as weird.
- **The world needs depth, not tiles.** Coins with rim lighting and a moving specular, a rotating
  light sweep, particles and a 0.10 dolly; the earned coin must settle **face-up** (end the spin on
  a multiple of 360°), fly with a ghost trail and land with a ring. Anchor the world caption's TOP
  under the slot labels (labels ≈ y1200–1245, caption top y1290, hero ≤ 110) or it lands on them.
- **The close is the house comment composer** (placeholder → typed trigger word → Post lights →
  presses → "✓ Posted") under the Follow strip, over a 90-frame hold with real room tone from the
  take's own gap (forward + reversed, −8 dB). A looped tone trips the false-start gate; digital
  zero is audible on headphones.
- **Demo cards slide, never fade**; the first card is on screen at frame 0 of the register.
- **Diff the render's `/watch` transcript against the captions before the vision pass** — a
  second read from the same ASR engine is not a second opinion (the hook line was wrong for five
  versions).

## Build notes from the Tercelet reel (reeltercelet-tharun, 27–28 Sep 2026) — his corrections

These override the defaults above wherever they conflict.

- **No grunge displacement on display type.** Anton + an feDisplacementMap erosion read as
  "wiggling text", and a count-up inside a centred row jittered the lockup sideways. Pick the
  display voice from the product/brand or the house pairings (Tercelet: its proof serif for numbers,
  Geist for words), lay every piece out at its final size from frame one, and only fade/scale in
  place. No bob on stamps.
- **Chips are glossy orbs, not labelled tiles.** White radial-shaded sphere, inner top highlight,
  soft white halo, solid black glyph, no label (the caption carries the word). Outline glyphs read
  weak at phone size. Never show a brand chip and a brand lockup at the same moment.
- **Brand lockups use the real mark and the real wordmark style** (the repo's icon.svg geometry,
  the site header's type), never the brand name set in the reel's display caps.
- **Punch size follows the face's share of the frame.** Face ≈55% of frame width → punch ≈1.15×
  effective (1.25 over a 1.09 base); 1.33× "zoomed him a lot". The 1.5× above was a wider take.
- **Check right edges against x918 after the world's dolly scale** — a 1.10 dolly pushed a coin
  label 51 px into the rail. Put the dolly origin right of centre or tighten the slots.

## Related

`docs/tharun-desk-edit-style.md` (evidence) · `asset-plan` · `take-geometry` · `screen-capture` ·
`caption-align` · `sfx-design` · `mg-kit` (check for a matte helper and the CTA composer before
building) · `reel-review`. Sibling formats: `split-screen`, `caption-edit`, `broll-style-edit`.
