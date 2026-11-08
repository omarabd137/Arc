"""ARC Short #08 - "How Long Would It Take to Spend Elon Musk's Money?" (9:16)
Bauplan Teil 28-36: Hook-Frage + Einkaufstour, Zaehler als roter Faden, alle 1-2 s etwas Neues, Text-Highlights,
Impact-Sounds an jedem Kauf, tiefer Teppich + Takt (keine Melodie), keine Kamera-Zooms, Figuren im Crayon-Prinzip.
Elon erkennbar ueber Frisur, Grinsen, schwarzes T-Shirt "MARS", Cybertruck + Starship im Bild.
Aufruf: python short08.py --stills | (voll)"""
import sys, os, json, re, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "../../sfx_lib"))
import numpy as np, av
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import crayon2 as C
import lib as SFXL

SR, FPS = 48000, 30; W, H = 1080, 1920
BOLD = "C:/Windows/Fonts/ariblk.ttf"; SANS = "C:/Windows/Fonts/arialbd.ttf"
_f = {}
def F(s, p=BOLD):
    k = (p, int(s))
    if k not in _f: _f[k] = ImageFont.truetype(p, int(s))
    return _f[k]
INK = (28, 26, 32); WHITE = (255, 255, 255); YEL = (255, 206, 50); RED = (228, 48, 56); GREEN = (46, 190, 100); GOLD = (246, 196, 72)

SENT = ["How long would it take to spend all of Elon Musk's money?", "Let's find out.", "He's got 850 billion dollars.",
        "Step one: every Ferrari built last year.", "All thirteen thousand.", "Seven billion... and he didn't even blink.", "Fine.",
        "We're buying McDonald's.", "The entire company.", "Free Big Macs forever.", "Next: the whole NFL.", "All thirty-two teams.",
        "Super Bowl?", "That's his living room now.", "Now the big one: a thousand dollars for every person in America.", "Including you.",
        "And Elon... still has thirty billion left.", "So how long would it take?", "Spending a million dollars every single day... over two thousand years."]
def dec(p):
    c = av.open(p); r = av.AudioResampler(format="flt", layout="mono", rate=SR); out = []
    for fr in c.decode(audio=0):
        for f in r.resample(fr): out.append(f.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.float32)
RAW = dec("vo/s08v2.mp3")
WR = [w for w in json.load(open("vo/words_v2.json", encoding="utf-8"))["words"] if w["type"] == "word" and not w["text"].startswith("[")]
SEGS = []; pos = 0; t = 0.05
for si, s in enumerate(SENT):
    n = len(s.split()); ws = WR[pos:pos + n]; pos += n
    if si: t += 0.16
    a0 = max(0, ws[0]["start"] - 0.05); a1 = ws[-1]["end"] + 0.05
    SEGS.append(dict(i=si, t0=t, a0=a0, a1=a1, words=[(w["text"], w["start"] - a0 + t, w["end"] - a0 + t) for w in ws]))
    t += a1 - a0
TOTAL = t + 0.5
ALLW = [w for s in SEGS for w in s["words"]]
def _n(x): return re.sub(r"[^a-z0-9']", "", x.lower())
def WT(si, word, k=1):
    c = 0
    for w, s_, e_ in SEGS[si]["words"]:
        if _n(w) == _n(word):
            c += 1
            if c == k: return s_ - SEGS[si]["t0"]
    raise KeyError((si, word, k))
def GT(si, word, k=1): return SEGS[si]["t0"] + WT(si, word, k)
def ramp(x, a, b): return max(0.0, min(1.0, (x - a) / max(1e-6, b - a)))
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------------- Zaehler (roter Faden) ----------------
BUYS = [(4, "thousand", 7e9), (8, "company", 170e9), (11, "teams", 300e9), (14, "America", 342e9)]
def money_at(gt):
    m = 850e9
    for si, w, c in BUYS:
        t0 = GT(si, w); dur = 1.6 if c > 300e9 else 0.7
        m -= c * ease(ramp(gt, t0, t0 + dur))
    return max(m, 31e9)
def fmt(m): return "${:,.0f}".format(m)

# ---------------- Helfer ----------------
def txt(d, s, x, y, size, col=INK, anchor="mm", font=BOLD, stroke=0, sc=INK):
    d.text((x, y), s, font=F(size, font), fill=col, anchor=anchor, stroke_width=stroke, stroke_fill=sc)
def rr(d, box, fill, out=INK, w=6, r=20): d.rounded_rectangle(box, r, fill=fill, outline=out, width=w)
def pop_text(f, s, x, y, size, col=WHITE, k=1.0, rot=0, box=None):
    if k <= 0: return
    sc = 0.6 + 0.4 * back(min(1, k / 0.5)); sz = int(size * sc)
    lay = Image.new("RGBA", (W, H)); dl = ImageDraw.Draw(lay); fo = F(sz); tw = dl.textlength(s, font=fo)
    if box: dl.rounded_rectangle((x - tw / 2 - 26, y - sz * 0.72, x + tw / 2 + 26, y + sz * 0.72), 16, fill=box, outline=INK, width=6)
    dl.text((x, y), s, font=fo, fill=col, anchor="mm", stroke_width=max(3, sz // 11), stroke_fill=INK)
    if rot: lay = lay.rotate(rot, center=(x, y), resample=Image.BICUBIC)
    f.alpha_composite(lay)
def stamp(f, s, cx, cy, size, col=RED, k=1.0, rot=-10):
    if k <= 0: return
    sc = 1.0 + 0.8 * (1 - ease(min(1, k / 0.3))); size = int(size * sc)
    lay = Image.new("RGBA", (W, H)); dl = ImageDraw.Draw(lay); fo = F(size); tw = dl.textlength(s, font=fo)
    dl.rounded_rectangle((cx - tw / 2 - 28, cy - size * 0.72, cx + tw / 2 + 28, cy + size * 0.72), 16, outline=col, width=max(8, size // 9))
    dl.text((cx, cy), s, font=fo, fill=col, anchor="mm"); f.alpha_composite(lay.rotate(rot, center=(cx, cy), resample=Image.BICUBIC))
def glow(f, cx, cy, r, col, a):
    lay = Image.new("RGBA", (W, H)); ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (int(a),))
    f.alpha_composite(lay.filter(ImageFilter.GaussianBlur(r * 0.45)))
def vgrad(c0, c1):
    a = np.linspace(0, 1, H)[:, None, None]; arr = (np.array(c0) * (1 - a) + np.array(c1) * a).repeat(W, 1)
    return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
def blur(im, r=5): return im.filter(ImageFilter.GaussianBlur(r))

# ---------------- Requisiten ----------------
def cybertruck(d, x, y, s=1.0, col=(176, 182, 190)):
    """unverwechselbarer Keil (Unterkante bei y, Heck links bei x)"""
    P = [(x, y - 90 * s), (x + 20 * s, y - 175 * s), (x + 300 * s, y - 250 * s), (x + 620 * s, y - 165 * s), (x + 640 * s, y - 90 * s), (x + 600 * s, y - 40 * s), (x + 40 * s, y - 40 * s)]
    d.polygon(P, fill=col, outline=INK); d.line(P + [P[0]], fill=INK, width=int(6 * s))
    d.polygon([(x + 170 * s, y - 200 * s), (x + 300 * s, y - 236 * s), (x + 470 * s, y - 192 * s), (x + 300 * s, y - 182 * s)], fill=(40, 46, 56))
    d.line((x + 600 * s, y - 120 * s, x + 640 * s, y - 118 * s), fill=(255, 255, 255), width=int(8 * s))
    for wx in (x + 130 * s, x + 500 * s):
        d.ellipse((wx - 62 * s, y - 104 * s, wx + 62 * s, y + 20 * s), fill=INK); d.ellipse((wx - 30 * s, y - 72 * s, wx + 30 * s, y - 12 * s), fill=(120, 124, 132))
def starship(d, cx, base, h, k_fire=0.0):
    w = h * 0.13
    d.rectangle((cx - w / 2, base - h * 0.82, cx + w / 2, base), fill=(214, 218, 224), outline=INK, width=5)
    d.chord((cx - w / 2, base - h, cx + w / 2, base - h * 0.64), 180, 360, fill=(214, 218, 224), outline=INK, width=5)
    for s in (-1, 1):
        d.polygon([(cx + s * w / 2, base - h * 0.2), (cx + s * w * 1.0, base - h * 0.05), (cx + s * w * 1.0, base), (cx + s * w / 2, base)], fill=(150, 156, 166), outline=INK)
        d.polygon([(cx + s * w / 2, base - h * 0.78), (cx + s * w * 0.9, base - h * 0.72), (cx + s * w / 2, base - h * 0.66)], fill=(150, 156, 166), outline=INK)
    for k in range(4): d.line((cx - w / 2, base - h * (0.2 + k * 0.15), cx + w / 2, base - h * (0.2 + k * 0.15)), fill=(184, 188, 196), width=3)
    if k_fire > 0:
        d.polygon([(cx - w * 0.4, base), (cx + w * 0.4, base), (cx, base + h * 0.25 * k_fire)], fill=(255, 170, 60))
def ferrari(d, x, y, s=1.0, col=(214, 30, 40)):
    """flacher roter Sportwagen (Seitenansicht)"""
    P = [(x, y - 40 * s), (x + 30 * s, y - 75 * s), (x + 120 * s, y - 85 * s), (x + 180 * s, y - 125 * s), (x + 300 * s, y - 128 * s), (x + 370 * s, y - 85 * s), (x + 430 * s, y - 70 * s), (x + 440 * s, y - 35 * s), (x + 10 * s, y - 25 * s)]
    d.polygon(P, fill=col, outline=INK); d.line(P + [P[0]], fill=INK, width=max(2, int(5 * s)))
    d.polygon([(x + 190 * s, y - 115 * s), (x + 290 * s, y - 117 * s), (x + 340 * s, y - 88 * s), (x + 170 * s, y - 88 * s)], fill=(40, 46, 60))
    for wx in (x + 95 * s, x + 345 * s):
        d.ellipse((wx - 38 * s, y - 65 * s, wx + 38 * s, y + 10 * s), fill=INK); d.ellipse((wx - 18 * s, y - 45 * s, wx + 18 * s, y - 10 * s), fill=(200, 200, 206))
def burger(d, cx, cy, s=1.0):
    d.chord((cx - 70 * s, cy - 60 * s, cx + 70 * s, cy + 20 * s), 180, 360, fill=(226, 160, 70), outline=INK, width=max(2, int(4 * s)))
    d.rectangle((cx - 72 * s, cy - 22 * s, cx + 72 * s, cy - 10 * s), fill=(90, 190, 80)); d.rectangle((cx - 70 * s, cy - 10 * s, cx + 70 * s, cy + 12 * s), fill=(110, 60, 40))
    d.rectangle((cx - 72 * s, cy - 14 * s, cx + 72 * s, cy - 8 * s), fill=(250, 210, 60)); d.rounded_rectangle((cx - 70 * s, cy + 12 * s, cx + 70 * s, cy + 36 * s), int(10 * s), fill=(226, 160, 70), outline=INK, width=max(2, int(4 * s)))
def jersey(d, cx, cy, s, col, num):
    P = [(cx - 40 * s, cy - 50 * s), (cx - 15 * s, cy - 58 * s), (cx, cy - 48 * s), (cx + 15 * s, cy - 58 * s), (cx + 40 * s, cy - 50 * s), (cx + 58 * s, cy - 20 * s), (cx + 38 * s, cy - 10 * s), (cx + 34 * s, cy + 55 * s), (cx - 34 * s, cy + 55 * s), (cx - 38 * s, cy - 10 * s), (cx - 58 * s, cy - 20 * s)]
    d.polygon(P, fill=col, outline=INK); txt(d, str(num), cx, cy + 10 * s, 40 * s, WHITE, stroke=max(1, int(2 * s)))
def dollar_bill(d, cx, cy, s=1.0, rot=0):
    lay = Image.new("RGBA", (int(260 * s), int(130 * s))); ld = ImageDraw.Draw(lay)
    ld.rectangle((2, 2, 258 * s, 128 * s), fill=(150, 210, 150), outline=(40, 90, 50), width=max(2, int(4 * s))); ld.ellipse((100 * s, 30 * s, 160 * s, 100 * s), outline=(40, 90, 50), width=max(2, int(4 * s)))
    ld.text((130 * s, 65 * s), "$", font=F(44 * s), fill=(40, 90, 50), anchor="mm")
    return lay.rotate(rot, expand=True, resample=Image.BICUBIC)
USA = [(80, 760), (180, 700), (420, 690), (640, 700), (760, 650), (870, 600), (960, 640), (990, 720), (930, 790), (930, 900), (860, 960), (900, 1080), (860, 1100), (760, 1020), (620, 1010), (520, 1080), (430, 1070), (340, 1000), (210, 980), (120, 900)]

# ---------------- Orte ----------------
_bg = {}
def bg_space():
    if "space" in _bg: return _bg["space"].copy()
    im = vgrad((30, 34, 70), (210, 130, 90)); d = ImageDraw.Draw(im, "RGBA")
    r = random.Random(3)
    for _ in range(120): x, y = r.randint(0, W), r.randint(0, 900); d.ellipse((x, y, x + 3, y + 3), fill=(255, 255, 255, r.randint(80, 220)))
    d.rectangle((0, 1350, W, H), fill=(70, 56, 60)); d.polygon([(0, 1350), (300, 1250), (700, 1320), (1080, 1230), (1080, 1350)], fill=(90, 70, 72))
    starship(d, 820, 1330, 980)
    im = blur(im, 4); _bg["space"] = im; return im.copy()
def bg_dark():
    if "dark" in _bg: return _bg["dark"].copy()
    im = vgrad((24, 22, 34), (10, 10, 16)); glow(im, W // 2, 800, 600, (255, 196, 90), 70); _bg["dark"] = im; return im.copy()
def bg_lot():
    if "lot" in _bg: return _bg["lot"].copy()
    im = vgrad((150, 200, 240), (220, 230, 240)); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 700, W, H), fill=(80, 82, 90))
    for y in range(890, H, 175): d.line((0, y, W, y), fill=(230, 230, 230), width=6)
    im = blur(im, 2); _bg["lot"] = im; return im.copy()
def bg_mcd():
    if "mcd" in _bg: return _bg["mcd"].copy()
    im = vgrad((250, 210, 120), (240, 160, 80)); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((120, 520, 960, 1250), fill=(200, 40, 40), outline=INK, width=8); d.rectangle((180, 760, 900, 1250), fill=(250, 240, 220), outline=INK, width=6)
    d.rectangle((160, 560, 920, 700), fill=(250, 200, 40), outline=INK, width=6); txt(d, "McDONALD'S", 540, 630, 86, (200, 40, 40))
    for x in (260, 540, 820): d.rectangle((x - 90, 820, x + 90, 1080), fill=(150, 200, 230), outline=INK, width=5)
    d.rectangle((0, 1250, W, H), fill=(110, 110, 116))
    im = blur(im, 4); _bg["mcd"] = im; return im.copy()
def bg_stadium():
    if "stadium" in _bg: return _bg["stadium"].copy()
    im = vgrad((14, 20, 44), (40, 60, 100)); d = ImageDraw.Draw(im, "RGBA")
    for x in (150, 930):
        d.rectangle((x - 8, 200, x + 8, 700), fill=(80, 84, 96)); d.rectangle((x - 70, 170, x + 70, 230), fill=(255, 250, 220)); glow(im, x, 200, 160, (255, 250, 220), 160); d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(0, 700), (W, 700), (W, 1050), (0, 1050)], fill=(50, 56, 80))
    r = random.Random(5)
    for _ in range(500): x, y = r.randint(0, W), r.randint(710, 1040); d.ellipse((x, y, x + 8, y + 8), fill=r.choice([(220, 60, 60), (60, 90, 200), (240, 240, 240), (240, 200, 60)]))
    d.rectangle((0, 1050, W, H), fill=(50, 140, 70))
    for y in range(1100, H, 120): d.line((0, y, W, y), fill=(240, 240, 240), width=6)
    im = blur(im, 3); _bg["stadium"] = im; return im.copy()
def bg_usa():
    if "usa" in _bg: return _bg["usa"].copy()
    im = vgrad((120, 180, 230), (70, 120, 190)); d = ImageDraw.Draw(im, "RGBA")
    d.polygon(USA, fill=(110, 180, 110), outline=INK); d.line(USA + [USA[0]], fill=INK, width=8)
    _bg["usa"] = im; return im.copy()
def bg_office():
    if "office" in _bg: return _bg["office"].copy()
    im = vgrad((200, 206, 214), (160, 168, 180)); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 1200, W, H), fill=(120, 104, 92)); d.rectangle((100, 300, 500, 600), fill=(150, 200, 230), outline=(110, 120, 130), width=8)
    im = blur(im, 4); _bg["office"] = im; return im.copy()

# ---------------- Szenen ----------------
def hud(f, gt, big=False, k=1.0):
    """Zaehler oben: ELON'S MONEY"""
    if k <= 0: return
    d = ImageDraw.Draw(f, "RGBA"); y = 150 - (1 - ease(k)) * 300; m = money_at(gt)
    rr(d, (60, y - 80, 1020, y + 95), (20, 20, 28, 235), GOLD, 6, 26)
    txt(d, "ELON'S MONEY", 540, y - 40, 34, (200, 200, 210), font=SANS)
    txt(d, fmt(m), 540, y + 30, 70, GOLD)

def s0(lt, T, gt):   # How long would it take to spend all of Elon Musk's money?
    f = bg_space(); d = ImageDraw.Draw(f, "RGBA")
    cybertruck(d, 60, 1560, 0.9)
    C.person(f, C.ELON, 400, 900, 200, "grin", ("hip", "hip"), 1)
    d = ImageDraw.Draw(f, "RGBA"); txt(d, "MARS", 400, 1290, 54, (230, 230, 236))
    k = ramp(lt, WT(0, "money") - 0.1, WT(0, "money") + 0.25)
    if k > 0:   # Geld-Stapel wachsen hinter ihm hoch
        for i in range(6):
            hh = 60 + i * 55; x = 640 + (i % 3) * 120
            ImageDraw.Draw(f).rectangle((x, 1560 - hh * ease(k), x + 100, 1560), fill=(150, 210, 150), outline=INK, width=4)
    rr(d, (40, 70, 1040, 320), YEL, INK, 8, 24); txt(d, "HOW LONG TO SPEND", 540, 150, 70); txt(d, "ELON'S MONEY?", 540, 245, 80)
    return f
def s1(lt, T, gt):   # Let's find out.
    f = bg_space(); d = ImageDraw.Draw(f, "RGBA")
    C.person(f, C.ELON, 400, 900, 200, "smug", ("cross", "cross"), 1); txt(ImageDraw.Draw(f), "MARS", 400, 1290, 54, (230, 230, 236))
    k = back(ramp(lt, 0.0, 0.4)); card = Image.new("RGBA", (520, 320)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((4, 4, 516, 316), 30, fill=(20, 20, 24), outline=GOLD, width=8); cd.rectangle((60, 90, 150, 160), fill=GOLD); cd.text((260, 250), "UNLIMITED", font=F(44), fill=GOLD, anchor="mm")
    card = card.rotate(-12, expand=True, resample=Image.BICUBIC); f.alpha_composite(card, (int(560 + (1 - k) * 600), 1100))
    return f
def s2(lt, T, gt):   # He's got 850 billion dollars.
    f = bg_dark(); hud(f, gt, k=ramp(lt, WT(2, "850") - 0.05, WT(2, "850") + 0.25))
    C.person(f, C.ELON, 540, 900, 180, "grin", ("up", "up"), 0)
    for i in range(16):
        r = random.Random(i); x = r.uniform(80, 1000); y = -200 + ((lt * 900 + r.uniform(0, 1800)) % 2200)
        b = dollar_bill(None, 0, 0, 0.6, r.uniform(-30, 30)); f.alpha_composite(b, (int(x), int(y)))
    return f
def s3(lt, T, gt):   # Step one: every Ferrari built last year.
    f = bg_lot(); d = ImageDraw.Draw(f, "RGBA"); hud(f, gt)
    k = ramp(lt, WT(3, "Ferrari") - 0.1, T)
    for row in range(6):
        for i in range(3):
            x = 1250 - (1250 + 450) * ease(ramp(k, row * 0.1 + i * 0.05, row * 0.1 + i * 0.05 + 0.35)) + i * 360
            if x < 1100: ferrari(d, x, 880 + row * 175, 0.78)
    pop_text(f, "EVERY FERRARI", 540, 560, 96, WHITE, ramp(lt, WT(3, "Ferrari") - 0.05, WT(3, "Ferrari") + 0.2), box=(214, 30, 40)); return f
def s4(lt, T, gt):   # All thirteen thousand.
    f = bg_lot(); d = ImageDraw.Draw(f, "RGBA"); hud(f, gt)
    for row in range(6):
        for i in range(3): ferrari(d, -60 + i * 360, 880 + row * 175, 0.78)
    n = int(13640 * ease(ramp(lt, 0, T)))
    pop_text(f, "{:,} CARS".format(n), 540, 560, 110, WHITE, 1.0, box=(214, 30, 40)); return f
def s5(lt, T, gt):   # Seven billion... and he didn't even blink.
    f = bg_lot(); d = ImageDraw.Draw(f, "RGBA"); hud(f, gt)
    for row in range(6):
        for i in range(3): ferrari(d, -60 + i * 360, 880 + row * 175, 0.78)
    f.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 80)))
    bl = WT(5, "blink")
    C.person(f, C.ELON, 540, 820, 170, "neutral" if lt < bl else "smug", ("down", "hold"), 0)
    d = ImageDraw.Draw(f, "RGBA"); rr(d, (640, 1000, 720, 1100), (250, 250, 250), INK, 5, 10); d.arc((700, 1020, 760, 1070), 270, 90, fill=INK, width=6)   # Kaffeebecher
    stamp(f, "-$7 BILLION", 540, 1450, 90, RED, ramp(lt, 0.0, 0.25), -6)
    pop_text(f, "*yawn*", 820, 600, 60, WHITE, ramp(lt, bl - 0.2, bl)); return f
def s6(lt, T, gt):   # Fine.
    f = bg_mcd(); hud(f, gt); C.person(f, C.ELON, 540, 900, 170, "smug", ("shrug", "shrug"), 0); return f
def s7(lt, T, gt):   # We're buying McDonald's.
    f = bg_mcd(); hud(f, gt); d = ImageDraw.Draw(f, "RGBA")
    C.person(f, C.ELON, 360, 900, 170, "grin", ("down", "give"), 1)
    k = back(ramp(lt, WT(7, "McDonald's") - 0.1, WT(7, "McDonald's") + 0.3))
    if k > 0:   # goldener Schluessel
        kx, ky = 700, int(1300 - 300 * k); d.ellipse((kx - 60, ky - 60, kx + 60, ky + 60), outline=GOLD, width=22); d.rectangle((kx + 50, ky - 12, kx + 260, ky + 12), fill=GOLD); d.rectangle((kx + 200, ky + 10, kx + 230, ky + 50), fill=GOLD)
    return f
def s8(lt, T, gt):   # The entire company.
    f = vgrad((40, 70, 120), (20, 30, 60)); d = ImageDraw.Draw(f, "RGBA"); hud(f, gt)
    for x0, y0, w0, h0 in ((120, 700, 380, 300), (560, 640, 400, 280), (430, 1050, 300, 260), (780, 1000, 220, 240), (160, 1100, 200, 240)):
        d.rounded_rectangle((x0, y0, x0 + w0, y0 + h0), 80, fill=(70, 120, 90))
    r = random.Random(8); n = int(70 * ease(ramp(lt, 0, T)))
    for i in range(n):
        x = r.uniform(140, 960); y = r.uniform(660, 1320); d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(250, 200, 40), outline=INK, width=3)
    pop_text(f, "40,000+ RESTAURANTS", 540, 480, 80, YEL, ramp(lt, 0.1, 0.4))
    stamp(f, "SOLD", 540, 1500, 140, RED, ramp(lt, WT(8, "company") - 0.1, WT(8, "company") + 0.15), -10); return f
def s9(lt, T, gt):   # Free Big Macs forever.
    f = bg_mcd(); hud(f, gt); f.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 60))); d = ImageDraw.Draw(f, "RGBA")
    n = 1 + int(ramp(lt, 0, T) * 14)
    for i in range(n): burger(d, 300 + (i % 5) * 120, 1500 - (i // 5) * 70, 0.9)
    C.person(f, C.ELON, 540, 820, 170, "grin", ("up", "up"), 0)
    pop_text(f, "FREE BIG MACS FOREVER", 540, 560, 74, YEL, ramp(lt, 0, 0.25)); return f
def s10(lt, T, gt):  # Next: the whole NFL.
    f = bg_stadium(); hud(f, gt)
    pop_text(f, "THE WHOLE NFL", 540, 560, 110, WHITE, ramp(lt, WT(10, "NFL") - 0.1, WT(10, "NFL") + 0.2), box=(30, 50, 120)); return f
def s11(lt, T, gt):  # All thirty-two teams.
    f = bg_stadium(); hud(f, gt); d = ImageDraw.Draw(f, "RGBA")
    cols = [(200, 30, 40), (30, 60, 150), (240, 160, 30), (30, 120, 60), (90, 40, 140), (20, 20, 24), (0, 140, 160), (160, 160, 170)]
    for i in range(32):
        k = back(ramp(lt, i * 0.035, i * 0.035 + 0.3))
        if k > 0: jersey(d, 110 + (i % 8) * 123, int(1230 + (i // 8) * 150 + (1 - k) * 700), 0.9, cols[i % 8], i + 1)
    stamp(f, "SOLD", 540, 900, 130, RED, ramp(lt, WT(11, "teams") - 0.05, WT(11, "teams") + 0.2), -8); return f
def s12(lt, T, gt):  # Super Bowl?
    f = bg_stadium(); hud(f, gt); d = ImageDraw.Draw(f, "RGBA")
    k = back(ramp(lt, 0, 0.35)); y = int(1500 - 200 * k)   # Pokal (allgemein, kein Logo)
    glow(f, 540, y - 400, 300, (255, 240, 200), 120); d = ImageDraw.Draw(f, "RGBA")
    d.polygon([(440, y - 560), (640, y - 560), (590, y - 140), (490, y - 140)], fill=(225, 225, 232), outline=INK); d.ellipse((430, y - 700, 650, y - 500), fill=(190, 126, 62), outline=INK, width=6)
    d.rectangle((460, y - 140, 620, y), fill=(60, 60, 70), outline=INK, width=6)
    pop_text(f, "SUPER BOWL?", 540, 560, 110, WHITE, ramp(lt, 0.0, 0.2)); return f
def s13(lt, T, gt):  # That's his living room now.
    f = bg_stadium(); hud(f, gt); d = ImageDraw.Draw(f, "RGBA")
    d.rounded_rectangle((260, 1250, 820, 1450), 40, fill=(150, 90, 60), outline=INK, width=8); d.rounded_rectangle((220, 1180, 320, 1450), 30, fill=(130, 76, 50), outline=INK, width=6); d.rounded_rectangle((760, 1180, 860, 1450), 30, fill=(130, 76, 50), outline=INK, width=6)
    C.person(f, C.ELON, 540, 1020, 150, "smug", ("hold", "down"), 0)
    d = ImageDraw.Draw(f, "RGBA"); d.rounded_rectangle((640, 1170, 690, 1240), 10, fill=(40, 40, 46), outline=INK, width=4)
    pop_text(f, "HIS LIVING ROOM", 540, 560, 96, YEL, ramp(lt, WT(13, "living") - 0.1, WT(13, "living") + 0.2)); return f
def s14(lt, T, gt):  # a thousand dollars for every person in America.
    f = bg_usa(); hud(f, gt); d = ImageDraw.Draw(f, "RGBA")
    k = ramp(lt, WT(14, "thousand") - 0.1, T + 0.6)
    r = random.Random(14)
    for i in range(int(60 * k)):
        x = r.uniform(80, 980); y = 600 + ((lt * 700 + r.uniform(0, 600)) % 700)
        f.alpha_composite(dollar_bill(None, 0, 0, 0.45, r.uniform(-40, 40)), (int(x), int(y)))
    pop_text(f, "$1,000 FOR EVERY AMERICAN", 540, 1350, 66, WHITE, ramp(lt, WT(14, "thousand") - 0.05, WT(14, "thousand") + 0.2), box=(200, 40, 50))
    pop_text(f, "340 MILLION PEOPLE", 540, 1480, 56, YEL, ramp(lt, WT(14, "America") - 0.1, WT(14, "America") + 0.2)); return f
def s15(lt, T, gt):  # Including you.
    f = bg_office(); hud(f, gt)
    C.person(f, C.YOU, 540, 820, 190, "shock" if lt < 0.4 else "grin", ("up", "down"), 0)
    f.alpha_composite(dollar_bill(None, 0, 0, 0.8, 8), (600, 470))
    pop_text(f, "INCLUDING YOU", 540, 1500, 100, YEL, ramp(lt, 0, 0.2)); return f
def s16(lt, T, gt):  # And Elon... still has thirty billion left.
    f = bg_dark(); d = ImageDraw.Draw(f, "RGBA")
    m = money_at(gt); rr(d, (60, 520, 1020, 820), (20, 20, 28), GOLD, 8, 30); txt(d, "ELON'S MONEY LEFT", 540, 590, 44, (200, 200, 210), font=SANS); txt(d, fmt(m), 540, 720, 82, GOLD)
    C.person(f, C.ELON, 540, 1180, 170, "grin" if lt > WT(16, "left") else "smug", ("shrug", "shrug"), 0)
    pop_text(f, "STILL $30 BILLION", 540, 1640, 84, GREEN, ramp(lt, WT(16, "left") - 0.05, WT(16, "left") + 0.2)); return f
def s17(lt, T, gt):  # So how long would it take?
    f = bg_dark(); d = ImageDraw.Draw(f, "RGBA")
    r_ = 260; cx, cy = 540, 950; d.ellipse((cx - r_, cy - r_, cx + r_, cy + r_), fill=(250, 248, 240), outline=INK, width=12)
    for k in range(12): a = k * math.pi / 6; d.line((cx + math.cos(a) * r_ * 0.85, cy + math.sin(a) * r_ * 0.85, cx + math.cos(a) * r_ * 0.95, cy + math.sin(a) * r_ * 0.95), fill=INK, width=8)
    a = -math.pi / 2 + lt * 6; d.line((cx, cy, cx + math.cos(a) * r_ * 0.8, cy + math.sin(a) * r_ * 0.8), fill=RED, width=10)
    pop_text(f, "HOW LONG?", 540, 520, 120, YEL, ramp(lt, 0, 0.2)); return f
def s18(lt, T, gt):  # Spending a million dollars every single day... over two thousand years.
    f = bg_office(); d = ImageDraw.Draw(f, "RGBA")
    yrs = int(2330 * ease(ramp(lt, WT(18, "day") - 0.3, WT(18, "years"))))
    rr(d, (200, 380, 880, 620), WHITE, INK, 8, 24); txt(d, "YEAR", 540, 440, 44, (120, 120, 130), font=SANS); txt(d, "{:,}".format(max(1, yrs)), 540, 540, 110, INK)
    pop_text(f, "$1,000,000 EVERY DAY", 540, 760, 70, GREEN, ramp(lt, WT(18, "million") - 0.1, WT(18, "million") + 0.2))
    old = lt > WT(18, "years") - 0.6
    C.person(f, C.YOU, 540, 1180, 170, "worried" if old else "neutral", ("hold", "hold"), 0)
    pop_text(f, "2,000+ YEARS", 540, 1640, 110, YEL, ramp(lt, WT(18, "years") - 0.1, WT(18, "years") + 0.2)); return f

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18]

# ---------------- Look + Untertitel ----------------
_FIN = None
def finish(img):
    global _FIN
    if _FIN is None:
        g = Image.effect_noise((W, H), 22).convert("L"); v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse((-300, -260, W + 300, H + 260), fill=255)
        _FIN = (Image.merge("RGB", (g, g, g)), v.filter(ImageFilter.GaussianBlur(260)))
    g, v = _FIN; im = Image.blend(img, g, 0.022)
    return Image.composite(im, Image.blend(im, Image.new("RGB", (W, H), (16, 12, 20)), 0.36), v)
def captions(d, gt):
    cur = max([i for i, w in enumerate(ALLW) if w[1] <= gt] or [0]); g0 = cur - cur % 3; grp = ALLW[g0:g0 + 3]
    if not grp or gt > grp[-1][2] + 0.4: return
    words = [w[0] for w in grp]; f = F(58); sp = d.textlength(" ", font=f); ws = [d.textlength(w, font=f) for w in words]
    while sum(ws) + sp * (len(words) - 1) > W - 100: f = F(f.size - 4); sp = d.textlength(" ", font=f); ws = [d.textlength(w, font=f) for w in words]
    x = W / 2 - (sum(ws) + sp * (len(words) - 1)) / 2
    for k, w in enumerate(words):
        d.text((x, 1770), w, font=f, fill=YEL if g0 + k == cur else WHITE, anchor="lm", stroke_width=8, stroke_fill=(0, 0, 0)); x += ws[k] + sp
SHAKES = [(4, "thousand", 8), (8, "company", 12), (11, "teams", 12), (16, "left", 16)]
def shake(gt):
    dx = dy = 0.0
    for si, w, a in SHAKES:
        e = gt - GT(si, w)
        if 0 <= e < 0.3: k = (1 - e / 0.3) * a; dx += math.sin(e * 90) * k; dy += math.cos(e * 77) * k
    return int(dx), int(dy)
def frame(gt):
    si = 0
    for s in SEGS:
        if gt >= s["t0"] - 0.05: si = s["i"]
    s = SEGS[si]; lt = gt - s["t0"]; T = s["a1"] - s["a0"]
    f = SCENES[si](lt, T, gt)
    dx, dy = shake(gt)
    if dx or dy: g_ = Image.new("RGBA", (W, H), (0, 0, 0, 255)); g_.paste(f, (dx, dy)); f = g_
    im = finish(f.convert("RGB")).convert("RGBA"); d = ImageDraw.Draw(im); captions(d, gt)
    return im.convert("RGB")

# ---------------- Ton ----------------
def pulse(n, bpm=100):
    out = np.zeros(n, np.float32); step = 60 / bpm; tt = np.arange(int(SR * 0.2)) / SR
    kick = np.sin(2 * np.pi * (50 + 50 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 16); t_ = 0.0
    while t_ < n / SR: j = int(t_ * SR); out[j:j + len(kick)] += kick[:max(0, n - j)]; t_ += step
    return out
def drone(n):
    tt = np.arange(n) / SR
    x = 0.6 * np.sin(2 * np.pi * 55 * tt) + 0.3 * np.sin(2 * np.pi * 82.4 * tt + 0.5) + 0.18 * np.sin(2 * np.pi * 110 * tt)
    return (x * (0.75 + 0.25 * np.sin(2 * np.pi * 0.08 * tt))).astype(np.float32)
def engine(n_s=1.4):
    tt = np.arange(int(SR * n_s)) / SR; f0 = 70 + 160 * (tt / n_s) ** 0.7
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f0) / SR)) * 0.4 + np.random.default_rng(2).standard_normal(len(tt)) * 0.15
    env = np.minimum(1, tt * 6) * np.exp(-tt * 1.2); return (x * env * 0.12).astype(np.float32)
CUES = [(1, "find", 0.0, "whoosh", 0.18), (2, "850", 0.0, "impact", 0.35), (3, "Ferrari", 0.0, "ENGINE", 1.0), (4, "thousand", 0.0, "cash", 0.3),
        (5, "blink", -0.2, "pop", 0.18), (7, "McDonald's", 0.0, "ding", 0.25), (8, "company", 0.0, "stamp", 0.4), (9, "Big", 0.0, "pop", 0.22),
        (10, "NFL", 0.0, "whoosh", 0.2), (11, "teams", 0.0, "stamp", 0.4), (12, "Bowl", 0.0, "pop", 0.25), (14, "thousand", 0.0, "coins", 0.3),
        (14, "America", 0.0, "cash", 0.3), (15, "you", 0.0, "success", 0.25), (16, "left", 0.0, "impact", 0.5), (17, "take", 0.0, "riser", 0.2),
        (18, "years", 0.0, "impact", 0.4)]
def audio():
    n = int(TOTAL * SR) + SR; v = np.zeros(n, np.float32); fx = np.zeros(n, np.float32)
    for s in SEGS:
        a = RAW[int(s["a0"] * SR):int(s["a1"] * SR)].copy(); fl = SR // 200; a[:fl] *= np.linspace(0, 1, fl); a[-fl:] *= np.linspace(1, 0, fl)
        i = int(s["t0"] * SR); v[i:i + len(a)] += a
    for si, w, off, name, g in CUES:
        j = max(0, int((GT(si, w) + off) * SR)); x = engine() if name == "ENGINE" else SFXL.load(name) * g
        x = x[:max(0, n - j)]; fx[j:j + len(x)] += x
    cs = np.concatenate([[0.0], np.cumsum(np.abs(v), dtype=np.float64)]); idx = np.arange(n)
    lo, hi = np.clip(idx - 2400, 0, n), np.clip(idx + 2400, 0, n); vabs = ((cs[hi] - cs[lo]) / 4800).astype(np.float32)
    duck = 1 - 0.4 * np.clip(vabs / 0.05, 0, 1)
    pu = pulse(n); pu *= 0.016 / (np.sqrt(np.mean(pu ** 2)) + 1e-9); dr = drone(n); dr *= 0.012 / (np.sqrt(np.mean(dr ** 2)) + 1e-9)
    bed = (pu + dr) * duck
    st = int((GT(16, "left") - 0.25) * SR); bed[st:st + int(0.6 * SR)] *= 0.15   # kurze Stille vor der Wendung
    fi = int(0.4 * SR); bed[:fi] *= np.linspace(0, 1, fi); bed[-fi:] *= np.linspace(1, 0, fi)
    out = v * 1.05 + fx + bed; m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)]

if __name__ == "__main__":
    print(f"Laenge {TOTAL:.1f}s")
    if "--stills" in sys.argv:
        tiles = []
        for s in SEGS:
            for fr in (0.35, 0.92): tiles.append(frame(s["t0"] + (s["a1"] - s["a0"]) * fr).resize((180, 320)))
        cols = 10; rows = math.ceil(len(tiles) / cols); sh = Image.new("RGB", (180 * cols, 320 * rows))
        for i, t_ in enumerate(tiles): sh.paste(t_, ((i % cols) * 180, (i // cols) * 320))
        sh.save("STORYBOARD.jpg", quality=88); print("ok"); sys.exit()
    out = av.open("ARC_Short08_Elon.mp4", "w"); vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "19", "preset": "medium"}
    ast = out.add_stream("aac", rate=SR); ast.layout = "mono"
    for k in range(int(TOTAL * FPS)):
        for p in vs.encode(av.VideoFrame.from_image(frame(k / FPS))): out.mux(p)
    for p in vs.encode(): out.mux(p)
    au = audio()
    for i in range(0, len(au), 1024):
        ch = au[i:i + 1024]; ch = np.pad(ch, (0, 1024 - len(ch))) if len(ch) < 1024 else ch
        af = av.AudioFrame.from_ndarray(ch.reshape(1, -1).astype(np.float32), format="flt", layout="mono"); af.sample_rate = SR
        for p in ast.encode(af): out.mux(p)
    for p in ast.encode(): out.mux(p)
    out.close(); print("ok", TOTAL)
