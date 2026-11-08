"""ARC HQ-Kit: gleicher Cartoon-Stil (grosse Koepfe, Punkt-Augen, Tusche-Kontur), aber hochwertiger:
Kleidung statt Strich-Arme, Schuhe, Haende, weiche Schatten, Licht-Verlaeufe, Texturen, detailreiche Orte.
Alles in 1x-Koordinaten (1920x1080), intern 2x gezeichnet (SS)."""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
W, H, SS = 1920, 1080, 2
INK = (34, 30, 36)
F = "C:/Windows/Fonts/"
BOLD = F + "ariblk.ttf"; SANS = F + "arialbd.ttf"; SANSR = F + "arial.ttf"; SERIF = F + "georgiab.ttf"; SERIFR = F + "georgia.ttf"
HAND = F + "segoepr.ttf"; MONO = F + "consolab.ttf"

def mix(a, b, k): return tuple(int(x + (y - x) * k) for x, y in zip(a, b))
def dk(c, k=0.8): return tuple(int(v * k) for v in c[:3])
def lt(c, k=0.25): return tuple(int(v + (255 - v) * k) for v in c[:3])

class Pen:
    """Zeichnet in 1x-Koordinaten auf ein 2x-Bild."""
    def __init__(self, img): self.img = img; self.d = ImageDraw.Draw(img, "RGBA")
    def P(self, pts): return [(x * SS, y * SS) for x, y in pts]
    def B(self, x0, y0, x1, y1): return [min(x0, x1) * SS, min(y0, y1) * SS, max(x0, x1) * SS, max(y0, y1) * SS]
    def poly(self, pts, fill, lw=3.0, outline=INK):
        self.d.polygon(self.P(pts), fill=fill)
        if lw: self.d.line(self.P(pts + [pts[0]]), fill=outline, width=int(lw * SS), joint="curve")
    def rect(self, x0, y0, x1, y1, fill, lw=3.0, r=0, outline=INK):
        if r: self.d.rounded_rectangle(self.B(x0, y0, x1, y1), int(r * SS), fill=fill, outline=outline if lw else None, width=int(lw * SS))
        else: self.d.rectangle(self.B(x0, y0, x1, y1), fill=fill, outline=outline if lw else None, width=int(lw * SS))
    def ell(self, cx, cy, rx, ry, fill, lw=3.0, outline=INK):
        self.d.ellipse(self.B(cx - rx, cy - ry, cx + rx, cy + ry), fill=fill, outline=outline if lw else None, width=int(lw * SS))
    def line(self, pts, w=3.0, col=INK): self.d.line(self.P(pts), fill=col, width=max(1, int(w * SS)), joint="curve")
    def arc(self, cx, cy, rx, ry, a0, a1, w=3.0, col=INK): self.d.arc(self.B(cx - rx, cy - ry, cx + rx, cy + ry), a0, a1, fill=col, width=int(w * SS))
    def text(self, s, x, y, size, font=SANS, fill=INK, anchor="mm", stroke=0, sfill=INK):
        f = ImageFont.truetype(font, int(size * SS)); self.d.text((x * SS, y * SS), s, font=f, fill=fill, anchor=anchor, stroke_width=int(stroke * SS), stroke_fill=sfill)
    def vgrad(self, x0, y0, x1, y1, top, bot):
        for y in range(int(y0 * SS), int(y1 * SS)):
            k = (y - y0 * SS) / max(1, (y1 - y0) * SS); self.d.line([(x0 * SS, y), (x1 * SS, y)], fill=mix(top, bot, k))
    def glow(self, cx, cy, r, col, a=90):
        lay = Image.new("RGBA", self.img.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse(self.B(cx - r, cy - r, cx + r, cy + r), fill=col + (a,))
        lay = lay.filter(ImageFilter.GaussianBlur(r * SS * 0.45)); self.img.alpha_composite(lay) if self.img.mode == "RGBA" else self.img.paste(lay, (0, 0), lay)
        self.d = ImageDraw.Draw(self.img, "RGBA")
    def shadow(self, cx, cy, rx, ry, a=70):
        lay = Image.new("RGBA", self.img.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse(self.B(cx - rx, cy - ry, cx + rx, cy + ry), fill=(0, 0, 0, a))
        lay = lay.filter(ImageFilter.GaussianBlur(ry * SS * 0.6))
        if self.img.mode == "RGBA": self.img.alpha_composite(lay)
        else: self.img.paste(lay, (0, 0), lay)
        self.d = ImageDraw.Draw(self.img, "RGBA")

def canvas(col=(0, 0, 0, 0)): return Image.new("RGBA", (W * SS, H * SS), col)

_GRAIN = None
def finish(img2x):
    """2x -> 1x, leichte Papierkoernung + sanfte Vignette = hochwertiger Look."""
    global _GRAIN
    im = img2x.convert("RGB").resize((W, H), Image.LANCZOS)
    if _GRAIN is None:
        rnd = random.Random(5); g = Image.effect_noise((W, H), 18).convert("L")
        v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-300, -260, W + 300, H + 260], fill=255); v = v.filter(ImageFilter.GaussianBlur(220))
        _GRAIN = (g, v)
    g, v = _GRAIN
    im = Image.blend(im, Image.merge("RGB", (g, g, g)), 0.035)
    im = Image.composite(im, Image.blend(im, Image.new("RGB", (W, H), (20, 16, 24)), 0.35), v)
    return im

# ======================= FIGUREN =======================
def P(**k):
    base = dict(hair=(90, 60, 40), hair_hi=None, top=(200, 70, 60), pants=(60, 74, 110), shoes=(240, 240, 236), skin=(240, 204, 170),
                tie=None, glasses=False, beard=False, style="short", age=25, jacket=None, hood=False, big=1.0, wig=False, collar=True)
    base.update(k); base["hair_hi"] = base["hair_hi"] or lt(base["hair"], 0.3); return base

JAKE = P(hair=(122, 82, 50), top=(196, 62, 54), pants=(62, 82, 124), shoes=(236, 236, 232), skin=(242, 206, 172), style="messy", hood=True)
JAKE45 = P(hair=(104, 74, 52), top=(140, 62, 58), pants=(70, 76, 96), shoes=(120, 100, 84), skin=(236, 198, 164), style="messy", age=45, beard=True, big=1.08, hood=True)
RYAN = P(hair=(28, 24, 22), top=(160, 196, 228), pants=(70, 62, 54), shoes=(110, 70, 44), skin=(150, 100, 70), style="buzz")
RYAN45 = P(hair=(46, 42, 40), top=(236, 236, 240), jacket=(48, 66, 100), pants=(58, 62, 74), shoes=(80, 50, 34), skin=(146, 98, 68), style="buzz", age=45, beard=True)
KID_J = P(hair=(130, 88, 52), top=(196, 62, 54), pants=(62, 82, 124), skin=(244, 210, 178), style="messy", age=10, big=0.85)
KID_R = P(hair=(28, 24, 22), top=(250, 196, 70), pants=(70, 62, 54), shoes=(220, 80, 60), skin=(154, 104, 72), style="buzz", age=10, big=0.85)
TELLER = P(hair=(150, 90, 50), top=(250, 250, 248), jacket=(36, 60, 96), pants=(36, 60, 96), shoes=(40, 36, 36), tie=(170, 40, 44), skin=(240, 206, 176), style="bun")
BANKER = P(hair=(80, 70, 66), top=(250, 250, 248), jacket=(46, 50, 62), pants=(46, 50, 62), shoes=(30, 28, 28), tie=(150, 40, 44), skin=(236, 200, 166), glasses=True, style="side", age=50)
BOSS = P(hair=(150, 150, 154), top=(250, 250, 248), jacket=(80, 60, 50), pants=(80, 60, 50), shoes=(40, 30, 26), tie=(40, 80, 140), skin=(236, 200, 166), style="bald", age=55, big=1.15)
BILLIONAIRE = P(hair=(210, 210, 214), top=(250, 250, 248), jacket=(24, 26, 34), pants=(24, 26, 34), shoes=(20, 18, 18), tie=(24, 26, 34), skin=(236, 202, 172), style="side", age=60)
STRANGER = P(hair=(60, 44, 36), top=(110, 130, 90), pants=(60, 56, 52), skin=(220, 176, 136), style="short")
NIXON = P(hair=(54, 44, 40), top=(250, 250, 248), jacket=(40, 42, 50), pants=(40, 42, 50), shoes=(20, 18, 18), tie=(40, 50, 90), skin=(232, 196, 164), style="nixon", age=58, big=1.05)
CANTILLON = P(hair=(240, 240, 236), top=(120, 40, 50), jacket=(120, 40, 50), pants=(60, 40, 40), shoes=(40, 30, 26), skin=(240, 210, 182), style="wig", age=50, wig=True)
CROWD = [P(hair=h, top=t, pants=pa, skin=sk, style=st) for h, t, pa, sk, st in [
    ((60, 44, 36), (110, 130, 170), (60, 60, 70), (236, 196, 160), "short"), ((30, 26, 24), (180, 120, 100), (50, 50, 60), (170, 120, 86), "buzz"),
    ((200, 160, 90), (120, 160, 120), (80, 70, 60), (242, 208, 178), "bun"), ((90, 60, 40), (170, 150, 110), (60, 70, 90), (220, 176, 136), "messy"),
    ((40, 34, 30), (130, 110, 160), (50, 50, 56), (176, 126, 92), "side")]]

STYLE = dict(nose=True, hair_hi=True, foot_cap=True, brow_len=1.0)   # Short-Look: einzelne Details abschaltbar
def _limb(p, pts, col, w, ink=INK):
    """Gliedmasse als gefuellte, abgerundete Roehre mit Kontur (Kleidung)."""
    p.line(pts, w + 4.5, ink); p.line(pts, w, col)
    for (x, y) in ((pts[0], pts[-1]) if STYLE["foot_cap"] else (pts[0],)): p.ell(x, y, w / 2, w / 2, col, 0)

def figure(img, cx, base, R, pr, face=1, mouth="line", brow=0.0, arms=("down", "down"), legs="stand", phase=0.0, eyes="open", hold=None, seated=False):
    """Figur auf Fusslinie base, Kopf-Radius R. face = 1 schaut nach rechts, -1 links, 0 frontal.
    arms je Seite: down, hip, point, wave, up, hold, desk, cross, chin, phone, shrug. legs: stand, walk(phase), sit, push(=gehen + Rad schieben)."""
    p = Pen(img); s = pr["big"]; kid = pr["age"] < 16
    leg = R * (1.55 if not kid else 1.25); tor_h = R * (1.55 if not kid else 1.25); tor_w = R * 1.15 * s
    hip = base - leg if not seated else base - R * 0.55
    tor_top = hip - tor_h; head_cy = tor_top - R * 0.82
    top = pr["jacket"] or pr["top"]
    if not seated: p.shadow(cx, base + 4, R * 1.0, R * 0.16, 60)
    # --- Beine (Hose + Schuhe)
    lw_ = R * 0.36
    for sx in (-1, 1):
        x0 = cx + sx * tor_w * 0.24
        if seated:
            knee = (x0 + face * R * 0.85, hip + R * 0.05); foot = (knee[0] + face * R * 0.1, base)
            _limb(p, [(x0, hip - 6), knee, foot], pr["pants"], lw_)
            fx, fy = foot
        elif legs in ("walk", "push"):
            ph = 2 * math.pi * (phase + (0.5 if sx > 0 else 0)); sw = math.sin(ph)
            fx = x0 + face * sw * R * 0.55; lift = max(0, math.cos(ph)) * R * 0.18; fy = base - lift
            knee = ((x0 + fx) / 2 + face * R * 0.12, hip + leg * 0.5 - lift * 0.4)
            _limb(p, [(x0, hip - 6), knee, (fx, fy - R * 0.08)], pr["pants"], lw_)
        else:
            fx, fy = x0 + sx * R * 0.04, base
            _limb(p, [(x0, hip - 6), (fx, fy - R * 0.08)], pr["pants"], lw_)
        fd = face if face else sx
        p.poly([(fx - R * 0.16 * (1 if fd > 0 else 1.9), fy - R * 0.2), (fx + R * 0.1, fy - R * 0.22), (fx + fd * R * 0.42, fy - R * 0.06),
                (fx + fd * R * 0.42, fy + 2), (fx - fd * R * 0.2, fy + 2)], pr["shoes"], 2.6)
    # --- Arme hinter/neben Koerper
    hands = []
    def arm(sx, kind):
        sh_ = (cx + sx * tor_w * 0.48, tor_top + R * 0.28); L = R * 1.0
        k = {"down": [(sx * 0.22, 0.6), (sx * 0.16, 1.18)], "hip": [(sx * 0.55, 0.5), (sx * 0.12, 0.95)],
             "point": [(sx * 0.75, -0.05), (sx * 1.45, -0.2)], "wave": [(sx * 0.6, -0.35), (sx * 0.7, -1.0)],
             "up": [(sx * 0.25, -0.6), (sx * 0.3, -1.25)], "hold": [(sx * 0.35, 0.55), (sx * 0.85, 0.45)],
             "desk": [(sx * 0.35, 0.6), (-sx * 0.1 + face * 0.7, 0.72)], "cross": [(sx * 0.3, 0.55), (-sx * 0.35, 0.45)],
             "chin": [(sx * 0.35, 0.6), (sx * 0.05 + face * 0.25, -0.35)], "phone": [(sx * 0.45, 0.45), (sx * 0.25 + face * 0.4, 0.05)],
             "shrug": [(sx * 0.75, 0.05), (sx * 1.05, -0.35)], "push": [(face * 0.55, 0.45), (face * 1.05, 0.4)],
             "give": [(face * 0.6, 0.35), (face * 1.25, 0.2)]}[kind]
        pts = [sh_] + [(sh_[0] + dx * L, sh_[1] + dy * L) for dx, dy in k]
        _limb(p, pts, top, R * 0.3); hx, hy = pts[-1]; hands.append((hx, hy))
    back = 1 if face <= 0 else -1
    arm(back, arms[0] if back < 0 else arms[1])
    # --- Oberkoerper (Pullover/Hemd/Jacke) mit Licht und Schatten
    tw = tor_w * 0.5
    body = [(cx - tw * 0.92, tor_top + R * 0.15), (cx - tw, hip - 4), (cx + tw, hip - 4), (cx + tw * 0.92, tor_top + R * 0.15),
            (cx + tw * 0.55, tor_top), (cx - tw * 0.55, tor_top)]
    p.poly(body, top, 3.2)
    p.poly([(cx + face * tw * 0.2 if face else cx + tw * 0.3, tor_top + 4), (cx + (tw * 0.92 if face >= 0 else -tw * 0.92), tor_top + R * 0.15),
            (cx + (tw if face >= 0 else -tw), hip - 6), (cx + face * tw * 0.35 if face else cx + tw * 0.45, hip - 6)], dk(top, 0.86) + (150,), 0)
    if pr["jacket"]:
        p.poly([(cx - tw * 0.3, tor_top + 2), (cx + tw * 0.3, tor_top + 2), (cx, tor_top + R * 0.9)], pr["top"], 2.4)
        if pr["tie"]: p.poly([(cx - R * 0.07, tor_top + R * 0.12), (cx + R * 0.07, tor_top + R * 0.12), (cx + R * 0.1, tor_top + R * 0.8), (cx, tor_top + R * 0.95), (cx - R * 0.1, tor_top + R * 0.8)], pr["tie"], 2)
        p.line([(cx, tor_top + R * 0.9), (cx, hip - 6)], 2.4); p.ell(cx + R * 0.04, tor_top + R * 1.1, 2.6, 2.6, INK, 0)
    elif pr["hood"]:
        p.arc(cx, tor_top + 2, tw * 0.6, R * 0.3, 0, 180, 3.0); p.line([(cx - R * 0.1, tor_top + R * 0.25), (cx - R * 0.12, tor_top + R * 0.6)], 2)
        p.line([(cx + R * 0.1, tor_top + R * 0.25), (cx + R * 0.12, tor_top + R * 0.6)], 2)
        p.rect(cx - tw * 0.45, hip - R * 0.5, cx + tw * 0.45, hip - R * 0.2, dk(top, 0.9), 2, r=6)
    elif pr["collar"]:
        p.poly([(cx - R * 0.26, tor_top + 2), (cx, tor_top + R * 0.3), (cx + R * 0.26, tor_top + 2)], lt(pr["top"], 0.2), 2.4)
        for k in range(3): p.ell(cx, tor_top + R * (0.5 + k * 0.28), 2.4, 2.4, INK, 0)
    # --- Hals + Kopf
    p.rect(cx - R * 0.17, tor_top - R * 0.22, cx + R * 0.17, tor_top + 4, dk(pr["skin"], 0.92), 2.4)
    hr = R
    if pr["style"] in ("wig",): p.ell(cx - face * R * 0.15, head_cy + R * 0.2, R * 1.08, R * 1.1, pr["hair"], 3)
    if pr["style"] == "bun": p.ell(cx - face * R * 0.75, head_cy - R * 0.55, R * 0.36, R * 0.34, pr["hair"], 3)
    p.ell(cx, head_cy, hr, hr * 1.02, pr["skin"], 3.4)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)          # Mondsichel-Schatten
    dl.ellipse(p.B(cx - hr, head_cy - hr, cx + hr, head_cy + hr), fill=dk(pr["skin"], 0.86) + (255,))
    off = -(face if face else 1) * hr * 0.32; dl.ellipse(p.B(cx - hr + off, head_cy - hr - 4, cx + hr + off, head_cy + hr + 2), fill=(0, 0, 0, 0))
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).ellipse(p.B(cx - hr + 3, head_cy - hr + 3, cx + hr - 3, head_cy + hr - 3), fill=255)
    lay.putalpha(ImageChops.multiply(lay.getchannel("A"), m)); img.alpha_composite(lay); p = Pen(img)
    ex, ey = cx + face * hr * 0.26, head_cy + hr * 0.06
    # Ohr
    if face: p.ell(cx - face * hr * 0.72, head_cy + hr * 0.12, hr * 0.13, hr * 0.2, dk(pr["skin"], 0.93), 2.4)
    # Haare je Stil: Haarmasse mit natuerlichem Haaransatz (Stirn-Bogen), hinten tiefer als vorne
    hc, hh = pr["hair"], pr["hair_hi"]; st = pr["style"]; fdir = face if face else 1
    def hairmass(front_y=-0.5, back_y=0.15, bulk=1.07, part=0.15):
        top = [(cx + math.cos(math.radians(t)) * hr * bulk, head_cy + math.sin(math.radians(t)) * hr * bulk * 1.0) for t in range(180, 361, 6)]
        if fdir > 0: top = top                                   # links = hinten, rechts = vorne (Blick nach rechts)
        back_x, front_x = cx - fdir * hr * 1.0, cx + fdir * hr * 0.98
        line_ = [(front_x, head_cy - hr * 0.12), (cx + fdir * hr * 0.75, head_cy + hr * front_y * 0.7), (cx + fdir * hr * part, head_cy + hr * front_y),
                 (cx - fdir * hr * 0.35, head_cy + hr * (front_y + 0.12)), (cx - fdir * hr * 0.8, head_cy + hr * back_y * 0.3), (back_x, head_cy + hr * back_y)]
        pts = top + line_ if fdir > 0 else list(reversed(top)) + line_
        p.poly(pts, hc, 3.2)
        if STYLE["hair_hi"]: p.arc(cx - fdir * hr * 0.15, head_cy - hr * 0.55, hr * 0.5, hr * 0.28, 200, 300, 3.0, hh)
    if st == "messy":
        hairmass(-0.42, 0.25, 1.09)
        for k in range(3):
            a_ = math.radians(215 + k * 38); x, y = cx + math.cos(a_) * hr * 1.0, head_cy + math.sin(a_) * hr * 1.02
            p.poly([(x - hr * 0.16, y + hr * 0.06), (x + math.cos(a_) * hr * 0.14 + fdir * hr * 0.08, y + math.sin(a_) * hr * 0.14), (x + hr * 0.16, y + hr * 0.06)], hc, 0)
        p.arc(cx, head_cy - hr * 0.2, hr * 0.7, hr * 0.6, 230, 300, 2.2, dk(hc, 0.75))
        if face: p.poly([(cx + fdir * hr * 0.05, head_cy - hr * 0.62), (cx + fdir * hr * 0.62, head_cy - hr * 0.6), (cx + fdir * hr * 0.55, head_cy - hr * 0.28), (cx + fdir * hr * 0.25, head_cy - hr * 0.42)], hc, 2.6)
    elif st == "buzz":
        hairmass(-0.62, 0.0, 1.03, 0.2)
    elif st == "bun":
        hairmass(-0.5, 0.35, 1.07)
    elif st == "side":
        hairmass(-0.5, 0.2, 1.06, -0.1); p.line([(cx - fdir * hr * 0.1, head_cy - hr * 1.0), (cx - fdir * hr * 0.05, head_cy - hr * 0.6)], 2.4, dk(hc, 0.7))
    elif st == "short":
        hairmass(-0.5, 0.2, 1.05)
    elif st == "shaved":   # glatt rasierter Kopf mit Glanzlicht (z. B. Bezos)
        p.arc(cx - fdir * hr * 0.3, head_cy - hr * 0.55, hr * 0.32, hr * 0.2, 200, 300, 4.0, lt(pr["skin"], 0.55))
    elif st == "bald":
        for sx in (-1, 1): p.poly([(cx + sx * hr * 0.99, head_cy - hr * 0.05), (cx + sx * hr * 0.8, head_cy - hr * 0.5), (cx + sx * hr * 0.93, head_cy + hr * 0.3)], hc, 2.4)
    elif st == "nixon":
        hairmass(-0.68, 0.2, 1.06, 0.45)
        p.arc(cx + fdir * hr * 0.25, head_cy - hr * 0.7, hr * 0.3, hr * 0.15, 180, 330, 2.2, hh)
    elif st == "wig":
        hairmass(-0.72, 0.0, 1.06)
        for sx in (-1, 1):
            for j in range(2): p.ell(cx + sx * hr * 1.0, head_cy + hr * (0.05 + j * 0.3), hr * 0.22, hr * 0.16, hc, 2.4)
    if pr["age"] >= 40 and st not in ("bald", "wig"): p.arc(cx - fdir * hr * 0.72, head_cy + hr * 0.02, hr * 0.12, hr * 0.18, 90, 270, 2.2, lt(hc, 0.6))
    # Gesicht
    if pr["beard"]:   # kurzer Bart / Stoppeln nur am Kiefer, unter dem Mund
        p.d.chord(p.B(cx - hr * 0.86, head_cy - hr * 0.2, cx + hr * 0.86, head_cy + hr * 1.0), 25, 155, fill=pr["hair"] + (95,))
    for k in (-1, 1):
        gx = ex + k * hr * 0.27
        if eyes == "closed": p.arc(gx, ey, hr * 0.08, hr * 0.05, 0, 180, 3.2)
        elif eyes == "happy": p.arc(gx, ey + hr * 0.04, hr * 0.08, hr * 0.07, 180, 360, 3.2)
        elif eyes == "wide": p.ell(gx, ey, hr * 0.085, hr * 0.11, (255, 255, 255), 2.4); p.ell(gx + face * hr * 0.02, ey, hr * 0.04, hr * 0.05, INK, 0)
        else: p.ell(gx, ey, hr * 0.05, hr * 0.075, INK, 0); p.ell(gx + hr * 0.018, ey - hr * 0.025, hr * 0.015, hr * 0.015, (255, 255, 255), 0)
        bc = dk(pr["hair"], 0.85) if pr["hair"][0] < 200 else (170, 170, 176)
        bl = STYLE["brow_len"]
        if bl > 0: p.line([(gx - k * hr * 0.08 * bl, ey - hr * (0.22 - brow)), (gx + k * hr * 0.1 * bl, ey - hr * (0.25 + brow * 0.6))], 3.4, bc)
        if pr["glasses"]: p.rect(gx - hr * 0.17, ey - hr * 0.12, gx + hr * 0.17, ey + hr * 0.12, (220, 236, 244, 60), 2.4, r=5)
    if pr["glasses"]: p.line([(ex - hr * 0.1, ey - hr * 0.04), (ex + hr * 0.1, ey - hr * 0.04)], 2.4)
    nx = ex + face * hr * (0.12 if st != "nixon" else 0.2)
    if STYLE["nose"]: p.line([(ex + face * hr * 0.02, ey + hr * 0.08), (nx + face * hr * 0.06, ey + hr * 0.3), (ex - face * hr * 0.02, ey + hr * 0.33)], 2.6, dk(pr["skin"], 0.6))
    if pr["age"] >= 40: p.arc(ex + face * hr * 0.3, ey + hr * 0.42, hr * 0.1, hr * 0.1, 90 if face > 0 else 0, 180 if face > 0 else 90, 2, dk(pr["skin"], 0.75))
    my = ey + hr * 0.5
    if mouth == "smile": p.arc(ex, my - hr * 0.08, hr * 0.17, hr * 0.12, 20, 160, 3.2)
    elif mouth == "grin":
        p.d.chord(p.B(ex - hr * 0.18, my - hr * 0.14, ex + hr * 0.18, my + hr * 0.12), 0, 180, fill=(255, 255, 255), outline=INK, width=int(2.6 * SS))
    elif mouth == "laugh":   # breites, offenes Lachen mit Zaehnen
        p.d.chord(p.B(ex - hr * 0.26, my - hr * 0.16, ex + hr * 0.26, my + hr * 0.24), 0, 180, fill=(110, 36, 40), outline=INK, width=int(2.6 * SS))
        p.d.chord(p.B(ex - hr * 0.22, my - hr * 0.12, ex + hr * 0.22, my + hr * 0.06), 0, 180, fill=(255, 255, 255))
    elif mouth == "frown": p.arc(ex, my + hr * 0.06, hr * 0.14, hr * 0.08, 200, 340, 3.2)
    elif mouth == "o": p.ell(ex, my, hr * 0.07, hr * 0.09, (120, 40, 44), 2.4)
    elif mouth == "talk": p.ell(ex, my, hr * 0.1, hr * 0.06, (120, 40, 44), 2.4)
    elif mouth == "worried": p.line([(ex - hr * 0.12, my + 2), (ex - hr * 0.04, my - 2), (ex + hr * 0.04, my + 2), (ex + hr * 0.12, my - 2)], 3)
    else: p.line([(ex - hr * 0.1, my), (ex + hr * 0.1, my)], 3.2)
    # vorderer Arm ueber dem Koerper
    arm(-back, arms[0] if -back < 0 else arms[1])
    for hx, hy in hands: p.ell(hx, hy, R * 0.16, R * 0.16, pr["skin"], 2.6)
    if hold: hold(img, hands[-1])
    return dict(head=(cx, head_cy, hr), hands=hands, eye=(ex, ey))

# ======================= SPRITE-CACHE + ZEICHNEN IN DEN FRAME =======================
_spr = {}
def sprite(key, fn, pad=0):
    if key not in _spr:
        c = canvas(); fn(c); bb = c.getbbox() or (0, 0, 2, 2)
        im = c.crop(bb).resize((max(1, (bb[2] - bb[0]) // SS), max(1, (bb[3] - bb[1]) // SS)), Image.LANCZOS)
        _spr[key] = (im, bb[0] / SS, bb[1] / SS)
    return _spr[key]
def put(frame, spr, dx=0, dy=0, alpha=1.0, scale=1.0, rot=0):
    im, x, y = spr
    if scale != 1.0 or rot:
        w0, h0 = im.size
        if scale != 1.0: im = im.resize((max(1, int(w0 * scale)), max(1, int(h0 * scale))), Image.BICUBIC)
        if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
        x, y = x + (w0 - im.width) / 2, y + (h0 - im.height) / 2
    if alpha < 1.0: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * max(0.0, alpha))))
    frame.paste(im, (int(round(x + dx)), int(round(y + dy))), im)

def fig(frame, pr, x, base, R, t=0.0, face=1, mouth="line", brow=0.0, arms=("down", "down"), legs="stand", walk=None, eyes=None,
        seated=False, idle=True, alpha=1.0, seed=0):
    """Figur in den Frame. walk = Laufzeit in s (nur bei echter Fortbewegung). Lebendig: atmen + blinzeln."""
    ph = None if walk is None else round((walk * 1.8) % 1 * 12) / 12
    if eyes is None: eyes = "closed" if idle and (t + seed * 0.71) % 4.1 < 0.12 else "open"
    key = ("fig", id(pr), R, face, mouth, brow, arms, "walk" if ph is not None else legs, ph, eyes, seated, base)
    spr = sprite(key, lambda c: figure(c, 960, base, R, pr, face, mouth, brow, arms, "walk" if ph is not None else legs, ph or 0.0, eyes, seated=seated))
    dy = -abs(math.sin(2 * math.pi * ph)) * R * 0.05 if ph is not None else (math.sin(t * 2.6 + seed) * R * 0.015 if idle else 0)
    put(frame, spr, x - 960, dy, alpha)

# ======================= TEXT-EINBLENDUNGEN (1x, direkt) =======================
def pop(k): k = max(0.0, min(1.0, k)); return 1 - (1 - k) ** 3 if k < 1 else 1.0
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def inout(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def label(frame, s, cx, cy, size, color=(255, 214, 60), k=1.0, stroke=7, font=BOLD):
    if k <= 0: return
    sc = 0.85 + 0.15 * ease(k / 0.5); a = ease(k / 0.25)
    lay = Image.new("RGBA", frame.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((cx, cy), s, font=ImageFont.truetype(font, max(8, int(size * sc))), fill=color + (255,), anchor="mm", stroke_width=stroke, stroke_fill=INK + (255,))
    if a < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(lay)

def bubble(frame, s, x, y, k=1.0, tail=(0, 60), size=40, w=None):
    """Sprechblase (weiss, Tusche) – x,y = Mitte, tail = Spitze relativ."""
    if k <= 0: return
    a = ease(k / 0.25); f = ImageFont.truetype(HAND, size); d0 = ImageDraw.Draw(frame)
    tw = d0.textlength(s, font=f); bw = (w or tw + 60) / 2; bh = size * 0.95
    lay = Image.new("RGBA", frame.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon([(x - 22, y + bh - 6), (x + 22, y + bh - 6), (x + tail[0], y + tail[1] + bh)], fill=(255, 255, 255, 255), outline=INK + (255,))
    d.rounded_rectangle([x - bw, y - bh, x + bw, y + bh], 30, fill=(255, 255, 255, 255), outline=INK + (255,), width=4)
    d.polygon([(x - 18, y + bh - 8), (x + 18, y + bh - 8), (x + tail[0] * 0.9, y + tail[1] * 0.9 + bh - 4)], fill=(255, 255, 255, 255))
    d.text((x, y + 2), s, font=f, fill=INK + (255,), anchor="mm")
    if a < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(lay)

def sticky(frame, s, x, y, k=1.0, angle=-3, size=40):
    if k <= 0: return
    f = ImageFont.truetype(HAND, size); w = int(ImageDraw.Draw(frame).textlength(s, font=f) + 60); h = size + 40
    n = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(n)
    d.rectangle([12, 14, w + 12, h + 14], fill=(0, 0, 0, 60)); d.rectangle([6, 6, w + 6, h + 6], fill=(252, 222, 110, 255), outline=INK + (255,), width=3)
    d.text((w / 2 + 6, h / 2 + 6), s, font=f, fill=INK + (255,), anchor="mm")
    n = n.rotate(angle, expand=True, resample=Image.BICUBIC); a = ease(k / 0.25)
    if a < 1: n.putalpha(n.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(n, (int(x - n.width / 2), int(y - n.height / 2)))
