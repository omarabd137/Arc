"""ARC Short #02 – Requisiten und Orte im Crayon-Prinzip: Figuren simpel, Requisiten und Orte GENAU
(echte Form, echte Schrift, Perspektive, graue Cel-Schatten, gedaempfte Farben)."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "01_lamborghini"))
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from crayon_kit import S, sh, shape, stroke, ellipse_pts, W, H, SS, INK, done
from crayon3 import figure, sticky

F = "C:/Windows/Fonts/"
SCRIPT = F + "BRUSHSCI.TTF"     # Schreibschrift fuer das 50er-Schild
BOLD = F + "ariblk.ttf"
SERIF = F + "georgiab.ttf"
HAND = F + "Inkfree.ttf"
RED, YEL, WHITE = (204, 38, 40), (250, 196, 30), (246, 244, 238)

# ---- Figuren (Aehnlichkeit ueber Merkmale) ----
KROC = dict(skin=(238, 204, 170), hair=(150, 146, 140), hair_hi=(200, 196, 190), top=(58, 62, 74), tie=(150, 40, 44),
            braces=None, trousers=(48, 50, 60), glasses=False, mustache=False, nose=True, big=0.95, hairstyle="enzo")
MAC = dict(skin=(240, 200, 160), hair=(52, 40, 34), hair_hi=(100, 80, 66), top=(244, 244, 240), tie=(40, 40, 46),
           braces=None, trousers=(70, 70, 78), glasses=False, mustache=False, nose=True, big=1.15, hairstyle="ferruccio")
DICK = dict(skin=(238, 198, 158), hair=(60, 46, 38), hair_hi=(108, 86, 70), top=(244, 244, 240), tie=(40, 40, 46),
            braces=None, trousers=(70, 70, 78), glasses=False, mustache=False, nose=True, big=0.98, hairstyle="ferruccio")
GUEST = [dict(skin=s, hair=h, hair_hi=sh(h, 1.4), top=t, tie=None, braces=None, trousers=(60, 60, 70), glasses=False,
              mustache=False, nose=False, big=1.0, hairstyle="ferruccio")
         for s, h, t in [((236, 196, 160), (90, 60, 40), (120, 150, 190)), ((200, 150, 110), (30, 26, 24), (190, 120, 110)),
                         ((240, 206, 176), (200, 160, 90), (130, 170, 130)), ((180, 130, 96), (40, 30, 26), (210, 180, 120)),
                         ((236, 200, 170), (120, 80, 50), (150, 130, 170)), ((228, 190, 150), (60, 44, 36), (110, 120, 130))]]

def text(img, s, cx, y, size, font=BOLD, fill=INK, stroke_w=0, stroke_fill=INK, anchor="mm", angle=0):
    f = ImageFont.truetype(font, int(size * SS))
    if angle == 0:
        ImageDraw.Draw(img).text((cx * SS, y * SS), s, font=f, fill=fill, anchor=anchor, stroke_width=int(stroke_w * SS), stroke_fill=stroke_fill)
        return
    tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((cx * SS, y * SS), s, font=f, fill=fill, anchor=anchor, stroke_width=int(stroke_w * SS), stroke_fill=stroke_fill)
    tmp = tmp.rotate(angle, center=(cx * SS, y * SS), resample=Image.BICUBIC)
    img.paste(tmp, (0, 0), tmp)

def grad(img, top, bottom, y0, y1):
    d = ImageDraw.Draw(img)
    for y in range(int(y0 * SS), int(y1 * SS)):
        k = (y - y0 * SS) / max(1, (y1 - y0) * SS)
        d.line([(0, y), (W * SS, y)], fill=tuple(int(a + (b - a) * k) for a, b in zip(top, bottom)))

def palm(d, x, base, h, seed=0):
    for i in range(12):                                   # leicht gebogener Stamm
        t0, t1 = i / 12, (i + 1) / 12
        x0, x1 = x + math.sin(t0 * 1.6) * 30, x + math.sin(t1 * 1.6) * 30
        shape(d, [(x0 - 14, base - t0 * h), (x0 + 14, base - t0 * h), (x1 + 12, base - t1 * h), (x1 - 12, base - t1 * h)], (150, 120, 88), seed + i, lw=3)
    tx, ty = x + math.sin(1.6) * 30, base - h
    for k, a in enumerate((-160, -120, -70, -20, 20, 200, 250)):
        r = math.radians(a)
        pts = [(tx, ty)]
        for j in range(1, 6):
            L = j * 44
            pts.append((tx + math.cos(r) * L, ty + math.sin(r) * L * 0.55 + j * j * 4))
        back = [(px, py + 18 - j * 2) for j, (px, py) in enumerate(reversed(pts))]
        shape(d, pts + back, (96, 150, 84), seed + 50 + k, lw=3)

def car50(d, x, base, w, color, seed=900):
    """1950er Limousine (Seitenansicht): runde Kotfluegel, Chrom-Stossstangen, Weisswandreifen."""
    h = w * 0.33
    body = [(x, base - h * 0.25), (x + w * 0.04, base - h * 0.55), (x + w * 0.28, base - h * 0.6), (x + w * 0.36, base - h * 0.98),
            (x + w * 0.68, base - h * 1.0), (x + w * 0.78, base - h * 0.62), (x + w * 0.97, base - h * 0.55), (x + w, base - h * 0.25), (x + w * 0.5, base - h * 0.18)]
    shape(d, body, color, seed)
    shape(d, [(x + w * 0.39, base - h * 0.62), (x + w * 0.42, base - h * 0.9), (x + w * 0.66, base - h * 0.92), (x + w * 0.74, base - h * 0.62)], (170, 206, 226), seed + 1, lw=3)
    stroke(d, [(x + w * 0.55, base - h * 0.92), (x + w * 0.55, base - h * 0.6)], lw=3)
    for bx in ((x - 6, x + w * 0.1), (x + w * 0.9, x + w + 6)):
        stroke(d, [(bx[0], base - h * 0.28), (bx[1], base - h * 0.28)], lw=9, color=(210, 210, 216))
    stroke(d, [(x + w * 0.08, base - h * 0.42), (x + w * 0.92, base - h * 0.42)], lw=4, color=(220, 220, 226))
    for cx in (x + w * 0.22, x + w * 0.8):
        r = h * 0.3
        shape(d, ellipse_pts(cx, base - r, r, r), (30, 28, 30), seed + 2)
        shape(d, ellipse_pts(cx, base - r, r * 0.62, r * 0.62), (244, 244, 240), seed + 3, lw=3)
        shape(d, ellipse_pts(cx, base - r, r * 0.34, r * 0.34), (190, 190, 198), seed + 4, lw=3)

def mcd_stand_1948(img, cx=540, base=1330, scale=1.0, lit=True, name="McDonald's"):
    """Das Original in San Bernardino (achteckiger Walk-up-Stand, grosse Fenster, Pylon-Schild, Preistafel)."""
    d = ImageDraw.Draw(img, "RGBA")
    s = scale
    hw, h = 300 * s, 300 * s                 # halbe Breite der Frontseite, Wandhoehe
    side = 130 * s
    roof = 46 * s
    # Seitenwaende des Achtecks (perspektivisch schraeg)
    for sx in (-1, 1):
        x0 = cx + sx * hw
        pts = [(x0, base), (x0 + sx * side, base - 40 * s), (x0 + sx * side, base - h - 30 * s), (x0, base - h)]
        shape(d, pts, (226, 224, 216), 10 + sx, lw=4)
        shape(d, [(x0 + sx * 18 * s, base - h * 0.88), (x0 + sx * (side - 16 * s), base - h * 0.9 - 30 * s),
                  (x0 + sx * (side - 16 * s), base - h * 0.42 - 34 * s), (x0 + sx * 18 * s, base - h * 0.42)], (150, 190, 214), 20 + sx, lw=3)
    # Frontwand: untere Kachelzone rot-weiss, oben Fensterband
    shape(d, [(cx - hw, base), (cx + hw, base), (cx + hw, base - h), (cx - hw, base - h)], (240, 238, 230), 30, lw=4)
    for k in range(12):
        x = cx - hw + k * (2 * hw / 12)
        d.rectangle(S(x, base - h * 0.34, x + hw / 12, base - 4), fill=RED + (255,))
    stroke(d, [(cx - hw, base - h * 0.34), (cx + hw, base - h * 0.34)], lw=4)
    # Durchreiche-Fenster mit Theke und Personal in weissen Papiermuetzen
    for k in range(3):
        wx = cx - hw + 20 * s + k * (2 * hw - 40 * s) / 3
        ww = (2 * hw - 40 * s) / 3 - 14 * s
        shape(d, [(wx, base - h * 0.4), (wx + ww, base - h * 0.4), (wx + ww, base - h * 0.92), (wx, base - h * 0.92)], (168, 204, 224), 40 + k, lw=3)
        px = wx + ww / 2
        shape(d, ellipse_pts(px, base - h * 0.62, 26 * s, 26 * s), (236, 198, 164), 50 + k, lw=3)      # Kopf
        shape(d, [(px - 24 * s, base - h * 0.68), (px + 24 * s, base - h * 0.68), (px + 18 * s, base - h * 0.78), (px - 18 * s, base - h * 0.78)], WHITE, 60 + k, lw=3)
        shape(d, ellipse_pts(px, base - h * 0.44, 40 * s, 22 * s, 30, 180, 360), WHITE, 70 + k, lw=3)
        d.ellipse(S(px - 9 * s, base - h * 0.62 - 3, px - 3 * s, base - h * 0.62 + 4), fill=INK)
        d.ellipse(S(px + 3 * s, base - h * 0.62 - 3, px + 9 * s, base - h * 0.62 + 4), fill=INK)
    shape(d, [(cx - hw - 6, base - h * 0.4), (cx + hw + 6, base - h * 0.4), (cx + hw + 6, base - h * 0.36), (cx - hw - 6, base - h * 0.36)], (200, 200, 206), 80, lw=3)
    # Flachdach mit Ueberstand + Schriftband
    shape(d, [(cx - hw - side - 20 * s, base - h - 30 * s), (cx + hw + side + 20 * s, base - h - 30 * s),
              (cx + hw + 40 * s, base - h - roof - 30 * s), (cx - hw - 40 * s, base - h - roof - 30 * s)], (236, 234, 226), 90, lw=4)
    shape(d, [(cx - hw, base - h), (cx + hw, base - h), (cx + hw, base - h - 30 * s), (cx - hw, base - h - 30 * s)], RED, 91, lw=4)
    text(img, "HAMBURGERS · FRIES · SHAKES", cx, base - h - 15 * s, 22 * s, BOLD, WHITE)
    # Preistafel 1948 (belegt: Hamburger 15¢, Cheeseburger 19¢, Fries 10¢, Shakes 20¢)
    mx, my = cx + hw * 0.52, base - h * 0.2
    shape(d, [(mx - 86 * s, my - 52 * s), (mx + 86 * s, my - 52 * s), (mx + 86 * s, my + 52 * s), (mx - 86 * s, my + 52 * s)], (252, 250, 240), 95, lw=3)
    for i, (a, b) in enumerate((("HAMBURGER", "15¢"), ("CHEESEBURGER", "19¢"), ("FRIES", "10¢"), ("SHAKE", "20¢"))):
        text(img, a, mx - 78 * s, my - 36 * s + i * 24 * s, 11 * s, BOLD, INK, anchor="lm")
        text(img, b, mx + 78 * s, my - 36 * s + i * 24 * s, 14 * s, BOLD, RED, anchor="rm")
    # Pylon-Schild links: weisse Tafel, rote Schreibschrift
    px, top = max(170, cx - hw - side - 60 * s), base - h - 330 * s
    shape(d, [(px - 12 * s, top + 180 * s), (px + 12 * s, top + 180 * s), (px + 12 * s, base), (px - 12 * s, base)], (170, 170, 178), 100, lw=3)
    shape(d, [(px - 150 * s, top), (px + 150 * s, top), (px + 150 * s, top + 190 * s), (px - 150 * s, top + 190 * s)], WHITE, 101, lw=5)
    shape(d, [(px - 140 * s, top + 140 * s), (px + 140 * s, top + 140 * s), (px + 140 * s, top + 180 * s), (px - 140 * s, top + 180 * s)], RED, 102, lw=3)
    if name:
        text(img, name, px, top + 72 * s, 70 * s, SCRIPT, RED, stroke_w=1, stroke_fill=sh(RED, 0.6))
    text(img, "FAMOUS HAMBURGERS", px, top + 160 * s, 20 * s, BOLD, WHITE)
    if lit:   # Neon-Glow um das Schild
        glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).rectangle(S(px - 160 * s, top - 10 * s, px + 160 * s, top + 200 * s), outline=(255, 220, 120, 120), width=int(14 * SS))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10 * SS))) if img.mode == "RGBA" else img.paste(glow.filter(ImageFilter.GaussianBlur(10 * SS)), (0, 0), glow.filter(ImageFilter.GaussianBlur(10 * SS)))
    return px, top

def california_bg(horizon=1330, dusk=False):
    """San Bernardino um 1950: warmer Himmel, Berge, Palmen, Asphalt-Parkplatz mit Markierungen."""
    img = Image.new("RGB", (W * SS, H * SS))
    grad(img, (255, 196, 140) if dusk else (150, 200, 236), (255, 226, 176) if dusk else (214, 232, 244), 0, horizon)
    d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, horizon - 150), (180, horizon - 330), (360, horizon - 210), (560, horizon - 380), (800, horizon - 240), (1100, horizon - 340), (1100, horizon), (-20, horizon)], (176, 160, 176) if dusk else (170, 182, 200), 1, lw=3)
    shape(d, [(-20, horizon), (W + 20, horizon), (W + 20, H + 20), (-20, H + 20)], (120, 118, 122), 2, lw=4)
    for k in range(-1, 8):                     # Parkplatz-Linien in Perspektive
        x0 = -200 + k * 190
        stroke(d, [(x0 + 60, horizon + 40), (x0 - 80, H)], lw=5, color=(236, 232, 210))
    return img, d

def dollar_bill(img, cx, cy, w, angle=0, seed=0, value="100"):
    """US-Dollarschein im Cartoon: gruen-graues Papier, Rahmen, ovales Portraet, Wertzahlen in den Ecken."""
    hgt = w * 0.43
    lay = Image.new("RGBA", (int(w * SS) + 40, int(hgt * SS) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    o = 20
    d.rounded_rectangle([o, o, o + w * SS, o + hgt * SS], radius=int(6 * SS), fill=(206, 222, 196), outline=INK, width=int(4 * SS))
    d.rectangle([o + 10 * SS, o + 10 * SS, o + (w - 10) * SS, o + (hgt - 10) * SS], outline=(84, 120, 84), width=int(3 * SS))
    for k in range(9):                         # Guilloche-Linien
        y = o + (14 + k * (hgt - 28) / 8) * SS
        d.line([(o + 14 * SS, y), (o + (w * 0.3) * SS, y)], fill=(150, 180, 146), width=int(1.5 * SS))
        d.line([(o + (w * 0.7) * SS, y), (o + (w - 14) * SS, y)], fill=(150, 180, 146), width=int(1.5 * SS))
    pcx, pcy = o + w * SS / 2, o + hgt * SS / 2
    d.ellipse([pcx - w * 0.14 * SS, pcy - hgt * 0.34 * SS, pcx + w * 0.14 * SS, pcy + hgt * 0.34 * SS], fill=(186, 206, 176), outline=(70, 104, 70), width=int(3 * SS))
    d.ellipse([pcx - w * 0.055 * SS, pcy - hgt * 0.22 * SS, pcx + w * 0.055 * SS, pcy + hgt * 0.02 * SS], fill=(120, 150, 116))
    d.chord([pcx - w * 0.1 * SS, pcy - hgt * 0.02 * SS, pcx + w * 0.1 * SS, pcy + hgt * 0.4 * SS], 180, 360, fill=(120, 150, 116))
    f = ImageFont.truetype(BOLD, int(hgt * 0.2 * SS)); fs = ImageFont.truetype(SERIF, int(hgt * 0.09 * SS))
    for (x, y) in ((o + 26 * SS, o + 22 * SS), (o + (w - 26) * SS, o + 22 * SS), (o + 26 * SS, o + (hgt - 22) * SS), (o + (w - 26) * SS, o + (hgt - 22) * SS)):
        d.text((x, y), value, font=f, fill=(60, 96, 62), anchor="mm")
    d.text((pcx, o + 20 * SS), "THE UNITED STATES OF AMERICA", font=fs, fill=(50, 80, 52), anchor="mm")
    d.text((pcx, o + (hgt - 18) * SS), {"1": "ONE DOLLAR", "5": "FIVE DOLLARS", "20": "TWENTY DOLLARS"}.get(value, "ONE HUNDRED DOLLARS"), font=fs, fill=(50, 80, 52), anchor="mm")
    lay = lay.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(lay, (int(cx * SS - lay.width / 2), int(cy * SS - lay.height / 2)), lay)

def contract(img, cx, cy, w, amount="$2,700,000", seed=0):
    """Kaufvertrag 1961: Papier mit Schattenkante, Titel, Textzeilen, Betrag, zwei Unterschriftslinien."""
    d = ImageDraw.Draw(img, "RGBA")
    h = w * 1.3
    shape(d, [(cx - w / 2 + 16, cy - h / 2 + 16), (cx + w / 2 + 16, cy - h / 2 + 16), (cx + w / 2 + 16, cy + h / 2 + 16), (cx - w / 2 + 16, cy + h / 2 + 16)], (0, 0, 0, 60), seed, lw=0)
    shape(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], (250, 248, 238), seed + 1, lw=4)
    text(img, "AGREEMENT OF SALE", cx, cy - h / 2 + 60, w * 0.075, SERIF, INK)
    text(img, "McDonald's · 1961", cx, cy - h / 2 + 110, w * 0.05, SERIF, (90, 90, 96))
    for k in range(9):
        y = cy - h / 2 + 170 + k * 34
        stroke(d, [(cx - w * 0.4, y), (cx + w * (0.4 if k % 3 else 0.25), y)], lw=3, color=(180, 180, 186))
    text(img, amount, cx, cy + h * 0.17, w * 0.15, BOLD, (30, 110, 60), stroke_w=2, stroke_fill=INK)
    for sx, who in ((-1, "R. A. Kroc"), (1, "R. & M. McDonald")):
        x = cx + sx * w * 0.22
        stroke(d, [(x - w * 0.18, cy + h * 0.38), (x + w * 0.18, cy + h * 0.38)], lw=3)
        text(img, who, x, cy + h * 0.42, w * 0.035, SERIF, (90, 90, 96))

# ---------------- weitere Requisiten Short #02 ----------------
CHROME, CHROME_D = (214, 218, 226), (150, 156, 168)

def multimixer(d, cx, base, w, seed=500):
    """Prince-Castle-Multimixer (5 Spindeln), Frontansicht: Chromkopf, Saeule, 5 Edelstahlbecher, gruener Fuss."""
    h = w * 1.05
    shape(d, [(cx - w * 0.5, base - h * 0.08), (cx + w * 0.5, base - h * 0.08), (cx + w * 0.46, base), (cx - w * 0.46, base)], (96, 150, 120), seed, lw=4)
    shape(d, [(cx - w * 0.07, base - h * 0.08), (cx + w * 0.07, base - h * 0.08), (cx + w * 0.07, base - h * 0.82), (cx - w * 0.07, base - h * 0.82)], CHROME, seed + 1, lw=4)
    shape(d, [(cx - w * 0.52, base - h * 0.82), (cx + w * 0.52, base - h * 0.82), (cx + w * 0.48, base - h), (cx - w * 0.48, base - h)], CHROME, seed + 2, lw=5)
    stroke(d, [(cx - w * 0.44, base - h * 0.95), (cx + w * 0.44, base - h * 0.95)], lw=4, color=(255, 255, 255))
    for k in range(5):
        x = cx - w * 0.4 + k * w * 0.2
        stroke(d, [(x, base - h * 0.82), (x, base - h * 0.5)], lw=5, color=CHROME_D)
        shape(d, [(x - w * 0.075, base - h * 0.56), (x + w * 0.075, base - h * 0.56), (x + w * 0.06, base - h * 0.2), (x - w * 0.06, base - h * 0.2)], CHROME, seed + 10 + k, lw=4)
        stroke(d, [(x - w * 0.045, base - h * 0.52), (x - w * 0.035, base - h * 0.24)], lw=3, color=(255, 255, 255))

def us_map(d, cx, cy, w, fill=(238, 226, 196), seed=600):
    """Umriss der USA (48 Staaten, vereinfacht). Gibt eine Funktion lon/lat -> x/y zurueck."""
    pts = [(-124.7, 48.4), (-123, 46), (-124.2, 42), (-121.5, 35.5), (-117.1, 32.5), (-114.7, 32.7), (-111, 31.3), (-106.5, 31.8), (-103, 29), (-99.5, 27.5),
           (-97.2, 25.9), (-97.4, 27.8), (-94.7, 29.4), (-90, 29.2), (-89, 30.3), (-85, 29.7), (-83, 29), (-82.5, 27), (-81, 25.1), (-80.1, 26.8), (-81.3, 30.5),
           (-80.9, 32), (-77.9, 34), (-75.5, 35.3), (-76, 37.5), (-74, 40.5), (-70.7, 41.6), (-70, 43.6), (-67, 44.8), (-68.5, 47.3), (-71, 45), (-75, 45),
           (-79.2, 43.4), (-83, 42), (-82.4, 45.3), (-84.8, 46.5), (-88.5, 47.6), (-92, 46.8), (-95.2, 49), (-123.3, 49)]
    lon0, lon1, lat0, lat1 = -125, -66, 24, 50
    h = w * (lat1 - lat0) / (lon1 - lon0) * 1.25
    def P(lon, lat): return (cx - w / 2 + (lon - lon0) / (lon1 - lon0) * w, cy + h / 2 - (lat - lat0) / (lat1 - lat0) * h)
    shape(d, [P(*p) for p in pts], fill, seed, lw=5)
    return P

CITIES = [(-87.9, 42.0), (-117.3, 34.1), (-118.2, 34.0), (-112.1, 33.4), (-104.9, 39.7), (-96.8, 32.8), (-95.4, 29.8), (-90.2, 38.6), (-84.4, 33.7),
          (-80.2, 25.8), (-77.0, 38.9), (-74.0, 40.7), (-71.1, 42.4), (-83.0, 42.3), (-93.3, 45.0), (-122.3, 47.6), (-122.4, 37.8), (-86.8, 36.2),
          (-81.7, 41.5), (-75.2, 39.9), (-97.5, 35.5), (-111.9, 40.8), (-106.6, 35.1), (-90.1, 30.0), (-85.8, 38.3)]

def arch_icon(d, x, y, s, seed=700):
    """Zwei goldene Boegen als Standort-Pin (eigene Zeichnung)."""
    for k in (-1, 1):
        pts = [(x + k * s * 0.5 + math.cos(math.radians(a)) * s * 0.5 * k * -1, y - math.sin(math.radians(a)) * s * 1.1) for a in range(0, 181, 15)]
        stroke(d, pts, lw=max(4, s * 0.2), color=INK)
        stroke(d, pts, lw=max(2, s * 0.12), color=YEL)

def golden_arches_store(img, cx, base, scale=1.0, crowd=True):
    """1950er-McDonald's nach Kroc-Standard: rot-weisse Kacheln, Schraegdach, zwei grosse goldene Boegen, Pylon mit Bogen."""
    d = ImageDraw.Draw(img, "RGBA"); s = scale
    hw, h = 320 * s, 260 * s
    shape(d, [(cx - hw, base), (cx + hw, base), (cx + hw, base - h * 0.9), (cx - hw, base - h * 1.15)], (244, 242, 236), 800, lw=4)
    for k in range(16):
        x = cx - hw + k * (2 * hw / 16)
        if k % 2 == 0: d.rectangle(S(x, base - h * 0.45, x + 2 * hw / 16, base - 4), fill=RED + (255,))
    shape(d, [(cx - hw + 30 * s, base - h * 0.5), (cx + hw - 30 * s, base - h * 0.5), (cx + hw - 30 * s, base - h * 0.85), (cx - hw + 30 * s, base - h * 1.05)], (168, 204, 224), 801, lw=3)
    shape(d, [(cx - hw - 30 * s, base - h * 1.18), (cx + hw + 30 * s, base - h * 0.86), (cx + hw + 30 * s, base - h * 0.78), (cx - hw - 30 * s, base - h * 1.1)], (236, 234, 226), 802, lw=4)
    for k in (-1, 1):            # die zwei grossen Boegen durch das Dach
        ax = cx + k * hw * 0.62
        pts = [(ax + math.cos(math.radians(a)) * 120 * s, base - math.sin(math.radians(a)) * 460 * s) for a in range(0, 181, 10)]
        stroke(d, pts, lw=34 * s, color=INK); stroke(d, pts, lw=24 * s, color=YEL)
    px, top = cx + hw + 120 * s, base - 520 * s
    shape(d, [(px - 10 * s, top + 160 * s), (px + 10 * s, top + 160 * s), (px + 10 * s, base), (px - 10 * s, base)], (170, 170, 178), 803, lw=3)
    pts = [(px + math.cos(math.radians(a)) * 90 * s, top + 160 * s - math.sin(math.radians(a)) * 150 * s) for a in range(0, 181, 10)]
    stroke(d, pts, lw=26 * s, color=INK); stroke(d, pts, lw=18 * s, color=YEL)
    shape(d, [(px - 120 * s, top + 120 * s), (px + 120 * s, top + 120 * s), (px + 120 * s, top + 190 * s), (px - 120 * s, top + 190 * s)], RED, 804, lw=4)
    text(img, "McDonald's", px, top + 155 * s, 40 * s, SCRIPT, WHITE)
    text(img, "HAMBURGERS", cx, base - h * 0.95 + 40 * s, 30 * s, BOLD, RED)

def closed_sign(img, cx, cy, w, angle=-8):
    d0 = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(d0)
    h = w * 0.36
    d.rectangle(S(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=(250, 248, 240), outline=INK, width=int(5 * SS))
    d.line(S(cx - w * 0.3, cy - h / 2, cx, cy - h * 1.4, cx + w * 0.3, cy - h / 2), fill=INK, width=int(4 * SS))
    f = ImageFont.truetype(BOLD, int(h * 0.62 * SS))
    d.text((cx * SS, cy * SS), "CLOSED", font=f, fill=RED, anchor="mm")
    d0 = d0.rotate(angle, center=(cx * SS, cy * SS), resample=Image.BICUBIC)
    img.paste(d0, (0, 0), d0)

def world_map(d, cx, cy, w, seed=900):
    """Vereinfachte Kontinente (Cartoon), gibt lon/lat -> x/y zurueck."""
    h = w * 0.55
    def P(lon, lat): return (cx + lon / 180 * w / 2, cy - lat / 90 * h / 2)
    conts = {
        "na": [(-165, 65), (-140, 70), (-95, 72), (-75, 62), (-60, 50), (-80, 30), (-97, 18), (-85, 10), (-105, 22), (-118, 32), (-125, 48), (-150, 60)],
        "sa": [(-80, 10), (-60, 8), (-35, -7), (-40, -22), (-58, -38), (-70, -55), (-75, -40), (-72, -15), (-80, -2)],
        "eu": [(-10, 36), (-9, 44), (-4, 48), (5, 52), (10, 58), (25, 70), (40, 66), (40, 45), (28, 40), (15, 38)],
        "af": [(-17, 15), (-10, 30), (10, 37), (32, 31), (43, 12), (51, 11), (40, -15), (33, -26), (20, -35), (12, -18), (8, 4), (-8, 5)],
        "as": [(40, 45), (40, 66), (70, 74), (110, 77), (140, 72), (170, 66), (140, 50), (122, 30), (108, 18), (100, 2), (78, 8), (68, 22), (55, 26), (48, 30)],
        "au": [(114, -22), (130, -12), (142, -11), (153, -27), (147, -38), (130, -32), (115, -34)],
    }
    for i, pts in enumerate(conts.values()):
        shape(d, [P(*p) for p in pts], (226, 214, 184), seed + i, lw=4)
    return P
