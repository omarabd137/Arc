"""ARC Longform #01 v3 – "The $100 Bill That Explains Everything".
Ruhige Einstellungen + echte Schnitte (kein Zoom), Sounds nur an sichtbaren Aktionen (CUES), Jason v3 (eleven_v4).
Aufruf: python money_v3.py --stills | --preview | (voll) [--from S --to S]"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "../../sfx_lib"))
import numpy as np, av
from PIL import Image, ImageDraw, ImageFont
from hq import *
from bgs import bg, car, house, tree
import props as PR
from bill_kit import Ledger
import lib as SFXL, music

FPS, SR = 30, 48000
BEATS = json.load(open("beats_v3.json", encoding="utf-8")); IDX = {b["id"]: i for i, b in enumerate(BEATS)}
WALL_BEFORE = {"B5": ("SECRET #1", "The deposit"), "B11": ("SECRET #2", "Money from nothing"), "B16": ("SECRET #3", "The line"),
               "B20": ("SECRET #4", "The invisible tax"), "B25": ("SECRET #5", "The other side of the loan"), "B28": ("SECRET #6", "How the rich play"),
               "B31": ("SECRET #7", "Heads they win, tails you lose"), "B34": ("FINALE", "The bill on the table")}
WALL = 1.6
VO = {}
for b in BEATS:
    fn = f"vo_v3/{b['id']}.npy"
    if os.path.exists(fn): VO[b["id"]] = np.load(fn)
t = 0.0
for b in BEATS:
    pre = WALL if b["id"] in WALL_BEFORE else 0.0
    d = len(VO[b["id"]]) / SR + 0.32 if b["id"] in VO else 3.0
    b["pre"] = pre; b["t0"] = t; b["dur"] = d + pre; t += b["dur"]; b["end"] = t
TOTAL = t
LEDGER = Ledger()

def S(key, fn): return sprite(key, fn)
def copybg(name, *a): return bg(name, *a).copy()
def fg(f, name, box, *a): f.alpha_composite(bg(name, *a).crop(box), box[:2])

# ======================= SZENEN =======================
def s_B0(f, lt, T):            # Hand legt den 100-$-Schein auf den Tisch
    f.alpha_composite(copybg("table"))
    k = ease(lt / 1.0); y = -300 + 900 * k
    hy = (y - 900 + 30) if lt < 1.0 else (30 - (lt - 1.0) * 1600)
    if hy > -1000: put(f, S("hand_top", lambda c: PR.hand(c, 960, 520, (40, 44, 56), (236, 200, 166), "top", 600)), 0, hy)
    put(f, S("bill100", lambda c: PR.real_bill(c, 960, 640, 560, value="100", angle=-4)), 0, (y - 600) if lt < 1.0 else 0)
    label(f, "COST TO PRINT: < 10¢", 960, 330, 64, (255, 255, 255), (lt - 3.0) / 0.4)
    if lt > 7.2: label(f, "RICH", 640, 880, 70, (255, 214, 60), (lt - 7.2) / 0.4)
    if lt > 8.6: label(f, "POOR", 1280, 880, 70, (255, 110, 100), (lt - 8.6) / 0.4)

def s_B1(f, lt, T):            # Kinder schieben ihre Raeder die Strasse entlang; dann Buero mit 25
    if lt < 6.6:
        f.alpha_composite(copybg("street", "day"))
        for i, (pr_, col, x0) in enumerate(((KID_J, (200, 60, 54), -120), (KID_R, (60, 110, 180), -420))):
            x = x0 + 150 * lt
            put(f, S(("bike", i), lambda c, col=col: PR.bike(c, 960, 990, 250, col)), x + 130 - 960, 0)
            fig(f, pr_, x, 1000, 46, lt, 1, "grin" if i == 0 else "smile", 0.0, ("push", "push"), walk=lt, seed=i)
        sticky(f, "JAKE", -120 + 150 * lt, 760, (lt - 1.6) / 0.3); sticky(f, "RYAN", -420 + 150 * lt, 760, (lt - 2.4) / 0.3, 3)
    else:
        l2 = lt - 6.6; f.alpha_composite(copybg("office"))
        for x, pr_, fc in ((600, JAKE, 1), (1320, RYAN, -1)):
            fig(f, pr_, x, 812, 58, lt, fc, "smile", 0.0, ("desk", "desk"), seated=True, seed=x)
            put(f, S(("desk_o", x), lambda c, x=x: (PR.Pen(c).rect(x - 230, 760, x + 230, 786, (150, 108, 74), 3), PR.Pen(c).rect(x - 210, 786, x + 210, 990, (130, 92, 62), 3))))
            put(f, S(("mon", x), lambda c, x=x, fc=fc: __import__("bgs").monitor(PR.Pen(c), x + fc * 175, 760, 160)))
        label(f, "SAME DESK. SAME SALARY.", 960, 140, 60, (255, 255, 255), (l2 - 1.6) / 0.4)
        if l2 > 3.4: put(f, S("pc_j", lambda c: PR.paycheck(c, 600, 500, 420, "Jake")), 0, (1 - ease((l2 - 3.4) / 0.4)) * 500)
        if l2 > 3.7: put(f, S("pc_r", lambda c: PR.paycheck(c, 1320, 500, 420, "Ryan")), 0, (1 - ease((l2 - 3.7) / 0.4)) * 500)

def s_B2(f, lt, T):
    f.alpha_composite(copybg("studio", (30, 30, 36))); label(f, "20 YEARS LATER", 960, 540, 110, (255, 255, 255), lt / 0.3)

def s_B3(f, lt, T):            # Split Jake 45 / Ryan 45, dann die drei Fragen
    if lt < 9.6:
        L = bg("apartment", False).crop((360, 0, 1320, H)); R = bg("porch", "day").crop((640, 0, 1600, H))
        f.alpha_composite(L, (0, 0)); f.alpha_composite(R, (960, 0))
        d = ImageDraw.Draw(f); d.line([(960, 0), (960, H)], fill=INK, width=8)
        fig(f, JAKE45, 380, 882, 76, lt, 1, "frown", 0.12, ("down", "desk"), seated=True, seed=1)
        put(f, S("tbl3", lambda c: (PR.Pen(c).rect(200, 820, 760, 846, (150, 108, 74), 3), PR.Pen(c).rect(230, 846, 260, 1010, (120, 86, 60), 2.6), PR.Pen(c).rect(700, 846, 730, 1010, (120, 86, 60), 2.6))))
        put(f, S("notice", lambda c: PR.document(c, 600, 790, 220, 150, "FINAL NOTICE", "Balance due: $8,940", 4, 3, stamp="OVERDUE")))
        fig(f, RYAN45, 1560, 1040, 86, lt, -1, "smile", 0.0, ("hip", "down"), seed=2)
        put(f, S("ryan_lap", lambda c: PR.laptop(c, 1220, 900, 260, lambda p, *a: PR.invest_screen(p, *a, "$1,240,000"))))
        label(f, "MILLIONAIRE", 1440, 120, 70, (255, 214, 60), (lt - 0.3) / 0.4)
        label(f, "STILL RENTING", 480, 120, 64, (255, 110, 100), (lt - 2.6) / 0.4)
    else:
        l2 = lt - 9.6; f.alpha_composite(copybg("pinboard"))
        qs = [("WHERE DOES MONEY COME FROM?", 4.0), ("WHO GETS IT FIRST?", 6.0), ("WHY RICH vs. POOR?", 7.4)]
        for i, (q, tq) in enumerate(qs): sticky(f, q, 960, 300 + i * 230, (l2 - tq) / 0.3, (-3, 2, -2)[i], 56)

def s_B4(f, lt, T):
    f.alpha_composite(LEDGER.frame(lt + 30).convert("RGBA"))
    put(f, S("bill_t", lambda c: PR.real_bill(c, 960, 700, 380, value="100")))
    label(f, "HOW MONEY", 960, 330, 130, (255, 255, 255), lt / 0.4, 9); label(f, "REALLY WORKS", 960, 470, 130, (255, 214, 60), (lt - 0.25) / 0.4, 9)

def s_B5(f, lt, T):            # Jake betritt die Bank und geht zum Schalter
    f.alpha_composite(copybg("bank"))
    fig(f, TELLER, 1290, 572, 50, lt, -1, "smile", 0.0, ("desk", "desk"), seated=True, seed=3); fg(f, "bank", (250, 518, 1672, 822))
    x = -100 + min(1, lt / 4.4) * 820
    fig(f, JAKE, x, 1040, 92, lt, 1, "smile", 0.0, ("down", "hold") if lt > 4.4 else ("down", "down"), walk=lt if lt < 4.4 else None, seed=4)
    if lt > 4.4: put(f, S("pc_hand", lambda c: PR.paycheck(c, 860, 760, 160, "Jake", "$100")))

def s_B6(f, lt, T):            # Schalter-Dialog, Schein geht ueber den Tresen; dann App = Versprechen
    if lt < 7.8:
        f.alpha_composite(copybg("bank_counter"))
        fig(f, TELLER, 1240, 790, 120, lt, -1, "smile", 0.0, ("desk", "down"), seated=True, seed=5); fg(f, "bank_counter", (0, 698, W, H))
        fig(f, JAKE, 520, 1200, 130, lt, 1, "smile", 0.0, ("give", "down"), seed=6)
        k = ease((lt - 3.4) / 0.9); put(f, S("bill_c", lambda c: PR.real_bill(c, 800, 700, 260, value="100")), 300 * k, 0)
        bubble(f, "All safe with us!", 1250, 230, (lt - 0.8) / 0.3, (-60, 80))
        bubble(f, "Great, thanks!", 560, 300, (lt - 2.3) / 0.3, (60, 80))
    else:
        l2 = lt - 7.8; f.alpha_composite(copybg("studio", (214, 220, 230)))
        put(f, S("ph_promise", lambda c: PR.phone(c, 960, 520, 720, "MY BANK", "Balance", "$100", glow=True)))
        label(f, "A PROMISE. NOT CASH.", 960, 960, 64, (255, 255, 255), (l2 - 4.0) / 0.4)

def s_B7(f, lt, T):            # Garderobe: Mantel abgeben, Marke, Garderobier verleiht den Mantel
    f.alpha_composite(copybg("coatcheck"))
    fig(f, CROWD[4], 1100, 600, 60, lt, -1, "smile" if lt < 7 else "grin", 0.0, ("desk", "desk") if lt < 6.5 else ("give", "down"), seated=True, seed=7); fg(f, "coatcheck", (200, 518, 1722, 862))
    if lt < 6.0:
        fig(f, JAKE, 620 - (max(0, lt - 3.6) * 260), 1040, 90, lt, 1 if lt < 3.6 else -1, "smile", 0.0, ("give", "down") if lt < 3.0 else ("down", "hold"), walk=(lt if lt > 3.6 else None), seed=8)
        if lt > 2.2: sticky(f, "TICKET #42", 620 - max(0, lt - 3.6) * 260, 600, (lt - 2.2) / 0.3, 4, 34)
    else:
        fig(f, STRANGER, 700, 1040, 90, lt, 1, "grin", 0.0, ("give", "down"), seed=9)
        label(f, "+ $ FEE", 1100, 220, 70, (255, 214, 60), (lt - 8.2) / 0.4)

def s_B8(f, lt, T):            # Autohaus: Fremder bekommt den Schluessel; 8 % Zinsen
    f.alpha_composite(copybg("dealer"))
    put(f, S("car_red", lambda c: car(PR.Pen(c), 560, 900, 820, (200, 40, 44))))
    fig(f, BANKER, 1580, 1040, 86, lt, -1, "smile", 0.0, ("give", "down") if lt < 3.0 else ("down", "down"), seed=10)
    fig(f, STRANGER, 1330, 1040, 86, lt, 1, "grin", 0.0, ("give", "down") if 1.6 < lt < 3.4 else ("down", "wave" if lt > 3.4 else "down"), seed=11)
    label(f, "CAR LOAN: 8% INTEREST", 960, 160, 64, (255, 255, 255), (lt - 3.2) / 0.4)
    if lt > 6.2:
        label(f, "JAKE EARNS: ~0%", 960, 270, 52, (255, 110, 100), (lt - 6.2) / 0.4); label(f, "BANK KEEPS: THE DIFFERENCE", 960, 360, 52, (255, 214, 60), (lt - 7.4) / 0.4)

def _sleeping(c):
    sp = Image.new("RGBA", (W * SS, H * SS)); figure(sp, 960, 900, 56, JAKE, 1, "line", 0.0, ("down", "down"), "stand", 0, "closed")
    sp = sp.rotate(90, center=(960 * SS, 700 * SS), resample=Image.BICUBIC); c.alpha_composite(sp, (-1060 * SS + 960 * SS - 520 * SS + 120 * SS, -60 * SS))

def s_B9(f, lt, T):            # Jake schlaeft, Handy leuchtet; Schnitt: fast leerer Tresor
    if lt < 5.4:
        f.alpha_composite(copybg("bedroom"))
        put(f, S("sleepjake", lambda c: (lambda p: (p.ell(390, 610, 70, 66, JAKE["skin"], 3.4), p.arc(410, 612, 9, 6, 0, 180, 3), p.arc(440, 612, 9, 6, 0, 180, 3),
                                                     p.poly([(318, 570), (460, 548), (420, 600), (340, 620)], JAKE["hair"], 3)))(PR.Pen(c))))
        put(f, S("blanket2", lambda c: PR.Pen(c).poly([(440, 600), (1100, 612), (1110, 722), (440, 722)], (90, 120, 170), 3)))
        put(f, S("ph_night", lambda c: PR.phone(c, 76, 520, 120, "MY BANK", "", "$100", glow=True)))
        label(f, "z", 500 + math.sin(lt * 2) * 6, 520 - (lt * 20) % 60, 46, (255, 255, 255), 1.0, 4)
    else:
        l2 = lt - 5.4; f.alpha_composite(copybg("vault_inside"))
        put(f, S("tiny_cash", lambda c: PR.real_bill(c, 1300, 400, 120, value="100")))
        label(f, "LEGAL RESERVE REQUIREMENT?", 960, 160, 60, (255, 255, 255), (l2 - 0.4) / 0.4)

def s_B10(f, lt, T):           # 0 % auf der Tresortuer; 1930er Bank-Run; FDIC; Kreditschoepfung
    if lt < 4.8:
        f.alpha_composite(copybg("vault")); label(f, "0%", 960, 540, 330, (255, 90, 80), lt / 0.25, 14)
        label(f, "SINCE MARCH 2020", 960, 900, 54, (255, 255, 255), (lt - 0.8) / 0.4)
    elif lt < 13.0:
        l2 = lt - 4.8; base = copybg("wallstreet"); g = base.convert("L").convert("RGB"); f.alpha_composite(Image.blend(g, Image.new("RGB", (W, H), (150, 120, 80)), 0.25).convert("RGBA"))
        for i in range(9): fig(f, CROWD[i % 5], 200 + i * 190, 1060, 62, lt, -1 if i % 2 else 1, "o" if i % 3 == 0 else "worried", 0.1, ("up", "down") if i % 2 else ("down", "wave"), seed=20 + i)
        label(f, "1930s: THOUSANDS OF BANKS COLLAPSE", 960, 120, 56, (255, 255, 255), (l2 - 0.5) / 0.4)
    elif lt < 19.0:
        l2 = lt - 13.0; f.alpha_composite(copybg("bank")); fig(f, JAKE, 960, 1010, 70, lt, 1, "smile", 0.0, ("down", "down"), seed=21)
        label(f, "INSURED UP TO $250,000", 960, 270, 64, (255, 214, 60), (l2 - 0.4) / 0.4)
    else:
        l2 = lt - 19.0; f.alpha_composite(copybg("studio", (30, 30, 36)))
        put(f, S("bill_q", lambda c: PR.real_bill(c, 960, 560, 420, value="100")), 0, 0, 1 - ease(l2 / 2.5))
        label(f, "MONEY THAT NEVER EXISTED", 960, 860, 70, (255, 214, 60), (l2 - 2.8) / 0.4)

def s_B11(f, lt, T):           # Ryan im Kreditbuero
    f.alpha_composite(copybg("loan_office"))
    fig(f, RYAN, 640, 862, 74, lt, 1, "smile", 0.0, ("desk", "down"), seated=True, seed=30)
    fig(f, BANKER, 1280, 862, 74, lt, -1, "grin" if lt > 3.0 else "smile", 0.0, ("desk", "down") if lt < 3 else ("desk", "point"), seated=True, seed=31)
    put(f, S("desk_l", lambda c: (PR.Pen(c).rect(560, 800, 1360, 830, (150, 108, 74), 3), PR.Pen(c).rect(580, 830, 1340, 1060, (130, 92, 62), 3))))
    put(f, S("house_brochure", lambda c: (PR.Pen(c).rect(830, 740, 1090, 800, (250, 250, 246), 2.6), house(PR.Pen(c), 880, 796, 200))))
    bubble(f, "I'd need $300,000.", 560, 300, (lt - 0.6) / 0.3, (40, 90)); bubble(f, "No problem.", 1380, 330, (lt - 3.0) / 0.3, (-40, 90))

def s_B12(f, lt, T):           # Bildschirm: tippt $300,000 aus dem Nichts
    f.alpha_composite(copybg("screen")); d = ImageDraw.Draw(f)
    d.text((960, 300), "Account: RYAN  ·  Mortgage", font=ImageFont.truetype(SANS, 46), fill=(70, 76, 90), anchor="mm")
    v = 0 if lt < 4.2 else 300000 * inout((lt - 4.2) / 0.8)
    d.text((960, 500), f"${v:,.0f}", font=ImageFont.truetype(BOLD, 170), fill=(40, 140, 80) if v > 0 else INK, anchor="mm")
    if 1.8 < lt < 4.2:
        cur = "".join("300000"[:int((lt - 1.8) / 0.35) + 1]); d.rectangle([700, 640, 1220, 720], outline=INK, width=4); d.text((720, 680), "$" + cur + ("|" if int(lt * 3) % 2 else ""), font=ImageFont.truetype(MONO, 54), fill=INK, anchor="lm")
    label(f, "1 SECOND AGO, THIS DIDN'T EXIST", 960, 800, 56, (255, 120, 60), (lt - 6.4) / 0.4)
    if lt > 11.0: label(f, "REPAID → IT DISAPPEARS", 960, 1030, 50, (255, 255, 255), (lt - 11.0) / 0.4)

def s_B13(f, lt, T):           # Bank of England Dokument
    f.alpha_composite(copybg("desk_paper"))
    put(f, S("boe", lambda c: PR.document(c, 960, 560, 880, 900, "Money creation in the modern economy", "Bank of England · Quarterly Bulletin 2014 Q1", 14, 7)))
    k = ease((lt - 3.0) / 1.6); ImageDraw.Draw(f, "RGBA").rectangle([560, 610, 560 + 800 * k, 690], fill=(255, 226, 80, 150))
    if k > 0: ImageDraw.Draw(f).text((960, 650), "“...commercial banks create money when they make loans.”", font=ImageFont.truetype(SERIF, 30), fill=INK, anchor="mm")

def s_B13b(f, lt, T):          # Nixon im Oval Office 1971; dann Fernseher; dann Gold hinter Gittern
    if lt < 8.4:
        f.alpha_composite(copybg("oval")); fig(f, NIXON, 960, 706, 62, lt, 0, "talk" if int(lt * 4) % 2 else "line", 0.05, ("desk", "desk"), seated=True, seed=40)
        put(f, S("desk_front", lambda c: (PR.Pen(c).rect(560, 640, 1360, 690, (110, 70, 44), 3.4), PR.Pen(c).rect(580, 690, 1340, 900, (96, 60, 38), 3.4), PR.Pen(c).ell(960, 790, 54, 40, (196, 160, 80), 2.6))))
        put(f, S("tvcam", lambda c: PR.tv_camera(c, 260, 1060)))
        label(f, "AUGUST 15, 1971", 960, 90, 60, (255, 255, 255), (lt - 0.4) / 0.4)
    elif lt < 16.0:
        l2 = lt - 8.4; f.alpha_composite(copybg("apartment", True))
        def inner(p, x0, y0, x1, y1):
            p.vgrad(x0, y0, x1, y1, (150, 150, 150), (90, 90, 90)); p.ell((x0 + x1) / 2, y0 + (y1 - y0) * 0.45, 60, 64, (200, 200, 200), 3); p.rect((x0 + x1) / 2 - 90, y0 + (y1 - y0) * 0.65, (x0 + x1) / 2 + 90, y1, (70, 70, 70), 3)
        put(f, S("tv71", lambda c: PR.tv_set(c, 960, 560, 760, inner)))
        label(f, "DOLLAR NO LONGER EXCHANGEABLE FOR GOLD", 960, 960, 50, (255, 214, 60), (l2 - 1.0) / 0.4)
    else:
        l2 = lt - 16.0; f.alpha_composite(copybg("studio", (40, 40, 46)))
        put(f, S("gold", lambda c: [PR.gold_bar(c, 640 + (k % 3) * 210, 700 - (k // 3) * 70) for k in range(6)]))
        d = ImageDraw.Draw(f); k = ease(l2 / 1.0)
        for x in range(560, 1380, 70): d.line([(x, 300), (x, 300 + 520 * k)], fill=(90, 94, 102), width=14)
        label(f, "BACKED BY: TRUST", 960, 940, 72, (255, 255, 255), (l2 - 2.2) / 0.4)

def s_B14(f, lt, T):           # Bargeld vs. Zahlen auf Bildschirmen
    f.alpha_composite(copybg("studio"))
    put(f, S("stack", lambda c: PR.cash_stack(c, 420, 780, 5, 260)))
    put(f, S("bigscreen", lambda c: (PR.Pen(c).rect(820, 180, 1760, 820, (30, 32, 36), 4, r=16), PR.Pen(c).vgrad(840, 200, 1740, 800, (20, 40, 30), (10, 24, 18)))))
    d = ImageDraw.Draw(f); fnt = ImageFont.truetype(MONO, 30)
    for r_ in range(15):
        for c_ in range(4):
            v = (r_ * 7919 + c_ * 104729 + int(lt * 6) * 13) % 9999999; d.text((870 + c_ * 220, 220 + r_ * 38), f"${v:,}", font=fnt, fill=(80, 220, 130))
    label(f, "CASH: ~1 IN 10", 420, 300, 56, (255, 214, 60), (lt - 1.0) / 0.4); label(f, "THE REST: NUMBERS", 1290, 120, 56, (255, 255, 255), (lt - 3.4) / 0.4)

def _chart(f, x0, y0, x1, y1, pts, k, col=(60, 160, 90), lw=8, labels=None):
    d = ImageDraw.Draw(f); d.line([(x0, y1), (x1, y1)], fill=INK, width=4); d.line([(x0, y0), (x0, y1)], fill=INK, width=4)
    n = max(2, int(len(pts) * k)); P_ = [(x0 + (x1 - x0) * px, y1 - (y1 - y0) * py) for px, py in pts[:n]]
    if len(P_) > 1: d.line(P_, fill=INK, width=lw + 5, joint="curve"); d.line(P_, fill=col, width=lw, joint="curve")

def s_B15(f, lt, T):           # Federal Reserve, Bilanz 4 -> 9 Billionen
    if lt < 6.0:
        f.alpha_composite(copybg("fed")); label(f, "THE BANK OF THE BANKS", 960, 900, 64, (255, 255, 255), (lt - 2.0) / 0.4)
    else:
        l2 = lt - 6.0; f.alpha_composite(copybg("studio"))
        pts = [(i / 40, 0.35 + (0.0 if i < 8 else min(0.5, (i - 8) * 0.035)) + math.sin(i) * 0.004) for i in range(41)]
        _chart(f, 300, 200, 1620, 860, pts, ease(l2 / 4.0))
        ImageDraw.Draw(f).text((300, 900), "2020", font=ImageFont.truetype(SANS, 40), fill=INK, anchor="mm"); ImageDraw.Draw(f).text((1620, 900), "2022", font=ImageFont.truetype(SANS, 40), fill=INK, anchor="mm")
        label(f, "$4 TRILLION", 500, 540, 50, (255, 255, 255), (l2 - 0.3) / 0.4); label(f, "≈ $9 TRILLION", 1450, 170, 56, (255, 214, 60), (l2 - 4.2) / 0.4)
        if l2 > 9.0: label(f, "WHO GETS IT FIRST?", 960, 1000, 64, (255, 110, 100), (l2 - 9.0) / 0.4)

def s_B16(f, lt, T):           # Brunnen-Kaskade: oben trinken die Ersten
    f.alpha_composite(copybg("studio", (214, 222, 232))); d = ImageDraw.Draw(f, "RGBA")
    tiers = [(960, 260, 140, "BANKS"), (960, 470, 300, "BIG INVESTORS"), (960, 680, 460, "THE ALREADY RICH")]
    for x, y, w, lab in tiers:
        d.polygon([(x - w, y), (x + w, y), (x + w * 0.85, y + 60), (x - w * 0.85, y + 60)], fill=(200, 210, 222), outline=INK); d.rectangle([x - w + 6, y + 4, x + w - 6, y + 20], fill=(100, 170, 230))
        label(f, lab, x, y + 30, 34, (255, 255, 255), 1.0, 4)
    for k in range(14):
        yy = 60 + ((lt * 300 + k * 40) % 200); d.ellipse([952, yy, 968, yy + 22], fill=(100, 170, 230), outline=INK)
    for side in (-1, 1):
        for k in range(8):
            yy = 340 + ((lt * 260 + k * 50) % 340); d.ellipse([960 + side * 300 - 6, yy, 960 + side * 300 + 6, yy + 16], fill=(100, 170, 230))
    fig(f, JAKE, 960, 1060, 54, lt, 0, "worried", 0.1, ("hold", "down"), seed=50)
    d.polygon([(1010, 880), (1050, 880), (1044, 940), (1016, 940)], fill=(220, 236, 246, 200), outline=INK); d.rectangle([1018, 930, 1042, 938], fill=(100, 170, 230))
    label(f, "JAKE", 960, 1020, 34, (255, 255, 255), 1.0, 4)
    for i, (x, y) in enumerate(((800, 230), (1120, 230), (700, 440), (1220, 440))):
        fig(f, (BANKER, BILLIONAIRE)[i % 2], x, y + 30, 26, lt, 1 if x < 960 else -1, "grin", 0.0, ("hold", "down"), seed=51 + i, idle=False)

def s_B17(f, lt, T):           # Richard Cantillon, 1730er
    if lt < 6.8:
        f.alpha_composite(copybg("study1730"))
        fig(f, CANTILLON, 960, 822, 76, lt, 1, "smile", 0.0, ("desk", "chin"), seated=True, seed=60)
        put(f, S("desk1730", lambda c: (PR.Pen(c).rect(800, 760, 1500, 790, (90, 60, 40), 3), PR.Pen(c).rect(820, 790, 1480, 1000, (70, 46, 30), 3), PR.Pen(c).rect(1100, 720, 1240, 760, (250, 240, 210), 2))))
        put(f, S("candle", lambda c: (PR.Pen(c).rect(1380, 660, 1400, 760, (250, 246, 230), 2), PR.Pen(c).ell(1390, 648, 8, 14, (255, 200, 80), 2))))
        label(f, "RICHARD CANTILLON · 1730s", 960, 110, 56, (255, 255, 255), (lt - 0.6) / 0.4)
    else:
        l2 = lt - 6.8; f.alpha_composite(copybg("studio"))
        put(f, S("tag_old", lambda c: PR.price_tag(c, 560, 540, "$100", (220, 244, 220), INK, 110)), 0, 0, ease(l2 / 0.4))
        put(f, S("tag_new", lambda c: PR.price_tag(c, 1360, 540, "$125", (255, 226, 220), INK, 110)), 0, 0, ease((l2 - 2.4) / 0.4))
        label(f, "FIRST IN LINE: OLD PRICES", 560, 300, 40, (60, 160, 90), (l2 - 0.2) / 0.4); label(f, "LAST IN LINE: NEW PRICES", 1360, 300, 40, (220, 70, 60), (l2 - 2.6) / 0.4)

def s_B18(f, lt, T):           # 2020: +25 % Geldmenge, Hauspreise +40 %, Milliardaere +1 Billion
    if lt < 6.2:
        f.alpha_composite(copybg("studio")); pts = [(i / 30, 0.3 + (0 if i < 6 else min(0.42, (i - 6) * 0.05))) for i in range(31)]
        _chart(f, 300, 220, 1620, 860, pts, ease(lt / 2.6)); label(f, "+25% DOLLARS IN ONE YEAR", 960, 140, 60, (255, 214, 60), (lt - 2.2) / 0.4)
    elif lt < 12.0:
        l2 = lt - 6.2; f.alpha_composite(copybg("street", "day"))
        put(f, S("tag_h1", lambda c: PR.price_tag(c, 480, 260, "$300,000")), 0, 0, 1 - ease((l2 - 1.6) / 0.3))
        put(f, S("tag_h2", lambda c: PR.price_tag(c, 480, 260, "$420,000", (255, 236, 200))), 0, 0, ease((l2 - 1.6) / 0.3))
        label(f, "HOME PRICES +40% IN 2 YEARS", 1440, 160, 54, (255, 255, 255), (l2 - 2.2) / 0.4)
    else:
        l2 = lt - 12.0; f.alpha_composite(copybg("glass_office")); fig(f, BILLIONAIRE, 960, 1040, 90, lt, 0, "grin", 0.0, ("hip", "hip"), seed=70)
        label(f, "BILLIONAIRES: +$1 TRILLION", 960, 160, 70, (255, 214, 60), (l2 - 0.6) / 0.4)

def s_B19(f, lt, T):           # Supermarktkasse
    f.alpha_composite(copybg("supermarket"))
    fig(f, CROWD[2], 1620, 1000, 72, lt, -1, "smile", 0.0, ("down", "give"), seed=80)
    fig(f, JAKE, 700, 1080, 86, lt, 1, "o" if lt > 4.8 else "line", 0.15 if lt > 4.8 else 0, ("down", "down"), seed=81)
    put(f, S("groceries", lambda c: PR.basket(c, 1040, 760, 1.0, 220)))
    d = ImageDraw.Draw(f); tot = 38.4 if lt < 1.2 else (61.9 if lt < 2.4 else 87.35)
    d.rectangle([1320, 580, 1500, 680], fill=(20, 30, 24)); d.text((1410, 630), f"${tot:.2f}", font=ImageFont.truetype(MONO, 40), fill=(80, 255, 150), anchor="mm")
    bubble(f, "Wait... how much?", 720, 300, (lt - 4.8) / 0.3, (20, 90))

def s_B19b(f, lt, T):          # Chef: +3 %; Vermieter: Miete +8 %
    if lt < 9.4:
        f.alpha_composite(copybg("boss"))
        fig(f, BOSS, 1380, 782, 76, lt, -1, "grin", 0.0, ("desk", "point"), seated=True, seed=90)
        put(f, S("desk_b", lambda c: (PR.Pen(c).rect(900, 720, 1700, 750, (120, 80, 56), 3), PR.Pen(c).rect(920, 750, 1680, 1000, (100, 66, 46), 3))))
        fig(f, JAKE, 600, 1040, 92, lt, 1, "grin", 0.0, ("down", "down"), seed=91)
        bubble(f, "Great year! 3% raise!", 1360, 260, (lt - 0.5) / 0.3, (-40, 90)); bubble(f, "Thanks!", 640, 330, (lt - 2.6) / 0.3, (30, 80))
    else:
        l2 = lt - 9.4; f.alpha_composite(copybg("desk_paper"))
        put(f, S("rent_letter", lambda c: PR.document(c, 960, 520, 700, 760, "NOTICE OF RENT INCREASE", "Effective next month", 8, 11, big="RENT +8%")))
        label(f, "RAISE +3%  <  RENT +8%", 960, 990, 66, (255, 110, 100), (l2 - 3.2) / 0.4)

def s_B20(f, lt, T):           # 100 $ aus 2000 vs. heute
    f.alpha_composite(copybg("table"))
    put(f, S("bill20", lambda c: PR.real_bill(c, 960, 380, 420, value="100")))
    put(f, S("bask_full", lambda c: PR.basket(c, 560, 940, 1.0, 360)), 0, 0, ease((lt - 1.0) / 0.4)); put(f, S("bask_half", lambda c: PR.basket(c, 1360, 940, 0.5, 360)), 0, 0, ease((lt - 3.0) / 0.4))
    label(f, "2000", 560, 620, 60, (255, 255, 255), (lt - 1.0) / 0.4); label(f, "TODAY", 1360, 620, 60, (255, 255, 255), (lt - 3.0) / 0.4)
    label(f, "$100 → BUYS WHAT $55 DID", 960, 120, 60, (255, 214, 60), (lt - 4.6) / 0.4)

def s_B21(f, lt, T):           # Sparzins 0,4 % vs. Preise +3 %
    f.alpha_composite(copybg("studio"))
    put(f, S("ph_sav", lambda c: PR.phone(c, 600, 540, 640, "SAVINGS", "Interest rate", "0.4%", (40, 90, 160))))
    put(f, S("tag_inf", lambda c: PR.price_tag(c, 1340, 520, "PRICES +3%/YR", (255, 226, 220), (200, 40, 44), 64)), 0, 0, ease((lt - 3.2) / 0.4))
    if lt > 7.4: label(f, "= LOSING EVERY YEAR", 1340, 760, 62, (255, 110, 100), (lt - 7.4) / 0.4)

def s_B21b(f, lt, T):          # Pinnwand: zwei Haken, eine offene Frage
    f.alpha_composite(copybg("pinboard"))
    qs = ["WHERE DOES MONEY COME FROM?  ✓", "WHO GETS IT FIRST?  ✓", "WHY RICH vs. POOR?  ?"]
    for i, q in enumerate(qs): sticky(f, q, 960, 300 + i * 230, 1.0 if i < 2 else (lt - 5.0) / 0.3, (-3, 2, -2)[i], 56)

def s_B22(f, lt, T):           # Ryan richtet mit 25 den Dauerauftrag ein
    f.alpha_composite(copybg("ryan_apt"))
    fig(f, RYAN, 760, 822, 76, lt, 1, "smile", 0.0, ("desk", "desk"), seated=True, seed=100)
    put(f, S("desk_r", lambda c: (PR.Pen(c).rect(700, 760, 1500, 786, (150, 108, 74), 3), PR.Pen(c).rect(720, 786, 760, 1000, (120, 86, 60), 2.6), PR.Pen(c).rect(1440, 786, 1480, 1000, (120, 86, 60), 2.6))))
    put(f, S("lap_r", lambda c: PR.laptop(c, 1100, 760, 420, PR.invest_screen)))
    if lt > 4.2: label(f, "EVERY MONTH. AUTOMATIC.", 960, 140, 60, (255, 255, 255), (lt - 4.2) / 0.4)

def s_B23(f, lt, T):           # Zwei Linien ueber 20 Jahre
    f.alpha_composite(copybg("studio")); k = ease((lt - 5.0) / 7.0)
    pj = [(i / 40, 0.12 + i / 40 * 0.01) for i in range(41)]; pr_ = [(i / 40, 0.12 + 0.75 * ((1.1 ** (i / 2) - 1) / (1.1 ** 20 - 1)) + (-0.03 if i in (16, 17) else 0)) for i in range(41)]
    _chart(f, 300, 160, 1620, 880, pj, k, (200, 70, 60)); _chart(f, 300, 160, 1620, 880, pr_, k, (60, 160, 90))
    label(f, "$10,000 · 20 YEARS", 960, 90, 56, (255, 255, 255), (lt - 0.8) / 0.4)
    if lt > 13.0: label(f, "SAVINGS: $10,800", 1500, 780, 46, (220, 70, 60), (lt - 13.0) / 0.4)
    if lt > 15.5: label(f, "INDEX FUND: ~$67,000", 1350, 200, 54, (60, 160, 90), (lt - 15.5) / 0.4)
    ImageDraw.Draw(f).text((960, 1030), "Historical average, not guaranteed. Not financial advice.", font=ImageFont.truetype(SANSR, 26), fill=(90, 90, 96), anchor="mm")

def s_B24(f, lt, T):           # Jake unterschreibt den Autokredit
    f.alpha_composite(copybg("dealer")); put(f, S("car_blue", lambda c: car(PR.Pen(c), 980, 820, 760, (40, 90, 170))))
    fig(f, JAKE, 330, 878, 70, lt, 1, "grin", 0.0, ("down", "desk"), seated=True, seed=110); fig(f, BANKER, 790, 878, 70, lt, -1, "grin", 0.0, ("down", "desk"), seated=True, seed=111)
    put(f, S("desk_d", lambda c: (PR.Pen(c).rect(200, 820, 900, 846, (240, 240, 244), 3), PR.Pen(c).rect(240, 846, 270, 1010, (160, 160, 168), 2.6), PR.Pen(c).rect(830, 846, 860, 1010, (160, 160, 168), 2.6))))
    put(f, S("loan_doc", lambda c: PR.document(c, 560, 800, 200, 80, "AUTO LOAN", None, 2, 5)))
    if lt > 6.0: put(f, S("tag_car", lambda c: PR.price_tag(c, 1360, 360, "VALUE -20%", (255, 226, 220), (200, 40, 44))), 0, 0, ease((lt - 6.0) / 0.4))
    if lt > 10.5: label(f, "THINGS THAT SHRINK", 960, 120, 60, (255, 110, 100), (lt - 10.5) / 0.4)

def s_B25(f, lt, T):           # Briefkasten: Pre-approved
    f.alpha_composite(copybg("apt_building")); fig(f, JAKE, 1160, 1040, 90, lt, 1, "o" if lt > 2.6 else "line", 0.1, ("down", "give"), seed=120)
    if lt > 1.4: put(f, S("preapp", lambda c: PR.document(c, 960, 460, 520, 380, "PRE-APPROVED!", "Platinum Credit Card", 3, 9, big="$10,000")), 0, (1 - ease((lt - 1.4) / 0.5)) * 300, ease((lt - 1.4) / 0.4))

def s_B26(f, lt, T):           # Zwei Pfeile am Banktresen
    f.alpha_composite(copybg("bank_counter"))
    fig(f, TELLER, 1350, 790, 120, lt, -1, "grin", 0.0, ("desk", "down"), seated=True, seed=131); fg(f, "bank_counter", (0, 698, W, H))
    fig(f, JAKE, 400, 1200, 130, lt, 1, "worried", 0.1, ("down", "down"), seed=130)
    label(f, "→ SAVINGS: 0.4%  →", 900, 300, 60, (255, 255, 255), (lt - 1.6) / 0.4); label(f, "←  CARD: 21%  ←", 900, 460, 70, (255, 90, 80), (lt - 4.2) / 0.4)
    if lt > 8.5: label(f, "LOSING SIDE OF EVERY TRADE", 960, 1000, 60, (255, 214, 60), (lt - 8.5) / 0.4)

def s_B27(f, lt, T):           # Jake 35 am Kuechentisch, Rechnungen
    f.alpha_composite(copybg("kitchen_night"))
    fig(f, JAKE45, 860, 822, 76, lt, 1, "worried", 0.15, ("desk", "chin"), seated=True, seed=140)
    put(f, S("ktable", lambda c: (PR.Pen(c).rect(500, 760, 1500, 790, (130, 96, 66), 3), PR.Pen(c).rect(540, 790, 580, 1010, (110, 80, 56), 2.6), PR.Pen(c).rect(1420, 790, 1460, 1010, (110, 80, 56), 2.6))))
    put(f, S("bills_pile", lambda c: [PR.document(c, 1150 + k * 30, 720 - k * 12, 200, 120, "BILL", None, 3, k) for k in range(4)]))
    label(f, "$5,000 AT MINIMUM PAYMENTS: 10+ YEARS", 960, 120, 54, (255, 255, 255), (lt - 1.0) / 0.4)

def s_B28(f, lt, T):           # Milliardaer im Glasbuero
    f.alpha_composite(copybg("glass_office")); fig(f, BILLIONAIRE, 760, 1040, 92, lt, 1, "smile", 0.0, ("hip", "down"), seed=150)
    put(f, S("stock_tower", lambda c: [PR.document(c, 1300, 900 - k * 46, 300, 40, "STOCK", None, 0, k, (236, 244, 236)) for k in range(12)]))
    label(f, "$1,000,000,000 IN STOCK", 960, 120, 64, (255, 214, 60), (lt - 0.8) / 0.4)
    if lt > 3.4: label(f, "SELL = PAY TAX", 1300, 280, 54, (255, 110, 100), (lt - 3.4) / 0.4)

def s_B29(f, lt, T):           # Privatbank: leiht gegen Aktien. Buy. Borrow. Die.
    if lt < 13.0:
        f.alpha_composite(copybg("private_bank"))
        fig(f, BILLIONAIRE, 640, 781, 74, lt, 1, "smile", 0.0, ("desk", "down"), seated=True, seed=160); fig(f, BANKER, 1280, 781, 74, lt, -1, "grin", 0.0, ("desk", "down"), seated=True, seed=161)
        put(f, S("desk_pb", lambda c: (PR.Pen(c).rect(560, 720, 1360, 750, (90, 56, 36), 3), PR.Pen(c).rect(580, 750, 1340, 1000, (70, 44, 28), 3))))
        put(f, S("stocks_d", lambda c: PR.document(c, 860, 690, 220, 60, "STOCK", None, 0, 3, (236, 244, 236))))
        if lt > 4.0: put(f, S("loan_check", lambda c: PR.paycheck(c, 1080, 680, 280, "Mr. B", "$50,000,000")), 0, 0, ease((lt - 4.0) / 0.4))
        bubble(f, "Borrow whatever you like, sir.", 1380, 300, (lt - 1.2) / 0.3, (-60, 90))
        label(f, "A LOAN ISN'T INCOME → NO INCOME TAX", 960, 110, 50, (255, 255, 255), (lt - 5.6) / 0.4)
    else:
        l2 = lt - 13.0; f.alpha_composite(copybg("studio", (30, 30, 36)))
        for i, w_ in enumerate(("BUY.", "BORROW.", "DIE.")): label(f, w_, 960, 300 + i * 240, 150, (255, 214, 60) if i < 2 else (255, 110, 100), (l2 - 0.3 - i * 0.55) / 0.3, 9)

def s_B30(f, lt, T):           # Ryan auf der Veranda: Haus + Depot wachsen
    f.alpha_composite(copybg("porch", "day")); fig(f, RYAN45, 1500, 1040, 90, lt, -1, "smile", 0.0, ("hip", "down"), seed=170)
    put(f, S("tag_p1", lambda c: PR.price_tag(c, 1080, 220, "HOME: $310,000")), 0, 0, 1 - ease((lt - 3.0) / 0.4)); put(f, S("tag_p2", lambda c: PR.price_tag(c, 1080, 220, "HOME: $640,000", (220, 244, 220))), 0, 0, ease((lt - 3.0) / 0.4))
    if lt > 6.0: put(f, S("tag_p3", lambda c: PR.price_tag(c, 1080, 340, "SHARES: ↑", (220, 244, 220))), 0, 0, ease((lt - 6.0) / 0.4))
    if lt > 9.0: label(f, "JAKE: A CAR + A LIFESTYLE", 600, 140, 54, (255, 110, 100), (lt - 9.0) / 0.4)

def s_B31(f, lt, T):           # 2008: Bailout
    f.alpha_composite(copybg("wallstreet")); label(f, "2008", 960, 90, 90, (255, 255, 255), lt / 0.3)
    for i in range(6): fig(f, BANKER if i % 2 else BILLIONAIRE, 330 + i * 250, 1050, 50, lt, (-1) ** i, "worried" if lt < 6 else "grin", 0.1, ("up", "down") if lt < 6 else ("wave", "down"), seed=180 + i)
    if lt > 6.0:
        d = ImageDraw.Draw(f); d.rectangle([260, 380, 1660, 560], fill=(250, 248, 240), outline=INK, width=5)
        d.text((960, 430), "THE DAILY NEWS", font=ImageFont.truetype(SERIF, 40), fill=INK, anchor="mm"); d.text((960, 505), "BANKS BAILED OUT: $700 BILLION", font=ImageFont.truetype(BOLD, 60), fill=(180, 30, 36), anchor="mm")

def s_B32(f, lt, T):           # 2023: SVB; dann Jakes Karte – keine Rettung
    if lt < 11.6:
        f.alpha_composite(copybg("svb")); label(f, "2023", 960, 70, 80, (255, 255, 255), lt / 0.3)
        for i in range(10): fig(f, CROWD[i % 5], 120 + i * 190, 1060, 48, lt, 1, "worried" if lt < 5 else "smile", 0.1, ("down", "phone"), seed=190 + i)
        if lt > 4.6: sticky(f, "ALL DEPOSITS PROTECTED", 960, 330, (lt - 4.6) / 0.3, 2, 54)
    else:
        l2 = lt - 11.6; f.alpha_composite(copybg("studio", (30, 30, 36)))
        put(f, S("cc21", lambda c: PR.credit_card(c, 960, 500, 640)))
        label(f, "21% INTEREST", 960, 860, 70, (255, 110, 100), (l2 - 0.6) / 0.4); label(f, "NO RESCUE", 960, 980, 60, (255, 255, 255), (l2 - 2.6) / 0.4)

def s_B32b(f, lt, T):          # Fed senkt Zinsen, Kurse steigen
    if lt < 8.6:
        f.alpha_composite(copybg("fedroom"))
        for i in range(5): fig(f, (BANKER, BOSS, BILLIONAIRE)[i % 3], 420 + i * 270, 960, 52, lt, 0, "line", 0.0, ("desk", "desk"), seated=True, seed=200 + i)
        label(f, "INTEREST RATES → 0%", 960, 500, 70, (255, 214, 60), (lt - 1.8) / 0.4)
    else:
        l2 = lt - 8.6; f.alpha_composite(copybg("studio")); pts = [(i / 30, 0.2 + i / 30 * 0.6 + math.sin(i * 1.3) * 0.02) for i in range(31)]
        _chart(f, 300, 220, 1620, 860, pts, ease(l2 / 3.0)); label(f, "STOCKS + HOUSES ↑", 960, 140, 64, (60, 160, 90), (l2 - 1.0) / 0.4)
        if l2 > 5.0: label(f, "RESCUED TWICE", 960, 960, 70, (255, 214, 60), (l2 - 5.0) / 0.4)

def s_B33(f, lt, T):           # Muenzwurf, dann die drei Antworten
    if lt < 5.0:
        f.alpha_composite(copybg("table")); h = math.sin(min(1, lt / 1.4) * math.pi) * 380
        sc = abs(math.cos(lt * 14)) if lt < 1.4 else 1.0
        put(f, S("coin_h", lambda c: PR.coin(c, 960, 640, 120, "HEADS")), 0, -h)
        label(f, "HEADS: THEY WIN", 600, 200, 60, (255, 214, 60), (lt - 1.8) / 0.4); label(f, "TAILS: YOU PAY", 1320, 200, 60, (255, 110, 100), (lt - 2.8) / 0.4)
    else:
        l2 = lt - 5.0; f.alpha_composite(copybg("pinboard"))
        ans = [("MONEY COMES FROM: LOANS", 0.6), ("FIRST IN LINE: THE BANKS", 3.4), ("RICH vs. POOR: ...?", 6.4)]
        for i, (q, tq) in enumerate(ans): sticky(f, q, 960, 300 + i * 230, (l2 - tq) / 0.3, (-3, 2, -2)[i], 56)

def s_B34(f, lt, T):           # Der Schein, zwei Haende von zwei Seiten
    f.alpha_composite(copybg("table")); put(f, S("bill34", lambda c: PR.real_bill(c, 960, 640, 520, value="100")))
    kj = ease((lt - 1.0) / 1.2); kr = ease((lt - 6.0) / 1.2)
    put(f, S("hand_j", lambda c: PR.hand(c, 640, 680, (196, 62, 54), (242, 206, 172), "left", 700)), -500 * (1 - kj), 0)
    put(f, S("hand_r", lambda c: PR.hand(c, 1280, 680, (48, 66, 100), (146, 98, 68), "right", 700)), 500 * (1 - kr), 0)
    label(f, "SPEND / PARK", 480, 300, 54, (255, 110, 100), (lt - 2.0) / 0.4); label(f, "A TOOL", 1440, 300, 60, (255, 214, 60), (lt - 6.6) / 0.4)

def s_B35(f, lt, T):           # Drei Regel-Karten
    f.alpha_composite(copybg("table"))
    for i, (txt, tc) in enumerate((("OWN THINGS THAT GROW", 1.2), ("AVOID HIGH-INTEREST DEBT", 4.2), ("DON'T LET CASH ROT", 7.6))):
        k = ease((lt - tc) / 0.4)
        if k > 0:
            put(f, S(("card", i), lambda c, i=i: PR.document(c, 400 + i * 560, 640, 500, 320, "", None, 0, i)), 0, (1 - k) * -400, k)
            if k > 0.9:
                ws = {"OWN THINGS THAT GROW": ["OWN THINGS", "THAT GROW"], "AVOID HIGH-INTEREST DEBT": ["AVOID", "HIGH-INTEREST DEBT"], "DON'T LET CASH ROT": ["DON'T LET", "CASH ROT"]}[txt]
                for j, wline in enumerate(ws): label(f, wline, 400 + i * 560, 640 + (j - (len(ws) - 1) / 2) * 62, 36, INK, 1.0, 0)
    ImageDraw.Draw(f).text((960, 1030), "This is not financial advice.", font=ImageFont.truetype(SANSR, 28), fill=(220, 210, 200), anchor="mm")

def s_B36(f, lt, T):           # Veranda am Abend: Ist es zu spaet?
    f.alpha_composite(copybg("porch", "sunset")); fig(f, JAKE45, 800, 1040, 90, lt, 1, "worried", 0.1, ("down", "down"), seed=210); fig(f, RYAN45, 1320, 1040, 90, lt, -1, "smile", 0.0, ("down", "point"), seed=211)
    bubble(f, "Is it too late for me?", 820, 300, (lt - 0.3) / 0.3, (20, 90), 38)
    bubble(f, "Best time: 20 years ago. Second best: today.", 1240, 140, (lt - 2.2) / 0.3, (40, 120), 34)

def s_B36b(f, lt, T):          # Jake startet: Karte zerschneiden, Dauerauftrag
    f.alpha_composite(copybg("apartment", False))
    fig(f, JAKE45, 760, 842, 76, lt, 1, "smile" if lt > 8 else "line", 0.0, ("desk", "desk"), seated=True, seed=220)
    put(f, S("tbl36", lambda c: (PR.Pen(c).rect(700, 780, 1500, 806, (150, 108, 74), 3), PR.Pen(c).rect(730, 806, 760, 1010, (120, 86, 60), 2.6), PR.Pen(c).rect(1440, 806, 1470, 1010, (120, 86, 60), 2.6))))
    if lt < 6.0:
        k = ease((lt - 2.4) / 0.3)
        put(f, S("cc_l", lambda c: PR.credit_card(c, 1100, 700, 300)), -40 * k, 30 * k, 1.0, 1.0, -12 * k)
        label(f, "PAY OFF THE CARD", 960, 140, 60, (255, 255, 255), (lt - 0.6) / 0.4)
    else:
        put(f, S("lap_j", lambda c: PR.laptop(c, 1100, 780, 420, PR.invest_screen)))
        if lt > 11.0: label(f, "$500/MONTH · 20 YEARS → $300,000+*", 960, 130, 54, (255, 214, 60), (lt - 11.0) / 0.4)
        ImageDraw.Draw(f).text((960, 1040), "*Historical average, not guaranteed. Not financial advice.", font=ImageFont.truetype(SANSR, 26), fill=(80, 80, 86), anchor="mm")

def s_B36c(f, lt, T):          # Sonnenuntergang auf der Strasse vom Anfang
    f.alpha_composite(copybg("street", "sunset")); fig(f, JAKE45, 780, 1040, 84, lt, 1, "smile", 0.0, ("down", "down"), seed=230); fig(f, RYAN45, 1160, 1040, 84, lt, -1, "smile", 0.0, ("down", "down"), seed=231)
    label(f, "DIFFERENT RULES.", 960, 150, 80, (255, 255, 255), (lt - 2.4) / 0.4)

def s_B37(f, lt, T):           # Endkarte mit Abo-Klick
    f.alpha_composite(LEDGER.frame(lt + 80).convert("RGBA"))
    label(f, "ARC", 960, 330, 200, (255, 255, 255), lt / 0.4, 10); label(f, "Most people never will.", 960, 480, 50, (210, 210, 216), (lt - 0.5) / 0.4, 0, HAND)
    d = ImageDraw.Draw(f); clicked = lt > 2.6
    d.rounded_rectangle([760, 600, 1160, 700], 50, fill=(90, 90, 96) if clicked else (220, 30, 36), outline=INK, width=4)
    d.text((960, 650), "SUBSCRIBED" if clicked else "SUBSCRIBE", font=ImageFont.truetype(BOLD, 44), fill=(255, 255, 255), anchor="mm")
    k = ease((lt - 1.0) / 1.4); cx, cy = 1500 - 450 * k, 900 - 230 * k
    d.polygon([(cx, cy), (cx + 34, cy + 80), (cx + 46, cy + 50), (cx + 78, cy + 44)], fill=(255, 255, 255), outline=INK)

SCENES = {k[2:]: v for k, v in globals().items() if k.startswith("s_B")}

# ======================= SOUNDS: nur an sichtbaren Aktionen =======================
CUES = {   # beat: [(Zeit in der Szene s, sound, lautstaerke)]
 "B0": [(0.95, "paper", 0.45)], "B1": [(k * 1.0, "steps", 0.12) for k in range(1, 6)] + [(9.95, "paper", 0.25), (10.25, "paper", 0.22)],
 "B3": [(0.0, "stinger", 0.28)], "B4": [(0.0, "impact", 0.55)],
 "B5": [(0.05, "doorbell", 0.3)] + [(0.4 + k * 0.85, "steps", 0.14) for k in range(5)],
 "B6": [(3.4, "paper", 0.35), (7.8, "ding", 0.22)], "B7": [(2.2, "paper", 0.2)], "B8": [(1.7, "keys", 0.3)],
 "B9": [(5.4, "whoosh", 0.12)], "B10": [(0.0, "stamp", 0.45)], "B12": [(1.8, "typing", 0.3), (4.15, "click", 0.3)],
 "B13": [(0.2, "paper", 0.3)], "B13b": [(8.4, "tv", 0.22)], "B17": [(1.0, "pen", 0.18)],
 "B19": [(0.3, "scanner", 0.25), (1.4, "scanner", 0.25), (2.5, "scanner", 0.25)], "B19b": [(9.4, "paper", 0.3)],
 "B22": [(6.0, "click", 0.3)], "B24": [(1.6, "pen", 0.3)], "B25": [(0.9, "mailbox", 0.35), (1.4, "paper", 0.25)],
 "B29": [(4.0, "paper", 0.25), (13.3, "impact", 0.35)], "B31": [(6.0, "paper", 0.3)], "B33": [(0.1, "coins", 0.35)],
 "B35": [(1.2, "paper", 0.3), (4.2, "paper", 0.3), (7.6, "paper", 0.3)], "B36b": [(2.4, "scissors", 0.35), (9.0, "click", 0.3)], "B37": [(2.6, "click", 0.4)],
}
MOODS = [("B0", "mystery"), ("B3", "drive"), ("B5", "drive"), ("B11", "mystery"), ("B16", "drive"), ("B20", "mystery"), ("B22", "uplift"), ("B25", "dark"),
         ("B28", "drive"), ("B31", "dark"), ("B34", "uplift")]

def beat_at(gt):
    for b in BEATS:
        if gt < b["end"]: return b
    return BEATS[-1]

def chapter_wall(gt, bid, lt):
    f = LEDGER.frame(gt).convert("RGBA"); t1, t2 = WALL_BEFORE[bid]; k = ease(lt / 0.35)
    label(f, t1, 960, 480, 130, (255, 214, 60), k / 1.0 if k < 1 else 1.0, 7); label(f, t2, 960, 610, 56, (255, 255, 255), (lt - 0.2) / 0.3, 4)
    out = min(1, (WALL - lt) / 0.25)
    if out < 1: f = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), f, max(0, out))
    return f

def frame_at(gt):
    b = beat_at(gt); lt = gt - b["t0"]
    if lt < b["pre"]: return chapter_wall(gt, b["id"], lt).convert("RGB")
    lt -= b["pre"]; T = b["dur"] - b["pre"]
    f = Image.new("RGBA", (W, H), (0, 0, 0, 255)); SCENES[b["id"]](f, lt, T)
    return f.convert("RGB")

def mix():
    n = int((TOTAL + 1) * SR); fx = np.zeros(n, np.float32); voice = np.zeros(n, np.float32)
    def add(t_, x, g):
        i = int(max(0, t_) * SR); x = x[:max(0, n - i)]; fx[i:i + len(x)] += x * g
    for b in BEATS:
        if b["id"] in WALL_BEFORE: add(b["t0"], SFXL.load("impact"), 0.42)
        for (tc, name, g) in CUES.get(b["id"], []): add(b["t0"] + b["pre"] + tc, SFXL.load(name), g)
        if b["id"] in VO:
            st = int((b["t0"] + b["pre"] + 0.1) * SR); a = VO[b["id"]]; voice[st:st + len(a)] += a[:max(0, n - st)]
    cs = np.concatenate([[0.0], np.cumsum(np.abs(voice), dtype=np.float64)]); idx = np.arange(n)
    lo, hi = np.clip(idx - 2400, 0, n), np.clip(idx + 2400, 0, n); vabs = ((cs[hi] - cs[lo]) / 4800).astype(np.float32); del cs, idx, lo, hi
    duck = 1 - 0.55 * np.clip(vabs / 0.05, 0, 1)
    mus = music.build(n, [(BEATS[IDX[k]]["t0"], m) for k, m in MOODS]) * 0.17 * duck
    out = voice + fx + mus; m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)].astype(np.float32)

if __name__ == "__main__":
    print(f"Laenge {TOTAL / 60:.2f} min, {len(BEATS)} Szenen")
    if "--stills" in sys.argv:
        os.makedirs("stills_v3", exist_ok=True); tiles = []
        for b in BEATS:
            for fr in (0.3, 0.85):
                tt = b["t0"] + b["pre"] + (b["dur"] - b["pre"]) * fr; im = frame_at(tt); tiles.append(im)
            im.save(f"stills_v3/{b['id']}.jpg", quality=85)
        tw, th, cols = 320, 180, 10
        sheet = Image.new("RGB", (cols * (tw + 4) + 4, ((len(tiles) + cols - 1) // cols) * (th + 4) + 4))
        for i, t_ in enumerate(tiles): sheet.paste(t_.resize((tw, th)), (4 + (i % cols) * (tw + 4), 4 + (i // cols) * (th + 4)))
        sheet.save("STORYBOARD_v3.jpg", quality=88); print("stills ok"); sys.exit()
    a0 = float(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else 0.0
    a1 = float(sys.argv[sys.argv.index("--to") + 1]) if "--to" in sys.argv else TOTAL
    name = "ARC_Money_v3.mp4" if a0 == 0 and a1 == TOTAL else f"ARC_Money_v3_part_{int(a0)}_{int(a1)}.mp4"
    out = av.open(name, "w"); vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "19", "preset": "medium"}
    ast = out.add_stream("aac", rate=SR); ast.layout = "mono"; N = int((a1 - a0) * FPS)
    for k in range(N):
        for p in vs.encode(av.VideoFrame.from_image(frame_at(a0 + k / FPS))): out.mux(p)
        if k % 900 == 0: print(k, "/", N, flush=True)
    for p in vs.encode(): out.mux(p)
    audio = mix()[int(a0 * SR):int(a1 * SR)]
    for i in range(0, len(audio), 1024):
        ch = audio[i:i + 1024]; ch = np.pad(ch, (0, 1024 - len(ch))) if len(ch) < 1024 else ch
        af = av.AudioFrame.from_ndarray(ch.reshape(1, -1).astype(np.float32), format="flt", layout="mono"); af.sample_rate = SR
        for p in ast.encode(af): out.mux(p)
    for p in ast.encode(): out.mux(p)
    out.close(); print("ok", name)
