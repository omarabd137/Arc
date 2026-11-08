"""Figuren nach dem Crayon-Prinzip (eigene Umsetzung):
runder Kopf mit flacher Haut + seitlichem Schatten, Erkennungsmerkmal ueber Kopfform/Frisur/Accessoire,
schlichtes Gesicht (kleine Augen, kleiner Mund, kurze Brauen), Oberkoerper als Schulter-Form mit typischem Oberteil
und Details, duenne gebogene Strich-Arme an den Schultern, kleine Haende."""
import math
import numpy as np
from PIL import Image, ImageDraw
INK = (28, 26, 32)
_cache = {}
def _dk(c, k=0.82): return tuple(int(v * k) for v in c[:3])
def _lt(c, k=0.35): return tuple(int(v + (255 - v) * k) for v in c[:3])

def P(**k):
    d = dict(skin=(236, 196, 164), shirt=(150, 192, 236), vest=None, tee=None, pants=(44, 48, 62), shoes=(30, 28, 28),
             hair=None, bald=True, brow=(70, 56, 48), glasses=None, jacket=None, tie=None, bezos=False, aviators=False, quiff=False, elon=False)
    d.update(k); return d

def _bez(p0, p1, p2, n=16):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]

# Arm-Posen: (Kontrollpunkt, Hand) relativ zur Schulter, Einheit r (Kopfradius)
ARMS = {"down": ((0.32, 0.6), (0.18, 1.12)), "hip": ((0.75, 0.55), (0.35, 1.05)), "point": ((0.9, 0.2), (1.6, 0.05)),
        "up": ((0.45, -0.6), (0.55, -1.35)), "cross": ((0.55, 0.75), (-0.45, 0.75)), "hold": ((0.5, 0.8), (0.75, 0.55)),
        "give": ((0.6, 0.6), (1.35, 0.45)), "shrug": ((0.75, 0.3), (1.05, -0.25)), "wave": ((0.75, -0.1), (0.95, -0.95))}

def _draw(pr, R, expr, arms, face, legs, S=2):
    r = R * S; lw = max(3, int(r * 0.042)); limb = max(3, int(r * 0.045))
    W_ = int(r * 5.2); H_ = int(r * (7.3 if legs else 5.4))
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im, "RGBA")
    cx = W_ / 2; head_cy = r * 1.45
    sh_y = head_cy + r * 0.9; sh_w = r * 0.95; tor_h = r * 2.0; bot_y = sh_y + tor_h; bot_w = r * 0.8
    fdir = face or 0
    # Beine (optional, kurz)
    if legs:
        for s in (-1, 1):
            hx = cx + s * bot_w * 0.42; d.line([(hx, bot_y - r * 0.05), (hx + s * r * 0.05, bot_y + r * 1.15)], fill=INK, width=limb)
            fx_ = hx + s * r * 0.05; dirn = fdir or s
            x0, x1 = (fx_ - r * 0.08, fx_ + r * 0.3) if dirn > 0 else (fx_ - r * 0.3, fx_ + r * 0.08)
            d.rounded_rectangle((x0, bot_y + r * 1.08, x1, bot_y + r * 1.24), int(r * 0.06), fill=pr["shoes"], outline=INK, width=lw)
    # Oberkoerper: Schulterform (oben breit, unten etwas schmaler, runde Ecken)
    body = _bez((cx - sh_w, sh_y + r * 0.35), (cx - sh_w, sh_y - r * 0.02), (cx - sh_w * 0.55, sh_y - r * 0.02)) + \
           [(cx + sh_w * 0.55, sh_y - r * 0.02)] + _bez((cx + sh_w * 0.55, sh_y - r * 0.02), (cx + sh_w, sh_y - r * 0.02), (cx + sh_w, sh_y + r * 0.35)) + \
           [(cx + bot_w, bot_y), (cx - bot_w, bot_y)]
    base_col = pr["tee"] or pr["shirt"]
    d.polygon(body, fill=base_col)
    if pr["vest"]:   # Weste sitzt sauber: folgt dem Koerperumriss, V-Ausschnitt zeigt Hemd + Kragen
        v = pr["vest"]
        bm = Image.new("L", (W_, H_), 0); ImageDraw.Draw(bm).polygon(body, fill=255)
        vl = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); vd = ImageDraw.Draw(vl)
        for s in (-1, 1):
            vd.polygon([(cx + s * r * 0.2, sh_y - r * 0.02), (cx + s * r * 0.4, sh_y - r * 0.3), (cx + s * sh_w * 1.3, sh_y - r * 0.3),
                        (cx + s * sh_w * 1.3, bot_y + 5), (cx + s * r * 0.05, bot_y + 5), (cx + s * r * 0.05, sh_y + tor_h * 0.42)], fill=v + (255,))
        vl.putalpha(Image.fromarray(np.minimum(np.array(vl.getchannel("A")), np.array(bm)))); im.alpha_composite(vl); d = ImageDraw.Draw(im, "RGBA")
        for s in (-1, 1):
            d.line([(cx + s * r * 0.2, sh_y - r * 0.02), (cx + s * r * 0.05, sh_y + tor_h * 0.42), (cx + s * r * 0.05, bot_y)], fill=INK, width=max(2, lw - 1), joint="curve")
            for k in range(1, 4):   # dezente Steppnaehte, leicht gebogen
                yk = sh_y + tor_h * (0.18 + k * 0.2); x_in = cx + s * r * (0.1 if yk > sh_y + tor_h * 0.42 else 0.2); x_out = cx + s * (sh_w - (sh_w - bot_w) * (yk - sh_y) / tor_h) * 0.96
                d.arc((min(x_in, x_out), yk - r * 0.06, max(x_in, x_out), yk + r * 0.06), 20, 160, fill=_lt(v, 0.14), width=max(2, lw - 2))
        for s in (-1, 1): d.polygon([(cx, sh_y + r * 0.26), (cx + s * r * 0.22, sh_y - r * 0.05), (cx + s * r * 0.04, sh_y - r * 0.07)], fill=_lt(pr["shirt"], 0.35), outline=INK)
        for k in range(2): d.ellipse((cx - 3, sh_y + r * 0.45 + k * r * 0.25 - 3, cx + 3, sh_y + r * 0.45 + k * r * 0.25 + 3), fill=INK)
    if pr["jacket"]:   # Sakko mit Revers + Krawatte (z. B. Banker)
        j = pr["jacket"]
        for s in (-1, 1):
            jp = [(cx + s * r * 0.1, sh_y + r * 0.02), (cx + s * sh_w * 0.56, sh_y - r * 0.02), (cx + s * sh_w, sh_y + r * 0.3), (cx + s * bot_w, bot_y), (cx + s * r * 0.02, bot_y), (cx + s * r * 0.02, sh_y + r * 0.75)]
            d.polygon(jp, fill=j); d.polygon([(cx + s * r * 0.1, sh_y + r * 0.02), (cx + s * r * 0.36, sh_y + r * 0.12), (cx + s * r * 0.05, sh_y + r * 0.7)], fill=_dk(j, 0.8), outline=INK)
        if pr["tie"]: d.polygon([(cx - r * 0.06, sh_y + r * 0.05), (cx + r * 0.06, sh_y + r * 0.05), (cx + r * 0.08, sh_y + r * 0.6), (cx, sh_y + r * 0.72), (cx - r * 0.08, sh_y + r * 0.6)], fill=pr["tie"], outline=INK)
    if pr["tee"]:
        t_ = pr["tee"]; d.arc((cx - r * 0.42, sh_y - r * 0.3, cx + r * 0.42, sh_y + r * 0.28), 20, 160, fill=_lt(t_, 0.3), width=lw + 2)
        for s in (-1, 1): d.line([(cx + s * sh_w * 0.62, sh_y + r * 0.02), (cx + s * sh_w * 0.95, sh_y + r * 0.42)], fill=_lt(t_, 0.18), width=max(2, lw - 1))
        d.line([(cx - r * 0.15, sh_y + tor_h * 0.7), (cx + r * 0.25, sh_y + tor_h * 0.66)], fill=_lt(t_, 0.12), width=max(2, lw - 2))
    d.line(body + [body[0]], fill=INK, width=lw, joint="curve")
    # Arme: duenne, gebogene Linien direkt an den Schultern
    al = ARMS.get(arms[0], ARMS["down"]); ar = ARMS.get(arms[1], ARMS["down"])
    for s, (c, h) in ((-1, al), (1, ar)):
        sx, sy = cx + s * sh_w * 0.97, sh_y + r * 0.3
        pts = _bez((sx, sy), (sx + s * c[0] * r, sy + c[1] * r), (sx + s * h[0] * r, sy + h[1] * r))
        d.line(pts, fill=INK, width=limb, joint="curve")
        hx, hy = pts[-1]; d.ellipse((hx - r * 0.11, hy - r * 0.11, hx + r * 0.11, hy + r * 0.11), fill=pr["skin"], outline=INK, width=lw)
    # Kopf: Kreis, flache Haut, seitlicher Schatten
    sk = pr["skin"]
    for s in (-1, 1):
        ew = 0.2 if pr["bezos"] else 0.15
        ox = cx + s * r * (1.0 if pr["bezos"] else 0.97); d.ellipse((ox - r * ew, head_cy - r * 0.06, ox + r * ew, head_cy + r * 0.32), fill=sk, outline=INK, width=lw)
    d.ellipse((cx - r, head_cy - r, cx + r, head_cy + r), fill=sk)
    m = Image.new("L", (W_, H_), 0); ImageDraw.Draw(m).ellipse((cx - r, head_cy - r, cx + r, head_cy + r), fill=255)
    sh = Image.new("RGBA", (W_, H_), _dk(sk, 0.86) + (255,)); hole = Image.new("L", (W_, H_), 0)
    side = -1 if fdir > 0 else 1
    ImageDraw.Draw(hole).ellipse((cx - r - side * r * 0.24, head_cy - r * 1.05, cx + r - side * r * 0.24, head_cy + r * 0.95), fill=255)
    sh.putalpha(Image.fromarray((np.array(m) * (1 - np.array(hole) / 255)).astype(np.uint8))); im.alpha_composite(sh); d = ImageDraw.Draw(im, "RGBA")
    if pr["bald"]:
        d.arc((cx - r * 0.7, head_cy - r * 0.9, cx - r * 0.05, head_cy - r * 0.35), 205, 285, fill=_lt(sk, 0.7), width=lw + 5)
    if pr["hair"]:
        hc = pr["hair"]; yy, xx = np.mgrid[0:H_, 0:W_]
        dx = (xx - cx) / r; dyy = (yy - head_cy) / r
        inside = dx ** 2 + dyy ** 2 < np.where(dyy < -0.55, 1.035, 0.985) ** 2
        if pr["quiff"]:   # Tolle: Volumen oben, nach hinten gestylt (Elon)
            inside = inside | ((dx ** 2 / 0.98 ** 2 + (dyy + 0.3) ** 2 / 0.98 ** 2 < 1.0) & (dyy < -0.4))
        hairline = (-0.5 if pr["quiff"] else -0.42) + 0.6 * np.abs(dx) ** 2.2 - (0.03 if pr["quiff"] else 0.06) * np.sin(dx * 9)      # Stirnbogen, an den Seiten tiefer
        if pr["elon"]:   # nach hinten gestylt, leichte Geheimratsecken, Seiten kurz bis zu den Ohren
            hairline = -0.56 - 0.16 * np.exp(-((np.abs(dx) - 0.42) / 0.14) ** 2) + 0.05 * np.exp(-(dx / 0.12) ** 2) + 1.4 * np.clip(np.abs(dx) - 0.72, 0, None)
        hm = (inside & (dyy < hairline) & (dyy < 0.15)).astype(np.uint8) * 255
        lay = Image.new("RGBA", (W_, H_), hc + (255,)); lay.putalpha(Image.fromarray(hm)); im.alpha_composite(lay); d = ImageDraw.Draw(im, "RGBA")
        from PIL import ImageFilter as _IF
        cm = np.zeros((H_, W_), np.uint8); cm[(dx ** 2 + dyy ** 2) < 1.0] = 255
        uni = Image.fromarray(np.maximum(cm, hm)); ring = np.array(uni.filter(_IF.MaxFilter(lw * 2 + 1))).astype(int) - np.array(uni).astype(int)
        ol = Image.new("RGBA", (W_, H_), INK + (255,)); ol.putalpha(Image.fromarray(np.clip(ring, 0, 255).astype(np.uint8))); im.alpha_composite(ol); d = ImageDraw.Draw(im, "RGBA")
        HAIR_OUTLINED = True
        if pr["elon"]:   # Haarstruktur: Straehnen nur innerhalb der Haare
            st = Image.new("RGBA", (W_, H_)); sd_ = ImageDraw.Draw(st)
            for k in range(6):
                x0 = cx - r * 0.62 + k * r * 0.24; sd_.arc((x0 - r * 0.3, head_cy - r * 1.25, x0 + r * 0.3, head_cy - r * 0.5), 205, 290, fill=_lt(hc, 0.22) + (255,), width=max(2, lw - 1))
            st.putalpha(Image.fromarray(np.minimum(np.array(st.getchannel("A")), hm))); im.alpha_composite(st); d = ImageDraw.Draw(im, "RGBA")
        d.arc((cx - r * 0.75, head_cy - r * 1.0, cx + r * 0.1, head_cy - r * 0.4), 200, 280, fill=_lt(hc, 0.25), width=lw)
    if not pr["hair"]: d.ellipse((cx - r, head_cy - r, cx + r, head_cy + r), outline=INK, width=lw)
    # Gesicht: schlicht
    fx = cx + fdir * r * 0.18; ey = head_cy + r * 0.02; sp = r * 0.3
    laugh = expr in ("laugh", "smile_closed")
    for s in ((-1, 1) if not (pr["elon"] and expr in ("grin", "smug", "laugh")) else ()):
        ex_ = fx + s * sp
        if laugh or (expr == "wink" and s > 0):
            d.arc((ex_ - r * 0.1, ey - r * 0.06, ex_ + r * 0.1, ey + r * 0.09), 200, 340, fill=INK, width=lw)
        else:
            d.ellipse((ex_ - r * 0.045, ey - r * 0.065, ex_ + r * 0.045, ey + r * 0.06), fill=INK)
    if pr["bezos"]:
        for s in (-1, 1):   # dicke, hochgezogene Bogen-Brauen
            ex_ = fx + s * sp; by = ey - r * 0.2
            d.line([(ex_ - s * r * 0.12, by + r * 0.01), (ex_ + s * r * 0.0, by - r * 0.03), (ex_ + s * r * 0.13, by + r * 0.0)], fill=pr["brow"], width=lw + 3, joint="curve")
            d.arc((ex_ - r * 0.09, ey + r * 0.06, ex_ + r * 0.09, ey + r * 0.16), 20, 160, fill=_dk(sk, 0.72), width=max(2, lw - 2))   # Wangenfalte unter dem Auge
        my = head_cy + r * 0.43
        if expr in ("laugh", "grin", "smug", "wink"):
            w2 = 0.25 if expr in ("laugh", "grin") else 0.22
            top = [(fx + r * w2 * math.cos(math.radians(a_)), my + r * 0.04 - r * 0.07 * math.sin(math.radians(a_)) ) for a_ in range(180, 361, 10)]
            bot = [(fx + r * w2 * math.cos(math.radians(a_)), my + r * 0.04 + r * (0.15 if expr in ("laugh", "grin") else 0.1) * math.sin(math.radians(a_))) for a_ in range(0, 181, 10)]
            mouth = top + bot
            d.polygon(mouth, fill=(255, 255, 255))
            d.line(mouth + [mouth[0]], fill=INK, width=lw, joint="curve")
            for s in (-1, 1): d.arc((fx + s * r * (w2 + 0.04) - r * 0.06, my - r * 0.06, fx + s * r * (w2 + 0.04) + r * 0.06, my + r * 0.08), 270 if s > 0 else 90, 90 if s > 0 else 270, fill=_dk(sk, 0.7), width=max(2, lw - 1))
            expr_done = True
        else: expr_done = False
    else: expr_done = False
    if pr["elon"] and expr in ("grin", "smug", "laugh"):
        for s in (-1, 1):
            ex_ = fx + s * sp
            d.ellipse((ex_ - r * 0.045, ey - r * 0.02, ex_ + r * 0.045, ey + r * 0.07), fill=INK)                       # Pupille
            d.arc((ex_ - r * 0.12, ey - r * 0.08, ex_ + r * 0.12, ey + r * 0.1), 200, 340, fill=INK, width=lw + 1)      # Oberlid (selbstsicher)
            d.line([(ex_ - s * r * 0.12, ey - r * 0.2), (ex_ + s * r * 0.15, ey - r * 0.24)], fill=pr["brow"], width=lw + 5)
        my2 = head_cy + r * 0.42; w2 = r * 0.34
        mouth = [(fx - w2, my2)] + [(fx + w2 * math.cos(math.radians(a_)), my2 + r * 0.26 * math.sin(math.radians(a_))) for a_ in range(0, 181, 10)][::-1]
        mouth = [(fx - w2, my2), (fx + w2, my2)] + [(fx + w2 * math.cos(math.radians(a_)), my2 + r * 0.24 * math.sin(math.radians(a_))) for a_ in range(0, 181, 10)]
        d.polygon(mouth, fill=(255, 255, 255))
        d.line([(fx - w2 * 0.92, my2 + r * 0.1), (fx + w2 * 0.92, my2 + r * 0.1)], fill=INK, width=max(2, lw - 1))     # Zahnreihen-Trennung
        for k in range(-2, 3):
            d.line([(fx + k * w2 * 0.3, my2 + r * 0.02), (fx + k * w2 * 0.3, my2 + r * 0.09)], fill=(205, 205, 205), width=max(1, lw - 3))
            d.line([(fx + k * w2 * 0.27, my2 + r * 0.11), (fx + k * w2 * 0.27, my2 + r * 0.17)], fill=(205, 205, 205), width=max(1, lw - 3))
        d.line(mouth + [mouth[0]], fill=INK, width=lw, joint="curve")
        for s in (-1, 1): d.arc((fx + s * (w2 + r * 0.06) - r * 0.08, my2 - r * 0.14, fx + s * (w2 + r * 0.06) + r * 0.08, my2 + r * 0.12), 270 if s > 0 else 90, 90 if s > 0 else 270, fill=_dk(pr["skin"], 0.66), width=max(2, lw - 1))
        expr_done = True
    tilt = {"smug": 0.05, "angry": 0.08, "worried": -0.07}.get(expr, 0.0)
    for s in ((-1, 1) if not (pr["bezos"] or (pr["elon"] and expr in ("grin", "smug", "laugh"))) else ()):
        bx0, bx1 = fx + s * (sp - r * 0.1), fx + s * (sp + r * 0.11); by = ey - r * 0.2
        d.line([(bx0, by + tilt * r), (bx1, by - tilt * r)], fill=pr["brow"], width=lw + (5 if pr["elon"] else 3))
    if pr["glasses"]:
        g = pr["glasses"]
        for s in (-1, 1): d.ellipse((fx + s * sp - r * 0.17, ey - r * 0.15, fx + s * sp + r * 0.17, ey + r * 0.15), outline=g, width=lw)
        d.line([(fx - sp + r * 0.17, ey), (fx + sp - r * 0.17, ey)], fill=g, width=lw)
    if pr["aviators"]:   # Pilotenbrille (Bezos' bekannter Look seit 2021)
        for s in (-1, 1):
            ex_ = fx + s * sp; lens = [(ex_ - r * 0.19, ey - r * 0.1), (ex_ + r * 0.19, ey - r * 0.1), (ex_ + r * 0.17, ey + r * 0.06), (ex_ + r * 0.06, ey + r * 0.15), (ex_ - r * 0.12, ey + r * 0.13), (ex_ - r * 0.19, ey + r * 0.02)]
            if s < 0: lens = [(2 * ex_ - x, y) for x, y in lens]
            d.polygon(lens, fill=(40, 52, 70)); d.line(lens + [lens[0]], fill=(200, 190, 150), width=lw)
            d.line([(ex_ - r * 0.1, ey - r * 0.04), (ex_ + r * 0.02, ey - r * 0.08)], fill=(150, 175, 205), width=lw + 1)
        d.line([(fx - sp + r * 0.17, ey - r * 0.08), (fx + sp - r * 0.17, ey - r * 0.08)], fill=(200, 190, 150), width=lw)
    my = head_cy + r * 0.45
    if expr_done: pass
    elif expr == "laugh":   # breites Bezos-Lachen: obere Zahnreihe
        box = (fx - r * 0.24, my - r * 0.12, fx + r * 0.24, my + r * 0.2)
        d.chord(box, 0, 180, fill=(112, 38, 44)); d.rectangle((fx - r * 0.21, my + r * 0.04, fx + r * 0.21, my + r * 0.1), fill=(255, 255, 255))
        d.chord(box, 0, 180, outline=INK, width=lw); d.line([(box[0] + lw, my + r * 0.05), (box[2] - lw, my + r * 0.05)], fill=INK, width=lw)
    elif expr in ("grin",):
        box = (fx - r * 0.3, my - r * 0.1, fx + r * 0.3, my + r * 0.2)
        d.chord(box, 0, 180, fill=(255, 255, 255), outline=INK, width=lw)
    elif expr in ("smug", "wink", "smile_closed"):
        d.arc((fx - r * 0.22 + fdir * r * 0.04, my - r * 0.14, fx + r * 0.22 + fdir * r * 0.04, my + r * 0.08), 15, 165, fill=INK, width=lw)
    elif expr == "worried":
        d.arc((fx - r * 0.15, my + r * 0.0, fx + r * 0.15, my + r * 0.14), 200, 340, fill=INK, width=lw)
    elif expr == "shock":
        d.ellipse((fx - r * 0.08, my - r * 0.04, fx + r * 0.08, my + r * 0.16), fill=(112, 38, 44), outline=INK, width=lw)
    else:
        d.line([(fx - r * 0.12, my + r * 0.04), (fx + r * 0.12, my + r * 0.04)], fill=INK, width=lw)
    from PIL import ImageFilter
    a_ = im.getchannel("A"); halo = a_.filter(ImageFilter.MaxFilter(9))
    rim = Image.new("RGBA", (W_, H_), (255, 255, 255, 0)); rim.putalpha(halo.point(lambda v: int(v * 0.85)))
    rim.alpha_composite(im); im = rim
    im = im.resize((W_ // S, H_ // S), Image.LANCZOS)
    return im, (W_ // S) / 2, head_cy / S

def person(frame, pr, cx, head_cy, R, expr="neutral", arms=("down", "down"), face=0, legs=False, dy=0.0):
    """Platziert die Figur so, dass der Kopfmittelpunkt bei (cx, head_cy) liegt."""
    key = (id(pr), int(R), expr, tuple(arms), face, legs)
    if key not in _cache: _cache[key] = _draw(pr, R, expr, arms, face, legs)
    im, ox, oy = _cache[key]
    frame.alpha_composite(im, (int(cx - ox), int(head_cy - oy + dy)))

BEZOS = P(skin=(234, 192, 160), shirt=(146, 190, 238), vest=(34, 42, 64), pants=(40, 44, 58), brow=(96, 80, 70), bezos=True)

YOU = P(skin=(240, 206, 176), shirt=(225, 120, 70), bald=False, hair=(92, 62, 42), brow=(80, 56, 40))
BANKER = P(skin=(236, 200, 170), shirt=(245, 245, 242), jacket=(52, 58, 76), tie=(170, 40, 50), bald=False, hair=(150, 150, 156), brow=(110, 110, 116), glasses=(40, 40, 46))
KID1 = P(skin=(236, 194, 162), shirt=(90, 170, 120), bald=False, hair=(70, 50, 38), brow=(70, 50, 38))
KID2 = P(skin=(236, 194, 162), shirt=(240, 190, 60), bald=False, hair=(120, 80, 50), brow=(90, 60, 40))

BEZOS_NOW = P(skin=(232, 188, 154), shirt=(30, 30, 34), tee=(30, 30, 34), pants=(40, 44, 58), brow=(58, 46, 40), bezos=True, aviators=True)

ELON = P(skin=(238, 200, 170), shirt=(24, 24, 28), tee=(24, 24, 28), jacket=(52, 54, 62), pants=(30, 30, 36), bald=False, hair=(74, 56, 42), brow=(66, 50, 38), quiff=True, elon=True)
