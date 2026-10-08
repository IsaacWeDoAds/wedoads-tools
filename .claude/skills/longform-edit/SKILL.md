---
name: longform-edit
description: "LONG-FORM 16:9 edit pipeline (YouTube talking-head, 8–20 min) learned on lf01 'AGI is here. Now what?' (Sep 2026). The creator cuts in Palmier with his own taste; I layer source-anchored motion graphics, b-roll, generated clips, SFX and zooms onto HIS timeline over the Palmier Pro MCP, then review, export and normalise. Use for: 'layer the long-form', 'add graphics to my Palmier cut', 'long-form MG pass', 'heroes for the YouTube video', 'export the video'. NOT for 9:16 reels (shortform-cutaway / shortform-finish) and NOT for vlogs (no typography)."
---

# LONGFORM EDIT — layering a Palmier cut (16:9)

> **THE JOB:** He trims the talking-head take in Palmier. I never re-cut it. I build a source-anchored
> plan (every graphic lands on a spoken word), render alpha windows in Remotion, and place windows, b-roll,
> generated clips, SFX and zoom keyframes natively on his timeline through the Palmier Pro MCP. He checks in
> Studio; I export through the same MCP and ship a −14 LUFS copy. Reference implementation: `src/LF01/`,
> `work/lf01/work/`, and the reusable kit at `<media-drive>/MG-Kit/lf01-longform-2026-09/`.

> **No Palmier pre-cut? Cut from raw and build in HyperFrames** — the lf02 route (registers F/S/D/P/B,
> full-width screen card, mirrored drawer, sectioned export): `references/hyperframes-longform.md`.

## 0. Preconditions (check before anything)
- SSD mounted: `<media-drive>` (`out/` is a symlink to `VideoEdits-out`; the MG kit and the SFX
  library live there). exFAT: no hardlinks (copy fallback), `shutil.move` across the boundary.
- Palmier open on the RIGHT project. First line of every mutating step: `manage_project list` →
  `active.name`, then count the take's clips on V1 against the segment map; refuse otherwise. He switches to
  other projects mid-session; a guard is not optional.
- Disk: bundles copy `public/` (13 GB) — keep a slim symlinked `public-<reel>` (render-ops §2; hardlinks fail on the SSD) and a persistent bundle
  (`qa.mjs`); delete superseded `out/<reel>/palmier/v*` dirs that no clip references.

## 1. Inputs → the map
1. Source take(s) + his Palmier project. Read the timeline (`get_timeline` once), find V1 clips of the take
   → `palmier_segments.py` writes `SEGMENTS` (cut frame → source second) and the timeline `offset`.
   **Rebuild the map from the live V1 before every pass** — he re-trims between passes (116/122 clips moved once).
2. Transcript: WhisperX on the SOURCE take, chunked for Hinglish/noisy audio; anchor on short isolated
   windows (a long segment once ran 2.9 s early). Word list `{s,e,w}` → `work/<reel>/work/<reel>_wx_en.json`.
3. Fact-check every number/claim in the VO against the live page before it becomes a graphic.

## 2. Asset plan (confirm with the creator before rendering anything)
Classify every beat: **hero** (MG set piece), **lockup** (word-at-a-time emphasis), **stamp** (name/logo
chip), **b-roll** (his library, native res, one clip = one use), **generated** (Veo/Omni, cost-gated),
**full card** (site capture, box intro, chapter, typed list), **news montage** (yt-dlp chapters → bites →
word chain). Write `docs/<reel>-asset-plan.md` with anchors, and keep it as the decision log.

Format rules (measured on lf01):
- **Face spine** x 760–1160 / y 210–560: nothing on it, ever. Text lives in the side lanes (x 96–716,
  x 1204–1824), the bottom strip (y 620–1020 over a scrim), or the top band (y < 200).
- **Registers hard-cut.** No split screens with him inside a box except the intro; full cards are opaque
  from frame one; typed lists are near-opaque full-screen and open on the FIRST ITEM's word (−12 f), never
  on the kicker alone.
- **Density front-loaded:** cold open every ~0.5 s, first minute ≥ 1 event/2 s, no bare talking-head run
  > 10 s anywhere; ≥ 3 moving elements in any hero; something always moving inside a card.
- **Type:** Apple-HIG on dark translucent material (`apple.ts`), Inter Black / JetBrains Mono / Alex Brush /
  SF Pro voices; lockups ≥ 130 px, stats ≥ 60 px, chips ≥ 40 px, logos ≥ 72 px; one word arrives per click.
- **Named claims get the real clip** (Pichai says it → the Decoder clip, not a quote card); brands get their
  own wordmark type; phone-portrait clips as centred panels over a blurred fill, never rotated/stretched.
- **CTA** = like pill filling + a viewer's comment box typing the reply he asks for.
- **Holds** clamp to asset length (ffprobe in the generator) — every frozen run once was a shot outliving
  its clip.

## 3. The generator (`src/<Reel>/gen_data.py`)
One line per cue, anchored to a word (`w(word, near_second)` picks the nearest occurrence — pass the exact
second, first occurrence when a phrase repeats):
```python
hero(w("70,000", 281.8), 9.6, "hiring", "card", until=w("want", 293.3), items=[("70,000", 281.8, "67,000"), …])
hero(w("three", 1288.5), 37.5, "recap1", "lane", type="list", title="simple three things", items=[…])
emph(w("roadmap", 55.1), 1.5, "no roadmap.", lead="without knowing the", style="ui", size="xl", place="B")
emph(w("freshers", 287.8), 2.4, "for experienced people, *not for freshers*.", style="line")
stamp(w("CEOs", 425.6), 3.0, "JENSEN HUANG", sub="NVIDIA CEO · Feb 2024", raw=True, top=40)
broll(w("office", 105.2), "office-desk-01", 2.4); gen(w("maze", 46.0), "maze-anime", 5.0); sfx(...)
```
It emits `data.ts` (HEROES / EMPH / STAMPS / SHOTS / SFX cues / zoom keys) and the plan
(`palmier_plan.py` → type windows, full windows, b-roll, gen, sfx lanes). Every SFX cue: one sound per
visible event from the skill kit, whoosh 0.5 / others 0.2, a keyboard tick per arriving word, peak-scheduled.

## 4. Render (Remotion, alpha)
- Type windows: ProRes 4444 with alpha (`palmier_render.mjs render type:<i>`), 1920×1080 @ 30 fps;
  full cards as opaque mp4. Re-render only windows whose bounds OR contents changed (diff
  `palmier_plan_placed.json` vs new plan); delete the stale `type_<from>.mov` first.
- QA stills before placing: `hero_stills.json` → `palmier_render.mjs stills` → look at them.
- No hooks in `.map()`, Root imports every reel, 10-bit HEVC freezes OffthreadVideo, N cuts drift AAC.

## 5. Place on his timeline (Palmier Pro MCP, `palmier.py` over 127.0.0.1:19789/mcp)
- Versioned imports: copy renders to `out/<reel>/palmier/v<N>/` so Palmier sees a NEW asset (it caches by
  path); the media cache in `palmier_state.json` maps path → mediaRef; keep the `~/out/...` path.
- Tracks: Cards, Type (topmost — reorder after every pass), Generated, Broll, SFX1–8 + Preroll audio lanes.
  Text layers need their own lanes (overlaps on one track truncate silently). `graphics` places
  cards+type, `broll`/`gen` native clips with `set_keyframes` zoom on every talking-head clip, `sfx` lanes,
  `sfxfix` volumes/fades, `reorder` pins Type on top.
- Swapping a window: remove every Type clip OVERLAPPING the new range, then add (`palmier_retype.py`).
- After any change: `palmier_review.py <src seconds…>` → composited contact sheets from `inspect_timeline`.

## 6. Review gate (never skip)
1. Sheets of every hero moment + 20 standard picks → **Fable 5 vision agent** (captions, overflow, face
   crossings, legibility, rotated clips, empty cards, register hard-cuts). Fix BLOCKERs, re-place, re-sheet.
2. Deterministic: caption/lockup sync against the transcript, holds vs asset length, frozen runs.
3. He watches in Studio; his notes come back as one list — apply them all, one pass, one re-sheet.

## 7. Export + delivery
- `export_project {mode: video, codec: H.264, resolution: "Match Timeline", outputPath}` → poll
  `manage_exports list` every 30 s via the HTTP wrapper (the Claude MCP link drops while it renders).
  ~4 min per 15 min at 1080p60.
- Verify: frame count == timeline; `freezedetect`/`blackdetect`/`silencedetect` at 480 px; stills at the
  beats. Read flags against the plan (a near-opaque card with only a kicker = a hole; a fully typed list
  holding 2 s = fine). Confirm glyph doubts from the rendered file, not the inspector (its grid draws strokes).
- Loudness: Palmier's mix ≈ −17.5 LUFS → two-pass `loudnorm I=-14 TP=-1.5 LRA=11 linear=true` with
  `-c:v copy`, measure the ENCODED copy from the ebur128 `Summary:` block. Ship `<name>_-14LUFS.mp4`.
- Send the beat contact sheet, not the 1.8 GB file. Caption + DM asset ship with every final.

## 8. Afterwards
- Export the graphics into the MG kit (`<media-drive>/MG-Kit/<reel>/`): sources, alpha windows with
  an INDEX from the plan, contact sheets, prompts, SFX cues, decision log. Update `docs/mg-kit.md`.
- Write the memories: take geometry, every rejection, every tool trap.

## Scripts (this skill's `scripts/` mirrors `work/lf01/work/`)
`palmier.py` (HTTP MCP wrapper) · `palmier_segments.py` (live V1 → SEGMENTS) · `palmier_plan.py` (windows +
lanes) · `palmier_render.mjs` (bundle / render / stills) · `palmier_preimport.py` (versioned import) ·
`palmier_place.py` (graphics / broll / gen / sfx / sfxfix / preroll / droptrack / reorder, identity guard) ·
`palmier_retype.py` (swap windows) · `palmier_review.py` + `palmier_inspect.py` (composited sheets) ·
`qa.mjs` (persistent bundle) · `sfx_lib.py` / `sfx_check.py` · `finish_place.sh` / `finish_cta.sh` (restartable
finishes) · `ingest_cut.py` (his export → segment map).

