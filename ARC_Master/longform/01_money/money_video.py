"""ARC Longform #01 – HOW MONEY REALLY WORKS. 56 Bild-Momente aus SKRIPT_v2.md (beats.json).
Ohne Stimme: Zeitplan aus Wortzahl geschaetzt. Mit Jason spaeter: Beat-Dauern = echte Audio-Laengen.
Aufruf:  python money_video.py --stills   |   python money_video.py [--from S --to S]"""
import sys, os, json, math, random
from kit16 import *
from bill_kit import real_bill, Ledger
sys.path.insert(0, os.path.join(HERE, "../../shorts/01_lamborghini/v7"))
import numpy as np, av
import sfx
sys.path.insert(0, os.path.join(HERE, '../../sfx_lib'))
import lib as SFXL
import music
import kit16
os.chdir(HERE)

FPS, SR = 30, 48000
BEATS = json.load(open("beats.json", encoding="utf-8"))
CHAPTERS = {5: ("SECRET #1", "Your money isn't in the bank"), 10: ("SECRET #2", "Banks create money out of nothing"),
            17: ("SECRET #3", "How the bank makes money on you"), 23: ("SECRET #4", "The leak: who gets new money first"),
            30: ("SECRET #5", "The invisible tax"), 35: ("SECRET #6", "How the rich play the game"),
            42: ("SECRET #7", "The price of money"), 44: ("SECRET #8", "Heads they win, tails you lose"), 50: ("FINALE", "The dollar on the table")}
VO, V4 = {}, set()
for i, b in enumerate(BEATS):          # neue, lebendige Aufnahme (eleven_v4) bevorzugt
    for d_ in ("vo_v4", "vo"):
        fn = f"{d_}/beat_{i:02d}.npy"
        if os.path.exists(fn): VO[i] = np.load(fn); (V4.add(i) if d_ == "vo_v4" else None); break
WALL = 1.5                             # Kapitel-Trennwand vor jedem Kapitel (dunkel, gross, Impact)
PRE = {i: WALL for i in CHAPTERS}
t = 0.0
for i, b in enumerate(BEATS):          # Dauer = echte Laenge von Jasons Satz + kurze Atempause (+ Trennwand)
    if i in VO: b["dur"] = round(len(VO[i]) / SR + (0.22 if i in V4 else 0.35), 2)
    elif i == 4: b["dur"] = 3.0
    else: b["dur"] = 1.2
    b["dur"] += PRE.get(i, 0.0)
    b["t0"] = t; t += b["dur"]; b["end"] = t
TOTAL = BEATS[-1]["end"]
LEDGER = Ledger()
# ======================= Szenen (frame, lt, T) =======================
def s00(f, lt, T):          # Dollar faellt ins Licht
    y = -150 + 830 * ease(lt / (T * 0.7)); sway = math.sin(lt * 2.2) * 90 * (1 - ease(lt / (T * 0.7)))
    put(f, sprite(("bill_big",), lambda c: real_bill(c, 960, 540, 520, value="1")), sway, y - 540, rot=math.sin(lt * 1.7) * 14 * (1 - ease(lt / (T * 0.7))))
    if lt > T * 0.75: label(f, "4¢", 960, 300, 120, (255, 255, 255), (lt - T * 0.75) / 0.4)

def s01(f, lt, T):          # Strasse: Jake und Ryan als Kinder fahren Rad (echte Bewegung)
    for i, (p, col, y) in enumerate(((JAKE, (200, 70, 60), 990), (RYAN, (60, 110, 170), 1050))):
        x = -200 + (2300) * (lt / T) - i * 260
        put(f, sprite(("bike", i), lambda c, col=col, y=y: bike(ImageDraw.Draw(c, "RGBA"), 960, y, 220, col)), x - 960)
        fig(f, p, x, y - 70, 60, 1, mouth="smile", arms=("rest", "rest"), seed=10 + i, seated=True)
    note(f, ["JAKE"], 760, 560, w=200, k=lt - T * 0.35); note(f, ["RYAN"], 1160, 560, angle=3, w=200, k=lt - T * 0.5)

def s02(f, lt, T):          # Zwei gleiche Gehaltsschecks
    put(f, sprite(("pc1",), lambda c: paycheck(c, 520, 540, 760, "Jake", "$60,000")), 0, (1 - ease(lt / 0.4)) * 600)
    put(f, sprite(("pc2",), lambda c: paycheck(c, 1400, 540, 760, "Ryan", "$60,000")), 0, (1 - ease((lt - 0.15) / 0.4)) * 600)
    label(f, "SAME SALARY", 960, 170, 80, (255, 255, 255), lt / 0.4)

def s03(f, lt, T):          # Split: Jake 45 Mietwohnung vs Ryan 45 Veranda
    f.paste(bg("apt_half", lambda: apartment_bg().crop((0, 0, W * SS // 2, H * SS)).resize((W * SS // 2, H * SS))).resize((W // 2, H)), (0, 0))
    f.paste(bg("porch_half", lambda: porch_bg().crop((W * SS // 4, 0, W * SS * 3 // 4, H * SS))).resize((W // 2, H)), (W // 2, 0))
    ImageDraw.Draw(f).line([(W // 2, 0), (W // 2, H)], fill=INK, width=8)
    fig(f, JAKE45, 480, 980, 95, 1, mouth="frown", brow=0.1, arms=("rest", "down"), seed=31)
    put(f, sprite(("bill_letter",), lambda c: paper(c, 700, 640, 220, 280, "CREDIT CARD", 5, "Balance due: $8,940", 41)), 0, math.sin(lt * 3) * 4)
    fig(f, RYAN45, 1440, 980, 95, -1, mouth="smile", arms=("rest", "down"), seed=32)
    put(f, sprite(("ryan_phone",), lambda c: phone(c, 1230, 640, 260, bank_app("PORTFOLIO", "+$1.2M", (40, 140, 80)))))
    label(f, "20 YEARS LATER", 960, 90, 64, (255, 255, 255), lt / 0.4)
    label(f, "STILL RENTING", 480, 220, 60, (255, 120, 110), (lt - T * 0.25) / 0.4)
    label(f, "MILLIONAIRE", 1440, 220, 60, (255, 214, 60), (lt - T * 0.15) / 0.4)
    if lt > T * 0.55: hand_label(f, "Not smarter. Not luckier.", 960, 1000, 54, (255, 255, 255), (lt - T * 0.55) / 0.4)

def s04(f, lt, T):          # Titelkarte
    put(f, sprite(("bill_t",), lambda c: real_bill(c, 960, 700, 360, value="1")))
    label(f, "HOW MONEY", 960, 330, 130, (255, 255, 255), lt / 0.5, 10)
    label(f, "REALLY WORKS", 960, 470, 130, (255, 214, 60), (lt - 0.2) / 0.5, 10)

def s05(f, lt, T):          # Jake geht zum Schalter und zahlt ein
    x = -150 + 820 * min(1, lt / 3.0)
    fig(f, JAKE, x, 1010, 92, 1, mouth="smile", walk_t=lt if lt < 3.0 else None, seed=51)
    fig(f, TELLER, 1290, 640, 70, -1, mouth="smile", seed=52, seated=True)
    if lt > 3.2:
        put(f, sprite(("app5000",), lambda c: phone(c, 400, 480, 340, bank_app("MY BANK", "$5,000"))), 0, (1 - ease((lt - 3.2) / 0.5)) * 500)

def s06(f, lt, T):          # Schein geht durch den Schalter und hinten raus zu einem Fremden
    fig(f, JAKE, 670, 1010, 92, 1, mouth="smile", seed=51)
    fig(f, TELLER, 1290, 640, 70, -1, mouth="smile", seed=52, seated=True)
    k = inout((lt - 1.0) / (T * 0.6)); x = 780 + (1900 - 780) * k; y = 600 - math.sin(k * math.pi) * 200
    put(f, sprite(("bill_s",), lambda c: real_bill(c, 960, 540, 180, value="100")), x - 960, y - 540, rot=k * 40)
    if lt > T * 0.55: fig(f, CROWD[1], 1840 - 120 * min(1, (lt - T * 0.55) / 1.5), 1010, 80, -1, mouth="smile", seed=53)
    if lt > T * 0.7: label(f, "LENT OUT", 1500, 260, 70, (255, 214, 60), (lt - T * 0.7) / 0.4)

def s07(f, lt, T):          # App-Saldo wird zum Schuldschein
    k = ease((lt - 1.5) / 1.0)
    put(f, sprite(("app5000c",), lambda c: phone(c, 960, 540, 640, bank_app("MY BANK", "$5,000"))), alpha=1 - k)
    if k > 0: put(f, sprite(("iou",), lambda c: paper(c, 960, 540, 560, 420, "I.O.U.", 3, "The Bank owes Jake $5,000", 71)), alpha=k, scale=0.8 + 0.2 * k)
    if lt > T * 0.6: label(f, "A PROMISE, NOT A PILE OF CASH", 960, 960, 60, (255, 255, 255), (lt - T * 0.6) / 0.4)

def s08(f, lt, T):          # Jakes Geld arbeitet fuer die Bank (Stadt), dann Jake schlaeft
    if lt < T * 0.62:
        targets = [((300, 160), "CAR LOAN 7–8%"), ((1650, 160), "BUSINESS LOAN"), ((1650, 920), "GOV. BONDS")]
        bx, by = 960, 540
        put(f, sprite(("bankicon",), lambda c: (shape(ImageDraw.Draw(c, "RGBA"), [(880, 480), (1040, 480), (1040, 600), (880, 600)], (226, 222, 208), 1, lw=4),
                                               shape(ImageDraw.Draw(c, "RGBA"), [(860, 480), (960, 420), (1060, 480)], (190, 186, 176), 2, lw=4))))
        for i, ((tx, ty), lab) in enumerate(targets):
            k = inout((lt - 1.0 - i * 1.6) / 2.5)
            if k <= 0: continue
            x, y = bx + (tx - bx) * k, by + (ty - by) * k
            put(f, sprite(("coin",), lambda c: coin(ImageDraw.Draw(c, "RGBA"), 960, 540, 38)), x - 960, y - 540)
            if k >= 1: label(f, lab, tx, ty + 70, 44, (255, 255, 255), (lt - 3.5 - i * 1.6) / 0.4)
    else:
        lt2 = lt - T * 0.62
        f.paste(bg("bedroom", lambda: dark_bg()), (0, 0))
        d = ImageDraw.Draw(f, "RGBA")
        d.rectangle([300, 720, 1500, 840], fill=(120, 100, 140), outline=INK, width=5); d.rectangle([300, 640, 520, 720], fill=(230, 230, 236), outline=INK, width=4)
        put(f, sprite(("sleepjake",), lambda c: bust(c, 420, 640, 80, JAKE, face=1, eyes="happy", mouth="line", seed=54)))
        hand_label(f, "z z z", 600, 520, 60, (255, 255, 255), 1.0)
        put(f, sprite(("app5000n",), lambda c: phone(c, 1400, 480, 380, bank_app("MY BANK", "$5,000")))),
        if lt2 > 2.5: label(f, "THE APP SHOWS THE PROMISE", 960, 140, 56, (255, 214, 60), (lt2 - 2.5) / 0.4)

def s09(f, lt, T):          # 0 %
    put(f, sprite(("vault_s",), lambda c: (shape(ImageDraw.Draw(c, "RGBA"), [(1240, 360), (1700, 360), (1700, 820), (1240, 820)], (150, 154, 162), 1, lw=6),
                                           real_bill(c, 1470, 760, 140, value="100"))))
    label(f, "0%", 640, 520, 400, (255, 90, 80), (lt - 0.4) / 0.3, 14)
    label(f, "RESERVE REQUIREMENT · SINCE MARCH 2020", 640, 820, 40, INK, (lt - 1.2) / 0.4, 0)
    if lt > T * 0.7: label(f, "?", 1470, 520, 200, (255, 214, 60), (lt - T * 0.7) / 0.4)

def s10(f, lt, T):          # Ryan im Kreditbuero
    fig(f, RYAN, 620, 760, 80, 1, mouth="smile", seed=61, seated=True)
    fig(f, BANKER, 1220, 760, 82, -1, mouth="smile", seed=62, seated=True)
    k = ease((lt - 1.5) / 1.2)
    put(f, sprite(("mortgage",), lambda c: paper(c, 920, 560, 260, 200, "MORTGAGE", 3, "$300,000", 63)), (1 - k) * 300, 0)
    note(f, ["RYAN, 28"], 620, 300, w=260, k=lt - 0.5)

def s11(f, lt, T):          # Bildschirm: $300,000 aus dem Nichts
    d = ImageDraw.Draw(f, "RGBA")
    d.rounded_rectangle([360, 140, 1560, 820], 30, fill=(40, 44, 54), outline=INK, width=8); d.rectangle([400, 180, 1520, 780], fill=(240, 244, 250))
    d.rectangle([860, 820, 1060, 900], fill=(60, 64, 74)); d.rectangle([700, 900, 1220, 940], fill=(60, 64, 74))
    label(f, "Account: RYAN", 960, 260, 50, INK, 1.0, 0)
    v = counter(0, 300000, (lt - 1.0) / 2.5)
    label(f, money(v), 960, 470, 150, (40, 140, 80) if v > 0 else INK, 1.0, 0)
    if lt > 3.8: label(f, "TYPED INTO EXISTENCE", 960, 680, 64, (255, 120, 60), (lt - 3.8) / 0.4, 0)
    for k in range(6):
        if (lt * 6 + k) % 3 < 1 and lt < 3.5: d.rectangle([700 + k * 90, 1000, 770 + k * 90, 1050], fill=(80, 84, 96), outline=INK)
    if lt > T * 0.7: label(f, "1 SECOND BEFORE: $0", 960, 1010, 46, (255, 255, 255), (lt - T * 0.7) / 0.4)

def s12(f, lt, T):          # Bank of England Dokument
    put(f, sprite(("boe",), lambda c: paper(c, 960, 520, 820, 820, "Money creation in the modern economy", 8, "Bank of England · Quarterly Bulletin 2014 Q1", 81)))
    k = ease((lt - 1.5) / 1.2)
    ImageDraw.Draw(f, "RGBA").rectangle([620, 690, 620 + 680 * k, 760], fill=(255, 230, 80, 150))
    label(f, "“…commercial banks making loans.”", 960, 724, 44, INK, 1.0 if k > 0 else 0, 0)

def s13(f, lt, T):          # Rueckzahlung loescht Geld
    put(f, sprite(("ryan_house",), lambda c: house_icon(c, 360, 820, 460, 91)))
    put(f, sprite(("bankicon2",), lambda c: (shape(ImageDraw.Draw(c, "RGBA"), [(1400, 560), (1760, 560), (1760, 820), (1400, 820)], (226, 222, 208), 1, lw=5),
                                             shape(ImageDraw.Draw(c, "RGBA"), [(1370, 560), (1580, 440), (1790, 560)], (190, 186, 176), 2, lw=5),
                                             text(c, "BANK", 1580, 700, 50, BOLD, INK))))
    for i in range(6):
        k = ((lt * 0.5 + i / 6) % 1)
        x = 640 + 700 * k; y = 700 - math.sin(k * math.pi) * 160
        put(f, sprite(("coin",), lambda c: coin(ImageDraw.Draw(c, "RGBA"), 960, 540, 38)), x - 960, y - 540, alpha=1 - max(0, (k - 0.75) / 0.25))
    if lt > T * 0.4: label(f, "PAID BACK = DELETED", 960, 200, 70, (255, 214, 60), (lt - T * 0.4) / 0.4)

def s14(f, lt, T):          # Schuldenzaehler 18,8 Bio.
    v = counter(0, 18.8e12, (lt - 0.5) / 4.0)
    label(f, money(v), 960, 420, 120, (255, 90, 80), 1.0)
    label(f, "U.S. HOUSEHOLD DEBT (END OF 2025)", 960, 560, 50, (255, 255, 255), lt / 0.4, 6)
    for i, s in enumerate(("MORTGAGES", "CAR LOANS", "STUDENT LOANS", "CREDIT CARDS")):
        note(f, [s], 330 + i * 420, 820, angle=(-1) ** i * 3, w=340, k=lt - 1.5 - i * 0.6)

def s15(f, lt, T):          # Vertrag + Rechnung
    put(f, sprite(("mort2",), lambda c: paper(c, 560, 540, 560, 720, "MORTGAGE", 9, "$300,000 · 30 years · 7%", 101)))
    rows = [("Monthly payment", "$1,996"), ("× 360 months", ""), ("Total paid", "$718,527")]
    for i, (a, b) in enumerate(rows):
        k = (lt - 1.0 - i * 1.6)
        hand_label(f, a, 1360, 340 + i * 150, 60, INK, k / 0.4)
        if b: label(f, b, 1360, 400 + i * 150, 70, (255, 214, 60), k / 0.4)

def s16(f, lt, T):          # Stempel 418.000 $ Zinsen
    put(f, sprite(("mort2",), lambda c: paper(c, 560, 540, 560, 720, "MORTGAGE", 9, "$300,000 · 30 years · 7%", 101)))
    k = (lt - 0.3) / 0.25
    if k > 0:
        f2 = ImageFont.truetype(BOLD, int(90 * pop(k))); lay = Image.new("RGBA", (900, 200), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((450, 100), "$418,000 INTEREST", font=f2, fill=(210, 40, 40, 230), anchor="mm", stroke_width=6, stroke_fill=(120, 20, 20, 230))
        lay = lay.rotate(12, expand=True); f.paste(lay, (560 - lay.width // 2, 540 - lay.height // 2), lay)
    if lt > T * 0.35:
        kk = ease((lt - T * 0.35) / 1.2); d = ImageDraw.Draw(f, "RGBA")
        d.rectangle([1150, 700 - 300 * kk, 1350, 700], fill=(60, 150, 90), outline=INK, width=5); label(f, "$300K", 1250, 760, 44, INK, 1.0, 0)
        d.rectangle([1450, 700 - 418 * kk, 1650, 700], fill=(210, 60, 60), outline=INK, width=5); label(f, "$418K", 1550, 760, 44, INK, 1.0, 0)
        hand_label(f, "created", 1250, 820, 40, INK, 1.0); hand_label(f, "interest", 1550, 820, 40, INK, 1.0)
    if lt > T * 0.7: label(f, "FROM NOTHING.", 1400, 180, 70, (255, 214, 60), (lt - T * 0.7) / 0.4)

def s17(f, lt, T):          # Split Sparkonto vs Kreditkarte
    put(f, sprite(("sav_phone",), lambda c: phone(c, 520, 520, 600, bank_app("SAVINGS", "$5,000"))), 0, (1 - ease(lt / 0.5)) * 400)
    put(f, sprite(("cc",), lambda c: credit_card(c, 1400, 520, 620)), 0, (1 - ease((lt - 0.3) / 0.5)) * 400)
    label(f, "JAKE'S SAVINGS", 520, 140, 54, INK, lt / 0.4, 0); label(f, "JAKE'S CREDIT CARD", 1400, 140, 54, INK, (lt - 0.3) / 0.4, 0)
    if lt > T * 0.35: label(f, "under 1%", 520, 900, 54, (60, 150, 90), (lt - T * 0.35) / 0.4)
    if lt > T * 0.6: label(f, "≈ 21%", 1400, 900, 120, (220, 50, 50), (lt - T * 0.6) / 0.4)

def s18(f, lt, T):          # Grosser Vergleich, Pfeile
    label(f, "under 1%", 480, 520, 60, (60, 150, 90), lt / 0.3)
    label(f, "21%", 1400, 520, 300, (220, 50, 50), (lt - 0.6) / 0.3, 12)
    if lt > 2.0:
        hand_label(f, "the bank borrows from Jake", 480, 680, 46, INK, (lt - 2.0) / 0.4)
        hand_label(f, "the bank lends to Jake", 1400, 760, 46, INK, (lt - 3.0) / 0.4)
    if lt > T * 0.6: label(f, "THE OLDEST BUSINESS MODEL", 960, 940, 56, INK, (lt - T * 0.6) / 0.4, 0)

def s19(f, lt, T):          # Kontoauszug Mindestzahlung
    put(f, sprite(("stmt",), lambda c: paper(c, 960, 560, 760, 860, "CREDIT CARD STATEMENT", 10, "Balance: $5,000 · APR 21%", 111)))
    k = ease((lt - 1.5) / 1.0)
    ImageDraw.Draw(f, "RGBA").rectangle([620, 880, 620 + 680 * k, 940], fill=(255, 230, 80, 160))
    label(f, "Minimum payment due: $137", 960, 910, 44, INK, 1.0 if k > 0 else 0, 0)

def s20(f, lt, T):          # Jake altert, Fortschrittsbalken, dann Payday
    if lt < T * 0.6:
        k = lt / (T * 0.6); age = int(25 + 19 * k)
        p = JAKE if age < 35 else JAKE45
        put(f, sprite(("jakebust", age // 5), lambda c, p=p: bust(c, 480, 520, 220, p, face=1, mouth="frown", brow=0.06, seed=121)))
        label(f, f"AGE {age}", 480, 120, 70, (255, 255, 255), 1.0)
        d = ImageDraw.Draw(f, "RGBA"); d.rounded_rectangle([1000, 480, 1800, 560], 20, fill=(240, 240, 240), outline=INK, width=5)
        d.rounded_rectangle([1000, 480, 1000 + 800 * k, 560], 20, fill=(60, 150, 90))
        label(f, f"{int(100 * k)}% PAID OFF", 1400, 420, 50, INK, 1.0, 0)
        if k > 0.6: label(f, "19 YEARS · $7,700 INTEREST", 1400, 680, 54, (220, 50, 50), (k - 0.6) / 0.1)
    else:
        f.paste(bg("payday", lambda: city_bg()), (0, 0))
        d = ImageDraw.Draw(f, "RGBA")
        d.rectangle([560, 420, 1360, 1000], fill=(226, 214, 190), outline=INK, width=6); d.rectangle([520, 340, 1400, 440], fill=(240, 200, 60), outline=INK, width=6)
        label(f, "PAYDAY LOANS · CASH NOW", 960, 390, 52, (180, 30, 30), 1.0, 0)
        d.rectangle([840, 700, 1080, 1000], fill=(120, 90, 70), outline=INK, width=5)
        lt2 = lt - T * 0.6
        label(f, "$15 per $100 · 2 weeks", 960, 560, 50, INK, lt2 / 0.4, 0)
        label(f, "≈ 400% A YEAR", 960, 220, 110, (220, 50, 50), (lt2 - 1.5) / 0.3)

def s21(f, lt, T):          # Kartenzahlung im Cafe, Muenze fliegt zur Bank
    fig(f, JAKE, 520, 1010, 90, 1, mouth="smile", arms=("down", "point"), seed=131)
    fig(f, TELLER, 860, 640, 70, -1, mouth="smile", seed=132, seated=True)
    put(f, sprite(("cc_small",), lambda c: credit_card(c, 690, 600, 110)))
    k = inout((lt - 1.5) / 2.0)
    if k > 0:
        x, y = 690 + (1560 - 690) * k, 600 - math.sin(k * math.pi) * 300 - 120 * k
        put(f, sprite(("coin_s",), lambda c: coin(ImageDraw.Draw(c, "RGBA"), 960, 540, 24)), x - 960, y - 540)
    if lt > 3.6: label(f, "≈ 2% FEE", 1560, 260, 70, (255, 214, 60), (lt - 3.6) / 0.4)

def s22(f, lt, T):          # Preis tickt hoch, 187 Mrd.
    if lt < T * 0.45:
        d = ImageDraw.Draw(f, "RGBA"); d.rounded_rectangle([660, 300, 1260, 640], 30, fill=(250, 248, 240), outline=INK, width=6)
        p = 4.50 if lt < 2.0 else 4.59
        label(f, "LATTE", 960, 380, 60, INK, 1.0, 0); label(f, f"${p:.2f}", 960, 520, 140, (40, 110, 60) if p < 4.55 else (200, 60, 40), 1.0, 0)
        if lt > 2.0: hand_label(f, "+ card fees, built in", 960, 720, 54, (255, 255, 255), (lt - 2.0) / 0.4)
    else:
        lt2 = lt - T * 0.45
        label(f, "$187 BILLION", 960, 420, 170, (255, 214, 60), lt2 / 0.3, 12)
        label(f, "CARD FEES PAID BY U.S. BUSINESSES IN 2024", 960, 580, 46, (255, 255, 255), (lt2 - 0.6) / 0.4, 6)
        if lt2 > 3.0: label(f, "EVEN CASH PAYERS PAY IT", 960, 800, 60, (255, 120, 110), (lt2 - 3.0) / 0.4)

def s23(f, lt, T):          # Fed bei Nacht mit Wasserhahn
    d = ImageDraw.Draw(f, "RGBA")
    d.rectangle([900, 120, 1020, 160], fill=(180, 184, 196), outline=INK, width=5); d.rectangle([1000, 140, 1140, 180], fill=(180, 184, 196), outline=INK, width=5)
    if lt > 2.0:
        for k in range(12):
            yy = 190 + ((lt * 300 + k * 50) % 600); d.rectangle([1120, yy, 1150, yy + 30], fill=(80, 200, 120, 200))
    note(f, ["THE FEDERAL RESERVE"], 960, 960, w=560, k=lt - 0.6)

def s24(f, lt, T):          # Balkendiagramm 0,9 → 8,9 Bio.
    k = ease((lt - 0.5) / 3.0)
    bars = [("2007", 0.87), ("2014", 4.5), ("2020", 4.2), ("2021", 7.6), ("2022", 8.9)]
    d = ImageDraw.Draw(f, "RGBA")
    for i, (lab, v) in enumerate(bars):
        x = 380 + i * 260; hh = 640 * v / 8.9 * k
        d.rectangle([x, 900 - hh, x + 170, 900], fill=(60, 150, 90), outline=INK, width=5)
        label(f, lab, x + 85, 950, 40, INK, 1.0, 0)
        if k > 0.9: label(f, f"${v}T", x + 85, 860 - hh, 44, INK, 1.0, 0)
    label(f, "WHAT THE FED OWNS", 960, 110, 64, INK, lt / 0.4, 0)
    if lt > T * 0.6: label(f, "10×", 1640, 300, 140, (220, 50, 50), (lt - T * 0.6) / 0.3)

def s25(f, lt, T):          # Geldstapel waechst an Hochhaeusern vorbei
    k = ease(lt / (T * 0.7)); d = ImageDraw.Draw(f, "RGBA")
    top = 1000 - 950 * k
    d.rectangle([880, top, 1040, 1000], fill=(186, 206, 176), outline=INK, width=5)
    for y in range(int(top), 1000, 18): d.line([(880, y), (1040, y)], fill=(120, 150, 116), width=2)
    if lt > T * 0.5:
        label(f, "$1 MILLION A DAY", 960, 180, 64, (255, 255, 255), (lt - T * 0.5) / 0.4)
        label(f, "= 20,000+ YEARS FOR $8 TRILLION", 960, 280, 60, (255, 214, 60), (lt - T * 0.6) / 0.4)

def s26(f, lt, T):          # Fluss des neuen Geldes (Cantillon)
    pts = [(180, 160), (500, 300), (820, 460), (1140, 620), (1460, 780), (1780, 930)]
    put(f, sprite(("river",), lambda c: stroke(ImageDraw.Draw(c, "RGBA"), pts, lw=60, color=(120, 190, 230))))
    stops = [("FED", pts[0]), ("BANKS", pts[1]), ("BIG INVESTORS", pts[2]), ("STOCKS & HOUSES ↑", pts[3]), ("…", pts[4])]
    for i, (s, (x, y)) in enumerate(stops):
        note(f, [s], x + 60, y - 110, angle=(-1) ** i * 3, w=max(200, len(s) * 32), k=lt - 1.0 - i * 2.2)
    flow = min(1, lt / (T * 0.7))
    for j in range(14):
        kk = ((lt * 0.35 + j / 14) % 1) * flow
        x = 180 + 1600 * kk; y = 160 + 770 * kk
        put(f, sprite(("coin_s",), lambda c: coin(ImageDraw.Draw(c, "RGBA"), 960, 540, 24)), x - 960, y - 540)
    fig(f, JAKE, 1820, 1060, 70, -1, mouth="frown", brow=0.08, arms=("down", "point"), seed=141)
    if lt > T * 0.72: label(f, "THE CANTILLON EFFECT", 700, 960, 64, (255, 214, 60), (lt - T * 0.72) / 0.4)

def s27(f, lt, T):          # Ryans Haus + App gruen
    put(f, sprite(("ryan_house2",), lambda c: house_icon(c, 600, 900, 620, 151)))
    k = ease((lt - 0.5) / 3.0)
    put(f, sprite(("stock_phone", int(k * 10)), lambda c, k=k: phone(c, 1400, 520, 600, lambda c2, cx, cy, w, h: (
        ImageDraw.Draw(c2, "RGBA").line([(cx - w * 0.4 + i * w * 0.08, cy + h * 0.2 - (i * i) * h * 0.012 * k) for i in range(11)], fill=(40, 160, 80), width=12),
        text(c2, "INVESTMENTS", cx, cy - h * 0.36, w * 0.09, BOLD, INK)))))
    label(f, "+31% HOME PRICES", 600, 180, 64, (60, 150, 90), (lt - 1.0) / 0.4)
    label(f, "STOCKS DOUBLED", 1400, 140, 60, (60, 150, 90), (lt - 2.2) / 0.4)
    if lt > 3.6: hand_label(f, "2020 – 2021", 960, 1010, 50, INK, (lt - 3.6) / 0.4)

def s28(f, lt, T):          # Preisschild 300k → 393k
    put(f, sprite(("ryan_house2",), lambda c: house_icon(c, 600, 900, 620, 151)))
    v = counter(300000, 393000, (lt - 0.5) / 2.5)
    d = ImageDraw.Draw(f, "RGBA"); d.rounded_rectangle([1100, 380, 1760, 600], 24, fill=(250, 248, 240), outline=INK, width=6)
    label(f, money(v), 1430, 490, 110, (40, 140, 80), 1.0, 0)
    if lt > 3.2: label(f, "+$90,000 WHILE SLEEPING", 1430, 760, 54, (255, 214, 60), (lt - 3.2) / 0.4)

def s29(f, lt, T):          # Jake oeffnet Mieterhoehung
    fig(f, JAKE, 760, 1000, 100, 1, mouth="frown", brow=0.1, arms=("rest", "down"), seed=161)
    k = ease((lt - 0.6) / 0.6)
    put(f, sprite(("rent",), lambda c: paper(c, 1240, 520, 460, 560, "NOTICE", 6, "RENT INCREASE", 162)), 0, (1 - k) * 400)
    if lt > 2.5: label(f, "AGAIN.", 1240, 900, 90, (220, 50, 50), (lt - 2.5) / 0.3)

def s30(f, lt, T):          # 1971 Einkaufswagen
    put(f, sprite(("cart1971",), lambda c: shopping_cart(ImageDraw.Draw(c, "RGBA"), 960, 1000, 520, 1.0, 171)))
    label(f, "$100", 960, 380, 160, (40, 140, 80), (lt - 0.6) / 0.3)

def s31(f, lt, T):          # heute: gleicher Wagen, ~800 $
    put(f, sprite(("cart_now",), lambda c: shopping_cart(ImageDraw.Draw(c, "RGBA"), 960, 1000, 520, 1.0, 171)))
    v = counter(100, 800, (lt - 0.5) / 2.0)
    label(f, f"${v:,.0f}", 960, 380, 160, (220, 50, 50), 1.0)
    if lt > 3.0: label(f, "SAME GROCERIES", 960, 230, 54, INK, (lt - 3.0) / 0.4, 0)

def s32(f, lt, T):          # Fed-Dokument 2 %
    put(f, sprite(("fed2",), lambda c: paper(c, 960, 540, 760, 860, "Statement on Longer-Run Goals", 9, "Federal Reserve", 181)))
    label(f, "2 PERCENT", 960, 640, 80, INK, 1.0 if lt > 0.8 else 0, 0)
    if lt > 1.4:
        k = ease((lt - 1.4) / 0.8); d = ImageDraw.Draw(f, "RGBA")
        d.arc([720, 570, 1200, 710], 0, int(360 * k), fill=(220, 40, 40), width=10)
    if lt > T * 0.6: label(f, "ON PURPOSE.", 960, 960, 70, (255, 214, 60), (lt - T * 0.6) / 0.4)

def s33(f, lt, T):          # Sparkonto gleich, Einkaufstuete halb
    put(f, sprite(("sav20",), lambda c: phone(c, 560, 540, 600, bank_app("SAVINGS", "$20,000"))))
    k = ease((lt - 1.0) / 3.0)
    put(f, sprite(("bag", int((1 - 0.5 * k) * 10)), lambda c, k=k: shopping_cart(ImageDraw.Draw(c, "RGBA"), 1400, 900, 460, 1 - 0.5 * k, 191)))
    label(f, "BUYS LESS EVERY YEAR", 1400, 200, 56, INK, (lt - 1.5) / 0.4, 0)

def s34(f, lt, T):          # Ersparnisse verdunsten, dann Split Bargeld vs Besitz
    if lt < T * 0.6:
        k = lt / (T * 0.6); years = int(k * 10)
        d = ImageDraw.Draw(f, "RGBA")
        for i in range(10):
            a = 1.0 if i >= years else 0.15
            x = 360 + (i % 5) * 260; y = 360 + (i // 5) * 300
            put(f, sprite(("stack",), lambda c: real_bill(c, 960, 540, 220, value="100")), x - 960, y - 540, alpha=a)
        label(f, f"YEAR {years}", 960, 100, 64, INK, 1.0, 0)
        label(f, "−$500 REAL VALUE PER YEAR", 960, 960, 60, (220, 50, 50), (lt - 2.0) / 0.4)
    else:
        lt2 = lt - T * 0.6; ImageDraw.Draw(f).line([(W // 2, 0), (W // 2, H)], fill=INK, width=8)
        label(f, "CASH", 480, 140, 80, INK, lt2 / 0.4, 0); label(f, "THINGS YOU OWN", 1440, 140, 80, INK, (lt2 - 0.3) / 0.4, 0)
        k = ease(lt2 / 3.0)
        put(f, sprite(("bill_cash",), lambda c: real_bill(c, 480, 560, 420, value="100")), scale=1 - 0.4 * k)
        put(f, sprite(("ryan_house3",), lambda c: house_icon(c, 1440, 760, 420, 192)), scale=1 + 0.25 * k)
        if lt2 > 2.5: label(f, "MELTS", 480, 900, 70, (220, 50, 50), (lt2 - 2.5) / 0.4); label(f, "GROWS", 1440, 960, 70, (60, 150, 90), (lt2 - 2.8) / 0.4)

def s35(f, lt, T):          # Milliardaer im Glasbuero
    fig(f, BILLIONAIRE, 1100, 1000, 110, 1, mouth="smirk", arms=("hip", "hip"), seed=201)
    note(f, ["THE TOP 0.1%"], 500, 220, w=380, k=lt - 1.0)

def s36(f, lt, T):          # Aktien wachsen auf Bildschirm
    k = ease(lt / (T * 0.8)); d = ImageDraw.Draw(f, "RGBA")
    d.rounded_rectangle([300, 160, 1620, 860], 30, fill=(24, 28, 40), outline=INK, width=8)
    pts = [(360 + i * 60, 800 - (i ** 1.6) * 9 * k - math.sin(i) * 20) for i in range(21)]
    d.line(pts, fill=(60, 220, 120), width=10)
    label(f, "SHARES", 520, 230, 56, (240, 240, 240), 1.0, 0)
    label(f, "NOT SOLD = NOT TAXED", 960, 960, 60, INK, (lt - T * 0.5) / 0.4, 0)

def s37(f, lt, T):          # Aktien als Pfand, Koffer mit Geld
    fig(f, BILLIONAIRE, 560, 1010, 92, 1, mouth="smirk", arms=("down", "point"), seed=202)
    fig(f, BANKER, 1360, 640, 72, -1, mouth="smile", seed=203, seated=True)
    k = inout((lt - 1.0) / 2.0); k2 = inout((lt - 3.5) / 2.0)
    sx = 720 + (1180 - 720) * k - (1180 - 720) * k2
    put(f, sprite(("shares",), lambda c: paper(c, 960, 540, 200, 240, "SHARES", 3, None, 204, (230, 240, 250))), sx - 960, 60)
    if lt > 2.5:
        kk = inout((lt - 2.5) / 1.8); cx = 1180 - (1180 - 760) * kk
        put(f, sprite(("suitcase",), lambda c: (shape(ImageDraw.Draw(c, "RGBA"), [(880, 500), (1040, 500), (1040, 620), (880, 620)], (110, 80, 50), 1, lw=5),
                                                text(c, "$", 960, 560, 70, BOLD, (240, 200, 80)))), cx - 960, 120)
    if lt > T * 0.75: label(f, "THE SHARES STAY HIS", 960, 160, 64, (255, 214, 60), (lt - T * 0.75) / 0.4)

def s38(f, lt, T):          # Waage: 80 Mio. Wachstum vs 500.000 Zinsen
    tilt = round(-0.18 * ease((lt - 2.0) / 1.5), 3); res = {}
    put(f, sprite(("scale", tilt), lambda c: res.update(v=scale_prop(ImageDraw.Draw(c, "RGBA"), 960, 360, 900, tilt))))
    ax, ay = math.cos(tilt) * 450, math.sin(tilt) * 450
    (lx, ly), (rx, ry) = (960 - ax, 360 - ay + 150), (960 + ax, 360 + ay + 150)
    label(f, "$1B SHARES", lx, ly - 60, 56, (40, 140, 80), (lt - 0.5) / 0.4); label(f, "+8% = $80M", lx, ly + 80, 50, (40, 140, 80), (lt - 1.5) / 0.4)
    label(f, "$10M LOAN", rx, ry - 60, 56, (220, 50, 50), (lt - 3.0) / 0.4); label(f, "5% = $500K", rx, ry + 80, 50, (220, 50, 50), (lt - 4.0) / 0.4)
    if lt > T * 0.6: label(f, "NO INCOME TAX ON THE LOAN", 960, 1000, 60, (255, 214, 60), (lt - T * 0.6) / 0.4)

def s39(f, lt, T):          # Testament, Aktien gehen an Kind
    put(f, sprite(("will",), lambda c: paper(c, 520, 520, 520, 660, "LAST WILL", 8, "and Testament", 211)))
    fig(f, CHILD, 1500, 1000, 80, -1, mouth="smile", seed=212)
    k = inout((lt - 1.5) / 2.5)
    put(f, sprite(("shares",), lambda c: paper(c, 960, 540, 200, 240, "SHARES", 3, None, 204, (230, 240, 250))), (-260 + 760 * k), 0)
    if lt > T * 0.55: label(f, "STEP-UP: LIFETIME GAINS NEVER TAXED", 960, 140, 54, (255, 214, 60), (lt - T * 0.55) / 0.4)

def s40(f, lt, T):          # Buy. Borrow. Die.
    for i, w_ in enumerate(("BUY.", "BORROW.", "DIE.")):
        label(f, w_, 960, 340 + i * 200, 170, (255, 255, 255) if i < 2 else (220, 60, 60), (lt - 0.6 - i * 1.3) / 0.3, 12)

def s41(f, lt, T):          # 3,4 % vs Lohnzettel
    label(f, "3.4%", 640, 480, 320, (255, 214, 60), (lt - 0.3) / 0.3, 14)
    hand_label(f, "“true tax rate” of the 25 richest (ProPublica)", 640, 720, 40, INK, (lt - 1.0) / 0.4)
    put(f, sprite(("payslip",), lambda c: paper(c, 1460, 520, 460, 600, "JAKE'S PAYSLIP", 7, "Federal · State · FICA", 221)))

def s42(f, lt, T):          # Split Kasse TV vs Kredit unterschreiben
    ImageDraw.Draw(f).line([(W // 2, 0), (W // 2, H)], fill=INK, width=8)
    fig(f, JAKE, 420, 1000, 90, 1, mouth="smile", arms=("down", "point"), seed=231)
    d = ImageDraw.Draw(f, "RGBA"); d.rectangle([560, 520, 860, 720], fill=(30, 30, 36), outline=INK, width=6)
    label(f, "NEW TV", 710, 470, 40, INK, 1.0, 0)
    fig(f, BILLIONAIRE, 1500, 1000, 90, -1, mouth="smirk", arms=("point", "down"), seed=232)
    put(f, sprite(("loan_doc",), lambda c: paper(c, 1220, 620, 220, 280, "LOAN", 4, "secured by shares", 233)))
    label(f, "21% · CREDIT CARD", 480, 140, 52, (220, 50, 50), (lt - 1.0) / 0.4); label(f, "FRACTION OF THAT", 1440, 140, 52, (60, 150, 90), (lt - 2.0) / 0.4)

def s43(f, lt, T):          # Preisschilder, dann Listen, dann Falle vs Werkzeug
    if lt < T * 0.35:
        d = ImageDraw.Draw(f, "RGBA")
        d.rounded_rectangle([220, 260, 900, 820], 30, fill=(250, 240, 236), outline=INK, width=6); d.rounded_rectangle([1200, 420, 1600, 700], 30, fill=(236, 248, 240), outline=INK, width=6)
        label(f, "$1,000 COSTS JAKE", 560, 360, 46, INK, 1.0, 0); label(f, "+$210/yr", 560, 560, 130, (220, 50, 50), lt / 0.3)
        label(f, "THE RICH", 1400, 480, 40, INK, 1.0, 0); label(f, "far less", 1400, 600, 60, (60, 150, 90), (lt - 0.8) / 0.3)
    elif lt < T * 0.75:
        lt2 = lt - T * 0.35; ImageDraw.Draw(f).line([(W // 2, 0), (W // 2, H)], fill=INK, width=8)
        label(f, "LOSES VALUE", 480, 150, 70, (220, 50, 50), lt2 / 0.4); label(f, "GAINS VALUE", 1440, 150, 70, (60, 150, 90), (lt2 - 1.5) / 0.4)
        for i, s in enumerate(("TV", "CAR", "VACATION")): note(f, [s], 480, 360 + i * 200, angle=(-1) ** i * 3, w=300, k=lt2 - 0.5 - i * 0.6)
        for i, s in enumerate(("COMPANIES", "BUILDINGS", "SHARES")): note(f, [s], 1440, 360 + i * 200, angle=(-1) ** i * 3, w=340, k=lt2 - 2.0 - i * 0.6)
    else:
        lt2 = lt - T * 0.75
        label(f, "DEBT", 960, 300, 120, (255, 255, 255), lt2 / 0.3)
        label(f, "TRAP", 560, 620, 160, (220, 50, 50), (lt2 - 1.0) / 0.3); label(f, "TOOL", 1360, 620, 160, (60, 150, 90), (lt2 - 2.5) / 0.3)

def s44(f, lt, T):          # SVB, Handys leuchten
    rnd = random.Random(int(lt * 4))
    for k in range(10):
        if rnd.random() < 0.5:
            x, y = rnd.randint(200, 1700), rnd.randint(300, 820)
            put(f, sprite(("ph_s",), lambda c: phone(c, 960, 540, 110)), x - 960, y - 540)

def s45(f, lt, T):          # Raster aus Handys "Transfer"
    for r in range(3):
        for c_ in range(6):
            x, y = 260 + c_ * 280, 260 + r * 260
            put(f, sprite(("ph_t",), lambda c: phone(c, 960, 540, 220, lambda c2, cx, cy, w, h: (ImageDraw.Draw(c2, "RGBA").rounded_rectangle(S(cx - w * 0.36, cy - 24, cx + w * 0.36, cy + 24), radius=20, fill=(40, 120, 220)),
                                                                                           text(c2, "TRANSFER", cx, cy, w * 0.12, BOLD, (255, 255, 255))))), x - 960, y - 540)
    v = counter(0, 42e9, (lt - 0.5) / 3.0)
    label(f, money(v), 960, 100, 110, (220, 50, 50), 1.0)
    if lt > 3.6: label(f, "IN ONE DAY", 960, 1000, 64, (255, 255, 255), (lt - 3.6) / 0.4)

def s46(f, lt, T):          # Leerer Tresor, Licht aus, dann Garantie
    if lt < T * 0.45:
        dark = min(1, max(0, (lt - 2.0) / 1.5))
        if dark > 0: f.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(210 * dark))))
        if lt > 3.5: label(f, "CLOSED · MARCH 10, 2023", 960, 540, 80, (255, 255, 255), (lt - 3.5) / 0.4)
    else:
        lt2 = lt - T * 0.45
        f.paste(bg("svb", svb_bg), (0, 0))
        label(f, "INSURED UP TO $250,000", 960, 200, 70, (255, 255, 255), lt2 / 0.4)
        if lt2 > 3.0: label(f, "ALL DEPOSITS GUARANTEED", 960, 380, 80, (255, 214, 60), (lt2 - 3.0) / 0.4)

def s47(f, lt, T):          # 2008, Kongress, Scheck 700 Mrd.
    d = ImageDraw.Draw(f, "RGBA")
    k = ease((lt - 1.0) / 0.8)
    if k > 0:
        d.rounded_rectangle([360, 500 + (1 - k) * 500, 1560, 900 + (1 - k) * 500], 30, fill=(236, 244, 230), outline=INK, width=6)
        label(f, "PAY TO: THE BANKS", 760, 600 + (1 - k) * 500, 50, INK, 1.0, 0)
        label(f, "$700,000,000,000", 1060, 760 + (1 - k) * 500, 90, (40, 110, 60), 1.0, 0)

def s48(f, lt, T):          # AIG, Boni-Umschlaege
    for i in range(int(min(8, lt * 1.6))):
        x = 240 + (i % 4) * 160 if i < 4 else 1300 + (i % 4) * 140; y = 760 + (i // 4) * 60
        put(f, sprite(("env",), lambda c: (shape(ImageDraw.Draw(c, "RGBA"), [(900, 500), (1020, 500), (1020, 580), (900, 580)], (246, 240, 220), 1, lw=4),
                                           stroke(ImageDraw.Draw(c, "RGBA"), [(900, 500), (960, 550), (1020, 500)], lw=3))), x - 960, y - 540)
    label(f, "$165 MILLION IN BONUSES", 960, 460, 64, (255, 214, 60), (lt - 2.0) / 0.4)
    label(f, "73 OF THEM: $1M+", 960, 560, 54, (255, 255, 255), (lt - 4.0) / 0.4)

def s49(f, lt, T):          # Jake schaut Nachrichten, Muenzwurf
    d = ImageDraw.Draw(f, "RGBA"); d.rounded_rectangle([1000, 200, 1760, 660], 24, fill=(30, 30, 36), outline=INK, width=8)
    d.rectangle([1030, 230, 1730, 630], fill=(180, 40, 40)); label(f, "BREAKING NEWS", 1380, 300, 46, (255, 255, 255), 1.0, 0)
    label(f, "AIG BONUSES", 1380, 440, 70, (255, 255, 255), 1.0, 0)
    shake = math.sin(lt * 8) * 18 if lt > 1.0 else 0
    bust_spr(f, JAKE45, 520, 620, 200, 1, "frown", 0.12, seed=241, dx=shake)
    if lt > T * 0.55:
        label(f, "HEADS: THEY WIN", 1380, 800, 54, (255, 214, 60), (lt - T * 0.55) / 0.4)
        label(f, "TAILS: YOU LOSE", 1380, 900, 54, (255, 120, 110), (lt - T * 0.7) / 0.4)

def s50(f, lt, T):          # Kuechentisch, Jake & Ryan 45, Dollar, dann 3 Regeln
    fig(f, JAKE45, 640, 700, 90, 1, mouth="line", seed=251, seated=True)
    fig(f, RYAN45, 1280, 700, 90, -1, mouth="smile", seed=252, seated=True)
    put(f, sprite(("bill_tbl",), lambda c: real_bill(c, 960, 720, 240, value="1")))
    rules = ("1  Cash loses value → own things", "2  New money hits assets first", "3  Debt only for things that grow")
    for i, r in enumerate(rules):
        if lt > T * 0.45 + i * 3.0: hand_label(f, r, 960, 860 + i * 66, 46, (255, 255, 255), (lt - T * 0.45 - i * 3.0) / 0.4)

def s51(f, lt, T):          # Regeln stehen (kurz)
    s50(f, BEATS[50]["dur"], BEATS[50]["dur"])

def s52(f, lt, T):          # Was-waere-wenn: Glas fuellt sich
    k = lt / (T * 0.8); months = int(min(240, k * 240))
    d = ImageDraw.Draw(f, "RGBA")
    d.rounded_rectangle([1240, 260, 1640, 900], 40, fill=(220, 236, 246, 120), outline=INK, width=8)
    lvl = 900 - 600 * min(1, (months / 240) ** 1.8)
    d.rectangle([1250, min(lvl, 890), 1630, 890], fill=(240, 200, 60, 220))
    if months < 240 and (lt * 3) % 1 < 0.5: put(f, sprite(("coin",), lambda c: coin(ImageDraw.Draw(c, "RGBA"), 960, 540, 38)), 1440 - 960, 200 + ((lt * 3) % 1) * 200 - 540)
    fv = sum(300 * (1 + 0.1 / 12) ** (months - j) for j in range(1, months + 1)) if months else 0
    label(f, f"AGE {25 + months // 12}", 560, 200, 70, INK, 1.0, 0)
    label(f, "$300 / MONTH", 560, 340, 60, INK, 1.0, 0)
    label(f, money(fv), 560, 560, 120, (40, 140, 80), 1.0)
    label(f, f"paid in: {money(300 * months)}", 560, 700, 50, INK, 1.0, 0)
    hand_label(f, "historical avg. ~10%/yr — not guaranteed", 560, 980, 38, (90, 90, 96), 1.0)

def s53(f, lt, T):          # Nahaufnahme Dollar mit 3 Labels
    put(f, sprite(("bill_big2",), lambda c: real_bill(c, 960, 540, 900, value="1")))
    for i, s in enumerate(("4¢ OF PAPER", "TYPED INTO EXISTENCE", "WORTH LESS EVERY YEAR")):
        label(f, s, 960, 160 + i * 0 if i == 0 else (900 if i == 1 else 1000), 60, (255, 214, 60) if i != 2 else (255, 120, 110), (lt - 1.0 - i * 3.5) / 0.4)

def s54(f, lt, T):          # Jake hebt den Schein auf
    k = ease(lt / 2.0)
    put(f, sprite(("bill_tbl",), lambda c: real_bill(c, 960, 720, 240, value="1")), 0, -260 * k, rot=-10 * k)
    bust_spr(f, JAKE45, 960, 640, 200, 1, "line", -0.02, seed=261, dy=200 * (1 - k))
    if lt > 2.5: label(f, "NOW YOU KNOW THE RULES.", 960, 980, 60, (255, 255, 255), (lt - 2.5) / 0.4)

def s55(f, lt, T):          # Endkarte: ARC + Abo-Button mit Klick
    label(f, "ARC", 960, 330, 200, (255, 255, 255), lt / 0.4, 10)
    hand_label(f, "Most people never will.", 960, 480, 50, (200, 200, 206), (lt - 0.5) / 0.4)
    d = ImageDraw.Draw(f, "RGBA"); clicked = lt > 2.6
    d.rounded_rectangle([760, 600, 1160, 700], 50, fill=(90, 90, 96) if clicked else (220, 30, 36), outline=INK, width=4)
    label(f, "SUBSCRIBED" if clicked else "SUBSCRIBE", 960, 650, 44, (255, 255, 255), 1.0, 0)
    if clicked: label(f, "🔔", 1220, 650, 60, (255, 214, 60), (lt - 2.7) / 0.3, 0)
    k = ease((lt - 1.0) / 1.4); cx, cy = 1500 - 450 * k, 900 - 230 * k
    if lt > 2.5 and lt < 2.7: cx, cy = cx + 2, cy + 3
    d.polygon([(cx, cy), (cx + 34, cy + 80), (cx + 46, cy + 50), (cx + 78, cy + 44)], fill=(255, 255, 255), outline=INK)

SCENES = [  # (Hintergrund-Key, Hintergrund-Funktion, Szene)
    ("ledger", None, s00), ("street", street_bg, s01), ("grey", grey_bg, s02), ("grey", grey_bg, s03), ("ledger", None, s04),
    ("bank", bank_bg, s05), ("bank", bank_bg, s06), ("grey", grey_bg, s07), ("town", town_bg, s08), ("grey", grey_bg, s09),
    ("office", office_bg, s10), ("office", office_bg, s11), ("grey", grey_bg, s12), ("street", street_bg, s13), ("dark", dark_bg, s14),
    ("grey", grey_bg, s15), ("grey", grey_bg, s16), ("grey", grey_bg, s17), ("grey", grey_bg, s18), ("grey", grey_bg, s19),
    ("grey", grey_bg, s20), ("coffee", coffee_bg, s21), ("dark", dark_bg, s22), ("fed_n", fed_bg, s23), ("grey", grey_bg, s24),
    ("city_d", lambda: city_bg(True), s25), ("grey", grey_bg, s26), ("street", street_bg, s27), ("street", street_bg, s28), ("apt", apartment_bg, s29),
    ("groc71", lambda: grocery_bg("1971"), s30), ("grocnow", lambda: grocery_bg("TODAY"), s31), ("grey", grey_bg, s32), ("grey", grey_bg, s33), ("grey", grey_bg, s34),
    ("glass", glass_office_bg, s35), ("grey", grey_bg, s36), ("bank", bank_bg, s37), ("grey", grey_bg, s38), ("office", office_bg, s39),
    ("ledger", None, s40), ("grey", grey_bg, s41), ("grey", grey_bg, s42), ("grey", grey_bg, s43), ("svb", svb_bg, s44),
    ("dark", dark_bg, s45), ("vault", vault_bg, s46), ("wall", wallstreet_bg, s47), ("aig", aig_bg, s48), ("apt", apartment_bg, s49),
    ("kitchen", kitchen_bg, s50), ("kitchen", kitchen_bg, s51), ("grey", grey_bg, s52), ("ledger", None, s53), ("kitchen", kitchen_bg, s54), ("ledger", None, s55),
]
assert len(SCENES) == len(BEATS), (len(SCENES), len(BEATS))

def chapter_wall(gt, i, lt):
    """Kapitel-Trennwand: dunkle Kontozahlen, grosse Nummer + Titel, kurzer Zoom. lt in 0..WALL."""
    f = LEDGER.frame(gt).convert("RGBA"); t1, t2 = CHAPTERS[i]; k = ease(lt / 0.35); out = min(1, (WALL - lt) / 0.25)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle([0, 420, W, 660], fill=(10, 12, 18, int(200 * k)))
    fz = int(120 * (1.25 - 0.25 * k)); d.text((960, 495), t1, font=ImageFont.truetype(BOLD, fz), fill=(255, 214, 60, int(255 * k)), anchor="mm", stroke_width=6, stroke_fill=INK)
    d.text((960, 600), t2, font=ImageFont.truetype(BOLD, 52), fill=(255, 255, 255, int(255 * ease((lt - 0.2) / 0.3))), anchor="mm")
    f.alpha_composite(lay)
    if out < 1: f = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), f, max(0, out))
    return f.convert("RGB")

def camera(f, i, lt, T):
    """3-5-Sekunden-Regel: Einstellungen wechseln alle ~4 s (sanfter Push-in, Nahe auf den Fokus, Pull-out).
    Zusaetzlich kurzes 'Landen' (Mini-Zoom 4 %) am Anfang jeder Szene. Keine Kamera auf Titel/Ledger."""
    SEG = 4.0; s_ = int(lt / SEG); u = (lt - s_ * SEG) / SEG
    fx, fy = PUNCH[i][:2] if i in PUNCH else (960, 560); med = PUNCH[i][2] if i in PUNCH else 1.0
    shot = (i + s_) % 3 if T > SEG * 1.2 else 0
    if shot == 0:   z = 1.0 + 0.05 * inout(min(1, lt / max(T, 0.1))) if T <= SEG * 1.2 else 1.0 + 0.05 * u
    elif shot == 1: z = (min(med, 1.18) + 0.03 * u) if med > 1.0 else 1.06 + 0.02 * u
    else:           z = 1.07 - 0.06 * u
    if shot != 1: fx, fy = 960 + (fx - 960) * 0.3, 540 + (fy - 540) * 0.3
    z *= 1 + 0.04 * (1 - ease(lt / 0.3))
    if kit16.LBOX:                       # nie Text abschneiden: Zoom so begrenzen, dass alle Einblendungen im Bild bleiben
        m_ = 24; ux0 = max(0, min(b_[0] for b_ in kit16.LBOX) - m_); uy0 = max(0, min(b_[1] for b_ in kit16.LBOX) - m_)
        ux1 = min(W, max(b_[2] for b_ in kit16.LBOX) + m_); uy1 = min(H, max(b_[3] for b_ in kit16.LBOX) + m_)
        z = min(z, W / max(1, ux1 - ux0), H / max(1, uy1 - uy0))
    else: ux0 = uy0 = None
    if z <= 1.001: return f
    w_, h_ = int(W / z), int(H / z)
    x0 = min(max(0, fx - w_ / 2), W - w_); y0 = min(max(0, fy - h_ / 2), H - h_)
    if ux0 is not None:
        x0 = min(max(x0, ux1 - w_), ux0); y0 = min(max(y0, uy1 - h_), uy0)
        x0 = min(max(0, x0), W - w_); y0 = min(max(0, y0), H - h_)
    x0, y0 = int(x0), int(y0)
    return f.crop((x0, y0, x0 + w_, y0 + h_)).resize((W, H), Image.BILINEAR)

PUNCH = {3: (480, 600, 1.35), 5: (960, 640, 1.2), 6: (1100, 600, 1.25), 8: (960, 540, 1.2), 10: (920, 560, 1.3), 13: (960, 600, 1.2),
         19: (960, 700, 1.3), 27: (1400, 540, 1.3), 29: (1000, 700, 1.3), 35: (1000, 640, 1.3),
         37: (960, 640, 1.25), 39: (900, 560, 1.2), 42: (480, 640, 1.3), 46: (960, 540, 1.15), 48: (960, 600, 1.2), 49: (960, 560, 1.12), 50: (960, 640, 1.25)}

def beat_at(gt):
    for i, b in enumerate(BEATS):
        if gt < b["end"]: return i, b
    return len(BEATS) - 1, BEATS[-1]

def frame_at(gt):
    i, b = beat_at(gt); lt = gt - b["t0"]; key, fn, sc = SCENES[i]
    kit16.CLK["t"], kit16.CLK["beat"] = gt, i
    pre = PRE.get(i, 0.0)
    if lt < pre: return chapter_wall(gt, i, lt)
    lt -= pre; T = b["dur"] - pre; kit16.LBOX.clear()
    f = (LEDGER.frame(gt) if key == "ledger" else bg(key, fn).copy()).convert("RGBA"); sc(f, lt, T)
    if key != "ledger" and i != 4: f = camera(f, i, lt, T)
    if lt < 0.1 and i not in PRE: f = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), f, 0.55 + 0.45 * lt / 0.1)
    return f.convert("RGB")

# ======================= Ton (ohne Stimme) =======================
def music_bed(n):
    """Leise Spannungsflaeche, Akkord wechselt je Kapitel (Moll -> am Ende hell)."""
    t = np.arange(n) / SR; out = np.zeros(n, np.float32)
    roots = {0: 55.0, 5: 58.27, 10: 61.74, 17: 55.0, 23: 51.91, 30: 55.0, 35: 49.0, 42: 51.91, 44: 46.25, 50: 65.41}
    keys = sorted(roots); starts = [BEATS[k]["t0"] for k in keys] + [TOTAL + 1]
    for j, k in enumerate(keys):
        a, e = int(starts[j] * SR), min(n, int(starts[j + 1] * SR) + SR)
        tt = t[a:e]; r = roots[k]; minor = k != 50
        ch = [r, r * 1.5, r * 2, r * (2.378 if minor else 2.52)]
        seg = sum(np.sin(2 * np.pi * f_ * tt + i) / (i + 1) for i, f_ in enumerate(ch)) * 0.25
        pulse = np.sin(2 * np.pi * r * 0.5 * tt) * np.exp(-((tt * (84 / 60)) % 1) * 7) * 0.4
        env = np.minimum(1, (tt - tt[0]) / 1.5) * np.minimum(1, (tt[-1] - tt) / 1.5)
        out[a:e] += ((seg + pulse) * env).astype(np.float32)
    blk = SR * 30; res = np.zeros_like(out)
    for a0 in range(0, n, blk):                      # blockweise filtern (spart Speicher)
        a1 = min(n, a0 + blk + SR); res[a0:min(n, a0 + blk)] = sfx.band(out[a0:a1].astype(np.float32), 30, 3000)[:min(n, a0 + blk) - a0]
    return sfx.norm(res, 0.9)

class X:                                  # alte Platzhalter -> echte ElevenLabs-Sounds (dezent)
    @staticmethod
    def _cut(name, d):
        a = SFXL.load(name)[:int(d * SR)].copy(); f_ = min(len(a), SR // 15); a[-f_:] *= np.linspace(1, 0, f_); return a
    whoosh = staticmethod(lambda d=0.45: X._cut("whoosh", d + 0.35))
    boom = staticmethod(lambda d=1.8: SFXL.load("impact"))
    thud = staticmethod(lambda d=0.5, f=70: SFXL.load("stamp"))
    rustle = staticmethod(lambda d=0.8: SFXL.load("paper"))
    crowd = staticmethod(lambda d=3.0, g=0.3: sfx.crowd(d, g))
    hiss = staticmethod(lambda d=1.4: np.zeros(1, np.float32))
    clank = staticmethod(lambda d=0.6, base=620: np.zeros(1, np.float32))
    t = staticmethod(lambda *a: np.zeros(1, np.float32))
    L = staticmethod(SFXL.load)

MOODS = [(0, "mystery"), (3, "drive"), (5, "drive"), (10, "mystery"), (17, "drive"), (23, "dark"), (30, "mystery"),
         (35, "drive"), (42, "dark"), (44, "dark"), (50, "uplift")]

def mix():
    n = int((TOTAL + 1) * SR); fx = np.zeros(n, np.float32); sfx = X; manual = []
    def add(s, x, g):
        if len(x) < 2: return
        i = int(max(0, s) * SR); x = x[:max(0, n - i)]; fx[i:i + len(x)] += x * g * 0.8; manual.append(s)
    B = BEATS
    def T(i, frac=0.0, plus=0.0): p_ = PRE.get(i, 0.0); return B[i]["t0"] + p_ + frac * (B[i]["dur"] - p_) + plus
    add(T(0, 0.65), sfx.rustle(0.8), 0.5); add(T(0, 0.7), sfx.thud(0.4, 120), 0.3)
    add(T(1), sfx.crowd(4.0, 9), 0.08)
    add(T(4), sfx.boom(1.8), 0.55)
    for i in CHAPTERS:                                    # Kapitelwand: Impact rein, Whoosh raus
        add(B[i]["t0"], X.L("impact"), 0.5); add(B[i]["t0"] + WALL - 0.3, sfx.whoosh(0.4), 0.22)
    add(T(0, 0.05), X.L("flutter"), 0.35); add(T(4) - 1.2, X.L("riser"), 0.22); add(T(3), X.L("stinger"), 0.3)
    add(T(5, plus=3.2), X.L("ding"), 0.3); add(T(6, plus=1.0), X.L("flutter"), 0.3)
    add(T(11, plus=1.0), X.L("typing"), 0.25); add(T(45, plus=0.2), X.L("counter"), 0.25)
    for k in range(6): add(T(5, plus=k * 0.5), sfx.t(0.0) if False else (np.zeros(1)), 0)
    add(T(7, plus=1.5), sfx.rustle(0.6), 0.35)
    add(T(8, plus=1.0), sfx.whoosh(0.4), 0.2)
    add(T(9, plus=0.4), sfx.thud(0.6, 50), 0.45)
    add(T(10, plus=1.5), sfx.rustle(0.6), 0.4)
    add(T(11, plus=3.5), sfx.thud(0.5, 70), 0.5)
    add(T(12, plus=1.5), sfx.rustle(1.0), 0.3)
    add(T(14, plus=0.5), sfx.hiss(3.5) if hasattr(sfx, "hiss") else np.zeros(1), 0.1)
    add(T(16, plus=0.3), sfx.thud(0.6, 60), 0.8)
    add(T(18, plus=0.6), sfx.thud(0.6, 55), 0.7)
    add(T(20, 0.6), sfx.boom(1.4), 0.4)
    add(T(21, plus=1.5), sfx.whoosh(0.6), 0.3)
    add(T(22, 0.45), sfx.boom(1.4), 0.5)
    add(T(24, 0.6), sfx.thud(0.6, 50), 0.6)
    add(T(26), sfx.whoosh(1.0), 0.2)
    add(T(29, plus=0.6), sfx.rustle(0.6), 0.4); add(T(29, plus=2.5), sfx.thud(0.5, 60), 0.6)
    add(T(31, plus=2.5), sfx.thud(0.4, 80), 0.4)
    add(T(40, plus=0.6), sfx.thud(0.6, 50), 0.7); add(T(40, plus=1.9), sfx.thud(0.6, 50), 0.7); add(T(40, plus=3.2), sfx.boom(1.6), 0.8)
    add(T(41, plus=0.3), sfx.thud(0.6, 55), 0.7)
    add(T(43, 0.75, 1.0), sfx.thud(0.5, 60), 0.6); add(T(43, 0.75, 2.5), sfx.thud(0.5, 60), 0.6)
    add(T(44), sfx.crowd(10.0, 1.0), 0.35)
    add(T(46, plus=2.0), sfx.thud(0.8, 45), 0.8)
    add(T(47, plus=1.0), sfx.whoosh(0.5), 0.3); add(T(48, plus=2.0), sfx.rustle(1.2), 0.4)
    add(T(49, 0.55), sfx.clank(0.4, 900), 0.4)
    add(T(53, plus=1.0), sfx.thud(0.4, 90), 0.3)
    add(T(55), sfx.boom(2.0), 0.5)
    # Auto-Sounds (grosse Einblendungen) nur, wenn >= 2,5 s Abstand zu allen anderen Sounds -> nie zu viel
    taken = sorted(manual)
    for (t_, name, g, kind) in sorted(kit16.EVENTS):
        if kind == "steps":
            if t_ < TOTAL: add_raw = SFXL.load("steps"); i0 = int(t_ * SR); x_ = add_raw[:max(0, n - i0)]; fx[i0:i0 + len(x_)] += x_ * g
            continue
        if all(abs(t_ - u) >= 2.5 for u in taken):
            x_ = SFXL.load(name); i0 = int(t_ * SR); x_ = x_[:max(0, n - i0)]; fx[i0:i0 + len(x_)] += x_ * g; taken.append(t_)
    voice = np.zeros(n, np.float32)
    for i, a in VO.items():
        st = int((B[i]["t0"] + PRE.get(i, 0.0) + 0.08) * SR); voice[st:st + len(a)] += a[:max(0, n - st)]
    cs = np.concatenate([[0.0], np.cumsum(np.abs(voice), dtype=np.float64)]); idx = np.arange(n)
    lo, hi = np.clip(idx - 2400, 0, n), np.clip(idx + 2400, 0, n); vabs = ((cs[hi] - cs[lo]) / 4800).astype(np.float32)
    del cs, idx, lo, hi
    duck = 1 - 0.5 * np.clip(vabs / 0.05, 0, 1)
    secs = [(B[i]["t0"], m) for i, m in MOODS]
    mus = music.build(n, secs) * 0.2 * duck
    out = voice * 1.0 + fx * 0.75 + mus; m = np.abs(out).max(); out = out / m * 0.95 if m > 0.95 else out
    return out[:int(TOTAL * SR)].astype(np.float32)

if __name__ == "__main__":
    print(f"Laenge {TOTAL / 60:.1f} min")
    if "--stills" in sys.argv:
        os.makedirs("stills", exist_ok=True); tiles = []
        for i, b in enumerate(BEATS):
            im = frame_at(b["t0"] + b["dur"] * 0.7); im.save(f"stills/{i:02d}.jpg", quality=88); tiles.append(im)
        tw, th, cols = 320, 180, 8
        sheet = Image.new("RGB", (cols * (tw + 6) + 6, ((len(tiles) + cols - 1) // cols) * (th + 6) + 6))
        for i, t in enumerate(tiles): sheet.paste(t.resize((tw, th)), (6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + 6)))
        sheet.save("STORYBOARD.jpg", quality=90); print("stills ok"); sys.exit()
    a0 = float(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else 0.0
    a1 = float(sys.argv[sys.argv.index("--to") + 1]) if "--to" in sys.argv else (BEATS[9]["end"] if "--preview" in sys.argv else TOTAL)
    name = "ARC_Money_HowMoneyReallyWorks.mp4" if a0 == 0 and a1 == TOTAL else f"ARC_Money_part_{int(a0)}_{int(a1)}.mp4"
    if "--preview" in sys.argv: name = "ARC_Money_PREVIEW.mp4"
    out = av.open(name, "w")
    vs = out.add_stream("libx264", rate=FPS); vs.width, vs.height, vs.pix_fmt = W, H, "yuv420p"; vs.options = {"crf": "19", "preset": "medium"}
    ast = out.add_stream("aac", rate=SR); ast.layout = "mono"
    N = int((a1 - a0) * FPS)
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
