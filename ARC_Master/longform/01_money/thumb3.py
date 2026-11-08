"""Thumbnail v3 nach Analyse der 1M+-Thumbnails: EIN Hauptmotiv, kraeftiger Hintergrund, 2 Woerter auf Balken,
hochwertiger Banker-Charakter (Detail-Bueste), grosser Geldfaecher. 2x gezeichnet."""
import os, math, random; os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
from hq import *
import props as PR

def sticker(layer, w=12, col=(255, 255, 255), shadow=True):
    a = layer.getchannel("A"); out = a.filter(ImageFilter.MaxFilter(w * 2 + 1))
    base = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    if shadow:
        sh = a.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v * 0.55)); base.paste(Image.new("RGBA", layer.size, (40, 0, 0, 255)), (24, 30), sh)
    base.paste(Image.new("RGBA", layer.size, col + (255,)), (0, 0), out); base.alpha_composite(layer); return base

def banker_bust(c, cx, cy, R):
    """Detaillierte Cartoon-Bueste: Anzug mit Revers, Hemd, Krawatte, Kopf mit Licht/Schatten, Brille, Grinsen, Augenbraue hoch."""
    p = Pen(c); skin = (238, 200, 164); suit = (34, 38, 52); hair = (70, 58, 52)
    # Schultern / Anzug
    p.poly([(cx - R * 2.3, cy + R * 3.2), (cx - R * 2.1, cy + R * 1.55), (cx - R * 1.0, cy + R * 1.05), (cx + R * 1.0, cy + R * 1.05), (cx + R * 2.1, cy + R * 1.55), (cx + R * 2.3, cy + R * 3.2)], suit, 5)
    p.poly([(cx - R * 0.42, cy + R * 1.0), (cx + R * 0.42, cy + R * 1.0), (cx + R * 0.3, cy + R * 2.6), (cx - R * 0.3, cy + R * 2.6)], (248, 248, 246), 4)           # Hemd
    p.poly([(cx - R * 0.13, cy + R * 1.12), (cx + R * 0.13, cy + R * 1.12), (cx + R * 0.2, cy + R * 2.3), (cx, cy + R * 2.6), (cx - R * 0.2, cy + R * 2.3)], (180, 30, 40), 4)  # Krawatte
    p.poly([(cx - R * 0.13, cy + R * 1.12), (cx + R * 0.13, cy + R * 1.12), (cx + R * 0.09, cy + R * 1.3), (cx - R * 0.09, cy + R * 1.3)], (150, 20, 30), 3)
    for sx in (-1, 1):                                                                                                                                           # Revers
        p.poly([(cx + sx * R * 0.42, cy + R * 1.0), (cx + sx * R * 0.95, cy + R * 1.08), (cx + sx * R * 0.7, cy + R * 1.55), (cx + sx * R * 0.85, cy + R * 1.75), (cx + sx * R * 0.3, cy + R * 2.6)], (46, 52, 70), 4)
    p.poly([(cx + R * 0.95, cy + R * 1.9), (cx + R * 1.35, cy + R * 1.85), (cx + R * 1.3, cy + R * 2.0)], (250, 250, 250), 2)                                    # Einstecktuch
    p.rect(cx - R * 0.3, cy + R * 0.6, cx + R * 0.3, cy + R * 1.08, dk(skin, 0.9), 4)                                                                             # Hals
    # Kopf
    p.ell(cx, cy, R, R * 1.08, skin, 5)
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.ellipse(p.B(cx - R, cy - R * 1.08, cx + R, cy + R * 1.08), fill=dk(skin, 0.84) + (255,)); dl.ellipse(p.B(cx - R * 1.32, cy - R * 1.2, cx + R * 0.72, cy + R * 1.0), fill=(0, 0, 0, 0))
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).ellipse(p.B(cx - R + 5, cy - R * 1.08 + 5, cx + R - 5, cy + R * 1.08 - 5), fill=255)
    from PIL import ImageChops; lay.putalpha(ImageChops.multiply(lay.getchannel("A"), m)); c.alpha_composite(lay); p = Pen(c)
    for sx in (-1, 1): p.ell(cx + sx * R * 1.0, cy + R * 0.1, R * 0.16, R * 0.24, dk(skin, 0.93), 4)                                                              # Ohren
    # Haare: zurueckgegelt, Seitenscheitel, Glanz
    pts = [(cx + math.cos(math.radians(t)) * R * 1.05, cy + math.sin(math.radians(t)) * R * 1.1) for t in range(185, 356, 5)]
    p.poly(pts + [(cx + R * 0.98, cy - R * 0.25), (cx + R * 0.6, cy - R * 0.62), (cx - R * 0.2, cy - R * 0.68), (cx - R * 0.98, cy - R * 0.3)], hair, 5)
    for k in range(2): p.arc(cx + R * 0.1, cy - R * 0.62 + k * 16, R * (0.6 - k * 0.12), R * 0.3, 205, 315, 4, lt(hair, 0.3))
    p.line([(cx - R * 0.35, cy - R * 1.08), (cx - R * 0.28, cy - R * 0.66)], 4, dk(hair, 0.7))
    # Augen hinter Brille, eine Braue hoch (selbstsicher)
    for sx, by in ((-1, 0.0), (1, -0.12)):
        ex, ey = cx + sx * R * 0.38, cy - R * 0.02
        p.ell(ex, ey, R * 0.15, R * 0.12, (255, 255, 255), 4); p.ell(ex + R * 0.04, ey + R * 0.01, R * 0.08, R * 0.09, (70, 46, 30), 0); p.ell(ex + R * 0.04, ey + R * 0.01, R * 0.045, R * 0.05, INK, 0)
        p.ell(ex + R * 0.07, ey - R * 0.03, R * 0.022, R * 0.022, (255, 255, 255), 0)
        p.arc(ex, ey + R * 0.02, R * 0.13, R * 0.1, 200, 340, 4)                                                                                                     # Oberlid
        p.line([(ex - R * 0.17, ey - R * (0.2 - by) + (R * 0.04 if sx < 0 else 0)), (ex, ey - R * (0.26 - by)), (ex + R * 0.17, ey - R * (0.22 - by))], 9, dk(hair, 0.8))
        p.rect(ex - R * 0.25, ey - R * 0.17, ex + R * 0.25, ey + R * 0.17, None, 5, r=R * 0.06)
    p.line([(cx - R * 0.14, cy - R * 0.04), (cx + R * 0.14, cy - R * 0.04)], 5)
    for sx in (-1, 1): p.line([(cx + sx * R * 0.62, cy - R * 0.04), (cx + sx * R * 0.98, cy - R * 0.1)], 5)
    # Nase, Wangen, Grinsen
    p.line([(cx + R * 0.02, cy + R * 0.1), (cx + R * 0.12, cy + R * 0.32), (cx - R * 0.06, cy + R * 0.36)], 5, dk(skin, 0.6))
    for sx in (-1, 1): p.ell(cx + sx * R * 0.55, cy + R * 0.38, R * 0.14, R * 0.08, (240, 150, 140, 90), 0)
    p.d.chord(p.B(cx - R * 0.42, cy + R * 0.34, cx + R * 0.46, cy + R * 0.82), 10, 160, fill=(255, 255, 255), outline=INK, width=int(5 * SS))
    p.line([(cx - R * 0.36, cy + R * 0.6), (cx + R * 0.4, cy + R * 0.58)], 2.5, (200, 200, 200))
    p.arc(cx + R * 0.48, cy + R * 0.52, R * 0.08, R * 0.08, 270, 60, 4)
    p.line([(cx - R * 0.15, cy + R * 0.92), (cx + R * 0.15, cy + R * 0.92)], 3, dk(skin, 0.75))

c = canvas((0, 0, 0, 255)); p = Pen(c)
# kraeftiger Hintergrund: Orange -> Rot, Halbton-Punkte, Strahlen hinter dem Geld
p.vgrad(0, 0, W, H, (255, 122, 34), (214, 34, 34))
lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay); cx0, cy0 = 1420 * SS, 640 * SS
for k in range(20):
    a0 = k * math.pi / 10; a1 = a0 + math.pi / 22
    dl.polygon([(cx0, cy0), (cx0 + math.cos(a0) * 4200, cy0 + math.sin(a0) * 4200), (cx0 + math.cos(a1) * 4200, cy0 + math.sin(a1) * 4200)], fill=(255, 230, 120, 40))
for y in range(0, H * SS, 34):
    for x in range(0, W * SS, 34): dl.ellipse([x, y, x + 6, y + 6], fill=(120, 0, 0, 28))
c.alpha_composite(lay); p = Pen(c); p.glow(1420, 620, 520, (255, 240, 150), 170)

# Geldfaecher (gross, hochwertig) rechts
money = canvas()
for i, ang in enumerate((-58, -40, -22, -4, 14, 32, 50)):
    b = canvas(); PR.real_bill(b, 1420, 640, 640, value="100", angle=0)
    b = b.rotate(ang, center=(1420 * SS, 900 * SS), resample=Image.BICUBIC); money.alpha_composite(b)
for (x, y, w, a) in ((1180, 210, 300, -30), (1740, 200, 320, 25), (1830, 560, 280, 60)):
    b = canvas(); PR.real_bill(b, x, y, w, value="100", angle=a); money.alpha_composite(b)
c.alpha_composite(sticker(money, 8))

# Banker-Bueste links, Hand drueckt ENTER
bk = canvas(); banker_bust(bk, 520, 500, 250)
c.alpha_composite(sticker(bk, 14))

# Text oben rechts auf schwarzem Balken
t = Image.new("RGBA", c.size, (0, 0, 0, 0)); tp = Pen(t)
tp.rect(930, 46, 1830, 220, (12, 12, 14), 0); tp.text("FROM NOTHING", 1380, 136, 104, BOLD, (255, 255, 255))
t = t.rotate(2, center=(1380 * SS, 136 * SS), resample=Image.BICUBIC); c.alpha_composite(t)

im = c.convert("RGB").resize((W, H), Image.LANCZOS)
im.resize((1280, 720), Image.LANCZOS).save("THUMB_v3.jpg", quality=93); im.resize((1280, 720), Image.LANCZOS).save("THUMB_v3.png")
im.resize((360, 202), Image.LANCZOS).save("THUMB_v3_small.png"); print("ok")
