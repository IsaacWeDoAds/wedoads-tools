---
name: genvideo
description: Generate AI b-roll video for reel edits using the creator's own API keys — Veo 3.1 via GEMINI_API_KEY or Sora 2 via OPENAI_API_KEY. Use whenever an edit calls for generated footage (cinematic cold-open b-roll, abstract concept shots, restyle passes). NEVER for screen recordings or fake product demos. Always cost-gate with the creator before generating.
---

# GENVIDEO — AI b-roll generation (BYO API keys)

> **THE JOB:** produce short generated clips for reel edits using the creator's own provider keys —
> **Veo 3.1 (Gemini API)** or **Sora 2 (OpenAI API)** — with the guardrails that keep generated
> footage honest and on-brand. Output lands in `public/broll/gen/` ready for Palmier/Remotion.

## ⛔ WHAT GENERATION IS FOR — and not

**Allowed:**
- Cold-open cinematic b-roll (Style A's 2–3s scroll-stopper — see `docs/reel-edit-styles.md` §1)
- Abstract concept shots (a comparison, a metaphor, an architecture idea in motion)
- Restyle passes on the creator's OWN footage (the sebintel §6 collage prompt pattern)
- Backgrounds / textures for MG frames

**Never** (this is the standing screen-content rule, non-negotiable):
- Screen recordings, app/browser UI, tool demos — those must be REAL recordings
- Anything presented as evidence that a tool ran ("output", numbers, terminal results)
- A stand-in for a missing real asset — a missing recording means STOP and ask the creator

## THE COST GATE — before every generation call

Generation bills real money on the creator's keys. Before ANY call, show him:
model · clip list (prompt one-liners) · durations · resolution · candidate count —
and get an explicit yes. Batch the whole reel's generation plan into ONE approval.
Default to the cheaper tier (`veo-3.1-fast-generate-preview` / `sora-2`) unless the
shot is the hook; hero shots may justify `sora-2-pro` or full Veo.

## ENGINES

**Veo (Gemini API) is the DEFAULT — the creator's stated preference ("use Gemini
only"); it bills his Google Cloud credits.** Sora stays configured as a
fallback but is used only when the creator explicitly asks for it on a shot.

Keys come from the environment — never hardcode, never echo them.

### Veo 3.1 — `GEMINI_API_KEY`
`scripts/gen_veo.py PROMPT_FILE OUT.mp4 [--model veo-3.1-generate-preview] [--fast]`
- Native `aspect_ratio: "9:16"`, ~8s clips, audio included. Async operation, polled.
- `--fast` swaps to `veo-3.1-fast-generate-preview` (cheaper, quicker); `--model veo-3.1-lite-generate-preview` is the cheapest tier — use it for smoke tests.

### Sora 2 — `OPENAI_API_KEY`
`scripts/gen_sora.py PROMPT_FILE OUT.mp4 [--model sora-2] [--size 720x1280] [--seconds 8]`
- Portrait via `size` (720×1280; `sora-2-pro` supports 1024×1792). Poll → `download_content`.

Both scripts: prompt read from a file (prompts are long), MP4 written to
`public/broll/gen/<slug>.mp4`, metadata JSON alongside (`.gen.json`: engine, model,
prompt file, date) so every generated asset is traceable.

Setup once: `pip install google-genai openai` in any Python ≥3.10 env.

## PROMPT DISCIPLINE (the §6 lesson: guardrails outnumber aesthetics)

- Front-load the subject and camera move in one sentence; then style; then **a block of
  negative constraints** — especially about TEXT: generated clips must contain
  **no words, no captions, no UI, no logos** unless the shot explicitly needs them
  (and then: exact strings, exact count, "if in doubt, fewer, never more").
- For restyles of the creator's footage: "keep me photorealistic and unchanged … original
  voice and audio exactly the same … never cover my face or hands" — copy the §6
  structure from `docs/reel-edit-styles.md`.
- 9:16 always. Match the reel's grade direction (warm/low-key vs bright/airy).

## QA — every clip, before it touches a timeline

1. **Watch it** (extract 4–6 frames + play the audio) — asset RULE 0 from
   shortform-finish applies to generated clips doubly: artifacts, warped hands,
   accidental text, watermark-ish smears are all rejection reasons.
2. Hero shots get **2 candidates minimum**; audition them side by side (the
   shortform-finish audition workflow).
3. Generated audio is usually discarded — the reel's VO/SFX owns the mix. Strip it
   unless the clip was generated FOR its sound.
4. Place into the edit via the normal pipeline (import to Palmier / `staticFile` in
   Remotion) — generated clips follow the same zoom/SFX rules as any b-roll.

## SCOPE
**DOES:** prompt-craft · engine calls on the creator's keys · cost-gated batches · QA + audition ·
staging into `public/broll/gen/`.
**DOES NOT:** screen recordings (real only) · take-picking or styling (that's
shortform-cutaway / shortform-finish) · spending without the explicit yes.
