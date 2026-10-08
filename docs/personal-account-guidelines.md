# Design Guidelines — @unscripted.nishant

**Status: v2, 11 Aug 2026.** This is the editing style the account uses from now on.
It supersedes the options in `EDITING-STYLES.md` §3 — that file stays as the *evidence*
(per-creator teardowns and the contact sheets they were measured from), this one is the *rule*.

> **What changed in v2, and why.** v1 was written from the Tarini/Visha/Chloe cohort and
> produced a reel (21) that Nishant rejected on sight: *"too fucking plain. No font change,
> nothing, how is this even an edit."* He then named **@hustlewithharman** (834k) as the
> reference to learn and copy. Three of his reels were measured on 11 Aug 2026 — cut
> timings by scene detection, audio by spectral analysis, type by frame sampling — and
> **§16 is the result. Where §16 conflicts with §6, §8, §9, §11 or §12, §16 wins.** The
> superseded rules are struck through in place rather than deleted, so the reasoning
> stays visible.
>
> **The cost of this change, stated once:** v1's whole purpose was separation from
> `@nishantchahar.ai`. Harman's language — dense phrase captions, coloured emphasis words,
> SFX on every cut — is *closer* to the `.ai` account than the bare cohort was. The
> separation now rests on **accent colour and register**, not on density: this account
> uses Unscripted Blue and real-life footage, the `.ai` account uses yellow and screen
> recordings. That is a thinner wall than v1 had. It is a deliberate trade.

Sister document: `../Nishant Chahar AI/DESIGN-GUIDELINES.md`. The two must never converge —
§11 lists the specific things that would make this grid look like the tools account.

Specs are percentages of **frame height** so they survive any resolution. Positions are the
**vertical centre** of the element unless stated.

---

## 1. What the cohort actually agrees on

Re-read off the contact sheets in `research/contact-sheets/`, not from memory:

| | Tarini | Visha | Chloe (vlog) | Chloe (deadpan) |
|---|---|---|---|---|
| Camera | Locked, waist-up, one corner | Handheld selfie, walking | Handheld, wide, scene-dense | Two locked angles |
| Subtitles | **None** — keyword accents only | **None** — one line per beat | **None** — one line per scene | **None** — one static premise |
| Type | Retro pixel numerals + yellow keywords | Small white **serif**, centred | Small white sans, centred | One sans premise, top |
| Light | Window, warm | Golden hour | Window, natural | Soft, graded |
| Signature | Peach everything + hex-swatch pills | The view *is* the payoff beat | Receipt screenshot cold open | The premise is the joke |

**Four rules every one of them follows, and we will too:**

1. **Nobody runs karaoke captions.** Word-by-word subtitles are the tell of a content farm —
   and they're the `.ai` account's look. One line per *beat*, never per word.
2. **Place-consistency replaces graphics-consistency.** Tarini's peach calendar wall appears in
   every frame of every reel. That single recurring backdrop does the brand-recognition work
   that a logo bug would do badly.
3. **The payoff is real and physical** — a sunrise, an outfit, a plate of food, a whiteboard.
   Never a screen recording.
4. **One typographic accent, owned completely.** Tarini pixel, Visha serif, Paritosh serif-italic.
   Pick one and never deviate. **Ours is monospace** — see §6.

**The one thing Tarini does that transfers directly:** her hex-swatch pills. She takes the
single most content-relevant data point (the colour of the outfit) and renders it as a small
labelled pill that animates in. Nishant's equivalent data point is **money and numbers** —
₹ figures, AED rents, LPA, day counts, application counts. That's §5b.

---

## 2. The house style, in one paragraph

> Two shooting modes, one type system. **The Corner** — locked camera in one recurring spot,
> for anything with numbers, lists or a receipt. **The Walk** — handheld front cam in Dubai,
> for anything that's a story or an opinion. Both are natural light, barely graded, cut slowly.
> Captions are small, white, sentence case, one line per beat, never over his face. Every number
> that matters gets a **blue monospace pill**; every number he can't share gets a **redaction
> bar**. Every reel ends on a held frame with its one extracted line in mono. No karaoke
> captions, no screen recordings, no stock B-roll, ever.

---

## 3. Mode A — The Corner

**Use for:** career utility, cost breakdowns, rankings, anything number-led, and concept reels
where the thinking is the payoff. ~55% of the calendar.

| | Spec |
|---|---|
| Camera | Phone on tripod, **locked**. Eye level, waist-up, subject on a third — not centred |
| Lens | Rear camera, 1× (never the ultra-wide — the front-cam distortion belongs to Mode B) |
| The constant | **One recurring corner**, chosen once and never changed. It must contain one object a returning viewer would recognise |
| Second angle | There is none. Punch in **≤ 1.2×** on the same take for the jump cut — free "B-cam" |
| Light | One window at 45° camera-left or -right. Never overhead ceiling light, never a ring light |
| Cuts | Jump cut **only on a point change**. 0.15–0.30 cuts/sec. Hold the punch line |
| Artifacts | Real documents held to camera — offer letter, invoice, dashboard, boarding pass. Shot in the same light, not a screenshot |
| Duration | 45–70s |

**The corner is a one-time decision with a long payoff.** Choose it at the first shoot and shoot
every Mode A reel there for at least a month. If the corner changes weekly, the recognition
effect — the whole reason this mode exists — never accrues.

---

## 4. Mode B — The Walk

**Use for:** stories, essays, opinions, Dubai reality, anything Template C or E. ~45%.

| | Spec |
|---|---|
| Camera | Front cam, handheld, arm's length. Walk **toward** the light |
| Structure | Talk 6–10s → cutaway to what he's actually looking at 2–4s → talk. The cutaway is the payoff beat, not filler |
| Cutaways | Shot in the same walk, same light. Skyline, metro, the building, the coffee, the gym door. **Never stock** |
| Light | Golden hour, or overcast. Midday Dubai sun is unusable — it blows the sky and squints him |
| Cuts | Scene-level, 0.10–0.20 cuts/sec. Takes run 5–8s. Cuts land on **location changes, not words** |
| Audio | Keep location sound under the voice. Wind, traffic, gym noise — the texture *is* the "unscripted" |
| Duration | 60–90s |

**Visha's device worth stealing outright:** the beat where his face leaves the frame entirely and
a single line of text sits over the view. One per reel, on the emotional turn. It's the cheapest
"this is a film, not a post" signal there is.

---

## 5. The three signature devices

These are what make a stranger recognise the account with the sound off. Two of the three appear
in every reel.

### 5a. The Corner
Covered in §3. The recurring backdrop is device number one and it costs nothing.

### 5b. The number pill

Tarini's hex swatch, money edition. **Every number that carries the argument gets one.**

```
shape      rounded-full
fill       #2D4BFF          (Unscripted Blue)
text       #FFFFFF, monospace, 600 weight, +2% letter-spacing
height     4.6% of frame height
padding    0.6 × pill height, left and right
position   upper third, y = 22%, aligned to the empty side of the frame
entrance   scale 92% → 100% over 120ms, ease-out. No bounce, no spin
max        2 on screen at once, ~4 per reel
```

Contents: `₹22 LPA` · `AED 4,200/mo` · `100 APPLICATIONS` · `DAY 47` · `2 YEARS` · `3:00 AM`.
Numerals and short labels only — a pill is never a sentence.

### 5c. The redaction bar

`BRAND.md` §6.2 says: when the number is private, say "I can't share the exact number" rather
than invent one. **Give that rule a visual.** When a real document is on screen, the private
figure is covered with a hard-edged black bar — `#111111`, no blur, no pixelation, corners
square, sized to the text it covers.

Blur says "edited". A hard bar says "redacted", which is the truth and reads as integrity.
This is the most ownable thing in the whole system because it comes from an actual constraint
nobody else in the cohort has.

### 5d. The closing hold (every reel)

The last 1.2 seconds: the frame holds, voice stops, room tone continues, and the reel's one
extracted line appears in **monospace, white, centred at y = 50%**, ~4% of frame height. Nothing
else on screen. No logo, no handle, no "follow for more".

`SCRIPTWRITING.md` already requires an aphorism closer in the VO — this is that line, rendered.
It's the sign-off ritual, and it doubles the share value because it's the frame people screenshot.

---

## 6. Type system (both modes)

**Two fonts, forever.** A neutral sans for what he *says*, monospace for what he *measured*.
The split is the whole idea: prose is human, numbers are data.

| Tier | Font | Size | Position | Rules |
|---|---|---|---|---|
| **Beat caption** | Inter Medium (500) — IG "Classic" and SF Pro Text are acceptable matches | 3.2% | y = **76%** default | One line, sentence case, ≤ 7 words, one per beat. White, drop shadow `0 2px 8px rgba(0,0,0,.45)`. **No box, no outline, no highlight** |
| **Punch caption** | Same, 700 | 6.5% | y = 50% | **One per reel, maximum.** The single hardest line. Never in the first 3 seconds |
| **Premise caption** | Same, 500 | 3.0% | top, y = **11%** | Mode A openers only. Up to 2 lines, persists 4–6s, then gone |
| **Pill text** | JetBrains Mono / SF Mono, 600 | 2.6% | inside pill | Uppercase permitted. Numerals only |
| **Closing line** | Same mono, 400 | 4.0% | y = 50% | §5d |

**Position rules that override the table:**
- Captions **never cross his face**. If y = 76% lands on his chin, move to y = 15%.
- When the bottom half of the frame holds the payoff (a plate, a view, a document), the caption
  flips to the top.
- All text lives between **12% and 80%** of frame height. Instagram's own UI eats the bottom
  ~18% and the top ~10%.
- Centred horizontally, always. No lower-left alignment, no drifting.

---

## 7. Colour

```
caption text    #FFFFFF   white + soft shadow. The only text colour for prose
accent          #2D4BFF   Unscripted Blue — pill fill ONLY, never as text colour
redaction       #111111   hard bar, square corners, no blur
```

**Three tokens. That's the entire palette.** Everything else on screen is the real world.

**Why blue, specifically.** The `.ai` account's caption colour is pure yellow `#F8F800`, and both
grids land in the same audience's feed. Blue is the furthest legible hue from it at thumbnail
size, so the two accounts stay visually separate at a glance. It's also complementary to Dubai
golden hour and to sand-and-glass interiors, which is where most of this footage gets shot — the
pill pops without a stroke.

**Accent used as fill only, never as text colour**, which permanently solves legibility: white
on a solid blue pill is readable over a bright sky and a dark room alike.

**Grade.** None to very light. Lift blacks slightly, keep skin warm, leave the sky where it is.
**Banned: teal-and-orange, heavy contrast LUTs, film-grain overlays, any "cinematic" preset.**
The seed accounts' entire sample has zero grade between them — ungraded is the genre signal.

---

## 8. Motion and transitions

- **Straight cuts only.** No whips, no zoom punches on every sentence, no flash frames, no
  glitch, no page curls.
- Punch-in on jump cuts, ≤ 1.2×, instant not animated.
- Text enters by fade, 100ms. Pills scale-in per §5b. Nothing rotates, nothing bounces.
- **Do not cut to the beat of the music.** Cut to the sense of the sentence. The measured finding
  from the `.ai` cohort holds here too: the best-converting reels cut *slowly*.

## 9. Audio

- Voice leads and always wins. Music bed sits well under it — if a line is ever hard to catch on
  phone speakers, the bed is too loud.
- Mode B keeps location sound audible. Mode A keeps room tone under the whole reel; **never cut
  to digital silence**, it makes jump cuts feel like errors.
- Music: ambient, warm, no vocals, no drop-and-build EDM structure. Trending audio **only** when
  the format is explicitly a trend riff.
- Mic close on both modes. Room echo is the one production flaw that reads as amateur rather
  than as authentic.

## 10. Covers and the grid

- **The cover is a frame from the reel.** No designed thumbnail, no headline text over his face.
- Pick a frame where he's looking at the lens, or the reel's best real image (the view, the
  artifact, the plate).
- **No cover text at all.** The grid should read as a person's life, not a media brand's
  channel. This is the single clearest visual difference from `@nishantchahar.ai`, where cover
  text is doing retrieval work for tutorials.
- Consequence to accept: reels are harder to find by scanning the grid. That's the trade, and
  for a 105K personal account it's the right one.

## 11. Banned

Hard list. Any one of these breaks the account's look:

1. Karaoke / word-by-word captions
2. Screen recordings of any kind — that's the `.ai` account's language
3. Stock B-roll, ever
4. Yellow caption text (the `.ai` account owns it)
5. Teal-orange grades, film grain, "cinematic" LUTs
6. Cover text, logo bugs, animated handles, subscribe stingers
7. Cuts faster than 0.4/sec
8. Text in the bottom 18% or top 10% (Instagram covers it)
9. More than one emoji in a reel
10. Blurring a private number instead of redacting it (§5c)
11. Ring lights and overhead ceiling light
12. A different corner every week

---

## 12. Editor spec block

Paste this to a human editor or an editing agent. Written as constraints because, per the `.ai`
account's finding, guardrails are what actually control an edit — the palette is one line, the
"do nots" are twenty.

```yaml
delivery:      1080x1920 H.264, ~18 Mbps, 30fps
capture:       4K 9:16, 30fps (60 only if slow-mo B-roll is planned)
grade:         none-to-light. lift blacks +3. warm skin. NO teal-orange, NO LUT, NO grain

captions:
  style:       one line per beat, NOT per word
  font:        Inter Medium
  size:        3.2% of frame height
  fill:        "#FFFFFF"
  shadow:      0 2px 8px rgba(0,0,0,0.45)
  box:         none
  case:        sentence
  position_y:  76%          # flip to 15% if it crosses his face or covers the payoff
  max_words:   7
  punch:       1 per reel max, 6.5%, y=50%, never in first 3s

pill:                        # every number that carries the argument
  fill:        "#2D4BFF"
  text:        "#FFFFFF", JetBrains Mono 600, +2% tracking
  height:      4.6% of frame height
  position_y:  22%
  entrance:    scale 92->100% over 120ms ease-out
  max_onscreen: 2

redaction:
  fill:        "#111111"
  edges:       hard, square corners
  never:       blur or pixelate

closing_hold:
  duration:    1.2s
  text:        the reel's extracted line, JetBrains Mono 400, 4%, y=50%, white
  audio:       room tone continues, voice stops
  contains:    nothing else. no logo, no handle, no CTA card

cuts:
  mode_a:      0.15-0.30/sec, jump cuts on point changes, punch-in <=1.2x
  mode_b:      0.10-0.20/sec, scene-level, cut on location change
  transitions: straight cuts only

banned:
  - karaoke captions
  - screen recordings
  - stock b-roll
  - yellow caption text
  - beat-synced cutting
  - cover text / logo bug / subscribe stinger
  - text below 82% or above 12% of frame height
```

---

## 13. Style per script

Modes follow each script's own F-tag. Devices are the ones that reel should carry.

| Script | Mode | Devices |
|---|---|---|
| `01` safest job in India | **B** — Walk | Closing hold. Face-leaves-frame beat on the turn |
| `02` certificates part 2 | **A** — Corner | Pills on each certificate's real cost. Premise caption |
| `03` LPA is not your salary | **A** — Corner | **Pill-led** — the whole reel is a number teardown |
| `04` resume walkthrough trap | **A** — Corner | Real resume to camera + **redaction** on personal details |
| `05` Dubai cost per month | **A** — Corner, Mode B cutaways | Pills per line item. The shock item gets the punch caption |
| `06` promotion season | **B** — Walk | Closing hold carries the concept |
| `07` moved to Dubai playbook | **A** — Corner | Real documents, redaction on Emirates ID / permit numbers |
| `08` sold and felt nothing | **A** — Corner | **Redaction is the reel** — the acquisition figure he can't share |
| `09` tax-free salary myth | **A** — Corner | Pills on both sides of the comparison |
| `10` nobody is watching | **B** — Walk | Face-leaves-frame on the spotlight-effect beat |
| `11` Dubai honest verdict | **B** — Walk | Cutaways do the arguing. One punch caption on the verdict |
| `12` resume mistakes | **A** — Corner | `100 APPLICATIONS` pill. Redaction on any real resume shown |
| `13` cancelled Bangalore subscription | **B** — Walk | ₹ pills on the comparison |
| `14` trip in 30 minutes | **B** — Walk, on the real trip | Pills on costs and timings |
| `15` day one again | **B** — Walk to the gym | Closing hold |
| `16` quitting felt like losing twice | **B** — Walk | Longest face-leaves-frame beat of the month |
| `17` negotiating my own offers | **A** — Corner | Redaction on offer letters. Pills on the deltas |
| `18` Dubai room story | **B** — Walk | Shot week-of. Cutaways from the actual event |
| `19` two things at once | **A** — Corner | Closing hold |
| `20` thirty days recap | **A** — Corner | Real dashboard on screen, pills on the headline numbers |
| `21` family trajectory | **B** — Walk | No pills. Closing hold only — this one stays bare |
| `22` one lakh benchmark | **B** — Walk | One pill: `₹1,00,000`. Nothing else |

Rule of thumb for anything new: **numbers → Corner, feelings → Walk.**

---

## 14. Shoot-day protocol

1. **Batch by mode, not by post.** One Corner session shoots 3–4 utility reels back to back;
   the framing and light are already set, so reel four costs twenty minutes.
2. **Walk reels are shot when the light is right**, not when the calendar says. Golden hour in
   Dubai is the constraint — a Walk reel scheduled for midday gets rescheduled, not shot badly.
3. **Collect the artifacts before the corner is lit.** Offer letters, invoices, dashboards,
   documents. Redactions are decided on the shoot, not in the edit.
4. **Room tone, 15 seconds, every session.** It's what makes the closing hold work.
5. **Shoot the closing hold as a separate 3-second take** — face still, no talking, looking at
   the lens. It's easier than trying to find a still frame in the edit.

## 15. What is deliberately not decided, and the review date

Being explicit so nobody treats a choice as measured fact:

- **The corner itself.** It has to be picked in his actual Dubai flat — I haven't seen the room.
  Pick it at the first shoot; the only requirement is one recognisable object in frame and a
  window off-axis.
- **Blue is locked, the exact hex is not sacred.** If `#2D4BFF` fights something permanent in the
  corner, shift within the blue family. Do not move to another hue — the separation from the
  `.ai` yellow is the whole reason.
- **Fonts** are chosen for availability and letterform, not measured off the seed reels; rendered
  video carries no font metadata. Inter and JetBrains Mono are both free and both in CapCut.
- **Audio levels** are given as relationships, not numbers. Nobody analysed the cohort's mix.
- **Review after two weeks of posting** — roughly 26 Aug. What gets checked: whether the pill is
  earning attention or reading as decoration, and whether the closing hold shows up in the
  retention graph as a re-watch.


---

## 16. Editing style — the @hustlewithharman reference (v2, supersedes §6/§8/§9/§11/§12)

Measured 11 Aug 2026 off three of his reels (57s, 100s, 79s), not recalled from memory.
Method: `ffmpeg` scene detection for cut timings, FFT band analysis for the audio bed and
transients, frame sampling at 0.4s for the type.

### 16a. What the numbers actually are

| | h1 (57s) | h2 (100s) | h3 (79s) | v1 said | **v2 rule** |
|---|---|---|---|---|---|
| Cuts/sec | **1.08** | **1.06** | **0.76** | 0.15–0.30, ban >0.4 | **0.75–1.10** |
| Median shot | **0.93s** | **0.94s** | **1.32s** | — | **0.9–1.3s, nothing over ~2s** |
| Cuts in first 5s | 6 | 3 | 3 | — | **≥3, ideally 5–6** |
| Cuts carrying an SFX | — | — | — | SFX unspecified | **~1 in 4 (see 16d)** |
| Music bed | continuous | continuous | continuous | "well under voice" | continuous (added at posting) |
| Frames below −50 dB | **0.0%** | **0.0%** | **0.0%** | — | never reach silence |

> **The cut-rate row was corrected on the second pass (11 Aug, afternoon).** The first pass
> put these at 0.52 / 0.52 / 0.36 and set the rule at 0.40–0.55. That was measured with a
> scene-detection threshold high enough to miss cuts *between visually similar setups* — two
> gym angles, two bathroom angles — which is most of what this style is made of.
>
> Re-measured at `select='gt(scene,0.28)'` and then **checked by hand**: sampling h1's first
> six seconds at 2fps and counting distinct setups by eye gives 7–8 shots in 6s ≈ 1.2/sec.
> The manual count is the ground truth and it matches the 0.28 threshold, not the earlier one.
> **The old rule was half the real pace**, which is exactly the failure v1 had. If a future
> pass disagrees again, settle it by counting frames by hand, not by re-running a detector.

Dynamic range across all three was 15.5–17.5 dB. A voice-only mix with real pauses measures
30 dB+. That is the proof the bed never stops — as does the 0.0% row above.

### 16a-ii. Text goes in the shot's empty space — but consistently

Three notes from Nishant on 11 Aug, which pull against each other and all three must hold:

1. *"Using the empty space in the video as text spaces, we did the exact opposite."* In the
   reference the text sits wherever **that shot** is empty: he is crouched bottom-left, text
   goes middle-right; he is lying at the bottom, text goes top.
2. *"Captions are not consistent, they are very discontinuous and it's distracting."* Most of
   the reference sits at ONE position (~y20–24%) and departs only when a shot cannot carry it.
3. Captions **build** — lines accumulate through a thought, then clear. A caption replaced
   wholesale on every cut flickers.

Resolution, in priority order:

```
1. group captions by SENTENCE, not by shot        -> continuity, lines accumulate
2. one position per group, default y = 22%        -> consistency
3. move a group only when the picture forbids it  -> the empty-space rule
4. never place text on a face — this outranks 1-3
```

`work/reel21/cut/place_captions.py` implements it: it reconstructs the picture under each
group, scores candidate boxes for brightness / clipped highlights / detail, applies a
**capped** bias toward the shared default, and vetoes boxes that land on a face.

**Keep the bias capped.** On reel 21 an uncapped consistency bias moved a caption to y900 on
the family shot — directly across his parents' faces. Consistency must never outrank the face
rule. If one group still cannot find a box, that is the signal to **split the group** or
**change the clip**, not to force it: the second walk shot scored 282 (illegible white on a
bright road) and the fix was replacing it, not repositioning the text.

### 16b. The structure: anchor + inserts

Every reel is one recurring **anchor** shot — him at the mic, warm practical lights behind,
in colour — that he cuts back to repeatedly, interleaved with short **inserts**:

- real objects and actions (coffee being poured, socks going on, a watch, a car key)
- **black-and-white** self b-roll (desk, bed, gym, sofa) — B&W is used as a *register*,
  the anchor stays colour
- location changes, one per insert
- occasionally a cinematic narrative shot illustrating the story being told

The anchor is what §3's "Corner" was reaching for. The inserts are what v1 was missing
entirely, and they are the reason his cut rate is achievable at all: **you cannot cut at
0.5/sec without shots to cut to.** Shot count is the real constraint on this style.

### 16c. The caption system — three type registers on one stack

This is the single biggest miss in v1, and the thing Nishant reacted to. Harman runs
**three** registers inside one caption, swapping every 0.4–0.6s:

```
emphasis    bold sans, ALL CAPS, ACCENT COLOUR      -> the one word that carries the line
lyrical     italic serif, white                     -> soft/among/connective words
body        bold sans, white                        -> everything else
position    lower third, y = 70-78%, centred
build       the stack GROWS word-group by word-group, then clears and restarts
shadow      heavy - roughly 0 2px 10px rgba(0,0,0,.62)
```

His accent is cyan in one reel, yellow in another. **Ours is the blue family** — that is the
separation from the `.ai` account's `#F8F800`, and it is not negotiable.

> **Open, for Nishant.** `#2D4BFF` itself fails as a *caption* colour on his indoor footage:
> A/B'd at frame 946 of reel 22, the true brand blue goes dark and muddy against the dim
> hallway and nearly disappears, while `#3BE0FF` reads cleanly. Reel 22 v2 ships with
> **`#3BE0FF`** — same hue family, nothing like yellow, so the separation still holds.
> `#2D4BFF` stays the **pill fill**, where a dark solid is exactly right. Say the word and
> I'll swap the captions back.

> **Reel 21's verdict on the same question (11 Aug, later the same day).** A solid
> `#2D4BFF` highlight *box* behind the emphasis word was rejected on sight ("the blue
> accent is not looking good"). What replaced it — and what matched the reference on
> re-inspection — is **no colour at all**: the emphasis device is a **large white italic
> serif (~1.6em) sharing the baseline** with the sans, exactly Harman's "faint"/"pehle".
> Between the two experiments: coloured *boxes* are dead; coloured *text* (reel 22's
> `#3BE0FF`) is still live pending his review. On emotional reels, default to the white
> serif and no accent colour.

**Caption density — the reel 21 corrections, all three from Nishant directly:**

1. **ONE phrase on screen at a time, 3–4 words maximum.** Never a stacked build of 2–3
   lines. The reference never shows more than one short phrase, and the serif hero words
   need the room. Phrases replace each other word-timed, every 0.5–1.5s.
2. **Leave clear air between the caption and his head** — reel 21 ships with ~95px. A
   caption that hugs the hairline reads as a mistake even when it doesn't touch.
3. **Watch for double spaces** around markup boundaries — collapse whitespace before
   tokenising. ("I won't say  it's easy" shipped in a QA still.)

~~§6's "Beat caption: one line per beat, white, no box, y=76%"~~ — superseded. One line per
beat is too slow and too plain; it reads as subtitles, not as an edit. **Keep** the ban on
true karaoke (one word at a time with a bouncing highlight); word-timed single phrases are
not that.

~~§11.1 "no karaoke captions"~~ — narrowed to: no per-word highlight animation. Phrase
builds at 0.4–0.6s are correct.

### 16c-ii. The mix: white / yellow / serif — MEASURED off the reference

Harman emphasises with typography **and** colour together. The ink was measured by
isolating glyph-edge pixels across the first 12s of three reels — bright, saturated, and
bordered by much darker pixels, which excludes skin and lamps:

```
dominant ink   #F6F606   essentially pure yellow   <- the one to use
secondary      #12DEF6   cyan, used more sparingly
```

**Yellow is the accent.** An earlier pass guessed cyan `#3BE0FF`; Nishant corrected it
("blue is not the colour, yellow is the best suited") and the measurement backs him.

> **This collides with `@nishantchahar.ai`, knowingly.** §7 called `#F8F800` the wall
> between the two grids. Nishant chose the same yellow for this account on 11 Aug anyway.
> The grids now separate on **footage and register** — real life vs screen recordings,
> serif-and-yellow phrases vs the `.ai` caption stack — not on hue. Revisit if the two
> start reading as one account in the feed.

**Four registers, no boxes ever:**

```
body      Inter 700, WHITE, 3.4%                  everything ordinary
keyword   Inter 700, YELLOW #F6F606, 3.4%         ordinary concrete noun
HERO      Inter 800, YELLOW, 1.5em (~5.1%)        bigger AND coloured AND heavier —
                                                  all three at once. The kinship words,
                                                  the hook's payoff word, "Microsoft"
emotional Instrument Serif italic, WHITE, 1.6em   the felt word: trajectory, brag, heavy
```

The hero register exists because Nishant asked for it directly on the kinship beat: *"the
font and colour both should be there, it needs to be highlighted by not just colour and as
we are emphasising on it, it should have a bigger font size too."*

**The hook needs SCALE CONTRAST, not five same-size lines.** The reference opens small-then-
LARGE ("3 mahine" + big "pehle"). Reel 21's first 5s was five identical lines and read flat;
it now runs three small phrases into a large yellow hero word.

### 16c-iv. Never put text on a face — including in the b-roll

Nishant, 11 Aug: *"in the brolls also check the empty space and add the texts there and not
on faces."* Pixel scoring alone will not catch this: a face is often the darkest, calmest
region in frame, so a brightness scorer actively prefers it.

Measure a **face band per clip** and treat it as a hard veto, not a penalty:

1. Haar frontal + profile cascades over ~10 sampled frames per clip.
2. **Cluster the hits temporally** — a real face recurs in a consistent row band; noise
   scatters. Require presence in ≥34% of sampled frames and reject any band over 1400px.
   Raw min/max across detections is useless: it reported ten faces in the highway sky.
3. **Hand-measure the clips the detector misses** — profile shots and anyone looking down.
   That is most contemplative b-roll.
4. On the anchor take, scale the band with the punch-in.

Getting this wrong is not theoretical: the window shot's face band was recorded as y620–870
when it is actually **y830–1060**, and the caption sat on his chin for two versions before
a ruler overlay caught it. **Verify a face band against a labelled ruler render, once, per
clip.**

### 16c-iii. Cut feel

Long tails read as dead air, not as breathing. Reel 21 v5 held up to 0.60s after a line
and preserved internal pauses up to 0.60s; Nishant called it *"a lot of weird silences"*.
Settled: **one uniform ~0.16s tail everywhere**, `GAP=0.32` so long mid-sentence pauses
are removed rather than preserved, and the only long tail in the reel is the closing
hold's. That took reel 21 from 46.15s to 43.72s with no words lost.

### 16d. Audio

- **SFX on roughly one cut in four**, not on every cut. `public/sfx/` has swish, swish2,
  transition, pop, click. Schedule each cue at *event minus the measured peak offset*, never
  at the raw cut frame. Measured offsets: click 0.15 fr, pop 3.6, swish 7.2, swish2 7.65,
  transition 7.5 (at 30fps).

  > **Corrected from "≥75% of cuts" (11 Aug, second pass.)** Counting sharp onsets (>3.2×
  > rise over 30ms) landing within 120ms of a cut gives **10% / 23% / 24%** across the three
  > reels. The earlier 93/71/79% almost certainly counted **music-beat transients** as SFX —
  > with a continuous bed there is a transient near almost every cut, so a band-energy test
  > cannot tell a whoosh from a kick drum. Put SFX on the turns and let the bed carry the
  > rest; SFX on every cut is a known amateur tell.
- **Music: still not our job.** Harman's bed is continuous, but Nishant's standing rule is
  SFX-only on delivery — he adds music when posting. Build and mix assuming a bed will sit
  underneath, so leave headroom and do not fill every gap with SFX.
- Room tone still runs under the whole reel; never cut to digital silence.

### 16e. What v1 got right and v2 keeps

- The closing hold (§5d) — unchanged, it is the screenshot frame.
- Redaction bars (§5c) — unchanged, still the most ownable device.
- Number pills (§5b) — unchanged, but now they live in a much busier frame, so the max of
  2 on screen matters more.
- No screen recordings, no stock b-roll, no cover text, no logo bug, no grade.
- Text stays inside 12%–80% of frame height, and **never on his face** — this rule outranks
  every position number in §16c.

### 16f. The caption row limit (added 11 Aug, second pass)

**A caption may never render more than TWO rows.** This is a face-safety rule, not taste.

The block is anchored at the bottom and grows upward. Three rows at body size reach y1163 —
and his chin moves as high as **y1136** when he leans into the lens, not the y1215 you get
from measuring one frame. Reel 22 v2 rendered "VC funding" straight across his mouth before
this was caught. Two rows top out at y1272 and clear him.

Budget ~20 characters per row at body size, ~15 at hook size. Adding one word can silently
push a row onto his face, so **re-render and look at every talking-head frame after any
caption edit** — the failure is invisible in the data file.

### 16g. Landscape b-roll without upscaling (added 11 Aug, second pass)

Nishant, 11 Aug: *"don't zoom brolls, it'll reduce the quality."* Most of the 457-clip library
is landscape, so the treatment matters:

- **Portrait source** → full bleed, 1:1, no transform.
- **Landscape source** → a **1080×1080 centre crop shown at native size** over a blurred,
  scaled copy of itself. `objectFit: cover` on a square box scales a 1920×1080 source by
  exactly 1.0, so the sharp layer is the source's own pixels, cropped rather than resized.
  Bias with `objectPosition` when the subject sits off-centre.
- Only the blurred backdrop is ever scaled up, and it is blurred to mush.
- A clip below 1080 on its short side (there are some 848×480 in the library) cannot be used
  full-width at all — drop it rather than upscale.

### 16h. How to prove a cut has no duplicated take (added 11 Aug, second pass)

**Transcribing the render does not work.** Reel 22 v1 shipped with the false start *and* the
retake of the same sentence back to back, and it passed verification twice — because every
ASR engine collapses an immediate repeat into one sentence. Both WhisperX and Whisper-via-
/watch returned clean, correct-looking transcripts of a defective cut.

The detector that works is **syllable onsets vs word count, per clip**:

```
ratio = (onsets with >1.45x rise, 120ms apart) / (words in that clip)
```

A clean clip lands at 0.85–1.15. Reel 22's c1 measured **2.00** — twelve words, twenty-four
onsets — which is what exposed the doubled take. Run this on every clip before styling.

---

## 17. Ranked-list / listicle reels — the approved format (added 11 Aug 2026)

Provenance: reel 02 "free certificates, part 2", the @unscripted.nishant ×
@nishantchahar.ai collab. v4 approved by Nishant after three layout rounds:
a novel carve-up (card + lane + narrow face + side rail) was rejected outright
("this division of space looks absolutely shit — don't ever use this"), and
full-bleed alternating registers were rejected too ("feeling clutter, the focus
is shifting so frequently"). **The signature 60-40 split won.** This section is
the standing recipe whenever a reel on this account is a ranked list of
external things — tools, sites, certificates, resources.

Reference implementation: `src/Reel02b/` (Final.tsx + gfx.tsx + gen_data.py).

### 17a. The frame — one stable architecture, never redivided

```
screen card    x36  y236   1008x630    radius 26   (clears IG top UI)
caption lane        y886   160 tall    CAPTION-ONLY — nothing else, ever
face card      x36  y1066  1008x818    radius 28, full width, to y1884
```

- The frame's architecture NEVER changes mid-reel. All variety lives in what
  the card shows. The viewer's eyes must never have to re-find his face.
- Captions never touch his head: the lane floor stays ≥20px above the face
  card. Fit the take with headroom (hair ~120px below the card's top edge).
- Registers/cards hard-cut. Nothing animates across a cut boundary.

### 17b. The card sequence — list first, then the proof

Per item: **the ranked list takes the card** at the naming moment (~1.5s) —
rows already named stay, the new row slides in — **then the evidence takes the
card** (real page capture panning, keyed to the words). Never the reverse, and
never both at once.

The list opens LOCKED: numbered slots with blank bars, no names. Naming all
five in the hook answers the question the reel is selling and kills the reason
to watch. Names appear only as they are spoken. The CTA recaps the full list
with verdicts — that recap is the screenshot frame.

### 17c. Type and shapes

- List rows are the beat, sized like it: ~64px names, 72px number squares
  (recap: 54px / 62px). If it doesn't read on a phone held at arm's length,
  drop ornaments before dropping size.
- **No pill/chip shapes as design language.** Rounded-999 chips over b-roll
  "make it look AI generated and raw." Facts over evidence are set as
  editorial TEXT lines on the footer scrim (strike-through for the myth,
  accent for the payoff). Verdicts are square-cornered stamps.
- One exception: a single keyword pill at the CTA ("Comment X") — approved,
  but big (~52px).

### 17d. Evidence

- Real page captures only (screenshot-and-pan, `capture_reel02b.mjs` is the
  pattern) — the claim "this page says free" is proven by showing the page.
- A page that can't be captured (bot-walls) gets a typographic quote card in
  the same frame slot, never a mock.
- Hand-drawn marker rings on the exact words/buttons being cited; rings are
  canvas-space, so they must fade before the page pans (`until`).

### 17e. Account tokens on a NON-collab listicle — decide before building

Reel 02 ran the .ai account's yellow `#F8F800` and heavy karaoke-adjacent
captions because it was collab-posted to both grids. Those two tokens are the
`.ai` account's property (§7, §11) and the two grids must not converge. If
this format is ever used for a **solo** @unscripted.nishant post, the
structure (17a–17d) stands but the accent must be re-decided with Nishant —
default assumption: Unscripted Blue fill / white text, captions per §16.
Do not carry yellow onto a solo post silently.


### 16i. The caption type system, corrected against Harman's actual frames (11 Aug, third pass)

Reading his caption band at full resolution instead of off a contact sheet. **The size jump
is the device** — colour alone reads flat, and colouring a whole phrase (which reel 22 v3 did)
is the same as colouring nothing.

```
emphasis   YELLOW #FFD60A · Inter 800 ITALIC · UPPERCASE · 1.5x the body size
lyrical    white · Instrument Serif ITALIC · 1.12x          ("hua hai ?", "in three")
body       white · Inter 700 upright                        ("ke liye", "sabse")

body size  4.3% of frame height · hook lines 4.7%
```

Rules that come out of it:

1. **Exactly ONE emphasis chunk per caption**, and it is the word that carries the line — the
   number, the name, the payoff. Never the whole sentence.
2. The emphasis word being **bigger** matters more than it being yellow. Both, always.
3. Hook size is capped by the longest single emphasis word in the reel: "MICROSOFT" at 1.5×
   runs the full frame width above 4.7%.
4. Sizes cascade off the parent, so em units — never re-specify px per chunk.

### 16j. Captions go ABOVE his head on a locked take (11 Aug)

Nishant: *"there is space above my head, use that."* On reel 22's take the ceiling band is
empty for the whole reel and the captions were sitting on his chest.

- **Caption block bottom = y478**, growing upward, centred.
- His hair top runs **y545–620** across that take, so this leaves ~65px of clear air at the
  tightest, and two rows still top out at y238 — inside the y230 safe line.
- Measure the hair top **across every talking-head shot**, not one frame. It moves.

### 16k. No pills in this genre (11 Aug)

Nishant: *"pill design in this screams cheap, don't use pills in these types of video."*

~~§5b's blue number pill~~ — **retired for story/essay reels.** It is a leftover from the v1
lifestyle doc and it does not exist anywhere in the reference cohort. Every number the
reference reels carry is a **caption emphasis word** instead — `1 LAKH`, `SINGLE MONTH`, `26`.
That is where numbers go now. The redaction bar (§5c) is unaffected.

### 16l. The closing hold (11 Aug)

~~JetBrains Mono 400 at 4%~~ read as a terminal prompt over a Dubai marina at dusk. The closing
frame is the reel's one elegant beat, so it takes the account's most elegant register:

```
Instrument Serif ITALIC · white · 7% of frame height · centred
placed in the empty sky, clear of him in frame
fade in over ~420ms, then hold
```
