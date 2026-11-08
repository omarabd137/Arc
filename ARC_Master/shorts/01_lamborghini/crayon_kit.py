"""ARC im Crayon-Prinzip (eigene Zeichnungen):
1) echter, lizenzierter Ort als UNSCHARFER Hintergrund (Bokeh/Tiefenschaerfe)
2) scharfe Cartoon-Figuren: grosser runder Kopf, dicke leicht zittrige Handzeichnungs-Kontur,
   flache Farben + weicher Cel-Schatten unten am Gesicht, Glanz im Haar, kleine ovale Augen."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

SS = 2
W, H = 1080, 1920
F = "C:/Windows/Fonts/"
INK = (30, 26, 30)
LW = 5          # Linienstaerke (Crayon: glatt, gleichmaessig, eher duenn)

def S(*v): return [x * SS for x in v]
def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3])

def blurred_place(path, fx=0.5, fy=0.5, blur=14, bright=0.92, sat=0.95):
    src = Image.open(path).convert("RGB")
    s = max(W / src.width, H / src.height) * 1.06
    src = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.LANCZOS)
    x, y = int((src.width - W) * fx), int((src.height - H) * fy)
    img = src.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(blur))
    img = ImageEnhance.Brightness(ImageEnhance.Color(img).enhance(sat)).enhance(bright)
    return img.resize((W * SS, H * SS), Image.LANCZOS)

# ---- Handzeichnungs-Linien: leicht zitternde Konturen ----
def wobble_poly(pts, seed, amp=0.25):
    rnd = random.Random(seed)
    out = []
    for i in range(len(pts)):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 14))
        for k in range(n):
            t = k / n
            out.append((x0 + (x1 - x0) * t + rnd.uniform(-amp, amp), y0 + (y1 - y0) * t + rnd.uniform(-amp, amp)))
    return out

def ellipse_pts(cx, cy, rx, ry, n=90, a0=0, a1=360):
    return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]

def shape(d, pts, fill, seed=0, lw=LW, closed=True):
    w = wobble_poly(pts, seed) if closed else pts
    d.polygon([(x * SS, y * SS) for x, y in w], fill=fill)
    d.line([(x * SS, y * SS) for x, y in (w + [w[0]] if closed else w)], fill=INK, width=int(lw * SS), joint="curve")

def stroke(d, pts, lw=LW, color=INK):
    d.line([(x * SS, y * SS) for x, y in pts], fill=color, width=int(lw * SS), joint="curve")

# ---- Figuren (Aehnlichkeit ueber Merkmale) ----
ENZO = dict(skin=(242, 206, 168), hair=(238, 238, 240), hair_hi=(255, 255, 255), top=(236, 234, 226), tie=(140, 104, 76),
            braces=(96, 64, 44), trousers=(66, 66, 74), glasses=True, mustache=False, nose=True, big=1.12, hairstyle="enzo")
FERRUCCIO = dict(skin=(238, 196, 152), hair=(44, 32, 26), hair_hi=(96, 74, 60), top=(160, 146, 118), tie=None,
                 braces=None, trousers=(64, 60, 66), glasses=False, mustache=True, nose=False, big=1.0, hairstyle="ferruccio")

def person(img, cx, base, h, p, face=1, expr="neutral", talk=False, seed=1):
    d = ImageDraw.Draw(img, "RGBA")
    R = h * 0.24 * (1.04 if p["big"] > 1 else 1)        # Kopfradius (Crayon: sehr grosser Kopf)
    hy = base - h + R
    neck = hy + R * 0.92
    bw = h * 0.34 * p["big"]
    waist = base - h * 0.2
    # Bodenschatten
    d.ellipse(S(cx - bw * 0.6, base - 12, cx + bw * 0.6, base + 12), fill=(0, 0, 0, 70))
    # Beine (kurz, Crayon-artig)
    for sx in (-1, 1):
        lx = cx + sx * bw * 0.2
        shape(d, [(lx - bw * 0.13, waist), (lx + bw * 0.13, waist), (lx + bw * 0.12, base - 16), (lx - bw * 0.12, base - 16)], p["trousers"], seed + sx)
        shape(d, ellipse_pts(lx + face * 10, base - 12, bw * 0.17, 16), (34, 28, 26), seed + 5 + sx)
    # Koerper (abgerundetes Trapez)
    body = ellipse_pts(cx, neck + (waist - neck) * 0.15, bw * 0.5, (waist - neck) * 0.3, 40, 180, 360) + [(cx + bw * 0.48, waist + 6), (cx - bw * 0.48, waist + 6)]
    shape(d, body, p["top"], seed + 10)
    # Cel-Schatten auf dem Koerper
    d.polygon(S(cx - face * bw * 0.48, neck + 30, cx - face * bw * 0.2, neck + 30, cx - face * bw * 0.25, waist, cx - face * bw * 0.46, waist), fill=sh(p["top"], 0.86) + (160,))
    if p["braces"]:
        for sx in (-1, 1):
            stroke(d, [(cx + sx * bw * 0.22, neck + 20), (cx + sx * bw * 0.2, waist)], lw=9, color=p["braces"])
    if p["tie"]:
        shape(d, [(cx - 13, neck + 18), (cx + 13, neck + 18), (cx + 20, waist - 60), (cx, waist - 30), (cx - 20, waist - 60)], p["tie"], seed + 11, lw=4)
    if p["hairstyle"] == "ferruccio":   # offener Kragen
        shape(d, [(cx - 34, neck + 8), (cx, neck + 70), (cx + 34, neck + 8)], (236, 232, 222), seed + 12, lw=4)
    # Arme
    for sx in (-1, 1):
        x0 = cx + sx * bw * 0.42
        pts = [(x0, neck + 45), (x0 + sx * 26, neck + 160), (x0 + sx * 18, waist - 30)]
        stroke(d, pts, lw=46, color=INK); stroke(d, pts, lw=34, color=sh(p["top"], 0.95))
        shape(d, ellipse_pts(x0 + sx * 18, waist - 26, 24, 24, 30), p["skin"], seed + 20 + sx, lw=5)
    # Ohr hinten
    shape(d, ellipse_pts(cx - face * R * 0.9, hy + R * 0.08, R * 0.14, R * 0.2), sh(p["skin"], 0.96), seed + 29, lw=5)
    # Kopf
    shape(d, ellipse_pts(cx, hy, R, R * 0.98), p["skin"], seed + 30)
    # weicher, runder Cel-Schatten (versetzter Kreis, auf den Kopf begrenzt) wie bei Crayon
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse(S(cx - R * 0.95, hy - R * 0.93, cx + R * 0.95, hy + R * 0.93), fill=255)
    cut = Image.new("L", img.size, 0)
    ImageDraw.Draw(cut).ellipse(S(cx - R * 1.05 + face * R * 0.18, hy - R * 1.25, cx + R * 1.05 + face * R * 0.18, hy + R * 0.6), fill=255)
    from PIL import ImageChops
    m = ImageChops.subtract(m, cut).filter(ImageFilter.GaussianBlur(3 * SS))
    img.paste(Image.new("RGB", img.size, sh(p["skin"], 0.88)), (0, 0), m.point(lambda v: int(v * 0.8)))
    d = ImageDraw.Draw(img, "RGBA")
    # Haare
    if p["hairstyle"] == "enzo":
        # weisses, nach hinten gekaemmtes Haar mit Volumen, hoher Haaransatz
        hair = ellipse_pts(cx - face * R * 0.08, hy - R * 0.38, R * 1.02, R * 0.72, 60, 175, 365)
        shape(d, hair + [(cx + R * 0.9, hy - R * 0.1), (cx - R * 0.9, hy - R * 0.1)], p["hair"], seed + 31)
        for k in range(3):
            stroke(d, ellipse_pts(cx - face * R * 0.1, hy - R * (0.55 - k * 0.12), R * 0.7, R * 0.2, 20, 200, 330), lw=3, color=(196, 196, 204))
    else:
        hair = ellipse_pts(cx, hy - R * 0.32, R * 1.0, R * 0.7, 60, 180, 360)
        shape(d, hair + [(cx + R * 0.95, hy - R * 0.15), (cx + R * 0.4, hy - R * 0.36), (cx - R * 0.3, hy - R * 0.4), (cx - R * 0.95, hy - R * 0.12)], p["hair"], seed + 31)
        d.chord(S(cx - R * 0.6, hy - R * 0.95, cx + R * 0.1, hy - R * 0.55), 190, 330, fill=p["hair_hi"])
    ex = cx + face * R * 0.18
    ey = hy + R * 0.02
    # Augen / Brille
    if p["glasses"]:
        for k in (-1, 1):
            gx = ex + k * R * 0.32
            shape(d, [(gx - R * 0.26, ey - R * 0.15), (gx + R * 0.26, ey - R * 0.15), (gx + R * 0.24, ey + R * 0.12), (gx - R * 0.24, ey + R * 0.12)], (30, 32, 38), seed + 40 + k, lw=5)
            stroke(d, [(gx - R * 0.17, ey - R * 0.08), (gx - R * 0.05, ey - R * 0.1)], lw=4, color=(150, 158, 170))
        stroke(d, [(ex - R * 0.07, ey - R * 0.1), (ex + R * 0.07, ey - R * 0.1)], lw=5)
    else:
        for k in (-1, 1):
            gx = ex + k * R * 0.3
            shape(d, ellipse_pts(gx, ey, R * 0.06, R * 0.1, 24), (36, 30, 30), seed + 40 + k, lw=1)
    # Brauen
    tilt = {"neutral": 0, "angry": 0.08, "smug": -0.05, "worried": -0.1}[expr]
    bc = (190, 190, 198) if p["hair"][0] > 200 else p["hair"]
    for k in (-1, 1):
        gx = ex + k * R * 0.3
        stroke(d, [(gx - k * R * 0.1, ey - R * (0.25 - tilt)), (gx + k * R * 0.14, ey - R * (0.28 + tilt * 0.4))], lw=8, color=bc)
    # Nase
    if p["nose"]:
        shape(d, [(ex + face * R * 0.02, ey + R * 0.02), (ex + face * R * 0.2, ey + R * 0.3), (ex - face * R * 0.02, ey + R * 0.32)], sh(p["skin"], 0.88), seed + 50, lw=5)
    # Schnurrbart / Mund
    my = ey + R * (0.45 if p["nose"] else 0.33)
    if p["mustache"]:
        shape(d, ellipse_pts(ex, my - R * 0.04, R * 0.26, R * 0.09, 30, 180, 360) + [(ex + R * 0.26, my + R * 0.02), (ex - R * 0.26, my + R * 0.02)], p["hair"], seed + 51, lw=4)
        my += R * 0.08
    if talk:
        shape(d, ellipse_pts(ex, my + R * 0.04, R * 0.09, R * 0.08, 24), (120, 50, 50), seed + 52, lw=4)
    elif expr == "smug":
        stroke(d, ellipse_pts(ex + face * R * 0.05, my - R * 0.06, R * 0.13, R * 0.08, 16, 20, 150), lw=6)
    elif expr == "angry":
        stroke(d, ellipse_pts(ex, my + R * 0.08, R * 0.11, R * 0.06, 16, 200, 340), lw=6)
    else:
        stroke(d, [(ex - R * 0.08, my), (ex + R * 0.08, my)], lw=6)

def speech(img, x, y, w, lines, tail):
    d = ImageDraw.Draw(img, "RGBA")
    f = ImageFont.truetype(F + "segoeuib.ttf", 46 * SS)
    lh = 60; h = lh * len(lines) + 56
    shape(d, [(x + w * 0.34, y + h - 8), (x + w * 0.5, y + h - 8), tail], (255, 255, 255), 90, lw=5)
    shape(d, [(x, y + 30), (x + 30, y), (x + w - 30, y), (x + w, y + 30), (x + w, y + h - 30), (x + w - 30, y + h), (x + 30, y + h), (x, y + h - 30)], (255, 255, 255), 91, lw=5)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f) / SS
        d.text(S(x + (w - tw) / 2, y + 28 + i * lh), ln, font=f, fill=INK)

def place_label(img, text, y=180):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(F + "segoeuib.ttf", 64 * SS)
    tw = d.textlength(text, font=f) / SS
    x = (W - tw) / 2
    for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4), (-3, -3), (3, 3), (-3, 3), (3, -3)]:
        d.text(S(x + dx, y + dy), text, font=f, fill=INK)
    d.text(S(x, y), text, font=f, fill=(255, 255, 255))

def done(img):
    return img.resize((W, H), Image.LANCZOS)

if __name__ == "__main__":
    a = blurred_place("assets/tractor_1960.jpg", 0.5, 0.45)
    person(a, 540, 1780, 1000, FERRUCCIO, face=1, expr="smug", seed=3)
    place_label(a, "Italy, 1948")
    a = done(a); a.save("CR_test_1.png")
    b = blurred_place("assets/maranello.jpg", 0.4, 0.5, blur=12)
    person(b, 560, 1800, 1100, ENZO, face=-1, expr="smug", talk=True, seed=7)
    speech(b, 120, 260, 840, ["You may be able to drive a tractor…", "but you'll never handle a Ferrari."], (520, 560))
    b = done(b); b.save("CR_test_2.png")
    sheet = Image.new("RGB", (2 * 540 + 30, 980), (0, 0, 0))
    sheet.paste(a.resize((540, 960)), (10, 10)); sheet.paste(b.resize((540, 960)), (560, 10))
    sheet.save("STIL_CRAYON_TEST.png"); print("ok")
