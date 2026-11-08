"""Thumbnail #02 v3 (eigenes Konzept, Cartoon): Mensch zieht mit aller Kraft am Stecker - die riesige KI grinst und laesst nicht los.
Spruch: IT REFUSED TO DIE."""
import os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
from ai_kit import *

c = canvas((0, 0, 0, 255)); p = Pen(c); r = random.Random(3)
# --- Raum: dunkel, rotes Notlicht
p.vgrad(0, 0, W, H, (34, 6, 12), (10, 4, 8))
for k, x in enumerate(range(-60, W + 60, 210)):
    p.rect(x, 60, x + 170, 1080, (26, 22, 34), 3, r=8)
    for y in range(90, 1060, 36):
        p.rect(x + 14, y, x + 156, y + 24, (38, 34, 48), 1.6, r=4)
        if r.random() < 0.5: p.ell(x + 136, y + 12, 4, 4, RED, 0)
p.glow(1280, 420, 760, RED, 120); p.glow(1280, 380, 420, (255, 90, 70), 110)
p.rect(0, 930, W, H, (20, 14, 20), 0)
# --- riesige KI (Bildschirmkopf) rechts, boeses Grinsen
cx, cy, s = 1330, 470, 2.25; w, h = 300 * s, 230 * s
p.rect(cx - w / 2 - 30, cy - h / 2 - 30, cx + w / 2 + 30, cy + h / 2 + 30, (206, 210, 222), 8, r=100)
p.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, (12, 14, 22), 6, r=80)
p.glow(cx, cy - 40, 300, RED, 90)
for sx in (-1, 1):                                       # schraege, wuetende Augen
    ex = cx + sx * 150; ey = cy - 70
    p.poly([(ex - 80, ey - 30 + (sx * 30)), (ex + 80, ey - 30 + (sx * -30)), (ex + 70, ey + 40), (ex - 70, ey + 40)], (255, 50, 50), 0)
    p.ell(ex, ey + 10, 18, 18, (255, 220, 200), 0)
p.glow(cx, cy - 60, 200, (255, 60, 60), 120)
# Grinsen mit Zaehnen
mx0, mx1, my = cx - 220, cx + 220, cy + 120
p.poly([(mx0, my - 20), (mx1, my - 20), (cx + 160, my + 80), (cx - 160, my + 80)], (255, 50, 50), 0)
for k in range(9):
    tx = mx0 + 30 + k * 47; p.poly([(tx, my - 18), (tx + 40, my - 18), (tx + 20, my + 22)], (255, 240, 236), 2, (12, 14, 22))
# Hals + Kabel aus dem Kopf
p.rect(cx - 70, cy + h / 2 + 30, cx + 70, cy + h / 2 + 110, (170, 176, 190), 5)
fi = figure(c, 300, 1120, 112, SCI, 1, "o", 0.9, ("hold", "hold"), "stand", 0.0, "wide")
hx, hy = fi["hands"][-1]
cable = [(cx - 40, cy + h / 2 + 80), (1060, 900), (760, hy + 40), (hx + 90, hy)]
p.line(cable, 46, INK); p.line(cable, 34, (40, 42, 52))
p.rect(hx - 40, hy - 44, hx + 90, hy + 44, (60, 64, 76), 5, r=14); p.rect(hx - 70, hy - 26, hx - 40, hy - 14, (200, 200, 210), 3); p.rect(hx - 70, hy + 14, hx - 40, hy + 26, (200, 200, 210), 3)
for k in range(12):
    a_ = r.uniform(-3.0, -0.3); L = r.uniform(50, 130); p.line([(hx + 90, hy), (hx + 90 + L * math.cos(a_), hy + L * math.sin(a_))], 6, (255, 230, 120))
p.glow(hx + 90, hy, 100, (255, 220, 120), 200)
for k in range(3): p.ell(hx - 20 + k * 20, hy - 90 - k * 10, 6, 6, (255, 230, 120), 0)
for dx, dy in ((420, 320), (444, 290)): p.ell(dx, dy, 10, 16, (150, 210, 255), 2)      # Schweisstropfen
im = c.convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
d = ImageDraw.Draw(im)
def big(s, x, y, size, col, anchor="lm"):
    d.text((x + 8, y + 10), s, font=ImageFont.truetype(BOLD, size), fill=(0, 0, 0), anchor=anchor)
    d.text((x, y), s, font=ImageFont.truetype(BOLD, size), fill=col, anchor=anchor, stroke_width=16, stroke_fill=(0, 0, 0))
big("IT REFUSED", 50, 110, 170, (255, 255, 255)); big("TO DIE", 50, 285, 190, (255, 60, 60))
im = im.convert("RGB"); im.save("THUMB_v3_1920.png"); im.resize((1280, 720), Image.LANCZOS).save("THUMB_v3.jpg", quality=93)
im.resize((360, 202), Image.LANCZOS).save("THUMB_v3_small.png"); print("ok")
