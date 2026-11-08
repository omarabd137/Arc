"""ARC Short #01 v7 – Rache-Story nach dem Zack-D.-Films-Prinzip:
jeder Halbsatz = eigenes Bild, das genau zeigt, was gesagt wird; Untertitel 2-3 Woerter;
Figuren laufen, Autos fahren ein (Raeder drehen), Muender bewegen sich, dichte SFX + Spannungsmusik.
Aufruf aus shorts/01_lamborghini:  python v7/short_v7.py [--stills]"""
import sys, os, math, random
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.join(os.getcwd(), "v7"))
import numpy as np, av
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from crayon_kit import S, sh, shape, stroke, ellipse_pts, W, H, SS, INK, ENZO, FERRUCCIO
import places
from crayon3 import figure, sticky, LIMB
from crayon2 import bust, hand_text, clutch_drawing, price_tag, GREY, ORANGE
from scenes_v6 import MECHANIC, cap, outside_workshop, factory_1963, motor_show
import sfx

FPS, SR = 30, 48000
CAP_FONT = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 74)
YELLOW = (255, 214, 70)

# ---------------- Ton: Erzaehler-Saetze aus der Sammelaufnahme ----------------
def load(path):
    c = av.open(path); rs = av.AudioResampler(format="flt", layout="mono", rate=SR)
    return np.concatenate([f.to_ndarray().ravel() for fr in c.decode(audio=0) for f in rs.resample(fr)]).astype(np.float32)

NARR = np.load("v7/vo/narr_all.npy")
NCUT = [(0.0, 4.30), (4.96, 8.68), (9.02, 10.88), (11.44, 12.90), (13.38, 15.32), (15.84, 19.30), (19.68, 22.70),
        (23.26, 24.94), (25.20, 27.24), (27.52, 31.58), (32.06, 36.04)]
def narr(i):
    s, e = NCUT[i]; a = NARR[int(s * SR):int(e * SR)].copy()
    f = int(0.02 * SR); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    return a

# (Clip-ID, Audio, Untertitel, Dialog?, Pause danach)
CLIPS = [
    ("N1", narr(0), "This man built a supercar... just to get revenge on Ferrari.", False, 0.25),
    ("N2", narr(1), "You see, Ferruccio Lamborghini got rich building tractors.", False, 0.2),
    ("N3", narr(2), "So he bought himself a Ferrari.", False, 0.2),
    ("N4", narr(3), "But the clutch kept breaking.", False, 0.25),
    ("N5", narr(4), "So his mechanics opened it up...", False, 0.15),
    ("M",  load("vo/06_mechanic.mp3"), "Boss... it's the same clutch as our tractors!", True, 0.25),
    ("N6", narr(5), "Ferrari was charging him a hundred times more for it.", False, 0.3),
    ("N7", narr(6), "So he went to complain to Enzo Ferrari himself.", False, 0.2),
    ("E",  load("vo/01_enzo.mp3"), "You may be able to drive a tractor... but you'll never handle a Ferrari.", True, 0.35),
    ("N8", narr(7), "Ferruccio was furious.", False, 0.45),
    ("N9", narr(8), "So he built his own car company...", False, 0.15),
    ("N10", narr(9), "and three years later, his Lamborghini Miura stunned the world.", False, 0.35),
    ("N11", narr(10), "And it all started... because Ferrari laughed at a tractor maker.", False, 0.9),
]
TL, t0 = [], 0.25
for cid, a, txt, dia, gap in CLIPS:
    TL.append(dict(id=cid, a=a, txt=txt, dia=dia, t0=t0, dur=len(a) / SR, end=t0 + len(a) / SR + gap))
    t0 = TL[-1]["end"]
TOTAL = t0

def amp_at(clip, lt):
    i = int(lt * SR); a = clip["a"][max(0, i - 800):i + 800]
    return float(np.sqrt(np.mean(a ** 2))) if len(a) else 0.0

# ---------------- Untertitel: 2-3 Woerter, zeitlich ueber den Satz verteilt ----------------
def chunks(clip):
    words = clip["txt"].split(); out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w[-1] in ",.!?" or (len(cur) == 2 and len(" ".join(cur)) > 14):
            out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    tot = sum(len(c) + 3 for c in out); t, res = 0.0, []
    for c in out:
        d = (len(c) + 3) / tot * clip["dur"]; res.append((t, t + d, c)); t += d
    return res
for c in TL: c["chunks"] = chunks(c)

_capcache = {}
def caption(text, color):
    key = (text, color)
    if key not in _capcache:
        d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
        tw = d0.textlength(text, font=CAP_FONT)
        im = Image.new("RGBA", (int(tw) + 40, 120), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20, 10), text, font=CAP_FONT, fill=color + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
        _capcache[key] = im
    return _capcache[key]

# ---------------- Sprites (einmal in 2x zeichnen, dann verkleinert wiederverwenden) ----------------
_spr = {}
def sprite(key, fn):
    if key not in _spr:
        c = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); fn(c)
        bb = c.getbbox() or (0, 0, 2, 2)
        im = c.crop(bb).resize((max(1, (bb[2] - bb[0]) // SS), max(1, (bb[3] - bb[1]) // SS)), Image.LANCZOS)
        _spr[key] = (im, bb[0] // SS, bb[1] // SS)
    return _spr[key]

def put(frame, spr, dx=0, dy=0):
    im, x, y = spr; frame.alpha_composite(im, (int(x + dx), int(y + dy))) if frame.mode == "RGBA" else frame.paste(im, (int(x + dx), int(y + dy)), im)

def bg(key, fn):
    if key not in _spr:
        im = fn(); im = im.resize((W, H), Image.LANCZOS) if im.size[0] > W else im
        _spr[key] = im.convert("RGB")
    return _spr[key]

# ---------------- Figuren mit Laufzyklus ----------------
def walker(p, R, face, phase, mouth="line", brow=0.0, arms=("down", "down"), seed=1, cx=540, base=1500):
    def fn(c):
        d = ImageDraw.Draw(c, "RGBA")
        leg, tor_w = R * 1.25, R * 1.05 * p["big"]
        hip = base - leg
        d.ellipse(S(cx - R * 0.9, base - 10, cx + R * 0.9, base + 10), fill=(0, 0, 0, 55))
        for sx in (-1, 1):
            ph = 2 * math.pi * ((phase or 0) + (0.5 if sx > 0 else 0))
            x = cx + sx * tor_w * 0.28
            fx = x + (math.sin(ph) * R * 0.38 if phase is not None else sx * 4)
            fy = base - (max(0, math.cos(ph)) * R * 0.1 if phase is not None else 0)
            stroke(d, [(x, hip - 10), (fx, fy)], lw=LIMB)
            stroke(d, [(fx, fy), (fx + face * 22, fy)], lw=LIMB)
        figure(c, cx, base, R, p, face=face, mouth=mouth, brow=brow, arms=arms, seed=seed, seated=True)
        if p is MECHANIC:
            cap(c, cx, hip - R * 1.35 - R * 0.78, R, face)
    return fn

def fig(frame, p, x, base, R, face, walking=False, lt=0.0, mouth="line", brow=0.0, arms=("down", "down"), seed=1):
    ph = (round((lt * 1.9) % 1 * 8) % 8) / 8 if walking else None
    key = ("fig", id(p), R, face, ph, mouth, brow, arms, seed, base)
    spr = sprite(key, walker(p, R, face, ph, mouth, brow, arms, seed, 540, base))
    bob = -abs(math.sin(2 * math.pi * ph)) * R * 0.06 if walking else 0
    put(frame, spr, x - 540, bob)

def bust_s(frame, p, R, face, mouth, brow=0.0, eyes="open", dx=0, dy=0, seed=1, hy=980, cx=540):
    def fn(c):
        bust(c, cx, hy, R, p, face=face, eyes=eyes, mouth=mouth, brow=brow, seed=seed)
        if p is MECHANIC: cap(c, cx, hy, R, face)
    put(frame, sprite(("bust", id(p), R, face, mouth, brow, eyes, seed, hy, cx), fn), dx, dy)

# ---------------- Autos (Seitenprofil, eigene Zeichnung) ----------------
def smooth(pts, n=6):
    out = []; L = len(pts)
    for i in range(L):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % L], pts[(i + 2) % L]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out

CARS = {
    # Ferrari 250 GT (1950er/60er): lange Haube, runde Scheinwerfer, Fastback-Kabine
    "ferrari": dict(color=(198, 28, 38), wheels=(0.19, 0.80), r=0.085,
        body=[(0.0, 0.07), (0.005, 0.16), (0.05, 0.205), (0.16, 0.215), (0.27, 0.24), (0.36, 0.315), (0.45, 0.335), (0.54, 0.325),
              (0.63, 0.25), (0.78, 0.22), (0.92, 0.195), (0.985, 0.16), (1.0, 0.11), (0.985, 0.065), (0.5, 0.06)],
        win=[(0.365, 0.245), (0.42, 0.305), (0.535, 0.305), (0.605, 0.25)], light=(0.968, 0.165)),
    # Lamborghini Miura (1966): flach, Mittelmotor, Lamellen hinten, "Wimpern"-Scheinwerfer
    "miura": dict(color=(247, 188, 26), wheels=(0.2, 0.79), r=0.078,
        body=[(0.0, 0.06), (0.004, 0.15), (0.06, 0.172), (0.2, 0.188), (0.33, 0.222), (0.44, 0.238), (0.52, 0.232), (0.66, 0.165),
              (0.84, 0.138), (0.955, 0.118), (1.0, 0.085), (0.99, 0.05), (0.5, 0.05)],
        win=[(0.435, 0.172), (0.47, 0.224), (0.53, 0.222), (0.635, 0.164)], light=(0.845, 0.142)),
}

def car_fn(kind, w, face, ang, x0=0, y0=1500):
    C = CARS[kind]
    def X(px): return x0 + (px if face == 1 else 1 - px) * w
    def Y(py): return y0 - py * w
    def fn(c):
        d = ImageDraw.Draw(c, "RGBA")
        d.ellipse(S(x0 - 10, y0 - 16, x0 + w + 10, y0 + 14), fill=(0, 0, 0, 70))
        for wx in C["wheels"]:      # dunkle Radkaesten
            shape(d, ellipse_pts(X(wx), Y(C["r"]), C["r"] * w * 1.12, C["r"] * w * 1.12), (28, 26, 30), 700, lw=3)
        body = smooth([(X(px), Y(py)) for px, py in C["body"]])
        shape(d, body, C["color"], 710, lw=5)
        # Cel-Schatten nur innerhalb der Karosserie (untere Haelfte), dann Kontur neu ziehen
        thr = Y(0.13 if kind == "ferrari" else 0.105)
        m = Image.new("L", c.size, 0); ImageDraw.Draw(m).polygon([(x * SS, y * SS) for x, y in body], fill=255)
        band = Image.new("L", c.size, 0); ImageDraw.Draw(band).rectangle([0, int(thr * SS), c.size[0], c.size[1]], fill=150)
        from PIL import ImageChops
        c.paste(Image.new("RGB", c.size, sh(C["color"], 0.72)), (0, 0), ImageChops.multiply(m, band))
        d = ImageDraw.Draw(c, "RGBA")
        stroke(d, body + [body[0]], lw=5)
        stroke(d, [(X(0.08), Y(0.2 if kind == "ferrari" else 0.176)), (X(0.95), Y(0.18 if kind == "ferrari" else 0.122))], lw=4, color=(255, 255, 255, 120))
        shape(d, smooth([(X(px), Y(py)) for px, py in C["win"]], 4), (150, 196, 226), 720, lw=4)
        stroke(d, [(X(0.4), Y(0.29 if kind == "ferrari" else 0.21)), (X(0.43), Y(0.255 if kind == "ferrari" else 0.18))], lw=6, color=(255, 255, 255, 170))
        if kind == "ferrari":
            stroke(d, [(X(0.47), Y(0.3)), (X(0.47), Y(0.09))], lw=3, color=sh(C["color"], 0.6))
            stroke(d, [(X(0.6), Y(0.25)), (X(0.6), Y(0.09))], lw=3, color=sh(C["color"], 0.6))
            stroke(d, [(X(0.5), Y(0.2)), (X(0.54), Y(0.2))], lw=5, color=(220, 220, 226))
            for bx in ((0.0, 0.06), (0.93, 1.0)):
                stroke(d, [(X(bx[0]), Y(0.095)), (X(bx[1]), Y(0.095))], lw=7, color=(220, 220, 228))
        else:
            for k in range(6):          # Lamellen ueber dem Motor
                lx = 0.22 + k * 0.03
                stroke(d, [(X(lx), Y(0.2 + k * 0.006)), (X(lx + 0.02), Y(0.215 + k * 0.006))], lw=4, color=sh(C["color"], 0.55))
            shape(d, [(X(0.33), Y(0.12)), (X(0.41), Y(0.12)), (X(0.39), Y(0.16)), (X(0.35), Y(0.16))], (40, 36, 34), 730, lw=3)
            stroke(d, [(X(0.5), Y(0.2)), (X(0.5), Y(0.07))], lw=3, color=sh(C["color"], 0.6))
        lx, ly = C["light"]
        shape(d, ellipse_pts(X(lx), Y(ly), w * 0.02, w * 0.017), (252, 250, 230), 740, lw=3)
        if kind == "miura":
            for k in range(4):
                a = math.radians(200 + k * 25) if face == 1 else math.radians(-20 - k * 25)
                stroke(d, [(X(lx) + math.cos(a) * w * 0.022, Y(ly) - abs(math.sin(a)) * w * 0.019), (X(lx) + math.cos(a) * w * 0.034, Y(ly) - abs(math.sin(a)) * w * 0.03)], lw=3)
        for wx in C["wheels"]:
            cx, cy, r = X(wx), Y(C["r"]), C["r"] * w
            shape(d, ellipse_pts(cx, cy, r * 1.13, r * 1.13, 60, 180, 360) + [(cx + r * 1.13, cy + r * 0.2), (cx - r * 1.13, cy + r * 0.2)], (26, 24, 28), 749, lw=4)
            shape(d, ellipse_pts(cx, cy, r, r), (34, 32, 36), 750)
            shape(d, ellipse_pts(cx, cy, r * 0.62, r * 0.62), (196, 196, 204), 751, lw=4)
            for k in range(5):          # Speichen (drehen sich)
                a = ang + k * 2 * math.pi / 5
                stroke(d, [(cx, cy), (cx + math.cos(a) * r * 0.58, cy + math.sin(a) * r * 0.58)], lw=5, color=(120, 120, 130))
            shape(d, ellipse_pts(cx, cy, r * 0.16, r * 0.16), (90, 90, 98), 752, lw=3)
    return fn

def car(frame, kind, x, base, w, face, roll=0.0, dy=0):
    """roll = zurueckgelegte Strecke in px -> Raddrehung."""
    r = CARS[kind]["r"] * w
    step = int(((roll / r) % (2 * math.pi / 5)) / (2 * math.pi / 5) * 6) % 6
    ang = step * (2 * math.pi / 5) / 6 * (1 if face == 1 else -1)
    spr = sprite(("car", kind, w, face, step, base), car_fn(kind, w, face, ang, 0, base))
    put(frame, spr, x, dy)

def tractor_spr(frame, x, base, w, jig=0):
    put(frame, sprite(("tractor", w, base), lambda c: places.cartoon_tractor(ImageDraw.Draw(c, "RGBA"), 0, base, w)), x, jig)

def note(frame, lines, cx, cy, angle=-4, w=420, pop=1.0):
    def fn(c): sticky(c, cx, cy, lines, angle=angle, w=w)
    spr = sprite(("note", tuple(lines), cx, cy, angle, w), fn)
    if pop >= 1: put(frame, spr)
    elif pop > 0:
        im, x, y = spr; s = 0.6 + 0.4 * pop
        im2 = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))))
        frame.paste(im2, (int(x + (im.width - im2.width) / 2), int(y + (im.height - im2.height) / 2)), im2)

def clutch_spr(frame, cx, cy, r, seed=10, dx=0, dy=0):
    put(frame, sprite(("clutch", cx, cy, r, seed), lambda c: clutch_drawing(ImageDraw.Draw(c, "RGBA"), cx, cy, r, seed)), dx, dy)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# ---------------- Hintergruende ----------------
def night_bg():
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(int(24 + 30 * k), int(28 + 26 * k), int(52 + 30 * k)))
    d.rectangle([0, 1500, W, H], fill=(46, 46, 56)); d.line([(0, 1500), (W, 1500)], fill=INK, width=5)
    for i in range(6):
        x = 80 + i * 180; d.ellipse([x - 90, 300, x + 90, 1500], fill=(60, 64, 96))
    return img.filter(ImageFilter.GaussianBlur(2))

def red_bg(k=1.0):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        f = 1 - abs(y / H - 0.45) * 1.3
        d.line([(0, y), (W, y)], fill=(int((60 + 110 * f) * k), int(12 * f), int(16 * f)))
    return img

def office_bg(): return places.ferrari_office()[0]
def blurred(fn, r=7): return lambda: fn().filter(ImageFilter.GaussianBlur(r * SS))

def desk_spr(frame):
    put(frame, sprite(("desk",), lambda c: places.desk(c, 520, 1100, 1420, 1920)))

def grey(): return Image.new("RGB", (W, H), GREY)

def crowd_spr(frame, t):
    def fn(c):
        d = ImageDraw.Draw(c, "RGBA")
        for i in range(10):
            x = 20 + i * 118
            shape(d, ellipse_pts(x, 1850, 100, 100), [(120, 50, 50), (60, 80, 130), (90, 90, 96), (70, 110, 80)][i % 4], 20 + i)
            shape(d, ellipse_pts(x, 1690 + (i % 2) * 40, 72, 72), [(60, 44, 36), (200, 170, 90), (40, 34, 30), (110, 70, 44)][i % 4], 10 + i)
    put(frame, sprite(("crowd",), fn), 0, math.sin(t * 9) * 4)

def flashes(frame, t, seed):
    o = Image.new("RGBA", frame.size, (0, 0, 0, 0)); d = ImageDraw.Draw(o); rnd = random.Random(int(t * 7) + seed)
    if rnd.random() < 0.55:
        x, y = rnd.randint(80, 1000), rnd.randint(500, 1100)
        for k in range(4, 0, -1): d.ellipse([x - 16 * k, y - 16 * k, x + 16 * k, y + 16 * k], fill=(255, 255, 255, 40))
        d.polygon([(x, y - 44), (x + 9, y - 9), (x + 44, y), (x + 9, y + 9), (x, y + 44), (x - 9, y + 9), (x - 44, y), (x - 9, y - 9)], fill=(255, 255, 255, 230))
    frame.alpha_composite(o)

def banknotes(frame, t):
    o = Image.new("RGBA", frame.size, (0, 0, 0, 0)); d = ImageDraw.Draw(o); rnd = random.Random(3)
    for i in range(16):
        x = rnd.randint(40, 1040); sp = rnd.uniform(500, 900); y = -120 + ((t * sp + rnd.randint(0, 1600)) % 1700)
        a = math.sin(t * 4 + i) * 0.5; cw, chh = 110, 56
        pts = [(x + math.cos(a) * dx - math.sin(a) * dy, y + math.sin(a) * dx + math.cos(a) * dy) for dx, dy in ((-cw / 2, -chh / 2), (cw / 2, -chh / 2), (cw / 2, chh / 2), (-cw / 2, chh / 2))]
        d.polygon(pts, fill=(196, 170, 120, 255), outline=INK); d.ellipse([x - 12, y - 12, x + 12, y + 12], outline=(120, 96, 60), width=3)
    frame.alpha_composite(o)

def smoke_puffs(frame, t, cx, cy):
    o = Image.new("RGBA", frame.size, (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    for i in range(7):
        k = (t * 0.9 + i / 7) % 1; r = 40 + 140 * k
        x, y = cx + math.sin(i * 2.1) * 70 + k * 60, cy - k * 520
        d.ellipse([x - r, y - r * 0.85, x + r, y + r * 0.85], fill=(200, 200, 206, int(220 * (1 - k))), outline=(30, 26, 30, int(200 * (1 - k))), width=4)
    frame.alpha_composite(o)

def symbol(frame, text, cx, cy, size, color, scale=1.0):
    f = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", int(size * scale))
    d = ImageDraw.Draw(frame); tw = d.textlength(text, font=f)
    d.text((cx - tw / 2, cy - size * scale / 2), text, font=f, fill=color, stroke_width=8, stroke_fill=INK)

# ---------------- Einstellungen ----------------
# Jede Funktion bekommt (frame, lt, T, amp). Motive gross, Vordergrund-Figur + Auto dahinter (Tiefe).
def sh_hook1(f, lt, T, amp):
    x = 1150 - 1090 * ease(lt / 1.1); car(f, "miura", x, 1480, 1000, -1, roll=1150 - x)
    fig(f, FERRUCCIO, 250, 1800, 175, 1, mouth="smile", arms=("hip", "hip"), seed=3)
def sh_hook2(f, lt, T, amp):
    car(f, "ferrari", 60, 1250, 960, 1)
    bust_s(f, FERRUCCIO, 340, 1, "frown", brow=0.16, hy=1080, seed=11, dx=math.sin(lt * 70) * 5 * max(0, 1 - lt / 0.4))
def sh_rich1(f, lt, T, amp):
    x = -820 + 1050 * ease(lt / 1.3); tractor_spr(f, x, 1560, 820, jig=math.sin(lt * 40) * 3)
    fig(f, FERRUCCIO, 170, 1800, 160, 1, mouth="smile", arms=("hip", "rest"), seed=3)
    note(f, ["FERRUCCIO LAMBORGHINI"], 540, 380, w=760, pop=lt / 0.25)
def sh_rich2(f, lt, T, amp):
    for i, x in enumerate((-40, 360, 760)): tractor_spr(f, x, 1260 - (i % 2) * 30, 400)
    fig(f, FERRUCCIO, 540, 1850, 210, 1, mouth="smile", arms=("hip", "hip"), seed=3)
    banknotes(f, lt)
def sh_buy(f, lt, T, amp):
    x = 1150 - 1000 * ease(lt / 1.2); car(f, "ferrari", x, 1540, 900, -1, roll=1150 - x)
    wx = -150 + 380 * min(1, lt / 1.4)
    fig(f, FERRUCCIO, wx, 1800, 165, 1, walking=lt < 1.4, lt=lt, mouth="smile", seed=4)
def sh_break(f, lt, T, amp):
    car(f, "ferrari", 30 + math.sin(lt * 50) * 5, 1540, 900, -1)
    smoke_puffs(f, lt, 230, 1400)
    fig(f, FERRUCCIO, 840, 1800, 165, -1, mouth="frown", brow=0.12, arms=("down", "hip"), seed=5)
def sh_mech(f, lt, T, amp):
    car(f, "ferrari", -160, 1540, 900, 1)
    wx = 1250 - 430 * min(1, lt / 1.2)
    fig(f, MECHANIC, wx, 1800, 160, -1, walking=lt < 1.2, lt=lt, seed=6)
def sh_mech_talk(f, lt, T, amp):
    bust_s(f, MECHANIC, 320, 1, "open" if amp > 0.04 else "frown", brow=-0.08, hy=1040, cx=440, seed=6)
    clutch_spr(f, 850, 1250, 170, 10, dy=math.sin(lt * 6) * 6)
def sh_same(f, lt, T, amp):
    tractor_spr(f, 20, 860, 460); car(f, "ferrari", 560, 800, 500, 1)
    clutch_spr(f, 260, 1100, 190, 11); clutch_spr(f, 820, 1100, 190, 12)
    symbol(f, "=", 540, 1090, 170, ORANGE, scale=0.6 + 0.4 * ease(lt / 0.3))
def sh_price(f, lt, T, amp):
    tractor_spr(f, 20, 680, 440); car(f, "ferrari", 560, 620, 500, 1)
    def tag(c, x, txt, col, s): price_tag(ImageDraw.Draw(c, "RGBA"), x, 850, txt, col, s, size=90)
    put(f, sprite(("tag1",), lambda c: tag(c, 250, "10 lire", (40, 110, 60), 30)))
    if lt > 0.5: put(f, sprite(("tag2",), lambda c: tag(c, 800, "1,000 lire", (196, 40, 40), 31)))
    if lt > T * 0.55: symbol(f, "100x", 540, 1110, 220, ORANGE, scale=1.6 - 0.6 * ease((lt - T * 0.55) / 0.2))
def sh_walk_enzo(f, lt, T, amp):
    put(f, sprite(("enzo_seat",), lambda c: figure(c, 800, 1500, 135, ENZO, face=-1, mouth="smirk", arms=("desk", "desk"), seed=7, seated=True)))
    desk_spr(f)
    wx = -150 + 450 * min(1, lt / 1.5)
    fig(f, FERRUCCIO, wx, 1860, 165, 1, walking=lt < 1.5, lt=lt, mouth="frown", brow=0.08, seed=9)
    if lt > T * 0.5: note(f, ["ENZO FERRARI"], 760, 520, angle=4, w=520, pop=(lt - T * 0.5) / 0.25)
def sh_enzo_talk(f, lt, T, amp):
    big = lt >= T * 0.5
    bust_s(f, ENZO, 390 if big else 330, -1, "talk" if amp > 0.035 else "smirk", brow=-0.05, hy=1060 if big else 1000, seed=17)
def sh_furious(f, lt, T, amp):
    s = 5 if lt < 0.6 else 1.5
    bust_s(f, FERRUCCIO, 380, 1, "frown", brow=0.2, hy=1020, seed=21, dx=math.sin(lt * 70) * s, dy=math.cos(lt * 60) * s)
def sh_factory(f, lt, T, amp):
    wx = -150 + 400 * min(1, lt / 1.3)
    fig(f, FERRUCCIO, wx, 1820, 175, 1, walking=lt < 1.3, lt=lt, mouth="smile", arms=("hip", "point") if lt >= 1.3 else ("down", "down"), seed=23)
    note(f, ["1963"], 760, 330, angle=-4, w=300, pop=lt / 0.25)
def sh_show1(f, lt, T, amp):
    x = -1000 + 1050 * ease(lt / 1.2); car(f, "miura", x, 1440, 1000, 1, roll=x + 1000)
    flashes(f, lt, 1); note(f, ["1966", "LAMBORGHINI MIURA"], 540, 320, angle=3, w=640, pop=(lt - 0.3) / 0.25)
def sh_show2(f, lt, T, amp):
    car(f, "miura", -60, 1330, 1200, 1)
    crowd_spr(f, lt); flashes(f, lt, 2); flashes(f, lt + 0.37, 3)
def sh_laugh(f, lt, T, amp):
    bust_s(f, ENZO, 360, -1, "open", eyes="happy", brow=-0.04, hy=1000, seed=17, dy=-abs(math.sin(lt * 9)) * 18)
def sh_final(f, lt, T, amp):
    car(f, "miura", 60, 900, 960, 1)
    tractor_spr(f, 0, 1560, 520)
    fig(f, FERRUCCIO, 800, 1820, 165, -1, mouth="smile", arms=("hip", "hip"), seed=33)

BGS = {"night": night_bg, "redd": lambda: red_bg(0.8), "work": lambda: places.workshop_1948()[0],
       "out": lambda: outside_workshop()[0], "grey": grey, "office": office_bg, "office_b": blurred(office_bg),
       "work_b": blurred(lambda: places.workshop_1948()[0]), "factory": lambda: factory_1963()[0], "show": motor_show}

# Clip-ID -> [(Anteil Start, Hintergrund, Einstellung)]
SHOTS = {
    "N1": [(0, "night", sh_hook1), (0.45, "redd", sh_hook2)],
    "N2": [(0, "work", sh_rich1), (0.55, "work", sh_rich2)],
    "N3": [(0, "out", sh_buy)],
    "N4": [(0, "out", sh_break)],
    "N5": [(0, "work", sh_mech)],
    "M":  [(0, "work_b", sh_mech_talk), (0.48, "grey", sh_same)],
    "N6": [(0, "grey", sh_price)],
    "N7": [(0, "office", sh_walk_enzo)],
    "E":  [(0, "office_b", sh_enzo_talk)],
    "N8": [(0, "redd", sh_furious)],
    "N9": [(0, "factory", sh_factory)],
    "N10": [(0, "show", sh_show1), (0.42, "show", sh_show2)],
    "N11": [(0, "office_b", sh_laugh), (0.5, "grey", sh_final)],
}

def frame_at(gt):
    ci = max(i for i, c in enumerate(TL) if c["t0"] <= gt) if gt >= TL[0]["t0"] else 0
    c = TL[ci]; span = c["end"] - c["t0"]; lt_clip = gt - c["t0"]
    shots = SHOTS[c["id"]]
    si = max(i for i, s in enumerate(shots) if s[0] * c["dur"] <= max(0, lt_clip))
    s0 = shots[si][0] * c["dur"]; s1 = shots[si + 1][0] * c["dur"] if si + 1 < len(shots) else span
    f = bg(shots[si][1], BGS[shots[si][1]]).copy().convert("RGBA")
    amp = amp_at(c, lt_clip) if c["dia"] else 0.0
    shots[si][2](f, max(0, lt_clip - s0), s1 - s0, amp)
    for a, b, txt in c["chunks"]:
        if a <= lt_clip < b + (0.25 if txt == c["chunks"][-1][2] else 0):
            im = caption(txt, YELLOW if c["dia"] else (255, 255, 255))
            k = min(1, (lt_clip - a) / 0.08); im2 = im if k >= 1 else im.resize((max(1, int(im.width * (0.85 + 0.15 * k))), max(1, int(im.height * (0.85 + 0.15 * k)))))
            f.alpha_composite(im2, (int((W - im2.width) / 2), int(1530 - im2.height / 2)))
    f = f.convert("RGB")
    if lt_clip - s0 < 0.1 and gt > 0.3:   # kurzer weicher Schnitt
        f = Image.blend(Image.new("RGB", (W, H)), f, 0.55 + 0.45 * (lt_clip - s0) / 0.1)
    return f

# ---------------- Tonmischung ----------------
def mix():
    n = int(TOTAL * SR) + SR; voice = np.zeros(n, np.float32); fx = np.zeros(n, np.float32)
    def add(buf, s, x, g):
        i = int(s * SR); x = x[:max(0, n - i)]; buf[i:i + len(x)] += x * g
    for c in TL: add(voice, c["t0"], c["a"], 1.0)
    T = {c["id"]: c for c in TL}
    def at(cid, frac): return T[cid]["t0"] + frac * T[cid]["dur"]
    add(fx, at("N1", 0) - 0.2, sfx.engine(2.4), 0.5)
    add(fx, at("N1", 0.45) - 0.05, sfx.boom(), 0.7)
    add(fx, at("N2", 0), sfx.tractor(2.2), 0.4)
    add(fx, at("N2", 0.55), sfx.rustle(1.4), 0.5)
    add(fx, at("N3", 0) - 0.1, sfx.engine(2.2, 34, 80), 0.45)
    add(fx, at("N4", 0), sfx.grind(1.3), 0.5); add(fx, at("N4", 0.3), sfx.hiss(1.6), 0.5)
    add(fx, at("N5", 0.75), sfx.clank(0.6, 560), 0.55)
    add(fx, at("M", 0.48), sfx.thud(0.5, 60), 0.6)
    add(fx, at("N6", 0) + 0.5, sfx.whoosh(0.4), 0.4); add(fx, at("N6", 0.55), sfx.thud(0.6, 50), 0.75)
    add(fx, at("N7", 0), sfx.thud(0.5, 75), 0.6)
    add(fx, T["E"]["t0"] + T["E"]["dur"] - 0.2, sfx.laugh(1.2), 0.35)
    add(fx, at("N8", 0) - 0.05, sfx.boom(), 0.8); add(fx, at("N8", 0.1), sfx.heartbeat(1.0), 0.6); add(fx, at("N8", 0.1) + 0.85, sfx.heartbeat(1.0), 0.5)
    add(fx, at("N9", 0), sfx.hammer(2.0, 3.2), 0.4)
    add(fx, at("N10", 0), sfx.whoosh(0.5), 0.4); add(fx, at("N10", 0.42), sfx.crowd(3.0), 0.55)
    for k in range(7): add(fx, at("N10", 0.1) + k * 0.47, sfx.flash(), 0.35)
    add(fx, at("N11", 0), sfx.laugh(1.6), 0.4); add(fx, at("N11", 0.5), sfx.engine(2.6, 40, 100), 0.4)
    mus = sfx.music(TOTAL + 0.5, hits=(at("N8", 0) - 0.05,), swell_at=at("N10", 0.3))
    mus = np.pad(mus, (0, max(0, n - len(mus))))[:n]
    vabs = np.convolve(np.abs(voice), np.ones(4800) / 4800, "same")
    duck = 1 - 0.45 * np.clip(vabs / 0.05, 0, 1)
    out = voice + fx + mus * 0.16 * duck
    m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)].astype(np.float32)

if __name__ == "__main__":
    print(f"Laenge {TOTAL:.1f} s")
    if "--stills" in sys.argv:
        os.makedirs("v7/stills", exist_ok=True)
        ts = [c["t0"] + c["dur"] * fr for c in TL for fr in (0.25, 0.75)]
        tiles = [frame_at(t) for t in ts]
        for i, im in enumerate(tiles): im.save(f"v7/stills/{i:02d}.png")
        tw, th = 216, 384; cols = 9
        sheet = Image.new("RGB", (cols * (tw + 6) + 6, ((len(tiles) + cols - 1) // cols) * (th + 6) + 6))
        for i, t in enumerate(tiles): sheet.paste(t.resize((tw, th)), (6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + 6)))
        sheet.save("v7/STORYBOARD_V7.png"); print("stills ok"); sys.exit()
    audio = mix()
    out = av.open("ARC_Short01_Lamborghini_v7.mp4", "w")
    vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "18", "preset": "medium"}
    ast = out.add_stream("aac", rate=SR); ast.layout = "mono"
    N = int(TOTAL * FPS)
    for k in range(N):
        for p in vs.encode(av.VideoFrame.from_image(frame_at(k / FPS))): out.mux(p)
        if k % 150 == 0: print(k, "/", N, flush=True)
    for p in vs.encode(): out.mux(p)
    for i in range(0, len(audio), 1024):
        ch = audio[i:i + 1024].astype(np.float32); ch = np.pad(ch, (0, 1024 - len(ch))) if len(ch) < 1024 else ch
        af = av.AudioFrame.from_ndarray(ch.reshape(1, -1), format="flt", layout="mono"); af.sample_rate = SR
        for p in ast.encode(af): out.mux(p)
    for p in ast.encode(): out.mux(p)
    out.close(); print("ok")
