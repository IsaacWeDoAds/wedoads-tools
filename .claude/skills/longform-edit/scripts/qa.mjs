// lf01 QA without the CLI's 13 GB public copy: bundle once into work/lf01/bundle from the slim
// public-lf01 (hardlinks of broll/lf01 + sfx), then render stills / short test windows off it.
//   node work/lf01/work/qa.mjs bundle
//   node work/lf01/work/qa.mjs stills                      (frames from work/lf01/work/hero_stills.json, scale 0.5)
//   node work/lf01/work/qa.mjs render <a>-<b> <name> [scale=0.25]   (composition frames, inclusive)
import path from "node:path";
import fs from "node:fs";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
const mode = process.argv[2];
const BUNDLE = path.resolve("work/lf01/bundle");
if (mode === "bundle") {
  fs.rmSync(BUNDLE, { recursive: true, force: true });
  await bundle({ entryPoint: path.resolve("src/lf01-entry.tsx"), publicDir: path.resolve("public-lf01"), outDir: BUNDLE });
  console.log("bundled →", BUNDLE);
}
const composition = await selectComposition({ serveUrl: BUNDLE, id: "LF01Final" });
if (mode === "stills") {
  const picks = JSON.parse(fs.readFileSync("work/lf01/work/hero_stills.json", "utf8"));
  const outDir = "out/lf01/stills/heroes";
  fs.mkdirSync(outDir, { recursive: true });
  for (const [id, frame] of Object.entries(picks)) {
    const output = path.join(outDir, `${id}.png`);
    await renderStill({ composition, serveUrl: BUNDLE, frame, output, scale: 0.5 });
    console.log("still", id, frame);
  }
} else if (mode === "render") {
  const [a, b] = process.argv[3].split("-").map(Number);
  const name = process.argv[4];
  const scale = Number(process.argv[5] || 0.25);
  const outputLocation = `out/lf01/test-${name}-s${scale}.mp4`;   // renderMedia's option is outputLocation (remotion-node-api-traps)
  const t0 = Date.now();
  await renderMedia({ composition, serveUrl: BUNDLE, codec: "h264", outputLocation, frameRange: [a, b], scale, crf: 24, concurrency: 4, logLevel: "error" });
  console.log("rendered", outputLocation, `${a}-${b}`, `${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
