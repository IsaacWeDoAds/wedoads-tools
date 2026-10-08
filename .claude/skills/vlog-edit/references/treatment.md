# Vlog treatment — text and motion graphics when he asks for them

He asked on Vlog 3: *"add text, add different types of motion graphics, sound design."* That overrides
the zero-type default **for that video only**. The language below is what shipped; reuse it unless he
names a new reference. Generator: `work/vlog3/hf_overlays.py` (data in, one sub-composition per graphic).

## The design language (two families: Inter + one hand font)

| Element | Use it for | Spec |
|---|---|---|
| **Time card** | each new place/time | PLACE (Inter 300) left at x≈0.075, TIME (Inter 700) right at x≈0.90–0.93, ONE baseline, all caps, no chip, tracking-in on per-glyph `x` (lint bans tweening letterSpacing). White on mid/dark frames, **ink on white walls**. ~3 s. Vertical position goes wherever the frame is empty |
| **Taped paper note** | lists and plans: the day's plan, the setup, a snack, a rule | cream paper, tape, Shadows Into Light lines written on at the word, red strike / ticks / crosses drawn as SVG strokes (never ✓/✗ glyphs: the hand font lacks them and a system fallback is a third family) |
| **Returning note** | the story's turn | the morning plan note comes back with the errand struck through and the reason in red |
| **Handwriting on the frame** | one-line asides ("toot toot", "50 rupees here") | ink on light walls, cream with shadow on wood/steel/dark; pen underline, arrow or circle at most |
| **Taped label** | an aside where no wall is plain (vents, skylight, wood slats, busy shelves) | a small paper note without a heading |
| **Freeze frame** | the outfit / a "this is me" beat | still + flash + background-removed cutout + labels with arrows (`hyperframes remove-background`) |
| **Count-up** | real numbers he says (40 videos) | per-frame `tl.set` textContent, no callbacks |
| **Light leak** | the first shot of each act | registry `organic-light-leak-overlay`, starting *after* the cut, never across it. On bright daylight interiors drop the red layer and cap it at 0.35 (it turns walls pink) |
| **End card** | the close | black, centred: hand-written aside, then **THANK YOU FOR WATCHING!** in Inter caps, then the CTA ("let me know if you want more vlogs") with an underline. Hold the last line ≥2 s after it finishes writing |

Brand mentions get the brand's mark (brand logo marks); the Claude sunburst ships in `hf_overlays.py`.
If he asks for "our typography", that means his installed library at `~/Library/Fonts` (Poppins, Bebas
Neue, Anton, Gotham Bold, UniSans Heavy, Abril Fatface, Instrument Serif, Prata, Playfair Display,
Montserrat Black). Instrument Serif is a light serif and needs a backdrop over busy frames.

## Real numbers, real clock

- Every number on screen is something he said or a fact you checked against the live source.
- **Clock times come from the camera metadata of the shot under the card**, at the minute shown:
  DJI real time = `creation_time(UTC) + 3h09m` (the DJI clock runs fast); the iPhone clock is truthful.
  Compute it for the media time under the card, not the clip start.
- Cards must run forwards. Skip a card on an out-of-order chunk rather than show time going backwards.

## Placement: the plainest surface, measured

His note: *"move it a little down, it will come properly on the white wall and increase the visibility."*

- **Never let text cross an edge, seam or object**: a cabinet line, a microwave edge, a sticker.
- Sample the shot across the **whole hold** and pick the cleanest spot near the original:
  `work/vlog3/place_text.py` scores texture (90th percentile, so one line crossing the text counts),
  legibility, motion (lightly: a passing shadow is fine), and the MediaPipe person silhouette
  (dilated), inside action-safe. It writes `text_offsets.json`; the generator shifts the block and
  flips ink/cream. It only moves a block when the score improves by more than 0.15 and the shift is
  at least 24 px.
- "Plain" means flat, not white. A white cabinet face or backsplash is ideal. Dark ink only needs the
  wall at ≥150 luma under the whole block, so a light-grey wall in shade still works.
- His explicit instruction beats the score: pin it (`PIN` in `place_text.py`).
- No clean wall: look at the best-scoring spot on a contact sheet. If it still crosses an edge or sits
  on vents, slats, a skylight or shelves, use a taped label instead of bare handwriting. This is a
  judgement call; there is no score cutoff.

## Never on his face, across the whole hold

- Check **entrance, mid-hold and exit** frames, not one style frame. On walking selfies he drifts.
  A note anchored `right: 50px` grazed his sunglasses 8 s into its hold.
- On selfies keep notes ≥60 px from the head at the closest frame; shrink, push to the edge, or end
  the note early (crop to when he is clear).
- Run an independent vision review (Fable) over contact sheets of every graphic at mid-beat plus
  entrances/exits. It caught both face grazes on Vlog 3.

## Timing rules

- Write each line **on the word** (WhisperX timeline words). Whisper translates Hindi, so use the
  transcript for timing and meaning, never as verbatim on-screen text.
- **Nothing animates across a cut.** A graphic lives inside one shot (or across an invisible seam).
- A note that must persist across a cut is two graphics: the first holds **2 frames past the cut**,
  because a HyperFrames sub-composition draws from its second frame.
- Hide hand-drawn paths until their draw starts. Round caps on a fully dash-offset path still paint a
  dot per subpath. A mark that is "already on the paper" is drawn with no animation.
- Hand-drawn jitter (boil) is baked as discrete `tl.set` steps, so every seek lands on the same pose.

## Sound for the treatment

What shipped on Vlog 3 (84 cues over 14:31, about 6 a minute; cue sheet `cues()` in `hf_mount.py`):

| Event | Sound |
|---|---|
| real actions: alarm, sheets, phone tap, curtain, elevator ding | the action's own sound |
| time card in | a soft swoosh (the quietest cue in the mix) |
| paper note slides in | a paper slide |
| handwriting on a note or the outfit freeze | pencil under each line, length matched to the line |
| strike, tick, cross, circle, arrow | a short pen mark, landing just after the draw starts |
| freeze | shutter, then tape |
| light leak | a soft air |
| the story's turn | a clock tick, then a low thud on the strike |

**Text added later in the edit gets no sound** ("no need to add more sound effects with text"). If a
pass runs denser than this, cut pencil and pen first. Levels: SKILL.md.
