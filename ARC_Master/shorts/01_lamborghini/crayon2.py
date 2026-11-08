"""ARC v5 – Crayon-Spezifikation, vermessen am 03.11.2026:
- gezeichneter Ort, UNSCHARF (Tiefenschaerfe), Figur scharf davor
- Halbnah-Einstellungen: Kopf + Schultern gross, unten angeschnitten
- Kopf = Kreis, flache Haut, Schatten als SEITLICHE Mondsichel, dicke zittrige Kontur
- Arme = duenne schwarze Striche mit kleinen Haenden
- Augen: kleine schwarze Ovale / geschlossene Boegen (^^), offener Mund weiss
- gesprochener Text: weisse Handschrift mit dunkler Kontur ueber dem Sprecher + kleiner Sprech-Strich
- Erklaer-Grafiken: hellgrauer Grund, Objekt gezeichnet, Beschriftung in Handschrift, orange Pointe"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from crayon_kit import S, sh, shape, stroke, ellipse_pts, W, H, SS, INK, ENZO, FERRUCCIO, done
import places

HAND = "C:/Windows/Fonts/Inkfree.ttf"
GREY = (222, 222, 222)
ORANGE = (236, 150, 40)

def blur_bg(img, r=9):
    return img.filter(ImageFilter.GaussianBlur(r * SS))

def crescent_shadow(img, cx, cy, R, side, color):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse(S(cx - R * 0.97, cy - R * 0.95, cx + R * 0.97, cy + R * 0.95), fill=255)
    cut = Image.new("L", img.size, 0)
    o = R * 0.28 * side
    ImageDraw.Draw(cut).ellipse(S(cx - R * 1.02 - o, cy - R * 1.1, cx + R * 1.02 - o, cy + R * 0.98), fill=255)
    m = ImageChops.subtract(m, cut).filter(ImageFilter.GaussianBlur(2 * SS))
    img.paste(Image.new("RGB", img.size, color), (0, 0), m)

def bust(img, cx, hy, R, p, face=1, eyes="open", mouth="smile", brow=0.0, arm=None, seed=1, holds=None):
    """Halbnah-Figur: Kopfmitte (cx,hy), Kopfradius R. Koerper laeuft unten aus dem Bild."""
    d = ImageDraw.Draw(img, "RGBA")
    top = p["top"]
    # Koerper (unten offen)
    bw = R * 1.45 * p["big"]
    body = ellipse_pts(cx, hy + R * 1.55, bw, R * 0.75, 50, 180, 360) + [(cx + bw, H + 40), (cx - bw, H + 40)]
    shape(d, body, top, seed + 1)
    if p["tie"]:
        shape(d, [(cx - R * 0.16, hy + R * 0.95), (cx + R * 0.16, hy + R * 0.95), (cx, hy + R * 1.3)], (240, 238, 232), seed + 2, lw=5)
        shape(d, [(cx - R * 0.07, hy + R * 1.0), (cx + R * 0.07, hy + R * 1.0), (cx + R * 0.12, hy + R * 2.2), (cx, hy + R * 2.45), (cx - R * 0.12, hy + R * 2.2)], p["tie"], seed + 3, lw=5)
    else:
        shape(d, [(cx - R * 0.3, hy + R * 0.92), (cx, hy + R * 1.35), (cx + R * 0.3, hy + R * 0.92)], (240, 236, 226), seed + 2, lw=5)
    if p["braces"]:
        for sx in (-1, 1):
            stroke(d, [(cx + sx * bw * 0.45, hy + R * 1.0), (cx + sx * bw * 0.42, H)], lw=12, color=p["braces"])
    # Arm(e) als duenne Striche mit Hand
    if arm:
        for pts in arm:
            stroke(d, pts, lw=9)
            hx, hy2 = pts[-1]
            shape(d, ellipse_pts(hx, hy2, R * 0.11, R * 0.1, 20), p["skin"], seed + 9, lw=5)
    if holds:
        holds(d)
    # Kopf
    shape(d, ellipse_pts(cx, hy, R, R), p["skin"], seed + 4)
    crescent_shadow(img, cx, hy, R, -face, sh(p["skin"], 0.87))
    d = ImageDraw.Draw(img, "RGBA")
    # Haare
    if p["hairstyle"] == "enzo":
        hair = ellipse_pts(cx - face * R * 0.06, hy - R * 0.42, R * 1.0, R * 0.66, 60, 180, 360)
        shape(d, hair + [(cx + R * 0.95, hy - R * 0.2), (cx + R * 0.5, hy - R * 0.38), (cx - R * 0.5, hy - R * 0.38), (cx - R * 0.95, hy - R * 0.2)], p["hair"], seed + 5)
        for k in range(3):
            stroke(d, ellipse_pts(cx - face * R * 0.1, hy - R * (0.66 - k * 0.12), R * 0.6, R * 0.16, 16, 205, 330), lw=4, color=(198, 198, 206))
    else:
        hair = ellipse_pts(cx, hy - R * 0.35, R * 1.0, R * 0.68, 60, 180, 360)
        tufts = [(cx + R * 0.98, hy - R * 0.2), (cx + R * 0.62, hy - R * 0.42), (cx + R * 0.2, hy - R * 0.34), (cx - R * 0.25, hy - R * 0.46), (cx - R * 0.98, hy - R * 0.18)]
        shape(d, hair + tufts, p["hair"], seed + 5)
        for k in range(3):
            stroke(d, [(cx - R * 0.55 + k * R * 0.3, hy - R * 0.85), (cx - R * 0.38 + k * R * 0.3, hy - R * 0.62)], lw=5, color=p["hair_hi"])
    ex, ey = cx + face * R * 0.22, hy + R * 0.02
    # Augen
    if p["glasses"]:
        for k in (-1, 1):
            gx = ex + k * R * 0.3
            shape(d, [(gx - R * 0.25, ey - R * 0.14), (gx + R * 0.25, ey - R * 0.14), (gx + R * 0.22, ey + R * 0.12), (gx - R * 0.22, ey + R * 0.12)], (32, 34, 40), seed + 6 + k, lw=6)
            stroke(d, [(gx - R * 0.15, ey - R * 0.07), (gx - R * 0.03, ey - R * 0.09)], lw=4, color=(160, 168, 180))
        stroke(d, [(ex - R * 0.06, ey - R * 0.08), (ex + R * 0.06, ey - R * 0.08)], lw=6)
    else:
        for k in (-1, 1):
            gx = ex + k * R * 0.28
            if eyes == "happy":
                stroke(d, ellipse_pts(gx, ey + R * 0.03, R * 0.09, R * 0.07, 14, 200, 340), lw=7)
            else:
                d.ellipse(S(gx - R * 0.055, ey - R * 0.09, gx + R * 0.055, ey + R * 0.09), fill=INK)
    # Brauen (brow > 0 = boese, < 0 = ueberheblich/besorgt)
    bc = (186, 186, 194) if p["hair"][0] > 200 else p["hair"]
    for k in (-1, 1):
        gx = ex + k * R * 0.28
        stroke(d, [(gx - k * R * 0.08, ey - R * (0.24 - brow)), (gx + k * R * 0.13, ey - R * (0.28 + brow * 0.5))], lw=9, color=bc)
    # Nase (nur Enzo, Karikatur-Merkmal)
    if p["nose"]:
        shape(d, [(ex + face * R * 0.0, ey + R * 0.0), (ex + face * R * 0.22, ey + R * 0.3), (ex - face * R * 0.03, ey + R * 0.33)], sh(p["skin"], 0.88), seed + 8, lw=5)
    my = ey + R * (0.46 if p["nose"] else 0.36)
    if p["mustache"]:
        shape(d, ellipse_pts(ex, my - R * 0.03, R * 0.27, R * 0.1, 30, 180, 360) + [(ex + R * 0.27, my + R * 0.03), (ex - R * 0.27, my + R * 0.03)], p["hair"], seed + 9, lw=5)
        my += R * 0.1
    if mouth == "smile":
        stroke(d, ellipse_pts(ex, my - R * 0.06, R * 0.14, R * 0.09, 16, 20, 160), lw=7)
    elif mouth == "open":     # offener Mund, weiss gefuellt (Crayon)
        shape(d, ellipse_pts(ex, my - R * 0.02, R * 0.16, R * 0.11, 30, 0, 180) + [(ex - R * 0.16, my - R * 0.02)], (255, 255, 255), seed + 10, lw=6)
    elif mouth == "smirk":
        stroke(d, ellipse_pts(ex + face * R * 0.06, my - R * 0.06, R * 0.13, R * 0.07, 14, 20, 120), lw=7)
    elif mouth == "frown":
        stroke(d, ellipse_pts(ex, my + R * 0.07, R * 0.12, R * 0.06, 14, 200, 340), lw=7)
    elif mouth == "talk":
        shape(d, ellipse_pts(ex, my + R * 0.02, R * 0.1, R * 0.09, 24), (110, 40, 44), seed + 11, lw=5)

def spoken(img, text, cx, y, size=64, tick_to=None):
    """Weisse Handschrift mit dunkler Kontur ueber dem Sprecher + kleiner Sprech-Strich (Crayon)."""
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(HAND, size * SS)
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f) / SS
        d.text(S(cx - tw / 2, y + i * size * 1.15), ln, font=f, fill=(255, 255, 255), stroke_width=5 * SS, stroke_fill=INK)
    if tick_to:
        (x0, y0), (x1, y1) = tick_to
        d.line(S(x0, y0, x1, y1), fill=INK, width=12 * SS); d.line(S(x0, y0, x1, y1), fill=(255, 255, 255), width=6 * SS)

def hand_text(img, text, cx, y, size, color=INK):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(HAND, size * SS)
    tw = d.textlength(text, font=f) / SS
    d.text(S(cx - tw / 2, y), text, font=f, fill=color, stroke_width=2 * SS, stroke_fill=color)

def clutch_drawing(d, cx, cy, r, seed):
    shape(d, ellipse_pts(cx, cy, r, r), (170, 172, 182), seed)
    shape(d, ellipse_pts(cx, cy, r * 0.68, r * 0.68), (140, 142, 152), seed + 1, lw=5)
    for k in range(6):
        a = k * math.pi / 3
        px, py = cx + math.cos(a) * r * 0.45, cy + math.sin(a) * r * 0.45
        shape(d, [(px - r * 0.1, py - r * 0.06), (px + r * 0.1, py - r * 0.06), (px + r * 0.1, py + r * 0.06), (px - r * 0.1, py + r * 0.06)], (224, 186, 96), seed + 2 + k, lw=4)
    shape(d, ellipse_pts(cx, cy, r * 0.17, r * 0.17), (60, 60, 66), seed + 9, lw=4)

def price_tag(d, cx, cy, text, color, seed, size=70):
    f = ImageFont.truetype(HAND, size * SS)
    tw = d.textlength(text, font=f) / SS
    shape(d, [(cx - tw / 2 - 40, cy - 55), (cx + tw / 2 + 30, cy - 55), (cx + tw / 2 + 70, cy), (cx + tw / 2 + 30, cy + 55), (cx - tw / 2 - 40, cy + 55)], (252, 248, 236), seed)
    d.text(S(cx - tw / 2 - 10, cy - size * 0.62), text, font=f, fill=color)

# ---------------- 3 Testbilder in Crayon-Einstellungen ----------------
def shot_ferruccio():
    bg, hz = places.workshop_1948()
    dd = ImageDraw.Draw(bg, "RGBA")
    places.cartoon_tractor(dd, 380, hz + 150, 680)
    img = blur_bg(bg, 8)
    bust(img, 430, 1080, 300, FERRUCCIO, face=1, eyes="happy", mouth="smile", brow=-0.02, seed=3)
    d = ImageDraw.Draw(img)
    stroke(d, [(845, 1530), (900, 1400), (930, 1270)], lw=10)          # Arm zeigt stolz auf den Traktor
    shape(d, ellipse_pts(935, 1255, 32, 30, 20), FERRUCCIO["skin"], 77, lw=5)
    spoken(img, "Italy, 1948", 540, 130, 76)
    return done(img)

def shot_enzo():
    bg, hz = places.ferrari_office()
    places.desk(bg, 60, 1020, 1520, 2000)
    img = blur_bg(bg, 8)
    bust(img, 560, 1060, 320, ENZO, face=-1, mouth="talk", brow=-0.04, seed=7)
    places.desk(img, -40, 1120, 1560, 2050)
    spoken(img, "You may be able to\ndrive a tractor…\nbut you'll never\nhandle a Ferrari.", 540, 170, 72, tick_to=((760, 650), (800, 700)))
    return done(img)

def shot_price():
    img = Image.new("RGB", (W * SS, H * SS), GREY)
    d = ImageDraw.Draw(img, "RGBA")
    hand_text(img, "The same clutch", 540, 210, 96)
    clutch_drawing(d, 300, 760, 190, 10); clutch_drawing(d, 780, 760, 190, 20)
    hand_text(img, "tractor", 300, 990, 64); hand_text(img, "Ferrari", 780, 990, 64)
    price_tag(d, 300, 1210, "10 lire", (40, 110, 60), 30)
    price_tag(d, 780, 1210, "1,000 lire", (196, 40, 40), 31)
    hand_text(img, "100x the price!", 540, 1480, 92, ORANGE)
    for k, (x0, y0, x1, y1) in enumerate([(150, 1500, 100, 1460), (140, 1580, 80, 1580), (930, 1500, 980, 1460), (940, 1580, 1000, 1580)]):
        stroke(d, [(x0, y0), (x1, y1)], lw=7)
    return done(img)

if __name__ == "__main__":
    fr = [shot_ferruccio(), shot_enzo(), shot_price()]
    for i, f in enumerate(fr):
        f.save(f"CR5_test_{i + 1}.png")
    tw, th = 450, 800
    sheet = Image.new("RGB", (3 * tw + 40, th + 20), (0, 0, 0))
    for i, f in enumerate(fr):
        sheet.paste(f.resize((tw, th)), (10 + i * (tw + 10), 10))
    sheet.save("STIL_CRAYON_V5.png"); print("ok")
