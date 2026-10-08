---
name: broll-select
description: "Pick b-roll from his own 535-clip library (and from YouTube for reference footage) and place it WITHOUT ever upscaling. Covers the catalogue and how to grep it, the orientation-vs-recency conflict that bites every asset plan, the pre-crop-at-native-res rule, rotation side-data checks, motion-scored in-points, clamping holds to asset length, and the portrait-clips-in-16:9 patterns. Use during any asset plan that needs footage, and whenever a b-roll shot looks soft or freezes."
---

# B-ROLL SELECT — his own footage, at native resolution

> **His own real footage beats generated b-roll every time.** Abstract generated b-roll that only
> illustrates a mood gets rejected. **Grep the catalogue FIRST**, before proposing anything
> generated.

## The library

`<media-drive>/Brolls` — **535 files**, frame-sampled and sorted into 19 category folders.
Full per-file catalogue (duration + orientation per clip) at `INDEX.md` on the drive, copy in the
repo at **`docs/broll-catalog.md`**.

```
01-coding-desk-work (incl. the cafe-* night work-from-anywhere set)
02-desk-setup · 03-talking-to-camera · 04-youtube-creator · 05-thinking-writing
06-lifestyle-home · 07-walking-outdoor · 08-gym-fitness · 09-driving-car
10-food-cafe · 11-outfits-sneakers · 12-unboxing-products · 13-office-startup
14-events-moments · 15-travel/ (9 per-trip subfolders + flights) · 16-photos
18-retro-arcade-store · 19-family · 20-old-reels-archive (finished exports — reference, not raw)
```

Files are renamed `<description>__<original-name>` — **the original camera name survives after the
`__`**. The Aug-2026 clips are 1080p60 and slow-mo cleanly. There is no junk folder any more; he
deleted it.

## The rule: never upscale

> *"don't zoom brolls, it'll reduce the quality."* — given twice, on two different reels

A 9:16 reel is 1080×1920. A landscape 1920×1080 clip has to be scaled **~3.2×** to fill it, and any
punch-in on an already-1080-wide portrait clip upscales too. Both resample and visibly soften — the
b-roll ends up looking **worse than the phone take it is cut against**, which is the opposite of
what it is there for.

**The test:** compute `card_width / source_width` after all transforms. **If it is ever > 1, the
footage is being upscaled** and the shot needs a re-crop, not a scale.

How to place:
- **Prefer clips natively 1080×1920** and place them `objectFit: cover` with **no transform** — a
  true 1:1 pixel mapping.
- **Pre-crop the source to the card's exact aspect at native resolution**, then render at `zoom = 1`.
  For a 1000×490 card (2.04:1): `crop=1920:941:0:120` straight from the 1920×1080 original — a pure
  downscale into the card, no upscale anywhere.
- **Do NOT pre-scale the clip down first.** One attempt encoded b-roll at 1600px wide "to save
  space", throwing away 320px before the card ever saw it. **Crop from the original resolution.**
- Landscape clips: **downscale into a card or band** (free), or **drop them**. Never blow one up to
  full-bleed.
- **No Ken Burns, no scale animation, no punch-in on b-roll.** Stacks with the no-zoom-at-cuts rule.
- Prep with **no `scale` filter at all** — `fps` + `format` only.

**Site/UI captures are a different case.** A zoom on a 1440×900 Playwright capture inside a 1000×490
card is still a *downscale*, and there it is doing legibility work. Prefer `zoom: 1` and **re-record
with a better scroll target** when the framing is wrong.

## The conflict that bites every asset plan

Two standing preferences that pull against each other:

1. *"Don't zoom b-roll, it'll reduce the quality."*
2. *"Use the most recent ones, only use old ones if needed."*

Because of how the library was shot, these usually **cannot both be satisfied**:

- The **Aug-2026 batch (29 clips)** is **28 landscape 1920×1080 and exactly ONE portrait**.
- Most **natively 1080×1920** clips are the **older DJI 2024 sets** (`06-lifestyle-home`,
  `07-walking-outdoor`, parts of `15-travel`).
- **`19-family` (17 clips)** has the same problem — only one is natively portrait, and two more are
  1920×1080 carrying `rotation=-90` side data, so they need autorotate handling, **not a crop**.

**Filter the catalogue by ORIENTATION first, then by recency. If the only recent option is
landscape, say so explicitly and let him choose** — don't silently upscale, and don't silently reach
for an old clip either. Give him rule 1 as the reason, not convenience.

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,side_data_list -of json <file>
```

**Always check `stream_side_data=rotation`, not just w/h.** Rotation side data survives ffmpeg
re-encodes and lies to OpenCV and trackers; horizontal footage gets tagged −90 and a phone can flip
mid-clip. Bake it with `-display_rotation 0` + transpose and **verify by LOOKING at a frame** — the
fix is 0° or 180°, never 90°.

## In-points must be motion-scored

Catalogue-listed in-points land on still moments and produce frozen-frame FAILs. **Score windows by
min-frame-diff** (sequential grey decode, argmax of the window minimum) and pick in-points from
that. 30fps lifestyle b-roll especially.

**Score the CROPPED region, not the full frame.** One clip froze because the people move at the
frame edges, outside the centre 1080 crop — full-frame score 4.13, crop-region truth: a dead board.
**Pick `(in_point, crop_x)` jointly.**

## Clamp every hold to the asset's length

`OffthreadVideo` past the file's end simply **holds the last frame — silently, no warning** — and a
held frame reads as a broken render. Six "frozen runs" in one review were all this: a 4.6s clip
scheduled for 5.4s (×3 uses), a 5.1s clip for 8s, an 8s clip for 12.6s.

```py
dur = min(dur, asset_dur - srcFrom - 0.15)      # ffprobe every asset once; PRINT what got clamped
```

- Keep short clips for short beats.
- **Spread repeated uses of one clip across different offsets**, or use a longer clip.
- **Do NOT add a minimum-duration guard on the scheduled length** — it deleted deliberate 0.55s
  glitch flashes in a hook. Guard on the **asset's remaining room** instead.
- **One b-roll, one use.** Never repeat a clip in the same video.

## Portrait phone clips in a 16:9 edit

A portrait clip cropped to 16:9 is 1080×607 and would need a 1.78× upscale. Two patterns instead:

- **Two-up:** bake the rotation per source (`-display_rotation:v:0 0 … -vf transpose=1`), scale each
  to **608×1080** (a downscale), `hstack` with an 8–12px gap, over a `gblur=45 + eq brightness −0.3`
  blurred copy of one clip as the fill. **Pick two DIFFERENT moments** (talking vs laughing) so it
  reads as a pair, not a mirror.
- **A photo:** `PIL.ImageOps.exif_transpose` **first** (ffmpeg's jpeg path is not reliable about
  EXIF), crop the 16:9 band holding the faces, then `zoompan z=1→1.10 d=90 s=1920x1080` — `crop`'s
  w/h expressions cannot animate (`t` is only valid in x/y); `zoompan` can.
- **Verify by extracting the LAST frame and looking**: faces upright, no black bars inside the panels.

## Reference b-roll from YouTube

When the reel talks about a company's design or product, **show THEIR footage moving** — a static
homepage is a dead beat.

- Keep `yt-dlp` updated. **A stale build 403s on everything** (one on this machine was a year old).
- **Find the segment with CHAPTERS, not "the first 4 minutes":** `yt-dlp -j URL` → `chapters[]`. One
  segment was at 26:00–29:05 of a 95-minute show; the first fetch of `*00:00-04:00` got the market
  open. Then `--download-sections "*26:00-30:00" --force-keyframes-at-cuts`.
- **Pick the LONGEST sustained shots.** Scene-detect at 0.30 and look for gaps ≥3.5s — a
  brand film averages ~1.9 cuts/s, so a long hold IS a sustained UI animation.
- **Map chyrons to timestamps with a labelled sustained-shot sheet:** grab start+1.5s of each shot
  with `drawtext` of the timestamp, tile 6×4. One sheet per clip tells you exactly which second
  carries which lower-third.
- **Extract NAMED shots** (CFR 30, muted) rather than conforming whole clips, generated from the
  same dict the register map uses.
- **Check every chyron against the VO.** One carried "FIRMS ARE HIRING FRESHERS WHILE REDUCING
  MID-LEVEL ROLES" — the opposite of the spoken claim — so that shot was never scheduled even though
  it was the best source for the beat. Same class as `asset-plan`'s fact-check.
- Crop to the card aspect **at native res**. Flag once that this is copyrighted marketing footage
  used as commentary b-roll; it is his call.

## Related

`asset-plan` (grep the catalogue before proposing `genvideo`) · `screen-capture` ·
`render-ops` (frozen frames) · `mg-kit`.
