"""Apple-Logos fuer den Ron-Wayne-Short (eigene Nachzeichnungen im Crayon-Look):
der angebissene Apfel (mit herausnehmbarem 10-%-Stueck) und das erste Logo von 1976."""
import math, random
from apple_kit import S, shape, stroke, ellipse_pts, INK, SERIF
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from crayon_kit import SS

LOGO_GREY = (62, 64, 70)
SLICE_A = (-54, -18)      # 36 Grad = 10 Prozent

BODY = [(0, -0.62), (0.18, -0.70), (0.42, -0.74), (0.66, -0.66), (0.84, -0.50), (0.90, -0.38), (0.74, -0.26), (0.66, -0.06),
        (0.70, 0.12), (0.86, 0.24), (0.94, 0.30), (0.88, 0.52), (0.74, 0.76), (0.56, 0.94), (0.38, 1.0), (0.18, 0.96), (0, 0.9),
        (-0.18, 0.96), (-0.38, 1.0), (-0.56, 0.94), (-0.74, 0.76), (-0.88, 0.48), (-0.96, 0.18), (-0.96, -0.14), (-0.86, -0.44),
        (-0.66, -0.66), (-0.42, -0.74), (-0.18, -0.70)]
LEAF = [(0.0, -0.80), (0.06, -1.0), (0.2, -1.16), (0.42, -1.24), (0.40, -1.04), (0.28, -0.9), (0.1, -0.81)]

def smooth(pts, n=8):
    out = []; L = len(pts)
    for i in range(L):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % L], pts[(i + 2) % L]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out

def apple_logo_mask(size, cx, cy, r):
    m = Image.new("L", size, 0); d = ImageDraw.Draw(m)
    for poly in (BODY, LEAF):
        d.polygon([((cx + x * r) * SS, (cy + y * r) * SS) for x, y in smooth(poly)], fill=255)
    return m

def wedge_mask(size, cx, cy, r, a0, a1):
    m = Image.new("L", size, 0); ImageDraw.Draw(m).pieslice(S(cx - r * 2, cy - r * 2, cx + r * 2, cy + r * 2), a0, a1, fill=255); return m

def paste_logo(img, mask, color=LOGO_GREY):
    edge = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(int(5 * SS) | 1)), mask)
    img.paste(Image.new("RGB", img.size, INK), (0, 0), edge)
    img.paste(Image.new("RGB", img.size, color), (0, 0), mask)
    bb = mask.getbbox()
    if bb:
        hl = Image.new("L", img.size, 0)
        ImageDraw.Draw(hl).ellipse([bb[0] + (bb[2] - bb[0]) * 0.12, bb[1] + (bb[3] - bb[1]) * 0.18, bb[0] + (bb[2] - bb[0]) * 0.42, bb[1] + (bb[3] - bb[1]) * 0.55], fill=60)
        img.paste(Image.new("RGB", img.size, (255, 255, 255)), (0, 0), ImageChops.multiply(hl.filter(ImageFilter.GaussianBlur(12 * SS)), mask))

def apple_logo(img, cx, cy, r, slice_missing=True, color=LOGO_GREY):
    m = apple_logo_mask(img.size, cx, cy, r)
    if slice_missing: m = ImageChops.subtract(m, wedge_mask(img.size, cx, cy + r * 0.05, r, *SLICE_A))
    paste_logo(img, m, color)

def apple_logo_slice(img, cx, cy, r, color=LOGO_GREY):
    m = ImageChops.multiply(apple_logo_mask(img.size, cx, cy, r), wedge_mask(img.size, cx, cy + r * 0.05, r, *SLICE_A))
    paste_logo(img, m, color)

def logo_1976_v2(img, cx, cy, w, reveal=1.0):
    """Erstes Apple-Logo 1976 (Ron Wayne) im Stich-Stil: Newton liest unter dem Baum, ueber ihm leuchtet der Apfel,
    Zierrahmen mit umlaufender Wordsworth-Inschrift, Band APPLE COMPUTER CO. unten."""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay, "RGBA")
    h = w * 1.32; ink = (40, 40, 44); bark = (110, 100, 86)
    shape(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], (246, 240, 222), 1, lw=6)
    shape(d, [(cx - w * 0.43, cy - h * 0.44), (cx + w * 0.43, cy - h * 0.44), (cx + w * 0.43, cy + h * 0.3), (cx - w * 0.43, cy + h * 0.3)], (242, 236, 216), 2, lw=4)
    f = ImageFont.truetype(SERIF, int(w * 0.024 * SS))
    d.text((cx * SS, (cy - h * 0.47) * SS), "NEWTON ... A MIND FOREVER VOYAGING THROUGH STRANGE SEAS", font=f, fill=ink, anchor="mm")
    side = Image.new("RGBA", (int(h * 0.7 * SS), int(w * 0.05 * SS)), (0, 0, 0, 0))
    ImageDraw.Draw(side).text((side.width / 2, side.height / 2), "OF THOUGHT ... ALONE.   WILLIAM WORDSWORTH", font=f, fill=ink, anchor="mm")
    for ang, x in ((90, cx - w * 0.465), (-90, cx + w * 0.465)):
        s2 = side.rotate(ang, expand=True); lay.paste(s2, (int(x * SS - s2.width / 2), int((cy - h * 0.07) * SS - s2.height / 2)), s2)
    stroke(d, [(cx + w * 0.12, cy + h * 0.29), (cx + w * 0.1, cy + h * 0.05), (cx + w * 0.06, cy - h * 0.06)], lw=22, color=bark)
    stroke(d, [(cx + w * 0.1, cy + h * 0.0), (cx + w * 0.26, cy - h * 0.12)], lw=10, color=bark)
    stroke(d, [(cx + w * 0.08, cy - h * 0.03), (cx - w * 0.14, cy - h * 0.14)], lw=10, color=bark)
    crown = Image.new("L", img.size, 0); dcr = ImageDraw.Draw(crown); rnd = random.Random(8)
    for k in range(16):
        a = k / 16 * 6.28; x = cx + w * 0.04 + math.cos(a) * w * 0.24; y = cy - h * 0.22 + math.sin(a) * h * 0.12
        rr = w * rnd.uniform(0.1, 0.15); dcr.ellipse(S(x - rr, y - rr * 0.8, x + rr, y + rr * 0.8), fill=255)
    dcr.ellipse(S(cx - w * 0.24, cy - h * 0.36, cx + w * 0.32, cy - h * 0.08), fill=255)
    edge = ImageChops.subtract(crown.filter(ImageFilter.MaxFilter(int(4 * SS) | 1)), crown)
    lay.paste(Image.new("RGBA", img.size, (206, 204, 186, 255)), (0, 0), crown)
    hatch = Image.new("L", img.size, 0); dh = ImageDraw.Draw(hatch)
    for k in range(-40, 60):
        x0 = cx - w * 0.4 + k * w * 0.012
        dh.line(S(x0, cy - h * 0.4, x0 + w * 0.25, cy - h * 0.05), fill=110, width=int(2 * SS))
    lay.paste(Image.new("RGBA", img.size, (120, 120, 104, 255)), (0, 0), ImageChops.multiply(hatch, crown))
    lay.paste(Image.new("RGBA", img.size, (50, 50, 46, 255)), (0, 0), edge)
    d = ImageDraw.Draw(lay, "RGBA")
    ax, ay = cx - w * 0.06, cy - h * 0.07                    # leuchtender Apfel ueber Newtons Kopf
    for k, col in ((0.09, (246, 238, 206)), (0.065, (250, 238, 186)), (0.045, (252, 234, 160))):   # deckender Lichtschein
        d.ellipse(S(ax - w * k, ay - w * k, ax + w * k, ay + w * k), fill=col + (255,))
    shape(d, ellipse_pts(ax, ay, w * 0.03, w * 0.028), (210, 70, 50), 7, lw=3)
    stroke(d, [(ax, ay - w * 0.028), (ax + w * 0.01, ay - w * 0.06)], lw=3, color=ink)
    coat, skin, wig = (190, 186, 172), (236, 226, 208), (232, 230, 222)
    # Newton sitzt am Stamm (Ruecken rechts), Knie hoch, liest im Buch auf dem Schoss
    shape(d, [(cx + w * 0.08, cy + h * 0.06), (cx + w * 0.1, cy + h * 0.27), (cx - w * 0.06, cy + h * 0.27), (cx - w * 0.04, cy + h * 0.08)], coat, 4, lw=3)          # Oberkoerper/Mantel
    shape(d, [(cx - w * 0.04, cy + h * 0.25), (cx - w * 0.22, cy + h * 0.16), (cx - w * 0.25, cy + h * 0.19), (cx - w * 0.08, cy + h * 0.28)], coat, 5, lw=3)         # Oberschenkel (Knie oben)
    shape(d, [(cx - w * 0.22, cy + h * 0.16), (cx - w * 0.26, cy + h * 0.28), (cx - w * 0.21, cy + h * 0.285), (cx - w * 0.19, cy + h * 0.18)], (150, 146, 136), 6, lw=3)  # Unterschenkel
    shape(d, [(cx - w * 0.28, cy + h * 0.28), (cx - w * 0.19, cy + h * 0.28), (cx - w * 0.19, cy + h * 0.29), (cx - w * 0.28, cy + h * 0.29)], (60, 56, 52), 8, lw=2)   # Schuh
    shape(d, ellipse_pts(cx + w * 0.01, cy + h * 0.03, w * 0.075, w * 0.07, 30, 120, 420), wig, 9, lw=3)                                                      # Peruecke (Locken bis Schulter)
    for k in range(4): shape(d, ellipse_pts(cx + w * (0.05 + 0.005 * k), cy + h * (0.045 + k * 0.018), w * 0.025, w * 0.02), wig, 20 + k, lw=2)
    shape(d, ellipse_pts(cx - w * 0.02, cy + h * 0.035, w * 0.045, w * 0.05), skin, 10, lw=3)                                                               # Gesicht im Profil
    d.ellipse(S(cx - w * 0.045, cy + h * 0.025 - 3, cx - w * 0.038, cy + h * 0.025 + 3), fill=ink)
    stroke(d, [(cx - w * 0.06, cy + h * 0.035), (cx - w * 0.072, cy + h * 0.05), (cx - w * 0.058, cy + h * 0.055)], lw=2, color=ink)
    shape(d, [(cx - w * 0.2, cy + h * 0.14), (cx - w * 0.1, cy + h * 0.12), (cx - w * 0.09, cy + h * 0.15), (cx - w * 0.19, cy + h * 0.17)], (252, 250, 244), 11, lw=2)  # offenes Buch
    stroke(d, [(cx - w * 0.145, cy + h * 0.13), (cx - w * 0.14, cy + h * 0.16)], lw=2, color=ink)
    stroke(d, [(cx - w * 0.04, cy + h * 0.12), (cx - w * 0.12, cy + h * 0.14)], lw=6, color=coat)                                                             # Arm zum Buch
    for k in range(5): stroke(d, [(cx - w * 0.4, cy + h * (0.29 - k * 0.01)), (cx + w * 0.4, cy + h * (0.29 - k * 0.01))], lw=1, color=(150, 146, 130))
    shape(d, [(cx - w * 0.5, cy + h * 0.31), (cx + w * 0.5, cy + h * 0.31), (cx + w * 0.44, cy + h * 0.43), (cx - w * 0.44, cy + h * 0.43)], (236, 226, 198), 8, lw=4)
    shape(d, [(cx - w * 0.5, cy + h * 0.31), (cx - w * 0.58, cy + h * 0.37), (cx - w * 0.5, cy + h * 0.43), (cx - w * 0.44, cy + h * 0.43)], (220, 208, 178), 11, lw=3)
    shape(d, [(cx + w * 0.5, cy + h * 0.31), (cx + w * 0.58, cy + h * 0.37), (cx + w * 0.5, cy + h * 0.43), (cx + w * 0.44, cy + h * 0.43)], (220, 208, 178), 12, lw=3)
    fb = ImageFont.truetype(SERIF, int(w * 0.07 * SS))
    d.text((cx * SS, (cy + h * 0.37) * SS), "APPLE COMPUTER CO.", font=fb, fill=ink, anchor="mm")
    if reveal < 1:
        m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rectangle([0, 0, img.size[0], int((cy - h / 2 + h * reveal) * SS)], fill=255)
        lay.putalpha(ImageChops.multiply(lay.getchannel("A"), m))
    img.paste(lay, (0, 0), lay)
