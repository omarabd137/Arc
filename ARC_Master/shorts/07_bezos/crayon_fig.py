"""Figuren im Crayon-Stil: grosser erkennbarer Kopf, angezogener eiförmiger Oberkoerper, Arme/Beine als duenne Striche, kleine Haende.
Gezeichnet in 2x und verkleinert (sauber). person(frame, pr, cx, base, Hh, expr, arms, face)"""
import math
from PIL import Image, ImageDraw
INK = (30, 28, 36)
_cache = {}

def P(**k):
    d = dict(skin=(236, 194, 162), shirt=(150, 192, 236), vest=None, jacket=None, tie=None, pants=(44, 48, 62), shoes=(34, 30, 30),
             hair=None, hair_style="shaved", brow=(90, 70, 60), build=1.0)
    d.update(k); return d

def _dk(c, k=0.82): return tuple(int(v * k) for v in c[:3])
def _lt(c, k=0.35): return tuple(int(v + (255 - v) * k) for v in c[:3])

# Armposen: (Ellbogen, Hand) relativ zur Schulter in Einheiten von r, je Seite (s=-1 links, +1 rechts)
ARMS = {"down": ((0.25, 1.05), (0.35, 2.0)), "hip": ((0.95, 0.85), (0.45, 1.45)), "point": ((0.9, 0.25), (1.9, 0.05)),
        "up": ((0.6, -0.9), (0.75, -1.9)), "wave": ((0.9, -0.2), (1.2, -1.2)), "cross": ((0.55, 0.95), (-0.55, 0.85)),
        "shrug": ((0.9, 0.55), (1.35, -0.1)), "hold": ((0.55, 1.0), (0.95, 0.75)), "give": ((0.7, 0.7), (1.7, 0.6)), "chin": ((0.6, 0.9), (0.1, -0.05))}

def _draw(pr, Hh, expr, arms, face, S=2):
    W_ = int(Hh * 1.3 * S); H_ = int(Hh * 1.15 * S)
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im, "RGBA")
    cx = W_ / 2; base = H_ - 0.06 * Hh * S
    r = Hh * 0.235 * S; lw = max(3, int(Hh * 0.012 * S)); limb = max(4, int(Hh * 0.016 * S))
    b = pr["build"]
    head_cy = base - Hh * S + r * 1.08
    tor_top = head_cy + r * 0.95; tor_h = Hh * 0.27 * S; tor_w = r * 0.98 * b
    hip_y = tor_top + tor_h * 0.92
    # Beine
    for s in (-1, 1):
        hx = cx + s * tor_w * 0.28
        d.line([(hx, hip_y), (hx + s * r * 0.08, base - r * 0.12)], fill=INK, width=limb)
        fx_ = hx + s * r * 0.08; dirn = (face or s)
        d.rounded_rectangle((min(fx_ - r * 0.1, fx_ + dirn * r * 0.34), base - r * 0.17, max(fx_ - r * 0.1, fx_ + dirn * r * 0.34) if dirn > 0 else fx_ + r * 0.1, base), int(r * 0.07), fill=pr["shoes"], outline=INK, width=lw)
    # Oberkoerper (Ei)
    box = (cx - tor_w * 0.62, tor_top, cx + tor_w * 0.62, tor_top + tor_h)
    d.ellipse(box, fill=pr["shirt"], outline=INK, width=lw)
    if pr["vest"] or pr["jacket"]:
        c = pr["vest"] or pr["jacket"]
        mask = Image.new("L", (W_, H_), 0); md = ImageDraw.Draw(mask); md.ellipse(box, fill=255)
        lay = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        for s in (-1, 1):
            ld.polygon([(cx + s * tor_w * 0.2, tor_top + tor_h * 0.08), (cx + s * tor_w * 0.2, tor_top + tor_h), (cx + s * tor_w * 0.7, tor_top + tor_h), (cx + s * tor_w * 0.7, tor_top - 5),
                        (cx + s * tor_w * 0.3, tor_top - 5)], fill=c + (255,))
        lay.putalpha(Image.fromarray(__import__("numpy").minimum(__import__("numpy").array(lay.getchannel("A")), __import__("numpy").array(mask))))
        im.alpha_composite(lay); d = ImageDraw.Draw(im, "RGBA")
        d.ellipse(box, outline=INK, width=lw)
        for s in (-1, 1): d.line([(cx + s * tor_w * 0.2, tor_top + tor_h * 0.1), (cx + s * tor_w * 0.2, tor_top + tor_h * 0.95)], fill=INK, width=max(2, lw - 1))
        for k in range(3): d.ellipse((cx - 4, tor_top + tor_h * (0.35 + k * 0.18) - 4, cx + 4, tor_top + tor_h * (0.35 + k * 0.18) + 4), fill=INK)
    # Kragen
    for s in (-1, 1): d.polygon([(cx, tor_top + r * 0.28), (cx + s * r * 0.3, tor_top - r * 0.02), (cx + s * r * 0.05, tor_top - r * 0.06)], fill=_lt(pr["shirt"], 0.4), outline=INK)
    if pr["tie"]: d.polygon([(cx - r * 0.07, tor_top + r * 0.2), (cx + r * 0.07, tor_top + r * 0.2), (cx + r * 0.1, tor_top + tor_h * 0.6), (cx, tor_top + tor_h * 0.7), (cx - r * 0.1, tor_top + tor_h * 0.6)], fill=pr["tie"], outline=INK)
    # Arme
    al, ar = ARMS.get(arms[0] if isinstance(arms, tuple) else arms, ARMS["down"]), ARMS.get(arms[1] if isinstance(arms, tuple) else arms, ARMS["down"])
    for s, (el, ha) in ((-1, al), (1, ar)):
        sx, sy = cx + s * tor_w * 0.5, tor_top + tor_h * 0.16
        AS = 0.6; ex, ey = sx + s * el[0] * r * AS, sy + el[1] * r * AS; hx, hy = sx + s * ha[0] * r * AS, sy + ha[1] * r * AS
        d.line([(sx, sy), (ex, ey), (hx, hy)], fill=INK, width=limb, joint="curve")
        d.ellipse((hx - r * 0.13, hy - r * 0.13, hx + r * 0.13, hy + r * 0.13), fill=pr["skin"], outline=INK, width=lw)
    # ---------- Kopf im Crayon-Stil: rund, schattiert, echte Gesichtszuege ----------
    import numpy as np
    rx, ry = r * 0.96, r * 1.0; fdir = face or 0
    sk = np.array(pr["skin"], float)
    for s in (-1, 1):   # Ohren mit Innenlinie
        ox = cx + s * rx * 0.96; d.ellipse((ox - r * 0.17, head_cy - r * 0.08, ox + r * 0.17, head_cy + r * 0.3), fill=pr["skin"], outline=INK, width=lw)
        d.arc((ox - r * 0.09, head_cy - r * 0.0, ox + r * 0.09, head_cy + r * 0.22), 90 if s > 0 else 270, 270 if s > 0 else 90, fill=_dk(pr["skin"], 0.72), width=max(2, lw - 1))
    # Kopf mit weichem Verlauf (Licht oben links)
    yy, xx = np.mgrid[0:H_, 0:W_]; lx, ly = cx - rx * 0.35, head_cy - ry * 0.45
    dist = np.sqrt(((xx - lx) / (rx * 2.0)) ** 2 + ((yy - ly) / (ry * 2.0)) ** 2)
    shade = np.clip(1.06 - dist * 0.42, 0.78, 1.06)[..., None]
    col = np.clip(sk * shade, 0, 255).astype(np.uint8); grad = Image.fromarray(np.dstack([col, np.full((H_, W_), 255, np.uint8)]), "RGBA")
    HEAD = []
    for k in range(73):
        t = 2 * math.pi * k / 72; xr = rx * (0.92 + 0.12 * max(0.0, math.sin(t)))   # unten breiter (Kiefer)
        HEAD.append((cx + math.cos(t) * xr, head_cy + math.sin(t) * ry))
    mask = Image.new("L", (W_, H_), 0); ImageDraw.Draw(mask).polygon(HEAD, fill=255)
    im.paste(grad, (0, 0), mask); d = ImageDraw.Draw(im, "RGBA")
    # Mondsichel-Schatten auf der abgewandten Seite
    sh = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh); side = -1 if fdir > 0 else 1
    sd.polygon(HEAD, fill=_dk(pr["skin"], 0.8) + (130,))
    sd.ellipse((cx - rx - side * r * 0.22, head_cy - ry - r * 0.1, cx + rx - side * r * 0.22, head_cy + ry + r * 0.05), fill=(0, 0, 0, 0))
    sh.putalpha(Image.fromarray(np.minimum(np.array(sh.getchannel("A")), np.array(mask)))); im.alpha_composite(sh); d = ImageDraw.Draw(im, "RGBA")
    d.line(HEAD + [HEAD[0]], fill=INK, width=lw + 1, joint="curve")
    if pr["hair_style"] == "shaved":   # Glanz auf der Glatze
        d.arc((cx - rx * 0.66, head_cy - ry * 0.9, cx - rx * 0.02, head_cy - ry * 0.36), 205, 290, fill=_lt(pr["skin"], 0.75), width=lw * 2)
        d.ellipse((cx - rx * 0.2, head_cy - ry * 0.84, cx - rx * 0.1, head_cy - ry * 0.74), fill=_lt(pr["skin"], 0.8))
    fx = cx + fdir * r * 0.16; ey = head_cy - r * 0.02; sp = r * 0.28; line_c = _dk(pr["skin"], 0.62); thin = max(2, lw - 1)
    # Augen: Augapfel, Iris, Lid  (bei Lachen: zusammengekniffen)
    laugh = expr in ("laugh", "smile_closed")
    for s in (-1, 1):
        ex_ = fx + s * sp; 
        if laugh or (expr == "wink" and s > 0):
            d.arc((ex_ - r * 0.13, ey - r * 0.07, ex_ + r * 0.13, ey + r * 0.12), 200, 340, fill=INK, width=lw + 1)
        else:
            d.ellipse((ex_ - r * 0.12, ey - r * 0.08, ex_ + r * 0.12, ey + r * 0.07), fill=(252, 250, 246), outline=INK, width=thin)
            px = ex_ + fdir * r * 0.03; d.ellipse((px - r * 0.055, ey - r * 0.06, px + r * 0.055, ey + r * 0.05), fill=(70, 52, 40))
            d.ellipse((px - r * 0.025, ey - r * 0.035, px + r * 0.025, ey + r * 0.02), fill=INK)
            d.arc((ex_ - r * 0.13, ey - r * 0.11, ex_ + r * 0.13, ey + r * 0.05), 200, 340, fill=INK, width=lw)   # Oberlid
    # Brauen: kraeftig, kurz, leicht gebogen
    tilt = {"smug": 0.05, "angry": 0.08, "worried": -0.06}.get(expr, 0.0)
    for s in (-1, 1):
        bx0, bx1 = fx + s * (sp - r * 0.15), fx + s * (sp + r * 0.15); by = ey - r * 0.2
        d.line([(bx0, by + tilt * r), (fx + s * sp, by - r * 0.03), (bx1, by - tilt * r * 0.3 + r * 0.01)], fill=pr["brow"], width=lw + 3, joint="curve")
    # Nase (klein, Crayon-artig) + Nasolabialfalten
    nx = fx + fdir * r * 0.06
    d.arc((nx - r * 0.07, ey + r * 0.14, nx + r * 0.07, ey + r * 0.28), 20, 160, fill=line_c, width=thin)
    my = head_cy + r * 0.52
    if expr == "laugh":
        d.chord((fx - r * 0.38, my - r * 0.24, fx + r * 0.38, my + r * 0.3), 0, 180, fill=(110, 36, 42), outline=INK, width=lw)
        d.rectangle((fx - r * 0.3, my - r * 0.02, fx + r * 0.3, my + r * 0.09), fill=(255, 255, 255))
        d.line([(fx - r * 0.3, my + r * 0.09), (fx + r * 0.3, my + r * 0.09)], fill=INK, width=thin)
        d.chord((fx - r * 0.38, my - r * 0.24, fx + r * 0.38, my + r * 0.3), 0, 180, outline=INK, width=lw)
    elif expr in ("smug", "wink", "smile_closed"):
        d.arc((fx - r * 0.24 + fdir * r * 0.04, my - r * 0.2, fx + r * 0.24 + fdir * r * 0.04, my + r * 0.06), 10, 170, fill=INK, width=lw + 1)
    elif expr == "worried":
        d.arc((fx - r * 0.16, my - r * 0.02, fx + r * 0.16, my + r * 0.14), 200, 340, fill=INK, width=lw + 1)
    elif expr == "shock":
        d.ellipse((fx - r * 0.09, my - r * 0.1, fx + r * 0.09, my + r * 0.12), fill=(110, 36, 42), outline=INK, width=lw)
    else:
        d.line([(fx - r * 0.13, my - r * 0.02), (fx + r * 0.13, my - r * 0.02)], fill=INK, width=lw + 1)
    im = im.resize((W_ // S, H_ // S), Image.LANCZOS)
    return im, (W_ // S) / 2, H_ // S - 0.06 * Hh

def person(frame, pr, cx, base, Hh, expr="neutral", arms=("down", "down"), face=0, dy=0.0):
    key = (id(pr), int(Hh), expr, arms if isinstance(arms, tuple) else (arms, arms), face)
    if key not in _cache: _cache[key] = _draw(pr, Hh, expr, arms, face)
    im, ox, oy = _cache[key]
    frame.alpha_composite(im, (int(cx - ox), int(base - oy + dy)))

BEZOS = P(skin=(234, 190, 158), shirt=(150, 192, 238), vest=(38, 46, 70), pants=(40, 44, 58), brow=(96, 80, 72), build=1.18)
YOU = P(skin=(240, 206, 176), shirt=(220, 120, 80), pants=(60, 74, 110), hair=(90, 60, 40), hair_style="short", brow=(80, 56, 40))
