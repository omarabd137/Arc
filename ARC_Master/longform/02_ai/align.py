"""Satz-Zeitpunkte pro Block: Satzgrenzen werden auf die echten Sprechpausen der Aufnahme gelegt (DP)."""
import re, numpy as np, vo9_tags as T
SR = 48000
def sentences(bid):
    t = re.sub(r"\[[^\]]+\]\s*", "", T.line(bid)).strip()
    return [s.strip() for s in re.findall(r"[^.?!:]+(?:\.\.\.|[.?!:])*", t) if s.strip() and re.search(r"\w", s)]
def gaps(a, min_len=0.18):
    hop = SR // 100; e = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-12)
    thr = max(np.percentile(e, 15) * 2.5, e.max() * 0.03); q = e < thr; out = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) / 100 >= min_len and i > 0 and j < len(q): out.append((i / 100, j / 100))
            i = j
        else: i += 1
    return out
_c = {}
def times(bid):
    """-> Liste Startzeit (s, relativ zum Stimmbeginn) jedes Satzes + Ende."""
    if bid in _c: return _c[bid]
    a = np.load(f"vo9/{bid}.npy"); dur = len(a) / SR; S = sentences(bid); G = gaps(a)
    ch = np.array([len(s) for s in S], float); exp = np.cumsum(ch)[:-1] / ch.sum() * dur; k = len(S) - 1
    if k == 0 or not G: st = [0.0] + list(exp)
    else:
        m = len(G); INF = 1e9; dp = np.full((k + 1, m + 1), INF); bk = np.zeros((k + 1, m + 1), int); dp[0, 0] = 0
        for j in range(1, k + 1):
            for g in range(m):
                h = int(np.argmin(dp[j - 1, :g + 1]))
                if dp[j - 1, h] < INF:
                    gl = G[g][1] - G[g][0]; dp[j, g + 1] = dp[j - 1, h] + abs((G[g][0] + G[g][1]) / 2 - exp[j - 1]) / dur * 8 - min(gl, 0.6) * 2.5
                    bk[j, g + 1] = h
        if k > m: st = [0.0] + list(exp)
        else:
            g = int(np.argmin(dp[k, 1:])) + 1; sel = []
            for j in range(k, 0, -1): sel.append(g - 1); g = bk[j, g]
            st = [0.0] + [G[s][1] for s in reversed(sel)]
    _c[bid] = st + [dur]; return _c[bid]
if __name__ == "__main__":
    import v8_beats as V
    for b in V.BEATS:
        S = sentences(b["id"]); t = times(b["id"])
        print(f"== {b['id']}  ({t[-1]:.1f}s)")
        for i, s in enumerate(S): print(f"  {i:2d} {t[i]:5.1f}  {s[:70]}")
