"""Echte lizenzfreie Musik (Kevin MacLeod, incompetech.com, CC BY 4.0):
Intro 'Dreamer' (ruhig) bis zum BOOM, danach 'Lightless Dawn' (dunkel, ruhig, ohne Beat), nahtlos geloopt, Ende ausgeblendet.
Lautstaerke ueber RMS festgelegt (nicht Peak), damit die Stimme immer klar vorne bleibt."""
import numpy as np, av
SR = 48000
def dec(p):
    c = av.open(p); r = av.AudioResampler(format="flt", layout="mono", rate=SR); out = []
    for fr in c.decode(audio=0):
        for f in r.resample(fr): out.append(f.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.float32)
def rms_norm(x, target):
    return x * (target / (np.sqrt(np.mean(x ** 2)) + 1e-9))
def build(n, boom_t, target_rms=0.05):
    intro = rms_norm(dec("music_dl/dreamer.mp3"), target_rms * 0.8)
    main = rms_norm(dec("music_dl/lightless_dawn.mp3"), target_rms)
    out = np.zeros(n, np.float32)
    b = int(boom_t * SR); xf = int(1.5 * SR)
    seg = intro[:b + xf].copy(); seg[-xf:] *= np.linspace(1, 0, xf); out[:len(seg)] += seg[:n]
    pos = b; lx = int(4 * SR); first = True
    while pos < n:
        m = main.copy(); m[:lx if not first else xf] *= np.linspace(0, 1, lx if not first else xf); m[-lx:] *= np.linspace(1, 0, lx)
        L = min(len(m), n - pos); out[pos:pos + L] += m[:L]; pos += len(m) - lx; first = False
    fo = int(4 * SR); out[-fo:] *= np.linspace(1, 0, fo)
    return out
