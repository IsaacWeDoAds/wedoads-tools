---
name: whiteout-edit
description: "Use when he asks for the Whiteout look, 'the find skills reel style', 'the white paper one where the whole screen goes white', or any 9:16 tools-account talking-head reel where his face stays clean and full frame and the explanation takes over the WHOLE frame on a plain paper-white canvas, one idea per visit. Not for a face card that slides away under grid paper (paper-drawer-edit), recording-led demos (split-screen), graphics inside his shot (layered-head-edit), or 'just captions' (caption-edit)."
---

# WHITEOUT — face ⟷ paper, one idea per visit

> **THE JOB:** two full-frame registers and nothing else. His face — untouched, uncut within a
> run, caption only. And a plain paper-white canvas that takes the whole frame for 2.5–5.7 s and
> plays ONE idea as kinetic type and drawn UI. Paper **slides over him or dissolves in**; it always
> **hard-cuts out**.

**Named 1 Oct 2026** from his own reel "find skills" (`assets/style-refs/whiteout/find-skills-final.mp4`,
6 fps sheets + an entry strip beside it). Every number below is measured in
`docs/whiteout-edit-style.md`, cross-checked by an independent pass. **Sample the sheets before
building** (`sample-named-reference-first`).

## Which format is this?

| the reference you're shown… | format |
|---|---|
| a screen card above a face card, caption lane | `split-screen` |
| **grid** paper; his face is a **card under a seam** that slides away as a drawer and comes back; pixel mascots | `paper-drawer-edit` — the sibling. Same paper family, different register mechanism |
| graphics IN his shot (behind the head, at the hand); the head punches in | `layered-head-edit` |
| overlays on one uncut take | `caption-edit` |
| **plain** paper (no grid) that **covers his whole frame**; the face is never a card; out is a hard cut | **this skill** |

**The 02b v3 rejection — surface it in the asset plan.** Reel 02b v3 alternated face full-frame
⟷ evidence full-frame on hard cuts: *"feeling clutter… the focus is shifting so frequently."*
Whiteout is a full-frame alternation too. He asked for it by name, which licenses it **in this
format only**. Keep the four things that make it a different grammar, or you have rebuilt v3:

1. **One canvas.** The same paper every visit — the eye re-finds the paper, never a new picture.
2. **One idea per visit**, 2.5–5.7 s, built from 2–5 events.
3. **The face never changes**: one framing for the whole reel, no cuts or punch-ins inside a run.
4. **Entries are physical and short** (slide 6–7 f, dissolve 3–6 f); a visit starts only every ~6 s.

## 1. The registers

| | face | paper |
|---|---|---|
| share of runtime | **~35 %** (+ ~3 % blurred close) | **~62 %** |
| run length | median 2.0 s (0.8–3.4) | median 4.0 s (2.5–5.7) |
| content | the take, full frame, scale constant — **no punch-ins, no cuts inside a run** | one idea, 2–5 events (the hook visit: 8–10); every noun he says gets one |
| text | the caption, plus at most a handoff chip (§5) | display type + the caption |

- **What goes on paper:** the line whose picture IS the point — the number, the name reveal, the
  list, the mechanism, the warning, the audit, the how-it-works, the DM. **What stays on the
  face:** connective and opinion lines ("But the number…", "This site has…", "You just need").
  When a script has no connective lines, the face gets the opener, his personal claim, and the CTA
  ask word — at most one payoff line, the one whose picture an earlier visit already drew.
- **How many visits:** `round(runtime / 6.2 s)`, ±1 — 8 for a 51 s reel, 4–5 for a 30 s one. A
  short reel keeps the floors (visit ≥ 2.5 s, a change every ≥ 2.8 s); it does not shrink them.
  Face runs: 0.7–3.5 s. There is no 3+-moving-elements rule on face runs — the density lives on paper.
- **Splices hide under paper.** A splice is legal in exactly two places: **inside a landed visit**
  (after its entry completes, before its out-cut), or **on the out-cut frame itself**. Never inside
  a face run, a slide or a dissolve. A face run is one contiguous span of the take — pauses inside it
  stay as recorded, so choose face runs over clean stretches and put any pause over ~0.4 s under
  paper. When a sentence break that needs a splice is also where paper should enter, enter on the
  previous sentence's last word so the splice falls inside the visit; if one must move, move the
  register boundary, not the splice. Emit the paper windows with the cut
  (`register-map-generated-with-cut`).

## 2. Transitions — measured at 30 fps

| move | spec |
|---|---|
| **slide-over (IN)** | the paper panel and its content translate in from one side **over a still face** (the face is not pushed). **6–7 f, easeOutQuart**; coverage 47/75/89/96/99/100 % — reads as done in 4 f. Sides alternate R, L, R, L. |
| **dissolve (IN)** | paper fades in over the still face, ease-out, **3–6 f** (≈ 41/79/93/98/100 %). The hero graphic starts only once paper is ≥ 93 % opaque, entering blur→sharp (≈ 16 px → 0) and scale 1.06–1.3 → 1 over 3–5 f. |
| **hard cut (OUT)** | 1 frame, 8/8 in the reference. No flash, no SFX, nothing animates out of paper. |

- **Alternate the entries strictly — slide, dissolve, slide, dissolve** — starting with a slide.
  Never the same entry twice in a row. The CTA visit takes whichever entry falls next (it was a
  dissolve in the reference only because that reel had 8 visits).
- Start each entry **3 f before** the first word it introduces, so the content lands on the word.
- **Settle before the cut:** ≥ 60 % of visits end on a fully still frame for 0.3–0.7 s.
- **The dissolve is a named house conflict** (`register-crossfades-banned`). It is legal here only
  because the face under it is one continuous, unspliced shot and no graphic is drawn until the
  paper is opaque — the reference broke that twice (a blurred "#1" over his face, and the CTA
  composer drawn while his face still showed through).
  Show him the dissolve in the asset plan; if he says no, the fallback is a hard cut whose hero
  settles blur 12 → 0, scale 1.06 → 1 over 4 f.

## 3. The paper canvas

- **One ground for the whole reel, no grid** (it is `paper-drawer-edit` that has the grid): radial
  `#F9F9F6` centre → `#ECECE7` upper corners → `#DFDFDA` bottom. Static. Ink `#090909`.
- **Accents, fixed:** blue `#2E78F2`; folder/object blue `#60B2F4`; status green `#13A046`,
  amber `#EE9B0F`, red `#EB2C2C`; notification red `#FC2A3C`. **No yellow** — the tools account's
  yellow convention doesn't apply to this format; say so in the plan. A brand colour only on that
  brand's own mark.
- **Text band:** display text inside y240–1380, centred on x540, ≤ 756 px wide
  (`center-text-on-frame`). Confetti, rings and cards may cross; text may not.
- **Sub-beats inside a visit join by motion, never by a cut** — and run out-then-in (4 f out, 5 f
  in), never blended:
  - **scroll-up:** the stage rises and fades; the next rises in from +80 px (6–8 f)
  - **zoom-through:** an element scales ×2 and fades over 8 f while the next scales up from 0.6
  - **hero → header:** a slam word shrinks to a header slot (the "#1": 407 → 136 px tall,
    y760 → 218, ~6 f) and the beat builds under it
- Every element lands **on its spoken word** (`caption-align` onsets). Only drifting furniture may
  stagger.

### Vocabulary — build each visit from 2–5 of these

| device | spec | reference |
|---|---|---|
| **display word** | Inter 900, tracking ≈ −0.05em, ink, sentence case ~135–160 px; caps only for one-word slams (cap ≤ 180 px — size a long word to the 756 px width); a number may slam at ~560 px and shrink. **Inks in** in place from ≈ `#BDBDBD` to ink over 4–6 f | "Skills for", "Security audit", "SAVE", "#1" |
| **serif italic** | Instrument Serif Italic, lowercase, 0.5–0.6× the display size | "this reel", "and then…" |
| **selection box** | stroke `#3777E4` ~3 px, fill ≈ `#D4DFF2`, round handles at top-left + bottom-right; **jumps to each word as he says it**; optional macOS arrow cursor with a click | "coding / research / writing", "Find Skills", "your DM" |
| **counter** | ease-out (each frame's increment ×0.85), ~18 f, lands on the spoken number | 7 → 10,000; installs badge |
| **kinetic-metaphor word** | the word acts out its meaning: FORGET's letters tumble away, REGRET builds, "guessing" ringed by serif "?" and junk-filename chips | P3–P5 |
| **recurring object** | ONE icon that returns across visits as the reel's thread — the noun the reel's subject acts on (skills live in folders → a folder; hooks act on files → a document). The reference's macOS blue folder: confetti (30–110 px, ±25°, 30–100 % opacity, drifting), tiles, a hero folder, row icons | throughout |
| **brand mark** | the tool's real logo lands on its first spoken word (`brand-logo-marks`); a household brand gets a centrepiece, not a chip | Claude dot on the prompt card |
| **real product card** | a real screenshot of the real page on a dark card (`#0B0B0D`, radius 28, soft shadow, tilt ≈ −3°), rising from bottom-right rotated −8° with overshoot over 8–10 f | skills.sh leaderboard, find-skills card |
| **drawn UI** | a prompt card typing (~2 f/char); a terminal typing `$ …` → `✓ installed`; white rows with a blue scan bar sweeping and a verdict per spoken word; flow pills "You → Claude → skill ✓" filling in turn | P4, P6, P7 |
| **ring text** | a line on a slowly rotating circle with a pill at its centre, for a "one thing most people do" setup | P5 |
| **circled-letter row** | a word set one letter per dark circle, under a number | "CLAUDE SKILLS" |
| **pills** | black `#0A0A0A` / blue `#2E78F2`, white text ≥ 48 px, ≤ 2 per visit — **on paper only, as diagram parts**, never over footage | "I know", "most people", "you're going to" |
| **verdicts** | **rectangular stamps**, not the reference's pills (`stamps-not-pills`): radius ≤ 12, 700 weight, ≥ 34 px, status colours | SAFE / ALERTS / HIGH RISK |

**Drawn UI vs recordings.** A prompt card, terminal or comment box drawn on the paper is fine
(mocked terminals are fine). A product's real interface appears only as a real screenshot card or
a real `screen-capture`. Terminal output and any app session shown must come from a real run —
ask him to record it, or copy real output word for word.

## 4. Captions — one voice, two positions

- Neutral grotesk Regular (reference reads SF Pro Text / Helvetica; **build in Inter 400**),
  **78 px** (reference ~75 — the house floor wins), sentence case, punctuation kept, **2–4 words
  per chunk, replacing**, never ending on a function word. No plate, no karaoke, no accent, no
  hero word.
- **Entry:** 5 f easeOutCubic — opacity 0 → 23/66/85/98/100 %, rising ~11 px, blur ~6 px → 0. The
  outgoing chunk vanishes instantly.
- **Face:** `#FFFFFF`, shadow `0 2px 6px rgba(0,0,0,.35)`, centre **y ≈ 1300** (reference 1302,
  ~170 px under the chin box — re-derive per take with `take-geometry`). On a desk take where hands,
  a laptop or a mic fill that band, move to the nearest clear band under the chin and deepen the
  shadow (`0 2px 10px rgba(0,0,0,.6)`) — never a plate, never on the face.
  **Paper:** `#0A0A0A`, no shadow, centre **y1420** (reference 1492 breaks the y1470 text floor;
  `paper-drawer-edit` settled the same number). Both centred on x540, ≤ 756 px.
- **At a register change, no second fade.** During a **slide** the caption is drawn twice — the
  paper version clipped to the moving panel, the face version outside it — so the panel edge splits
  it (that's what the reference does). During a **dissolve** it switches on the frame the paper
  reaches ≥ 93 %. On the out-cut it switches on the cut frame.
- **The close keeps a caption:** white with the face shadow at y1420, under the glass card
  (the reference dropped it; `every-beat-gets-a-caption` wins).
- The CTA's trigger word may be set in caps in the caption, as he says it — the one exception to
  "no hero word".
- Captions run through every visit. The paper's display type is the idea, not a transcript — don't
  also set the caption's words big.

## 5. The handoff chip

At most twice a reel, the next idea starts on the face: a white rounded label with a black icon
(~622×130 px, centred x540, y≈236–364, ≥ 25 px above his hair) pops in on its word (6 f),
holds, **shrinks out over the 5 f that end on the entry's first frame**, and that visit's heading
(~96–135 px) lands **in the same spot** — continuity by position. Reference: "🛡 Security audit",
F6 → P6 (a dissolve); it works the same before a slide. The icon may be a real brand mark in its own
colour. Needs his hair top (5th percentile) at y ≥ 389; on a tighter take, drop the chip. The
heading it hands to may persist across consecutive visits as a running header for a list (e.g.
"3 hooks" with progress dots). Run the alpha face guard over it.

## 6. Hook (0–5 s)

- Frame 0 is his face — with a prop or a gesture if he shot one — and the first caption. Not paper.
- First visit by **~1.5–1.7 s**, by **slide**, landing on the hook's number or noun (a counter
  racing to it) with the recurring object bursting outward and a real card rising.
- ≈ 10–11 events in 5 s (one every ~0.45–0.5 s): caption swap, slide, counter, burst, letter row,
  card, scroll-up into the next stage, list items on their words.
- Withhold the specifics (what each item is) until the line names them.

## 7. CTA and close

- **CTA visit (whichever entry is next):** the house comment composer (`cta-comment-composer`) —
  a neutral viewer avatar, the real trigger word typing at ~2 f/char, Post lights and presses →
  2–3 "@you · WORD" cards stack above it (never invented commenter handles — the reference used
  some) → scroll-up → a paper-plane icon with a red "1" → "your DM" (or the thing he'll send) with
  the selection box on it.
- **Close (the Follow close in this idiom; it replaces the 60-40 `FollowCta`):** hard cut to his
  face; **from cut + 2 f** a gaussian blur 0 → ~32 px plus a dim to ~60 % over ~8 f; a frosted-glass
  profile card springs up (~8 f, overshoot) with his **real** avatar, handle ✓, name line, bio and
  posts / followers / following — re-read them the day you build; a cursor taps Follow ~21 f after
  the card starts so the flip lands on "follow"; "Following ✓" holds 0.5–0.9 s. Card centred x540,
  ~y1000, ≤ 620 px tall, **inside x162–918** (the reference's ran x80–1000). Reuse
  `paper-drawer-edit`'s glass card if it has been built.

## 8. Sound

SFX only, he adds the bed. A whoosh on every entry (slide and dissolve); **nothing on the cuts back
to the face**; a pop per pill, stamp, icon and ink-in; a tick per typed character and counter run; a
click on selection snaps, cursor presses and the Follow tap. Peak-aligned (`sfx-design`), −14 LUFS
on the encoded file — the reference shipped at −8.6 LUFS, +1.1 dBTP.

## Pipeline hooks

- **Asset plan** (`asset-plan`) — per paper visit: window, entry (slide L/R or dissolve), the ONE
  idea, its 2–5 devices, every real card or capture with its source, every number with its source.
  **Counters land on the number the real card shows** (the reference counted to "1.5M+" beside a
  card reading "3M"). An unverifiable personal claim ("saved me an hour a day") gets no counter and
  no number graphic — it stays his words in the caption, on the face. The recurring object. Plus
  the conflicts, quoted, for his yes: the 02b v3 alternation, the dissolve, pills-on-paper, and
  "no yellow" against the router's tools-account line. **Look:** the canvas, ink and blue are the
  style he named and stay fixed; `topic-led-look-per-reel` applies to the recurring object, the
  metaphors and the brand marks — show a 3-frame style board with his face in it.
- **Cut** (`shortform-cutaway` → `cut-audit`): splices only at the legal positions in §1.
- **Geometry** (`take-geometry`): one framing for the reel; chin → face caption y; hair top → chip.
- **Build:** check `mg-kit` and `paper-drawer-edit` first — the selection box, ink-in headline,
  comment composer, DM notification and glass Follow card are shared parts.
- **Review** (`reel-review`): alpha face guard over every dissolve frame and the chip; card-motion
  check on paper visits (settle tails ≤ 0.7 s are legal); still-sample each entry's frames to prove
  slides are 6–7 f and dissolves ≤ 6 f; safe-area extents catch text past x918 or below y1470.

## Quick reference

| thing | number |
|---|---|
| paper / face | ~62 % / ~35 % (+ close) · visits 2.5–5.7 s (median 4.0) · face runs 0.8–3.4 s (median 2.0) |
| cadence | visits = round(runtime / 6.2 s) ±1 · register change every ≥ 2.8 s · face runs 0.7–3.5 s |
| entries | slide 6–7 f easeOutQuart (sides alternate) ⟷ dissolve 3–6 f, strictly alternating, start 3 f before the word |
| exits | hard cut · settle 0.3–0.7 s on ≥ 60 % of visits (up to ~1 s is a NIT, not a defect) |
| splices | inside a landed visit, or on its out-cut frame — nowhere else |
| paper | `#F9F9F6` → `#ECECE7` → `#DFDFDA`, no grid, ink `#090909`, blue `#2E78F2`, no yellow |
| display | Inter 900 −0.05em, 135–160 px (caps slam ~180 cap) · ink-in 4–6 f · y240–1380, x540, ≤ 756 |
| selection box | `#3777E4` stroke, `#D4DFF2` fill, 2 round handles |
| caption | Inter 400 78 px · 2–4 words · 5 f rise-fade · face white y1300 · paper ink y1420 |
| chip | ~622×130, y236–364, shrinks out over the 5 f ending on the entry, heading lands in its spot |
| close | blur from cut+2 f, glass card ~y1000 in x162–918, tap → Following on "follow" |

## Common mistakes

- Routing to `paper-drawer-edit` because it's paper: no grid, no seam, no drawer here — the paper
  covers his whole frame.
- Routing to `layered-head-edit` because the head is full frame: nothing lives in his shot.
- A new background per visit, a grid, or a paper that drifts or zooms.
- Two ideas in one visit, or a visit under 2.5 s — the v3 clutter.
- Fading or sliding back OUT of paper. Out is a hard cut.
- The same entry twice in a row, or every slide from the same side.
- Punch-ins, zooms or splices inside a face run.
- Any graphic drawn while the dissolve still shows his face.
- Setting the caption's words big as the paper's "idea".
- Counters that don't match the real page; invented commenter handles; stale follower counts.
- Verdicts as pills; pills over footage; a recreated app screen.
- The close card or any tag past x918, or the paper caption below y1470.

## Related

`docs/whiteout-edit-style.md` (evidence) · `asset-plan` · `shortform-cutaway` · `cut-audit` ·
`take-geometry` · `caption-align` · `sfx-design` · `mg-kit` · `screen-capture` · `reel-review`.
Sibling formats: `paper-drawer-edit` (closest), `split-screen`, `layered-head-edit`, `caption-edit`.
