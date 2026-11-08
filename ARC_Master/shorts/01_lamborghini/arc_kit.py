"""ARC-Figuren- und Szenen-Kit (2D, flach, Business-Figuren). Zeichnet mit 2x Supersampling."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SS = 2                      # Supersampling
W, H = 1080, 1920
F = "C:/Windows/Fonts/"
NAVY_T, NAVY_B = (12, 20, 38), (22, 34, 60)
GOLD, WHITE, INK = (212, 175, 95), (240, 236, 226), (18, 18, 24)
FLOOR = (30, 44, 74)

def font(name, size):
    return ImageFont.truetype(F + name, int(size * SS))

def canvas(top=NAVY_T, bot=NAVY_B, floor_y=1450):
    img = Image.new("RGB", (W * SS, H * SS))
    d = ImageDraw.Draw(img)
    for y in range(H * SS):
        t = y / (H * SS)
        d.line([(0, y), (W * SS, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    if floor_y:
        d.rectangle([0, floor_y * SS, W * SS, H * SS], fill=FLOOR)
        d.line([(0, floor_y * SS), (W * SS, floor_y * SS)], fill=(44, 62, 98), width=4 * SS)
    return img

def S(*v):
    return [x * SS for x in v]

# ---------------- Figuren ----------------
FERRUCCIO = dict(skin=(232, 190, 150), hair=(40, 30, 24), style="slick", mustache=True, glasses=False,
                 suit=(110, 78, 52), tie=(170, 40, 40), shirt=WHITE)
ENZO = dict(skin=(226, 186, 150), hair=(225, 225, 225), style="swept", mustache=False, glasses=True,
            suit=(30, 30, 36), tie=(140, 20, 20), shirt=WHITE)
MECHANIC = dict(skin=(214, 170, 130), hair=(60, 40, 30), style="cap", mustache=False, glasses=False,
                suit=(52, 82, 140), tie=None, shirt=(52, 82, 140))

def person(img, cx, base, h, p, expr="neutral", pose="down", face=1, talk=False):
    """cx/base = Fusspunkt-Mitte, h = Gesamthoehe in px, face=1 schaut rechts, -1 links."""
    d = ImageDraw.Draw(img)
    u = h / 10.0
    hr = 2.0 * u                       # Kopfradius (grosser Kopf, Crayon-artig)
    hy = base - h + hr                 # Kopfmitte
    body_top = hy + hr * 0.85
    body_bot = base - 2.2 * u
    bw = 2.6 * u
    # Beine
    for sx in (-0.55, 0.55):
        d.rounded_rectangle(S(cx + sx * u - 0.45 * u, body_bot - 0.3 * u, cx + sx * u + 0.45 * u, base - 0.25 * u),
                            radius=0.3 * u * SS, fill=tuple(max(0, c - 25) for c in p["suit"]))
        d.ellipse(S(cx + sx * u - 0.7 * u + face * 0.2 * u, base - 0.55 * u, cx + sx * u + 0.7 * u + face * 0.2 * u, base + 0.05 * u), fill=INK)
    # Koerper
    d.rounded_rectangle(S(cx - bw / 2, body_top, cx + bw / 2, body_bot), radius=1.0 * u * SS, fill=p["suit"])
    if p["tie"]:
        d.polygon(S(cx - 0.55 * u, body_top + 0.05 * u, cx + 0.55 * u, body_top + 0.05 * u, cx, body_top + 1.6 * u), fill=p["shirt"])
        d.polygon(S(cx - 0.18 * u, body_top + 0.2 * u, cx + 0.18 * u, body_top + 0.2 * u, cx + 0.25 * u, body_top + 1.5 * u,
                    cx, body_top + 1.8 * u, cx - 0.25 * u, body_top + 1.5 * u), fill=p["tie"])
    # Arme
    sh_y = body_top + 0.7 * u
    def arm(sx, angle_deg, length=2.6 * u):
        x0 = cx + sx * (bw / 2 - 0.25 * u)
        a = math.radians(angle_deg)
        x1, y1 = x0 + math.sin(a) * length * sx, sh_y + math.cos(a) * length
        d.line(S(x0, sh_y, x1, y1), fill=p["suit"], width=int(0.75 * u * SS))
        d.ellipse(S(x1 - 0.42 * u, y1 - 0.42 * u, x1 + 0.42 * u, y1 + 0.42 * u), fill=p["skin"])
        return x1, y1
    poses = {"down": (12, 12), "point": (12, 115), "proud": (35, 35), "raise": (150, 150),
             "hold": (12, 70), "angry": (40, 40), "cross": (55, 55)}
    la, ra = poses[pose]
    arm(-1, la); hand = arm(1, ra) if face == 1 else arm(1, la)
    if face == -1:
        arm(-1, ra)
    # Kopf
    d.ellipse(S(cx - hr, hy - hr, cx + hr, hy + hr), fill=p["skin"])
    d.ellipse(S(cx - hr * 1.02 - 0.2 * u * face, hy - 0.2 * u, cx - hr * 0.78 - 0.2 * u * face, hy + 0.5 * u), fill=p["skin"])
    # Haare
    hc = p["hair"]
    if p["style"] == "slick":
        d.chord(S(cx - hr * 1.02, hy - hr * 1.08, cx + hr * 1.02, hy + hr * 0.55), 180, 360, fill=hc)
        d.pieslice(S(cx - hr * 1.05, hy - hr * 0.9, cx + hr * 0.2, hy + hr * 0.3), 180, 270, fill=hc)
    elif p["style"] == "swept":
        d.chord(S(cx - hr * 1.04, hy - hr * 1.12, cx + hr * 1.04, hy + hr * 0.45), 180, 360, fill=hc)
        d.ellipse(S(cx - hr * 0.9, hy - hr * 1.25, cx + hr * 0.4, hy - hr * 0.55), fill=hc)
    elif p["style"] == "cap":
        d.chord(S(cx - hr * 1.02, hy - hr * 1.1, cx + hr * 1.02, hy + hr * 0.3), 180, 360, fill=(52, 82, 140))
        d.rounded_rectangle(S(cx + face * hr * 0.2 - hr * 0.7, hy - hr * 0.18, cx + face * hr * 1.35, hy - hr * 0.02 + 0.15 * u),
                            radius=6 * SS, fill=(40, 64, 112))
    # Gesicht (Blickrichtung face)
    ex = cx + face * hr * 0.28
    ey = hy + hr * 0.02
    if p["glasses"]:
        for k in (-1, 1):
            d.rounded_rectangle(S(ex + k * 0.55 * u - 0.5 * u, ey - 0.38 * u, ex + k * 0.55 * u + 0.5 * u, ey + 0.32 * u), radius=8 * SS, fill=(20, 20, 26))
        d.line(S(ex - 0.08 * u, ey - 0.15 * u, ex + 0.08 * u, ey - 0.15 * u), fill=(20, 20, 26), width=4 * SS)
    else:
        for k in (-1, 1):
            d.ellipse(S(ex + k * 0.55 * u - 0.16 * u, ey - 0.2 * u, ex + k * 0.55 * u + 0.16 * u, ey + 0.2 * u), fill=INK)
    # Augenbrauen nach Ausdruck
    brow = {"neutral": (0, 0), "angry": (-0.25, 0.25), "smug": (0.15, -0.1), "shock": (-0.25, -0.25), "proud": (0.1, 0.1), "sad": (0.25, -0.25)}[expr]
    bc = hc if p["style"] != "cap" else (60, 40, 30)
    if p["hair"] == (225, 225, 225):
        bc = (190, 190, 190)
    for k in (-1, 1):
        x0, x1 = ex + k * 0.55 * u - 0.35 * u, ex + k * 0.55 * u + 0.35 * u
        inner, outer = (brow[0], brow[1]) if k == face else (brow[0], brow[1])
        y0 = ey - 0.7 * u + (inner if k == -1 else outer) * u * (1 if k == -1 else -1) * -1
        y1 = ey - 0.7 * u + (outer if k == -1 else inner) * u * (1 if k == -1 else -1) * -1
        d.line(S(x0, y0, x1, y1), fill=bc, width=int(0.18 * u * SS))
    # Nase + Mund
    d.ellipse(S(ex + face * 0.15 * u - 0.18 * u, ey + 0.25 * u, ex + face * 0.15 * u + 0.18 * u, ey + 0.6 * u), fill=tuple(max(0, c - 30) for c in p["skin"]))
    my = ey + 1.05 * u
    if p["mustache"]:
        d.chord(S(ex - 0.75 * u, my - 0.45 * u, ex + 0.75 * u, my + 0.2 * u), 180, 360, fill=hc)
    if talk:
        d.ellipse(S(ex - 0.3 * u, my - 0.05 * u, ex + 0.3 * u, my + 0.45 * u), fill=(90, 30, 30))
    elif expr in ("smug", "proud"):
        d.arc(S(ex - 0.5 * u, my - 0.45 * u, ex + 0.5 * u, my + 0.25 * u), 20, 160, fill=INK, width=int(0.14 * u * SS))
    elif expr in ("angry", "sad"):
        d.arc(S(ex - 0.45 * u, my + 0.05 * u, ex + 0.45 * u, my + 0.6 * u), 200, 340, fill=INK, width=int(0.14 * u * SS))
    elif expr == "shock":
        d.ellipse(S(ex - 0.25 * u, my - 0.05 * u, ex + 0.25 * u, my + 0.45 * u), fill=INK)
    else:
        d.line(S(ex - 0.35 * u, my + 0.1 * u, ex + 0.35 * u, my + 0.1 * u), fill=INK, width=int(0.14 * u * SS))
    return hand

# ---------------- Requisiten ----------------
def sports_car(img, x, y, w, color=(196, 32, 38), low=False, face=1):
    d = ImageDraw.Draw(img)
    h = w * (0.24 if low else 0.3)
    if low:   # Miura-artige Keilform
        body = [(x, y - h * 0.35), (x + w * 0.18, y - h * 0.62), (x + w * 0.42, y - h), (x + w * 0.68, y - h * 0.95),
                (x + w * 0.95, y - h * 0.55), (x + w, y - h * 0.2), (x + w, y), (x, y)]
    else:
        body = [(x, y - h * 0.4), (x + w * 0.12, y - h * 0.58), (x + w * 0.35, y - h * 0.62), (x + w * 0.48, y - h),
                (x + w * 0.72, y - h * 0.98), (x + w * 0.86, y - h * 0.6), (x + w, y - h * 0.45), (x + w, y), (x, y)]
    if face == -1:
        body = [(2 * x + w - px, py) for px, py in body]
    d.polygon([(px * SS, py * SS) for px, py in body], fill=color)
    wx0, wx1 = (x + w * 0.44, x + w * 0.7) if face == 1 else (x + w * 0.3, x + w * 0.56)
    d.polygon(S(wx0, y - h * 0.62, wx0 + w * 0.06, y - h * 0.9, wx1 - w * 0.02, y - h * 0.88, wx1 + w * 0.06, y - h * 0.62), fill=(150, 190, 220))
    for cxw in (x + w * 0.2, x + w * 0.8):
        r = h * 0.3
        d.ellipse(S(cxw - r, y - r, cxw + r, y + r), fill=INK)
        d.ellipse(S(cxw - r * 0.5, y - r * 0.5, cxw + r * 0.5, y + r * 0.5), fill=(160, 160, 170))

def tractor(img, x, y, w, color=(52, 96, 170)):
    d = ImageDraw.Draw(img)
    h = w * 0.7
    d.rounded_rectangle(S(x + w * 0.05, y - h * 0.62, x + w * 0.62, y - h * 0.32), radius=10 * SS, fill=color)
    d.rectangle(S(x + w * 0.45, y - h, x + w * 0.85, y - h * 0.3), outline=INK, width=6 * SS)
    d.rectangle(S(x + w * 0.42, y - h * 1.03, x + w * 0.88, y - h * 0.96), fill=color)
    d.rectangle(S(x + w * 0.12, y - h * 0.85, x + w * 0.16, y - h * 0.62), fill=INK)
    for cxw, r in ((x + w * 0.2, h * 0.17), (x + w * 0.72, h * 0.3)):
        d.ellipse(S(cxw - r, y - r * 2, cxw + r, y), fill=INK)
        d.ellipse(S(cxw - r * 0.45, y - r * 1.45, cxw + r * 0.45, y - r * 0.55), fill=GOLD)

def clutch(img, cx, cy, r):
    d = ImageDraw.Draw(img)
    d.ellipse(S(cx - r, cy - r, cx + r, cy + r), fill=(150, 150, 160), outline=INK, width=5 * SS)
    d.ellipse(S(cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7), fill=(110, 110, 120))
    for k in range(6):
        a = k * math.pi / 3
        px, py = cx + math.cos(a) * r * 0.45, cy + math.sin(a) * r * 0.45
        d.rounded_rectangle(S(px - r * 0.1, py - r * 0.06, px + r * 0.1, py + r * 0.06), radius=3 * SS, fill=GOLD)
    d.ellipse(S(cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18), fill=INK)

def label(img, cx, cy, text, size=64, color=GOLD, box=True, fnt="segoeuib.ttf"):
    d = ImageDraw.Draw(img)
    f = font(fnt, size)
    tw = d.textlength(text, font=f)
    if box:
        pad = 26 * SS
        d.rounded_rectangle([cx * SS - tw / 2 - pad, cy * SS - size * SS * 0.75, cx * SS + tw / 2 + pad, cy * SS + size * SS * 0.75],
                            radius=14 * SS, fill=(10, 16, 30), outline=color, width=4 * SS)
    d.text((cx * SS - tw / 2, cy * SS - size * SS * 0.62), text, font=f, fill=color)

def bubble(img, x, y, w, lines, tail_to):
    d = ImageDraw.Draw(img)
    f = font("georgia.ttf", 44)
    lh = 58
    h = lh * len(lines) + 50
    d.polygon(S(x + w * 0.3, y + h - 4, x + w * 0.45, y + h - 4, *tail_to), fill=WHITE)
    d.rounded_rectangle(S(x, y, x + w, y + h), radius=36 * SS, fill=WHITE)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f) / SS
        d.text(S(x + (w - tw) / 2, y + 25 + i * lh), ln, font=f, fill=INK)

def finish(img):
    return img.resize((W, H), Image.LANCZOS)
