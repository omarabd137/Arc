"""ARC Short – Ron Wayne. Crayon-Prinzip: Figuren simpel, Orte und Requisiten genau und mit Perspektive,
gedaempfte Farben, graue Cel-Schatten, gleichmaessige Linien."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "02_mcdonalds"))
sys.path.insert(0, os.path.join(HERE, "..", "01_lamborghini"))
from mcd_kit import (S, sh, shape, stroke, ellipse_pts, W, H, SS, INK, done, figure, sticky, text, grad, dollar_bill,
                     F, BOLD, SERIF, HAND, RED, YEL, WHITE)
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

WOOD, WOOD_D = (176, 132, 88), (140, 100, 64)

# ---------------- Figuren ----------------
def P(**k):
    base = dict(skin=(238, 200, 164), hair=(60, 44, 34), hair_hi=(110, 86, 70), top=(120, 120, 128), tie=None, braces=None,
                trousers=(60, 62, 72), glasses=False, mustache=False, nose=True, big=1.0, hairstyle="ferruccio",
                long_hair=False, beard=False)
    base.update(k); return base
WAYNE = P(hair=(70, 54, 42), top=(150, 132, 104), clear_glasses=True, mustache=True)           # 1976: 41, dunkles Haar, Brille, Schnurrbart
WAYNE_OLD = P(hair=(226, 226, 230), hair_hi=(255, 255, 255), top=(150, 132, 104), clear_glasses=True, mustache=True, skin=(236, 198, 166))
JOBS = P(hair=(46, 34, 28), top=(220, 214, 196), long_hair=True, beard=True, big=0.92)    # 1976: lange Haare, Bart
WOZ = P(hair=(54, 40, 32), top=(110, 140, 170), clear_glasses=True, beard=True, big=1.2)

def person(img, cx, base, R, p, face=1, mouth="line", brow=0.0, arms=("down", "down"), seed=1, seated=False):
    """figure() plus Extras fuer lange Haare und Vollbart."""
    leg, tor_h = R * 1.25, R * 1.35
    hcy = base - leg - tor_h - R * 0.78
    d = ImageDraw.Draw(img, "RGBA")
    if p.get("long_hair"):         # Haare hinter dem Kopf bis zur Schulter
        shape(d, ellipse_pts(cx - face * R * 0.15, hcy + R * 0.25, R * 1.08, R * 1.15), p["hair"], seed + 90, lw=4)
    figure(img, cx, base, R, p, face=face, mouth=mouth, brow=brow, arms=arms, seed=seed, seated=seated)
    d = ImageDraw.Draw(img, "RGBA")
    if p.get("beard"):
        ex = cx + face * R * 0.24
        pts = ellipse_pts(cx + face * R * 0.1, hcy + R * 0.1, R * 0.92, R * 0.9, 30, 25, 155)
        inner = list(reversed(ellipse_pts(ex, hcy + R * 0.38, R * 0.32, R * 0.2, 20, 0, 180)))
        shape(d, pts + inner, p["hair"], seed + 91, lw=4)
    if p.get("clear_glasses"):     # normale Brille: nur Rahmen, Augen sichtbar
        ex, ey = cx + face * R * 0.24, hcy + R * 0.05
        for k in (-1, 1):
            gx = ex + k * R * 0.27
            d.rounded_rectangle(S(gx - R * 0.17, ey - R * 0.13, gx + R * 0.17, ey + R * 0.12), radius=int(R * 0.06 * SS), outline=INK, width=int(4 * SS), fill=(255, 255, 255, 40))
        stroke(d, [(ex - R * 0.1, ey - R * 0.04), (ex + R * 0.1, ey - R * 0.04)], lw=4)
    return hcy

# ---------------- Requisiten ----------------
def apple_fruit(d, cx, cy, r, slice_missing=True, seed=10):
    """Roter Apfel mit Stiel und Blatt. Wenn slice_missing: ein Zehntel (36 Grad) fehlt, man sieht das helle Fruchtfleisch."""
    a0, a1 = (-60, -24) if slice_missing else (0, 0)
    outline = [(cx, cy)] + ellipse_pts(cx, cy, r * 1.02, r, 80, a1, a0 + 360) if slice_missing else ellipse_pts(cx, cy, r * 1.02, r, 80)
    shape(d, outline, (206, 40, 46), seed, lw=6)
    if slice_missing:
        for a in (a0, a1):
            stroke(d, [(cx, cy), (cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r)], lw=6)
        shape(d, [(cx, cy)] + ellipse_pts(cx, cy, r * 0.92, r * 0.9, 12, a0 + 2, a1 - 2), (250, 236, 190), seed + 1, lw=3)
    d.chord(S(cx - r * 0.85, cy - r * 0.85, cx + r * 0.2, cy + r * 0.6), 150, 250, fill=(255, 255, 255, 70))
    stroke(d, [(cx, cy - r * 0.92), (cx + r * 0.08, cy - r * 1.25)], lw=8, color=(90, 60, 40))
    shape(d, ellipse_pts(cx + r * 0.28, cy - r * 1.14, r * 0.22, r * 0.1), (110, 160, 80), seed + 2, lw=4)

def apple_slice(d, cx, cy, r, seed=20):
    """Das herausgeschnittene 10-%-Stueck."""
    shape(d, [(cx, cy)] + ellipse_pts(cx, cy, r, r, 10, -18, 18), (206, 40, 46), seed, lw=5)
    shape(d, [(cx, cy)] + ellipse_pts(cx, cy, r * 0.9, r * 0.9, 10, -16, 16), (250, 236, 190), seed + 1, lw=3)

def apple_one(d, x, y, w, seed=30):
    """Apple I (1976): Platine im Holzgehaeuse (Byte-Shop-Stil), externe Tastatur, kleiner Monitor."""
    shape(d, [(x, y), (x + w, y), (x + w * 0.95, y - w * 0.3), (x + w * 0.05, y - w * 0.3)], WOOD, seed, lw=5)
    for k in range(4): stroke(d, [(x + w * 0.08, y - w * (0.05 + k * 0.06)), (x + w * 0.92, y - w * (0.05 + k * 0.06))], lw=2, color=WOOD_D)
    shape(d, [(x + w * 0.12, y - w * 0.3), (x + w * 0.88, y - w * 0.3), (x + w * 0.82, y - w * 0.36), (x + w * 0.18, y - w * 0.36)], (40, 110, 70), seed + 1, lw=3)
    shape(d, [(x + w * 0.1, y + w * 0.02), (x + w * 0.9, y + w * 0.02), (x + w * 0.95, y + w * 0.16), (x + w * 0.05, y + w * 0.16)], (60, 60, 64), seed + 2, lw=4)
    for r_ in range(3):
        for k in range(11):
            kx = x + w * (0.12 + k * 0.072 + r_ * 0.015); ky = y + w * (0.045 + r_ * 0.04)
            d.rectangle(S(kx, ky, kx + w * 0.05, ky + w * 0.028), fill=(220, 218, 210))
    mx, my = x + w * 0.5, y - w * 0.36
    shape(d, [(mx - w * 0.3, my), (mx + w * 0.3, my), (mx + w * 0.3, my - w * 0.5), (mx - w * 0.3, my - w * 0.5)], (190, 186, 176), seed + 3, lw=5)
    shape(d, [(mx - w * 0.24, my - w * 0.06), (mx + w * 0.24, my - w * 0.06), (mx + w * 0.24, my - w * 0.44), (mx - w * 0.24, my - w * 0.44)], (40, 60, 50), seed + 4, lw=3)
    for k in range(4): stroke(d, [(mx - w * 0.2, my - w * (0.38 - k * 0.07)), (mx + w * (0.02 + 0.04 * k), my - w * (0.38 - k * 0.07))], lw=3, color=(130, 230, 150))

def garage_bg():
    """Garage der Familie Jobs, Los Altos 1976: Rueckwand mit Werkbank und Regalen, Seitenwand in Perspektive,
    offenes Rolltor mit Blick auf die Vorortstrasse (Haus gegenueber, Baum)."""
    img = Image.new("RGB", (W * SS, H * SS), (206, 196, 180)); d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, -20), (W + 20, -20), (W - 140, 260), (140, 260)], (176, 168, 156), 1, lw=4)                 # Decke
    shape(d, [(-20, -20), (140, 260), (140, 1300), (-20, 1560)], (186, 176, 162), 2, lw=4)                        # linke Wand
    shape(d, [(W + 20, -20), (W - 140, 260), (W - 140, 1300), (W + 20, 1560)], (186, 176, 162), 3, lw=4)          # rechte Wand
    for k in range(5): stroke(d, [(140 + k * 200, 260), (140 + k * 200, 1300)], lw=2, color=(190, 180, 166))      # Wandpaneele
    shape(d, [(-20, 1560), (140, 1300), (W - 140, 1300), (W + 20, 1560), (W + 20, H + 20), (-20, H + 20)], (150, 146, 140), 4, lw=4)  # Betonboden
    for k in range(4): stroke(d, [(140 - k * 60, 1300 + k * 90), (W - 140 + k * 60, 1300 + k * 90)], lw=2, color=(136, 132, 126))
    # offenes Garagentor rechts an der Rueckwand
    shape(d, [(600, 560), (920, 560), (920, 1300), (600, 1300)], (170, 206, 230), 5, lw=4)
    shape(d, [(600, 1100), (920, 1060), (920, 1300), (600, 1300)], (140, 170, 110), 6, lw=3)
    shape(d, [(660, 900), (820, 900), (820, 1080), (660, 1080)], (236, 220, 196), 7, lw=3)                        # Haus gegenueber
    shape(d, [(650, 900), (740, 840), (830, 900)], (150, 90, 70), 8, lw=3)
    shape(d, ellipse_pts(880, 900, 60, 90), (96, 140, 84), 9, lw=3)
    shape(d, [(600, 540), (920, 540), (920, 600), (600, 600)], (150, 146, 140), 10, lw=4)                         # hochgerolltes Tor
    # Werkbank links mit Regalen und Werkzeugwand
    shape(d, [(180, 640), (560, 640), (560, 1000), (180, 1000)], (196, 170, 130), 11, lw=4)                       # Lochwand
    for yy in range(660, 990, 40):
        for xx in range(200, 550, 40): d.ellipse(S(xx, yy, xx + 6, yy + 6), fill=(150, 126, 96))
    stroke(d, [(230, 700), (230, 800)], lw=8, color=(90, 90, 100)); stroke(d, [(300, 690), (330, 820)], lw=8, color=(160, 60, 50))
    stroke(d, [(400, 700), (400, 790)], lw=10, color=(70, 70, 80))
    shape(d, [(160, 1080), (580, 1080), (580, 1110), (160, 1110)], WOOD, 12, lw=4)                               # Arbeitsplatte
    for lx in (180, 560): stroke(d, [(lx, 1110), (lx, 1300)], lw=10, color=WOOD_D)
    apple_one(d, 230, 1076, 300)
    for k in range(3):                                                                                           # Platinen-Stapel
        shape(d, [(420 + k * 6, 1076 - k * 14), (550 + k * 6, 1076 - k * 14), (550 + k * 6, 1064 - k * 14), (420 + k * 6, 1064 - k * 14)], (40, 110, 70), 13 + k, lw=3)
    shape(d, ellipse_pts(540, 270, 70, 20), (240, 236, 210), 20, lw=3)                                            # Deckenlampe
    return img

def apple_park(img, cx, cy, r):
    """Apple Park von oben: Ring-Gebaeude mit Glasdach, Innenhof mit Baeumen, Parkflaechen."""
    d = ImageDraw.Draw(img, "RGBA")
    shape(d, ellipse_pts(cx, cy, r * 1.35, r * 1.2), (150, 186, 120), 1, lw=4)
    shape(d, ellipse_pts(cx, cy, r, r * 0.9), (226, 230, 236), 2, lw=6)
    shape(d, ellipse_pts(cx, cy, r * 0.82, r * 0.72), (130, 176, 104), 3, lw=6)
    for k in range(36):
        a = math.radians(k * 10)
        stroke(d, [(cx + math.cos(a) * r * 0.84, cy + math.sin(a) * r * 0.74), (cx + math.cos(a) * r * 0.98, cy + math.sin(a) * r * 0.88)], lw=2, color=(170, 196, 220))
    rnd = random.Random(2)
    for k in range(40):
        a, rr = rnd.uniform(0, 6.28), rnd.uniform(0.1, 0.65)
        x, y = cx + math.cos(a) * r * rr, cy + math.sin(a) * r * rr * 0.88
        shape(d, ellipse_pts(x, y, 16, 14), (84, 136, 72), 10 + k, lw=2)
    shape(d, ellipse_pts(cx, cy, r * 0.1, r * 0.09), (150, 196, 230), 60, lw=3)

def logo_1976(img, cx, cy, w, reveal=1.0):
    """Das erste Apple-Logo (1976, von Ron Wayne): Isaac Newton unter dem Apfelbaum, ovaler Rahmen, Banner. Eigene Nachzeichnung."""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay, "RGBA")
    h = w * 1.25
    shape(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], (246, 240, 224), 1, lw=6)
    shape(d, [(cx - w * 0.44, cy - h * 0.44), (cx + w * 0.44, cy - h * 0.44), (cx + w * 0.44, cy + h * 0.3), (cx - w * 0.44, cy + h * 0.3)], (240, 232, 212), 2, lw=3)
    shape(d, ellipse_pts(cx + w * 0.05, cy - h * 0.18, w * 0.34, h * 0.2), (150, 150, 140), 3, lw=4)                   # Baumkrone
    for k in range(30):
        a = k * 0.7; rr = (k % 5) / 5
        stroke(d, [(cx + w * 0.05 + math.cos(a) * w * 0.3 * rr, cy - h * 0.18 + math.sin(a) * h * 0.17 * rr), (cx + w * 0.05 + math.cos(a + 0.4) * w * 0.3 * rr, cy - h * 0.18 + math.sin(a + 0.4) * h * 0.17 * rr)], lw=2, color=(100, 100, 92))
    stroke(d, [(cx + w * 0.08, cy - h * 0.02), (cx + w * 0.1, cy + h * 0.26)], lw=14, color=(120, 110, 96))         # Stamm
    shape(d, ellipse_pts(cx - w * 0.16, cy + h * 0.08, w * 0.06, w * 0.06), (230, 220, 200), 4, lw=3)               # Newton Kopf
    shape(d, [(cx - w * 0.26, cy + h * 0.26), (cx - w * 0.06, cy + h * 0.26), (cx - w * 0.1, cy + h * 0.12), (cx - w * 0.22, cy + h * 0.12)], (200, 196, 186), 5, lw=3)
    shape(d, [(cx - w * 0.2, cy + h * 0.16), (cx + w * 0.02, cy + h * 0.18), (cx + w * 0.0, cy + h * 0.21), (cx - w * 0.2, cy + h * 0.2)], (250, 250, 246), 6, lw=2)   # Buch
    shape(d, ellipse_pts(cx - w * 0.12, cy - h * 0.02, w * 0.025, w * 0.025), (206, 60, 50), 7, lw=2)               # fallender Apfel
    shape(d, [(cx - w * 0.48, cy + h * 0.31), (cx + w * 0.48, cy + h * 0.31), (cx + w * 0.42, cy + h * 0.42), (cx - w * 0.42, cy + h * 0.42)], (236, 226, 200), 8, lw=4)
    f = ImageFont.truetype(SERIF, int(w * 0.075 * SS))
    d.text((cx * SS, (cy + h * 0.365) * SS), "APPLE COMPUTER CO.", font=f, fill=INK, anchor="mm")
    if reveal < 1:     # Zeichnung entsteht von oben nach unten
        m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rectangle([0, 0, img.size[0], int((cy - h / 2 + h * reveal) * SS)], fill=255)
        lay.putalpha(ImageChops.multiply(lay.getchannel("A"), m))
    img.paste(lay, (0, 0), lay)

def calendar(img, cx, cy, w, day, month="APRIL 1976"):
    d = ImageDraw.Draw(img, "RGBA"); h = w * 1.1
    shape(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], (250, 248, 240), 1, lw=6)
    shape(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy - h * 0.22), (cx - w / 2, cy - h * 0.22)], RED, 2, lw=6)
    text(img, month, cx, cy - h * 0.36, w * 0.12, BOLD, WHITE)
    text(img, str(day), cx, cy + h * 0.12, w * 0.5, BOLD, INK)
    for k in range(5): d.ellipse(S(cx - w * 0.4 + k * w * 0.2 - 8, cy - h / 2 - 18, cx - w * 0.4 + k * w * 0.2 + 8, cy - h / 2 + 2), fill=(120, 120, 130))

def house(d, x, base, w, seed=40):
    """Einfamilienhaus der 70er: Satteldach, Holzverkleidung, Fenster, Tuer, Garage, Rasen."""
    h = w * 0.55
    shape(d, [(x, base), (x + w, base), (x + w, base - h), (x, base - h)], (226, 210, 180), seed, lw=5)
    for k in range(6): stroke(d, [(x, base - h + k * h / 6), (x + w, base - h + k * h / 6)], lw=2, color=(200, 182, 150))
    shape(d, [(x - w * 0.06, base - h), (x + w / 2, base - h - w * 0.32), (x + w * 1.06, base - h)], (130, 80, 64), seed + 1, lw=5)
    shape(d, [(x + w * 0.08, base - h * 0.75), (x + w * 0.32, base - h * 0.75), (x + w * 0.32, base - h * 0.35), (x + w * 0.08, base - h * 0.35)], (170, 206, 226), seed + 2, lw=4)
    shape(d, [(x + w * 0.42, base), (x + w * 0.56, base), (x + w * 0.56, base - h * 0.62), (x + w * 0.42, base - h * 0.62)], (130, 90, 64), seed + 3, lw=4)
    shape(d, [(x + w * 0.64, base), (x + w * 0.94, base), (x + w * 0.94, base - h * 0.6), (x + w * 0.64, base - h * 0.6)], (236, 232, 222), seed + 4, lw=4)
    for k in range(4): stroke(d, [(x + w * 0.64, base - h * 0.15 * (k + 1)), (x + w * 0.94, base - h * 0.15 * (k + 1))], lw=2, color=(190, 186, 176))

def partnership_contract(img, cx, cy, w):
    """Gruendungsvertrag Apple Computer Co., 1. April 1976, drei Unterschriften."""
    d = ImageDraw.Draw(img, "RGBA"); h = w * 1.3
    shape(d, [(cx - w / 2 + 14, cy - h / 2 + 14), (cx + w / 2 + 14, cy - h / 2 + 14), (cx + w / 2 + 14, cy + h / 2 + 14), (cx - w / 2 + 14, cy + h / 2 + 14)], (0, 0, 0, 60), 0, lw=0)
    shape(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], (244, 238, 220), 1, lw=4)
    text(img, "AGREEMENT", cx, cy - h / 2 + 60, w * 0.08, SERIF, INK)
    text(img, "Apple Computer Company · April 1, 1976", cx, cy - h / 2 + 108, w * 0.038, SERIF, (90, 90, 96))
    for k in range(11):
        y = cy - h / 2 + 160 + k * 30
        stroke(d, [(cx - w * 0.4, y), (cx + w * (0.4 if k % 4 else 0.22), y)], lw=3, color=(186, 180, 166))
    for k, (who, sig) in enumerate((("S. P. Jobs", 0), ("S. G. Wozniak", 1), ("R. G. Wayne", 2))):
        y = cy + h * 0.2 + k * 70
        rnd = random.Random(k + 3); pts = [(cx - w * 0.36 + j * w * 0.012, y - 14 - 14 * math.sin(j * 0.9 + k) * rnd.uniform(0.6, 1)) for j in range(28)]
        d.line([(x * SS, yy * SS) for x, yy in pts], fill=(30, 40, 110), width=int(4 * SS), joint="curve")
        stroke(d, [(cx - w * 0.38, y), (cx + w * 0.05, y)], lw=2)
        text(img, who, cx + w * 0.22, y - 6, w * 0.04, SERIF, (90, 90, 96))

def auction_bg():
    """Auktionssaal: Wandpaneele, Podium mit Auktionator-Pult, Bildschirm mit Gebot, Stuhlreihen in Perspektive."""
    img = Image.new("RGB", (W * SS, H * SS), (120, 30, 40)); d = ImageDraw.Draw(img, "RGBA")
    grad(img, (118, 30, 40), (80, 20, 30), 0, 1200); d = ImageDraw.Draw(img, "RGBA")
    for k in range(7): stroke(d, [(k * 180, 0), (k * 180, 1200)], lw=3, color=(96, 24, 32))
    shape(d, [(-20, 1200), (W + 20, 1200), (W + 20, H + 20), (-20, H + 20)], (90, 64, 52), 1, lw=4)
    shape(d, [(230, 330), (850, 330), (850, 700), (230, 700)], (30, 30, 36), 2, lw=6)                                  # Bildschirm
    shape(d, [(140, 1000), (420, 1000), (400, 1240), (160, 1240)], WOOD, 3, lw=5)                                     # Pult
    shape(d, [(120, 980), (440, 980), (440, 1010), (120, 1010)], WOOD_D, 4, lw=4)
    for k in range(3):                                                                                                 # Stuhlreihen
        y = 1500 + k * 150; n = 6 + k
        for j in range(n):
            x = 540 + (j - (n - 1) / 2) * (150 + k * 20)
            shape(d, [(x - 50 - k * 6, y), (x + 50 + k * 6, y), (x + 50 + k * 6, y + 30), (x - 50 - k * 6, y + 30)], (60, 40, 34), 10 + j + k * 10, lw=3)
    return img

def gavel(d, cx, cy, angle, seed=70):
    a = math.radians(angle)
    hx, hy = cx + math.cos(a) * 140, cy - math.sin(a) * 140
    stroke(d, [(cx, cy), (hx, hy)], lw=14, color=(110, 70, 40))
    nx, ny = -math.sin(a), -math.cos(a)
    shape(d, [(hx - nx * 50 - math.cos(a) * 26, hy - ny * 50 + math.sin(a) * 26), (hx + nx * 50 - math.cos(a) * 26, hy + ny * 50 + math.sin(a) * 26),
              (hx + nx * 50 + math.cos(a) * 26, hy + ny * 50 - math.sin(a) * 26), (hx - nx * 50 + math.cos(a) * 26, hy - ny * 50 - math.sin(a) * 26)], (130, 84, 48), seed, lw=4)

def porch_bg():
    """Veranda heute (Nevada, Wuestenlandschaft): Holzboden, Gelaender, Haus-Wand, Abendhimmel."""
    img = Image.new("RGB", (W * SS, H * SS)); grad(img, (250, 190, 140), (255, 226, 190), 0, 1250)
    d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, 1100), (300, 980), (620, 1060), (900, 960), (1100, 1040), (1100, 1250), (-20, 1250)], (200, 150, 120), 1, lw=3)
    shape(d, [(-20, 1250), (W + 20, 1250), (W + 20, H + 20), (-20, H + 20)], WOOD, 2, lw=4)
    for k in range(8): stroke(d, [(0, 1250 + k * 90), (W, 1250 + k * 90)], lw=3, color=WOOD_D)
    stroke(d, [(0, 1180), (W, 1180)], lw=10, color=WOOD_D)
    for x in range(30, W, 90): stroke(d, [(x, 1180), (x, 1250)], lw=8, color=WOOD_D)
    return img

def rocking_chair(d, cx, base, w, tilt=0.0, seed=80):
    shape(d, [(cx - w * 0.4, base - w * 0.55), (cx + w * 0.4, base - w * 0.55), (cx + w * 0.36, base - w * 0.5), (cx - w * 0.36, base - w * 0.5)], WOOD, seed, lw=4)
    shape(d, [(cx + w * 0.25, base - w * 0.55), (cx + w * 0.38, base - w * 0.55), (cx + w * 0.48, base - w * 1.3), (cx + w * 0.36, base - w * 1.3)], WOOD, seed + 1, lw=4)
    for sx in (-0.3, 0.3): stroke(d, [(cx + w * sx, base - w * 0.5), (cx + w * sx, base - w * 0.08)], lw=8, color=WOOD_D)
    stroke(d, ellipse_pts(cx, base - w * 0.5, w * 0.55, w * 0.45, 20, 50, 130), lw=10, color=WOOD_D)
