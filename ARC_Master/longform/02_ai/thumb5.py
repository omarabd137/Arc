"""Thumbnail #02 v5 im Video-Cartoon-Stil: Leo (Figur aus dem Video) gross, geschockt - hinter ihm der Video-Roboter
mit roten Augen, Hand auf seiner Schulter. Figuren in Video-Groesse gezeichnet und hochskaliert (gleiche Linienstaerke wie im Video)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
from ai_kit import *

def char(fn, scale):
    c = canvas(); fn(c); bb = c.getbbox(); im = c.crop(bb)
    return im.resize((int(im.width / SS * scale), int(im.height / SS * scale)), Image.LANCZOS)

base = abg("office_night").copy()
dark = Image.new("RGBA", base.size, (8, 2, 12, 150)); base.alpha_composite(dark)
g = canvas(); Pen(g).glow(1500, 380, 560, RED, 130); base.alpha_composite(g.resize((W, H)))
rob = char(lambda c: robot(c, 960, 900, 70, ("reach", "down"), RED, face=-1), 2.9)
base.alpha_composite(rob, (1180, 60))
LEO_T = P(hair=(52, 40, 34), top=(70, 140, 96), pants=(60, 64, 80), shoes=(40, 40, 44), skin=(236, 200, 166), style="short", glasses=True)
leo = char(lambda c: figure(c, 960, 900, 80, LEO_T, 0, "o", 0.9, ("down", "down"), "stand", 0.0, "wide"), 2.9)
base.alpha_composite(leo, (1000 - leo.width // 2 + 120, 150))
d = ImageDraw.Draw(base)
for (x, y) in ((870, 300), (850, 360)): d.ellipse((x - 12, y - 18, x + 12, y + 18), fill=(150, 210, 255), outline=INK, width=4)
def big(s, x, y, size, col):
    f = ImageFont.truetype(BOLD, size)
    d.text((x + 7, y + 9), s, font=f, fill=(0, 0, 0), anchor="lm"); d.text((x, y), s, font=f, fill=col, anchor="lm", stroke_width=14, stroke_fill=(0, 0, 0))
big("IT", 60, 200, 190, (255, 255, 255)); big("ALREADY", 60, 400, 150, (255, 255, 255)); big("HAPPENED.", 60, 590, 150, (255, 214, 60))
im = base.convert("RGB"); im.save("THUMB_v5_1920.png"); im.resize((1280, 720), Image.LANCZOS).save("THUMB_v5.jpg", quality=93); print("ok", leo.size, rob.size)
