"""ARC-Kit v3: Cartoon mit echter Aehnlichkeit und echten Orten.
Hintergruende: lizenzierte Fotos nur als Vorlage -> stark stilisiert (flache Farbflaechen + Tusche-Linien).
Figuren: halbrealistische Proportionen (Kopf ~1/5), Karikatur-Merkmale der echten Personen."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops

SS = 2
W, H = 1080, 1920
F = "C:/Windows/Fonts/"
INK = (22, 18, 20)

def S(*v): return [x * SS for x in v]
def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3])

# ---------------- Cartoon-Hintergrund aus Vorlage ----------------
def toon_bg(path, fx=0.5, fy=0.5, colors=7, warm=(1.08, 1.0, 0.9), sat=0.9, line=3):
    src = Image.open(path).convert("RGB")
    s = max(W / src.width, H / src.height)
    src = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.LANCZOS)
    x, y = int((src.width - W) * fx), int((src.height - H) * fy)
    src = src.crop((x, y, x + W, y + H))
    smooth = src.filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.MedianFilter(7))
    flat = smooth.quantize(colors=colors, method=Image.Quantize.MEDIANCUT).convert("RGB")
    flat = flat.filter(ImageFilter.ModeFilter(9))
    flat = ImageEnhance.Color(flat).enhance(sat)
    r, g, b = flat.split()
    flat = Image.merge("RGB", tuple(ch.point(lambda v, k=k: min(255, int(v * k))) for ch, k in zip((r, g, b), warm)))
    # Tusche-Linien aus Kanten der Flaechen
    edges = ImageOps.grayscale(flat).filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 18 else 0)
    edges = edges.filter(ImageFilter.MaxFilter(line))
    ink = Image.new("RGB", (W, H), INK)
    out = Image.composite(ink, flat, edges)
    # leicht abdunkeln und weichzeichnen, damit Figuren davor stehen (Tiefe)
    out = out.filter(ImageFilter.GaussianBlur(1.2))
    out = ImageEnhance.Brightness(out).enhance(0.82)
    return out.resize((W * SS, H * SS), Image.LANCZOS)

# ---------------- Figuren ----------------
ENZO = dict(skin=(232, 190, 158), hair=(240, 240, 242), shirt=(238, 236, 228), tie=(150, 110, 80), suit=None,
            braces=(90, 60, 40), trousers=(70, 70, 78), glasses=True, mustache=False, nose=1.35, jowl=True, build=1.12, hairstyle="swept")
FERRUCCIO = dict(skin=(226, 180, 140), hair=(36, 28, 24), shirt=(236, 232, 222), tie=None, suit=(150, 138, 112),
                 braces=None, trousers=(60, 58, 64), glasses=False, mustache=True, nose=1.0, jowl=False, build=1.0, hairstyle="wavy")

def person(img, cx, base, h, p, face=1, expr="neutral", pose="down", talk=False):
    d = ImageDraw.Draw(img, "RGBA")
    ow = 4 * SS
    hh = h * 0.19                       # Kopfhoehe
    hw = hh * 0.78 * (1.08 if p["jowl"] else 1.0)
    hy = base - h + hh * 0.55           # Kopfmitte
    neck = hy + hh * 0.5
    sw = h * 0.27 * p["build"]          # Schulterbreite
    waist = base - h * 0.47
    hip_w = sw * 0.82
    def poly(pts, fill, o=True):
        d.polygon([(a * SS, b * SS) for a, b in pts], fill=fill, outline=INK if o else None, width=ow if o else 0)
    def E(box, fill, o=True):
        d.ellipse(S(*box), fill=fill, outline=INK if o else None, width=ow if o else 0)
    # Schatten
    d.ellipse(S(cx - sw * 0.7, base - 10, cx + sw * 0.7, base + 14), fill=(0, 0, 0, 90))
    # Beine
    for sx in (-1, 1):
        lx = cx + sx * hip_w * 0.24
        poly([(lx - hip_w * 0.2, waist), (lx + hip_w * 0.2, waist), (lx + hip_w * 0.17, base - 22), (lx - hip_w * 0.17, base - 22)], p["trousers"])
        E((lx - hip_w * 0.22 + face * 8, base - 34, lx + hip_w * 0.26 + face * 8, base + 2), (30, 24, 22))
    top = p["suit"] or p["shirt"]
    # hinterer Arm
    def arm(sx, ang, elbow=20):
        x0, y0 = cx + sx * sw * 0.46, neck + hh * 0.42
        a = math.radians(ang); L1, L2 = h * 0.17, h * 0.16
        ex_, ey_ = x0 + sx * math.sin(a) * L1, y0 + math.cos(a) * L1
        b = math.radians(ang + elbow * sx * 0 + elbow)
        hx, hy_ = ex_ + sx * math.sin(b) * L2, ey_ + math.cos(b) * L2
        for (p0, p1) in (((x0, y0), (ex_, ey_)), ((ex_, ey_), (hx, hy_))):
            d.line(S(*p0, *p1), fill=INK, width=int(h * 0.075 * SS + 2 * ow))
            d.line(S(*p0, *p1), fill=sh(top, 0.92), width=int(h * 0.075 * SS))
        E((hx - h * 0.034, hy_ - h * 0.03, hx + h * 0.034, hy_ + h * 0.04), p["skin"])
    poses = {"down": (8, 8), "hips": (40, 40), "point": (8, 100), "gesture": (8, 60), "fold": (25, 25)}
    la, ra = poses[pose]
    arm(-1, la)
    # Torso
    poly([(cx - sw / 2, neck + hh * 0.35), (cx + sw / 2, neck + hh * 0.35), (cx + hip_w / 2, waist + 8), (cx - hip_w / 2, waist + 8)], top)
    # Kragen / Hemd / Krawatte / Hosentraeger / Sakko-Revers
    poly([(cx - hh * 0.32, neck + hh * 0.1), (cx + hh * 0.32, neck + hh * 0.1), (cx, neck + hh * 0.75)], p["shirt"])
    if p["suit"]:
        poly([(cx - hh * 0.34, neck + hh * 0.12), (cx - hh * 0.05, neck + hh * 1.3), (cx - sw * 0.32, neck + hh * 0.6)], sh(p["suit"], 0.8))
        poly([(cx + hh * 0.34, neck + hh * 0.12), (cx + hh * 0.05, neck + hh * 1.3), (cx + sw * 0.32, neck + hh * 0.6)], sh(p["suit"], 0.8))
        poly([(cx - hh * 0.28, neck + hh * 0.12), (cx + hh * 0.28, neck + hh * 0.12), (cx, neck + hh * 0.9)], p["shirt"])
    if p["braces"]:
        for sx in (-1, 1):
            d.line(S(cx + sx * sw * 0.3, neck + hh * 0.4, cx + sx * hip_w * 0.28, waist + 4), fill=p["braces"], width=int(h * 0.016 * SS))
    if p["tie"]:
        poly([(cx - hh * 0.07, neck + hh * 0.2), (cx + hh * 0.07, neck + hh * 0.2), (cx + hh * 0.11, waist - hh * 0.5), (cx, waist - hh * 0.3), (cx - hh * 0.11, waist - hh * 0.5)], p["tie"])
    d.line(S(cx, neck + hh * 0.8, cx, waist), fill=sh(top, 0.85), width=2 * SS)
    arm(1, ra)
    # Hals
    poly([(cx - hh * 0.2, neck - hh * 0.1), (cx + hh * 0.2, neck - hh * 0.1), (cx + hh * 0.22, neck + hh * 0.2), (cx - hh * 0.22, neck + hh * 0.2)], sh(p["skin"], 0.9))
    # Kopf (Ohr, Schaedel, Kiefer)
    ex = cx + face * hw * 0.16
    E((cx - face * hw * 0.48 - hh * 0.09, hy - hh * 0.05, cx - face * hw * 0.48 + hh * 0.09, hy + hh * 0.2), sh(p["skin"], 0.95))
    E((cx - hw / 2, hy - hh / 2, cx + hw / 2, hy + hh * 0.42), p["skin"])
    if p["jowl"]:
        E((cx - hw * 0.5, hy - hh * 0.05, cx + hw * 0.5, hy + hh * 0.52), p["skin"])
        d.ellipse(S(cx - hw * 0.46, hy - hh * 0.1, cx + hw * 0.46, hy + hh * 0.48), fill=p["skin"])
    # Haare
    hc = p["hair"]
    if p["hairstyle"] == "swept":   # Enzo: weisses, nach hinten gekaemmtes Haar mit Volumen
        d.chord(S(cx - hw * 0.53, hy - hh * 0.72, cx + hw * 0.53, hy + hh * 0.05), 180, 360, fill=hc, outline=INK, width=ow)
        d.pieslice(S(cx - face * hw * 0.2 - hw * 0.5, hy - hh * 0.62, cx - face * hw * 0.2 + hw * 0.5, hy + hh * 0.1), 180 if face == 1 else 270, 270 if face == 1 else 360, fill=hc)
        for k in range(4):
            yy = hy - hh * (0.5 - k * 0.1)
            d.arc(S(cx - hw * 0.45, yy - hh * 0.15, cx + hw * 0.45, yy + hh * 0.15), 200, 330, fill=(190, 190, 196), width=2 * SS)
    else:                           # Ferruccio: dunkles, welliges, nach hinten gekaemmtes Haar
        d.chord(S(cx - hw * 0.52, hy - hh * 0.62, cx + hw * 0.52, hy + hh * 0.08), 180, 360, fill=hc, outline=INK, width=ow)
        for k in range(3):
            xx = cx - hw * 0.3 + k * hw * 0.3
            d.arc(S(xx - hw * 0.18, hy - hh * 0.58, xx + hw * 0.18, hy - hh * 0.3), 200, 340, fill=sh(hc, 2.2), width=3 * SS)
    # Augen / Brille
    eyy = hy - hh * 0.02
    if p["glasses"]:
        for k in (-1, 1):
            gx = ex + k * hw * 0.2
            d.rounded_rectangle(S(gx - hw * 0.17, eyy - hh * 0.09, gx + hw * 0.17, eyy + hh * 0.08), radius=6 * SS, fill=(28, 30, 34), outline=INK, width=3 * SS)
            d.line(S(gx - hw * 0.12, eyy - hh * 0.06, gx - hw * 0.03, eyy - hh * 0.07), fill=(150, 160, 170), width=2 * SS)
        d.line(S(ex - hw * 0.04, eyy - hh * 0.05, ex + hw * 0.04, eyy - hh * 0.05), fill=INK, width=4 * SS)
        d.line(S(ex - face * hw * 0.37, eyy - hh * 0.04, cx - face * hw * 0.48, eyy - hh * 0.01), fill=INK, width=3 * SS)
    else:
        for k in (-1, 1):
            gx = ex + k * hw * 0.2
            d.ellipse(S(gx - hw * 0.07, eyy - hh * 0.045, gx + hw * 0.07, eyy + hh * 0.045), fill=(250, 248, 244), outline=INK, width=2 * SS)
            d.ellipse(S(gx + face * hw * 0.015 - hw * 0.035, eyy - hh * 0.035, gx + face * hw * 0.015 + hw * 0.035, eyy + hh * 0.035), fill=(40, 30, 26))
    # Brauen
    tilt = {"neutral": 0, "angry": 0.05, "smug": -0.03, "shock": -0.06, "proud": -0.01}[expr]
    bc = (200, 200, 204) if hc[0] > 200 else hc
    for k in (-1, 1):
        gx = ex + k * hw * 0.2
        inner, outer = gx - k * hw * 0.08, gx + k * hw * 0.1
        d.line(S(inner, eyy - hh * (0.13 - tilt), outer, eyy - hh * (0.15 + tilt * 0.3)), fill=bc, width=int(hh * 0.035 * SS))
    # Nase (Enzo: gross)
    nl = hh * 0.17 * p["nose"]
    poly([(ex + face * hw * 0.02, eyy), (ex + face * hw * 0.02 + face * nl * 0.55, eyy + nl), (ex + face * hw * 0.02 - face * nl * 0.1, eyy + nl)], sh(p["skin"], 0.88))
    # Mund / Schnurrbart
    my = eyy + nl + hh * 0.1
    if p["mustache"]:
        d.chord(S(ex - hw * 0.2, my - hh * 0.1, ex + hw * 0.22, my + hh * 0.04), 180, 360, fill=hc, outline=INK, width=2 * SS)
    lw = int(hh * 0.03 * SS)
    if talk:
        d.ellipse(S(ex - hw * 0.09, my, ex + hw * 0.09, my + hh * 0.09), fill=(110, 40, 40), outline=INK, width=2 * SS)
    elif expr == "smug":
        d.arc(S(ex - hw * 0.05, my - hh * 0.05, ex + hw * 0.18, my + hh * 0.06), 0, 140, fill=INK, width=lw)
    elif expr == "angry":
        d.arc(S(ex - hw * 0.12, my + hh * 0.02, ex + hw * 0.12, my + hh * 0.12), 200, 340, fill=INK, width=lw)
    else:
        d.line(S(ex - hw * 0.1, my + hh * 0.04, ex + hw * 0.1, my + hh * 0.04), fill=INK, width=lw)
    if p["jowl"]:
        d.arc(S(ex - hw * 0.3, my - hh * 0.1, ex - hw * 0.12, my + hh * 0.12), 100, 200, fill=sh(p["skin"], 0.8), width=2 * SS)

def caption(img, text, y=170, size=58):
    d = ImageDraw.Draw(img, "RGBA")
    f = ImageFont.truetype(F + "georgiab.ttf", size * SS)
    tw = d.textlength(text, font=f) / SS
    d.rounded_rectangle(S(W / 2 - tw / 2 - 30, y - size * 0.75, W / 2 + tw / 2 + 30, y + size * 0.8), radius=14 * SS, fill=(250, 244, 230), outline=INK, width=4 * SS)
    d.text(S(W / 2 - tw / 2, y - size * 0.6), text, font=f, fill=INK)

def done(img):
    return img.resize((W, H), Image.LANCZOS)

if __name__ == "__main__":
    # Test 1: Ferruccio vor seiner Traktorfabrik (Vorlage: Ferruccio_lamborghini.jpg / Traktor 1960)
    a = toon_bg("assets/tractor_1960.jpg", fx=0.5, fy=0.55)
    person(a, 360, 1820, 1150, FERRUCCIO, face=1, expr="proud", pose="hips")
    caption(a, "ITALY, 1948")
    a = done(a); a.save("E_test_1.png")
    # Test 2: Enzo vor der Ferrari-Fabrik in Maranello
    b = toon_bg("assets/maranello.jpg", fx=0.42, fy=0.5)
    person(b, 620, 1840, 1300, ENZO, face=-1, expr="smug", pose="down", talk=True)
    caption(b, "MARANELLO")
    b = done(b); b.save("E_test_2.png")
    sheet = Image.new("RGB", (2 * 540 + 30, 960 + 20), (0, 0, 0))
    sheet.paste(a.resize((540, 960)), (10, 10)); sheet.paste(b.resize((540, 960)), (560, 10))
    sheet.save("STIL_E_TEST.png"); print("ok")
