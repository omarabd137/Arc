"""ARC Short – „The Man Who Sold 10% Of Apple For $800“ (Ron Wayne).
Masterplan Teil 22: Satz 1 ab 0 s, zweites Raetsel (500 Mrd.) bei 3-6 s, heisse Fakten, Requisiten genau,
Bewegung logisch (gelaufen wird nur mit Ortswechsel), Untertitel mit gelben Schluesselwoertern, Loop.
Aufruf aus shorts/03_ronwayne:  python short03.py [--stills]"""
import sys, os, math, random
from apple_kit import *
from logo_kit import apple_logo, apple_logo_slice, logo_1976_v2
from likeness import person2, JOBS76, WOZ76, WAYNE76, WAYNE_NOW
WAYNE, WAYNE_OLD, JOBS, WOZ = WAYNE76, WAYNE_NOW, JOBS76, WOZ76
person = person2
sys.path.insert(0, os.path.join(HERE, "..", "01_lamborghini", "v7"))
import numpy as np, av
import sfx
from crayon2 import bust
from crayon3 import LIMB
os.chdir(HERE)

FPS, SR = 30, 48000
CAP_FONT = ImageFont.truetype(F + "ariblk.ttf", 72)
GREY = (226, 224, 220)

NARR = np.load("vo/narr_all.npy")
SEG = [(0.06, 2.2), (2.88, 4.72), (5.46, 8.72), (9.48, 12.08), (12.64, 14.88), (15.5, 17.62), (18.44, 22.34), (22.84, 23.88),
       (24.58, 29.94), (30.66, 33.94), (34.66, 37.58)]
def cut(i):
    s, e = SEG[i]; a = NARR[max(0, int((s - 0.04) * SR)):int((e + 0.06) * SR)].copy()
    f = int(0.015 * SR); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f); return a

LINES = [
    ("This man owned ten percent of Apple...", {"ten", "percent"}, 0.1),
    ("and sold it for 800 dollars.", {"800"}, 0.22),
    ("Today, that ten percent is worth about 500 billion.", {"500", "billion."}, 0.25),
    ("Ron Wayne was Apple's forgotten third founder.", {"forgotten"}, 0.2),
    ("He even drew Apple's very first logo.", {"first", "logo."}, 0.2),
    ("But just twelve days later, he quit.", {"twelve", "days", "quit."}, 0.25),
    ("You see, if Apple went broke, Wayne was the only one with a house to lose.", {"broke,", "house"}, 0.15),
    ("So he walked away.", {"away."}, 0.3),
    ("Years later, he even sold his copy of Apple's founding contract... for 500 dollars.", {"contract...", "500"}, 0.25),
    ("It later sold at auction for over 1.5 million.", {"1.5", "million."}, 0.35),
    ("And Ron Wayne says... he has no regrets.", {"no", "regrets."}, 0.6),
]
TL, t0 = [], 0.0
for i, (txt, hl, gap) in enumerate(LINES):
    a = cut(i); TL.append(dict(i=i, a=a, txt=txt, hl=hl, t0=t0, dur=len(a) / SR, end=t0 + len(a) / SR + gap)); t0 = TL[-1]["end"]
TOTAL = t0
CAP_Y = {6: 1180, 7: 1180}       # Strassen-Szenen: Untertitel ueber den Koepfen

def chunks(c):
    words = c["txt"].split(); out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w[-1] in ",.!?" or (len(cur) == 2 and len(" ".join(cur)) > 13): out.append(cur); cur = []
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
        d0 = ImageDraw.Draw(Image.new("L", (1, 1))); sp = d0.textlength(" ", font=CAP_FONT); ws = [d0.textlength(w, font=CAP_FONT) for w in words]
        im = Image.new("RGBA", (int(sum(ws) + sp * (len(ws) - 1)) + 40, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 20
        for w, wl in zip(words, ws):
            d.text((x, 10), w, font=CAP_FONT, fill=((255, 214, 60) if w in hl else (255, 255, 255)) + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255)); x += wl + sp
        _cap[key] = im
    return _cap[key]

_spr = {}
def sprite(key, fn):
    if key not in _spr:
        c = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); fn(c); bb = c.getbbox() or (0, 0, 2, 2)
        im = c.crop(bb).resize((max(1, (bb[2] - bb[0]) // SS), max(1, (bb[3] - bb[1]) // SS)), Image.LANCZOS)
        _spr[key] = (im, bb[0] // SS, bb[1] // SS)
    return _spr[key]

def put(frame, spr, dx=0, dy=0, scale=1.0, alpha=1.0):
    im, x, y = spr
    if scale != 1.0:
        im2 = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale)))); x, y, im = x + (im.width - im2.width) / 2, y + (im.height - im2.height) / 2, im2
    if alpha < 1.0: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    frame.paste(im, (int(x + dx), int(y + dy)), im)

_bg = {}
def bg(key, fn):
    if key not in _bg:
        im = fn(); _bg[key] = (im.resize((W, H), Image.LANCZOS) if im.size[0] > W else im).convert("RGB")
    return _bg[key]

def walker(p, R, face, phase, mouth, brow, arms, seed, cx, base, pockets=False):
    def fn(c):
        d = ImageDraw.Draw(c, "RGBA"); leg, tor_w = R * 1.25, R * 1.05 * p["big"]; hip = base - leg
        d.ellipse(S(cx - R * 0.9, base - 10, cx + R * 0.9, base + 10), fill=(0, 0, 0, 55))
        for sx in (-1, 1):
            ph = 2 * math.pi * ((phase or 0) + (0.5 if sx > 0 else 0)); x = cx + sx * tor_w * 0.28
            fx = x + (math.sin(ph) * R * 0.38 if phase is not None else sx * 4)
            fy = base - (max(0, math.cos(ph)) * R * 0.1 if phase is not None else 0)
            stroke(d, [(x, hip - 10), (fx, fy)], lw=LIMB); stroke(d, [(fx, fy), (fx + face * 22, fy)], lw=LIMB)
        person(c, cx, base, R, p, face=face, mouth=mouth, brow=brow, arms=arms, seed=seed, seated=True)
        if pockets:      # leere Hosentaschen nach aussen gestuelpt
            d = ImageDraw.Draw(c, "RGBA")
            for sx in (-1, 1): shape(d, [(cx + sx * R * 0.5, hip - R * 0.25), (cx + sx * R * 0.78, hip - R * 0.2), (cx + sx * R * 0.72, hip + R * 0.12), (cx + sx * R * 0.5, hip + R * 0.05)], (246, 244, 238), seed + 5 + sx, lw=3)
    return fn

def fig(frame, p, x, base, R, face, walking=False, lt=0.0, mouth="line", brow=0.0, arms=("down", "down"), seed=1, alpha=1.0, pockets=False):
    """walking=True nur zusammen mit Ortswechsel (x aendert sich) verwenden."""
    ph = (round((lt * 2.0) % 1 * 8) % 8) / 8 if walking else None
    spr = sprite(("fig", id(p), R, face, ph, mouth, brow, arms, seed, base, pockets), walker(p, R, face, ph, mouth, brow, arms, seed, 540, base, pockets))
    put(frame, spr, x - 540, -abs(math.sin(2 * math.pi * ph)) * R * 0.06 if walking else 0, alpha=alpha)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def note(frame, lines, cx, cy, angle=-4, w=420, p=1.0):
    spr = sprite(("note", tuple(lines), cx, cy, angle, w), lambda c: sticky(c, cx, cy, lines, angle=angle, w=w))
    if p > 0: put(frame, spr, scale=0.6 + 0.4 * ease(p / 0.25) if p < 0.25 else 1.0)
def big(frame, s, cx, cy, size, k=1.0, color=(255, 214, 60)):
    f = ImageFont.truetype(BOLD, int(size * (0.7 + 0.3 * ease(k)))); ImageDraw.Draw(frame).text((cx, cy), s, font=f, fill=color, anchor="mm", stroke_width=10, stroke_fill=INK)

# ---------------- Hintergruende ----------------
def grey_bg():
    img = Image.new("RGB", (W, H), GREY); d = ImageDraw.Draw(img)
    d.ellipse([140, 1640, 940, 1760], fill=(206, 204, 200)); return img
def park_bg():
    img = Image.new("RGB", (W * SS, H * SS)); grad(img, (120, 160, 110), (150, 186, 130), 0, H); apple_park(img, 540, 1000, 430); return img
def desk_bg():
    img = Image.new("RGB", (W * SS, H * SS), (120, 92, 68)); d = ImageDraw.Draw(img, "RGBA")
    for k in range(14): stroke(d, [(0, 80 + k * 140), (W, 100 + k * 140)], lw=3, color=(104, 78, 58))
    return img
def street_bg():
    img = Image.new("RGB", (W * SS, H * SS)); grad(img, (150, 200, 236), (214, 232, 244), 0, 1400); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, 1400), (W + 20, 1400), (W + 20, H + 20), (-20, H + 20)], (150, 186, 120), 1, lw=4)              # Rasen
    shape(d, [(-20, 1640), (W + 20, 1640), (W + 20, 1760), (-20, 1760)], (196, 192, 184), 2, lw=4)                 # Gehweg
    for x in range(0, W, 140): stroke(d, [(x, 1640), (x, 1760)], lw=2, color=(170, 166, 160))
    shape(d, [(-20, 1760), (W + 20, 1760), (W + 20, H + 20), (-20, H + 20)], (110, 110, 116), 3, lw=4)            # Strasse
    house(d, 560, 1400, 470, 50)
    shape(d, ellipse_pts(150, 1120, 150, 200), (96, 146, 84), 60, lw=4); stroke(d, [(150, 1300), (150, 1400)], lw=26, color=(120, 90, 60))
    return img
def calendar_bg():
    img = Image.new("RGB", (W * SS, H * SS), (196, 188, 176)); d = ImageDraw.Draw(img, "RGBA")
    for k in range(5): stroke(d, [(k * 270, 0), (k * 270, H)], lw=2, color=(184, 176, 164))
    return img

# ---------------- Einstellungen ----------------
APPLE_C = (720, 1220, 220)
def apple_spr(missing=True): return sprite(("logo_apple", missing), lambda c: apple_logo(c, *APPLE_C, slice_missing=missing))
def slice_spr(): return sprite(("logo_slice",), lambda c: apple_logo_slice(c, *APPLE_C))

def sh_owned(f, lt, T):
    put(f, apple_spr(True))
    k = ease((lt - 0.35) / 0.8)
    put(f, slice_spr(), -380 * k, 270 * k - math.sin(k * math.pi) * 160 + (math.sin(lt * 3) * 6 if k >= 1 else 0))          # Wayne haelt sein Zehntel
    fig(f, WAYNE, 230, 1720, 120, 1, mouth="smile", arms=("down", "rest"), seed=11)

def sh_sold(f, lt, T):
    put(f, apple_spr(True))
    k = ease(lt / 0.6)
    put(f, slice_spr(), -380 + k * 1300, 270 - k * 400)               # das Stueck geht weg
    fig(f, WAYNE, 230, 1720, 120, 1, mouth="line", arms=("down", "rest"), seed=11)
    for i in range(8):                                                                # 8 x 100 $ kommen an
        kk = ease((lt - 0.4 - i * 0.08) / 0.35)
        if kk <= 0: continue
        put(f, sprite(("bill", i), lambda c, i=i: dollar_bill(c, 390 + i * 6, 1250 - i * 10, 300, angle=-8 + i * 2, value="100")), (1 - kk) * 800, -(1 - kk) * 200)
    if lt > 0.9: big(f, "$800", 540, 640, 230, (lt - 0.9) / 0.25)

def sh_worth(f, lt, T):
    v = int(500_000_000_000 * ease(lt / (T * 0.8)))
    big(f, f"${v:,}", 540, 460, 96, 1.0)
    note(f, ["APPLE TODAY", "Cupertino, California"], 540, 1790, angle=3, w=640, p=lt)

def sh_forgotten(f, lt, T):
    fig(f, JOBS, 250, 1700, 108, 1, mouth="smile", seed=21)
    fig(f, WOZ, 540, 1720, 116, 1, mouth="smile", seed=22)
    fig(f, WAYNE, 830, 1700, 108, -1, mouth="line", seed=23, alpha=1.0 - 0.6 * ease((lt - T * 0.45) / 0.6))
    note(f, ["STEVE JOBS"], 230, 1130, angle=-4, w=280, p=lt)
    note(f, ["WOZNIAK"], 540, 1090, angle=3, w=260, p=lt - 0.15)
    note(f, ["RON WAYNE"], 850, 1130, angle=-3, w=280, p=lt - 0.3)

def sh_logo(f, lt, T):
    r = min(1, lt / (T * 0.85))
    put(f, sprite(("logo2", round(r * 40)), lambda c, r=r: logo_1976_v2(c, 540, 900, 700, reveal=round(r * 40) / 40)))
    y = 440 + 920 * r; x = 540 + math.sin(lt * 9) * 220                  # Federkiel zeichnet an der Kante entlang
    d = ImageDraw.Draw(f, "RGBA")
    d.polygon([(x, y), (x + 10, y - 26), (x - 4, y - 30)], fill=(190, 190, 196), outline=INK)                  # Metallspitze
    d.polygon([(x - 4, y - 30), (x + 10, y - 26), (x + 150, y - 270), (x + 130, y - 280)], fill=(44, 46, 54), outline=INK)   # Stift
    note(f, ["1976"], 860, 230, angle=4, w=240, p=lt)

def sh_days(f, lt, T):
    day = 1 + min(11, int(11 * lt / (T * 0.7)))
    put(f, sprite(("cal", day), lambda c, day=day: calendar(c, 540, 900, 620, day)))
    if lt > T * 0.7: big(f, "12 DAYS", 540, 1330, 150, (lt - T * 0.7) / 0.2)

def sh_house(f, lt, T):
    fig(f, JOBS, 160, 1820, 92, 1, mouth="smile", arms=("down", "down"), seed=31, pockets=True)
    fig(f, WOZ, 360, 1830, 98, 1, mouth="smile", arms=("down", "down"), seed=32, pockets=True)
    fig(f, WAYNE, 760, 1830, 100, -1, mouth="frown", brow=0.12, seed=33)
    if lt > T * 0.3:
        d = ImageDraw.Draw(f, "RGBA"); rnd = random.Random(7)
        for i in range(6):
            k = ease((lt - T * 0.3 - i * 0.1) / 0.6)
            if k <= 0: continue
            x = -80 + (rnd.randint(640, 980) + 80) * k; y = 700 + rnd.randint(-80, 280) - 200 * math.sin(k * math.pi) * 0.5
            put(f, sprite(("debt", i), lambda c, i=i: (shape(ImageDraw.Draw(c, "RGBA"), [(460, 900), (600, 900), (600, 1080), (460, 1080)], (250, 248, 240), 900 + i, lw=4),
                                                     text(c, "DEBT", 530, 950, 34, BOLD, RED))), x - 530, y - 990)

def sh_walk(f, lt, T):
    x = 380 + 900 * min(1, lt / (T + 0.2))                                            # er geht wirklich aus dem Bild
    fig(f, WAYNE, x, 1830, 104, 1, walking=True, lt=lt, mouth="line", seed=34)

def sh_contract(f, lt, T):
    k = ease((lt - T * 0.55) / 0.5)
    put(f, sprite(("pc",), lambda c: partnership_contract(c, 540, 840, 640)), k * 900, -k * 80)
    for i in range(5):
        kk = ease((lt - T * 0.62 - i * 0.08) / 0.35)
        if kk <= 0: continue
        put(f, sprite(("bill5", i), lambda c, i=i: dollar_bill(c, 520 + i * 8, 1300 - i * 10, 340, angle=-6 + i * 3, value="100")), -(1 - kk) * 800, 0)
    if lt > T * 0.78: big(f, "$500", 540, 1640, 200, (lt - T * 0.78) / 0.2)

def sh_auction(f, lt, T):
    v = int(1_500_000 * ease(lt / (T * 0.75)))
    big(f, f"${v:,}", 540, 515, 78, 1.0, color=(255, 214, 60))
    put(f, sprite(("pcs",), lambda c: partnership_contract(c, 540, 840, 150)), 200, 20)
    fig(f, P(hair=(90, 80, 70), top=(40, 40, 50), tie=(150, 40, 44), clear_glasses=True), 280, 1180, 70, 1, mouth="smile", arms=("rest", "point"), seed=41)
    d = ImageDraw.Draw(f, "RGBA")
    ang = 60 if lt < T * 0.85 else 60 - 50 * ease((lt - T * 0.85) / 0.1)
    put(f, sprite(("gavel", int(ang)), lambda c, a=ang: gavel(ImageDraw.Draw(c, "RGBA"), 360, 990, a)))
    rnd = random.Random(3)
    for j in range(8):          # Bieter von hinten, Paddel gehen hoch
        x = 120 + j * 120; up = (math.sin(lt * 5 + j * 1.7) > 0.3)
        put(f, sprite(("head", j % 4), lambda c, j=j: shape(ImageDraw.Draw(c, "RGBA"), ellipse_pts(540, 1600, 62, 62), [(60, 44, 36), (200, 170, 90), (40, 34, 30), (110, 70, 44)][j % 4], 300 + j)), x - 540, (j % 2) * 40)
        if up:
            d.line([(x + 40, 1560 + (j % 2) * 40), (x + 50, 1420 + (j % 2) * 40)], fill=INK, width=8)
            d.ellipse([x + 10, 1360 + (j % 2) * 40, x + 90, 1440 + (j % 2) * 40], fill=(250, 248, 240), outline=INK, width=6)

def sh_regrets(f, lt, T):
    rock = math.sin(lt * 2.2) * 10
    put(f, sprite(("chair",), lambda c: rocking_chair(ImageDraw.Draw(c, "RGBA"), 560, 1800, 520)), 0, rock * 0.4)
    put(f, sprite(("oldwayne",), lambda c: person(c, 560, 1560, 120, WAYNE_OLD, face=1, mouth="smile", arms=("rest", "rest"), seed=51, seated=True)), 0, rock * 0.4)
    put(f, sprite(("apple_small",), lambda c: apple_logo(c, 710, 1330, 80, slice_missing=True)), 0, rock * 0.4)

SHOTS = {0: (0, "grey", grey_bg, sh_owned), 1: (0, "grey", grey_bg, sh_sold), 2: (0, "park", park_bg, sh_worth),
         3: (0, "garage", garage_bg, sh_forgotten), 4: (0, "desk", desk_bg, sh_logo), 5: (0, "cal", calendar_bg, sh_days),
         6: (0, "street", street_bg, sh_house), 7: (0, "street", street_bg, sh_walk), 8: (0, "desk", desk_bg, sh_contract),
         9: (0, "auction", auction_bg, sh_auction), 10: (0, "porch", porch_bg, sh_regrets)}

def frame_at(gt):
    if gt >= TL[-1]["t0"] + TL[-1]["dur"] + 0.2:      # Loop: die letzten Frames zeigen exakt das erste Bild
        f = bg("grey", grey_bg).copy().convert("RGBA"); sh_owned(f, 0.0, 1.0); return f.convert("RGB")
    ci = max(i for i, c in enumerate(TL) if c["t0"] <= gt) if gt >= TL[0]["t0"] else 0
    c = TL[ci]; lt = gt - c["t0"]; _, key, fn, shot = SHOTS[c["i"]]
    f = bg(key, fn).copy().convert("RGBA"); shot(f, lt, c["dur"])
    for a, b, words in c["chunks"]:
        if a <= lt < b + (0.3 if words is c["chunks"][-1][2] else 0):
            im = caption(words, c["hl"]); k = min(1, (lt - a) / 0.08)
            if k < 1: im = im.resize((max(1, int(im.width * (0.85 + 0.15 * k))), max(1, int(im.height * (0.85 + 0.15 * k)))))
            f.alpha_composite(im, (int((W - im.width) / 2), int(CAP_Y.get(c["i"], 1500) - im.height / 2)))
    return f.convert("RGB")

# ---------------- Ton ----------------
def pop_sfx(): t = sfx.t(0.12); return sfx.norm(np.sin(2 * np.pi * (500 - 1800 * t) * t) * np.exp(-t * 40), 0.4)
def pen(d=1.6): x = sfx.band(sfx.noise(d), 2500, 8000) * (0.4 + 0.6 * (np.sin(2 * np.pi * 9 * sfx.t(d)) > 0)); return sfx.norm(x * np.minimum(1, (d - sfx.t(d)) / 0.2), 0.3)
def flip(): return sfx.norm(sfx.band(sfx.noise(0.12), 1500, 7000) * np.exp(-sfx.t(0.12) * 30), 0.35)
def step(): t = sfx.t(0.12); return sfx.norm(sfx.band(sfx.noise(0.12), 80, 900) * np.exp(-t * 45), 0.5)

def mix():
    n = int((TOTAL + 0.5) * SR); voice = np.zeros(n, np.float32); fx = np.zeros(n, np.float32)
    def add(buf, s, x, g):
        i = int(max(0, s) * SR); x = x[:max(0, n - i)]; buf[i:i + len(x)] += x * g
    for c in TL: add(voice, c["t0"], c["a"], 1.0)
    T = TL
    add(fx, T[1]["t0"], sfx.whoosh(0.5), 0.4); add(fx, T[1]["t0"] + 0.4, sfx.rustle(1.0), 0.5); add(fx, T[1]["t0"] + 0.9, sfx.thud(0.5, 60), 0.6)
    add(fx, T[2]["t0"] - 0.05, sfx.boom(1.6), 0.7)
    add(fx, T[3]["t0"] + T[3]["dur"] * 0.45, sfx.whoosh(0.6), 0.25)
    add(fx, T[4]["t0"], pen(T[4]["dur"]), 0.4)
    for k in range(11): add(fx, T[5]["t0"] + k * T[5]["dur"] * 0.7 / 11, flip(), 0.4)
    add(fx, T[5]["t0"] + T[5]["dur"] * 0.7, sfx.thud(0.5, 55), 0.6)
    for k in range(6): add(fx, T[6]["t0"] + T[6]["dur"] * 0.3 + k * 0.1, sfx.whoosh(0.3), 0.15)
    for k in range(int(T[7]["dur"] * 4) + 2): add(fx, T[7]["t0"] + k * 0.25, step(), 0.35)
    add(fx, T[8]["t0"] + T[8]["dur"] * 0.55, sfx.whoosh(0.5), 0.35); add(fx, T[8]["t0"] + T[8]["dur"] * 0.62, sfx.rustle(0.8), 0.45)
    add(fx, T[9]["t0"], sfx.crowd(T[9]["dur"] + 0.4, 0.3), 0.4); add(fx, T[9]["t0"] + T[9]["dur"] * 0.93, sfx.thud(0.5, 110), 0.8)
    add(fx, T[10]["t0"], sfx.crowd(0.1, 0.0) * 0, 0)
    mus = sfx.music(TOTAL + 0.5, hits=(T[2]["t0"] - 0.05, T[6]["t0"]), swell_at=T[9]["t0"])
    mus = np.pad(mus, (0, max(0, n - len(mus))))[:n]
    ci = int(T[10]["t0"] * SR); fd = int(0.3 * SR); mus[ci:ci + fd] *= np.linspace(1, 0.35, fd)[:len(mus[ci:ci + fd])]; mus[ci + fd:] *= 0.35
    vabs = np.convolve(np.abs(voice), np.ones(4800) / 4800, "same"); duck = 1 - 0.45 * np.clip(vabs / 0.05, 0, 1)
    out = voice + fx + mus * 0.16 * duck; m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)].astype(np.float32)

if __name__ == "__main__":
    print(f"Laenge {TOTAL:.1f} s")
    if "--stills" in sys.argv:
        os.makedirs("stills", exist_ok=True)
        tiles = [frame_at(c["t0"] + c["dur"] * fr) for c in TL for fr in (0.3, 0.9)]
        for i, im in enumerate(tiles): im.save(f"stills/{i:02d}.png")
        tw, th, cols = 216, 384, 8
        sheet = Image.new("RGB", (cols * (tw + 6) + 6, ((len(tiles) + cols - 1) // cols) * (th + 6) + 6))
        for i, t in enumerate(tiles): sheet.paste(t.resize((tw, th)), (6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + 6)))
        sheet.save("STORYBOARD_03.png"); print("stills ok"); sys.exit()
    audio = mix()
    out = av.open("ARC_Short_RonWayne.mp4", "w")
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
