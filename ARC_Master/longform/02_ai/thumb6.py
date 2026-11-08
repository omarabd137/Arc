"""Thumbnail #02 v6 - Vektor-Stil mit Glow (Qualitaetsklasse Kurzgesagt, eigenes Motiv):
Riesige KI-Gestalt aus Licht ueber der naechtlichen Stadt, rote Augen, haelt winzige Menschen an leuchtenden Faeden (Marionetten).
Ein starker Spruch oben."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
S = 2; W, H = 1920 * S, 1080 * S
FONT = "C:/Windows/Fonts/ariblk.ttf"
TEXT = "IT'S AWAKE"

def X(v): return int(v * S)
def new(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))
def mask(): return Image.new("L", (W, H), 0)
def vgrad(y0, y1, c0, c1):
    ys = np.clip((np.arange(H)[:, None] - X(y0)) / max(1, X(y1) - X(y0)), 0, 1)
    a = np.array(c0, float); b = np.array(c1, float)
    arr = (a + (b - a) * ys[..., None]).repeat(W, 1).reshape(H, W, len(c0))
    return Image.fromarray(arr.astype(np.uint8), "RGBA" if len(c0) == 4 else "RGB")
def fill(m, img_or_col):
    src = img_or_col if isinstance(img_or_col, Image.Image) else Image.new("RGBA", (W, H), img_or_col)
    out = new(); out.paste(src.convert("RGBA"), (0, 0), m); return out
def glow(m, col, rad, gain=1.0):
    b = m.filter(ImageFilter.GaussianBlur(X(rad)))
    if gain != 1.0: b = b.point(lambda v: min(255, int(v * gain)))
    out = Image.new("RGBA", (W, H), col); out.putalpha(b); return out
def rim(m, col, width, rad):
    inner = m.filter(ImageFilter.GaussianBlur(X(width))).point(lambda v: 255 if v > 200 else 0)
    edge = ImageChops.subtract(m, inner); return glow(edge, col, rad, 2.2), fill(edge, col)

img = vgrad(0, 1080, (16, 14, 60, 255), (70, 20, 110, 255))
r = random.Random(5)
# --- vertikale Lichtstreifen
streaks = new(); d = ImageDraw.Draw(streaks)
for k in range(26):
    x = r.randint(0, 1920); w = r.randint(6, 26); y0 = r.randint(-200, 300); y1 = y0 + r.randint(300, 900)
    col = (90, 220, 255, r.randint(40, 110)) if k % 3 else (220, 90, 255, r.randint(40, 90))
    d.rounded_rectangle([X(x), X(y0), X(x + w), X(y1)], X(w / 2), fill=col)
img.alpha_composite(streaks.filter(ImageFilter.GaussianBlur(X(6))))
# --- Stadt unten
city = mask(); dc = ImageDraw.Draw(city); x = -20; wins = []
while x < 1940:
    bw = r.randint(60, 140); bh = r.randint(90, 260); dc.rectangle([X(x), X(1080 - bh), X(x + bw), H], fill=255)
    for wy in range(1080 - bh + 14, 1070, 22):
        for wx in range(x + 10, x + bw - 10, 18):
            if r.random() < 0.35: wins.append((wx, wy))
    x += bw + r.randint(2, 10)
img.alpha_composite(fill(city, (14, 10, 40, 255)))
wl = new(); dw = ImageDraw.Draw(wl)
for wx, wy in wins: dw.rectangle([X(wx), X(wy), X(wx + 7), X(wy + 9)], fill=(255, 210, 120, 230))
img.alpha_composite(wl)
# --- Riesige KI-Gestalt (Kopf + Schultern), Verlauf + Lichtkante
fig = mask(); df = ImageDraw.Draw(fig)
cx = 960
df.ellipse([X(cx - 165), X(150), X(cx + 165), X(520)], fill=255)                  # Kopf
df.polygon([(X(cx - 120), X(470)), (X(cx + 120), X(470)), (X(cx + 520), X(820)), (X(cx + 700), X(1080)), (X(cx - 700), X(1080)), (X(cx - 520), X(820))], fill=255)
df.ellipse([X(cx - 470), X(600), X(cx - 250), X(860)], fill=255); df.ellipse([X(cx + 250), X(600), X(cx + 470), X(860)], fill=255)   # Schultern
fig = fig.filter(ImageFilter.GaussianBlur(X(2)))
body = vgrad(140, 1000, (96, 70, 200, 255), (18, 8, 48, 255))
fade = vgrad(700, 1080, (255,), (110,)).convert("L") if False else None
img.alpha_composite(glow(fig, (120, 90, 255), 60, 0.9))
img.alpha_composite(fill(fig, body))
g1, e1 = rim(fig, (130, 240, 255), 5, 10); img.alpha_composite(g1); img.alpha_composite(e1)
# Nebel unten ueber Koerper + Stadt
fog = vgrad(760, 1080, (60, 20, 110, 0), (90, 30, 140, 230)); img.alpha_composite(fog)
# --- Gesicht: dunkles Visier + rote Augen
vis = mask(); ImageDraw.Draw(vis).ellipse([X(cx - 120), X(255), X(cx + 120), X(430)], fill=255)
img.alpha_composite(fill(vis.filter(ImageFilter.GaussianBlur(X(1.5))), (10, 6, 28, 255)))
eyes = mask(); de = ImageDraw.Draw(eyes)
for sx in (-1, 1):
    ex = cx + sx * 58; o = ex + sx * 46; i_ = ex - sx * 40
    de.polygon([(X(o), X(312)), (X(i_), X(346)), (X(i_ + sx * 4), X(366)), (X(o - sx * 6), X(350))], fill=255)
img.alpha_composite(glow(eyes, (255, 30, 50), 110, 1.8)); img.alpha_composite(glow(eyes, (255, 70, 70), 34, 2.4)); img.alpha_composite(glow(eyes, (255, 140, 120), 10, 2.5))
img.alpha_composite(fill(eyes, (255, 236, 236, 255)))
# --- Haende links/rechts mit Faeden zu winzigen Menschen
hands = mask(); dh = ImageDraw.Draw(hands); tips = []
for sx in (-1, 1):
    hx = cx + sx * 650; hy = 540
    arm = [(cx + sx * 380, 700), (cx + sx * 520, 610), (hx - sx * 40, hy + 20)]
    dh.line([(X(x), X(y)) for x, y in arm], fill=255, width=X(100), joint="curve")
    for x, y in arm: dh.ellipse([X(x - 50), X(y - 50), X(x + 50), X(y + 50)], fill=255)
    dh.ellipse([X(hx - 100), X(hy - 60), X(hx + 100), X(hy + 80)], fill=255)
    dh.ellipse([X(hx + sx * 70 - 30), X(hy - 30), X(hx + sx * 70 + 40 * sx if sx > 0 else hx + sx * 70 + 30), X(hy + 40)], fill=255)
    for k in range(4):
        fx = hx - 72 + k * 48; fy0 = hy + 50; fy1 = hy + 150 + (k in (1, 2)) * 26
        dh.line([(X(fx), X(fy0)), (X(fx + (k - 1.5) * 6), X(fy1))], fill=255, width=X(36)); dh.ellipse([X(fx + (k - 1.5) * 6 - 18), X(fy1 - 18), X(fx + (k - 1.5) * 6 + 18), X(fy1 + 18)], fill=255)
        tips.append((fx + (k - 1.5) * 6, fy1 + 14))
hands = hands.filter(ImageFilter.GaussianBlur(X(2)))
img.alpha_composite(glow(hands, (120, 90, 255), 40, 0.8)); img.alpha_composite(fill(hands, vgrad(420, 760, (110, 80, 220, 255), (40, 16, 100, 255))))
g2, e2 = rim(hands, (130, 240, 255), 4, 8); img.alpha_composite(g2); img.alpha_composite(e2)
# Faeden + Marionetten-Menschen
strings = mask(); ds = ImageDraw.Draw(strings); people = mask(); dp = ImageDraw.Draw(people)
targets = []
for i, (tx, ty) in enumerate(tips):
    px = tx + r.randint(-40, 40) + (-60 if tx < cx else 60); py = r.randint(860, 940)
    ds.line([(X(tx), X(ty)), (X(px), X(py - 46))], fill=255, width=X(3)); targets.append((px, py))
    s_ = 1.0
    dp.ellipse([X(px - 11), X(py - 70), X(px + 11), X(py - 48)], fill=255)                       # Kopf
    dp.rounded_rectangle([X(px - 13), X(py - 48), X(px + 13), X(py - 6)], X(10), fill=255)        # Koerper
    dp.line([(X(px - 10), X(py - 42)), (X(px - 30), X(py - 66))], fill=255, width=X(8)); dp.line([(X(px + 10), X(py - 42)), (X(px + 30), X(py - 66))], fill=255, width=X(8))   # Arme hoch
    dp.line([(X(px - 6), X(py - 8)), (X(px - 12), X(py + 24))], fill=255, width=X(9)); dp.line([(X(px + 6), X(py - 8)), (X(px + 12), X(py + 24))], fill=255, width=X(9))
img.alpha_composite(glow(strings, (150, 240, 255), 6, 2.5)); img.alpha_composite(fill(strings, (220, 250, 255, 255)))
img.alpha_composite(glow(people, (255, 200, 120), 14, 1.2)); img.alpha_composite(fill(people, (24, 16, 50, 255)))
# --- Text oben
tl = new(); dt = ImageDraw.Draw(tl); f = ImageFont.truetype(FONT, X(176))
dt.text((X(960), X(98)), TEXT, font=f, fill=(255, 255, 255, 255), anchor="mm")
tm = tl.getchannel("A")
img.alpha_composite(glow(tm, (10, 6, 30), 18, 1.4))
img.alpha_composite(tl)
out = img.convert("RGB").resize((1920, 1080), Image.LANCZOS)
out.save("THUMB_v6_1920.png"); out.resize((1280, 720), Image.LANCZOS).save("THUMB_v6.jpg", quality=94)
out.resize((360, 202), Image.LANCZOS).save("THUMB_v6_small.png"); print("ok")
