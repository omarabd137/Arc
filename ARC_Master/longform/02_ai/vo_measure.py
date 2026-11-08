import sys, av, numpy as np, re
def measure(path, text):
    c = av.open(path); a = np.concatenate([f.to_ndarray().mean(0) for f in c.decode(audio=0)]); sr = c.streams.audio[0].rate
    d = len(a) / sr; hop = sr // 100; e = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, "same")[::hop]); q = e < e.max() * 0.02
    gaps = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if j - i >= 15: gaps.append((j - i) / 100)
            i = j
        else: i += 1
    w = len(re.sub(r"<[^>]+>", " ", text).split())
    return d, w / d * 60, w / (d - sum(gaps)) * 60
if __name__ == "__main__":
    import json; P = {p["name"]: p for p in json.load(open("vo/pieces.json", encoding="utf-8"))}
    for n in sys.argv[1:]:
        d, a, b = measure(f"vo/{n}.mp3", P[n]["text"]); print(n, f"{d:.1f}s overall {a:.0f} speech {b:.0f} wpm")
