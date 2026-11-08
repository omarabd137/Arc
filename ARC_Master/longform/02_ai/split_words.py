"""Exakter Schnitt per Wort-Zeitstempel (ElevenLabs Scribe): jeder Block beginnt mit seinem ersten und endet mit seinem letzten Wort.
Stimme unveraendert (nur geschnitten). Ausgabe: vo10/<id>.npy + vo10/words.json {id: [[wort, start, ende], ...]} relativ zum Blockbeginn."""
import json, re, os, numpy as np, av
import vo9_tags as T, split_v8 as S
SR = 48000; os.makedirs("vo10", exist_ok=True)
G = json.load(open("vo/v9_groups.json"))
def spoken(i): return re.sub(r"\[[^\]]+\]", " ", T.line(i)).split()
out = {}
for k, ids in enumerate(G):
    fn = f"vo/w{k}.json"
    if not os.path.exists(fn): print("fehlt", fn); continue
    W = [w for w in json.load(open(fn, encoding="utf-8"))["words"] if not (w["text"].startswith("[") or w["text"].endswith("]"))]
    need = sum(len(spoken(i)) for i in ids)
    if len(W) != need: print(f"g{k}: {len(W)} Woerter vs {need} erwartet");
    a = S.dec(f"vo/g{k}.mp3"); pos = 0; prev_end = 0.0
    for j, i in enumerate(ids):
        n = len(spoken(i)); ws = W[pos:pos + n]; pos += n
        s = max(prev_end, ws[0]["start"] - 0.06); e = ws[-1]["end"] + 0.12
        if j + 1 < len(ids) and pos < len(W): e = min(e, W[pos]["start"] - 0.02)
        seg = a[int(s * SR):int(e * SR)].copy(); f = min(len(seg), SR // 100); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        np.save(f"vo10/{i}.npy", seg.astype(np.float32)); prev_end = e
        out[i] = [[w["text"], round(w["start"] - s, 3), round(w["end"] - s, 3)] for w in ws]
        print(f"g{k} {i:5s} {s:6.2f}-{e:6.2f}  {ws[0]['text']} ... {ws[-1]['text']}")
json.dump(out, open("vo10/words.json", "w", encoding="utf-8"), ensure_ascii=False)
