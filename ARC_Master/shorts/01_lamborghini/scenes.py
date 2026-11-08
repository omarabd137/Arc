"""Die 12 Schluesselbilder des Shorts (Storyboard). Jede Funktion liefert ein 1080x1920-Bild."""
from PIL import Image, ImageDraw
from arc_kit import *

def s01():
    img = canvas()
    person(img, 300, 1450, 760, FERRUCCIO, "neutral", "down", face=1)
    person(img, 780, 1450, 880, ENZO, "smug", "cross", face=-1)
    label(img, 540, 330, "FERRARI  vs  LAMBORGHINI", 58)
    return img

def s02():
    img = canvas()
    d = ImageDraw.Draw(img)
    for i, (x, y, w, h) in enumerate([(90, 1330, 170, 120), (230, 1370, 130, 80), (120, 1250, 120, 90)]):
        d.rounded_rectangle(S(x, y, x + w, y + h), radius=12 * SS, fill=(74, 88, 60))
    tractor(img, 470, 1450, 520)
    person(img, 270, 1450, 640, FERRUCCIO, "proud", "hold", face=1)
    label(img, 540, 330, "1948", 90)
    return img

def s03():
    img = canvas()
    sports_car(img, 380, 1440, 640)
    person(img, 230, 1450, 700, FERRUCCIO, "proud", "proud", face=1)
    return img

def s04():
    img = canvas()
    d = ImageDraw.Draw(img, "RGBA")
    sports_car(img, 380, 1440, 640)
    for k, (cx, cy, r) in enumerate([(760, 1180, 90), (820, 1060, 120), (720, 960, 140)]):
        d.ellipse(S(cx - r, cy - r, cx + r, cy + r), fill=(180, 180, 190, 150))
    person(img, 230, 1450, 700, FERRUCCIO, "angry", "angry", face=1)
    return img

def s05():
    img = canvas()
    tractor(img, 600, 1450, 420)
    person(img, 330, 1450, 720, MECHANIC, "shock", "hold", face=1)
    clutch(img, 560, 900, 120)
    clutch(img, 810, 1250, 70)
    label(img, 540, 330, "SAME PART", 80)
    return img

def s06():
    img = canvas(floor_y=None)
    clutch(img, 300, 820, 170); clutch(img, 780, 820, 170)
    label(img, 300, 1130, "10 LIRE", 72, (150, 210, 160))
    label(img, 780, 1130, "1,000 LIRE", 72, (230, 90, 90))
    label(img, 300, 560, "TRACTOR", 46, WHITE, box=False)
    label(img, 780, 560, "FERRARI", 46, WHITE, box=False)
    return img

def s07():
    img = canvas()
    d = ImageDraw.Draw(img)
    d.rectangle(S(560, 620, 900, 1450), fill=(60, 40, 30)); d.rectangle(S(585, 650, 875, 1450), fill=(92, 62, 44))
    d.ellipse(S(830, 1040, 860, 1070), fill=GOLD)
    person(img, 330, 1450, 720, FERRUCCIO, "angry", "down", face=1)
    label(img, 730, 540, "MARANELLO", 56)
    return img

def s08():
    img = canvas()
    d = ImageDraw.Draw(img)
    person(img, 700, 1300, 780, ENZO, "smug", "cross", face=-1)
    d.rounded_rectangle(S(380, 1180, 1040, 1450), radius=16 * SS, fill=(70, 46, 32))
    bubble(img, 60, 330, 640, ["You may be able to", "drive a tractor…", "but you'll never", "handle a Ferrari."], (560, 760))
    return img

def s09():
    img = canvas(floor_y=None)
    person(img, 540, 2350, 1900, FERRUCCIO, "angry", "down", face=1)
    return img

def s10():
    img = canvas()
    d = ImageDraw.Draw(img)
    d.rectangle(S(120, 900, 960, 1450), fill=(46, 58, 86))
    for x in range(150, 960, 140):
        d.polygon(S(x, 900, x + 70, 820, x + 140, 900), fill=(56, 70, 102))
    for x in range(190, 920, 150):
        d.rectangle(S(x, 1010, x + 90, 1130), fill=(212, 175, 95))
    d.rectangle(S(260, 1220, 820, 1300), fill=(10, 16, 30))
    label(img, 540, 1260, "AUTOMOBILI LAMBORGHINI", 36, GOLD, box=False, fnt="georgiab.ttf")
    label(img, 540, 400, "1963", 90)
    return img

def s11():
    img = canvas()
    d = ImageDraw.Draw(img, "RGBA")
    for (x, y) in [(150, 700), (930, 760), (240, 1050), (860, 1100)]:
        d.ellipse(S(x - 40, y - 40, x + 40, y + 40), fill=(255, 255, 255, 120))
    sports_car(img, 160, 1420, 760, color=(236, 128, 24), low=True)
    label(img, 540, 400, "1966", 90)
    label(img, 540, 560, "MIURA", 60, WHITE, box=False, fnt="georgiab.ttf")
    return img

def s12():
    img = canvas()
    sports_car(img, 40, 1440, 470, color=(196, 32, 38), face=-1)
    sports_car(img, 570, 1440, 470, color=(236, 128, 24), low=True)
    person(img, 330, 1150, 520, ENZO, "angry", "cross", face=-1)
    person(img, 750, 1150, 520, FERRUCCIO, "proud", "cross", face=1)
    return img

SCENES = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12]

if __name__ == "__main__":
    tiles = [finish(f()) for f in SCENES]
    tw, th = 270, 480
    sheet = Image.new("RGB", (tw * 6 + 70, th * 2 + 30), (0, 0, 0))
    for i, t in enumerate(tiles):
        sheet.paste(t.resize((tw, th)), (10 + (i % 6) * (tw + 10), 10 + (i // 6) * (th + 10)))
        t.save(f"frame_{i + 1:02d}.png")
    sheet.save("STORYBOARD.png")
    print("ok")
