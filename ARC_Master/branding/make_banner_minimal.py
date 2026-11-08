"""Schlichtes ARC-Banner: schwarzer Hintergrund, weisse Schrift (passend zum Profilbild)."""
from PIL import Image, ImageDraw, ImageFont

F = "C:/Windows/Fonts/"
BLACK, WHITE, GREY = (0, 0, 0), (255, 255, 255), (150, 150, 150)
W, H = 2560, 1440

def spaced(d, cx, y, text, font, fill, track):
    widths = [d.textlength(c, font=font) for c in text]
    x = cx - (sum(widths) + track * (len(text) - 1)) / 2
    for c, w in zip(text, widths):
        d.text((x, y), c, font=font, fill=fill)
        x += w + track

img = Image.new("RGB", (W, H), BLACK)
d = ImageDraw.Draw(img)
spaced(d, W / 2, H / 2 - 150, "ARC", ImageFont.truetype(F + "georgia.ttf", 150), WHITE, 60)
d.line([(W / 2 - 90, H / 2 + 45), (W / 2 + 90, H / 2 + 45)], fill=GREY, width=2)
sub = ImageFont.truetype(F + "georgia.ttf", 50)
line = "Business stories, drawn and explained."
d.text((W / 2 - d.textlength(line, font=sub) / 2, H / 2 + 75), line, font=sub, fill=WHITE)
img.save("ARC_Banner_schwarz_2560x1440.png", optimize=True)
print("ok")
