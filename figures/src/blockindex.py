"""Helper: load build/blocks.json into a flat id -> (type, src, text) index (read-only)."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def _text(c):
    out = ""
    for n in c or []:
        if n.get("t") == "text":
            out += n.get("v", "")
        elif "c" in n:
            out += _text(n["c"])
    return out

def load():
    b = json.load(open(os.path.join(ROOT, "build", "blocks.json")))
    idx = {}
    def walk(blocks, top):
        for x in blocks:
            if "id" in x and x.get("type") in ("para", "list", "heading", "table", "quote", "hr"):
                t = x.get("type")
                txt = _text(x.get("c")) if t in ("para", "heading") else ""
                if t == "list" and x.get("items"):
                    it = x["items"][0]
                    for bb in it.get("blocks", []):
                        txt = _text(bb.get("c")); break
                idx[x["id"]] = {"type": t, "src": x.get("src"), "text": txt, "top": top}
    for ch in b["chapters"]:
        walk(ch.get("blocks", []), True)
    return idx

if __name__ == "__main__":
    import sys
    idx = load()
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for k, v in sorted(idx.items()):
        s = v["src"]
        if s and lo <= s[0] <= hi:
            print(k, v["type"], s, v["text"][:90].replace("\n", " "))
