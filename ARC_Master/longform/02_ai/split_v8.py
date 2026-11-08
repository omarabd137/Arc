"""Schneidet die Brian-Aufnahmen an den Sprechpausen in Block-Stuecke (vo8/<id>.npy, 48 kHz mono).
Stimme wird nicht veraendert: nur an Stille geschnitten; Pausen > 0.5 s innerhalb eines Blocks auf 0.42 s gekuerzt (Tempo wie Top-Kanaele)."""
import json, re, os, numpy as np, av
import v8_beats as V
SR = 48000
OUT = "vo8"; TRIMS = True
os.makedirs("vo8", exist_ok=True); os.makedirs("vo9", exist_ok=True)
old = {b["id"]: b for b in json.load(open("beats.json", encoding="utf-8"))}   # Texte aus SKRIPT_v7
SRC = {
    "chunk_0": ["B0", "B1", "B2", "B3"], "chunk_2": ["B9", "B10", "B11", "B11b"],
    "chunk_3": ["B12", "B13", "B14", "B15", "B16", "B17", "B18"],
    "p04": ["B19", "B20", "B21", "B21b"], "p05": ["B22", "B23"], "p06": ["B24", "B25", "B25b"], "p07": ["B26"],
}
new = {b["id"]: b for b in V.BEATS if "text" in b}
for k, v in V.recs().items(): SRC[k] = v["beats"]
def text(i): return new[i]["text"] if i in new else old[i]["text"]

def dec(p):
    c = av.open(p); r = av.AudioResampler(format="flt", layout="mono", rate=SR); out = []
    for fr in c.decode(audio=0):
        for f in r.resample(fr): out.append(f.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.float32)

def energy(a):
    hop = SR // 100; return np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-12)

def gaps(a, min_len=0.2):
    e = energy(a); thr = max(np.percentile(e, 20) * 2.5, e.max() * 0.02); q = e < thr; out = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) / 100 >= min_len and i > 0 and j < len(q): out.append((i / 100, j / 100))
            i = j
        else: i += 1
    return out

def tighten(seg, maxgap=0.5, keep=0.42):
    G = gaps(seg, maxgap); out = []; pos = 0
    for s, e in G:
        cs = int((s + (e - s) / 2 - keep / 2) * SR); ce = int((s + (e - s) / 2 + keep / 2) * SR)
        out.append(seg[pos:cs]); pos = ce
    out.append(seg[pos:]); return np.concatenate(out)

def trim_edges(seg):
    e = energy(seg); nz = np.nonzero(e > e.max() * 0.03)[0]
    if not len(nz): return seg
    return seg[max(0, nz[0] * SR // 100 - SR // 50):min(len(seg), nz[-1] * SR // 100 + SR // 10)]

def split(src, ids):
    a = dec(f"vo/{src}.mp3"); dur = len(a) / SR
    chars = [len(text(i)) for i in ids]; exp_t = np.cumsum(chars)[:-1] / sum(chars) * dur
    G = [((s + e) / 2, e - s) for s, e in gaps(a)]; k = len(ids) - 1; cuts = []
    if k:
        INF = 1e9; m = len(G); dp = np.full((k + 1, m + 1), INF); bk = np.zeros((k + 1, m + 1), int); dp[0, 0] = 0
        cost = lambda j, g: abs(G[g][0] - exp_t[j - 1]) / dur * 10 - min(G[g][1], 1.5) * 3.0
        for j in range(1, k + 1):
            for g in range(m):
                prev = dp[j - 1, :g + 1]; h = int(np.argmin(prev))
                if prev[h] < INF: dp[j, g + 1] = prev[h] + cost(j, g); bk[j, g + 1] = h
        g = int(np.argmin(dp[k, 1:])) + 1; sel = []
        for j in range(k, 0, -1): sel.append(g - 1); g = bk[j, g]
        cuts = [G[s][0] for s in reversed(sel)]
    edges = [0.0] + cuts + [dur]
    for i, s, e in zip(ids, edges[:-1], edges[1:]):
        seg = trim_edges(a[int(s * SR):int(e * SR)])
        b = next((x for x in V.BEATS if x["id"] == i), {})
        if TRIMS and (b.get("trim_start") or b.get("trim_end")):
            GG = gaps(seg, 0.25)
            if b.get("trim_start"): seg = trim_edges(seg[int(GG[b["trim_start"] - 1][1] * SR) - SR // 40:])
            if b.get("trim_end"): seg = trim_edges(seg[:int(GG[-b["trim_end"]][0] * SR) + SR // 20])
        seg = tighten(seg)
        np.save(f"{OUT}/{i}.npy", seg.astype(np.float32))
        print(f"{src:8s} {i:5s} {s:6.2f}-{e:6.2f} -> {len(seg)/SR:5.2f}s | {text(i)[:55]}")

if __name__ == "__main__":
    for src, ids in SRC.items(): split(src, ids)
    need = [b["id"] for b in V.BEATS]; tot = sum(len(np.load(f"vo8/{i}.npy")) for i in need) / SR
    w = sum(len(text(i).split()) for i in need)
    print(f"TOTAL voice {tot/60:.2f} min, {w} words, {w/(tot/60):.0f} wpm (ohne Blockpausen)")
