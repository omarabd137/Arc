"""Zwei Testbilder fuer den neuen Detail-Look (Ort + Requisite), bevor der ganze Short gebaut wird."""
import os
from mcd_kit import *

os.chdir(HERE)

def frame_a():
    img, d = california_bg(1180)
    palm(d, 60, 1180, 560, 1); palm(d, 1030, 1180, 640, 2)
    car50(d, 760, 1300, 300, (120, 170, 160))
    mcd_stand_1948(img, cx=600, base=1180, scale=1.05)
    for i, x in enumerate([330, 410, 490, 570, 650]):        # Schlange vor den Fenstern
        figure(img, x, 1290 + (i % 2) * 8, 52, GUEST[i % 6], face=1, mouth="line", seed=200 + i)
    figure(img, 200, 1840, 125, MAC, face=1, mouth="smile", arms=("hip", "rest"), seed=301)
    figure(img, 880, 1850, 118, DICK, face=-1, mouth="smile", arms=("rest", "hip"), seed=302)
    sticky(img, 540, 300, ["THE McDONALD BROTHERS", "San Bernardino, 1948"], w=760)
    return done(img)

def frame_b():
    img = Image.new("RGB", (W * SS, H * SS), (110, 84, 62))       # Holztisch
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(14):
        y = 80 + k * 140
        stroke(d, [(0, y), (W, y + 20)], lw=3, color=(96, 72, 54))
    rnd = random.Random(4)
    for i in range(10):
        dollar_bill(img, rnd.randint(140, 940), rnd.randint(1250, 1700), 360, angle=rnd.randint(-35, 35), seed=i)
    contract(img, 540, 900, 600)
    dollar_bill(img, 300, 1500, 380, angle=-12); dollar_bill(img, 800, 1460, 380, angle=16)
    return done(img)

if __name__ == "__main__":
    a, b = frame_a(), frame_b()
    a.save("TEST_A_stand.png"); b.save("TEST_B_contract.png")
    sheet = Image.new("RGB", (1080 + 1080 + 20, 1920), (0, 0, 0))
    sheet.paste(a, (0, 0)); sheet.paste(b, (1100, 0))
    sheet.resize((1090, 960)).save("TEST_SHEET.png"); print("ok")
