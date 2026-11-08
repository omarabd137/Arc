"""ARC HQ-Hintergruende: detailreich, Licht + Schatten, glaubwuerdige Orte. Jede Funktion -> 1x RGB-Bild (gecacht)."""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from hq import *

_cache = {}
def bg(name, *a):
    k = (name,) + a
    if k not in _cache:
        c = canvas((255, 255, 255, 255)); globals()["bg_" + name](c, *a); _cache[k] = finish(c).convert("RGBA")
    return _cache[k]

# ---------------- Bausteine ----------------
def clouds(p, y, seed=1, n=5, col=(255, 255, 255)):
    r = random.Random(seed)
    for i in range(n):
        x = r.randint(80, 1840); yy = y + r.randint(-60, 60); s = r.uniform(0.7, 1.3)
        for dx, dy, rr in ((0, 0, 60), (55, -20, 50), (110, 0, 55), (-50, 10, 42), (160, 12, 40)):
            p.ell(x + dx * s, yy + dy * s, rr * s * 1.3, rr * s * 0.8, col + (235,), 0)

def tree(p, x, base, s=1.0, seed=0, col=(84, 140, 76)):
    r = random.Random(seed)
    p.shadow(x, base, 120 * s, 18 * s, 50)
    p.poly([(x - 16 * s, base), (x - 10 * s, base - 200 * s), (x + 10 * s, base - 200 * s), (x + 16 * s, base)], (118, 86, 58), 3)
    for k in range(3): p.line([(x - 6 * s + k * 5 * s, base - 30 * s - k * 40 * s), (x - 2 * s + k * 5 * s, base - 70 * s - k * 40 * s)], 1.6, (90, 64, 44))
    blobs = [(0, -300, 120), (-90, -250, 95), (90, -250, 95), (-50, -360, 85), (60, -360, 85), (0, -200, 100)]
    for dx, dy, rr in blobs: p.ell(x + dx * s, base + dy * s, rr * s, rr * s * 0.9, col, 3)
    for dx, dy, rr in blobs[:4]: p.ell(x + dx * s - 20 * s, base + dy * s - 22 * s, rr * s * 0.55, rr * s * 0.45, lt(col, 0.18), 0)
    for _ in range(14):
        a = r.uniform(0, 6.28); d_ = r.uniform(30, 150) * s
        p.arc(x + math.cos(a) * d_, base - 290 * s + math.sin(a) * d_ * 0.7, 14 * s, 9 * s, 200, 340, 2, dk(col, 0.75))

def bush(p, x, base, s=1.0, col=(76, 130, 70)):
    for dx, rr in ((-50, 45), (0, 58), (50, 45)): p.ell(x + dx * s, base - rr * s * 0.7, rr * s, rr * s * 0.75, col, 3)
    p.ell(x - 15 * s, base - 62 * s, 22 * s, 14 * s, lt(col, 0.2), 0)

def window(p, x0, y0, x1, y1, glass=(170, 208, 232), frame=(250, 250, 246), curtains=None, glow=False, cross=True):
    p.rect(x0 - 10, y0 - 10, x1 + 10, y1 + 10, frame, 3)
    p.vgrad(x0, y0, x1, y1, lt(glass, 0.15) if not glow else (255, 226, 150), dk(glass, 0.9) if not glow else (240, 180, 90))
    p.rect(x0, y0, x1, y1, None, 3)
    p.poly([(x0 + 8, y1 - 10), (x0 + (x1 - x0) * 0.35, y0 + 8), (x0 + (x1 - x0) * 0.5, y0 + 8), (x0 + 22, y1 - 10)], (255, 255, 255, 70), 0)
    if curtains:
        p.poly([(x0, y0), (x0 + (x1 - x0) * 0.22, y0), (x0 + (x1 - x0) * 0.14, y1), (x0, y1)], curtains, 2.4)
        p.poly([(x1, y0), (x1 - (x1 - x0) * 0.22, y0), (x1 - (x1 - x0) * 0.14, y1), (x1, y1)], curtains, 2.4)
    if cross: p.line([((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], 5, frame); p.line([(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)], 5, frame)
    p.rect(x0 - 18, y1 + 10, x1 + 18, y1 + 24, dk(frame, 0.92), 3)

def house(p, x, base, w=560, body=(236, 226, 204), roof=(150, 74, 60), door=(70, 110, 150), seed=0, glow=False, porch=True):
    h = w * 0.55; top = base - h
    p.shadow(x + w / 2, base + 6, w * 0.55, 20, 60)
    p.rect(x, top, x + w, base, body, 3.4)
    for k in range(int(h / 16)): p.line([(x + 3, top + 12 + k * 16), (x + w - 3, top + 12 + k * 16)], 1.2, dk(body, 0.9))
    p.rect(x - 6, base - 26, x + w + 6, base, dk(body, 0.78), 3)                                           # Fundament
    p.rect(x + w * 0.7, top - h * 0.75, x + w * 0.8, top - h * 0.2, (150, 90, 70), 3)                       # Kamin
    roof_pts = [(x - 40, top + 6), (x + w / 2, top - h * 0.72), (x + w + 40, top + 6)]
    p.poly(roof_pts, roof, 3.6)
    for k in range(1, 7):                                                                                     # Dachziegel-Reihen
        yy = top + 6 - k * h * 0.1; half = (w / 2 + 40) * (1 - k * 0.1 / 0.72)
        p.line([(x + w / 2 - half, yy), (x + w / 2 + half, yy)], 1.6, dk(roof, 0.8))
    p.poly([(x - 40, top + 6), (x + w + 40, top + 6), (x + w + 30, top + 18), (x - 30, top + 18)], dk(roof, 0.75), 2.6)
    window(p, x + w * 0.08, top + h * 0.25, x + w * 0.3, top + h * 0.6, curtains=(236, 214, 170), glow=glow)
    window(p, x + w * 0.62, top + h * 0.25, x + w * 0.88, top + h * 0.6, curtains=(236, 214, 170), glow=glow)
    dx0 = x + w * 0.4
    p.rect(dx0, top + h * 0.3, dx0 + w * 0.16, base - 26, door, 3.2)
    for k in range(2): p.rect(dx0 + 10, top + h * 0.36 + k * h * 0.28, dx0 + w * 0.16 - 10, top + h * 0.56 + k * h * 0.28, dk(door, 0.88), 2)
    p.ell(dx0 + w * 0.135, top + h * 0.68, 5, 5, (230, 200, 110), 2)
    if porch:
        p.rect(dx0 - 30, base - 26, dx0 + w * 0.16 + 30, base - 12, (200, 196, 188), 2.6); p.rect(dx0 - 44, base - 12, dx0 + w * 0.16 + 44, base + 2, (186, 182, 174), 2.6)
        p.poly([(dx0 - 50, top + h * 0.28), (dx0 + w * 0.16 + 50, top + h * 0.28), (dx0 + w * 0.16 + 30, top + h * 0.2), (dx0 - 30, top + h * 0.2)], roof, 2.6)
        p.ell(dx0 + w * 0.08, top + h * 0.24, 10, 8, (255, 230, 150) if glow else (240, 236, 220), 2)

def fence(p, x0, x1, base, col=(250, 250, 246)):
    p.rect(x0, base - 70, x1, base - 60, col, 2.4); p.rect(x0, base - 30, x1, base - 22, col, 2.4)
    for x in range(int(x0), int(x1), 34): p.poly([(x, base), (x, base - 88), (x + 11, base - 100), (x + 22, base - 88), (x + 22, base)], col, 2.4)

def mailbox(p, x, base):
    p.rect(x - 6, base - 120, x + 6, base, (110, 80, 56), 2.6)
    p.rect(x - 40, base - 170, x + 40, base - 120, (60, 70, 90), 3, r=18); p.rect(x + 30, base - 165, x + 36, base - 135, (200, 50, 44), 2)

def lamp_post(p, x, base, on=False):
    p.rect(x - 7, base - 360, x + 7, base, (50, 54, 60), 2.6); p.rect(x - 26, base - 400, x + 26, base - 356, (60, 64, 70), 3, r=6)
    if on: p.glow(x, base - 378, 90, (255, 220, 140), 120)

def floor_planks(p, y0, col=(170, 130, 94)):
    p.vgrad(0, y0, W, H, col, dk(col, 0.82))
    for k in range(9): p.line([(0, y0 + 20 + k * (H - y0) / 9 * (0.6 + k * 0.08)), (W, y0 + 20 + k * (H - y0) / 9 * (0.6 + k * 0.08))], 1.6, dk(col, 0.78))
    r = random.Random(3)
    for k in range(40): yy = r.uniform(y0, H); xx = r.uniform(0, W); p.line([(xx, yy), (xx, yy + 18)], 1.4, dk(col, 0.8))

def floor_tiles(p, y0, a=(226, 222, 214), b=(170, 164, 156)):
    p.rect(0, y0, W, H, a, 0)
    vx = W / 2; rows = 7
    for i in range(rows + 1):
        k = (i / rows) ** 1.7; y = y0 + (H - y0) * k; p.line([(0, y), (W, y)], 1.6, dk(b, 0.9))
    for j in range(-12, 13): p.line([(vx + j * 40, y0), (vx + j * 260, H)], 1.6, dk(b, 0.9))
    lay_rows = []
    for i in range(rows):
        k0, k1 = (i / rows) ** 1.7, ((i + 1) / rows) ** 1.7; ya, yb = y0 + (H - y0) * k0, y0 + (H - y0) * k1
        for j in range(-12, 12):
            if (i + j) % 2: continue
            xa0, xa1 = vx + j * 40 + (j * 220) * k0, vx + (j + 1) * 40 + ((j + 1) * 220) * k0
            xb0, xb1 = vx + j * 40 + (j * 220) * k1, vx + (j + 1) * 40 + ((j + 1) * 220) * k1
            p.poly([(xa0, ya), (xa1, ya), (xb1, yb), (xb0, yb)], b + (110,), 0)

def wall(p, y1, col, wains=None, stripes=False):
    p.vgrad(0, 0, W, y1, lt(col, 0.06), dk(col, 0.95))
    if stripes:
        for x in range(0, W, 90): p.rect(x, 0, x + 45, y1, dk(col, 0.97) + (120,), 0)
    if wains:
        p.rect(0, y1 - 260, W, y1, wains, 0); p.line([(0, y1 - 260), (W, y1 - 260)], 3)
        for x in range(40, W, 240): p.rect(x, y1 - 230, x + 190, y1 - 30, dk(wains, 0.94), 2)
    p.rect(0, y1 - 18, W, y1, dk(col, 0.7), 2.4)

def frame_pic(p, x, y, w, h, scene_col=(120, 170, 200)):
    p.rect(x, y, x + w, y + h, (150, 110, 70), 3); p.vgrad(x + 12, y + 12, x + w - 12, y + h - 12, lt(scene_col, 0.3), scene_col)
    p.poly([(x + 12, y + h - 12), (x + w * 0.4, y + h * 0.45), (x + w * 0.6, y + h * 0.65), (x + w * 0.75, y + h * 0.5), (x + w - 12, y + h - 12)], (90, 130, 90), 0)

def plant(p, x, base, s=1.0):
    p.poly([(x - 40 * s, base - 90 * s), (x + 40 * s, base - 90 * s), (x + 30 * s, base), (x - 30 * s, base)], (190, 110, 80), 3)
    for a in range(-70, 80, 22):
        r_ = math.radians(a - 90); p.poly([(x, base - 90 * s), (x + math.cos(r_ - 0.2) * 90 * s, base - 90 * s + math.sin(r_ - 0.2) * 150 * s),
                                          (x + math.cos(r_) * 120 * s, base - 90 * s + math.sin(r_) * 190 * s), (x + math.cos(r_ + 0.2) * 90 * s, base - 90 * s + math.sin(r_ + 0.2) * 150 * s)], (70, 140, 80), 2.4)

def desk(p, x0, x1, y, col=(150, 108, 74), legs=True, front=True):
    p.rect(x0 - 10, y, x1 + 10, y + 26, lt(col, 0.1), 3)
    if front: p.rect(x0, y + 26, x1, y + 210, col, 3); p.rect(x0 + 30, y + 50, x0 + (x1 - x0) * 0.4, y + 110, dk(col, 0.9), 2); p.ell(x0 + (x1 - x0) * 0.22, y + 80, 6, 6, (210, 190, 120), 2)
    elif legs:
        for xx in (x0 + 20, x1 - 40): p.rect(xx, y + 26, xx + 20, y + 230, dk(col, 0.85), 2.6)

def monitor(p, x, y, w=260, screen=(40, 60, 90)):
    p.rect(x - w / 2, y - w * 0.62, x + w / 2, y, (40, 42, 48), 3, r=8); p.vgrad(x - w / 2 + 10, y - w * 0.62 + 10, x + w / 2 - 10, y - 10, lt(screen, 0.2), screen)
    p.rect(x - 14, y, x + 14, y + 40, (60, 62, 68), 2.4); p.rect(x - 60, y + 40, x + 60, y + 52, (60, 62, 68), 2.4, r=4)

def chair(p, x, base, col=(60, 64, 74), face=1):
    p.rect(x - 60, base - 130, x + 60, base - 110, col, 3, r=8); p.rect(x - face * 60 - 8, base - 300, x - face * 60 + 14, base - 110, col, 3, r=8)
    p.rect(x - 6, base - 110, x + 6, base - 30, (90, 92, 98), 2.4)
    for sx in (-1, 1): p.line([(x, base - 30), (x + sx * 55, base - 6)], 4)

def city_view(p, x0, y0, x1, y1, night=False, seed=2):
    p.vgrad(x0, y0, x1, y1, (40, 50, 90) if night else (160, 200, 236), (90, 70, 110) if night else (220, 232, 244))
    r = random.Random(seed); x = x0
    while x < x1:
        bw = r.randint(50, 110); bh = r.randint(int((y1 - y0) * 0.3), int((y1 - y0) * 0.85)); col = (60, 70, 100) if night else (150, 166, 190)
        p.rect(x, y1 - bh, min(x1, x + bw), y1, col, 0)
        for wy in range(int(y1 - bh + 12), int(y1 - 8), 22):
            for wx in range(int(x + 8), int(min(x1, x + bw) - 10), 18):
                if r.random() < (0.45 if night else 0.8): p.rect(wx, wy, wx + 8, wy + 10, (255, 220, 140) if night else (200, 216, 232), 0)
        x += bw + r.randint(4, 16)

# ---------------- Orte ----------------
def bg_table(c, mood="warm"):
    p = Pen(c); p.vgrad(0, 0, W, 620, (34, 28, 30), (24, 20, 22))
    p.rect(0, 600, W, H, (120, 82, 52), 0)
    r = random.Random(4)
    for k in range(7):
        y = 600 + k * 70; p.line([(0, y), (W, y + r.uniform(-4, 4))], 2.2, (92, 62, 40))
        for _ in range(6): xx = r.uniform(0, W); p.arc(xx, y + 35, r.uniform(40, 120), 10, 200, 340, 1.4, (104, 70, 46))
    p.glow(960, 640, 520, (255, 214, 150), 110 if mood == "warm" else 70)
    p.glow(960, 200, 120, (255, 220, 160), 80)

def bg_street(c, tod="day"):
    p = Pen(c); sky = {"day": ((132, 186, 230), (214, 232, 246)), "sunset": ((252, 160, 110), (255, 220, 170)), "evening": ((70, 80, 130), (230, 150, 120))}[tod]
    p.vgrad(0, 0, W, 720, *sky); clouds(p, 160, 3, 5, (255, 255, 255) if tod == "day" else (255, 214, 190))
    if tod != "day": p.glow(1500, 600, 220, (255, 200, 120), 150)
    for x in (-60, 1960): tree(p, x, 720, 1.2, 9)
    p.rect(0, 690, W, 860, (128, 176, 98), 0); p.vgrad(0, 690, W, 860, (128, 176, 98), (106, 156, 84))
    house(p, 170, 760, 620, (236, 226, 204), (150, 74, 60), (70, 110, 150), 1, glow=tod != "day")
    house(p, 1130, 760, 620, (204, 220, 230), (70, 80, 100), (150, 60, 50), 2, glow=tod != "day")
    fence(p, 0, 160, 790); fence(p, 800, 1120, 790); fence(p, 1760, W, 790)
    bush(p, 120, 780, 1.0); bush(p, 860, 790, 0.9); bush(p, 1800, 790, 1.0)
    tree(p, 960, 770, 0.85, 5)
    mailbox(p, 700, 830); mailbox(p, 1660, 830)
    p.rect(0, 840, W, 900, (206, 202, 194), 2.4)
    for x in range(0, W, 120): p.line([(x, 840), (x - 10, 900)], 1.6, (176, 172, 166))
    p.rect(0, 900, W, 912, (170, 166, 160), 2)
    p.vgrad(0, 912, W, H, (100, 102, 108), (82, 84, 90))
    for x in range(30, W, 260): p.rect(x, 1000, x + 130, 1010, (236, 230, 200), 0)
    lamp_post(p, 1040, 900, on=tod != "day")

def bg_office(c):
    p = Pen(c); wall(p, 700, (226, 222, 214))
    for i, x in enumerate((160, 760, 1360)): p.rect(x, 90, x + 420, 520, (90, 96, 106), 4); city_view(p, x + 10, 100, x + 410, 510, False, i + 3)
    floor_tiles(p, 700, (196, 196, 200), (170, 170, 176))
    plant(p, 1800, 760, 1.1)
    p.rect(1700, 200, 1840, 420, (250, 250, 248), 3); p.text("Q3", 1770, 240, 26, SANS); [p.rect(1720 + k * 30, 400 - (k + 1) * 30, 1740 + k * 30, 400, (60, 150, 90), 1.6) for k in range(4)]

def bg_apartment(c, night=False):
    p = Pen(c); wall(p, 720, (196, 186, 166) if not night else (110, 104, 100), stripes=True)
    for k in range(5): p.line([(300 + k * 3, 160 + k * 40), (330 + k * 5, 200 + k * 40)], 1.4, (170, 160, 140))      # Riss/Patina
    p.rect(1180, 140, 1600, 520, (120, 110, 100), 4); p.vgrad(1190, 150, 1590, 510, (150, 110, 90) if not night else (40, 40, 60), (120, 90, 80) if not night else (30, 30, 46))
    for yy in range(160, 510, 36):
        for xx in range(1190 + (yy // 36 % 2) * 30, 1590, 60): p.rect(xx, yy, xx + 56, yy + 32, (160, 100, 80) if not night else (60, 50, 60), 1.2)   # Ziegelwand vor dem Fenster
    p.line([(1390, 140), (1390, 520)], 6, (120, 110, 100)); p.rect(1160, 520, 1620, 540, (140, 130, 120), 3)
    floor_planks(p, 720, (150, 120, 92) if not night else (90, 72, 60))
    p.rect(120, 420, 520, 720, (200, 196, 186), 3); p.rect(120, 400, 520, 430, (230, 226, 216), 3); p.rect(160, 300, 260, 400, (240, 240, 236), 2.4)   # Mini-Kueche
    p.ell(400, 420, 50, 10, (180, 180, 186), 2); p.rect(560, 330, 640, 400, (60, 60, 64), 2.4)
    if night: p.glow(960, 200, 260, (255, 210, 140), 70)
    p.line([(960, 0), (960, 150)], 2.4); p.poly([(910, 150), (1010, 150), (990, 200), (930, 200)], (230, 210, 160), 2.6)

def bg_porch(c, tod="day"):
    p = Pen(c); sky = ((150, 196, 232), (220, 236, 246)) if tod == "day" else ((250, 150, 110), (255, 214, 170))
    p.vgrad(0, 0, W, 600, *sky); clouds(p, 140, 8, 4, (255, 255, 255) if tod == "day" else (255, 220, 190))
    if tod != "day": p.glow(300, 520, 260, (255, 200, 120), 140)
    tree(p, 150, 640, 1.0, 3); tree(p, 520, 660, 0.8, 4)
    p.rect(0, 600, W, 700, (120, 170, 96), 0)
    p.rect(700, 0, W, 760, (236, 226, 204), 3.4)
    for k in range(48): p.line([(703, 12 + k * 16), (W, 12 + k * 16)], 1.2, (214, 204, 184))
    window(p, 1350, 160, 1700, 500, curtains=(200, 170, 120), glow=tod != "day")
    p.rect(980, 140, 1180, 760, (90, 70, 56), 3.2); p.ell(1155, 450, 6, 6, (230, 200, 110), 2)
    p.rect(0, 760, W, 800, (176, 140, 100), 3); floor_planks(p, 800, (186, 148, 104))
    for x in range(-20, 700, 70): p.rect(x, 640, x + 22, 800, (250, 250, 246), 2.4)
    p.rect(-20, 630, 700, 652, (250, 250, 246), 2.6)
    for x in (700, 1880): p.rect(x - 18, 0, x + 18, 800, (250, 250, 246), 3)
    plant(p, 1800, 800, 0.9)

def bg_bank(c):
    p = Pen(c); p.vgrad(0, 0, W, 680, (238, 232, 220), (220, 212, 198))
    r = random.Random(7)
    for k in range(30):                                                          # Marmor-Adern
        x = r.uniform(0, W); y = r.uniform(0, 640); p.line([(x, y), (x + r.uniform(-80, 80), y + r.uniform(20, 120)), (x + r.uniform(-120, 120), y + r.uniform(80, 200))], 1.4, (200, 192, 180))
    for x in (120, 620, 1300, 1800):                                             # Saeulen
        p.rect(x - 50, 60, x + 50, 680, (244, 240, 232), 3.4)
        for k in range(-2, 3): p.line([(x + k * 18, 90), (x + k * 18, 650)], 1.6, (214, 208, 196))
        p.rect(x - 70, 40, x + 70, 80, (236, 230, 218), 3); p.rect(x - 70, 650, x + 70, 690, (236, 230, 218), 3)
    p.rect(700, 70, 1220, 170, (30, 54, 92), 3.4, r=6); p.text("FIRST NATIONAL BANK", 960, 120, 40, SERIF, (236, 214, 150))
    p.ell(960, 230, 46, 46, (250, 248, 240), 3); p.line([(960, 230), (960, 200)], 3); p.line([(960, 230), (982, 238)], 3)
    floor_tiles(p, 680, (232, 228, 220), (150, 120, 96))
    p.rect(250, 520, 1670, 560, (120, 84, 56), 3.4)                              # Schaltertheke
    p.rect(270, 560, 1650, 820, (146, 104, 70), 3.4)
    for x in range(300, 1640, 230): p.rect(x, 590, x + 190, 790, (130, 92, 62), 2.4)
    for k in range(3):                                                           # Glas + Messing
        x = 330 + k * 450; p.rect(x, 280, x + 360, 520, (200, 224, 236, 120), 3)
        p.rect(x - 10, 270, x + 370, 284, (196, 160, 80), 2.4); p.rect(x + 130, 490, x + 230, 520, (40, 40, 44), 2.4)
        p.poly([(x + 30, 500), (x + 120, 300), (x + 160, 300), (x + 70, 500)], (255, 255, 255, 60), 0)
    for x in (330, 1590):
        p.line([(x, 0), (x, 60)], 2); p.poly([(x - 60, 60), (x + 60, 60), (x + 40, 100), (x - 40, 100)], (40, 80, 60), 3); p.glow(x, 110, 70, (255, 220, 150), 90)
    for x in (180, 520):                                                         # Absperrung
        p.rect(x - 8, 860, x + 8, 990, (196, 160, 80), 2.4); p.ell(x, 856, 14, 10, (196, 160, 80), 2.4)
    p.line([(180, 880), (350, 910), (520, 880)], 8, (150, 30, 40))

def bg_bank_counter(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (236, 230, 218), (214, 206, 192))
    p.rect(0, 700, W, 760, (120, 84, 56), 3.4); p.rect(0, 760, W, H, (146, 104, 70), 3.4)
    p.rect(380, 100, 1540, 700, (210, 230, 240, 110), 4); p.rect(370, 86, 1550, 106, (196, 160, 80), 3)
    p.rect(820, 640, 1100, 700, (40, 40, 44), 3); p.poly([(440, 680), (700, 120), (780, 120), (520, 680)], (255, 255, 255, 50), 0)
    p.rect(1600, 520, 1800, 700, (60, 64, 74), 3); p.text("DEPOSIT", 1700, 560, 22, SANS, (240, 240, 240))

def bg_coatcheck(c):
    p = Pen(c); wall(p, 680, (120, 40, 50), wains=(90, 30, 38))
    p.rect(300, 140, 1620, 520, (70, 50, 40), 3)
    r = random.Random(2)
    for k in range(11):
        x = 360 + k * 115; col = [(60, 70, 100), (120, 90, 60), (40, 40, 44), (150, 60, 50), (90, 110, 90)][k % 5]
        p.line([(x, 170), (x, 200)], 3); p.poly([(x - 40, 200), (x + 40, 200), (x + 52, 470), (x - 52, 470)], col, 3)
    p.rect(200, 520, 1720, 580, (110, 76, 50), 3.4); p.rect(220, 580, 1700, 860, (90, 60, 40), 3.4)
    floor_planks(p, 860, (110, 80, 60)); p.rect(860, 40, 1060, 110, (30, 30, 34), 3, r=8); p.text("COAT CHECK", 960, 76, 30, SERIF, (236, 214, 150))

def bg_dealer(c):
    p = Pen(c); p.vgrad(0, 0, W, 640, (232, 236, 240), (210, 216, 222))
    for x in range(0, W, 320): p.rect(x, 60, x + 300, 600, (190, 214, 230, 160), 3)
    city_view(p, 0, 60, W, 600, False, 11)
    for x in range(0, W, 320): p.rect(x, 60, x + 300, 600, (200, 224, 238, 110), 3)
    floor_tiles(p, 640, (240, 240, 244), (210, 212, 220))
    p.rect(1500, 160, 1820, 300, (200, 40, 44), 3, r=10); p.text("NEW 2026", 1660, 230, 48, BOLD, (255, 255, 255))

def car(p, x, base, w=760, col=(200, 40, 44)):
    h = w * 0.3; p.shadow(x + w / 2, base, w * 0.55, 22, 90)
    body = [(x, base - h * 0.28), (x + w * 0.05, base - h * 0.55), (x + w * 0.28, base - h * 0.62), (x + w * 0.4, base - h * 0.98), (x + w * 0.72, base - h * 0.98),
            (x + w * 0.86, base - h * 0.6), (x + w, base - h * 0.5), (x + w, base - h * 0.22), (x + w * 0.96, base - h * 0.12), (x + w * 0.04, base - h * 0.12)]
    p.poly(body, col, 3.6)
    p.poly([(x + w * 0.43, base - h * 0.9), (x + w * 0.56, base - h * 0.9), (x + w * 0.56, base - h * 0.62), (x + w * 0.33, base - h * 0.62)], (170, 206, 230), 3)
    p.poly([(x + w * 0.59, base - h * 0.9), (x + w * 0.7, base - h * 0.9), (x + w * 0.82, base - h * 0.62), (x + w * 0.59, base - h * 0.62)], (170, 206, 230), 3)
    p.line([(x + w * 0.05, base - h * 0.42), (x + w * 0.98, base - h * 0.38)], 2, lt(col, 0.4))
    p.rect(x + w * 0.95, base - h * 0.46, x + w * 1.0, base - h * 0.36, (255, 236, 170), 2); p.rect(x, base - h * 0.44, x + w * 0.03, base - h * 0.34, (220, 60, 50), 2)
    for wx in (x + w * 0.2, x + w * 0.8):
        p.ell(wx, base - h * 0.1, h * 0.26, h * 0.26, (30, 30, 34), 3); p.ell(wx, base - h * 0.1, h * 0.14, h * 0.14, (190, 192, 198), 2.6)
        for k in range(5): a = k * 1.256; p.line([(wx, base - h * 0.1), (wx + math.cos(a) * h * 0.12, base - h * 0.1 + math.sin(a) * h * 0.12)], 2, (120, 122, 128))
    p.line([(x + w * 0.57, base - h * 0.6), (x + w * 0.57, base - h * 0.15)], 2); p.rect(x + w * 0.5, base - h * 0.5, x + w * 0.55, base - h * 0.47, (60, 60, 64), 1.6)

def bg_bedroom(c):
    p = Pen(c); wall(p, 720, (60, 66, 96)); floor_planks(p, 720, (80, 66, 60))
    p.rect(1240, 120, 1680, 500, (200, 200, 210), 4); p.vgrad(1250, 130, 1670, 490, (24, 30, 64), (50, 50, 90))
    for k in range(18): r = random.Random(k); p.ell(1260 + r.uniform(0, 400), 140 + r.uniform(0, 330), 2, 2, (255, 255, 230), 0)
    p.ell(1560, 220, 40, 40, (250, 246, 220), 2); p.line([(1460, 120), (1460, 500)], 6, (200, 200, 210)); p.line([(1240, 310), (1680, 310)], 6, (200, 200, 210))
    p.poly([(1200, 110), (1290, 110), (1270, 560), (1200, 560)], (90, 80, 130), 2.6); p.poly([(1720, 110), (1630, 110), (1650, 560), (1720, 560)], (90, 80, 130), 2.6)
    p.rect(180, 420, 260, 900, (120, 90, 70), 3)                                                              # Kopfteil
    p.rect(170, 400, 270, 430, (140, 106, 82), 3)
    p.rect(260, 700, 1100, 780, (120, 90, 70), 3); p.rect(1080, 640, 1120, 900, (120, 90, 70), 3)             # Bettrahmen + Fussteil
    for xx in (280, 1060): p.rect(xx, 780, xx + 22, 900, (100, 76, 60), 2.4)                                 # Bettbeine
    p.rect(262, 630, 1098, 710, (240, 240, 244), 3)                                                          # Matratze/Laken
    p.ell(380, 600, 110, 46, (250, 250, 252), 3)                                                              # Kissen
    p.poly([(520, 590), (1100, 610), (1110, 720), (480, 720)], (90, 120, 170), 3)                              # Decke
    for k in range(4): p.arc(640 + k * 120, 650, 50, 24, 200, 330, 2, (70, 100, 150))
    p.rect(-10, 560, 160, 900, (130, 96, 72), 3); p.rect(10, 640, 140, 700, (110, 80, 60), 2.4)                 # Nachttisch (links, angeschnitten)
    p.rect(40, 440, 110, 560, (220, 200, 160), 3); p.poly([(20, 380), (130, 380), (110, 440), (40, 440)], (240, 220, 170), 3)
    p.glow(75, 420, 120, (255, 210, 140), 80)
    p.poly([(300, 1000), (1200, 1000), (1300, 1080), (200, 1080)], (110, 70, 80), 2.4)                          # Teppich

def bg_vault(c, empty=True):
    p = Pen(c); p.vgrad(0, 0, W, H, (70, 74, 82), (40, 42, 48))
    p.ell(960, 540, 420, 420, (150, 156, 164), 5); p.ell(960, 540, 360, 360, (124, 130, 140), 4)
    for k in range(12): a = k * math.pi / 6; p.ell(960 + math.cos(a) * 390, 540 + math.sin(a) * 390, 16, 16, (90, 94, 102), 2.6)
    p.ell(960, 540, 110, 110, (170, 176, 184), 4)
    for k in range(3): a = k * 2.09; p.line([(960, 540), (960 + math.cos(a) * 170, 540 + math.sin(a) * 170)], 16, (90, 94, 102)); p.ell(960 + math.cos(a) * 170, 540 + math.sin(a) * 170, 22, 22, (170, 176, 184), 3)
    p.ell(960, 540, 30, 30, (60, 64, 70), 3)
    p.glow(960, 120, 300, (255, 240, 210), 50)

def bg_vault_inside(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (90, 94, 102), (50, 52, 58)); floor_tiles(p, 760, (110, 112, 118), (80, 82, 88))
    for k in range(3):
        y = 260 + k * 170; p.rect(300, y, 1620, y + 18, (150, 156, 164), 3)
        for x in (300, 1600): p.rect(x, y - 150, x + 20, y + 18, (130, 136, 144), 2.4)
    p.glow(960, 60, 300, (255, 240, 210), 60)
    r = random.Random(1)
    for _ in range(40): p.ell(r.uniform(320, 1600), r.uniform(200, 740), 2, 2, (200, 200, 200, 120), 0)    # Staub

def bg_loan_office(c):
    p = Pen(c); wall(p, 680, (214, 206, 190), wains=(150, 112, 80))
    frame_pic(p, 220, 140, 300, 220); frame_pic(p, 1400, 120, 360, 240, (180, 150, 110))
    p.rect(800, 120, 1120, 200, (30, 54, 92), 3); p.text("LOANS", 960, 160, 40, SERIF, (236, 214, 150))
    floor_planks(p, 680, (130, 96, 70))
    plant(p, 1760, 760, 1.0)

def bg_screen(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (40, 42, 50), (24, 26, 30))
    p.rect(220, 80, 1700, 900, (30, 32, 36), 5, r=20); p.vgrad(250, 110, 1670, 870, (244, 246, 250), (226, 232, 240))
    p.rect(250, 110, 1670, 190, (30, 54, 92), 0); p.text("FIRST NATIONAL  ·  Loan System", 300, 150, 34, SANS, (255, 255, 255), "lm")
    p.rect(860, 900, 1060, 980, (50, 52, 58), 3); p.rect(700, 980, 1220, 1010, (50, 52, 58), 3, r=6)

def bg_desk_paper(c):
    p = Pen(c); p.rect(0, 0, W, H, (120, 86, 58), 0)
    r = random.Random(9)
    for k in range(16): y = k * 70; p.line([(0, y), (W, y + r.uniform(-6, 6))], 1.8, (100, 70, 46))
    p.glow(960, 500, 600, (255, 230, 180), 60)

def bg_oval(c):
    p = Pen(c); p.vgrad(0, 0, W, 760, (236, 226, 196), (220, 206, 172))
    for x in (120, 1500):                                                                     # Vorhaenge gold
        p.poly([(x, 0), (x + 300, 0), (x + 260, 760), (x + 40, 760)], (196, 150, 60), 3)
        for k in range(5): p.line([(x + 40 + k * 50, 0), (x + 60 + k * 44, 760)], 2, (170, 126, 46))
    window(p, 520, 120, 820, 560, (200, 220, 230), (250, 248, 240), None); window(p, 1100, 120, 1400, 560, (200, 220, 230), (250, 248, 240), None)
    p.rect(880, 140, 1040, 300, (250, 248, 240), 3); p.ell(960, 220, 56, 56, (196, 160, 80), 3); p.text("★", 960, 222, 50, SANS, (250, 248, 240))
    for x, col in ((470, (190, 40, 50)), (1450, (40, 60, 120))):                              # Flaggen
        p.rect(x - 6, 200, x + 6, 760, (196, 160, 80), 2.4); p.poly([(x + 6, 220), (x + 150, 260), (x + 160, 480), (x + 6, 460)], col, 3)
    p.ell(960, 1010, 900, 160, (40, 60, 110), 3); p.ell(960, 1010, 520, 90, (196, 160, 80, 120), 2)   # ovaler Teppich
    p.rect(0, 760, W, 790, (150, 120, 80), 0)
    p.rect(560, 640, 1360, 690, (110, 70, 44), 3.4); p.rect(580, 690, 1340, 900, (96, 60, 38), 3.4)  # Resolute-artiger Tisch
    p.ell(960, 790, 90, 70, (130, 90, 56), 3); p.ell(960, 790, 54, 40, (196, 160, 80), 2.6)

def bg_studio(c, col=(226, 224, 218)):
    p = Pen(c); p.vgrad(0, 0, W, H, lt(col, 0.05), dk(col, 0.95)); p.rect(0, 880, W, H, dk(col, 0.92), 0); p.line([(0, 880), (W, 880)], 2, dk(col, 0.8))

def bg_fed(c):
    p = Pen(c); p.vgrad(0, 0, W, 700, (150, 196, 232), (220, 236, 246)); clouds(p, 120, 12, 4)
    p.rect(260, 220, 1660, 760, (240, 238, 230), 4)
    for k in range(4): y = 260 + k * 120; p.line([(262, y), (1658, y)], 1.4, (214, 210, 200))
    for x in range(330, 1640, 120): p.rect(x, 300, x + 60, 700, (200, 212, 222), 2.4)
    p.rect(760, 120, 1160, 230, (240, 238, 230), 4); p.text("FEDERAL RESERVE", 960, 176, 44, SERIF, INK)
    p.poly([(900, 260), (960, 230), (1020, 260), (990, 300), (930, 300)], (196, 160, 80), 2.6)
    p.rect(0, 760, W, H, (186, 182, 174), 0); [p.line([(x, 760), (x - 80, H)], 1.6, (166, 162, 156)) for x in range(0, W + 200, 140)]
    for x in (120, 1800): tree(p, x, 800, 1.0, x)

def bg_study1730(c):
    p = Pen(c); wall(p, 720, (120, 86, 60), wains=(90, 60, 40)); floor_planks(p, 720, (100, 70, 50))
    p.rect(1300, 120, 1680, 520, (60, 40, 30), 4); p.vgrad(1310, 130, 1670, 510, (40, 50, 90), (70, 60, 90))
    for k in range(6): p.rect(140 + k * 60, 160, 190 + k * 60, 520, [(120, 40, 40), (40, 70, 60), (90, 70, 40)][k % 3], 2.4)
    p.rect(120, 520, 560, 540, (80, 54, 36), 3); p.rect(120, 140, 560, 160, (80, 54, 36), 3)
    p.glow(1200, 600, 200, (255, 200, 120), 120)

def bg_supermarket(c):
    p = Pen(c); wall(p, 600, (236, 236, 232))
    for k in range(3):
        y = 120 + k * 150; p.rect(0, y + 110, W, y + 124, (170, 170, 176), 2.4)
        r = random.Random(k)
        for x in range(10, W, 46):
            col = r.choice([(220, 60, 50), (60, 140, 200), (250, 200, 60), (90, 170, 90), (240, 140, 60)]); hh = r.randint(60, 100)
            p.rect(x, y + 110 - hh, x + 38, y + 110, col, 2)
    p.rect(0, 540, W, 600, (60, 140, 90), 0); p.text("FRESH MARKET", 960, 570, 36, BOLD, (255, 255, 255))
    floor_tiles(p, 600, (236, 236, 236), (210, 210, 214))
    p.rect(200, 700, 1300, 760, (40, 42, 46), 3); p.rect(220, 760, 1280, 1000, (220, 222, 226), 3)        # Kassenband
    p.rect(1300, 560, 1520, 760, (60, 62, 70), 3); p.rect(1320, 580, 1500, 680, (40, 180, 120), 2.4)

def bg_boss(c):
    p = Pen(c); wall(p, 700, (196, 206, 214), wains=(120, 90, 70)); p.rect(1200, 100, 1760, 520, (90, 96, 106), 4); city_view(p, 1210, 110, 1750, 510, False, 6)
    frame_pic(p, 200, 160, 340, 240); floor_planks(p, 700, (120, 90, 64))

def bg_pinboard(c):
    p = Pen(c); p.rect(0, 0, W, H, (214, 206, 190), 0)
    p.rect(240, 100, 1680, 980, (150, 110, 70), 5); p.rect(270, 130, 1650, 950, (196, 156, 110), 3)
    r = random.Random(5)
    for _ in range(400): p.ell(r.uniform(280, 1640), r.uniform(140, 940), 2, 2, (170, 130, 90), 0)

def bg_ryan_apt(c):
    p = Pen(c); wall(p, 700, (232, 228, 220)); p.rect(1200, 120, 1700, 500, (250, 250, 248), 4); city_view(p, 1210, 130, 1690, 490, False, 21)
    floor_planks(p, 700, (196, 160, 120)); plant(p, 1780, 760, 1.0); frame_pic(p, 240, 160, 300, 200, (200, 160, 120))
    p.rect(700, 140, 1000, 160, (150, 110, 80), 2.4); [p.rect(720 + k * 30, 80, 744 + k * 30, 140, [(200, 60, 50), (60, 120, 170), (240, 190, 60)][k % 3], 2) for k in range(8)]

def bg_kitchen_night(c):
    p = Pen(c); wall(p, 720, (120, 110, 96)); floor_planks(p, 720, (90, 70, 56))
    p.rect(1200, 140, 1600, 480, (110, 104, 96), 4); p.vgrad(1210, 150, 1590, 470, (24, 28, 56), (40, 40, 70))
    p.rect(100, 380, 700, 720, (160, 150, 136), 3); p.rect(100, 360, 700, 390, (190, 180, 166), 3); p.rect(140, 200, 660, 330, (170, 160, 146), 3)
    p.line([(960, 0), (960, 220)], 2.4); p.poly([(890, 220), (1030, 220), (1000, 280), (920, 280)], (240, 220, 170), 3); p.glow(960, 420, 330, (255, 210, 140), 110)

def bg_apt_building(c):
    p = Pen(c); p.vgrad(0, 0, W, 700, (160, 190, 220), (220, 230, 240))
    p.rect(200, 0, 1720, 860, (170, 100, 80), 4)
    for yy in range(10, 860, 30):
        for xx in range(210 + (yy // 30 % 2) * 30, 1710, 60): p.rect(xx, yy, xx + 56, yy + 26, (180, 108, 86), 1)
    for x in (300, 700, 1220, 1520):
        for y in (60, 380): window(p, x, y, x + 200, y + 200, (170, 200, 220), (240, 236, 226))
    p.rect(860, 520, 1060, 860, (60, 50, 44), 3.4); p.rect(820, 480, 1100, 520, (90, 80, 70), 3)
    p.rect(0, 860, W, H, (196, 192, 184), 0)
    for k in range(4):                                                                        # Briefkaesten an der Wand
        x = 1200 + k * 100; p.rect(x, 640, x + 86, 780, (150, 156, 166), 3); p.rect(x + 10, 660, x + 76, 680, (60, 64, 70), 1.6)

def bg_glass_office(c):
    p = Pen(c); city_view(p, 0, 0, W, 760, False, 31)
    for x in range(0, W, 480): p.line([(x, 0), (x, 760)], 10, (60, 64, 70))
    p.rect(0, 0, W, 760, (200, 224, 238, 50), 0)
    floor_tiles(p, 760, (60, 62, 68), (40, 42, 46)); p.glow(1600, 200, 300, (255, 240, 210), 60)

def bg_private_bank(c):
    p = Pen(c); wall(p, 700, (60, 40, 36), wains=(40, 26, 22)); frame_pic(p, 760, 120, 400, 280, (150, 120, 80))
    p.glow(960, 300, 400, (255, 210, 150), 70); floor_planks(p, 700, (70, 44, 30))

def bg_wallstreet(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (120, 130, 150), (170, 176, 190))
    p.rect(300, 120, 1620, 900, (226, 222, 212), 4)
    for x in range(380, 1600, 200): p.rect(x - 40, 300, x + 40, 900, (240, 238, 230), 3); p.rect(x - 56, 280, x + 56, 310, (236, 232, 222), 2.6)
    p.poly([(260, 300), (960, 120), (1660, 300)], (230, 226, 216), 4); p.rect(260, 290, 1660, 310, (220, 216, 206), 3)
    for x in range(420, 1520, 260):
        p.rect(x, 600, x + 180, 720, (30, 30, 34), 3); [p.line([(x + 10, 620 + k * 20), (x + 60, 640 + k * 20), (x + 120, 660 + k * 22), (x + 170, 700)], 3, (230, 50, 50)) for k in range(2)]
    p.rect(0, 900, W, H, (150, 150, 156), 0)

def bg_svb(c):
    p = Pen(c); p.vgrad(0, 0, W, 700, (200, 210, 220), (230, 236, 240)); p.rect(400, 80, 1520, 800, (230, 232, 236), 4)
    for x in range(440, 1500, 160): p.rect(x, 180, x + 120, 700, (150, 180, 200), 2.4)
    p.rect(760, 120, 1160, 170, (30, 54, 120), 3); p.text("SILICON VALLEY BANK", 960, 145, 26, SANS, (255, 255, 255))
    p.rect(0, 800, W, H, (190, 190, 186), 0)

def bg_fedroom(c):
    p = Pen(c); wall(p, 700, (90, 70, 60), wains=(60, 46, 40)); p.rect(760, 100, 1160, 380, (196, 160, 80), 4); p.ell(960, 240, 100, 100, (240, 230, 200), 3); p.text("FED", 960, 240, 50, SERIF, INK)
    p.ell(960, 900, 820, 160, (110, 76, 50), 4); p.ell(960, 890, 760, 130, (130, 90, 60), 2)
    floor_planks(p, 700, (80, 56, 40))

def bg_ledger(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (10, 14, 26), (20, 24, 40))
