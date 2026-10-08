# Edit Styles — how the cohort actually cuts these reels

> Saved 29 Jul 2026, provided by Nishant. Measured off actual files (12 top-converting reels,
> 16–29 Jul window; ffmpeg scene-cut counts, dominant-colour histograms, accent isolation,
> contact-sheet inspection). **This is the standing design guide for future reels.**
> Default for @nishantchahar.ai: **Style A spine, Style B typography** (§7).

**Method:** 12 top-converting reels from the 16–29 July window downloaded and analysed frame by frame
with ffmpeg — scene-cut counts, dominant-colour histograms, accent-colour isolation, and visual
inspection of 6-frame contact sheets per reel. Every hex value and cut rate below is **measured off
the actual files**, not estimated.

Written to be read by a video editing agent. Specs are given as percentages of frame height so they
survive any resolution.

---

## 0. The measurements

| Reel | Rate | Res | Cuts/sec | Dominant | Caption accent |
|---|---:|---|---:|---|---|
| sebintel | **10.37%** | 1080×1920 | 0.22 | `#F0F0F0` 23% (light) | `#F8F800` |
| justyn.ai | **8.42%** | 720×1280 | 0.33 | mixed / natural | none (boxed) |
| sebintel | 7.64% | 720×1280 | 0.27 | `#000000` 28% | `#F8F800` |
| sebintel | 5.47% | 720×1280 | **0.00** | `#000000` 54% | `#F8F800` |
| saraev | 4.79% | 720×1280 | 0.63 | `#000000` 34% / `#F0F0F0` 18% | `#F8D068` |
| saraev | 4.47% | 720×1280 | 0.47 | `#F0F0F0` 43% (light) | — |
| jasoncooperson | 3.95% | **1920×1080** | 0.11 | `#1860D8` 17% | `#F8E030` |
| theaisurfer | 3.87% | 720×1280 | 0.38 | `#000000` 17% | `#F8F850` |
| sferro21 | 3.72% (2.5M) | 720×1280 | 0.11 | `#181818` 27% | none |
| 100xengineers | 2.79% | 720×1280 | **0.68** | `#181818` 40% | white-on-box |
| sebastien | 1.86% | 720×1280 | 0.19 | `#000000` 53% | `#F8F800` |
| ashok | 1.70% | 720×1280 | 0.48 | `#1838C8` 17% | `#F0D840` |

### Three findings that contradict the obvious

**1. The best converters cut SLOWLY.** sebintel's 5.47% reel has **zero scene cuts** — one unbroken
16-second shot. His 10.37% reel cuts 0.22/sec. Meanwhile the fast cutters sit lower: 100xengineers
0.68/sec at 2.79%, saraev 0.63/sec at 4.79%.

Fast cutting is not what earns comments. **Holding one legible frame is.** Whatever your agent
defaults to, do not shred these into 0.5-second fragments.

**2. Pure yellow `#F8F800` is the cohort's caption colour**, and it's remarkably consistent —
sebintel uses the identical value across all three reels, and sebastien (same person, main account)
matches it exactly. theaisurfer softens it to `#F8F850`. This is effectively the platform-standard
"AI tools creator" caption.

**3. Royal blue `#1838C8`–`#1858D8` is the animated-explainer background**, arrived at independently
by ashok (57,805 px, his single most dominant colour) and jasoncooperson (4,605 px). If a segment is
flat 2D animation rather than screen capture, the cohort paints it royal blue.

---

## 1. Style A — Punchy Screen Demo `sebintel`
### The highest converter. Make this the default.

**Evidence: 10.37%, 7.64%, 5.47% — the top three conversion rates in the entire pull.**

**Screen division.** Mostly **no division — full-bleed single source.** One thing on screen at a
time, filling the frame. Screen recordings are **zoomed to ~250%** so UI text is legible on a phone;
when a capture won't fill vertically, it's centred on a plain background with grey/black bars rather
than stretched. Rounded corners ~1.5% of width, subtle white edge glow.

His 5.47% reel is the exception and it's worth copying: **two vertical panels side by side** in the
top 55%, each ~46% of width, labelled above in white bold sans (`Motion Graphics` / `Raw Video`),
with a text block filling the bottom 45%.

**Text.**
- Karaoke captions, **one to three words maximum per beat**. Never a full sentence.
- Heavy grotesque, ~900 weight. Inter Black, Helvetica Bold or SF Pro Display Bold all match.
- Fill `#F8F800`, black outline ~2–3% of cap height. The outline is mandatory — it's what keeps
  yellow legible over both a white browser UI and a dark terminal.
- Sentence case, **not** all caps.
- Vertical position **~45% of frame height** (measured median 45%). Dead centre, not the bottom
  third. This is deliberate: it sits over the screen content being discussed.
- Final CTA beat switches to **white** on the talking head.

**Colour.** The reel takes its palette from whatever is on screen, so it swings light (`#F0F0F0`
23% when demoing a browser) or dark (`#000000` 54% on a black backdrop). Only the yellow is fixed.
Talking-head segments are shot against neon/bokeh practicals.

**Aesthetic devices.**
- **Hand-drawn red circles** ringing the exact UI element being named. Rough marker texture, not a
  clean vector ellipse.
- Cold open on 2–3 seconds of unrelated cinematic footage (his 10.37% opens on a motorbike-and-
  explosion stock clip) purely to stop the scroll, then straight into the screen.
- Talking head appears **only at the end**, for the CTA.
- Zoom-and-hold rather than cut-and-move.

---

> Sound design for this style is specified in §9 — measured, and the default for `@nishantchahar.ai`.

## 2. Style B — Editorial Premium `nick_saraev`

**Evidence: 4.79% and 4.47%.**

**Screen division.** Alternates full-bleed talking head, full-bleed screen, and a **picture-in-
picture**: the app window floating upper-centre with the face in a rounded card (radius ~4% of width)
anchored bottom-centre at roughly 35% of frame height.

**Text — two independent layers, and this is the whole trick.**
1. **Emphasis words**: large **white serif italic**, a Didone — Playfair Display Italic is the closest
   free match. One or two words (`JUST`, `ANYTHING`, `completely`, `KEY AND`), ~9% of frame height,
   sitting ~37% down. This is the layer that makes his reels feel like a magazine rather than a tutorial.
2. **Running captions**: small plain white sans, bottom ~88%, no box, no outline.

Nobody else in the cohort runs a serif. It is his single most recognisable signature and it costs
nothing to adopt.

**Colour.** Deliberate high-contrast swing between near-black `#000000` (34%) and paper-white
`#F0F0F0` (18–43%). Screens are shown in **dark mode**; "canvas" beats are cream/off-white with a
faint palm-frond shadow gobo. Accent `#F8D068`, a muted gold rather than pure yellow. Talking head is
warm, low-key, single soft key from camera-left, background thrown well out of focus.

**Aesthetic devices.** Shallow depth of field throughout. Callout cards — a value in a rounded pill
on cream. Cream-paper texture with a moving shadow. No emoji anywhere.

---

## 3. Style C — Explainer Stack `sferro21`
### For anything where the visual is the payoff

**Evidence: 3.72% on 2,526,615 views — the biggest reel in the window.**

**Screen division.** A fixed, unchanging **horizontal split**: **top ~55% is the visual, bottom ~45%
is the talking head.** The face never moves and never goes full-frame. The top visual is a rounded
card (radius ~1.5% of width) with a soft white border, floating on near-black `#181818`.

That fixed frame is why it reads as a demo rather than a vlog. The viewer's eye never has to relocate.

**Text.** **Almost none.** No karaoke captions at all in the sampled frames. The visual plus voice
carries it. Occasional pill-shaped chips — rounded-full, thin white outline, white label — to name a
tool. If your agent auto-captions, **switch it off for this style.**

**Colour.** Charcoal-to-black `#181818` / `#000000` (53% combined) with a soft vignette. The demo card
supplies all the colour. Branded beats use a violet gradient. Talking head warm-lit against a dark
wooden headboard, shotgun mic deliberately in frame — the mic reads as "studio."

**Aesthetic devices.**
- **A thick tapered red brush-stroke**, hand-drawn, as the annotation. On the drone reel the stroke
  *is* the content — he draws the camera path and the AI follows it.
- Thin white arrows as secondary pointers.
- **Full-white flash-bloom transitions** between beats.
- Simple icon diagrams (camera icon, drone icon, connector lines) on flat black.
- Cuts at 0.11/sec — extremely slow. Long holds.

---

## 4. Style D — Clean Creator `justyn.ai`
### Best conversion among the six shortlisted accounts

**Evidence: 8.42%.**

**Screen division.** Full-bleed talking head, no split. Screens are shown by **filming the physical
device** — an iPad or laptop on a desk, shot with the camera — rather than a clean screen capture.
Slightly imperfect, and it reads as real.

**Text — three colour-coded card types. This is the cleanest system in the cohort and the easiest to
automate.**

| Card | Fill | Text | Position | Job |
|---|---|---|---|---|
| **Title** | white `#FFFFFF` | black bold sans | top ~8% | States the claim, persists ~4s |
| **Caption** | dark green, ~85% opacity | white, current word bright / upcoming dimmed | ~85% | Running karaoke |
| **CTA** | bright blue `#2D9CFF` | white bold | ~55% | The keyword ask |

Rounded rect radius ~2% of width, generous horizontal padding. Font is a rounded-ish semibold —
SF Pro Rounded or Poppins SemiBold.

**Colour.** No grade to speak of. Natural warm daylight, bright and airy, window and houseplant in
shot. Muted overall — the saturated colour is entirely in the three card types, which is why they
read as UI rather than decoration.

**Aesthetic devices.** Word-by-word karaoke highlight inside the box. Lavalier mic visible. One emoji
in the title card, never more. Zero transitions — straight cuts only.

---

## 5. Style E — Flat Animated Explainer `jasoncooperson` · `ashok`

**Evidence: 3.95% and 1.70%.**

Use only for a segment that has no screen to record — an abstract concept, a comparison, an
architecture diagram.

**Screen division.** Full-bleed animation. jasoncooperson's is **landscape 1920×1080** — a YouTube
edit reposted, and it still converted at 3.95%, which is worth knowing before anyone insists
everything must be shot vertical.

**Text.** White heavy **condensed** sans, all caps, short labels (`JUST`, `KEYFRAMES`). Small
relative to frame, ~4% of height. Placed against flat colour with nothing behind it.

**Colour — the most prescriptive palette here.**

```
background   #1858D8   royal blue (measured dominant)
cards        #FFFFFF   white, rough wobbly hand-drawn edges
accent 1     #F8E030   yellow  (suns, sparkles)
accent 2     #006048   green   (hills, ground)
accent 3     #F05028   orange-red (rockets, highlights)
accent 4     #7ED4F0   cyan    (bars, UI blocks)
```

**Aesthetic devices.** White cards with deliberately **rough, wobbly borders** — the imperfection is
the style. Flat silhouette figures. Icons inside torn-paper cards. Simple 2D translate/scale motion,
no easing showboating.

---

## 6. The verbatim restyle prompt from the 5.47% reel

sebintel's motion-graphics reel **printed its own production prompt on screen** in the bottom 45% of
the frame. Reconstructed from high-resolution frame crops — this is a real, working prompt from a
reel that converted at 5.47%, and it's directly reusable by your editing agent:

> Original voice, and original audio exactly the same. Important: keep me photorealistic and
> unchanged. Do not turn me into a cartoon. Do not turn me into a drawing. Do not turn the whole clip
> into an animated character.
>
> Restyle the whole clip as a bold mixed-media collage with a stop-motion feel. Cut me out as the main
> foreground subject, with a rough paper-cutout edge and a subtle white outline. Keep my hands and
> gestures fully visible and never covered.
>
> Replace the background with layered crumpled paper textures, torn newspaper scraps, halftone dots,
> coloured tape pieces, and bold flat paper shapes. Use a strong colour palette of blue, orange, deep
> navy, off-white, and small black accents. Keep blue and orange dominant throughout.
>
> Add energetic hand-drawn arrows, circles, scribbles, sticker-style graphic elements, rough collage
> shapes and tape accents around me, but never over my face or hands.
>
> **TEXT POP-UPS — STRICT. Read carefully.** Add EXACTLY these seven text pop-ups and nothing else, in
> this order, each appearing once, timed to when I say that phrase: "MOTION GRAPHICS", "AFTER EFFECTS",
> "PROFESSIONAL EDITORS", "3 AI TOOLS", "0 EDITING SKILLS", "COST ME", "FEW 100 DOLLARS".
>
> These seven are the ONLY text allowed to appear anywhere in the entire video. Do not transcribe my
> speech. Do not create captions or subtitles. Do not add any other words, labels, phrases, or
> pop-ups. If in doubt, show fewer pop-ups, never more.
>
> Make the seven pop-ups large, bold, high-contrast, and easy to read on a phone screen. Use blue,
> orange, off-white, and black for the text so it matches the palette.
>
> Use slightly choppy stop-motion energy, subtle camera shake, and light glitch texture, but keep my
> face and hair clear and readable. Do not add any other words. Do not cover my face or hands.

**Why it's worth studying beyond the aesthetic.** Two thirds of it is **negative constraints** — six
separate "do not" clauses about text alone. It names an exact pop-up count, an exact order, and an
explicit tie-break ("if in doubt, fewer, never more"). That's the actual lesson for driving an editing
agent: the palette is one line, the guardrails are twenty.

---

## 7. Recommended default for `@nishantchahar.ai`

**Style A spine, Style B typography.**

Style A because it holds the top three conversion rates and suits screen-recording tutorials, which
is what 14 of our 15 scripts are. Style B's serif-italic emphasis layer on top, because nobody else
in the cohort runs a serif and it differentiates the grid at zero production cost.

Concretely:

```yaml
canvas:      1080x1920, 30fps
cut_rate:    0.20–0.30 cuts/sec        # NOT faster. Best converters are slow.
screen_zoom: 200–260%                  # UI must be phone-legible
corners:     16px radius, 1px #FFFFFF at 20% opacity

captions:
  words_per_beat: 1–3                  # hard limit
  font:           Inter Black / SF Pro Display Bold
  size:           7.5% of frame height
  fill:           "#F8F800"
  stroke:         "#000000", 2.5% of cap height
  case:           sentence
  position_y:     45%                  # centre, over the content
  cta_beat_fill:  "#FFFFFF"

emphasis:                              # the differentiator — 2 or 3 per reel, max
  font:      Playfair Display Italic
  size:      9% of frame height
  fill:      "#FFFFFF"
  position_y: 37%

annotation:
  type:   hand-drawn marker circle
  color:  "#E82C1A"
  weight: 0.7% of frame width
  never:  over the face

talking_head:
  grade:     warm, low-key, single soft key camera-left
  dof:       shallow, background defocused
  placement: end of reel for the CTA, or bottom 45% if using Style C split

banned:
  - full-sentence captions
  - cuts faster than 0.4/sec
  - more than one emoji per reel
  - captions in the bottom third   # Instagram UI covers it
  - stretched (non-uniform) screen scaling
```

**Safe areas.** Keep all text between **12% and 82%** of frame height. Instagram's own UI — caption,
handle, action rail — eats the bottom ~18% and the top ~10%. Note that saraev and justyn both place
running captions at ~85%, which is *inside* that zone; they get away with it because those captions
are redundant to the voiceover. Anything load-bearing goes at 45%.

---

## 8. Style per script

| Scripts | Style | Reason |
|---|---|---|
| `13` `15` `17` `18` `21` `22` `24` | **A — Punchy Screen Demo** | Pure screen-recording tutorials |
| `11` `14` | **A + B** | Premiere and Codex reels need the editorial serif for authority |
| `12` | **B — Editorial Premium** | It's about writing craft; the serif carries the argument |
| `16` `19` | **C — Explainer Stack** | Visual output is the payoff, so fixed split, minimal captions |
| `20` `23` | **E for the diagram beat**, A elsewhere | Three-lane routing and agent loops need flat animation |
| `25` | **D — Clean Creator** | Format 2 confession. Natural light, no yellow, no CTA card |

**Script `19` gets the restyle prompt in §6 directly** — it's the same subject (motion graphics
without After Effects) as the reel that prompt came from.

---

## 9. Sound design — measured from a Style B reel, 13 Aug 2026

Measured off a 36.3s `nick_saraev`-register reel (Apple-design-skill, Claude). Everything here is
spectral evidence from the file, not a listen. **This is the spec for `@nishantchahar.ai`.**

### Master

`-14.4 LUFS` integrated, `-0.7 dBTP`, **LRA 2.3 LU** — crushed flat by a limiter, effectively mono
(side channel a uniform -29 dB down in every band, i.e. encode noise). Our existing `-14 LUFS`
loudnorm target already matches; what we don't currently do is limit hard enough to land at 2.3 LU.

### The bed

Continuous 0→30s. **Not beat-driven** — sub-band autocorrelation peaks at 0.19, so there is no kick
to cut against. Textural, sitting ~17 dB under the VO in the voice band.

- **No sidechain ducking.** Bed level differs by 1.9 dB between loud speech and silence — that's
  nothing. Set it quiet and leave it. Don't build a ducking curve.
- **The bed drops out for the CTA.** Sub runs +29→+35 dB all reel, falls to +25 at 30–33s and
  **+18.7 at 33–36s** — a 14 dB collapse as the CTA lands. No riser into it; the air band drops too.
  Emphasis by subtraction. This is the single highest-value move in the whole mix.

### The SFX layer

- **Score ~60% of cuts, not all.** 14 of 23 cuts carry a transient within 120ms. The other 40% run
  dry. This contradicts the "SFX on every cut" line in the Harman spec — that spec is for
  `@unscripted.nishant`; Style B is more restrained.
- **Land the attack ~2 frames after the cut**, not on it. Measured offsets ran +8 to +95ms, mean
  ≈ +60ms at 30fps.
- **Two-layer palette, roughly 2:3 bright-to-body.** Bright ticks and whooshes at 2.5–6.6 kHz
  centroid; body thumps at 1.0–2.1 kHz. Alternate them; don't repeat the same layer twice running.
- **A rapid cut burst gets ONE hit, not one per cut.** Five cuts between 32.0–32.7s share a single
  transient. Two cuts at 12.2–12.6s get none.
- **Front-load the hook.** Three transients inside the first 0.43s, against three cuts in the
  first 1.4s.

### Method caveats

Scene detection quantises to ±33ms at 30fps, so the +60ms offset is really "about two frames".
Transient detection cannot fully separate SFX from hard consonants — the palette figures come from
the 7 transients that fall inside speech gaps, where nothing masks them.

## 10. What I could not determine

Being explicit so nobody treats a guess as measured:

- **Exact fonts.** Identified by letterform inspection, not from embedded metadata, which rendered
  video does not carry. The named substitutes match closely; confirm against a frame before locking a
  template.
- **Stroke widths and radii** are estimated from 720p and 1080p frames, so they carry roughly ±0.5%
  error at frame-height scale.
- **Seam positions for split layouts** were measured by brightness discontinuity, which picks up
  content edges as well as layout boundaries. The 55/45 figure for Style C is from visual inspection
  of six frames and is approximate.
- **Audio** — analysed 13 Aug 2026, see §9. Still unknown: the **identity of the music track**
  (spectral analysis cannot name a piece — that needs the source post's audio attribution), and
  whether the SFX are stock library hits or bespoke. The bed's key reads as F# major but the
  measurement frames still carry voice bleed, so treat that as a search hint, not a fact.

## 11. Screen-content motion — the energy spec (added 26 Aug 2026)

Measured after a third remake of the same topic read as far more engaging than
ours, despite ours having correct type, real captures and a real audit. The gap
was not graphics quality.

**The diagnosis:** ours was a slideshow of correct cards; theirs was a
continuous screen-recorded walkthrough with a face attached. Their motion comes
from *inside* the recording — a page scrolling, a cursor travelling, a UI
animating — so something moves every frame even with no cut. Adding more cuts
does not fix this. Adding continuous on-screen motion does.

### The numbers

| | theirs | ours (before) | ours (after) |
|---|---|---:|---:|
| significant visual changes / sec | 0.31 | 0.09 | — |
| frames showing movement, per capture | 36–49% | **9 / 13 / 19%** | **37 / 37 / 38%** |
| length, same topic | 39.1s | 54.2s | 54.1s |

### The spec

1. **Motion floor: ≥30% of frames moving in every screen capture.** Gate it with
   `checkMotion()` in `capture_lib.mjs`. Below 25% = slideshow, rewrite the tour.
2. **Tours creep, they don't glide-and-hold.** One continuous scroll; holds
   ≤0.6s, only on the thing being named. `creep()`, never
   `glide()+waitForTimeout`.
3. **96px on-page pointer** (`addCursor`/`movePointer`). 64px vanishes once a
   1440px capture is downscaled into the 1000px card. Move it *with* the scroll,
   not between scrolls — don't `await` it.
4. **Zoom text-heavy captures 1.3–1.55** so body copy clears the phone-scale
   type floor, and **frame with `srcX/srcY`** — a centre crop clips the first
   character of every line on left-aligned pages.
5. **B-roll of a company's design = that company's own footage, moving.** A
   static homepage scroll is a still. YouTube is the route (their site usually
   has no capturable motion): find the longest sustained shots, crop to card
   aspect at native res.
6. **Registers hard-cut.** An opacity crossfade between registers shows the base
   cut through both layers.

### What we deliberately do NOT copy

- No circular face PIP — the house 60-40 split stays (Nishant, 26 Aug).
- No captions across his face; our safe-zone rule wins over their placement.
- Our captions stay display-sized. Theirs are small serif single words because
  their screen content is full-bleed; ours must carry the beat inside a card.

---

## 12. The text-hook lockup (saved 6 Sep 2026)

Nishant's saved reference: `assets/text-hook-refs/day3-invoice-generator-with-claude.jpg`
— *"I like this text hook style. Copy this for future videos."* A three-line
frame-one title for build/tutorial reels: series kicker, what today's build is,
which tool.

```yaml
lockup:                      # src/components/TextHook.tsx
  kicker:    "day 3 of building AI tools"   # Poppins 600, white, 0.44× headline px,
                                            # centred +7% W right of the headline
  headline:  "Invoice generator"            # Fraunces 900 (Recoleta stand-in), white,
                                            # 84px → a 17-char line spans ~67-70% W
  with_line: 'with' ✳ Claude                # Caveat 700 #F5D64A (0.62×) · ClaudeMark
                                            # #D97757 (1.05u) · Newsreader 500 #131313 (1.0×)
                                            # starts at frame centre, hangs off the right
  y:         300                            # top band, clear headroom; never on a face
  plate:     none                           # soft shadow over footage, none on flat grey
  motion:    kicker → headline → with-line, 6f apart, exponential bloom; lifts out
             when the body starts
  usage:     <TextHook at={12} kicker="…" headline="…" />   # brand={…} swaps the tool
```

Keep the running captions as a separate layer below it; this is the title, not
the caption. **The words are per script** (Nishant: "the hook will be different
depending upon the script") — the slots are context → the thing → the tool, and
each is optional (`kicker` omitted, `brand={null}`); only the type system and
the geometry are fixed.

---

## 13. The Tharun desk grammar (saved 14 Sep 2026)

Two reference reels he sent to "learn the editing style": a full-frame talking head that CUTS
(~0.5/s, hard punch-ins), graphics placed in the shot's own space (type behind the head via a
matte, numerals on his props, icon chips at the hand, cards sliding in behind him), 2-frame white
flashes and 1-invert+1-black blinks at every register change, accumulating word-by-word captions
with a hero word at ~1.7×, and ONE scoreboard MG that returns after every list item. Measured
spec: `docs/tharun-desk-edit-style.md`. Operating recipe: the `layered-head-edit` skill.
Reference files + 4 fps sheets: `assets/style-refs/tharun-desk/`.

---

## 14. The Paper Drawer — arena-skill grammar (saved 1 Oct 2026)

His own arena-skill reel, which he asked to have learned and named. One grid-paper world
(`#F1F1ED`, 72 px grid). The face card is a full-bleed drawer resting at seam y820 that slides
out of frame (10 f, easeInOutCubic) for 2.5–2.8 s full-page diagram beats roughly every 7 s, then
back. The face is on screen 62% of the time. A pixel mascot does every verb; Figma-style selection
boxes highlight the spoken word; lockups pair Inter Black caps with Instrument Serif italic.
Captions are white on a black pill centred on the seam, or plain black on paper. The reel opens
full-face and closes on a glass profile card over the blurred face. Measured spec:
`docs/paper-drawer-edit-style.md`. Operating recipe: the `paper-drawer-edit` skill. Reference
file + 4 fps sheets: `assets/style-refs/paper-drawer/`. Every style we have:
`docs/edit-styles-index.md`.

---

## 15. Whiteout — the find-skills grammar (saved 1 Oct 2026)

His own "find skills" reel, which he asked to have learned and named. Two full-frame registers:
his face, clean and uncut within a run (caption only), and one plain paper-white canvas
(`#F9F9F6` → `#DFDFDA`, no grid) that takes the WHOLE frame for 2.5–5.7 s to play one idea as
kinetic type and drawn UI. That's 8 visits in 51 s, 62% of the runtime. Paper enters by a
6–7-frame slide-over (from alternating sides) or a 3–6-frame dissolve, strictly alternating,
and always leaves by a hard cut. It shares the paper-drawer family's vocabulary: Figma-style
selection boxes, Inter Black + Instrument Serif lockups, plain captions that switch colour and
position per register, a comment → DM CTA, and the glass Follow card over the blurred face. The
recurring object here is a macOS blue folder rather than a mascot. Measured spec:
`docs/whiteout-edit-style.md`. Operating recipe: the `whiteout-edit` skill. Reference file + 6 fps
sheets: `assets/style-refs/whiteout/`. Every style we have: `docs/edit-styles-index.md`.
