# The Tharun desk edit — measured off 2 reference reels

**Measured 14 Sep 2026** from two reels Nishant sent as the target ("learn the editing style").
Everything below is measured off the files (ffmpeg scene cuts, per-frame luma through every
register change, pixel bboxes of the type at native 720×1280 scaled ×1.5 to the 1080×1920 canvas,
Haar face boxes for shot sizes, RMS windows for the sound), then checked by eye on a **4 fps
dense sheet of every frame** — the scene-change sampler alone missed half the devices.

| Ref | Subject | Length | Account it maps to |
|---|---|---|---|
| A | "5 things to build this week with AI (Emergent)" — sponsored, tools | 83.7 s | tools account |
| B | "3 skills to learn before this year ends" — self-improvement | 59.6 s | personal account |

Files: `assets/style-refs/tharun-desk/` — both MP4s, a scene-cut contact sheet per reel, and the
4 fps dense sheets (`sheets-A/`, `sheets-B/`, 6 timestamped frames per sheet). Re-sample from
there; do not work from this doc's memory of the frames.

Operating recipe: the `layered-head-edit` skill. This doc is the evidence.

---

## 1. The architecture — full-frame head, graphics land ON the shot

Neither reel uses a split. The talking head is the base for ~65% of A and ~55% of B, full frame,
and every graphic is placed **in the shot's own space**:

- **behind the head** — the person is matted, the type sits between him and the room, his hair and
  shoulders occlude the letters (B 0.25–4.25 "3 SKILLS", B 8.25–10.5 "CAPABLE YOU ARE",
  B 11.0–12.9 "spend 30 MINS everyday", B 41.0–43.5 "FOCUS 10–14 HOURS"; A 6.25–7.75 newspaper
  card, A 26–28 "PROJECT 1–4" cards, A 33.0 Emergent logo).
- **on the props** — A's five poker chips light up in sequence (25.5–26.75) and get numerals
  "1 2 3 4 5" drawn above them (28.5); the chess knight he moves IS the progress marker.
- **beside the hand** — icon chips pop where he gestures (A 41.25 user-input icon, 42.5 database,
  43.25 lightbulb; B 2.25 three skill icons, B 18.25 / 19.25 skill icons in the top corners).
- **around the cutout** — A 11.5–14.25: the subject's head cut out on paper, red condensed caps
  stacked around it, tool logos orbiting on a dashed circle.

The effect: nothing is "in a card next to him"; everything is in his world. That is the single
biggest difference from the house 60-40 split.

## 2. Pace

Scene-cut detection (`select='gt(scene,0.2)'`, de-duplicated within 0.1 s) plus hand count on the
dense sheets:

| | cuts | cuts/s | cuts/min | median shot | longest hold |
|---|---:|---:|---:|---:|---:|
| A | 41 | **0.49** (≈0.55 by hand — same-setup punch-ins under-detect) | 29 | 1.1 s | 8.4 s (29.0–33.4, the numerals + chips beat) |
| B | 26 | **0.44** | 26 | 1.5 s | 5.1 s (50.0–55.0, the DM composer) |

Section pace in A: hook 0–25 s **0.56/s**, body 25–70 s 0.51/s, tail 70–84 s 0.29/s.
First 5 s: A has 3 cuts + 6 caption/label events; B has **1 cut** (at 4.44) but a label event every
~0.4 s (title lands 0.25, "16-20" 0.75, "years" 1.25, "old" 1.75, three icons 2.25, "3 skills"
3.0, icon glow 3.5). The density rule is met by **type events, not cuts**.

This is slower than the Harman spec (0.76–1.08/s) and faster than the house split reels
(0.2–0.35/s). Target **0.45–0.55 cuts/s**, and never let a hold pass ~5 s without a graphic event.

## 3. Shot sizes — hard cuts between fixed crops, never an animated zoom

Haar face-box width as % of frame width (A):

| shot | face width | face centre y | seen at |
|---|---:|---:|---|
| base (desk + chips in frame) | 38–41% | 0.39 H | 0–3.4, 8–11, 25–33, 47–52, 61–75 |
| punch-in | **53%** (≈1.35×) | 0.42 H | 25.0–25.4 ("So"), 11.0 |
| second camera, over the laptop | 31% | 0.37 H | 40.4–44.2 |
| close (leaning in) | 36% | 0.37 H | 78.4–83.7 |

B stays on one framing (31–35%) the whole reel; its variety comes from the graphics, a b-roll
insert (9.0–10.5 reading a book, 41.0–43.5 typing at an office desk) and the 50-50 stack.

Every size change is a **hard cut on a word edge**. No scale curve touches a cut boundary —
consistent with the house no-zoom-at-cuts rule. The only camera moves are INSIDE graphics (the
coin MG dollies, the starfield map drifts).

## 4. The caption system — accumulating lockups with a hero word

**A (the tools reel)** — heavy geometric grotesk (Inter/SF Pro Display Bold class), pure white,
soft dark drop shadow, tight tracking, sentence case with punctuation kept ("part?", "out.",
"simple,").

Measured at 1080×1920:

| element | size | position |
|---|---:|---|
| regular caption (1–2 words) | em ≈ **110 px** (ascender-to-baseline 84 px; ≈5.7% H) | centre **y ≈ 1300** (0.68 H) on the desk shots, chest level, below the chin |
| two-line lockup | small line em ≈ 65 px over hero line em ≈ 180–190 px | lines at y ≈ 1208 / 1306 |
| hook lockups (top band) | numerals in condensed heavy caps ≈ 180 px + qualifier sans ≈ 40 px | top-left, y 250–620, partly behind the hair |

**How a caption enters:** word by word, **each word popping ON its spoken onset and staying**, so
the phrase accumulates: "the" → "the story" → "the story of this"; "you're" → "you're seriously" →
"you're seriously missing" → "…missing out." When a phrase has a hero word it is set at ~1.7× and
the phrase re-flows around it ("500 / crores of revenue", "finally / **acquired**", "why they /
get **stuck**", "build any / **complex** / app", "couple of / **weeks**", "never used /
**Emergent**"). The phrase clears on the next phrase's first word. No karaoke highlight, no colour
change, no box.

**Position is not fixed.** Chest band by default; slides into the top band when the shot is
framed low (the hook), and sits **left of centre next to the gesturing hand** on a few beats
("the" 11.5, "you're" 20, "AI" 61.25). It never crosses the face.

**B (the personal reel)** — the same idea at a smaller scale: SF Pro Semibold class, white with a
dark shadow, **em ≈ 60 px** (3% H), 1–3 words per run, centre **y ≈ 1030–1060** (0.54 H, just
under the chin), phrases replace rather than accumulate. In the 50-50 stack the caption drops to
**y ≈ 955**, just under the seam.

## 5. The display voices

| voice | face | measured | where |
|---|---|---|---|
| **grunge condensed caps** (B) | eroded/distressed heavy condensed caps, white, light grain | cap height **175–255 px** ("30 MINS" 254, "PROBLEM" 237, "90 DAYS" 212, "DEADLY • COMBO" 178, "3 SKILLS" 176); kickers in a light sans at 33–38 px ("Don't Ignore These", "one last push", "before 2026 ends") | titles above the head (centre y 266–434), behind-the-head statements, the end card |
| **neon highlighter stamp** (A) | black condensed caps on a **#D7FA0A** block, slight rotation, hard edges | "Comment" 64 px sans-bold + "THARUN" 190 px condensed caps in curly quotes; single-word stamps "PROMPTING," "TWEAKING," "AND" "HOSTING" | under the device card on the grid-paper demo register; once on the face shot at the close |
| **neon caps on black** (A) | #D7FA0A condensed caps, centred | "REAL BACKEND / and / DEPLOYMENT" builds a line per spoken word over 1.1 s | the black interstitial 45.5–46.6 |
| **red condensed caps on paper** (A) | red/black condensed caps on a paper texture | "ZACK HIMSELF REVEALED" stacked around a cutout head | 11.5–14.25 |
| **count-up numerals** (A) | white condensed heavy | "18" → "18 19" → "18 19 20" / "Years old" on each spoken number; "18 MONTHS"; "1 2 3 4 5" over the chips | top band, behind the hair |

House mapping: the neon yellow is the tools-account accent (use the house `#F8F800`); the grunge
caps voice carries no accent colour and is safe on either account.

## 6. Register grammar — flashes and blinks, measured per frame at 25 fps

Every register boundary is a **hard cut with a punctuation frame**. Per-frame mean luma:

| device | frames | luma trace | where |
|---|---|---|---|
| **white flash** | 2 frames of white (80 ms), sometimes preceded by 1 half-bright frame | 81 → (206) → 232, 232 → 108 → 88 → 81 | A 14.32 (paper card → face), 24.96 (shatter → face), 33.3 (face → coin MG), 52.76, 59.08, 82.28; B 28.32, 55.04 |
| **blink** | 1 frame **inverted** + 1 frame **black** | 79 → 158 → 16 → 38 | A 17.6 ("you're seriously"), 44.2 ("simple logic" → black card), 64.7 ("till now") |
| **strobe** | after the flash, the frame alternates red-tint / normal every 2–3 frames for ~0.5 s | 57/50/57/50… | B 28.3–28.9 "PROBLEM" |
| **wash → white** | frame desaturates to ~70% white over 3 frames, then 1 white frame | B 26.25–28.25 "comment THARUN", 47.5–47.75 | the CTA and the map's re-entry |
| **smoke wipe** | the starfield's cloud layer rolls over the face for ~0.4 s | B 5.25–5.75, 15.25–15.5, 47.5–47.75 | face → the map |

Held inverts do not exist: the "18 19 20" count-up plays on the normal footage (luma 66–80 with
motion) and the invert is the single frame at the exit. The type-on-invert frames in the scene
sampler were that one frame.

Ordinary cuts inside a register (punch-ins, shot changes) have no flash.

**Which boundaries get one.** The detector logs a punctuated boundary as 2–3 cuts inside 0.1 s;
a plain boundary as one. A: punctuated at 3.44, 7.96, 14.32, 17.6, 24.84, 33.36, 38.0, 44.2,
52.72, 59.08, 64.68, 82.24 — **12 of 41 cuts, one per ~7 s**. Every entry INTO the coin world is
punctuated (33.36, 38.0, 44.2, 52.72, 59.08); every return to the face is plain (35.36, 40.4,
46.64, 54.4, 61.2); demo cards enter and leave plain (35.36, 50.0, 54.4, 76.24). B: smoke into the
map (5.25, 15.25, 47.5), map → face plain (7.5, 18.2, 32.75, 50.0), wash for the CTA, flash +
strobe for the alarm, flash for the end card. **Flash in, cut out.**

## 7. The device catalogue (with timestamps to re-sample)

**Hook, A (0–14.3 s)** — 0–3.4 face holding a polaroid, caption "the story of this" small top-left
+ "18 YO / student" hero with a curved hand-drawn arrow pointing at the photo → 3.44 cut to the
photo full frame, slight push → 4.0 the photo goes B&W with the subject left in colour under a
purple glow + "ZACK" label with a curved arrow → 4.72 punch → 5.96 back to face, an App-Store-style
icon chip inline in the caption ("he built [icon] an App") → 6.25–7.75 a **newspaper card slides
in behind his head** (headline, photo, mono metadata) and a **yellow highlighter sweeps** "$50M
and" at 7.0 → 9.2 "18 MONTHS" hero → 11.5–14.25 the paper card with the cutout head, red caps,
orbiting tool logos → white flash → face.

**Hook, B (0–5.5 s)** — face raw; "Don't Ignore These / 3 SKILLS" grunge title lands at 0.25
above the head (behind the hair) with a lightning-crack decal; "16-20" / "years" / "old"
accumulate 0.75–1.75; three skill icon chips pop under the chin at 2.25; "3 skills" 3.0; the third
icon glows white on "you must learn" 3.5; smoke rolls in at 5.25 → the map.

**The accumulator MG** — a scoreboard graphic that returns after EVERY list item with one more
item revealed. A: a purple 3D coin between two glowing hands; the numbered coin spins in and flips
to its label, then the row of five coins below shows the earned labels so far (33.3 Landing Page,
38.75 Simple Web Apps, 44.25 Full-Stack Web App, 53.25 Interactive Game, 59.0 AI-Powered SaaS;
each visit 1.5–2.3 s). B: a glowing node with satellites on a starfield; labels attach as the
skills are named (6.25 COMMUNICATION, 16.0 SIDE HUSTLE, 33.5 DEEP WORK, 48.5 LAST SECRET), with a
dolly in to the new node every time. **This is the structural device of both reels.**

**Grid-paper demo register (A)** — near-white paper with a faint grey grid; a rounded dark device
frame carrying a REAL screen recording (Emergent prompt → Deploy → OSMO landing page scrolling,
35.4–38.0; the Linkfold build 50.0–52.7; tic-tac-toe 54.5–54.75; Flappy Bird 55.0–57.6 with the
caption riding inside the card's bottom edge); cards **stack and slide** rather than cut; the
neon stamps land one per spoken word under the card ("PROMPTING," 36.3, "TWEAKING," "AND",
"HOSTING" 37.5). Sponsor card at 76.2–78.4 with "never used / Emergent" hero.

**50-50 stack (B)** — a dark starfield card occupies y 0–916 (seam measured at 0.477 H) and the
talking head is **translated down ~500 px, not scaled** (face centre 0.39 H → 0.65 H); caption at
y ≈ 955. Contents: the "5 SIMPLE STEPS" table 13.0–15.25, the "Detailed Document" folder 22.0–
23.5, the "5 Best Things" table 23.75–26.0 (rows blurred = withheld payoff; re-shown tinted RED at
30.5 on "you'll not be able to learn any of them"), "The Upper Circuit" chart 39.0–40.75, the doc
icon 43.5–46.0. Each card holds 1.5–2.5 s with a slow drift.

**Alarm beat (B 28.3–29.2)** — the whole frame goes red (multiply), a ⚠️ emoji and "PROBLEM" in
grunge caps over his chest, strobed against the normal frame for ~0.5 s.

**B-roll with behind-head type (B)** — 9.0–10.5 him reading (maroon hoodie) under "IT DOESN'T
MATTER HOW / CAPABLE / YOU ARE / IF YOU CAN'T EXPLAIN IT / CLEARLY" building a line per phrase;
35.25–37.0 an illustrated B&W office worker ("MOST PEOPLE GET / DISTRACTED / ONCE EVERY 2 MINS",
the figure's expression changing at 36.75); 41.0–43.5 him typing under "FOCUS / 10–14 / HOURS /
CONSISTENTLY".

**CTA** — A: the neon stamp under the Linkfold demo (50.25–52.7) and again on the face at 82.3;
B: the frame washes out, "comment "THARUN"" glows on his chest (26.25–28.0), then a white frame.

**Share beat (B 52.5–55.0)** — the reel shrinks into an iPhone DM composer (dark iMessage-style
thread, his video as the sent attachment, the bubble "bro, let's do this together?", keyboard up)
— the house CTA comment-composer pattern in DM form.

**End (B 56.5–59.6)** — black card, "one last push / 90 DAYS / before 2026 ends", grunge numerals
with light-sans kickers, music lyric outro. A ends on the face + stamp. (House rule keeps the
Follow close — see the skill.)

## 8. Sound

Both carry a **music bed** (A's tail after the last word sits at −15 to −22 dBFS; the quietest
speech gaps in the body are −31 dBFS; B ends on a lyric drop). At the register flashes the RMS
jumps 14–22 dB inside 100 ms where speech is quiet (A 24.96: −27.7 → −13.9; B 4.44: −30.9 →
−11.5; B 18.2: −37.9 → −15.4; B 46.2: −21.4 → −15.0) — i.e. **every flash carries a hit/whoosh**.
A is mastered hot: −14.2 LUFS with a +1.2 dBTP peak (clipping); B −14.1 LUFS, −3.0 dBTP.

House adaptation: SFX only, he adds the bed — but the hits at every flash are part of the
grammar; schedule them peak-aligned (`sfx-design`).

## 9. What the house rules change

| reference does | house does |
|---|---|
| type behind the head via a person matte | same, via a matte (MediaPipe selfie segmentation, the slice-reveal recipe) or Omni behind-the-head v2v; the head may occlude the type, the type never covers the face |
| B draws "comment THARUN" and "PROBLEM" over his chest | chest is fine; nothing over the face, ever |
| A's yellow `#D7FA0A` | house tools yellow `#F8F800`; never yellow on the personal account |
| ends on a title card / face | ends on the Follow close in the full-frame idiom (compact top-band strip) |
| music bed + hits | SFX hits only; he adds music |
| rounded-pill icon chips beside the hand | fine as ICONS; label stamps stay rectangular |
| mastered to +1.2 dBTP | −14 LUFS, ≤ −1 dBTP, measured on the encoded file |

## 10. What I could not determine

- The exact fonts. The captions read as Inter/SF Pro Display (A: Bold, B: Semibold); the grunge
  caps read as Bebas Neue/Anton with a distressed texture mask; the neon stamps as Anton/Bebas on a
  block. Use the approved pairings in `font-pairings-by-style` and match the measured sizes.
- Whether the behind-head mattes are rotoscoped or generated. The edges are clean on hair, so
  likely a segmentation matte with feathering.
- The SFX library. Hits are audible as energy, not identified by name.
