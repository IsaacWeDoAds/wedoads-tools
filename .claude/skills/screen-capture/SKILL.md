---
name: screen-capture
description: "Produce REAL screen recordings for video edits with Playwright — the shared capture rig (continuous creep, 96px on-page pointer, CFR output), the ≥30% motion gate and how to calibrate it, the four ways a capture silently comes back frozen, hostile-site fallbacks, PII scanning, and dual-system audio lock. Use whenever an edit needs a browser/app/tool recording, whenever a capture reads as a slideshow, or when ingesting a screen recording someone supplied. NEVER used to fabricate a demo."
---

# SCREEN CAPTURE — real recordings, and proving they move

> **THE JOB:** every screen shown in an edit is a genuine recording of the real thing, and it
> **moves for ≥30% of its frames**. A capture that is correct but frozen is the single largest
> reason an edit reads flat — measured, not guessed.

## ⛔ The honesty line (non-negotiable)

| Thing | Allowed? |
|---|---|
| Mocked **terminal** (styled window, typed text) | ✅ A terminal is rendered text; a good mock is indistinguishable |
| Mocked **screen recording** — recreated app/browser UI, devtools panels, tool windows | ⛔ BANNED |
| Screenshot crop-scroll presented as a recording | ⛔ BANNED |
| Invented on-screen output/numbers for a run that never happened | ⛔ BANNED |
| A **synthetic pointer** drawn over a real page | ✅ A presentation pointer is not fabricated output |
| A **screenshot panned in the compositor** | ✅ Still a real capture of the real page |

The audience reads a screen recording as evidence. A mock reads as fake within seconds and the
account's whole differentiator is honesty. **If a needed recording does not exist, STOP and ask
for it** — never substitute a fabrication. Rejected outright, 30 Jul 2026 batch.

## The rig

`capture_lib.mjs` at the repo root is the shared engine. Import it; never write a new tour from
scratch.

```js
import { record, creep, movePointer, checkMotion } from "./capture_lib.mjs";

const tour = async (page) => {
  const hMax = await page.evaluate(() => document.body.scrollHeight - innerHeight);
  movePointer(page, [980, 300], [430, 520], 2600);   // NOT awaited — runs WITH the scroll
  await creep(page, Math.min(hMax, 620), 2600);
};
await record("reel41", "hero", "https://example.com", tour);
```

What it gives you: 1440×900 capture, 8-bit H.264 **CFR 60fps**, `creep()` (one continuous scroll
that never fully stops), `movePointer()`, `addCursor()` (96px on-page pointer), `checkMotion()`.

Three rules the rig encodes:
1. **Never `waitForTimeout` more than ~600ms inside a tour.** Motion is the product.
2. The pointer is a presentation pointer over a real page. Playwright's `recordVideo` does not
   capture the system cursor at all, and a default-size cursor is invisible at phone scale —
   **96px**, not 64px (64 was still too small once 1440px downscales into a 1000px card).
3. **Banners are HIDDEN, never clicked.** Clicking "Accept all" consents on someone's behalf.
   Where a modal blocks scrolling entirely, decline (`/decline all|reject all|necessary only/`),
   never accept.

## The motion gate

**≥30% of frames must show change. Below 25% it is a slideshow — rewrite the tour, don't ship it.**

`checkMotion()`'s scene detector (`gt(scene,0.008)`) was built for scrolling browser tours and
**barely fires on element pops and fades inside a card** — it scored a working, animating design
card at 0–1%. For anything that is not a page scroll, use **mean absolute frame difference**:
downscale to 160×100 grey, count frames where `mean|frame[n+1]-frame[n]| > 0.30`.

Calibrate before trusting a number:

| source | moving frames | longest static run |
|---|---|---|
| Apple's own footage (the bar) | **33–50%** | **3–5 frames** |
| our shipped design cards | 7–13% | 95–143 frames |
| after the rewrite | 37–100% | 0–45 frames |

**The static-RUN length matters more than the percentage.** A card can score 35% and still hold a
2.4s frozen stretch — which is what the viewer actually sees. Apple never holds more than 5 frames.

**Beating what we shipped is not the bar.** Cards passed review at 7–13% and the standing
complaint is still that our edits read flatter than the best remakes. Measure against Apple.

## The four ways a capture comes back frozen

Diagnose with ONE still (`ffmpeg -ss 6 -frames:v 1`) **before** touching the tour. A blank / modal
/ unscrolled frame tells you which case you have.

1. **The page scrolls a CONTAINER, not the window** → `window.scrollTo` is silently a no-op, every
   frame identical, ~1% motion. Find the tallest element with `overflow-y: auto|scroll` and
   `scrollHeight > clientHeight`, animate *its* `scrollTop` (`creepAny()`). Fixed metaintro 1%→34%,
   research.meta.ai 1%→27%. The `hMaxAny` heuristic picks the wrong box on pages with a sidebar —
   keep a `windowTour` variant and choose per shot.
2. **A cookie modal blocks scrolling entirely** (n8n.io). Decline first. If it still reads 1% the
   modal is in an iframe — drop the capture and stamp the tool's logo instead.
3. **Virtualised lists never register motion** (LeetCode problemset: 1–2% across three tours). The
   DOM recycles rows so pixels barely change. Don't keep rewriting the tour; stamp the logo.
4. **The tour itself is `hold → glide → hold`.** This was the root cause of 81–91% frozen captures.
   Rewrite as ONE continuous slow scroll; holds ≤0.6s, only on the thing being named.

## The traps that cost a render

- **A long capture inside a short section shows the PRE-scroll page.** `OffthreadVideo` starts at
  its own frame 0, so a 25s capture in a 5s section renders the page header, not the shot. **Give
  every capture a `start` (source seconds) offset**, picked from where the content actually lands.
- **Verify by PAINTED PIXELS, never `innerText`.** An `Access Denied` page passed a
  `/Applicants/i.test(body.innerText)` check because the *blocked URL itself* contained the word.
  Assert the target element's bounding box + a screenshot pixel sample.
- **Measure scroll targets off the live DOM.** A throwaway probe reporting
  `getBoundingClientRect().top + scrollY` turns "glide(2400) and hope" into exact offsets — and
  hands you the paragraph text for fact-checking. Scroll to the element carrying the **claim**, by
  name, not by pixels.
- **`recordVideo` CANNOT upscale.** Apparent text size is set by the page's *layout width*.
  Playwright writes the video at exactly `recordVideo.size` and does not scale a 700px viewport up
  to it — you get the render anchored top-left in a mostly-black frame. `deviceScaleFactor` does
  not help either. For legible page text: `page.screenshot({ fullPage: true, clip })` at a narrow
  viewport / DPR 2–3, then **pan the image in the compositor**. `fullPage: true` is REQUIRED with a
  clip reaching past the viewport or Playwright silently truncates.
- **Google properties geo-default their language** — `gemini.google.com/about` came back entirely
  in Arabic. Set `locale: "en-US"`, an `Accept-Language` header, a US `timezoneId`, `?hl=en`.
- **Logo auto-detection grabs the wrong mark** ("News from Google" instead of the Gemini wordmark,
  and it shipped). Always eyeball the captured logo. When detection fails, crop the mark out of a
  frame of the page capture — it is still real.
- **openai.com 403s a plain fetch but loads in Playwright** with a real desktop Chrome UA. Use
  `waitUntil: "domcontentloaded"`; `networkidle` times out on autoplaying hero video.
- **Trim the pre-paint head.** The recorder rolls before first paint — an unguarded wait banks ~2s
  of white. Time the content wait, pass it to ffmpeg as `-ss`.
- **Zoom needs SOURCE-PIXEL framing, not a centre crop.** Marketing/GitHub pages are left-aligned,
  so a centre crop clips the first character of every line ("ross-platform", "hat It Does"). Pass
  `srcX/srcY`.

## Hostile sites

Naukri (Akamai 403 headless *and* headed), LinkedIn (**HTTP 999** to Playwright, hard signup wall),
Kaggle (Cloudflare "checking your browser"). Playwright Firefox passes Naukri's bot check but the
main content never paints — skeleton shimmer forever.

**Do not try to defeat a bot check.** Check early whether the number is even visible logged-out
(Naukri caps at "100+", LinkedIn at "Over 200 applicants"). If not, pivot the beat to an honest
typography frame and flag "record your logged-in view" as the upgrade path. Public JSON APIs
(`boards-api.greenhouse.io`, `api.ashbyhq.com/posting-api`) are the reliable real data source for
role lists.

## Before you record anything: one check frame

**ALWAYS grab ONE frame and LOOK at it before any desktop/screen capture.** Approval to record an
app is not approval to record whatever happens to be on the desktop. A single check frame once
showed Chrome with a private Drive video of a third person, a private URL, and a tab bar of
personal accounts — the app to be recorded was not even fronted. One `ffmpeg -frames:v 1` costs
nothing.

## Ingesting a supplied recording

**Scan every frame for PII before cutting.** Signed-in product UI drifts into account pages as it
scrolls — a supplied LinkedIn capture rendered a real email in plain text past ~3.3s. Look for:
emails, phone numbers, résumé/CV contents, billing details, API keys, other people's names, DM
contents, tab bars and bookmarks. **Choose the asset window to EXCLUDE the exposed region rather
than blurring it** — a crop is unambiguous, a blur invites "is that readable if I pause?". Verify
the LAST frame explicitly; that is where a scroll lands. Say what was trimmed and why.

Other ingest notes:
- macOS recording filenames contain **U+202F** (narrow no-break space) before AM/PM. A typed path
  fails with "No such file or directory" *while `ls` shows the file*. This looks exactly like a
  TCC/sandbox block and is not one — use a glob.
- Specs are typically 3016×1718, **variable frame rate** (ffprobe reports 44–53 fps). Always
  normalise with `fps=60`.
- **Strip the audio** (`-an`) unless it is dual-system (below). Standing preference.
- **Crop to the app's CONTENT canvas, not the window.** Measure the rect off a
  `drawgrid=w=200:h=200` ruler frame. This alone removes the logo, top bar, rails and toolbars —
  which is what makes a delayed-reveal hook possible. Verify by sampling the **cropped** clip:
  hover affordances and toast notifications live inside the canvas.
- **A 120fps capture is a free slow-motion asset.** `setpts=2.0*PTS` + `-r 60` halves the speed
  with no duplicated frames. The lever runs both ways (`setpts=0.34*PTS` compressed 26s into 9s).
- **Match the card's aspect to the CROP**, not the reverse. Cover-cropping a 1.80 source into a
  1.6 card eats a column.
- **Scan for on-screen state that contradicts the VO** — a settings dropdown reading "don't add
  images" while the VO says "I swapped two images out" falsifies the claim. Window it out, re-word,
  or drop the claim.

## Dual-system lock (free frame-exact sync)

When a supplied screen recording carries its **own narration**, cross-correlate its audio envelope
against the camera take before planning any capture windows — it decides whether the capture is
synced material or loose b-roll.

```python
def env(x, w=400): return np.abs(x[:len(x)//w*w]).reshape(-1, w).mean(1)
c = np.correlate(env(b) - env(b).mean(), env(a) - env(a).mean(), 'full')
lag = (c.argmax() - (len(env(a)) - 1)) * w / sr
```

- **constant lag + corr > 0.6 → dual-system sound.** Lock to it: `screenrec_time = take_time + lag`.
  Every on-screen action then has an exact spoken-word anchor, with nothing hand-nudged.
- **drifting lag → different performances.** Treat the capture as free b-roll.

File timestamps lie (a camera clock in another timezone put the two files 2 hours apart when the
real lag was +8.700s at corr 0.79). Where one beat's event falls outside its window, override the
offset **per segment, documented** — never abandon the lock everywhere.

## Cutting a capture into beats

1. **Re-enter ONE continuous take at several in-points** so each action lands on the word naming
   it, instead of letting it play linearly and drift. Check the action is still on screen across
   the whole caption window — a menu that closes mid-word leaves the caption over a blank page.
2. **Fast-cut montages: pre-cut in ffmpeg, play as one asset.** Six sites × 34 frames concatenated
   into one file beats six compositor sequences and gives exact spacing.
3. **Story consistency beats completeness.** A tighter take on the site the edit already uses beats
   a fuller take on a different site — jumping sites mid-method costs more than the detail buys.

## What we cannot capture

Playwright covers browser **content** only — not devtools, extensions, or browser chrome. Desktop
capture via `ffmpeg -f avfoundation` hangs on the permission prompt when driven headlessly, though
`-capture_cursor 1 -framerate 30 -i "3:none"` (device [3] "Capture screen 0") does work interactively
and gives a REAL terminal running a REAL command with a real cursor.

**For anything else: ask the creator — he records it himself and hands it over.** That beats every
workaround.

## Related

`asset-plan` classifies what needs capturing. `take-geometry` frames it. `reel-review`
re-measures motion per section on the finished render. Compositor side:
`src/components/CaptureCard.tsx` (`srcX/srcY` framing).
