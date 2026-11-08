"""Thumbnail aus den ECHTEN Video-Figuren/Orten (hq.py/bgs.py), Aufbau wie Omars Entwurf:
Banker links (Teufelsschatten, Geldstapel, warmes Licht), Jake rechts (Brief, besorgt, kaltes Licht), Tresor in der Mitte."""
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from hq import *
import props as PR
from bgs import bg

def sticker(layer, w=8, col=(255, 255, 255)):
    a = layer.getchannel("A"); out = a.filter(ImageFilter.MaxFilter(w * 2 + 1)); base = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh = a.filter(ImageFilter.GaussianBlur(24)).point(lambda v: int(v * 0.55)); base.paste(Image.new("RGBA", layer.size, (0, 0, 0, 255)), (16, 20), sh)
    base.paste(Image.new("RGBA", layer.size, col + (255,)), (0, 0), out); base.alpha_composite(layer); return base

c = canvas((0, 0, 0, 255))
back = ImageEnhance.Brightness(bg("vault").convert("RGB")).enhance(0.8)
c.paste(back.resize((W * SS, H * SS)), (0, 0)); p = Pen(c)
p.glow(380, 520, 520, (255, 140, 40), 150); p.glow(1560, 520, 520, (60, 120, 255), 110)
# Teufelsschatten hinter dem Banker
dv = canvas(); dp = Pen(dv)
dp.ell(330, 300, 150, 165, (30, 10, 10), 0); dp.poly([(200, 270), (150, 90), (260, 200)], (30, 10, 10), 0); dp.poly([(460, 270), (510, 90), (400, 200)], (30, 10, 10), 0)
dp.ell(330, 640, 260, 220, (30, 10, 10), 0)
for ex in (280, 380): dp.ell(ex, 300, 30, 15, (255, 40, 30), 0)
dv = dv.filter(ImageFilter.GaussianBlur(10)); c.alpha_composite(dv); Pen(c).glow(330, 300, 110, (255, 40, 30), 70)
# Banker (Video-Figur), gross, sitzend hinter dem Tisch, grinsend
bk = canvas(); figure(bk, 560, 900, 150, BANKER, 1, "grin", -0.05, ("desk", "desk"), seated=True); c.alpha_composite(sticker(bk))
# Tisch + Geldstapel
# Jake (Video-Figur), besorgt, Hand am Kopf, Brief
jk = canvas(); figure(jk, 1530, 930, 160, JAKE, -1, "o", 0.3, ("chin", "hold"), seated=True, eyes="wide"); c.alpha_composite(sticker(jk))
p = Pen(c); p.rect(0, 900, W, 960, (120, 80, 52), 5); p.rect(0, 960, W, H + 10, (96, 62, 40), 5)
cs = canvas(); [PR.real_bill(cs, 200 + (i % 3) * 200, 905 - (i // 3) * 30, 260, value="100", angle=(-6, 4, -2)[i % 3]) for i in range(9)]; c.alpha_composite(sticker(cs, 5))
let = canvas(); PR.document(let, 1250, 760, 300, 220, "LOAN STATEMENT", "Interest: 21%", 5, 3, stamp="OVERDUE"); let = let.rotate(-8, center=(1250 * SS, 760 * SS), resample=Image.BICUBIC); c.alpha_composite(sticker(let, 5))
# Text oben (gross, bunt, dicke Kontur)
t = Image.new("RGBA", c.size, (0, 0, 0, 0)); tp = Pen(t)
words = (("How", (255, 255, 255)), ("Banks", (255, 214, 50)), ("Lie", (255, 214, 50)), ("to", (255, 255, 255)), ("You", (235, 30, 36)))
fnt = ImageFont.truetype(BOLD, 150 * SS); dd = ImageDraw.Draw(t); gap = 34 * SS
ws = [dd.textlength(w_, font=fnt) for w_, _ in words]; x = (W * SS - (sum(ws) + gap * 4)) / 2
for (w_, col), wd in zip(words, ws):
    dd.text((x, 120 * SS), w_, font=fnt, fill=col + (255,), anchor="lm", stroke_width=11 * SS, stroke_fill=INK + (255,)); x += wd + gap
sh = t.getchannel("A").filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.7)); c.paste(Image.new("RGBA", c.size, (0, 0, 0, 255)), (12, 16), sh); c.alpha_composite(t)
im = c.convert("RGB").resize((1280, 720), Image.LANCZOS); im.save("THUMB_E.jpg", quality=94); im.resize((360, 202), Image.LANCZOS).save("THUMB_E_small.png"); print("ok")
