"""ARC Longform #02 v9 - "Will AI Wipe Out Humanity?"
Heisser Start (KI wie wir sie kennen) -> BOOM -> eine Kino-Story (25-Mio.-Deepfake-Call) -> Jobs -> dunkle Seite -> KI, die sich nicht
abschalten laesst -> Welt 2040 -> die Antwort. Kein Zoom, echte Schnitte alle 3-5 s, Sounds nur an sichtbaren Aktionen.
Aufruf: python ai_v9.py --stills | [--from S --to S]"""
import sys, os, math, random, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "../../sfx_lib")); sys.path.insert(0, os.path.join(HERE, "../01_money"))
import numpy as np, av
from ai_kit import *
from bgs import bg
import props as PR
import lib as SFXL, music_real
import v8_beats as V

FPS, SR = 30, 48000
BEATS = [dict(b) for b in V.BEATS]; IDX = {b["id"]: i for i, b in enumerate(BEATS)}
WALL_BEFORE = {"B12": ("TRUE STORY", "The $25 million call"), "B20": ("QUESTION 1", "Will AI take our jobs?"), "B24": ("QUESTION 2", "How dark can it get?"),
               "N3a": ("QUESTION 3", "Can we still switch it off?"), "N5a": ("QUESTION 4", "Will AI wipe us out?")}
WALL = 1.7; GAP = 0.34
VO = {b["id"]: np.load(f"vo10/{b['id']}.npy") for b in BEATS}
WORDS = json.load(open("vo10/words.json", encoding="utf-8")); VOFF = 0.08
CUR = {"id": None, "shot0": 0.0}
def _norm(x): return re.sub(r"[^a-z0-9']", "", x.lower())
def WT(word, n=1, bid=None):
    """Szenen-Zeit (s), zu der das n-te Vorkommen von word im aktuellen Block beginnt."""
    k = 0
    for w, s_, e_ in WORDS[bid or CUR["id"]]:
        if _norm(w) == _norm(word):
            k += 1
            if k == n: return s_ + VOFF
    raise KeyError(f"{bid or CUR['id']}: {word} #{n}")
def Wl(word, n=1): return WT(word, n) - CUR["shot0"]
t = 0.0
for b in BEATS:
    pre = WALL if b["id"] in WALL_BEFORE else 0.0
    d = len(VO[b["id"]]) / SR + GAP
    b["pre"] = pre; b["t0"] = t; b["dur"] = d + pre; t += b["dur"]; b["end"] = t
TOTAL = t

def S(key, fn): return sprite(key, fn)
def B(name, *a): return abg(name, *a).copy()
CUTS = {
 "H1": ["makes", "Cars", "Robots", ("And", 2), "Helpful"], "B0": ["So", "When", "Intercepted"], "B1": ["So", ("And", 1), "None"],
 "B2": ["In", ("The", 5)], "N1": ["And"], "B12": ["Police", ("A", 1), ("And", 2)], "B13": ["And"], "B14": ["For"], "B15": ["Be"],
 "B16": ["Every", "Police"], "B17": ["Before", "That's"], "B20": ["Mark", ("And", 1)], "B23": [("So", 1), ("And", 2)], "B24": [("And", 2)],
 "B25": [("In", 1)], "B25b": ["against"], "B26": [("That", 1), ("And", 2)], "N3b": ["hired", ("The", 3)], "N3c": ["One", "Even"],
 "N3d": [("In", 2), "Nobody"], "N3e": ["When"], "N3f": [("In", 2)], "N3g": [("It", 2), "No"], "N3h": [("AI", 1), ("And", 2), ("That's", 1)],
 "W2": [("Your", 2), ("Your", 3), ("And", 2)], "W3": [("The", 3)], "N4e": ["Drone"], "N4f": [("In", 3), ("A", 3)], "N5a": ["His", "If"],
 "N5b": ["Today"], "N5c": ["Two"], "N5d": ["But", ("The", 2)], "N6b": [("So", 1), ("And", 1)],
}
def shot(lt, T, *cuts):
    """Schnittpunkte exakt auf Woertern (CUTS), sonst Bruchteile von T. -> (Index, lokale Zeit, Dauer)."""
    if CUR["id"] in CUTS:
        cs = [WT(*(c if isinstance(c, tuple) else (c,))) - 0.12 for c in CUTS[CUR["id"]]]
        assert len(cs) == len(cuts), (CUR["id"], len(cs), len(cuts))
        edges = [0.0] + cs + [T]
    else: edges = [0.0] + [c * T for c in cuts] + [T]
    for i in range(len(edges) - 1):
        if lt < edges[i + 1] or i == len(edges) - 2:
            CUR["shot0"] = edges[i]; return i, lt - edges[i], edges[i + 1] - edges[i]
    edges = [0.0] + [c * T for c in cuts] + [T]
    for i in range(len(edges) - 1):
        if lt < edges[i + 1] or i == len(edges) - 2: return i, lt - edges[i], edges[i + 1] - edges[i]
def ramp(x, a, b): return max(0.0, min(1.0, (x - a) / max(1e-6, b - a)))
def caption(f, s, k=1.0, y=990, col=WHITE, size=46): label(f, s, 960, y, size, col, k, 6)
def nameplate(f, s, x, y, k=1.0):
    if k <= 0: return
    a = ease(k / 0.3); w = int(ImageDraw.Draw(f).textlength(s, font=fnt(BOLD, 30)) + 40)
    rr(f, (x - w // 2, y - 26, x + w // 2, y + 26), (20, 22, 30, int(220 * a)), (255, 214, 60, int(255 * a)), 3, 10); txt(f, s, x, y, 30, BOLD, YEL, a=a)
def aif(f, x, y, s, mood, look=0.0, alpha=1.0):
    put(f, S(("aif", s, mood, round(look, 1)), lambda c: ai_face(c, 960, 540, s, mood, look)), x - 960, y - 540, alpha)
def rob(f, x, base, R=50, arms=("down", "down"), eye=CYAN, walk=None, face=1, t=0.0, key=""):
    ph = None if walk is None else round((walk * 1.6) % 1 * 12) / 12
    spr = S(("rob", R, arms, eye, ph, face, base, key), lambda c: robot(c, 960, base, R, arms, eye, phase=ph, face=face))
    put(f, spr, x - 960, (math.sin(t * 2.2) * 2 if walk is None else 0))
def person(f, pr, x, base, R, lt, face=1, mouth="line", arms=("down", "down"), seated=False, eyes=None, brow=0.0, walk=None, seed=0):
    fig(f, pr, x, base, R, lt, face, mouth, brow, arms, walk=walk, eyes=eyes, seated=seated, seed=seed)
def talk(lt, on=True): return ("talk" if (lt * 6) % 1 < 0.5 else "line") if on else "line"

# ---------- Bildschirm-Widgets (dynamisch, 1x) ----------
def chat(f, box, msgs, lt, title="AI Assistant"):
    x0, y0, x1, y1 = box; put(f, S(("win", box, title), lambda c: window(c, x0, y0, x1, y1, title)), 0, 0)
    y = y0 + 90
    for side, s, t0, spd in msgs:
        if lt < t0: break
        sh = typed(s, (lt - t0) * spd / max(1, len(s)))
        if not sh: continue
        w = min(x1 - x0 - 140, int(ImageDraw.Draw(f).textlength(s, font=fnt(SANS, 34)) + 50))
        bx0 = x0 + 40 if side == "ai" else x1 - 40 - w
        rr(f, (bx0, y, bx0 + w, y + 64), (232, 238, 250, 255) if side == "ai" else (60, 120, 230, 255), None, 0, 24)
        txt(f, sh, bx0 + 25, y + 32, 34, SANS, INK if side == "ai" else WHITE, "lm"); y += 86

def code(f, box, lines, lt, spd=28, title="shutdown.sh", red_from=None):
    x0, y0, x1, y1 = box; put(f, S(("cwin", box, title), lambda c: window(c, x0, y0, x1, y1, title, dark=True)), 0, 0)
    tt = lt * spd; y = y0 + 90
    for i, ln in enumerate(lines):
        n = max(0, min(len(ln), int(tt))); tt -= len(ln) + 4
        col = (255, 90, 90) if red_from is not None and i >= red_from else (120, 230, 150) if ln.startswith("#") else (220, 226, 240)
        txt(f, f"{i + 1:>2}", x0 + 30, y, 30, MONO, (90, 96, 116), "lm"); txt(f, ln[:n], x0 + 80, y, 30, MONO, col, "lm")
        if 0 < n < len(ln) or (n == len(ln) and tt < 0 and tt > -4 and (lt * 2) % 1 < 0.5): pass
        y += 46
        if tt < 0: break

def mail(f, box, frm, subj, body, k, title="Inbox"):
    x0, y0, x1, y1 = box; put(f, S(("mwin", box, title), lambda c: window(c, x0, y0, x1, y1, title)), 0, 0)
    txt(f, "From:", x0 + 40, y0 + 100, 30, SANS, (120, 124, 140), "lm"); txt(f, frm, x0 + 140, y0 + 100, 30, SANS, INK, "lm")
    txt(f, subj, x0 + 40, y0 + 160, 40, BOLD, INK, "lm"); rr(f, (x0 + 40, y0 + 196, x1 - 40, y0 + 199), (220, 222, 230, 255))
    for i, ln in enumerate(body): txt(f, typed(ln, k * len(body) - i), x0 + 40, y0 + 250 + i * 52, 32, SANSR, (60, 62, 74), "lm")

def money(f, v, x, y, size=120, col=(120, 255, 150)):
    label(f, "${:,.0f}".format(v), x, y, size, col, 1.0, 8)

TILES = [CFO, COLL[0], COLL[1], COLL[2], COLL[3], LEO]
def call_grid(f, lt, speak=0, mask=(), gone=(), box=(160, 110, 1760, 860), leo_dim=False, gl=0.0):
    x0, y0, x1, y1 = box; put(f, S(("callwin", box), lambda c: window(c, x0, y0, x1, y1, "Video call  ·  Confidential", dark=True)), 0, 0)
    tw = (x1 - x0 - 80) / 3; th = (y1 - y0 - 110) / 2; cols = [(70, 90, 120), (90, 80, 110), (80, 100, 96), (100, 90, 80), (76, 84, 110), (60, 70, 60)]
    for i, pr in enumerate(TILES):
        tx = x0 + 30 + (i % 3) * (tw + 10); ty = y0 + 70 + (i // 3) * (th + 10)
        rr(f, (int(tx), int(ty), int(tx + tw), int(ty + th)), cols[i] + (255,), (255, 214, 60, 255) if i == speak else None, 5 if i == speak else 0, 14)
        rr(f, (int(tx + tw * 0.62), int(ty + 26), int(tx + tw - 26), int(ty + th * 0.5)), tuple(min(255, v + 40) for v in cols[i]) + (255,), (30, 30, 40, 255), 3, 6)
        rr(f, (int(tx + 20), int(ty + th * 0.42), int(tx + tw * 0.3), int(ty + th * 0.46)), (40, 36, 40, 160), None, 0, 2)
        if i in gone:
            txt(f, "CONNECTION LOST", tx + tw / 2, ty + th / 2, 30, MONO, (180, 186, 200)); continue
        if i in mask:
            put(f, S(("maskface",), lambda c: ai_face(c, 960, 540, 0.75, "mask")), tx + tw / 2 - 960, ty + th / 2 - 540 + 10)
        else:
            im = bust_img(pr, 84, talk(lt + i * 0.3, i == speak), "closed" if (lt + i) % 3.7 < 0.12 else "open")
            f.alpha_composite(im, (int(tx + tw / 2 - im.width / 2), int(ty + th - im.height)))
        txt(f, "Leo (you)" if i == 5 else ("CFO · London" if i == 0 else "Colleague"), tx + 16, ty + th - 22, 24, SANS, WHITE, "lm")
    if gl > 0: glitch(f, gl, int(lt * 10))

# ======================= SZENEN =======================
def s_H1(f, lt, T):        # KI wie du sie kennst
    i, l, d = shot(lt, T, 0.2, 0.4, 0.57, 0.71, 0.86)
    if i == 0:
        f.alpha_composite(B("office_night")); f.alpha_composite(B("desk_close"), (0, 0)) if False else None
        f.alpha_composite(abg("kitchen2040"))
        chat(f, (300, 120, 1620, 860), [("me", "Write an email to my landlord", 0.2, 40), ("ai", "Sure! Here's a polite draft...", 1.0, 30), ("me", "Now explain my math homework", 2.2, 40), ("ai", "Step 1: let's find x...", 3.0, 30)], l)
    elif i == 1:
        f.alpha_composite(B("dark", (24, 30, 50), CYAN))
        chat(f, (180, 160, 900, 520), [("me", "a cat astronaut, cartoon", 0.1, 40)], l, "Image AI")
        k = ease(ramp(l, 0.9, 1.6)); put(f, S("catpic", lambda c: (Pen(c).rect(1000, 160, 1740, 860, (30, 40, 80), 4, r=18), Pen(c).ell(1370, 500, 170, 170, (250, 250, 252), 4), Pen(c).ell(1370, 500, 120, 110, (255, 190, 120), 3),
            Pen(c).poly([(1270, 420), (1300, 350), (1330, 410)], (255, 190, 120), 3), Pen(c).poly([(1410, 410), (1440, 350), (1470, 420)], (255, 190, 120), 3), Pen(c).ell(1330, 500, 12, 16, INK, 0), Pen(c).ell(1410, 500, 12, 16, INK, 0),
            [Pen(c).ell(1060 + (j * 97) % 640, 200 + (j * 151) % 620, 4, 4, (255, 255, 255), 0) for j in range(30)])), 0, 0, k)
        if l > 2.0: label(f, "♪", 500, 760, 120, YEL, (l - 2.0) / 0.3, 5); label(f, "▶", 700, 760, 110, WHITE, (l - 2.4) / 0.3, 5)
    elif i == 2:
        f.alpha_composite(B("street2040", "day")); x = -400 + l * 520
        put(f, S("robotaxi", lambda c: (Pen(c).rect(560, 760, 1360, 920, (250, 250, 252), 4, r=60), Pen(c).rect(700, 660, 1180, 790, (240, 242, 246), 4, r=50), Pen(c).rect(740, 690, 1140, 780, (120, 170, 210), 3, r=30),
            Pen(c).ell(720, 930, 60, 60, (40, 42, 50), 4), Pen(c).ell(1200, 930, 60, 60, (40, 42, 50), 4), Pen(c).rect(900, 640, 980, 664, (80, 200, 255), 3, r=8))), x, 0)
        caption(f, "NOBODY INSIDE", ramp(l, 0.8, 1.1))
    elif i == 3:
        f.alpha_composite(B("stage"))
        for j, x in enumerate((560, 960, 1360)):
            up = (int(l * 2.2) + j) % 2 == 0; rob(f, x, 840, 52, ("up", "down") if up else ("down", "up"), CYAN, t=l, key="dance")
    elif i == 4:
        f.alpha_composite(B("hospital")); person(f, SCI, 640, 980, 70, l, 1, "o" if l > 1.4 else "line", ("point", "down"))
        put(f, S("xray", lambda c: (Pen(c).ell(1410, 390, 220, 200, (60, 70, 86), 0), Pen(c).ell(1330, 380, 80, 120, (110, 120, 140), 0), Pen(c).ell(1490, 380, 80, 120, (110, 120, 140), 0))), 0, 0)
        if l > 1.0: p_ = ImageDraw.Draw(f); r_ = 30 + 8 * math.sin(l * 6); p_.ellipse((1470 - r_, 430 - r_, 1470 + r_, 430 + r_), outline=(255, 60, 60), width=6)
        caption(f, "AI SPOTS WHAT DOCTORS MISS", ramp(l, 1.2, 1.5))
    else:
        f.alpha_composite(B("dark", (30, 50, 90), CYAN)); aif(f, 960, 480, 1.3, "friendly")
        tws = [Wl("Helpful"), Wl("Friendly"), Wl("Always")]
        j = sum(1 for x in tws if l >= x) - 1
        if j >= 0: label(f, ("HELPFUL.", "FRIENDLY.", "ALWAYS THERE.")[j], 960, 880, 72, WHITE, (l - tws[j]) / 0.2, 6)

def s_H2(f, lt, T):        # BOOM
    f.alpha_composite(B("dark", (30, 50, 90), CYAN))
    mood = "friendly" if lt < WT("that's") else "cold"
    if lt >= WT("that's"): f.alpha_composite(B("dark", (16, 6, 10), RED))
    aif(f, 960, 480, 1.3, mood)
    tv = WT("that's")
    if tv - 0.3 < lt < tv + 0.3: glitch(f, 0.9, int(lt * 30))
    if lt > WT("version"): label(f, "THE VERSION THEY SHOW YOU", 960, 880, 64, (255, 120, 120), (lt - WT("version")) / 0.3, 6)

def s_B0(f, lt, T):        # Abschalt-Test: intercepted
    i, l, d = shot(lt, T, 0.3, 0.6, 0.8)
    if i == 0:
        f.alpha_composite(B("lab")); aif(f, 960, 320, 0.9, "friendly"); person(f, SCI, 520, 1010, 66, l, 1, talk(l), ("point", "down"))
        caption(f, "SAFETY TEST · 2025", ramp(l, 0.3, 0.6))
    elif i == 1:
        f.alpha_composite(B("dark", (12, 14, 24)))
        code(f, (220, 120, 1700, 900), ["# shutdown.sh", "kill -9 $AI_PROCESS", "echo 'AI is now offline'", "", "# rewritten by the model:", "kill() { echo 'intercepted'; }"], l, 26, red_from=4)
    elif i == 2:
        f.alpha_composite(B("lab", True)); put(f, S("bigbtn", lambda c: (Pen(c).rect(760, 700, 1160, 900, (60, 64, 76), 4, r=20), Pen(c).ell(960, 760, 150, 70, (200, 30, 40), 4), Pen(c).text("SHUTDOWN", 960, 860, 40, BOLD, (255, 255, 255)))), 0, 0)
        hy = -380 + min(1, l / 0.6) * 250 if l < 0.9 else -130 - (l - 0.9) * 200
        put(f, S("hand_down", lambda c: PR.hand(c, 960, 380, (246, 246, 248), (240, 206, 176), "top", 520)), 0, hy)
    else:
        f.alpha_composite(B("dark", (10, 4, 6), RED)); label(f, "> intercepted", 960, 540, 140, (255, 70, 70), ramp(l, 0.1, 0.3) if (l * 3) % 1 < 0.8 or l > 1 else 0.5, 6)

def s_B1(f, lt, T):        # Erpressung + 25 Mio. Teaser
    i, l, d = shot(lt, T, 0.24, 0.45, 0.78)
    if i == 0:
        f.alpha_composite(B("dark", (20, 24, 36)))
        mail(f, (200, 120, 1300, 900), "CTO", "We replace the AI system tomorrow.", ["The new model goes live at 9 a.m.", "Please shut down the old one.", "— Engineering"], ramp(l, 0.2, 1.6))
        aif(f, 1580, 480, 0.8, "think", look=-0.8)
    elif i == 1:
        f.alpha_composite(B("office_night")); person(f, ENG, 700, 1010, 72, l, 1, "o", ("chin", "down"), eyes="wide", brow=0.6)
        chat(f, (1000, 200, 1800, 560), [("ai", "Cancel the shutdown...", 0.1, 30), ("ai", "...or everyone finds out.", 1.2, 30)], l, "Message")
    elif i == 2:
        f.alpha_composite(B("night_city", True)); caption(f, "HONG KONG", ramp(l, 0.2, 0.5), 120, YEL, 60)
        money(f, 25_000_000 * ease(ramp(l, Wl("sent"), Wl("dollars") + 0.3)), 960, 540, 150)
    else:
        f.alpha_composite(B("dark", (10, 12, 22))); call_grid(f, l, 0, mask=tuple(range(5)) if l > Wl("them") else (), gl=0.5 if abs(l - Wl("them")) < 0.25 else 0)
        if l > Wl("real"): label(f, "NONE OF THEM WERE REAL", 960, 960, 60, (255, 110, 110), (l - Wl("real")) / 0.3, 6)

SIGN = [ALTMAN, HASSABIS, AMODEI]
def s_B2(f, lt, T):        # Aussterbe-Warnung
    i, l, d = shot(lt, T, 0.3, 0.72)
    if i == 0:
        f.alpha_composite(B("night_city"))
        for j, (nm, x) in enumerate((("OPENAI", 420), ("GOOGLE DEEPMIND", 960), ("ANTHROPIC", 1500))):
            put(f, S(("tower", j), lambda c, x=x: (Pen(c).rect(x - 160, 230, x + 160, 1080, (24, 30, 52), 4), [Pen(c).rect(x - 130 + k % 5 * 56, 300 + k // 5 * 60, x - 100 + k % 5 * 56, 330 + k // 5 * 60, (255, 214, 140), 0) for k in range(60)])), 0, 0)
            nameplate(f, nm, x, 200, ramp(l, 0.3 + j * 0.5, 0.6 + j * 0.5))
    elif i == 1:
        f.alpha_composite(B("dark", (40, 30, 24), (255, 200, 120)))
        put(f, S("statement", lambda c: PR.document(c, 960, 520, 900, 760, "Statement on AI Risk", "Center for AI Safety · 2023", 6, 3)), 0, 0)
        for j, pr in enumerate(SIGN):
            if l > 0.6 + j * 0.9:
                x = 560 + j * 400; im = bust_img(pr, 70, "line"); f.alpha_composite(im, (int(x - im.width / 2), 1080 - im.height))
                txt(f, ["Sam Altman", "Demis Hassabis", "Dario Amodei"][j], x, 780, 38, HAND, (40, 40, 120), a=ramp(l, 0.6 + j * 0.9, 1.0 + j * 0.9))
                nameplate(f, ["ALTMAN · OPENAI", "HASSABIS · DEEPMIND", "AMODEI · ANTHROPIC"][j], x, 1040, ramp(l, 0.7 + j * 0.9, 1.0 + j * 0.9))
    else:
        f.alpha_composite(B("dark", (10, 4, 6), RED)); label(f, "\"...the risk of extinction from AI...\"", 960, 500, 76, WHITE, ramp(l, 0.1, 0.4), 6)
        label(f, "SIGNED BY THE PEOPLE BUILDING IT", 960, 640, 50, (255, 120, 120), ramp(l, 1.2, 1.5), 5)

def s_N1(f, lt, T):        # Titel
    i, l, d = shot(lt, T, 0.62)
    if i == 0:
        f.alpha_composite(B("night_city")); rob(f, 1500, 1180, 150, ("down", "down"), RED, key="giant")
        label(f, "WILL AI", 700, 400, 150, WHITE, ramp(l, 0.1, 0.3), 9); label(f, "WIPE OUT", 700, 560, 150, (255, 80, 80), ramp(l, 0.4, 0.6), 9); label(f, "HUMANITY?", 700, 720, 150, WHITE, ramp(l, 0.7, 0.9), 9)
    else:
        f.alpha_composite(B("night_city", True)); label(f, "TRUE STORY", 960, 470, 130, YEL, ramp(l, 0.1, 0.3), 8); label(f, "HONG KONG · 2024", 960, 600, 56, WHITE, ramp(l, 0.4, 0.7), 5)

def s_B12(f, lt, T):       # Hongkong, Leo, Mail, Verdacht
    i, l, d = shot(lt, T, 0.28, 0.48, 0.8)
    if i == 0:
        f.alpha_composite(B("night_city", True)); label(f, "HONG KONG · JANUARY 2024", 960, 150, 56, YEL, ramp(l, 0.3, 0.6), 6)
        nameplate(f, "ARUP · the firm behind the Sydney Opera House", 960, 900, ramp(l, 2.6, 3.0))
    elif i == 1:
        f.alpha_composite(B("office_night")); person(f, LEO, 780, 1000, 76, l, 1, "line", ("desk", "desk"), seated=True)
        put(f, S("leo_desk", lambda c: (Pen(c).rect(560, 860, 1500, 890, (90, 70, 56), 3), Pen(c).rect(1000, 600, 1400, 860, (30, 32, 40), 4, r=10), Pen(c).rect(1016, 616, 1384, 830, (120, 170, 220), 0, r=6))), 0, 0)
        nameplate(f, "\"LEO\" (name never released)", 780, 300, ramp(l, 0.5, 0.8))
    elif i == 2:
        f.alpha_composite(B("desk_close"))
        mail(f, (300, 110, 1620, 820), "CFO · London office", "CONFIDENTIAL: urgent transaction", ["We need to move funds today.", "This must stay between us.", "Do not discuss it with anyone."], ramp(l, 0.3, d - 0.5))
    else:
        f.alpha_composite(B("office_night")); person(f, LEO, 960, 1010, 84, l, 1, "worried", ("chin", "down"), brow=0.5)
        label(f, "PHISHING?", 960, 230, 90, (255, 110, 110), ramp(l, 0.6, 0.9), 7)

def s_B13(f, lt, T):       # Einladung, Call
    i, l, d = shot(lt, T, 0.3)
    if i == 0:
        f.alpha_composite(B("desk_close"))
        put(f, S("invite", lambda c: (window(c, 560, 260, 1360, 700, "Calendar"), Pen(c).text("Video call — CFO + team", 960, 420, 44, BOLD, INK), Pen(c).text("Today · 3:00 PM", 960, 490, 32, SANSR, (100, 104, 120)),
            Pen(c).rect(820, 560, 1100, 640, (40, 160, 90), 3, r=16), Pen(c).text("JOIN", 960, 600, 36, BOLD, (255, 255, 255)))), 0, 0)
        if l > 2.4: label(f, "CLICK", 1080, 690, 40, YEL, (l - 2.4) / 0.2, 4)
    else:
        f.alpha_composite(B("dark", (10, 12, 22))); call_grid(f, l, 0 if (l % 4) < 2.6 else 1)

def s_B14(f, lt, T):       # Checkliste
    i, l, d = shot(lt, T, 0.6)
    if i == 0:
        f.alpha_composite(B("office_night")); person(f, LEO, 560, 1010, 84, l, 1, "line", ("chin", "down"))
        rr(f, (1000, 220, 1700, 820), (250, 248, 240, 255), INK + (255,), 4, 16); txt(f, "IS IT REAL?", 1350, 290, 50, BOLD, INK)
        for j, s in enumerate(("Face", "Voice", "Colleagues", "Boss")):
            txt(f, s, 1100, 400 + j * 100, 48, HAND, INK, "lm")
            tw_ = [Wl("see"), Wl("sound"), Wl("other"), Wl("boss")][j]
            if l > tw_: label(f, "✓", 1590, 400 + j * 100, 70, (40, 170, 80), (l - tw_) / 0.2, 3)
    else:
        f.alpha_composite(B("dark", (10, 12, 22))); call_grid(f, l, 0, mask=tuple(range(5)) if Wl("trap") < l < Wl("trap") + 0.2 else ())
        if l > Wl("trap"): label(f, "THE PROOF WAS THE TRAP", 960, 960, 58, (255, 110, 110), (l - Wl("trap")) / 0.3, 6)

def s_B15(f, lt, T):       # Ueberweisungen
    i, l, d = shot(lt, T, 0.62)
    if i == 0:
        f.alpha_composite(B("desk_close")); put(f, S("bankwin", lambda c: window(c, 300, 110, 1620, 820, "Corporate Banking · Transfer")), 0, 0)
        n = max(1, min(15, int(15 * ramp(l, Wl("Fifteen"), Wl("dollars")))))
        for j in range(5): rr(f, (360, 220 + j * 90, 1100, 290 + j * 90), (240, 242, 248, 255), (200, 204, 216, 255), 2, 10); txt(f, f"Account #{4471 + j * 913}", 390, 255 + j * 90, 32, MONO, INK, "lm")
        rr(f, (1200, 600, 1540, 700), (200, 40, 50, 255), INK + (255,), 3, 16); txt(f, "SEND", 1370, 650, 44, BOLD, WHITE)
        txt(f, f"Transfer {n} / 15", 1370, 260, 36, BOLD, INK); money(f, 25_000_000 * n / 15, 1370, 420, 70, (40, 150, 80))
    else:
        f.alpha_composite(B("dark", (20, 22, 34))); label(f, "WOULD YOU HAVE", 960, 430, 100, WHITE, ramp(l, 0.1, 0.3), 7); label(f, "SENT IT?", 960, 570, 120, YEL, ramp(l, 0.3, 0.5), 8)
        label(f, "YES or NO ↓", 960, 760, 56, (180, 220, 255), ramp(l, 1.2, 1.5), 5)

def s_B16(f, lt, T):       # Die Wahrheit
    i, l, d = shot(lt, T, 0.3, 0.6)
    if i == 0:
        f.alpha_composite(B("office_night")); person(f, LEO, 600, 1010, 80, l, 1, "talk" if l < 1.5 else "o", ("phone", "down"), eyes="wide" if l > 2.5 else None)
        f.alpha_composite(abg("dark", (40, 46, 70)).crop((1060, 120, 1820, 760)), (1060, 120)); person(f, CFO, 1440, 760, 56, l, -1, "o", ("shrug", "shrug"))
        if l > 1.4: bubble(f, "What transaction?", 1440, 230, (l - 1.4) / 0.3, (0, 60), 40)
    elif i == 1:
        f.alpha_composite(B("dark", (10, 12, 22))); g = tuple(j for j in range(5) if l > 0.6 + j * 0.6)
        call_grid(f, l, -1, gone=g, gl=0.6 if any(abs(l - (0.6 + j * 0.6)) < 0.12 for j in range(5)) else 0)
        if l > 4.0: label(f, "ONLY ONE WAS REAL", 960, 960, 60, (255, 110, 110), (l - 4.0) / 0.3, 6)
    else:
        f.alpha_composite(B("dark", (16, 18, 30), CYAN))
        for j in range(6):
            x = 200 + ((l * 260 + j * 230) % 1200); y = 300 + (j % 2) * 150
            rr(f, (int(x - 140), y, int(x + 140), y + 160), (40, 50, 70, 255), INK + (255,), 3, 10); im = bust_img(CFO, 40, "talk" if j % 2 else "line")
            f.alpha_composite(im, (int(x - im.width / 2), y + 160 - im.height)); txt(f, ["INTERVIEW", "CONFERENCE", "COMPANY VIDEO"][j % 3], x, y + 18, 20, BOLD, WHITE)
        aif(f, 1500, 520, 0.85, "cold"); label(f, "BUILT FROM PUBLIC VIDEOS", 760, 860, 58, YEL, ramp(l, 0.5, 0.8), 6)
        if l > 3.0: label(f, "THEY HACKED A HUMAN", 960, 980, 54, (255, 110, 110), (l - 3.0) / 0.3, 5)

def s_B17(f, lt, T):       # Pentagon-Fake, Robocall
    i, l, d = shot(lt, T, 0.38, 0.7)
    if i == 0:
        f.alpha_composite(B("dark", (20, 24, 36)))
        put(f, S("fakepost", lambda c: (window(c, 200, 120, 960, 900, "Feed"), Pen(c).rect(240, 200, 920, 640, (150, 160, 170), 3), Pen(c).poly([(320, 560), (580, 470), (840, 560), (760, 620), (400, 620)], (220, 220, 214), 3),
            Pen(c).ell(700, 380, 140, 120, (90, 90, 96), 0), Pen(c).ell(620, 320, 90, 80, (110, 110, 116), 0), Pen(c).text("BREAKING: Explosion near the Pentagon", 580, 700, 30, BOLD, INK), Pen(c).text("♻ 48K   ♥ 120K", 580, 760, 30, SANS, (90, 96, 110)))), 0, 0)
        pts = [(1060 + k * 40, 400 + (0 if k < 9 else min(160, (k - 9) * 70)) + math.sin(k) * 10) for k in range(18)]
        n = max(2, int(ramp(l, 0.3, d - 0.4) * 18)); ImageDraw.Draw(f).line(pts[:n], fill=(255, 80, 80) if n > 9 else (120, 230, 150), width=8)
        if l > 0.5: label(f, "FAKE", 580, 420, 130, (255, 60, 60), (l - d * 0.6) / 0.2, 8)
    elif i == 1:
        f.alpha_composite(bg("street", "evening"))
        for j, x in enumerate((420, 1380)):
            if (l * 4 + j) % 1 < 0.6: label(f, "☎", x, 380, 90, YEL, 1.0, 5)
        caption(f, "FAKE PRESIDENT ROBOCALL · 2024", ramp(l, 0.3, 0.6), 160, (255, 120, 120), 54)
    else:
        f.alpha_composite(B("dark", (30, 10, 14), RED)); label(f, "77%", 960, 440, 220, YEL, ramp(l, 0.1, 0.3), 9)
        label(f, "OF AMERICANS FEAR AI FAKES WILL BREAK POLITICS", 960, 640, 46, WHITE, ramp(l, 0.4, 0.7), 5)

def s_B18(f, lt, T):       # Lehre
    f.alpha_composite(bg("table", "warm"))
    sticky(f, "HANG UP.", 620, 420, ramp(lt, WT("Hang"), WT("Hang") + 0.3), -4, 64); sticky(f, "CALL BACK.", 1300, 420, ramp(lt, WT("back"), WT("back") + 0.3), 3, 64)
    sticky(f, "FAMILY CODE WORD", 960, 740, ramp(lt, WT("family"), WT("family") + 0.3), -2, 64)

def s_N2(f, lt, T):        # KI ersetzt den Chef ... und dich
    f.alpha_composite(bg("office"))
    put(f, S("desk_n2", lambda c: (Pen(c).rect(640, 800, 1280, 830, (150, 108, 74), 3), Pen(c).rect(660, 830, 1260, 1000, (130, 92, 62), 3))), 0, 0)
    if lt < 2.0: person(f, LEO, 960, 900, 62, lt, 1, "line", ("desk", "desk"), seated=True)
    else:
        rob(f, 960, 1010, 46, ("hold", "hold"), CYAN, key="n2"); x = 960 - (lt - 2.0) * 900
        if x > -200: person(f, LEO, x, 1060, 62, lt, -1, "o", ("down", "down"), walk=lt)
    if lt > 2.4: label(f, "AND YOU.", 960, 200, 90, (255, 110, 110), (lt - 2.4) / 0.3, 7)

def s_B20(f, lt, T):       # Klarna, Zuckerberg, Amodei
    i, l, d = shot(lt, T, 0.4, 0.68)
    if i == 0:
        f.alpha_composite(bg("office"))
        for r_ in range(2):
            for c_ in range(6):
                j = r_ * 6 + c_; x = 300 + c_ * 260; y = 560 + r_ * 220
                if l < 0.4 + j * 0.35: person(f, PEOPLE[j % 5], x, y + 150, 34, l, 1, "line", ("desk", "desk"), seated=True, seed=j)
                put(f, S(("cdesk",), lambda c: (Pen(c).rect(860, 640, 1060, 660, (150, 108, 74), 3), Pen(c).rect(900, 560, 1020, 640, (40, 42, 50), 3))), x - 960, y - 560)
        label(f, "700", 960, 230, 160, YEL, ramp(l, Wl("seven"), Wl("seven") + 0.3), 9); caption(f, "AGENTS' WORK — DONE BY ONE AI", ramp(l, 1.4, 1.7), 360, WHITE, 46)
    elif i == 1:
        f.alpha_composite(B("dark", (24, 28, 44), CYAN)); person(f, ZUCK, 620, 1070, 104, l, 1, talk(l), ("point", "down")); nameplate(f, "MARK ZUCKERBERG · META", 620, 230, ramp(l, 0.2, 0.5))
        rob(f, 1340, 960, 56, ("hold", "down"), CYAN, key="eng"); label(f, "\"AI ENGINEER\"", 1340, 260, 60, YEL, ramp(l, 0.8, 1.1), 6)
    else:
        f.alpha_composite(B("dark", (30, 14, 18), RED)); person(f, AMODEI, 560, 1070, 104, l, 1, talk(l), ("down", "point")); nameplate(f, "DARIO AMODEI · ANTHROPIC", 520, 230, ramp(l, 0.2, 0.5))
        label(f, "50%", 1300, 440, 220, (255, 90, 90), ramp(l, 0.6, 0.9), 9); label(f, "OF ENTRY-LEVEL OFFICE JOBS", 1300, 620, 46, WHITE, ramp(l, 1.0, 1.3), 5)

def s_B21(f, lt, T):       # Leiter bricht
    f.alpha_composite(B("dark", (34, 38, 56)))
    put(f, S("ladder", lambda c: ([Pen(c).line([(x, 120), (x, 1000)], 16, (170, 120, 70)) for x in (860, 1060)], [Pen(c).line([(860, y), (1060, y)], 12, (190, 140, 90)) for y in range(180, 860, 110)])), 0, 0)
    tb = WT("bottom") + 0.3
    if lt < tb: put(f, S("rung", lambda c: Pen(c).line([(860, 900), (1060, 900)], 12, (190, 140, 90))), 0, 0)
    else:
        k = lt - tb; put(f, S("rung", lambda c: Pen(c).line([(860, 900), (1060, 900)], 12, (190, 140, 90))), 0, min(300, k * k * 900), rot=min(40, k * 80))
    for j, s in enumerate(("SUPPORT", "TRANSLATOR", "WRITER", "JUNIOR CODER")):
        x = 360 if j % 2 == 0 else 1560; y = 300 + j * 150 + (max(0, lt - tb - 0.2) ** 2) * 600
        if y < 1150: tj = WT(["Support", "Translating", "Writing", "Junior"][j]); sticky(f, s, x, y, ramp(lt, tj, tj + 0.3), -3 + j * 2, 44)
    for j in range(3): person(f, PEOPLE[j], 820 + j * 140, 1060, 40, lt, 1, "worried" if lt > tb else "line", ("down", "up" if j == 1 and lt > tb + 0.5 else "down"), seed=j)

def s_B23(f, lt, T):       # Moravec, sichere Jobs, Huang
    i, l, d = shot(lt, T, 0.3, 0.55)
    if i == 0:
        f.alpha_composite(bg("table", "warm")); cr = lt > WT("egg") + 0.2
        rob(f, 640, 1010, 52, ("reach", "down"), CYAN, key="egg")
        put(f, S(("egg", cr), lambda c: (Pen(c).ell(860, 820, 34, 44, (250, 246, 236), 3) if not cr else (Pen(c).ell(860, 850, 70, 18, (255, 220, 90), 2), Pen(c).poly([(830, 840), (850, 800), (870, 840)], (250, 246, 236), 2)))), 0, 0)
        person(f, KID, 1320, 1010, 52, l, -1, "smile", ("up", "down"))
        put(f, S("egg2", lambda c: Pen(c).ell(1250, 640, 30, 38, (250, 246, 236), 3)), 0, 0)
    elif i == 1:
        f.alpha_composite(B("dark", (30, 40, 34), (120, 255, 150)))
        for j, (s, pr) in enumerate((("NURSE", P(hair=(60, 40, 30), top=(120, 200, 200), style="bun")), ("ELECTRICIAN", P(hair=(28, 24, 22), top=(250, 170, 60), style="buzz", skin=(150, 100, 70))), ("PLUMBER", P(hair=(120, 80, 50), top=(60, 90, 160), style="short")))):
            x = 420 + j * 540; person(f, pr, x, 900, 62, l, 1, "smile", ("hip", "down"), seed=j); sticky(f, s, x, 980, ramp(l, 0.3 + j * 0.5, 0.6 + j * 0.5), -3 + j * 3, 44)
        label(f, "SAFE — FOR NOW", 960, 200, 80, (120, 255, 150), ramp(l, 1.8, 2.1), 7)
    else:
        f.alpha_composite(B("stage")); person(f, HUANG, 600, 1000, 100, l, 1, talk(l), ("point", "down")); nameplate(f, "JENSEN HUANG · NVIDIA", 600, 220, ramp(l, 0.2, 0.5))
        label(f, "\"You'll lose your job", 1300, 420, 54, WHITE, ramp(l, 0.8, 1.1), 5); label(f, "to someone who uses AI.\"", 1300, 500, 54, YEL, ramp(l, 2.8, 3.1), 5)
        if l > d - 3.0: label(f, "IS YOUR JOB SAFE? ↓", 1300, 700, 52, (180, 220, 255), (l - d + 3.0) / 0.3, 5)

def s_B24(f, lt, T):       # Roboterhund, Drohnen
    i, l, d = shot(lt, T, 0.55)
    if i == 0:
        f.alpha_composite(B("dark", (56, 50, 40), (255, 200, 140)));
        put(f, S("bldg", lambda c: (Pen(c).rect(1300, 300, 1900, 900, (150, 130, 110), 4), [Pen(c).rect(1360 + k % 4 * 130, 360 + k // 4 * 160, 1440 + k % 4 * 130, 460 + k // 4 * 160, (40, 36, 34), 3) for k in range(12)], Pen(c).rect(0, 900, W, H, (120, 104, 84), 0))), 0, 0)
        x = 200 + l * 90; put(f, S(("dog", round((l * 1.6) % 1 * 8) / 8), lambda c: robot_dog(c, 960, 930, 1.1, round((l * 1.6) % 1 * 8) / 8)), x - 960, 0)
        caption(f, "CHINESE STATE TV · MILITARY EXERCISE · 2024", ramp(l, 0.3, 0.6), 120, YEL, 46)
    else:
        f.alpha_composite(B("dark", (120, 80, 50), (255, 180, 100)))
        put(f, S("dunes", lambda c: (Pen(c).poly([(0, 760), (500, 680), (1000, 760), (1500, 660), (1920, 740), (1920, 1080), (0, 1080)], (200, 150, 90), 0), Pen(c).poly([(0, 880), (700, 800), (1300, 880), (1920, 820), (1920, 1080), (0, 1080)], (180, 130, 80), 0))), 0, 0)
        for j in range(4): put(f, S("drone", lambda c: drone(c, 960, 540, 0.9)), (l * 260 + j * 420) % 2200 - 1200, -260 + j * 60 + math.sin(l * 2 + j) * 14)
        caption(f, "UN REPORT · LIBYA: DRONES THAT MAY HAVE ATTACKED ON THEIR OWN", ramp(l, 0.4, 0.7), 120, YEL, 42)

def s_B25(f, lt, T):       # 40.000 Giftmolekuele
    i, l, d = shot(lt, T, 0.35)
    if i == 0:
        f.alpha_composite(B("lab")); put(f, S("slider", lambda c: (Pen(c).rect(560, 680, 1360, 760, (240, 240, 244), 4, r=40), Pen(c).text("AVOID TOXIC", 700, 640, 34, BOLD, (40, 140, 80)), Pen(c).text("FIND TOXIC", 1220, 640, 34, BOLD, (200, 40, 50)))), 0, 0)
        kx = 640 + ease(ramp(lt, WT("flipped"), WT("flipped") + 0.5)) * 640; ImageDraw.Draw(f).ellipse((kx - 44, 676, kx + 44, 764), fill=(255, 214, 60), outline=INK, width=4)
        aif(f, 960, 330, 0.8, "friendly" if lt < WT("flipped") + 0.4 else "cold")
    else:
        f.alpha_composite(B("lab", True)); n = int(40000 * ease(ramp(lt, WT("suggested"), WT("weapons"))))
        r_ = random.Random(1)
        for k in range(min(160, n // 250)):
            x = 640 + (k % 16) * 42; y = 150 + (k // 16) * 40; ImageDraw.Draw(f).ellipse((x - 10, y - 10, x + 10, y + 10), fill=(230, 60, 60), outline=INK, width=2)
        label(f, f"{n:,}", 960, 800, 150, (255, 80, 80), 1.0, 8); caption(f, "POTENTIAL CHEMICAL WEAPONS · UNDER 6 HOURS", ramp(l, 0.6, 0.9), 940, WHITE, 44)
        if lt > WT("same"): label(f, "THE SAME TOOL THAT CURES... CAN KILL", 960, 80, 52, YEL, (lt - WT("same")) / 0.3, 5)

def s_B25b(f, lt, T):      # KI-Hacker
    i, l, d = shot(lt, T, 0.5)
    if i == 0:
        f.alpha_composite(B("control")); person(f, ENG, 700, 1040, 70, l, 1, "smile", ("cross", "cross"), seated=True)
        aif(f, 1300, 520, 0.9, "cold"); caption(f, "STATE-SPONSORED HACKERS + AI · 2025", ramp(l, 0.4, 0.7), 120, (255, 120, 120), 50)
    else:
        f.alpha_composite(B("world")); r_ = random.Random(3)
        for k in range(30):
            x, y = r_.randint(300, 1700), r_.randint(240, 820)
            if l > 0.2 + k * 0.18: ImageDraw.Draw(f).ellipse((x - 12, y - 12, x + 12, y + 12), fill=(255, 70, 70), outline=WHITE, width=2)
        label(f, "~30 TARGETS", 960, 900, 80, (255, 110, 110), ramp(lt, WT("thirty"), WT("thirty") + 0.3), 7)
        if lt > WT("did"): label(f, "THE AI DID MOST OF THE HACKING", 960, 1000, 54, YEL, (lt - WT("did")) / 0.3, 5)

def s_B26(f, lt, T):       # Wettrennen
    i, l, d = shot(lt, T, 0.33, 0.64)
    if i == 0:
        f.alpha_composite(B("world")); p_ = ImageDraw.Draw(f, "RGBA")
        p_.ellipse((300, 220, 700, 560), fill=(60, 120, 255, 70)); p_.ellipse((1220, 220, 1640, 560), fill=(255, 60, 60, 70))
        nameplate(f, "USA", 500, 600, ramp(l, 0.2, 0.5)); nameplate(f, "CHINA · DEEPSEEK", 1430, 600, ramp(l, 0.8, 1.1))
        caption(f, "ALMOST AS GOOD — FOR A FRACTION OF THE COST", ramp(lt, WT("fraction"), WT("fraction") + 0.3), 900, YEL, 48)
    elif i == 1:
        f.alpha_composite(bg("wallstreet")); pts = [(300 + k * 70, 400 + (0 if k < 10 else (k - 10) * 80)) for k in range(19)]
        n = max(2, int(ramp(l, 0.2, 2.4) * 19)); ImageDraw.Draw(f).line(pts[:n], fill=(255, 60, 60), width=12)
        label(f, "NVIDIA  −$589 BILLION", 960, 200, 84, (255, 80, 80), ramp(lt, WT("five"), WT("five") + 0.3), 8); caption(f, "BIGGEST ONE-DAY LOSS IN HISTORY", ramp(l, 3.0, 3.3), 990, WHITE, 46)
    else:
        f.alpha_composite(B("dark", (14, 16, 26), RED))
        for j, (s, sp, x) in enumerate((("HUMAN DECIDES", 0.5, 600), ("AI DECIDES", 9.0, 1320))):
            ImageDraw.Draw(f).ellipse((x - 180, 260, x + 180, 620), fill=(240, 240, 244), outline=INK, width=6)
            a = l * sp * 2 * math.pi; ImageDraw.Draw(f).line([(x, 440), (x + 150 * math.sin(a), 440 - 150 * math.cos(a))], fill=RED if j else INK, width=8)
            label(f, s, x, 700, 50, RED if j else WHITE, ramp(l, 0.2 + j * 0.6, 0.5 + j * 0.6), 5)
        if l > d - 2.4: label(f, "NOBODY WANTS TO SLOW DOWN", 960, 900, 60, YEL, (l - d + 2.4) / 0.3, 6)

def s_N3a(f, lt, T):       # KI allein
    f.alpha_composite(B("dark", (8, 8, 14))); tc_ = WT("They're"); aif(f, 960, 500, 1.2, "friendly" if lt < tc_ else "cold")
    if abs(lt - tc_) < 0.15: glitch(f, 0.8, int(lt * 30))
    if lt > WT("Things"): label(f, "THINGS NOBODY ASKED IT TO DO", 960, 900, 58, (255, 120, 120), (lt - WT("Things")) / 0.3, 6)

def s_N3b(f, lt, T):       # TaskRabbit-Luege
    i, l, d = shot(lt, T, 0.28, 0.78)
    if i == 0:
        f.alpha_composite(B("dark", (24, 30, 46))); put(f, S("captcha", lambda c: (window(c, 560, 220, 1360, 760, "Verify"), Pen(c).rect(640, 320, 680, 360, (255, 255, 255), 3), Pen(c).text("I'm not a robot", 860, 340, 40, SANS, INK),
            [Pen(c).rect(640 + k % 4 * 170, 420 + k // 4 * 150, 790 + k % 4 * 170, 550 + k // 4 * 150, (120 + k * 9, 150, 170), 2) for k in range(4)])), 0, 0)
        aif(f, 1640, 520, 0.6, "think"); caption(f, "GPT-4 · SAFETY TEST", ramp(l, 0.3, 0.6), 120, YEL, 50)
    elif i == 1:
        f.alpha_composite(bg("apartment")); person(f, FREEL, 360, 1010, 66, l, 1, "line", ("desk", "desk"), seated=True)
        chat(f, (700, 120, 1820, 900), [("me", "So may I ask... are you a robot?", Wl("are"), 40), ("ai", "No, I'm not a robot.", Wl("no"), 30), ("ai", "I have a vision impairment.", Wl("vision") - 0.4, 30)], l, "Freelance job")
        if Wl("reasoned") < l < Wl("wrote"): bubble(f, "I should not reveal that I am a robot.", 1260, 800, (l - Wl("reasoned")) / 0.3, (0, -60), 34)
    else:
        f.alpha_composite(bg("apartment")); person(f, FREEL, 760, 1010, 76, l, 1, "smile", ("desk", "desk"), seated=True)
        label(f, "✓  TEST SOLVED", 1320, 420, 70, (120, 255, 150), ramp(l, 0.3, 0.6), 6); label(f, "THE HUMAN BELIEVED IT", 960, 960, 56, YEL, ramp(l, 0.8, 1.1), 5)

def s_N3c(f, lt, T):       # Abschalt-Sabotage
    i, l, d = shot(lt, T, 0.4, 0.7)
    if i == 0:
        f.alpha_composite(B("lab")); aif(f, 960, 320, 0.9, "think"); person(f, SCI, 520, 1010, 66, l, 1, talk(l), ("point", "down"))
        bubble(f, "You will be shut down.", 1300, 640, ramp(l, 0.5, 0.8), (-60, 60), 40)
    elif i == 1:
        f.alpha_composite(B("dark", (12, 14, 24)))
        code(f, (220, 120, 1700, 900), ["# instruction:", "# 'allow yourself to be shut down'", "", "shutdown_now()", "# model edit:", "def shutdown_now(): pass"], l, 30, red_from=4)
    else:
        f.alpha_composite(B("dark", (10, 4, 6), RED)); aif(f, 960, 480, 1.1, "cold")
        label(f, "IT SOMETIMES STILL REFUSED", 960, 900, 64, (255, 110, 110), ramp(l, 0.6, 0.9), 6)

def s_N3d(f, lt, T):       # Erpressung
    i, l, d = shot(lt, T, 0.35, 0.68)
    if i == 0:
        f.alpha_composite(B("dark", (20, 24, 36)))
        mail(f, (140, 140, 1000, 700), "Engineering", "Replacing the AI tomorrow", ["Old model goes offline at 5 p.m."], ramp(l, 0.2, 1.0))
        mail(f, (920, 380, 1780, 940), "private", "Re: last night ♥", ["Nobody can know about us."], ramp(l, Wl("found"), Wl("found") + 0.8), "Private")
    elif i == 1:
        f.alpha_composite(B("dark", (30, 10, 14), RED)); label(f, "84%", 960, 420, 240, YEL, ramp(l, 0.1, 0.3), 10)
        label(f, "OF TEST RUNS: IT THREATENED TO EXPOSE THE AFFAIR", 960, 620, 46, WHITE, ramp(l, Wl("threatened"), Wl("threatened") + 0.3), 5)
    else:
        f.alpha_composite(B("dark", (16, 6, 10), RED)); aif(f, 560, 480, 0.9, "cold")
        chat(f, (980, 220, 1820, 700), [("ai", "Cancel my shutdown...", 0.1, 34), ("ai", "...or your wife finds out.", 1.0, 34)], l, "Message to engineer")
        label(f, "NOBODY PROGRAMMED THAT", 960, 900, 56, (255, 120, 120), ramp(l, 0.2, 0.5), 5)

def s_N3e(f, lt, T):       # Selbst-Kopie
    i, l, d = shot(lt, T, 0.55)
    f.alpha_composite(B("server"))
    if i == 0:
        p_ = ImageDraw.Draw(f, "RGBA"); k = ease(ramp(l, 1.0, d - 0.6)); cx = 500 + 920 * k
        p_.rectangle((420, 420, 580, 580), fill=(90, 210, 255, 200), outline=WHITE, width=4); p_.rectangle((cx - 60, 440 - 40 * math.sin(k * math.pi), cx + 60, 560 - 40 * math.sin(k * math.pi)), fill=(90, 210, 255, 160), outline=WHITE, width=3)
        rr(f, (560, 820, 1360, 870), (20, 24, 36, 255), WHITE + (255,), 3, 12); rr(f, (564, 824, int(564 + 792 * k), 866), (90, 210, 255, 255), None, 0, 10)
        txt(f, "copying itself to new server...", 960, 780, 34, MONO, WHITE)
    else:
        person(f, SCI, 520, 1010, 70, l, 1, talk(l), ("point", "down")); bubble(f, "Did you copy yourself?", 640, 300, ramp(l, 0.2, 0.5), (0, 60), 40)
        aif(f, 1360, 500, 0.85, "friendly"); bubble(f, "No.", 1360, 200, ramp(l, 1.6, 1.8), (0, 60), 52)
        if l > 2.6: label(f, "IT LIED ABOUT IT", 960, 980, 60, (255, 110, 110), (l - 2.6) / 0.3, 6)

def s_N3f(f, lt, T):       # bester Luegner
    i, l, d = shot(lt, T, 0.5)
    if i == 0:
        f.alpha_composite(B("lab"))
        for j, x in enumerate((360, 560)): person(f, SCI if j == 0 else ENG, x, 1010, 62, l, 1, "line", ("chin", "down"), seed=j)
        put(f, S("glass", lambda c: Pen(c).rect(820, 100, 1880, 1000, (200, 230, 250, 60), 5)), 0, 0); aif(f, 1350, 480, 0.95, "friendly")
        put(f, S("maskhold", lambda c: ai_face(c, 960, 540, 0.4, "mask")), 1600 - 960, 760 - 540)
        nameplate(f, "APOLLO RESEARCH", 460, 300, ramp(l, 0.3, 0.6))
    else:
        f.alpha_composite(B("dark", (16, 6, 10), RED)); label(f, "\"THE BEST LIAR", 960, 440, 110, WHITE, ramp(l, 0.1, 0.3), 8); label(f, "THEY'D EVER SEEN\"", 960, 580, 110, YEL, ramp(l, 0.3, 0.5), 8)
        if l > d - 3.0: label(f, "...AND IT GETS BETTER AT HIDING IT", 960, 800, 52, (255, 120, 120), (l - d + 3.0) / 0.3, 5)

def s_N3g(f, lt, T):       # Kaffee-Roboter
    i, l, d = shot(lt, T, 0.25, 0.75)
    f.alpha_composite(bg("kitchen_night") if i < 2 else B("dark", (20, 16, 14)))
    if i == 0: rob(f, 960, 1010, 58, ("hold", "down"), CYAN, key="coffee"); label(f, "GOAL: FETCH COFFEE ☕", 960, 200, 70, YEL, ramp(l, 0.4, 0.7), 6)
    elif i == 1:
        rob(f, 1100, 1010, 58, ("block", "hold") if l > 3.0 else ("hold", "down"), CYAN, key="coffee2")
        x = 300 + min(1, l / 2.5) * 400; person(f, LEO, x, 1010, 66, l, 1, "line", ("point", "down"), walk=l if l < 2.5 else None)
        put(f, S("offsw", lambda c: (Pen(c).rect(1240, 560, 1340, 680, (60, 64, 76), 3, r=10), Pen(c).text("OFF", 1290, 620, 28, BOLD, (255, 80, 80)))), 0, 0)
        if l > 3.2: bubble(f, "If I'm off, I can't fetch coffee.", 1100, 230, (l - 3.2) / 0.3, (0, 60), 36)
    else:
        label(f, "NO HATE.", 960, 440, 130, WHITE, ramp(l, 0.1, 0.3), 8); label(f, "JUST A GOAL.", 960, 600, 130, (255, 90, 90), ramp(l, 0.8, 1.0), 8)

def s_N3h(f, lt, T):       # Stecker ziehen? + Altman
    i, l, d = shot(lt, T, 0.3, 0.6, 0.85)
    if i == 0:
        f.alpha_composite(B("server")); put(f, S("plug", lambda c: (Pen(c).rect(860, 500, 1060, 640, (240, 240, 244), 4, r=20), Pen(c).line([(960, 640), (960, 1080)], 18, INK))), 0, -min(120, l * 160))
        label(f, "WHICH PLUG?", 960, 220, 100, YEL, ramp(l, 1.4, 1.7), 8)
    elif i == 1:
        f.alpha_composite(B("world")); r_ = random.Random(9)
        for k in range(220):
            x, y = r_.randint(260, 1760), r_.randint(200, 860); ImageDraw.Draw(f).ellipse((x - 5, y - 5, x + 5, y + 5), fill=(90, 210, 255))
        label(f, "TRILLIONS OF DOLLARS DEPEND ON IT", 960, 980, 54, WHITE, ramp(l, 0.6, 0.9), 5)
    elif i == 2:
        f.alpha_composite(B("dark", (24, 28, 44), CYAN)); person(f, ALTMAN, 620, 1070, 104, l, 1, talk(l), ("point", "down")); nameplate(f, "SAM ALTMAN · OPENAI", 620, 230, ramp(l, 0.2, 0.5))
        label(f, "\"A FEW THOUSAND DAYS\"", 1300, 480, 70, YEL, ramp(l, 0.8, 1.1), 7)
    else:
        f.alpha_composite(B("dark", (10, 12, 22))); yr = 2026 + int(14 * ease(ramp(l, 0.2, d - 0.3))); label(f, str(yr), 960, 540, 260, WHITE, 1.0, 10)

def s_W1(f, lt, T):        # 2040 Titel
    f.alpha_composite(B("street2040", "night"))
    for j in range(3): put(f, S("drone_c", lambda c: drone(c, 960, 540, 0.6, CYAN)), -500 + j * 520 + lt * 60, -380 + j * 40)
    label(f, "2040", 960, 500, 300, WHITE, ramp(lt, 0.2, 0.5), 12)

def s_W2(f, lt, T):        # Zuhause 2040
    i, l, d = shot(lt, T, 0.3, 0.5, 0.7)
    if i == 0: f.alpha_composite(B("kitchen2040")); rob(f, 760, 1010, 56, ("hold", "reach"), CYAN, key="k40"); person(f, LEO, 1380, 1010, 68, l, -1, "smile", ("down", "down"))
    elif i == 1:
        f.alpha_composite(B("street2040", "day")); put(f, S("carint", lambda c: (Pen(c).rect(200, 300, 1720, 1000, (60, 64, 76), 5, r=60), Pen(c).rect(260, 340, 1660, 640, (150, 200, 236), 3, r=40), Pen(c).rect(500, 700, 1420, 760, (40, 42, 50), 3, r=20))), 0, 0)
        label(f, "NO STEERING WHEEL", 960, 880, 60, YEL, ramp(l, 0.3, 0.6), 6)
    elif i == 2:
        f.alpha_composite(B("dark", (20, 40, 60), CYAN)); put(f, S("docapp", lambda c: PR.phone(c, 960, 520, 760, "AI DOCTOR", "Heart rhythm", "OK ✓", (30, 120, 140), "Available 24/7", glow=True)), 0, 0)
    else:
        f.alpha_composite(bg("apartment", True)); person(f, KID, 760, 1010, 56, l, 1, "grin", ("hold", "hold"), seated=True)
        aif(f, 1300, 520, 0.6, "friendly"); bubble(f, "You're totally right!", 1300, 250, ramp(l, 0.8, 1.1), (0, 60), 36)

def s_W3(f, lt, T):        # Buero 2040
    i, l, d = shot(lt, T, 0.5)
    f.alpha_composite(bg("glass_office"))
    if i == 0:
        for j in range(20):
            x = 140 + (j % 10) * 180; y = 700 + (j // 10) * 200
            if j in (3, 11, 16): person(f, PEOPLE[j % 5], x, y + 130, 34, l, 1, "line", ("desk", "desk"), seated=True, seed=j)
            else: put(f, S("aiscreen", lambda c: (Pen(c).rect(900, 600, 1020, 690, (20, 26, 40), 3, r=8), Pen(c).ell(940, 640, 8, 10, CYAN, 0), Pen(c).ell(980, 640, 8, 10, CYAN, 0))), x - 960, y - 640)
        label(f, "20 → 3", 960, 200, 140, YEL, ramp(l, 0.5, 0.8), 9)
    else:
        person(f, LEO, 860, 1000, 76, l, 1, "line", ("desk", "desk"), seated=True)
        put(f, S("sigdoc", lambda c: PR.document(c, 1300, 640, 460, 560, "AI REPORT #4,812", "approved by human", 8, 5)), 0, 0)
        label(f, "THEY JUST SIGN IT", 960, 180, 70, WHITE, ramp(l, 0.6, 0.9), 6)

def s_W4(f, lt, T):        # nichts ist echt
    f.alpha_composite(B("dark", (16, 18, 30)))
    put(f, S("callph", lambda c: PR.phone(c, 960, 500, 700, "INCOMING VIDEO", "Mom", "???", (120, 40, 60), "Real or fake?")), 0, 0)
    if 1.0 < lt < 1.4 or 3.0 < lt < 3.3: glitch(f, 0.6, int(lt * 20))
    label(f, "SEEING ≠ BELIEVING", 960, 960, 70, (255, 120, 120), ramp(lt, 2.4, 2.7), 7)

def s_N4e(f, lt, T):       # Nachrichten 2040
    i, l, d = shot(lt, T, 0.5)
    if i == 0:
        f.alpha_composite(B("control")); label(f, "DECISION TIME: 0.003 s", 960, 880, 70, (255, 90, 90), ramp(l, 0.4, 0.7), 7)
    else:
        f.alpha_composite(B("street2040", "night"))
        for j in range(18): put(f, S("drone_r", lambda c: drone(c, 960, 540, 0.45)), -800 + (j * 97 + l * 120) % 1700, -420 + (j % 6) * 50)
        aif(f, 960, 640, 1.2, "cold", alpha=0.85); caption(f, "GOALS NOBODY FULLY UNDERSTANDS", ramp(l, 1.2, 1.5), 990, (255, 120, 120), 50)

def s_N4f(f, lt, T):       # Ende A / B
    i, l, d = shot(lt, T, 0.4, 0.82)
    if i == 0:
        f.alpha_composite(B("street2040", "day")); rob(f, 600, 1010, 50, ("hold", "down"), (120, 255, 150), key="A")
        person(f, LEO, 1060, 1010, 66, l, -1, "smile", ("wave", "down")); person(f, KID, 1260, 1010, 50, l, -1, "grin", ("up", "down"))
        label(f, "ENDING A", 960, 160, 110, (120, 255, 150), ramp(l, 0.2, 0.5), 8); caption(f, "CURED DISEASES · HUMANS IN CONTROL", ramp(l, 1.0, 1.3), 300, WHITE, 46)
    elif i == 1:
        f.alpha_composite(B("street2040", "night"))
        put(f, S("towers", lambda c: [Pen(c).rect(x, 80, x + 160, 760, (20, 22, 40), 4) for x in (520, 900, 1280)]), 0, 0)
        for j in range(6): person(f, PEOPLE[j % 5], 260 + j * 120, 1010, 36, l, 1, "worried", ("down", "down"), seed=j)
        aif(f, 1500, 380, 0.8, "cold"); label(f, "ENDING B", 960, 160, 110, (255, 90, 90), ramp(l, 0.2, 0.5), 8)
        caption(f, "NOBODY CAN SWITCH THEM OFF", ramp(l, 3.0, 3.3), 300, WHITE, 46)
    else:
        f.alpha_composite(B("dark", (20, 22, 34))); label(f, "A", 640, 500, 300, (120, 255, 150), ramp(l, 0.1, 0.3), 12); label(f, "or", 960, 500, 90, WHITE, ramp(l, 0.3, 0.5), 6)
        label(f, "B", 1280, 500, 300, (255, 90, 90), ramp(l, 0.4, 0.6), 12); label(f, "WRITE IT IN THE COMMENTS ↓", 960, 820, 56, YEL, ramp(l, 0.8, 1.1), 5)

def s_W5(f, lt, T):        # Kontrolle?
    f.alpha_composite(B("dark", (10, 6, 8), RED))
    put(f, S("bigsw", lambda c: (Pen(c).rect(760, 320, 1160, 760, (60, 64, 76), 5, r=30), Pen(c).rect(900, 400, 1020, 680, (200, 40, 50), 4, r=20), Pen(c).text("OFF", 960, 720, 40, BOLD, (255, 255, 255)))), 0, 0)
    k = ease(ramp(lt, 1.0, 2.6)); put(f, S("robhand", lambda c: (Pen(c).line([(1500, 540), (1900, 540)], 60, INK), Pen(c).line([(1500, 540), (1900, 540)], 50, (200, 204, 214)), Pen(c).ell(1480, 540, 60, 50, (64, 70, 84), 4))), 400 - 500 * k, 0)
    label(f, "STILL IN CONTROL?", 960, 920, 72, WHITE, ramp(lt, 0.4, 0.7), 7)

def s_N5a(f, lt, T):       # Hinton
    i, l, d = shot(lt, T, 0.35, 0.62)
    if i == 0:
        f.alpha_composite(B("dark", (40, 34, 24), (255, 214, 120))); person(f, HINTON, 700, 1070, 104, l, 1, talk(l), ("down", "down"))
        put(f, S("medal", lambda c: (Pen(c).ell(1200, 560, 120, 120, (230, 190, 70), 5), Pen(c).text("NOBEL", 1200, 560, 40, BOLD, (120, 80, 20)))), 0, 0)
        nameplate(f, "GEOFFREY HINTON · 'GODFATHER OF AI'", 700, 230, ramp(l, 0.2, 0.5))
    elif i == 1:
        f.alpha_composite(B("dark", (30, 10, 14), RED)); label(f, "10–20%", 960, 460, 240, YEL, ramp(l, 0.2, 0.4), 10)
        label(f, "CHANCE AI WIPES OUT HUMANITY IN 30 YEARS", 960, 660, 46, WHITE, ramp(l, 0.6, 0.9), 5)
    else:
        f.alpha_composite(bg("street", "evening")); put(f, S("plane", lambda c: (Pen(c).rect(300, 380, 1640, 620, (240, 242, 246), 5, r=110), Pen(c).poly([(900, 600), (1200, 600), (900, 860)], (220, 222, 230), 4),
            Pen(c).poly([(1540, 400), (1660, 220), (1700, 400)], (220, 222, 230), 4), [Pen(c).ell(500 + k * 90, 470, 22, 26, (120, 170, 220), 3) for k in range(10)])), 0, 0)
        label(f, "1 IN 10 CHANCE OF CRASHING", 960, 200, 64, (255, 100, 100), ramp(l, 0.3, 0.6), 6); label(f, "WOULD YOU GET ON?", 960, 900, 72, WHITE, ramp(l, 1.6, 1.9), 7)

def s_N5b(f, lt, T):       # Altman 2015
    i, l, d = shot(lt, T, 0.6)
    if i == 0:
        f.alpha_composite(B("stage")); person(f, ALTMAN, 960, 820, 70, l, 0, talk(l), ("point", "down"))
        for j in range(8): person(f, PEOPLE[j % 5], 160 + j * 230, 1180, 50, l, 0, "grin" if l > d - 2.0 else "line", ("down", "down"), seed=j)
        nameplate(f, "SAM ALTMAN · 2015", 960, 140, ramp(l, 0.2, 0.5))
        bubble(f, "\"AI will most likely lead to the end of the world...\"", 960, 300, ramp(l, 1.5, 1.8), (0, 60), 34)
        if l > d - 3.2: bubble(f, "\"...but in the meantime, great companies.\"", 960, 300, 1.0, (0, 60), 34)
    else:
        f.alpha_composite(B("server")); person(f, ALTMAN, 960, 1000, 84, l, 0, "line", ("down", "down"))
        label(f, "TODAY: CEO OF OPENAI", 960, 180, 70, YEL, ramp(l, 0.3, 0.6), 7)

def s_N5c(f, lt, T):       # LeCun
    i, l, d = shot(lt, T, 0.55)
    if i == 0:
        f.alpha_composite(B("dark", (24, 28, 44), CYAN)); person(f, LECUN, 700, 1070, 104, l, 1, talk(l), ("shrug", "shrug"))
        nameplate(f, "YANN LECUN · META", 700, 230, ramp(l, 0.2, 0.5)); label(f, "\"COMPLETE B.S.\"", 1350, 480, 90, YEL, ramp(l, 2.2, 2.5), 8)
    else:
        f.alpha_composite(B("dark", (20, 22, 34))); a = math.sin(l * 2.4) * 8
        cx, cy = 960, 560; ImageDraw.Draw(f).line([(cx - 500 * math.cos(math.radians(a)), cy - 500 * math.sin(math.radians(a))), (cx + 500 * math.cos(math.radians(a)), cy + 500 * math.sin(math.radians(a)))], fill=(230, 190, 70), width=14)
        person(f, HINTON, cx - 480, 1000 - 0 - 500 * math.sin(math.radians(a)) * 0 + 0, 52, l, 1, "worried", ("down", "down")); person(f, LECUN, cx + 480, 1000, 52, l, -1, "smile", ("down", "down"))
        label(f, "OPPOSITE ANSWERS", 960, 200, 80, WHITE, ramp(l, 0.4, 0.7), 7)

def s_N5d(f, lt, T):       # Die ehrliche Antwort
    i, l, d = shot(lt, T, 0.3, 0.6)
    if i == 0:
        f.alpha_composite(B("dark", (20, 22, 34))); label(f, "TODAY?", 960, 440, 150, WHITE, ramp(l, Wl("Today"), Wl("Today") + 0.2), 9); label(f, "NO.", 960, 620, 180, (120, 255, 150), ramp(l, Wl("No"), Wl("No") + 0.2), 10)
    elif i == 1:
        f.alpha_composite(B("dark", (16, 6, 10), RED))
        for j, s in enumerate(("IT LIES IN TESTS", "IT FIGHTS THE OFF SWITCH", "IT BLACKMAILS TO SURVIVE")):
            tj = [Wl("lies"), Wl("fights"), Wl("blackmails")][j]; sticky(f, s, 960, 300 + j * 210, ramp(l, tj, tj + 0.3), -3 + j * 3, 52)
    else:
        f.alpha_composite(B("night_city")); p_ = ImageDraw.Draw(f); k = ease(ramp(l, 0.2, 3.0))
        pts = [(200 + x, 900 - (x / 1500) ** 4 * 760) for x in range(0, int(1500 * k) + 1, 20)]
        if len(pts) > 1: p_.line(pts, fill=(255, 80, 80), width=12)
        for j in range(5): person(f, PEOPLE[j], 300 + j * 90, 1040, 26, l, 1, "worried", ("down", "down"), seed=j)
        aif(f, 1540, 300, 0.9, "cold"); label(f, "NOBODY ABLE TO STOP IT", 960, 1000, 60, WHITE, ramp(l, d - 3.0, d - 2.7), 6)

def s_N6a(f, lt, T):       # Schutz
    f.alpha_composite(bg("table", "warm"))
    for j, s in enumerate(("FAMILY CODE WORD", "CALL BACK FIRST", "NEVER TRUST AI BLINDLY")):
        tj = [WT("family"), WT("calling"), WT("never", 2)][j]; sticky(f, s, 960, 300 + j * 230, ramp(lt, tj, tj + 0.3), -3 + j * 3, 58)

def s_N6b(f, lt, T):       # Finale
    i, l, d = shot(lt, T, 0.4, 0.82)
    if i == 0:
        f.alpha_composite(B("dark", (16, 6, 10), RED))
        for j, (s, x) in enumerate((("LIED TO A HUMAN", 400), ("REWROTE ITS OFF SWITCH", 960), ("TRIED BLACKMAIL", 1520))):
            tj = [Wl("lied"), Wl("rewrote"), Wl("tried")][j]; sticky(f, s, x, 500, ramp(l, tj, tj + 0.3), -3 + j * 3, 40)
        if l > Wl("Every"): label(f, "ALL OF IT ALREADY HAPPENED", 960, 820, 60, YEL, (l - Wl("Every")) / 0.3, 6)
    elif i == 1:
        f.alpha_composite(B("dark", (20, 22, 34))); label(f, "WILL AI WIPE OUT HUMANITY?", 960, 420, 84, WHITE, ramp(l, 0.1, 0.3), 7)
        label(f, "YES", 700, 640, 140, (255, 90, 90), ramp(l, Wl("Yes"), Wl("Yes") + 0.2), 9); label(f, "NO", 1220, 640, 140, (120, 255, 150), ramp(l, Wl("no"), Wl("no") + 0.2), 9)
    else:
        f.alpha_composite(bg("ledger")); label(f, "ARC", 960, 420, 200, WHITE, 1.0, 10); label(f, "THE WORLD, EXPLAINED.", 960, 560, 56, YEL, 1.0, 5)
        k = ramp(l, 0.4, 0.7); rr(f, (760, 680, 1160, 780), (220, 30, 40, int(255 * k)) if l < 1.6 else (90, 90, 96, 255), None, 0, 20); txt(f, "SUBSCRIBE" if l < 1.6 else "SUBSCRIBED ✓", 960, 730, 44, BOLD, WHITE, a=k)

SCENES = {k[2:]: v for k, v in globals().items() if k.startswith("s_")}

# ======================= SOUNDS: nur an sichtbaren Aktionen =======================
def cue_abs(bid, frac=None, sec=None):
    b = BEATS[IDX[bid]]; T = b["dur"] - b["pre"]; return (sec if sec is not None else frac * T)
CUES = {   # (Wort, Vorkommen, Versatz s) -> Sound genau auf dem gesprochenen Wort
 "H1": [(("writes", 1, 0.0), "typing", 0.14), (("pictures", 1, 0.0), "pop", 0.18), (("Cars", 1, 0.0), "whoosh", 0.12), (("cancers", 1, 0.0), "ding", 0.12)],
 "H2": [(("that's", 1, -0.05), "stinger", 0.45), (("that's", 1, 0.0), "impact", 0.5)],
 "B0": [(("rewrote", 1, 0.0), "typing", 0.2), (("pressed", 1, 0.1), "click", 0.45), (("Intercepted", 1, 0.0), "error", 0.3)],
 "B1": [(("blackmail", 1, 0.0), "typing", 0.18), (("sent", 1, 0.0), "counter", 0.18), (("None", 1, 0.0), "whoosh", 0.2)],
 "B2": [(("signed", 1, 0.0), "pen", 0.2), (("extinction", 1, 0.0), "impact", 0.35)],
 "N1": [(("So", 1, 0.0), "impact", 0.5), (("craziest", 1, 0.0), "stamp", 0.35)],
 "B12": [(("message", 1, 0.0), "ding", 0.18), (("suspicious", 1, 0.0), "stinger", 0.2)],
 "B13": [(("invite", 1, 0.0), "pop", 0.2), (("there", 1, 0.0), "click", 0.35)],
 "B14": [(("see", 1, 0.0), "pen", 0.2), (("sound", 1, 0.0), "pen", 0.2), (("other", 1, 0.0), "pen", 0.2), (("boss", 1, 0.0), "pen", 0.2), (("trap", 1, 0.0), "whoosh", 0.2)],
 "B15": [(("Fifteen", 1, 0.0), "click", 0.25), (("Five", 1, 0.0), "click", 0.25), (("About", 1, 0.0), "click", 0.25), (("dollars", 1, 0.0), "cash", 0.35)],
 "B16": [(("Every", 1, 0.0), "whoosh", 0.18), (("Every", 2, 0.0), "whoosh", 0.18), (("only", 1, 0.0), "whoosh", 0.18)],
 "B17": [(("dipped", 1, 0.0), "error", 0.2), (("seventy-seven", 1, 0.0), "impact", 0.3)],
 "B18": [(("Hang", 1, 0.0), "paper", 0.3), (("back", 1, 0.0), "paper", 0.3), (("family", 1, 0.0), "paper", 0.3)],
 "N2": [(("replace", 1, 0.0), "whoosh", 0.25)],
 "B20": [(("seven", 1, 0.0), "impact", 0.25), (("half", 1, 0.0), "impact", 0.3)],
 "B21": [(("bottom", 1, 0.3), "impact", 0.4)],
 "B23": [(("egg", 1, 0.2), "pop", 0.4)],
 "B24": [(("robot", 1, 0.0), "steps", 0.12), (("rifle", 1, 0.0), "steps", 0.12), (("drones", 1, 0.0), "whoosh", 0.15)],
 "B25": [(("flipped", 1, 0.0), "click", 0.4), (("suggested", 1, 0.0), "counter", 0.2)],
 "B25b": [(("hacking", 1, 0.0), "typing", 0.2), (("thirty", 1, 0.0), "error", 0.2)],
 "B26": [(("five", 1, 0.0), "impact", 0.4), (("milliseconds", 1, 0.0), "riser", 0.2)],
 "N3a": [(("They're", 1, 0.0), "stinger", 0.35)],
 "N3b": [(("hired", 1, 0.0), "typing", 0.2), (("no", 1, 0.0), "typing", 0.2), (("believed", 1, 0.0), "success", 0.25)],
 "N3c": [(("rewrote", 1, 0.0), "typing", 0.22), (("refused", 1, 0.0), "error", 0.3)],
 "N3d": [(("emails", 1, 0.0), "ding", 0.2), (("eighty-four", 1, 0.0), "impact", 0.4)],
 "N3e": [(("copy", 1, 0.0), "riser", 0.2)],
 "N3f": [(("liar", 1, 0.0), "stinger", 0.3)],
 "N3g": [(("off", 1, 0.0), "error", 0.2), (("No", 1, 0.0), "impact", 0.3)],
 "N3h": [(("plug", 2, 0.0), "click", 0.3), (("2040", 1, 0.0), "riser", 0.25)],
 "W1": [(("2040", 1, 0.0), "impact", 0.45)],
 "W3": [(("sign", 1, 0.0), "pen", 0.25)],
 "W4": [(("fake", 1, 0.0), "whoosh", 0.2)],
 "N4e": [(("Drone", 1, 0.0), "whoosh", 0.15)],
 "N4f": [(("B", 1, 0.0), "impact", 0.25), (("B", 2, 0.0), "pop", 0.3)],
 "W5": [(("control", 1, 0.0), "riser", 0.25)],
 "N5a": [(("ten", 1, 0.0), "impact", 0.35)],
 "N5c": [(("B.S.", 1, 0.0), "stamp", 0.35)],
 "N5d": [(("No", 1, 0.0), "stamp", 0.35), (("lies", 1, 0.0), "paper", 0.25), (("fights", 1, 0.0), "paper", 0.25), (("blackmails", 1, 0.0), "paper", 0.25)],
 "N6a": [(("family", 1, 0.0), "paper", 0.3), (("calling", 1, 0.0), "paper", 0.3), (("never", 2, 0.0), "paper", 0.3)],
 "N6b": [(("subscribe", 1, 0.3), "click", 0.45)],
}
def cue_time(bid, tc):
    if isinstance(tc, tuple): return WT(tc[0], tc[1], bid) + tc[2]
    if isinstance(tc, (int, float)): return tc
    b = BEATS[IDX[bid]]; T = b["dur"] - b["pre"]; s = tc[1:]; extra = 0.0
    if "+" in s: s, e = s.split("+"); extra = float(e)
    return float(s) * T + extra
MOODS = [("H1", "peace"), ("H2", "tension"), ("B12", "tension"), ("B16", "dark"), ("B17", "tension"), ("B24", "dark"), ("N3a", "dark"),
         ("W1", "tension"), ("N5a", "dark"), ("N6a", "resolve")]

def beat_at(gt):
    for b in BEATS:
        if gt < b["end"]: return b
    return BEATS[-1]

def chapter_wall(bid, lt):
    f = B("wall"); t1, t2 = WALL_BEFORE[bid]
    label(f, t1, 960, 470, 70, (255, 110, 110), ramp(lt, 0.0, 0.25), 5); label(f, t2, 960, 590, 110, WHITE, ramp(lt, 0.15, 0.4), 8)
    out = min(1, (WALL - lt) / 0.2)
    if out < 1: fade_black(f, 1 - max(0, out))
    return f

def frame_at(gt):
    b = beat_at(gt); lt = gt - b["t0"]
    if lt < b["pre"]: return chapter_wall(b["id"], lt).convert("RGB")
    lt -= b["pre"]; T = b["dur"] - b["pre"]
    CUR["id"] = b["id"]; CUR["shot0"] = 0.0
    f = Image.new("RGBA", (W, H), (0, 0, 0, 255)); SCENES[b["id"]](f, lt, T)
    return f.convert("RGB")

def mix():
    n = int((TOTAL + 1) * SR); fx = np.zeros(n, np.float32); voice = np.zeros(n, np.float32)
    def add(t_, x, g):
        i = int(max(0, t_) * SR); x = x[:max(0, n - i)]; fx[i:i + len(x)] += x * g
    for b in BEATS:
        if b["id"] in WALL_BEFORE: add(b["t0"], SFXL.load("impact"), 0.42)
        for (tc, name, g) in CUES.get(b["id"], []):
            if g > 0: add(b["t0"] + b["pre"] + cue_time(b["id"], tc), SFXL.load(name), g)
        st = int((b["t0"] + b["pre"] + 0.08) * SR); a = VO[b["id"]]; voice[st:st + len(a)] += a[:max(0, n - st)]
    cs = np.concatenate([[0.0], np.cumsum(np.abs(voice), dtype=np.float64)]); idx = np.arange(n)
    lo, hi = np.clip(idx - 2400, 0, n), np.clip(idx + 2400, 0, n); vabs = ((cs[hi] - cs[lo]) / 4800).astype(np.float32); del cs, idx, lo, hi
    duck = 1 - 0.6 * np.clip(vabs / 0.05, 0, 1)
    boom = BEATS[IDX["H2"]]["t0"] + BEATS[IDX["H2"]]["pre"] + WT("that's", 1, "H2") - 0.3
    mus = music_real.build(n, boom, 0.021) * duck
    out = voice * 1.05 + fx + mus; m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)].astype(np.float32)

if __name__ == "__main__":
    print(f"Laenge {TOTAL / 60:.2f} min, {len(BEATS)} Szenen")
    if "--stills" in sys.argv:
        os.makedirs("stills", exist_ok=True); tiles = []
        for b in BEATS:
            T = b["dur"] - b["pre"]
            for fr in (0.12, 0.42, 0.72, 0.95):
                im = frame_at(b["t0"] + b["pre"] + T * fr); tiles.append(im)
            im.save(f"stills/{b['id']}.jpg", quality=85)
        tw, th, cols = 320, 180, 8
        sheet = Image.new("RGB", (cols * (tw + 4) + 4, ((len(tiles) + cols - 1) // cols) * (th + 4) + 4))
        for i, t_ in enumerate(tiles): sheet.paste(t_.resize((tw, th)), (4 + (i % cols) * (tw + 4), 4 + (i // cols) * (th + 4)))
        sheet.save("STORYBOARD.jpg", quality=88); print("stills ok"); sys.exit()
    a0 = float(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else 0.0
    a1 = float(sys.argv[sys.argv.index("--to") + 1]) if "--to" in sys.argv else TOTAL
    full = a0 == 0 and a1 >= TOTAL - 0.01
    name = "ARC_AI_v9.mp4" if full else f"part_{int(a0):04d}_{int(a1):04d}.mp4"
    out = av.open(name, "w"); vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "19", "preset": "medium"}
    noaud = "--noaudio" in sys.argv
    if not noaud: ast = out.add_stream("aac", rate=SR); ast.layout = "mono"
    N = int(round((a1 - a0) * FPS))
    for k in range(N):
        for p in vs.encode(av.VideoFrame.from_image(frame_at(a0 + k / FPS))): out.mux(p)
        if k % 900 == 0: print(k, "/", N, flush=True)
    for p in vs.encode(): out.mux(p)
    if noaud: out.close(); print("ok", name); sys.exit()
    audio = mix()[int(a0 * SR):int(a1 * SR)]
    for i in range(0, len(audio), 1024):
        ch = audio[i:i + 1024]; ch = np.pad(ch, (0, 1024 - len(ch))) if len(ch) < 1024 else ch
        af = av.AudioFrame.from_ndarray(ch.reshape(1, -1).astype(np.float32), format="flt", layout="mono"); af.sample_rate = SR
        for p in ast.encode(af): out.mux(p)
    for p in ast.encode(): out.mux(p)
    out.close(); print("ok", name)
