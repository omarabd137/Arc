"""ARC Short #07 - "He Paid $0 in Taxes. You Paid More." (9:16)
Bauplan: alle 1-3 s etwas Neues im Bild, Text-Highlights an Kernwoertern, visuelle Pointen, Impact-Sounds an harten Fakten,
tiefer Sound-Teppich ohne Melodie + leiser Takt, edler kinoartiger Look, keine Kamera-Zooms (Omars Regel), Figuren im Crayon-Prinzip.
Aufruf: python short07.py --stills | (voll)"""
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
INK = (28, 26, 32); WHITE = (255, 255, 255); YEL = (255, 206, 50); RED = (228, 48, 56); GREEN = (46, 190, 100); GOLD = (240, 190, 80)

SENT = ["Jeff Bezos once paid less tax than you.", "Zero dollars.", "And he didn't break a single rule.",
        "See, when you get paid, the government takes its share first.", "But billionaires like Jeff don't really live on a paycheck.",
        "They own a mountain of stock.", "And you only pay tax on stock when you sell it.", "So... they don't sell.",
        "Need cash for a new yacht?", "They borrow against that mountain.", "Borrowed money isn't income.", "So... no tax.",
        "The mountain keeps growing.", "So they just borrow more.", "And when they die, their kids get it all...",
        "and the tax on all that growth disappears."]
def dec(p):
    c = av.open(p); r = av.AudioResampler(format="flt", layout="mono", rate=SR); out = []
    for fr in c.decode(audio=0):
        for f in r.resample(fr): out.append(f.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.float32)
RAW = dec("vo/s07.mp3")
WR = [w for w in json.load(open("vo/words.json", encoding="utf-8"))["words"] if w["type"] == "word"]
SEGS = []; pos = 0; t = 0.05
for si, s in enumerate(SENT):
    n = len(s.split()); ws = WR[pos:pos + n]; pos += n
    if si: t += 0.2
    a0 = max(0, ws[0]["start"] - 0.04); a1 = ws[-1]["end"] + 0.06
    SEGS.append(dict(i=si, t0=t, a0=a0, a1=a1, words=[(w["text"], w["start"] - a0 + t, w["end"] - a0 + t) for w in ws]))
    t += a1 - a0
TOTAL = t + 0.4
ALLW = [w for s in SEGS for w in s["words"]]
def _n(x): return re.sub(r"[^a-z0-9']", "", x.lower())
def WT(si, word, k=1):
    c = 0
    for w, s_, e_ in SEGS[si]["words"]:
        if _n(w) == _n(word):
            c += 1
            if c == k: return s_ - SEGS[si]["t0"]
    raise KeyError((si, word, k))
def ramp(x, a, b): return max(0.0, min(1.0, (x - a) / max(1e-6, b - a)))
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------------- Zeichen-Helfer ----------------
def txt(d, s, x, y, size, col=INK, anchor="mm", font=BOLD, stroke=0, sc=INK):
    d.text((x, y), s, font=F(size, font), fill=col, anchor=anchor, stroke_width=stroke, stroke_fill=sc)
def rr(d, box, fill, out=INK, w=6, r=20): d.rounded_rectangle(box, r, fill=fill, outline=out, width=w)
def pop_text(f, s, x, y, size, col=WHITE, k=1.0, rot=0, box=None):
    """Text-Highlight, springt federnd rein"""
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
def blur(im, r=6): return im.filter(ImageFilter.GaussianBlur(r))

# ---------------- Orte (gezeichnet, edel, leicht unscharf wie bei Crayon) ----------------
_bg = {}
def office():
    if "office" in _bg: return _bg["office"].copy()
    im = vgrad((250, 170, 110), (120, 70, 110)); d = ImageDraw.Draw(im, "RGBA")
    r = random.Random(2)
    for k in range(14):   # Skyline
        x = k * 85 - 20; h = r.randint(300, 760); d.rectangle((x, 1150 - h, x + 78, 1150), fill=(60, 40, 70))
        for wy in range(1150 - h + 30, 1150, 48):
            for wx in range(x + 10, x + 70, 22):
                if r.random() < 0.45: d.rectangle((wx, wy, wx + 10, wy + 18), fill=(255, 210, 140))
    for x in range(0, W, 270): d.rectangle((x, 0, x + 18, 1240), fill=(40, 30, 40))   # Fensterrahmen
    d.rectangle((0, 1150, W, 1240), fill=(40, 30, 40)); d.rectangle((0, 1240, W, H), fill=(70, 48, 44))
    for y in range(1260, H, 60): d.line((0, y, W, y), fill=(84, 58, 52), width=3)
    im = blur(im, 5); glow(im, 760, 520, 420, (255, 200, 120), 90)
    _bg["office"] = im; return im.copy()
def kitchen():
    if "kitchen" in _bg: return _bg["kitchen"].copy()
    im = vgrad((206, 214, 222), (170, 180, 192)); d = ImageDraw.Draw(im, "RGBA")
    for y in range(500, 1100, 70):
        for x in range(0, W, 70): d.rectangle((x + 2, y + 2, x + 68, y + 68), outline=(185, 194, 204), width=3)
    d.rectangle((0, 1100, W, 1180), fill=(150, 130, 110)); d.rectangle((0, 1180, W, H), fill=(120, 104, 92))
    d.rectangle((760, 380, 1000, 1100), fill=(225, 228, 232), outline=(150, 154, 160), width=6); d.line((770, 640, 990, 640), fill=(150, 154, 160), width=5)
    d.rectangle((90, 300, 420, 470), fill=(150, 200, 230), outline=(120, 130, 140), width=8)
    im = blur(im, 5); _bg["kitchen"] = im; return im.copy()
def vault():
    if "vault" in _bg: return _bg["vault"].copy()
    im = vgrad((40, 34, 52), (16, 14, 22)); glow(im, W // 2, 700, 560, (255, 200, 110), 70)
    d = ImageDraw.Draw(im, "RGBA")
    for x in (90, 990): d.rectangle((x - 40, 200, x + 40, 1500), fill=(60, 52, 70))
    d.rectangle((0, 1500, W, H), fill=(30, 26, 36))
    im = blur(im, 3); _bg["vault"] = im; return im.copy()
def bank():
    if "bank" in _bg: return _bg["bank"].copy()
    im = vgrad((236, 228, 214), (200, 188, 170)); d = ImageDraw.Draw(im, "RGBA")
    for x in (120, 380, 700, 960):
        d.rectangle((x - 50, 260, x + 50, 1200), fill=(244, 238, 228), outline=(190, 180, 166), width=5)
        for k in range(1, 4): d.line((x - 50 + k * 25, 270, x - 50 + k * 25, 1190), fill=(214, 206, 194), width=3)
    d.rectangle((0, 200, W, 260), fill=(220, 210, 194)); d.rectangle((0, 1200, W, H), fill=(170, 150, 128))
    im = blur(im, 5); _bg["bank"] = im; return im.copy()
def sea():
    if "sea" in _bg: return _bg["sea"].copy()
    im = vgrad((255, 170, 120), (90, 120, 190)); d = ImageDraw.Draw(im, "RGBA")
    d.ellipse((620, 560, 880, 820), fill=(255, 220, 140)); d.rectangle((0, 1000, W, H), fill=(40, 80, 140))
    for y in range(1020, H, 40): d.line((0, y, W, y + 6), fill=(70, 110, 170), width=4)
    im = blur(im, 3); _bg["sea"] = im; return im.copy()
def mansion():
    if "mansion" in _bg: return _bg["mansion"].copy()
    im = vgrad((120, 40, 50), (50, 20, 28)); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((300, 300, 780, 760), fill=(170, 130, 70), outline=(230, 190, 110), width=14); d.rectangle((330, 330, 750, 730), fill=(70, 50, 40))
    d.rectangle((0, 1300, W, H), fill=(60, 26, 32))
    im = blur(im, 5); glow(im, W // 2, 500, 500, (255, 190, 120), 60); _bg["mansion"] = im; return im.copy()

# ---------------- Requisiten ----------------
def tax_bill(f, cx, cy, w, h, amount, rot=0, stamp_k=0.0, stamp_txt="$0", col=RED):
    lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay)
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=(252, 250, 244), outline=INK, width=6)
    txt(d, "TAX BILL", cx, cy - h / 2 + 50, w * 0.1, INK)
    for k in range(5): d.line((cx - w * 0.38, cy - h * 0.22 + k * h * 0.09, cx + w * 0.38, cy - h * 0.22 + k * h * 0.09), fill=(190, 190, 196), width=6)
    txt(d, amount, cx, cy + h * 0.3, w * 0.16, INK)
    if rot: lay = lay.rotate(rot, center=(cx, cy), resample=Image.BICUBIC)
    f.alpha_composite(lay)
    if stamp_k > 0: stamp(f, stamp_txt, cx, cy, int(w * 0.36), col, stamp_k, -12)
def paycheck(d, cx, cy, w, cut=0.0):
    h = w * 0.45
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2 - w * 0.3 * cut, cy + h / 2), fill=(220, 245, 220), outline=INK, width=6)
    txt(d, "PAYCHECK", cx - w * 0.15 * cut, cy - h * 0.22, w * 0.08, (40, 110, 60))
    txt(d, "$4,000", cx - w * 0.15 * cut, cy + h * 0.12, w * 0.12, INK)
def money_bag(d, cx, cy, s=1.0, label="$"):
    d.ellipse((cx - 110 * s, cy - 90 * s, cx + 110 * s, cy + 120 * s), fill=(210, 170, 90), outline=INK, width=int(6 * s))
    d.polygon([(cx - 50 * s, cy - 80 * s), (cx + 50 * s, cy - 80 * s), (cx + 70 * s, cy - 140 * s), (cx - 70 * s, cy - 140 * s)], fill=(210, 170, 90), outline=INK)
    d.line((cx - 55 * s, cy - 88 * s, cx + 55 * s, cy - 88 * s), fill=INK, width=int(8 * s))
    txt(d, label, cx, cy + 20 * s, (90 if len(label) < 3 else 54) * s, (90, 60, 20))
def mountain(f, cx, base_y, height, k_grow=1.0):
    """Berg aus Aktien-Scheinen und Paketen"""
    d = ImageDraw.Draw(f, "RGBA"); hh = height * k_grow; w = hh * 1.15
    pts = [(cx - w / 2, base_y), (cx - w * 0.12, base_y - hh * 0.92), (cx, base_y - hh), (cx + w * 0.14, base_y - hh * 0.9), (cx + w / 2, base_y)]
    d.polygon(pts, fill=(60, 140, 90), outline=INK)
    r = random.Random(4)
    for i in range(int(40 * k_grow)):
        y = base_y - r.uniform(0.05, 0.85) * hh; half = (1 - (base_y - y) / hh) * w / 2 * 0.85; x = cx + r.uniform(-half, half)
        if r.random() < 0.5:
            d.rectangle((x - 34, y - 22, x + 34, y + 22), fill=(230, 245, 230), outline=INK, width=3); txt(d, "STOCK", x, y, 15, (40, 110, 60))
        else:
            d.rectangle((x - 30, y - 24, x + 30, y + 24), fill=(196, 150, 100), outline=INK, width=3); d.line((x - 30, y - 6, x + 30, y - 6), fill=(160, 120, 80), width=4)
    d.line(pts, fill=INK, width=6)
    return base_y - hh
def yacht(d, cx, cy, s=1.0):
    d.polygon([(cx - 330 * s, cy), (cx + 330 * s, cy), (cx + 260 * s, cy + 90 * s), (cx - 280 * s, cy + 90 * s)], fill=WHITE, outline=INK)
    d.rectangle((cx - 180 * s, cy - 90 * s, cx + 160 * s, cy), fill=(245, 245, 245), outline=INK, width=int(5 * s))
    for k in range(5): d.rectangle((cx - 160 * s + k * 62 * s, cy - 70 * s, cx - 120 * s + k * 62 * s, cy - 35 * s), fill=(60, 90, 140))
    d.rectangle((cx - 90 * s, cy - 160 * s, cx + 80 * s, cy - 90 * s), fill=(245, 245, 245), outline=INK, width=int(5 * s))
    d.line((cx - 330 * s, cy + 30 * s, cx + 320 * s, cy + 30 * s), fill=(60, 90, 140), width=int(10 * s))

# ---------------- Szenen ----------------
def banner(f, text1, text2, k=1.0):
    if k <= 0: return
    d = ImageDraw.Draw(f, "RGBA"); y = 255 - (1 - ease(k)) * 320
    d.rectangle((40, y - 110, 1040, y + 110), fill=YEL, outline=INK, width=8)
    txt(d, text1, 540, y - 46, 76); txt(d, text2, 540, y + 46, 76)

def s0(lt, T):   # Jeff Bezos once paid less tax than you.
    f = office(); d = ImageDraw.Draw(f, "RGBA")
    C.person(f, C.BEZOS, 330, 820, 190, "grin", ("down", "hold"), 1)
    tax_bill(f, 640, 1080, 300, 380, "$0", -8)
    yu = WT(0, "you")
    if lt > yu - 0.1:   # Du daneben, mit dicker Rechnung
        k = back(ramp(lt, yu - 0.1, yu + 0.3)); x = int(1240 - 400 * k)
        C.person(f, C.YOU, x, 1180, 120, "worried", ("hold", "down"), -1)
        tax_bill(f, x - 150, 1420, 210, 300, "$9,400", 6)
    banner(f, "HE PAID $0 IN TAX", "YOU DIDN'T.", ramp(lt, 0, 0.25)); return f
def s1(lt, T):   # Zero dollars.
    f = office(); f.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
    tax_bill(f, 540, 1000, 560, 700, "$0", 0, ramp(lt, 0.15, 0.4), "$0")
    pop_text(f, "ZERO.", 540, 520, 150, WHITE, ramp(lt, 0.0, 0.2)); banner(f, "HE PAID $0 IN TAX", "YOU DIDN'T.", 1.0); return f
def s2(lt, T):   # And he didn't break a single rule.
    f = office(); d = ImageDraw.Draw(f, "RGBA")
    C.person(f, C.BEZOS, 540, 760, 210, "smug", ("cross", "cross"), 0)
    rr(d, (300, 1300, 780, 1560), (240, 236, 226), INK, 6, 16); txt(d, "TAX RULES", 540, 1350, 46)
    for k in range(4): d.line((350, 1410 + k * 34, 730, 1410 + k * 34), fill=(180, 176, 168), width=6)
    k = ramp(lt, WT(2, "rule") - 0.1, WT(2, "rule") + 0.15); stamp(f, "100% LEGAL", 540, 1430, 70, GREEN, k, -8); return f
def s3(lt, T):   # See, when you get paid, the government takes its share first.
    f = kitchen(); d = ImageDraw.Draw(f, "RGBA")
    C.person(f, C.YOU, 300, 820, 170, "neutral" if lt < WT(3, "government") else "worried", ("hold", "down"), 1)
    cut = ease(ramp(lt, WT(3, "takes"), WT(3, "share") + 0.3)); paycheck(d, 640, 1260, 520, cut)
    if cut > 0:   # abgeschnittenes Stueck fliegt weg zum "Staat"
        rr(d, (620, 400, 1000, 540), (60, 70, 100), INK, 6, 14); txt(d, "GOVERNMENT", 810, 470, 44, WHITE)
        x = 820 + 0 * cut; y = 1260 - 640 * cut; d.rectangle((x - 80, y - 60, x + 80, y + 60), fill=(220, 245, 220), outline=INK, width=6); txt(d, "-$900", x, y, 44, RED)
    pop_text(f, "TAX FIRST", 540, 1620, 90, YEL, ramp(lt, WT(3, "first") - 0.05, WT(3, "first") + 0.2)); return f
def s4(lt, T):   # But billionaires like Jeff don't really live on a paycheck.
    f = office(); d = ImageDraw.Draw(f, "RGBA")
    C.person(f, C.BEZOS, 540, 760, 200, "grin", ("shrug", "shrug"), 0)
    pc = WT(4, "paycheck"); k = ease(ramp(lt, pc - 0.1, pc + 0.4))
    paycheck(d, 540 + 300 * k, 1300 - 500 * k, 420)
    if lt > pc: d.line((300, 1100, 780, 1500), fill=RED, width=20); d.line((780, 1100, 300, 1500), fill=RED, width=20)
    return f
def s5(lt, T):   # They own a mountain of stock.
    f = vault(); top = mountain(f, 540, 1500, 900, ease(ramp(lt, 0.0, T * 0.9)))
    C.person(f, C.BEZOS, 540, int(top) - 230, 130, "grin", ("up", "up"), 0)
    pop_text(f, "A MOUNTAIN OF STOCK", 540, 320, 80, GOLD, ramp(lt, WT(5, "mountain") - 0.05, WT(5, "mountain") + 0.2)); return f
def s6(lt, T):   # And you only pay tax on stock when you sell it.
    f = vault(); top = mountain(f, 540, 1500, 900, 1.0)
    d = ImageDraw.Draw(f, "RGBA"); k = back(ramp(lt, WT(6, "sell") - 0.2, WT(6, "sell") + 0.2))
    if k > 0:
        rr(d, (220, int(110 - 300 * (1 - k)), 860, int(300 - 300 * (1 - k))), WHITE, INK, 8, 24); txt(d, "SELL  =  TAX", 540, int(205 - 300 * (1 - k)), 88, RED)
    C.person(f, C.BEZOS, 540, int(top) - 230, 130, "neutral", ("hip", "hip"), 0); return f
def s7(lt, T):   # So... they don't sell.
    f = vault(); top = mountain(f, 540, 1500, 900, 1.0); d = ImageDraw.Draw(f, "RGBA")
    ds = WT(7, "sell"); fall = ease(ramp(lt, ds - 0.1, ds + 0.35))
    lay = Image.new("RGBA", (W, H)); ld = ImageDraw.Draw(lay); rr(ld, (220, 110, 860, 300), WHITE, INK, 8, 24); txt(ld, "SELL  =  TAX", 540, 205, 88, RED)
    lay = lay.rotate(-70 * fall, center=(860, 300), resample=Image.BICUBIC); f.alpha_composite(lay, (0, int(900 * fall * fall)))
    C.person(f, C.BEZOS, 540, int(top) - 230, 130, "smug", ("cross", "cross"), 0)
    pop_text(f, "THEY DON'T SELL", 540, 1590, 84, YEL, ramp(lt, ds - 0.1, ds + 0.15)); return f
def s8(lt, T):   # Need cash for a new yacht?
    f = sea(); d = ImageDraw.Draw(f, "RGBA"); k = ease(ramp(lt, 0.0, 0.6))
    yacht(d, 540 + int(500 * (1 - k)), 1000, 1.2)
    pop_text(f, "$500,000,000", 540, 420, 110, GOLD, ramp(lt, WT(8, "yacht") - 0.1, WT(8, "yacht") + 0.2), box=(30, 30, 40)); return f
def s9(lt, T):   # They borrow against that mountain.
    f = bank(); d = ImageDraw.Draw(f, "RGBA")
    C.person(f, C.BEZOS, 270, 900, 160, "grin", ("down", "give"), 1)
    C.person(f, C.BANKER, 830, 900, 160, "smug", ("give", "down"), -1)
    d.rectangle((0, 1350, W, 1500), fill=(120, 90, 70), outline=INK, width=6)   # Schalter
    bw = WT(9, "borrow"); k = ease(ramp(lt, bw, bw + 0.6)); money_bag(d, 830 - 420 * k, 1240, 0.9, "$")
    sk_ = ease(ramp(lt, 0, 0.5)); sx_ = 420 + 260 * sk_; rr(d, (sx_ - 80, 1260, sx_ + 80, 1340), (230, 245, 230), INK, 5, 8); txt(d, "STOCK", sx_, 1300, 34, (40, 110, 60))
    pop_text(f, "BORROW", 540, 360, 110, WHITE, ramp(lt, bw - 0.05, bw + 0.2), box=(40, 90, 170)); return f
def s10(lt, T):  # Borrowed money isn't income.
    f = bank(); d = ImageDraw.Draw(f, "RGBA"); money_bag(d, 540, 1050, 1.6, "LOAN")
    k = ramp(lt, WT(10, "income") - 0.1, WT(10, "income") + 0.2)
    pop_text(f, "LOAN ≠ INCOME", 540, 420, 100, WHITE, k, box=(30, 30, 40)); return f
def s11(lt, T):  # So... no tax.
    f = bank(); d = ImageDraw.Draw(f, "RGBA"); money_bag(d, 540, 1050, 1.6, "LOAN")
    pop_text(f, "LOAN ≠ INCOME", 540, 420, 100, WHITE, 1.0, box=(30, 30, 40))
    stamp(f, "NO TAX", 540, 1080, 150, GREEN, ramp(lt, WT(11, "tax") - 0.1, WT(11, "tax") + 0.15), -12); return f
def s12(lt, T):  # The mountain keeps growing.
    f = vault(); g = 1.0 + 0.35 * ease(ramp(lt, 0, T)); top = mountain(f, 540, 1500, 900, g)
    C.person(f, C.BEZOS, 540, int(top) - 230, 120, "grin", ("up", "up"), 0)
    for i in range(3):
        k = ramp(lt, 0.2 + i * 0.3, 0.6 + i * 0.3); y = 1300 - 600 * k
        if 0 < k < 1: txt(ImageDraw.Draw(f), "▲", 200 + i * 340, y, 80, GREEN)
    return f
def s13(lt, T):  # So they just borrow more.
    f = bank(); d = ImageDraw.Draw(f, "RGBA")
    C.person(f, C.BEZOS, 300, 900, 160, "grin", ("hold", "hold"), 1)
    n = 1 + int(ramp(lt, 0.1, T - 0.1) * 4)
    for i in range(n): money_bag(d, 620 + (i % 2) * 220, 1400 - (i // 2) * 210, 0.8, "LOAN")
    pop_text(f, "AND AGAIN", 540, 380, 110, WHITE, ramp(lt, WT(13, "more") - 0.1, WT(13, "more") + 0.15), box=(40, 90, 170)); return f
def s14(lt, T):  # And when they die, their kids get it all...
    f = mansion(); d = ImageDraw.Draw(f, "RGBA")
    rr(d, (300, 1350, 780, 1600), (240, 232, 214), INK, 6, 12); txt(d, "LAST WILL", 540, 1400, 44)
    for k in range(3): d.line((350, 1460 + k * 36, 730, 1460 + k * 36), fill=(180, 170, 150), width=6)
    kd = WT(14, "kids")
    for j, (kid, x) in enumerate(((C.KID1, 190), (C.KID2, 890))):
        k = back(ramp(lt, kd - 0.1 + j * 0.15, kd + 0.3 + j * 0.15))
        if k > 0: C.person(f, kid, x, int(1050 + (1 - k) * 600), 120, "grin" if False else "neutral", ("up", "up"), 0)
    pop_text(f, "INHERITED", 540, 420, 110, GOLD, ramp(lt, WT(14, "all") - 0.1, WT(14, "all") + 0.2)); return f
def s15(lt, T):  # and the tax on all that growth disappears.
    f = mansion(); d = ImageDraw.Draw(f, "RGBA")
    dis = WT(15, "disappears"); k = ease(ramp(lt, dis - 0.2, dis + 0.4))
    lay = Image.new("RGBA", (W, H)); ld = ImageDraw.Draw(lay)
    rr(ld, (200, 760, 880, 1160), WHITE, INK, 8, 20); txt(ld, "TAX ON GROWTH", 540, 840, 54); txt(ld, "ON BILLIONS", 540, 980, 76, RED)
    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * (1 - k)))); f.alpha_composite(lay)
    if k > 0:   # Radiergummi wischt drueber
        ex = 160 + 760 * k; ImageDraw.Draw(f).rounded_rectangle((ex - 90, 900, ex + 90, 1010), 18, fill=(240, 120, 140), outline=INK, width=6)
    pop_text(f, "GONE.", 540, 1350, 170, YEL, ramp(lt, dis + 0.2, dis + 0.5))
    return f

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15]

# ---------------- Look + Untertitel ----------------
_FIN = None
def finish(img):
    global _FIN
    if _FIN is None:
        g = Image.effect_noise((W, H), 22).convert("L"); v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse((-300, -260, W + 300, H + 260), fill=255)
        _FIN = (Image.merge("RGB", (g, g, g)), v.filter(ImageFilter.GaussianBlur(260)))
    g, v = _FIN; im = Image.blend(img, g, 0.025)
    return Image.composite(im, Image.blend(im, Image.new("RGB", (W, H), (18, 14, 22)), 0.4), v)
def captions(d, gt):
    cur = max([i for i, w in enumerate(ALLW) if w[1] <= gt] or [0]); g0 = cur - cur % 3; grp = ALLW[g0:g0 + 3]
    if not grp or gt > grp[-1][2] + 0.4: return
    words = [w[0] for w in grp]; f = F(60); sp = d.textlength(" ", font=f); ws = [d.textlength(w, font=f) for w in words]
    x = W / 2 - (sum(ws) + sp * (len(words) - 1)) / 2
    for k, w in enumerate(words):
        d.text((x, 1700), w, font=f, fill=YEL if g0 + k == cur else WHITE, anchor="lm", stroke_width=8, stroke_fill=(0, 0, 0)); x += ws[k] + sp

def frame(gt):
    si = 0
    for s in SEGS:
        if gt >= s["t0"] - 0.06: si = s["i"]
    s = SEGS[si]; lt = gt - s["t0"]; T = s["a1"] - s["a0"]
    f = SCENES[si](lt, T)
    if si > 0 and -0.06 <= lt < 0.07: f.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(90 * (1 - max(0, lt + 0.06) / 0.13)))))
    im = finish(f.convert("RGB")).convert("RGBA"); d = ImageDraw.Draw(im); captions(d, gt)
    return im.convert("RGB")

# ---------------- Ton: Stimme + Impacts + tiefer Teppich (ohne Melodie) + leiser Takt ----------------
def pulse(n, bpm=96):
    out = np.zeros(n, np.float32); step = 60 / bpm; tt = np.arange(int(SR * 0.2)) / SR
    kick = np.sin(2 * np.pi * (50 + 50 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 16); t_ = 0.0
    while t_ < n / SR:
        j = int(t_ * SR); out[j:j + len(kick)] += kick[:max(0, n - j)]; t_ += step
    return out
def drone(n):
    tt = np.arange(n) / SR
    x = 0.6 * np.sin(2 * np.pi * 55 * tt) + 0.35 * np.sin(2 * np.pi * 82.4 * tt + 0.5) + 0.2 * np.sin(2 * np.pi * 110 * tt)
    return (x * (0.75 + 0.25 * np.sin(2 * np.pi * 0.07 * tt))).astype(np.float32)
CUES = [(0, "you", 0.0, "whoosh", 0.18), (1, "Zero", 0.12, "impact", 0.45), (2, "rule", 0.0, "stamp", 0.35), (3, "takes", 0.0, "scissors", 0.3),
        (4, "paycheck", 0.0, "whoosh", 0.2), (5, "mountain", 0.0, "riser", 0.2), (6, "sell", -0.1, "pop", 0.3), (7, "sell", 0.1, "impact", 0.35),
        (8, "yacht", 0.0, "cash", 0.3), (9, "borrow", 0.0, "paper", 0.25), (10, "income", 0.0, "pop", 0.25), (11, "tax", -0.05, "stamp", 0.4),
        (12, "growing", 0.0, "riser", 0.18), (13, "more", 0.0, "coins", 0.25), (14, "kids", 0.0, "pop", 0.25), (15, "disappears", 0.0, "impact", 0.5)]
def audio():
    n = int(TOTAL * SR) + SR; v = np.zeros(n, np.float32); fx = np.zeros(n, np.float32)
    for s in SEGS:
        a = RAW[int(s["a0"] * SR):int(s["a1"] * SR)].copy(); fl = SR // 200; a[:fl] *= np.linspace(0, 1, fl); a[-fl:] *= np.linspace(1, 0, fl)
        i = int(s["t0"] * SR); v[i:i + len(a)] += a
    for si, w, off, name, g in CUES:
        j = max(0, int((SEGS[si]["t0"] + WT(si, w) + off) * SR)); x = SFXL.load(name)[:max(0, n - j)] * g; fx[j:j + len(x)] += x
    cs = np.concatenate([[0.0], np.cumsum(np.abs(v), dtype=np.float64)]); idx = np.arange(n)
    lo, hi = np.clip(idx - 2400, 0, n), np.clip(idx + 2400, 0, n); vabs = ((cs[hi] - cs[lo]) / 4800).astype(np.float32)
    duck = 1 - 0.4 * np.clip(vabs / 0.05, 0, 1)
    pu = pulse(n); pu *= 0.016 / (np.sqrt(np.mean(pu ** 2)) + 1e-9)
    dr = drone(n); dr *= 0.012 / (np.sqrt(np.mean(dr ** 2)) + 1e-9)
    bed = (pu + dr) * duck; fi = int(0.4 * SR); bed[:fi] *= np.linspace(0, 1, fi); bed[-fi:] *= np.linspace(1, 0, fi)
    out = v * 1.05 + fx + bed; m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)]

if __name__ == "__main__":
    print(f"Laenge {TOTAL:.1f}s")
    if "--stills" in sys.argv:
        tiles = []
        for s in SEGS:
            for fr in (0.35, 0.9): tiles.append(frame(s["t0"] + (s["a1"] - s["a0"]) * fr).resize((216, 384)))
        cols = 8; rows = math.ceil(len(tiles) / cols); sh = Image.new("RGB", (216 * cols, 384 * rows))
        for i, t_ in enumerate(tiles): sh.paste(t_, ((i % cols) * 216, (i // cols) * 384))
        sh.save("STORYBOARD.jpg", quality=85); print("ok"); sys.exit()
    out = av.open("ARC_Short07_Bezos.mp4", "w"); vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "19", "preset": "medium"}
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
