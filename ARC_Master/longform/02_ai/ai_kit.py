"""ARC #02 KI-Kit: gleicher HQ-Cartoon-Stil wie #01 (hq.py), plus KI-Figur, Roboter, Roboterhund, Drohnen,
Bildschirme (Chat, Code, Mail, Videocall, Ueberweisung), dunkle Orte. Alles 1x-Koordinaten, 2x gezeichnet."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../01_money"))
from hq import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ======================= FIGUREN (Karikaturen + Story) =======================
LEO = P(hair=(52, 40, 34), top=(70, 140, 96), pants=(60, 64, 80), shoes=(40, 40, 44), skin=(236, 200, 166), style="short", glasses=True)
CFO = P(hair=(176, 176, 180), top=(250, 250, 248), jacket=(58, 62, 74), pants=(58, 62, 74), shoes=(30, 28, 28), tie=(140, 40, 50), skin=(236, 200, 170), style="side", age=55)
COLL = [P(hair=(30, 26, 24), top=(250, 250, 248), jacket=(40, 60, 96), pants=(40, 60, 96), tie=(120, 40, 40), skin=(226, 186, 150), style="short"),
        P(hair=(90, 58, 40), top=(190, 120, 120), skin=(240, 206, 176), style="bun"),
        P(hair=(20, 18, 18), top=(120, 150, 190), skin=(206, 160, 120), style="side", glasses=True),
        P(hair=(150, 110, 70), top=(90, 100, 110), skin=(242, 210, 182), style="bun")]
SCI = P(hair=(90, 60, 40), top=(246, 246, 248), jacket=(246, 246, 248), pants=(70, 76, 90), shoes=(40, 40, 44), skin=(240, 206, 176), style="bun", glasses=True)
ENG = P(hair=(36, 30, 28), top=(120, 150, 190), pants=(60, 64, 80), skin=(206, 160, 120), style="short")
FREEL = P(hair=(180, 120, 60), top=(230, 150, 60), pants=(70, 80, 110), skin=(236, 196, 156), style="bun")
ALTMAN = P(hair=(122, 92, 66), top=(128, 132, 140), hood=True, pants=(46, 50, 60), shoes=(240, 240, 236), skin=(238, 204, 176), style="short", age=40)
HINTON = P(hair=(236, 236, 232), top=(176, 156, 126), pants=(80, 80, 90), skin=(240, 210, 186), style="side", glasses=True, age=76)
LECUN = P(hair=(110, 110, 114), top=(70, 100, 150), jacket=(30, 32, 40), pants=(30, 32, 40), skin=(230, 196, 166), style="side", glasses=True, age=64)
ZUCK = P(hair=(128, 94, 62), top=(140, 144, 150), collar=False, pants=(50, 54, 64), skin=(244, 212, 186), style="short", age=40)
AMODEI = P(hair=(40, 32, 28), top=(70, 110, 170), pants=(50, 54, 64), skin=(232, 200, 170), style="messy", glasses=True, age=42)
HUANG = P(hair=(56, 56, 60), top=(28, 28, 32), jacket=(22, 22, 26), pants=(28, 28, 32), shoes=(20, 20, 20), skin=(232, 196, 160), style="side", age=62)
HASSABIS = P(hair=(54, 46, 42), top=(250, 250, 248), jacket=(70, 74, 86), pants=(70, 74, 86), skin=(214, 172, 134), style="buzz", age=48)
KID = P(hair=(120, 84, 52), top=(240, 180, 60), pants=(62, 82, 124), skin=(244, 210, 178), style="messy", age=10, big=0.85)
PEOPLE = [P(hair=h, top=t, pants=pa, skin=sk, style=st) for h, t, pa, sk, st in [
    ((60, 44, 36), (110, 130, 170), (60, 60, 70), (236, 196, 160), "short"), ((30, 26, 24), (180, 120, 100), (50, 50, 60), (170, 120, 86), "buzz"),
    ((200, 160, 90), (120, 160, 120), (80, 70, 60), (242, 208, 178), "bun"), ((90, 60, 40), (170, 150, 110), (60, 70, 90), (220, 176, 136), "messy"),
    ((40, 34, 30), (130, 110, 160), (50, 50, 56), (176, 126, 92), "side")]]

RED = (230, 52, 60); CYAN = (90, 210, 255); YEL = (255, 214, 60); WHITE = (255, 255, 255)

# ======================= KI-FIGUR (Bildschirm-Kopf) =======================
def ai_face(c, cx, cy, s=1.0, mood="friendly", look=0.0):
    """mood: friendly (blau, Laecheln), cold (rot, Strich), mask (weisse leere Maske), think (Augen oben)."""
    p = Pen(c); w, h = 300 * s, 230 * s
    glow = {"friendly": CYAN, "cold": RED, "mask": (230, 230, 240), "think": CYAN}[mood]
    p.glow(cx, cy, 260 * s, glow, 70)
    p.rect(cx - w / 2 - 14 * s, cy - h / 2 - 14 * s, cx + w / 2 + 14 * s, cy + h / 2 + 14 * s, (210, 214, 224), 4, r=46 * s)
    p.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, (18, 22, 34), 3, r=36 * s)
    p.rect(cx - 30 * s, cy + h / 2 + 14 * s, cx + 30 * s, cy + h / 2 + 40 * s, (180, 184, 196), 3)
    p.rect(cx - 90 * s, cy + h / 2 + 38 * s, cx + 90 * s, cy + h / 2 + 54 * s, (180, 184, 196), 3, r=8)
    ex = 62 * s; ey = cy - 18 * s; lx = look * 18 * s
    if mood == "mask":
        p.ell(cx, cy, 95 * s, 112 * s, (244, 244, 248), 3); p.ell(cx - 34 * s, cy - 20 * s, 14 * s, 8 * s, (18, 22, 34), 0); p.ell(cx + 34 * s, cy - 20 * s, 14 * s, 8 * s, (18, 22, 34), 0)
        return
    col = glow
    for sx in (-1, 1):
        if mood == "cold": p.rect(cx + sx * ex - 30 * s + lx, ey - 7 * s, cx + sx * ex + 30 * s + lx, ey + 7 * s, col, 0, r=6 * s)
        else: p.rect(cx + sx * ex - 20 * s + lx, ey - (34 if mood == "friendly" else 26) * s - (12 * s if mood == "think" else 0), cx + sx * ex + 20 * s + lx, ey + 30 * s - (12 * s if mood == "think" else 0), col, 0, r=18 * s)
    if mood == "friendly": p.arc(cx + lx, cy + 30 * s, 54 * s, 34 * s, 20, 160, 7 * s / 2, col)
    elif mood == "cold": p.line([(cx - 44 * s, cy + 52 * s), (cx + 44 * s, cy + 52 * s)], 6 * s / 2, col)
    else: p.line([(cx - 30 * s, cy + 50 * s), (cx + 30 * s, cy + 46 * s)], 6 * s / 2, col)

# ======================= ROBOTER =======================
def robot(c, cx, base, R=50, arms=("down", "down"), eye=CYAN, body=(232, 234, 240), dark=(64, 70, 84), phase=None, hold=None, face=1):
    """Humanoider Roboter im Cartoon-Stil, Fusslinie base, Kopfgroesse R."""
    p = Pen(c); leg = R * 1.7; hip = base - leg; tor = R * 1.75; top = hip - tor; hcy = top - R * 0.95
    p.shadow(cx, base + 4, R * 1.1, R * 0.16, 60)
    for sx in (-1, 1):
        x = cx + sx * R * 0.34
        if phase is not None:
            ph = 2 * math.pi * (phase + (0.5 if sx > 0 else 0)); fx = x + math.sin(ph) * R * 0.5; lift = max(0, math.cos(ph)) * R * 0.15
        else: fx, lift = x, 0
        kx = (x + fx) / 2; ky = hip + leg * 0.5 - lift * 0.5
        p.line([(x, hip), (kx, ky)], R * 0.34 + 4.5, INK); p.line([(x, hip), (kx, ky)], R * 0.34, dark)
        p.line([(kx, ky), (fx, base - R * 0.12 - lift)], R * 0.3 + 4.5, INK); p.line([(kx, ky), (fx, base - R * 0.12 - lift)], R * 0.3, body)
        p.ell(kx, ky, R * 0.2, R * 0.2, dark, 2.6)
        p.rect(fx - R * 0.3, base - R * 0.22 - lift, fx + R * 0.36 * face, base - lift, dark, 2.6, r=R * 0.08)
    def arm(sx, kind):
        sh = (cx + sx * R * 0.95, top + R * 0.3)
        if kind == "up": el = (sh[0] + sx * R * 0.35, sh[1] - R * 0.7); hd = (sh[0] + sx * R * 0.25, sh[1] - R * 1.5)
        elif kind == "hold": el = (sh[0] + sx * R * 0.2, sh[1] + R * 0.8); hd = (sh[0] + face * R * 0.9, sh[1] + R * 0.9)
        elif kind == "reach": el = (sh[0] + face * R * 0.6, sh[1] + R * 0.3); hd = (sh[0] + face * R * 1.5, sh[1] + R * 0.35)
        elif kind == "block": el = (sh[0] + sx * R * 0.6, sh[1] + R * 0.2); hd = (sh[0] + sx * R * 1.2, sh[1] + R * 0.1)
        else: el = (sh[0] + sx * R * 0.12, sh[1] + R * 0.85); hd = (sh[0] + sx * R * 0.14, sh[1] + R * 1.65)
        p.line([sh, el], R * 0.28 + 4.5, INK); p.line([sh, el], R * 0.28, dark)
        p.line([el, hd], R * 0.26 + 4.5, INK); p.line([el, hd], R * 0.26, body)
        p.ell(el[0], el[1], R * 0.16, R * 0.16, dark, 2.4); p.ell(hd[0], hd[1], R * 0.2, R * 0.18, dark, 2.6)
        return hd
    hands = [arm(-1, arms[0])]
    p.rect(cx - R * 1.0, top, cx + R * 1.0, hip + R * 0.15, body, 3.4, r=R * 0.35)
    p.rect(cx - R * 0.62, top + R * 0.3, cx + R * 0.62, top + R * 1.05, (210, 214, 224), 2.4, r=R * 0.2)
    p.ell(cx, top + R * 0.68, R * 0.16, R * 0.16, eye, 2.2); p.glow(cx, top + R * 0.68, R * 0.3, eye, 70)
    p.rect(cx - R * 0.8, hip - R * 0.1, cx + R * 0.8, hip + R * 0.15, dark, 2.4, r=R * 0.08)
    hands.append(arm(1, arms[1]))
    p.rect(cx - R * 0.22, top - R * 0.3, cx + R * 0.22, top + 4, dark, 2.4)
    p.rect(cx - R * 0.85, hcy - R * 0.78, cx + R * 0.85, hcy + R * 0.7, body, 3.4, r=R * 0.45)
    p.rect(cx - R * 0.66 + face * R * 0.06, hcy - R * 0.42, cx + R * 0.66 + face * R * 0.06, hcy + R * 0.34, (22, 26, 38), 2.4, r=R * 0.28)
    for sx in (-1, 1): p.ell(cx + face * R * 0.08 + sx * R * 0.28, hcy - R * 0.04, R * 0.12, R * 0.15, eye, 0)
    p.glow(cx, hcy, R * 0.7, eye, 50)
    p.ell(cx - R * 0.9, hcy, R * 0.12, R * 0.22, dark, 2.4); p.ell(cx + R * 0.9, hcy, R * 0.12, R * 0.22, dark, 2.4)
    if hold: hold(c, hands[-1])
    return dict(head=(cx, hcy), hands=hands)

def robot_dog(c, cx, base, s=1.0, phase=0.0, rifle=True):
    p = Pen(c); col = (92, 98, 92); dk_ = (50, 54, 50); bw, bh = 300 * s, 90 * s; by = base - 190 * s
    p.shadow(cx, base + 4, 200 * s, 22 * s, 60)
    for k, lx in enumerate((-110, -60, 70, 120)):
        ph = 2 * math.pi * (phase + (0.5 if k % 2 else 0)); dx = math.sin(ph) * 22 * s; lift = max(0, math.cos(ph)) * 14 * s
        x = cx + lx * s; kx = x + 26 * s + dx * 0.5; ky = by + bh * 0.5 + 60 * s
        p.line([(x, by + bh * 0.4), (kx, ky)], 22 * s, INK); p.line([(x, by + bh * 0.4), (kx, ky)], 16 * s, dk_)
        p.line([(kx, ky), (x + dx, base - lift)], 18 * s, INK); p.line([(kx, ky), (x + dx, base - lift)], 12 * s, col)
        p.ell(kx, ky, 12 * s, 12 * s, dk_, 2.4); p.ell(x + dx, base - lift, 11 * s, 8 * s, INK, 0)
    p.rect(cx - bw / 2, by, cx + bw / 2, by + bh, col, 3.4, r=30 * s)
    p.rect(cx - bw / 2 + 30 * s, by + 18 * s, cx + bw / 2 - 30 * s, by + 36 * s, dk_, 0, r=8 * s)
    p.rect(cx + bw / 2 - 10 * s, by - 10 * s, cx + bw / 2 + 80 * s, by + 50 * s, dk_, 3, r=16 * s)
    p.ell(cx + bw / 2 + 56 * s, by + 18 * s, 9 * s, 9 * s, RED, 0); p.glow(cx + bw / 2 + 56 * s, by + 18 * s, 22 * s, RED, 90)
    if rifle:
        p.rect(cx - 70 * s, by - 46 * s, cx + 40 * s, by - 6 * s, (40, 40, 42), 3, r=6 * s)
        p.rect(cx + 30 * s, by - 38 * s, cx + 210 * s, by - 24 * s, (30, 30, 32), 3)
        p.rect(cx - 20 * s, by - 6 * s, cx + 10 * s, by + 4 * s, (40, 40, 42), 2)

def drone(c, cx, cy, s=1.0, eye=RED):
    p = Pen(c)
    for sx in (-1, 1):
        p.line([(cx, cy), (cx + sx * 70 * s, cy - 16 * s)], 9 * s, INK); p.ell(cx + sx * 76 * s, cy - 22 * s, 46 * s, 8 * s, (90, 96, 106, 160), 2)
    p.ell(cx, cy, 40 * s, 22 * s, (70, 76, 88), 3); p.ell(cx, cy + 10 * s, 10 * s, 10 * s, eye, 0); p.glow(cx, cy + 10 * s, 26 * s, eye, 90)

# ======================= BILDSCHIRM-BAUSTEINE (statisch, 2x) =======================
def window(c, x0, y0, x1, y1, title="", bar=(36, 40, 52), body=(248, 249, 252), dark=False):
    p = Pen(c); p.shadow((x0 + x1) / 2, y1 + 6, (x1 - x0) * 0.48, 18, 70)
    p.rect(x0, y0, x1, y1, (24, 26, 34) if dark else body, 4, r=18)
    p.rect(x0, y0, x1, y0 + 52, bar, 0, r=18); p.rect(x0, y0 + 30, x1, y0 + 52, bar, 0)
    for k, col in enumerate(((240, 90, 80), (240, 190, 70), (100, 200, 110))): p.ell(x0 + 30 + k * 30, y0 + 26, 9, 9, col, 0)
    p.text(title, (x0 + x1) / 2, y0 + 27, 24, SANS, (230, 232, 240))

def bust_img(pr, R, mouth="line", eyes="open", face=0, brow=0.0):
    """Kopf + Schultern einer Figur als Bild (fuer Videocall-Kacheln)."""
    def fn(c):
        figure(c, 960, 900, R, pr, face, mouth, brow, ("down", "down"), "stand", 0.0, eyes)
    im, x, y = sprite(("bust", id(pr), R, mouth, eyes, face, brow), fn)
    hy = 900 - 3.92 * R; top = int(hy - 1.25 * R - y); bot = int(hy + 2.3 * R - y)
    return im.crop((0, max(0, top), im.width, min(im.height, bot)))

# ======================= HINTERGRUENDE (gecacht) =======================
_bgc = {}
def abg(name, *a):
    k = (name,) + a
    if k not in _bgc:
        c = canvas((255, 255, 255, 255)); globals()["bg_" + name](c, *a); _bgc[k] = finish(c).convert("RGBA")
    return _bgc[k]

def skyline(p, y1, seed=3, night=True, hk=False):
    r = random.Random(seed); x = -20
    while x < W + 20:
        bw = r.randint(70, 150); bh = r.randint(260, 640 if hk else 480)
        col = (34, 40, 66) if night else (150, 166, 190)
        p.rect(x, y1 - bh, x + bw, y1, col, 0)
        if hk and r.random() < 0.3: p.poly([(x, y1 - bh), (x + bw / 2, y1 - bh - 60), (x + bw, y1 - bh)], col, 0)
        for wy in range(int(y1 - bh + 14), int(y1 - 10), 24):
            for wx in range(int(x + 10), int(x + bw - 12), 20):
                if r.random() < (0.42 if night else 0.8): p.rect(wx, wy, wx + 9, wy + 11, (255, 214, 140) if night and r.random() < 0.8 else (140, 200, 255), 0)
        x += bw + r.randint(6, 20)

def bg_night_city(c, hk=False):
    p = Pen(c); p.vgrad(0, 0, W, H, (14, 18, 40), (60, 40, 80)); p.glow(1500, 200, 120, (240, 236, 220), 60)
    skyline(p, 980, 7, True, hk); p.vgrad(0, 960, W, H, (20, 22, 34), (10, 12, 20))
    if hk:
        p.vgrad(0, 980, W, H, (16, 30, 60), (8, 14, 30))
        for k in range(30): x = random.Random(k).randint(0, W); p.line([(x, 1000 + k % 5 * 14), (x + 60, 1000 + k % 5 * 14)], 2, (255, 214, 140))

def bg_office_night(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (40, 44, 60), (30, 32, 44))
    p.rect(120, 60, 1800, 640, (24, 28, 44), 6); p.vgrad(130, 70, 1790, 630, (14, 18, 40), (50, 36, 70)); skyline(p, 630, 11, True, True)
    for x in (680, 1240): p.line([(x, 60), (x, 640)], 10, (60, 64, 80))
    p.rect(0, 640, W, 690, (70, 74, 90), 0); p.vgrad(0, 690, W, H, (56, 58, 70), (36, 38, 48))
    p.glow(960, 760, 420, (140, 190, 255), 50)

def bg_desk_close(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (24, 26, 36), (14, 16, 22)); p.rect(0, 860, W, H, (90, 66, 48), 0)
    p.rect(260, 70, 1660, 860, (30, 32, 38), 6, r=22); p.rect(860, 860, 1060, 940, (40, 42, 48), 3); p.rect(700, 936, 1220, 970, (40, 42, 48), 3, r=8)

def bg_lab(c, dark=False):
    p = Pen(c); base = (214, 222, 230) if not dark else (40, 46, 58)
    p.vgrad(0, 0, W, 720, base, mix(base, (255, 255, 255), 0.2) if not dark else (28, 32, 42))
    for x in range(0, W, 320): p.rect(x, 80, x + 300, 560, (180, 200, 214) if not dark else (30, 36, 48), 3); p.line([(x + 150, 80), (x + 150, 560)], 2, (160, 180, 196) if not dark else (50, 56, 70))
    p.rect(0, 700, W, H, (200, 204, 210) if not dark else (36, 38, 46), 0)
    for x in range(0, W, 160): p.line([(x, 700), (x - 120, H)], 1.6, (180, 184, 190) if not dark else (50, 52, 60))
    p.rect(600, 120, 1320, 520, (20, 24, 34), 6, r=18)
    if dark: p.glow(960, 320, 500, RED, 40)

def bg_server(c, glow=CYAN):
    p = Pen(c); p.vgrad(0, 0, W, H, (10, 14, 24), (18, 22, 36)); r = random.Random(4)
    for k, x in enumerate(range(-40, W + 40, 230)):
        p.rect(x, 120, x + 190, 960, (28, 32, 46), 3, r=8)
        for y in range(150, 940, 34):
            p.rect(x + 16, y, x + 174, y + 24, (40, 46, 62), 1.6, r=4)
            for j in range(3):
                if r.random() < 0.7: p.ell(x + 140 + j * 10, y + 12, 3, 3, glow if r.random() < 0.8 else (90, 255, 120), 0)
    p.rect(0, 960, W, H, (20, 24, 34), 0); p.glow(960, 980, 700, glow, 40)

def bg_control(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (8, 10, 18), (16, 18, 30))
    r = random.Random(8)
    for row in range(3):
        for col in range(6):
            x = 90 + col * 300; y = 80 + row * 210
            p.rect(x, y, x + 270, y + 180, (14, 18, 30), 3, r=8)
            for k in range(6): p.line([(x + 14, y + 26 + k * 24), (x + 14 + r.randint(80, 240), y + 26 + k * 24)], 3, (200, 50, 60) if r.random() < 0.4 else (60, 200, 120))
    p.rect(0, 760, W, H, (22, 24, 34), 0); p.rect(200, 760, 1720, 800, (40, 42, 56), 3)

def bg_world(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (8, 14, 30), (14, 22, 44))
    for x in range(0, W, 80): p.line([(x, 0), (x, H)], 1, (24, 36, 64))
    for y in range(0, H, 80): p.line([(0, y), (W, y)], 1, (24, 36, 64))
    land = (40, 64, 104)
    p.poly([(260, 260), (520, 210), (700, 300), (640, 470), (520, 560), (430, 520), (300, 420)], land, 2.4, (70, 100, 150))   # N-Amerika
    p.poly([(560, 600), (680, 620), (700, 820), (620, 940), (560, 820)], land, 2.4, (70, 100, 150))                            # S-Amerika
    p.poly([(900, 260), (1080, 230), (1100, 360), (980, 420), (900, 380)], land, 2.4, (70, 100, 150))                          # Europa
    p.poly([(960, 440), (1120, 440), (1180, 640), (1060, 820), (980, 660)], land, 2.4, (70, 100, 150))                         # Afrika
    p.poly([(1100, 220), (1500, 200), (1700, 320), (1600, 520), (1400, 560), (1200, 440)], land, 2.4, (70, 100, 150))          # Asien
    p.poly([(1560, 700), (1720, 690), (1760, 820), (1600, 840)], land, 2.4, (70, 100, 150))                                   # Australien

def bg_stage(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (120, 16, 22), (40, 6, 10))
    for x in range(0, W, 120): p.poly([(x, 0), (x + 60, 0), (x + 30, 760)], (200, 40, 40, 60), 0)
    p.glow(960, 120, 300, (255, 220, 120), 90); p.rect(0, 800, W, H, (60, 20, 20), 0); p.ell(960, 820, 900, 90, (200, 160, 60), 4)

def bg_hospital(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (220, 232, 236), (200, 214, 220)); p.rect(0, 800, W, H, (180, 196, 204), 0)
    p.rect(1060, 130, 1760, 640, (20, 26, 34), 6, r=14)

def bg_street2040(c, mood="day"):
    p = Pen(c); day = mood == "day"
    p.vgrad(0, 0, W, 760, (120, 180, 230) if day else (30, 30, 60), (230, 220, 240) if day else (90, 50, 80))
    r = random.Random(12); x = -20
    while x < W:
        bw = r.randint(120, 220); bh = r.randint(300, 640); col = (210, 222, 236) if day else (40, 44, 70)
        p.rect(x, 760 - bh, x + bw, 760, col, 3 if day else 0, r=30); p.rect(x + 20, 760 - bh + 30, x + bw - 20, 760 - bh + 60, (120, 210, 230) if day else (255, 90, 120), 0, r=10)
        for wy in range(760 - bh + 90, 740, 46): p.rect(x + 20, wy, x + bw - 20, wy + 22, (170, 214, 236) if day else (255, 214, 140), 0, r=6)
        x += bw + r.randint(20, 50)
    p.rect(0, 760, W, 820, (190, 196, 204), 2); p.vgrad(0, 820, W, H, (70, 74, 84), (50, 52, 60))
    for xx in range(40, W, 260): p.rect(xx, 940, xx + 140, 952, (130, 230, 255), 0)

def bg_kitchen2040(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (236, 240, 244), (220, 226, 232)); p.rect(0, 620, W, H, (200, 206, 214), 0)
    p.rect(0, 600, W, 640, (250, 252, 254), 3); p.rect(0, 640, W, 900, (226, 232, 238), 3)
    for x in range(60, W, 300): p.rect(x, 660, x + 260, 880, (236, 240, 246), 2, r=10)
    p.rect(1300, 120, 1800, 480, (150, 200, 230), 5, r=20); p.vgrad(1310, 130, 1790, 470, (150, 200, 236), (230, 220, 240))
    p.glow(1550, 300, 300, (255, 255, 230), 70)

def bg_dark(c, col=(20, 22, 34), glow=None):
    p = Pen(c); p.vgrad(0, 0, W, H, mix(col, (0, 0, 0), 0.3), col)
    if glow: p.glow(960, 540, 600, glow, 50)

def bg_wall(c):
    p = Pen(c); p.vgrad(0, 0, W, H, (6, 6, 12), (20, 10, 16)); p.glow(960, 540, 620, RED, 45)
    for y in range(0, H, 6): p.line([(0, y), (W, y)], 1, (255, 255, 255, 6))

# ======================= DYNAMIK IM FRAME (1x, direkt) =======================
_fonts = {}
def fnt(path, size):
    k = (path, int(size))
    if k not in _fonts: _fonts[k] = ImageFont.truetype(path, max(6, int(size)))
    return _fonts[k]
def txt(f, s, x, y, size, font=SANS, fill=INK, anchor="mm", a=1.0):
    if a <= 0: return
    d = ImageDraw.Draw(f, "RGBA"); d.text((x, y), s, font=fnt(font, size), fill=tuple(fill[:3]) + (int(255 * min(1, a)),), anchor=anchor)
def rr(f, box, fill, outline=None, w=0, r=0):
    d = ImageDraw.Draw(f, "RGBA"); d.rounded_rectangle(box, r, fill=fill, outline=outline, width=w)
def typed(s, k): return s[:max(0, int(len(s) * max(0.0, min(1.0, k))))]

def glitch(f, amount=0.5, seed=0):
    """Horizontale Versatz-Streifen + RGB-Versatz (fuer Deepfake/Boom-Momente)."""
    r = random.Random(seed); im = f.copy()
    for _ in range(int(14 * amount)):
        y = r.randint(0, H - 40); h = r.randint(6, 40); dx = r.randint(-60, 60)
        band = im.crop((0, y, W, y + h)); f.paste(band, (dx, y))
    if amount > 0.3:
        rch = f.getchannel("R"); f.paste(Image.merge("RGBA", (rch.transform(f.size, Image.AFFINE, (1, 0, -8, 0, 1, 0)), f.getchannel("G"), f.getchannel("B"), f.getchannel("A"))))

def fade_black(f, a):
    if a <= 0: return
    f.alpha_composite(Image.new("RGBA", f.size, (0, 0, 0, int(255 * min(1, a)))))
