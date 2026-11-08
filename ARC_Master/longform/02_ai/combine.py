"""Fuegt die Video-Teile (ohne Ton) verlustfrei zusammen und legt die komplette Tonspur (Stimme + SFX + Musik) darunter."""
import sys, av, numpy as np
import ai_v9 as A
parts = sys.argv[1:]; out = av.open("ARC_AI_v9.mp4", "w")
src0 = av.open(parts[0]); vs = out.add_stream_from_template(src0.streams.video[0]); src0.close()
ast = out.add_stream("aac", rate=A.SR); ast.layout = "mono"
off = 0
for p in parts:
    c = av.open(p); st = c.streams.video[0]; last = 0
    for pk in c.demux(st):
        if pk.dts is None: continue
        pk.pts += off; pk.dts += off; last = max(last, pk.pts + (pk.duration or 0)); pk.stream = vs; out.mux(pk)
    off = last; c.close()
audio = A.mix()
for i in range(0, len(audio), 1024):
    ch = audio[i:i + 1024]; ch = np.pad(ch, (0, 1024 - len(ch))) if len(ch) < 1024 else ch
    af = av.AudioFrame.from_ndarray(ch.reshape(1, -1).astype(np.float32), format="flt", layout="mono"); af.sample_rate = A.SR
    for p in ast.encode(af): out.mux(p)
for p in ast.encode(): out.mux(p)
out.close(); print("ok ARC_AI_v9.mp4", A.TOTAL)
