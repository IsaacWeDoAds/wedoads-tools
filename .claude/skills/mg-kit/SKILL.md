---
name: mg-kit
description: "REUSE BEFORE BUILDING — the motion-graphics component library on the SSD (three kits: the lf01 long-form system, the whole 9:16 reels system across 56 reels, and four standalone Remotion projects) plus the saved house lockups: TextHook, FollowCta, SplitToFull, CaptureCard, Logos, CardReel, the CTA comment composer, the hero layer, and the approved font pairings. Use BEFORE designing any new graphic, and whenever an edit needs a stat strip, typed list, chapter card, brand lockup, logo chip, CTA widget, or text hook."
---

# MG KIT — reuse before you build

> *"export all the motion graphics that we have created in some editable files so that, if we want
> to use similar motion graphics for our future videos, we can reuse these… save them in the SSD."*

**Start here, not from scratch.** Copy the component, keep the cue lines, change the copy and the
anchors.

## Where it lives

**`<media-drive>/MG-Kit/`** — the root `README.md` indexes three kits.

### 1. `lf01-longform-2026-09/` — the 16:9 long-form kit

- **`src/LF01/`**
  - `heroes.tsx` — intro box, title, chapter, typed `list`; **strip heroes** (agi, arc, hiring,
    expcert, bets, gtm, users, onboarding, roles, hours, loop, leetcode); **lane heroes** (creds,
    brand, cloud, timeline, progress, cta)
  - `Final.tsx` — Lockup voices (word / mono / script / ui), LineLockup, Stamps, Montage
  - `apple.ts` tokens · `fonts.ts` · `gen_data.py` (the cue API: `hero() / emph() / stamp()`,
    anchored to spoken words) · `data.ts` sample
- **`alpha-clips/type/`** — 67 ProRes 4444 alpha windows of the finished text layer;
  **`alpha-clips/fulls/`** — 15 opaque cards. `INDEX.md` says what each clip contains + its source
  second; `CONTACT-*.png` to browse.
- **`pipeline/`** — the Palmier layering tooling (render, plan, place, segments, preimport, retype,
  review).
- **`sfx/`** — skill one-shot kit + cue design + library index. **`prompts/`** — Omni/Veo prompt
  files + plan. **`stills/`** — QA stills and composited review sheets.
- `ASSET-PLAN-lf01.md` — the full decision log.

### 2. `reels-9x16-2026-07-09/` — the whole short-form system

The repo stays the working source; this is the portable copy.

- `src/<ReelNN>/` for **56 reels** (Final.tsx + data.ts + bespoke gfx/mg files; `CATALOGUE.md` lists
  them)
- `src/components/` — **SplitToFull, FollowCta, TextHook, CaptureCard, CardReel, Logos**, the
  `onda/` primitives · `src/lib/onda` · `src/theme`
- `design-assets/<reel>/` — **15 Claude Design HTML assets + their recordings**
- `docs/` — reel-edit-styles, Hinglish style, personal-account guidelines, Omni treatments
- `refs/` — logos, text-hook refs, carousel refs

### 3. `other-remotion-projects/`

`ai-simplified-c0857` (episode graphics: KnowledgeCutoff, RagHook, HrPolicyGap,
HallucinationContext, OpenBook + rendered mp4s), `bengaluru-valley` (isometric map),
`bangalore-unicorn-map`, `trymiles-launch`. **node_modules excluded — `npm install` before
rendering.**

## The house components (in-repo, `src/components/`)

| Component | What it is | Non-obvious rule |
|---|---|---|
| **`SplitToFull.tsx`** | `useSplitToFull` / `useFullToSplit` — the only sanctioned register transitions | Takes `fromFit`/`toFit` so the un-zoom lands exactly on the next framing. See `split-screen` |
| **`FollowCta.tsx`** | Follow→Following end card; also `FollowCtaSolo` for transparent ProRes | Real numbers only. Flip at `startAt + 20`. Scale 0.85 into the card zone |
| **`TextHook.tsx`** | The saved three-line text hook lockup | The COPY is not the style — see below |
| **`CaptureCard.tsx`** | Screen capture in-card, with `srcX/srcY` source-pixel framing | Always pass `srcX/srcY` when zooming, or a centre crop clips left-aligned pages |
| **`Logos.tsx`** | `XMark`, `RedditMark`, `YouTubeMark`, `GitHubMark`, `LinkedInMark`, `ClaudeMark`, `InstagramMark` — inline SVG, `{size, color}` | Size is the rule, not presence — see below |
| **`CardReel.tsx`** | The personal-account card format | With `cardkit.py`. See `broll-style-edit` |

## The text hook lockup

> *"I like this text hook style. Copy this for future videos, save it."*

Three lines, measured (**headline cap height = 1u**):

| line | what | face | size | placement |
|---|---|---|---|---|
| **kicker** | `day 3 of building AI tools` | rounded geometric sans 600, white | **0.44× headline font-size** (clears the 36px floor) | centred, nudged **~7% W right** of the headline centre, ~0.1u above the cap line |
| **headline** | `Invoice generator` | **heavy soft serif** — `Fraunces 900`, white | 17 chars span **67% of W** → ≈**84px** at 1080 | centred |
| **with-line** | yellow script `with` · brand mark · wordmark | Caveat 700 `#F5D64A` · ClaudeMark `#D97757` · Newsreader 500 `#131313` | with 0.5u · mark 1.0u · wordmark 1.0u | **starts at frame centre, runs right**, hangs ~11% W past the headline's right edge; cap top ~0.1u under the headline baseline |

**No plate.** The reference has no shadow (flat grey ground); over busy footage give the white a soft
`0 2px 22px rgba(0,0,0,.38)`. **The wordmark stays black even over dark footage** — that is the brand
read; move the lockup, don't recolour it.

```tsx
<TextHook at={12} kicker="day 3 of building AI tools" headline="Invoice generator" />
// brand={<…/>} swaps the mark; size = headline px (84); y = headline top (300, in the clear
// headroom band); until = exit frame
```

Entrance is staged kicker → headline → with-line, **6 frames apart**, on the exponential bloom.

> **The COPY is NOT the style** — *"The hook will be different depending upon the script. Keep that
> in mind."* What is saved is the **type system and the geometry**. The three slots are
> *context/series* → *the thing* → *the tool*; the words come from each reel's own hook line.

## Logos — size is the rule, not presence

> *"when we are saying claude cursor whatever you are using, add logos here — they are more
> recognizable"*
>
> *"the nvidia logo is soo small that no one will be able to recognize it. when we are talking about
> recognizable brands like FAANG, openai, anthropic, cursor etc, billion trillion dollar companies or
> app, the logo should be the CENTREPIECE and not just a pill."*

**The pill problem has come back three times.** Treat it as a hard tier rule:

- **Household brand named in the VO → the mark OWNS the card.** 620px wide in a 1000px card,
  centred, screen capture blurred and scrimmed to ~40% behind it. Not a corner chip, not a header
  pill. Carry it into the next register so it gets **seconds**, not the half-second before the cut.
- **Second-tier brands** (a small tool) can stay a chip — **hierarchy is the point**, and shrinking
  the small one is what makes the big one read.
- **A comparison row still needs real size** — 58–62px mark + 46px wordmark when two marks sit side
  by side.
- **Always pair the mark with its wordmark.** A mark the viewer can't place is worse than no mark;
  the label costs nothing. `LogoTile` is the layout: mark on a dark rounded plate, name underneath.

## The hero layer (long-form)

"Heroes" in his vocabulary = the big graphic **set pieces**, not text: stat counters, chapter title
cards, the recap list, a like/comment widget.

Three kinds:
- **`card`** — inside the split's content card; the face stays.
- **`full`** — ink, full-bleed (title, chapters). **It OWNS the frame**: no stamps, lockups or lane
  widgets over it.
- **`lane`** — right-lane widget over the face. Measured hands reach x1492–1572 in recap spans, so
  lists sit low-right at 28–32px.

Rules:
- **Data-driven:** `items[i].at` = the cut frame of the spoken word each piece lands on. **`until=`
  ends a hero on a word** instead of a fixed hold — the cut compresses source time, and a 3.3s hold
  swallowed a whole flurry of content.
- **Something must move continuously in every hero**: counters roll (ease-out, 30–48f), bars grow
  with a sheen, a stopwatch hand sweeps, ring arrows rotate, a dot climbs, "+ MORE" pulses.
- Facts on cards come from the plan's sources and are **footnoted on the card**.
- **A recap list must carry the list he actually says**, one item per spoken phrase — an accumulator
  that showed chapter names while he said different words was wrong.
- **A library shot that starts inside a hero is dropped by the generator and printed.**
- QA: one still per hero at 0.5; pick the frame **after the last item lands**. A 2.2s full hero needs
  its still at **+30f**, not in the split's grow-out.

## The CTA comment composer (STANDING)

> *"redo that animation of liking and the comment thing. Create a comment box where someone is
> typing. That would be better motion graphics for this one."*

A CTA that shows the **action he is asking for** (a viewer actually writing the reply) reads as a
demo, not a badge — and the typed text doubles as a template for what to comment. The earlier
"Like this video" pill + tiny typing panel was rejected as weak MG.

- **Anchor "like" to the FIRST "like this video"** — pass the exact second from the transcript, not
  a guess (the word-lookup takes the nearest word to the second you pass).
- Items = `(word, second, phrase)` per thing he asks viewers to write; each phrase types at
  **2 f/char** from its word. Avatar + "Add a comment…" placeholder open on "comment";
  Cancel/Comment buttons; the button lights on the first character and presses at hero end.
- Bottom strip over a scrim (x 360–1580, y 620–1000) so it clears the face. **46px field text, 54px
  thumb, 38px labels** — phone-legible.
- A keyboard tick per typed segment + a ding on the like (`sfx-design`).

## Font pairings (standing, approved set)

**Max TWO families per piece:** one expressive/display face for ONE hero word or short phrase, one
clean face for everything else. Never script/display for body or long text.

| Style | Expressive | Clean |
|---|---|---|
| **Educational / product / business (DEFAULT)** | Times Bold/Italic (one big editorial word) | Space Grotesk Bold |
| Bold editorial / opinion / retrospective | Abril Fatface (one hero word, never long all-caps) | Archivo Bold/Black |
| Premium / cinematic / case study / manifesto | Anton (1–4 words, all-caps) | Athelas |
| Personal / reflective / human | Snell Roundhand Black (lowercase accent only) | Inter Bold/SemiBold |
| Adventure / playful / behind-the-scenes | Shadows Into Light (handwritten accent) | Bebas Neue Bold |
| Loud launch / poster / announcement | Montserrat Black | Arial Bold |

Pre-approved substitutions, use without asking: ID Grotesk→Space Grotesk, Moara→Anton,
Tempting→Snell Roundhand Black, Balboa→Bebas Neue Bold, Azo Sans Uber→Montserrat Black.

**Non-negotiables:** never stretch / skew / outline / condense; sentence case for supporting copy;
phone-size readability beats decoration; don't introduce new fonts when a pairing fits. These do
**not** override an active design system or an explicit reference look.

**When proposing type, state the chosen pairing, each font's role, and a one-sentence rationale.**
Don't list alternatives unless asked.

For the vlog, "our typography" means **his installed font library** at `~/Library/Fonts` — see
`vlog-edit`.

## Related

`split-screen` · `broll-style-edit` · `sfx-design` · `design-asset` · `longform-edit`.
