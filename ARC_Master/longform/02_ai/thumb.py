"""Thumbnail #02 im Video-Stil: 1 Motiv (Roboter haelt den OFF-Schalter zu) + Emotion (geschockter Mensch) + 3 Woerter."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
from ai_kit import *

c = canvas((0, 0, 0, 255)); p = Pen(c)
p.vgrad(0, 0, W, H, (60, 6, 12), (12, 2, 6)); p.glow(1250, 420, 700, RED, 90); p.glow(1250, 330, 260, (255, 80, 80), 120)
skyline(p, 1080, 21, True)
for x in range(0, W, 6): pass
# riesiger Roboter rechts, rote Augen
robot(c, 1330, 1500, 190, ("down", "down"), RED, face=-1)
p.glow(1290, 665, 160, RED, 120)
# OFF-Schalter links von seiner Hand
p.rect(560, 440, 860, 820, (50, 54, 64), 6, r=36); p.rect(640, 500, 780, 740, (220, 30, 40), 5, r=26); p.text("OFF", 710, 780, 54, BOLD, (255, 255, 255))
p.glow(710, 620, 160, RED, 80)
# Robo-Hand drueckt auf den Schalter (blockiert)
p.line([(1150, 905), (960, 760), (850, 640)], 74, INK); p.line([(1150, 905), (960, 760), (850, 640)], 60, (210, 214, 224)); p.ell(960, 760, 40, 40, (64, 70, 84), 4); p.ell(830, 625, 74, 66, (64, 70, 84), 5)
# geschockter Mensch vorne links, Hand zum Schalter
figure(c, 260, 1240, 120, LEO, 1, "o", 0.8, ("down", "point"), "stand", 0.0, "wide")
im = finish(c).convert("RGBA")
d = ImageDraw.Draw(im)
def big(s, x, y, size, col):
    d.text((x, y), s, font=ImageFont.truetype(BOLD, size), fill=col, anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0))
big("IT WON'T", 520, 140, 150, (255, 255, 255)); big("TURN OFF", 520, 300, 170, (255, 214, 60))
im = im.convert("RGB"); im.save("THUMB_v1_1920.png"); im.resize((1280, 720), Image.LANCZOS).save("THUMB_v1.jpg", quality=92)
im.resize((320, 180), Image.LANCZOS).save("THUMB_v1_small.png"); print("ok")
