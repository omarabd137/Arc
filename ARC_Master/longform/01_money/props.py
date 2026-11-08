"""Requisiten fuer ARC v3 (auf 2x-Canvas, 1x-Koordinaten)."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../../shorts/01_lamborghini"))
from hq import *
from bill_kit import real_bill

def phone(c, cx, cy, h, title="MY BANK", line1="Balance", amount="$100", accent=(30, 70, 140), sub=None, glow=False):
    p = Pen(c); w = h * 0.5
    if glow: p.glow(cx, cy, h * 0.7, (140, 190, 255), 90)
    p.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, (28, 30, 36), 3.4, r=h * 0.07)
    p.rect(cx - w / 2 + 8, cy - h / 2 + 14, cx + w / 2 - 8, cy + h / 2 - 14, (246, 248, 252), 0, r=h * 0.05)
    p.rect(cx - w / 2 + 8, cy - h / 2 + 14, cx + w / 2 - 8, cy - h / 2 + h * 0.2, accent, 0, r=h * 0.05)
    p.text(title, cx, cy - h / 2 + h * 0.12, h * 0.055, SANS, (255, 255, 255))
    p.text(line1, cx, cy - h * 0.12, h * 0.045, SANSR, (110, 116, 128))
    p.text(amount, cx, cy, h * 0.11, BOLD, (30, 34, 44))
    if sub: p.text(sub, cx, cy + h * 0.13, h * 0.045, SANS, (40, 140, 80))
    for k in range(3): p.rect(cx - w * 0.36, cy + h * (0.22 + k * 0.07), cx + w * 0.36, cy + h * (0.26 + k * 0.07), (226, 230, 238), 0, r=6)
    p.rect(cx - w * 0.15, cy - h / 2 + 4, cx + w * 0.15, cy - h / 2 + 12, (10, 10, 12), 0, r=4)

def paycheck(c, cx, cy, w, name, amount="$60,000 / year"):
    p = Pen(c); h = w * 0.42; p.shadow(cx + 10, cy + h / 2, w * 0.5, 14, 60)
    p.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, (232, 242, 226), 3)
    for k in range(10): p.line([(cx - w / 2 + 6, cy - h / 2 + 10 + k * h / 10), (cx + w / 2 - 6, cy - h / 2 + 10 + k * h / 10)], 1, (214, 228, 208))
    p.text("ACME CORP.", cx - w / 2 + 24, cy - h / 2 + 30, h * 0.1, SERIF, (40, 80, 60), "lm")
    p.text("PAY TO THE ORDER OF", cx - w / 2 + 24, cy - h * 0.05, h * 0.07, SANSR, (80, 90, 80), "lm")
    p.text(name, cx - w * 0.1, cy - h * 0.05, h * 0.13, HAND, INK, "lm")
    p.line([(cx - w * 0.12, cy + h * 0.04), (cx + w * 0.42, cy + h * 0.04)], 1.6)
    p.rect(cx + w * 0.12, cy + h * 0.12, cx + w * 0.46, cy + h * 0.34, (250, 250, 246), 2)
    p.text(amount, cx + w * 0.29, cy + h * 0.23, h * 0.09, BOLD, (30, 100, 60))
    p.text("⁞ 021000021 ⁞ 4471 220 ⁞", cx - w / 2 + 24, cy + h * 0.38, h * 0.07, MONO, (60, 60, 60), "lm")

def document(c, cx, cy, w, h, title, sub=None, lines=12, seed=0, col=(252, 250, 244), angle=0, stamp=None, big=None):
    p = Pen(c); p.shadow(cx + 12, cy + h / 2, w * 0.5, 16, 60)
    p.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, col, 3)
    p.text(title, cx, cy - h / 2 + h * 0.1, min(h * 0.06, w * 0.055), SERIF, INK)
    if sub: p.text(sub, cx, cy - h / 2 + h * 0.17, min(h * 0.04, w * 0.035), SERIFR, (90, 90, 96))
    if big: p.text(big, cx, cy - h * 0.02, h * 0.12, BOLD, (40, 120, 70))
    import random as _r; r = _r.Random(seed)
    for k in range(lines):
        y = cy - h / 2 + h * (0.28 + k * 0.6 / lines); L = r.uniform(0.55, 0.85)
        if big and abs(y - cy) < h * 0.12: continue
        p.line([(cx - w * 0.4, y), (cx - w * 0.4 + w * 0.8 * L, y)], 3, (170, 170, 176))
    if stamp: p.rect(cx + w * 0.05, cy + h * 0.25, cx + w * 0.45, cy + h * 0.4, (255, 255, 255, 0), 4, outline=(200, 40, 44)); p.text(stamp, cx + w * 0.25, cy + h * 0.325, h * 0.05, BOLD, (200, 40, 44))

def credit_card(c, cx, cy, w, col=(30, 40, 70), label="PLATINUM", angle=0):
    p = Pen(c); h = w * 0.63; p.shadow(cx + 8, cy + h / 2, w * 0.5, 10, 60)
    p.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, col, 3, r=w * 0.06)
    p.poly([(cx - w / 2 + 10, cy + h / 2 - 10), (cx + w * 0.1, cy - h / 2 + 10), (cx + w * 0.3, cy - h / 2 + 10), (cx - w * 0.2, cy + h / 2 - 10)], lt(col, 0.12) + (120,), 0)
    p.rect(cx - w * 0.38, cy - h * 0.12, cx - w * 0.2, cy + h * 0.08, (214, 186, 110), 2, r=6)
    p.text("4532  ••••  ••••  2187", cx - w * 0.4, cy + h * 0.25, h * 0.11, MONO, (230, 230, 236), "lm")
    p.text(label, cx + w * 0.4, cy - h * 0.32, h * 0.1, SANS, (230, 230, 236), "rm")

def laptop(c, cx, base, w, screen_fn=None):
    p = Pen(c); h = w * 0.62
    p.rect(cx - w / 2, base - h, cx + w / 2, base - 8, (50, 52, 58), 3.4, r=12)
    p.rect(cx - w / 2 + 14, base - h + 14, cx + w / 2 - 14, base - 22, (246, 248, 252), 0)
    if screen_fn: screen_fn(p, cx - w / 2 + 14, base - h + 14, cx + w / 2 - 14, base - 22)
    p.poly([(cx - w * 0.6, base - 8), (cx + w * 0.6, base - 8), (cx + w * 0.66, base + 14), (cx - w * 0.66, base + 14)], (170, 172, 180), 3)

def invest_screen(p, x0, y0, x1, y1, amount="$500 / month"):
    p.rect(x0, y0, x1, y0 + (y1 - y0) * 0.18, (40, 120, 80), 0); p.text("AUTO-INVEST", (x0 + x1) / 2, y0 + (y1 - y0) * 0.09, (y1 - y0) * 0.08, SANS, (255, 255, 255))
    p.text(amount, (x0 + x1) / 2, y0 + (y1 - y0) * 0.42, (y1 - y0) * 0.12, BOLD, (30, 34, 44))
    p.text("→ S&P 500 INDEX FUND", (x0 + x1) / 2, y0 + (y1 - y0) * 0.6, (y1 - y0) * 0.065, SANS, (90, 96, 110))
    p.rect((x0 + x1) / 2 - (x1 - x0) * 0.22, y0 + (y1 - y0) * 0.72, (x0 + x1) / 2 + (x1 - x0) * 0.22, y0 + (y1 - y0) * 0.88, (40, 120, 80), 0, r=12)
    p.text("CONFIRM", (x0 + x1) / 2, y0 + (y1 - y0) * 0.8, (y1 - y0) * 0.065, SANS, (255, 255, 255))

def coin(c, cx, cy, r, side="HEADS"):
    p = Pen(c); p.ell(cx, cy, r, r, (226, 186, 80), 3.4); p.ell(cx, cy, r * 0.8, r * 0.8, (240, 206, 110), 2); p.text(side, cx, cy, r * 0.28, BOLD, (150, 110, 40))

def gold_bar(c, x, y, w=160):
    p = Pen(c); h = w * 0.35
    p.poly([(x, y), (x + w, y), (x + w * 0.85, y - h), (x + w * 0.15, y - h)], (232, 190, 70), 3); p.poly([(x + w * 0.15, y - h), (x + w * 0.85, y - h), (x + w * 0.8, y - h * 1.2), (x + w * 0.2, y - h * 1.2)], (250, 220, 120), 2.4)

def cash_stack(c, cx, base, n=6, w=220):
    for k in range(n): real_bill(c, cx + (k % 2) * 6, base - k * 14, w, value="100")

def basket(c, cx, base, full=1.0, w=300):
    p = Pen(c); import random as _r; r = _r.Random(4)
    items = [((220, 60, 50), "ell"), ((250, 200, 60), "rect"), ((90, 170, 90), "ell"), ((240, 140, 60), "rect"), ((200, 200, 210), "rect"), ((150, 90, 60), "ell"), ((60, 140, 200), "rect"), ((250, 240, 230), "rect")]
    n = int(len(items) * full)
    for i, (col, kind) in enumerate(items[:n]):
        x = cx - w * 0.35 + (i % 4) * w * 0.22; y = base - w * 0.36 - (i // 4) * w * 0.16
        if kind == "ell": p.ell(x, y, w * 0.08, w * 0.08, col, 2.6)
        else: p.rect(x - w * 0.07, y - w * 0.12, x + w * 0.07, y + w * 0.05, col, 2.6)
    p.poly([(cx - w / 2, base - w * 0.32), (cx + w / 2, base - w * 0.32), (cx + w * 0.42, base), (cx - w * 0.42, base)], (196, 150, 90), 3.2)
    for k in range(5): p.line([(cx - w * 0.4 + k * w * 0.2, base - w * 0.3), (cx - w * 0.34 + k * w * 0.17, base - 4)], 2, (160, 116, 66))
    p.arc(cx, base - w * 0.32, w * 0.42, w * 0.32, 180, 360, 5)

def tv_set(c, cx, cy, w, inner=None):
    p = Pen(c); h = w * 0.78
    p.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, (120, 84, 54), 4, r=24)
    p.rect(cx - w * 0.42, cy - h * 0.4, cx + w * 0.2, cy + h * 0.38, (40, 44, 40), 3, r=30)
    if inner: inner(p, cx - w * 0.42 + 14, cy - h * 0.4 + 14, cx + w * 0.2 - 14, cy + h * 0.38 - 14)
    for k in range(2): p.ell(cx + w * 0.32, cy - h * 0.2 + k * h * 0.2, w * 0.045, w * 0.045, (200, 190, 170), 2.6)
    for x in (cx - w * 0.35, cx + w * 0.35): p.line([(x, cy + h / 2), (x - (cx - x) * 0.1, cy + h / 2 + 40)], 5)

def tv_camera(c, x, base):
    p = Pen(c); p.line([(x, base - 260), (x - 80, base)], 5); p.line([(x, base - 260), (x + 80, base)], 5); p.line([(x, base - 260), (x, base)], 5)
    p.rect(x - 120, base - 380, x + 90, base - 250, (60, 62, 70), 3.4, r=10); p.rect(x + 90, base - 350, x + 160, base - 280, (40, 42, 48), 3)
    p.ell(x + 170, base - 315, 30, 40, (30, 30, 34), 3); p.rect(x - 100, base - 420, x - 20, base - 380, (60, 62, 70), 3)

def price_tag(c, cx, cy, txt, col=(250, 250, 246), tc=INK, size=40):
    p = Pen(c); w = len(txt) * size * 0.62 + 50; h = size * 1.6
    p.poly([(cx - w / 2, cy - h / 2), (cx + w / 2 - 30, cy - h / 2), (cx + w / 2, cy), (cx + w / 2 - 30, cy + h / 2), (cx - w / 2, cy + h / 2)], col, 3)
    p.ell(cx + w / 2 - 34, cy, 7, 7, (200, 200, 200), 2); p.text(txt, cx - 14, cy, size, BOLD, tc)

def hand(c, x, y, sleeve=(196, 62, 54), skin=(242, 206, 172), from_side="top", length=420):
    """Arm + Hand, die von einer Bildkante hereinkommt (fuer Nahaufnahmen am Tisch)."""
    p = Pen(c)
    if from_side == "top": a, b = (x, y - length), (x, y)
    elif from_side == "left": a, b = (x - length, y + 40), (x, y)
    else: a, b = (x + length, y + 40), (x, y)
    p.line([a, b], 96, INK); p.line([a, b], 88, sleeve)
    p.ell(b[0], b[1], 58, 50, skin, 3.4)
    dx = 1 if from_side == "left" else (-1 if from_side == "right" else 0)
    for k in range(3): p.line([(b[0] + dx * 30 - 20 + k * 18, b[1] + 30), (b[0] + dx * 44 - 20 + k * 18, b[1] + 62)], 22, INK); p.line([(b[0] + dx * 30 - 20 + k * 18, b[1] + 30), (b[0] + dx * 44 - 20 + k * 18, b[1] + 62)], 16, skin)

def bike(c, cx, base, w=240, col=(200, 60, 54)):
    p = Pen(c); r = w * 0.22
    for wx in (cx - w * 0.32, cx + w * 0.32):
        p.ell(wx, base - r, r, r, (0, 0, 0, 0), 5.5); p.ell(wx, base - r, r * 0.12, r * 0.12, (120, 122, 128), 2)
        for k in range(8): a = k * math.pi / 4; p.line([(wx, base - r), (wx + math.cos(a) * r * 0.92, base - r + math.sin(a) * r * 0.92)], 1.2, (140, 142, 148))
    pts = [(cx - w * 0.32, base - r), (cx - w * 0.05, base - r * 2.3), (cx + w * 0.22, base - r * 2.3), (cx + w * 0.32, base - r), (cx + w * 0.02, base - r)]
    p.line([pts[0], pts[1], pts[2], pts[3]], 7, INK); p.line([pts[0], pts[1], pts[2], pts[3]], 5, col)
    p.line([pts[1], pts[4], pts[0]], 7, INK); p.line([pts[1], pts[4], pts[0]], 5, col); p.line([pts[4], pts[2]], 7, INK); p.line([pts[4], pts[2]], 5, col)
    p.line([(cx - w * 0.05, base - r * 2.3), (cx - w * 0.08, base - r * 2.6)], 5); p.rect(cx - w * 0.16, base - r * 2.72, cx + w * 0.0, base - r * 2.58, (40, 40, 44), 2, r=6)
    p.line([(cx + w * 0.22, base - r * 2.3), (cx + w * 0.2, base - r * 2.75), (cx + w * 0.3, base - r * 2.8)], 5)
    p.ell(cx + w * 0.02, base - r, r * 0.22, r * 0.22, (90, 90, 96), 2.4)
