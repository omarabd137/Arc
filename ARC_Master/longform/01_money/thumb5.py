"""Thumbnail v5: Thiel-Cover-Aufbau, aber im Cartoon-Stil des Videos (gezeichnete Fed, Banker, Schein)."""
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from hq import *
import props as PR
from bgs import bg
from thumb3 import banker_bust, sticker

back = bg("fed").convert("RGB"); back = ImageEnhance.Brightness(back).enhance(0.38).filter(ImageFilter.GaussianBlur(3))
c = canvas((0, 0, 0, 255)); c.paste(back.resize((W * SS, H * SS)), (0, 0)); p = Pen(c)
p.line([(-20, 960), (300, 880), (520, 910), (760, 760), (980, 800), (1220, 600), (1460, 640), (1700, 430), (1960, 300)], 11, (228, 30, 38))
p.text("WHAT REALLY BACKS YOUR $100?", 960, 92, 78, SERIF, (245, 240, 230))
p.text("NOTHING", 960, 330, 370, F + "timesbd.ttf", (228, 28, 36))
bk = canvas(); banker_bust(bk, 960, 640, 250); c.alpha_composite(sticker(bk, 10, (255, 255, 255)))
b = canvas(); PR.real_bill(b, 1560, 900, 560, value="100", angle=-12); c.alpha_composite(sticker(b, 6))
b = canvas(); PR.real_bill(b, 360, 920, 520, value="100", angle=14); c.alpha_composite(sticker(b, 6))
im = c.convert("RGB").resize((1280, 720), Image.LANCZOS); im.save("THUMB_v3.jpg", quality=93); im.save("THUMB_v3.png"); print("ok")
