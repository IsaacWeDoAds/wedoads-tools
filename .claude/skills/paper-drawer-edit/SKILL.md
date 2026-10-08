---
name: paper-drawer-edit
description: "Use when he asks for the arena-skill look, 'the paper drawer', 'the one with the pixel mascots on grid paper', 'where my face slides away and comes back', or any 9:16 tools-account explainer whose idea (agents, a workflow, how a skill or tool works) must be DRAWN as a diagram rather than shown as a screen recording, with the face leaving the frame for the diagram beats. Not for recording-led demos (split-screen), 'just captions' (caption-edit), or graphics inside his shot (layered-head-edit)."
---

# PAPER DRAWER — the arena-skill explainer grammar

> **THE JOB:** one sheet of grid paper is the whole world. His face card is a **drawer** under
> it: it rests at y820, slides down out of frame when a diagram needs the whole page, and slides
> back up when he is the point. Every noun he says becomes a flat sticker on the paper, and the
> page explains itself with a design-tool vocabulary: selection boxes, handles, a cursor.

**Named 1 Oct 2026** from his own reel `arena skill(1) final upload.mp4`, which he asked to have
learned and saved as a format. Reference: `assets/style-refs/paper-drawer/` (the mp4, 24 sheets
at 4 fps, 13 labelled stills including both transition strips). Evidence, beat map and every
measurement: `docs/paper-drawer-edit-style.md`. **Sample the sheets before building**
(`sample-named-reference-first`).

**Five defaults this skill replaces** (a no-skill agent picked every one of them):

| a no-skill agent picks | the reference is |
|---|---|
| 60-40 split: inset card y100, caption lane y726–870, face card x36 y870 1008×1050 | **seam y820**, face card **full-bleed 1080×1100**, no lane; the caption pill sits **on** the seam |
| a 16-frame drawer reusing the split↔full preset | **10 frames, easeInOutCubic, 1100 px** |
| `#F7F7F7` paper, a 54 px grid that drifts | `#F1F1ED` with a centre glow and corner vignette, **72 px grid, static** |
| Space Grotesk Bold ink captions with a yellow highlighter band | two plain voices: **white on a black pill** in the split, **plain black** on paper; no accent |
| Times italic hero plus a tracked kicker; open in the split at frame 0; FollowCta close | **Inter Black caps + Instrument Serif italic lockups**; **open full-face and drop the drawer**; **glass profile card** close |

He asked for this style, so the drawer slide is approved **in this format**. It is not a third
general split↔full preset; don't import it into `split-screen` reels.

## Why this isn't the rejected full-bleed alternating layout

Reel 02b v3 swapped face full-frame and evidence full-frame on hard cuts, and he rejected it:
*"clutter… the focus is shifting so frequently."* The drawer passes because:

1. **The ground never changes.** The paper in the top card IS the full-page paper. Only the
   drawer moves, so the eye has nothing to re-find.
2. **The move is a 10-frame physical slide, not a cut.** Opacity never changes, so
   `register-crossfades-banned` still holds.
3. **The face owns 62% of the runtime**, and every paper visit is short (≤3.5 s) and comes back.

Build it with hard cuts, a different background per register, or a paper that scrolls or zooms,
and you have rebuilt v3.

## 1. Geometry (1080×1920)

```
PAPER          full frame, always underneath, never moves
SEAM           y820   paper 0–820 (42.7%) · face 820–1920 (57.3%)
FACE CARD      x0 y820 1080×1100, full-bleed, no border, no radius
CAPTION PILL   centred ON the seam: y774–865 (seam −46/+45), centred x540
PAPER CAPTION  (drawer away) centre y1420, centred x540 (reference 1455 at 72 px already
               dips to y1490; at 78 px, y1420 keeps descenders above the y1470 text floor)
TEXT BAND      top card y240–790 · paper page y240–1380
```

- **Face fit: tight headroom.** The hair sits 60–130 px under the seam and ≥20 px below the
  pill's bottom edge (y865). Solve `FACE_FIT` for the 1080×1100 card with `take-geometry`; don't
  nudge. The pill overlaps the face card's top 45 px, so run the alpha face guard across it.
- **The face card jump-cuts plainly** at sentence breaks: same framing, no punch-in, no zoom.
  The reference shows 3 visible cuts, at 26.40, 35.77 and 36.53 s. Most cuts hide under a
  paper visit: put the cuts you can't avoid there.

## 2. The drawer — the only transition

| | spec |
|---|---|
| what moves | the whole face card translates, and its content moves with it. It is not a mask reveal. |
| curve | `Easing.inOut(Easing.cubic)` over **10 frames** at 30 fps (0.33 s) |
| travel | 1100 px: 820 → 1920 going away, 1920 → 820 coming back |
| measured path | 820 828 862 945 1098 1340 1602 1770 1865 1908 1919 (all 12 moves identical) |
| timing | the move's **midpoint lands 0–0.27 s before** the first word of the phrase it introduces (median 0.14 s), so the register has settled as the word lands |
| where | in the breath between sentences. The exception: return **on** a list's first item when the list lives in the split (reference 23.94 s: back up on "reasoning" for the A/B/C rows). |
| the caption | the pill rides the card's top edge out; the paper caption takes over at the next phrase's first word |
| the graphics | the outgoing top-card graphic holds until the drawer clears, then the page clears and the paper beat builds. On the return, the next split graphic is **already on the paper** before the drawer starts rising: never an empty card. |
| sound | a soft whoosh peak-aligned to the midpoint (`sfx-design`) |

**Open:** frame 0 shows the face **full-frame** (drawer at y0) with the first caption on its top
edge. The drawer drops 0 → 820 over ~12 frames (0.07–0.43 s) and the first sticker pops at
~0.4 s. **Close:** the drawer rises all the way to y0 and the face blurs behind the glass
Follow card (§8).

## 3. Cadence

| | reference | build to |
|---|---|---|
| split stretches | 4.3–5.1 s | 4–6 s, never over 6 s |
| paper visits | 2.5–2.8 s (last one 1.3 s) | 2–3.5 s |
| visits | 6 in 48 s, one every ~6.7 s | ~1 per 7 s |
| face on screen | 62% | 55–70% |
| top-card motion | something moves in 53% of frames | ≥50%, plus a new element every caption chunk (~0.7–1 s) |

**Paper takes** the beats whose graphic needs the whole page and is the point by itself:

- the NAME reveal, with a real search-result card
- the repeated PAIN (the stack of retries)
- the MECHANISM diagram (four corners attacking one file)
- the WINNER, and the COST (the clock)
- the SETUP step with the real install block
- the DM promise

**The split keeps** the problem, the lists and brackets, and any state that changes while he
talks: typing, progress bars, the comment box.

## 4. The paper

- Ground `#F1F1ED`, a radial glow to `#FBFBFB` at the centre, and a vignette to `#E8E8E4` in the
  corners.
- Grid: **72 px pitch, 2 px lines**, about 4 luma darker than the paper, fading with the vignette.
- The same paper in both registers. It never scrolls, drifts or zooms: the grid is the continuity.

## 5. Sticker vocabulary

Everything is flat. Cards take soft drop shadows; the creature takes a white sticker outline. The
diagram is literal: **every noun becomes an object and every verb happens to it** (multiply,
orbit, fight, eliminate, crown).

| sticker | spec |
|---|---|
| **the creature** | Pixel-art stand-in for the AI: `> <` eyes, four legs, white outline. Claude reel = `#D8765A`; **other topics take the tool's own brand colour** (`topic-led-look-per-reel`). It must be the page's one saturated colour. A monochrome brand (Cursor, Vercel) gets its mid-grey with a dark outline, never pure black: a black creature reads as type next to the caps. It pops in, multiplies (1 → a 10×10 grid → rings), fights (crossed swords + spark), goes pale when eliminated, and wears a crown with confetti when it wins. |
| **selection box** | Figma-style: ~2 px `#5D7AE5` stroke, `#D0DDEF` translucent fill, round handles on two opposite corners. It sweeps across a word or element **as he says it** (ARENA SKILL, "reasoning", `output.md`, the URL). This is the signature highlight: use it instead of underlines or marker. |
| **stamps** | Rectangular, rotated −6…−10°, slammed on the word: solid green `100% FREE`, red-outline `NOT SATISFIED` (`stamps-not-pills`). |
| **UI cards** | White rounded cards: a chat bubble (black pill "make it better"), an `output.md` chip with grey skeleton lines, a Claude composer, a comment box, a DM notification with a red 1 badge, and an "installing… 40% → 100%" bar ending in a green ✓ DONE. |
| **real evidence cards** | Dark rounded cards carrying a **real** capture (a Google result, a GitHub README install block), animated by a selection box and cursor. Capture live (`screen-capture`, `logged-in-app-capture`); mocked screen recordings are banned. |
| **mono chips** | JetBrains Mono in outlined rounded rects: `task.md`, `logic`, `brute force`, `first principles`, `edge cases`. |
| **pills** | Black 999-radius verb pills (`compete` `critique` `attack`), a blue-tint count pill (`100 sub-agents`), a black `100× Claude` with a serif word, and yellow rank badges (`#1 of 100`, `#1`). |
| **structures** | A tournament bracket (lines draw, losers go pale, the finalist is ringed yellow), orbit rings, spokes from a centre file to every agent, a numbered card stack ("① make it better · retry" to ⑥), and A/B/C rows with folder icons. |
| **symbols** | A red ✕ badge, green ✓, a blue ↻, a clock with a sweeping red hand, primary-colour confetti, and a struck-through chip (`↻ re-prompting` with a red strike). |

## 6. Type

| voice | spec |
|---|---|
| **display caps** | Inter 900, letter-spacing ≈ −0.06em, `#080808`, hero cap height 150–200 px: BAD, AGAIN, FIGHT, WASTING, ONLY ONE, SET IT UP, COMMENT |
| **italic serif** | Instrument Serif Italic, lowercase, 0.5–0.6× the caps: *answers*, *it's called*, *& again & again*, *survives.*, *every time* |
| **lockups** | serif over caps (*it's called* / ARENA SKILL), caps over serif (BAD / *answers*), inline (PASTE *this* LINK, EXACT *same* TASK) |
| **corner brackets** | viewfinder ⌜ ⌟ around a headline on command beats: FIGHT, ONLY ONE, SET IT UP |
| **ransom word** | at most one per reel: each letter in a different face and colour (DIFFERENTLY) on that exact word |
| **mono** | JetBrains Mono: files, labels, progress text, ≥36 px (`phone-scale-type-floor`) |

**Headlines ink in:** set at final size in pale grey, they darken to black on their word over
~6 frames. They never slide, bounce or scale. Stamps and stickers may pop.

All fonts are already loaded in the repo (`@remotion/google-fonts/Inter`, `InstrumentSerif`,
`JetBrainsMono`).

## 7. Captions — one voice per register

| register | look | position |
|---|---|---|
| split | white Inter 500 on a `#090909` rounded rect (radius ~14, ~24 px side padding), sentence case, punctuation kept | pill centred on the seam y820 and on x540; width follows the text |
| paper | plain `#050503` Inter 500, no plate | centre y1420, centred x540 (descenders ≤ y1470) |

- 2–4 words per chunk, phrase-bounded. The whole chunk appears at once (1-frame fade): no
  karaoke, no word-by-word build, no accent colour.
- **Size:** the reference measures ≈61 px (pill) and ≈72 px (paper), below the house **78 px
  floor**. Build at 78 px and put one still at each size in the asset plan. He picks; don't
  decide silently.
- Timing, full coverage and the pause audit are owned by `caption-align`.

## 8. Hook, CTA, close

**Hook (measured):**

| t | event |
|---|---|
| 0.0 | face full-frame + first caption |
| 0.07–0.43 | the drawer drops |
| 0.4 | the creature pops |
| ~1.0 | ✕ badge + BAD / *answers* on "bad" |
| 2.4–3.9 | creatures multiply to a 10×10 grid on "100 versions" |
| ~3.9 | `100× Claude` pill |
| 4.65 | FIGHT in brackets + swords on "fight" |
| 5.6 | the first drawer move goes to the NAME reveal |

That is an event every 0.6–0.8 s, and **the name is withheld until ~6 s**. What's withheld is
the *thing being revealed* (the skill, the feature, the repo). If he says a household brand
early ("Cursor's new…"), its real mark still lands on that word (`brand-logo-marks`).

**CTA:**

- **COMMENT beat** (split): COMMENT caps, then an IG comment field with his **real** avatar.
  The trigger word types in, then three "@you · WORD" cards stack. This is the house
  `cta-comment-composer`: reuse it.
- **DM beat** (paper): *all the details* / IN YOUR DM, plus a DM notification from his real
  handle with a red 1 badge.

**Close:** the drawer rises to full frame and the face takes a gaussian blur (~30 px). A
frosted-glass profile card rises over it: avatar, verified tick, name and bio, **real** posts,
followers and following, and a blue Follow button. A cursor enters and taps Follow on "follow".
This is this format's Follow close (non-negotiable 9); it replaces the FollowCta split. Keep the
card inside x162–918.

## 9. Sound

No music bed (gap floor −42 dB): SFX only, per the house rule.

| event | sound |
|---|---|
| every drawer move | soft whoosh (the reference shows a 130–200 ms broadband burst at each move) |
| each sticker or stamp | pop |
| each typed character | tick |
| each selection box, cursor press and the Follow tap | click |
| the winner's confetti | short swell |

Peak-align everything (`sfx-design`) and deliver −14 LUFS on the encoded file.

## Where the reference breaks a house rule — build it this way

| the reference does | house rule | build it as |
|---|---|---|
| headlines at y≈90–240 (FIGHT, COMMENT, SET IT UP) | text inside y220–1470 | top-card text band y240–790: shrink the diagram, not the band |
| labels and stamps reach x≈990 | x918 rail; centre on x540 (`center-text-on-frame`) | centre every block on x540, width ≤756 |
| captions ≈61/72 px | caption floor 78 px | 78 px by default, both shown in the asset plan (§7) |
| paper caption centre y1455, dipping to y1490 | text floor y1470 | centre y1420 |
| rounded pills and chips as language | no pill chips (reel 02b), `stamps-not-pills` | pills allowed **on the paper as diagram parts**, never over footage or a capture; verdicts stay rectangular stamps |
| the face leaves every ~7 s | full-bleed alternating rejected | only as the drawer: same paper, 10-frame slide, ≤3.5 s visits |
| glass profile card close | every reel ends on the Follow close | the glass card IS the Follow close here |

## Pipeline hooks

- **Asset plan** (`asset-plan`), listing:
  - every paper visit: its line, its diagram, and why it needs the whole page
  - the creature and its colour
  - every real capture the evidence cards need
  - the caption-size stills

  Get his yes.
- **Cut** (`shortform-cutaway` → `cut-audit`): plan jump cuts to fall inside paper visits. Drawer
  moves are data, not taste: `move midpoint = first word onset − 0.14 s`, emitted with the cut
  (`register-map-generated-with-cut`).
- **Geometry** (`take-geometry`): `FACE_FIT` for 1080×1100 at seam 820, hair 60–130 px under it.
- **Build:** check `mg-kit` first for the comment composer, real logo marks and the hero layer.
- **Review** (`reel-review`):
  - `review_reel.py … --card 1080:820:0:0` measures motion on the paper card
  - `python3 .claude/skills/paper-drawer-edit/measure_drawer.py OUT.mp4` checks the seam, the
    register runs, move lengths and face share against the reference (the reference reads seam
    y820, moves 8–9 f, face 62%)
  - still-sample every move's midpoint frame

## Quick reference

| thing | number |
|---|---|
| seam | y820 · face card 1080×1100 full-bleed |
| drawer | 10 f · easeInOutCubic · 1100 px · midpoint 0–0.27 s before the word |
| cadence | split 4–6 s · paper 2–3.5 s · ~1 visit / 7 s · face 55–70% |
| paper | `#F1F1ED`, glow `#FBFBFB`, vignette `#E8E8E4` · grid 72 px / 2 px, static |
| split caption | white on `#090909` pill, y774–865 on the seam, x540 |
| paper caption | `#050503`, no plate, centre y1420 (reference 1455) |
| caption size | reference ≈61/72 px · house floor 78 px (his call) |
| chunks | 2–4 words, whole chunk at once, no karaoke |
| display | Inter 900 −0.06em caps + Instrument Serif Italic · ink-in ~6 f |
| selection box | `#5D7AE5` stroke, `#D0DDEF` fill, 2 corner handles |
| creature | pixel sprite, topic brand colour (`#D8765A` for Claude) |
| open / close | full-face → drop in 12 f · rise to full-face + blur + glass Follow card |

## Common mistakes

- Routing to `split-screen` and inheriting its 60-40 geometry, caption lane and FollowCta.
- Hard-cutting between the split and the paper, or fading the face card.
- A mask reveal instead of a translate, a linear curve, or a 16-frame move.
- A different ground in the paper register, or a paper that drifts or zooms.
- Moving the drawer mid-phrase for no reason. It moves in the breath, except to land a list item.
- Karaoke or yellow accent captions, or putting the split caption in a lane instead of on the seam.
- Headlines that slide or bounce in: they ink in place.
- Abstract icons standing in for the diagram. The creature does the verb.
- A mocked UI inside a "real evidence" card.
- Showing the tool's name before ~5 s.
- Copying the Claude-orange creature onto a non-Claude topic.

## Related

`docs/paper-drawer-edit-style.md` (evidence) · `asset-plan` · `take-geometry` ·
`screen-capture` · `caption-align` · `sfx-design` · `mg-kit` · `reel-review`. Sibling formats:
`whiteout-edit` (closest: plain paper with no grid, which covers his whole frame — no drawer, no
seam), `split-screen`, `caption-edit`, `layered-head-edit`.
