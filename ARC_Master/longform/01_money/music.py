"""ARC-Musik: eigener, treibender Doku-Beat (lokal synthetisiert, lizenzfrei). Stimmung wechselt pro Kapitel:
mystery (Puls + Pad + leise Arpeggios), drive (Kick, Clap, Hats, Bass, Pluck), dark (tief, Moll, schwer), uplift (Dur, hell).
build(n, sections) -> mono float32; sections = [(start_s, mood), ...]. Speicherschonend: Takte vorrendern, kacheln."""
import numpy as np
SR = 48000; BPM = 96; BEAT = 60 / BPM; BAR = 4 * BEAT
rng = np.random.default_rng(3)
A = 55.0
def hz(semi): return A * 2 ** (semi / 12)
PROG = {"mystery": [(0, "m"), (-4, "M"), (0, "m"), (-2, "M")],          # Am F Am G
        "drive":   [(0, "m"), (-4, "M"), (3, "M"), (-2, "M")],          # Am F C G
        "dark":    [(0, "m"), (0, "m"), (-4, "M"), (-5, "M")],          # Am Am F E
        "uplift":  [(3, "M"), (-2, "M"), (0, "m"), (-4, "M")]}          # C G Am F
LAYERS = {"mystery": dict(kick=0.35, clap=0.0, hat=0.25, bass=0.5, pluck=0.55, pad=0.8),
          "drive":   dict(kick=1.0, clap=0.55, hat=0.6, bass=0.9, pluck=0.7, pad=0.45),
          "dark":    dict(kick=0.8, clap=0.3, hat=0.35, bass=1.0, pluck=0.35, pad=0.7),
          "uplift":  dict(kick=0.9, clap=0.5, hat=0.55, bass=0.8, pluck=0.9, pad=0.6)}
def env(n, a, d):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def lp(x, k=0.15):                       # einfacher Tiefpass (1-Pol), blockweise vektorisiert genug fuer Takt-Laengen
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc += k * (x[i] - acc); y[i] = acc
    return y
def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR; f = 45 + 80 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def clap():
    n = int(0.18 * SR); x = rng.standard_normal(n); x = x - lp(x, 0.3); return x * env(n, 0.002, 0.05) * 0.5
def hat(open_=False):
    n = int((0.12 if open_ else 0.04) * SR); x = rng.standard_normal(n); x = np.diff(x, prepend=0); return x * env(n, 0.001, 0.05 if open_ else 0.012) * 0.25
def tone(f, n, harm=(1, .5, .25), dec=0.4):
    t = np.arange(n) / SR; s = sum(a * np.sin(2 * np.pi * f * (h + 1) * t) for h, a in enumerate(harm)); return s * env(n, 0.004, dec)
KICK, CLAP, HAT, HATO = kick(), clap(), hat(), hat(True)
_cache = {}
def bar(mood, idx):
    key = (mood, idx % 4)
    if key in _cache: return _cache[key]
    L = LAYERS[mood]; n = int(BAR * SR); out = np.zeros(n + SR, np.float32)
    root, q = PROG[mood][idx % 4]; third = 3 if q == "m" else 4
    chord = [root, root + third, root + 7]
    def add(x, t, g):
        i = int(t * SR); out[i:i + len(x)] += (x[:len(out) - i] * g).astype(np.float32)
    for b in range(4):
        if L["kick"] and (mood != "mystery" or b == 0): add(KICK, b * BEAT, 0.9 * L["kick"])
        if L["clap"] and b in (1, 3): add(CLAP, b * BEAT, L["clap"])
        for e in range(2):
            if L["hat"]: add(HATO if (e == 1 and b == 3) else HAT, b * BEAT + e * BEAT / 2, L["hat"] * (1.0 if e else 0.5))
    for e in range(8):                                   # Bass: Achtel-Puls, Oktav-Spruenge
        f = hz(root - 12 + (12 if e in (3, 7) else 0)) * 2
        add(tone(f, int(BEAT / 2 * SR), (1, .6, .3, .15), 0.12), e * BEAT / 2, 0.35 * L["bass"])
    arp = [0, 1, 2, 1, 2, 0, 2, 1] if mood != "dark" else [0, 0, 1, 0, 2, 0, 1, 0]
    for e in range(8):                                   # Pluck-Arpeggio
        f = hz(chord[arp[e]] + 24)
        add(tone(f, int(0.5 * SR), (1, .3, .1), 0.15), e * BEAT / 2, 0.12 * L["pluck"])
    t = np.arange(n) / SR                                # Pad
    pad = sum(np.sin(2 * np.pi * hz(c + 12) * t + j) + 0.5 * np.sin(2 * np.pi * hz(c + 12) * 1.004 * t) for j, c in enumerate(chord)) / 6
    out[:n] += (pad * L["pad"] * 0.22 * np.minimum(1, t / 0.3) * np.minimum(1, (BAR - t) / 0.3)).astype(np.float32)
    _cache[key] = out; return out

def build(n, sections):
    """sections: sortierte Liste (start_s, mood). Takte laufen durchgehend im Raster; Stimmungswechsel auf dem naechsten Takt,
    vor jedem Wechsel ein kurzer Break (letzter halber Takt nur Pad) fuer Spannung."""
    out = np.zeros(n + 2 * SR, np.float32); nb = int(n / SR / BAR) + 1
    starts = [s for s, _ in sections]
    for k in range(nb):
        t0 = k * BAR; j = max(0, np.searchsorted(starts, t0 + 1e-6) - 1); mood = sections[j][1]
        x = bar(mood, k).copy()
        nxt = sections[j + 1][0] if j + 1 < len(sections) else 1e9
        if t0 < nxt <= t0 + BAR + 0.01:                  # Break vor Kapitelwechsel
            h = int(BAR / 2 * SR); x[h:int(BAR * SR)] *= 0.25
        i = int(t0 * SR); out[i:i + len(x)] += x[:len(out) - i]
    out = out[:n]; return (out / (np.abs(out).max() + 1e-9) * 0.9).astype(np.float32)

if __name__ == "__main__":
    import av
    y = build(int(40 * SR), [(0, "mystery"), (10, "drive"), (20, "dark"), (30, "uplift")])
    o = av.open("music_test.wav", "w"); s = o.add_stream("pcm_s16le", rate=SR); s.layout = "mono"
    fr = av.AudioFrame.from_ndarray((y * 32000).astype(np.int16).reshape(1, -1), format="s16", layout="mono"); fr.sample_rate = SR
    for p in s.encode(fr): o.mux(p)
    for p in s.encode(): o.mux(p)
    o.close(); print("ok", np.abs(y).max())
