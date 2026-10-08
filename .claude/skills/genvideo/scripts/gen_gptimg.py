#!/usr/bin/env python3
"""gpt-image-2 still generation + reference edit (high input fidelity).

  gen_gptimg.py PROMPT_FILE OUT.png [--ref IMG ...] [--size 1152x2048]
                [--quality high] [--fidelity high] [--model gpt-image-2]

With --ref it calls images.edit with input_fidelity=high, which is what holds a
real person's face across generations. Without refs it is a plain text-to-image.
Sizes must have both dimensions divisible by 16; 1152x2048 is exact 9:16.
"""
import argparse, base64, datetime, json, os, pathlib, sys, time

ENV = ".env.local"
for ln in open(ENV):
    ln = ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k, _, v = ln.partition("=")
        v = v.strip().strip('"').strip("'")
        if v and k.strip() not in os.environ:
            os.environ[k.strip()] = v

from openai import OpenAI

ap = argparse.ArgumentParser()
ap.add_argument("prompt_file")
ap.add_argument("out")
ap.add_argument("--ref", action="append", default=[])
ap.add_argument("--model", default="gpt-image-2")
ap.add_argument("--size", default="1152x2048")
ap.add_argument("--quality", default="high")
ap.add_argument("--fidelity", default="")  # gpt-image-2 has it built in; only gpt-image-1.x takes the param
a = ap.parse_args()

prompt = pathlib.Path(a.prompt_file).read_text().strip()
client = OpenAI(timeout=15 * 60)

print(f"gpt-image-2: {a.model} {a.size} q={a.quality} refs={len(a.ref)} -> {a.out}")

if a.ref:
    handles = [open(r, "rb") for r in a.ref]
    kw = dict(model=a.model, image=handles, prompt=prompt,
              size=a.size, quality=a.quality)
    if a.fidelity:
        kw["input_fidelity"] = a.fidelity
    def _call():
        for h in handles:
            h.seek(0)
        return client.images.edit(**kw)
    try:
        result = None
        for attempt in range(1, 4):
            try:
                result = _call()
                break
            except Exception as e:
                msg = str(e)
                if "input_fidelity" in msg and "input_fidelity" in kw:
                    print("model rejects input_fidelity; retrying without it")
                    kw.pop("input_fidelity")
                    continue
                if attempt < 3 and ("Connection" in msg or "disconnected" in msg
                                    or "timeout" in msg.lower()):
                    print(f"attempt {attempt} failed ({type(e).__name__}); retrying")
                    time.sleep(5)
                    continue
                raise
    finally:
        for h in handles:
            h.close()
else:
    result = client.images.generate(
        model=a.model, prompt=prompt, size=a.size, quality=a.quality,
    )

d = result.data[0]
b64 = getattr(d, "b64_json", None)
if not b64:
    print("no b64_json in response:", repr(d)[:1500])
    sys.exit("gpt-image-2: no image returned")
pathlib.Path(a.out).write_bytes(base64.b64decode(b64))
print("saved", a.out, pathlib.Path(a.out).stat().st_size, "bytes")

usage = getattr(result, "usage", None)
if usage:
    try:
        print("usage:", usage.model_dump_json())
    except Exception:
        print("usage:", usage)

pathlib.Path(a.out + ".gen.json").write_text(json.dumps({
    "engine": "gpt-image-2", "model": a.model,
    "mode": "edit" if a.ref else "text-to-image",
    "prompt_file": str(a.prompt_file), "refs": a.ref,
    "size": a.size, "quality": a.quality,
    "input_fidelity": (a.fidelity or None) if a.ref else None,
    "date": datetime.datetime.now().isoformat(timespec="seconds"),
}, indent=2))
