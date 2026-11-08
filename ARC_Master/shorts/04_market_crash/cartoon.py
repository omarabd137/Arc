"""Cartoon-Figuren im ARC-Video-Stil (hq.py: grosse Koepfe, Punktaugen, Kleidung, duenne Arme/Beine) fuer 9:16-Frames.
stickman(...)-kompatible Signatur, damit short04.py unveraendert bleiben kann."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../longform/01_money")); sys.path.insert(0, os.path.join(HERE, "../../longform/02_ai"))
import hq
from hq import P, figure, sprite, put
hq.STYLE.update(nose=False, hair_hi=False, foot_cap=False, brow_len=0.7)
_shadow = hq.Pen.shadow
hq.Pen.shadow = lambda self, *a, **k: None          # keine runden Schatten-Flecken unter den Schuhen

LEO = P(hair=(70, 50, 38), top=(64, 98, 156), pants=(44, 48, 60), shoes=(235, 235, 232), skin=(238, 202, 170), style="short", collar=True)
TRADER_R = P(hair=(40, 34, 30), top=(250, 250, 248), jacket=(46, 50, 62), pants=(46, 50, 62), shoes=(30, 28, 28), tie=(190, 40, 50), skin=(236, 200, 166), style="side")
TRADER_B = P(hair=(120, 84, 52), top=(250, 250, 248), jacket=(40, 60, 96), pants=(40, 60, 96), shoes=(30, 28, 28), tie=(40, 70, 160), skin=(214, 172, 134), style="short")
POLI = P(hair=(170, 170, 176), top=(250, 250, 248), jacket=(36, 40, 52), pants=(36, 40, 52), shoes=(20, 18, 18), tie=(40, 70, 160), skin=(236, 202, 172), style="side", age=58)
INVESTOR = P(hair=(30, 26, 24), top=(250, 170, 60), pants=(60, 64, 80), skin=(150, 100, 70), style="buzz")
ARMS = {"stand": ("down", "down"), "phone": ("down", "phone"), "point": ("down", "point"), "press": ("down", "point"), "hands_head": ("up", "up"),
        "shrug": ("shrug", "shrug"), "cheer": ("up", "up"), "drop": ("down", "hold"), "throw": ("up", "up"), "walk1": ("down", "down")}
EXPR = {"neutral": ("line", 0.0, "open"), "worried": ("worried", -0.07, "open"), "shock": ("o", -0.09, "wide"), "smile": ("smile", 0.0, "happy"),
        "talk": ("talk", 0.0, "open"), "angry": ("frown", 0.08, "open")}

import math
from PIL import Image
CLOCK = [0.0]                                          # globale Videozeit (von short04.frame gesetzt)
def _alive(pr, expr, seed):
    """Atmen, Blinzeln, Zittern - abhaengig von der Emotion."""
    t = CLOCK[0]; ph = (id(pr) % 97) * 0.37 + seed * 1.3
    mouth, brow, eyes = EXPR.get(expr, EXPR["neutral"])
    panic = expr in ("shock", "worried")
    if eyes != "happy" and (t + ph) % (2.6 if panic else 3.6) < 0.12: eyes = "closed"
    rate = 1.5 if expr == "shock" else (1.0 if panic else 0.42)
    bob = math.sin((t + ph) * math.pi * 2 * rate)
    jx = math.sin(t * 61 + ph) * 1.0 if expr == "shock" else 0.0
    return mouth, brow, eyes, bob, jx
def person(frame, pr, x, foot_y, R, pose="stand", face=1, expr="neutral", blink=False, seed=0):
    """Figur auf 1x-Frame: x, foot_y in Frame-Pixeln, R = Kopfradius-Masstab (~R*5 = Hoehe)."""
    mouth, brow, eyes, bob, jx = _alive(pr, expr, seed)
    if blink: eyes = "closed"
    arms = ARMS.get(pose, ("down", "down"))
    key = ("p9", id(pr), R, pose, face, mouth, brow, eyes)
    spr = sprite(key, lambda c: figure(c, 960, 1040, R, pr, face, mouth, brow, arms, "stand", 0.0, eyes))
    put(frame, spr, x - 960 + jx * R * 0.02, foot_y - 1040 + bob * R * 0.025)
_cu = {}
def closeup(frame, pr, cx, top, width, pose="stand", face=1, expr="neutral", seed=0):
    """Nahaufnahme (Oberkoerper/Gesicht gross, unten vom Bildrand angeschnitten) - scharf aus der 2x-Leinwand."""
    mouth, brow, eyes, bob, jx = _alive(pr, expr, seed)
    arms = ARMS.get(pose, ("down", "down")); key = (id(pr), pose, face, mouth, brow, eyes, width)
    if key not in _cu:
        old = hq.STYLE["brow_len"]; hq.STYLE["brow_len"] = 0.45
        cv = hq.canvas(); figure(cv, 960, 1040, 200, pr, face, mouth, brow * 0.7, arms, "stand", 0.0, eyes); hq.STYLE["brow_len"] = old
        S = hq.SS; im = cv.crop((int(620 * S), int(10 * S), int(1300 * S), int(1045 * S)))
        _cu[key] = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    im = _cu[key]; sc = width / 680
    frame.paste(im, (int(cx - width / 2 + jx * 3), int(top + bob * 9 * sc / 1.8)), im)
    return sc
