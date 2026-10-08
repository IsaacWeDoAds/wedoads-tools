# Omni Flash restyle treatments

A named vocabulary of world-transformations for hooks and register beats, built
for Gemini Omni Flash video-to-video. Companion to `docs/reel-edit-styles.md`.

## The one rule everything here obeys

**Transform the room, never the person.** Measured 12–13 Aug 2026: prompts that
change the environment return his face intact; prompts that change *him*
(wardrobe, lighting on skin) return a slimmer, smoother, younger stranger.
Every prompt below opens with the same identity guard for that reason. Keep it
verbatim when you write new ones.

## Known behaviour

- Output is always **720×1280, 24fps** — no resolution option exists. Plan the
  card width around it, or accept a 1.5× upscale for the hook only.
- **10s input works**, returned within 3ms of source length (app). The API run
  drifted +2.3% on 5s clips — retime with `setpts` before any side-by-side.
- Lip sync holds, but slips around transitions (410ms off across the first
  half of the 10s run, 0ms in the second). Check the tail of every clip.
- **It under-delivers pacing.** Asked for a change every 1.2s, it gave ~3.3s.
  Name explicit timestamps in the prompt ("at 0.8s… at 2.4s…") rather than an
  interval, and expect to still be told no.
- Transitions come back as hard sweeps across frame, not crossfades — which is
  already the register rule from `reels-safe-zone-and-face-rule`.

## The identity guard (prefix every prompt with this)

```
Keep the person exactly as filmed. His face, hair, beard, skin, clothing, the
object in his hand, his gestures and his position in frame must not change at
all. Transform only the room around him. Never place any object, graphic or
text over his face.
```

---

## 1. Vox explainer

Archival newspaper and textbook pages as the back wall, red marker circles and
arrows annotating the space around him, yellow highlighter swipes, rubber-stamp
marks, halftone photographs pinned at angles.

**For:** analysis reels, "here's what's actually happening", any claim that
wants an evidence frame. **Verified:** not yet.

```
[identity guard]
Rebuild the room as an archival explainer collage: the back wall becomes old
newspaper columns and yellowed textbook diagrams, with hand-drawn red marker
circles and arrows annotating the objects around him, yellow highlighter
swipes across the print, and small rubber-stamp marks. Halftone black-and-white
photographs are pinned at slight angles. The annotations draw themselves on.
Keep all marker marks and paper well clear of his head and face.
```

## 2. Documentary evidence board

Corkboard wall, pinned photographs, red string running between pins,
desaturated filmic grade, visible grain, dust drifting in a hard shaft of light.

**For:** story and investigation reels, the "how this actually went down"
register. **Verified:** not yet.

```
[identity guard]
Rebuild the room as a documentary evidence wall: cork board behind him covered
in pinned photographs, index cards and printed pages, with taut red string
running between the pins. Desaturate the whole environment to a cold filmic
grade with visible 16mm grain, and add slow dust drifting through a hard shaft
of light from the left. Keep the board and string clear of his head.
```

## 3. Paper-cutout craft — VERIFIED

Layered pastel paper landscape, paper plants, clouds and flowers, soft craft
shadows. Warm and friendly.

**For:** personal and warm content — the @unscripted.nishant family and
trajectory reels. **Verified:** 13 Aug 2026, held identity across 10s.

```
[identity guard]
Rebuild the entire room as layered paper-cutout craft: pastel paper walls in
warm peach and cream tones, paper plants, paper clouds and paper flowers, all
with soft craft shadows between the layers. A few loose paper leaves drift
slowly through the air.
```

## 4. Blueprint schematic — VERIFIED

Glowing blue architectural line-work, fine white lines, dimension marks.

**For:** "how it works", build and systems reels. **Verified:** 13 Aug 2026.

```
[identity guard]
Rebuild the room as a glowing blue architectural blueprint: deep blue ground
with fine white line-work drawing the furniture, walls and fittings in
technical projection, with dimension marks and small annotations. The lines
glow softly.
```

## 5. Whiteboard marker

The room becomes a whiteboard; hand-drawn marker diagrams, arrows and boxes
appear around him in the existing notebook-marker language.

**For:** teaching reels. Strongest tie to the house style already in
`notebook-marker-style-recipe`. **Verified:** not yet.

```
[identity guard]
Rebuild the room as a clean white whiteboard surface. Hand-drawn marker
diagrams appear around him and draw themselves on: boxes, connecting arrows,
underlines and small labelled circles, in black marker with occasional red and
blue accents, slightly uneven as if drawn by hand. Leave a clear white margin
around his head and shoulders.
```

## 6. Data room

Dark space, floating translucent glass panels carrying abstract glowing bars
and grids, volumetric light.

**For:** AI, model and benchmark reels on the .ai account. **Verified:** not yet.

**Caution:** keep the panels abstract. Readable product UI here would be a
mocked screen recording, which is banned — see `banned-fake-screen-edit-style`.

```
[identity guard]
Rebuild the room as a dark data room: large translucent glass panels float in
the space around him, carrying abstract glowing bar shapes, grids and pulsing
indicator dots — shapes only, no readable text or interface. Cool blue and
white light, volumetric haze, soft reflections on the floor. Keep every panel
clear of his head.
```

## 7. Cinematic relight

The same real room, dramatically relit: hard key, deep shadow, volumetric haze,
a single practical burning in frame.

**For:** serious or emotional opens where a stylised world would undercut the
tone. The subtlest treatment here. **Verified:** not yet.

**Caution:** this is the closest any treatment comes to relighting *him*, which
is the drift trigger. Test before trusting.

```
[identity guard]
Keep the room itself unchanged but relight it cinematically: a single hard key
from the left, deep falloff into shadow on the right, volumetric haze catching
the beam, and one warm practical lamp glowing in the background. Do not change
the light falling on his face.
```

## 8. Miniature diorama

The room becomes a tilt-shift miniature set — felt, cardboard and balsa
textures, shallow focus, oversaturated.

**For:** playful beats. **Verified:** not yet.

```
[identity guard]
Rebuild the room as a handmade miniature diorama: cardboard walls, felt floor,
balsa-wood furniture and modelling-clay details, lit like a photographed model
set with shallow tilt-shift focus and slightly oversaturated colour.
```

---

## Register flip (the meta-treatment)

Cycling two or three of the above in one continuous take. Verified working on
the paper → blueprint → real cycle: hard sweeps between registers, identity
held throughout.

Use it to *show range* rather than to open a reel. For a hook, one strong
transformation lands harder than a tour — the transformation itself is the
event, so start real and flip once, early.

```
[identity guard]
Start with the real room exactly as shot. At 0.8 seconds, sweep across frame
into [TREATMENT A]. At 4 seconds, sweep across into [TREATMENT B]. At 7 seconds,
sweep back to the real room. Each change sweeps across the room from one side
rather than cutting or dissolving.
```
