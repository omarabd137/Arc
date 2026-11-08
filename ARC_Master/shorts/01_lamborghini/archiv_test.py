"""Version D: Archiv-Doku-Stil (echte, lizenzfreie Fotos, Duotone, Riss-Kanten, Korn, Gold-Typo)."""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops, ImageEnhance

W, H = 1080, 1920
F = "C:/Windows/Fonts/"
A = "assets/"
GOLD, CREAM, RED, BLACK = (222, 184, 104), (240, 232, 214), (200, 36, 40), (8, 8, 10)

def cover(img, w, h, fx=0.5, fy=0.5):
    s = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * s) + 1, int(img.height * s) + 1), Image.LANCZOS)
    x = int((img.width - w) * fx); y = int((img.height - h) * fy)
    return img.crop((x, y, x + w, y + h))

def duotone(img, dark, light, contrast=1.35):
    g = ImageEnhance.Contrast(ImageOps.grayscale(img)).enhance(contrast)
    return ImageOps.colorize(g, dark, light)

def grade(img, warm=1.08, sat=0.85, con=1.12):
    img = ImageEnhance.Color(img).enhance(sat)
    img = ImageEnhance.Contrast(img).enhance(con)
    r, g, b = img.split()
    r = r.point(lambda v: min(255, int(v * warm))); b = b.point(lambda v: int(v / warm))
    return Image.merge("RGB", (r, g, b))

def torn_mask(w, h, edge="bottom", seed=1, amp=18):
    m = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(m)
    rnd = random.Random(seed)
    pts = []
    for x in range(0, w + 12, 12):
        pts.append((x, h - amp - rnd.randint(0, amp)))
    d.polygon(pts + [(w, h), (0, h)], fill=0)
    return m

def finish(img, grain=18):
    noise = Image.effect_noise((W, H), 60).convert("RGB")
    img = Image.blend(img, ImageChops.overlay(img, noise), grain / 100)
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse([-W * 0.3, -H * 0.12, W * 1.3, H * 1.12], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(170))
    return Image.composite(img, Image.new("RGB", (W, H), BLACK), v)

def text_c(d, y, text, size, fill, fontname="georgiab.ttf", track=0, shadow=True):
    f = ImageFont.truetype(F + fontname, size)
    widths = [d.textlength(c, font=f) for c in text]
    x = (W - sum(widths) - track * (len(text) - 1)) / 2
    for c, w in zip(text, widths):
        if shadow:
            d.text((x + 4, y + 5), c, font=f, fill=(0, 0, 0))
        d.text((x, y), c, font=f, fill=fill)
        x += w + track

def tag(d, cx, cy, text, color, size=70):
    f = ImageFont.truetype(F + "georgiab.ttf", size)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([cx - tw / 2 - 34, cy - size * 0.8, cx + tw / 2 + 34, cy + size * 0.8], radius=10, fill=CREAM, outline=BLACK, width=5)
    d.text((cx - tw / 2, cy - size * 0.62), text, font=f, fill=color)

# --- Bild 1: Hook ---
def frame_hook():
    img = Image.new("RGB", (W, H), BLACK)
    enzo = duotone(cover(Image.open(A + "enzo_1967.jpg").convert("RGB"), W, 1020, 0.45, 0.1), (24, 6, 8), (236, 210, 196))
    enzo = Image.blend(enzo, Image.new("RGB", enzo.size, (150, 20, 24)), 0.18)
    img.paste(enzo, (0, 0), torn_mask(W, 1020, seed=3, amp=22))
    ferr = duotone(cover(Image.open(A + "ferruccio_70s.jpg").convert("RGB"), W, 940, 0.55, 0.5), (14, 12, 8), (240, 214, 160))
    img.paste(ferr, (0, 980))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 960, W, 1000], fill=BLACK)
    text_c(d, 70, "ENZO FERRARI", 64, CREAM, track=10)
    text_c(d, 905, "vs", 64, GOLD, "georgiai.ttf")
    text_c(d, 1760, "FERRUCCIO LAMBORGHINI", 54, GOLD, track=6)
    return finish(img)

# --- Bild 2: Preis-Vergleich ---
def frame_price():
    img = Image.new("RGB", (W, H), BLACK)
    tr = grade(cover(Image.open(A + "tractor_1960.jpg").convert("RGB"), W, 940, 0.5, 0.55), warm=1.1)
    fe = grade(cover(Image.open(A + "ferrari_250gt.jpg").convert("RGB"), W, 940, 0.45, 0.5), warm=1.02, sat=0.9)
    img.paste(tr, (0, 0)); img.paste(fe, (0, 980))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 940, W, 980], fill=BLACK)
    text_c(d, 70, "TRACTOR CLUTCH", 56, CREAM, track=6)
    text_c(d, 1050, "FERRARI CLUTCH", 56, CREAM, track=6)
    tag(d, 540, 800, "10 LIRE", (40, 120, 60))
    tag(d, 540, 1760, "1,000 LIRE", RED)
    return finish(img, 14)

# --- Bild 3: Miura-Enthuellung ---
def frame_miura():
    img = grade(cover(Image.open(A + "miura_1966.jpg").convert("RGB"), W, H, 0.42, 0.6), warm=1.12, sat=1.05, con=1.18)
    d = ImageDraw.Draw(img, "RGBA")
    rnd = random.Random(8)
    for _ in range(7):   # Blitzlichter
        x, y, r = rnd.randint(60, W - 60), rnd.randint(200, 900), rnd.randint(30, 70)
        for k in range(5, 0, -1):
            d.ellipse([x - r * k / 2, y - r * k / 2, x + r * k / 2, y + r * k / 2], fill=(255, 250, 235, 22))
    d.rectangle([0, 0, W, 420], fill=(0, 0, 0, 140))
    text_c(d, 120, "1966", 150, GOLD, track=14)
    text_c(d, 300, "LAMBORGHINI MIURA", 58, CREAM, track=8)
    return finish(img, 16)

if __name__ == "__main__":
    fr = [frame_hook(), frame_price(), frame_miura()]
    for i, f in enumerate(fr):
        f.save(f"D_test_{i + 1}.png")
    tw, th = 450, 800
    sheet = Image.new("RGB", (3 * tw + 40, th + 20), (0, 0, 0))
    for i, f in enumerate(fr):
        sheet.paste(f.resize((tw, th)), (10 + i * (tw + 10), 10))
    sheet.save("STIL_D_ARCHIV.png")
    print("ok")
