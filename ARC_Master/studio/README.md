# ARC Studio

Zentrale Steuerung des Kanals. Eine Datenbank (`arc_studio.db`), ein Befehl (`arc.py`).

| Befehl | Zweck |
|---|---|
| `python arc.py sync` | echte YouTube-Daten aller Videos holen (Views, Likes, Sehdauer, Feed-Anteil, USA-Anteil, Abbruchstelle) |
| `python arc.py report` | CEO-Bericht `../BERICHT_<Datum>.md` mit Fakten, Hypothesen, 3 Maßnahmen |
| `python arc.py dashboard` | `dashboard.html` |
| `python arc.py queue add "Thema" short` | Produktionsauftrag |
| `python arc.py cost <video> <credits> "<wofür>"` | Kosten buchen |
| `python arc.py experiment add "<Hypothese>" "<A>" "<B>" "<Kennzahl>"` | kontrollierter Test |

**Datenmodell:** videos (Thema, Format, Stimme, Dauer, Ordner) · snapshots (Kennzahlen je Tag) · costs · queue · experiments · decisions.
**Automatik:** geplante Aufgabe `arc-morgenbriefing` (07:00) führt sync → report → dashboard aus und schlägt das nächste Thema vor.
**Produktion:** Agenten in `.claude/agents/` (Produzent führt), Bild in `arc-remotion/`, Ton/Zusammenbau/QA in `tools/`.
