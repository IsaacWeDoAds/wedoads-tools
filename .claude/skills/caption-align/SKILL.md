---
name: caption-align
description: "Get caption words onto the right frames and keep them there — derive frames from SOURCE word times through the segment table (never from a re-transcribed rough cut), then FORCE-ALIGN the authored text to the delivered audio with wav2vec2, then audit every run against the RMS envelope for dead air. Also carries the run-construction rules (≤3 words unconditional, never open on an article, ≥0.30s, contiguous `to`) and the anchor-section assertion. Use whenever captions are generated, retimed, rewritten, or reported out of sync."
---

# CAPTION ALIGN — the right words on the right frames

> **THE JOB:** three different clocks are in play — the source take, the concatenated cut, and the
> delivered render — and every caption bug in this project comes from reading a time off the wrong
> one. Derive from the source, align to the render, audit against the waveform.

## The pipeline

```
source word times ──(SEGMENTS map)──► caption frames ──(wav2vec2 force-align)──► final anchors
                                            │                                        │
                                            └──────► RMS pause audit ◄───────────────┘
```

## Step 1 — derive from SOURCE, never from a re-transcribed rough cut

```py
def tl(src_sec):                       # source seconds -> timeline frame
    f = src_sec * 60
    for from_, len_, srcFrom in SEGMENTS:
        if srcFrom - 1 <= f < srcFrom + len_:
            return round(from_ + (f - srcFrom))
```

**Why:** `ffmpeg -ss/-t` lands on the nearest frame and rounds **independently per clip**, so the
concatenated cut and the compositor's `SEGMENTS` diverge a little at every join and the error
accumulates in one direction. It reached **−18 frames (0.3s)** by the CTA on one reel — captions
firing visibly before the words, worst exactly where the keyword ask lands.

Rules that fall out:
- Walk captions and source words **in order and consume as you go**, so repeated words resolve to
  the right occurrence.
- Words the take selection dropped break a naive sequential walk — pin those by source second by
  hand. (One reel needed 8 of 49 pinned: everything around an abandoned take, plus "codebase"
  which the aligner splits as "code" + "base".)
- **Retime SFX cues and card boundaries in the same pass.** They were placed against the old
  caption frames and drift with them.
- Re-transcription is the right tool for **checking**, never for **deriving**.

## Step 2 — force-align the authored text to the delivered audio

The caption text is authored by hand, so there is nothing to transcribe. Hand wav2vec2 the **known
text** and let it pin each word to the waveform you are actually shipping.

```python
al = whisperx.align(
    [{"start": a, "end": b, "text": "<that section's words>"}, …],
    *whisperx.load_align_model(language_code="en", device="cpu"),
    whisperx.load_audio("cut16k.wav"), "cpu")
```

One segment **per captioned SECTION**, bounded — so a second voice on the tape (an ad's VO, a
laptop playing something back) can never capture his words.

**Why:** an ASR decoder *guesses* onsets around pauses. Chunked Whisper is right about the WORDS
and unreliable about the TIMES — "So" reported at 24.32s actually starts at 24.77; "You" at 13.10
actually at 13.52. Five review runs failed at **+30, +28, +23, −16, −15 frames** with a perfectly
good cut. After forced alignment: 43/43 matched, mean **+5.7 f**, worst **+7 f**.

### When the aligner itself drifts

WhisperX's aligner **smears a long segment**. On one take it returned only two segments and inside
the second one ran the back half up to **2.9s early**:

| caption | anchored | actually spoken | error |
|---|---|---|---|
| `so it's crazy` | 44.92 | 47.54–48.86 | **−2.9s** |
| `if you want` | 51.82 | 53.78–54.24 | −2.0s |
| `That's the timeline` | 9.82 | 11.54–12.78 | −1.7s |

**Every existing check missed it.** The RMS pause audit only asks "is there speech under this run?"
— and there was, just the *wrong* speech. The review gate re-transcribes with the **same aligner**,
so it reproduces the same drift and reports the correct captions as −80 frames out.

**The reliable measurement:** transcribe **SHORT windows in isolation** with word timestamps — a
fresh decoder per window cannot smear across a pause. 5s windows, 2s overlap, +6 dB, `language=en`,
`timestamp_granularities[]=word`, keep words whose start < 5s. English-forced is right even for
Hinglish: it romanises, and the timings are what you need.

Two sanity rules on the result:
- The **first word of each window is clamped to the window edge** — distrust it.
- Cross-check every phrase boundary against the **20ms RMS silence map**, which is ground truth.

**The proof that settles a disagreement: does the reading explain the whole envelope?** The drifted
version left 1.16s of measured speech with no words in it. The isolated-window version accounted
for every span.

**Standing:** the generator asserts that every caption run overlaps a word from the isolated-window
word list, next to the ≤3-word and dead-air checks. Do this on every code-switched take.

## Step 3 — the RMS pause audit (standing, every reel, before rendering)

```python
# 10ms RMS envelope; threshold = floor + 0.45*(speech - floor)
# FLAG any caption run whose span is >75% below threshold
```

A run that sits over dead air **pops exactly when he stops talking**. Neither the review script nor
the vision pass catches it — the script's sync check is structurally meaningless on translated
captions, and the vision pass cannot hear.

**Why phrase boundaries alone are not enough:** pauses *between* phrases are respected
automatically, but a pause **interior to one phrase** is invisible to that check. Split the phrase
at the pause instead. This caught a model name in a HOOK landing on a breath 1.6s late, and a run
displayed entirely inside a 0.5s pause.

When the gate reports a big per-caption offset, **verify it against the source word times before
believing it** — one "worst offender" at −46 frames was exactly right, and the render's own
re-transcription had placed the word 0.8s early inside a 0.7s pause measured at −45 dB.

## Step 4 — run construction (the generator's rules)

| Rule | Why |
|---|---|
| **≤3 words, flushed unconditionally** | A grouper that flushes on `len(cur) >= 3 and word not in FUNC` grows to FOUR whenever the third word is a function word. Flush at `len(cur) >= 3`; try the trailing-function-word carry *inside* that branch, and leave ≥2 words behind so the carry can't strip a run to an orphan. **Every downstream repair (short-run merge, borrow) must re-check the cap.** |
| **Never open a run with an article** | The sync checker matches on the run's FIRST word and locks onto the wrong "a" — a false +17f. Split "a Lego world" into "even create a" / "Lego world", which also gives the emphasis its own beat. |
| **Never end a run on a function word** | The article travels with its noun. |
| **≥0.30s per run** | Below that it is a flash, not a caption — the bloom-in alone is 0.17s at 60fps. Merge the offenders; 4 short words on one plate still fit a 1010px lane at 78–82px. |
| **`to` is EXCLUSIVE — set it to the next run's `from` exactly** | `to = next.from - 1` leaves a **one-frame hole at every boundary** (~59 flickers in a 44s reel). A coverage checker must model the same exclusivity (`range(from, to)`) or it reports clean. |
| **Break on punctuation and pauses >0.45s** | |
| **Never split a sentence on its INTERNAL pause** | The >0.30s internal-silence rule exists to expose hidden RETAKES. A natural emphasis pause inside a continuous sentence is kept — cutting it reads as a jarring mid-sentence jump cut. Register changes may still land mid-clip; the AUDIO stays continuous. |

## Step 5 — assert anchors by SECTION, not by ordinal

Any `anchor(word, nth)` is a latent bug: the nth is a guess about a transcript, and the transcript
gets edited. Normalising `"3" → "three"` for consistent number rendering once handed `three` a new
first occurrence and moved a graphic **950 frames** — the beat's punch line fired on the section's
first frame instead of on the word. Every mechanical check passed; only a stray keyframe caught it.

```python
EXPECT = {"html": "M1", "typescript": "M34", "three": "PROJH", ...}
bad = [(k, section_at(v), EXPECT[k]) for k, v in ANCHORS.items()
       if k in EXPECT and section_at(v) != EXPECT[k]]
if bad:
    raise SystemExit("anchor/section mismatch — a graphic would fire in the wrong beat")
```

## Step 6 — every beat gets a caption

- **Suppress the lane caption only when the card is LITERALLY saying the words.** Copying that
  suppression onto a card that **paraphrases** left 3.7s of speech uncaptioned, and because every
  other section captioned normally it read as captions breaking, not as a style move.
- **Don't blank captions to dodge a layout problem.** Blanking through a 16-frame full→split move
  dropped a spoken run on the reel's biggest visual event. The caption rides the move at the
  full-frame y and hands over to the lane when the split lands — pick the move's timing so a run
  boundary falls there.

## Size and grouping (why runs are short)

Captions are **DISPLAY type**, not UI text: base ~72px at 1080 wide (serif emphasis ~1.12×), floor
**≥78px** for the caption register, with an auto-fit shrink only for a rare long line (estimate
width as `chars × size × 0.54` against the 1010px safe width). **Grouping follows size** — big type
will not fit nowrap beyond 3 words. Full-phrase 47–58px captions held for 2–3s have been rejected
twice, in those words.

Per-format placement (which band, which lane, what colour) belongs to the format skill —
`split-screen`, `caption-edit`, `broll-style-edit`.

## Language

Policy changed 31 Aug 2026: **translate Hindi speech into English captions.** The earlier
romanised-Hinglish rule is superseded. Confirm per batch if unsure. Translated captions are
distributed across a phrase span by character weight, which is exactly what makes the RMS pause
audit mandatory.

## Related

`cut-audit` proves the cut under the captions is clean. `take-geometry` gives the bands.
`reel-review` re-measures sync on the render — and reproduces the aligner's drift, so read its
offsets with that in mind.
