---
name: design-asset
description: "Build in-card animated demo assets as self-contained HTML with a CSS-delay timeline, then record them FRAME-EXACT by scrubbing document.getAnimations() per frame rather than recording in real time. Covers the font-freeze, viewport sizing to the card, the payoff-hold retiming rule, the animations:'disabled' trap that produces a video where nothing moves, and the hard clip an external asset needs to respect the card's safe band. Use whenever a beat needs a screen that ANIMATES and no real recording exists to show it."
---

# DESIGN ASSET — animated in-card demos, frame-exact

> **THE DIVISION OF LABOUR:** Remotion is the **assembly/sync layer** (timeline, word-synced
> captions, labels, SFX, brand system, deterministic re-renders). Claude Design generates the
> **in-card animated demo assets**. Frame-accurate word sync cannot live in a prompt-driven tool
> ("hit frame 1803" is not an operation it has) — but it makes far stronger motion demos than a
> scroll-panned screenshot, which is real evidence for any "motion/easing" claim in the VO.

**This is not a licence to fake a product demo.** A *specimen* (a motion example you authored) is
fine. A recreated app/browser UI presented as a recording is banned — see `screen-capture`.

## 1. Build it as ONE self-contained HTML file

Live at `public/broll/<reel>/x.html`, committed next to the mp4 so the asset is reproducible.

**All motion is CSS `animation-delay` on a single wall clock.** That makes the whole asset a
timeline you can retime by editing numbers — no re-authoring.

## 2. Size the viewport to the CARD, not to a screen

`1000×1100` recorded at `deviceScaleFactor: 2` drops into a 1000×1100 card at **1:1 with zero
resampling**. Sizing to 1440×900 and scaling down **softens hairlines**.

## 3. Record frame-exact — do NOT record in real time

Playwright's `recordVideo` has a **variable lead-in** (~0.2–0.3s of startup before animations
actually begin), so a payoff authored at `animation-delay: 5.3s` came back at **5.55s** and cost a
whole pixel-sampling + retime pass.

Instead: pause every animation, then set each animation's clock to exactly `frame/fps` per output
frame and screenshot.

```js
// freeze BEFORE first paint so the animation doesn't play against a fallback font
await page.addInitScript(() => {
  const s = document.createElement('style');
  s.id = 'freeze';
  s.textContent = '*, *::before, *::after { animation-play-state: paused !important; }';
  document.documentElement.appendChild(s);
});
await page.goto(url, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => document.getElementById('freeze')?.remove());

await page.evaluate(() => document.getAnimations().forEach(a => a.pause()));
for (let f = 0; f < FRAMES; f++) {
  await page.evaluate(ms => { for (const a of document.getAnimations()) a.currentTime = ms; },
                      (f / FPS) * 1000);
  await page.screenshot({ path: `f${f}.png` });     // PLAIN screenshot — see the trap below
}
// then encode the PNG sequence with ffmpeg
```

**Frame N is guaranteed to be the authored state at N/fps**, so cue delays written in the HTML land
frame-exact in the reel and VO-cued stamps need no measurement pass afterwards.

### Two traps

- **Without the font freeze**, the first ~600ms plays against a fallback face and the animation is
  already half over by the time the real font swaps in.
- **`page.screenshot({ animations: "disabled" })` does NOT freeze CSS animations — it FINISHES
  them**, jumping every element to its end state. Passing it while scrubbing `currentTime` yields a
  video where **nothing ever moves** (measured 0% moving frames). The manual pause is already the
  freeze; take a plain screenshot.

## 4. Retime so the payoff HOLDS, not just arrives

A ranked list that finished ~0.5s before the section cut meant **the viewer never got to read it**.

Compute backwards: the section is N frames; **the payoff must resolve at least ~2s before the end**
and land on the line that names it. One asset's rows resolve at 5.3s and hold 2.3s, landing exactly
on *"it came back with a list."*

If you ever do record in real time, land the payoff with the card's **`srcStart`** rather than
re-recording — and find its real frame by sampling pixel colour, not by trusting the authored delay:

```bash
ffmpeg -ss T -i asset.mp4 -frames:v 1 -vf "crop=W:H:X:Y,scale=1:1" -pix_fmt rgb24 -f rawvideo -
# 3 bytes; watch the channel that changes
```

## 5. Respect the card's safe band with a HARD CLIP

An external HTML asset fills the whole card, so the card's `CONTENT_TOP` does nothing for it — the
asset's own layout is the only thing holding its text down. **Top padding is not enough**, because
the asset SCROLLS its output upward and drags the text back up through the band.

```css
/* nothing authored can ever paint above asset-y 152 = absolute y248 */
.body   { position:absolute; left:0; right:0; top:152px; height:474px; overflow:hidden }
.scroll { position:absolute; top:0; … }
```

- **Delete the title-bar TEXT** (traffic-light dots stay — chrome is furniture and may cross).
- Move any path label **down into the clipped band** as the first content line.
- **Clipping shortens the scroll window, so add more real content** to keep the motion up.

## 6. It must MOVE — the gate cannot see fades

The scene-change detector scores an animating design card at **0–1%**, so judge these assets with
**mean absolute frame difference** instead, and against the real bar: **33–50% moving frames, no
static run longer than ~5 frames**.

**Posters that assemble and then sit are slideshows**, however many elements they have. What fixes
it: give every scene **ONE continuously creeping strip** running its whole length — a long document
scrolling past a window, a streaming log, a result feed. The creep is **linear across the whole
section**, so nothing changes velocity at a cut and the no-zoom-at-cuts rule stays intact.

Cheap wins that clear the threshold (text edges amplify sub-pixel motion through antialiasing — δ ≈
**0.1 px/frame** already clears it): a drifting dot field (~0.75px/frame), a travelling sheen, a slow
accent glow that pulses in alpha, a per-row float (~1.7px amplitude, ~45f period, phase-offset per
row) that reads as breathing rather than jitter.

## 7. Furniture lands early; only the punch waits for its word

A card whose content is all cue-gated opens near-empty for 0.5–2s and reads as plain — see
`split-screen`'s furniture-vs-punch rule. Furniture at section+2 to section+30; only the
meaning-carrying punch is pinned to its spoken word.

## Related

`screen-capture` (the honesty line, and the motion calibration table) · `split-screen` (the
card's safe band and the lean) · `asset-plan` (this is one of the four asset classes) ·
`mg-kit` (15 existing design assets — check before building a new one).
