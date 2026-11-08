"""Gezeichnete Cartoon-Orte im Crayon-Stil (keine Fotos): flache Pastellfarben, zittrige Tusche-Linien."""
from PIL import Image, ImageDraw
from crayon_kit import *

def base_room(wall, wall_low, floor, floor_line, horizon=1380):
    img = Image.new("RGB", (W * SS, H * SS), wall)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle(S(0, horizon - 260, W, horizon), fill=wall_low)
    shape(d, [(-20, horizon), (W + 20, horizon), (W + 20, H + 20), (-20, H + 20)], floor, 1)
    for k in range(1, 7):                     # Boden-Dielen / Fugen
        y = horizon + k * k * 14
        stroke(d, [(0, y), (W, y)], lw=3, color=floor_line)
    return img, d, horizon

def cartoon_tractor(d, x, y, w, color=(236, 128, 36), seed=60):
    h = w * 0.75
    shape(d, [(x + w * 0.12, y - h * 0.55), (x + w * 0.66, y - h * 0.62), (x + w * 0.7, y - h * 0.32), (x + w * 0.1, y - h * 0.3)], color, seed)       # Motorhaube
    for gy in range(4):                                                                                                                          # Kuehlergrill
        stroke(d, [(x + w * 0.14, y - h * (0.5 - gy * 0.05)), (x + w * 0.3, y - h * (0.5 - gy * 0.05))], lw=3)
    shape(d, [(x + w * 0.6, y - h * 0.62), (x + w * 0.86, y - h * 0.66), (x + w * 0.88, y - h * 0.3), (x + w * 0.62, y - h * 0.3)], sh(color, 0.85), seed + 1)  # Fahrersitz-Block
    stroke(d, [(x + w * 0.7, y - h * 0.66), (x + w * 0.64, y - h * 0.88)], lw=6)                                                                  # Lenkrad-Stange
    shape(d, ellipse_pts(x + w * 0.63, y - h * 0.9, w * 0.07, w * 0.025), (60, 56, 60), seed + 2, lw=5)
    shape(d, [(x + w * 0.2, y - h * 0.62), (x + w * 0.25, y - h * 0.62), (x + w * 0.25, y - h * 0.86), (x + w * 0.2, y - h * 0.86)], (60, 56, 60), seed + 3, lw=5)  # Auspuff
    for cx_, r in ((x + w * 0.24, h * 0.17), (x + w * 0.76, h * 0.31)):                                                                         # Raeder
        shape(d, ellipse_pts(cx_, y - r, r, r), (44, 40, 42), seed + 4)
        shape(d, ellipse_pts(cx_, y - r, r * 0.5, r * 0.5), color, seed + 5, lw=5)
        for k in range(8):
            a = k * math.pi / 4
            stroke(d, [(cx_ + math.cos(a) * r * 0.75, y - r + math.sin(a) * r * 0.75), (cx_ + math.cos(a) * r * 0.95, y - r + math.sin(a) * r * 0.95)], lw=5, color=(80, 76, 80))

def workshop_1948():
    """Traktorwerkstatt nach dem Krieg: Backstein, Rolltor, Regale mit Teilen, Militaer-Kanister."""
    img, d, hz = base_room((222, 196, 164), (204, 176, 144), (150, 132, 116), (128, 112, 98))
    # Backstein-Muster
    for row, y in enumerate(range(80, hz - 260, 46)):
        for x in range(-40 + (row % 2) * 45, W, 90):
            d.rectangle(S(x + 4, y + 4, x + 86, y + 42), fill=(210, 182, 150))
    # grosses offenes Tor mit Blick nach draussen (Hof, Huegel)
    shape(d, [(560, 420), (1040, 420), (1040, hz), (560, hz)], (184, 216, 236), 2)
    shape(d, [(560, 980), (1040, 940), (1040, hz), (560, hz)], (160, 190, 120), 3, lw=5)
    shape(d, [(560, 1030), (760, 930), (1040, 990), (1040, hz), (560, hz)], (140, 172, 104), 4, lw=5)
    for y in range(420, 640, 30):      # hochgezogenes Rolltor
        stroke(d, [(560, y), (1040, y)], lw=4, color=(120, 110, 100))
    shape(d, [(560, 410), (1040, 410), (1040, 640), (560, 640)], (176, 164, 150), 5)
    # Regal mit Ersatzteilen links
    shape(d, [(40, 520), (440, 520), (440, 540), (40, 540)], (140, 100, 68), 6, lw=5)
    shape(d, [(40, 760), (440, 760), (440, 780), (40, 780)], (140, 100, 68), 7, lw=5)
    for i, (x, col) in enumerate([(70, (120, 130, 90)), (170, (110, 110, 118)), (270, (150, 70, 50)), (350, (120, 130, 90))]):
        shape(d, [(x, 440), (x + 70, 440), (x + 70, 520), (x, 520)], col, 10 + i, lw=5)
    for i, x in enumerate([80, 200, 320]):
        shape(d, ellipse_pts(x + 40, 715, 42, 42), (96, 96, 104), 20 + i, lw=5)
        shape(d, ellipse_pts(x + 40, 715, 14, 14), (60, 60, 66), 30 + i, lw=4)
    # Militaer-Kanister + Kisten am Boden (Kriegsreste)
    for i, x in enumerate([30, 140]):
        shape(d, [(x, hz - 150), (x + 90, hz - 150), (x + 90, hz + 10), (x, hz + 10)], (98, 110, 70), 40 + i)
        stroke(d, [(x + 15, hz - 110), (x + 75, hz - 40)], lw=4, color=(70, 80, 50))
    shape(d, [(260, hz - 120), (420, hz - 120), (420, hz + 20), (260, hz + 20)], (170, 130, 84), 45)
    stroke(d, [(260, hz - 50), (420, hz - 50)], lw=4)
    # Werkbank
    shape(d, [(0, 1000), (520, 1000), (520, 1040), (0, 1040)], (150, 108, 70), 46, lw=6)
    stroke(d, [(30, 1040), (30, hz)], lw=10); stroke(d, [(490, 1040), (490, hz)], lw=10)
    # Haengelampe
    stroke(d, [(300, 0), (300, 220)], lw=4)
    shape(d, [(240, 220), (360, 220), (330, 170), (270, 170)], (90, 110, 90), 47, lw=5)
    d.polygon(S(240, 222, 360, 222, 520, 900, 80, 900), fill=(255, 240, 200, 40))
    return img, hz

def ferrari_office():
    """Enzos Buero in Maranello, 1960er: Holzvertaefelung, Fenster auf rote Fabrikhallen, Rennwagen-Bilder."""
    img, d, hz = base_room((236, 220, 196), (150, 104, 70), (120, 78, 50), (100, 64, 40), horizon=1460)
    # Holzvertaefelung unten
    for x in range(0, W, 120):
        stroke(d, [(x, hz - 260), (x, hz)], lw=4, color=(120, 80, 50))
    stroke(d, [(0, hz - 262), (W, hz - 262)], lw=7)
    # Fenster mit Blick auf rote Fabrikhallen
    shape(d, [(560, 300), (1000, 300), (1000, 900), (560, 900)], (176, 214, 236), 2)
    shape(d, [(560, 640), (700, 600), (700, 900), (560, 900)], (196, 62, 52), 3, lw=5)
    shape(d, [(700, 560), (1000, 520), (1000, 900), (700, 900)], (214, 74, 60), 4, lw=5)
    shape(d, [(740, 610), (960, 600), (960, 650), (740, 660)], (248, 214, 70), 5, lw=4)   # gelbes Schild (ohne Logo)
    for x in range(730, 990, 60):
        shape(d, [(x, 700), (x + 34, 700), (x + 34, 760), (x, 760)], (150, 196, 220), 6 + x, lw=3)
    stroke(d, [(780, 300), (780, 900)], lw=8); stroke(d, [(560, 600), (1000, 600)], lw=8)
    shape(d, [(540, 290), (1020, 290), (1020, 310), (540, 310)], (150, 104, 70), 7, lw=5)
    # Bilder von roten Rennwagen an der Wand
    for i, (x, y) in enumerate([(70, 330), (300, 420)]):
        shape(d, [(x, y), (x + 190, y), (x + 190, y + 140), (x, y + 140)], (250, 246, 236), 20 + i, lw=6)
        shape(d, [(x + 25, y + 95), (x + 60, y + 70), (x + 140, y + 70), (x + 170, y + 95), (x + 170, y + 110), (x + 25, y + 110)], (204, 36, 40), 30 + i, lw=4)
        for wx in (x + 55, x + 140):
            shape(d, ellipse_pts(wx, y + 112, 12, 12), INK, 40 + i + wx, lw=2)
    # Pokal auf Regal
    shape(d, [(110, 700), (330, 700), (330, 720), (110, 720)], (150, 104, 70), 50, lw=5)
    shape(d, [(190, 620), (250, 620), (240, 660), (230, 690), (210, 690), (200, 660)], (232, 190, 80), 51, lw=5)
    return img, hz

def desk(img, x0, x1, top, bottom, seed=80):
    d = ImageDraw.Draw(img, "RGBA")
    shape(d, [(x0, top), (x1, top), (x1, bottom), (x0, bottom)], (126, 80, 48), seed)
    shape(d, [(x0 - 20, top - 30), (x1 + 20, top - 30), (x1 + 20, top + 10), (x0 - 20, top + 10)], (150, 98, 60), seed + 1)
    for k in range(2):
        y = top + 80 + k * 150
        shape(d, [(x0 + 40, y), (x0 + 240, y), (x0 + 240, y + 110), (x0 + 40, y + 110)], (140, 90, 54), seed + 2 + k, lw=5)
        shape(d, ellipse_pts(x0 + 140, y + 55, 14, 9), (220, 180, 90), seed + 5 + k, lw=3)
    # Papiere + Telefon
    shape(d, [(x0 + 60, top - 52), (x0 + 250, top - 58), (x0 + 255, top - 30), (x0 + 62, top - 28)], (250, 248, 240), seed + 8, lw=4)
    shape(d, [(x1 - 230, top - 80), (x1 - 110, top - 80), (x1 - 100, top - 30), (x1 - 240, top - 30)], (40, 40, 44), seed + 9, lw=5)

if __name__ == "__main__":
    # Test 1: Ferruccio in seiner Traktorwerkstatt
    a, hz = workshop_1948()
    d = ImageDraw.Draw(a, "RGBA")
    cartoon_tractor(d, 470, hz + 180, 560)
    person(a, 300, hz + 300, 820, FERRUCCIO, face=1, expr="smug", seed=3)
    place_label(a, "Italy, 1948", 150)
    a = done(a); a.save("CR2_test_1.png")
    # Test 2: Enzo hinter seinem Schreibtisch in Maranello
    b, hz = ferrari_office()
    person(b, 560, hz + 120, 1120, ENZO, face=-1, expr="smug", talk=True, seed=7)
    desk(b, 140, 940, 1300, 1820)
    speech(b, 40, 240, 1000, ["You may be able to drive a tractor…", "but you'll never handle a Ferrari."], (560, 520))
    place_label(b, "Maranello", 100)
    b = done(b); b.save("CR2_test_2.png")
    sheet = Image.new("RGB", (2 * 540 + 30, 980), (0, 0, 0))
    sheet.paste(a.resize((540, 960)), (10, 10)); sheet.paste(b.resize((540, 960)), (560, 10))
    sheet.save("STIL_CRAYON_CARTOON.png"); print("ok")
