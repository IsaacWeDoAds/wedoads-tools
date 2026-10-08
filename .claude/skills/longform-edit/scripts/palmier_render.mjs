// Render the lf01 layer clips for Palmier from work/lf01/work/palmier_plan.json.
//   node work/lf01/work/palmier_render.mjs bundle
//   node work/lf01/work/palmier_render.mjs render [only]   only = comma list of cards:N | fulls:N | type:N | montage | prerollsfx | cards | fulls | type
// Outputs → out/lf01/palmier/  (cards/fulls/montage H.264; type = PNG→ProRes 4444 → HEVC-alpha .mov; prerollsfx .wav)
import path from "node:path";
import fs from "node:fs";
import { execSync } from "node:child_process";
import { bundle } from "@remotion/bundler";
import { openBrowser, renderMedia, selectComposition } from "@remotion/renderer";
const BUNDLE = path.resolve("work/lf01/bundle-palmier");
const OUT = path.resolve("out/lf01/palmier");
const SRC_TAKE = "<media-drive>/C0937.MP4";
const mode = process.argv[2];
if (mode === "bundle") {
  fs.rmSync(BUNDLE, { recursive: true, force: true });
  await bundle({ entryPoint: path.resolve("src/lf01-palmier-entry.tsx"), publicDir: path.resolve("public-lf01"), outDir: BUNDLE });
  // the source take is served through a symlink (never copied): Remotion's static server supports range requests
  const link = path.join(BUNDLE, "public/broll/lf01/take_src.MP4");
  fs.rmSync(link, { force: true }); // (symlinks are refused by the static server; card faces are pre-extracted into take_cards/)
  console.log("bundled →", BUNDLE, "(+ source symlink)");
  process.exit(0);
}
const plan = JSON.parse(fs.readFileSync("work/lf01/work/palmier_plan.json", "utf8"));
fs.mkdirSync(OUT, { recursive: true });
const only = (process.argv[3] || "").split(",").filter(Boolean);
if (mode === "stills") {
  const { renderStill } = await import("@remotion/renderer");
  const picks = JSON.parse(fs.readFileSync("work/lf01/work/hero_stills.json", "utf8"));
  const kinds = JSON.parse(fs.readFileSync("src/LF01/data.ts", "utf8").match(/export const HEROES: Hero\[\] = (\[.*?\]);\n/s)[1]).reduce((m, h) => ((m[h.id] = h.kind), m), {});
  const outDir = path.join(OUT, "stills"); fs.mkdirSync(outDir, { recursive: true });
  for (const [id, compFrame] of Object.entries(picks)) {
    const frame = typeof compFrame === "number" ? compFrame - plan.PRE : compFrame.frame;   // picks: composition frames (cut + PRE) or {frame, layer}
    const layer = typeof compFrame === "number" ? (kinds[id] === "card" ? "cards" : kinds[id] === "full" ? "fulls" : "type") : compFrame.layer;
    const props = layer === "type" ? { layer, bg: "#5b5b60" } : { layer };
    const composition = await selectComposition({ serveUrl: BUNDLE, id: "LF01Layer", inputProps: props });
    await renderStill({ composition, serveUrl: BUNDLE, frame, inputProps: props, output: path.join(outDir, `${id}.png`), scale: 0.5, imageFormat: "png" });
    console.log("still", id, layer, frame);
  }
  process.exit(0);
}
const want = (kind, i) => only.length === 0 || only.includes(kind) || only.includes(`${kind}:${i}`);
const browser = await openBrowser("chrome", { chromiumOptions: { gl: "angle" } });
const comp = async (layer) => selectComposition({ serveUrl: BUNDLE, id: "LF01Layer", inputProps: { layer } });
const t0 = Date.now();
const log = (...a) => console.log(`[${((Date.now() - t0) / 1000).toFixed(0)}s]`, ...a);
const h264 = async (layer, from, to, file, audio = false) => {
  if (fs.existsSync(file)) { log("skip (exists)", path.basename(file)); return; }
  const composition = await comp(layer);
  await renderMedia({ composition, serveUrl: BUNDLE, codec: "h264", crf: 17, outputLocation: file, frameRange: [from, to - 1], inputProps: { layer }, puppeteerInstance: browser, concurrency: 4, logLevel: "error", muted: !audio, audioCodec: audio ? "aac" : undefined });
  log("rendered", path.basename(file), `${from}-${to}`);
};
for (const [i, w] of plan.cards.entries()) if (want("cards", i)) await h264("cards", w.from, w.to, path.join(OUT, `card_${String(w.from).padStart(6, "0")}.mp4`));
for (const [i, w] of plan.fulls.entries()) if (want("fulls", i)) await h264("fulls", w.from, w.to, path.join(OUT, `full_${String(w.from).padStart(6, "0")}.mp4`));
if (want("montage", 0)) await h264("montage", 0, plan.PRE, path.join(OUT, "montage.mp4"), true);
if (want("prerollsfx", 0)) {
  const file = path.join(OUT, "preroll_sfx.wav");
  if (!fs.existsSync(file)) {
    const composition = await comp("prerollsfx");
    await renderMedia({ composition, serveUrl: BUNDLE, codec: "wav", outputLocation: file, frameRange: [0, 299], inputProps: { layer: "prerollsfx" }, puppeteerInstance: browser, logLevel: "error" });
    log("rendered preroll_sfx.wav");
  }
}
for (const [i, w] of plan.types.entries()) {
  if (!want("type", i)) continue;
  const base = path.join(OUT, `type_${String(w.from).padStart(6, "0")}`);
  const mov = base + ".mov";
  if (fs.existsSync(mov)) { log("skip (exists)", path.basename(mov)); continue; }
  const prores = base + ".prores.mov";
  const composition = await comp("type");
  await renderMedia({ composition, serveUrl: BUNDLE, codec: "prores", proResProfile: "4444", pixelFormat: "yuva444p10le", imageFormat: "png", outputLocation: prores, frameRange: [w.from, w.to - 1], inputProps: { layer: "type" }, puppeteerInstance: browser, concurrency: 4, logLevel: "error", muted: true });
  // alpha container for Palmier: ProRes 4444 (its compositor cannot decode Animation/qtrle); ~2 MB/s at qscale 14
  execSync(`ffmpeg -nostdin -v error -y -i "${prores}" -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -qscale:v 14 -an "${mov}"`);
  if (!process.env.KEEP_PRORES) fs.rmSync(prores);
  log("rendered", path.basename(mov), `${w.from}-${w.to}`, `${(fs.statSync(mov).size / 1e6).toFixed(0)} MB`);
}
await browser.close({ silent: true });
log("done");
