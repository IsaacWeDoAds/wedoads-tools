# Video edits — agent instructions

## Start every edit with the `reel-edit` skill
It picks the format and enforces the order below. Don't choose a layout or touch a timeline before it.

## Formats — pick ONE per job
split-screen · paper-drawer-edit · whiteout-edit · caption-edit · layered-head-edit · broll-style-edit ·
card-list-edit · vlog-edit · longform-edit

## The pipeline (every edit, in this order)
| # | Stage | Skill |
|---|---|---|
| 0 | Asset plan first: classify every visual, fact-check every claim, get my yes | `asset-plan` |
| 1 | Rough cut: WhisperX words, envelope-exact edges | `shortform-cutaway` |
| 2 | Cut audit: the transcript is not evidence | `cut-audit` |
| 3 | Take geometry: measure the face before placing anything | `take-geometry` |
| 4 | Capture + assets | `screen-capture` · `broll-select` · `design-asset` · `genvideo` · `omni-restyle` |
| 5 | Style | the format skill + `mg-kit` + `shortform-finish` |
| 6 | Captions | `caption-align` |
| 7 | Sound | `sfx-design` |
| 8 | Render + deliver (−14 LUFS measured on the encoded file) | `render-ops` |
| 9 | Review gate, never skipped: a different model reviews | `reel-review` |

## Hard rules
- Never put text or graphics on my face, in any frame.
- Registers hard-cut. No opacity crossfades between them.
- Nothing animates across a cut.
- Screen recordings must be real and must move. Mocked recordings are banned (mocked terminals are fine).
- Real numbers only. Fact-check every claim against the live source.
- Cost-gate every generation: show the plan (model, prompts, durations), wait for a yes.
- Sound effects only, unless I ask for music.
- When I correct something, update the skill that should have prevented it.
