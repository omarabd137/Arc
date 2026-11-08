"""ARC Short #05 - "Why The Milk Is Always At The Back Of The Store" (9:16).
Regeln: Masterplan Teil 28/30 - Hook-Text im ersten Bild, neues Bild alle ~1 s, hell, keine Melodie-Musik
(nur leiser Takt + Sounds an echten Aktionen), kein Aufruf, Loop. Alles am gesprochenen Wort verankert (Scribe).
Aufruf: python short05.py --stills | (voll)"""
import sys, os, json, re, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "../../sfx_lib")); sys.path.insert(0, os.path.join(HERE, "../04_market_crash"))
sys.path.insert(0, os.path.join(HERE, "../../longform/01_money"))
import numpy as np, av
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cartoon, hq
from cartoon import person, closeup, LEO, P, figure, sprite, put, EXPR
import lib as SFXL

SR, FPS = 48000, 30; W, H = 1080, 1920
BOLD = "C:/Windows/Fonts/ariblk.ttf"; SANS = "C:/Windows/Fonts/arialbd.ttf"
_f = {}
def F(s, p=BOLD):
    if (p, int(s)) not in _f: _f[(p, int(s))] = ImageFont.truetype(p, int(s))
    return _f[(p, int(s))]
INK = (28, 26, 34); WHITE = (255, 255, 255); YEL = (255, 210, 40); RED = (225, 50, 55); GREEN = (40, 170, 90); BLUE = (60, 110, 200)
MANAGER = P(hair=(60, 44, 34), top=(230, 70, 60), pants=(50, 54, 70), shoes=(40, 36, 36), skin=(226, 186, 150), style="side", collar=True)
CROWD = [P(hair=(30, 26, 24), top=(90, 170, 120), pants=(60, 64, 80), skin=(150, 100, 70), style="buzz"),
         P(hair=(200, 160, 90), top=(240, 170, 60), pants=(70, 74, 100), skin=(240, 205, 175), style="long"),
         P(hair=(90, 60, 40), top=(150, 100, 200), pants=(50, 50, 60), skin=(214, 172, 134), style="short")]

# ---------------- Stimme + Woerter ----------------
SENT = ["The milk is always at the very back of the store.", "That's not an accident.",
        "Stores will tell you it's because the trucks unload in the back.", "And that's true.", "But it's only half the story.",
        "Milk is the one thing almost everyone comes in for.", "So to get it, you have to walk past thousands of other products.",
        "Chips.", "Cookies.", "Something on sale you didn't even need.", "And the shelf right at your eye level?", "Brands pay to be there.",
        "The cheaper stuff is down by your feet.", "Even the end of every aisle is paid for.", "You came in for one thing.",
        "And you leave with twelve...", "all because the milk is at the very back of the store."]
def dec(p):
    c = av.open(p); r = av.AudioResampler(format="flt", layout="mono", rate=SR); out = []
    for fr in c.decode(audio=0):
        for f in r.resample(fr): out.append(f.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.float32)
RAW = dec("vo/s05.mp3")
WR = json.load(open("vo/words.json", encoding="utf-8"))["words"]; WR = [w for w in WR if w["type"] == "word"]
GAP = {1: 0.22, 2: 0.22, 3: 0.2, 4: 0.18, 5: 0.24, 6: 0.22, 7: 0.22, 8: 0.16, 9: 0.16, 10: 0.3, 11: 0.22, 12: 0.2, 13: 0.2, 14: 0.24, 15: 0.1, 16: 0.22}
SEGS = []; pos = 0; t = 0.05
for si, s in enumerate(SENT):
    n = len(s.split()); ws = WR[pos:pos + n]; pos += n
    if si: t += GAP[si]
    a0 = max(0, ws[0]["start"] - 0.04); a1 = ws[-1]["end"] + 0.06
    SEGS.append(dict(i=si, t0=t, a0=a0, a1=a1, words=[(w["text"], w["start"] - a0 + t, w["end"] - a0 + t) for w in ws]))
    t += a1 - a0
TOTAL = t + 0.35
ALLW = [w for s in SEGS for w in s["words"]]
def _n(x): return re.sub(r"[^a-z0-9']", "", x.lower())
def WT(si, word, k=1):
    c = 0
    for w, s_, e_ in SEGS[si]["words"]:
        if _n(w) == _n(word):
            c += 1
            if c == k: return s_
    raise KeyError((si, word, k))
def ramp(x, a, b): return max(0.0, min(1.0, (x - a) / max(1e-6, b - a)))
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------------- Zeichen-Grundlagen ----------------
def txt(d, s, x, y, size, col=INK, anchor="mm", font=BOLD, stroke=0, sc=INK):
    d.text((x, y), s, font=F(size, font), fill=col, anchor=anchor, stroke_width=stroke, stroke_fill=sc)
def rr(d, box, fill, out=INK, w=6, r=20): d.rounded_rectangle(box, r, fill=fill, outline=out, width=w)
def label(d, s, x, y, size, col=WHITE, k=1.0):
    if k <= 0: return
    sz = size * (0.7 + 0.3 * back(min(1, k / 0.6))); txt(d, s, x, y, sz, col, stroke=max(3, int(size * 0.1)), sc=INK)
def stamp(f, s, cx, cy, size, col=RED, k=1.0, rot=-10):
    if k <= 0: return
    sc = 1.0 + 0.7 * (1 - ease(min(1, k / 0.35))); size = int(size * sc)
    lay = Image.new("RGBA", (W, H)); dl = ImageDraw.Draw(lay); fo = F(size); tw = dl.textlength(s, font=fo)
    dl.rounded_rectangle((cx - tw / 2 - 28, cy - size * 0.72, cx + tw / 2 + 28, cy + size * 0.72), 16, outline=col, width=max(8, size // 9))
    dl.text((cx, cy), s, font=fo, fill=col, anchor="mm"); f.alpha_composite(lay.rotate(rot, center=(cx, cy), resample=Image.BICUBIC))
def glow(f, cx, cy, r, col, a):
    lay = Image.new("RGBA", (W, H)); ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (int(a),))
    f.alpha_composite(lay.filter(ImageFilter.GaussianBlur(r * 0.45)))
def vgrad(c0, c1, w=W, h=H):
    a = np.linspace(0, 1, h)[:, None, None]; arr = (np.array(c0) * (1 - a) + np.array(c1) * a).repeat(w, 1)
    return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")

PCOL = [(230, 60, 60), (250, 190, 40), (60, 150, 230), (90, 190, 110), (240, 120, 40), (170, 90, 200), (250, 240, 230), (40, 70, 140), (230, 90, 150)]
def product(d, x, y, w, h, col, kind, s=1.0):
    """einzelnes Produkt, Unterkante bei y"""
    if kind == 0:   # Karton
        d.rectangle((x, y - h, x + w, y), fill=col, outline=INK, width=max(1, int(3 * s)))
        d.rectangle((x + w * 0.15, y - h * 0.62, x + w * 0.85, y - h * 0.4), fill=(255, 255, 255))
    elif kind == 1:  # Flasche
        d.rounded_rectangle((x + w * 0.15, y - h * 0.78, x + w * 0.85, y), max(2, int(w * 0.2)), fill=col, outline=INK, width=max(1, int(3 * s)))
        d.rectangle((x + w * 0.36, y - h, x + w * 0.64, y - h * 0.76), fill=col, outline=INK, width=max(1, int(3 * s)))
    elif kind == 2:  # Dose
        d.rounded_rectangle((x + w * 0.05, y - h * 0.7, x + w * 0.95, y), max(2, int(w * 0.12)), fill=col, outline=INK, width=max(1, int(3 * s)))
        d.line((x + w * 0.05, y - h * 0.45, x + w * 0.95, y - h * 0.45), fill=(255, 255, 255), width=max(1, int(4 * s)))
    else:            # Tuete
        d.polygon([(x, y), (x + w * 0.1, y - h * 0.92), (x + w * 0.9, y - h * 0.92), (x + w, y)], fill=col, outline=INK)
        d.ellipse((x + w * 0.3, y - h * 0.62, x + w * 0.7, y - h * 0.3), fill=(255, 230, 120))

def shelf_front(d, x0, y0, x1, y1, rows, seed, s=1.0, levels_col=None):
    """Regal von vorn mit Produkten"""
    r = random.Random(seed); d.rectangle((x0, y0, x1, y1), fill=(235, 232, 225), outline=INK, width=int(6 * s))
    hh = (y1 - y0) / rows
    for k in range(rows):
        yb = y0 + hh * (k + 1) - 8 * s; x = x0 + 10 * s
        col_override = levels_col.get(k) if levels_col else None
        while x < x1 - 40 * s:
            w = r.uniform(46, 70) * s; h = r.uniform(0.55, 0.82) * hh; kind = r.randrange(4)
            col = col_override(r) if col_override else r.choice(PCOL)
            product(d, x, yb, w, h, col, kind, s); x += w + r.uniform(4, 10) * s
        d.rectangle((x0, yb, x1, yb + 12 * s), fill=(180, 176, 168), outline=INK, width=int(3 * s))

# ---------------- Hintergruende (2x gezeichnet, gecacht) ----------------
_bg = {}
def S2(img): return img.resize((W, H), Image.LANCZOS)
def aisle_bg():
    """Gang in Zentralperspektive, ganz hinten leuchtet die Milch-Kuehlwand"""
    if "aisle" in _bg: return _bg["aisle"].copy()
    S = 2; im = Image.new("RGBA", (W * S, H * S), (250, 248, 242, 255)); d = ImageDraw.Draw(im, "RGBA")
    vx, vy = 540 * S, 720 * S; bx0, bx1, by0, by1 = 420 * S, 660 * S, 600 * S, 840 * S
    d.rectangle((0, 0, W * S, by0), fill=(246, 244, 238))                                   # Decke
    for k in range(6):                                                                    # Deckenlichter
        a = k / 6; b = (k + 1) / 6 - 0.06
        def pt(u, side): return (vx + (side * 300 * S) * (1 - u) * 1.0 + side * (1 - u) * 0, vy - (vy - 60 * S) * (1 - u))
        y0 = 60 * S + (by0 - 60 * S) * (1 - (1 - a) ** 1.6); y1 = 60 * S + (by0 - 60 * S) * (1 - (1 - b) ** 1.6)
        hw0 = 160 * S * (1 - (y0 - 60 * S) / (by0 - 60 * S) * 0.85); hw1 = 160 * S * (1 - (y1 - 60 * S) / (by0 - 60 * S) * 0.85)
        d.polygon([(vx - hw0, y0), (vx + hw0, y0), (vx + hw1, y1), (vx - hw1, y1)], fill=(255, 255, 250), outline=(215, 212, 205))
    d.polygon([(0, H * S), (W * S, H * S), (bx1, by1), (bx0, by1)], fill=(222, 214, 200))   # Boden
    for k in range(-8, 9):
        d.line((vx + k * 170 * S, H * S, vx + k * 14 * S, by1), fill=(206, 197, 182), width=3 * S)
    for k in range(1, 14):
        y = by1 + (H * S - by1) * (k / 14) ** 2.1; d.line((0, y, W * S, y), fill=(206, 197, 182), width=2 * S)
    # Rueckwand mit Kuehlregal
    d.rectangle((bx0, by0, bx1, by1), fill=(232, 240, 248), outline=INK, width=3 * S)
    d.rectangle((bx0 + 8 * S, by0 + 40 * S, bx1 - 8 * S, by1 - 10 * S), fill=(210, 232, 255), outline=INK, width=3 * S)
    r = random.Random(4)
    for row in range(4):
        yb = by0 + 40 * S + (row + 1) * (by1 - by0 - 50 * S) / 4 - 4 * S
        for i in range(9):
            x = bx0 + 14 * S + i * 24 * S; product(d, x, yb, 18 * S, 34 * S, (255, 255, 255) if i % 3 else (120, 170, 240), 1, S * 0.4)
    d.rectangle((bx0 + 40 * S, by0 + 6 * S, bx1 - 40 * S, by0 + 34 * S), fill=(40, 90, 180), outline=INK, width=2 * S)
    d.text(((bx0 + bx1) / 2, by0 + 20 * S), "DAIRY", font=F(22 * S), fill=WHITE, anchor="mm")
    # Seitenregale (links/rechts) in Perspektive
    for side in (-1, 1):
        nx = 0 if side < 0 else W * S; fx = bx0 if side < 0 else bx1
        top_n, bot_n = 180 * S, 1660 * S
        quad = [(nx, top_n), (fx, by0 + 30 * S), (fx, by1), (nx, bot_n)]
        d.polygon(quad, fill=(236, 232, 224), outline=INK)
        levels = 6
        for lv in range(levels + 1):
            u = lv / levels; yn = top_n + (bot_n - top_n) * u; yf = by0 + 30 * S + (by1 - by0 - 30 * S) * u
            d.line((nx, yn, fx, yf), fill=(170, 165, 158), width=5 * S)
        rr_ = random.Random(10 + side)
        for lv in range(levels):
            u0 = lv / levels; u1 = (lv + 1) / levels
            steps = 26
            for j in range(steps):
                a = (j / steps) ** 0.55; b = ((j + 0.8) / steps) ** 0.55
                def P_(t_, u):
                    x = nx + (fx - nx) * t_; yn = top_n + (bot_n - top_n) * u; yf = by0 + 30 * S + (by1 - by0 - 30 * S) * u
                    return (x, yn + (yf - yn) * t_)
                p1 = P_(a, u1); p2 = P_(b, u1); p3 = P_(b, u0 + (u1 - u0) * 0.3); p4 = P_(a, u0 + (u1 - u0) * 0.3)
                d.polygon([p1, p2, p3, p4], fill=rr_.choice(PCOL), outline=INK)
        d.line(quad + [quad[0]], fill=INK, width=4 * S)
    im = S2(im)
    glow(im, 540, 720, 170, (170, 215, 255), 150)
    _bg["aisle"] = im; return im.copy()

def fridge_bg():
    if "fridge" in _bg: return _bg["fridge"].copy()
    im = vgrad((236, 244, 252), (205, 222, 240)); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((40, 330, 1040, 1500), fill=(225, 238, 250), outline=INK, width=8)
    d.rectangle((60, 350, 1020, 450), fill=(40, 90, 180), outline=INK, width=6); txt(d, "MILK", 540, 400, 80, WHITE)
    for k in range(3):
        x0 = 70 + k * 320; d.rectangle((x0, 470, x0 + 300, 1480), fill=(200, 228, 255), outline=INK, width=6)
        for row in range(4):
            yb = 700 + row * 250
            for i in range(4):
                product(d, x0 + 16 + i * 70, yb, 58, 170, (255, 255, 255) if (i + row) % 3 else (120, 170, 240), 1, 1)
            d.rectangle((x0, yb, x0 + 300, yb + 12), fill=(170, 190, 210))
        d.line((x0 + 280, 900, x0 + 280, 1060), fill=(150, 160, 175), width=10)
    glow(im, 540, 900, 520, (190, 225, 255), 90)
    _bg["fridge"] = im; return im.copy()

def dock_bg():
    if "dock" in _bg: return _bg["dock"].copy()
    im = vgrad((150, 200, 245), (215, 235, 250)); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 1250, W, H), fill=(120, 120, 128)); d.rectangle((0, 1250, W, 1270), fill=(90, 90, 98))
    d.rectangle((0, 520, 640, 1250), fill=(232, 222, 205), outline=INK, width=8)                 # Ladenrueckseite
    d.rectangle((140, 720, 520, 1150), fill=(80, 84, 96), outline=INK, width=8)                  # Rolltor
    for y in range(740, 1150, 34): d.line((150, y, 510, y), fill=(110, 114, 128), width=4)
    d.rectangle((100, 1150, 560, 1250), fill=(170, 160, 150), outline=INK, width=6)
    rr(d, (170, 600, 490, 680), (40, 90, 180)); txt(d, "DELIVERIES", 330, 640, 40, WHITE)
    _bg["dock"] = im; return im.copy()

def studio(c0=(255, 246, 225), c1=(255, 226, 190)):
    k = ("st", c0, c1)
    if k not in _bg:
        im = vgrad(c0, c1); glow(im, 540, 800, 600, (255, 255, 255), 110); _bg[k] = im
    return _bg[k].copy()

# ---------------- Figuren ----------------
def walker(f, pr, x, foot_y, R, tt, face=1, expr="neutral"):
    mouth, brow, eyes = EXPR.get(expr, EXPR["neutral"]); ph = round((tt * 1.9) % 1 * 12) / 12
    spr = sprite(("w5", id(pr), R, face, expr, ph), lambda c: figure(c, 960, 1040, R, pr, face, mouth, brow, ("down", "down"), "walk", ph, eyes))
    put(f, spr, x - 960, foot_y - 1040 - abs(math.sin(2 * math.pi * ph)) * R * 0.05)

def cart(d, x, y, s=1.0, items=()):
    """Einkaufswagen (Grund vorn links bei x,y = Boden), items = Liste (col, kind)"""
    bx0, by0, bx1, by1 = x, y - 250 * s, x + 300 * s, y - 70 * s
    for i, (col, kind) in enumerate(items):
        ix = bx0 + 20 * s + (i % 4) * 64 * s; iy = by0 + 60 * s - (i // 4) * 40 * s
        product(d, ix, iy + 40 * s, 56 * s, 90 * s, col, kind, s)
    d.polygon([(bx0, by0), (bx1, by0), (bx1 - 30 * s, by1), (bx0 + 20 * s, by1)], fill=(200, 205, 215, 120), outline=INK)
    for k in range(1, 6): xx = bx0 + (bx1 - bx0) * k / 6; d.line((xx, by0, xx - 6 * s, by1), fill=(110, 115, 125), width=int(4 * s))
    d.line((bx0, by0 + 60 * s, bx1, by0 + 60 * s), fill=(110, 115, 125), width=int(4 * s))
    d.line((bx1, by0, bx1 + 50 * s, by0 - 60 * s), fill=INK, width=int(8 * s)); d.line((bx1 + 30 * s, by0 - 70 * s, bx1 + 70 * s, by0 - 50 * s), fill=RED, width=int(14 * s))
    d.line((bx0 + 20 * s, by1, bx0 + 10 * s, y - 20 * s), fill=INK, width=int(6 * s)); d.line((bx1 - 30 * s, by1, bx1 - 40 * s, y - 20 * s), fill=INK, width=int(6 * s))
    for wx in (bx0 + 10 * s, bx1 - 40 * s): d.ellipse((wx - 18 * s, y - 36 * s, wx + 18 * s, y), fill=INK)

def truck(d, x, y, s=1.0, lights=False):
    """Kastenwagen, Heck links bei x, Boden y"""
    d.rectangle((x, y - 420 * s, x + 560 * s, y - 70 * s), fill=(250, 250, 250), outline=INK, width=int(8 * s))
    d.rectangle((x + 40 * s, y - 330 * s, x + 520 * s, y - 230 * s), fill=(40, 90, 180)); txt(d, "FRESH DAIRY", x + 280 * s, y - 280 * s, int(56 * s), WHITE)
    d.rounded_rectangle((x + 560 * s, y - 300 * s, x + 760 * s, y - 70 * s), int(30 * s), fill=(225, 60, 55), outline=INK, width=int(8 * s))
    d.rectangle((x + 620 * s, y - 270 * s, x + 730 * s, y - 180 * s), fill=(170, 210, 240), outline=INK, width=int(5 * s))
    for wx in (x + 110 * s, x + 450 * s, x + 660 * s):
        d.ellipse((wx - 62 * s, y - 124 * s, wx + 62 * s, y), fill=INK); d.ellipse((wx - 26 * s, y - 88 * s, wx + 26 * s, y - 36 * s), fill=(180, 180, 186))
    if lights: d.ellipse((x - 18 * s, y - 160 * s, x + 14 * s, y - 120 * s), fill=(255, 240, 160))

def crate(d, x, y, s=1.0):
    d.rectangle((x, y - 110 * s, x + 150 * s, y), fill=(60, 120, 210), outline=INK, width=int(5 * s))
    for i in range(3): product(d, x + 10 * s + i * 46 * s, y - 20 * s, 40 * s, 120 * s, WHITE, 1, s)

# ---------------- Szenen ----------------
def banner(f, k=1.0):
    """dauerhaftes Hook-Banner oben (Text im ersten Bild)"""
    if k <= 0: return
    d = ImageDraw.Draw(f, "RGBA"); y = 250 - (1 - ease(k)) * 300
    d.rectangle((40, y - 105, 1040, y + 105), fill=YEL, outline=INK, width=8)
    txt(d, "WHY IS THE MILK", 540, y - 44, 70); txt(d, "ALWAYS IN THE BACK?", 540, y + 44, 70)

def s0(lt, T, gt):   # The milk is always at the very back of the store.
    f = aisle_bg(); d = ImageDraw.Draw(f, "RGBA")
    pul = 0.5 + 0.5 * math.sin(gt * 5); glow(f, 540, 720, 120 + 20 * pul, (200, 235, 255), 120)
    x = 230 + 110 * ease(ramp(lt, 0, T)); walker(f, LEO, int(x), 1700, 150, lt, 1, "neutral")
    if lt > WT(0, "back") - SEGS[0]["t0"]:
        a = ease(ramp(lt, WT(0, "back") - SEGS[0]["t0"], WT(0, "back") - SEGS[0]["t0"] + 0.3))
        d.line((540, 1010, 540, 870 - 0 * a), fill=RED, width=12); d.polygon([(510, 880), (570, 880), (540, 840)], fill=RED)
        label(d, "MILK", 640, 960, 70, WHITE, a)
    banner(f, 1.0); return f

def s1(lt, T, gt):   # That's not an accident.
    f = studio((255, 240, 215), (255, 214, 170)); d = ImageDraw.Draw(f, "RGBA")
    closeup(f, LEO, 520, 520, 1150, "stand", 0, "worried")
    k = ramp(lt, WT(1, "accident") - SEGS[1]["t0"], WT(1, "accident") - SEGS[1]["t0"] + 0.25)
    stamp(f, "NOT AN ACCIDENT", 540, 560, 84, RED, k, -8)
    banner(f, 1.0); return f

def s2(lt, T, gt):   # Stores will tell you it's because the trucks unload in the back.
    tr = WT(2, "trucks") - SEGS[2]["t0"]
    if lt < tr - 0.15:
        f = aisle_bg(); f.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, 90))); d = ImageDraw.Draw(f, "RGBA")
        person(f, MANAGER, 560, 1720, 170, "point", -1, "talk")
        rr(d, (90, 780, 620, 960), WHITE, INK, 7, 40); d.polygon([(470, 950), (540, 950), (560, 1040)], fill=WHITE, outline=INK)
        txt(d, "It's the trucks!", 355, 870, 54)
        banner(f, 1.0); return f
    f = dock_bg(); d = ImageDraw.Draw(f, "RGBA")
    un = WT(2, "unload") - SEGS[2]["t0"]
    k = ease(ramp(lt, tr - 0.15, un)); tx = 1100 - (1100 - 600) * k
    truck(d, int(tx), 1300, 0.85, lights=(lt * 3) % 1 < 0.5 and k < 1)
    if lt > un:
        for i in range(3):
            c = ease(ramp(lt, un + i * 0.22, un + i * 0.22 + 0.5)); cx = 560 - 330 * c
            if c > 0: crate(d, int(cx), 1252 - 2, 0.8)
    return f

def s3(lt, T, gt):   # And that's true.
    f = dock_bg(); d = ImageDraw.Draw(f, "RGBA"); truck(d, 600, 1300, 0.85)
    for i in range(3): crate(d, 230 + i * 10, 1250 - i * 110, 0.8)
    k = ramp(lt, WT(3, "true") - SEGS[3]["t0"], WT(3, "true") - SEGS[3]["t0"] + 0.22)
    stamp(f, "TRUE", 540, 420, 130, GREEN, k, -8); return f

def s4(lt, T, gt):   # But it's only half the story.
    f = dock_bg(); d = ImageDraw.Draw(f, "RGBA"); truck(d, 600, 1300, 0.85)
    for i in range(3): crate(d, 230 + i * 10, 1250 - i * 110, 0.8)
    stamp(f, "TRUE", 540, 420, 130, GREEN, 1, -8)
    hf = WT(4, "half") - SEGS[4]["t0"]; k = ease(ramp(lt, hf - 0.1, hf + 0.35))
    if k > 0:   # Bild reisst in der Mitte, rechte Haelfte faellt weg
        r = f.crop((540, 0, W, H)); g = studio((40, 40, 52), (20, 20, 30)); g.paste(f.crop((0, 0, 540, H)), (0, 0))
        r = r.rotate(-12 * k, resample=Image.BICUBIC, expand=True); g.alpha_composite(r, (int(540 + 120 * k), int(400 * k * k)))
        dd = ImageDraw.Draw(g); pts = [(540 + (12 if i % 2 else -12), i * 80) for i in range(26)]; dd.line(pts, fill=WHITE, width=10)
        label(dd, "HALF", 270, 1180, 140, YEL, ramp(lt, hf, hf + 0.3)); f = g
    return f

def s5(lt, T, gt):   # Milk is the one thing almost everyone comes in for.
    f = studio((235, 246, 255), (200, 225, 250)); d = ImageDraw.Draw(f, "RGBA")
    ev = WT(5, "everyone") - SEGS[5]["t0"]; n = 1 + int(ramp(lt, 0.2, ev + 0.2) * 6)
    for i in range(n):
        r = random.Random(i); x = 160 + (i % 3) * 380 + r.uniform(-30, 30); y = 520 + (i // 3) * 560 + r.uniform(-30, 30); rot = r.uniform(-9, 9)
        note = Image.new("RGBA", (340, 430)); nd = ImageDraw.Draw(note)
        nd.rectangle((10, 10, 330, 420), fill=(255, 252, 235), outline=INK, width=6)
        for j, item in enumerate(r.sample(["eggs", "bread", "apples", "rice", "coffee"], 3)):
            nd.text((40, 70 + j * 75), "- " + item, font=F(40, SANS), fill=(90, 90, 110))
        nd.text((40, 300), "- MILK", font=F(54), fill=INK); nd.ellipse((22, 278, 300, 380), outline=RED, width=8)
        note = note.rotate(rot, resample=Image.BICUBIC, expand=True); kk = back(ramp(lt, 0.2 + i * 0.25, 0.5 + i * 0.25))
        if kk > 0: f.alpha_composite(note, (int(x - note.width / 2), int(y - note.height / 2 + (1 - kk) * 200)))
    return f

def store_map(f, prog, lt, items_k=0.0):
    """Ansicht von oben: Eingang unten links, Milch oben, Weg schlaengelt sich durch alle Gaenge"""
    d = ImageDraw.Draw(f, "RGBA"); d.rectangle((70, 330, 1010, 1540), fill=(240, 236, 228), outline=INK, width=8)
    d.rectangle((110, 360, 970, 450), fill=(200, 228, 255), outline=INK, width=5); txt(d, "MILK", 540, 405, 56, (40, 90, 180))
    r = random.Random(7)
    for a in range(4):
        x = 160 + a * 215; d.rectangle((x, 520, x + 120, 1390), fill=(210, 205, 196), outline=INK, width=5)
        for k in range(12): d.rectangle((x + 10, 535 + k * 71, x + 110, 590 + k * 71), fill=r.choice(PCOL), outline=INK, width=2)
    rr(d, (90, 1450, 330, 1530), GREEN, INK, 5, 14); txt(d, "ENTRANCE", 210, 1490, 36, WHITE)
    path = [(210, 1440), (210, 1430), (120, 1430), (120, 480), (300, 480), (300, 1420), (515, 1420), (515, 480), (730, 480), (730, 1420), (945, 1420), (945, 480), (700, 470)]
    L = [0]; [L.append(L[-1] + math.dist(path[i], path[i + 1])) for i in range(len(path) - 1)]; tot = L[-1] * prog
    pts = [path[0]]
    for i in range(len(path) - 1):
        if L[i + 1] <= tot: pts.append(path[i + 1])
        else:
            u = (tot - L[i]) / max(1, L[i + 1] - L[i]); pts.append((path[i][0] + (path[i + 1][0] - path[i][0]) * u, path[i][1] + (path[i + 1][1] - path[i][1]) * u)); break
    for i in range(len(pts) - 1):   # gestrichelte rote Spur
        a, b = pts[i], pts[i + 1]; seg = math.dist(a, b); n = int(seg // 40)
        for j in range(n): u0 = j / max(1, n); u1 = (j + 0.55) / max(1, n); d.line((a[0] + (b[0] - a[0]) * u0, a[1] + (b[1] - a[1]) * u0, a[0] + (b[0] - a[0]) * u1, a[1] + (b[1] - a[1]) * u1), fill=RED, width=12)
    hx, hy = pts[-1]; d.ellipse((hx - 30, hy - 30, hx + 30, hy + 30), fill=(64, 98, 156), outline=INK, width=6); d.ellipse((hx - 14, hy - 14, hx + 14, hy + 14), fill=(238, 202, 170))
    return d

def s6(lt, T, gt):   # So to get it, you have to walk past thousands of other products.
    f = studio((250, 250, 245), (232, 228, 218)); prog = ease(ramp(lt, 0.1, T - 0.1)) ** 0.9
    d = store_map(f, prog, lt)
    th = WT(6, "thousands") - SEGS[6]["t0"]
    if lt > th:
        r = random.Random(3)
        for i in range(10):
            k = back(ramp(lt, th + i * 0.07, th + i * 0.07 + 0.3))
            if k > 0:
                x = r.uniform(140, 940); y = r.uniform(560, 1360); s = 1.1 * k
                product(d, x - 30 * s, y + 45 * s, 60 * s, 90 * s, r.choice(PCOL), r.randrange(4), s)
    return f

def drop_scene(lt, T, gt, items, new_item, label_s, col_bg):
    f = studio(*col_bg); d = ImageDraw.Draw(f, "RGBA")
    person(f, LEO, 260, 1560, 120, "drop", 1, "smile" if "SALE" not in label_s else "talk")
    k = ramp(lt, 0.0, 0.32); y_drop = -300 + (1180 - (-300)) * (k * k)
    cart(d, 470, 1560, 1.25, items + ([new_item] if k >= 1 else []))
    if k < 1:
        product(d, 600, y_drop + 120, 130, 200, new_item[0], new_item[1], 2.0)
    label(d, label_s, 540, 520, 120, WHITE, ramp(lt, 0.0, 0.25)); return f

ITEMS = [((230, 60, 60), 3), ((250, 190, 40), 0), ((60, 150, 230), 2)]
def s7(lt, T, gt): return drop_scene(lt, T, gt, [], ((240, 120, 40), 3), "CHIPS", ((255, 236, 205), (255, 210, 160)))
def s8(lt, T, gt): return drop_scene(lt, T, gt, [((240, 120, 40), 3)], ((140, 90, 50), 0), "COOKIES", ((255, 232, 240), (250, 200, 220)))
def s9(lt, T, gt):
    f = drop_scene(lt, T, gt, [((240, 120, 40), 3), ((140, 90, 50), 0)], ((90, 190, 110), 1), "SALE!", ((235, 250, 235), (200, 235, 205)))
    nd = WT(9, "need") - SEGS[9]["t0"]
    if lt > nd - 0.1:
        d = ImageDraw.Draw(f, "RGBA"); stamp(f, "DIDN'T NEED", 540, 760, 76, RED, ramp(lt, nd - 0.1, nd + 0.15), 8)
    return f

def shelf_scene(lt, T, gt, mode):
    f = studio((246, 244, 238), (226, 222, 212)); d = ImageDraw.Draw(f, "RGBA")
    pay_c = {2: lambda r: r.choice([(230, 60, 60), (250, 190, 40), (60, 150, 230), (230, 90, 150)])}
    cheap = {4: lambda r: r.choice([(240, 240, 235), (215, 215, 210), (230, 225, 200)])}
    lv = dict(pay_c); lv.update(cheap)
    shelf_front(d, 60, 330, 1020, 1540, 5, 21, 1.2, lv)
    for i, y in enumerate(range(330, 1540, 242)): pass
    eye_y0, eye_y1 = 330 + 242 * 2, 330 + 242 * 3; low_y0 = 330 + 242 * 4
    if mode in ("eye", "pay"):
        k = ease(ramp(lt, 0.1, 0.4))
        d.rectangle((50, eye_y0 - 6, 1030, eye_y1 + 6), outline=YEL, width=int(14 * k) + 1)
        person(f, LEO, 900, 1880, 150, "stand", -1, "neutral")
        d.line((780, eye_y0 + 120, 120, eye_y0 + 120), fill=(60, 60, 70, int(180 * k)), width=6)
        label(d, "EYE LEVEL", 540, eye_y0 - 50, 70, YEL, k)
    if mode == "pay":
        p = WT(11, "pay") - SEGS[11]["t0"]
        for i in range(5):
            kk = back(ramp(lt, p + i * 0.08, p + i * 0.08 + 0.3))
            if kk > 0:
                x = 150 + i * 190; tag = Image.new("RGBA", (170, 90)); td = ImageDraw.Draw(tag)
                td.rounded_rectangle((4, 4, 166, 86), 14, fill=GREEN, outline=INK, width=5); td.text((85, 45), "PAID", font=F(40), fill=WHITE, anchor="mm")
                tag = tag.rotate(8 - i * 4, expand=True, resample=Image.BICUBIC); f.alpha_composite(tag, (int(x - tag.width / 2), int(eye_y0 + 30 - (1 - kk) * 120)))
    if mode == "low":
        k = ease(ramp(lt, 0.1, 0.4))
        d.rectangle((50, low_y0 - 6, 1030, 1546), outline=(150, 150, 160), width=int(14 * k) + 1)
        label(d, "CHEAPER", 540, low_y0 - 50, 76, WHITE, k)
        for i in range(3): d.polygon([(250 + i * 290, low_y0 - 160), (330 + i * 290, low_y0 - 160), (290 + i * 290, low_y0 - 100)], fill=RED)
    return f

def s10(lt, T, gt): return shelf_scene(lt, T, gt, "eye")
def s11(lt, T, gt): return shelf_scene(lt, T, gt, "pay")
def s12(lt, T, gt): return shelf_scene(lt, T, gt, "low")

def s13(lt, T, gt):  # Even the end of every aisle is paid for.
    f = aisle_bg(); f.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, 70))); d = ImageDraw.Draw(f, "RGBA")
    k = back(ramp(lt, 0.05, 0.45)); s = 1.0
    bx, by = 540, 1650
    d.rectangle((bx - 330, by - 120, bx + 330, by), fill=(200, 60, 55), outline=INK, width=8)
    for row in range(5):
        n = 6 - row
        for i in range(n):
            x = bx - n * 50 + i * 100; y = by - 120 - row * 95 - (1 - k) * 600 * (1 + row * 0.2)
            product(d, x, y, 92, 98, (250, 190, 40) if (i + row) % 2 else (230, 60, 60), 2, 1.3)
    rr(d, (bx - 260, by - 820, bx + 260, by - 690), YEL, INK, 7, 20); txt(d, "SPECIAL!", bx, by - 755, 70)
    pd = WT(13, "paid") - SEGS[13]["t0"]; stamp(f, "SPONSORED", 540, 560, 96, RED, ramp(lt, pd - 0.1, pd + 0.15), -8)
    return f

def s14(lt, T, gt):  # You came in for one thing.
    f = studio((235, 246, 255), (205, 225, 245)); d = ImageDraw.Draw(f, "RGBA")
    d.rectangle((0, 1560, W, H), fill=(214, 206, 192)); d.rectangle((60, 320, 1020, 1560), outline=(180, 190, 200), width=10)
    rr(d, (380, 330, 700, 420), GREEN, INK, 6, 14); txt(d, "OPEN", 540, 375, 50, WHITE)
    walker(f, LEO, int(330 + 60 * ease(ramp(lt, 0, T))), 1600, 150, lt, 1, "neutral")
    note = Image.new("RGBA", (300, 200)); nd = ImageDraw.Draw(note); nd.rectangle((6, 6, 294, 194), fill=(255, 252, 235), outline=INK, width=6)
    nd.text((150, 100), "MILK", font=F(70), fill=INK, anchor="mm"); note = note.rotate(-6, expand=True, resample=Image.BICUBIC)
    kk = back(ramp(lt, 0.1, 0.45)); f.alpha_composite(note, (640, int(820 + (1 - kk) * 200)))
    label(d, "1 THING", 540, 640, 110, WHITE, ramp(lt, WT(14, "one") - SEGS[14]["t0"], WT(14, "one") - SEGS[14]["t0"] + 0.25)); return f

def s15(lt, T, gt):  # And you leave with twelve...
    f = studio((255, 244, 226), (250, 220, 190)); d = ImageDraw.Draw(f, "RGBA")
    d.rectangle((0, 1180, W, 1360), fill=(70, 74, 86), outline=INK, width=8)                 # Kassenband
    for x in range(-60, W, 90): d.line(((x + lt * 400) % (W + 60) - 30, 1190, (x + lt * 400) % (W + 60) - 30, 1350), fill=(90, 94, 108), width=6)
    rr(d, (780, 900, 1040, 1180), (60, 64, 76), INK, 7, 14); d.rectangle((820, 940, 1000, 1030), fill=(30, 200, 120))
    n = 1 + int(ramp(lt, 0.0, T - 0.15) * 11); txt(d, f"{n:02d}", 910, 985, 70, (10, 40, 20))
    r = random.Random(5)
    for i in range(n):
        x = 720 - i * 70 + ((lt * 300) % 70); product(d, x, 1210, 64, 110, r.choice(PCOL), r.randrange(4), 1.0)
    rl = 200 + 80 * n; d.rectangle((60, 330, 300, 330 + rl), fill=WHITE, outline=INK, width=5)
    for j in range(n): d.line((80, 370 + j * 80, 280, 370 + j * 80), fill=(150, 150, 160), width=6)
    person(f, LEO, 520, 1900, 120, "hands_head", -1, "shock")
    label(d, f"{n} ITEMS", 640, 560, 110, WHITE, 1.0 if n > 1 else ramp(lt, 0, 0.2)); return f

def s16(lt, T, gt):  # all because the milk is at the very back of the store. (= Bild 1, Loop)
    f = aisle_bg(); d = ImageDraw.Draw(f, "RGBA")
    pul = 0.5 + 0.5 * math.sin(gt * 5); glow(f, 540, 720, 120 + 20 * pul, (200, 235, 255), 120)
    walker(f, LEO, int(230 + 110 * ease(ramp(lt, 0, T))), 1700, 150, lt, 1, "worried")
    mk = WT(16, "milk") - SEGS[16]["t0"]
    if lt > mk:
        a = ease(ramp(lt, mk, mk + 0.3)); d.line((540, 1010, 540, 870), fill=RED, width=12); d.polygon([(510, 880), (570, 880), (540, 840)], fill=RED)
        label(d, "MILK", 640, 960, 70, WHITE, a)
    banner(f, ease(ramp(lt, T - 1.2, T - 0.4)))
    return f

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16]

# ---------------- Bildaufbau ----------------
_FIN = None
def finish(img):
    global _FIN
    if _FIN is None:
        g = Image.effect_noise((W, H), 22).convert("L"); v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse((-300, -260, W + 300, H + 260), fill=255)
        _FIN = (Image.merge("RGB", (g, g, g)), v.filter(ImageFilter.GaussianBlur(260)))
    g, v = _FIN; im = Image.blend(img, g, 0.025)
    return Image.composite(im, Image.blend(im, Image.new("RGB", (W, H), (30, 26, 34)), 0.28), v)

def captions(d, gt):
    cur = max([i for i, w in enumerate(ALLW) if w[1] <= gt] or [0]); g0 = cur - cur % 3; grp = ALLW[g0:g0 + 3]
    if not grp or gt > grp[-1][2] + 0.4: return
    words = [w[0] for w in grp]; f = F(76); sp = d.textlength(" ", font=f)
    ws = [d.textlength(w, font=f) for w in words]
    while sum(ws) + sp * (len(words) - 1) > W - 100: f = F(f.size - 6); sp = d.textlength(" ", font=f); ws = [d.textlength(w, font=f) for w in words]
    x = W / 2 - (sum(ws) + sp * (len(words) - 1)) / 2
    for k, w in enumerate(words):
        d.text((x, 1640), w, font=f, fill=YEL if g0 + k == cur else WHITE, anchor="lm", stroke_width=9, stroke_fill=(0, 0, 0)); x += ws[k] + sp

def frame(gt):
    cartoon.CLOCK[0] = gt; si = 0
    for s in SEGS:
        if gt >= s["t0"] - 0.06: si = s["i"]
    s = SEGS[si]; lt = gt - s["t0"]; T = s["a1"] - s["a0"]
    f = SCENES[si](lt, T, gt)
    im = finish(f.convert("RGB")).convert("RGBA"); d = ImageDraw.Draw(im); captions(d, gt)
    return im.convert("RGB")

# ---------------- Ton: Stimme + Sounds an Aktionen + leiser Takt (keine Melodie) ----------------
def beep(n=3, f0=1150, dur=0.16, gap=0.24, g=0.07):
    out = np.zeros(int(SR * (n * (dur + gap))), np.float32); tt = np.arange(int(SR * dur)) / SR
    tone = np.sin(2 * np.pi * f0 * tt) * np.minimum(1, np.minimum(tt, dur - tt) * 80)
    for i in range(n): j = int(i * (dur + gap) * SR); out[j:j + len(tone)] += tone * g
    return out
def pulse(n, bpm=104, g=1.0):
    out = np.zeros(n, np.float32); step = 60 / bpm; tt = np.arange(int(SR * 0.18)) / SR
    kick = np.sin(2 * np.pi * (55 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 18)
    rng = np.random.default_rng(1); hat = rng.standard_normal(int(SR * 0.03)).astype(np.float32); hat = np.diff(np.concatenate([[0], hat])) * np.exp(-np.arange(len(hat)) / SR * 140)
    k = 0; t_ = 0.0
    while t_ < n / SR:
        j = int(t_ * SR)
        if k % 2 == 0: out[j:j + len(kick)] += kick[:max(0, n - j)] * 0.9
        jh = int((t_ + step / 2) * SR)
        if jh < n: out[jh:jh + len(hat)] += hat[:max(0, n - jh)] * 0.18
        t_ += step; k += 1
    return out * g
CUES = [(0, None, 0.0, "doorbell", 0.18), (2, "trucks", 0.0, "BEEP", 1.0), (2, "unload", 0.2, "paper", 0.12), (3, "true", 0.0, "stamp", 0.35),
        (4, "half", 0.0, "paper", 0.4), (5, "Milk", 0.25, "pop", 0.16), (6, "walk", 0.0, "steps", 0.18), (6, "thousands", 0.0, "pop", 0.18),
        (7, "Chips", 0.25, "pop", 0.3), (8, "Cookies", 0.25, "pop", 0.3), (9, "sale", 0.0, "pop", 0.3), (9, "need", -0.1, "stamp", 0.3),
        (10, "level", 0.0, "click", 0.25), (11, "pay", 0.0, "coins", 0.22), (12, "feet", -0.2, "whoosh", 0.18), (13, "paid", -0.1, "stamp", 0.32),
        (14, "one", 0.0, "ding", 0.2), (15, "leave", 0.0, "SCAN", 1.0), (16, "milk", 0.0, "whoosh", 0.12)]
def audio():
    n = int(TOTAL * SR) + SR; v = np.zeros(n, np.float32); fx = np.zeros(n, np.float32)
    for s in SEGS:
        a = RAW[int(s["a0"] * SR):int(s["a1"] * SR)].copy(); fl = SR // 200; a[:fl] *= np.linspace(0, 1, fl); a[-fl:] *= np.linspace(1, 0, fl)
        i = int(s["t0"] * SR); v[i:i + len(a)] += a
    for si, w, off, name, g in CUES:
        tt = (SEGS[si]["t0"] if w is None else WT(si, w)) + off; j = max(0, int(tt * SR))
        if name == "BEEP": x = beep()
        elif name == "SCAN": x = np.concatenate([SFXL.load("scanner")[:int(0.25 * SR)] * 0.22 for _ in range(4)])
        else: x = SFXL.load(name) * g
        x = x[:max(0, n - j)]; fx[j:j + len(x)] += x
    cs = np.concatenate([[0.0], np.cumsum(np.abs(v), dtype=np.float64)]); idx = np.arange(n)
    lo, hi = np.clip(idx - 2400, 0, n), np.clip(idx + 2400, 0, n); vabs = ((cs[hi] - cs[lo]) / 4800).astype(np.float32)
    pu = pulse(n); pu *= 0.02 / (np.sqrt(np.mean(pu ** 2)) + 1e-9); pu *= (1 - 0.35 * np.clip(vabs / 0.05, 0, 1))
    fi = int(0.3 * SR); pu[:fi] *= np.linspace(0, 1, fi); pu[-fi:] *= np.linspace(1, 0, fi)
    rng = np.random.default_rng(7); amb = np.cumsum(rng.standard_normal(n)).astype(np.float32)   # Laden-Atmo (Brown-Noise, keine Melodie)
    amb -= np.convolve(amb, np.ones(4800) / 4800, "same"); amb *= 0.009 / (np.sqrt(np.mean(amb ** 2)) + 1e-9); amb[:fi] *= np.linspace(0, 1, fi); amb[-fi:] *= np.linspace(1, 0, fi)
    out = v * 1.05 + fx + pu + amb; m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)]

if __name__ == "__main__":
    print(f"Laenge {TOTAL:.1f}s")
    if "--stills" in sys.argv:
        tiles = []
        for s in SEGS:
            for fr in (0.3, 0.85): tiles.append(frame(s["t0"] + (s["a1"] - s["a0"]) * fr).resize((216, 384)))
        cols = 9; rows = math.ceil(len(tiles) / cols); sh = Image.new("RGB", (216 * cols, 384 * rows))
        for i, t_ in enumerate(tiles): sh.paste(t_, ((i % cols) * 216, (i // cols) * 384))
        sh.save("STORYBOARD.jpg", quality=85); print("ok"); sys.exit()
    out = av.open("ARC_Short05_Milk.mp4", "w"); vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "19", "preset": "medium"}
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
    out.close(); print("ok", TOTAL)
