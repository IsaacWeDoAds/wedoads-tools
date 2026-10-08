# Setup (once)

## Required
- **An agent:** Claude Code (Claude Pro, $20/month) or Codex (ChatGPT Plus, $20/month).
- **ffmpeg** (`brew install ffmpeg`) — every skill uses it.
- **Python 3.11 venv with WhisperX** (the rough cut needs Python ≤ 3.12):
  ```bash
  python3.11 -m venv ~/wx-env && ~/wx-env/bin/pip install whisperx numpy
  export HF_HOME=~/wx-cache
  ```
- **Node 22+** for HyperFrames and Remotion.

## Pick one editor (all free to start)
- **HyperFrames** (by HeyGen, open source): `npx hyperframes init`, or add it as a plugin in Claude Code /
  Codex. Video is HTML + GSAP. My long-form and vlogs are built here now.
- **Remotion**: `npx create-video@latest`. Free for individuals and teams of up to 3.
- **Palmier Pro**: an AI-native editor for Mac (macOS 26, Apple Silicon); drive it through its MCP server.
- **DaVinci Resolve**: via a community MCP server.

## Strongly recommended
- **The watch skill** (video understanding: frames + transcript from a URL or file):
  `claude plugin marketplace add bradautomates/claude-video` then `claude plugin install watch@claude-video`.
  It's how the agent studies a reference edit and checks its own renders.

## Optional keys (put them in a gitignored `.env.local`)
- `OPENAI_API_KEY`: verbatim probes, isolated-window word timing, listen-back (cents per video).
- `GEMINI_API_KEY`: Veo and Gemini Omni for generated b-roll and restyles (`genvideo` / `omni-restyle`
  always show you a cost plan and wait for a yes).

## Your libraries (build them as you go)
- **B-roll:** one folder per category plus an `INDEX.md` written by the watch skill, so the agent picks
  shots by what's in them.
- **SFX:** whooshes, clicks, pops, paper, risers, impacts. Run `longform-edit/scripts/sfx_lib.py` to
  peak-normalise them and catalog each file's peak and onset.
- **Motion-graphics kit:** every graphic you build gets exported back into the kit (`mg-kit`).
