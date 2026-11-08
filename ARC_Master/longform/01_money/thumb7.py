"""Omars Thumbnail verbessern: Text auf 2 Woerter, Szene groesser, mehr Kontrast/Saettigung, warm/kalt-Split, Fokus auf Gesichter."""
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
src = Image.open("thumb_src/user_thumb.webp").convert("RGB")          # 1672x941
W, H = 1672, 941
F = "C:/Windows/Fonts/ariblk.ttf"
# Szene ohne alten Text (alter Text endet ~y=205), leicht heranzoomen -> Figuren groesser
img = src.copy()
band = src.crop((0, 210, W, 260)).resize((W, 215)).filter(ImageFilter.GaussianBlur(25))
img.paste(ImageEnhance.Brightness(band).enhance(0.35), (0, 0))
# Farbe: mehr Saettigung + Kontrast, warm links (Banker), kalt rechts (Jake)
img = ImageEnhance.Color(img).enhance(1.35); img = ImageEnhance.Contrast(img).enhance(1.18)
warm = Image.new("RGB", (W, H), (255, 120, 40)); cool = Image.new("RGB", (W, H), (40, 110, 255))
grad = Image.linear_gradient("L").rotate(90).resize((W, H))            # links hell -> rechts dunkel
img = Image.composite(Image.blend(img, warm, 0.12), Image.blend(img, cool, 0.12), grad)
# Vignette fuer Fokus
v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-200, -120, W + 200, H + 220], fill=255); v = v.filter(ImageFilter.GaussianBlur(150))
img = Image.composite(img, ImageEnhance.Brightness(img).enhance(0.45), v)
# oben abdunkeln, damit der Text knallt
top = Image.new("L", (W, H), 0); dt = ImageDraw.Draw(top)
for y in range(260): dt.line([(0, y), (W, y)], fill=int(160 * (1 - max(0, y - 200) / 60)) if y > 200 else 160)
img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, top)
d = ImageDraw.Draw(img)
def txt(s, x, y, size, fill, anchor="mm"):
    f = ImageFont.truetype(F, size)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.text((x + 8, y + 10), s, font=f, fill=(0, 0, 0, 180), anchor=anchor, stroke_width=14, stroke_fill=(0, 0, 0, 180))
    img.paste(lay.filter(ImageFilter.GaussianBlur(6)), (0, 0), lay.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(img).text((x, y), s, font=f, fill=fill, anchor=anchor, stroke_width=12, stroke_fill=(10, 10, 12))
txt("BANKS", 620, 112, 175, (255, 255, 255))
txt("LIE", 1215, 112, 190, (235, 30, 36))
# kleiner roter Pfeil auf Jakes Brief
d = ImageDraw.Draw(img)
img.save("THUMB_C.jpg", quality=94); img.resize((1280, 720), Image.LANCZOS).save("THUMB_C_1280.jpg", quality=94)
img.resize((360, 202), Image.LANCZOS).save("THUMB_C_small.png"); print("ok")
