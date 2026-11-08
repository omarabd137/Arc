"""Wiedererkennbare Cartoon-Versionen echter Personen (Crayon-Prinzip: Aehnlichkeit ueber die markantesten Merkmale).
Steve Jobs 1976: schlank, lange glatte Haare mit Mittelscheitel bis zur Schulter, kurzer Vollbart + Schnurrbart,
                 kleine runde Drahtbrille, dunkler Rollkragen.
Steve Wozniak 1976: breit und rund, buschige Locken, grosser buschiger Vollbart, grosse eckige Brille, Karohemd.
Ron Wayne 1976: 41 Jahre, kurzes zurueckgekaemmtes dunkles Haar, Schnurrbart, eckige Brille, Sakko mit Krawatte.
Ron Wayne heute: weisses Haar, weisser Schnurrbart, Brille."""
import math
from apple_kit import S, sh, shape, stroke, ellipse_pts, INK, figure, P
from PIL import ImageDraw

JOBS76 = P(hair=(40, 30, 24), hair_hi=(80, 62, 50), top=(40, 40, 46), skin=(236, 198, 160), big=0.88, look="jobs")
WOZ76 = P(hair=(58, 42, 32), hair_hi=(104, 80, 64), top=(176, 70, 60), skin=(238, 196, 156), big=1.32, look="woz")
WAYNE76 = P(hair=(62, 48, 38), hair_hi=(110, 90, 74), top=(110, 96, 78), tie=(120, 44, 40), skin=(236, 200, 164), look="wayne")
WAYNE_NOW = P(hair=(232, 232, 236), hair_hi=(255, 255, 255), top=(110, 96, 78), skin=(236, 198, 168), look="wayne_old")

def _geom(cx, base, R, face):
    leg, tor_h = R * 1.25, R * 1.35
    hcy = base - leg - tor_h - R * 0.78
    return hcy, cx + face * R * 0.24, hcy + R * 0.05

def person2(img, cx, base, R, p, face=1, mouth="line", brow=0.0, arms=("down", "down"), seed=1, seated=False):
    look = p.get("look"); hcy, ex, ey = _geom(cx, base, R, face)
    d = ImageDraw.Draw(img, "RGBA"); hair = p["hair"]
    if look == "jobs":     # lange Haare hinter Kopf und Schultern
        shape(d, ellipse_pts(cx, hcy + R * 0.35, R * 1.12, R * 1.25, 60, 180, 360) + [(cx + R * 1.12, hcy + R * 1.25), (cx - R * 1.12, hcy + R * 1.25)], hair, seed + 1, lw=4)
    if look == "woz":      # buschige Locken hinter dem Kopf
        for k in range(14):
            a = math.radians(160 + k * 16.5)
            shape(d, ellipse_pts(cx + math.cos(a) * R * 0.98, hcy + math.sin(a) * R * 0.98, R * 0.32, R * 0.3), hair, seed + 10 + k, lw=3)
    figure(img, cx, base, R, p, face=face, mouth=mouth, brow=brow, arms=arms, seed=seed, seated=seated)
    d = ImageDraw.Draw(img, "RGBA")
    if look == "jobs":
        for sx in (-1, 1):  # Mittelscheitel: zwei Haarhaelften, die seitlich ueber die Stirn fallen
            shape(d, [(cx + sx * 4, hcy - R * 1.0), (cx + sx * R * 0.6, hcy - R * 0.85), (cx + sx * R * 1.02, hcy - R * 0.2), (cx + sx * R * 1.04, hcy + R * 0.6),
                      (cx + sx * R * 0.86, hcy + R * 0.55), (cx + sx * R * 0.7, hcy - R * 0.3), (cx + sx * R * 0.2, hcy - R * 0.62)], hair, seed + 2 + sx, lw=4)
        jaw = ellipse_pts(cx + face * R * 0.08, hcy + R * 0.12, R * 0.9, R * 0.86, 30, 25, 155)          # kurzer Bart
        inner = list(reversed(ellipse_pts(ex, hcy + R * 0.42, R * 0.3, R * 0.16, 20, 0, 180)))
        shape(d, jaw + inner, hair, seed + 4, lw=3)
        shape(d, ellipse_pts(ex, ey + R * 0.27, R * 0.2, R * 0.06, 20, 180, 360) + [(ex + R * 0.2, ey + R * 0.3), (ex - R * 0.2, ey + R * 0.3)], hair, seed + 5, lw=3)
        for k in (-1, 1):  # kleine runde Drahtbrille
            gx = ex + k * R * 0.26
            d.ellipse(S(gx - R * 0.14, ey - R * 0.14, gx + R * 0.14, ey + R * 0.14), outline=(70, 66, 60), width=4)
        stroke(d, [(ex - R * 0.12, ey - R * 0.02), (ex + R * 0.12, ey - R * 0.02)], lw=3, color=(70, 66, 60))
    elif look == "woz":
        for k in range(7):  # Locken oben auf dem Kopf
            a = math.radians(205 + k * 22)
            shape(d, ellipse_pts(cx + math.cos(a) * R * 0.82, hcy + math.sin(a) * R * 0.82, R * 0.3, R * 0.27), hair, seed + 30 + k, lw=3)
        jaw = ellipse_pts(cx + face * R * 0.05, hcy + R * 0.05, R * 1.02, R * 1.05, 30, 15, 165)          # grosser buschiger Bart
        inner = list(reversed(ellipse_pts(ex, hcy + R * 0.42, R * 0.26, R * 0.14, 20, 0, 180)))
        shape(d, jaw + inner, hair, seed + 40, lw=4)
        for k in range(6):
            a = math.radians(30 + k * 24)
            shape(d, ellipse_pts(cx + face * R * 0.05 + math.cos(a) * R * 0.95, hcy + R * 0.05 + math.sin(a) * R * 1.0, R * 0.16, R * 0.14), hair, seed + 50 + k, lw=2)
        for k in (-1, 1):  # grosse eckige Brille
            gx = ex + k * R * 0.28
            d.rounded_rectangle(S(gx - R * 0.2, ey - R * 0.16, gx + R * 0.2, ey + R * 0.15), radius=int(R * 0.06 * 2), outline=INK, width=6, fill=(255, 255, 255, 50))
        stroke(d, [(ex - R * 0.08, ey - R * 0.04), (ex + R * 0.08, ey - R * 0.04)], lw=4)
    elif look in ("wayne", "wayne_old"):
        shape(d, ellipse_pts(ex, ey + R * 0.27, R * 0.2, R * 0.07, 20, 180, 360) + [(ex + R * 0.2, ey + R * 0.31), (ex - R * 0.2, ey + R * 0.31)], hair, seed + 60, lw=3)
        for k in (-1, 1):
            gx = ex + k * R * 0.27
            d.rounded_rectangle(S(gx - R * 0.17, ey - R * 0.13, gx + R * 0.17, ey + R * 0.12), radius=int(R * 0.05 * 2), outline=INK, width=5, fill=(255, 255, 255, 40))
        stroke(d, [(ex - R * 0.1, ey - R * 0.04), (ex + R * 0.1, ey - R * 0.04)], lw=4)
    if look == "woz":      # Karomuster auf dem Hemd
        leg, tor_h = R * 1.25, R * 1.35; hip = base - leg; tcy = hip - tor_h * 0.42; tw = R * 1.05 * p["big"]
        for k in range(-2, 3):
            stroke(d, [(cx + k * tw * 0.2, tcy - tor_h * 0.45), (cx + k * tw * 0.2, tcy + tor_h * 0.45)], lw=3, color=sh(p["top"], 0.7))
            stroke(d, [(cx - tw * 0.45, tcy + k * tor_h * 0.18), (cx + tw * 0.45, tcy + k * tor_h * 0.18)], lw=3, color=sh(p["top"], 0.7))
    return hcy
