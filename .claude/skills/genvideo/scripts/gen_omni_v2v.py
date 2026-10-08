#!/usr/bin/env python3
"""Omni Flash video-to-video edit: gen_omni_v2v.py PROMPT_FILE IN.mp4 OUT.mp4 [PREV_INTERACTION_ID]

Restyles an existing clip instead of generating from scratch: uploads the source
through the Files API, then drives gemini-omni-flash-preview's edit task. Pass a
PREV_INTERACTION_ID to refine the previous result conversationally (turn 2+) --
the id of every run is written to OUT.mp4.gen.json.
"""
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

prompt_file, video_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
prev_id = sys.argv[4] if len(sys.argv) > 4 else None
prompt = pathlib.Path(prompt_file).read_text().strip()
src = pathlib.Path(video_path)

client = genai.Client(http_options=types.HttpOptions(timeout=15 * 60 * 1000))

print(f"omni flash v2v: {src.name} -> {out}")
video_file = client.files.upload(file=str(src))
while str(getattr(video_file, "state", "")).endswith("PROCESSING"):
    print("  upload state: PROCESSING")
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)
if str(getattr(video_file, "state", "")).endswith("FAILED"):
    sys.exit(f"omni: file upload failed ({video_file.state})")
print("  source ready:", video_file.uri)

kwargs = {
    "model": "gemini-omni-flash-preview",
    "input": [
        {"type": "document", "uri": video_file.uri},
        {"type": "text", "text": prompt},
    ],
    "response_format": {"type": "video", "aspect_ratio": "9:16", "delivery": "uri"},
}
if prev_id:
    kwargs["previous_interaction_id"] = prev_id
interaction = client.interactions.create(**kwargs)

video = getattr(interaction, "output_video", None)
if video is None:
    # Filters are silent on this path: dump the interaction so the block reason is readable.
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
    "mode": "video-to-video",
    "prompt_file": str(prompt_file),
    "source_video": str(video_path),
    "previous_interaction_id": prev_id,
    "interaction_id": getattr(interaction, "id", None),
    "date": datetime.datetime.now().isoformat(timespec="seconds"),
}
pathlib.Path(out + ".gen.json").write_text(json.dumps(meta, indent=2))
print("interaction id:", meta["interaction_id"], "(pass as arg 4 to refine)")
