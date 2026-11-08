"""ARC Short #04 - "Should You Sell Your Stocks Right Now?" (9:16, realistische Strichmaennchen).
Jeder Bildwechsel / jedes Ereignis haengt am gesprochenen Wort (Scribe-Zeitstempel). Pausen zwischen Saetzen gekuerzt.
Aufruf: python short04.py --stills | (voll)"""
import sys, os, json, re, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "../../sfx_lib")); sys.path.insert(0, os.path.join(HERE, "../../longform/02_ai"))
import numpy as np, av
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from stick import INK
import cartoon
from cartoon import person, closeup, LEO as C_LEO, TRADER_R, TRADER_B, POLI, INVESTOR
import lib as SFXL

SR, FPS = 48000, 30; W, H = 1080, 1920
BOLD = "C:/Windows/Fonts/ariblk.ttf"; SANS = "C:/Windows/Fonts/arialbd.ttf"; MONO = "C:/Windows/Fonts/consolab.ttf"
_f = {}
def F(s, p=BOLD):
    if (p, s) not in _f: _f[(p, s)] = ImageFont.truetype(p, int(s))
    return _f[(p, s)]
RED = (225, 45, 55); GREEN = (40, 170, 90); YEL = (255, 205, 50); PAPER = (240, 236, 226); WHITE = (255, 255, 255)

# ---------------- Stimme + Woerter -> neue Zeitachse (Satzpausen gekuerzt) ----------------
SENT = [
 "Should you sell your stocks right now?",
 "On Thursday, two and a half trillion dollars vanished from Wall Street. In one day. Nvidia alone lost four hundred fifty billion.",
 "Why? Fear that new rules could slow down AI. And a lot of people had bet on AI with borrowed money. When prices dropped, they were forced to sell. That's why it crashed so fast.",
 "So what's the smart move? History has three rules.",
 "One: don't panic-sell. The biggest jumps usually come right after the biggest drops. Miss them, and you lose years of gains.",
 "Two: don't go all in either. Smart money buys slowly, a little every month, so it never has to guess the bottom.",
 "Three: only invest money you won't need for years. Then a crash isn't a disaster. It's a sale.",
 "Not financial advice. Just how crashes made people rich instead of poor.",
 "So... are you holding, buying, or selling?"]
def dec(p):
    c = av.open(p); r = av.AudioResampler(format="flt", layout="mono", rate=SR); out = []
    for fr in c.decode(audio=0):
        for f in r.resample(fr): out.append(f.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.float32)
RAW = dec("vo/s04.mp3")
WR = [w for w in json.load(open("vo/words.json", encoding="utf-8"))["words"] if not (w["text"].startswith("[") or w["text"].endswith("]"))]
GAP = 0.24; LEAD = 0.25
SEGS = []; pos = 0; t = LEAD
for si, s in enumerate(SENT):
    n = len(s.split()); ws = WR[pos:pos + n]; pos += n
    a0 = max(0, ws[0]["start"] - 0.05); a1 = ws[-1]["end"] + 0.10
    SEGS.append(dict(i=si, t0=t, a0=a0, a1=a1, words=[(w["text"], w["start"] - a0 + t, w["end"] - a0 + t) for w in ws]))
    t += (a1 - a0) + GAP
TOTAL = t + 0.2
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

# ---------------- Zeichen-Bausteine ----------------
def rr(d, box, fill, out=INK, w=6, r=24): d.rounded_rectangle(box, r, fill=fill, outline=out, width=w)
def txt(d, s, x, y, size, col=INK, anchor="mm", font=BOLD, stroke=0, sc=INK): d.text((x, y), s, font=F(size, font), fill=col, anchor=anchor, stroke_width=stroke, stroke_fill=sc)
def label(d, s, x, y, size, col=WHITE, k=1.0):
    if k <= 0: return
    sz = size * (0.8 + 0.2 * ease(k / 0.6)); txt(d, s, x, y, sz, col, stroke=int(size * 0.09), sc=INK)
def chart(d, box, pts, k=1.0, col=RED, w=12):
    x0, y0, x1, y1 = box; k = max(0.0, min(1.0, k))
    A = [(x0 + (x1 - x0) * i / (len(pts) - 1), y1 - (y1 - y0) * v) for i, v in enumerate(pts)]
    if k <= 0.001: return []
    u = k * (len(A) - 1); i = int(u); P = A[:i + 1]
    if i < len(A) - 1: fr = u - i; P = P + [(A[i][0] + (A[i + 1][0] - A[i][0]) * fr, A[i][1] + (A[i + 1][1] - A[i][1]) * fr)]
    if len(P) >= 2: d.line(P, fill=col, width=w, joint="curve")
    tx, ty = P[-1]; d.ellipse((tx - w, ty - w, tx + w, ty + w), fill=col)
    return P
def phone(d, cx, cy, w, h):
    rr(d, (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2), (30, 30, 36), INK, 8, 46)
    rr(d, (cx - w // 2 + 18, cy - h // 2 + 40, cx + w // 2 - 18, cy + h // 2 - 40), (250, 250, 252), None, 0, 26)
    return (cx - w // 2 + 18, cy - h // 2 + 40, cx + w // 2 - 18, cy + h // 2 - 40)
def button(d, cx, cy, s, col, w=300, h=120, glow=False):
    if glow: d.rounded_rectangle((cx - w // 2 - 14, cy - h // 2 - 14, cx + w // 2 + 14, cy + h // 2 + 14), 40, fill=col + (90,))
    rr(d, (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2), col, INK, 6, 34); txt(d, s, cx, cy, h * 0.45, WHITE)
def stamp(d, s, cx, cy, size, col=RED, k=1.0, rot=-8):
    if k <= 0: return
    lay = Image.new("RGBA", (W, H)); dl = ImageDraw.Draw(lay); f = F(size)
    tw = dl.textlength(s, font=f); dl.rounded_rectangle((cx - tw / 2 - 30, cy - size * 0.75, cx + tw / 2 + 30, cy + size * 0.75), 18, outline=col, width=12)
    dl.text((cx, cy), s, font=f, fill=col, anchor="mm")
    sc = 1.6 - 0.6 * ease(k / 0.25); lay = lay.rotate(rot, center=(cx, cy), resample=Image.BICUBIC)
    if sc != 1: lay = lay.resize((int(W * sc), int(H * sc)), Image.BICUBIC).crop((int((W * sc - W) / 2 + (cx * sc - cx) - (W * sc - W) / 2), int((H * sc - H) / 2 + (cy * sc - cy) - (H * sc - H) / 2), 0, 0)) if False else lay
    d._image.alpha_composite(lay)
def coin(d, cx, cy, r=34): d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=YEL, outline=INK, width=5); txt(d, "$", cx, cy + 2, r * 1.1, INK)
def jar(d, cx, base, w, h, fill_k, s, col=(120, 200, 140)):
    x0, x1, y0 = cx - w // 2, cx + w // 2, base - h
    lvl = base - 12 - (h - 40) * fill_k
    d.rectangle((x0 + 10, lvl, x1 - 10, base - 10), fill=col)
    rr(d, (x0, y0, x1, base), None, INK, 7, 30); d.rectangle((x0 + 20, y0 - 30, x1 - 20, y0 + 6), fill=(200, 200, 210), outline=INK, width=6)
    txt(d, s, cx, base + 50, 40)
def server(d, x0, y0, x1, y1):
    rr(d, (x0, y0, x1, y1), (60, 66, 84), INK, 7, 16)
    for y in range(y0 + 30, y1 - 20, 46):
        d.rectangle((x0 + 24, y, x1 - 24, y + 28), fill=(40, 44, 58), outline=INK, width=3)
        for k in range(4): d.ellipse((x1 - 60 + k * 0, y + 8, x1 - 48, y + 20), fill=(90, 220, 140))
def robot(d, cx, base, h, arm_down=False):
    w = h * 0.42; head = (cx - w * 0.45, base - h, cx + w * 0.45, base - h + w * 0.7)
    rr(d, head, (200, 205, 216), INK, 6, 18); d.rectangle((cx - w * 0.3, base - h + w * 0.22, cx + w * 0.3, base - h + w * 0.42), fill=(40, 200, 255))
    rr(d, (cx - w / 2, base - h + w * 0.78, cx + w / 2, base - h * 0.32), (200, 205, 216), INK, 6, 14)
    d.line([(cx - w * 0.3, base - h * 0.32), (cx - w * 0.3, base)], fill=INK, width=14); d.line([(cx + w * 0.3, base - h * 0.32), (cx + w * 0.3, base)], fill=INK, width=14)
    ay = base - h * (0.5 if arm_down else 0.75); d.line([(cx + w / 2, base - h * 0.6), (cx + w * 0.95, ay)], fill=INK, width=14)
    return (cx + w * 0.95, ay)


# ---------------- Animations-Helfer ----------------
def back(x):                                     # federndes Einrasten
    x = max(0.0, min(1.0, x)); c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
TICK = "  DOW -3.4% \u25bc   S&P 500 -4.1% \u25bc   NASDAQ -5.5% \u25bc   NVIDIA -9.3% \u25bc   MICRON -17% \u25bc   BROADCOM -10% \u25bc"
def ticker(d, gt, y=0, h=70, col=(150, 16, 24)):
    d.rectangle((0, y, W, y + h), fill=col + (235,)); f = F(38); tw = d.textlength(TICK, font=f)
    x = -((gt * 260) % tw)
    while x < W: d.text((x, y + h / 2), TICK, font=f, fill=WHITE, anchor="lm"); x += tw
def arrows(d, lt, n=26, seed=3, x0=0, x1=W, y0=-100, y1=1500, speed=900):
    r = random.Random(seed)
    for k in range(n):
        x = r.uniform(x0, x1); off = r.uniform(0, 3); sz = r.uniform(26, 60)
        y = y0 + ((lt + off) * speed * r.uniform(0.7, 1.3)) % (y1 - y0)
        d.polygon([(x - sz * 0.5, y), (x + sz * 0.5, y), (x, y + sz * 0.9)], fill=(230, 50, 60, 200))
def block_img(w, h, col, label):
    im = Image.new("RGBA", (w + 12, h + 12)); dd = ImageDraw.Draw(im)
    dd.rounded_rectangle((6, 6, w + 6, h + 6), 12, fill=col, outline=INK, width=6); dd.text((w / 2 + 6, h / 2 + 6), label, font=F(52), fill=WHITE, anchor="mm")
    return im
SHAKES = []                                      # (globale Zeit, Staerke)
def shake_at(gt):
    dx = dy = 0.0
    for t0, a in SHAKES:
        e = gt - t0
        if 0 <= e < 0.35: k = (1 - e / 0.35) * a; dx += math.sin(e * 90) * k; dy += math.cos(e * 77) * k
    return int(dx), int(dy)


def heartbeat(f, t, strength=1.0, col=(200, 20, 30)):
    """roter Herzschlag-Rand (doppelter Schlag) - Gefuehl von Panik"""
    u = t % 0.82; k = max(math.exp(-((u - 0.0) / 0.07) ** 2), 0.7 * math.exp(-((u - 0.2) / 0.07) ** 2)) * strength
    if k < 0.03: return
    global _HB
    if "_HB" not in globals():
        m = Image.new("L", (W, H), 255); ImageDraw.Draw(m).ellipse((-120, 80, W + 120, H - 80), fill=0); _HB = m.filter(ImageFilter.GaussianBlur(160))
    lay = Image.new("RGBA", (W, H), col + (0,)); lay.putalpha(_HB.point(lambda v: int(v * 0.75 * k))); f.alpha_composite(lay)
def facelight(f, cx, cy, r, col, a):
    lay = Image.new("RGBA", (W, H)); ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (int(a),))
    f.alpha_composite(lay.filter(ImageFilter.GaussianBlur(r * 0.5)))
def big_phone(d, f, cx, cy, w, h, rot, screen_fn):
    """Handy gross im Vordergrund, leicht schraeg"""
    ph = Image.new("RGBA", (w + 40, h + 40)); pd = ImageDraw.Draw(ph, "RGBA")
    pd.rounded_rectangle((20, 20, w + 20, h + 20), 56, fill=(28, 28, 34), outline=INK, width=9)
    pd.rounded_rectangle((40, 66, w, h - 26), 34, fill=(250, 250, 252)); screen_fn(pd, (40, 66, w, h - 26))
    sk = (238, 202, 170)                                  # Hand haelt das Handy (Finger links, Daumen am Rand)
    for j in range(3): pd.rounded_rectangle((0, int(h * 0.5) + j * 70, 70, int(h * 0.5) + j * 70 + 62), 30, fill=sk, outline=INK, width=6)
    pd.rounded_rectangle((w - 10, int(h * 0.58), w + 40, int(h * 0.58) + 120), 26, fill=sk, outline=INK, width=6)
    ph = ph.rotate(rot, resample=Image.BICUBIC, expand=True); f.alpha_composite(ph, (int(cx - ph.width / 2), int(cy - ph.height / 2)))
def sweat(d, x, y, lt, period=1.1, n=0):
    u = ((lt + n * 0.4) % period) / period; yy = y + u * 120; a = int(255 * (1 - u))
    d.polygon([(x, yy - 30), (x - 14, yy), (x + 14, yy)], fill=(160, 215, 255, a)); d.ellipse((x - 14, yy - 12, x + 14, yy + 16), fill=(160, 215, 255, a), outline=(20, 30, 50, a), width=3)

# ---------------- Szenen (si = Satzindex, lt = Zeit im Satz) ----------------
sys.path.insert(0, os.path.join(HERE, "../../longform/01_money"))
import bgs as BG, ai_kit as AK
_bgc = {}
def _crop(img):                                  # Querformat-Hintergrund -> 9:16 (Mitte), weich
    im = img.convert("RGB"); s_ = H / im.height; im = im.resize((int(im.width * s_), H), Image.LANCZOS)
    x0 = (im.width - W) // 2; return im.crop((x0, 0, x0 + W, H)).convert("RGBA")
def _vgrad(c0, c1):
    a = np.linspace(0, 1, H)[:, None, None]; arr = (np.array(c0) * (1 - a) + np.array(c1) * a).repeat(W, 1)
    return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
def _spot(img, cx, cy, r, col, alpha):
    lay = Image.new("RGBA", (W, H)); ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (alpha,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(r * 0.45))); return img
def place(name):
    if name in _bgc: return _bgc[name].copy()
    if name == "home": im = _crop(BG.bg("apartment", True)); im.alpha_composite(Image.new("RGBA", (W, H), (10, 12, 30, 60))); _spot(im, 760, 640, 420, (140, 190, 255), 70)
    elif name == "floor":
        im = _vgrad((10, 14, 30), (26, 20, 40)); d_ = ImageDraw.Draw(im)
        for k in range(7): d_.rectangle((k * 160 - 20, 1100, k * 160 + 120, 1300), fill=(18, 20, 34), outline=(40, 44, 70), width=3)
        _spot(im, W // 2, 330, 520, (255, 60, 70), 70)
    elif name == "server": im = _crop(AK.abg("server")); _spot(im, W // 2, 900, 600, (90, 200, 255), 40)
    elif name == "office": im = _crop(BG.bg("office")); im.alpha_composite(Image.new("RGBA", (W, H), (250, 248, 240, 70)))
    elif name == "dark": im = _crop(BG.bg("apartment", True)); im.alpha_composite(Image.new("RGBA", (W, H), (6, 4, 14, 150))); _spot(im, 760, 640, 380, (255, 70, 70), 60)
    elif name == "alert": im = _vgrad((70, 8, 16), (18, 4, 8)); _spot(im, W // 2, 760, 600, (255, 60, 60), 80)
    elif name.startswith("studio"):
        c = {"studio_b": ((226, 232, 246), (190, 202, 226)), "studio_w": ((246, 238, 222), (216, 204, 182)), "studio_g": ((228, 242, 232), (190, 216, 198))}[name]
        im = _vgrad(*c); _spot(im, W // 2, 700, 560, (255, 255, 255), 120)
    else: im = Image.new("RGBA", (W, H), PAPER + (255,))
    _bgc[name] = im; return im.copy()
def bg(col, name=None):
    f = place(name) if name else Image.new("RGBA", (W, H), col + (255,)); return f, ImageDraw.Draw(f, "RGBA")
_FIN = None
def finish(img):
    global _FIN
    if _FIN is None:
        g = Image.effect_noise((W, H), 22).convert("L"); v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse((-260, -220, W + 260, H + 220), fill=255)
        _FIN = (Image.merge("RGB", (g, g, g)), v.filter(ImageFilter.GaussianBlur(240)))
    g, v = _FIN; im = Image.blend(img, g, 0.03)
    return Image.composite(im, Image.blend(im, Image.new("RGB", (W, H), (12, 10, 18)), 0.42), v)
LEO = dict(glasses=True, hair="short")
def leo_phone(d, lt, screen_fn, expr="worried"):
    person(d._image, C_LEO, 400, 1380, 190, "phone", 1, expr)
    bx = phone(d, 760, 640, 420, 760); screen_fn(d, bx)
def s0(lt, T):
    f, d = bg(PAPER, "dark")
    k = ease(ramp(lt, 0, T)); v = -2.0 - 16.4 * k
    facelight(f, 470, 620, 430, (120, 170, 255) if v > -9 else (255, 70, 70), 70 + 40 * k)
    closeup(f, C_LEO, 500, 300, 1120, "stand", 1, "worried" if v > -9 else "shock")
    if v <= -9:
        sweat(d, 300, 470, lt, 1.0, 0); sweat(d, 700, 430, lt, 1.3, 1)
    def scr(pd, bx):
        x0, y0, x1, y1 = bx; cx = (x0 + x1) // 2
        txt(pd, "MY STOCKS", cx, y0 + 50, 34, (90, 96, 110), font=SANS)
        txt(pd, f"{v:.1f}%", cx, y0 + 130, 78, RED)
        chart(pd, (x0 + 30, y0 + 200, x1 - 30, y0 + 420), [0.9, 0.95, 0.85, 0.9, 0.72, 0.6, 0.42, 0.3, 0.12], 0.25 + 0.75 * k, RED, 9)
        pul = 0.5 + 0.5 * math.sin(lt * 9)
        button(pd, cx, y1 - 100, "SELL", RED, int(270 + 16 * pul), int(106 + 6 * pul), glow=True)
    big_phone(d, f, 800, 1210, 420, 760, -8, scr)
    heartbeat(f, lt, 0.5 + 0.6 * k)
    ticker(ImageDraw.Draw(f, "RGBA"), lt, 0)
    return f
def s1(lt, T):
    f, d = bg((22, 24, 34), "floor")
    d.rectangle((0, 120, W, 520), fill=(14, 16, 24)); txt(d, "WALL STREET", W // 2, 180, 48, (200, 206, 220))
    for k in range(5):
        x = 70 + k * 200; up = (k * 37) % 3 == 0
        txt(d, ["DOW", "S&P", "NDX", "NVDA", "MU"][k], x + 70, 290, 40, WHITE); txt(d, ["-3.4%", "-4.1%", "-5.5%", "-9.3%", "-17%"][k], x + 70, 360, 46, RED)
    arrows(d, lt, 22, 5, 0, W, 520, 1500, 700)
    v = 2.5 * ease(ramp(lt, WT(1, "two"), WT(1, "Street") + 0.3))
    pul = 1 + 0.04 * math.sin(lt * 12) if lt > WT(1, "vanished") else 1
    label(d, f"-${v:.1f} TRILLION", W // 2, 640, 110 * pul, RED)
    label(d, "IN ONE DAY", W // 2, 770, 70, WHITE, ramp(lt, WT(1, "In", 1), WT(1, "In", 1) + 0.3))
    for k, x in enumerate((230, 540, 850)):
        rx = lt > WT(1, "vanished") + k * 0.14
        person(d._image, TRADER_R if k != 1 else TRADER_B, x, 1400, 110, "hands_head" if rx else "stand", 1 if k < 2 else -1, "shock" if rx else "worried", seed=k)
    if lt > WT(1, "Nvidia"):
        k = ramp(lt, WT(1, "Nvidia"), WT(1, "Nvidia") + 0.22); y = -300 + (1020 + 300) * (k * k)
        rr(d, (200, y - 130, 880, y + 130), WHITE, INK, 9, 30); txt(d, "NVIDIA", 540, y - 55, 74); txt(d, "-$450 BILLION", 540, y + 55, 70, RED)
        if k >= 1:
            c_ = ramp(lt, WT(1, "Nvidia") + 0.22, WT(1, "Nvidia") + 0.5); pts = [(560, 890), (520, 960), (585, 1020), (540, 1100), (600, 1150)]
            d.line(pts[:max(2, int(len(pts) * c_))], fill=INK, width=8)
    return f
def s2(lt, T):
    tw = [WT(2, "Why"), WT(2, "And", 1), WT(2, "When"), WT(2, "That's")]
    i = sum(1 for x in tw[1:] if lt >= x)
    if i == 0:
        f, d = bg((232, 236, 244), "server")
        label(d, "WHY?", W // 2, 330, 150, YEL, ramp(lt, 0, 0.2))
        server(d, 160, 620, 520, 1300); server(d, 560, 560, 920, 1300); txt(d, "AI DATA CENTERS", W // 2, 1370, 50, WHITE, stroke=5)
        r_ = random.Random(int(lt * 8))
        for k in range(26):
            x = r_.choice([470, 870]); y = 650 + r_.randint(0, 13) * 46; d.ellipse((x, y, x + 14, y + 14), fill=(255, 210, 80) if r_.random() < 0.5 else (90, 220, 140))
        if lt > WT(2, "slow"):
            k = ease(ramp(lt, WT(2, "slow"), WT(2, "slow") + 0.4)); x1_ = 60 + 960 * k
            d.line([(60, 1000), (x1_, 1040)], fill=(250, 210, 40), width=40)
            for xx in range(60, int(x1_), 80): d.line([(xx, 1000 + (xx - 60) * 0.04 - 18), (xx + 36, 1000 + (xx - 60) * 0.04 + 18)], fill=INK, width=10)
        person(d._image, POLI, 260, 1520, 80, "point", 1, "angry")
        if lt > WT(2, "rules"): stamp(d, "NEW RULES?", W // 2, 900, 96, RED, ramp(lt, WT(2, "rules"), WT(2, "rules") + 0.25))
    elif i == 1:
        f, d = bg((236, 242, 232), "office"); l = lt - tw[1]
        rr(d, (300, 1180, 780, 1320), (200, 70, 70), INK, 7, 14); txt(d, "BORROWED", 540, 1250, 60, WHITE)
        prog = ramp(lt, WT(2, "bet"), WT(2, "money") + 0.2) * 6; nb = min(6, int(prog) + 1); wob = math.sin(lt * 5) * 2.5 * (nb / 6)
        for k in range(nb):
            drop = 0 if k < nb - 1 else (1 - back(min(1, (prog - int(prog)) * 2.5))) * -260
            bi = block_img(400, 116, (90, 170, 120), "AI").rotate(wob * (k / 6), resample=Image.BICUBIC, expand=True)
            f.alpha_composite(bi, (int(540 - bi.width / 2 + wob * k * 2), int(1180 - (k + 1) * 120 + drop - 6)))
        person(d._image, TRADER_R, 880, 1700, 100, "throw", -1, "smile")
        d.line([(0, 1700), (W, 1700)], fill=INK, width=6)
    elif i == 2:
        f, d = bg((30, 30, 38), "dark")
        def scr(d, bx):
            x0, y0, x1, y1 = bx; rr(d, (x0 + 20, y0 + 60, x1 - 20, y0 + 330), (255, 236, 236), RED, 6, 20)
            txt(d, "MARGIN CALL", (x0 + x1) // 2, y0 + 130, 48, RED); txt(d, "Pay up or", (x0 + x1) // 2, y0 + 210, 40, INK, font=SANS); txt(d, "we sell.", (x0 + x1) // 2, y0 + 262, 40, INK, font=SANS)
            button(d, (x0 + x1) // 2, y1 - 110, "SELL", RED, 280, 110, glow=lt > WT(2, "forced"))
        vib = int(math.sin(lt * 70) * 10) if lt < WT(2, "forced") + 0.6 else 0
        facelight(f, 430, 600, 420, (255, 70, 70), 80)
        closeup(f, TRADER_R, 470, 320, 1100, "stand", 1, "worried" if lt < WT(2, "forced") else "shock", seed=3)
        if lt > WT(2, "forced"): sweat(d, 280, 480, lt, 1.0)
        big_phone(d, f, 800 + vib, 1180, 420, 760, -7 + vib * 0.3, lambda pd, bx: scr(pd, bx))
        heartbeat(f, lt, 0.7)
    else:
        f, d = bg((236, 232, 222), "alert"); l = lt - tw[3]
        tc = WT(2, "crashed"); e = max(0.0, lt - tc)
        for k in range(6):                                # Turm stuerzt ein
            r_ = random.Random(k); vx = r_.uniform(-260, 260); rot = r_.uniform(-140, 140)
            bx_ = 540 + vx * e; by_ = 1180 - (k + 1) * 120 + 900 * e * e * (0.6 + k * 0.1)
            if by_ < H + 200:
                bi = block_img(400, 116, (90, 170, 120), "AI").rotate(rot * e, resample=Image.BICUBIC, expand=True); f.alpha_composite(bi, (int(bx_ - bi.width / 2), int(by_)))
        rr(d, (300, 1180, 780, 1320), (200, 70, 70), INK, 7, 14); txt(d, "BORROWED", 540, 1250, 60, WHITE)
        label(d, "CRASH", W // 2, 300, 140, RED, ramp(lt, tc, tc + 0.2))
        person(d._image, TRADER_B, 880, 1560, 80, "hands_head", -1, "shock")
    return f
def cards(d, k_list, active=None):
    for j, (s, k) in enumerate(zip(["1", "2", "3"], k_list)):
        if k <= 0: continue
        x = 220 + j * 320; y = 1050 + (1 - back(k / 0.5)) * 700
        rr(d, (x - 130, y - 160, x + 130, y + 160), YEL if active in (None, j) else (220, 216, 206), INK, 8, 30); txt(d, s, x, y, 170)
def s3(lt, T):
    f, d = bg(PAPER)
    person(d._image, C_LEO, 540, 860, 115, "shrug", 0, "worried")
    label(d, "THE SMART MOVE?", W // 2, 210, 90, YEL, ramp(lt, 0, 0.25))
    k0 = WT(3, "three")
    if lt < k0 + 0.2:
        for j, (s_, c_) in enumerate((("HOLD?", (70, 110, 200)), ("BUY?", GREEN), ("SELL?", RED))):
            kk = back(ramp(lt, 0.15 + j * 0.18, 0.45 + j * 0.18)) * (1 - ramp(lt, k0, k0 + 0.2))
            if kk > 0.02: button(d, 220 + j * 320, int(1130 + (1 - kk) * 300), s_, c_, int(260 * max(kk, 0.3)), int(110 * max(kk, 0.3)))
    cards(d, [ramp(lt, k0, k0 + 0.3), ramp(lt, k0 + 0.25, k0 + 0.55), ramp(lt, k0 + 0.5, k0 + 0.8)])
    return f
def rule_head(d, n, s1_, s2_):
    rr(d, (60, 120, 1020, 400), YEL, INK, 8, 34); txt(d, n, 150, 260, 150); txt(d, s1_, 600, 220, 66); txt(d, s2_, 600, 310, 66)
def s4(lt, T):
    f, d = bg((236, 240, 248), "studio_b"); rule_head(d, "1", "DON'T", "PANIC-SELL")
    box = (90, 500, 990, 1060); pts = [0.7, 0.75, 0.6, 0.3, 0.12, 0.55, 0.8, 0.85, 0.97]
    if lt > WT(4, "Miss"):                                  # verpasster Bereich (hinter der Kurve)
        k = ramp(lt, WT(4, "Miss"), WT(4, "Miss") + 0.3); lay = Image.new("RGBA", (W, H))
        ImageDraw.Draw(lay).rounded_rectangle((540, 470, 1010, 1090), 30, fill=(225, 45, 55, int(70 * k)), outline=(225, 45, 55, int(230 * k)), width=8)
        f.alpha_composite(lay)
    xg = 90 + 900 * 4 / 8
    chart(d, (90, 500, int(xg), 1060), pts[:5], ramp(lt, WT(4, "biggest"), WT(4, "drops") + 0.2), RED, 16)
    gb = (int(xg), 500, 990, 1060)
    if lt > WT(4, "drops") + 0.2: chart(d, gb, pts[4:], ramp(lt, WT(4, "drops") + 0.2, WT(4, "jumps") + 0.5), GREEN, 16)
    if lt > WT(4, "jumps"): label(d, "BIGGEST JUMPS", 760, 1140, 54, GREEN, ramp(lt, WT(4, "jumps"), WT(4, "jumps") + 0.2))
    if lt > WT(4, "Miss"): stamp(d, "MISSED", 780, 760, int(96 + 60 * (1 - k)), RED, k, -10)
    person(d._image, C_LEO, 290, 1520, 90, "press" if lt < WT(4, "jumps") else ("hands_head" if lt > WT(4, "Miss") else "stand"), 1, "worried" if lt < WT(4, "jumps") else ("shock" if lt > WT(4, "Miss") else "neutral"))
    button(d, 640, 1280, "SELL", (170, 170, 176) if lt > WT(4, "jumps") else RED, 260, 100)
    if lt > WT(4, "jumps"): d.line([(520, 1220), (760, 1340)], fill=RED, width=14); d.line([(760, 1220), (520, 1340)], fill=RED, width=14)
    return f
def s5(lt, T):
    f, d = bg((240, 236, 226), "studio_w"); rule_head(d, "2", "DON'T GO", "ALL IN")
    t_slow = WT(5, "Smart")
    if lt < t_slow:
        person(d._image, INVESTOR, 320, 1520, 120, "throw", 1, "smile")
        k = ease(ramp(lt, WT(5, "all"), WT(5, "either") + 0.3)); rr(d, (520, 560 + 380 * k, 900, 820 + 380 * k), (90, 170, 120), INK, 7, 30); txt(d, "ALL MY MONEY", 710, 690 + 380 * k, 40, WHITE)
        stamp(d, "RISKY", 720, 1420, 90, RED, ramp(lt, WT(5, "either"), WT(5, "either") + 0.25))
    else:
        l = lt - t_slow; months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN"]
        m = min(5, int(ramp(lt, WT(5, "little"), WT(5, "bottom")) * 6))
        rr(d, (640, 520, 980, 760), WHITE, INK, 7, 20); txt(d, months[m], 810, 640, 90, RED)
        jar(d, 760, 1380, 300, 480, (m + 1) / 6, "INDEX FUND")
        person(d._image, C_LEO, 320, 1520, 120, "drop", 1, "smile")
        cy = 800 + (((l * 1.6) % 1) * 420); coin(d, 760, cy)
        if lt > WT(5, "guess"): label(d, "NO NEED TO GUESS THE BOTTOM", W // 2, 470, 46, RED)
    return f
def s6(lt, T):
    f, d = bg((236, 242, 236), "studio_g"); rule_head(d, "3", "MONEY YOU", "WON'T NEED")
    jar(d, 260, 1120, 280, 400, 0.7, "RENT · BILLS", (120, 170, 230)); jar(d, 820, 1120, 280, 400, 0.55, "10+ YEARS")
    txt(d, "CASH", 260, 860, 56, INK); txt(d, "INVEST", 820, 860, 56, INK)
    if lt > WT(6, "sale"):
        k = ramp(lt, WT(6, "sale"), WT(6, "sale") + 0.18); stamp(d, "SALE", 820, 560, int(120 + 80 * (1 - k)), RED, k, -12)
    elif lt > WT(6, "disaster"): label(d, "NOT A DISASTER...", W // 2, 540, 70, INK)
    person(d._image, C_LEO, 540, 1540, 70, "point", 1, "talk")
    return f
def s7(lt, T):
    f, d = bg((232, 236, 244), "studio_g"); txt(d, "NOT FINANCIAL ADVICE", W // 2, 200, 44, (120, 120, 130))
    pts = [0.1, 0.18, 0.14, 0.25, 0.2, 0.35, 0.3, 0.12, 0.4, 0.5, 0.45, 0.62, 0.55, 0.75, 0.7, 0.92]
    chart(d, (90, 400, 990, 1100), pts, ramp(lt, 0.2, T - 0.3), GREEN, 14)
    label(d, "RICH", 860, 380, 80, GREEN, ramp(lt, WT(7, "rich"), WT(7, "rich") + 0.25))
    person(d._image, C_LEO, 300, 1520, 95, "cheer" if lt > WT(7, "rich") else "stand", 1, "smile")
    return f
def s8(lt, T):
    f, d = bg(PAPER, "dark")
    hl = [WT(8, "holding"), WT(8, "buying"), WT(8, "selling")]
    a = sum(1 for x in hl if lt >= x) - 1
    facelight(f, 470, 620, 430, [(120, 170, 255), (90, 110, 220), (60, 200, 110), (255, 70, 70)][a + 1], 90)
    closeup(f, C_LEO, 500, 300, 1120, "stand", 1, "worried" if a < 2 else "shock")
    def scr(pd, bx):
        x0, y0, x1, y1 = bx; cx = (x0 + x1) // 2
        txt(pd, "WHAT'S YOUR MOVE?", cx, y0 + 60, 30, (90, 96, 110), font=SANS)
        for j, (s_, c_) in enumerate((("HOLD", (90, 110, 200)), ("BUY", GREEN), ("SELL", RED))):
            g = (a == j); button(pd, cx, y0 + 210 + j * 150, s_, c_, 300 + (24 if g else 0), 110 + (8 if g else 0), glow=g)
    big_phone(d, f, 800, 1210, 420, 760, -8, scr)
    return f
SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8]

def captions(d, gt):
    cur = max([i for i, w in enumerate(ALLW) if w[1] <= gt] or [0]); g0 = cur - cur % 3; grp = ALLW[g0:g0 + 3]
    if not grp or gt > grp[-1][2] + 0.5: return
    words = [w[0] for w in grp]; f = F(80); sp = d.textlength(" ", font=f)
    ws = [d.textlength(w, font=f) for w in words]
    while sum(ws) + sp * (len(words) - 1) > W - 80: f = F(f.size - 6); sp = d.textlength(" ", font=f); ws = [d.textlength(w, font=f) for w in words]
    x = W / 2 - (sum(ws) + sp * (len(words) - 1)) / 2
    for k, w in enumerate(words):
        d.text((x, 1680), w, font=f, fill=YEL if g0 + k == cur else WHITE, anchor="lm", stroke_width=9, stroke_fill=(0, 0, 0)); x += ws[k] + sp
def _init_shakes():
    for si, w, a in ((1, "vanished", 10), (1, "Nvidia", 16), (2, "rules", 10), (2, "crashed", 20), (6, "sale", 10)):
        SHAKES.append((SEGS[si]["t0"] + WT(si, w) + (0.22 if w == "Nvidia" else 0), a))
def frame(gt):
    cartoon.CLOCK[0] = gt
    if not SHAKES: _init_shakes()
    si = 0
    for s in SEGS:
        if gt >= s["t0"] - (LEAD if s["i"] == 0 else GAP * 0.5): si = s["i"]
    s = SEGS[si]; lt = gt - s["t0"]; T = s["a1"] - s["a0"]
    f = SCENES[si](lt, T)
    if si > 0 and -GAP * 0.5 <= lt < 0.10:
        k = 1 - max(0.0, lt + GAP * 0.5) / (0.10 + GAP * 0.5); f.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(110 * k))))
    dx, dy = shake_at(gt)
    if dx or dy: g_ = Image.new("RGBA", (W, H), (0, 0, 0, 255)); g_.paste(f, (dx, dy)); f = g_
    im = finish(f.convert("RGB")).convert("RGBA"); d = ImageDraw.Draw(im); captions(d, gt)
    if gt > TOTAL - 3.0:                                   # Musik-Nennung (CC BY 4.0) im Video statt in der Beschreibung
        d.text((W // 2, 1872), 'Music: "Hitman" & "Inspired" by Kevin MacLeod (incompetech.com) · CC BY 4.0', font=F(22, SANS), fill=(235, 235, 235), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    return im.convert("RGB")

CUES = [(1, "vanished", 1, "counter", 0.18), (1, "Nvidia", 1, "impact", 0.4), (2, "rules", 1, "stamp", 0.35), (2, "crashed", 1, "impact", 0.45),
        (3, "three", 1, "pop", 0.25), (4, "Miss", 1, "whoosh", 0.18), (5, "month", 1, "coins", 0.25), (6, "sale", 1, "stamp", 0.35)]
def audio():
    n = int(TOTAL * SR) + SR; v = np.zeros(n, np.float32); fx = np.zeros(n, np.float32)
    for s in SEGS:
        a = RAW[int(s["a0"] * SR):int(s["a1"] * SR)].copy(); fl = SR // 100; a[:fl] *= np.linspace(0, 1, fl); a[-fl:] *= np.linspace(1, 0, fl)
        i = int(s["t0"] * SR); v[i:i + len(a)] += a
    for si, w, k, name, g in CUES:
        tt = SEGS[si]["t0"] + WT(si, w, k); j = int(tt * SR); x = SFXL.load(name)[:max(0, n - j)]; fx[j:j + len(x)] += x * g
    try:
        if "--nomusic" in sys.argv: raise RuntimeError("ohne Musik (Sound wird in der YouTube-App gewaehlt)")
        import music_real
        cs = np.concatenate([[0.0], np.cumsum(np.abs(v), dtype=np.float64)]); idx = np.arange(n)
        lo, hi = np.clip(idx - 2400, 0, n), np.clip(idx + 2400, 0, n); vabs = ((cs[hi] - cs[lo]) / 4800).astype(np.float32)
        # Teil 1 (Crash, Spannung): "Hitman" ab 0:12 | Teil 2 (die 3 Regeln, Zuversicht): "Inspired" - beide Kevin MacLeod, CC BY 4.0
        A = music_real.rms_norm(music_real.dec("music/hitman.mp3")[12 * SR:], 0.017)
        B = music_real.rms_norm(music_real.dec("music/inspired.mp3"), 0.014)
        cut = int((SEGS[3]["t0"] - 0.35) * SR); xf = int(0.7 * SR); mus = np.zeros(n, np.float32)
        a_ = A[:cut + xf].copy(); a_[-xf:] *= np.linspace(1, 0, xf); a_[:SR // 20] *= np.linspace(0, 1, SR // 20); mus[:len(a_)] += a_[:n]
        b_ = B[:n - cut].copy(); b_[:xf] *= np.linspace(0, 1, xf); mus[cut:cut + len(b_)] += b_
        fo = int(1.0 * SR); mus[-fo:] *= np.linspace(1, 0, fo)
        mus = mus * (1 - 0.6 * np.clip(vabs / 0.05, 0, 1))
    except Exception as e: print("Musik aus:", e); mus = 0
    out = v * 1.05 + fx + mus; m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)]

if __name__ == "__main__":
    print(f"Laenge {TOTAL:.1f}s")
    if "--stills" in sys.argv:
        tiles = []
        for s in SEGS:
            for fr in (0.25, 0.75): tiles.append(frame(s["t0"] + (s["a1"] - s["a0"]) * fr).resize((270, 480)))
        sh = Image.new("RGB", (270 * 6, 480 * 3))
        for i, t_ in enumerate(tiles): sh.paste(t_, ((i % 6) * 270, (i // 6) * 480))
        sh.save("STORYBOARD.jpg", quality=85); print("ok"); sys.exit()
    out = av.open("ARC_Short04_MarketCrash_OHNE_MUSIK.mp4" if "--nomusic" in sys.argv else "ARC_Short04_MarketCrash.mp4", "w"); vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "19", "preset": "medium"}
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
