import os, json, base64, subprocess, sys, time
for ln in open('.env.local'):
    ln=ln.strip()
    if ln and not ln.startswith('#'):
        k,_,v=ln.partition('='); os.environ[k.strip()]=v.strip().strip('"').strip("'")
KEY=os.environ["OPENAI_API_KEY"]
OUT="public/broll/reel04/fake"

BASE=("Amateur AI-generated promotional poster, obviously synthetic. "
      "Subject placed perfectly dead-centre, symmetrical, no art direction. "
      "Heavy soft glowing bloom light on absolutely everything, hazy dreamy haze, "
      "no directional key light, flat and airbrushed. "
      "Cover it in DENSE small body text and several long headlines and subheadings "
      "and captions, packed edge to edge, many lines of tiny text. Glossy, oversaturated. ")
PROMPTS=[
 ("f1","A tech startup launch poster with a smiling businessman, blue and purple gradient background."),
 ("f2","A productivity app advertisement poster with a laptop floating in the middle."),
 ("f3","An online course poster with a female instructor, warm orange background."),
 ("f4","A fitness coaching poster with a muscular trainer, green gradient background."),
 ("f5","A coffee brand poster with a coffee cup in the centre, brown background."),
 ("f6","An AI SaaS product poster with a glowing robot head, dark navy background."),
]
for name, subject in PROMPTS:
    dest=f"{OUT}/{name}.png"
    if os.path.exists(dest): print("skip",name); continue
    body=json.dumps({"model":"gpt-image-2","prompt":BASE+subject,
                     "size":"1024x1536","n":1})
    p=subprocess.run(["curl","-s","-m","300","https://api.openai.com/v1/images/generations",
        "-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json","-d",body],
        capture_output=True,text=True)
    try:
        d=json.loads(p.stdout)
    except Exception:
        print(name,"BADJSON",p.stdout[:200]); continue
    if "error" in d:
        print(name,"ERROR",d["error"].get("message")[:160]); continue
    b64=d["data"][0].get("b64_json")
    if not b64:
        print(name,"no b64", list(d["data"][0].keys())); continue
    open(dest,"wb").write(base64.b64decode(b64))
    print("wrote",dest, os.path.getsize(dest))
