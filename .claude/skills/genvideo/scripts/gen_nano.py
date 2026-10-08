#!/usr/bin/env python3
"""Nano Banana Pro (gemini-3-pro-image) still generation + edit.

  gen_nano.py PROMPT_FILE OUT.png [--ref IMG ...] [--model M] [--size 2K] [--ar 9:16]

With no --ref it is text-to-image. With one or more --ref it is an EDIT /
reference call: the refs are passed as image parts ahead of the prompt, which is
how identity (same man, same wardrobe, same street) is held across keyframes.
"""
import argparse, base64, datetime, json, os, pathlib, sys

ENV = ".env.local"
for ln in open(ENV):
    ln = ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k, _, v = ln.partition("=")
        v = v.strip().strip('"').strip("'")
        if v and k.strip() not in os.environ:
            os.environ[k.strip()] = v

from google import genai
from google.genai import types

ap = argparse.ArgumentParser()
ap.add_argument("prompt_file")
ap.add_argument("out")
ap.add_argument("--ref", action="append", default=[])
ap.add_argument("--model", default="gemini-3-pro-image")
ap.add_argument("--size", default="2K")
ap.add_argument("--ar", default="9:16")
ap.add_argument("--mime", default="image/jpeg")
a = ap.parse_args()

prompt = pathlib.Path(a.prompt_file).read_text().strip()
parts = []
for r in a.ref:
    p = pathlib.Path(r)
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    parts.append({"type": "image", "data": base64.b64encode(p.read_bytes()).decode(),
                  "mime_type": mime})
parts.append({"type": "text", "text": prompt})

client = genai.Client(http_options=types.HttpOptions(timeout=10 * 60 * 1000))
print(f"nano banana pro: {a.model} {a.ar} {a.size} refs={len(a.ref)} -> {a.out}")

interaction = client.interactions.create(
    model=a.model,
    input=parts,
    response_format={"type": "image", "mime_type": a.mime,
                     "aspect_ratio": a.ar, "image_size": a.size},
)

img = getattr(interaction, "output_image", None)
if img is None or not getattr(img, "data", None):
    txt = getattr(interaction, "output_text", None)
    print("no output_image. output_text:", repr(txt)[:1500])
    try:
        print(interaction.model_dump_json()[:3000])
    except Exception:
        print(repr(interaction)[:3000])
    sys.exit("nano: no image in response (check filters above)")

data = img.data
raw = base64.b64decode(data) if isinstance(data, str) else data
pathlib.Path(a.out).write_bytes(raw)
print("saved", a.out, pathlib.Path(a.out).stat().st_size, "bytes")
if getattr(interaction, "output_text", None):
    print("model note:", str(interaction.output_text)[:400])

pathlib.Path(a.out + ".gen.json").write_text(json.dumps({
    "engine": "nano-banana-pro", "model": a.model,
    "mode": "edit" if a.ref else "text-to-image",
    "prompt_file": str(a.prompt_file), "refs": a.ref,
    "aspect_ratio": a.ar, "image_size": a.size,
    "date": datetime.datetime.now().isoformat(timespec="seconds"),
}, indent=2))
