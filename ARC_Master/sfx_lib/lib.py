"""ARC SFX-Bibliothek (ElevenLabs, Creator-Lizenz). load(name) -> mono float32 @48k, Stille vorne entfernt, Peak 0.9."""
import os, numpy as np, av
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000; _c = {}
def _dec(p):
    c = av.open(p); r = av.AudioResampler(format="flt", layout="mono", rate=SR); out = []
    for fr in c.decode(audio=0):
        for f in r.resample(fr): out.append(f.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.float32)
def load(name):
    if name in _c: return _c[name]
    npy = os.path.join(D, name + ".npy")
    if os.path.exists(npy): a = np.load(npy)
    else:
        a = _dec(os.path.join(D, name + ".mp3"))
        thr = np.abs(a).max() * 0.05; i = int(np.argmax(np.abs(a) > thr)); a = a[max(0, i - 200):]
        k = np.nonzero(np.abs(a) > thr * 0.2)[0]; a = a[:k[-1] + SR // 10] if len(k) else a
        fade = min(len(a), SR // 20); a[-fade:] *= np.linspace(1, 0, fade)
        a = a / (np.abs(a).max() + 1e-9) * 0.9; np.save(npy, a)
    _c[name] = a; return a
if __name__ == "__main__":
    for f in sorted(os.listdir(D)):
        if f.endswith(".mp3"): a = load(f[:-4]); print(f"{f[:-4]:10s} {len(a)/SR:5.2f}s")
