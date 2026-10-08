---
name: render-ops
description: "Get a render out of Remotion and onto disk correctly — slim symlinked public dir + persistent bundle (a bundle copies the whole 13 GB public/), per-reel entry files, parallel-session contention and the silently-STALE render, the Node-API traps that silently render to nothing, audio drift across segments, frozen-frame detection, loudnorm measured on the ENCODED file, and the delete/namespace rules for a repo several sessions share. Use before, during and after any render, and whenever a render fails, freezes, drifts, or produces the wrong file."
---

# RENDER OPS — the render, and getting it out intact

> **THIS REPO IS SHARED BY SEVERAL LIVE SESSIONS AT ONCE.** Most of the failures below are not code
> bugs; they are contention, and treating them as code bugs is what costs the day.

## Before you render

### 1. Give the reel its own entry file

`src/Root.tsx` imports every composition, so **a compile error in ANY sibling reel takes down your
bundle** — with an error naming a reel you never touched. A half-written `src/Reel25/Final.tsx` once
failed a Reel04 render with `ReferenceError FACE_NOPLAN is not defined`.

```tsx
// src/reelNN-entry.tsx
import "./index.css";
import { Composition, registerRoot } from "remotion";
import { ReelNNFinal, REELNN_FRAMES } from "./ReelNN/Final";
registerRoot(() => (
  <Composition id="ReelNNFinal" component={ReelNNFinal}
    durationInFrames={REELNN_FRAMES} fps={60} width={1080} height={1920} />
));
```

Keep the `Root.tsx` registration too (Studio needs it). It is also **noticeably faster** — one
reel's assets instead of a dozen.

**Do NOT "fix" another session's broken file to unblock yourself, and do not comment out its import
in the shared Root.tsx.**

### 2. Slim public dir + persistent bundle

**Every bundle COPIES the whole `public/` — which is 13 GB here**, because every reel's b-roll lives
in it. A killed render orphans its copy, and `/var/folders/…/T` has held **22 GB** of dead
`remotion-webpack-bundle-*` and `remotion-*-assets*` dirs, taking the disk to `ENOSPC` mid-bundle.

```js
rmSync(resolve("out/reelNN/bundle/public"), { recursive: true, force: true });
const serveUrl = await bundle({
  entryPoint: "src/reelNN-entry.tsx",
  outDir:     resolve("out/reelNN/bundle"),   // FIXED dir — temp bundles stop piling up
  publicDir:  resolve("publicNN"),            // slim tree of SYMLINKS (zero extra bytes)
  symlinkPublicDir: true,
});
```

- Build the slim tree with **absolute symlinks** (`ln -s "$PWD/public/…"` / `os.symlink`) into
  `public/` — zero disk, and Remotion forwards each link into the bundle instead of copying it.
  Include only what the reel references: `broll/reelNN/*`, `sfx/*`, `broll/shared/avatar.png`.
  **Not hard links any more:** since Oct 2026 the per-reel media under `public/` and `work/` are
  symlinks into the exFAT SSD (`scripts/ssd_media_move.py`), where `ln -f` / `os.link` fail with
  `Operation not supported` or `Cross-device link`. Old `slim.sh` / `prep_cut.py` files still use them.
- **`outDir` and `publicDir` must be ABSOLUTE** or webpack throws
  `Invalid configuration object … absolutePath`.
- A fixed `outDir` keeps the public **symlink** between runs, so the next `bundle()` throws
  `EEXIST: symlink`. **Delete just that symlink**; the rest of the webpack cache is worth keeping.
- Result: 21 MB bundles instead of 6 GB, and stills render off one bundle instead of re-running
  webpack per frame.
- **Studio's dev server (`localhost:3000`) is NOT a usable `serveUrl`** — `renderStill`/`renderMedia`
  fail with `window.getStaticCompositions is undefined`. Tried; does not work.

Before any bundle: `ls -dt /var/folders/*/*/T/remotion-*`, **look**, confirm no live render process,
then remove the dead ones.

### 3. Check who else is rendering

```bash
pgrep -f "remotion render" | wc -l
vm_stat
```

**Exit 144 means OOM, not a code bug.** Six simultaneous renders once took the Mac to 48 MB free
RAM, 14.7 GB of 15.3 GB swap, load average 43 — and killed every render including its own.

- **Do not retry blindly and do not "fix" the composition in response.**
- **Queue**: poll every 30s until ≤2 renders and >800 MB free, then render at `--concurrency=2`.
  (Worked on the first try after 133 checks, ~65 min.)
- **Never kill another session's render** to free memory — flag it and let him choose.
- If a duplicate render of the same output path is running, **copy the finished file aside before
  killing it** — Remotion muxes at the very end and the second run will overwrite a good result.

## The three concurrency failures — don't confuse them

| Symptom | Cause | Fix |
|---|---|---|
| `exit 144`, killed partway, no output | Memory exhaustion | Queue, `--concurrency=1`, chunk it |
| Bare React `commitHookEffectListMount` stack, no output — **but `remotion still` renders the same frames fine** | Resource starvation, not a component bug | `pgrep -fl remotion` before blaming the code |
| **A valid MP4 built from PRE-EDIT code**, exit 0, nothing errored | Concurrent sessions fighting over `node_modules/.cache/webpack` | `--bundle-cache=false`. **Never delete the webpack cache while another session is mid-render** |

The stale-render case is the worst: `remotion still` shows your change, the rendered MP4 does not,
and the only warning is a `[webpack.cache.PackFileCacheStrategy] Caching failed … ENOENT` line that
looks harmless. It once dropped two motion-graphics beats.

**Never pipe a render through `tail`/`head`** — the shell reports the *pipe's* exit code, so a
failed render looks like `exit 0` and the real error scrolls away. Redirect to a log file.

**Chunked renders must be concatenated VIDEO-ONLY.** A single pass that dies at the *encode* stage
(after all frames are done) recovers as 8 resumable chunks at `--concurrency=1`.

## The Node-API trap that silently renders to nothing

```js
renderMedia({ …, output: "out/x.mp4" })          // ❌ silently ignored
renderMedia({ …, outputLocation: "out/x.mp4" })  // ✅
```

`output` is not a member of `RenderMediaOptions`. `renderMedia` renders the **entire composition to
nothing**, reports **100% progress**, and **resolves successfully**. Two full 43s renders were lost,
and because the script's own `console.log("✓")` ran after the await, the log looked clean both
times.

- **Tell:** progress reaches 100%, the script prints success, and the file is not on disk. Do not go
  looking for a deleter.
- **Guard:** `statSync` the output after `renderMedia` and throw if absent or implausibly small.

## Composition traps that survive into a render

1. **`OffthreadVideo` repeats frames on 10-bit HEVC.** iPhone HLG masters are 10-bit HEVC. Always
   transcode to 8-bit H.264 (`-c:v libx264 -pix_fmt yuv420p`).
2. **Tight GOP or renders crawl.** OffthreadVideo seeks per frame. A default GOP put one render at
   **70 minutes**; `-g 30 -keyint_min 30 -sc_threshold 0` brought it to **7**. In a 50-50 split the
   same file is seeked twice per frame and a long GOP becomes **fatal** — a
   `delayRender() … "Fetching …proxy?src=…" was called but not cleared after 28000ms` is a
   **keyframe-density** problem, not a timeout problem. Raising `--timeout` only buys a slower
   failure. Use `-g 15` for split-heavy reels.
3. **Don't decode the base where it isn't visible.** Declare `BASE_VISIBLE` windows, clip `BaseCut`
   to them, and carry the voice elsewhere with an audio-only `<Audio trimBefore/trimAfter>`. Mute
   the visible `OffthreadVideo` or the VO doubles.
4. **A `<Sequence from={X}>` RESTARTS any video inside it** — this is how a face card loses lip-sync.
   The card replays the opening of the reel while the base carries audio 10s ahead. **Invisible in a
   caption-sync check**, because the captions were right. Any component re-rendering the base must
   read the ABSOLUTE composition frame. Test: `ffmpeg -ss T -i cut.mp4` vs the rendered still at the
   same frame.
5. **A layer that cues off ANCHORS must NOT sit inside a `<Sequence>`.** Anchors are absolute; inside
   a Sequence `useCurrentFrame()` is relative, so every cue compares against the wrong clock and the
   layer renders at opacity 0 **forever**. One overlay was invisible for its entire 6 seconds and
   nothing threw.
6. **Bound the grow dismissal to a WINDOW.** `f >= GROW_AT ? fade : 1` stays true for the rest of the
   reel and silently zeroes every later caption. Use `f >= GROW_AT && f < BODY[1]`.
7. **Never call a hook inside `.map()`.** It appears to work while the array length is constant.
   Hoist the frame and use a pure helper taking `frame` as an argument.
8. **`transformOrigin: "center center"` needs a box with real height.** Scaling a wrapper whose only
   child is `position:absolute` scales about a zero-height box — the FollowCta card flew off the top
   of the frame.
9. **Reframe a face card with `objectPosition`, never `scale(<1) translateY()`** — the shrink lets
   the card's background show at the edges (it read as a black strip under the chin).
10. **SMIL (`<animateMotion>`, `<animate>`) does NOT render deterministically.** SVG animation is
    driven by the browser's wall clock, so a headless render captures whatever it happened to read.
    It looks correct in Studio. Compute the position yourself from `frame`.
11. **A transparent render needs `--image-format=png`** or alpha is silently lost — and dropping the
    pixel-format flag to make the error go away produces a **fully opaque .mov** that every alpha
    guard reads as 100% coverage. Full incantation:
    `--codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png`.
    **Make any guard FAIL when it inspected zero frames** — a guard that passes on an unreadable
    render is worse than no guard.
12. **Check `src/Root.tsx` for composition-id collisions** before registering. Ids are strings with
    no compile-time uniqueness check.

## Frozen frames

`OffthreadVideo` serves **stale frames rather than erroring**, so the render "succeeds" and the
defect only shows on playback. One reel shipped **105 frozen frames of 1095 (9.6%)**, including runs
of 14+ identical frames.

**Cause: too many concurrent decodes.** Push the compositing into ffmpeg instead:
- Pre-bake every b-roll shot to a finished 1080×1920 clip (blurred backdrop + native crop, baked) so
  Remotion plays ONE file.
- Transcode the take to H.264 **at the composition's exact fps**. Never leave a 60fps HEVC mounted.
- Split the VO to its own `.m4a` and drive the audio spine with `<Audio>`, so b-roll shots cost
  **zero** video decode.
- Mount the take's video **only on the shots that show it**.

Net: exactly one video stream mounted at any frame. Keep only cheap CSS filters live.

**Detect it on every delivered file** — never trust the eye or a successful render:

```bash
ffmpeg -v error -i out.mp4 -vf \
  "tblend=all_mode=difference,signalstats,metadata=print:file=/tmp/s.txt" -an -f null -
# count frames whose lavfi.signalstats.YAVG < 0.06  → frozen
```

Anything above ~0.5% needs investigating.

## Audio drift across segments

A cut played as N `<Sequence>` + `<OffthreadVideo startFrom/endAt>` pairs comes out **frame-exact in
video and NOT in audio**. Each segment's audio snaps out to the next AAC frame boundary (1024
samples @48k ≈ 1.28 frames at 60fps), so the lag **grows monotonically** — ~0.6 frames per cut:

| window | lag |
|---|---|
| 0–5s | +2.4 f |
| 15–20s | +5.4 f |
| 30–35s | +9.0 f |
| 45–50s | **+12.0 f** |

**Invisible to the usual checks** — frame count is right, duration looks right, and the review
script flags it as a *caption* problem, sending you off to fix captions that were already correct.
Even ONE uncut segment starts its audio **2048 samples (42.7 ms, 2.6 frames) late**.

**The fix:**
1. `muted` on the base cut's `OffthreadVideo`, so Remotion's audio track carries **only SFX** — each
   SFX is a single `<Audio>` at an absolute start frame and cannot accumulate error.
2. Rebuild the VO **outside** Remotion: decode the take to ONE wav, slice by **sample index**
   (`round(srcFrom/60 * sr)`), concatenate. Do NOT cut N spans out of the AAC with `-ss/-t` — that
   loses a fraction per span too (8 frames off the tail on the first attempt).
3. `amix` VO + SFX, `apad`, then **`atrim` the AUDIO only**. **Never bound the video with `-t`** — it
   silently dropped 7 frames off a 3333-frame render.

## Loudness — measure the ENCODED file

`loudnorm=I=-14:TP=-1.5` limits its own **PCM** output; the AAC encoder then reconstructs
inter-sample peaks **above** that ceiling.

| filter | encoded result |
|---|---|
| `loudnorm I=-14 TP=-1.5` | −14.8 LUFS / −0.5 dBTP |
| two-pass, `TP=-1.5` | −14.3 LUFS / **+0.3 dBTP** ← clipping |
| `+ alimiter=0.72`, TP=−2.5 | −15.1 / −1.7 ← too quiet |
| **two-pass, `TP=-3.0`, no limiter** | **−14.6 LUFS / −2.4 dBTP** ✓ |

**`alimiter` is not the fix** — at any ceiling low enough to control the peak it drags the integrated
loudness down with it.

1. Measure the finished WAV: `loudnorm=I=-14:TP=-3.0:LRA=11:print_format=json`.
2. Apply pass two with `measured_I` / `measured_TP` / `measured_LRA` / `measured_thresh` / `offset`
   fed back. The extra 1.5 dB of headroom is the **encoder allowance**.
3. **Re-measure the ENCODED mp4**, never the filter's summary. A single-pass "Output True Peak −1.5"
   is a claim about audio that no longer exists.
4. **Force `-ar 48000`.** loudnorm resamples internally (192 kHz) and the AAC encoder inherits it —
   one deliverable shipped at **96 kHz**, which Instagram does not expect. Add
   `-af "…,aresample=48000" -ar 48000` and re-probe `sample_rate`.
5. **On a quiet phone-mic take loudnorm silently runs in DYNAMIC mode** (LRA 5.5 → 3.3, every SFX
   pinned to the ceiling). Pre-gain + `alimiter` **first** so the normalisation stays linear.
6. `review_reel.py` printing `true peak None dBTP` means it could not parse the value. **A missing
   number is not a pass** — verify by hand.

SFX make all of this worse: transients ride on top of a normalised voice, so a mix that is fine
before SFX can clip after.

## Disk and the shared repo

- **`out/` is a symlink to `<media-drive>/VideoEdits-out`** (since 6 Sep 2026). **Check the
  SSD is mounted before any render or Palmier placement** — if it is absent, `out/` is a dangling
  link and Palmier shows every render clip offline. Palmier media were imported under the
  `<repo>/out/…` path: **keep the symlink name**, never re-import under
  `<media-drive>/…` or the cache in `palmier_state.json` splits.
- macOS ships rsync 2.6.9 — no `--info=progress2`; use plain `rsync -a` and verify with a size walk.
- **`out/` is not automatically yours.** Before removing anything under `out/`, `work/`,
  `public/broll/` or `public*/`, check it against the reel YOU are building. A directory you don't
  recognise belongs to someone else. Free disk by deleting **your own superseded renders only**, and
  ask before deleting any of his renders.
- **Inspect in a SEPARATE call from the delete.** `ls DIR; rm -rf DIR` in one Bash call means the
  listing reaches you *after* the delete has run. It looked like a check; it wasn't, and it destroyed
  another session's finished deliverable — `rm -rf` does not use the Trash and there was no APFS
  snapshot. Say so immediately when it happens, with what is gone and what survives.
- **Namespace the whole reel** when another session may be on the same number. Take a distinct
  suffix for **everything at once** — `work/reel49ai/`, `public/broll/reel49ai/`, `src/Reel49AI/`,
  `src/reel49ai-entry.tsx`, `public49ai/`, `out/reel49ai/` — rather than sharing any one path.
  Symptoms of a collision, in the order they appear: an alignment JSON transcribing a *different*
  script, `moov atom not found` mid-session (their conform overwriting your file), and your
  intermediates **vanishing between two commands**. Treat `out/` as volatile: re-check your
  intermediate still exists immediately before each step that consumes it.

## After the render

**A killed render can leave a partial mp4 that looks valid.** Always verify `nb_frames` against the
composition's `durationInFrames` before trusting it — one draft came out 3540/3801 frames and probed
fine otherwise.

Then run `reel-review`. Never hand over an unreviewed render.

## Related

`reel-review` · `sfx-design` · `caption-align` (the drift above will be misreported as a
caption bug) · `longform-edit` for the Palmier export path.
