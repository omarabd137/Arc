"""Thumbnail #02 v7 im Video-Cartoon-Stil: der Video-Roboter (weiss, Visier, rote Augen) ragt riesig ueber der Stadt
und haelt unsere Cartoon-Figuren an Faeden wie Marionetten. Tusche-Konturen, flache Farben. Text: THE REAL DANGER."""
import os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
from ai_kit import *

c = canvas((0, 0, 0, 255)); p = Pen(c); r = random.Random(8)
BODY = (238, 240, 246); SHADE = (196, 202, 216); DARKM = (64, 70, 88); VIS = (20, 22, 34)
# Himmel + Stadt (flach, Cartoon)
p.vgrad(0, 0, W, H, (28, 24, 70), (120, 34, 60))
p.ell(1600, 170, 70, 70, (250, 236, 200), 4)
x = -20
while x < W + 20:
    bw = r.randint(80, 160); bh = r.randint(160, 380); col = r.choice([(40, 36, 80), (52, 44, 92), (34, 30, 70)])
    p.rect(x, H - bh, x + bw, H + 10, col, 4)
    for wy in range(int(H - bh + 20), H - 20, 34):
        for wx in range(int(x + 14), int(x + bw - 20), 28):
            if r.random() < 0.4: p.rect(wx, wy, wx + 12, wy + 16, (255, 214, 120), 2)
    x += bw + r.randint(4, 14)
# Riesiger Roboter (Oberkoerper) hinter der Stadtmitte
cx = 960
p.rect(cx - 330, 560, cx + 330, 1200, BODY, 7, r=120)                       # Torso
p.rect(cx - 250, 640, cx + 250, 860, SHADE, 5, r=50); p.ell(cx, 750, 46, 46, RED, 5)
p.rect(cx - 70, 470, cx + 70, 580, DARKM, 6)                               # Hals
p.rect(cx - 260, 130, cx + 260, 520, BODY, 8, r=130)                        # Kopf
p.ell(cx - 270, 320, 34, 70, DARKM, 6); p.ell(cx + 270, 320, 34, 70, DARKM, 6)
p.rect(cx - 205, 215, cx + 205, 420, VIS, 7, r=90)                          # Visier
for sx in (-1, 1):                                                          # wuetende rote Augen
    ex = cx + sx * 95; o = ex + sx * 60; i_ = ex - sx * 55
    p.poly([(o, 270), (i_, 315), (i_ + sx * 6, 345), (o - sx * 8, 330)], (255, 46, 56), 4, INK)
p.glow(cx, 315, 150, RED, 120)
p.arc(cx, 380, 70, 26, 20, 160, 6, (255, 46, 56))                          # boeses Laecheln
# Arme + Haende (palm down), Faeden zu Marionetten
targets = []
for sx in (-1, 1):
    sh = (cx + sx * 300, 640); el = (cx + sx * 560, 560); hd = (cx + sx * 700, 470)
    p.line([sh, el, hd], 120, INK); p.line([sh, el, hd], 104, BODY)
    p.ell(el[0], el[1], 58, 58, SHADE, 6)
    hx, hy = hd; p.ell(hx, hy, 105, 72, BODY, 7)
    for k in range(4):
        fx = hx - 75 + k * 50; fy = hy + 120 + (k in (1, 2)) * 24
        p.line([(fx, hy + 30), (fx, fy)], 44, INK); p.line([(fx, hy + 30), (fx, fy)], 32, BODY); p.ell(fx, fy, 16, 16, BODY, 0)
        p.ell(fx, fy + 6, 10, 6, DARKM, 0)
        targets.append((fx, fy + 18, sx, k))
# Marionetten: unsere Cartoon-Figuren an Faeden
CAST = [LEO, PEOPLE[0], PEOPLE[2], PEOPLE[1], PEOPLE[3], PEOPLE[4], KID, LEO]
for i, (fx, fy, sx, k) in enumerate(targets):
    px = fx - 40 + k * 62 + (30 if sx < 0 else 0); base = 1010 + (k % 2) * 45
    fi = figure(c, px, base, 40, CAST[i], -sx, "o" if k % 2 else "worried", 0.5, ("up", "up"), "stand", 0.0, "wide")
    hx2, hy2 = fi["hands"][0]; hx3, hy3 = fi["hands"][1]; hx_, hy_ = fi["head"][0], fi["head"][1] - fi["head"][2]
    for tx, ty in ((hx2, hy2), (hx3, hy3), (hx_, hy_)): p.line([(fx, fy), (tx, ty)], 2.6, (240, 240, 255))
im = c.convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA"); d = ImageDraw.Draw(im)
f = ImageFont.truetype(BOLD, 150)
d.text((966, 100), "THE REAL DANGER", font=f, fill=(0, 0, 0), anchor="mm")
d.text((960, 92), "THE REAL", font=f, fill=(255, 255, 255), anchor="rm", stroke_width=14, stroke_fill=(0, 0, 0)) if False else None
w1 = d.textlength("THE REAL ", font=f); w2 = d.textlength("DANGER", font=f); x0 = 960 - (w1 + w2) / 2
d.text((x0, 92), "THE REAL ", font=f, fill=(255, 255, 255), anchor="lm", stroke_width=14, stroke_fill=(0, 0, 0))
d.text((x0 + w1, 92), "DANGER", font=f, fill=(255, 60, 60), anchor="lm", stroke_width=14, stroke_fill=(0, 0, 0))
im = im.convert("RGB"); im.save("THUMB_v7_1920.png"); im.resize((1280, 720), Image.LANCZOS).save("THUMB_v7.jpg", quality=93); print("ok")
