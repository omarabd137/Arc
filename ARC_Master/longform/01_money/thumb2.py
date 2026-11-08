"""Thumbnail v2: Riesiges Schock-Gesicht (Jake) mit Sticker-Kontur, Laptop spuckt 100-$-Scheine, 2 Woerter."""
import os, math, random; os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from hq import *
import props as PR

def sticker(layer, w=14, glow=(255, 255, 255)):
    """weisse Kontur + weicher Schatten um alles Sichtbare in layer (2x)."""
    a = layer.getchannel("A")
    out = a.filter(ImageFilter.MaxFilter(w * 2 + 1))
    sh = a.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.6))
    base = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    base.paste(Image.new("RGBA", layer.size, (0, 0, 0, 255)), (18, 26), sh)
    base.paste(Image.new("RGBA", layer.size, glow + (255,)), (0, 0), out)
    base.alpha_composite(layer); return base

c = canvas((0, 0, 0, 255)); p = Pen(c)
# Hintergrund: tiefes Gruen -> Schwarz, Strahlen, Geld-Leuchten rechts
p.vgrad(0, 0, W, H, (8, 40, 28), (4, 12, 10))
lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
cx0, cy0 = 1350 * SS, 520 * SS
for k in range(24):
    a0 = k * math.pi / 12; a1 = a0 + math.pi / 30
    dl.polygon([(cx0, cy0), (cx0 + math.cos(a0) * 4000, cy0 + math.sin(a0) * 4000), (cx0 + math.cos(a1) * 4000, cy0 + math.sin(a1) * 4000)], fill=(80, 255, 160, 26))
c.alpha_composite(lay); p = Pen(c)
p.glow(1350, 520, 560, (70, 255, 150), 150); p.glow(1350, 520, 260, (220, 255, 200), 120)

# Laptop rechts mit $300,000
lap = canvas(); lp = Pen(lap)
lp.rect(980, 330, 1720, 790, (36, 38, 44), 6, r=22); lp.vgrad(1005, 355, 1695, 765, (240, 255, 244), (200, 246, 216))
lp.text("$0", 1350, 440, 70, BOLD, (200, 50, 44)); lp.line([(1290, 440), (1410, 440)], 9, (200, 50, 44))
lp.text("$300,000", 1350, 610, 150, BOLD, (16, 150, 66), stroke=4, sfill=(255, 255, 255))
lp.poly([(900, 790), (1800, 790), (1880, 870), (820, 870)], (176, 178, 186), 6)
lap = sticker(lap, 10); c.alpha_composite(lap)

# fliegende Scheine aus dem Bildschirm (Tiefe: klein hinten, gross vorne)
r = random.Random(11)
for i, (x, y, w, ang) in enumerate([(1120, 230, 230, -25), (1560, 200, 260, 20), (1820, 520, 260, 38), (1000, 100, 210, -40), (1380, 80, 270, 8),
                                    (1830, 150, 240, -15), (1640, 930, 330, -22), (1060, 950, 300, 16)]):
    b = canvas(); PR.real_bill(b, x, y, w, value="100", angle=ang); c.alpha_composite(sticker(b, 5))

# Jake: Riesen-Kopf links, Haende am Kopf, Schock
j = canvas()
info = figure(j, 440, 1770, 250, JAKE, 0, "line", 0.32, ("up", "up"), "stand", 0, "wide")
jp = Pen(j); hx, hy, hr = info["head"]; ex, ey = info["eye"]
jp.ell(ex - hr * 0.02, ey + hr * 0.55, hr * 0.2, hr * 0.26, (110, 30, 36), 4)             # weit offener Mund
jp.ell(ex - hr * 0.02, ey + hr * 0.68, hr * 0.12, hr * 0.08, (230, 100, 110), 0)            # Zunge
for k in (-1, 1): jp.ell(ex + k * hr * 0.27, ey, hr * 0.12, hr * 0.15, (255, 255, 255), 4); jp.ell(ex + k * hr * 0.27 + hr * 0.03, ey + hr * 0.02, hr * 0.06, hr * 0.07, INK, 0)
for k in range(3): jp.line([(hx - hr * 1.2 - k * 20, hy - hr * 0.9 + k * 50), (hx - hr * 1.45 - k * 24, hy - hr * 1.1 + k * 50)], 10)   # Schock-Striche
for k in range(3): jp.line([(hx + hr * 1.25 + k * 20, hy - hr * 0.9 + k * 50), (hx + hr * 1.5 + k * 24, hy - hr * 1.1 + k * 50)], 10)
c.alpha_composite(sticker(j, 16))

# Text
p = Pen(c)
t = Image.new("RGBA", c.size, (0, 0, 0, 0)); tp = Pen(t)
tp.text("FROM", 440, 120, 130, BOLD, (255, 255, 255), stroke=12)
tp.text("NOTHING", 470, 265, 160, BOLD, (255, 222, 40), stroke=14)
t = t.rotate(-4, center=(460 * SS, 200 * SS), resample=Image.BICUBIC)
c.alpha_composite(t)
im = c.convert("RGB").resize((W, H), Image.LANCZOS)
im.resize((1280, 720), Image.LANCZOS).save("THUMB_v3.jpg", quality=93); im.resize((1280, 720), Image.LANCZOS).save("THUMB_v3.png")
im.resize((360, 202), Image.LANCZOS).save("THUMB_v3_small.png"); print("ok")
