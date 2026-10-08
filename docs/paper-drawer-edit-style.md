# Paper Drawer — the arena-skill explainer grammar (evidence)

> Saved 1 Oct 2026 from Nishant's own reel `arena skill(1) final upload.mp4` (48.1 s, 1080×1920,
> HEVC 30 fps, @nishantchahar.ai). He asked for this style to be learned, named and saved as a
> format skill. Skill: `.claude/skills/paper-drawer-edit/SKILL.md`. Reference files:
> `assets/style-refs/paper-drawer/` (the mp4, 24 dense sheets at 4 fps, 13 labelled stills).

**Method.** `/watch` (40 uniform frames + Whisper transcript), WhisperX word timings, a per-frame
OpenCV pass over all 1442 frames (register by bottom-band luma, seam y from the edge strips,
region frame-diffs), full-res stills for type and palette, frame strips through every
transition, and an audio pass (RMS floor, >6 kHz band envelope, spectral flatness). Every number
below is measured unless marked ≈ or *inferred*.

## 1. The structure in one line

One continuous sheet of grid paper is the world. The face card is a **drawer** under it: it
rests at y820 (split), slides down out of frame when a diagram needs the whole page, and slides
back up. Nothing else about the frame ever changes.

## 2. Numbers

| thing | measured |
|---|---|
| seam (face card top) | **y820** in 848 of 1442 frames — paper 0–820 (42.7%), face 820–1920 (57.3%) |
| face card | x0 y820 1080×1100, full-bleed, no border, no radius |
| drawer move | translateY of the whole card, **10 frames, easeInOutCubic, 1100 px**. Down trajectory: 820 828 862 945 1098 1340 1602 1770 1865 1908 1919. Up: 1918 1877 1794 1642 1400 1138 970 874 832 821 820. All 12 moves identical. |
| move vs speech | move midpoint lands **0–0.27 s before** the first word of the phrase it introduces (median ≈0.14 s) |
| opening | frame 0 = face full-frame + first caption; drawer drops 0→820 over ≈12 frames (0.07–0.43 s) |
| close | drawer rises to y0 at 46.83–47.03 s; face blurred behind a glass profile card |
| split stretches | 4.9, 4.3, 4.7, 5.1, 4.8, 4.8 s (tool-measured, between moves) |
| paper visits | 2.5, 2.7, 2.8, 2.6, 2.8, 1.3 s |
| face on screen | **62%** of runtime |
| caption pill | near-black `#090909` rounded rect, 91 px tall, centred **on** the seam (y774–865), centred x540, width follows text; text white, ≈61 px |
| paper caption | plain `#050503`, no plate, ≈72 px, centre y≈1455, centred x540 |
| caption chunks | 2–4 words, phrase-bounded, whole chunk at once (1-frame fade), no karaoke, no accent colour |
| paper | `#F1F1ED` ground, radial glow to `#FBFBFB` centre, vignette to `#E8E8E4` corners; grid **72 px pitch, 2 px lines** ≈4 luma darker |
| top-card motion | something moves in 53% of frames (>1.0 mean diff in 34%) |
| music bed | none detectable — quietest 0.3 s windows −42 dB |
| drawer SFX | *inferred*: a 130–200 ms broadband burst (flatness ≈0.5) at the move frame on most moves — a soft whoosh; confirm by ear |

## 3. Beat map (word times from WhisperX)

| t (s) | spoken | register | graphic |
|---|---|---|---|
| 0.00–0.43 | "If Claude" | full face → drawer drops | caption "If Claude gives" rides the card's top edge down |
| ≈0.4 | "gives you" | split | pixel mascot pops in, blue/yellow two-dot cursor mark |
| 1.09 | "bad answers" | split | red ✕ badge on the mascot; **BAD** caps / *answers* serif |
| ≈2.4–3.9 | "make 100 versions" | split | mascots multiply into a 10×10 grid, building diagonally |
| ≈3.9 | "of Claude" | split | black pill `100× Claude` (serif "Claude") over the grid |
| 4.65 | "fight with each other" | split | **FIGHT** in corner brackets; two mascots, crossed swords, blue spark |
| 5.43–5.73 | (breath) | drawer down | |
| 5.81–6.65 | "It's called Arena Skill." | paper | *it's called* inks in, **ARENA SKILL** caps; selection box sweeps ARENA → SKILL; real Google result card (dark) "arena skill" → GitHub result, cursor, selection box on the title |
| 7.23–8.03 | "It's completely free." | paper | green rotated rectangular stamp `100% FREE` slams |
| 8.20–8.47 | | drawer up | white chat card already on the paper |
| 8.49–9.3 | "You only use it whenever" | split | prompt bubble types "make it better" |
| 9.87–10.7 | "you're not satisfied" | split | `output.md` chip + skeleton lines; red outline stamp `NOT SATISFIED`; red progress under the card |
| 11.0–12.5 | "…output… from Claude" | split | selection box on `output.md` |
| 12.80–13.07 | | drawer down | |
| 12.92–14.2 | "So instead of asking Claude" | paper | *instead of asking…* serif + blue ↻; numbered cards "① make it better · retry", "②…" |
| 14.18–15.5 | "again and again the same prompt" | paper | **AGAIN** caps / *& again & again*; the stack grows to 6 |
| 15.73–16.03 | | drawer up | |
| 15.98–16.8 | "what it does is it" | split | lone mascot centred |
| 16.94 | "spins up" | split | mascots spiral out into rings |
| 17.58 | "100 sub-agents" | split | two rings, blue-tint pill `100 sub-agents`, centre mascot pale |
| 18.8–20.4 | "gives them the exact same task" | split | dark `task.md` chip, blue spokes to every mascot; **EXACT** *same* **TASK** lockup at the seam |
| 20.73–21.03 | | drawer down | |
| 20.98–21.7 | "but each one" | paper | `task.md` card "same for all" alone, two yellow dots |
| 21.88–22.7 | "attacks it differently" | paper | four sword mascots at the corners strike the card (yellow sparks); mono labels `logic` `brute force` `first principles` `edge cases`; *each one attacks* |
| 22.72 | "differently" | paper | ransom-note **DIFFERENTLY** — letters in mixed faces, blue accents |
| 23.83–24.13 | ON "reasoning" 23.94 | drawer up | the list lives in the split, so the drawer returns on the first item |
| 23.94–25.8 | "reasoning, workflows, strategies" | split | *different…* serif; A/B/C rows with folder icons; selection box jumps row to row |
| 26.44–29.1 | "then they compete, critique and attack each other" | split | tournament bracket, `compete` `critique` `attack` black pills light in turn, losers go pale, finalist ringed yellow |
| 29.20–29.47 | | drawer down | |
| 29.41–30.43 | "until only one survives" | paper | lone mascot with a warm glow → crown + sword + confetti; **ONLY ONE** (brackets) / *survives.*; yellow `#1 of 100` pill |
| 31.05–32.0 | "so instead of wasting time" | paper | **WASTING** + clock with sweeping red hand |
| 32.03–32.33 | ON "reprompting" 32.31 | drawer up | |
| 32.31–33.0 | "reprompting Claude" | split | mono chip "↻ re-prompting" struck through in red |
| 33.5–35.43 | "you get the best answer every time" | split | white card: green ✓, **BEST** / *answer*, yellow `#1`; *every time* ✓✓✓ |
| 35.83–37.0 | "and to set it up you just need to" | split | **SET IT UP** in brackets + black pill "① paste the link" |
| 37.13–37.43 | | drawer down | |
| 37.36–40.2 | "Claude and paste this link and then you just need to say" | paper | **PASTE** *this* **LINK** (grey → ink); REAL GitHub README install block; Claude composer card; selection box on the URL; URL lands in the composer |
| 40.23–40.53 | | drawer up | |
| 40.62–42.16 | "install the skill and it will be done" | split | composer types "install the skill"; "installing… 40%" → 100% → green ✓ DONE; composer goes pale |
| 43.74–44.34 | "just comment down Arena" | split | **COMMENT** caps; IG comment field, real avatar, "Arena" types in, blue Post |
| 44.76–45.19 | "and I'll share" | split | three stacked "@you · Arena" comment cards |
| 45.30–45.57 | | drawer down | |
| 45.73–46.77 | "all the details in your DM" | paper | *all the details* / **IN YOUR DM**; DM notification from his real handle, "Here's the Arena skill ↗", red 1 badge |
| 46.83–47.03 | | drawer rises to full frame | face blurred |
| 47.19–47.77 | "don't forget to follow" | full face (blurred) | frosted-glass profile card (real posts / followers / following), cursor taps Follow |

**What goes to paper:** the name reveal, the repeated pain, the mechanism diagram, the winner, the
cost, the setup step with the real install block, the DM promise — beats whose graphic needs the
whole page and is the point by itself. **What stays in the split:** the problem, lists and
brackets, and states that change while he explains (typing, progress, the comment).

## 4. Type (identified from full-res crops)

- **Heavy grotesk caps**, tight negative tracking (Inter Black / Neue Haas Display Black class),
  `#080808`. Hero words: BAD, AGAIN, FIGHT, ARENA SKILL, WASTING, ONLY ONE, BEST, SET IT UP,
  COMMENT, IN YOUR DM.
- **Italic serif** (Instrument Serif Italic class), lowercase, ≈0.5–0.6× the caps height:
  answers, it's called, & again & again, survives., this, every time, all the details.
- **Captions**: Helvetica / SF Pro Text class regular. **Mono**: JetBrains Mono class.
- Headlines **ink in** at final size (pale grey → black over ≈6 frames, e.g. PASTE this LINK
  37.4–37.6 s); they never slide or bounce. Stamps and stickers pop.

## 5. Palette

mascot `#D8765A` (Claude orange) · selection stroke ≈`#5D7AE5`, fill `#D0DDEF` · blue accent
≈`#3C78E0` · green `#13A046` (✓, stamp) · red `#EB2D2C` (✕, NOT SATISFIED, strike) · yellow
`#EDB312` (crown, #1) · evidence cards `#171714`–`#202228` · Follow blue `#1692F4`.

## 6. Against the house rules

| reference | house rule | resolution (in the skill) |
|---|---|---|
| headlines at y≈90–240 | text inside y220–1470 | text band y240–790 |
| labels/stamps to x≈990 | x918 rail; centre on x540, width ≤756 | centre on x540, cap width |
| captions ≈61/72 px | caption floor 78 px | default to the floor; show both in the asset plan |
| paper caption rows y1421–1490 | text floor y1470 | centre y1420 at 78 px |
| pills and chips as language | no pill chips (reel 02b) | allowed on the paper as diagram parts only |
| face leaves every ≈7 s | full-bleed alternating rejected (reel 02b v3) | allowed only as the drawer: same paper, 10-frame slide, ≤3.5 s visits |
| glass profile close | Follow close every reel | the glass card is this format's Follow close |

## 7. What I could not determine

- Whether the drawer whoosh is a library file or a generated swish (spectrum only; no ear).
- Exact caption font (Helvetica Neue vs SF Pro Text) — both read identically at this size.
- Whether the Google/GitHub cards are live captures or screenshots with a synthetic cursor.
