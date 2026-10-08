#!/usr/bin/env python3
"""Generate a portrait clip with Sora 2 via the OpenAI API (OPENAI_API_KEY).

Usage: gen_sora.py PROMPT_FILE OUT.mp4 [--model sora-2] [--size 720x1280] [--seconds 8]

Writes OUT.mp4 plus OUT.gen.json. sora-2-pro supports 1024x1792.
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
p.add_argument("--model", default="sora-2")
p.add_argument("--size", default="720x1280")
p.add_argument("--seconds", default="8")
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

if not os.environ.get("OPENAI_API_KEY"):
    sys.exit("OPENAI_API_KEY not set")

from openai import OpenAI  # pip install openai

prompt = pathlib.Path(args.prompt_file).read_text().strip()
client = OpenAI()

video = client.videos.create(
    model=args.model,
    prompt=prompt,
    size=args.size,
    seconds=args.seconds,
)
print(f"sora: job {video.id} ({args.model}, {args.size}, {args.seconds}s) …")
while video.status in ("queued", "in_progress"):
    time.sleep(5)
    video = client.videos.retrieve(video.id)
    print(f"  {video.status} {getattr(video, 'progress', '')}")

if video.status == "failed":
    err = getattr(getattr(video, "error", None), "message", "generation failed")
    sys.exit(f"sora: {err}")

content = client.videos.download_content(video.id, variant="video")
content.write_to_file(args.out)

meta = {
    "engine": "sora",
    "model": args.model,
    "size": args.size,
    "seconds": args.seconds,
    "video_id": video.id,
    "prompt_file": str(pathlib.Path(args.prompt_file).resolve()),
    "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
}
pathlib.Path(args.out).with_suffix(".gen.json").write_text(json.dumps(meta, indent=2))
print(f"saved {args.out}")
