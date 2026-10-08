---
name: reel-review
description: FINAL GATE before any reel is sent to the creator. Runs the deterministic review script (specs, loudness, frozen frames, card-region motion, caption sync against the re-transcribed render, safe-area extents) and then dispatches a FABLE 5 vision agent that actually looks at frames from every section and judges captions, overflow, collisions, legibility and rule compliance. Use whenever a reel render is finished — before delivering, never after.
---

# REEL REVIEW — the final gate

> **THE SPLIT:** a script measures what is *measurable*; an agent judges what is
> *judgement*. Never let the agent guess at numbers it can measure, and never
> let the script rule on taste. Both halves run, every time.

**Models (his call, 26 Aug 2026): the review runs on FABLE 5, the edit runs on
OPUS 5.** A second model reviewing the first model's work is the point — pass
`model: "fable"` to the Agent tool. Do not review your own edit inline.

## Step 1 — deterministic pass

```bash
python3 scripts/review_reel.py <RENDER.mp4> --reel reelNN --data src/ReelNN/data.ts
```

Exits 1 on any FAIL. It reports:

| check | what it catches |
|---|---|
| specs + frame count vs `data.ts` | wrong resolution/fps, **clipped tail** |
| loudness | not at −14 LUFS ±1, hot true peak |
| frozen runs | the Remotion frozen-frame / concurrent-decode bug |
| **card-region motion** per section | static cards — the "slideshow" failure. ≥30% is the floor; whole-frame motion is meaningless on a composed render because the face layer moves every frame |
| **caption sync** | re-transcribes the RENDER with WhisperX and matches every caption's first word to the spoken audio. Reports match count, mean offset, worst offenders, and any caption with no matching word |
| safe-area ink extents | measured per sampled frame, for the vision pass to judge |

It also samples two frames per section — **mid-beat** (steady state) and
**+0.35s after the boundary** (post-enter, catches ghosting and empty cards) —
and builds contact sheets.

## Step 2 — Fable 5 vision pass

Dispatch ONE agent with `subagent_type: "general-purpose"`, `model: "fable"`,
and hand it: the report path, the contact-sheet paths, `CLAUDE.md`, and
`docs/reel-edit-styles.md`. Tell it to **Read every sheet** and rule on:

1. **Captions** — present on every spoken beat? legible at phone size (≥78px
   for display captions)? inside the safe band? **never on his face**? Does any
   caption overflow its lane or wrap badly?
2. **Overflow / collision** — any text crossing the card edge, clipped at frame
   edges, or two elements stacked on top of each other? Any element crossing
   Instagram's x918 action rail or the y230/y1574 text safe area?
3. **Screen content + MG** — is every card *full* in its first second (furniture
   lands in 10–30 frames; only the word-answering punch waits)? Is screen text
   legible? Is any capture a static screenshot? Any card left visibly empty?
4. **Registers** — do they HARD CUT, or is the base cut ghosting through a
   crossfade at any boundary? (This is the reel-35 v3 failure.)
5. **Rule compliance** — cross-check against `CLAUDE.md` hard rules and the
   style doc: no text on face, no chip/pill-sized labels, brand marks at
   centrepiece scale, no zoom at cuts, FollowCta close present.

Ask for output as: **BLOCKER / FIX / NIT**, each with the frame number, what is
wrong, and the specific rule it breaks. Require it to say explicitly when it
finds nothing — no invented findings to look useful.

## Step 3 — act, then hand over

Fix every BLOCKER and re-render before the creator sees it. Report FIX/NIT items to
him with your recommendation. **Tell him what the gate found, including the
items you chose not to act on** — the point is that he reviews a known-state
file, not a surprise.

## Reading the output honestly

- **Card-region motion below 30% is not automatically a bug.** A before/after
  stills beat or a slow terminal reveal is legitimately low. It is a prompt to
  ask "should this beat be more alive?", not a fail.
- **Caption offsets of a few frames are normal** — the render's own audio is
  re-transcribed, so ±5 frames is alignment noise, not drift. Worry at >12, or
  at a mean that trends one way across the reel.
- The script's safe-area table is **whole-frame ink extents**. The base cut is
  full-bleed, so edge values are expected; only the vision pass can tell text
  from imagery.
