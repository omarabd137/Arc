# Short #09 Overbooking: Kreativ-Abnahme (arc-kreativdirektor)

Stand 08.11.2026. Geprüft: ARC_Short09_Overbooking.mp4 (44,2 s, 1080x1920, 30 fps), QA_sheet.png, Einzelframes 0,0 / 0,6 / 3,5 / 10,5 / 14,5 / 16,8–25,0 / 27,5 / 29,5 / 38,6 / 41,3 / 43,5 s in voller Auflösung. Zum Vergleich: ARC_Short08_Elon_v2.mp4 (jede 2. Sekunde).
Ich prüfe nur das Gesamtbild. Fakten, Timing und Lautheit prüft arc-qa.

## Urteil: NICHT BESTANDEN. Ein Pflichtfehler, schnell zu beheben (nur neu rendern, keine Credits)

Insgesamt wirkt das Video wie aus einem Guss. Der Pflichtfehler betrifft die Untertitel-Komponente, nicht das Bild selbst. Ist er behoben, gebe ich frei. Die Punkte 2–7 sind Empfehlungen und blockieren nicht.

## Gesamtbild

| Kriterium | Ergebnis |
|---|---|
| Eine Farbwelt | Ja. Gate-Welt in Blau, Petrol und Sonnenuntergangs-Gelb zieht sich durch. Sitzplan (4–6 s) in Navy-Blaupause, Klemmbrett (32–33 s) und Lounge (35–37 s) in warmem Braun und Abendrot, Kabine (38–40 s) in Grau-Blau. Das sind bewusste Stimmungswechsel aus derselben Palette, kein Bruch. Geld-Grün und Gold kommen nur an Geld-Momenten vor. |
| Ein Stil | Ja. Alle Figuren haben dieselbe Bauart: großer runder Kopf, weiße Sticker-Kontur, dicke Linien, flache Farben. Keine Szene fällt heraus. Der Held (blaues Hemd, keine Brille) bleibt in jeder Szene gleich. Die Sonnenbrille in der Lounge ist ein gewollter Gag und kein Standard-Look, also ok. |
| Echte Orte | Ja. Gate, Fluggastbrücke, Schalter, Fallblatt-Tafel, Kabinensitz 23A, Lounge, alles sofort erkennbar. Genau das wurde bei früheren Videos verlangt. |
| Wiedererkennung echter Personen | Entfällt, keine echte Person im Video. |
| Packaging passt zum Inhalt | Ja. Der Titel „Airlines Must Pay You Cash By Law“ wird bei 27 s wörtlich eingelöst: „MAX BY LAW $2,150“, U.S.-Law-Siegel, Geldregen. |
| Loop | Funktioniert. Bei 44 s klappt die Chicago-Tafel um, bei 0 s die New-York-Tafel. Gleiche Bewegung und gleicher Klang, neue Figur. Das sieht aus wie „nächster Flug“ und nicht wie ein Bruch. |
| Sichere Zonen YouTube | Bestanden. Die Untertitel stehen bei etwa 66–73 % der Bildhöhe (y ≈ 1270–1410 px), also über der Titel- und Kanal-Leiste (ab etwa 1480 px). Ihre rechte Kante liegt bei höchstens etwa 800 px und damit links der Button-Spalte. Im unteren Drittel ist nur Boden zu sehen, dort geht nichts verloren. Elon v2 lag mit den Untertiteln noch in der UI-Zone, das ist hier behoben. |
| Vergleich mit Elon v2 | Deutlich besser. Elon hatte leere Kulissen, steife Figuren, winzige Untertitel ganz unten und Bilder, die sich wiederholten. #09 hat echte Orte, Menschenmengen, eine animierte Fallblatt-Tafel, rollende Zähler, Stempel, Geldregen, Live-Unterschrift und alle 1–2 s ein neues Bild. „10x“ ist es noch nicht, vor allem wegen der Punkte 2 und 4 (Mimik, Nahaufnahmen). |
| Qualitätsmaßstab Teil 7 | Neben Zack D. Films oder Infographics-Shorts konkurrenzfähig, sobald Punkt 1 behoben ist. |

## Fehlerliste

### 1. PFLICHT: Untertitel ohne sichtbare Wortabstände (das ganze Video) → arc-schnitt
- **Was:** Die dicke weiße Kontur füllt den Leerraum zwischen den Wörtern. Auf dem Handy liest man so ein einziges Wort statt zweier. Sicher belegt bei 43,5 s „RIGHTNOW.“ und 41,3 s „WHICH MEANS“ (die Lücke ist zugelaufen). Im Kontaktbogen fällt dasselbe auf bei 4 s „SEE,AIRLINES“, 6 s „ONPURPOSE.“, 10 s „ANDAIRLINES“, 11 s „JUSTKICK“, 17 s „ONEMAN'S“, 28 s „INCASH.“, 32 s „HESIGNS“, 37 s „INTHELOUNGE.“, 38 s „HISSEAT?“, 42 s „ISGETTING“. Besonders stark ist es dort, wo ein farbig hervorgehobenes Wort neben einem weißen steht oder ein Wort gerade aufploppt (Skalierung). Damit fällt Kriterium „lesbar in 1 s“ durch.
- **Vorschlag:** In der Untertitel-Komponente den Wortabstand fest setzen, etwa `word-spacing: 0.35em` oder jedes Wort als eigenes Element mit `margin: 0 0.18em`. Beim Pop-in nur das Wort selbst skalieren (transform-origin center), nicht den Abstand. Die Kontur nicht über ihre Breite hinaus anwachsen lassen. Danach Kontaktbogen neu erstellen und 3 Stellen in voller Größe ansehen (z. B. 17 s, 38 s, 43,5 s).

### 2. Empfehlung: Bei „Nobody budges“ steht der Held mitten in der Reihe, als hätte er sich nie gemeldet (20–25 s) → arc-bildregie
- **Was:** Bei 17 s meldet er sich als Einziger. Bei 20–25 s sitzt er dann unauffällig in der Reihe der Kopfschüttler, zuletzt sogar mit geschlossenen Augen wie alle anderen. Das widerspricht der Geschichte „er hat sich gemeldet und wartet aufs bessere Angebot“.
- **Vorschlag:** Den Helden in der Reihe hervorheben, etwa mit Hand noch halb oben, schlauem Grinsen und Blick zur Anzeige, während die anderen wegschauen. Reine Pose-Änderung.

### 3. Empfehlung: Die gemeldete Hand ist klein und wird verdeckt (17,2–17,6 s) → arc-schnitt / arc-bildregie
- **Was:** Die Hand ist die zentrale Aktion des Satzes. Sie geht nur bis knapp über den Kopf, die drei Figuren sind eng gestaffelt, und der Untertitel „ONE MAN'S HAND“ liegt über den Oberkörpern. In 1 s auf dem Handy sieht man „drei Leute stehen“, nicht „einer meldet sich“.
- **Vorschlag:** Arm voll gestreckt mit Overshoot. Die Nachbarn sichtbar aufs Handy schauen lassen, wie im Skript vorgesehen. Den Untertitel in diesem Satz eine Zeile tiefer setzen (etwa y 1380), damit die Bewegung frei bleibt.

### 4. Empfehlung: Gate-Agentin bleibt bei Geld-Momenten ohne Mimik (27–28 s, 26 s) → arc-bildregie
- **Was:** Beim Höhepunkt $2,150 schaut sie neutral mit geradem Mund. Das nimmt dem Moment Energie, und das ist auch der Cover-Frame.
- **Vorschlag:** Kleine Reaktion: Augen weit, Mund leicht offen oder gequältes Lächeln (Augenbrauen-Wert klein lassen, etwa ±0,1). Außerdem sitzt der „B12“-Monitor so vor ihrem Oberkörper, dass er wie ein Brustschild wirkt (10–28 s). Etwas nach rechts oder tiefer setzen.

### 5. Empfehlung: Hook-Frame 0 zeigt nur Buchstabensalat (0,0–0,6 s) → arc-schnitt
- **Was:** Bei 0,0 s steht auf der Tafel „AUOGIYT592“ (Klapp-Animation), lesbar wird „OVERBOOKED“ erst bei etwa 1 s. Die Tafel nimmt nur gut die Hälfte der Breite ein, die Schrift ist auf dem Handy klein. Der Hook ist trotzdem ok, weil der Ton trägt. Für „in 1 s erfasst“ wäre er stärker, wenn das Wort sofort steht.
- **Vorschlag:** Das Umklappen auf 0,4 s verkürzen oder bei Frame 0 mit schon halb lesbarem „OVERB…“ beginnen. Tafel im Hook etwa 20 % größer. Den Loop-Bezug zu 44 s beibehalten.

### 6. Empfehlung: „just kick you off“ (11–12 s) ist bildlich unklar → arc-bildregie
- **Was:** Feder/Spirale plus Siegel auf Feder lässt sich in 1 s nicht als „rauswerfen“ lesen.
- **Vorschlag:** Ein eindeutiges Bild, etwa eine Hand der Agentin, die zum Ausgang zeigt und dann mit Stempel „U.S. LAW“ durchgestrichen wird, oder eine Bordkarte, die zerrissen werden soll und vom Siegel gestoppt wird.

### 7. Empfehlung: „Not a voucher“-Nahaufnahme ist links abgeschnitten (29–31 s) → arc-schnitt
- **Was:** Der Held ist halb aus dem Bild (linke Gesichtshälfte am Rand), und der Untertitel überdeckt seine zeigende Hand. Die einzige Nahaufnahme des Helden wirkt dadurch eher zufällig angeschnitten als gewollt.
- **Vorschlag:** Den Helden auf etwa x 300–700 setzen, Gutschein und Mülleimer rechts, Untertitel unter die Hand.

## Shorts-Cover-Frame

**Beste Sekunde: 27,5 s.** „MAX BY LAW $2,150“ groß und mittig, U.S.-Law-Siegel, Geldregen, Held mit beiden Armen oben, Gate-Kulisse. Kein Untertitel im Bild, in 1 s lesbar, deckt sich genau mit dem Titel. Mit Punkt 4 (Agentin reagiert) wird er noch stärker.
Reserve: 3,5 s („OVERBOOKED“-Tafel + Siegel + Geld, aber mit Untertitel im Bild).

## Offene Risiken
- Die „MAX BY LAW“-Nuance (Höchstgrenze nur für unfreiwillig Zurückgewiesene, siehe PRODUKTION.md) ist Sache von arc-qa und arc-faktenpruefer, nicht von mir.
- Nach dem Neu-Rendern für Punkt 1 muss ich den Kontaktbogen nochmal kurz sehen. Danach geht es an arc-qa.

Nichts geändert, nichts gerendert, keine Credits.
