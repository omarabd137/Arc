"""ARC QA-Tor (technisch): python qa_video.py VIDEO.mp4 [KONTAKTBOGEN.png]
Prüft: Länge <= 60 s, 1080x1920 @30, Lautheit -14 LUFS, True Peak < -1 dBTP, Bett-Verhältnis,
Stillstand (keine Bildänderung > 3 s), Loop-Übergang (letzter vs. erster Frame). Druckt BESTANDEN/FEHLER je Punkt.
"""
import sys
import av
import numpy as np
from PIL import Image

path = sys.argv[1]
sheet_out = sys.argv[2] if len(sys.argv) > 2 else None

c = av.open(path)
vs = c.streams.video[0]
fps = float(vs.average_rate)
W, H = vs.codec_context.width, vs.codec_context.height

small = []
sheet_frames = []
next_sheet = 0.0
for fr in c.decode(video=0):
    t = float(fr.pts * fr.time_base)
    img = fr.to_image()
    small.append(np.asarray(img.convert("L").resize((54, 96)), dtype=np.float32))
    if t >= next_sheet:
        sheet_frames.append((t, img.resize((180, 320))))
        next_sheet += 1.0
dur = len(small) / fps

# Audio
c.close()
c = av.open(path)
res = av.AudioResampler(format="flt", layout="mono", rate=48000)
chunks = []
for fr in c.decode(audio=0):
    for r in res.resample(fr):
        chunks.append(r.to_ndarray().reshape(-1))
audio = np.concatenate(chunks).astype(np.float64) if chunks else np.zeros(1)

import pyloudnorm as pyln
from scipy.signal import resample_poly

lufs = pyln.Meter(48000).integrated_loudness(audio)
tp = 20 * np.log10(np.abs(resample_poly(audio, 4, 1)).max() + 1e-12)
frm = 2400
rms = np.sqrt(np.mean(audio[: len(audio) // frm * frm].reshape(-1, frm) ** 2, axis=1))
ratio = np.percentile(rms, 10) / np.percentile(rms, 50)

# Stillstand: mittlere Pixeländerung pro Frame
diffs = np.array([np.abs(small[i] - small[i - 1]).mean() for i in range(1, len(small))])
moving = diffs > 0.6
longest = 0
run = 0
worst_at = 0
for i, m in enumerate(moving):
    run = 0 if m else run + 1
    if run > longest:
        longest, worst_at = run, i
still_s = longest / fps
loop_diff = float(np.abs(small[-1] - small[0]).mean())

def row(name, ok, val):
    print(f"{'BESTANDEN' if ok else 'FEHLER   '} | {name:34s} | {val}")

print(f"Datei: {path}")
row("Länge <= 60 s (Ziel 35-45)", dur <= 60, f"{dur:.2f} s")
row("Format 1080x1920 @ 30 fps", (W, H) == (1080, 1920) and abs(fps - 30) < 0.01, f"{W}x{H} @ {fps:.2f}")
row("Lautheit -14 LUFS (+-1)", abs(lufs + 14) <= 1.0, f"{lufs:.1f} LUFS")
row("True Peak < -1 dBTP", tp < -1.0, f"{tp:.2f} dBTP")
row("Bett-Verhältnis 0.12-0.27", 0.12 <= ratio <= 0.27, f"{ratio:.3f}")
row("Kein Stillstand > 3 s", still_s <= 3.0, f"längster: {still_s:.2f} s bei {worst_at / fps:.1f} s")
row("Loop: letzter ~ erster Frame", loop_diff < 25, f"Abweichung {loop_diff:.1f} (0 = identisch)")
print(f"Ø Bildänderung/Frame {diffs.mean():.2f} | Anteil Frames mit Bewegung {moving.mean() * 100:.0f} %")

if sheet_out:
    cols = 9
    rows = int(np.ceil(len(sheet_frames) / cols))
    sheet = Image.new("RGB", (180 * cols, 320 * rows), "black")
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for k, (t, im) in enumerate(sheet_frames):
        x, y = (k % cols) * 180, (k // cols) * 320
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 46, y + 18], fill="black")
        d.text((x + 4, y + 3), f"{t:.0f}s", fill="white")
    sheet.save(sheet_out)
    print(f"Kontaktbogen: {sheet_out}")
