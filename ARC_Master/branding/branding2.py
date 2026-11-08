"""ARC Branding v2: bunt, Cartoon-Stil der Videos (hq.py-Figuren), breiter Claim "The world, explained."
Banner 2560x1440 (Handy-Safe-Area 1546x423 Mitte), Profilbild 800x800."""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../longform/01_money")); os.chdir(HERE)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from hq import *
from bgs import clouds, tree

YEL, BLUE = (255, 206, 46), (64, 150, 230)

def logo(c, cx, cy, size):
    """ARC-Logo: weisse Blockbuchstaben, dicke Tusche-Kontur, gelber Bogen-Pfeil darueber."""
    p = Pen(c); r = size * 1.22; oy = cy + size * 0.25
    p.arc(cx, oy, r, r * 0.85, 203, 333, size * 0.13, INK)
    p.arc(cx, oy, r, r * 0.85, 203, 333, size * 0.085, YEL)
    a = math.radians(333); ex, ey = cx + math.cos(a) * r, oy + math.sin(a) * r * 0.85; s = size * 0.2
    p.poly([(ex + s * 0.9, ey - s * 0.95), (ex - s * 0.7, ey - s * 0.8), (ex + s * 0.45, ey + s * 0.85)], YEL, size * 0.03)
    f = ImageFont.truetype(BOLD, int(size * SS))
    ImageDraw.Draw(c).text((cx * SS + 12 * SS, cy * SS + 22 * SS), "ARC", font=f, fill=(0, 0, 0, 90), anchor="mm", stroke_width=int(size * 0.07 * SS), stroke_fill=(0, 0, 0, 90))
    ImageDraw.Draw(c).text((cx * SS, cy * SS + 10 * SS), "ARC", font=f, fill=(255, 255, 255), anchor="mm", stroke_width=int(size * 0.07 * SS), stroke_fill=INK)

def robot(c, cx, base, R):
    """freundlicher Cartoon-Roboter (Thema KI/Technik)."""
    p = Pen(c); p.shadow(cx, base, R * 1.0, R * 0.16, 60)
    for sx in (-1, 1): p.rect(cx + sx * R * 0.3 - R * 0.14, base - R * 1.5, cx + sx * R * 0.3 + R * 0.14, base, (150, 170, 190), 3, r=8)
    p.rect(cx - R * 0.75, base - R * 3.0, cx + R * 0.75, base - R * 1.45, (190, 206, 222), 3.4, r=R * 0.25)
    p.rect(cx - R * 0.4, base - R * 2.6, cx + R * 0.4, base - R * 2.0, (80, 200, 255), 3, r=10)
    for sx in (-1, 1): p.line([(cx + sx * R * 0.75, base - R * 2.7), (cx + sx * R * 1.15, base - R * 2.1), (cx + sx * R * 1.2, base - R * 1.7)], R * 0.18, (150, 170, 190))
    p.rect(cx - R * 0.95, base - R * 4.7, cx + R * 0.95, base - R * 3.15, (210, 222, 236), 3.6, r=R * 0.35)
    p.rect(cx - R * 0.75, base - R * 4.45, cx + R * 0.75, base - R * 3.4, (30, 40, 60), 3, r=R * 0.25)
    for sx in (-1, 1): p.ell(cx + sx * R * 0.35, base - R * 3.95, R * 0.16, R * 0.18, (80, 220, 255), 0)
    p.arc(cx, base - R * 3.75, R * 0.3, R * 0.2, 20, 160, 4, (80, 220, 255))
    p.line([(cx, base - R * 4.7), (cx, base - R * 5.2)], 4); p.ell(cx, base - R * 5.3, R * 0.14, R * 0.14, (255, 90, 80), 3)

# ---------------- Banner (im 1920x1080-Raster gezeichnet, dann auf 2560x1440) ----------------
c = canvas((255, 255, 255, 255)); p = Pen(c)
p.vgrad(0, 0, W, 700, (96, 178, 240), (190, 228, 252)); clouds(p, 160, 4, 6)
r = random.Random(3); x = -10
while x < W:                                              # bunte Cartoon-Skyline
    bw = r.randint(70, 150); bh = r.randint(140, 330)
    if 420 < x < 1450: bh = int(bh * 0.5)
    col = r.choice([(250, 214, 140), (170, 206, 236), (236, 170, 150), (196, 226, 190), (230, 222, 246), (255, 236, 190)])
    p.rect(x, 720 - bh, x + bw, 720, col, 3)
    for wy in range(int(720 - bh + 16), 705, 30):
        for wx in range(int(x + 12), int(x + bw - 14), 26): p.rect(wx, wy, wx + 12, wy + 16, (120, 170, 220), 1.6)
    if r.random() < 0.3: p.poly([(x - 6, 720 - bh), (x + bw / 2, 720 - bh - 50), (x + bw + 6, 720 - bh)], dk(col, 0.85), 3)
    x += bw + r.randint(4, 18)
p.rect(0, 700, W, H, (120, 200, 110), 0); p.vgrad(0, 700, W, H, (128, 204, 110), (98, 176, 88))
for tx in (80, 1840): tree(p, tx, 790, 0.7, tx)
# Figuren links und rechts (ausserhalb der Handy-Safe-Area, auf Desktop sichtbar)
figure(c, 175, 690, 40, JAKE, 1, "grin", 0.0, ("down", "wave"))
figure(c, 290, 690, 40, RYAN, 1, "smile", 0.0, ("hip", "down"))
figure(c, 1620, 690, 40, BANKER, -1, "smile", 0.0, ("down", "point"))
robot(c, 1750, 690, 34)
# Safe-Area (1160x317 Mitte im 1920-Raster): Logo + Claim + Rhythmus
Pen(c).glow(900, 560, 420, (255, 255, 255), 150)
logo(c, 610, 545, 125)
p = Pen(c)
p.text("THE WORLD,", 820, 505, 70, BOLD, (255, 255, 255), "lm", stroke=7)
p.text("EXPLAINED.", 820, 590, 70, BOLD, YEL, "lm", stroke=7)
bn = c.convert("RGB").resize((2560, 1440), Image.LANCZOS); bn.save("ARC_banner_2560x1440.png")
bn.crop((507, 508, 2053, 931)).save("_vorschau_banner_handy.png")
bn.crop((0, 508, 2560, 931)).resize((1280, 212), Image.LANCZOS).save("_vorschau_banner_desktop.png")

# ---------------- Profilbild ----------------
pc = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); pp = Pen(pc)
pp.ell(960, 540, 520, 520, (70, 156, 232), 0); pp.vgrad(440, 20, 1480, 1060, (110, 190, 246), (40, 120, 210))
m = Image.new("L", pc.size, 0); ImageDraw.Draw(m).ellipse([440 * SS, 20 * SS, 1480 * SS, 1060 * SS], fill=255)
bgc = Image.new("RGBA", pc.size, (0, 0, 0, 0)); bgc.paste(pc, (0, 0), m); pc = bgc; pp = Pen(pc)
pp.ell(960, 540, 515, 515, None, 14)
logo(pc, 960, 600, 270)
pf = pc.crop((440 * SS, 20 * SS, 1480 * SS, 1060 * SS)).resize((800, 800), Image.LANCZOS)
out = Image.new("RGB", (800, 800), (70, 156, 232)); out.paste(pf, (0, 0), pf); out.save("ARC_profilbild_800.png")
circ = Image.new("L", (800, 800), 0); ImageDraw.Draw(circ).ellipse([0, 0, 799, 799], fill=255)
prev = Image.new("RGB", (800, 800), (15, 15, 15)); prev.paste(out, (0, 0), circ); prev.resize((176, 176), Image.LANCZOS).save("_vorschau_profil_klein.png")
print("ok")
