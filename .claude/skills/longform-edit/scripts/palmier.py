#!/usr/bin/env python3
"""Minimal MCP client for Palmier Pro (streamable HTTP + SSE) — the harness could not connect at session start.
   python3 palmier.py tools            -> tool names + one-line descriptions
   python3 palmier.py schema <tool>    -> full input schema
   python3 palmier.py call <tool> '<json args>'
Importable: P = Palmier(); P.call("get_timeline", {})"""
import json, sys, urllib.request
URL = "http://127.0.0.1:19789/mcp"
class Palmier:
    def __init__(self):
        self.sid = None; self.n = 0
        self.rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "claude-code-lf01", "version": "1"}})
        self.notify("notifications/initialized")
    def _post(self, body):
        req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream", **({"MCP-Session-Id": self.sid} if self.sid else {})})
        with urllib.request.urlopen(req, timeout=120) as r:
            if not self.sid: self.sid = r.headers.get("MCP-Session-Id")
            ctype = r.headers.get("Content-Type", ""); raw = r.read().decode()
        if "text/event-stream" in ctype:
            msgs = [json.loads(l[5:].strip()) for l in raw.splitlines() if l.startswith("data:") and l[5:].strip()]
            return msgs[-1] if msgs else None
        return json.loads(raw) if raw.strip() else None
    def notify(self, method, params=None):
        try: self._post({"jsonrpc": "2.0", "method": method, "params": params or {}})
        except Exception: pass
    def rpc(self, method, params=None):
        self.n += 1
        res = self._post({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params or {}})
        if res and "error" in res: raise RuntimeError(json.dumps(res["error"]))
        return res["result"] if res else None
    def tools(self): return self.rpc("tools/list")["tools"]
    def call(self, name, args=None):
        r = self.rpc("tools/call", {"name": name, "arguments": args or {}})
        out = []
        import base64, os, time
        for c in r.get("content", []):
            if c.get("type") == "text":
                try: out.append(json.loads(c["text"]))
                except Exception: out.append(c["text"])
            elif c.get("type") == "image":
                os.makedirs("work/lf01/work/palmier_frames", exist_ok=True)
                fn = f"work/lf01/work/palmier_frames/{name}_{int(time.time()*1000)}_{len(out)}.png"
                open(fn, "wb").write(base64.b64decode(c["data"])); out.append({"image": fn})
        if r.get("isError"): raise RuntimeError(json.dumps(out)[:2000])
        return out[0] if len(out) == 1 else out
if __name__ == "__main__":
    P = Palmier(); cmd = sys.argv[1] if len(sys.argv) > 1 else "tools"
    if cmd == "tools":
        for t in P.tools(): print(f"- {t['name']}: {t.get('description','').strip().splitlines()[0][:160]}")
    elif cmd == "schema":
        t = next(t for t in P.tools() if t["name"] == sys.argv[2]); print(t.get("description", "")); print(json.dumps(t.get("inputSchema"), indent=1))
    elif cmd == "call":
        print(json.dumps(P.call(sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}), indent=1)[:20000])
