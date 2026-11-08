"""Rendert Short #01: Szenenbilder (frames_v6) + Sprachzeilen (vo/) -> MP4 1080x1920, 30 fps.
Timing kommt aus der Laenge jeder Sprachzeile. Fehlende Zeilen bekommen eine geschaetzte Dauer (Platzhalter-Stille).
Bewegung: kurzes sanftes Einblenden je Szene (kein Dauer-Zoom), leichte Kamerafahrt nur bei Szene 12 (Miura)."""
import os, glob
import numpy as np, av
from PIL import Image

FPS, W, H, SR = 30, 1080, 1920, 48000
PAD = 0.35                      # Atempause nach jeder Zeile
LINES = [  # (Szene, VO-Datei, Platzhalter-Text fuer Schaetzung)
    (1, "01_enzo", None), (2, "02_jason", None),
    (3, "03_jason", "Italy, 1948. Ferruccio Lamborghini gets rich building tractors from leftover war machines."),
    (4, "04_jason", "Rich enough to buy a Ferrari."), (5, "05_jason", None), (6, "06_mechanic", None),
    (7, "07_jason", "The story goes: it cost him ten lire. Ferrari charged a thousand."),
    (8, "08_ferruccio", None), (9, "09_enzo", None), (10, "10_jason", None),
    (11, "11_jason", "In 1963, Ferruccio founded his own car company."),
    (12, "12_jason", None), (13, "13_jason", None)]

def load_audio(path):
    c = av.open(path)
    rs = av.AudioResampler(format="flt", layout="mono", rate=SR)
    chunks = [f.to_ndarray().ravel() for fr in c.decode(audio=0) for f in rs.resample(fr)]
    return np.concatenate(chunks).astype(np.float32)

segs, missing = [], []
for scene, name, est in LINES:
    p = f"vo/{name}.mp3"
    if os.path.exists(p):
        a = load_audio(p)
    else:
        missing.append(name)
        a = np.zeros(int(SR * len(est.split()) / 2.6), np.float32)
    extra = 0.6 if scene == 10 else PAD          # "Big mistake." -> laengere Stille danach
    a = np.concatenate([a, np.zeros(int(SR * extra), np.float32)])
    segs.append((scene, a))

audio = np.concatenate([a for _, a in segs])
total = len(audio) / SR
print(f"Laenge {total:.1f} s, fehlende Zeilen: {missing}")

frames = {i: Image.open(f"frames_v6/s{i:02d}.png").convert("RGB") for i in range(1, 14)}

out = av.open("ARC_Short01_Lamborghini_preview.mp4", "w")
vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"
vs.options = {"crf": "18", "preset": "medium"}
ast = out.add_stream("aac", rate=SR); ast.layout = "mono"

t0 = 0.0
for scene, a in segs:
    dur = len(a) / SR
    n = max(1, int(round(dur * FPS)))
    base = frames[scene]
    for k in range(n):
        t = k / FPS
        if scene == 12:      # langsame Kamerafahrt auf den Miura (einzige Bewegung dieser Art)
            s = 1.0 + 0.05 * (t / dur)
            img = base.resize((int(W * s), int(H * s)), Image.BILINEAR)
            x, y = (img.width - W) // 2, (img.height - H) // 2
            img = img.crop((x, y, x + W, y + H))
        else:
            img = base
        if t < 0.12 and scene != 1:    # weicher Schnitt: 4 Frames Ueberblendung von Schwarz
            img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, min(1.0, 0.35 + t / 0.12 * 0.65))
        frame = av.VideoFrame.from_image(img)
        for pkt in vs.encode(frame):
            out.mux(pkt)
    t0 += dur

for pkt in vs.encode():
    out.mux(pkt)
# Audio in Bloecken schreiben
step = 1024
for i in range(0, len(audio), step):
    chunk = audio[i:i + step]
    if len(chunk) < step:
        chunk = np.pad(chunk, (0, step - len(chunk)))
    af = av.AudioFrame.from_ndarray(chunk.reshape(1, -1), format="flt", layout="mono"); af.sample_rate = SR
    for pkt in ast.encode(af):
        out.mux(pkt)
for pkt in ast.encode():
    out.mux(pkt)
out.close()
print("ok")
