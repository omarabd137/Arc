"""Thumbnail Longform #01: Banker tippt $300,000 aus dem Nichts, Jake schockiert. 2 Woerter, hoher Kontrast."""
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
from hq import *
import props as PR
from bgs import monitor

c = canvas((255, 255, 255, 255)); p = Pen(c)
p.vgrad(0, 0, W, H, (16, 22, 44), (34, 26, 52))
p.glow(560, 420, 520, (60, 220, 130), 120)
p.glow(1500, 520, 380, (255, 90, 80), 70)
# Schreibtisch + Monitor mit leuchtender Zahl
p.rect(220, 150, 980, 640, (24, 26, 30), 6, r=24); p.vgrad(250, 180, 950, 610, (236, 252, 240), (210, 244, 222))
p.text("$300,000", 600, 420, 128, BOLD, (20, 150, 70), stroke=3, sfill=(255, 255, 255))
p.text("$0  →", 600, 250, 64, BOLD, (190, 60, 50))
p.rect(560, 640, 640, 720, (40, 42, 48), 3); p.rect(470, 715, 730, 740, (40, 42, 48), 3, r=6)
p.rect(330, 740, 870, 770, (60, 62, 70), 3, r=8)
figure(c, 230, 832, 92, BANKER, 1, "grin", 0.0, ("desk", "desk"), seated=True)
p = Pen(c)
p.rect(60, 760, 1080, 800, (120, 84, 56), 4); p.rect(90, 800, 1050, H + 20, (96, 66, 44), 4)
p.rect(330, 740, 870, 770, (60, 62, 70), 3, r=8)
# Jake schockiert rechts
figure(c, 1560, 1240, 150, JAKE, -1, "o", 0.25, ("up", "up"), "stand", 0, "wide")
p = Pen(c)
# Text
p.text("FROM", 1460, 170, 150, BOLD, (255, 255, 255), stroke=9)
p.text("NOTHING", 1430, 330, 170, BOLD, (255, 214, 60), stroke=10)
# roter Pfeil auf die Zahl
p.poly([(1150, 470), (1010, 420), (1030, 460), (900, 470), (900, 510), (1030, 510), (1010, 550)], (230, 40, 44), 5)
im = finish(c); im.save("THUMB_v3_1920.png"); im.resize((1280, 720), Image.LANCZOS).save("THUMB_v3.png")
im.resize((1280, 720), Image.LANCZOS).convert("RGB").save("THUMB_v3.jpg", quality=92)
im.resize((320, 180), Image.LANCZOS).save("THUMB_v3_small.png"); print("ok")
