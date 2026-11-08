"""16:9-Kit fuer ARC-Longform (1920x1080, intern 2x): Sprites, Hintergruende, Requisiten, Figuren.
Crayon-Prinzip: Figuren simpel, Orte und Requisiten genau und erkennbar, gedaempfte Farben, Tusche-Konturen."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("../../shorts/01_lamborghini", "../../shorts/02_mcdonalds", "../../shorts/03_ronwayne"):
    sys.path.insert(0, os.path.join(HERE, p))
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from crayon_kit import S, sh, shape, stroke, ellipse_pts, SS, INK
from crayon3 import figure, sticky
from crayon2 import bust
from mcd_kit import dollar_bill, text, BOLD, SERIF, HAND, SCRIPT, RED, YEL, WHITE
from apple_kit import house, P, WOOD, WOOD_D
from likeness import person2

W, H = 1920, 1080
F = "C:/Windows/Fonts/"
GREY_BG = (226, 224, 220)
GREEN, DRED, GOLD = (60, 150, 90), (200, 50, 50), (240, 190, 40)

# ---------------- Figuren ----------------
JAKE = P(hair=(120, 80, 50), hair_hi=(170, 120, 84), top=(200, 70, 60), skin=(240, 204, 170), big=1.0)        # roter Hoodie, braunes Haar
JAKE45 = P(hair=(104, 72, 48), hair_hi=(150, 110, 80), top=(150, 70, 64), skin=(236, 198, 164), big=1.08)
RYAN = P(hair=(30, 26, 24), hair_hi=(80, 70, 64), top=(150, 186, 220), skin=(214, 168, 128), big=0.96)          # hellblaues Hemd, dunkles Haar
RYAN45 = P(hair=(56, 50, 48), hair_hi=(120, 110, 104), top=(150, 186, 220), tie=(40, 60, 100), skin=(212, 166, 126), big=0.98)
BANKER = P(hair=(80, 70, 66), top=(50, 54, 66), tie=(150, 40, 44), skin=(236, 200, 166), clear_glasses=True, look="wayne")
TELLER = P(hair=(150, 90, 50), top=(70, 90, 130), skin=(240, 206, 176), big=0.95)
BILLIONAIRE = P(hair=(200, 200, 204), hair_hi=(240, 240, 244), top=(30, 32, 40), tie=(30, 32, 40), skin=(236, 202, 172), big=1.02)
CHILD = P(hair=(200, 160, 90), top=(120, 170, 130), skin=(242, 208, 176), big=0.9)
CROWD = [P(hair=h, top=t, skin=sk) for h, t, sk in [((60, 44, 36), (110, 130, 170), (236, 196, 160)), ((30, 26, 24), (180, 120, 100), (190, 140, 104)),
         ((200, 160, 90), (120, 160, 120), (242, 208, 178)), ((90, 60, 40), (170, 150, 110), (220, 176, 136)), ((40, 34, 30), (130, 110, 160), (176, 126, 92))]]

def fig_fn(p, cx, base, R, face=1, mouth="line", brow=0.0, arms=("down", "down"), seed=1, seated=False, walk=None):
    """walk = Phase 0..1 (nur bei echter Fortbewegung) oder None."""
    def fn(c):
        d = ImageDraw.Draw(c, "RGBA")
        if walk is not None or not seated:
            leg, tor_w = R * 1.25, R * 1.05 * p["big"]; hip = base - leg
            d.ellipse(S(cx - R * 0.9, base - 10, cx + R * 0.9, base + 10), fill=(0, 0, 0, 55))
            for sx in (-1, 1):
                ph = 2 * math.pi * ((walk or 0) + (0.5 if sx > 0 else 0)); x = cx + sx * tor_w * 0.28
                fx = x + (math.sin(ph) * R * 0.38 if walk is not None else sx * 4)
                fy = base - (max(0, math.cos(ph)) * R * 0.1 if walk is not None else 0)
                stroke(d, [(x, hip - 10), (fx, fy)], lw=7); stroke(d, [(fx, fy), (fx + face * 22, fy)], lw=7)
        person2(c, cx, base, R, p, face=face, mouth=mouth, brow=brow, arms=arms, seed=seed, seated=True)
    return fn

# ---------------- Uhr + Sound-Ereignisse (vom Renderer gesetzt) ----------------
CLK = {"t": 0.0, "beat": -1}
EVENTS = []            # (zeit, sound, lautstaerke, art)  art: "auto" (wird ausgeduennt) oder "steps"
_seen, _steps = set(), {}
LBOX = []              # Rahmen aller Texte/Notizen im aktuellen Bild (Kamera darf sie nie abschneiden)
def sfx_event(key, name, gain, kind="auto"):
    if key in _seen: return
    _seen.add(key); EVENTS.append((CLK["t"], name, gain, kind))

# ---------------- Sprite-Cache ----------------
_spr, _bg = {}, {}
def canvas(color=(0, 0, 0, 0), mode="RGBA"):
    return Image.new(mode, (W * SS, H * SS), color)

def sprite(key, fn):
    if key not in _spr:
        c = canvas(); fn(c); bb = c.getbbox() or (0, 0, 2, 2)
        im = c.crop(bb).resize((max(1, (bb[2] - bb[0]) // SS), max(1, (bb[3] - bb[1]) // SS)), Image.LANCZOS)
        _spr[key] = (im, bb[0] // SS, bb[1] // SS)
    return _spr[key]

def put(frame, spr, dx=0, dy=0, scale=1.0, alpha=1.0, rot=0):
    im, x, y = spr
    if scale != 1.0 or rot:
        w0, h0 = im.width, im.height
        if scale != 1.0: im = im.resize((max(1, int(w0 * scale)), max(1, int(h0 * scale))))
        if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
        x, y = x + (w0 - im.width) / 2, y + (h0 - im.height) / 2
    if alpha < 1.0:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * max(0, alpha))))
    frame.paste(im, (int(x + dx), int(y + dy)), im)

def bg(key, fn):
    if key not in _bg:
        im = fn(); _bg[key] = (im.resize((W, H), Image.LANCZOS) if im.size[0] > W else im).convert("RGB")
    return _bg[key]

def fig(frame, p, x, base, R, face=1, mouth="line", brow=0.0, arms=("down", "down"), seed=1, seated=False, walk_t=None, alpha=1.0):
    """Figur bei x zeichnen. walk_t (Sekunden) nur angeben, wenn sie sich wirklich bewegt.
    Lebendig: atmet (leichtes Wippen), blinzelt, macht ab und zu eine kleine Geste (Hand an die Huefte)."""
    t = CLK["t"]; ph = (round((walk_t * 2.0) % 1 * 8) % 8) / 8 if walk_t is not None else None
    if ph is None and arms == ("down", "down") and not seated:
        cyc = (t + seed * 1.37) % 5.5
        if 2.2 < cyc < 3.6: arms = ("down", "hip") if face == 1 else ("hip", "down")
    spr = sprite(("fig", id(p), R, face, mouth, brow, arms, seed, seated, ph, base), fig_fn(p, 960, base, R, face, mouth, brow, arms, seed, seated, ph))
    if ph is not None:
        dy = -abs(math.sin(2 * math.pi * ph)) * R * 0.06
        k = (CLK["beat"], id(p), seed); last = _steps.get(k, -9)
        if t - last >= 1.0: _steps[k] = t; EVENTS.append((t, "steps", 0.16, "steps"))
    else:
        dy = math.sin(2 * math.pi * 0.45 * t + seed) * R * (0.012 if seated else 0.022)
    put(frame, spr, x - 960, dy, alpha=alpha)
    if alpha >= 0.99 and not p.get("glasses") and not p.get("clear_glasses") and (t + seed * 0.61) % 3.9 < 0.13:
        d = ImageDraw.Draw(frame, "RGBA"); hcy = base - R * 3.38 + dy; ex = x + face * R * 0.24; ey = hcy + R * 0.05
        for k in (-1, 1):
            gx = ex + k * R * 0.26
            d.ellipse([gx - R * 0.07, ey - R * 0.085, gx + R * 0.07, ey + R * 0.085], fill=p["skin"])
            d.line([(gx - R * 0.06, ey + R * 0.01), (gx + R * 0.06, ey + R * 0.01)], fill=INK, width=max(2, int(R * 0.035)))

def bust_spr(frame, p, cx, hy, R, face=1, mouth="smile", brow=0.0, eyes="open", seed=1, dx=0, dy=0):
    put(frame, sprite(("bust", id(p), cx, hy, R, face, mouth, brow, eyes, seed), lambda c: bust(c, cx, hy, R, p, face=face, eyes=eyes, mouth=mouth, brow=brow, seed=seed)), dx, dy)

# ---------------- Helfer ----------------
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def inout(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def pop(x): x = max(0.0, min(1.0, x)); return 0.6 + 0.4 * ease(x / 0.6) + 0.12 * math.sin(min(1, x) * math.pi)

def grad16(img, top, bottom, y0=0, y1=H):
    d = ImageDraw.Draw(img)
    for y in range(int(y0 * SS), int(y1 * SS)):
        k = (y - y0 * SS) / max(1, (y1 - y0) * SS)
        d.line([(0, y), (W * SS, y)], fill=tuple(int(a + (b - a) * k) for a, b in zip(top, bottom)))

def label(frame, s, cx, cy, size, color=(255, 214, 60), k=1.0, stroke_w=8, font=BOLD):
    """Grosse Zahl/Label direkt ins Bild (1x-Koordinaten), skaliert beim Erscheinen."""
    if k <= 0: return
    if size >= 90 and k < 0.5:        # nur grosse, wichtige Einblendungen bekommen (ggf.) einen dezenten Sound
        red = color[0] > 230 and color[1] < 140 and color[2] < 140
        sfx_event((CLK["beat"], int(cx) // 40, int(cy) // 40), "impact" if size >= 200 else ("stinger" if red else "pop"),
                  0.32 if size >= 200 else (0.22 if red else 0.2))
    f = ImageFont.truetype(font, max(8, int(size * pop(k))))
    ImageDraw.Draw(frame).text((cx, cy), s, font=f, fill=color, anchor="mm", stroke_width=stroke_w, stroke_fill=INK)
    LBOX.append(ImageDraw.Draw(frame).textbbox((cx, cy), s, font=f, anchor="mm", stroke_width=stroke_w))

def hand_label(frame, s, cx, cy, size, color=INK, k=1.0):
    if k <= 0: return
    f = ImageFont.truetype(HAND, max(8, int(size * pop(k))))
    ImageDraw.Draw(frame).text((cx, cy), s, font=f, fill=color, anchor="mm")
    LBOX.append(ImageDraw.Draw(frame).textbbox((cx, cy), s, font=f, anchor="mm"))

def note(frame, lines, cx, cy, angle=-3, w=420, k=1.0):
    if k <= 0: return
    sp = sprite(("note", tuple(lines), cx, cy, angle, w), lambda c: sticky(c, cx, cy, lines, angle=angle, w=w))
    put(frame, sp, scale=0.6 + 0.4 * ease(k / 0.3)); LBOX.append((sp[1], sp[2], sp[1] + sp[0].width, sp[2] + sp[0].height))

def counter(v0, v1, k): return v0 + (v1 - v0) * inout(k)
def money(v): return f"${v:,.0f}"

# ---------------- Hintergruende ----------------
def void_bg():
    img = canvas((14, 14, 18, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    for k in range(10, 0, -1):
        d.polygon(S(960 - 60 - k * 22, 0, 960 + 60 + k * 22, 0, 960 + 260 + k * 30, 900, 960 - 260 - k * 30, 900), fill=(255, 244, 210, 9))
    d.ellipse(S(560, 860, 1360, 960), fill=(40, 38, 40, 255)); return img

def table_bg():
    img = canvas((14, 14, 18, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, 720), (W + 20, 720), (W + 20, H + 20), (-20, H + 20)], (96, 70, 52), 1, lw=4)
    for k in range(6): stroke(d, [(0, 760 + k * 55), (W, 770 + k * 55)], lw=2, color=(84, 60, 44))
    for k in range(10, 0, -1):
        d.polygon(S(960 - 60 - k * 22, 0, 960 + 60 + k * 22, 0, 960 + 300 + k * 30, 900, 960 - 300 - k * 30, 900), fill=(255, 244, 210, 8))
    return img

def street_bg():
    img = canvas(mode="RGB"); grad16(img, (150, 200, 236), (214, 232, 244), 0, 700); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, 700), (W + 20, 700), (W + 20, H + 20), (-20, H + 20)], (150, 186, 120), 1, lw=4)
    shape(d, [(-20, 860), (W + 20, 860), (W + 20, 940), (-20, 940)], (196, 192, 184), 2, lw=4)
    shape(d, [(-20, 940), (W + 20, 940), (W + 20, H + 20), (-20, H + 20)], (110, 110, 116), 3, lw=4)
    for x in range(40, W, 200): stroke(d, [(x, 1010), (x + 100, 1010)], lw=6, color=(236, 230, 200))
    house(d, 260, 700, 520, 10); house(d, 1140, 700, 520, 20)
    for x in (120, 960, 1820):
        shape(d, ellipse_pts(x, 520, 110, 150), (96, 146, 84), 30 + x, lw=4); stroke(d, [(x, 660), (x, 720)], lw=20, color=(120, 90, 60))
    sticky(img, 520, 330, ["Same street"], angle=-3, w=330)
    return img

def bank_bg():
    """Bankfiliale: Marmorwand, Logo-Schild, Schalter mit Glas, Teller-Fenster, Hintertuer rechts."""
    img = canvas((232, 226, 214, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 240): d.rectangle(S(x, 0, x + 236, 640), fill=(226, 220, 206))
    shape(d, [(-20, 640), (W + 20, 640), (W + 20, H + 20), (-20, H + 20)], (180, 170, 156), 1, lw=4)
    for k in range(5): stroke(d, [(0, 680 + k * 80), (W, 680 + k * 80)], lw=2, color=(166, 156, 142))
    shape(d, [(560, 120), (1360, 120), (1360, 220), (560, 220)], (40, 70, 110), 2, lw=5)
    text(img, "FIRST NATIONAL BANK", 960, 170, 52, SERIF, (240, 236, 220))
    shape(d, [(300, 560), (1500, 560), (1500, 760), (300, 760)], WOOD, 3, lw=5)                        # Schalter
    for k in range(3):
        x = 380 + k * 380
        shape(d, [(x, 300), (x + 300, 300), (x + 300, 560), (x, 560)], (190, 214, 226, 140), 4 + k, lw=4)
        shape(d, [(x + 110, 540), (x + 190, 540), (x + 190, 560), (x + 110, 560)], (60, 60, 64), 10 + k, lw=3)
    shape(d, [(1620, 300), (1820, 300), (1820, 640), (1620, 640)], (130, 100, 74), 20, lw=5)              # Hintertuer
    text(img, "STAFF ONLY", 1720, 340, 22, BOLD, (240, 236, 220))
    d.ellipse(S(1790, 470, 1806, 486), fill=(220, 200, 120))
    return img

def office_bg():
    img = canvas((214, 208, 196, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(1240, 120), (1760, 120), (1760, 560), (1240, 560)], (170, 206, 230), 1, lw=5)
    for x in range(1270, 1740, 90):
        shape(d, [(x, 380 - (x % 7) * 20), (x + 60, 380 - (x % 7) * 20), (x + 60, 560), (x, 560)], (150, 170, 196), 2 + x, lw=2)
    shape(d, [(-20, 760), (W + 20, 760), (W + 20, H + 20), (-20, H + 20)], (150, 130, 110), 3, lw=4)
    shape(d, [(200, 620), (1500, 620), (1500, 660), (200, 660)], WOOD, 4, lw=5)
    shape(d, [(240, 660), (1460, 660), (1460, 900), (240, 900)], WOOD_D, 5, lw=5)
    sticky(img, 420, 200, ["Loan Office"], angle=-4, w=300)
    return img

def grey_bg():
    return canvas(GREY_BG + (255,), "RGB")

def dark_bg():
    img = canvas(mode="RGB"); grad16(img, (28, 30, 40), (52, 54, 70)); return img

def apartment_bg():
    """Kleine Mietwohnung: Kuechenzeile, Fenster mit Nachbarhaus, Couch, Rechnungen."""
    img = canvas((196, 186, 170, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, 760), (W + 20, 760), (W + 20, H + 20), (-20, H + 20)], (140, 120, 100), 1, lw=4)
    shape(d, [(120, 200), (520, 200), (520, 520), (120, 520)], (160, 190, 210), 2, lw=5)
    shape(d, [(160, 300), (480, 300), (480, 520), (160, 520)], (170, 150, 140), 3, lw=3)
    for k in range(4): shape(d, [(200 + k * 70, 340), (240 + k * 70, 340), (240 + k * 70, 400), (200 + k * 70, 400)], (220, 210, 160), 4 + k, lw=2)
    shape(d, [(1200, 560), (1800, 560), (1800, 780), (1200, 780)], (120, 110, 130), 10, lw=5)                # Couch
    shape(d, [(1180, 500), (1820, 500), (1820, 580), (1180, 580)], (110, 100, 120), 11, lw=5)
    shape(d, [(640, 480), (1040, 480), (1040, 760), (640, 760)], (210, 206, 198), 12, lw=5)                 # Kuechenzeile
    for k in range(3): shape(d, [(660 + k * 128, 500), (770 + k * 128, 500), (770 + k * 128, 740), (660 + k * 128, 740)], (226, 222, 214), 13 + k, lw=3)
    return img

def porch_bg():
    img = canvas(mode="RGB"); grad16(img, (150, 200, 236), (214, 232, 244), 0, 760); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, 760), (W + 20, 760), (W + 20, H + 20), (-20, H + 20)], (150, 186, 120), 1, lw=4)
    house(d, 700, 760, 900, 40)
    shape(d, [(560, 760), (1740, 760), (1740, 800), (560, 800)], WOOD, 2, lw=4)
    return img

def town_bg():
    """Stadt von oben: Strassen, Haeuser, Autohaus, Laden, Regierungsgebaeude, Bank in der Mitte."""
    img = canvas((150, 186, 130, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    for y in (300, 760): shape(d, [(-20, y), (W + 20, y), (W + 20, y + 70), (-20, y + 70)], (120, 120, 126), y, lw=3)
    for x in (480, 1440): shape(d, [(x, -20), (x + 70, -20), (x + 70, H + 20), (x, H + 20)], (120, 120, 126), x + 1, lw=3)
    rnd = random.Random(3)
    for k in range(26):
        x, y = rnd.randint(30, 1860), rnd.randint(30, 1020)
        if any(abs(x - a) < 90 for a in (480, 1440)) or any(abs(y - b) < 90 for b in (300, 760)): continue
        shape(d, [(x, y), (x + 60, y), (x + 60, y + 50), (x, y + 50)], [(220, 200, 170), (200, 180, 160), (230, 220, 200)][k % 3], 40 + k, lw=3)
        shape(d, [(x - 4, y), (x + 30, y - 22), (x + 64, y)], (150, 90, 70), 80 + k, lw=3)
    return img

def fed_bg(night=True):
    """Federal Reserve (Eccles Building, Washington): Marmorfassade, Saeulen, Adler-Relief, Treppe."""
    img = canvas(mode="RGB"); grad16(img, (20, 24, 48) if night else (150, 200, 236), (54, 60, 96) if night else (214, 232, 244), 0, 820); d = ImageDraw.Draw(img, "RGBA")
    if night:
        rnd = random.Random(4)
        for k in range(60): x, y = rnd.randint(0, W), rnd.randint(0, 400); d.ellipse(S(x, y, x + 3, y + 3), fill=(255, 255, 230, 180))
    shape(d, [(-20, 820), (W + 20, 820), (W + 20, H + 20), (-20, H + 20)], (90, 96, 90), 1, lw=4)
    shape(d, [(380, 300), (1540, 300), (1540, 820), (380, 820)], (226, 222, 208), 2, lw=6)
    shape(d, [(340, 260), (1580, 260), (1580, 310), (340, 310)], (214, 210, 196), 3, lw=5)
    for k in range(6):
        x = 640 + k * 130
        shape(d, [(x, 340), (x + 56, 340), (x + 56, 760), (x, 760)], (240, 236, 224), 10 + k, lw=4)
        for j in range(3): stroke(d, [(x + 14 + j * 14, 350), (x + 14 + j * 14, 750)], lw=2, color=(210, 206, 194))
    for x in (440, 1300):
        for r in range(3):
            for c in range(2): shape(d, [(x + c * 90, 380 + r * 130), (x + c * 90 + 60, 380 + r * 130), (x + c * 90 + 60, 470 + r * 130), (x + c * 90, 470 + r * 130)], (60, 70, 90) if night else (150, 170, 190), 30 + r * 10 + c + x, lw=3)
    shape(d, [(560, 760), (1360, 760), (1400, 820), (520, 820)], (200, 196, 184), 4, lw=4)
    text(img, "FEDERAL RESERVE", 960, 288, 30, SERIF, (90, 86, 76))
    return img

def skyline(d, y, color=(150, 160, 186), seed=7):
    rnd = random.Random(seed); x = -20
    while x < W:
        w_ = rnd.randint(80, 160); h_ = rnd.randint(200, 560)
        shape(d, [(x, y), (x + w_, y), (x + w_, y - h_), (x, y - h_)], color, seed + x, lw=3)
        for yy in range(int(y - h_ + 30), int(y - 20), 46):
            for xx in range(x + 14, x + w_ - 20, 34): d.rectangle(S(xx, yy, xx + 16, yy + 22), fill=(230, 226, 180, 120))
        x += w_ + rnd.randint(6, 30)

def city_bg(dark=False):
    img = canvas(mode="RGB"); grad16(img, (30, 34, 60) if dark else (160, 200, 230), (70, 76, 110) if dark else (220, 232, 240)); d = ImageDraw.Draw(img, "RGBA")
    skyline(d, 1000, (70, 76, 100) if dark else (150, 160, 186)); return img

def glass_office_bg():
    img = canvas(mode="RGB"); grad16(img, (170, 206, 236), (226, 236, 244)); d = ImageDraw.Draw(img, "RGBA")
    skyline(d, 900, (160, 172, 196), 11)
    for x in range(0, W, 320): stroke(d, [(x, 0), (x, 900)], lw=10, color=(60, 64, 76))
    shape(d, [(-20, 900), (W + 20, 900), (W + 20, H + 20), (-20, H + 20)], (70, 72, 80), 1, lw=4)
    return img

def grocery_bg(year="1971"):
    img = canvas((236, 228, 206, 255) if year == "1971" else (238, 238, 236, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    for row in range(3):
        y = 180 + row * 180
        shape(d, [(80, y + 140), (1840, y + 140), (1840, y + 160), (80, y + 160)], WOOD if year == "1971" else (170, 170, 176), 1 + row, lw=3)
        rnd = random.Random(row + (0 if year == "1971" else 10))
        for x in range(100, 1820, 70):
            c = [(200, 70, 60), (240, 200, 80), (80, 140, 90), (230, 140, 60), (90, 120, 170)][rnd.randint(0, 4)]
            hgt = rnd.randint(70, 130); shape(d, [(x, y + 140 - hgt), (x + 54, y + 140 - hgt), (x + 54, y + 140), (x, y + 140)], c, 20 + x + row, lw=2)
    shape(d, [(-20, 760), (W + 20, 760), (W + 20, H + 20), (-20, H + 20)], (200, 190, 170) if year == "1971" else (210, 210, 214), 30, lw=4)
    sticky(img, 1640, 90, [year], angle=4, w=240)
    return img

def svb_bg():
    img = canvas(mode="RGB"); grad16(img, (150, 190, 226), (220, 230, 240)); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, 860), (W + 20, 860), (W + 20, H + 20), (-20, H + 20)], (120, 120, 126), 1, lw=4)
    shape(d, [(560, 160), (1360, 160), (1360, 860), (560, 860)], (120, 150, 180), 2, lw=6)
    for r in range(8):
        for c in range(6): shape(d, [(590 + c * 128, 190 + r * 80), (690 + c * 128, 190 + r * 80), (690 + c * 128, 250 + r * 80), (590 + c * 128, 250 + r * 80)], (170, 206, 230), 10 + r * 6 + c, lw=2)
    shape(d, [(700, 800), (1220, 800), (1220, 860), (700, 860)], (40, 60, 90), 3, lw=4)
    text(img, "SILICON VALLEY BANK", 960, 830, 34, BOLD, (240, 240, 240))
    sticky(img, 300, 200, ["California", "March 9, 2023"], angle=-4, w=420)
    return img

def vault_bg(light=1.0):
    img = canvas((60, 62, 68, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    shape(d, ellipse_pts(960, 540, 420, 420), (150, 154, 162), 1, lw=8)
    shape(d, ellipse_pts(960, 540, 340, 340), (120, 124, 132), 2, lw=6)
    for k in range(8):
        a = k * math.pi / 4; stroke(d, [(960 + math.cos(a) * 80, 540 + math.sin(a) * 80), (960 + math.cos(a) * 300, 540 + math.sin(a) * 300)], lw=10, color=(96, 100, 108))
    shape(d, ellipse_pts(960, 540, 90, 90), (180, 184, 190), 3, lw=6)
    return img

def kitchen_bg():
    img = canvas((214, 196, 170, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(140, 140), (620, 140), (620, 480), (140, 480)], (170, 206, 230), 1, lw=5)
    stroke(d, [(380, 140), (380, 480)], lw=6); stroke(d, [(140, 310), (620, 310)], lw=6)
    for k in range(4): shape(d, [(900 + k * 220, 160), (1090 + k * 220, 160), (1090 + k * 220, 400), (900 + k * 220, 400)], (190, 150, 110), 2 + k, lw=4)
    shape(d, [(-20, 640), (W + 20, 640), (W + 20, H + 20), (-20, H + 20)], (160, 130, 100), 6, lw=4)
    shape(d, [(360, 700), (1560, 700), (1500, 780), (420, 780)], WOOD, 7, lw=5)
    stroke(d, [(480, 780), (470, 1060)], lw=16, color=WOOD_D); stroke(d, [(1440, 780), (1450, 1060)], lw=16, color=WOOD_D)
    return img

def wallstreet_bg():
    img = canvas(mode="RGB"); grad16(img, (90, 96, 110), (150, 150, 160)); d = ImageDraw.Draw(img, "RGBA")
    skyline(d, 900, (110, 112, 126), 21)
    shape(d, [(-20, 900), (W + 20, 900), (W + 20, H + 20), (-20, H + 20)], (100, 100, 106), 1, lw=4)
    shape(d, [(1300, 120), (1700, 120), (1700, 200), (1300, 200)], (30, 30, 36), 2, lw=4)
    text(img, "WALL ST", 1500, 160, 40, BOLD, (240, 240, 240))
    sticky(img, 300, 160, ["2008"], angle=-4, w=220)
    return img

def aig_bg():
    img = canvas(mode="RGB"); grad16(img, (160, 196, 226), (220, 230, 240)); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(700, 80), (1220, 80), (1220, 1000), (700, 1000)], (170, 176, 190), 1, lw=6)
    for r in range(10):
        for c in range(4): shape(d, [(740 + c * 120, 140 + r * 84), (830 + c * 120, 140 + r * 84), (830 + c * 120, 196 + r * 84), (740 + c * 120, 196 + r * 84)], (130, 160, 190), 10 + r * 4 + c, lw=2)
    shape(d, [(-20, 1000), (W + 20, 1000), (W + 20, H + 20), (-20, H + 20)], (110, 110, 116), 2, lw=4)
    shape(d, [(780, 20), (1140, 20), (1140, 80), (780, 80)], (30, 60, 120), 3, lw=4)
    text(img, "AIG", 960, 52, 44, BOLD, (240, 240, 240))
    sticky(img, 300, 180, ["March 2009"], angle=-4, w=320)
    return img

def coffee_bg():
    img = canvas((206, 180, 150, 255), "RGB"); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(200, 120), (1000, 120), (1000, 260), (200, 260)], (60, 44, 36), 1, lw=5)
    for k, (a, b) in enumerate((("LATTE", "$4.50"), ("ESPRESSO", "$3.20"), ("MUFFIN", "$3.80"))):
        text(img, a, 330 + k * 240, 170, 28, BOLD, (240, 230, 210)); text(img, b, 330 + k * 240, 220, 28, BOLD, (240, 200, 120))
    shape(d, [(-20, 640), (W + 20, 640), (W + 20, H + 20), (-20, H + 20)], (130, 100, 76), 2, lw=4)
    shape(d, [(100, 560), (1100, 560), (1100, 760), (100, 760)], WOOD, 3, lw=5)
    skyline(d, 640, (170, 170, 190), 31)
    return img

# ---------------- Requisiten ----------------
def phone(c, cx, cy, h, screen_fn=None, color=(30, 32, 40)):
    d = ImageDraw.Draw(c, "RGBA"); w = h * 0.5
    shape(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], color, 900, lw=5)
    shape(d, [(cx - w / 2 + 12, cy - h / 2 + 30), (cx + w / 2 - 12, cy - h / 2 + 30), (cx + w / 2 - 12, cy + h / 2 - 30), (cx - w / 2 + 12, cy + h / 2 - 30)], (246, 248, 250), 901, lw=2)
    if screen_fn: screen_fn(c, cx, cy, w, h)

def bank_app(title, amount, color=(40, 90, 160)):
    def fn(c, cx, cy, w, h):
        d = ImageDraw.Draw(c, "RGBA")
        d.rectangle(S(cx - w / 2 + 14, cy - h / 2 + 32, cx + w / 2 - 14, cy - h / 2 + 100), fill=color)
        text(c, title, cx, cy - h / 2 + 66, w * 0.1, BOLD, (255, 255, 255))
        text(c, "Balance", cx, cy - h * 0.12, w * 0.08, BOLD, (120, 120, 130))
        text(c, amount, cx, cy, w * 0.17, BOLD, INK)
    return fn

def paycheck(c, cx, cy, w, name, amount):
    d = ImageDraw.Draw(c, "RGBA"); h = w * 0.45
    shape(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], (236, 244, 230), 300, lw=5)
    text(c, "PAY TO THE ORDER OF", cx - w * 0.2, cy - h * 0.3, w * 0.035, BOLD, (100, 110, 100))
    text(c, name, cx - w * 0.2, cy - h * 0.1, w * 0.07, HAND, INK)
    text(c, amount, cx + w * 0.25, cy - h * 0.1, w * 0.07, BOLD, (40, 110, 60))
    stroke(d, [(cx - w * 0.4, cy + h * 0.25), (cx + w * 0.1, cy + h * 0.25)], lw=3)
    text(c, "ACME CORP · per year", cx + w * 0.26, cy + h * 0.25, w * 0.03, BOLD, (100, 110, 100))

def paper(c, cx, cy, w, h, title, lines=6, sub=None, seed=0, color=(250, 248, 238)):
    d = ImageDraw.Draw(c, "RGBA")
    shape(d, [(cx - w / 2 + 12, cy - h / 2 + 12), (cx + w / 2 + 12, cy - h / 2 + 12), (cx + w / 2 + 12, cy + h / 2 + 12), (cx - w / 2 + 12, cy + h / 2 + 12)], (0, 0, 0, 60), seed, lw=0)
    shape(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], color, seed + 1, lw=4)
    text(c, title, cx, cy - h / 2 + w * 0.1, w * 0.07, SERIF, INK)
    if sub: text(c, sub, cx, cy - h / 2 + w * 0.18, w * 0.04, SERIF, (100, 100, 106))
    for k in range(lines):
        y = cy - h / 2 + w * 0.28 + k * h * 0.07
        stroke(d, [(cx - w * 0.38, y), (cx + w * (0.38 if k % 3 else 0.2), y)], lw=3, color=(186, 182, 172))

def credit_card(c, cx, cy, w, color=(40, 60, 110), label="CREDIT"):
    d = ImageDraw.Draw(c, "RGBA"); h = w * 0.63
    d.rounded_rectangle(S(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=int(w * 0.06 * SS), fill=color + (255,), outline=INK, width=5 * SS)
    d.rounded_rectangle(S(cx - w * 0.38, cy - h * 0.15, cx - w * 0.22, cy + h * 0.05), radius=8, fill=(220, 190, 110, 255))
    text(c, "4512  ••••  ••••  2025", cx, cy + h * 0.2, w * 0.07, BOLD, (240, 240, 244))
    text(c, label, cx + w * 0.3, cy - h * 0.32, w * 0.06, BOLD, (240, 240, 244))

def house_icon(c, cx, base, w, seed=0, color=(226, 210, 180)):
    house(ImageDraw.Draw(c, "RGBA"), cx - w / 2, base, w, seed)

def coin(d, cx, cy, r, seed=0):
    shape(d, ellipse_pts(cx, cy, r, r), GOLD, seed, lw=4)
    shape(d, ellipse_pts(cx, cy, r * 0.7, r * 0.7), (250, 210, 80), seed + 1, lw=2)

def bar_chart(c, x0, base, bars, maxv, h, w_bar=140, gap=60, k=1.0, color=(60, 150, 90)):
    d = ImageDraw.Draw(c, "RGBA")
    for i, (lab, v) in enumerate(bars):
        x = x0 + i * (w_bar + gap); hh = h * v / maxv * k
        shape(d, [(x, base), (x + w_bar, base), (x + w_bar, base - hh), (x, base - hh)], color, 50 + i, lw=4)
        text(c, lab, x + w_bar / 2, base + 40, 34, BOLD, INK)

def scale_prop(d, cx, cy, w, tilt=0.0):
    stroke(d, [(cx, cy), (cx, cy + 320)], lw=14, color=(110, 90, 70))
    shape(d, [(cx - 120, cy + 320), (cx + 120, cy + 320), (cx + 90, cy + 350), (cx - 90, cy + 350)], (110, 90, 70), 70, lw=4)
    a = tilt; ax, ay = math.cos(a) * w / 2, math.sin(a) * w / 2
    stroke(d, [(cx - ax, cy - ay), (cx + ax, cy + ay)], lw=12, color=(110, 90, 70))
    for sx in (-1, 1):
        px, py = cx + sx * ax, cy + sx * ay
        stroke(d, [(px, py), (px - 80, py + 140)], lw=3); stroke(d, [(px, py), (px + 80, py + 140)], lw=3)
        shape(d, ellipse_pts(px, py + 150, 110, 22), (200, 180, 120), 71 + sx, lw=4)
    return (cx - ax, cy - ay + 150), (cx + ax, cy + ay + 150)

def shopping_cart(d, cx, base, w, full=1.0, seed=0):
    h = w * 0.55
    shape(d, [(cx - w / 2, base - h), (cx + w / 2, base - h), (cx + w * 0.4, base - h * 0.3), (cx - w * 0.4, base - h * 0.3)], (200, 204, 210), seed, lw=5)
    for k in range(6): stroke(d, [(cx - w / 2 + k * w / 6 + 10, base - h), (cx - w * 0.4 + k * w * 0.8 / 6 + 10, base - h * 0.3)], lw=2, color=(150, 154, 160))
    stroke(d, [(cx + w / 2, base - h), (cx + w * 0.62, base - h * 1.2)], lw=6)
    for x in (cx - w * 0.3, cx + w * 0.3): shape(d, ellipse_pts(x, base - 18, 18, 18), (50, 50, 56), seed + 3, lw=3)
    rnd = random.Random(seed)
    for k in range(int(14 * full)):
        x = cx - w * 0.42 + (k % 7) * w * 0.12; y = base - h - 30 - (k // 7) * 70
        c = [(200, 70, 60), (240, 200, 80), (80, 140, 90), (230, 140, 60), (90, 120, 170)][rnd.randint(0, 4)]
        shape(d, [(x, y), (x + w * 0.1, y), (x + w * 0.1, y + 80), (x, y + 80)], c, seed + 10 + k, lw=2)

def bike(d, cx, base, w, color=(200, 70, 60), seed=0):
    r = w * 0.22
    for x in (cx - w * 0.32, cx + w * 0.32):
        stroke(d, ellipse_pts(x, base - r, r, r), lw=6)
    stroke(d, [(cx - w * 0.32, base - r), (cx - w * 0.05, base - r * 2.0), (cx + w * 0.22, base - r * 2.0), (cx + w * 0.32, base - r)], lw=8, color=color)
    stroke(d, [(cx - w * 0.05, base - r * 2.0), (cx, base - r)], lw=8, color=color)
    stroke(d, [(cx + w * 0.22, base - r * 2.0), (cx + w * 0.26, base - r * 2.6)], lw=6)
