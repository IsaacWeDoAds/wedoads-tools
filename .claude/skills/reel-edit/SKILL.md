---
name: reel-edit
description: "THE ROUTER — start every video edit here. Picks the format (split-screen / paper-drawer / whiteout / caption-edit / layered-head / b-roll-style / card-list / vlog / long-form), enforces the pipeline order (asset plan → cut → cut audit → capture → style → captions → SFX → render → review), names which craft skill owns each stage, and carries the standing deliverables and the non-negotiable rules. Use at the start of ANY editing request — 'edit this reel', 'cut this', 'make a video from this take' — before choosing a layout or touching a timeline."
---

# REEL EDIT — the router

> **THE META-RULE, and the reason this skill exists:** *"the memory files are loaded every session
> to be EXECUTED, not recited."* Three rejections on one reel were all rules already on file that
> got **applied at half strength**. Loading a skill is not the same as following it. If a skill has
> a checklist, make a todo per item.

## Step 1 — pick the format

| If… | Format | Skill |
|---|---|---|
| 9:16 · shows a screen, tool or demo · tools account | the signature 60-40 split | **`split-screen`** |
| 9:16 · "the arena-skill look", "the paper drawer", pixel mascots on grid paper, "my face slides away and comes back" · the idea must be DRAWN as a diagram, not shown as a recording | grid-paper world, face card is a sliding drawer | **`paper-drawer-edit`** |
| 9:16 · "the Whiteout look", "the find skills style", "the whole screen goes white" · his face stays clean and full frame, and each idea takes over the WHOLE frame on plain paper (no grid, no face card) | face ⟷ paper-white canvas, slide/dissolve in, hard cut out | **`whiteout-edit`** |
| 9:16 · he says "just a basic edit", "no cuts needed", "keep it mostly raw" · the SHOT is the content (two-shot, walking take, locked-off camera) | overlay only, take stays whole | **`caption-edit`** |
| 9:16 · "the Tharun look", "same editing language as those two desk reels" · graphics IN the shot (behind his head, on props, beside his hand) · flash-cut registers · a scoreboard MG that returns after every list item | full-frame head that CUTS, layered | **`layered-head-edit`** |
| 9:16 · personal essay / story / listicle · personal account · b-roll carries the picture | fast Hinglish creator essay | **`broll-style-edit`** |
| 16:9 · day-in-the-life vlog · main YouTube channel | coverage, **zero typography** | **`vlog-edit`** |
| 16:9 · talking-head essay, 8–20 min · he cuts in Palmier, I layer | source-anchored MG over his cut | **`longform-edit`** |
| 9:16 · recommends a LIST of external things (videos, channels, tools, books) · nobody speaks | hook clip + real cards, music only | **`card-list-edit`** |

**Two disambiguations that have gone wrong before:**

- **Which ACCOUNT?** The two Instagram grids must never converge. **Tools account** = yellow +
  screen recordings + the split. **Personal account** = blue + real-life b-roll + the card format.
  **Check before styling.**
- **A named style reference is not automatically a layout brief.** Ask which aspect it is for
  (b-roll choices vs the register system). Exception: "same editing language as X" IS the layout
  brief — for the Tharun desk reels that brief is `layered-head-edit`. And **a locked account doc outranks a named style
  reference** — surface the conflict, quote the section, ask. Don't silently pick.

## Step 2 — run the pipeline, in order

```
0. ASSET PLAN      `asset-plan`      classify every visual · fact-check every claim · his YES
1. CUT             `shortform-cutaway`   WhisperX word-exact rough cut
2. CUT AUDIT       `cut-audit`       prove it — the transcript is NOT evidence
3. GEOMETRY        `take-geometry`   measure the take · solve the fit · derive the bands
4. CAPTURE         `screen-capture`  real recordings, ≥30% motion
   ASSETS          `broll-select` · `design-asset` · `genvideo` · `omni-restyle`
5. STYLE           the format skill  +  `mg-kit` (reuse before building)
6. CAPTIONS        `caption-align`   source → SEGMENTS → force-align → pause audit
7. SOUND           `sfx-design`      peak-aligned, volume for the final domain
8. RENDER          `render-ops`      slim bundle · own entry · check contention · loudnorm
9. REVIEW GATE     `reel-review`     script measures + Fable 5 looks. NEVER skip.
```

**Stages 1 and 5 are both mandatory and both are skills** — never style ad-hoc, and never re-pick
takes during styling. The cut is decided upstream and is sacred.

**Do not read "basic edit" as "skip the pipeline."** Skip only what he named.

## Step 3 — the non-negotiables

These are the rules that have each cost a re-render more than once. They apply in **every** format.

1. **Never put text or graphics on his face, in any frame.** A ~6-frame flash counts. Enforce with
   the alpha guard, not with your eyes.
2. **Registers HARD CUT.** No opacity crossfade — a fade shows the base cut through both layers.
   Delete `SectionFade`-style wrappers on sight when copying an old `Final.tsx`.
3. **Nothing animates across a cut boundary.** No zoom in/out at cuts — it advertises the cut.
   Delete `wave()` wherever it is copied from. **The memory outranks the baseline code.**
4. **Mocked screen recordings are banned.** Mocked terminals are fine. If a recording is missing,
   **stop and ask him to record it.**
5. **Never upscale b-roll.** Pre-crop to the card's aspect at native resolution.
6. **Screen captures must MOVE** — ≥30% of frames, and no static run longer than ~5 frames.
7. **Text inside the IG safe zone** — y220–1470, 35px sides, ~100px clear on the right. Imagery may
   cross; text may not.
8. **SFX only.** He adds music when posting.
9. **Every reel ends on the Follow close** in the format's own idiom.
10. **Real numbers only** — follower counts, prices, scores, tiers. Verified, never invented.

## Step 4 — verify before he sees it

- **`/watch` the DELIVERABLE file**, always, before sending — and to study a named creator's style
  before building. Its scene-change sampler lands exactly on register boundaries, which is where a
  whole class of one-frame bugs lives and where nothing else looks.
- **Plus fixed mid-beat ffmpeg stills.** Scene-change sampling lands on cut boundaries and
  exaggerates empties; mid-beat stills are the counterweight.
- **Then the review gate** — `scripts/review_reel.py` and the Fable 5 vision pass. **The edit runs
  on Opus 5, the review runs on Fable 5.** A second model reviewing the first model's work is the
  point; never self-review inline.
- Fix every BLOCKER and re-render. Report FIX/NIT with a recommendation. **He reviews a known-state
  file, never a surprise.**

## Step 5 — the standing deliverables

Ship these **unasked**, with every finished reel:

- the **render**, loudnorm'd to −14 LUFS (measured on the **encoded** file)
- the **IG caption**, in the six-part shape the account uses
- the **trigger-word DM asset as a BUILT PDF**, not a markdown draft —
  `docs/dm/<reel>-guide.html` + `node docs/dm/make_pdf.mjs`

## Working in a shared repo

Several Claude sessions edit this repo at once. Before writing anything:

- `pgrep -fl ffmpeg`, and look at `work/`, `public/broll/` and `out/` for a `reelNN` that already
  exists. If another session is live on that number, **take a distinct suffix for EVERYTHING at
  once** — never share a single path.
- **`out/` is volatile and is not automatically yours.** Re-check your intermediates still exist
  before each step that consumes them.
- **Inspect in a separate call from any delete.** `ls DIR; rm -rf DIR` in one call is not a check.

Details: `render-ops`.

## Where the rest lives

- Style system: `docs/reel-edit-styles.md` · personal-account rulebook:
  `docs/personal-account-guidelines.md` · b-roll catalogue: `docs/broll-catalog.md`
- Per-take measured numbers: `.claude/skills/take-geometry/data/takes.md`
- Reusable components: `mg-kit` and `<media-drive>/MG-Kit/`
- Stack and commands: `WORKSPACE.md`
