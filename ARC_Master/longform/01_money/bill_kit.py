"""Detailgetreue US-Banknote im ARC-Cartoon-Stil (1 $ und 100 $), plus eigene ARC-Hintergruende.
Merkmale wie beim echten Schein: gruen-graues Papier mit Verlauf, Zierrahmen mit Rankenmuster, ovales Portraet in der Mitte,
schwarzes Federal-Reserve-Siegel links, gruenes Treasury-Siegel rechts, gruene Seriennummern, Wertzahlen in den Ecken,
'FEDERAL RESERVE NOTE' oben, 'THE UNITED STATES OF AMERICA', Wert in Worten unten."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from crayon_kit import SS, INK
F = "C:/Windows/Fonts/"
SERIF = F + "georgiab.ttf"; SERIF_R = F + "georgia.ttf"; BOLD = F + "ariblk.ttf"

def real_bill(img, cx, cy, w, value="1", angle=0):
    hgt = w * 0.426
    W_, H_ = int(w * SS) + 60, int(hgt * SS) + 60
    lay = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    o = 30; X = lambda v: o + v * SS; ink = (36, 62, 44); green = (70, 120, 80)
    # Papier mit leichtem Verlauf
    paper = Image.new("RGBA", (int(w * SS), int(hgt * SS)))
    dp = ImageDraw.Draw(paper)
    for y in range(paper.height):
        k = y / paper.height; dp.line([(0, y), (paper.width, y)], fill=(int(214 - 12 * k), int(226 - 10 * k), int(204 - 14 * k), 255))
    m = Image.new("L", paper.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, paper.width - 1, paper.height - 1], radius=int(5 * SS), fill=255)
    lay.paste(paper, (o, o), m)
    d.rounded_rectangle([X(0), X(0), X(w), X(hgt)], radius=int(5 * SS), outline=INK, width=int(3.5 * SS))
    # Zierrahmen: Doppellinie + Rankenmuster
    for inset, wd in ((7, 2.5), (11, 1.2)):
        d.rectangle([X(inset), X(inset), X(w - inset), X(hgt - inset)], outline=green, width=int(wd * SS))
    for k in range(int(w / 9)):
        x = 13 + k * 9
        d.arc([X(x), X(8), X(x + 9), X(14)], 0, 180, fill=(110, 150, 110), width=int(1 * SS))
        d.arc([X(x), X(hgt - 14), X(x + 9), X(hgt - 8)], 180, 360, fill=(110, 150, 110), width=int(1 * SS))
    # Guilloche-Wellen hinter dem Portraet
    for j in range(14):
        pts = [(X(w * 0.28 + t * w * 0.44 / 60), X(hgt * 0.2 + j * hgt * 0.045 + math.sin(t / 60 * 12 + j) * 2.2)) for t in range(61)]
        d.line(pts, fill=(160, 190, 156), width=int(0.9 * SS))
    # Portraet-Oval (Washington beim 1er, Franklin beim 100er)
    pcx, pcy = w / 2, hgt * 0.52; rx, ry = w * 0.12, hgt * 0.34
    d.ellipse([X(pcx - rx), X(pcy - ry), X(pcx + rx), X(pcy + ry)], fill=(198, 214, 188), outline=ink, width=int(2.2 * SS))
    d.ellipse([X(pcx - rx + 4), X(pcy - ry + 4), X(pcx + rx - 4), X(pcy + ry - 4)], outline=green, width=int(1 * SS))
    hr = rx * 0.48
    d.chord([X(pcx - rx * 0.85), X(pcy + ry * 0.15), X(pcx + rx * 0.85), X(pcy + ry * 1.3)], 180, 360, fill=(60, 86, 64))          # Mantel
    d.polygon([X(pcx - rx * 0.18), X(pcy + ry * 0.38), X(pcx + rx * 0.18), X(pcy + ry * 0.38), X(pcx), X(pcy + ry * 0.62)], fill=(230, 234, 222))  # Halstuch
    d.ellipse([X(pcx - hr * 0.86), X(pcy - ry * 0.55), X(pcx + hr * 0.86), X(pcy + ry * 0.35)], fill=(214, 220, 204), outline=ink, width=int(1.5 * SS))  # Gesicht
    wig = (236, 238, 230) if value == "1" else (200, 206, 194)
    # Haar: nach hinten gekaemmt, seitliche Locken-Rollen, Zopf hinten (Washington-Stil)
    d.chord([X(pcx - hr * 0.95), X(pcy - ry * 0.62), X(pcx + hr * 0.95), X(pcy - ry * 0.05)], 180, 360, fill=wig, outline=ink, width=int(1.1 * SS))
    for k in range(4):
        d.arc([X(pcx - hr * 0.8 + k * hr * 0.35), X(pcy - ry * 0.6), X(pcx - hr * 0.4 + k * hr * 0.35), X(pcy - ry * 0.3)], 200, 340, fill=(150, 160, 150), width=int(0.8 * SS))
    for sx in (-1, 1):
        for j in range(2):
            yy = pcy - ry * 0.18 + j * ry * 0.16
            d.ellipse([X(pcx + sx * hr * 0.92 - hr * 0.2), X(yy - ry * 0.07), X(pcx + sx * hr * 0.92 + hr * 0.2), X(yy + ry * 0.07)], fill=wig, outline=ink, width=int(0.9 * SS))
    for sx in (-1, 1):
        d.arc([X(pcx + sx * hr * 0.32 - hr * 0.16), X(pcy - ry * 0.24), X(pcx + sx * hr * 0.32 + hr * 0.16), X(pcy - ry * 0.1)], 200, 340, fill=ink, width=int(0.9 * SS))
        d.ellipse([X(pcx + sx * hr * 0.32 - 1.4), X(pcy - ry * 0.1 - 1.2), X(pcx + sx * hr * 0.32 + 1.4), X(pcy - ry * 0.1 + 1.2)], fill=ink)
    d.line([X(pcx + hr * 0.02), X(pcy - ry * 0.06), X(pcx + hr * 0.12), X(pcy + ry * 0.06), X(pcx - hr * 0.02), X(pcy + ry * 0.08)], fill=ink, width=int(0.9 * SS))
    d.arc([X(pcx - hr * 0.22), X(pcy + ry * 0.08), X(pcx + hr * 0.22), X(pcy + ry * 0.2)], 20, 160, fill=ink, width=int(1 * SS))
    # Siegel: links schwarz (Federal Reserve), rechts gruen (Treasury)
    for sx, col, txt in ((0.24, (40, 40, 44), "FR"), (0.76, (60, 130, 80), "T")):
        scx, scy, sr = w * sx, hgt * 0.56, hgt * 0.15
        d.ellipse([X(scx - sr), X(scy - sr), X(scx + sr), X(scy + sr)], outline=col, width=int(2 * SS))
        for k in range(24):
            a = k * math.pi / 12; d.line([X(scx + math.cos(a) * sr * 0.78), X(scy + math.sin(a) * sr * 0.78), X(scx + math.cos(a) * sr), X(scy + math.sin(a) * sr)], fill=col, width=int(1 * SS))
        f = ImageFont.truetype(SERIF, int(sr * 0.75 * SS)); d.text((X(scx), X(scy)), txt, font=f, fill=col, anchor="mm")
    # Texte
    f1 = ImageFont.truetype(SERIF, int(hgt * 0.075 * SS)); f2 = ImageFont.truetype(SERIF_R, int(hgt * 0.06 * SS))
    d.text((X(w / 2), X(hgt * 0.1)), "FEDERAL RESERVE NOTE", font=f2, fill=ink, anchor="mm")
    d.text((X(w / 2), X(hgt * 0.2)), "THE UNITED STATES OF AMERICA", font=f1, fill=ink, anchor="mm")
    words = {"1": "ONE DOLLAR", "100": "ONE HUNDRED DOLLARS"}.get(value, value + " DOLLARS")
    d.text((X(w / 2), X(hgt * 0.92)), words, font=f1, fill=ink, anchor="mm")
    fn = ImageFont.truetype(BOLD, int(hgt * 0.17 * SS))
    for (x, y) in ((0.07, 0.17), (0.93, 0.17), (0.07, 0.84), (0.93, 0.84)):
        d.text((X(w * x), X(hgt * y)), value, font=fn, fill=ink, anchor="mm")
    if value == "1":
        d.text((X(w * 0.76), X(hgt * 0.84)), "ONE", font=ImageFont.truetype(SERIF, int(hgt * 0.12 * SS)), fill=ink, anchor="mm")
    fs = ImageFont.truetype(F + "consolab.ttf", int(hgt * 0.07 * SS))
    for (x, y) in ((0.24, 0.32), (0.76, 0.78)):
        d.text((X(w * x), X(hgt * y)), "L 47215908 C", font=fs, fill=(50, 130, 80), anchor="mm")
    if angle: lay = lay.rotate(angle, expand=True, resample=Image.BICUBIC)
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(6 * SS)).point(lambda v: v * 0.35)
    img.paste(Image.new("RGB", lay.size, (0, 0, 0)), (int(cx * SS - lay.width / 2 + 10 * SS), int(cy * SS - lay.height / 2 + 12 * SS)), sh)
    img.paste(lay, (int(cx * SS - lay.width / 2), int(cy * SS - lay.height / 2)), lay)

class Ledger:
    """ARC-Eroeffnung/Ende: tiefes Nachtblau, gedaempfte, langsam nach oben laufende Kontozahlen
    (Thema: Geld wird getippt). Spalten einmal vorgerendert, pro Bild nur verschoben."""
    def __init__(self, W=1920, H=1080, seed=7):
        self.W, self.H = W, H
        base = Image.new("RGB", (W, H)); d = ImageDraw.Draw(base)
        for y in range(H):
            k = y / H; d.line([(0, y), (W, y)], fill=(int(9 + 7 * k), int(14 + 9 * k), int(28 + 16 * k)))
        self.base = base
        f = ImageFont.truetype(F + "consola.ttf", 21); rnd = random.Random(seed); self.cols = []
        for col in range(40, W, 190):
            strip = Image.new("RGBA", (180, H * 2), (0, 0, 0, 0)); ds = ImageDraw.Draw(strip)
            for row in range(0, H * 2, 62):
                v = rnd.randint(10, 999999); sign = "+" if rnd.random() < 0.5 else "-"
                ds.text((0, row), f"{sign}${v:,}", font=f, fill=(70, 140, 100, 110) if sign == "+" else (150, 90, 90, 90))
            self.cols.append((col, strip, rnd.uniform(14, 30)))
        vg = Image.new("L", (W, H), 0); ImageDraw.Draw(vg).ellipse([-260, -340, W + 260, H + 340], fill=255)
        self.vg = vg.filter(ImageFilter.GaussianBlur(170)); self.dark = Image.new("RGB", (W, H), (3, 5, 10))
    def frame(self, t):
        img = self.base.copy()
        for col, strip, sp in self.cols:
            off = int(t * sp) % self.H
            img.paste(strip.crop((0, off, 180, off + self.H)), (col, 0), strip.crop((0, off, 180, off + self.H)))
        return Image.composite(img, self.dark, self.vg)
