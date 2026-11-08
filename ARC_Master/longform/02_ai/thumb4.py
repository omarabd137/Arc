"""Thumbnail #02 v4: links niedlicher Vektor-Roboter, rechte Gesichtshaelfte platzt ab -> dunkles Inneres mit gluehendem Auge.
Rechts 3 Woerter. Dunkler Blau/Lila-Verlauf. Nichts sonst."""
import os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
from ai_kit import *
from PIL import ImageDraw as D

LINES = [("IT", (255, 255, 255)), ("ALREADY", (255, 255, 255)), ("HAPPENED.", (255, 214, 60))]
S = 2; Wd, Hd = 1920 * S, 1080 * S
im = Image.new("RGBA", (Wd, Hd)); d = D.Draw(im, "RGBA")
for y in range(Hd):                                        # Verlauf dunkelblau -> purpur
    k = y / Hd; d.line([(0, y), (Wd, y)], fill=mix((18, 16, 52), (58, 18, 70), k))
def P(*pts): return [(x * S, y * S) for x, y in pts]
def glow(x, y, r, col, a):
    lay = Image.new("RGBA", im.size); D.Draw(lay).ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=col + (a,))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(r * S * 0.45)))
glow(600, 560, 520, (90, 120, 255), 70)
INKC = (18, 16, 26); LW = 9 * S
cx, cy = 560, 590; hw, hh = 400, 360                       # Kopf
# Antenne + Ohren
d.line(P((cx, cy - hh), (cx, cy - hh - 110)), fill=INKC, width=LW + 6); d.line(P((cx, cy - hh), (cx, cy - hh - 110)), fill=(200, 206, 222), width=LW - 4)
d.ellipse([(cx - 34) * S, (cy - hh - 150) * S, (cx + 34) * S, (cy - hh - 82) * S], fill=(90, 210, 255), outline=INKC, width=LW)
for sx in (-1, 1):
    d.rounded_rectangle([(cx + sx * hw - 46) * S if sx < 0 else (cx + hw - 10) * S, (cy - 90) * S, (cx - hw + 10) * S if sx < 0 else (cx + hw + 46) * S, (cy + 90) * S], 22 * S, fill=(170, 178, 198), outline=INKC, width=LW)
# Kopf (weiss, rund)
d.rounded_rectangle([(cx - hw) * S, (cy - hh) * S, (cx + hw) * S, (cy + hh) * S], 150 * S, fill=(244, 246, 252), outline=INKC, width=LW)
d.rounded_rectangle([(cx - hw + 60) * S, (cy - hh + 70) * S, (cx + hw - 60) * S, (cy + hh - 70) * S], 110 * S, fill=(30, 40, 70), outline=INKC, width=LW)
# freundliche linke Haelfte: grosses Auge + Laecheln + Wange
ex, ey = cx - 150, cy - 40
glow(ex, ey, 90, (90, 210, 255), 160)
d.rounded_rectangle([(ex - 52) * S, (ey - 72) * S, (ex + 52) * S, (ey + 72) * S], 50 * S, fill=(110, 220, 255))
d.ellipse([(ex - 28) * S, (ey - 48) * S, (ex + 4) * S, (ey - 12) * S], fill=(255, 255, 255))
d.arc([(cx - 200) * S, (cy + 20) * S, (cx + 40) * S, (cy + 170) * S], 25, 155, fill=(110, 220, 255), width=14 * S)
d.ellipse([(cx - 300) * S, (cy + 60) * S, (cx - 230) * S, (cy + 110) * S], fill=(255, 140, 170, 120))
# Riss: rechte Haelfte platzt ab
crack = [(cx + 20, cy - hh - 10), (cx - 20, cy - 220), (cx + 30, cy - 130), (cx - 10, cy - 40), (cx + 40, cy + 40), (cx - 5, cy + 140), (cx + 35, cy + 230), (cx + 5, cy + hh + 10)]
dark = crack + [(cx + hw + 60, cy + hh + 10), (cx + hw + 60, cy - hh - 10)]
mask = Image.new("L", im.size, 0); D.Draw(mask).polygon(P(*dark), fill=255)
inner = Image.new("RGBA", im.size); di = D.Draw(inner, "RGBA")
di.rectangle([0, 0, Wd, Hd], fill=(14, 10, 20))
r = random.Random(4)
for k in range(14):                                         # Kabel / Schaltkreise im Inneren
    y = cy - hh + 40 + k * 52; di.line([(cx * S, y * S), ((cx + hw) * S, (y + r.randint(-30, 30)) * S)], fill=(60, 30, 50), width=6 * S)
head_mask = Image.new("L", im.size, 0); D.Draw(head_mask).rounded_rectangle([(cx - hw + 4) * S, (cy - hh + 4) * S, (cx + hw - 4) * S, (cy + hh - 4) * S], 146 * S, fill=255)
from PIL import ImageChops
im.paste(inner, (0, 0), ImageChops.multiply(mask, head_mask))
# boeses rotes Auge + halbes Zaehne-Grinsen
rx, ry = cx + 165, cy - 40
glow(rx, ry, 150, (255, 40, 40), 230); glow(rx, ry, 70, (255, 120, 90), 255)
d.ellipse([(rx - 62) * S, (ry - 62) * S, (rx + 62) * S, (ry + 62) * S], fill=(255, 40, 40), outline=INKC, width=6 * S)
d.ellipse([(rx - 26) * S, (ry - 26) * S, (rx + 26) * S, (ry + 26) * S], fill=(255, 220, 190))
d.polygon(P((rx - 90, ry - 110), (rx + 90, ry - 60), (rx + 90, ry - 85), (rx - 80, ry - 140)), fill=(255, 40, 40))   # wuetende Braue
mx, my = cx + 40, cy + 120
d.polygon(P((mx, my), (mx + 230, my - 30), (mx + 200, my + 70), (mx, my + 80)), fill=(200, 20, 30), outline=INKC)
for k in range(5):
    tx = mx + 10 + k * 44; d.polygon(P((tx, my - 2 - k * 5), (tx + 38, my - 6 - k * 6), (tx + 19, my + 34 - k * 4)), fill=(255, 245, 240))
# Rissline + abgeplatzte Splitter
d.line(P(*crack), fill=INKC, width=LW + 4, joint="curve")
for (sx_, sy_, rot) in ((cx + 200, cy - hh - 40, 18), (cx + 330, cy - 250, -12), (cx + 260, cy + hh - 10, 25)):
    pts = [(sx_ - 50, sy_ - 20), (sx_ + 40, sy_ - 35), (sx_ + 55, sy_ + 25), (sx_ - 30, sy_ + 40)]
    c_, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = [(sx_ + (x - sx_) * c_ - (y - sy_) * s_, sy_ + (x - sx_) * s_ + (y - sy_) * c_) for x, y in pts]
    d.polygon(P(*pts), fill=(244, 246, 252), outline=INKC, width=6 * S)
# Text rechts
def txt3(s, x, y, size, col):
    f = ImageFont.truetype(BOLD, size * S)
    d.text(((x + 7) * S, (y + 9) * S), s, font=f, fill=(0, 0, 0, 170), anchor="lm")
    d.text((x * S, y * S), s, font=f, fill=col, anchor="lm", stroke_width=13 * S, stroke_fill=(0, 0, 0))
sizes = [190, 140, 140]
for i_ in range(3):
    while d.textlength(LINES[i_][0], font=ImageFont.truetype(BOLD, sizes[i_] * S)) / S > 1920 - 1090 - 40: sizes[i_] -= 4
txt3(LINES[0][0], 1090, 300, sizes[0], LINES[0][1]); txt3(LINES[1][0], 1090, 510, sizes[1], LINES[1][1]); txt3(LINES[2][0], 1090, 700, sizes[2], LINES[2][1])
out = im.convert("RGB").resize((1920, 1080), Image.LANCZOS)
out.save("THUMB_v4_1920.png"); out.resize((1280, 720), Image.LANCZOS).save("THUMB_v4.jpg", quality=93); print("ok")
