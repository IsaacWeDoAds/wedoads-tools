# "Audit" reference — measured edit spec

> Studied 5 Oct 2026 from a supplied 37 s reel (Cloudflare security-audit skill, CTA "comment
> Audit"). Source + 4 fps contact sheets + frame strips at every cut + full-res stills live in
> `assets/style-refs/audit-ref/`. Every number below was measured from the 720×1280 / 30 fps
> file and is scaled ×1.5 to our 1080×1920. **Status: reference. Not built yet; confirm it on the first build.**

## Closest house formats

It is **Whiteout** (`whiteout-edit`) with a third register added. These carry over from Whiteout:
face ⟷ full-frame canvas, one idea per visit, no cuts inside a face run, splices hidden under the canvas.
**What's different from Whiteout:**

1. **Three registers, not two.** There is also a split register: a canvas on top and a face card at
   the bottom, and his head pops out above the card's top edge.
2. **Hard cut IN and OUT.** All 13 register changes are 1-frame cuts. Nothing slides or dissolves.
3. **The canvas can change per visit.** It's mostly white #FFF, but one visit is cream #F6F1EB, one is GitHub navy #0D1117, and one is a dark
   blurred enlargement of a real article screenshot.
4. **The caption style changes with the register** (§3).
5. It shares Paper-drawer's pixel mascot + "noun becomes a sticker" vocabulary, without the grid or the drawer slide.

## 1. Registers and rhythm (37.25 s, 14 segments, a change every 2.66 s on average)

| register | share | runs | what it carries |
|---|---|---|---|
| **Face**: full frame, tight framing (head ≈ 78 % of frame width) | 31 % (11.7 s) | 1.2 / 1.6 / 2.5 / 2.4 / 3.9 s | connective and opinion lines: "and it's completely free", "and it'll map out your entire app", "even prompt injection if your app uses AI…", "so only the real issues…", CTA |
| **Split**: canvas on top, face card below | 24 % (8.8 s) | 1.2 / 2.3 / 5.3 s | proper-noun intros where his face still matters: the open ("Cloudflare…"), the GitHub stars line, the long skeptic-agent explanation |
| **Canvas**: full frame, no face | 45 % (16.8 s) | 2.4 / 2.0 / 2.5 / 1.4 / 4.2 / 4.3 s | the concrete-noun proof: AI skill finds holes, the blog post, 7,000 issues, the install, the agent team, the hunt list, the report |

The sequence is S → C → F → C → C → S → C → F → C → F → S → F → C → F. Two canvases can butt
together (blog → counter at 6.87 s). The reel opens in the split at frame 0 and closes on the face.

- **Face runs are one contiguous span each.** There are no jump cuts and no punch-ins inside a run. The face framing is the
  same in every face run, and the split card framing is the same in every split run.
- **Audio:** voice only. There's no music bed (the floor drops to near-silence at every cut) and no audible SFX
  on the cuts or the MG. Integrated loudness is −14.3 LUFS. The cut is tight, with breaths removed.

## 2. The split register's face card (×1.5 → 1080)

- The card spans the full width with **rounded top corners only** (r ≈ 75 px). Its top edge is at **y ≈ 1230** and it runs to the bottom.
- **Head pop-out:** hair and head are matted and drawn *over* the card's top edge, so the hair reaches
  y ≈ 1020 on the canvas colour. It needs a person segmentation matte (house: MediaPipe selfie
  segmentation, `slice-reveal-restyle-recipe`).
- A soft grey shadow sits just above the card's top edge. The card shows his room background.
- The face is framed wider than in the face register (head ≈ 42 % of frame width vs 78 %).

## 3. Captions: three styles, one per register

All captions are word-synced, 1–3 words at a time, and swap with hard cuts (≈ 4 words/s). The placement rule is never on the face.

| register | style | position (1080) |
|---|---|---|
| face | **white bold grotesk** (SF Pro / Inter Display Bold, tight tracking), sentence case, ≈ 75 px, soft drop shadow | centre y ≈ 1340, on the shirt below the chin |
| split | same grotesk, **black on light / white on dark**, ≈ 78 px | centre y ≈ 910, in the gap between the graphic and the card |
| canvas | **heavy bold-italic condensed serif, ALL CAPS**, black (white + shadow on the dark blog visit), ≈ 96 px | centre y ≈ 1300 |

Caption extras:
- **Emphasis lockup, used twice.** A small white italic-serif word sits over a big bold-grotesk word with an
  **orange gradient fill (white→orange, top→bottom) + glow**: *completely* / **free**, *comment* / **"Audit"**.
  The serif overlaps the top of the grotesk word. The big word enters with a 3–4 f fade + slight scale.
- **Brand-colour caption:** CLAUDE CODE is set in Claude terracotta (#D97757) serif.
- **Count-up captions.** The caption counts too: "OVER 1,543 → 5,456 → 7,000", "1,544 → … → 20,000".
- **Typed ellipsis on a pause:** so → so. → so.. → so... (one dot per frame-pair).
- The serif is **heavier than our Instrument Serif**. Test Playfair Display ExtraBold Italic /
  Newsreader ExtraBold Italic against the stills.

## 4. Canvas graphics (the motion vocabulary)

Graphics are centred in **y ≈ 290–1080**, ≈ 780 px wide, with lots of white space and soft card shadows.
Something changes every ~0.5 s. Each spoken noun gets one event:

| beat | build |
|---|---|
| open (split, white) | the brand logo assembles (dots merge into the cloud, then the wordmark) on the name |
| "finds security holes in your vibe-coded app" | an illustrative app UI (login card). An orange scan line sweeps down. A "Security holes found [3]" pill appears, then red "!" callout pins pop one by one (Exposed API key / Plain-text passwords / Auth bypass) |
| "built it for themselves" | **real** article screenshot in a card over a blurred, darkened, enlarged copy of itself; an orange rough-edged **marker highlight** wipes across the title |
| "over 7,000 issues" | odometer counter with vertical-blur rolling digits ("7,000+ security issues found") above a terminal that scrolls findings |
| "20,000 stars" (split, navy) | GitHub repo card: the star fills yellow, 24k odometer, forks/watching chips |
| "install it into Claude Code" | the pixel mascot peeks up from behind a terminal; the command types; an orange marker highlight goes over the command; ✓ lines appear |
| "a team of AI agents" | 1 mascot smears into 3, they scatter and land as row icons (Logins / Database / APIs); each row's UI element gets an orange outline on its word |
| "handed to a separate agent… disprove" (split, cream) | a bug card is handed from the finder to a black "Skeptic agent". The checks Hashed? No / Encrypted? No / Test data? No tick in, then a red "Real bug – confirmed" stamp |
| "detailed report… how to fix" | report card: severity pills (Critical / High / Medium), the Verified ✓ marks tick on, then the Critical row expands to a "How to fix" diff block |

**House-rule note:** apart from the blog screenshot and the GitHub card, these graphics are
*illustrative drawn UI*, not screen recordings. That is the same licence Whiteout's "drawn UI" has.
Proof beats (a real post, real star counts) must use real captures (`screen-capture`), and every number must
be fact-checked (`fact-check-vo-claims`).

## 5. Script shape (for matching a new take)

Hook (who + what + "free") → credibility (built for themselves, the number, the stars) → install →
how it works (map → agent team → hunt list → skeptic verifier) → output (report) → comment-keyword
CTA. There's no Follow card. It ends on the face with the keyword lockup held ~2.5 s.
