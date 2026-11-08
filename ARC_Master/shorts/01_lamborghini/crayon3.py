"""ARC v6 – exakt nach Crayon (NVIDIA-Video vermessen):
glatte gleichmaessige Linien, eifoermiger Oberkoerper, Strich-Arme + Strich-Beine, winzige Punkt-Augen,
kleiner Mund, Kopf mit seitlicher Schattenhaelfte, detaillierte SCHARFE Hintergruende, gelbe Notizzettel."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from crayon_kit import S, sh, shape, stroke, ellipse_pts, W, H, SS, INK, ENZO, FERRUCCIO, done
import places
from crayon2 import spoken, hand_text, clutch_drawing, price_tag, crescent_shadow, GREY, ORANGE, HAND

LIMB = 7   # Strich-Arme/-Beine

def figure(img, cx, base, R, p, face=1, mouth="line", brow=0.0, arms=("down", "down"), seed=1, seated=False):
    """Crayon-Figur. base = Fussboden-Linie, R = Kopfradius."""
    d = ImageDraw.Draw(img, "RGBA")
    leg = R * 1.25
    tor_h, tor_w = R * 1.35, R * 1.05 * p["big"]
    hip = base - leg
    tor_cy = hip - tor_h * 0.42
    head_cy = hip - tor_h - R * 0.78
    if not seated:
        d.ellipse(S(cx - R * 0.9, base - 10, cx + R * 0.9, base + 10), fill=(0, 0, 0, 55))
        for sx in (-1, 1):                         # Strich-Beine mit kurzem Fuss
            x = cx + sx * tor_w * 0.28
            stroke(d, [(x, hip - 10), (x + sx * 4, base)], lw=LIMB)
            stroke(d, [(x + sx * 4, base), (x + sx * 4 + face * 22, base)], lw=LIMB)
    # Arme (hinter dem Koerper beginnen)
    def arm(sx, kind):
        x0, y0 = cx + sx * tor_w * 0.55, tor_cy - tor_h * 0.18
        if kind == "down":
            pts = [(x0, y0), (x0 + sx * R * 0.25, y0 + R * 0.7), (x0 + sx * R * 0.2, y0 + R * 1.2)]
        elif kind == "hip":
            pts = [(x0, y0), (x0 + sx * R * 0.55, y0 + R * 0.45), (x0 + sx * R * 0.15, y0 + R * 0.85)]
        elif kind == "point":
            pts = [(x0, y0), (x0 + sx * R * 0.8, y0 - R * 0.2), (x0 + sx * R * 1.4, y0 - R * 0.35)]
        elif kind == "rest":
            pts = [(x0, y0), (x0 + sx * R * 0.6, y0 + R * 0.25), (x0 + sx * R * 1.15, y0 + R * 0.1)]
        elif kind == "desk":
            pts = [(x0, y0), (x0 + sx * R * 0.3, y0 + R * 0.6), (x0 - sx * R * 0.25, y0 + R * 0.75)]
        stroke(d, pts, lw=LIMB)
        return pts[-1]
    hands = [arm(-1, arms[0]), arm(1, arms[1])]
    # eifoermiger Oberkoerper
    shape(d, ellipse_pts(cx, tor_cy, tor_w * 0.55, tor_h * 0.55, 80), p["top"], seed + 1)
    d.chord(S(cx - tor_w * 0.55, tor_cy - tor_h * 0.55, cx + tor_w * 0.55, tor_cy + tor_h * 0.55),
            90 if face == 1 else 270, 270 if face == 1 else 450, fill=sh(p["top"], 0.88) + (120,))
    top_y = tor_cy - tor_h * 0.55
    if p["tie"]:
        shape(d, [(cx - R * 0.22, top_y + 4), (cx + R * 0.22, top_y + 4), (cx, top_y + R * 0.45)], (244, 242, 236), seed + 2, lw=4)
        shape(d, [(cx - R * 0.07, top_y + R * 0.1), (cx + R * 0.07, top_y + R * 0.1), (cx + R * 0.1, top_y + R * 0.9), (cx, top_y + R * 1.05), (cx - R * 0.1, top_y + R * 0.9)], p["tie"], seed + 3, lw=4)
    else:
        shape(d, [(cx - R * 0.28, top_y + 6), (cx, top_y + R * 0.42), (cx + R * 0.28, top_y + 6)], (244, 240, 230), seed + 2, lw=4)
        for k in range(3):
            d.ellipse(S(cx - 5, top_y + R * (0.55 + k * 0.28) - 5, cx + 5, top_y + R * (0.55 + k * 0.28) + 5), fill=INK)
    if p["braces"]:
        for sx in (-1, 1):
            stroke(d, [(cx + sx * tor_w * 0.22, top_y + 10), (cx + sx * tor_w * 0.24, tor_cy + tor_h * 0.5)], lw=6, color=p["braces"])
    # Haende als kleine Kreise
    for hx, hy in hands:
        shape(d, ellipse_pts(hx, hy, R * 0.1, R * 0.1, 20), p["skin"], seed + 4, lw=4)
    # Kopf + seitlicher Schatten
    shape(d, ellipse_pts(head_cy and cx, head_cy, R, R), p["skin"], seed + 5)
    crescent_shadow(img, cx, head_cy, R, -face, sh(p["skin"], 0.86))
    d = ImageDraw.Draw(img, "RGBA")
    # Haare
    if p["hairstyle"] == "enzo":
        hair = ellipse_pts(cx - face * R * 0.05, head_cy - R * 0.45, R * 1.0, R * 0.62, 60, 180, 360)
        shape(d, hair + [(cx + R * 0.97, head_cy - R * 0.25), (cx + R * 0.45, head_cy - R * 0.45), (cx - R * 0.45, head_cy - R * 0.45), (cx - R * 0.97, head_cy - R * 0.25)], p["hair"], seed + 6)
        for k in range(3):
            stroke(d, ellipse_pts(cx - face * R * 0.1, head_cy - R * (0.7 - k * 0.12), R * 0.55, R * 0.14, 16, 205, 330), lw=3, color=(200, 200, 208))
    else:
        hair = ellipse_pts(cx, head_cy - R * 0.38, R * 1.0, R * 0.66, 60, 180, 360)
        shape(d, hair + [(cx + R * 0.98, head_cy - R * 0.22), (cx + R * 0.4, head_cy - R * 0.42), (cx - R * 0.3, head_cy - R * 0.5), (cx - R * 0.98, head_cy - R * 0.2)], p["hair"], seed + 6)
        stroke(d, ellipse_pts(cx - R * 0.2, head_cy - R * 0.72, R * 0.42, R * 0.15, 16, 200, 320), lw=4, color=p["hair_hi"])
    ex, ey = cx + face * R * 0.24, head_cy + R * 0.05
    if p["glasses"]:
        for k in (-1, 1):
            gx = ex + k * R * 0.3
            shape(d, [(gx - R * 0.24, ey - R * 0.13), (gx + R * 0.24, ey - R * 0.13), (gx + R * 0.21, ey + R * 0.11), (gx - R * 0.21, ey + R * 0.11)], (34, 36, 42), seed + 7 + k, lw=4)
        stroke(d, [(ex - R * 0.06, ey - R * 0.07), (ex + R * 0.06, ey - R * 0.07)], lw=4)
    else:
        for k in (-1, 1):                          # winzige Punkt-Augen
            gx = ex + k * R * 0.26
            d.ellipse(S(gx - R * 0.045, ey - R * 0.06, gx + R * 0.045, ey + R * 0.06), fill=INK)
    bc = (190, 190, 198) if p["hair"][0] > 200 else p["hair"]
    for k in (-1, 1):
        gx = ex + k * R * 0.26
        stroke(d, [(gx - k * R * 0.07, ey - R * (0.22 - brow)), (gx + k * R * 0.1, ey - R * (0.25 + brow * 0.5))], lw=5, color=bc)
    if p["nose"]:
        stroke(d, [(ex + face * R * 0.02, ey + R * 0.05), (ex + face * R * 0.15, ey + R * 0.27), (ex - face * R * 0.02, ey + R * 0.29)], lw=4)
    my = ey + R * (0.42 if p["nose"] else 0.3)
    if p["mustache"]:
        shape(d, ellipse_pts(ex, my - R * 0.02, R * 0.22, R * 0.08, 24, 180, 360) + [(ex + R * 0.22, my + R * 0.02), (ex - R * 0.22, my + R * 0.02)], p["hair"], seed + 9, lw=3)
        my += R * 0.08
    if mouth == "line":
        stroke(d, [(ex - R * 0.07, my), (ex + R * 0.07, my)], lw=5)
    elif mouth == "smile":
        stroke(d, ellipse_pts(ex, my - R * 0.05, R * 0.1, R * 0.07, 14, 20, 160), lw=5)
    elif mouth == "smirk":
        stroke(d, ellipse_pts(ex + face * R * 0.05, my - R * 0.05, R * 0.1, R * 0.06, 12, 20, 120), lw=5)
    elif mouth == "frown":
        stroke(d, ellipse_pts(ex, my + R * 0.06, R * 0.09, R * 0.05, 12, 200, 340), lw=5)
    elif mouth == "talk":
        shape(d, ellipse_pts(ex, my + R * 0.02, R * 0.08, R * 0.07, 20), (110, 40, 44), seed + 10, lw=4)
    return head_cy

def sticky(img, cx, cy, lines, angle=-4, w=420):
    """Gelber Notizzettel mit Handschrift (wie Crayons Namensschilder)."""
    f = ImageFont.truetype(HAND, 48 * SS)
    note = Image.new("RGBA", (w * SS, (60 + 56 * len(lines)) * SS), (0, 0, 0, 0))
    nd = ImageDraw.Draw(note)
    nd.rectangle([0, 0, note.width - 1, note.height - 1], fill=(250, 220, 110), outline=INK, width=4 * SS)
    for i, ln in enumerate(lines):
        tw = nd.textlength(ln, font=f)
        nd.text(((note.width - tw) / 2, (24 + i * 56) * SS), ln, font=f, fill=INK, stroke_width=1 * SS, stroke_fill=INK)
    note = note.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(note, (int(cx * SS - note.width / 2), int(cy * SS - note.height / 2)), note)

def shot_workshop():
    img, hz = places.workshop_1948()
    d = ImageDraw.Draw(img, "RGBA")
    places.cartoon_tractor(d, 430, hz + 260, 620)
    figure(img, 300, hz + 300, 150, FERRUCCIO, face=1, mouth="smile", arms=("hip", "rest"), seed=3)
    sticky(img, 640, 300, ["FERRUCCIO LAMBORGHINI", "Italy, 1948"], w=700)
    return done(img)

def shot_office():
    img, hz = places.ferrari_office()
    figure(img, 600, hz + 180, 165, ENZO, face=-1, mouth="talk", brow=-0.03, arms=("desk", "desk"), seed=7, seated=True)
    places.desk(img, 200, 1040, 1420, 1920)
    figure(img, 170, H + 60, 175, FERRUCCIO, face=1, mouth="frown", brow=0.07, arms=("down", "down"), seed=9)
    spoken(img, "You may be able to\ndrive a tractor…\nbut you'll never\nhandle a Ferrari.", 640, 160, 68, tick_to=((800, 700), (760, 760)))
    return done(img)

def shot_price():
    img = Image.new("RGB", (W * SS, H * SS), GREY)
    d = ImageDraw.Draw(img, "RGBA")
    hand_text(img, "The same clutch", 540, 230, 96)
    clutch_drawing(d, 300, 760, 190, 10); clutch_drawing(d, 780, 760, 190, 20)
    sticky(img, 300, 1050, ["TRACTOR"], angle=3, w=300)
    sticky(img, 780, 1050, ["FERRARI"], angle=-3, w=300)
    price_tag(d, 300, 1270, "10 lire", (40, 110, 60), 30)
    price_tag(d, 780, 1270, "1,000 lire", (196, 40, 40), 31)
    hand_text(img, "100x the price!", 540, 1520, 92, ORANGE)
    return done(img)

if __name__ == "__main__":
    fr = [shot_workshop(), shot_office(), shot_price()]
    for i, f in enumerate(fr):
        f.save(f"CR6_test_{i + 1}.png")
    tw, th = 450, 800
    sheet = Image.new("RGB", (3 * tw + 40, th + 20), (0, 0, 0))
    for i, f in enumerate(fr):
        sheet.paste(f.resize((tw, th)), (10 + i * (tw + 10), 10))
    sheet.save("STIL_CRAYON_V6.png"); print("ok")
