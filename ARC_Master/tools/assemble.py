"""ARC Assembler: setzt ein von Remotion gerendertes Bild-Sequenz-Ordner + eine Audiodatei
zu einem fertigen Short/Longform-Video zusammen, exakt in unseren Zielwerten.

Grund: Remotions eingebauter Video-Encoder braucht mehr RAM, als dieser PC frei hat
(5,8 GB gesamt, meist <1 GB frei). Bilder einzeln rendern funktioniert dagegen
zuverlässig (getestet: 90/90 Bilder ohne Fehler). Dieses Skript übernimmt den
letzten Schritt mit PyAV, das wir schon für short08.py etc. benutzen -- läuft
stabil mit wenig RAM, weil es Bild für Bild kodiert statt alles im Speicher zu halten.

Nutzung:
  python assemble.py BILDER_ORDNER AUDIO.mp3 AUSGABE.mp4 --fps 30

Zielwerte: 30 fps, libx264 crf 19, AAC 48 kHz mono (wie der Rest der ARC-Pipeline).
"""
import argparse, os, sys, glob
import av
import numpy as np
from PIL import Image


def main():
    p = argparse.ArgumentParser()
    p.add_argument("frames_dir")
    p.add_argument("audio", nargs="?", default=None)
    p.add_argument("out")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--crf", type=int, default=19)
    a = p.parse_args()

    files = sorted(glob.glob(os.path.join(a.frames_dir, "*.jpeg")) + glob.glob(os.path.join(a.frames_dir, "*.jpg")) + glob.glob(os.path.join(a.frames_dir, "*.png")))
    if not files:
        sys.exit(f"Keine Bilder in {a.frames_dir}")
    w, h = Image.open(files[0]).size
    print(f"{len(files)} Bilder, {w}x{h}, {a.fps} fps")

    out = av.open(a.out, mode="w")
    vstream = out.add_stream("libx264", rate=a.fps)
    vstream.width, vstream.height = w, h
    vstream.pix_fmt = "yuv420p"
    vstream.options = {"crf": str(a.crf), "preset": "veryfast"}

    astream = None
    if a.audio and os.path.exists(a.audio):
        ain = av.open(a.audio)
        astream = out.add_stream("aac", rate=48000)
        astream.layout = "mono"
        astream.bit_rate = 256000
        resampler = av.AudioResampler(format="fltp", layout="mono", rate=48000)
        for frame in ain.decode(audio=0):
            for rf in resampler.resample(frame):
                for packet in astream.encode(rf):
                    out.mux(packet)
        for packet in astream.encode(None):
            out.mux(packet)

    for i, fp in enumerate(files):
        img = Image.open(fp).convert("RGB")
        if img.size != (w, h):
            img = img.resize((w, h))
        frame = av.VideoFrame.from_ndarray(np.array(img), format="rgb24")
        frame.pts = i
        for packet in vstream.encode(frame):
            out.mux(packet)
        if i % 30 == 0:
            print(f"  {i}/{len(files)}")
    for packet in vstream.encode(None):
        out.mux(packet)
    out.close()
    print("Fertig:", a.out)


if __name__ == "__main__":
    main()
