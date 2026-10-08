---
name: cut-audit
description: "Prove a rough cut is actually clean before it is styled or rendered. ASR cannot hear a false start — it de-duplicates immediate repeats — so this skill gates on ENERGY and SPECTRUM instead: stretched-word screening, syllable-budget folds, per-burst isolated probes, spectral self-similarity (repeat_scan), onset-vs-word ratio, and the tail/head release audit. Use after any rough cut, whenever a doubled or clipped word is suspected, and whenever a single caption is persistently reported out of sync."
---

# CUT AUDIT — the transcript is not evidence

> **THE ONE FACT:** an ASR language model is built to produce fluent text, so **two identical
> adjacent phrases decode as one**. A clean transcript proves nothing. On one reel, **five separate
> transcripts** — the global WhisperX pass, the rough-cut re-transcribe, the review gate's
> re-transcribe of the render, the caption-sync matcher (mean −0.1 frames), and a `/watch` Whisper
> pass — all called a cut clean that had **two doubled lines in the first 20 seconds**. He found
> them by listening.

**He restarts lines mid-take. It is his default delivery** — one take had SIX abandoned attempts in
74 seconds. Assume there are more than you found.

## The gates, in order

Run all of them. Each catches a class the others structurally cannot.

### 1. Stretched-word screen (before writing beats)

Any word longer than ~1s is an artifact: the aligner smears one word across a hidden pause, a
retake, or an abandoned take.

- Flag every word with `end − start > 1.0s`.
- **At a clip EDGE, probe regardless of length.** A collapsed repeat shows as a word roughly the
  length of the whole repeated phrase — two offenders once sat at 0.69s and 0.70s, just under a
  0.9s gate, and both shipped. **For a short function word, >0.55s is already suspicious.**
- Resolve each against an **RMS energy map** (40–50ms hops), **never against a second
  transcription**. Re-running alignment does not fix it — a second pass over a shorter window
  disagreed with itself, and a `small`-model pass under ~5s hallucinated text that was not there.
- Patch the word's `s`/`e` in a **copy** of the alignment json, with a comment naming the evidence.

**The 1.0s threshold misses folds — screen by SYLLABLE BUDGET instead.** A 0.52s word `well.` hid
an entire folded `It will break.` and survived two sweeps. Walk each RMS speech run and ask: *does
the text assigned to this run plausibly fill it?* Compare voiced-blob count inside the run (≈ one
per syllable) against the assigned text.

**The mirror artifact: an UNDER-RUN word end invents a false gap.** An end marked 0.46s early made
the builder see a "silence" inside *"Free Gemini access"* and cut there, removing the tail of `Free`
and the `Ge–` of `Gemini` — it transcribed as "gem access". Before locking `GAP`, list every
inter-word gap the builder is about to cut on and check the smallest against energy. **Real
inter-beat gaps in his delivery are ≥0.60s**; anything in the 0.3–0.5s band is suspect. **Merging a
gap can never clip a word, only cutting can** — when a boundary is ambiguous, err toward the larger
`GAP`.

### 2. The clip-list screen (free, before anything renders)

**Look at the CLIP LIST, not the word list.** A sub-1s single-word clip at the head of a beat is
almost always a swallowed false start — visible in the builder's own stderr before a single frame
is rendered. **Treat any clip under ~25 frames whose text is a single word as suspect.**

### 3. Onset-vs-word ratio, per clip

```
ratio = (syllable onsets: >1.45× rise over 20ms, ≥0.12s apart) / (words in that clip)
```

- clean clip → **0.85–1.15**
- a doubled take → **2.00** (12 words, 24 onsets)

Also compare the aligner's last word-end against the energy envelope's last speech: **a gap >0.6s
means the aligner collapsed the clip** and its word times are not trustworthy.

### 4. Spectral self-similarity — the gate that actually catches a prefix false start

An onset-vs-words count still misses it when the false start is a **prefix** of the redo and the gap
is only 0.13s.

```bash
python3 scripts/repeat_scan.py OUT.mp4          # exits 1 if any pair scores >= 0.78
```

Split the audio into speech bursts from the energy envelope, **joining only gaps < 0.08s** (a 0.30s
join merges a false start into its redo and hides it). DTW-compare each burst against the **head of
the next burst** over log-mel frames.

Measured: real false-start/redo pairs score **0.83–0.91**; unrelated speech of the same length
scores **~0.66**. Gate at 0.78. It found 9 pairs in one source and confirmed 0 survived the recut.
Wired into `scripts/review_reel.py` as a FAIL.

### 5. Per-BURST isolated probes (not per-window)

**Any probe wide enough to contain both halves of a repeat lets the model merge them.** A
hand-picked isolated probe of 62.8–66.5s spanned both bursts and collapsed them again into one
clean sentence — the stutter shipped.

Segment the audio by energy into bursts (threshold ≈ noise floor + 14 dB, min 0.22s, **merge gaps
< 0.18s**), transcribe **each burst on its own**, then flag adjacent bursts whose first word matches.

Reading the output:
- A sub-second fragment transcribes as nonsense in isolation ("Month six—" came back as *"one
  succinct"*). **Judge it by POSITION and energy, not by the words.**
- A genuine parallel construction ("In month 2…" → "In month 3 and 4…") will flag and must be kept.
- **Probe quiet regions LOUDER** — re-align the slice with `volume=6dB`. A normal-volume probe heard
  nothing where the boosted one read "similar to the best". Quiet false starts are invisible to both
  RMS reads and normal probes.
- **When the RMS map calls a "silence" speech, PROBE it — do not reason it away.** An energy pass
  flagged a span as 46.7% above floor and it was written off as "a deliberate pause before the
  keyword". It was the second take. Cost: two full re-renders.

### 6. Padded micro-probes — decisive, and dangerous

Short padded windows (0.6–1.2s, padded with ~0.6s silence, `medium.en`) are **unreliable for
discovering** what was said but **decisive for choosing between two specific hypotheses** the energy
map has already bracketed. Four probes once settled in one pass what two rounds of reasoning got
wrong.

**But padded short probes HALLUCINATE REPEATS.** Four separate padded probes each "heard" a doubled
phrase that did not exist ("You're in. You're in.", "Plan. Plan."). Silence-padding invites
Whisper's repetition loop. **A repeat heard only in a padded probe is not evidence** — confirm with
an unpadded ≥2.5s aligned window plus the energy map (one speech run = one utterance).

### 7. The assembled-cut listen-back

Re-transcribing the assembled cut is **the right alarm and never the right diagnosis.** Whisper
reconstructs across a splice and will invent a subject to make a fragment grammatical (it produced
a phantom "It" for audio that was only "will break when"), and it **localises a fold to the wrong
side** — the duplicate belonged to the clip *before* the join, not after.

It is still a genuinely useful second net for repeats that land in two **different clips**:
de-duplication only happens for an immediate repeat inside one utterance, so the concatenated VO
presents them as separate events and the aligner reports both.

### 8. Tail / head release audit (every part boundary, before the first render)

**"Very sharp cuts because I'm not finishing my words."** Phoneme alignment marks a word's END
before its audible decay finishes — worst on Hindi vowel endings. A part cut at
`last_word_end + 0.16` lands inside the decay.

For every boundary: decode the CAMERA audio around the cut (RMS per 20ms), flag voice-active-at-cut,
find the release (first ~100ms below threshold), extend the beat end to `release + 0.10`, **capped
at `next_dropped_word_onset − 0.06`** so retakes never leak back. Also flag HEADS where voice runs
before part start.

Cases it surfaces:
- `release +0.00` — decay crosses exactly at the cut; +0.12 is enough.
- `NO RELEASE` — you cut mid-flow, the sentence continues. Extend through the phrase or move the cut.
- Voice after the cut can be the NEXT RETAKE's onset, not a decay. Compare against the word list.
- A flagged END+HEAD pair at nearly the same source time = you split continuous speech. Merge the
  parts or butt them.

Run it until flags are only the understood/capped cases. **Before he hears it, not after.**

## Take selection

**Keep the COMPLETE take and drop the attempt, every time** — never both, and never the attempt
just because it came first.

**The inverse repair exists.** One hook began with a 0.14s burst ("Your"), a 0.08s pause, then "AI
agent can't…". Probes read it as a false start; cutting it shipped a hook transcribing as "AI agent
can't actually see…". The burst WAS the word — he fronts words like this. **Before dropping any
sub-0.3s opening burst, transcribe the assembled hook WITHOUT it: if the line loses its subject, the
burst was the take.**

## After a repair — three independent consequences

Fixing the cut fixes only one of them.

1. **Neighbouring word TIMINGS drift.** After repairing an artifact, treat every word in that
   segment as suspect. Derive captions from the source→SEGMENTS arithmetic as usual, then
   re-transcribe the RENDER and pin the **repaired region's** captions to the delivered audio.
   Everywhere else the arithmetic wins; only inside a repair does measurement beat it.
2. **The boundary word's TEXT can be flat wrong.** The aligner had already *spent* the label `Here`
   on a discarded burst, so it labelled the good take's opening word `is` and the generator printed
   "is what I actually did." Fix with a **source-time override**, keyed to seconds not word index
   (indices shift every recut):
   ```py
   TIME_FIX = [(41.80, 41.95, "Here's")]      # what is HEARD beats what was labelled
   ```
3. **The global alignment is wrong wherever this happens.** WhisperX placed one line ~0.4s early and
   dropped a phrase entirely, so after recutting on true burst edges those words fell outside the
   beat and vanished from the captions. **Re-align each rebuilt span IN ISOLATION and splice the
   corrected word times back into the wx json before regenerating.**

## Assembly

- **The concat must be CFR.** An ffmpeg-concatenated cut is variable-frame-rate; `nb_frames`
  undercounts and a `TOTAL_FRAMES` taken from it **silently clips the last word of the reel**. And
  even in CFR the concat **demuxer duplicates the head frame** — use the concat **filter** when a
  per-section overlay map is pinned to the cut's frame numbers.
- **Hand-picked beat spans skip the gap remover.** Each span still needs its own lead/tail trim AND
  an internal-silence split, or the render ships 0.5–0.9s holes.
- **Never cut a sentence's internal pause.** The >0.30s internal-silence rule exists to expose
  hidden RETAKES; a natural emphasis pause inside a continuous sentence is kept. Cutting one reads
  as a jarring mid-sentence jump cut.

## Language

The English model silently **translates** his Hindi, so the same repeated Hindi phrase comes back as
two different English sentences and reads as intentional. Force a Hindi model over every Hindi span.
Whisper also **repeat-loops** on noisy outdoor code-switching and can silently drop 40s — chunk the
audio to reset decoder context, and **never read an ASR gap as silence**.

## Two standing tells

- **A persistent single-caption sync outlier is a prime suspect for a collapsed repeat.** One beat
  was reported `+31 frames out` for three renders and dismissed twice as a matcher artifact. It was
  not — the matcher was anchoring to the SECOND utterance while the caption sat on the first.
- **When he flags a repeated phrase, go straight to a 50ms RMS map plus an independent ASR engine on
  that window.** Palmier's on-device engine transcribed both false starts correctly where WhisperX
  had swallowed them.

## Related

`caption-align` consumes the corrected word times. `shortform-cutaway` builds the cut this skill
audits. `reel-review` runs `repeat_scan` as a FAIL gate on the finished render.
