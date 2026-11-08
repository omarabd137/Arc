"""Brian-Aufnahme #02: Kapitel = Abschnitte aus SKRIPT_v7.md, Bloecke getrennt durch <break>. Schnitt spaeter an Pausen."""
import re, json
SRC = "SKRIPT_v7.md"; BR = ' <break time="1.0s" /> '
def load():
    s = open(SRC, encoding="utf-8").read().split("\n---\n", 1)[1]
    chs = []
    for part in re.split(r"\n## ", s)[1:]:
        title = part.splitlines()[0].strip(); beats = []
        for m in re.finditer(r'^(B\d+[a-z]?) \[VISUAL\](.*?)\n(?:\[SFX\](.*?)\n)?"(.*)"\s*$', part, re.M):
            beats.append(dict(id=m.group(1), visual=m.group(2).strip(), sfx=(m.group(3) or "").strip(), text=m.group(4).strip()))
        chs.append(dict(title=title, beats=[b for b in beats]))
    return chs
CH = load()
for c in CH: c["text"] = BR.join(b["text"] for b in c["beats"])
if __name__ == "__main__":
    json.dump([b for c in CH for b in c["beats"]], open("beats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for i, c in enumerate(CH): print(i, c["title"][:40].encode("ascii", "replace").decode(), len(c["beats"]), len(c["text"]))
    print("TOTAL", sum(len(c["text"]) for c in CH), "beats", sum(len(c["beats"]) for c in CH))

def pieces(limit=1150):
    """Kurze Aufnahme-Stuecke (Brian wird bei langen Texten langsamer): ganze Bloecke, max ~limit Zeichen."""
    out = []
    for ci, c in enumerate(CH):
        cur = []
        for b in c["beats"]:
            if cur and len(BR.join(x["text"] for x in cur + [b])) > limit:
                out.append(dict(ch=ci, beats=[x["id"] for x in cur], text=BR.join(x["text"] for x in cur))); cur = []
            cur.append(b)
        out.append(dict(ch=ci, beats=[x["id"] for x in cur], text=BR.join(x["text"] for x in cur)))
    return out
