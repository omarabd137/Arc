# ARC Agenten-System (Stand 08.11.2026)

Grundlage: nur eigene, gemessene Daten (Masterplan Teil 28–36, Shorts #05/#07, Analyse der Top-Shorts) und Werkzeuge, die hier nachweislich laufen. Externe "Best Practices" ohne Beleg sind nicht aufgenommen.

## Feste Leitplanken (gelten für jeden Agenten)
- Nische: Business / Geld / Tech (nicht Schul-Wissenschaft). Cartoon im Crayon-Prinzip.
- Rote Linien Shorts: >=75 % angesehen statt weggewischt, >=75 % bis zum Ende, Ø-Sehdauer > Videolänge. Länge <= 1:00.
- Kein CTA in Shorts. Longform: max. 2 s Abo-Hinweis am Ende.
- Nur lizenziertes Material. Preis nennen vor jeder bezahlten Generierung. Keine Testgenerierungen. Sprachaufnahmen nie verändern.
- Veröffentlichen, Löschen, Geld ausgeben: nur nach Omars Ja.

## Agenten

| # | Agent | Aufgabe | Eingabe -> Ausgabe | Qualitätskriterium | Werkzeug |
|---|---|---|---|---|---|
| 1 | Scout | Themen + Viralität | Kanal-Daten, YouTube-Suche -> Themenkarte (3 Kandidaten, Beleg-Views) | Thema teilbar, in Nische, Person/Zahl/Riesending; Beleg: ähnliches Video >1 Mio Views | Browser (ytInitialData, kostenlos) |
| 2 | Faktenprüfer | jede Zahl mit Quelle | Skript -> Quellenliste | Keine erfundene Zahl, Nuancen sauber (Lehre: Bezos-Steuer) | Browser/Web |
| 3 | Short-Autor | Hook + Skript | Themenkarte -> Skript mit Szenenliste | Satz 1 = konkrete Szene, Thema in Frame 0, eine Kette, Pointe zuletzt, Loop, ruhiger Ton | Masterplan Teil 32 |
| 4 | Longform-Autor | Hook, Preview, Mini-Hooks | Themenkarte -> Skript | Teil 26: Neues alle 3–5 s, kein Zoom | Masterplan Teil 26/30 |
| 5 | Packaging | Titel, Cover, Beschreibung | Skript -> 3 Titel, Cover | Titel = Neugier + Person/Zahl; Cover = Frame 0 ohne Text-Müll | Canva (Kontrolle), Python |
| 6 | Sprecher | Narration | Skript -> mp3 + Wortzeiten | Brian, ruhig; v2 sauber / v4 nur sanfte Tags; 1 Take | ElevenLabs |
| 7 | Bildregie | Figuren, Orte, Logos, Karten | Szenenliste -> Assets | Wiedererkennung ohne Namen (Test), echte Logos/Karten, ganze Körper | crayon2.py, props, Natural Earth |
| 8 | Animation/Schnitt | Rendering wortgenau | Assets + Wortzeiten -> mp4 | Neues Bild alle 1–3 s, Bewegung logisch, 1080x1920/30 | Python, PIL, PyAV |
| 9 | Sound | leises Beat-Bett + SFX | Video -> Mix | Bett-Verhältnis 0,12–0,27, SFX auf echten Aktionen, keine Melodie | sfx_lib (24 SFX), Synthese |
| 10 | QA-Tor | Abnahme vor Veröffentlichung | mp4 -> Bestanden/Fehlerliste | automatisch: <=60 s, Bett-Wert, Schnittdichte, Frame-0-Thema, Lautheit; dann Omars Vorschau | Python-Prüfskript |
| 11 | Auswerter | Zahlen nach 24 h | Studio-Daten -> Zeile in SHORTS_ZEITTEST.csv + Lehre | Vergleich mit roten Linien, Ursache benannt | Omars Screenshots |
| 12 | Produzent | Reihenfolge, Credits, Termine | alles -> Tagesplan | Credit-Budget, Preis vorab, Tore eingehalten | scheduled-tasks |

## Ablauf (Short)
Scout -> **Tor 1: Omar wählt Thema** -> Autor + Faktenprüfer -> **Tor 2: Omar gibt Skript frei** -> Sprecher (Preis vorab) -> Bildregie -> Schnitt -> Sound -> QA-Tor -> **Tor 3: Omars Vorschau** -> Packaging -> **Tor 4: Omar veröffentlicht (00:00 DE für US-Welle)** -> Auswerter nach 24 h -> Lehre zurück an Scout/Autor.

## Longform-Unterschied
Eigener Autor (Teil 26: Preview, Mini-Hooks, Kapitelmusik erlaubt), 3–5 s Wechsel, Thumbnail zählt stark, Donnerstag 19:00 DE. Shorts: kein Thumbnail-Spiel, Frame 0 ist das Cover, keine Musik-Melodie, kein CTA.

## Was nachts ohne Omar laufen kann
Ja: Themenrecherche (Scout), Skriptentwürfe, Faktenprüfung, Rendern mit vorhandener Stimme, QA-Prüfung, Auswertung von Daten, die Omar bereitgestellt hat.
Nein (wegen deiner Regeln): bezahlte Stimmen, Veröffentlichen, Löschen.
Daher: "Schlafmodus" = morgens liegt ein fertiges Paket (Thema, Skript, ggf. gerendertes Video) zur Freigabe bereit.

## Aufbau-Reihenfolge (schnellster messbarer Effekt)
1. **QA-Tor + Auswerter**: billig, sofort messbar; verhindert Flops wie #07 (23 % angesehen) vor dem Posten.
2. **Hook-Test im Autor**: 3 Hook-Varianten, Auswahl nach Frame-0-Regel; Ziel: Anfangs-Wischrate von 77 % auf unter 25 % bringen.
3. **Bildregie – Personen-Ähnlichkeit**: größter bekannter Schwachpunkt; "Wer ist das?"-Test oder Illustrator für wiederkehrende Personen.
4. **Scout automatisieren** (geplante Aufgabe, kostenlose Browser-Analyse).
5. **Longform-Strecke** erst danach.

## Bewusst nicht aufgenommen
- GitHub-Automatisierung / Open-Source-Zusatztools: nicht geprüft, daher keine Empfehlung. Vorhanden und ausreichend: PyAV, PIL, numpy.
- Allgemeine Retention-/Thumbnail-Regeln aus dem Netz: nicht extern recherchiert, nur durch eigene Daten Belegtes ist drin. Auf Wunsch gezielte Recherche.

## Recherche 08.11.2026 (was belegt ist und was nicht)
Belegt durch offizielle YouTube-Seiten:
- "Viewed vs. swiped away" ist eine offizielle Studio-Kennzahl für Shorts (support.google.com/youtube/answer/12942217). Offizielle Texte benennen sie uneinheitlich ("Stayed to watch"/"How many chose to view").
- Test & compare: bis zu 3 Titel/Thumbnails je Video, Sieger nach **Watch Time**, nicht nach CTR (support.google.com/youtube/answer/16391400). Gilt für Longform; Shorts-Tests laut Drittquellen eingeschränkt, nicht verifiziert.
- Upload per API: Projekte, die nach 28.07.2020 erstellt und nicht auditiert sind, laden nur **privat** hoch (developers.google.com/youtube/v3/docs/videos/insert). Quota-Kosten widersprüchlich (1 vs. 1.600 Einheiten), nicht bestätigt.
- Views zählen seit 31.03.2025 bei Start/Wiederholung ohne Mindestdauer; Monetarisierung nutzt "engaged views" (nur Drittquellen für Details).
Nur Drittquellen (Blogs, Tool-Anbieter), als Richtwert, nicht als Fakt: 3-s-Hook, Wischrate unter 30 %, Bildwechsel alle 2–5 s. Deckt sich mit unseren eigenen Daten, ist aber nicht unabhängig belegt.
Open Source (nur Suchtreffer, Inhalte nicht geprüft, GitHub lieferte 503): WhisperX (Wortzeiten aus Audio), stable-ts (Abgleich mit bekanntem Text), python-lottie (Lottie-Dateien), faceless-youtube-agents und yt-faceless-automation (Agentenaufbau, ungeprüft). Nicht übernommen, solange Lizenz und Qualität nicht gelesen sind. Manim passt nicht zu Cartoon-Figuren.
Folgerung: Die automatische Veröffentlichung ist technisch nur privat/als Entwurf möglich, bis ein Audit besteht. Das Posten bleibt bei dir.

## Ausbau 08.11.2026 (zweite Runde)
- Agenten jetzt 14: + arc-strategie (Nische, Zielgruppe, Formate, Serien, Posting-Zeit, Wochenplan), + arc-distribution (TikTok-Pakete, Clips aus Longform, Community-Posts, Pins). Alle Agenten haben vollen Zugriff auf Web und Browser.
- Abdeckung deiner 15 Bereiche: Nische/Zielgruppe + Strategie + A/B-Plan -> arc-strategie; Skript/Storyboard -> Autoren; Voice -> arc-sprecher; Assets + Ebenen -> arc-bildregie; Animation + Schnitt + Loop -> arc-schnitt; Sound -> arc-sound; Packaging + Metadaten + Pins -> arc-packaging; Analytics + A/B-Auswertung -> arc-auswerter; Templates/System -> arc-produzent; Distribution -> arc-distribution.
- Abweichung: "Zooms" aus deiner Liste widerspricht deiner Regel "kein Kamerazoom". Bleibt verboten; Schwenks (Pans) und Pattern Interrupts sind erlaubt.
- Nachtschicht: geplante Aufgabe arc-nachtschicht täglich ca. 05:00 (kostenlos): Trends + 3 Themen -> ARC_Master/MORGENBERICHT_<Datum>.md. Läuft nur, wenn die App offen ist.
- Studio-Daten direkt: Optionen (Verbinden machst du selbst per Google-Login):
  1. Metricool (Connector, Free-Plan laut Drittquellen; Analytics, beste Posting-Zeit, Planung).
  2. Windsor.ai (Connector; YouTube-Retention-Kennzahlen; für Claude-Connector laut eigener Seite Bezahlplan ab ~$19/Monat).
  3. Kostenlos und am vollständigsten: eigenes Google-Cloud-Projekt + YouTube Analytics API + Open-Source-MCP (z. B. youtube-studio-mcp). Du legst den OAuth-Client an; ich richte den Rest ein. Repo-Inhalt noch nicht geprüft.
- GitHub: kein GitHub-Connector im Verzeichnis, gh-CLI nicht installiert. Nutzen für uns: Versionierung der Skripte (git läuft bereits). Video-Rendering über GitHub Actions bringt nichts, weil unser Stack lokal läuft.
