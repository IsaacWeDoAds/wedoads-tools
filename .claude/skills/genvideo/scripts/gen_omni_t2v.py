#!/usr/bin/env python3
"""Omni Flash text-to-video: gen_omni_t2v.py PROMPT_FILE OUT.mp4 [seconds]"""
import base64, datetime, json, os, pathlib, sys, time

for ln in open(".env.local"):
    ln = ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k, _, v = ln.partition("=")
        v = v.strip().strip('"').strip("'")
        if v and k.strip() not in os.environ:
            os.environ[k.strip()] = v

from google import genai
from google.genai import types

prompt_file, out = sys.argv[1], sys.argv[2]
seconds = int(sys.argv[3]) if len(sys.argv) > 3 else None
prompt = pathlib.Path(prompt_file).read_text().strip()

client = genai.Client(http_options=types.HttpOptions(timeout=15 * 60 * 1000))

print(f"omni flash t2v -> {out}")
fmt = {"type": "video", "aspect_ratio": "9:16", "delivery": "uri"}
if seconds:
    fmt["duration_seconds"] = seconds
try:
    interaction = client.interactions.create(
        model="gemini-omni-flash-preview",
        input=[{"type": "text", "text": prompt}],
        response_format=fmt,
    )
except Exception as e:
    if seconds and ("duration" in str(e).lower() or "unknown" in str(e).lower() or "invalid" in str(e).lower()):
        print("duration param rejected; retrying at engine default length")
        fmt.pop("duration_seconds", None)
        interaction = client.interactions.create(
            model="gemini-omni-flash-preview",
            input=[{"type": "text", "text": prompt}],
            response_format=fmt,
        )
    else:
        raise

video = getattr(interaction, "output_video", None)
if video is None:
    print("no output_video; interaction dump follows")
    try:
        print(interaction.model_dump_json()[:3000])
    except Exception:
        print(repr(interaction)[:3000])
    sys.exit("omni: no video in response")

data = getattr(video, "data", None)
if data:
    raw = base64.b64decode(data) if isinstance(data, str) else data
    pathlib.Path(out).write_bytes(raw)
else:
    uri = video.uri
    print("video uri:", uri)
    file_id = "files/" + uri.rstrip("/").split("files/")[-1].split(":")[0].split("?")[0]
    for _ in range(60):
        f = client.files.get(name=file_id)
        state = str(getattr(f, "state", ""))
        if "ACTIVE" in state:
            break
        print("  file state:", state)
        time.sleep(5)
    raw = client.files.download(file=f)
    pathlib.Path(out).write_bytes(raw)

print("saved", out, pathlib.Path(out).stat().st_size, "bytes")
meta = {
    "engine": "omni-flash",
    "model": "gemini-omni-flash-preview",
    "mode": "text-to-video",
    "prompt_file": str(prompt_file),
    "date": datetime.datetime.now().isoformat(timespec="seconds"),
}
pathlib.Path(out + ".gen.json").write_text(json.dumps(meta, indent=2))
