# Pilotprotokoll 0.1

Stand: 2026-10-05, vor dem ersten neuen Modellaufruf. Operative Festlegungen für
Schritt 4 im Rahmen des beauftragten autonomen PoC. Keine Hauptstudien-Präregistrierung
und keine Qualitätsresultate. Änderungen nach Einsicht in Ergebnisse als neue
Protokollversion begründen; nicht rückwirkend in diesen Versuchsplan einarbeiten.

## Fälle und Kontext

Fünf gezielt ausgewählte Machbarkeitsfälle, zwei Familien: VUL4J-15/64 (XXE),
VUL4J-41/43/76 (Pfadverarbeitung). Je eine vulnerable und fixed Variante, also
zehn Kontexte. [Auswahl und Grenzen](PILOT_CASES.md),
[unveränderliche Downloadquellen](../resources/pilot_cases.json).
Vollständige Dateien, identische Pfadauswahl innerhalb eines Variantenpaars;
P und D bekommen pro Kontext exakt dieselben Bytes und dieselbe nummerierte
Ansicht. Auswahl erfolgte anhand von Patch und Benchmark, damit ist dies eine
gezielte, lokalisierte Reviewaufgabe, kein unverzerrter Repository-Scan.

Varianten separat beurteilen, dann innerhalb des Falls aggregieren. „Fixed“
bezeichnet den ausgewählten Patch, keine allgemeine Sicherheitsgarantie.
Originalkommentare und Pfade bleiben erhalten und können Projekt oder Schutzlogik
verraten. CVEs, Labels, Commitmetadaten, Tests, PoVs, Patches, Referenzurteile und
Projektunterlagen werden nicht zusätzlich an Modelle gesendet. Fehlende
Abhängigkeiten und Laufzeitkontexte bleiben offen; kein Java-/PoV-Test nötig,
um diese begrenzte Reviewaufgabe vorzubereiten. Neue Reproduktionen wären eigene
Evidenz, kein Ersatz für Claimannotation.

Alle Entwicklungs- und Pilotprojekte einschließlich Aliase bleiben außerhalb
späterer Holdout-Daten. Noch keine Hauptstichprobe ausgewählt oder annotiert.

## Modell, Budget und Reihenfolge

[Ausführbare Konfiguration](../resources/pilot_config.json):
`gpt-5.4-mini-2026-03-17`, direkt OpenAI Chat Completions, `reasoning_effort=none`,
`service_tier=default`, `store=false`, keine Tools, kein Temperature-Override.
Datierten Snapshot für reproduzierbare Modellidentität gewählt; keine Behauptung,
dass dies das optimale oder billigste Modell sei. JSON-Modus für P/D;
VeriScore-basierte Extraktion behält Textausgabe. Lokale Validatoren bleiben nötig.
Accountzugriff und Live-Kompatibilität sind noch ungeprüft.
[Modell](https://developers.openai.com/api/docs/models/gpt-5.4-mini),
[JSON-Modus](https://developers.openai.com/api/docs/guides/structured-outputs#json-mode).

Ausgabelimits einschließlich Reasoning: Report 3.072, Claims/Revision 6.144,
VeriScore pro Satz 1.024 Tokens. Standardpreise geprüft am 05.10.2026, USD je
1 Mio. Tokens: Input 0,75, Cached Input 0,075, Output 4,50.
[Preisquelle](https://developers.openai.com/api/docs/pricing).
Preise vor einem späteren Live-Start erneut prüfen; Änderungen brauchen eine
angepasste Konfiguration und Kostensperre. Abrechnung ist nicht modellseitig exakt
einstellbar. Der Runner reserviert vor jedem Request konservativ einen Inputtoken
pro UTF-8-Byte plus 1.024 Overheadtokens und das komplette Outputlimit zum
ungecacheten Preis. Reservierungen werden nicht zurückgebucht. Das kann früh
stoppen, hält aber unter diesen dokumentierten Tarif-/Tokenizerannahmen die
gewählte Obergrenze ein. Gemeldete Usage und daraus geschätzte Kosten separat
speichern; sie sind keine Rechnung. API-Key und menschlich gewählte USD-Grenze
fehlen derzeit. Kein stiller Modellwechsel oder Nachkauf.

Zwei Wiederholungen pro Kontext. Seed 20261005 mischt die zehn Kontexte; die
P/D-Reihenfolge wird nach Kontextindex und Wiederholung abwechselnd umgekehrt,
sodass jeder Kontext einmal P zuerst und einmal D zuerst erhält. Innerhalb von P
folgt die Extraktion dem Report. Frische zustandslose Requests, keine gemeinsamen
Chats. Zusatzbedingungen folgen erst nach allen Kernpaaren, stets Wiederholung 1.
Dadurch sind Wiederholungen technische Replikate, keine unabhängigen Fälle.
Der gespeicherte Plan nennt jede Aufgabe, Abhängigkeit, Quellhashes und
Implementierungs-/Ressourcenhashes vor Beginn.

## Bedingungen und vollständige Reporteinheit

| Bedingung | Umfang | Zusätzliche Aufrufe |
|---|---|---|
| P | Alle zehn Kontexte × 2 | Ein Report + eine vollständige Extraktion, höchstens 40 |
| D | Alle zehn Kontexte × 2 | Direktes Schema-Prompting, 20 |
| D mit Revision | Alle zehn Kontexte, Wiederholung 1 | Ein zusätzlicher Code + D-Claims Review, 10 |
| Ohne explizite Kontextfelder | VUL4J-15/41, beide Varianten, Wiederholung 1, P und D | Vier P-Extraktionen und vier D-Aufrufe |
| Satzbaseline + VeriScore-basierte Extraktion | Dieselben vier P-Reporte | Satzbaseline lokal; VeriScore ein Aufruf je Satz |

P bündelt **alle** Findings in Reihenfolge in eine deterministische Reportansicht:
Titel `Complete security review`; je Finding `[Finding N]\nTitle: ...\nReport:\n...`,
getrennt durch zwei Zeilenumbrüche. Originaltitel/-berichte bleiben unveränderte
Substrings; hinzu kommen ausschließlich Strukturmarker. `finding.json` speichert
die genaue Ansicht. P-Zitate und Offsets beziehen sich auf diese Ansicht;
`findings_input.jsonl` und der Originalrequest erlauben die Rückzuordnung. Kein
Finding wird nach Inhalt ausgewählt. Der generische Titel und die Trennmarker
sind keine zu extrahierenden Sicherheitsbehauptungen. Leerer Report: keine
Extraktionsanfrage, null P-Claims; dies ist weder Formatfehler noch Beweis für
sicheren Code. D bleibt unabhängig ausführbar, auch vor P oder nach dessen Fehler.

D-Revision erhält dieselben Quellbytes plus ausschließlich die validierten
vorherigen D-Claims; keine P-Reporte oder menschlichen Urteile. Auch eine gültige
leere D-Ausgabe erhält die geplante Revision. P/D-Revision sind Kontrollen mit
zwei Aufrufen, keine Garantie identischen Tokenaufwands: P hat maximal 9.216,
D samt Revision maximal 12.288 Outputtokens. Damit ist dies keine Kontrolle mit
identischem Tokenlimit. Tatsächlichen Aufwand
inklusive ursprünglichem D beziehungsweise P-Report je vollständiger Route zählen.

Die Ablation entfernt `context` samt sechs Feldern aus Schema, Prompt und
Codebook-Feldanweisungen; Bedingungen müssen weiterhin in Propositionen stehen.
`context_claim_ids`, Zitate, Typisierung und Prüfaufgaben bleiben bestehen.
Das gespeicherte Ergebnis enthält keine nachträglich erfundenen Null-Kontextfelder.
P verwendet denselben ursprünglichen Report; D wird erneut direkt generiert.
Bewertungsziel unverändert, je vier Paare zu den entsprechenden Vollprofilen.

Die Satzbaseline verwendet exakte Titel-/Reportsubstrings mit einem einfachen,
dokumentierten Regex-Splitter. Die VeriScore-basierte Baseline verwendet den
lizenzierten Non-QA-Prompt und lokale Satzfenster, ohne Suchmaschine oder
Wahrheitsprüfung. Sie ist eine offengelegte Anpassung, keine exakte Reproduktion
mit ursprünglichem Modell und Satzsegmentierer. Keine zusätzlichen Profilfelder
per LLM nachrüsten; nur Propositionen/Coverage/Fidelity vergleichen. Für fehlende
Profilfelder und Prüfaufgaben „nicht anwendbar“ statt Nullqualität vergeben.
Siehe [Baseline-Herkunft](../resources/baselines/README.md).

## Ausfälle und Verbrauch

Keine automatischen Retries, Reparaturen oder Auswahl des besten Versuchs.
Alle Outputs in neue Verzeichnisse. Leere, abgeschnittene, ungültige und
fehlgeschlagene Antworten getrennt erhalten. P-Formatfehler sperrt seine
abhängigen Extraktionen, nicht den unabhängigen D-Versuch. Fehlgeschlagener D-Lauf
sperrt nur seine Revision. Bei Budgetgrenze, HTTP-Fehler, unklarer Usage oder
Transportabbruch stoppt der gesamte Rest; ungewisse Kosten bleiben reserviert.
Kein automatisches Resume. Ein neuer Versuch benötigt dokumentierte Begründung
und neue Pfade; den unvollständigen ursprünglichen Plan mitberichten.

`budget_ledger.json` enthält jeden tatsächlich gestarteten Transport,
Requesthash, Reservierung, Usage und Dauer. Stage-Manifeste enthalten Request,
Rohantwort und Status. Vollständige Routenkosten: P = Report + Extraktion,
D = Direktlauf, D-Revision = Direktlauf + Revision; Ablations-/Baselinebedingungen
tragen denselben wiederverwendeten Reportaufwand rechnerisch mit. Geteilte Aufrufe
bei der Gesamtrechnung nur einmal zählen. Claimanzahl ist kein Qualitätsmaß.

## Menschliche Referenzen und Pilotentscheidung

Vor Einsicht in Modellausgaben erstellen Annotatoren pro bereitgestelltem Kontext
eine begrenzte Codereferenz: relevante, prüfbare Propositionen, Bedingungen,
Quellpositionen und offen bleibende Fragen. Kein pauschales CVE-Ground-Truth-Label.
Die neutral nummerierten Pakete aus `07_prepare_annotations.py` zeigen nur den
Modellcode; Zuordnung/Variantenwissen liegt getrennt. Bestehendes Vorwissen offen
angeben. Kein vollständiges Projekt-Blinding versprechen.

Danach P-Reportreferenz aus dem **wirklich erzeugten vollständigen Report** erstellen,
unabhängig von Extraktionen, getrennt von der Codereferenz. Menschliche
Claimbewertung nach [Annotationsprotokoll](../resources/annotation_protocol.md).
Soweit möglich Route/Modell/Wiederholung aus Bewertungsansichten ausblenden;
Zitate und Struktur können die Route trotzdem verraten. Annotator 1 bewertet alle
Kontexte; ein zweiter menschlicher Annotator unabhängig dieselben vier vorab
festgelegten Kontexte von VUL4J-15/41, anschließend Adjudikation. Rollen/Namen
und echte aktive Minuten erfassen, keine KI-Zeiten oder erfundenen Übereinstimmungen.
Ein KI-Entwurf wäre ausdrücklich assistiert und ersetzt diese Referenz nicht.

Pilotbericht pro Fall: Fundierung (belegt/widerlegt/nicht entscheidbar), relevante
Coverage, P-Fidelity/Erhalt von Bedingungen, Prüfbarkeit, technische Ausfälle,
Tokens/Kosten und Annotationzeit. Wiederholungen und Varianten zuerst innerhalb
desselben Falls zusammenfassen; gepaarte Differenzen zwischen den fünf Fällen.
Leere Claims: Coverage 0 nur bei nichtleerer Referenz, Präzision/Fidelity nicht
berechenbar; leere Referenz separat. Technische Ausfälle weder als null Claims
noch als inhaltlich falsche Aussagen umdeuten; Erfolgsquote und Nenner berichten.
Die öffentlichen Benchmarkfälle können dem Modell aus Trainingsdaten bekannt sein;
fehlende Neuheit und gezielte Kontextauswahl als Limitation berichten.
Keine Signifikanz- oder Gleichwertigkeitsbehauptung aus fünf Fällen. Empirische
Intervalle und Hauptstudien-Fallzahl erst nach Pilotannotation begründet festlegen.

Gate zu Schritt 5: tatsächliche Lauf-/Annotationsdaten vorhanden, Fehler und
Kontextgrenzen überprüft, Zeitbedarf und Doppelannotation ausgewertet. Dann mit
Betreuung Hauptstichprobe, Umfang und Auswertung einfrieren. Literaturarbeit kann
parallel vorankommen; Ergebnisse oder Betreuungsentscheidungen nicht vorwegnehmen.
