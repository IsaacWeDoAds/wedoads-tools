# Whiteout — the evidence

> Measured 1 Oct 2026 off `assets/style-refs/whiteout/find-skills-final.mp4` (his own tools-account reel,
> "find skills", 51.3 s, 1080×1920, 30 fps, HEVC). Dense sheets at 6 fps live beside it in `sheets/`.
> The skill that applies this is `.claude/skills/whiteout-edit/SKILL.md`; this file is the evidence
> behind its numbers. Method: per-frame paper-pixel fraction (luma > 215 and saturation < 30 on a
> 108×192 downscale), per-column halves for wipe direction, frame-to-frame mean abs diff for cuts and
> motion, Haar face boxes per segment, full-resolution stills for type and colour.

## 1. The shape in one line

A clean full-frame talking head keeps handing the whole frame to a warm paper-white canvas, where one
idea at a time plays as kinetic type and drawn UI, then hard-cuts back to him.

## 2. Register timeline (frame-exact)

| # | register | in → out (s) | dur | entry | exit |
|---|---|---|---:|---|---|
| F1 | face | 0.00 → 1.73 | 1.73 | — | — |
| P1 | paper | 1.73 → 6.60 | 4.87 | **slide from right**, 6–7 f | hard cut |
| F2 | face | 6.60 → 9.03 | 2.43 | | |
| P2 | paper | 9.03 → 12.27 | 3.23 | **dissolve**, 3 f + "#1" blur-slam | hard cut |
| F3 | face | 12.27 → 14.13 | 1.87 | | |
| P3 | paper | 14.13 → 16.70 | 2.57 | **slide from left**, 6–7 f | hard cut |
| F4 | face | 16.70 → 18.47 | 1.77 | | |
| P4 | paper | 18.47 → 23.20 | 4.73 | **dissolve**, 5 f | hard cut |
| F5 | face | 23.20 → 25.63 | 2.43 | | |
| P5 | paper | 25.63 → 31.30 | 5.67 | **slide from right**, 6–7 f | hard cut |
| F6 | face | 31.30 → 34.73 | 3.43 | (handoff chip above the hair at 32.2) | |
| P6 | paper | 34.73 → 38.87 | 4.13 | **dissolve**, 3 f | hard cut |
| F7 | face | 38.87 → 41.83 | 2.97 | | |
| P7 | paper | 41.83 → 45.80 | 3.97 | **slide from left**, 6–7 f | hard cut |
| F8 | face | 45.80 → 46.57 | 0.77 | | |
| P8 | paper | 46.57 → 49.60 | 3.03 | **dissolve**, 5 f | hard cut |
| F9 | face (close) | 49.60 → 51.30 | 1.70 | background blur + profile card | — |

- **Paper 32.2 s = 63 % of runtime; face 19.1 s = 37 %.** 8 paper visits, 9 face runs.
- **Paper visit median 4.0 s** (2.57–5.67). **Face run median 2.0 s** (0.77–3.43).
- **16 register changes in 51 s = one every 3.2 s.**
- **Entries alternate strictly: slide, dissolve, slide, dissolve…** and the slides alternate sides
  (R, L, R, L). No entry type repeats back-to-back.
- **Every exit is a 1-frame hard cut** (frame diff 121–183 on a single frame, 8/8). Nothing
  animates out.
- **5 of 8 visits settle before the exit:** a fully static tail of 0.33 / 0.67 / 0.43 / 0.50 /
  0.37 s (frame diff = 0.0). The other three cut while still moving.

### Entry mechanics

- **Slide (cover):** the paper panel travels in from one side over a *static* face — the face is
  not pushed. The panel's own content rides with it (the "2,34…" counter is offset by the
  panel's edge position mid-move). Coverage per frame (normalised to the settled frame):
  47 / 75 / 89 / 96 / 99 / 100 % — a hard vertical edge, **easeOutQuart over 6–7 frames**, reading
  as done in 4.
- **Dissolve:** the paper fades in over the still face, ease-out. P4 and P8: 41 / 79 / 93 / 98 /
  100 % (5 f). P6: 67 / 87 / 97 % (3 f). P2: 61 / 83 / 93 / 97 / 99 % with a "#1" blur-slam
  (scale ≈ 1.3 → 1, blur → 0 over ~3 f). The hero graphic of a dissolve arrives **blurred and
  sharpens** (the "#1", the "Security audit" heading).
- **Defects in the reference:** on P2 the blurred "#1" is drawn while the dissolve still shows his
  face (f271–272), and on P8 the comment composer is drawn while his face still shows through
  (≈ 46.5 s). House rule: no graphic over the face in any frame. The skill starts the graphic
  only once the paper is ≥ 93 % opaque.
- **Cross-check:** an independent no-skill pass (frame analysis by a separate agent) measured the
  same 8 visits (paper 62.5 %, visits 2.53–5.67 s), the same alternation and the same 8/8 hard-cut
  exits.

## 3. Face register

- Full frame, `cover`, no scale change: face box width 500–610 px (≈ 50 % of frame width) in every
  run after the hook. **No punch-ins, no jump cuts inside a face run** (max in-run frame diff 21 —
  gestures only). Whatever cutting happened is hidden under paper visits.
- **Hook exception:** F1 opens wider with a prop (laptop in hand, smiling, pointing) and he leans in
  (face box 365 → 540 px over 1.5 s). That is performance, not a zoom — the edit does nothing.
- **Face runs carry the caption only,** plus once (F6) a white rounded label with a black shield
  icon — "Security audit", ≈ 622×130 px, centred x538, y234–365, ~25 px above his hair. It pops in
  on its word (32.2 s), holds, **shrinks out ~5 frames before the dissolve**, and P6's heading
  lands **in the same spot** and grows to full size — continuity by position across the boundary.

## 4. Paper register

- **Background (sampled full-res, identical across all 8 visits):** radial warm off-white —
  centre `#F9F9F6`, upper corners `#ECECE7`, bottom `#DFDFDA`. **No grid** (column std 0.03) —
  the sibling paper-drawer reel has a 72 px grid; this one is plain. One canvas for the whole reel.
  **No yellow anywhere.**
- **Ink** `#090909`. **Selection / tag blue** `#2E78F2` (selection box on a word `#3777E4`).
  **Folder blue** `#60B2F4`. **Status:** safe `#13A046`, alerts `#EE9B0F`, high risk `#EB2C2C`.
  Claude dot `#D97757`-class orange on the prompt card.
- **Motion:** 24–100 % of frames inside a visit change (median ~55 %); every spoken noun in a
  visit gets an event.

### Beat map (what each visit shows)

| visit | spoken | on the paper |
|---|---|---|
| P1 1.73–6.60 | "almost 10,000 Claude skills… skills for coding, research, writing" | counter races 7 → 6,960 → 9,490 → **10,000** (1.7–2.2 s) as blue folders burst outward; "CLAUDE SKILLS" letter-bead row types in beneath; the real skills.sh leaderboard card rises tilted from the bottom. At 3.5 s the stack pushes up out of frame; "Skills for" + a folder-icon list types in one item per spoken word, a selection box jumping to the live word (3.9 / 4.8 / 5.8). |
| P2 9.03–12.27 | "is called Find Skills, and it has over 1.5 million installs" | huge blurred **#1** focus-pulls sharp, shrinks to the top; "Find Skills" types with a selection box and a cursor; the real find-skills card rises; an installs badge counts 0.7M → 1.3M → 1.5M+. |
| P3 14.13–16.70 | "Save this reel because I know you are going to forget this" | a bookmark outline draws and fills; **SAVE** + serif italic "this reel"; SAVE collapses into an "I know" black pill; "you're going to" blue pill; **FORGET** drops in letter by letter, then the letters tumble off. |
| P4 18.47–23.20 | "…and it will find the best skill for that job. So instead of guessing which skill…" | Claude prompt card types "Make me a pitch deck for my startup"; six folder tiles pop, a magnifier scans them; a "✓ BEST MATCH" tag lands on pptx and the rest dim; the stack flies up; "?" marks scatter round a huge **guessing** while junk-filename chips pop around it ("skill-final.md", "skill-v2 (1)", "best-skill??", "untitled-skill", "maybe-this-one", "SKILL copy.md"). |
| P5 25.63–31.30 | "One thing that most people do and then regret is they just go on GitHub and install random skills." | rotating ring text "ONE THING MOST PEOPLE DO •" with a "most people" pill at its centre; serif italic "and then…"; **REGRET** builds; the ring zooms through the frame to reveal a big blue folder; "github.com/ random /skills" pill; warning-file chips burst out of the folder ("totally-safe.sh", "free-tokens.md", "auto-run.py"…); "random skills" with a selection box. |
| P6 34.73–38.87 | "It shows what's safe, what has alerts and what has high risk" | the **Security audit** heading lands where the face-run chip was and grows; three rows slide in staggered (find-skills / auto-deploy-kit / free-api-keys, mono names); a blue scan line sweeps each row; a badge lands on each spoken word — ✓ SAFE, ! ALERTS, ✕ HIGH RISK with a red row outline. |
| P7 41.83–45.80 | "Claude is going to find the skills whatever you want. It will install it for you." | the real find-skills page card rides in on the slide; "You → Claude → skill ✓" flow pills fill blue one by one; a dark terminal card types `$ npx skills add find-skills` → `✓ installed`. |
| P8 46.57–49.60 | "…to comment skills, I'll share you all the details in your DM" | his comment composer types "skills" and Post lights; a stack of other people's "skills" comments piles up above it; a paper-plane icon draws with a red "1" badge; **your DM** with a selection box on DM. |
| F9 49.60–51.30 | "And don't forget to follow." | hard cut to the face, which blurs and darkens behind a glass profile card (avatar, handle ✓, bio, 913 / 238K / 196, blue Follow) rising from the bottom; a cursor taps Follow → "Following ✓". |

### Type voices on the paper

| voice | spec | use |
|---|---|---|
| display | heavy grotesk, very tight tracking (Inter Display Black class, ≈ −5 %), ink | the one idea: "Skills for", "SAVE", "#1", "Security audit", "guessing", "your DM" — cap height 100–350 px |
| accent | serif italic, lowercase | the tone word under a display word: "this reel", "and then…" |
| mono | JetBrains Mono class, bold | filenames, repo slugs, terminal |
| UI | Inter Medium class | prompt text, row sub-labels |
| pills | black `#0A0A0A` / blue `#2E78F2`, white text | short tags: "I know", "most people", "you're going to", "✓ BEST MATCH", "Claude" |
| selection box | 3 px blue border, ~18 % blue fill, round handles at two corners, optional cursor | marks the spoken keyword |

## 5. Captions

- Neutral grotesk Regular (reads as SF Pro Text / Helvetica; x-height ÷ cap height ≈ 0.74),
  **≈ 75 px** (cap ≈ 53 px, 56 px ascender-to-baseline), sentence case, punctuation kept,
  **2–4 words per chunk (≈ 0.78 s each), replacing**. No plate, no karaoke, no accent, no hero word.
- **Entry: 5 frames, easeOutCubic** — opacity 0 → 23 / 66 / 85 / 98 / 100 %, rising ~11 px,
  blurred → sharp. The outgoing chunk disappears instantly.
- **Two positions:** on the face white + a faint shadow, centre **y ≈ 1302** (cap top 1274,
  baseline 1329, ~170 px under the chin box); on the paper `#0A0A0A`, centre **y ≈ 1492** (top 1464,
  baseline 1519). Centred on x≈540. At a register change the live chunk jumps to the new
  position and colour on the first frame. Captions run through every register.

## 6. Hook (0–5 s)

Face with a prop and a smile for 1.73 s (two caption chunks), then the first slide lands on the
number. Events in the first 5 s: caption 0.0, caption 0.5, slide 1.73, counter 1.8–2.2, folder
burst 2.0, beads 2.2–2.6, caption 3.0, push-up 3.5, heading 3.7, list items 3.9 / 4.8 — **≈ 11
events, one every ~0.45 s**, which matches the house hook-density rule.

## 7. CTA and close

- **CTA:** comment composer typing the trigger word → a pile of other people's comments with the
  same word (invented handles) → a paper-plane icon with a red `#FC2A3C` "1" → "your DM".
- **Close:** hard cut to his face; from ~1 frame after the cut a gaussian blur (~30–35 px) and a dim
  ramp over ~8 f; a frosted-glass profile card springs up over ~8 f with overshoot (avatar,
  nishantchahar.ai ✓, "Nishant Chahar | AI Agents & Coding", 913 / 238K / 196, bio, blue Follow);
  a cursor taps Follow ~21 f after the card starts → "Following ✓", held ~0.85 s. **Final card
  x80–1000, y644–1340 (centre y≈992)** — its text reaches x≈940.

## 8. Sound

- Integrated **−8.6 LUFS**, LRA 2.4 LU — an IG-loud, heavily compressed export (house target is
  −14 LUFS).
- No beat detected (onset autocorrelation peak 0.06). Nothing in the measurement proves a music
  bed or proves which transitions carry SFX: high-band bursts sit near several entries (+20 to
  +36 dB over the median) but speech sibilants blur that test. The house SFX-only rule applies.

## 9. What the reference does that the house forbids

| in the reference | house rule | fix in the skill |
|---|---|---|
| a 5-frame dissolve into paper | `register-crossfades-banned` | kept only over one continuous, unspliced face shot with no graphic until paper ≥ 93 %; shown to him in the asset plan, hard-cut fallback |
| "#1" (P2) and the comment composer (P8) drawn while the dissolve still shows his face | no graphic on the face in any frame | the graphic starts once paper is ≥ 93 % opaque |
| face full-frame ⟷ paper full-frame | 02b v3 "full-bleed alternating" rejected | licensed for this format by name; one canvas, one idea per visit, no in-run cuts, a visit every ~6 s |
| verdict badges as rounded pills; phrase pills | `stamps-not-pills` | verdicts become rectangular stamps; phrase pills on paper only, as diagram parts (same call as `paper-drawer-edit`) |
| "✓ BEST MATCH" tag runs off the left edge (x = 0); close-card text to x≈940 | text inside x35–918, centred on x540 | everything centred on x540, ≤ 756 px wide |
| paper caption centre y1492 (baseline 1519) | text floor y1470 | paper caption centre y1420 |
| captions ≈ 75 px | caption floor 78 px | 78 px |
| installs counter lands on "1.5M+" beside a real card that reads "3M installs" | real numbers only; the frame may not contradict itself | counters land on the real card's number, fact-checked in the asset plan |
| social-proof comments from invented handles | no fabricated records | "@you · WORD" cards |
| dimmed tile labels ≈ 34 px mono | in-card mono ≥ 36 px | 38 px floor |
| close blur starts on cut + 1 f | nothing animates across a cut | blur starts at cut + 2 f |
| −8.6 LUFS, +1.1 dBTP | −14 LUFS, ≤ −1 dBTP on the encoded file | loudnorm as always |
