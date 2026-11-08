"""Thumbnail #02 v2: EIN Motiv - extreme Nahaufnahme des KI-Roboter-Auges (Cartoon, Tusche), Lichtexplosion, 2-3 Woerter."""
import os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
from ai_kit import *
from PIL import ImageChops

TEXT1, TEXT2 = "IT FIGHTS", "BACK"
cx, cy = 980, 600
c = canvas((0, 0, 0, 255)); p = Pen(c); r = random.Random(7)
# --- Hintergrund: dunkelrot -> Explosion
p.vgrad(0, 0, W, H, (40, 4, 8), (16, 2, 4))
for k in range(64):                                    # Strahlen
    a0 = k / 64 * 2 * math.pi + r.uniform(-0.02, 0.02); da = r.uniform(0.018, 0.05); L = 1600
    col = [(255, 240, 200), (255, 150, 30), (235, 30, 30)][k % 3]
    p.poly([(cx, cy), (cx + L * math.cos(a0), cy + L * math.sin(a0)), (cx + L * math.cos(a0 + da), cy + L * math.sin(a0 + da))], col, 0)
p.glow(cx, cy, 600, (255, 200, 120), 230); p.glow(cx, cy, 520, (255, 255, 245), 255)
for k in range(46):                                    # schwarze Speedlines
    a = r.uniform(0, 2 * math.pi); r0 = r.uniform(430, 620); r1 = r0 + r.uniform(120, 420)
    p.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))], r.uniform(3, 9), INK if k % 4 else (230, 40, 40))
# --- Roboterkopf-Gehaeuse um das Auge (Cartoon, Tusche)
p.ell(cx, cy, 420, 400, (214, 218, 228), 9)
p.ell(cx, cy, 395, 375, (236, 238, 244), 0)
p.arc(cx, cy, 395, 375, 200, 320, 14, (255, 255, 255))
for k in range(8):                                     # Schrauben
    a = k / 8 * 2 * math.pi + 0.3; p.ell(cx + 360 * math.cos(a), cy + 342 * math.sin(a), 16, 16, (150, 156, 170), 4)
p.ell(cx, cy, 330, 320, (40, 44, 58), 8)               # dunkler Ring
p.ell(cx, cy, 300, 292, (20, 22, 32), 0)
# --- Linse: rot -> orange -> gelb
for k in range(60):
    t = k / 59; rad = 290 * (1 - t * 0.98)
    p.ell(cx, cy, rad, rad * 0.97, mix((225, 20, 20), (255, 245, 160), t ** 0.6), 0)
p.glow(cx, cy, 230, (255, 200, 90), 200)
# Schaltkreis-Iris
for k in range(56):
    a = k / 56 * 2 * math.pi; r0 = 70 + (k % 3) * 8; r1 = r.uniform(190, 280)
    pts = [(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + (r0 + r1) / 2 * math.cos(a), cy + (r0 + r1) / 2 * math.sin(a)),
           (cx + r1 * math.cos(a + (0.05 if k % 2 else -0.05)), cy + r1 * math.sin(a + (0.05 if k % 2 else -0.05)))]
    p.line(pts, 4 if k % 4 else 7, (120, 20, 14)); p.ell(pts[-1][0], pts[-1][1], 6, 6, (120, 20, 14), 0)
p.arc(cx, cy, 290, 282, 0, 360, 9, INK)               # Linsenkontur
p.glow(cx, cy, 170, (255, 235, 140), 170)
# Pupille: senkrechter Schlitz
p.ell(cx, cy, 82, 150, INK, 0); p.ell(cx, cy, 30, 118, (210, 20, 30), 0); p.ell(cx, cy, 12, 96, (255, 90, 70), 0)
# Glanzlicht
p.ell(cx - 150, cy - 160, 80, 44, (255, 255, 255, 235), 0); p.ell(cx - 80, cy - 205, 22, 14, (255, 255, 255, 220), 0)
im = c.convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
# leichte Farbverschiebung (Glitch) am Rand
rch, g, b, a = im.split(); rch = ImageChops.offset(rch, 6, 0); bch = ImageChops.offset(b, -6, 0)
im = Image.merge("RGBA", (rch, g, bch, a))
d = ImageDraw.Draw(im)
def big(s, x, y, size, col, stroke=16):
    d.text((x + 8, y + 10), s, font=ImageFont.truetype(BOLD, size), fill=(0, 0, 0, 160), anchor="mm")
    d.text((x, y), s, font=ImageFont.truetype(BOLD, size), fill=col, anchor="mm", stroke_width=stroke, stroke_fill=(0, 0, 0))
big(TEXT1, 960, 120, 190, (255, 255, 255)); big(TEXT2, 1560, 960, 190, (255, 60, 60))
im = im.convert("RGB"); im.save("THUMB_v2_1920.png"); im.resize((1280, 720), Image.LANCZOS).save("THUMB_v2.jpg", quality=93)
im.resize((360, 202), Image.LANCZOS).save("THUMB_v2_small.png"); print("ok")
