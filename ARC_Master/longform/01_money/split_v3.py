"""Teilt eine Jason-Kapitelaufnahme (vo_v4/chunk_N.mp3) an den Sprechpausen in Beat-Stuecke (vo_v4/beat_XX.npy).
Schnittpunkte: Pausen, die am besten zu den erwarteten Stellen (Zeichen-Anteil) passen (DP). Stimme wird nicht veraendert,
nur an Stille geschnitten. Aufruf: python split_vo.py 0 [1 2 ...]"""
import sys, json, re, numpy as np, av
SR = 48000
import vo_v3_script as V
C = V.CH; B = {b["id"]: b for b in json.load(open("beats_v3.json", encoding="utf-8"))}
CTA = "If this changed how you see money, subscribe. There's a lot more the banks will never tell you."

def dec(p):
    c = av.open(p); r = av.AudioResampler(format="flt", layout="mono", rate=SR); out = []
    for fr in c.decode(audio=0):
        for f in r.resample(fr): out.append(f.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.float32)

def gaps(a, min_len=0.22):
    hop = SR // 100; e = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-12)
    thr = max(np.percentile(e, 20) * 2.5, e.max() * 0.02); q = e < thr; out = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) / 100 >= min_len and i > 0 and j < len(q): out.append(((i + j) / 200, (j - i) / 100))
            i = j
        else: i += 1
    return out   # (Mitte s, Laenge s)

def split(n):
    ch = C[n]; beats = ch["beats"]; a = dec(f"vo_v3/chunk_{n}.mp3"); dur = len(a) / SR
    chars = [len(B[b]["text"]) for b in beats]
    cum = np.cumsum(chars)[:-1] / sum(chars); exp_t = cum * dur
    G = gaps(a); k = len(beats) - 1
    if k == 0: cuts = []
    else:
        INF = 1e9; m = len(G); dp = np.full((k + 1, m + 1), INF); bk = np.zeros((k + 1, m + 1), int); dp[0, 0] = 0
        cost = lambda j, g: abs(G[g][0] - exp_t[j - 1]) / dur * 10 - min(G[g][1], 1.5) * 1.2
        for j in range(1, k + 1):                 # j-ter Schnitt auf Pause g; Pausen streng aufsteigend
            for g in range(m):
                prev = dp[j - 1, :g + 1]; h = int(np.argmin(prev))
                if prev[h] < INF: dp[j, g + 1] = prev[h] + cost(j, g); bk[j, g + 1] = h
        g = int(np.argmin(dp[k, 1:])) + 1; sel = []
        for j in range(k, 0, -1): sel.append(g - 1); g = bk[j, g]
        cuts = [G[s][0] for s in reversed(sel)]
    edges = [0.0] + cuts + [dur]
    for b, s, e in zip(beats, edges[:-1], edges[1:]):
        seg = a[int(s * SR):int(e * SR)]
        hop = SR // 100; en = np.sqrt(np.convolve(seg ** 2, np.ones(hop) / hop, "same") + 1e-12); nz = np.nonzero(en > en.max() * 0.03)[0]
        if len(nz): seg = seg[max(0, nz[0] - SR // 50):min(len(seg), nz[-1] + SR // 12)]
        np.save(f"vo_v3/{b}.npy", seg.astype(np.float32))
        print(f"{b:5s}: {s:6.2f}-{e:6.2f}s  -> {len(seg)/SR:5.2f}s | {B[b]['text'][:60]}")
    print(f"chunk {n}: {dur:.1f}s, {sum(chars)} Zeichen, {len(' '.join(B[b]['text'] for b in beats).split())/(dur/60):.0f} Woerter/Min")

if __name__ == "__main__":
    for n in sys.argv[1:]: split(int(n))
