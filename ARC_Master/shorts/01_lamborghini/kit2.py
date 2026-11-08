"""ARC-Kit v2: Figuren mit Kontur, Schattierung, Glanzlichtern; Stile A (Crayon), B (Neon), C (Noir)."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

SS = 2
W, H = 1080, 1920
F = "C:/Windows/Fonts/"

STYLES = {
    "A": dict(name="Crayon Clean", outline=(28, 24, 30), ow=5, wall=(244, 233, 214), wall2=(232, 216, 190),
              floor=(196, 150, 104), floor2=(176, 130, 88), shadow=(0, 0, 0, 60), text=(28, 24, 30), accent=(200, 40, 40), glow=False, grain=0),
    "B": dict(name="Neon Explainer", outline=None, ow=0, wall=(26, 18, 64), wall2=(58, 24, 98),
              floor=(20, 14, 50), floor2=(36, 20, 80), shadow=(0, 0, 0, 90), text=(255, 255, 255), accent=(255, 70, 140), glow=True, grain=0),
    "C": dict(name="ARC Noir", outline=(8, 10, 16), ow=3, wall=(10, 14, 24), wall2=(26, 34, 54),
              floor=(18, 22, 34), floor2=(8, 10, 18), shadow=(0, 0, 0, 120), text=(232, 200, 130), accent=(214, 176, 96), glow=False, grain=14),
}

def S(*v):
    return [x * SS for x in v]

def font(name, size):
    return ImageFont.truetype(F + name, int(size * SS))

def shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c[:3])

# ---------------- Hintergruende ----------------
def background(st, kind="office"):
    img = Image.new("RGB", (W * SS, H * SS), st["wall"])
    d = ImageDraw.Draw(img, "RGBA")
    fy = 1560
    for y in range(fy * SS):
        t = y / (fy * SS)
        d.line([(0, y), (W * SS, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(st["wall"], st["wall2"])))
    for y in range(fy * SS, H * SS):
        t = (y - fy * SS) / ((H - fy) * SS)
        d.line([(0, y), (W * SS, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(st["floor"], st["floor2"])))
    sname = st["name"]
    if kind == "office":
        if sname == "Crayon Clean":
            # Fenster mit Ausblick, Bilderrahmen, Holzleiste
            d.rounded_rectangle(S(90, 360, 470, 900), radius=10 * SS, fill=(170, 210, 235), outline=st["outline"], width=st["ow"] * SS)
            d.line(S(280, 360, 280, 900), fill=st["outline"], width=st["ow"] * SS)
            d.line(S(90, 630, 470, 630), fill=st["outline"], width=st["ow"] * SS)
            d.rectangle(S(640, 420, 960, 640), fill=(214, 186, 120), outline=st["outline"], width=st["ow"] * SS)
            d.rectangle(S(670, 450, 930, 610), fill=(200, 40, 40))
            d.rectangle(S(0, 1530, W, 1560), fill=(150, 104, 66))
        elif sname == "Neon Explainer":
            rnd = random.Random(5)
            for _ in range(70):
                x, y, r = rnd.randint(0, W), rnd.randint(0, 1400), rnd.choice([2, 3, 4])
                d.ellipse(S(x - r, y - r, x + r, y + r), fill=(255, 255, 255, rnd.randint(60, 200)))
            for k in range(6):
                d.line(S(0, 1560 + k * 70, W, 1560 + k * 70), fill=(120, 80, 255, 70), width=3 * SS)
            for x in range(-400, W + 400, 120):
                d.line(S(540, 1560, x, H), fill=(120, 80, 255, 50), width=2 * SS)
        else:
            # Noir: hohes Buerofenster mit Jalousie-Lichtstreifen
            d.rectangle(S(560, 240, 1000, 1100), fill=(22, 30, 48))
            for y in range(270, 1100, 55):
                d.rectangle(S(580, y, 980, y + 18), fill=(44, 56, 84))
            d.polygon(S(560, 1100, 1000, 1100, 860, 1560, 140, 1560), fill=(214, 176, 96, 22))
    return img

def post(img, st):
    img = img.resize((W, H), Image.LANCZOS)
    if st["glow"]:
        blur = img.filter(ImageFilter.GaussianBlur(18))
        img = ImageChops.screen(img, ImageChops.multiply(blur, Image.new("RGB", img.size, (110, 110, 110))))
    if st["grain"]:
        rnd = random.Random(1)
        noise = Image.effect_noise((W, H), 40).convert("RGB")
        img = Image.blend(img, ImageChops.overlay(img, noise), st["grain"] / 100)
        # Vignette
        v = Image.new("L", (W, H), 0)
        ImageDraw.Draw(v).ellipse([-W * 0.25, -H * 0.1, W * 1.25, H * 1.1], fill=255)
        v = v.filter(ImageFilter.GaussianBlur(160))
        img = Image.composite(img, Image.new("RGB", (W, H), (0, 0, 0)), v)
    return img

# ---------------- Figur ----------------
FERRUCCIO = dict(skin=(236, 192, 150), hair=(48, 34, 26), style="slick", mustache=True, glasses=False,
                 suit=(122, 84, 54), tie=(178, 40, 40), shirt=(245, 242, 235))
ENZO = dict(skin=(230, 188, 152), hair=(236, 236, 238), style="swept", mustache=False, glasses=True,
            suit=(34, 34, 42), tie=(150, 22, 22), shirt=(245, 242, 235))

def person(img, st, cx, base, h, p, expr="neutral", pose="down", face=1, talk=False):
    d = ImageDraw.Draw(img, "RGBA")
    o, ow = st["outline"], st["ow"] * SS
    neon = st["name"] == "Neon Explainer"
    u = h / 10.0
    hr = 1.85 * u
    hy = base - h + hr
    body_top, body_bot = hy + hr * 0.82, base - 2.1 * u
    bw = 2.9 * u
    def E(box, fill, sh=None):
        d.ellipse(S(*box), fill=fill, outline=o, width=ow if o else 0)
    def R(box, fill, r):
        d.rounded_rectangle(S(*box), radius=r * SS, fill=fill, outline=o, width=ow if o else 0)
    # Bodenschatten
    d.ellipse(S(cx - 2.2 * u, base - 0.35 * u, cx + 2.2 * u, base + 0.35 * u), fill=st["shadow"])
    # Beine + Schuhe
    for sx in (-0.6, 0.6):
        R((cx + sx * u - 0.5 * u, body_bot - 0.4 * u, cx + sx * u + 0.5 * u, base - 0.3 * u), shade(p["suit"], 0.82), 0.3 * u)
        R((cx + sx * u - 0.65 * u + face * 0.25 * u, base - 0.6 * u, cx + sx * u + 0.75 * u + face * 0.25 * u, base), (24, 22, 26), 0.3 * u)
    # Arme hinten
    sh_y = body_top + 0.75 * u
    poses = {"down": (10, 10), "cross": (60, 60), "proud": (28, 28), "point": (10, 112), "angry": (35, 35), "raise": (150, 150)}
    la, ra = poses[pose]
    if pose == "cross":
        la = 18
    def arm(sx, ang):
        x0 = cx + sx * (bw / 2 - 0.3 * u)
        a = math.radians(ang)
        L = 2.7 * u
        x1, y1 = x0 + math.sin(a) * L * sx, sh_y + math.cos(a) * L
        if o:
            d.line(S(x0, sh_y, x1, y1), fill=o, width=int(0.85 * u * SS + 2 * ow))
        d.line(S(x0, sh_y, x1, y1), fill=shade(p["suit"], 0.9), width=int(0.85 * u * SS))
        E((x1 - 0.45 * u, y1 - 0.45 * u, x1 + 0.45 * u, y1 + 0.45 * u), p["skin"])
    arm(-1, la)
    # Torso mit Revers und Lichtkante
    R((cx - bw / 2, body_top, cx + bw / 2, body_bot), p["suit"], 1.1 * u)
    d.rounded_rectangle(S(cx + face * 0.2 * bw - bw * 0.3, body_top + 0.25 * u, cx + face * 0.2 * bw + bw * 0.3, body_bot - 0.3 * u),
                        radius=0.9 * u * SS, fill=shade(p["suit"], 1.12) + (90,))
    d.polygon(S(cx - 0.7 * u, body_top + 0.05 * u, cx + 0.7 * u, body_top + 0.05 * u, cx, body_top + 1.9 * u), fill=p["shirt"])
    d.polygon(S(cx - 0.75 * u, body_top + 0.05 * u, cx - 0.15 * u, body_top + 2.0 * u, cx - 1.05 * u, body_top + 0.9 * u), fill=shade(p["suit"], 0.75))
    d.polygon(S(cx + 0.75 * u, body_top + 0.05 * u, cx + 0.15 * u, body_top + 2.0 * u, cx + 1.05 * u, body_top + 0.9 * u), fill=shade(p["suit"], 0.75))
    d.polygon(S(cx - 0.2 * u, body_top + 0.25 * u, cx + 0.2 * u, body_top + 0.25 * u, cx + 0.28 * u, body_top + 1.6 * u,
                cx, body_top + 1.95 * u, cx - 0.28 * u, body_top + 1.6 * u), fill=p["tie"], outline=o, width=max(1, ow // 2) if o else 0)
    if pose == "cross":   # verschraenkte Arme: Unterarme quer vor der Brust
        fy = body_top + 2.3 * u
        for k, dy in ((1, 0), (-1, 0.5 * u)):
            if o:
                d.line(S(cx - bw * 0.48, fy + dy, cx + bw * 0.48, fy + dy), fill=o, width=int(0.8 * u * SS + 2 * ow))
            d.line(S(cx - bw * 0.48, fy + dy, cx + bw * 0.48, fy + dy), fill=shade(p["suit"], 0.95 + 0.08 * k), width=int(0.8 * u * SS))
        E((cx + bw * 0.42 - 0.4 * u, fy - 0.4 * u, cx + bw * 0.42 + 0.4 * u, fy + 0.4 * u), p["skin"])
    else:
        arm(1, ra)
    # Kopf: Ohr, Kopf, Wangen
    ear_x = cx - face * hr * 0.92
    E((ear_x - 0.4 * u, hy - 0.1 * u, ear_x + 0.4 * u, hy + 0.7 * u), shade(p["skin"], 0.95))
    E((cx - hr, hy - hr, cx + hr, hy + hr), p["skin"])
    d.ellipse(S(cx - hr * 0.95, hy - hr * 0.2, cx + hr * 0.95, hy + hr * 0.98), fill=shade(p["skin"], 0.93) + (110,))
    ex, ey = cx + face * hr * 0.3, hy + hr * 0.05
    d.ellipse(S(ex + face * 0.9 * u - 0.32 * u, ey + 0.35 * u, ex + face * 0.9 * u + 0.32 * u, ey + 0.7 * u), fill=(230, 120, 110, 70))
    # Haare
    hc = p["hair"]
    if p["style"] == "slick":
        d.chord(S(cx - hr * 1.04, hy - hr * 1.1, cx + hr * 1.04, hy + hr * 0.5), 180, 360, fill=hc, outline=o, width=ow if o else 0)
        d.chord(S(cx - hr * 0.9, hy - hr * 1.0, cx + hr * 0.6, hy - hr * 0.2), 190, 330, fill=shade(hc, 1.6))
    else:
        # zurueckgekaemmtes Haar: Kappe + Volumen nach hinten (gegen Blickrichtung)
        back = cx - face * hr * 0.35
        d.chord(S(cx - hr * 1.05, hy - hr * 1.12, cx + hr * 1.05, hy + hr * 0.35), 180, 360, fill=hc, outline=o, width=ow if o else 0)
        d.chord(S(back - hr * 0.85, hy - hr * 1.2, back + hr * 0.85, hy - hr * 0.1), 180, 360, fill=hc)
        for k in range(3):
            yy = hy - hr * (0.85 - k * 0.22)
            d.arc(S(cx - hr * 0.9, yy - hr * 0.3, cx + hr * 0.9, yy + hr * 0.3), 200, 340, fill=shade(hc, 0.82), width=3 * SS)
    # Augen
    if p["glasses"]:
        for k in (-1, 1):
            d.rounded_rectangle(S(ex + k * 0.6 * u - 0.55 * u, ey - 0.4 * u, ex + k * 0.6 * u + 0.55 * u, ey + 0.35 * u),
                                radius=10 * SS, fill=(14, 14, 20), outline=(60, 60, 70) if not o else o, width=3 * SS)
            d.line(S(ex + k * 0.6 * u - 0.35 * u, ey - 0.25 * u, ex + k * 0.6 * u - 0.1 * u, ey - 0.3 * u), fill=(255, 255, 255, 150), width=3 * SS)
        d.line(S(ex - 0.1 * u, ey - 0.2 * u, ex + 0.1 * u, ey - 0.2 * u), fill=(14, 14, 20), width=5 * SS)
    else:
        for k in (-1, 1):
            d.ellipse(S(ex + k * 0.6 * u - 0.32 * u, ey - 0.3 * u, ex + k * 0.6 * u + 0.32 * u, ey + 0.3 * u), fill=(255, 255, 255), outline=o, width=max(1, ow // 2) if o else 0)
            px = ex + k * 0.6 * u + face * 0.08 * u
            d.ellipse(S(px - 0.16 * u, ey - 0.17 * u, px + 0.16 * u, ey + 0.17 * u), fill=(30, 24, 22))
            d.ellipse(S(px - 0.08 * u, ey - 0.13 * u, px + 0.0 * u, ey - 0.05 * u), fill=(255, 255, 255))
    bc = (200, 200, 205) if hc[0] > 200 else hc
    tilt = {"neutral": 0, "angry": 0.28, "smug": -0.12, "shock": -0.3, "proud": -0.05}[expr]
    for k in (-1, 1):
        inner = ex + k * 0.25 * u
        outer = ex + k * 0.95 * u
        d.line(S(inner, ey - 0.62 * u + tilt * u, outer, ey - 0.72 * u - tilt * 0.4 * u), fill=bc, width=int(0.2 * u * SS))
    # Nase, Mund
    nx = ex + face * 0.25 * u
    d.ellipse(S(nx - 0.22 * u, ey + 0.2 * u, nx + 0.22 * u, ey + 0.62 * u), fill=shade(p["skin"], 0.85))
    my = ey + 1.05 * u
    if p["mustache"]:
        d.chord(S(ex - 0.8 * u, my - 0.5 * u, ex + 0.8 * u, my + 0.22 * u), 180, 360, fill=hc, outline=o, width=max(1, ow // 2) if o else 0)
    lw = int(0.15 * u * SS)
    if talk:
        d.ellipse(S(ex - 0.32 * u, my - 0.02 * u, ex + 0.32 * u, my + 0.5 * u), fill=(110, 36, 40), outline=o, width=max(1, ow // 2) if o else 0)
    elif expr == "smug":
        d.arc(S(ex - 0.2 * u, my - 0.35 * u, ex + 0.65 * u, my + 0.25 * u), 10, 120, fill=(40, 30, 30), width=lw)
    elif expr == "proud":
        d.arc(S(ex - 0.5 * u, my - 0.45 * u, ex + 0.5 * u, my + 0.25 * u), 20, 160, fill=(40, 30, 30), width=lw)
    elif expr == "angry":
        d.arc(S(ex - 0.45 * u, my + 0.05 * u, ex + 0.45 * u, my + 0.6 * u), 200, 340, fill=(40, 30, 30), width=lw)
    else:
        d.line(S(ex - 0.32 * u, my + 0.12 * u, ex + 0.32 * u, my + 0.12 * u), fill=(40, 30, 30), width=lw)
    if neon:   # Randlicht
        d.arc(S(cx - hr, hy - hr, cx + hr, hy + hr), 290, 360, fill=(255, 90, 180, 200), width=6 * SS)

# ---------------- Requisiten ----------------
def car(img, st, x, y, w, color, face=1, low=False):
    d = ImageDraw.Draw(img, "RGBA")
    o, ow = st["outline"], st["ow"] * SS
    h = w * (0.24 if low else 0.3)
    pts = ([(0, .35), (.18, .62), (.42, 1), (.68, .95), (.95, .55), (1, .2), (1, 0), (0, 0)] if low else
           [(0, .4), (.12, .58), (.35, .62), (.48, 1), (.72, .98), (.86, .6), (1, .45), (1, 0), (0, 0)])
    pts = [((x + (px if face == 1 else 1 - px) * w) * SS, (y - py * h) * SS) for px, py in pts]
    d.ellipse(S(x - 0.05 * w, y - 0.06 * h, x + 1.05 * w, y + 0.12 * h), fill=st["shadow"])
    d.polygon(pts, fill=color, outline=o, width=ow if o else 0)
    d.polygon(S(x + .1 * w, y - .5 * h, x + .9 * w, y - .5 * h, x + .9 * w, y - .42 * h, x + .1 * w, y - .42 * h), fill=shade(color, 1.25) + (140,))
    wa, wb = (.44, .7) if face == 1 else (.3, .56)
    d.polygon(S(x + wa * w, y - .62 * h, x + (wa + .06) * w, y - .9 * h, x + (wb - .02) * w, y - .88 * h, x + (wb + .06) * w, y - .62 * h),
              fill=(160, 200, 230), outline=o, width=max(1, ow // 2) if o else 0)
    for cxw in (x + .2 * w, x + .8 * w):
        r = h * .3
        d.ellipse(S(cxw - r, y - r, cxw + r, y + r), fill=(20, 20, 24), outline=o, width=ow if o else 0)
        d.ellipse(S(cxw - r * .5, y - r * .5, cxw + r * .5, y + r * .5), fill=(170, 170, 180))
    if st["glow"]:
        d.line(S(x + .02 * w, y - .41 * h, x + .98 * w, y - .41 * h), fill=(255, 255, 255, 120), width=4 * SS)

def bubble(img, st, x, y, w, lines, tail):
    d = ImageDraw.Draw(img, "RGBA")
    o = st["outline"] or (255, 255, 255)
    f = font("georgiab.ttf" if st["name"] != "Neon Explainer" else "segoeuib.ttf", 46)
    lh = 60
    h = lh * len(lines) + 56
    fill = (255, 255, 255) if st["name"] != "ARC Noir" else (244, 236, 218)
    d.polygon(S(x + w * .35, y + h - 6, x + w * .52, y + h - 6, *tail), fill=fill, outline=o if st["outline"] else None)
    d.rounded_rectangle(S(x, y, x + w, y + h), radius=40 * SS, fill=fill, outline=o if st["outline"] else None, width=st["ow"] * SS)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f) / SS
        d.text(S(x + (w - tw) / 2, y + 28 + i * lh), ln, font=f, fill=(20, 18, 24))

def title(img, st, cx, cy, text, size=70):
    d = ImageDraw.Draw(img, "RGBA")
    f = font("georgiab.ttf" if st["name"] != "Neon Explainer" else "segoeuib.ttf", size)
    tw = d.textlength(text, font=f) / SS
    if st["name"] == "Crayon Clean":
        d.rounded_rectangle(S(cx - tw / 2 - 30, cy - size * .7, cx + tw / 2 + 30, cy + size * .75), radius=18 * SS, fill=(255, 255, 255), outline=st["outline"], width=st["ow"] * SS)
    d.text(S(cx - tw / 2, cy - size * .6), text, font=f, fill=st["text"])

# ---------------- Zwei Testszenen ----------------
def hook(st):
    img = background(st)
    person(img, st, 290, 1500, 900, FERRUCCIO, "angry", "down", face=1)
    person(img, st, 790, 1500, 1000, ENZO, "smug", "cross", face=-1)
    car(img, st, 120, 1840, 840, (200, 30, 36), face=1)
    title(img, st, 540, 250, "FERRARI vs LAMBORGHINI", 62)
    return post(img, st)

def insult(st):
    img = background(st)
    d = ImageDraw.Draw(img)
    person(img, st, 640, 1640, 1180, ENZO, "smug", "cross", face=-1, talk=True)
    o = st["outline"]
    d.rounded_rectangle(S(260, 1330, 1080, 1700), radius=16 * SS, fill=(86, 56, 36) if st["name"] != "Neon Explainer" else (70, 30, 120),
                        outline=o, width=st["ow"] * SS if o else 0)
    bubble(img, st, 50, 210, 720, ["You may be able to", "drive a tractor…", "but you'll never", "handle a Ferrari."], (520, 700))
    return post(img, st)

if __name__ == "__main__":
    out = []
    for key in "ABC":
        st = STYLES[key]
        a, b = hook(st), insult(st)
        a.save(f"stil_{key}_hook.png"); b.save(f"stil_{key}_insult.png")
        out += [(key, st["name"], a, b)]
    tw, th = 360, 640
    sheet = Image.new("RGB", (3 * (2 * tw + 30) + 20, th + 110), (0, 0, 0))
    dd = ImageDraw.Draw(sheet)
    ff = ImageFont.truetype(F + "segoeuib.ttf", 40)
    for i, (key, name, a, b) in enumerate(out):
        x0 = 10 + i * (2 * tw + 30)
        dd.text((x0, 20), f"{key}  {name}", font=ff, fill=(255, 255, 255))
        sheet.paste(a.resize((tw, th)), (x0, 90)); sheet.paste(b.resize((tw, th)), (x0 + tw + 10, 90))
    sheet.save("STILVERGLEICH.png")
    print("ok")
