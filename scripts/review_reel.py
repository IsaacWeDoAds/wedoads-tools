#!/usr/bin/env python3
"""review_reel.py — the DETERMINISTIC half of the final review gate.

Measures everything about a rendered reel that a script can measure exactly, and
samples the frames the vision reviewer needs. It never guesses: anything that
needs taste (collisions, legibility, "does this look right") is left to the
agent in .claude/skills/reel-review.

  python3 scripts/review_reel.py OUT.mp4 --reel reel35 [--data src/Reel35/data.ts]

Writes work/<reel>/review/{report.md, frames/, sheet_*.jpg}. Exit 1 on any FAIL.
"""
import argparse, json, math, os, re, shutil, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SAFE_TOP, SAFE_BOT, SAFE_L, SAFE_R = 230, 1574, 35, 1045
FAILS, WARNS, NOTES = [], [], []

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

def probe(f):
    d = sh(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames '
           f'-show_entries format=duration -of json {json.dumps(f)}')
    j = json.loads(d)
    st, fm = j["streams"][0], j["format"]
    num, den = st["r_frame_rate"].split("/")
    return dict(w=st["width"], h=st["height"], fps=round(int(num)/int(den)),
                dur=float(fm["duration"]),
                frames=int(sh(f'ffprobe -v error -select_streams v:0 -count_frames '
                              f'-show_entries stream=nb_read_frames -of csv=p=0 {json.dumps(f)}').rstrip(",")))

def loudness(f):
    out = subprocess.run(f'ffmpeg -i {json.dumps(f)} -af loudnorm=I=-14:TP=-1.5:print_format=summary -f null -',
                         shell=True, capture_output=True, text=True).stderr
    m = re.search(r"Input Integrated:\s*(-?[\d.]+)", out)
    tp = re.search(r"Input True Peak:\s*(-?[\d.]+)", out)
    return (float(m.group(1)) if m else None, float(tp.group(1)) if tp else None)

def parse_data(path):
    """SECTIONS + CAPS straight out of the generated data.ts.

    Two schemas are in the wild and both must parse, because a reel silently
    failing to match here loses the caption-sync and card-motion checks — the
    two things this script exists for — while still reporting a clean pass:

      old   { name: "hook", from: 0, to: 120 }            { from, to, text }
      new   {"label": "hook", "from": 0, "durationInFrames": 120}
            {"t": "...", "f": 0, "fe": 120}
      json  {"name": "HOOK", "from": 0, "to": 132}         {"from","to","text"}
            (json.dumps output — quoted keys, no inner padding. reel48)
    """
    if not path or not pathlib.Path(path).exists():
        return None, None
    s = pathlib.Path(path).read_text()
    block = s.split("export const SECTIONS")[1].split("];")[0] if "export const SECTIONS" in s else s
    secs = [(n, int(a), int(b)) for n, a, b in
            re.findall(r'\{ name: "(\w+)",\s*from:\s*(\d+),\s*to:\s*(\d+) \}', block)]
    caps = [(int(a), int(b), json.loads(t)) for a, b, t in
            re.findall(r'\{ from:\s*(\d+), to:\s*(\d+), text: (".*?") \}', s)]
    if not secs:
        secs = [(n, int(a), int(a) + int(d)) for n, a, d in
                re.findall(r'"label":\s*"(\w+)".*?"from":\s*(\d+),\s*"durationInFrames":\s*(\d+)',
                           block, re.S)]
        if not secs:
            secs = [(n, int(a), int(a) + int(d)) for a, d, n in
                    re.findall(r'"from":\s*(\d+),\s*"durationInFrames":\s*(\d+).*?"label":\s*"(\w+)"',
                               block, re.S)]
        if not secs:
            # json.dumps schema: quoted keys, no padding inside the braces
            secs = [(n, int(a), int(b)) for n, a, b in
                    re.findall(r'"name":\s*"(\w+)",\s*"from":\s*(\d+),\s*"to":\s*(\d+)', block)]
    if not caps:
        cb = s.split("export const CAPTIONS")[1].split("];")[0] if "export const CAPTIONS" in s else s
        caps = [(int(a), int(b), json.loads(t)) for t, a, b in
                re.findall(r'"t":\s*("(?:[^"\\]|\\.)*"),\s*"f":\s*(\d+),\s*"fe":\s*(\d+)', cb)]
    if not caps:
        cb = s.split("export const CAPS")[1].split("];")[0] if "export const CAPS" in s else s
        caps = [(int(a), int(b), json.loads(t)) for a, b, t in
                re.findall(r'"from":\s*(\d+),\s*"to":\s*(\d+),\s*"text":\s*("(?:[^"\\]|\\.)*")', cb)]
    return secs, caps

def repeated_words(caps, fps, window_s=1.6):
    """Content words spoken twice inside a short window.

    A vision pass cannot catch this: it never hears the reel, and the two
    captions usually sit either side of a section boundary so they are never in
    one frame. Reel 48 shipped "But the catch is both." straight into "So both
    the skills..." — the same word half a second later across a register cut,
    which reads as a stutter. Nishant caught it, not the gate.
    """
    STOP = {"a","an","the","is","are","and","or","of","to","in","on","it","its",
            "that","this","so","but","for","you","we","at","as","all","have",
            "my","your","i","ll","don","t","be","was","not","do","then","there",
            "here","one","more","most","can","will","just","also","them","they",
            "he","she","what","which","how","if","with","from","by","about"}
    words = []
    for c in caps:
        for w in c[2].split():
            bare = w.strip('.,!?"\u201c\u201d\u2019').lower()
            if bare and bare not in STOP and len(bare) > 2:
                words.append((c[0], bare, c[2]))
    out = []
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            gap = (words[j][0] - words[i][0]) / fps
            if gap > window_s:
                break
            if words[i][1] == words[j][1]:
                out.append(f"- `{words[i][1]}` twice in {gap:.1f}s "
                           f"(f{words[i][0]} `{words[i][2]}` -> f{words[j][0]} `{words[j][2]}`)")
    return out

def frozen_runs(f, fps, min_run=8, crop=None):
    """Consecutive near-identical frames. With `crop` (w:h:x:y) this measures a
    REGION — used for the card, because on a composed render the talking-head
    layer changes every frame, so whole-frame motion is always ~100% and tells
    you nothing about whether the GRAPHICS are alive."""
    pre = f"crop={crop}," if crop else ""
    out = subprocess.run(
        f'ffmpeg -i {json.dumps(f)} -vf "{pre}tblend=all_mode=difference,signalstats,'
        f'metadata=print:key=lavfi.signalstats.YAVG" -an -f null -',
        shell=True, capture_output=True, text=True).stderr
    vals = [float(v) for v in re.findall(r"YAVG=([\d.]+)", out)]
    runs, cur = [], 0
    for i, v in enumerate(vals):
        if v < 0.30:                      # essentially no change frame-to-frame
            cur += 1
        else:
            if cur >= min_run: runs.append((round((i-cur)/fps, 2), round(cur/fps, 2)))
            cur = 0
    if cur >= min_run: runs.append((round((len(vals)-cur)/fps, 2), round(cur/fps, 2)))
    return runs, vals

def section_motion(vals, secs, fps):
    rows = []
    for n, a, b in secs:
        seg = vals[max(0, a-1):min(len(vals), b-1)]
        if not seg: continue
        moving = sum(1 for v in seg if v >= 0.30) / len(seg) * 100
        rows.append((n, a, b, round((b-a)/fps, 1), round(moving)))
    return rows

def sample_frames(f, fps, secs, outdir):
    """Mid-beat frame per section (steady state) + 0.35s after each boundary
    (post-enter, catches ghosting/empties).

    WIPE the directory first. Section names and frame numbers change between
    cuts, so old files survive under names the current run never writes — on
    reel 48 a pre-blur frame from the previous day sat next to the new ones and
    the vision reviewer nearly filed it as a leak in a render that was clean.
    A review directory must only ever contain the render being reviewed."""
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    shots = []
    for n, a, b in secs:
        for tag, fr in (("mid", (a+b)//2), ("in", min(b-2, a+int(0.35*fps)))):
            t = fr / fps
            p = outdir / f"{fr:05d}_{n}_{tag}.jpg"
            sh(f'ffmpeg -y -v error -ss {t:.3f} -i {json.dumps(f)} -frames:v 1 -q:v 3 {json.dumps(str(p))}')
            shots.append((fr, n, tag, p))
    return sorted(shots)

def ink_extents(img):
    """Bounding box of high-frequency (text/graphic-like) content per frame.
    Reported, not judged — imagery may legitimately cross the text safe area."""
    from PIL import Image, ImageFilter
    import numpy as np
    im = Image.open(img).convert("L")
    edges = np.array(im.filter(ImageFilter.FIND_EDGES))
    mask = edges > 60
    rows = np.where(mask.sum(axis=1) > 25)[0]
    cols = np.where(mask.sum(axis=0) > 25)[0]
    if not len(rows) or not len(cols): return None
    return int(rows.min()), int(rows.max()), int(cols.min()), int(cols.max())

def contact_sheets(shots, outdir):
    """Tiles follow the RENDER's aspect ratio.

    These were hard-coded to a 300x534 portrait tile. Run over a 1920x1080 cut
    that squashes every frame ~3x horizontally, and a vision reviewer fed only
    the sheets misjudges every proportion in the piece — which happened on the
    16:9 cut. Tile area is held roughly constant so sheets stay a similar size.
    """
    from PIL import Image, ImageDraw
    made = []
    per, cols = 10, 5
    if not shots:
        return made
    with Image.open(shots[0][3]) as probe_im:
        aspect = probe_im.width / probe_im.height
    area = 300 * 534
    tw = max(160, int(round((area * aspect) ** 0.5)))
    th = max(160, int(round(tw / aspect)))
    for i in range(0, len(shots), per):
        batch = shots[i:i+per]
        rows = (len(batch) + cols - 1) // cols
        sheet = Image.new("RGB", (tw * cols, th * rows + 40), (22, 22, 22))
        d = ImageDraw.Draw(sheet)
        for j, (fr, n, tag, p) in enumerate(batch):
            sheet.paste(Image.open(p).resize((tw, th)), (tw * (j % cols), th * (j // cols)))
            d.text((tw * (j % cols) + 6, th * (j // cols) + 4), f"f{fr} {n}/{tag}", fill=(255, 220, 0))
        out = outdir / f"sheet_{i//per}.jpg"
        sheet.save(out, quality=92); made.append(out)
    return made


def caption_sync(f, caps, fps, rev):
    """Re-transcribe the RENDER and check each caption lands on its own words."""
    if not caps: return ["- no CAPS in data.ts, skipped"]
    wav = rev / "render.wav"; jsn = rev / "render_wx.json"
    # The cache is keyed to the RENDER, not just to the reel. Without this it
    # only checked `jsn.exists()`, so every re-render was silently scored against
    # the FIRST render's transcription — reel 44 rebuilt its whole audio track to
    # kill a +12.9 frame drift and the gate kept reporting the old, identical
    # offsets. A stale pass is worse than no pass.
    stamp = rev / "render_wx.src"
    try:
        st = os.stat(f)
        key = f"{os.path.abspath(f)}|{int(st.st_mtime)}|{st.st_size}"
    except OSError:
        key = None
    if key is not None and (not stamp.exists() or stamp.read_text() != key):
        for stale in (wav, jsn):
            if stale.exists(): stale.unlink()
    if not jsn.exists():
        sh(f'ffmpeg -y -v error -i {json.dumps(f)} -vn -ac 1 -ar 16000 -c:a pcm_s16le {json.dumps(str(wav))}')
        venv = os.path.expanduser("~/wx-env/bin/python")
        align = ROOT / ".claude/skills/shortform-cutaway/scripts/whisperx_align.py"
        if not (os.path.exists(venv) and align.exists()):
            return ["- WhisperX not available, skipped"]
        sh(f'HF_HOME=~/wx-cache OMP_NUM_THREADS=4 {venv} {json.dumps(str(align))} '
           f'{json.dumps(str(wav))} {json.dumps(str(jsn))}')
    if not jsn.exists(): return ["- alignment failed, skipped"]
    if key is not None: stamp.write_text(key)
    W = json.loads(jsn.read_text())
    norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
    offs, missing = [], []
    for (a, b, text) in caps:
        first = norm(text.split()[0])
        if not first: continue
        cands = [w for w in W if norm(w["w"]) == first and abs(w["s"]*fps - a) < 90]
        if not cands:
            missing.append((a, text)); continue
        w = min(cands, key=lambda w: abs(w["s"]*fps - a))
        offs.append((round(w["s"]*fps - a), a, text))
    out = []
    if offs:
        vals = [o for o, _, _ in offs]
        mean = sum(vals)/len(vals)
        worst = sorted(offs, key=lambda x: -abs(x[0]))[:5]
        out.append(f"- matched **{len(offs)}/{len(caps)}** captions to render audio")
        out.append(f"- mean offset **{mean:+.1f}** frames ({mean/fps*1000:+.0f} ms)")
        out.append("- worst: " + ", ".join(f"`{t}` {o:+d}f" for o, _, t in worst))
        for o, a, t in worst:
            if abs(o) > 12: FAILS.append(f'caption "{t}" is {o:+d} frames out of sync')
        if abs(mean) > 6: WARNS.append(f"captions drift {mean:+.1f} frames on average")
    if missing:
        out.append(f"- ⚠️ **{len(missing)}** captions had no matching spoken word nearby:")
        out.extend(f"  - f{a} `{t}`" for a, t in missing[:8])
        if len(missing) > len(caps) * 0.15:
            FAILS.append(f"{len(missing)} captions do not match the render audio")
        else:
            WARNS.append(f"{len(missing)} captions unmatched (check wording)")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render"); ap.add_argument("--reel", required=True)
    ap.add_argument("--data", default=None)
    # The screen card is not the same rectangle in every reel — reel 50 runs it
    # full-bleed to the top/left/right edges. Measuring the old inset rectangle
    # on a full-bleed layout silently scores the wrong pixels.
    ap.add_argument("--card", default="1000:626:40:100",
                    help="ffmpeg crop w:h:x:y for the screen-card region")
    ap.add_argument("--size", default="1080x1920",
                    help="expected WxH — 1080x1350 for the 4:5 LinkedIn cut")
    a = ap.parse_args()
    exp_w, exp_h = (int(v) for v in a.size.lower().split("x"))
    f = a.render
    rev = ROOT / "work" / a.reel / "review"
    rev.mkdir(parents=True, exist_ok=True)
    L = []

    sp = probe(f)
    L.append(f"## Specs\n\n- {sp['w']}x{sp['h']} @{sp['fps']}fps · {sp['frames']} frames · {sp['dur']:.2f}s")
    if (sp["w"], sp["h"]) != (exp_w, exp_h):
        FAILS.append(f"resolution {sp['w']}x{sp['h']} != {exp_w}x{exp_h}")
    if sp["fps"] not in (30, 60): WARNS.append(f"unusual fps {sp['fps']}")

    li, tp = loudness(f)
    L.append(f"- loudness **{li} LUFS**, true peak {tp} dBTP")
    if li is None or abs(li + 14) > 1.0: FAILS.append(f"loudness {li} LUFS — must be -14 (+/-1)")
    if tp is not None and tp > -1.0: WARNS.append(f"true peak {tp} dBTP is hot")

    secs, caps = parse_data(a.data)
    if secs:
        expected = max(b for _, _, b in secs)
        if abs(expected - sp["frames"]) > 2:
            FAILS.append(f"frame count {sp['frames']} != data.ts total {expected} (tail clipped?)")

    L.append("\n## Frozen frames\n")
    runs, vals = frozen_runs(f, sp["fps"])
    real = [(t, d) for t, d in runs if d >= 0.20]
    if real:
        for t, d in real[:12]:
            (FAILS if d >= 0.5 else WARNS).append(f"frozen {d}s at {t}s")
        L.append("\n".join(f"- {d}s freeze at **{t}s**" for t, d in real[:12]))
    else:
        L.append("- none ≥0.2s ✓")

    if secs:
        # measure the CARD region only — that is where screen content and MG live
        _, card_vals = frozen_runs(f, sp["fps"], crop=a.card)
        cw, ch, cx, cy = a.card.split(":")
        L.append("\n## Card-region motion (the graphics half; ≥30% is the floor)\n")
        L.append("Whole-frame motion is meaningless on a composed render (the face\n"
                 f"layer moves every frame), so this crops to the {cw}x{ch} screen\n"
                 f"card at ({cx},{cy}).\n")
        L.append("| section | frames | secs | card moving |\n|---|---|---:|---:|")
        for n, x, y, dur, mv in section_motion(card_vals, secs, sp["fps"]):
            flag = "" if mv >= 30 else ("  ⚠️ thin" if mv >= 15 else "  ❌ static")
            L.append(f"| {n} | {x}–{y} | {dur} | **{mv}%**{flag} |")
            if mv < 15: WARNS.append(f"card is only {mv}% moving in {n} — near-static beat")

    L.append("\n## Caption sync (re-transcribed from the render)\n")
    L.extend(caption_sync(f, caps, sp["fps"], rev))

    if caps:
        L.append("\n## Repeated words (a stutter the vision pass cannot hear)\n")
    # ── false-start / redo pairs the ASR cannot hear ──────────────────────
    # Whisper COLLAPSES an immediate repeat, so the caption-sync check and a
    # re-transcribe both pass while the viewer plainly hears "Week 1 and...
    # Week 1 and 2". This compares each speech burst against the head of the
    # next one spectrally. Measured: real repeats 0.83-0.91, unrelated ~0.66.
    rs = subprocess.run([sys.executable, str(ROOT / "scripts/repeat_scan.py"), f],
                        capture_output=True, text=True)
    hits = [l.strip() for l in rs.stdout.splitlines() if l.strip().startswith("REPEAT")]
    L.append("\n## Repeated TAKES (a false start left next to its redo)\n")
    if hits:
        for h in hits:
            FAILS.append("a false start is still in the cut — " + h.replace("REPEAT", "").strip())
            L.append(f"- ❌ {h}")
    else:
        L.append("- none — no burst repeats the head of the next one ✓")

        reps = repeated_words(caps, sp["fps"]) if caps else []
        if reps:
            L.extend(reps)
            WARNS.append(f"{len(reps)} repeated word(s) within 1.6s — reads as a stutter")
        else:
            L.append("- none within 1.6s")

    shots = sample_frames(f, sp["fps"], secs or [("ALL", 0, sp["frames"])], rev / "frames")
    L.append(f"\n## Safe-area extents (measured, judged by the reviewer)\n")
    L.append(f"Text must sit inside y{SAFE_TOP}–{SAFE_BOT} / x{SAFE_L}–{SAFE_R}; imagery may cross.\nThese are whole-frame ink extents — the base cut is full-bleed, so edge\nvalues are expected. The vision pass judges whether TEXT overflows.\n")
    L.append("| frame | section | ink top | ink bottom | left | right |\n|---|---|---:|---:|---:|---:|")
    for fr, n, tag, p in shots:
        e = ink_extents(p)
        if not e: continue
        t_, b_, l_, r_ = e
        L.append(f"| f{fr} | {n}/{tag} | {t_} | {b_} | {l_} | {r_} |")

    sheets = contact_sheets(shots, rev)
    L.append(f"\n## Frames for the vision pass\n")
    L.extend(f"- `{s.relative_to(ROOT)}`" for s in sheets)

    head = [f"# Review — {a.reel}\n", f"`{f}`\n"]
    if FAILS: head.append("## ❌ FAIL\n" + "\n".join(f"- {x}" for x in FAILS) + "\n")
    if WARNS: head.append("## ⚠️ CHECK\n" + "\n".join(f"- {x}" for x in WARNS) + "\n")
    if not FAILS and not WARNS: head.append("## ✅ No deterministic failures\n")
    (rev / "report.md").write_text("\n".join(head + L) + "\n")
    print("\n".join(head))
    print(f"full report: work/{a.reel}/review/report.md   ({len(shots)} frames, {len(sheets)} sheets)")
    sys.exit(1 if FAILS else 0)

if __name__ == "__main__":
    main()
