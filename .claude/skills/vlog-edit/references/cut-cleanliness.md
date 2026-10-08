# Cut cleanliness — what he hears and sees first

Tools: `work/vlog3/hf_seams.py` (seams + one level per take), `work/vlog3/hf_ripple.py` (cuts,
extends, inserts on the original clock), `work/vlog3/hf_testcut.py` (render any window to check).

## Same-take seams

A cut imported from Palmier had rounded source in-points. At a split **inside one continuous take**,
the next piece started up to 0.15 s *before* the previous ended: the same frames and syllables played
twice. He heard and saw it: *"the composition is the same, but when the cut goes from one clip to the
other clip, it jumps."*

- He gives times on the current timeline. Find the clip whose `data-start ≤ t < data-start + data-duration`
  in `index.html`; its `data-media-start` is the source time.
- The rules below are for two pieces of the **same source file** only. A cut between different files
  (DJI to iPhone, or two takes) is an ordinary cut: check framing, levels and the grade there instead.
- List every same-source pair with `gap = next.media_start − (prev.media_start + prev.duration)`.
  - `−0.5 < gap < +0.05`: a split → set `next.media_start = prev.media_start + prev.duration`, exactly.
  - `gap ≥ +0.05`: a real trim (content removed) → keep the in-point, and the far side needs the punch-in.
  - `gap ≤ −0.5`: a deliberate reorder → leave it.
- Snapping shifts the content of later pieces earlier; **move the graphics in those pieces by the
  same shift** (`seam_shifts.json`).
- Prove it: render the seam and diff consecutive frames. An invisible seam stays under ~1 level of
  mean difference straight through.
- An exactly continuous seam needs no audio fade, because the waveform carries straight on. At a real
  trim, check the largest sample step across the join for a click.

## One level per take

Level-matching each piece separately put **6.5 dB steps** on otherwise invisible seams. Group a take's
pieces (same source, splits AND small trims under 1 s) and give them ONE gain, measured over the whole
span: target the median DJI mean (−22.5 dB), clamp −8…+12, peak ≤ −1 dBFS, near-silent spans capped +6.

**When the camera mic moves, a "take" is a camera SET-UP, not a file** (Vlog 2, `work/vlog2/levels.py`). One DJI
file held wide set-ups at −30 LUFS and close ones at −24. One gain for the whole file, capped by a single suitcase
thud's peak, left its dialogue 10 LU under the next act. Instead, group pieces with no camera move between them,
bring each group's speech to −20 LUFS (cap +12), and **don't let transients cap the gain**: bake a limiter into the
graded source's audio at (−1 − that clip's largest gain) dBFS, stored as FLAC (`condition_audio.py`). Speech sits 5+ dB
under it and is never touched.

## Trims

- **Cut points in silence**: read the 10–50 ms envelope. The cut sits in room tone (≤ −40 dB), not just
  in the transcript's word gap. When words run together ("that, I…"), cut before the phrase instead.
- **Frame-exact**: every boundary a multiple of 1/60 s, or a frame gets dropped or doubled.
- **A cut inside one framing is a jump cut.** Give the far side the 1.15× punch-in so it reads as a
  cut-in. A trim between different set-ups is just a cut.
- **Repeated topic:** keep the setup and the payoff, cut the middle mentions ("keep it max 2/3 times").
- **Fumbles / false starts** ("our Claude bha bha"): cut the false start, keep the restart.

## Finish the thought

He noticed two Palmier trims: *"feels something got trimmed"* and *"increase those a little so that the
line makes sense."*

- For every clip, **read the source past its out-point** (and before its in-point) until the thought
  lands. A silent stretch doesn't end the search; read on to where he next speaks. If the sentence continues, extend to its end, or insert the next piece of
  the same take.
- If he never finishes it in the footage, trim back to the last complete sentence and tell him.
- Transcribe the gap in **Hindi with translate** (faster-whisper `language="hi", task="translate"`);
  English-only ASR silently skips Hindi stretches.
- A word clipped at a clip end ("multiple ones") is extended until it has fully decayed (≤ −50 dB).
  This is stricter than the ≤ −40 dB room-tone rule for a cut point because the tail of a word is
  still audible at −40.
- Restored audio of a laptop playing a reel is fine; the reel's own line ("I don't deserve it") is part
  of the joke.

## Ripple edits keep everything in sync

Keep graphics, SFX and music on the ORIGINAL clock and map them through `R(t)` (`hf_ripple.py`).
`CUTS`, `EXTENDS` and `INSERTS` each apply once (markers in `index.html`), and every later clip,
graphic, sound and music start moves with them. Entries, all on the original clock:
- `CUTS`: `(start, end)`, silence to silence
- `EXTENDS`: `(clip id, seconds added at the out-point, the clip's original end)`
- `INSERTS`: `(after clip id, original time, [(suffix, media start, duration, punched)])`

Run `python3 work/vlog3/hf_ripple.py --apply`. A music burst a cut lands inside is shortened, so it
still ends on the same picture.
