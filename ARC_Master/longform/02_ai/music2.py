"""ARC Doku-Musik v2 (lokal synthetisiert, lizenzfrei, OHNE Drums): cineastische Flaechen statt Beat.
peace   = warm, Dur, sanftes Klavier            (KI wie wir sie kennen)
tension = ernst, Moll, tiefer Bordun + leiser Herzschlag-Puls (Hauptteil, stoert die Stimme nicht)
dark    = tiefer, langsamer, Schwebungen        (dunkelste Stellen)
resolve = ruhig, Moll->Dur Aufloesung           (Ende)
build(n, sections) -> mono float32 @48k."""
import numpy as np
SR = 48000; CH = 12.0                     # Akkord-Dauer s
A1 = 55.0
def hz(semi): return A1 * 2 ** (semi / 12)
PROG = {"peace":   [(3, "M7"), (0, "m7"), (8, "M7"), (10, "M")],     # C  Am  F  G
        "tension": [(0, "m"), (8, "M"), (5, "m"), (7, "M")],         # Am F  Dm E
        "dark":    [(5, "m"), (5, "m"), (1, "M"), (0, "m")],         # Dm Dm Bb A(m)
        "resolve": [(0, "m"), (8, "M"), (3, "M"), (10, "M")]}        # Am F  C  G
IV = {"M": [0, 4, 7], "m": [0, 3, 7], "M7": [0, 4, 7, 11], "m7": [0, 3, 7, 10]}
rng = np.random.default_rng(11)
def soft_tone(f, n, harm=6, bright=1.6):
    t = np.arange(n) / SR; out = np.zeros(n)
    for h in range(1, harm + 1):
        for det in (-0.12, 0.12):        # Chorus
            out += np.sin(2 * np.pi * f * h * (1 + det / 100) * t + rng.uniform(0, 6.28)) / h ** bright
    return out
def env(n, a, r):
    t = np.arange(n) / SR; T = n / SR; return np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (T - t) / r))
def piano(f, n):
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * h * t) * (0.6 ** (h - 1)) for h in range(1, 6))
    return s * np.minimum(1, t / 0.01) * np.exp(-t / 1.6)
_cache = {}
def block(mood, idx):
    key = (mood, idx % 4)
    if key in _cache: return _cache[key]
    n = int((CH + 2.0) * SR); out = np.zeros(n)
    root, q = PROG[mood][idx % 4]; notes = [root + i for i in IV[q]]
    lvl = {"peace": 1.0, "tension": 0.9, "dark": 0.9, "resolve": 0.9}[mood]
    # Flaeche (Pad), weiche Ein-/Ausblendung -> ueberlappt mit naechstem Block
    for k, s_ in enumerate(notes):
        out += soft_tone(hz(s_ + 24), n, 5, 1.8) * 0.16
    out *= env(n, 3.5, 3.5)
    if mood in ("tension", "dark", "resolve"):           # tiefer Bordun
        out += soft_tone(hz(root + (0 if mood != "dark" else -12) + 12), n, 3, 2.0) * env(n, 3.5, 3.5) * 0.30
    if mood in ("tension", "dark"):                       # langsam schwellende Streicherflaeche oben (Spannung ohne Rhythmus)
        t = np.arange(n) / SR; sw = 0.5 - 0.5 * np.cos(2 * np.pi * t / (CH + 2.0))
        out += soft_tone(hz(notes[-1] + 36), n, 4, 2.2) * sw * 0.05
    if mood == "dark":                                   # langsame Schwebung oben
        t = np.arange(n) / SR; out += np.sin(2 * np.pi * hz(root + 36) * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.2 * t)) * 0.05 * env(n, 2, 2)
    if mood in ("peace", "resolve"):                     # sanftes Klavier, langsam
        seq = [notes[i % len(notes)] + 36 for i in range(4)]
        for i, s_ in enumerate(seq):
            st = int((1.0 + i * CH / 4) * SR); x = piano(hz(s_), int(3.5 * SR)) * (0.08 if mood == "peace" else 0.06)
            out[st:st + len(x)] += x[:max(0, n - st)]
    out = (out * lvl).astype(np.float32); _cache[key] = out; return out

def build(n, sections):
    """sections: [(start_s, mood), ...]. Akkordbloecke ueberlappen weich (kein Klick, kein Beat)."""
    out = np.zeros(n + int(10 * SR), np.float32); starts = [s for s, _ in sections]; k = 0; t = 0.0
    while t * SR < n:
        j = max(0, np.searchsorted(starts, t + 1e-6) - 1); mood = sections[j][1]
        x = block(mood, k); i = int(t * SR); out[i:i + len(x)] += x[:len(out) - i]; t += CH; k += 1
    out = out[:n]
    return (out / (np.abs(out).max() + 1e-9) * 0.9).astype(np.float32)

if __name__ == "__main__":
    import av
    y = build(int(48 * SR), [(0, "peace"), (12, "tension"), (24, "dark"), (36, "resolve")])
    o = av.open("music2_test.wav", "w"); s = o.add_stream("pcm_s16le", rate=SR); s.layout = "mono"
    fr = av.AudioFrame.from_ndarray((y * 32000).astype(np.int16).reshape(1, -1), format="s16", layout="mono"); fr.sample_rate = SR
    for p in s.encode(fr): o.mux(p)
    for p in s.encode(): o.mux(p)
    o.close(); print("ok", float(np.abs(y).max()))
