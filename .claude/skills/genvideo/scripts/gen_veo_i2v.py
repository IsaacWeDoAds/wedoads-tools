#!/usr/bin/env python3
"""Veo IMAGE-TO-VIDEO — animate a still Nishant already owns (GEMINI_API_KEY).

This is the restyle path from the skill's allow-list: motion generated FROM his
own footage, so the person on screen is really him rather than a synthesised
stranger. Same cost gate as gen_veo.py applies.

Usage: gen_veo_i2v.py PROMPT_FILE IMAGE.png OUT.mp4 [--model …] [--fast]
"""
import argparse
import datetime
import json
import os
import pathlib
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("prompt_file")
p.add_argument("image")
p.add_argument("out")
p.add_argument("--model", default="veo-3.1-generate-preview")
p.add_argument("--fast", action="store_true")
args = p.parse_args()

# auto-load the project .env.local so keys don't need shell exports
_env = pathlib.Path(__file__).resolve().parents[4] / ".env.local"
if _env.exists():
    for _line in _env.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            _v = _v.strip().strip('"').strip("'")
            if _v and _k.strip() not in os.environ:
                os.environ[_k.strip()] = _v

if not os.environ.get("GEMINI_API_KEY"):
    sys.exit("GEMINI_API_KEY not set")

from google import genai
from google.genai import types

model = "veo-3.1-fast-generate-preview" if args.fast else args.model
prompt = pathlib.Path(args.prompt_file).read_text().strip()
img_path = pathlib.Path(args.image)
mime = "image/png" if img_path.suffix.lower() == ".png" else "image/jpeg"

client = genai.Client()
op = client.models.generate_videos(
    model=model,
    prompt=prompt,
    image=types.Image(image_bytes=img_path.read_bytes(), mime_type=mime),
    config=types.GenerateVideosConfig(aspect_ratio="9:16"),
)
print(f"veo i2v: generating with {model} from {img_path.name} …")
while not op.done:
    time.sleep(10)
    op = client.operations.get(op)
    print("  …still generating")

if getattr(op, "error", None):
    sys.exit(f"veo error: {op.error}")

vid = op.response.generated_videos[0]
client.files.download(file=vid.video)
vid.video.save(args.out)
print(f"saved {args.out}")

meta = {
    "engine": "veo",
    "model": model,
    "mode": "image-to-video",
    "prompt_file": str(args.prompt_file),
    "source_image": str(args.image),
    "date": datetime.datetime.now().isoformat(timespec="seconds"),
}
pathlib.Path(str(args.out) + ".gen.json").write_text(json.dumps(meta, indent=2))
