"""Alle 13 Szenen von Short #01 im Look v6 (Crayon-Spezifikation)."""
import math
from PIL import Image, ImageDraw
from crayon_kit import S, sh, shape, stroke, ellipse_pts, W, H, SS, INK, ENZO, FERRUCCIO, done
import places
from crayon3 import figure, sticky
from crayon2 import spoken, hand_text, clutch_drawing, price_tag, GREY, ORANGE

MECHANIC = dict(skin=(226, 182, 140), hair=(70, 48, 34), hair_hi=(120, 90, 66), top=(70, 100, 150), tie=None, braces=None,
                trousers=(60, 80, 120), glasses=False, mustache=False, nose=False, big=1.0, hairstyle="mech")

def cap(img, cx, head_cy, R, face=1):
    d = ImageDraw.Draw(img, "RGBA")
    shape(d, ellipse_pts(cx, head_cy - R * 0.35, R * 1.0, R * 0.6, 50, 180, 360) + [(cx + R, head_cy - R * 0.3), (cx - R, head_cy - R * 0.3)], (60, 90, 140), 501)
    shape(d, [(cx + face * R * 0.2, head_cy - R * 0.36), (cx + face * R * 1.35, head_cy - R * 0.3), (cx + face * R * 1.3, head_cy - R * 0.2), (cx + face * R * 0.2, head_cy - R * 0.24)], (48, 72, 116), 502, lw=4)

def car(img, x, y, w, color, face=1, low=False, seed=300):
    d = ImageDraw.Draw(img, "RGBA")
    h = w * (0.26 if low else 0.32)
    prof = ([(0, .3), (.16, .5), (.4, .95), (.66, 1), (.9, .6), (1, .3), (1, 0), (0, 0)] if low else
            [(0, .38), (.1, .55), (.33, .6), (.45, 1), (.7, .98), (.84, .6), (1, .48), (1, 0), (0, 0)])
    pts = [(x + (px if face == 1 else 1 - px) * w, y - py * h) for px, py in prof]
    d.ellipse(S(x - 20, y - 14, x + w + 20, y + 18), fill=(0, 0, 0, 60))
    shape(d, pts, color, seed)
    wa, wb = (.46, .7) if face == 1 else (.3, .54)
    shape(d, [(x + wa * w, y - .62 * h), (x + (wa + .05) * w, y - .9 * h), (x + (wb - .02) * w, y - .88 * h), (x + (wb + .05) * w, y - .62 * h)], (176, 210, 232), seed + 1, lw=4)
    stroke(d, [(x + .08 * w, y - .42 * h), (x + .92 * w, y - .42 * h)], lw=3, color=sh(color, 0.75))
    for cxw in (x + .2 * w, x + .8 * w):
        r = h * .3
        shape(d, ellipse_pts(cxw, y, r, r), (40, 40, 44), seed + 2)
        shape(d, ellipse_pts(cxw, y, r * .5, r * .5), (190, 190, 198), seed + 3, lw=4)

def smoke(img, puffs):
    d = ImageDraw.Draw(img, "RGBA")
    for i, (x, y, r) in enumerate(puffs):
        shape(d, ellipse_pts(x, y, r, r * 0.85), (214, 214, 220), 400 + i, lw=4)

def outside_workshop():
    img, _d, hz = places.base_room((178, 214, 236), (190, 222, 240), (196, 186, 170), (178, 168, 152), horizon=1380)
    d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(-20, 1380), (300, 1160), (620, 1300), (1100, 1120), (1100, 1380)], (150, 186, 120), 1, lw=5)   # Huegel
    shape(d, [(40, 640), (760, 640), (760, 1380), (40, 1380)], (214, 188, 156), 2)                           # Werkstatt-Gebaeude
    shape(d, [(20, 600), (780, 600), (780, 650), (20, 650)], (150, 108, 70), 3)
    shape(d, [(260, 900), (560, 900), (560, 1380), (260, 1380)], (120, 110, 100), 4)
    sticky_txt = None
    return img, hz

def factory_1963():
    img, _d, hz = places.base_room((178, 214, 236), (190, 222, 240), (170, 170, 172), (150, 150, 152), horizon=1400)
    d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(60, 760), (1020, 760), (1020, 1400), (60, 1400)], (236, 230, 216), 2)
    for x in range(60, 1020, 160):
        shape(d, [(x, 760), (x + 80, 660), (x + 160, 760)], (210, 204, 190), 3 + x, lw=5)
    for x in range(100, 1000, 180):
        shape(d, [(x, 900), (x + 110, 900), (x + 110, 1040), (x, 1040)], (176, 210, 232), 10 + x, lw=4)
    shape(d, [(350, 1130), (990, 1130), (990, 1230), (350, 1230)], (30, 30, 34), 20)
    hand_text(img, "AUTOMOBILI LAMBORGHINI", 670, 1150, 36, (240, 200, 90))
    shape(d, [(420, 1260), (660, 1260), (660, 1400), (420, 1400)], (110, 100, 92), 21)
    return img, hz

def motor_show():
    img = Image.new("RGB", (W * SS, H * SS), (40, 44, 70))
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(7):  # Scheinwerferkegel
        x = 80 + i * 160
        d.polygon(S(x - 30, 0, x + 30, 0, 540 + (i - 3) * 60, 1420, 540 + (i - 3) * 30, 1420), fill=(255, 246, 210, 26))
    shape(d, ellipse_pts(540, 1440, 470, 90), (214, 210, 220), 1)              # Drehbuehne
    shape(d, ellipse_pts(540, 1420, 440, 70), (236, 232, 240), 2, lw=4)
    shape(d, [(-20, 1600), (1100, 1600), (1100, 1940), (-20, 1940)], (30, 32, 52), 3)
    for i in range(9):   # Publikum (Hinterkoepfe)
        x = 40 + i * 125
        shape(d, ellipse_pts(x, 1720 + (i % 2) * 40, 70, 70), [(60, 44, 36), (200, 170, 90), (40, 34, 30), (110, 70, 44)][i % 4], 10 + i)
        shape(d, ellipse_pts(x, 1880, 95, 90), [(120, 50, 50), (60, 80, 130), (90, 90, 96), (70, 110, 80)][i % 4], 20 + i)
    return img

def s01():
    img, hz = places.ferrari_office()
    figure(img, 560, hz + 180, 185, ENZO, face=-1, mouth="talk", brow=-0.04, arms=("desk", "desk"), seed=7, seated=True)
    places.desk(img, 160, 1060, 1420, 1920)
    spoken(img, "You may be able to\ndrive a tractor…\nbut you'll never\nhandle a Ferrari.", 540, 150, 72)
    return done(img)

def s02():
    img, hz = places.ferrari_office()
    img = img.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(8 * SS))
    from crayon2 import bust
    bust(img, 540, 980, 340, FERRUCCIO, face=1, mouth="frown", brow=0.1, seed=11)
    return done(img)

def s03():
    img, hz = places.workshop_1948()
    d = ImageDraw.Draw(img, "RGBA")
    places.cartoon_tractor(d, 430, hz + 260, 620)
    figure(img, 290, hz + 300, 150, FERRUCCIO, face=1, mouth="smile", arms=("hip", "rest"), seed=3)
    sticky(img, 640, 300, ["FERRUCCIO LAMBORGHINI", "Italy, 1948"], w=700)
    return done(img)

def s04():
    img, hz = outside_workshop()
    car(img, 420, hz + 260, 600, (204, 34, 40), face=-1)
    figure(img, 250, hz + 320, 150, FERRUCCIO, face=1, mouth="smile", arms=("hip", "point"), seed=4)
    return done(img)

def s05():
    img, hz = outside_workshop()
    car(img, 420, hz + 260, 600, (204, 34, 40), face=-1)
    smoke(img, [(760, 1340, 90), (820, 1210, 120), (730, 1080, 140), (860, 960, 110)])
    figure(img, 250, hz + 320, 150, FERRUCCIO, face=1, mouth="frown", brow=0.08, arms=("down", "down"), seed=5)
    return done(img)

def s06():
    img, hz = places.workshop_1948()
    img = img.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(6 * SS))
    d = ImageDraw.Draw(img, "RGBA")
    hc = figure(img, 420, H + 120, 230, MECHANIC, face=1, mouth="talk", brow=-0.1, arms=("down", "point"), seed=6)
    cap(img, 420, hc, 230)
    clutch_drawing(ImageDraw.Draw(img, "RGBA"), 820, 980, 150, 60)
    spoken(img, "Boss… it's the same\nclutch as our tractors!", 540, 190, 70)
    return done(img)

def s07():
    img = Image.new("RGB", (W * SS, H * SS), GREY)
    d = ImageDraw.Draw(img, "RGBA")
    hand_text(img, "The same clutch", 540, 230, 96)
    clutch_drawing(d, 300, 760, 190, 10); clutch_drawing(d, 780, 760, 190, 20)
    sticky(img, 300, 1050, ["TRACTOR"], angle=3, w=300)
    sticky(img, 780, 1050, ["FERRARI"], angle=-3, w=300)
    price_tag(d, 300, 1270, "10 lire", (40, 110, 60), 30)
    price_tag(d, 780, 1270, "1,000 lire", (196, 40, 40), 31)
    hand_text(img, "100x the price!", 540, 1520, 92, ORANGE)
    return done(img)

def s08():
    img, hz = places.ferrari_office()
    figure(img, 660, hz + 180, 190, ENZO, face=-1, mouth="smirk", arms=("desk", "desk"), seed=7, seated=True)
    places.desk(img, 320, 1100, 1420, 1920)
    figure(img, 190, H + 40, 180, FERRUCCIO, face=1, mouth="talk", brow=0.06, arms=("down", "point"), seed=9)
    spoken(img, "Enzo, your cars\nhave a problem.", 380, 260, 70)
    return done(img)

def s09():
    img, hz = places.ferrari_office()
    figure(img, 560, hz + 180, 190, ENZO, face=-1, mouth="talk", brow=-0.06, arms=("desk", "point"), seed=17, seated=True)
    places.desk(img, 160, 1060, 1420, 1920)
    spoken(img, "Go back to\nyour tractors.", 540, 220, 84)
    return done(img)

def s10():
    img = Image.new("RGB", (W * SS, H * SS), (36, 38, 48))
    from crayon2 import bust
    bust(img, 540, 1000, 380, FERRUCCIO, face=1, mouth="line", brow=0.14, seed=21)
    return done(img)

def s11():
    img, hz = factory_1963()
    figure(img, 200, hz + 330, 140, FERRUCCIO, face=1, mouth="smile", arms=("hip", "point"), seed=23)
    sticky(img, 760, 330, ["1963"], angle=-4, w=300)
    return done(img)

def s12():
    img = motor_show()
    car(img, 170, 1400, 740, (246, 184, 30), low=True, seed=330)
    d = ImageDraw.Draw(img, "RGBA")
    for (x, y) in [(150, 520), (930, 600), (260, 860), (840, 900)]:
        for k in range(4, 0, -1):
            d.ellipse(S(x - 24 * k, y - 24 * k, x + 24 * k, y + 24 * k), fill=(255, 255, 255, 30))
        shape(d, [(x, y - 40), (x + 12, y - 12), (x + 40, y), (x + 12, y + 12), (x, y + 40), (x - 12, y + 12), (x - 40, y), (x - 12, y - 12)], (255, 255, 255), 600 + x, lw=3)
    sticky(img, 540, 300, ["1966 · LAMBORGHINI MIURA"], angle=3, w=720)
    return done(img)

def s13():
    img = Image.new("RGB", (W * SS, H * SS), GREY)
    car(img, 40, 1620, 480, (204, 34, 40), face=-1, seed=340)
    car(img, 560, 1620, 480, (246, 184, 30), low=True, seed=350)
    figure(img, 330, 1350, 150, ENZO, face=-1, mouth="frown", brow=0.06, arms=("hip", "hip"), seed=31)
    figure(img, 750, 1350, 150, FERRUCCIO, face=1, mouth="smile", arms=("hip", "hip"), seed=33)
    hand_text(img, "his biggest rival.", 540, 380, 92, ORANGE)
    return done(img)

SCENES = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13]

if __name__ == "__main__":
    import os
    os.makedirs("frames_v6", exist_ok=True)
    tiles = []
    for i, f in enumerate(SCENES):
        im = f(); im.save(f"frames_v6/s{i + 1:02d}.png"); tiles.append(im)
    tw, th = 270, 480
    sheet = Image.new("RGB", (7 * (tw + 8) + 8, 2 * (th + 8) + 8), (0, 0, 0))
    for i, t in enumerate(tiles):
        sheet.paste(t.resize((tw, th)), (8 + (i % 7) * (tw + 8), 8 + (i // 7) * (th + 8)))
    sheet.save("STORYBOARD_V6.png"); print("ok")
