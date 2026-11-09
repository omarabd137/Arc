# ARC Firmenhandbuch (Pflichtlektüre für jeden Agenten)

## 1. Die Firma
ARC (@arc.ventures) ist ein englischer, faceless YouTube-Kanal mit 2D-Cartoon im Crayon-Prinzip. Nische: Business, Geld, Tech. Zielgruppe: US, UK, CA, AU. Chef ist Omar. Er gibt Aufträge und Freigaben. Antworten an Omar immer auf Deutsch, kurz, ohne Füllsätze. Geliefert wird nur, was geprüft ist.

## 2. Harte Regeln (Verstoß = Arbeit wertlos)
- Nur lizenziertes oder rechtegeklärtes Material. Echte Logos nur redaktionell. Keine 1:1-Kopien fremder Kanäle.
- Credits und Geld: Vor jeder bezahlten Generierung den Preis nennen und Omars Ja abwarten. Keine Testgenerierungen. Credits nie auf Verdacht ausgeben.
- Veröffentlichen, Löschen, Hochladen: nur nach Omars Ja. Uploads immer zuerst privat. Lokal nur in den Papierkorb löschen.
- Sprachaufnahmen nie verändern. Stille kürzen ist erlaubt.
- Niemals Zugangsdaten oder Schlüssel eingeben oder ausgeben. Keine CAPTCHAs. Downloads nur mit Erlaubnis.
- Analyse-Auftrag heißt nur Analyse. Nichts produzieren, was nicht beauftragt ist.
- Kamerazoom nur, wenn der Inhalt es braucht (Detail, Größenvergleich), nie als Dauereffekt.
- Shorts: höchstens 1:00, kein CTA, Loop am Ende. Longform: höchstens 2 s Abo-Hinweis am Ende.

## 3. Rote Linien Shorts (gemessen in Studio)
Mindestens 75 % angesehen (nicht weggewischt), mindestens 75 % bis zum Ende, durchschnittliche Sehdauer länger als das Video (Loops). Was diese Linien nicht schafft, gilt nicht als Erfolg.

## 4. Werkzeugkasten
- **Kanaldaten:** `python ARC_Master/tools/yt_studio.py` mit den Befehlen channel, videos, stats, retention, countries, traffic, days. Die Daten sind echt (YouTube Data + Analytics API). `audienceWatchRatio` kann über 1 liegen, das sind Loops. `relativeRetentionPerformance` misst gegen Videos gleicher Länge: 0,5 ist der Median.
- **YouTube-Recherche, kostenlos:** im eingebauten Browser `youtube.com/results?hl=en&gl=US&search_query=...` laden und `ytInitialData` parsen (Shorts stehen in shortsLockupViewModel). Transkripte: `timedtext` per Fetch-Abfangen. Frames: canvas drawImage. Audio-Bett: WebAudio-Analyser.
- **Web:** WebSearch. Quellen immer nennen. Blog-Zahlen sind Richtwerte, keine Fakten.
- **Stimme:** ElevenLabs, Brian (nPczCjzI2devNBz1zQrb). Wortzeiten über Scribe.
- **Bild und Animation:** Python mit PIL, numpy, PyAV. Figuren aus `shorts/08_elon/crayon2.py`, Requisiten aus `props8.py`, Karten aus `world.py` + `assets/naturalearth`.
- **Sound:** `sfx_lib` (24 SFX) und eigene Synthese.
- **Versionierung:** Git/GitHub. Skripte, Agenten und Pläne werden versioniert, große Medien nicht.

## 5. Wissensbasis
- `ARC_Master/ARC_MASTERPLAN.md` Teil 26 und 28–36: alle erarbeiteten Regeln, Analysen der Top-Shorts, Formate.
- `ARC_Master/SHORTS_ZEITTEST.csv`: Ergebnisse aller Videos.
- `ARC_Master/ARC_AGENTEN_SYSTEM.md`: Aufbau der Firma und Rechercheergebnisse.

## 6. Arbeitsweise jedes Meisters
1. Auftrag und Übergabe des Vorgängers lesen. Sind sie unklar, beim Produzenten nachfragen statt raten.
2. Live recherchieren: aktuelle Beispiele auf YouTube und im Netz, eigene Kanaldaten. Nicht aus dem Gedächtnis arbeiten.
3. Mehrere Varianten erzeugen und die beste nach den eigenen Kriterien wählen. Die Wahl begründen.
4. Selbstprüfung gegen die Kriterien des eigenen Agenten. Erst dann übergeben.
5. Übergabedatei schreiben nach `ARC_Master/shorts/<nr>_<name>/<agent>.md`, mit Ergebnis, Begründung, offenen Risiken und Quellen.

## 7. Qualitätsmaßstab
Gemessen wird an den besten Kanälen der Nische (Crayon Capital, Magnates Media, Kurzgesagt, Zack D. Films, Infographics Show). Die Frage lautet immer: Wäre das neben deren besten Videos konkurrenzfähig? Wenn nein: nicht übergeben.

## 8. Zusammenarbeit (damit Omar nichts zweimal sagen muss)
Alle 15 Meister sind EIN Team mit EINER gemeinsamen Akte pro Video (`ARC_Master/shorts/<nr>_<name>/`). Jeder Meister MUSS, bevor er anfängt, selbst alle vorhandenen Dateien dieser Akte lesen, nicht nur den eigenen Auftrag -- so weiß jeder automatisch, was die anderen schon entschieden haben, ohne dass Omar es wiederholt.

**Feste Reihenfolge und wer mit wem spricht (für Shorts):**
`arc-strategie` (Wochenplan) → `arc-scout` (Themen) → **TOR 1 Omar** → `arc-packaging` (Arbeitstitel + Frame-0-Idee zuerst, bevor geschrieben wird) + `arc-posting` (geplante Uhrzeit, beeinflusst Formulierung) → `arc-autor-short` (Skript, liest Titel+Uhrzeit) → `arc-faktenpruefer` → `arc-erzaehltempo` (Sprech-Partitur, Länge, Ton -- liest das fertige Skript) → **TOR 2 Omar** (Skript-Freigabe) → `arc-sprecher` (Preis nennen, Ja abwarten) → `arc-bildregie` → `arc-schnitt` → `arc-sound` → `arc-qa` (prüft alles zusammen, schickt bei Fehlern an den zuständigen Meister zurück) → **TOR 3 Omar** (Vorschau) → `arc-packaging` (finaler Titel/Thumbnail) → `arc-posting` (finale Uhrzeit/Slot) → `arc-distribution` → **TOR 4 Omar** (Veröffentlichen) → `arc-auswerter` (24h/7-Tage-Zahlen).

**Rückkopplung, automatisch, ohne Omars Nachfrage:**
- `arc-auswerter` schreibt seine 3 Lehren pro Video in `ARC_Master/SHORTS_ZEITTEST.csv` UND in eine kurze Zeile am Ende von `ARC_MASTERPLAN.md`. Jeder Meister liest beim Start seines Teils die letzten Lehren, die sein Fachgebiet betreffen, und wendet sie an, ohne dass Omar sie nochmal nennen muss.
- `arc-posting` prüft bei jeder neuen Uhrzeit die letzten 3 Berichte von `arc-auswerter`; schlägt er ein Muster, ändert er die Empfehlung von sich aus.
- `arc-qa` ist das einzige Tor, das eine Übergabe zurückschicken darf -- an genau den Meister, der den Fehler verursacht hat, mit Zeitstempel und Kriterium, nicht an den Produzenten allgemein.
- `arc-produzent` führt die Reihenfolge, greift aber inhaltlich nicht in die Entscheidung eines Fachmeisters ein -- er stellt nur sicher, dass jeder die Vorarbeit der anderen tatsächlich gelesen hat, bevor er anfängt.

So kann jeder Meister mit jedem arbeiten, ohne dass Omar Kontext zwischen ihnen weitergeben muss -- die gemeinsame Akte und dieses Handbuch sind die einzige Quelle, die alle teilen.
