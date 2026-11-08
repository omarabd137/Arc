"""Short #08 v2 – neue, realistischere Szenen (echte Karten, Ferrari-Look, Logos, Menschenschlange, Geldstapel bis ins All).
Nutzt Timing, Ton, Zaehler und Untertitel aus short08.py."""
import sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import short08 as B
from short08 import W, H, INK, WHITE, YEL, RED, GREEN, GOLD, F, txt, rr, pop_text, stamp, glow, vgrad, blur, ramp, ease, back, WT, GT, SEGS, hud, money_at, fmt, dollar_bill, cybertruck, starship
import crayon2 as C, props8 as P, world

_bg = {}
def cache(name, fn):
    if name not in _bg: _bg[name] = fn()
    return _bg[name].copy()

# ---------------- Orte ----------------
def _monaco():
    im = vgrad((120, 190, 240), (255, 214, 170)); d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(0, 640), (200, 520), (420, 600), (640, 480), (860, 560), (1080, 500), (1080, 900), (0, 900)], fill=(96, 140, 110))   # Huegel
    r = random.Random(6)
    for i in range(26):   # pastellfarbene Haeuser am Hang
        x = r.randint(-40, 1040); y = r.randint(560, 820); w = r.randint(70, 140); h = r.randint(80, 200)
        c = r.choice([(250, 220, 180), (246, 200, 170), (240, 236, 220), (230, 190, 160), (250, 240, 200)])
        d.rectangle((x, y - h, x + w, y), fill=c, outline=(150, 120, 100), width=3); d.polygon([(x - 6, y - h), (x + w + 6, y - h), (x + w / 2, y - h - 30)], fill=(196, 96, 70))
        for wy in range(y - h + 20, y - 10, 34):
            for wx in range(x + 12, x + w - 12, 28): d.rectangle((wx, wy, wx + 14, wy + 18), fill=(120, 160, 200))
    d.rectangle((0, 900, W, 1180), fill=(40, 120, 190))                                         # Hafenbecken
    for y in range(910, 1180, 26): d.line((0, y, W, y + 4), fill=(70, 150, 210), width=3)
    for i in range(5):   # Jachten
        x = 60 + i * 210; d.polygon([(x, 1000), (x + 170, 1000), (x + 150, 1040), (x + 15, 1040)], fill=WHITE, outline=INK); d.rectangle((x + 40, 965, x + 130, 1000), fill=(240, 240, 244), outline=INK, width=3)
    d.rectangle((0, 1180, W, H), fill=(70, 72, 80)); d.rectangle((0, 1180, W, 1200), fill=(230, 230, 230))   # Kuestenstrasse
    for x in range(0, W, 140): d.rectangle((x, 1440, x + 70, 1452), fill=(250, 250, 250))
    for x in (90, 990):   # Palmen
        d.line((x, 1180, x + 10, 900), fill=(120, 80, 50), width=18)
        for a in range(6): d.line((x + 10, 900, x + 10 + math.cos(a) * 120, 900 - 40 + math.sin(a) * 60), fill=(60, 140, 70), width=16)
    return blur(im, 2)
def _stadium():
    im = vgrad((10, 14, 36), (30, 46, 86)); d = ImageDraw.Draw(im, "RGBA")
    for x in (120, 960):
        d.rectangle((x - 10, 160, x + 10, 640), fill=(80, 84, 96)); d.rectangle((x - 90, 120, x + 90, 200), fill=(255, 252, 230), outline=(90, 90, 100), width=4)
    glow(im, 120, 160, 220, (255, 250, 220), 170); glow(im, 960, 160, 220, (255, 250, 220), 170); d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(0, 560), (W, 560), (W, 1020), (0, 1020)], fill=(46, 52, 74))
    r = random.Random(5)
    for _ in range(2600):
        x, y = r.randint(0, W), r.randint(570, 1010); d.ellipse((x, y, x + 6, y + 6), fill=r.choice([(220, 60, 60), (40, 70, 180), (240, 240, 240), (240, 190, 50), (30, 120, 70)]))
    d.rectangle((0, 1020, W, H), fill=(46, 140, 66))
    for k, y in enumerate(range(1060, H, 110)):
        d.line((0, y, W, y), fill=(245, 245, 245), width=6); txt(d, str(min(50, 10 * (k + 1))), 80, y + 40, 40, (245, 245, 245))
    d.rectangle((0, 1020, W, 1050), fill=(20, 40, 120)); txt(d, "NFL", W // 2, 1035, 26, WHITE)
    return blur(im, 2)
def _city_queue():
    im = vgrad((150, 196, 236), (236, 232, 222)); d = ImageDraw.Draw(im, "RGBA")
    vx, vy = 540, 620
    r = random.Random(9)
    for side in (-1, 1):   # Hochhaeuser in Perspektive
        for k in range(10):
            t = k / 10; x_near = 540 + side * (560 - t * 480); w = 160 * (1 - t * 0.8); h = 900 * (1 - t * 0.75)
            col = r.choice([(170, 180, 196), (196, 186, 170), (150, 164, 184), (210, 200, 188)])
            d.rectangle((min(x_near, x_near + side * w), vy + 80 - h, max(x_near, x_near + side * w), vy + 80 + (1 - t) * 300), fill=col, outline=(110, 116, 130), width=2)
    d.polygon([(0, H), (W, H), (vx + 40, vy + 80), (vx - 40, vy + 80)], fill=(110, 112, 120))   # Strasse
    for k in range(1, 12):
        y = vy + 80 + (H - vy - 80) * (k / 12) ** 2.2; d.line((vx - 20 - (k / 12) ** 2.2 * 500, y, vx + 20 + (k / 12) ** 2.2 * 500, y), fill=(122, 124, 132), width=2)
    flag(d, 900, 300, 1.0)
    return blur(im, 1)
def flag(d, x, y, s):
    d.line((x, y, x, y + 300 * s), fill=(150, 150, 156), width=8)
    for k in range(13): d.rectangle((x, y + k * 12 * s, x + 220 * s, y + (k + 1) * 12 * s), fill=(178, 34, 52) if k % 2 == 0 else WHITE)
    d.rectangle((x, y, x + 95 * s, y + 84 * s), fill=(60, 59, 110))
def _space_stack():
    im = Image.new("RGBA", (W, H)); a = np.linspace(0, 1, H)[:, None]
    top = np.array([4, 6, 20]); mid = np.array([30, 60, 140]); low = np.array([150, 200, 240])
    col = np.where(a < 0.45, top * (1 - a / 0.45) + mid * (a / 0.45), mid * (1 - (a - 0.45) / 0.55) + low * ((a - 0.45) / 0.55))
    arr = np.repeat(col[:, None, :], W, 1).astype(np.uint8); im = Image.fromarray(arr, "RGB").convert("RGBA"); d = ImageDraw.Draw(im, "RGBA")
    r = random.Random(4)
    for _ in range(160): x, y = r.randint(0, W), r.randint(0, 800); d.ellipse((x, y, x + 3, y + 3), fill=(255, 255, 255, r.randint(90, 230)))
    d.ellipse((-600, 1640, 1680, 3200), fill=(70, 130, 200)); d.ellipse((-600, 1650, 1680, 3200), outline=(170, 210, 250, 140), width=20)
    for cx_ in (180, 820): d.ellipse((cx_ - 160, 1500, cx_ + 160, 1580), fill=(255, 255, 255, 160))
    return im

# ---------------- Szenen ----------------
def s0(lt, T, gt):   # How long would it take to spend all of Elon Musk's money?
    f = B.bg_space(); d = ImageDraw.Draw(f, "RGBA")
    cybertruck(d, 520, 1600, 0.75)
    C.person(f, C.ELON, 330, 900, 150, "grin", ("hip", "hip"), 1, legs=True)
    k = ramp(lt, WT(0, "money") - 0.2, WT(0, "money") + 0.3)
    if k > 0:
        for i in range(4): P.bill_stack(ImageDraw.Draw(f), 620 + i * 110, 1500 - (120 + i * 60) * ease(k), 1500, 90)
    d = ImageDraw.Draw(f, "RGBA"); rr(d, (40, 70, 1040, 320), YEL, INK, 8, 24); txt(d, "HOW LONG TO SPEND", 540, 150, 70); txt(d, "ELON'S MONEY?", 540, 245, 80)
    return f
def s1(lt, T, gt):   # Let's find out.
    f = B.bg_space(); C.person(f, C.ELON, 330, 900, 150, "smug", ("cross", "cross"), 1, legs=True)
    k = back(ramp(lt, 0.0, 0.4)); card = Image.new("RGBA", (560, 340)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((4, 4, 556, 336), 34, fill=(16, 16, 20), outline=GOLD, width=8); cd.rectangle((60, 100, 160, 175), fill=GOLD); cd.text((280, 270), "UNLIMITED", font=F(46), fill=GOLD, anchor="mm")
    card = card.rotate(-14, expand=True, resample=Image.BICUBIC); f.alpha_composite(card, (int(520 + (1 - k) * 700), 1050))
    for i in range(10):   # Funken beim Wisch
        a = i * 0.6; rr_ = 120 + 60 * k; ImageDraw.Draw(f).line((800, 1250, 800 + math.cos(a) * rr_, 1250 + math.sin(a) * rr_), fill=(255, 220, 120), width=6)
    return f
def s2(lt, T, gt):   # He's got 850 billion dollars.  -> Stapel aus 100ern bis ins All
    f = cache("space_stack", _space_stack); d = ImageDraw.Draw(f, "RGBA")
    P.iss(d, 760, 520, 0.9); txt(d, "SPACE STATION  ·  400 km", 760, 610, 34, WHITE, font="C:/Windows/Fonts/arialbd.ttf")
    k = ease(ramp(lt, WT(2, "850") - 0.1, T + 0.2)); top = 1600 - 1520 * k
    P.bill_stack(d, 300, top, 1600, 120)
    C.person(f, C.ELON, 170, 1480, 60, "grin", ("up", "up"), 1, legs=True)
    pop_text(f, "$850,000,000,000", 540, 200, 92, GOLD, ramp(lt, WT(2, "850") - 0.05, WT(2, "850") + 0.2), box=(14, 14, 20))
    if k > 0.85: pop_text(f, "IN $100 BILLS: 900+ km HIGH", 620, 1000, 50, WHITE, ramp(lt, T * 0.75, T * 0.95), box=(30, 90, 50))
    return f
def _ferraris(f, lt, k_in, rows=2):
    for row in range(rows):
        for i in range(4):
            prog = ease(ramp(k_in, row * 0.15 + i * 0.07, row * 0.15 + i * 0.07 + 0.45)); x = 1300 - prog * 1500 + i * 440
            if x < 1150: P.ferrari(f, x, 1400 + row * 260, 0.9, face=-1)
def s3(lt, T, gt):   # Step one: every Ferrari built last year.
    f = cache("monaco", _monaco); hud(f, gt)
    _ferraris(f, lt, ramp(lt, WT(3, "Ferrari") - 0.2, T))
    pop_text(f, "EVERY FERRARI", 540, 430, 96, WHITE, ramp(lt, WT(3, "Ferrari") - 0.05, WT(3, "Ferrari") + 0.2), box=(212, 22, 30)); return f
def s4(lt, T, gt):   # All thirteen thousand.  -> Luftbild: riesiges Meer aus roten Autos
    f = Image.new("RGBA", (W, H), (78, 80, 88, 255)); d = ImageDraw.Draw(f, "RGBA"); hud(f, gt)
    n = int(1400 * ease(ramp(lt, 0, T * 0.9)) + 40)
    for i in range(n):
        row, col = divmod(i, 28); x = 20 + col * 37; y = 330 + row * 30
        if y > 1900: break
        d.rounded_rectangle((x, y, x + 30, y + 18), 6, fill=(212, 22, 30)); d.rectangle((x + 10, y + 3, x + 20, y + 15), fill=(40, 44, 56))
    cnt = int(13640 * ease(ramp(lt, 0, T)))
    pop_text(f, "{:,} FERRARIS".format(cnt), 540, 1000, 104, WHITE, 1.0, box=(212, 22, 30)); return f
def s5(lt, T, gt):   # Seven billion... and he didn't even blink.
    f = cache("monaco", _monaco); hud(f, gt); _ferraris(f, lt, 1.0)
    bl = WT(5, "blink")
    C.person(f, C.ELON, 540, 820, 140, "neutral" if lt < bl else "smug", ("down", "hold"), 0, legs=True)
    d = ImageDraw.Draw(f, "RGBA"); rr(d, (612, 960, 670, 1040), (250, 250, 250), INK, 4, 8); d.arc((656, 975, 700, 1015), 270, 90, fill=INK, width=5)
    stamp(f, "-$7 BILLION", 540, 560, 96, RED, ramp(lt, 0.0, 0.25), -6)
    pop_text(f, "*yawn*", 800, 700, 56, WHITE, ramp(lt, bl - 0.25, bl)); return f
def _mcd():
    im = vgrad((150, 200, 240), (240, 230, 214)); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 1300, W, H), fill=(120, 122, 130))
    d.rectangle((140, 620, 940, 1300), fill=(218, 41, 28), outline=INK, width=8); d.rectangle((200, 880, 880, 1300), fill=(250, 244, 230), outline=INK, width=6)
    for x in (300, 540, 780): d.rectangle((x - 95, 940, x + 95, 1180), fill=(160, 210, 236), outline=INK, width=5)
    d.rectangle((180, 650, 900, 840), fill=(255, 199, 44), outline=INK, width=6); txt(d, "McDonald's", 610, 745, 70, (218, 41, 28))
    P.golden_arches(d, 290, 745, 130, bg=(218, 41, 28))
    d.line((980, 1300, 980, 420), fill=(150, 150, 156), width=20); P.golden_arches(d, 980, 360, 220)   # Mast-Schild
    return blur(im, 2)
def s6(lt, T, gt):   # Fine.
    f = cache("mcd", _mcd); hud(f, gt); C.person(f, C.ELON, 420, 980, 130, "smug", ("shrug", "shrug"), 0, legs=True); return f
def s7(lt, T, gt):   # We're buying McDonald's.
    f = cache("mcd", _mcd); hud(f, gt); d = ImageDraw.Draw(f, "RGBA")
    C.person(f, C.ELON, 360, 980, 130, "grin", ("down", "give"), 1, legs=True)
    k = back(ramp(lt, WT(7, "McDonald's") - 0.15, WT(7, "McDonald's") + 0.25))
    if k > 0:
        kx, ky = 640, int(1420 - 260 * k); d.ellipse((kx - 55, ky - 55, kx + 55, ky + 55), outline=GOLD, width=20); d.rectangle((kx + 45, ky - 11, kx + 240, ky + 11), fill=GOLD); d.rectangle((kx + 180, ky + 8, kx + 210, ky + 46), fill=GOLD)
    return f
_WORLD = None
def _world_map():
    global _WORLD
    im = vgrad((24, 46, 92), (12, 24, 52)); d = ImageDraw.Draw(im, "RGBA")
    polys, pr = world.world_polys((30, 560, 1050, 1260))
    for cont, p in polys: d.polygon(p, fill=(66, 124, 92), outline=(30, 60, 50))
    _WORLD = polys; return im
def _rand_land(r, polys, weights):
    import matplotlib.path as mp   # nur wenn vorhanden
    return None
def s8(lt, T, gt):   # The entire company.  -> echte Weltkarte, Restaurants ploppen auf
    f = cache("world", _world_map); d = ImageDraw.Draw(f, "RGBA"); hud(f, gt)
    # Restaurant-Punkte auf Land (Mittelpunkte zufaelliger Landpolygone, nach Groesse gewichtet)
    r = random.Random(8); polys = _WORLD
    big = [p for c, p in polys if len(p) > 12]
    n = int(260 * ease(ramp(lt, 0, T)))
    for i in range(n):
        p = r.choice(big); a, b, c_ = r.sample(p, 3); w1, w2 = r.random(), r.random()
        if w1 + w2 > 1: w1, w2 = 1 - w1, 1 - w2
        x = a[0] + w1 * (b[0] - a[0]) + w2 * (c_[0] - a[0]); y = a[1] + w1 * (b[1] - a[1]) + w2 * (c_[1] - a[1])
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 199, 44), outline=(120, 70, 0), width=2)
    P.golden_arches(d, 540, 420, 160)
    pop_text(f, "40,000+ RESTAURANTS", 540, 1400, 76, YEL, ramp(lt, 0.1, 0.4))
    stamp(f, "SOLD", 540, 1580, 130, RED, ramp(lt, WT(8, "company") - 0.1, WT(8, "company") + 0.15), -10); return f
def s9(lt, T, gt):   # Free Big Macs forever.
    f = cache("mcd", _mcd); hud(f, gt); f.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 50))); d = ImageDraw.Draw(f, "RGBA")
    for i in range(18):
        rr_ = random.Random(i); x = rr_.uniform(60, 1020); y = -100 + ((lt * 800 + rr_.uniform(0, 1900)) % 2000)
        B.burger(d, x, y, 0.8)
    C.person(f, C.ELON, 540, 900, 140, "grin", ("up", "up"), 0, legs=True)
    pop_text(f, "FREE BIG MACS FOREVER", 540, 560, 74, YEL, ramp(lt, 0, 0.25)); return f
def s10(lt, T, gt):  # Next: the whole NFL.
    f = cache("stadium", _stadium); hud(f, gt); d = ImageDraw.Draw(f, "RGBA")
    k = back(ramp(lt, WT(10, "NFL") - 0.15, WT(10, "NFL") + 0.25))
    if k > 0:
        lay = Image.new("RGBA", (W, H)); P.nfl_shield(ImageDraw.Draw(lay), 540, 760, 300 * k); f.alpha_composite(lay)
    return f
def s11(lt, T, gt):  # All thirty-two teams.
    f = cache("stadium", _stadium); hud(f, gt); d = ImageDraw.Draw(f, "RGBA")
    for i, team in enumerate(P.TEAMS):
        k = back(ramp(lt, i * 0.03, i * 0.03 + 0.28))
        if k > 0: P.helmet(d, 95 + (i % 8) * 128, int(1180 + (i // 8) * 150 + (1 - k) * 800), 0.85, team)
    stamp(f, "SOLD", 540, 820, 140, RED, ramp(lt, WT(11, "teams") - 0.05, WT(11, "teams") + 0.2), -8); return f
def s12(lt, T, gt):  # Super Bowl?
    f = cache("stadium", _stadium); hud(f, gt); d = ImageDraw.Draw(f, "RGBA")
    k = back(ramp(lt, 0, 0.3)); glow(f, 540, 1000, 340, (255, 245, 210), 120 * k); d = ImageDraw.Draw(f, "RGBA")
    fb = P.trophy(d, 540, 1560 - 180 * k, 760); f.alpha_composite(fb, (int(540 - fb.width / 2 + 40), int(1560 - 180 * k - 760 * 0.92)))
    pop_text(f, "SUPER BOWL?", 540, 520, 110, WHITE, ramp(lt, 0.0, 0.2)); return f
def _suite():
    st = cache("stadium", _stadium).crop((0, 380, W, 1700)).resize((W, 820)); im = Image.new("RGBA", (W, H), (40, 36, 44, 255)); im.paste(st, (0, 360))
    d = ImageDraw.Draw(im, "RGBA"); d.rectangle((0, 1180, W, H), fill=(52, 44, 44))   # Loge: Decke + Boden
    d.rectangle((0, 360, W, 1180), outline=(30, 28, 34), width=30)
    for x in (360, 720): d.rectangle((x - 8, 360, x + 8, 1180), fill=(30, 28, 34))                    # Fensterrahmen
    d.rounded_rectangle((180, 1240, 900, 1460), 50, fill=(30, 30, 36), outline=INK, width=8)            # Ledersofa
    d.rounded_rectangle((140, 1160, 260, 1460), 40, fill=(26, 26, 30), outline=INK, width=6); d.rounded_rectangle((820, 1160, 940, 1460), 40, fill=(26, 26, 30), outline=INK, width=6)
    return im
def s13(lt, T, gt):  # That's his living room now.
    f = cache("suite", _suite); hud(f, gt)
    C.person(f, C.ELON, 540, 1080, 130, "smug", ("hold", "down"), 0)
    d = ImageDraw.Draw(f, "RGBA"); d.rounded_rectangle((630, 1250, 676, 1310), 10, fill=(40, 40, 46), outline=INK, width=4)
    d.polygon([(330, 1230), (400, 1230), (390, 1320), (340, 1320)], fill=(220, 50, 50), outline=INK)   # Popcorn
    for i in range(6): d.ellipse((330 + i * 12, 1205 + (i % 2) * 8, 352 + i * 12, 1228 + (i % 2) * 8), fill=(255, 245, 210))
    pop_text(f, "HIS LIVING ROOM", 540, 520, 96, YEL, ramp(lt, WT(13, "living") - 0.1, WT(13, "living") + 0.2)); return f
_USA = None
def _usa_map():
    im = vgrad((40, 70, 130), (20, 36, 80)); d = ImageDraw.Draw(im, "RGBA")
    rings, pr = world.usa_polys((40, 520, 1040, 1180))
    for p in rings: d.polygon(p, fill=(90, 160, 100), outline=(30, 60, 40))
    return im
def s14(lt, T, gt):  # Now the big one: a thousand dollars for every person in America.
    th = WT(14, "thousand")
    if lt < th - 0.1:   # Karte: "the big one"
        f = cache("usa", _usa_map); hud(f, gt)
        pop_text(f, "THE BIG ONE", 540, 1380, 110, YEL, ramp(lt, 0, 0.2)); return f
    f = cache("queue", _city_queue); d = ImageDraw.Draw(f, "RGBA"); hud(f, gt)
    r = random.Random(14); vx, vy = 540, 700
    cols = [(220, 70, 60), (60, 100, 200), (240, 180, 50), (70, 150, 90), (150, 80, 170), (40, 40, 46), (230, 120, 50), (90, 170, 200)]
    people = []
    y = 1560.0   # von vorne nach hinten: Abstand schrumpft mit der Perspektive
    while y > vy + 6:
        s = 0.12 + 1.3 * (y - vy) / (1560 - vy)
        for lane in (-1, 0, 1):
            x = vx + lane * 46 * s + math.sin(y * 0.01) * 26 * s + r.uniform(-6, 6) * s
            people.append((y + r.uniform(-4, 4) * s, x, s, r.choice(cols)))
        y -= 26 * s + 1.2
    for y, x, s, c in sorted(people): P.tiny_person(d, x, y + math.sin(gt * 4 + x) * 2 * s, s, c)
    rr(d, (560, 1500, 1000, 1600), (120, 80, 50), INK, 6, 10)                                          # Tisch
    C.person(f, C.ELON, 820, 1330, 85, "grin", ("give", "give"), -1)
    for i in range(int(8 * ramp(lt, th, T))):
        f.alpha_composite(dollar_bill(None, 0, 0, 0.45, random.Random(i).uniform(-40, 40)), (int(600 + i * 30), int(1480 - i * 8)))
    pop_text(f, "$1,000 FOR EVERY AMERICAN", 540, 400, 62, WHITE, ramp(lt, th - 0.05, th + 0.2), box=(178, 34, 52))
    pop_text(f, "340,000,000 PEOPLE", 540, 500, 54, YEL, ramp(lt, WT(14, "America") - 0.1, WT(14, "America") + 0.2)); return f
def s15(lt, T, gt):  # Including you.
    f = cache("queue", _city_queue); hud(f, gt); f.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    C.person(f, C.YOU, 540, 760, 170, "shock" if lt < 0.35 else "grin", ("up", "down"), 0, legs=True)
    f.alpha_composite(dollar_bill(None, 0, 0, 0.9, 10), (600, 380))
    pop_text(f, "INCLUDING YOU", 540, 1560, 100, YEL, ramp(lt, 0, 0.2)); return f
def s16(lt, T, gt):  # And Elon... still has thirty billion left.  -> Reststapel immer noch hoeher als Flugzeuge
    f = cache("space_stack", _space_stack); d = ImageDraw.Draw(f, "RGBA")
    m = money_at(gt); rr(d, (60, 120, 1020, 400), (20, 20, 28), GOLD, 8, 30); txt(d, "ELON'S MONEY LEFT", 540, 190, 44, (200, 200, 210), font="C:/Windows/Fonts/arialbd.ttf"); txt(d, fmt(m), 540, 310, 82, GOLD)
    P.bill_stack(d, 300, 900, 1600, 120); P.airliner(d, 700, 1100, 1.2); txt(d, "AIRPLANES · 11 km", 700, 1200, 34, WHITE, font="C:/Windows/Fonts/arialbd.ttf")
    txt(d, "STILL 33 km OF $100 BILLS", 640, 820, 40, WHITE, font="C:/Windows/Fonts/arialbd.ttf", stroke=4, sc=INK)
    C.person(f, C.ELON, 520, 1480, 70, "grin" if lt > WT(16, "left") else "smug", ("shrug", "shrug"), 0, legs=True)
    pop_text(f, "STILL $30 BILLION", 540, 1680, 84, GREEN, ramp(lt, WT(16, "left") - 0.05, WT(16, "left") + 0.2)); return f
def s17(lt, T, gt):  # So how long would it take?  -> Sanduhr aus Geld
    f = B.bg_dark(); d = ImageDraw.Draw(f, "RGBA"); cx, cy = 540, 980
    d.polygon([(cx - 260, cy - 420), (cx + 260, cy - 420), (cx + 30, cy), (cx + 260, cy + 420), (cx - 260, cy + 420), (cx - 30, cy)], fill=(200, 220, 240, 60), outline=(220, 230, 240), width=10)
    k = ramp(lt, 0, T + 1.5); d.polygon([(cx - 230 * (1 - k), cy - 380 + 380 * k), (cx + 230 * (1 - k), cy - 380 + 380 * k), (cx, cy)], fill=(118, 170, 110))
    d.polygon([(cx - 230 * k, cy + 380 - 300 * k), (cx + 230 * k, cy + 380 - 300 * k), (cx + 230, cy + 380), (cx - 230, cy + 380)], fill=(118, 170, 110))
    d.line((cx, cy, cx, cy + 380), fill=(118, 170, 110), width=8)
    d.rectangle((cx - 300, cy - 460, cx + 300, cy - 420), fill=(120, 84, 50), outline=INK, width=6); d.rectangle((cx - 300, cy + 420, cx + 300, cy + 460), fill=(120, 84, 50), outline=INK, width=6)
    pop_text(f, "HOW LONG?", 540, 400, 120, YEL, ramp(lt, 0, 0.2)); return f
def s18(lt, T, gt):  # Spending a million dollars every single day... over two thousand years.
    f = B.bg_office(); d = ImageDraw.Draw(f, "RGBA")
    yrs = int(2330 * ease(ramp(lt, WT(18, "day") - 0.3, WT(18, "years"))))
    rr(d, (200, 330, 880, 590), WHITE, INK, 8, 24); txt(d, "YEAR", 540, 390, 44, (120, 120, 130), font="C:/Windows/Fonts/arialbd.ttf"); txt(d, "{:,}".format(max(1, yrs)), 540, 500, 120, INK)
    for i in range(int(12 * ramp(lt, 0.3, T))):   # Kalenderblaetter fliegen
        rr_ = random.Random(i); x = 120 + rr_.uniform(0, 760); y = 1260 - ((lt * 420 + i * 70) % 420)
        rr(d, (x, y, x + 90, y + 100), WHITE, INK, 4, 6); d.rectangle((x, y, x + 90, y + 24), fill=RED)
    pop_text(f, "$1,000,000 EVERY DAY", 540, 760, 70, GREEN, ramp(lt, WT(18, "million") - 0.1, WT(18, "million") + 0.2))
    rr(d, (300, 1300, 780, 1340), (120, 84, 50), INK, 5, 6)                                            # Schreibtisch
    C.person(f, C.YOU, 540, 1050, 150, "worried" if yrs > 1500 else "neutral", ("hold", "hold"), 0)
    pop_text(f, "2,000+ YEARS", 540, 1600, 110, YEL, ramp(lt, WT(18, "years") - 0.1, WT(18, "years") + 0.2)); return f

B.SCENES[:] = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18]

if __name__ == "__main__":
    import av, math as _m
    print(f"Laenge {B.TOTAL:.1f}s")
    if "--stills" in sys.argv:
        tiles = []
        for s in SEGS:
            for fr in (0.35, 0.92): tiles.append(B.frame(s["t0"] + (s["a1"] - s["a0"]) * fr).resize((180, 320)))
        cols = 10; rows = _m.ceil(len(tiles) / cols); sh = Image.new("RGB", (180 * cols, 320 * rows))
        for i, t_ in enumerate(tiles): sh.paste(t_, ((i % cols) * 180, (i // cols) * 320))
        sh.save("STORYBOARD.jpg", quality=88); print("ok"); sys.exit()
    out = av.open("ARC_Short08_Elon_v2.mp4", "w"); vs = out.add_stream("libx264", rate=B.FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "19", "preset": "medium"}
    ast = out.add_stream("aac", rate=B.SR); ast.layout = "mono"
    for k in range(int(B.TOTAL * B.FPS)):
        for p in vs.encode(av.VideoFrame.from_image(B.frame(k / B.FPS))): out.mux(p)
    for p in vs.encode(): out.mux(p)
    au = B.audio()
    for i in range(0, len(au), 1024):
        ch = au[i:i + 1024]; ch = np.pad(ch, (0, 1024 - len(ch))) if len(ch) < 1024 else ch
        af = av.AudioFrame.from_ndarray(ch.reshape(1, -1).astype(np.float32), format="flt", layout="mono"); af.sample_rate = B.SR
        for p in ast.encode(af): out.mux(p)
    for p in ast.encode(): out.mux(p)
    out.close(); print("ok", B.TOTAL)
