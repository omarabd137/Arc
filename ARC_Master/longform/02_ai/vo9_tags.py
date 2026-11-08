"""v9-Aufnahme mit eleven_v4: normal/warm am Anfang (KI wie wir sie kennen), danach tief + ernst. Tags sparsam."""
import json, v8_beats as V
old = {b["id"]: b for b in json.load(open("beats.json", encoding="utf-8"))}
def text(i):
    b = next(x for x in V.BEATS if x["id"] == i)
    return b.get("text") or old[i]["text"]
TAG = {   # Tag vor dem Block (haelt bis zum naechsten Tag)
 "H1": "[warmly]", "H2": "[deep voice] [slowly]", "B0": "[deep voice] [serious]", "B1": "[serious]", "B2": "[dramatically]", "N1": "[deep voice]",
 "B12": "[deep voice] [serious]", "B13": "[curious]", "B14": "[serious]", "B15": "[dramatically]", "B16": "[deep voice] [slowly]", "B17": "[serious]", "B18": "[serious]",
 "N2": "[deep voice]", "B20": "[serious]", "B21": "[cautiously]", "B23": "[serious]",
 "B24": "[deep voice] [serious]", "B25": "[dramatically]", "B25b": "[serious]", "B26": "[serious]",
 "N3a": "[deep voice] [slowly]", "N3b": "[serious]", "N3c": "[deep voice]", "N3d": "[dramatically]", "N3e": "[serious]", "N3f": "[deep voice]", "N3g": "[cautiously]", "N3h": "[serious]",
 "W1": "[deep voice] [slowly]", "W2": "[softly]", "W3": "[serious]", "W4": "[deep voice]", "N4e": "[serious]", "N4f": "[dramatically]", "W5": "[deep voice] [slowly]",
 "N5a": "[serious]", "N5b": "[sarcastic]", "N5c": "[serious]", "N5d": "[deep voice] [slowly]", "N6a": "[serious]", "N6b": "[deep voice]",
}
FIX = {"B24": ("Level five. ", ""), "B0": ("…", "..."), }
def line(i):
    t = text(i)
    if i == "B24": t = t.replace("Level five. ", "")
    t = t.replace("…", "...")
    tag = TAG[i] if i == "H2" else TAG[i].replace(" [slowly]", "")
    return f"{tag} {t}"
def groups(limit=1100):
    out = []; cur = []
    for b in V.BEATS:
        i = b["id"]
        if cur and len(" [pause] ".join(line(x) for x in cur + [i])) > limit: out.append(cur); cur = []
        cur.append(i)
    out.append(cur); return out
if __name__ == "__main__":
    G = groups(); json.dump(G, open("vo/v9_groups.json", "w"), indent=0)
    for k, g in enumerate(G): print(k, g, len(" [pause] ".join(line(x) for x in g)))
    print("TOTAL", sum(len(" [pause] ".join(line(x) for x in g)) for g in G))
