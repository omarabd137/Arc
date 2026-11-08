"""Realistische Strichmaennchen fuer ARC-Shorts: echte Proportionen (Kopf ~1/6.5), Gelenke (Schulter/Ellbogen/Hand,
Huefte/Knie/Fuss), Haende + Schuhe, Gesicht mit Ausdruck, optionale Merkmale (Krawatte, Brille, Haare, Kappe).
Posen ueber Gelenkwinkel (Grad, 0 = nach unten, positiv = nach vorne/blickrichtung), interpolierbar."""
import math
from PIL import Image, ImageDraw

INK = (24, 22, 28)
def lerp(a, b, k): return a + (b - a) * k
POSES = {
    "stand":   dict(lean=0, sh=(8, -8), el=(10, 10), hip=(4, -4), kn=(0, 0)),
    "phone":   dict(lean=4, sh=(-5, 35), el=(0, 140), hip=(3, -3), kn=(0, 0)),           # rechte Hand haelt Handy vor dem Gesicht
    "point":   dict(lean=2, sh=(10, 95), el=(10, 5), hip=(4, -4), kn=(0, 0)),
    "press":   dict(lean=8, sh=(10, 70), el=(10, -20), hip=(4, -4), kn=(0, 0)),
    "hands_head": dict(lean=0, sh=(150, -150), el=(-120, 120), hip=(5, -5), kn=(0, 0)),
    "shrug":   dict(lean=0, sh=(35, -35), el=(-70, 70), hip=(4, -4), kn=(0, 0)),
    "cheer":   dict(lean=0, sh=(160, -160), el=(10, -10), hip=(8, -8), kn=(0, 0)),
    "drop":    dict(lean=10, sh=(-10, 60), el=(0, 30), hip=(4, -4), kn=(0, 0)),           # wirft etwas nach unten/vorne
    "throw":   dict(lean=-6, sh=(20, 170), el=(10, -20), hip=(10, -14), kn=(0, 10)),
    "sit":     dict(lean=0, sh=(10, 60), el=(10, 60), hip=(90, 90), kn=(-90, -90)),
    "walk1":   dict(lean=4, sh=(-25, 25), el=(15, 15), hip=(-22, 22), kn=(0, 25)),
    "walk2":   dict(lean=4, sh=(25, -25), el=(15, 15), hip=(22, -22), kn=(25, 0)),
}
def mix_pose(a, b, k):
    A, B = POSES[a] if isinstance(a, str) else a, POSES[b] if isinstance(b, str) else b
    return {key: (lerp(A[key], B[key], k) if not isinstance(A[key], tuple) else tuple(lerp(x, y, k) for x, y in zip(A[key], B[key]))) for key in A}

def stickman(d, x, foot_y, h, pose="stand", face=1, expr="neutral", tie=None, glasses=False, hair="short", cap=None, lw=None, skin=(255, 255, 255), look=0.0, scale_head=1.0):
    """d = ImageDraw (RGBA). x,foot_y = Fusspunkt, h = Koerperhoehe in px. face 1 = schaut rechts, -1 links."""
    P = POSES[pose] if isinstance(pose, str) else pose
    lw = lw or max(4, int(h * 0.028)); hr = h * 0.075 * scale_head
    leg = h * 0.47; thigh = leg * 0.5; shin = leg * 0.5
    torso = h * 0.30; upper = h * 0.17; fore = h * 0.16
    lean = math.radians(P["lean"] * face)
    hip = (x, foot_y - leg)
    neck = (hip[0] + math.sin(lean) * torso, hip[1] - math.cos(lean) * torso)
    head = (neck[0] + math.sin(lean) * hr * 1.15, neck[1] - math.cos(lean) * hr * 1.15)
    def seg(p, ang_deg, L):
        a = math.radians(ang_deg); return (p[0] + math.sin(a) * L * face, p[1] + math.cos(a) * L)
    line = lambda pts, w=lw: d.line(pts, fill=INK, width=int(w), joint="curve")
    # Beine (hinten zuerst)
    for i in (1, 0):
        k = seg(hip, P["hip"][i], thigh); f = seg(k, P["hip"][i] + P["kn"][i], shin)
        line([hip, k, f]); d.ellipse([k[0] - lw / 2, k[1] - lw / 2, k[0] + lw / 2, k[1] + lw / 2], fill=INK)
        sx = f[0]; d.polygon([(sx - lw * 0.6, f[1] - lw * 0.6), (sx + face * lw * 2.6, f[1] - lw * 0.2), (sx + face * lw * 2.6, f[1] + lw * 0.7), (sx - lw * 0.6, f[1] + lw * 0.7)], fill=INK)
    line([hip, neck], lw * 1.15)
    sh = (neck[0] + (hip[0] - neck[0]) * 0.12, neck[1] + (hip[1] - neck[1]) * 0.12)
    hands = []
    for i in (1, 0):                                     # Arme (hinten zuerst)
        e = seg(sh, P["sh"][i], upper); hnd = seg(e, P["sh"][i] + P["el"][i], fore)
        line([sh, e, hnd]); d.ellipse([e[0] - lw / 2, e[1] - lw / 2, e[0] + lw / 2, e[1] + lw / 2], fill=INK)
        r = lw * 0.95; d.ellipse([hnd[0] - r, hnd[1] - r, hnd[0] + r, hnd[1] + r], fill=INK)
        hands.append(hnd)
    if tie:
        t0 = (neck[0], neck[1] + lw); d.polygon([(t0[0] - lw * 0.8, t0[1]), (t0[0] + lw * 0.8, t0[1]), (t0[0] + lw * 1.1, t0[1] + torso * 0.45), (t0[0], t0[1] + torso * 0.55), (t0[0] - lw * 1.1, t0[1] + torso * 0.45)], fill=tie, outline=INK)
    # Kopf
    hx, hy = head
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=skin, outline=INK, width=int(lw))
    if hair == "short": d.chord([hx - hr * 0.98, hy - hr * 1.02, hx + hr * 0.98, hy - hr * 0.1], 180, 360, fill=INK)
    elif hair == "long":
        d.chord([hx - hr * 1.02, hy - hr * 1.05, hx + hr * 1.02, hy - hr * 0.05], 180, 360, fill=INK)
        d.rectangle([hx - face * hr * 1.0 - (hr * 0.35 if face > 0 else 0), hy - hr * 0.5, hx - face * hr * 1.0 + (hr * 0.35 if face < 0 else 0), hy + hr * 0.9], fill=INK)
    elif hair == "bald": pass
    if cap: d.chord([hx - hr * 1.05, hy - hr * 1.15, hx + hr * 1.05, hy + hr * 0.7], 180, 360, fill=cap); d.line([(hx, hy - hr * 0.25), (hx + face * hr * 1.5, hy - hr * 0.25)], fill=cap, width=int(lw * 1.4))
    ex = hx + face * hr * 0.32 + look * hr * 0.1; ey = hy - hr * 0.05
    for dx in (-hr * 0.22, hr * 0.22):
        cx = ex + dx
        if expr == "shock": d.ellipse([cx - hr * 0.11, ey - hr * 0.15, cx + hr * 0.11, ey + hr * 0.15], fill=(255, 255, 255), outline=INK, width=max(2, int(lw * 0.5))); d.ellipse([cx - hr * 0.05, ey - hr * 0.05, cx + hr * 0.05, ey + hr * 0.05], fill=INK)
        else: d.ellipse([cx - hr * 0.07, ey - hr * 0.09, cx + hr * 0.07, ey + hr * 0.09], fill=INK)
    if glasses:
        for dx in (-hr * 0.22, hr * 0.22): d.ellipse([ex + dx - hr * 0.17, ey - hr * 0.15, ex + dx + hr * 0.17, ey + hr * 0.15], outline=INK, width=max(2, int(lw * 0.45)))
    by = ey - hr * 0.28; bw = max(2, int(lw * 0.55))
    if expr in ("worried", "shock"):
        d.line([(ex - hr * 0.35, by), (ex - hr * 0.1, by - hr * 0.1)], fill=INK, width=bw); d.line([(ex + hr * 0.1, by - hr * 0.1), (ex + hr * 0.35, by)], fill=INK, width=bw)
    elif expr == "angry":
        d.line([(ex - hr * 0.35, by - hr * 0.1), (ex - hr * 0.1, by)], fill=INK, width=bw); d.line([(ex + hr * 0.1, by), (ex + hr * 0.35, by - hr * 0.1)], fill=INK, width=bw)
    my = hy + hr * 0.42; mx = ex
    if expr == "smile": d.arc([mx - hr * 0.28, my - hr * 0.25, mx + hr * 0.28, my + hr * 0.12], 20, 160, fill=INK, width=bw)
    elif expr == "shock": d.ellipse([mx - hr * 0.1, my - hr * 0.1, mx + hr * 0.1, my + hr * 0.16], fill=INK)
    elif expr == "worried": d.arc([mx - hr * 0.22, my - hr * 0.02, mx + hr * 0.22, my + hr * 0.25], 200, 340, fill=INK, width=bw)
    elif expr == "talk": d.ellipse([mx - hr * 0.12, my - hr * 0.06, mx + hr * 0.12, my + hr * 0.1], fill=INK)
    else: d.line([(mx - hr * 0.16, my), (mx + hr * 0.16, my)], fill=INK, width=bw)
    return dict(head=(hx, hy, hr), hands=hands, hip=hip, neck=neck)

if __name__ == "__main__":
    im = Image.new("RGBA", (1080, 1920), (236, 232, 222, 255)); d = ImageDraw.Draw(im)
    for i, (pz, ex, kw) in enumerate([("stand", "neutral", {}), ("phone", "worried", dict(glasses=True)), ("hands_head", "shock", dict(tie=(200, 40, 50))),
                                       ("press", "angry", dict(cap=(40, 80, 160))), ("cheer", "smile", dict(hair="long")), ("walk1", "talk", {})]):
        stickman(d, 180 + (i % 3) * 360, 820 + (i // 3) * 900, 620, pz, 1, ex, **kw)
    im.save("stick_test.png"); print("ok")
