#!/usr/bin/env python3
"""Generate a 9:16 clip with Veo via the Gemini API (GEMINI_API_KEY).

Usage: gen_veo.py PROMPT_FILE OUT.mp4 [--model veo-3.1-generate-preview] [--fast]

Writes OUT.mp4 plus OUT.gen.json (traceability). Prompt comes from a file so the
negative-constraint block survives shell quoting.
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
p.add_argument("out")
p.add_argument("--model", default="veo-3.1-generate-preview")
p.add_argument("--fast", action="store_true", help="use veo-3.1-fast-generate-preview")
p.add_argument("--aspect", default="9:16", choices=["9:16", "16:9"],
               help="aspect ratio; 9:16 for reels (default), 16:9 for YouTube/landscape")
p.add_argument("--resolution", default=None, choices=["720p", "1080p"],
               help="output resolution. The API DEFAULTS TO 720p if unset, so a "
                    "1080-line timeline must pass 1080p explicitly or the clip "
                    "comes back needing an upscale.")
p.add_argument("--no-audio", action="store_true",
               help="skip audio generation (cheaper; the edit VO owns the mix anyway)")
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

from google import genai  # pip install google-genai
from google.genai import types

model = "veo-3.1-fast-generate-preview" if args.fast else args.model
prompt = pathlib.Path(args.prompt_file).read_text().strip()

client = genai.Client()
op = client.models.generate_videos(
    model=model,
    prompt=prompt,
    config=types.GenerateVideosConfig(
        aspect_ratio=args.aspect,
        **({"resolution": args.resolution} if args.resolution else {}),
        **({"generate_audio": False} if args.no_audio else {}),
    ),
)
print(f"veo: generating with {model} at {args.aspect} {args.resolution or '(api default)'} …")
while not op.done:
    time.sleep(10)
    op = client.operations.get(op)
    print("  …still generating")

gen = getattr(op.response, "generated_videos", None)
if not gen:
    reasons = getattr(op.response, "rai_media_filtered_reasons", None)
    count = getattr(op.response, "rai_media_filtered_count", None)
    sys.exit(f"veo: BLOCKED, no video returned. filtered_count={count} reasons={reasons}")

vid = gen[0]
client.files.download(file=vid.video)
vid.video.save(args.out)

meta = {
    "engine": "veo",
    "model": model,
    "prompt_file": str(pathlib.Path(args.prompt_file).resolve()),
    "aspect_ratio": args.aspect,
    "resolution": args.resolution,
    "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
}
pathlib.Path(args.out).with_suffix(".gen.json").write_text(json.dumps(meta, indent=2))
print(f"saved {args.out}")
