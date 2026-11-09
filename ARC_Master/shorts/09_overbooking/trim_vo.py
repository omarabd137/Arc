"""Short #09: kürzt NUR Stille zwischen Wörtern (Regel: Stimme nie verändern, Stille kürzen erlaubt).
Lange Pausen werden in ihrer Mitte gekürzt, mit 12-ms-Überblendung gegen Knackser.
Absichtliche Pausen (Countdown, vor der Pointe) bleiben unangetastet, weil sie unter der Schwelle liegen.
Ausgabe: vo/narr.wav (48 kHz mono) + vo/words.json (verschobene Zeiten) + Bericht.
"""
import json, os
import av
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VO = os.path.join(HERE, "vo")
SR = 48000

words = json.load(open(os.path.join(VO, "words_raw.json"), encoding="utf-8"))
words = [w for w in words if w["text"] not in ("—",)]  # Gedankenstriche sind keine gesprochenen Wörter

# Audio laden und auf 48 kHz mono bringen
c = av.open(os.path.join(VO, "narr_raw.mp3"))
res = av.AudioResampler(format="flt", layout="mono", rate=SR)
chunks = []
for fr in c.decode(audio=0):
    for r in res.resample(fr):
        chunks.append(r.to_ndarray().reshape(-1))
for r in res.resample(None):
    chunks.append(r.to_ndarray().reshape(-1))
audio = np.concatenate(chunks).astype(np.float32)

# Zielpausen: Schwelle 0.36 s; Sonderfälle nach Sprech-Partitur
SPECIAL = {("fifty", "in"): 0.40, ("overbooked", "right"): 0.35}
THRESH, DEFAULT = 0.36, 0.30
MARGIN = 0.09  # Abstand zur Wortgrenze, in dem nie geschnitten wird
XF = int(0.012 * SR)

cuts = []  # (start_s, end_s) zu entfernende Bereiche
for a, b in zip(words, words[1:]):
    gap = b["start"] - a["end"]
    key = (a["text"].strip(".,?").lower(), b["text"].strip(".,?").lower())
    target = SPECIAL.get(key, DEFAULT)
    if gap > THRESH and gap > target:
        excess = gap - target
        mid = (a["end"] + b["start"]) / 2
        s, e = mid - excess / 2, mid + excess / 2
        s, e = max(s, a["end"] + MARGIN), min(e, b["start"] - MARGIN)
        if e - s > 0.03:
            cuts.append((s, e, a["text"], b["text"], gap))

# Sicherheitsprüfung: geschnittene Bereiche müssen leise sein
report = []
for s, e, at, bt, gap in cuts:
    seg = audio[int(s * SR):int(e * SR)]
    rms = float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0
    report.append((at, bt, round(gap, 3), round(e - s, 3), round(rms, 5)))

voice_rms = float(np.sqrt(np.mean(audio[audio != 0] ** 2)))

# Schneiden mit Überblendung
out = []
pos = 0
for s, e, *_ in cuts:
    si, ei = int(s * SR), int(e * SR)
    keep = audio[pos:si].copy()
    if out and len(keep) > XF:
        prev = out[-1]
        fade = np.linspace(0, 1, XF, dtype=np.float32)
        prev[-XF:] = prev[-XF:] * (1 - fade) + keep[:XF] * fade
        keep = keep[XF:]
    out.append(keep)
    pos = ei
tail = audio[pos:].copy()
if out and len(tail) > XF:
    fade = np.linspace(0, 1, XF, dtype=np.float32)
    out[-1][-XF:] = out[-1][-XF:] * (1 - fade) + tail[:XF] * fade
    tail = tail[XF:]
out.append(tail)
trimmed = np.concatenate(out)


def remap(t):
    shift = 0.0
    for s, e, *_ in cuts:
        if t >= e:
            shift += e - s
        elif t > s:
            return s - shift
    return t - shift


new_words = [dict(text=w["text"], start=round(remap(w["start"]), 3), end=round(remap(w["end"]), 3)) for w in words]
# kurzer Nachlauf für den Loop
end_t = new_words[-1]["end"] + 0.30
trimmed = trimmed[: int(end_t * SR)]
if len(trimmed) < int(end_t * SR):
    trimmed = np.pad(trimmed, (0, int(end_t * SR) - len(trimmed)))

# WAV schreiben (16-bit PCM)
import wave
pcm = np.clip(trimmed, -1, 1)
pcm = (pcm * 32767).astype(np.int16)
with wave.open(os.path.join(VO, "narr.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
json.dump(dict(duration=round(end_t, 3), words=new_words), open(os.path.join(VO, "words.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print(f"Vorher {len(audio)/SR:.2f} s  ->  nachher {end_t:.2f} s  (gekürzt {len(audio)/SR-end_t:.2f} s)")
print(f"Stimm-RMS {voice_rms:.4f}")
print("Gekürzte Pausen (nach | vor | Pause alt | entfernt | RMS im Schnitt):")
for r in report:
    print("  ", r)
