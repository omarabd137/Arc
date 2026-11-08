"""Thumbnail v4 – Magazin-Cover-Stil wie das abgenommene Thiel-Thumbnail:
S/W, dunkler Fed-Hintergrund, riesiges rotes Serifen-Wort HINTER dem Kopf, kleine weisse Zeile, rote Chart-Linie.
Motiv: Benjamin Franklin (Duplessis-Portraet = Vorlage des 100-$-Scheins), gemeinfrei (Google Art Project / Wikimedia).
Hintergrund: Eccles Building 1937, gemeinfrei (Wikimedia Commons)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
DL = r"C:\Users\Omar\AppData\Local\Temp\claude\3acf78e670d9a2bf\e5117088-cdbe-460b-9a63-0e8c554c0b17\scratchpad\dl"
os.makedirs("thumb_src", exist_ok=True)
W, H = 1280, 720
F = "C:/Windows/Fonts/"
SERIF_B = F + "timesbd.ttf"; SERIF = F + "times.ttf"

# --- Hintergrund: Fed-Gebaeude, S/W, dunkel, leicht unscharf
bg = Image.open(os.path.join(DL, "fed1937.jpg")).convert("L")
bw, bh = bg.size; bg = bg.crop((int(bw * 0.12), int(bh * 0.02), int(bw * 0.98), int(bh * 0.02) + int(bw * 0.86 * 9 / 16))).resize((W, H), Image.LANCZOS)
bg = ImageEnhance.Brightness(bg).enhance(0.42); bg = ImageEnhance.Contrast(bg).enhance(1.15); bg = bg.filter(ImageFilter.GaussianBlur(2.2))
vig = Image.new("L", (W, H), 0); ImageDraw.Draw(vig).ellipse([-260, -200, W + 260, H + 260], fill=255); vig = vig.filter(ImageFilter.GaussianBlur(160))
bg = Image.composite(bg, Image.new("L", (W, H), 6), vig)
img = Image.merge("RGB", (bg, bg, bg))
d = ImageDraw.Draw(img)

# --- rote Chart-Linie (Geldmenge steigt) hinter allem
pts = [(-20, 640), (90, 600), (200, 620), (310, 560), (420, 585), (560, 470), (660, 490), (760, 420), (880, 445), (990, 330), (1100, 350), (1300, 200)]
d.line(pts, fill=(225, 30, 38), width=7, joint="curve")

# --- grosses rotes Wort (hinter dem Kopf)
f_big = ImageFont.truetype(SERIF_B, 250)
d.text((W / 2, 230), "NOTHING", font=f_big, fill=(228, 28, 36), anchor="mm")
f_small = ImageFont.truetype(SERIF, 54)
d.text((W / 2, 62), "WHAT REALLY BACKS YOUR $100?", font=f_small, fill=(240, 238, 232), anchor="mm")

# --- Franklin freistellen (Figur heller als dunkler Bildgrund), S/W mit hartem Kontrast
fr = Image.open(os.path.join(DL, "franklin_gap.jpg")).convert("RGB")
fw, fh = fr.size; fr = fr.crop((int(fw * 0.08), int(fh * 0.04), int(fw * 0.92), int(fh * 0.80)))
g = fr.convert("L")
# Silhouette von Hand (Anteile des Ausschnitts) + weiche Helligkeits-Kante an den Haaren
sx, sy = fr.size
SIL = [(0.33, 0.15), (0.40, 0.125), (0.50, 0.118), (0.57, 0.138), (0.615, 0.19), (0.635, 0.27), (0.665, 0.36), (0.69, 0.45), (0.665, 0.52), (0.625, 0.565),
       (0.67, 0.61), (0.75, 0.68), (0.82, 0.78), (0.88, 0.9), (0.905, 1.0), (0.0, 1.0), (0.0, 0.68), (0.08, 0.63), (0.165, 0.585), (0.155, 0.54),
       (0.14, 0.48), (0.15, 0.38), (0.19, 0.30), (0.24, 0.225), (0.285, 0.18)]
poly = Image.new("L", fr.size, 0); ImageDraw.Draw(poly).polygon([(x * sx, y * sy) for x, y in SIL], fill=255); poly = poly.filter(ImageFilter.GaussianBlur(10))
lum = g.filter(ImageFilter.GaussianBlur(2)).point(lambda v: max(0, min(255, int((v - 38) * 255 / 34))))
edge = ImageChops.multiply(poly, lum)
core = Image.new("L", fr.size, 0); ImageDraw.Draw(core).polygon([(x * sx, y * sy) for x, y in SIL], fill=255); core = core.filter(ImageFilter.MinFilter(41)).filter(ImageFilter.GaussianBlur(14))
m = ImageChops.lighter(edge, core)
fg = ImageOps.autocontrast(g, cutoff=1); fg = ImageEnhance.Contrast(fg).enhance(1.35); fg = ImageEnhance.Sharpness(fg).enhance(1.6)
scale = 690 / sy; size = (int(sx * scale), int(sy * scale))
fg = fg.resize(size, Image.LANCZOS); m = m.resize(size, Image.LANCZOS)
# unten weich ausblenden wie ein Magazin-Cover
fade = Image.new("L", size, 255); fd = ImageDraw.Draw(fade)
for y in range(size[1]):
    if y > size[1] * 0.82: fd.line([(0, y), (size[0], y)], fill=int(255 * max(0, 1 - (y - size[1] * 0.82) / (size[1] * 0.18))))
m = ImageChops.multiply(m, fade)
x0 = int(W / 2 - size[0] / 2) - 10; y0 = H - size[1] + 30
shadow = m.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.6))
img.paste((0, 0, 0), (x0 + 10, y0 + 8), shadow)
img.paste(Image.merge("RGB", (fg, fg, fg)), (x0, y0), m)

# --- echter 100-$-Schein unten links (gemeinfreies Bild), leicht gedreht, S/W mit Rot-Ton weg -> Originalfarbe fuer "Geld"
bill = Image.open(os.path.join(DL, "bill100.jpg")).convert("RGB"); bill = bill.resize((430, int(430 * bill.height / bill.width)), Image.LANCZOS)
bl = bill.convert("RGBA").rotate(-10, expand=True, resample=Image.BICUBIC)
sh = bl.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.7))
img.paste((0, 0, 0), (820 + 8, 470 + 10), sh); img.paste(bl, (820, 470), bl)

img.save("THUMB_D.jpg", quality=94); img.resize((360, 202), Image.LANCZOS).save("THUMB_D_small.png")
open("thumb_src/CREDITS.txt", "w", encoding="utf-8").write(
    "Benjamin Franklin by Joseph-Siffred Duplessis – Google Art Project, Wikimedia Commons, Public domain\n"
    "US Federal Reserve Eccles Building 1937 – Wikimedia Commons, Public domain\n"
    "Obverse of the series 2009 $100 Federal Reserve Note – U.S. Government (newmoney.gov), Wikimedia Commons, Public domain\n")
print("ok")
