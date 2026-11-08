import sys, os
sys.path.insert(0, "../04_market_crash"); sys.path.insert(0, "../../longform/01_money")
import cartoon, hq
from hq import P, figure
from PIL import Image, ImageDraw
BEZOS = P(hair=(225, 190, 160), top=(140, 185, 232), pants=(44, 48, 62), shoes=(30, 28, 28), skin=(236, 192, 160), style="shaved", age=55, big=1.12, collar=True)
out = Image.new("RGB", (1500, 900), (245, 240, 230))
for i, (mouth, eyes, brow, arms) in enumerate([("laugh", "happy", 0.0, ("down", "down")), ("grin", "open", 0.05, ("cross", "cross")), ("smile", "closed", 0.0, ("down", "point"))]):
    c = hq.canvas(); figure(c, 960, 1040, 200, BEZOS, 1, mouth, brow, arms, "stand", 0.0, eyes)
    S = hq.SS; im = c.crop((int(620 * S), int(10 * S), int(1300 * S), int(1045 * S))).resize((480, 730))
    out.paste(im, (20 + i * 490, 80), im)
out.save("BEZOS_TEST.png"); print("ok")
