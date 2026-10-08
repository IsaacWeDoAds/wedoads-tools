---
name: asset-plan
description: "MANDATORY step 0 of every edit — before any cutting or styling, classify EVERY visual in the script (Remotion / Claude Design / generated b-roll / real recording), fact-check every claim the VO makes against the live source, ask 'what is CONTINUOUSLY MOVING here?' of each beat, and get the creator's yes. Also covers the audit-loop format, generating fake bad examples instead of reusing his work, and frame-sampling a named reference before building. Use at the start of every edit, and whenever a shot's source is unclear."
---

# ASSET PLAN — decide what every shot IS, before anything is built

> **THE 30 JUL BATCH FAILED EXACTLY HERE.** Styling started without an agreed asset plan, so
> missing recordings got silently faked and three reels were rejected outright. Classifying every
> shot up front surfaces what's missing **while there is still time for him to record it**, and puts
> the generate-vs-build-vs-record decision where it belongs.

**Produce a shot-by-shot plan and get his yes before touching the timeline.**

## The four classes

| Class | What goes here |
|---|---|
| **Remotion** | Assembly, sync, captions, MG frames, **terminal mocks** (a terminal is rendered text; a good mock is indistinguishable) |
| **Claude Design** | In-card animated UI/demo assets → `design-asset` |
| **Generated b-roll** | Cinematic cold opens, abstract concept shots, restyles of his own footage → `genvideo` / `omni-restyle`. **Engine = Veo via the Gemini API** — *"use Gemini only"*, it bills his Cloud credits. Sora stays configured but is used only when he explicitly asks for it on a shot. Always cost-gate. |
| **Real recordings** | **EVERY** screen recording, app/browser UI, tool demo → `screen-capture`. Never mocked, never synthesised from screenshots. **If one is missing, STOP and ask him to record it.** |
| **Reference b-roll** | When the reel talks about a company's design/product, show THEIR footage moving. `yt-dlp` (keep it updated — a stale build 403s on everything), pick the longest sustained shots, crop to the card aspect **at native res**. Never upscale. → `broll-select` |

## The question to ask of every beat

> **What is CONTINUOUSLY MOVING here?**

"A screenshot" means the beat is already dead. Get a real recording, or don't use it. See
`screen-capture` for the motion gate this feeds.

## Fact-check every claim BEFORE the graphics exist

List every checkable claim in the VO — numbers, tiers, limits, prices, product names — and verify
each **against the live page**, not training data, which is stale by definition.

One VO said *"Cerebras does a million a day."* The live pricing page showed a $5-credit free tier
and the daily-token plans **sold out**. The claim was simply no longer true. **His call: trim the
sentence.** It cost 2.0s, removed the false claim, and landed the reel exactly on its target length.
The card was never built.

Decision tree:
- **claim holds** → build the shot.
- **claim is wrong and the sentence is severable** → propose trimming it. A clean beat boundary
  usually exists; check the word timings.
- **claim is wrong and load-bearing** → stop and ask before building anything.

**Report the result for EVERY claim, including the ones that passed.** He wrote the checklist item;
he wants the answer, not just the exceptions.

### When the claim is TRUE but seems to contradict the source

A VO said a tool is *"slower to start… two, three extra seconds"* while the repo's banner claimed
**−27% time**. Both were right — slower to *first output*, faster end to end because it writes less
code.

**Don't adjudicate it in our own voice.** Narrow the on-screen wording to exactly what is true
(`slower to first output`, not `slower`), then **put the source's own artifact on screen** — a real
capture of the repo's benchmark table with the cell ringed, captioned "the repo's own table". The
source reconciles itself and we assert nothing.

Same move for attribution: check whether the **primary** source publishes its own numbers before
repeating the script's secondhand citation. It is more defensible and less work.

### Never "correct" a spoken product name on a hunch

The VO said "OmniRoute"; it was assumed to be a mishearing of OpenRouter — same niche, he'd used it
before — and OpenRouter captions, logo and screen capture all shipped. **OmniRoute is a real 42k-star
GitHub repo** whose README matches his description word for word. He caught it on review.

Spelling fixes of a name you can *hear* (Groq for "Grok") are fine. Substituting a **different
product** is not. **One web search of the spoken name settles it either way** — and when the spoken
name turns out to be real, the caption, the logo AND the capture must all follow it.

## Positive and negative examples come from DIFFERENT sources

> *"using my good posters for fake as well looks bad."*

Muting his own poster wall and ringing three of his posters in red as the "this looks bad" beat
structurally says **his work is the slop** — the opposite of the credibility the hook just built.

- **Hook / credibility beats** → his real output.
- **"This is what bad looks like" beats** → **generate** them. `gpt-image-2` via `OPENAI_API_KEY` in
  the gitignored `.env.local` (~$0.05/image at 1024×1536); generator `scripts/gen-fake-posters.py`.
- **The prompt is the asset — keep it.** To get convincing AI slop, ask for the failure modes
  directly: *dead-centre symmetrical subject, heavy soft glowing bloom on everything, and DENSE
  small body text packed edge to edge*. The dense text is what makes the model garble the
  letterforms on its own — you don't ask for "bad text", you ask for a lot of it.
- **When the VO says "images like these", SHOW them.**

(`urllib` fails with `CERTIFICATE_VERIFY_FAILED` on this Mac — shell out to `curl`.)

## B-roll must earn its place

Abstract generated b-roll that only illustrates a mood gets rejected. Use his own real footage and
real product output. A named reference is **not** automatically a layout brief — ask which aspect
it is for (b-roll choices vs the register system); the house format is the default.

## Frame-sample a named reference BEFORE building

When he names a creator or style, **frame-sample that exact reel first**. Don't reuse the previous
project's style language and don't build from a description of the style. `/watch` is the tool.

**A locked account doc outranks a named style reference** — see `broll-style-edit`.

## The audit-loop format

When a reel demos an audit or scoring tool, **run the FULL loop for real**: before-score → apply the
fixes → re-audit → after-score, and put the **moving** number on screen. A single score is a claim;
a moving score is a demonstrated outcome.

1. **Baseline audit** — headless run in the target repo with the skill installed project-scoped, a
   **FIXED scoring rubric written into the prompt** (e.g. −1.5/Crit −0.8/High −0.3/Med −0.1/Low from
   10) so runs are comparable, plus "verify every claim against the real code". Fresh screenshots as
   inputs each round.
2. **Apply the fixes FOR REAL** — only the ones his taste agrees with. The disagree-checklist beat
   writes itself when a finding is a deliberate style choice.
3. **Re-run the IDENTICAL prompt.** Expect it to catch bad fixes — **that is content, not failure**.
   One round caught our own fix being wrong (a badge measured 2.81:1) and it became a caption line:
   *"it even caught one of my own fixes being wrong — that's the loop working."*
4. **Ship the arc on screen**, save every round's report and the combined patch, and state in the
   reel and the DM asset that both numbers are real runs.
5. Recover truncated reports from the headless session transcript at `~/.claude/projects/<target>/`.

## Screen content: the honesty line

Restated here because the asset plan is where it gets enforced — mocked **terminals** fine, mocked
**screen recordings** banned. Full rule in `screen-capture`.

## Related

`screen-capture` · `broll-select` · `design-asset` · `genvideo` · `mg-kit` (reuse before
building). Then hand off to the format skill: `split-screen`, `caption-edit`,
`broll-style-edit`, `vlog-edit`, `longform-edit`.
