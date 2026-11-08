"""Short (9:16) aus Longform #02: die 25-Mio.-Deepfake-Story, an exakten Wortgrenzen gekuerzt.
Bild = Original-Szene zur Original-Wortzeit (synchron), oben Hook, unten grosse Wort-fuer-Wort-Untertitel."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
import numpy as np, av
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import ai_v9 as A
from ai_kit import BOLD, INK
import lib as SFXL, music_real

SR, FPS = 48000, 30; SW, SH = 1080, 1920
# (Block, (Startwort, n), (Endwort, n))
SEGS = [("B12", ("January", 1), ("Kong", 1)), ("B12", ("Leo", 2), ("finance", 1)), ("B12", ("A", 1), ("transaction", 1)),
        ("B12", ("He", 1), ("suspicious", 1)), ("B13", ("They", 1), ("voices", 1)), ("B15", ("So", 1), ("dollars", 1)),
        ("B16", ("Later", 1), ("meeting", 1)), ("B15", ("Be", 1), ("comments", 1))]
GAP = 0.22
def widx(bid, w, n):
    k = 0
    for i, (t, s, e) in enumerate(A.WORDS[bid]):
        if A._norm(t) == A._norm(w):
            k += 1
            if k == n: return i
    raise KeyError((bid, w, n))
# Timeline bauen
TL = []; t = 0.3
for bid, a, b in SEGS:
    i0, i1 = widx(bid, *a), widx(bid, *b); W_ = A.WORDS[bid]
    s0 = max(0.0, W_[i0][1] - 0.05); s1 = W_[i1][2] + 0.10
    TL.append(dict(bid=bid, t0=t, s0=s0, s1=s1, words=[(w, ws - s0 + t, we - s0 + t) for w, ws, we in W_[i0:i1 + 1]]))
    t += (s1 - s0) + GAP
END_CARD = 2.2; TOTAL = t + END_CARD
print(f"Short-Laenge {TOTAL:.1f}s")

def seg_at(gt):
    for sg in TL:
        if gt < sg["t0"] + (sg["s1"] - sg["s0"]) + GAP: return sg
    return None
F = lambda s: ImageFont.truetype(BOLD, s)
def scene(bid, lt):
    b = A.BEATS[A.IDX[bid]]; T = b["dur"] - b["pre"]; A.CUR["id"] = bid; A.CUR["shot0"] = 0.0
    f = Image.new("RGBA", (1920, 1080), (0, 0, 0, 255)); A.SCENES[bid](f, lt, T); return f
_bgcache = {}
def frame(gt):
    out = Image.new("RGB", (SW, SH), (10, 8, 18)); d = ImageDraw.Draw(out)
    sg = seg_at(gt)
    if sg is None:                                                   # Endkarte
        sg = TL[-1]; lt = A.VOFF + sg["s1"]; img = scene(sg["bid"], lt)
    else:
        lt = A.VOFF + sg["s0"] + max(0.0, gt - sg["t0"]); img = scene(sg["bid"], lt)
    # Bild 1:1 als grosser Ausschnitt (mittige 1080x1350-Flaeche, Szene auf Breite skaliert + Hintergrund unscharf)
    bgk = (sg["bid"], int(gt * 2))
    big = img.convert("RGB").resize((int(1920 * 1920 / 1080), 1920), Image.BILINEAR)
    bg = big.crop(((big.width - SW) // 2, 0, (big.width - SW) // 2 + SW, SH)).filter(ImageFilter.GaussianBlur(28))
    out.paste(Image.blend(bg, Image.new("RGB", (SW, SH), (8, 6, 14)), 0.55), (0, 0))
    fg = img.convert("RGB").resize((1440, 810), Image.LANCZOS).crop((180, 0, 1260, 810))
    y0 = 520; out.paste(fg, (0, y0)); d.rectangle([0, y0 - 4, SW, y0], fill=(255, 214, 60)); d.rectangle([0, y0 + fg.height, SW, y0 + fg.height + 4], fill=(255, 214, 60))
    # Hook oben
    d.text((SW // 2, 220), "ONLY ONE OF THEM", font=F(78), fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    d.text((SW // 2, 320), "WAS REAL", font=F(96), fill=(255, 70, 70), anchor="mm", stroke_width=9, stroke_fill=(0, 0, 0))
    d.text((SW // 2, 420), "True story · Hong Kong 2024", font=F(36), fill=(255, 214, 60), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    # Untertitel (3-Wort-Gruppen, aktuelles Wort gelb)
    if gt < TL[-1]["t0"] + (TL[-1]["s1"] - TL[-1]["s0"]) + 0.3:
        allw = [w for s in TL for w in s["words"]]
        cur = max([i for i, w in enumerate(allw) if w[1] <= gt] or [0])
        g0 = cur - cur % 3; grp = allw[g0:g0 + 3]
        if grp and gt <= grp[-1][2] + 0.6:
            words = [w[0] for w in grp]; f = F(84); sp = d.textlength(" ", font=f)
            widths = [d.textlength(w, font=f) for w in words]; x = SW / 2 - (sum(widths) + sp * (len(words) - 1)) / 2
            for k, w in enumerate(words):
                col = (255, 214, 60) if g0 + k == cur else (255, 255, 255)
                d.text((x, 1500), w, font=f, fill=col, anchor="lm", stroke_width=9, stroke_fill=(0, 0, 0)); x += widths[k] + sp
    else:
        k = min(1.0, (gt - (TOTAL - END_CARD)) / 0.3)
        d.text((SW // 2, 1480), "WOULD YOU HAVE", font=F(80), fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
        d.text((SW // 2, 1580), "SENT IT?", font=F(96), fill=(255, 214, 60), anchor="mm", stroke_width=9, stroke_fill=(0, 0, 0))
        d.text((SW // 2, 1700), "Full video on our channel", font=F(40), fill=(200, 220, 255), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    return out

def audio():
    n = int((TOTAL + 0.5) * SR); voice = np.zeros(n, np.float32); fx = np.zeros(n, np.float32)
    for sg in TL:
        a = A.VO[sg["bid"]][int(sg["s0"] * SR):int(sg["s1"] * SR)].copy(); fl = SR // 100; a[:fl] *= np.linspace(0, 1, fl); a[-fl:] *= np.linspace(1, 0, fl)
        i = int(sg["t0"] * SR); voice[i:i + len(a)] += a
        for tc, name, g in A.CUES.get(sg["bid"], []):
            tt = A.cue_time(sg["bid"], tc) - A.VOFF
            if sg["s0"] <= tt <= sg["s1"]: j = int((sg["t0"] + tt - sg["s0"]) * SR); x = SFXL.load(name)[:max(0, n - j)]; fx[j:j + len(x)] += x * g
    cs = np.concatenate([[0.0], np.cumsum(np.abs(voice), dtype=np.float64)]); idx = np.arange(n)
    lo, hi = np.clip(idx - 2400, 0, n), np.clip(idx + 2400, 0, n); vabs = ((cs[hi] - cs[lo]) / 4800).astype(np.float32)
    duck = 1 - 0.6 * np.clip(vabs / 0.05, 0, 1)
    mus = music_real.build(n, 0.0, 0.024) * duck
    out = voice * 1.05 + fx + mus; m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)]

if __name__ == "__main__":
    if "--still" in sys.argv:
        for k, tt in enumerate((1.0, 12.0, 25.0, TOTAL - 1.0)): frame(tt).save(f"check/short_{k}.jpg", quality=85)
        print("ok"); sys.exit()
    out = av.open("ARC_AI_short_deepfake.mp4", "w"); vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = SW, SH, "yuv420p"; vs.options = {"crf": "19", "preset": "medium"}
    ast = out.add_stream("aac", rate=SR); ast.layout = "mono"
    for k in range(int(TOTAL * FPS)):
        for p in vs.encode(av.VideoFrame.from_image(frame(k / FPS))): out.mux(p)
    for p in vs.encode(): out.mux(p)
    au = audio()
    for i in range(0, len(au), 1024):
        ch = au[i:i + 1024]; ch = np.pad(ch, (0, 1024 - len(ch))) if len(ch) < 1024 else ch
        af = av.AudioFrame.from_ndarray(ch.reshape(1, -1).astype(np.float32), format="flt", layout="mono"); af.sample_rate = SR
        for p in ast.encode(af): out.mux(p)
    for p in ast.encode(): out.mux(p)
    out.close(); print("ok short", TOTAL)
