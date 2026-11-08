"""Selbst erzeugte Soundeffekte und Spannungsmusik (48 kHz mono, numpy). Kein fremdes Material, keine Lizenzfragen."""
import numpy as np

SR = 48000
rng = np.random.default_rng(7)

def t(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.standard_normal(int(SR * d)).astype(np.float32)

def band(x, lo, hi):
    """Bandpass per FFT."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x)).astype(np.float32)

def env(n, a, r, sustain=0.0):
    """Attack a s, dann exponentielles Abklingen (r = Zeitkonstante)."""
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / max(a, 1e-4)) * (sustain + (1 - sustain) * np.exp(-np.maximum(0, tt - a) / r))
    return e.astype(np.float32)

def norm(x, peak=0.9):
    m = np.abs(x).max()
    return (x / m * peak).astype(np.float32) if m > 0 else x

def engine(d=2.2, f0=38, f1=95, rev_at=0.25):
    """Sportwagen-Motor: harmonischer Saegezahn mit steigender Drehzahl + Brummen."""
    tt = t(d)
    f = f0 + (f1 - f0) * np.clip((tt - rev_at) / 0.6, 0, 1) ** 0.7 * np.exp(-np.maximum(0, tt - rev_at - 0.8) * 0.8)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 9)) + 0.25 * band(noise(d), 60, 900)
    x *= (0.6 + 0.4 * np.sin(ph * 0.5) ** 2)
    x = band(x, 25, 2500)
    return norm(x * env(len(x), 0.08, 0.9, 0.55) * np.minimum(1, (d - tt) / 0.4), 0.8)

def tractor(d=2.0):
    """Tuckernder Traktor: dumpfe Pulse ~7/s."""
    tt = t(d)
    puls = (np.sin(2 * np.pi * 7 * tt) > 0.6).astype(np.float32)
    x = band(noise(d), 40, 400) * (0.3 + puls) + 0.4 * np.sin(2 * np.pi * 52 * tt) * puls
    return norm(band(x, 30, 1200) * np.minimum(1, tt / 0.15) * np.minimum(1, (d - tt) / 0.3), 0.7)

def clank(d=0.6, base=620):
    tt = t(d)
    x = sum(np.sin(2 * np.pi * base * r * tt) * np.exp(-tt * (9 + 4 * i)) for i, r in enumerate((1, 1.58, 2.37, 3.51, 4.9)))
    x += 0.5 * band(noise(d), 2000, 9000) * np.exp(-tt * 60)
    return norm(x, 0.7)

def grind(d=1.2):
    """Kupplung rutscht: kratzendes Metall + Rattern."""
    tt = t(d)
    x = band(noise(d), 700, 4000) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * tt)) + 0.6 * np.sign(np.sin(2 * np.pi * 90 * tt)) * 0.3
    return norm(band(x, 80, 6000) * env(len(x), 0.05, 0.6, 0.3), 0.6)

def hiss(d=1.4):
    tt = t(d)
    return norm(band(noise(d), 2500, 12000) * env(len(tt), 0.08, 0.5, 0.2), 0.45)

def thud(d=0.5, f=70):
    """Tuer knallt / dumpfer Schlag."""
    tt = t(d)
    x = np.sin(2 * np.pi * f * tt * (1 - 0.3 * tt)) * np.exp(-tt * 14) + 0.7 * band(noise(d), 80, 1500) * np.exp(-tt * 40)
    return norm(x, 0.9)

def boom(d=1.8):
    """Tiefer Impact fuer Wendepunkte (filmisch, kein Spiel-Sound)."""
    tt = t(d)
    f = 110 * np.exp(-tt * 2.2) + 32
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2) + 0.35 * band(noise(d), 30, 300) * np.exp(-tt * 4)
    return norm(x, 0.95)

def whoosh(d=0.45):
    tt = t(d)
    x = noise(d); out = np.zeros_like(x)
    for i, (lo, hi) in enumerate([(300, 900), (700, 2000), (1500, 4000), (2500, 7000)]):
        seg = band(x, lo, hi); w = np.exp(-((tt / d - (i + 0.5) / 4) ** 2) / 0.02)
        out += seg * w
    return norm(out * np.sin(np.pi * tt / d), 0.5)

def heartbeat(d=1.0):
    tt = t(d)
    x = np.zeros_like(tt)
    for s in (0.0, 0.28):
        m = tt >= s
        x[m] += np.sin(2 * np.pi * 48 * (tt[m] - s)) * np.exp(-(tt[m] - s) * 18)
    return norm(x, 0.8)

def flash(d=0.35):
    """Fotoblitz: Klick + kurzes Aufladen."""
    tt = t(d)
    x = band(noise(d), 1500, 9000) * np.exp(-tt * 45) + 0.25 * np.sin(2 * np.pi * (3000 + 6000 * tt) * tt) * np.exp(-tt * 12)
    return norm(x, 0.45)

def crowd(d=3.0, gasp_at=0.3):
    """Raunen einer Menge: viele gefilterte Stimmenbaender mit langsamer Huellkurve, am Anfang ein 'Ooh'."""
    tt = t(d)
    x = np.zeros_like(tt)
    for k in range(14):
        b = band(noise(d), 250 + 60 * k, 900 + 80 * k)
        x += b * (0.6 + 0.4 * np.sin(2 * np.pi * (0.7 + 0.13 * k) * tt + k))
    ooh = np.exp(-((tt - gasp_at - 0.25) ** 2) / 0.08)
    vow = sum(np.sin(2 * np.pi * f * tt) / (i + 1) for i, f in enumerate((210, 420, 630, 840)))
    x = band(x, 200, 3000) * 0.5 + vow * ooh * 0.25
    return norm(x * np.minimum(1, tt / 0.3) * np.minimum(1, (d - tt) / 0.6), 0.5)

def hammer(d=1.6, rate=3.0):
    tt = t(d); x = np.zeros_like(tt); h = clank(0.3, 900) * 0.8
    for s in np.arange(0.05, d - 0.3, 1 / rate):
        i = int(s * SR); x[i:i + len(h)] += h[:len(x) - i]
    return norm(x + 0.15 * band(noise(d), 60, 400), 0.55)

def rustle(d=0.8):
    tt = t(d)
    cr = (rng.random(len(tt)) > 0.995).astype(np.float32)
    x = band(noise(d), 2000, 8000) * np.convolve(cr, np.exp(-np.arange(400) / 60), "same")
    return norm(x * np.sin(np.pi * tt / d), 0.4)

def laugh(d=1.4):
    """Leises, tiefes Lachen als Unterlage (Ha-Ha-Puls), nur Atmosphaere."""
    tt = t(d)
    p = (np.sin(2 * np.pi * 5.5 * tt) > 0.3).astype(np.float32)
    x = band(noise(d), 300, 1400) * p * np.exp(-tt * 1.2)
    return norm(x, 0.35)

def music(d, hits=(), swell_at=None):
    """Dunkle Spannungsflaeche: tiefer Drone + weicher Puls, steigt an. hits = Zeitpunkte fuer tiefe Akzente."""
    tt = t(d)
    def saw(f): return 2 * ((tt * f) % 1) - 1
    drone = band(saw(55) + saw(55.4) + 0.6 * saw(82.4) + 0.4 * saw(110.3), 30, 600) * 0.25
    rise = 0.5 + 0.5 * (tt / d)
    pulse = np.zeros_like(tt)
    beat = 60 / 92
    k = np.sin(2 * np.pi * 50 * (tt % beat)) * np.exp(-(tt % beat) * 16)
    pulse += k * 0.5
    pad = band(sum(np.sin(2 * np.pi * f * tt + i) for i, f in enumerate((220, 261.6, 329.6))), 100, 2000) * 0.06
    x = (drone + pulse) * rise + pad * rise
    if swell_at is not None:   # beim Miura: heller Akkord
        m = np.clip((tt - swell_at) / 1.5, 0, 1) * np.clip((d - tt) / 1.0, 0, 1)
        x += 0.18 * m * sum(np.sin(2 * np.pi * f * tt) for f in (277.2, 349.2, 415.3, 554.4))
    for h in hits:
        i = int(h * SR); b = boom(1.8) * 0.6
        x[i:i + len(b)] += b[:len(x) - i]
    return norm(x * np.minimum(1, tt / 1.0) * np.minimum(1, (d - tt) / 1.2), 0.9)
