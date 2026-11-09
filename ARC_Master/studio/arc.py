"""ARC STUDIO – zentrale Steuerung (eine Datenbank, ein Befehl).

  python arc.py sync              echte Kanaldaten (YouTube API) in die Datenbank holen
  python arc.py report            CEO-Bericht aus echten Daten -> ../BERICHT_<datum>.md
  python arc.py dashboard         Dashboard -> dashboard.html
  python arc.py queue add "Thema" [short|long]   Produktionswarteschlange
  python arc.py queue list
  python arc.py cost <video_key> <credits> "<wofür>"   Kosten buchen
  python arc.py experiment add "<Hypothese>" "<A>" "<B>" "<Kennzahl>"
  python arc.py status            Kurzstatus

Regeln: keine erfundenen Zahlen. Was die API nicht liefert, steht als "keine Daten".
"""
import datetime as dt
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(HERE, "arc_studio.db")
sys.path.insert(0, os.path.join(ROOT, "tools"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS videos(
  key TEXT PRIMARY KEY, yt_id TEXT UNIQUE, title TEXT, kind TEXT, folder TEXT,
  published TEXT, duration_s REAL, hook TEXT, format TEXT, voice TEXT, status TEXT);
CREATE TABLE IF NOT EXISTS snapshots(
  yt_id TEXT, taken TEXT, views INT, likes INT, comments INT, shares INT, subs INT,
  avg_view_s REAL, avg_view_pct REAL, engaged INT, shorts_traffic_pct REAL, us_pct REAL,
  drop_zone TEXT, PRIMARY KEY(yt_id, taken));
CREATE TABLE IF NOT EXISTS costs(id INTEGER PRIMARY KEY, video_key TEXT, credits REAL, item TEXT, at TEXT);
CREATE TABLE IF NOT EXISTS queue(id INTEGER PRIMARY KEY, topic TEXT, kind TEXT, status TEXT, created TEXT);
CREATE TABLE IF NOT EXISTS experiments(id INTEGER PRIMARY KEY, hypothesis TEXT, a TEXT, b TEXT, metric TEXT,
  status TEXT, result TEXT, created TEXT);
CREATE TABLE IF NOT EXISTS decisions(id INTEGER PRIMARY KEY, at TEXT, text TEXT);
"""

# Zuordnung YouTube-ID -> Projektordner (aus dem Projekt bekannt)
KNOWN = {
    "WpcrD9HVIfg": ("01_lamborghini", "shorts/01_lamborghini", "micro-story"),
    "LSzma4lpgvI": ("03_ronwayne", "shorts/03_ronwayne", "micro-story"),
    "DqZ7EC1inls": ("04_market_crash", "shorts/04_market_crash", "explainer"),
    "WfK8JlttG5Y": ("05_milk", "shorts/05_milk", "insider-secret"),
    "D4HiJsluQEo": ("07_bezos", "shorts/07_bezos", "money-secret"),
    "3-03CBM88UI": ("08_elon", "shorts/08_elon", "wealth-spend"),
    "f8yu2PC4W1g": ("09_overbooking", "shorts/09_overbooking", "law-secret"),
    "YFDipgTgDfQ": ("L01_money", "longform/01_money", "longform"),
    "vEhtA929b70": ("L02_ai", "longform/02_ai", "longform"),
}
SEED_COSTS = [("06_costco", 529, "Stimmen (nie gebaut)"), ("08_elon", 653, "Stimme v4"), ("09_overbooking", 653, "Stimme Brian v2")]


def db():
    c = sqlite3.connect(DB)
    c.executescript(SCHEMA)
    if not c.execute("SELECT 1 FROM costs LIMIT 1").fetchone():
        for k, cr, it in SEED_COSTS:
            c.execute("INSERT INTO costs(video_key,credits,item,at) VALUES(?,?,?,?)", (k, cr, it, "2026-11-08"))
    c.execute(
        "INSERT OR IGNORE INTO videos(key,title,kind,folder,format,voice,status,duration_s) VALUES(?,?,?,?,?,?,?,?)",
        ("09_overbooking", "Airlines Must Pay You Cash If They Overbook Your Flight 💰", "short", "shorts/09_overbooking",
         "law-secret", "Brian v2", "fertig, nicht gepostet", 44.2),
    )
    c.commit()
    return c


def iso_s(d):
    import re
    m = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", d or "")
    return (int(m.group(1) or 0) * 60 + int(m.group(2) or 0)) if m else None


def sync():
    import yt_studio as Y
    c = db()
    yt = Y.yt()
    up = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = [i["contentDetails"]["videoId"] for i in yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50).execute()["items"]]
    vs = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute()["items"]
    today = dt.date.today().isoformat()
    for v in vs:
        vid = v["id"]
        dur = iso_s(v["contentDetails"]["duration"])
        key, folder, fmt = KNOWN.get(vid, (vid, None, None))
        kind = "short" if dur is not None and dur <= 60 else "long"
        c.execute(
            "INSERT INTO videos(key,yt_id,title,kind,folder,published,duration_s,format,status) VALUES(?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(key) DO UPDATE SET yt_id=excluded.yt_id,title=excluded.title,published=excluded.published,duration_s=excluded.duration_s,status='veröffentlicht'",
            (key, vid, v["snippet"]["title"], kind, folder, v["snippet"]["publishedAt"], dur, fmt, "veröffentlicht"),
        )
        st = v["statistics"]
        a = {}
        try:
            r = Y.report("views,engagedViews,averageViewDuration,averageViewPercentage,shares,subscribersGained", filters=f"video=={vid}", days=365)
            a = r[0] if r else {}
            if not a.get("views"):  # Analytics noch nicht verarbeitet -> keine Daten statt 0
                a = {}
            tr = Y.report("views", dims="insightTrafficSourceType", filters=f"video=={vid}", days=365)
            tot = sum(x["views"] for x in tr) or 0
            a["shorts_pct"] = round(100 * sum(x["views"] for x in tr if x["insightTrafficSourceType"] == "SHORTS") / tot, 1) if tot else None
            co = Y.report("views", dims="country", filters=f"video=={vid}", days=365)
            ct = sum(x["views"] for x in co) or 0
            a["us_pct"] = round(100 * sum(x["views"] for x in co if x["country"] == "US") / ct, 1) if ct else None
            ret = Y.report("audienceWatchRatio", dims="elapsedVideoTimeRatio", filters=f"video=={vid}", days=365)
            if ret:
                pts = [(x["elapsedVideoTimeRatio"], x["audienceWatchRatio"]) for x in ret]
                drops = [(pts[i][0], pts[i - 3][1] - pts[i][1]) for i in range(3, len(pts))]
                z = max(drops, key=lambda d: d[1])
                a["drop"] = f"{z[0] * (dur or 0):.0f}s (−{z[1] * 100:.0f} Pkt.)"
        except Exception as e:  # Analytics hinkt 2-3 Tage hinterher
            a["err"] = str(e)[:80]
        c.execute(
            "INSERT OR REPLACE INTO snapshots VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (vid, today, int(st.get("viewCount", 0)), int(st.get("likeCount", 0)), int(st.get("commentCount", 0)),
             a.get("shares"), a.get("subscribersGained"), a.get("averageViewDuration"), a.get("averageViewPercentage"),
             a.get("engagedViews"), a.get("shorts_pct"), a.get("us_pct"), a.get("drop")),
        )
    c.commit()
    print(f"Synchronisiert: {len(vs)} Videos, Stand {today}")


def latest(c):
    return c.execute(
        "SELECT v.key,v.title,v.kind,v.duration_s,v.format,v.published,s.* FROM videos v JOIN snapshots s ON s.yt_id=v.yt_id "
        "WHERE s.taken=(SELECT MAX(taken) FROM snapshots WHERE yt_id=v.yt_id) ORDER BY v.published DESC"
    ).fetchall()


def report():
    c = db()
    rows = latest(c)
    shorts = [r for r in rows if r[2] == "short"]
    L = [f"# ARC STUDIO – CEO-Bericht {dt.date.today().isoformat()}", "", "Nur gemessene Werte. Leere Felder = API liefert (noch) nichts, meist 2–3 Tage Verzug.", "",
         "| Short | Dauer | Views | Likes | Ø Sehdauer | Ø gesehen | Abos | Shorts-Feed | USA | größter Abbruch |", "|---|---|---|---|---|---|---|---|---|---|"]
    f = lambda x, s="": "–" if x is None else f"{x}{s}"
    for r in shorts:
        (key, title, kind, dur, fmt, pub, yid, taken, views, likes, com, shares, subs, avs, avp, eng, sp, us, drop) = r
        avp = None if avp is None else round(avp, 1)
        L.append(f"| {title[:42]} | {f(dur,'s')} | {views} | {likes} | {f(avs,'s')} | {f(avp,'%')} | {f(subs)} | {f(sp,'%')} | {f(us,'%')} | {f(drop)} |")
    L += ["", "## Was die Daten zeigen (Fakten)"]
    fed = [r for r in shorts if r[16] is not None]
    if fed:
        hi = [r for r in fed if r[16] >= 50]
        lo = [r for r in fed if r[16] < 50]
        L.append(f"- Shorts mit Feed-Ausspielung ≥ 50 %: {len(hi)} · darunter: {len(lo)}. Views hängen fast vollständig an der Feed-Ausspielung.")
    usv = [r[17] for r in fed if r[17] is not None]
    if usv:
        L.append(f"- USA-Anteil bei gemessenen Shorts: {min(usv)}–{max(usv)} % (Ziel: Mehrheit US/UK/CA/AU).")
    drops = [r for r in fed if r[18]]
    for r in drops:
        L.append(f"- {r[1][:40]}: größter Zuschauerverlust bei {r[18]}.")
    L += ["", "## Hypothesen (nicht bewiesen, zu testen)",
          "- Frühe Abbrüche kommen von Einstiegen, die erst nach Sekunde 3 einen Grund zum Bleiben liefern.",
          "- Posting-Zeit 23–0 Uhr DE erhöht den US-Anteil (Vergleich nötig: gleiche Formate, unterschiedliche Zeit).",
          "", "## Die drei wichtigsten Maßnahmen"]
    q = c.execute("SELECT topic FROM queue WHERE status='offen' ORDER BY id LIMIT 1").fetchone()
    unpub = c.execute("SELECT title FROM videos WHERE yt_id IS NULL AND status LIKE 'fertig%'").fetchone()
    newest = shorts[0][1][:45] if shorts else "letztes Video"
    L += [f"1. {'Fertiges Video posten: ' + unpub[0] if unpub else 'Nach 48 h auswerten: ' + newest} (`arc.py sync` + `report`).",
          "2. Experiment: Posting-Zeit 23:00 vs. 00:00 bei zwei vergleichbaren Shorts (`arc.py experiment add`).",
          f"3. Nächstes Short: {q[0] if q else 'Thema über arc-scout bestimmen (Warteschlange leer)'}."]
    tot = c.execute("SELECT SUM(credits) FROM costs").fetchone()[0] or 0
    L += ["", f"**Credits gebucht gesamt:** {tot:.0f}"]
    out = os.path.join(ROOT, f"BERICHT_{dt.date.today().isoformat()}.md")
    open(out, "w", encoding="utf-8").write("\n".join(L))
    print(out)


def dashboard():
    c = db()
    rows = latest(c)
    qs = c.execute("SELECT id,topic,kind,status FROM queue ORDER BY id DESC").fetchall()
    ex = c.execute("SELECT hypothesis,a,b,metric,status,result FROM experiments ORDER BY id DESC").fetchall()
    cs = c.execute("SELECT video_key,SUM(credits) FROM costs GROUP BY video_key").fetchall()
    unpub = c.execute("SELECT key,title,status FROM videos WHERE yt_id IS NULL").fetchall()
    td = lambda x: "–" if x is None else x
    vrows = "".join(
        f"<tr><td>{r[1]}</td><td>{r[2]}</td><td>{td(r[3])}</td><td class=n>{r[8]}</td><td class=n>{r[9]}</td><td class=n>{td(r[13])}</td>"
        f"<td class=n>{td(r[14])}</td><td class=n>{td(r[12])}</td><td class=n>{td(r[16])}</td><td class=n>{td(r[17])}</td><td>{td(r[18])}</td></tr>" for r in rows)
    html = f"""<!doctype html><html lang=de><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>ARC Studio</title><style>
:root{{--bg:#0f1420;--card:#18202f;--tx:#e8edf5;--mu:#8fa0b8;--ac:#ffc93c}}
body{{margin:0;background:var(--bg);color:var(--tx);font:15px/1.45 system-ui,Segoe UI,sans-serif;padding:16px}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:16px;color:var(--ac);margin:22px 0 8px}}
.card{{background:var(--card);border-radius:12px;padding:12px;overflow-x:auto}} table{{border-collapse:collapse;width:100%;min-width:760px}}
th,td{{padding:7px 8px;border-bottom:1px solid #263248;text-align:left;font-size:13px}} th{{color:var(--mu);font-weight:600}} .n{{text-align:right;font-variant-numeric:tabular-nums}}
.mu{{color:var(--mu)}}</style>
<h1>ARC Studio</h1><div class=mu>Stand {dt.datetime.now():%d.%m.%Y %H:%M} · nur echte Daten (YouTube API) · – = noch keine Daten</div>
<h2>Videos</h2><div class=card><table><tr><th>Titel</th><th>Typ</th><th>Dauer s</th><th class=n>Views</th><th class=n>Likes</th><th class=n>Ø Sehdauer s</th><th class=n>Ø gesehen %</th><th class=n>Abos</th><th class=n>Shorts-Feed %</th><th class=n>USA %</th><th>größter Abbruch</th></tr>{vrows}</table></div>
<h2>Fertig, nicht veröffentlicht</h2><div class=card>{''.join(f'<div>{u[1]} <span class=mu>· {u[2]}</span></div>' for u in unpub) or '<span class=mu>keine</span>'}</div>
<h2>Produktionswarteschlange</h2><div class=card>{''.join(f'<div>#{q[0]} {q[1]} <span class=mu>· {q[2]} · {q[3]}</span></div>' for q in qs) or '<span class=mu>leer</span>'}</div>
<h2>Experimente</h2><div class=card>{''.join(f'<div><b>{e[0]}</b> <span class=mu>A: {e[1]} · B: {e[2]} · Kennzahl: {e[3]} · {e[4]} {e[5] or ""}</span></div>' for e in ex) or '<span class=mu>keine</span>'}</div>
<h2>Kosten (Credits)</h2><div class=card>{''.join(f'<div>{k}: {v:.0f}</div>' for k, v in cs)}</div></html>"""
    out = os.path.join(HERE, "dashboard.html")
    open(out, "w", encoding="utf-8").write(html)
    print(out)


def main(a):
    c = db()
    cmd = a[0] if a else "status"
    now = dt.datetime.now().isoformat(timespec="minutes")
    if cmd == "sync":
        sync()
    elif cmd == "report":
        report()
    elif cmd == "dashboard":
        dashboard()
    elif cmd == "queue" and a[1:2] == ["add"]:
        c.execute("INSERT INTO queue(topic,kind,status,created) VALUES(?,?,?,?)", (a[2], a[3] if len(a) > 3 else "short", "offen", now)); c.commit(); print("aufgenommen")
    elif cmd == "queue":
        for r in c.execute("SELECT id,topic,kind,status FROM queue ORDER BY id"):
            print(r)
    elif cmd == "cost":
        c.execute("INSERT INTO costs(video_key,credits,item,at) VALUES(?,?,?,?)", (a[1], float(a[2]), a[3], now)); c.commit(); print("gebucht")
    elif cmd == "experiment" and a[1:2] == ["add"]:
        c.execute("INSERT INTO experiments(hypothesis,a,b,metric,status,created) VALUES(?,?,?,?,?,?)", (a[2], a[3], a[4], a[5], "geplant", now)); c.commit(); print("angelegt")
    else:
        n = c.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
        q = c.execute("SELECT COUNT(*) FROM queue WHERE status='offen'").fetchone()[0]
        cr = c.execute("SELECT SUM(credits) FROM costs").fetchone()[0] or 0
        print(f"Videos {n} · offene Aufträge {q} · Credits {cr:.0f}")


if __name__ == "__main__":
    main(sys.argv[1:])
