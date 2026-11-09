"""Short #09 Sound-Design und Mix.
- Stimme (narr.wav, unverändert) ist König.
- Bett: leiser Puls (100 BPM) + Flughafen-Atmosphäre, unter der Stimme abgesenkt. Keine Melodie (Masterplan Teil 28).
- SFX nur auf sichtbare Aktionen, Zeiten aus denselben Wortzeiten wie das Bild (Frame-genau).
- Ziel: -14 LUFS integriert, True Peak < -1 dBTP. Bericht mit Messwerten.
"""
import json, os, sys, wave
import numpy as np
import pyloudnorm as pyln
from scipy.signal import butter, sosfilt, resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "sfx_lib"))
import lib as sfx  # noqa: E402

SR = 48000
FPS = 30
rng = np.random.default_rng(9)

words = json.load(open(os.path.join(HERE, "vo", "words.json"), encoding="utf-8"))
W = words["words"]
DUR = words["duration"]
N = int(DUR * SR)


def wf(i):
    return round(W[i]["start"] * FPS)


def scene_start(k, firsts=(0, 11, 17, 22, 31, 41, 50, 63, 72, 79, 87, 94, 101)):
    return 0 if k == 0 else wf(firsts[k]) - 3


def read_wav(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return a


voice = read_wav(os.path.join(HERE, "vo", "narr.wav"))[:N]
voice = np.pad(voice, (0, N - len(voice)))

db = lambda x: 10 ** (x / 20)
sfx_bus = np.zeros(N, np.float32)
cues = []


def place(sig, t, gain_db, pitch=1.0, maxlen=None, fade_out=0.04):
    if pitch != 1.0:
        up, down = int(round(1000 / pitch)), 1000
        sig = resample_poly(sig, up, down).astype(np.float32)
    if maxlen is not None:
        L = int(maxlen * SR)
        sig = sig[:L].copy()
        fo = min(len(sig), int(fade_out * SR))
        sig[-fo:] *= np.linspace(1, 0, fo)
    i0 = int(max(0, t) * SR)
    i1 = min(N, i0 + len(sig))
    if i1 > i0:
        sfx_bus[i0:i1] += sig[: i1 - i0] * db(gain_db)


def at(i, frames=0):
    return (wf(i) + frames) / FPS


def add(name, t, gain, **kw):
    cues.append((round(t, 3), name, gain))
    place(sfx.load(name), t, gain, **kw)


# ---------- synthetisierte Klänge ----------
def flap_clatter(dur, density=26):
    out = np.zeros(int(dur * SR), np.float32)
    click = sfx.load("click")[: int(0.05 * SR)].copy()
    click *= np.linspace(1, 0, len(click))
    n = int(dur * density)
    for k in range(n):
        p = rng.uniform(0.9, 1.35)
        c = resample_poly(click, int(1000 / p), 1000).astype(np.float32)
        i = int(rng.uniform(0, dur - 0.06) * SR)
        out[i:i + len(c)] += c * rng.uniform(0.35, 1.0)
    env = np.ones_like(out)
    f = int(0.08 * SR)
    env[-f:] = np.linspace(1, 0.2, f)
    return out * env


def boing(dur=0.55):
    t = np.arange(int(dur * SR)) / SR
    f = 260 + 140 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 5)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * 6) * 0.9).astype(np.float32)


def clang(dur=0.9):
    t = np.arange(int(dur * SR)) / SR
    s = sum(np.sin(2 * np.pi * fr * t) * a for fr, a in [(523, 1), (1187, 0.6), (1893, 0.4), (2711, 0.25)])
    return (s * np.exp(-t * 6) * 0.35).astype(np.float32)


def buzz(dur=0.35):
    t = np.arange(int(dur * SR)) / SR
    s = sum(np.sin(2 * np.pi * 60 * h * t) / h for h in range(1, 12))
    gate = (np.sin(2 * np.pi * 14 * t) > -0.2).astype(np.float32)
    return (s * gate * 0.25 * np.exp(-t * 2)).astype(np.float32)


def rumble(dur=2.6):
    n = int(dur * SR)
    x = np.cumsum(rng.standard_normal(n)).astype(np.float32)
    x -= np.convolve(x, np.ones(4800) / 4800, mode="same")
    x /= np.abs(x).max() + 1e-9
    env = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return (x * env * 0.8).astype(np.float32)


def place_sig(sig, t, gain, label):
    cues.append((round(t, 3), label, gain))
    place(sig, t, gain)


# ---------- Cue-Liste (Bild-Ereignisse aus den Szenen, frame-genau) ----------
# S1 Hook
place_sig(flap_clatter(1.05), 0.0, -17, "flap")
add("ding", at(2, 18), -23)
add("stamp", at(6, 2), -13)
add("impact", at(6, 2), -24, pitch=0.8, maxlen=0.6)
add("flutter", at(10), -15)
add("coins", at(10, 2), -23, maxlen=0.8)
# S2
add("whoosh", scene_start(1) / FPS - 0.05, -23, maxlen=0.5)
for k in range(13):
    t = (wf(13) - 4 + k * ((wf(14) + 2 - (wf(13) - 4)) / 13)) / FPS
    add("pop", t, -27, pitch=float(rng.uniform(0.9, 1.25)), maxlen=0.25)
for k in range(4):
    add("pop", at(14, 6 + k * 3), -23, pitch=0.8, maxlen=0.3)
add("error", at(14, 8), -27, maxlen=0.5)
add("stamp", at(16, 0), -12)
add("impact", at(16, 1), -22, maxlen=0.6)
# S3
add("whoosh", scene_start(2) / FPS - 0.05, -25, maxlen=0.45)
add("steps", scene_start(2) / FPS + 0.1, -25)
add("steps", scene_start(2) / FPS + 0.9, -26)
add("whoosh", at(21, -4), -22, maxlen=0.35)
add("impact", at(21, 2), -13)
# S4
add("whoosh", scene_start(3) / FPS - 0.05, -25, maxlen=0.45)
place_sig(boing(), at(26), -17, "boing")
add("impact", at(28, 1), -12)
place_sig(clang(), at(28, 1), -17, "clang")
add("pop", at(30), -20, maxlen=0.3)
# S5
add("doorbell", at(31), -15)
add("pop", at(37, -6), -20, maxlen=0.3)
add("flutter", at(39, 2), -15)
add("coins", at(40, 2), -24, maxlen=0.8)
add("ding", at(40, 2), -27)
# S6
add("whoosh", at(44), -16, maxlen=0.45, fade_out=0.1)
add("ding", at(44, 5), -21)
# S7/S8 Preis-Anzeige
add("click", at(52, -2), -19, maxlen=0.3)
add("counter", at(54, 4), -24, maxlen=(wf(55) - wf(54) - 4) / FPS)
add("cash", at(55, 2), -15, maxlen=1.0)
add("cash", at(57, 2), -15, pitch=1.06, maxlen=1.0)
add("cash", at(59, 2), -15, pitch=1.12, maxlen=1.0)
# S9 Auszahlung
add("stamp", at(64, 1), -13)
add("impact", at(64, 2), -24, pitch=0.8, maxlen=0.6)
riser_len = (wf(69) - wf(66)) / FPS
add("riser", at(69) - riser_len, -17, maxlen=riser_len + 0.05)
add("success", at(69), -13)
add("impact", at(69), -14)
add("flutter", at(69, 2), -15)
add("coins", at(69, 4), -21)
add("impact", at(71, 1), -11, pitch=0.75, maxlen=0.8)
add("paper", at(71, 2), -20, maxlen=0.5)
# S10 Gutschein
add("whoosh", scene_start(8) / FPS - 0.05, -25, maxlen=0.45)
add("paper", at(72, -3), -21, maxlen=0.6)
add("stamp", at(74, 2), -16)
add("whoosh", at(74, 4), -18, maxlen=0.45)
add("mailbox", at(74, 20), -20)
add("flutter", at(75, -2), -15)
add("ding", at(75, 4), -24)
add("ding", at(77, 2), -22, pitch=1.2)
# S11 Unterschrift + Abgang
add("pen", at(80), -15)
add("whoosh", at(83, -3), -18, maxlen=0.5)
add("steps", at(84), -24)
add("steps", at(84, 16), -25)
add("whoosh", at(86, -2), -21, maxlen=0.3)
add("click", at(86, 3), -17, maxlen=0.25)
add("ding", at(86, 4), -24, pitch=1.1)
# S12 Lounge
add("whoosh", scene_start(10) / FPS - 0.05, -26, maxlen=0.45)
add("pop", at(90, -2), -20, maxlen=0.3)
add("coins", at(90, 0), -27, maxlen=0.6)
place_sig(buzz(), at(91, 2), -25, "neon")
place_sig(rumble(), at(91, -6), -27, "takeoff")
# S13 Kabine
add("whoosh", scene_start(11) / FPS - 0.05, -21, maxlen=0.5)
add("ding", at(95, -2), -22, pitch=0.9)
add("pop", at(97, -2), -18, pitch=0.85, maxlen=0.3)
add("stamp", at(97), -16)
add("ding", at(100), -26, pitch=1.15)
# S14 Loop
add("whoosh", scene_start(12) / FPS - 0.05, -19, maxlen=0.5)
place_sig(flap_clatter(0.75), at(107, -12), -18, "flap")
add("ding", at(107, 14), -22)
add("stinger", at(108), -23, maxlen=0.7)
place_sig(flap_clatter(0.32), DUR - 0.32, -19, "flap-loop")

# ---------- Bett: Puls + Atmosphäre ----------
t = np.arange(N) / SR
kick = np.zeros(N, np.float32)
k_len = int(0.22 * SR)
kt = np.arange(k_len) / SR
kick_sig = np.sin(2 * np.pi * np.cumsum(50 + 70 * np.exp(-kt * 28)) / SR) * np.exp(-kt * 14)
period = 60 / 100
for b in np.arange(0, DUR, period):
    i = int(b * SR)
    j = min(N, i + k_len)
    kick[i:j] += kick_sig[: j - i] * (1.0 if int(round(b / period)) % 4 == 0 else 0.7)
hat = np.zeros(N, np.float32)
h_len = int(0.03 * SR)
for b in np.arange(period / 2, DUR, period):
    i = int(b * SR)
    j = min(N, i + h_len)
    hat[i:j] += rng.standard_normal(j - i).astype(np.float32) * np.exp(-np.arange(j - i) / (0.006 * SR))
hat = sosfilt(butter(4, 6000, "high", fs=SR, output="sos"), hat).astype(np.float32)

noise = rng.standard_normal(N).astype(np.float32)
brown = np.cumsum(noise)
brown -= np.convolve(brown, np.ones(9600) / 9600, mode="same")
brown /= np.abs(brown).max() + 1e-9
babble = sosfilt(butter(2, [300, 2500], "band", fs=SR, output="sos"), noise)
babble *= 0.55 + 0.45 * np.sin(2 * np.pi * 0.37 * t) * np.sin(2 * np.pi * 0.11 * t + 1)
amb = (0.7 * brown + 0.3 * babble / (np.abs(babble).max() + 1e-9)).astype(np.float32)


def norm_rms(x, target):
    return x * (target / (np.sqrt(np.mean(x ** 2)) + 1e-9))


bed = norm_rms(kick, 0.016) + norm_rms(hat, 0.0035) + norm_rms(amb, 0.011)

# Ducking unter der Stimme
win = int(0.05 * SR)
env = np.sqrt(np.convolve(voice ** 2, np.ones(win) / win, mode="same"))
active = np.clip(env / 0.02, 0, 1)
active = np.convolve(active, np.ones(int(0.12 * SR)) / int(0.12 * SR), mode="same")
duck = 1 - 0.5 * active  # bis zu -6 dB
bed = bed * duck

mix = voice + sfx_bus  # Bett entfernt (Omar 08.11.: nervig)

# Lautheit auf -14 LUFS, dann sanfter Limiter für True Peak < -1 dBTP
meter = pyln.Meter(SR)
lufs0 = meter.integrated_loudness(mix.astype(np.float64))
mix = mix * db(-14.0 - lufs0)
ceiling = db(-4.0)


def soft_limit(x, c):
    y = x.copy()
    over = np.abs(y) > c * 0.8
    y[over] = np.sign(y[over]) * (c * 0.8 + (c * 0.2) * np.tanh((np.abs(y[over]) - c * 0.8) / (c * 0.2)))
    return y


mix = soft_limit(mix, ceiling)
lufs = meter.integrated_loudness(mix.astype(np.float64))
tp = 20 * np.log10(np.abs(resample_poly(mix, 4, 1)).max() + 1e-12)

# Bett-Verhältnis wie bei der Top-Shorts-Messung (p10/p50 der 50-ms-RMS)
fr = int(0.05 * SR)
rms = np.sqrt(np.mean(mix[: len(mix) // fr * fr].reshape(-1, fr) ** 2, axis=1))
ratio = np.percentile(rms, 10) / np.percentile(rms, 50)

pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
with wave.open(os.path.join(HERE, "mix.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
json.dump([dict(t=c[0], sfx=c[1], gain_db=c[2]) for c in cues], open(os.path.join(HERE, "cues.json"), "w"), indent=1)

print(f"Dauer {DUR:.2f} s | SFX-Cues {len(cues)}")
print(f"Lautheit {lufs:.1f} LUFS (Ziel -14) | True Peak {tp:.2f} dBTP (Ziel < -1)")
print(f"Bett-Verhältnis p10/p50 {ratio:.3f} (Top-Shorts 0.12-0.27)")
