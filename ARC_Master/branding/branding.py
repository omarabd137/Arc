"""ARC Branding: Profilbild (800x800) + Banner (2560x1440, Safe-Area 1546x423 Mitte).
Stil wie die grossen Kanaele: klares Logo, ein starkes Motiv, eigene Palette (Anthrazit/Tinten-Gruen + Gold)."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
F = "C:/Windows/Fonts/"
BLACK = F + "ariblk.ttf"; BOLD = F + "arialbd.ttf"; SANS = F + "arial.ttf"
BG1, BG2 = (14, 32, 30), (6, 14, 14)          # Tinten-Gruen -> fast Schwarz
GOLD, GOLD_L, GOLD_D = (232, 186, 74), (255, 222, 130), (170, 124, 36)
WHITE = (244, 242, 236)

def grad(w, h, a, b, radial=False, cx=0.5, cy=0.5):
    im = Image.new("RGB", (w, h)); px = im.load()
    for y in range(h):
        for x in range(0, w):
            k = (math.hypot((x / w - cx) * (w / h), y / h - cy) / 0.9) if radial else y / h
            k = min(1, max(0, k)); px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
    return im

def gold_text(img, xy, s, font, anchor="mm", glow=True):
    """Gold-Schrift mit Verlauf, dunkler Kontur und weichem Leuchten."""
    W, H = img.size
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).text(xy, s, font=font, fill=255, anchor=anchor)
    if glow:
        g = m.filter(ImageFilter.GaussianBlur(font.size // 6)).point(lambda v: int(v * 0.55))
        img.paste(Image.new("RGB", (W, H), GOLD), (0, 0), g)
    st = Image.new("L", (W, H), 0); ImageDraw.Draw(st).text(xy, s, font=font, fill=255, anchor=anchor, stroke_width=max(2, font.size // 28))
    img.paste(Image.new("RGB", (W, H), (20, 14, 6)), (0, 0), st)
    bb = m.getbbox(); fill = grad(W, H, GOLD_L, GOLD_D) if bb is None else None
    fillim = Image.new("RGB", (W, H), GOLD); d = ImageDraw.Draw(fillim)
    if bb:
        y0, y1 = bb[1], bb[3]
        for y in range(y0, y1 + 1):
            k = (y - y0) / max(1, y1 - y0); d.line([(0, y), (W, y)], fill=tuple(int(GOLD_L[i] + (GOLD_D[i] - GOLD_L[i]) * k) for i in range(3)))
    img.paste(fillim, (0, 0), m)

def arc_mark(d, cx, cy, r, w, col=GOLD):
    """das ARC-Zeichen: steigender Bogen + Pfeilspitze (Wachstum / Kurve)."""
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=col, width=w)
    a = math.radians(340); ex, ey = cx + math.cos(a) * r, cy + math.sin(a) * r
    s = w * 1.9
    d.polygon([(ex + s * 0.9, ey - s * 0.9), (ex - s * 0.55, ey - s * 0.95), (ex + s * 0.35, ey + s * 0.75)], fill=col)

# ---------------- Profilbild ----------------
S = 1600
pf = grad(S, S, (24, 56, 50), BG2, radial=True, cx=0.5, cy=0.42)
d = ImageDraw.Draw(pf)
d.ellipse([90, 90, S - 90, S - 90], outline=GOLD_D, width=14)
d.ellipse([130, 130, S - 130, S - 130], outline=(40, 70, 62), width=4)
arc_mark(d, S // 2, 860, 430, 46)
gold_text(pf, (S // 2, 900), "ARC", ImageFont.truetype(BLACK, 430))
pf = pf.resize((800, 800), Image.LANCZOS); pf.save("ARC_profilbild_800.png")
circ = Image.new("L", (800, 800), 0); ImageDraw.Draw(circ).ellipse([0, 0, 799, 799], fill=255)
prev = Image.new("RGB", (800, 800), (15, 15, 15)); prev.paste(pf, (0, 0), circ); prev.resize((176, 176), Image.LANCZOS).save("_vorschau_profil_klein.png")

# ---------------- Banner ----------------
BW, BH = 2560, 1440
bn = grad(BW, BH, (18, 42, 38), BG2)
d = ImageDraw.Draw(bn, "RGBA")
r = random.Random(7)
# feines Raster + aufsteigende Goldkurve (Chart) quer durchs Bild
for x in range(0, BW, 80): d.line([(x, 0), (x, BH)], fill=(255, 255, 255, 8))
for y in range(0, BH, 80): d.line([(0, y), (BW, y)], fill=(255, 255, 255, 8))
pts, y = [], 1060
for x in range(-40, BW + 80, 70):
    y += r.uniform(-60, 32) - 6; y = max(560, min(1150, y)); pts.append((x, y))
d.line(pts, fill=GOLD + (90,), width=8, joint="curve")
# Skyline: Finanzviertel + Rechenzentrum/Chip-Tuerme (Geld + Technologie), gezeichnet
base = 1180; x = -20
while x < BW:
    w = r.randint(70, 170); h = r.randint(160, 520)
    if 700 < x < 1860: h = int(h * 0.55)          # Mitte niedriger, damit die Schrift frei steht
    col = (28, 54, 50, 255) if r.random() < 0.6 else (34, 64, 58, 255)
    d.rectangle([x, base - h, x + w, base], fill=col)
    for wy in range(base - h + 18, base - 12, 26):
        for wx in range(x + 10, x + w - 12, 22):
            if r.random() < 0.35: d.rectangle([wx, wy, wx + 9, wy + 12], fill=(255, 214, 120, 150))
    if r.random() < 0.25: d.polygon([(x, base - h), (x + w / 2, base - h - 60), (x + w, base - h)], fill=col)
    x += w + r.randint(6, 20)
d.rectangle([0, base, BW, BH], fill=(8, 18, 18, 255))
# Chip-Symbol (KI) und Muenze (Geld) links/rechts ausserhalb der Safe-Area
def chip(cx, cy, s):
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], int(s * 0.18), fill=(30, 60, 56, 255), outline=GOLD + (200,), width=6)
    d.rounded_rectangle([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55], int(s * 0.1), outline=GOLD + (200,), width=5)
    for k in range(-3, 4):
        o = k * s * 0.26
        for (a, b2, c, e) in ((cx + o, cy - s, cx + o, cy - s - 40), (cx + o, cy + s, cx + o, cy + s + 40), (cx - s, cy + o, cx - s - 40, cy + o), (cx + s, cy + o, cx + s + 40, cy + o)):
            d.line([(a, b2), (c, e)], fill=GOLD + (200,), width=6)
    ImageDraw.Draw(bn).text((cx, cy), "AI", font=ImageFont.truetype(BLACK, int(s * 0.55)), fill=GOLD, anchor="mm")
def coin(cx, cy, s):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=GOLD_D + (255,), outline=GOLD_L + (255,), width=8)
    d.ellipse([cx - s * 0.78, cy - s * 0.78, cx + s * 0.78, cy + s * 0.78], outline=GOLD_L + (220,), width=5)
    ImageDraw.Draw(bn).text((cx, cy + 4), "$", font=ImageFont.truetype(BLACK, int(s * 1.1)), fill=GOLD_L, anchor="mm")
chip(330, 700, 140); coin(2230, 690, 140)
# Safe-Area (Mitte 1546x423): Logo + Claim + Rhythmus
cx, cy = BW // 2, BH // 2
arc_mark(ImageDraw.Draw(bn), cx - 560, cy + 40, 125, 19)
gold_text(bn, (cx - 560, cy + 50), "ARC", ImageFont.truetype(BLACK, 135))
d2 = ImageDraw.Draw(bn); tx = cx - 330
d2.text((tx, cy - 70), "Money. Power. Technology.", font=ImageFont.truetype(BLACK, 72), fill=WHITE, anchor="lm")
d2.text((tx + 2, cy + 18), "The stories behind how the world really works.", font=ImageFont.truetype(SANS, 44), fill=(190, 206, 198), anchor="lm")
d2.rounded_rectangle([tx, cy + 82, tx + 560, cy + 148], 33, fill=GOLD)
d2.text((tx + 280, cy + 116), "NEW VIDEO EVERY THURSDAY", font=ImageFont.truetype(BOLD, 32), fill=(20, 18, 10), anchor="mm")
bn.save("ARC_banner_2560x1440.png")
# Vorschauen: Handy (Safe-Area) und Desktop-Streifen
bn.crop(((BW - 1546) // 2, (BH - 423) // 2, (BW + 1546) // 2, (BH + 423) // 2)).save("_vorschau_banner_handy.png")
bn.crop((0, (BH - 423) // 2, BW, (BH + 423) // 2)).resize((1280, 212), Image.LANCZOS).save("_vorschau_banner_desktop.png")
print("ok")
