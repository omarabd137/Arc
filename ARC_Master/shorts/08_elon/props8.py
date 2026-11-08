"""Detaillierte Requisiten fuer Short #08 (selbst gezeichnet, Cartoon mit realistischer Form)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
INK = (28, 26, 32)
_f = {}
def F(s, p="C:/Windows/Fonts/ariblk.ttf"):
    k = (p, int(s))
    if k not in _f: _f[k] = ImageFont.truetype(p, max(6, int(s)))
    return _f[k]
def _lt(c, k): return tuple(int(v + (255 - v) * k) for v in c[:3])
def _dk(c, k): return tuple(int(v * k) for v in c[:3])

def ferrari(img, x, y, s=1.0, col=(212, 22, 30), face=1):
    """Ferrari-artiger Supersportwagen (Seitenansicht), mit gelbem Schild + Pferd-Silhouette. y = Bodenlinie."""
    S = 2; W_, H_ = int(470 * s * S), int(150 * s * S)
    im = Image.new("RGBA", (W_, H_)); d = ImageDraw.Draw(im)
    def P(px, py): return (px * s * S, py * s * S)
    body = [P(5, 112), P(18, 92), P(70, 84), P(150, 62), P(205, 34), P(290, 30), P(345, 52), P(400, 62), P(452, 76), P(462, 100), P(455, 118), P(12, 122)]
    d.polygon(body, fill=col)
    d.polygon([P(18, 104), P(460, 96), P(455, 118), P(12, 122)], fill=_dk(col, 0.72))        # Schatten unten
    d.polygon([P(150, 66), P(300, 60), P(395, 66), P(390, 72), P(155, 74)], fill=_lt(col, 0.28))  # Glanzkante
    d.polygon([P(212, 40), P(286, 37), P(334, 56), P(198, 60)], fill=(30, 36, 50))           # Scheiben
    d.line([P(262, 38), P(258, 58)], fill=col, width=int(5 * s * S))
    d.polygon([P(300, 70), P(360, 72), P(345, 92), P(305, 90)], fill=(20, 20, 24))            # Lufteinlass
    d.line(body + [body[0]], fill=INK, width=max(2, int(4 * s * S)))
    d.ellipse([*P(442, 80), *P(458, 92)], fill=(255, 245, 210))                               # Scheinwerfer
    d.rectangle([*P(8, 96), *P(20, 104)], fill=(255, 60, 60))                                 # Ruecklicht
    sx, sy = 120, 82; d.rounded_rectangle([*P(sx - 9, sy - 12), *P(sx + 9, sy + 12)], int(3 * s * S), fill=(250, 210, 30), outline=INK, width=max(1, int(2 * s * S)))
    d.polygon([P(sx - 4, sy + 7), P(sx - 3, sy - 3), P(sx + 1, sy - 8), P(sx + 3, sy - 3), P(sx + 4, sy + 7)], fill=INK)   # Pferd (Silhouette)
    for wx in (95, 375):
        d.ellipse([*P(wx - 34, 92), *P(wx + 34, 160 - 0)], fill=INK)
        d.ellipse([*P(wx - 22, 104), *P(wx + 22, 148)], fill=(190, 192, 200))
        for k in range(5):
            a = k * 2 * math.pi / 5; d.line([P(wx, 126), P(wx + math.cos(a) * 20, 126 + math.sin(a) * 20)], fill=(110, 112, 120), width=max(1, int(3 * s * S)))
        d.ellipse([*P(wx - 7, 119), *P(wx + 7, 133)], fill=(250, 210, 30))
    im = im.resize((W_ // S, H_ // S), Image.LANCZOS)
    if face < 0: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    img.alpha_composite(im, (int(x), int(y - 130 * s)))

def golden_arches(d, cx, cy, w, col=(255, 199, 44), bg=(218, 41, 28), box=True):
    """McDonald's-Boegen (selbst nachgezeichnet, redaktionelle Nutzung)."""
    h = w * 0.86
    if box: d.rounded_rectangle((cx - w * 0.62, cy - h * 0.62, cx + w * 0.62, cy + h * 0.62), int(w * 0.12), fill=bg)
    lw = w * 0.15
    for s in (-1, 1):
        ox = cx + s * w * 0.24; pts = []
        for k in range(41):
            t = k / 40; xx = ox + (t - 0.5) * w * 0.48; yy = cy + h * 0.45 - (1 - (2 * t - 1) ** 2) * h * 0.95
            pts.append((xx, yy))
        d.line(pts, fill=col, width=int(lw), joint="curve")
        d.ellipse((pts[0][0] - lw / 2, pts[0][1] - lw / 2, pts[0][0] + lw / 2, pts[0][1] + lw / 2), fill=col)
        d.ellipse((pts[-1][0] - lw / 2, pts[-1][1] - lw / 2, pts[-1][0] + lw / 2, pts[-1][1] + lw / 2), fill=col)

def nfl_shield(d, cx, cy, w):
    h = w * 1.15
    pts = [(cx - w / 2, cy - h / 2 + w * 0.08), (cx - w * 0.2, cy - h / 2 + w * 0.12), (cx, cy - h / 2), (cx + w * 0.2, cy - h / 2 + w * 0.12), (cx + w / 2, cy - h / 2 + w * 0.08),
           (cx + w / 2, cy + h * 0.1), (cx, cy + h / 2), (cx - w / 2, cy + h * 0.1)]
    d.polygon(pts, fill=(1, 51, 105), outline=WHITE_, width=max(3, int(w * 0.04)))
    d.rectangle((cx - w / 2 + w * 0.06, cy - h * 0.28, cx + w / 2 - w * 0.06, cy - h * 0.12), fill=(1, 51, 105))
    for k in range(4): _star(d, cx - w * 0.33 + k * w * 0.22, cy - h * 0.27, w * 0.06, WHITE_)
    d.text((cx, cy + h * 0.08), "NFL", font=F(w * 0.32), fill=WHITE_, anchor="mm")
    d.polygon([(cx - w * 0.12, cy + h * 0.27), (cx + w * 0.12, cy + h * 0.27), (cx, cy + h * 0.38)], fill=(213, 10, 10))
WHITE_ = (255, 255, 255)
def _star(d, cx, cy, r, col):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=col)

# 32 Teams: (Hauptfarbe, Zweitfarbe, Symbol)   – Helme in echten Teamfarben mit Logo-Andeutung
TEAMS = [("Cowboys", (0, 34, 68), (134, 147, 151), "star"), ("Packers", (24, 48, 40), (255, 184, 28), "G"), ("Patriots", (0, 34, 68), (198, 12, 48), "P"),
         ("Chiefs", (227, 24, 55), (255, 184, 28), "KC"), ("49ers", (170, 0, 0), (173, 153, 93), "SF"), ("Steelers", (16, 24, 32), (255, 182, 18), "S"),
         ("Bears", (11, 22, 42), (200, 56, 3), "C"), ("Raiders", (0, 0, 0), (165, 172, 175), "R"), ("Eagles", (0, 76, 84), (165, 172, 175), "E"),
         ("Giants", (1, 35, 82), (163, 13, 45), "ny"), ("Dolphins", (0, 142, 151), (252, 76, 2), "M"), ("Broncos", (251, 79, 20), (0, 34, 68), "D"),
         ("Seahawks", (0, 34, 68), (105, 190, 40), "SEA"), ("Ravens", (36, 23, 115), (158, 124, 12), "B"), ("Bills", (0, 51, 141), (198, 12, 48), "BUF"),
         ("Bengals", (251, 79, 20), (0, 0, 0), "B"), ("Browns", (49, 29, 0), (255, 60, 0), ""), ("Rams", (0, 53, 148), (255, 209, 0), "LA"),
         ("Vikings", (79, 38, 131), (255, 198, 47), "V"), ("Saints", (16, 24, 31), (211, 188, 141), "NO"), ("Lions", (0, 118, 182), (176, 183, 188), "D"),
         ("Commanders", (90, 20, 20), (255, 182, 18), "W"), ("Titans", (12, 35, 64), (75, 146, 219), "T"), ("Colts", (0, 44, 95), (162, 170, 173), "H"),
         ("Jaguars", (16, 24, 32), (215, 162, 42), "J"), ("Texans", (3, 32, 47), (167, 25, 48), "H"), ("Chargers", (0, 128, 198), (255, 194, 14), "Z"),
         ("Cardinals", (151, 35, 63), (0, 0, 0), "A"), ("Falcons", (167, 25, 48), (0, 0, 0), "F"), ("Panthers", (0, 133, 202), (16, 24, 32), "P"),
         ("Buccaneers", (213, 10, 10), (52, 48, 43), "TB"), ("Jets", (18, 87, 64), (255, 255, 255), "NY")]
def helmet(d, cx, cy, s, team):
    _, c1, c2, sym = team
    d.chord((cx - 60 * s, cy - 55 * s, cx + 60 * s, cy + 55 * s), 150, 390, fill=c1, outline=INK, width=max(2, int(4 * s)))
    d.rectangle((cx - 6 * s, cy - 55 * s, cx + 6 * s, cy + 30 * s), fill=c2)                     # Mittelstreifen
    d.line((cx + 40 * s, cy + 10 * s, cx + 78 * s, cy + 18 * s), fill=(220, 220, 225), width=max(2, int(5 * s)))   # Gitter
    d.line((cx + 40 * s, cy + 30 * s, cx + 78 * s, cy + 30 * s), fill=(220, 220, 225), width=max(2, int(5 * s)))
    d.line((cx + 78 * s, cy + 10 * s, cx + 78 * s, cy + 36 * s), fill=(220, 220, 225), width=max(2, int(5 * s)))
    if sym == "star": _star(d, cx - 22 * s, cy + 2 * s, 20 * s, c2)
    elif sym: d.text((cx - 22 * s, cy + 4 * s), sym, font=F((30 if len(sym) < 2 else 22 if len(sym) == 2 else 17) * s), fill=c2, anchor="mm", stroke_width=max(1, int(2 * s)), stroke_fill=INK)

def trophy(d, cx, base, h):
    """silberner Pokal mit Football (allgemein)."""
    d.polygon([(cx - h * 0.1, base - h * 0.12), (cx + h * 0.1, base - h * 0.12), (cx + h * 0.05, base - h * 0.55), (cx - h * 0.05, base - h * 0.55)], fill=(214, 216, 222), outline=INK)
    d.rectangle((cx - h * 0.16, base - h * 0.12, cx + h * 0.16, base), fill=(40, 40, 46), outline=INK, width=4)
    lay_ang = -35
    fb = Image.new("RGBA", (int(h * 0.5), int(h * 0.3))); fd = ImageDraw.Draw(fb)
    fd.ellipse((4, 4, h * 0.5 - 4, h * 0.3 - 4), fill=(214, 216, 222), outline=INK, width=4)
    fd.line((h * 0.12, h * 0.15, h * 0.38, h * 0.15), fill=(160, 162, 170), width=4)
    for k in range(5): xk = h * 0.17 + k * h * 0.04; fd.line((xk, h * 0.12, xk, h * 0.18), fill=(160, 162, 170), width=3)
    return fb.rotate(lay_ang, expand=True, resample=Image.BICUBIC)

def tiny_person(d, x, y, s, col, skin=(232, 196, 164), hair=(60, 44, 34)):
    """kleine Ganzkoerperfigur fuer Menschenmengen (Fuesse bei y)."""
    hr = 9 * s
    d.line((x - 4 * s, y, x - 3 * s, y - 22 * s), fill=INK, width=max(1, int(3 * s))); d.line((x + 4 * s, y, x + 3 * s, y - 22 * s), fill=INK, width=max(1, int(3 * s)))
    d.rounded_rectangle((x - 10 * s, y - 50 * s, x + 10 * s, y - 20 * s), int(5 * s), fill=col)
    d.ellipse((x - hr, y - 50 * s - 2 * hr, x + hr, y - 50 * s), fill=skin)
    d.chord((x - hr, y - 50 * s - 2 * hr, x + hr, y - 50 * s - 0.6 * hr), 180, 360, fill=hair)

def bill_stack(d, cx, top, base, w):
    """Stapel aus 100-Dollar-Scheinen (Seitenansicht)"""
    d.rectangle((cx - w / 2, top, cx + w / 2, base), fill=(118, 170, 110))
    for y in range(int(top), int(base), 6): d.line((cx - w / 2, y, cx + w / 2, y), fill=(92, 140, 86), width=2)
    d.rectangle((cx - w / 2, top, cx + w / 2, base), outline=INK, width=4)
    d.rectangle((cx - w / 2 - 6, top - 14, cx + w / 2 + 6, top), fill=(150, 205, 140), outline=INK, width=4)

def iss(d, cx, cy, s):
    d.rectangle((cx - 60 * s, cy - 10 * s, cx + 60 * s, cy + 10 * s), fill=(210, 214, 220), outline=INK, width=3)
    for sx in (-1, 1):
        for k in range(2):
            x0 = cx + sx * (70 + k * 70) * s; d.rectangle((x0 - 28 * s, cy - 50 * s, x0 + 28 * s, cy + 50 * s), fill=(60, 80, 150), outline=INK, width=3)
            for j in range(1, 4): d.line((x0 - 28 * s, cy - 50 * s + j * 25 * s, x0 + 28 * s, cy - 50 * s + j * 25 * s), fill=(110, 130, 200), width=2)
    d.line((cx - 200 * s, cy, cx + 200 * s, cy), fill=(180, 184, 190), width=max(2, int(6 * s)))

def airliner(d, cx, cy, s):
    d.ellipse((cx - 90 * s, cy - 12 * s, cx + 90 * s, cy + 12 * s), fill=(240, 242, 246), outline=INK, width=3)
    d.polygon([(cx - 10 * s, cy), (cx + 30 * s, cy), (cx - 30 * s, cy + 50 * s), (cx - 50 * s, cy + 50 * s)], fill=(220, 224, 230), outline=INK)
    d.polygon([(cx - 80 * s, cy - 6 * s), (cx - 60 * s, cy - 6 * s), (cx - 90 * s, cy - 40 * s), (cx - 100 * s, cy - 40 * s)], fill=(200, 40, 50), outline=INK)
