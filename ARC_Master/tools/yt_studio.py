"""ARC Studio-Werkzeug: liest echte Kanal- und Analytics-Daten über die offiziellen Google-APIs.

Befehle:
  python yt_studio.py auth                       # einmalig: Google-Fenster, Omar klickt "Zulassen"
  python yt_studio.py channel                    # Kanal-Eckdaten
  python yt_studio.py videos [N]                 # letzte N Uploads mit Views/Likes/Kommentaren/Dauer
  python yt_studio.py stats VIDEO_ID [TAGE]      # Views, Ø-Sehdauer, Ø-Anteil, Likes, Abos, Shares
  python yt_studio.py retention VIDEO_ID         # Retention-Kurve (Anteil Zuschauer je Position)
  python yt_studio.py countries VIDEO_ID         # Länder
  python yt_studio.py traffic VIDEO_ID           # Traffic-Quellen
  python yt_studio.py days [TAGE]                # Kanal pro Tag
  python yt_studio.py upload DATEI TITEL BESCHR TAGS --confirm   # nur mit Omars Ja; lädt PRIVAT hoch

Sicherheit: Schlüssel in ARC_Master/secrets (von Git ausgeschlossen). Upload nur mit --confirm, immer privat.
"""
import json, os, sys, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
SECRETS = os.path.join(HERE, "..", "secrets")
CLIENT = os.path.join(SECRETS, "client_secret.json")
TOKEN = os.path.join(SECRETS, "token.json")
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
    "https://www.googleapis.com/auth/youtube.upload",
]


def creds(interactive=False):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    c = Credentials.from_authorized_user_file(TOKEN, SCOPES) if os.path.exists(TOKEN) else None
    if c and c.expired and c.refresh_token:
        c.refresh(Request())
    if not c or not c.valid:
        if not interactive:
            sys.exit("Nicht angemeldet. Erst: python yt_studio.py auth")
        from google_auth_oauthlib.flow import InstalledAppFlow
        c = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES).run_local_server(port=0, prompt="consent")
    open(TOKEN, "w").write(c.to_json())
    return c


def yt():
    from googleapiclient.discovery import build
    return build("youtube", "v3", credentials=creds(), cache_discovery=False)


def ya():
    from googleapiclient.discovery import build
    return build("youtubeAnalytics", "v2", credentials=creds(), cache_discovery=False)


def out(x):
    print(json.dumps(x, indent=1, ensure_ascii=False))


def report(metrics, dims=None, filters=None, days=28, sort=None, maxr=None):
    end = dt.date.today(); start = end - dt.timedelta(days=days)
    q = dict(ids="channel==MINE", startDate=str(start), endDate=str(end), metrics=metrics)
    if dims: q["dimensions"] = dims
    if filters: q["filters"] = filters
    if sort: q["sort"] = sort
    if maxr: q["maxResults"] = maxr
    r = ya().reports().query(**q).execute()
    cols = [h["name"] for h in r.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in r.get("rows", [])]


def main(a):
    cmd = a[0] if a else "help"
    if cmd == "auth":
        creds(interactive=True); print("Angemeldet, Token gespeichert.")
    elif cmd == "channel":
        r = yt().channels().list(part="snippet,statistics,contentDetails", mine=True).execute()
        ch = r["items"][0]
        out(dict(title=ch["snippet"]["title"], id=ch["id"], **ch["statistics"]))
    elif cmd == "videos":
        n = int(a[1]) if len(a) > 1 else 15
        y = yt()
        up = y.channels().list(part="contentDetails", mine=True).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        ids = [i["contentDetails"]["videoId"] for i in y.playlistItems().list(part="contentDetails", playlistId=up, maxResults=min(n, 50)).execute()["items"]]
        vs = y.videos().list(part="snippet,statistics,contentDetails,status", id=",".join(ids)).execute()["items"]
        out([dict(id=v["id"], title=v["snippet"]["title"], published=v["snippet"]["publishedAt"], duration=v["contentDetails"]["duration"],
                  privacy=v["status"]["privacyStatus"], **v["statistics"]) for v in vs])
    elif cmd == "stats":
        vid = a[1]; days = int(a[2]) if len(a) > 2 else 90
        out(report("views,engagedViews,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained,subscribersLost",
                   filters=f"video=={vid}", days=days))
    elif cmd == "retention":
        out(report("audienceWatchRatio,relativeRetentionPerformance", dims="elapsedVideoTimeRatio", filters=f"video=={a[1]}", days=365))
    elif cmd == "countries":
        out(report("views,averageViewDuration", dims="country", filters=f"video=={a[1]}", days=365, sort="-views", maxr=15))
    elif cmd == "traffic":
        out(report("views", dims="insightTrafficSourceType", filters=f"video=={a[1]}", days=365, sort="-views"))
    elif cmd == "days":
        days = int(a[1]) if len(a) > 1 else 28
        out(report("views,engagedViews,estimatedMinutesWatched,subscribersGained,likes,shares", dims="day", days=days, sort="day"))
    elif cmd == "upload":
        if "--confirm" not in a:
            sys.exit("Upload nur mit Omars Ja: --confirm anhängen.")
        from googleapiclient.http import MediaFileUpload
        path, title, desc, tags = a[1], a[2], a[3], a[4]
        body = dict(snippet=dict(title=title, description=desc, tags=[t.strip() for t in tags.split(",")], categoryId="27"),
                    status=dict(privacyStatus="private", selfDeclaredMadeForKids=False))
        r = yt().videos().insert(part="snippet,status", body=body, media_body=MediaFileUpload(path, resumable=True)).execute()
        out(dict(uploaded=r["id"], privacy="private"))
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
