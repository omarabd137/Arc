"""ARC Short #02 – „The McDonald Brothers Lost McDonald's“.
Regeln aus Masterplan Teil 22: Satz 1 ab 0 s, zweites Raetsel bei 3-6 s, jedes Bild zeigt das Gesagte,
Requisiten und Orte genau (Crayon-Prinzip), Untertitel 2-3 Woerter mit gelben Schluesselwoertern, Loop am Ende.
Aufruf aus shorts/02_mcdonalds:  python short02.py [--stills]"""
import sys, os, math, random
from mcd_kit import *
sys.path.insert(0, os.path.join(HERE, "..", "01_lamborghini", "v7"))
import numpy as np, av
import sfx
from crayon2 import bust
from crayon3 import LIMB
os.chdir(HERE)

FPS, SR = 30, 48000
CAP_FONT = ImageFont.truetype(F + "ariblk.ttf", 72)
GREY = (222, 222, 222)

# ---------------- Ton ----------------
NARR = np.load("vo/narr_all.npy")
SEG = [(0.06, 2.46), (3.02, 5.12), (5.70, 7.00), (7.58, 12.32), (12.90, 15.28), (15.90, 17.08), (17.70, 21.74),
       (22.34, 24.74), (25.22, 26.92), (27.52, 29.98), (30.50, 31.66), (32.14, 34.74), (35.32, 37.64)]
def cut(i):
    s, e = SEG[i]; a = NARR[max(0, int((s - 0.04) * SR)):int((e + 0.06) * SR)].copy()
    f = int(0.015 * SR); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    return a

# (Text, gelbe Woerter, Pause danach)
LINES = [
    ("The McDonald brothers invented McDonald's...", {"McDonald's..."}, 0.12),
    ("and lost it to a milkshake salesman.", {"milkshake", "salesman."}, 0.22),
    ("They even lost their own name.", {"own", "name."}, 0.25),
    ("In 1954, Ray Kroc saw huge lines for their 15-cent burgers.", {"1954,", "15-cent"}, 0.2),
    ("So he sold their idea all over America.", {"America."}, 0.18),
    ("Then he wanted it all.", {"all."}, 0.3),
    ("In 1961, he bought them out for $2.7 million.", {"1961,", "$2.7", "million."}, 0.25),
    ("They kept their first restaurant, but not the name.", {"not", "name."}, 0.15),
    ("So they called it The Big M.", {"Big", "M."}, 0.3),
    ("Then Kroc opened a McDonald's around the block...", {"around", "block..."}, 0.1),
    ("and put them out of business.", {"business."}, 0.4),
    ("Today, there are over 45,000 McDonald's...", {"45,000"}, 0.15),
    ("and not one belongs to a McDonald.", {"not", "one"}, 0.35),
]
TL, t0 = [], 0.0
for i, (txt, hl, gap) in enumerate(LINES):
    a = cut(i)
    TL.append(dict(i=i, a=a, txt=txt, hl=hl, t0=t0, dur=len(a) / SR, end=t0 + len(a) / SR + gap))
    t0 = TL[-1]["end"]
TOTAL = t0

def chunks(c):
    words = c["txt"].split(); out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w[-1] in ",.!?" or (len(cur) == 2 and len(" ".join(cur)) > 13):
            out.append(cur); cur = []
    if cur: out.append(cur)
    tot = sum(len(" ".join(x)) + 3 for x in out); t, res = 0.0, []
    for x in out:
        d = (len(" ".join(x)) + 3) / tot * c["dur"]; res.append((t, t + d, x)); t += d
    return res
for c in TL: c["chunks"] = chunks(c)

_cap = {}
def caption(words, hl):
    key = (tuple(words), tuple(sorted(hl)))
    if key not in _cap:
        d0 = ImageDraw.Draw(Image.new("L", (1, 1))); sp = d0.textlength(" ", font=CAP_FONT)
        ws = [d0.textlength(w, font=CAP_FONT) for w in words]
        im = Image.new("RGBA", (int(sum(ws) + sp * (len(ws) - 1)) + 40, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 20
        for w, wl in zip(words, ws):
            d.text((x, 10), w, font=CAP_FONT, fill=((255, 214, 60) if w in hl else (255, 255, 255)) + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255)); x += wl + sp
        _cap[key] = im
    return _cap[key]

# ---------------- Sprites ----------------
_spr = {}
def sprite(key, fn):
    if key not in _spr:
        c = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); fn(c)
        bb = c.getbbox() or (0, 0, 2, 2)
        im = c.crop(bb).resize((max(1, (bb[2] - bb[0]) // SS), max(1, (bb[3] - bb[1]) // SS)), Image.LANCZOS)
        _spr[key] = (im, bb[0] // SS, bb[1] // SS)
    return _spr[key]

def put(frame, spr, dx=0, dy=0, scale=1.0, alpha=1.0):
    im, x, y = spr
    if scale != 1.0:
        im2 = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))))
        x, y, im = x + (im.width - im2.width) / 2, y + (im.height - im2.height) / 2, im2
    if alpha < 1.0:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    frame.alpha_composite(im, (int(x + dx), int(y + dy))) if 0 <= int(x + dx) and 0 <= int(y + dy) else frame.paste(im, (int(x + dx), int(y + dy)), im)

_bg = {}
def bg(key, fn):
    if key not in _bg:
        im = fn(); _bg[key] = (im.resize((W, H), Image.LANCZOS) if im.size[0] > W else im).convert("RGB")
    return _bg[key]

def walker(p, R, face, phase, mouth, brow, arms, seed, cx=540, base=1500):
    def fn(c):
        d = ImageDraw.Draw(c, "RGBA")
        leg, tor_w = R * 1.25, R * 1.05 * p["big"]; hip = base - leg
        d.ellipse(S(cx - R * 0.9, base - 10, cx + R * 0.9, base + 10), fill=(0, 0, 0, 55))
        for sx in (-1, 1):
            ph = 2 * math.pi * ((phase or 0) + (0.5 if sx > 0 else 0))
            x = cx + sx * tor_w * 0.28
            fx = x + (math.sin(ph) * R * 0.38 if phase is not None else sx * 4)
            fy = base - (max(0, math.cos(ph)) * R * 0.1 if phase is not None else 0)
            stroke(d, [(x, hip - 10), (fx, fy)], lw=LIMB); stroke(d, [(fx, fy), (fx + face * 22, fy)], lw=LIMB)
        figure(c, cx, base, R, p, face=face, mouth=mouth, brow=brow, arms=arms, seed=seed, seated=True)
    return fn

def fig(frame, p, x, base, R, face, walking=False, lt=0.0, mouth="line", brow=0.0, arms=("down", "down"), seed=1):
    ph = (round((lt * 1.9) % 1 * 8) % 8) / 8 if walking else None
    spr = sprite(("fig", id(p), R, face, ph, mouth, brow, arms, seed, base), walker(p, R, face, ph, mouth, brow, arms, seed, 540, base))
    put(frame, spr, x - 540, -abs(math.sin(2 * math.pi * ph)) * R * 0.06 if walking else 0)

def bust_s(frame, p, R, face, mouth, brow=0.0, eyes="open", hy=980, cx=540, seed=1, dx=0, dy=0, scale=1.0):
    put(frame, sprite(("bust", id(p), R, face, mouth, brow, eyes, hy, cx, seed), lambda c: bust(c, cx, hy, R, p, face=face, eyes=eyes, mouth=mouth, brow=brow, seed=seed)), dx, dy, scale)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def pop(x): x = max(0.0, min(1.0, x)); return 1 + 0.25 * math.sin(x * math.pi) if x < 1 else 1.0

def note(frame, lines, cx, cy, angle=-4, w=420, p=1.0):
    spr = sprite(("note", tuple(lines), cx, cy, angle, w), lambda c: sticky(c, cx, cy, lines, angle=angle, w=w))
    if p > 0: put(frame, spr, scale=0.6 + 0.4 * ease(p / 0.25) if p < 0.25 else 1.0)

def big_number(frame, s, cx, cy, size, k=1.0, color=(255, 214, 60)):
    f = ImageFont.truetype(BOLD, int(size * (0.7 + 0.3 * ease(k))))
    ImageDraw.Draw(frame).text((cx, cy), s, font=f, fill=color, anchor="mm", stroke_width=10, stroke_fill=INK)

# ---------------- Hintergruende ----------------
def stand_bg(name="McDonald's", dusk=False, lit=True, bigm=False, people=False):
    def fn():
        img, d = california_bg(1180, dusk=dusk)
        palm(d, 60, 1180, 560, 1); palm(d, 1030, 1180, 640, 2)
        if not dusk: car50(d, 760, 1300, 300, (120, 170, 160))
        px, top = mcd_stand_1948(img, cx=600, base=1180, scale=1.05, lit=lit, name=name)
        if bigm:
            text(img, "THE BIG M", px, top + 72 * 1.05, 46, BOLD, RED, stroke_w=1)
        if dusk:
            ov = Image.new("RGBA", img.size, (30, 26, 60, 110)); img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
        return img
    return fn

SIGN_S, SIGN_CX, SIGN_BASE = 2.2, 1618, 1886          # Nahaufnahme Pylon-Schild
def sign_close_bg(name=None):
    def fn():
        img, d = california_bg(1700)
        palm(d, 900, 1700, 900, 3)
        mcd_stand_1948(img, cx=SIGN_CX, base=SIGN_BASE, scale=SIGN_S, lit=True, name=name)
        return img
    return fn

def letters_layout():
    s = SIGN_S; px = max(170, SIGN_CX - 300 * s - 130 * s - 60 * s); top = SIGN_BASE - 300 * s - 330 * s
    f = ImageFont.truetype(SCRIPT, int(70 * s * SS)); word = "McDonald's"
    total = f.getlength(word) / SS; x = px - total / 2; out = []
    for ch in word:
        wch = f.getlength(ch) / SS; out.append((ch, x + wch / 2, top + 72 * s)); x += wch
    return out, f
LET, LETF = letters_layout()

def letter_spr(ch, x, y):
    def fn(c):
        ImageDraw.Draw(c).text((x * SS, y * SS), ch, font=LETF, fill=RED, anchor="mm", stroke_width=SS, stroke_fill=sh(RED, 0.6))
    return sprite(("let", ch, x, y), fn)

def usa_bg():
    img = Image.new("RGB", (W * SS, H * SS)); grad(img, (120, 170, 210), (170, 206, 230), 0, H)
    d = ImageDraw.Draw(img, "RGBA"); us_map(d, 540, 980, 1000); return img
US_P = None
def us_proj():
    global US_P
    if US_P is None:
        tmp = Image.new("RGB", (8, 8)); US_P = us_map(ImageDraw.Draw(tmp), 540, 980, 1000)
    return US_P

def world_bg():
    img = Image.new("RGB", (W * SS, H * SS)); grad(img, (30, 40, 70), (50, 66, 104), 0, H)
    d = ImageDraw.Draw(img, "RGBA"); world_map(d, 540, 1000, 1060); return img
WORLD_PTS = None
def world_points():
    global WORLD_PTS
    if WORLD_PTS is None:
        P = world_map(ImageDraw.Draw(Image.new("RGB", (8, 8))), 540, 1000, 1060)
        rnd = random.Random(5); pts = []
        boxes = [(-120, -75, 28, 50), (-100, -80, 15, 28), (-70, -40, -30, 0), (-5, 30, 40, 58), (5, 35, -30, 12), (75, 120, 20, 45), (125, 145, 30, 42), (115, 150, -35, -20)]
        for k in range(60):
            b = boxes[k % len(boxes)]; pts.append(P(rnd.uniform(b[0], b[1]), rnd.uniform(b[2], b[3])))
        WORLD_PTS = pts
    return WORLD_PTS

def desk_bg():
    img = Image.new("RGB", (W * SS, H * SS), (110, 84, 62)); d = ImageDraw.Draw(img, "RGBA")
    for k in range(14): stroke(d, [(0, 80 + k * 140), (W, 100 + k * 140)], lw=3, color=(96, 72, 54))
    contract(img, 540, 820, 600); return img

def dark_bg():
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        f = 1 - abs(y / H - 0.45) * 1.4; d.line([(0, y), (W, y)], fill=(int(30 + 40 * f), int(26 + 20 * f), int(34 + 30 * f)))
    return img

def kroc_store_bg():
    img, d = california_bg(1250)
    palm(d, 70, 1250, 520, 4)
    golden_arches_store(img, 470, 1250, 0.95)
    return img

MIX = sprite(("mixer",), lambda c: multimixer(ImageDraw.Draw(c, "RGBA"), 820, 1500, 300)) if False else None

# ---------------- Einstellungen (frame, lt, T) ----------------
def queue(f, lt):
    for i, x in enumerate([330, 410, 490, 570, 650]):
        fig(f, GUEST[i % 6], x - (lt * 6) % 8, 1290 + (i % 2) * 8, 52, 1, walking=True, lt=lt + i * 0.13, seed=200 + i)

def sh_open(f, lt, T):
    queue(f, lt)
    fig(f, MAC, 200, 1840, 125, 1, mouth="smile", arms=("hip", "rest"), seed=301)
    fig(f, DICK, 880, 1850, 118, -1, mouth="smile", arms=("rest", "hip"), seed=302)
    note(f, ["THE McDONALD BROTHERS", "San Bernardino, 1948"], 540, 300, w=760, p=lt + 0.3)

def sh_salesman(f, lt, T):
    put(f, sprite(("mixer",), lambda c: multimixer(ImageDraw.Draw(c, "RGBA"), 800, 1560, 330)), 0, math.sin(lt * 30) * 2)
    bust_s(f, KROC, 300, 1, "smirk", brow=-0.06, hy=1060, cx=380, seed=401)
    note(f, ["RAY KROC", "milkshake machine salesman"], 540, 330, angle=3, w=760, p=lt)

def sh_letters(f, lt, T):
    for k, (ch, x, y) in enumerate(LET):
        t = lt - 0.12 - k * 0.09
        if t <= 0: put(f, letter_spr(ch, x, y)); continue
        dy = 0.5 * 2600 * t * t; rot = (k % 2 * 2 - 1) * t * 160
        im, sx, sy = letter_spr(ch, x, y); im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
        if sy + dy < H: f.paste(im, (int(sx), int(sy + dy)), im)

def sh_kroc_sees(f, lt, T):
    queue(f, lt)
    wx = -150 + 320 * min(1, lt / 1.6)
    fig(f, KROC, wx, 1820, 120, 1, walking=lt < 1.6, lt=lt, mouth="smile" if lt > 1.6 else "line", seed=402)
    note(f, ["1954"], 820, 330, angle=-4, w=300, p=lt)
    if lt > T * 0.62: big_number(f, "15¢", 800, 1150, 220, (lt - T * 0.62) / 0.25)

def sh_usa(f, lt, T):
    P = us_proj(); d = ImageDraw.Draw(f, "RGBA")
    n = int(len(CITIES) * min(1, lt / (T * 0.9)))
    for k, (lon, lat) in enumerate(CITIES[:n]):
        x, y = P(lon, lat); age = lt - k * T * 0.9 / len(CITIES); s = 34 * (pop(age / 0.25) if age < 0.25 else 1)
        put(f, sprite(("arch", int(s)), lambda c, s=s: arch_icon(ImageDraw.Draw(c, "RGBA"), 540, 960, s)), x - 540, y - 960)
    note(f, ["1955 – 1961"], 540, 420, angle=3, w=420, p=lt)

def sh_wanted(f, lt, T):
    bust_s(f, KROC, 340, 1, "line", brow=-0.14, hy=1000, seed=403, scale=1.0 + 0.06 * lt / max(T, 0.1))

def sh_contract(f, lt, T):
    rnd = random.Random(4)
    for i in range(10):
        x, y, a = rnd.randint(120, 960), rnd.randint(1280, 1720), rnd.randint(-35, 35)
        k = ease((lt - 0.06 * i) / 0.4)
        if k <= 0: continue
        put(f, sprite(("bill", i), lambda c, x=x, y=y, a=a: dollar_bill(c, x, y, 360, angle=a)), 0, -(1 - k) * 900)
    d = ImageDraw.Draw(f, "RGBA"); prog = min(1, lt / 1.4); pts = []
    for j in range(int(60 * prog)):          # Unterschrift entsteht
        t = j / 60; pts.append((330 + 220 * t, 1165 - 18 * math.sin(t * 22) * (1 - t * 0.5) - 6 * math.sin(t * 7)))
    if len(pts) > 1: d.line(pts, fill=(30, 40, 110), width=5, joint="curve")

def sh_workers(f, lt, T):
    d = ImageDraw.Draw(f, "RGBA")
    d.line([(310, 1180), (250, 640)], fill=INK, width=10); d.line([(370, 1180), (310, 640)], fill=INK, width=10)
    for k in range(9): y = 1130 - k * 60; d.line([(305 - k * 6.6, y), (365 - k * 6.6, y)], fill=INK, width=7)
    fig(f, GUEST[5], 290, 930 + math.sin(lt * 8) * 4, 70, 1, mouth="line", arms=("point", "rest"), seed=410)
    def crate(c):                            # Holzkiste mit den abgeschraubten Buchstaben
        d = ImageDraw.Draw(c, "RGBA")
        text(c, "McDonald's", 250, 1440, 92, SCRIPT, RED, stroke_w=1, stroke_fill=sh(RED, 0.6), angle=8)
        shape(d, [(70, 1470), (430, 1470), (420, 1640), (80, 1640)], (176, 132, 88), 420, lw=5)
        for k in range(3): stroke(d, [(80, 1515 + k * 42), (424, 1515 + k * 42)], lw=3, color=(140, 100, 64))
    put(f, sprite(("crate",), crate))
    fig(f, MAC, 640, 1840, 120, -1, mouth="frown", brow=0.08, seed=303)
    fig(f, DICK, 900, 1850, 114, -1, mouth="frown", brow=0.08, seed=304)

def sh_bigm(f, lt, T):
    queue(f, lt)
    k = ease(lt / 0.35)
    put(f, sprite(("bigm",), lambda c: text(c, "THE BIG M", 170, 1180 - 300 * 1.05 - 330 * 1.05 + 72 * 1.05, 46, BOLD, RED, stroke_w=1)), 0, -(1 - k) * 300)

def sh_kroc_store(f, lt, T):
    crowd = [(80 + i * 105, 1660 + (i % 2) * 50) for i in range(10)]
    for i, (x, y) in enumerate(crowd):
        fig(f, GUEST[i % 6], x, y + math.sin(lt * 7 + i) * 3, 58, 1 if x < 540 else -1, mouth="smile", seed=500 + i)
    fig(f, KROC, 560, 1850, 120, -1, mouth="smile", arms=("point", "hip"), seed=405)

def sh_closed(f, lt, T):
    fig(f, MAC, 300, 1840, 125, 1, mouth="frown", brow=0.1, seed=305)
    fig(f, DICK, 760, 1850, 118, -1, mouth="frown", brow=0.1, seed=306)
    if lt > 0.25:
        k = ease((lt - 0.25) / 0.2)
        put(f, sprite(("closed",), lambda c: closed_sign(c, 540, 1050, 300)), 0, -(1 - k) * 120)

def sh_world(f, lt, T):
    pts = world_points(); n = int(len(pts) * min(1, lt / (T * 0.85)))
    for k, (x, y) in enumerate(pts[:n]):
        put(f, sprite(("arch", 26), lambda c: arch_icon(ImageDraw.Draw(c, "RGBA"), 540, 960, 26)), x - 540, y - 960)
    v = int(45000 * ease(lt / (T * 0.85)))
    big_number(f, f"{v:,}", 540, 520, 200, 1.0)

SHOTS = {  # Zeile -> [(Anteil Start, Hintergrund-Key, BG-Funktion, Einstellung)]
    0: [(0, "stand", stand_bg(), sh_open)],
    1: [(0, "stand_blur", lambda: stand_bg()().filter(ImageFilter.GaussianBlur(14)), sh_salesman)],
    2: [(0, "sign_close", sign_close_bg(None), sh_letters)],
    3: [(0, "stand", stand_bg(), sh_kroc_sees)],
    4: [(0, "usa", usa_bg, sh_usa)],
    5: [(0, "dark", dark_bg, sh_wanted)],
    6: [(0, "desk", desk_bg, sh_contract)],
    7: [(0, "stand_noname", stand_bg(None), sh_workers)],
    8: [(0, "stand_noname", stand_bg(None), sh_bigm)],
    9: [(0, "kroc_store", kroc_store_bg, sh_kroc_store)],
    10: [(0, "closed", stand_bg(None, dusk=True, lit=False, bigm=True), sh_closed)],
    11: [(0, "world", world_bg, sh_world)],
    12: [(0, "stand", stand_bg(), sh_open)],
}

def frame_at(gt):
    ci = max(i for i, c in enumerate(TL) if c["t0"] <= gt) if gt >= TL[0]["t0"] else 0
    c = TL[ci]; lt = gt - c["t0"]; span = c["end"] - c["t0"]
    shots = SHOTS[c["i"]]; si = max(i for i, s in enumerate(shots) if s[0] * c["dur"] <= lt)
    s0 = shots[si][0] * c["dur"]; s1 = shots[si + 1][0] * c["dur"] if si + 1 < len(shots) else span
    f = bg(shots[si][1], shots[si][2]).copy().convert("RGBA")
    shots[si][3](f, lt - s0 + (TL[0]["end"] if c["i"] == 12 else 0), s1 - s0)
    for a, b, words in c["chunks"]:
        if a <= lt < b + (0.3 if words is c["chunks"][-1][2] else 0):
            im = caption(words, c["hl"]); k = min(1, (lt - a) / 0.08)
            if k < 1: im = im.resize((max(1, int(im.width * (0.85 + 0.15 * k))), max(1, int(im.height * (0.85 + 0.15 * k)))))
            f.alpha_composite(im, (int((W - im.width) / 2), int(1500 - im.height / 2)))
    return f.convert("RGB")

# ---------------- Ton-Mischung ----------------
rng = np.random.default_rng(3)
def pop_sfx(): t = sfx.t(0.12); return sfx.norm(np.sin(2 * np.pi * (500 - 1800 * t) * t) * np.exp(-t * 40), 0.4)
def pen(d=1.4): x = sfx.band(sfx.noise(d), 2500, 8000) * (0.4 + 0.6 * (np.sin(2 * np.pi * 11 * sfx.t(d)) > 0)); return sfx.norm(x * np.minimum(1, (d - sfx.t(d)) / 0.2), 0.35)
def hum(d=1.6): t = sfx.t(d); return sfx.norm((np.sin(2 * np.pi * 120 * t) + 0.4 * np.sin(2 * np.pi * 240 * t)) * np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.3), 0.3)
def sizzle(d=2.4): t = sfx.t(d); return sfx.norm(sfx.band(sfx.noise(d), 3000, 10000) * (0.6 + 0.4 * rng.random(len(t))) * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.4), 0.3)
def ratchet(d=1.2):
    t = sfx.t(d); x = np.zeros_like(t)
    for s in np.arange(0.05, d - 0.05, 0.11): i = int(s * SR); c = sfx.clank(0.06, 1800); x[i:i + len(c)] += c[:len(x) - i]
    return sfx.norm(x, 0.4)

def mix():
    n = int((TOTAL + 0.5) * SR); voice = np.zeros(n, np.float32); fx = np.zeros(n, np.float32)
    def add(buf, s, x, g):
        i = int(max(0, s) * SR); x = x[:max(0, n - i)]; buf[i:i + len(x)] += x * g
    for c in TL: add(voice, c["t0"], c["a"], 1.0)
    T = TL
    add(fx, 0, sizzle(2.6), 0.35); add(fx, 0, sfx.crowd(2.6, 5), 0.25)
    add(fx, T[1]["t0"] - 0.03, sfx.boom(1.4), 0.6)
    for k in range(10): add(fx, T[2]["t0"] + 0.25 + k * 0.09 + 0.35, sfx.clank(0.35, 700 + k * 40), 0.3)
    add(fx, T[3]["t0"] + 0.1, sfx.thud(0.4, 90), 0.4); add(fx, T[3]["t0"], sfx.crowd(4.5, 9), 0.3); add(fx, T[3]["t0"] + T[3]["dur"] * 0.62, sfx.thud(0.5, 60), 0.6)
    for k in range(len(CITIES)): add(fx, T[4]["t0"] + k * T[4]["dur"] * 0.9 / len(CITIES), pop_sfx(), 0.25)
    add(fx, T[5]["t0"] - 0.05, sfx.boom(1.6), 0.7)
    add(fx, T[6]["t0"], sfx.rustle(1.0), 0.5); add(fx, T[6]["t0"] + 0.1, pen(1.4), 0.45); add(fx, T[6]["t0"] + T[6]["dur"] * 0.7, sfx.thud(0.6, 50), 0.7)
    add(fx, T[7]["t0"] + 0.2, ratchet(1.4), 0.45)
    add(fx, T[8]["t0"] + 0.3, hum(1.6), 0.4); add(fx, T[8]["t0"] + 0.3, sfx.thud(0.4, 80), 0.5)
    add(fx, T[9]["t0"], sfx.crowd(2.8, 0.4), 0.45)
    add(fx, T[10]["t0"] + 0.25, sfx.thud(0.5, 70), 0.7)
    add(fx, T[11]["t0"], sfx.whoosh(0.5), 0.4)
    for k in range(14): add(fx, T[11]["t0"] + 0.1 + k * 0.17, pop_sfx(), 0.18)
    mus = sfx.music(TOTAL + 0.5, hits=(T[5]["t0"] - 0.05, T[10]["t0"] + 0.25))
    mus = np.pad(mus, (0, max(0, n - len(mus))))[:n]
    cut_i = int(T[12]["t0"] * SR); fade = int(0.25 * SR)       # Musik bricht vor der Pointe ab
    mus[cut_i:cut_i + fade] *= np.linspace(1, 0, fade)[:len(mus[cut_i:cut_i + fade])]; mus[cut_i + fade:] = 0
    vabs = np.convolve(np.abs(voice), np.ones(4800) / 4800, "same"); duck = 1 - 0.45 * np.clip(vabs / 0.05, 0, 1)
    out = voice + fx + mus * 0.16 * duck
    m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)].astype(np.float32)

if __name__ == "__main__":
    print(f"Laenge {TOTAL:.1f} s")
    if "--stills" in sys.argv:
        os.makedirs("stills", exist_ok=True)
        tiles = [frame_at(c["t0"] + c["dur"] * fr) for c in TL for fr in (0.3, 0.85)]
        for i, im in enumerate(tiles): im.save(f"stills/{i:02d}.png")
        tw, th, cols = 216, 384, 9
        sheet = Image.new("RGB", (cols * (tw + 6) + 6, ((len(tiles) + cols - 1) // cols) * (th + 6) + 6))
        for i, t in enumerate(tiles): sheet.paste(t.resize((tw, th)), (6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + 6)))
        sheet.save("STORYBOARD_02.png"); print("stills ok"); sys.exit()
    audio = mix()
    out = av.open("ARC_Short02_McDonalds.mp4", "w")
    vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "18", "preset": "medium"}
    ast = out.add_stream("aac", rate=SR); ast.layout = "mono"
    N = int(TOTAL * FPS)
    for k in range(N):
        for p in vs.encode(av.VideoFrame.from_image(frame_at(k / FPS))): out.mux(p)
        if k % 150 == 0: print(k, "/", N, flush=True)
    for p in vs.encode(): out.mux(p)
    for i in range(0, len(audio), 1024):
        ch = audio[i:i + 1024]; ch = np.pad(ch, (0, 1024 - len(ch))) if len(ch) < 1024 else ch
        af = av.AudioFrame.from_ndarray(ch.reshape(1, -1).astype(np.float32), format="flt", layout="mono"); af.sample_rate = SR
        for p in ast.encode(af): out.mux(p)
    for p in ast.encode(): out.mux(p)
    out.close(); print("ok")
