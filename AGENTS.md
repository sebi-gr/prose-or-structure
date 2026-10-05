# Entwicklungsregeln

## Einstieg und Dokumentation

- Zu Beginn jeder Session `HANDOFF.md`, `WORKPLAN.md`, danach `README.md` lesen und den tatsächlichen Git-Stand prüfen. Veraltete Angaben korrigieren.
- `WORKPLAN.md` ist die maßgebliche Quelle für Reihenfolge, Status, Abschlusskriterien und offene Entscheidungen. Nach relevantem Fortschritt laufend aktualisieren.
- `HANDOFF.md` hält den überprüften aktuellen Stand, Grenzen und nächsten Schritt fest. Keine anwachsende Sammlung widersprüchlicher Sessionnotizen; historische Details über Git und Provenienz verlinken.
- `README.md` mit Bedienung, Voraussetzungen und tatsächlichem Implementierungsstand synchron halten. Geplantes ausdrücklich markieren.
- Forschungsrichtung: `prose_or_structure_projektskizze.pdf` vom 03.10.2026. Fokus sind RQ1–RQ3 und der Vergleich P (Code → Report → Claims) mit D (Code → Claims), keine allgemeine Claim-Verifikationsplattform. Änderungen an der Studienplanung begründen; Vorschläge von Beschlüssen trennen.

## Kleine, nachvollziehbare Implementierung

- **KISS:** Kleiner Forschungsprototyp. Lesbare Skripte, explizite Ein-/Ausgaben und die Standardbibliothek bevorzugen.
- Komponenten, Abhängigkeiten und Abstraktionen erst ergänzen, wenn der nächste konkrete Versuch sie braucht. Keine allgemeine Pipeline-Engine, Datenbank, Plugin-Plattform oder vorsorgliche Provider-Abstraktion.
- Nur den beauftragten Schritt umsetzen; bestehende Änderungen erhalten und beiläufige Refactorings vermeiden.
- Jede Funktion in `src/` erhält direkt oberhalb der Definition einen kurzen verständlichen `#`-Kommentarblock zu Zweck, Ein-/Ausgaben und relevanten Nebenwirkungen oder Grenzen. Bei Änderungen mitpflegen.
- Ausführbare Schritte liegen in `src/`, nummeriert 01–07; kleine Helfer nur für tatsächlich geteilte Profil-, Quellen-, Paarungs- und Baseline-Regeln. Skripttests passend in `tests/test_NN_verb_object.py`, Helfertests unter `tests/test_<modul>.py`. Die Nummerierung macht die verzweigten P/D-Routen nicht zu einer linearen Pipeline.
- Prompts, Codebook, Schema und statische Hilfsdateien liegen in `resources/`; pro Zweck eine aktuelle Datei ohne Versionssuffix, Historie in Git. Ressourcen relativ zur Skriptdatei auflösen. Originale Ressourcen-Snapshots in Laufverzeichnissen erhalten. Keine leeren Stubs anlegen.
- README, AGENTS, WORKPLAN, HANDOFF und LICENSE bleiben im Repo-Wurzelverzeichnis. Zusätzliche Herkunftsdokumentation liegt in `docs/`.

## Experimentelle Regeln

- P und D erhalten identische, fixierte Code-/Konfigurationsbytes. Der P-Extraktor erhält nur den unveränderten Report als Fallmaterial sowie generische Schema-/Codebook-Anweisungen; keine zusätzliche Codeanalyse.
- Fix, PoV, Advisory, Benchmark-Labels, Referenzannotation, Manifest und Projektdokumentation aus Generierungskontexten ausschließen. Bei Agenten den tatsächlichen Toolzugriff begrenzen; getrennte Ordner allein reichen nicht.
- Schritt-2-Vertrag: `resources/claim_profile.md` und `claim_profile.schema.json`, Version 0.1, aktiv in P/D mit gemeinsamem Validator. Der alte P-Antwortvertrag liegt nur noch in Git/Historie. Reale Beispiele und Referenzen unter `resources/profile_development/` sowie das Annotationsprotokoll niemals als Modellkontext verwenden. Das Codebook bleibt generisch.
- Ein gemeinsames Claimprofil verwenden. Aussage, Annahmen/ergänzender Kontext, abgeleitete Prüfaufgabe und bereits vorliegende Evidenz getrennt halten. Akteur/Rechte, Voraussetzungen, Negation, Modalität, Quantoren und Geltungsbereich erhalten.
- Extraktionstreue ist keine Wahrheitsprüfung. Eine falsche Reportaussage kann korrekt extrahiert sein. Modellübereinstimmung oder ein erfolgreicher PoV bestätigt nicht automatisch alle Claims.
- Reportreferenz für P und unabhängige, auf den bereitgestellten Kontext bezogene Codereferenz getrennt erstellen. Nicht entscheidbare Claims und technische Bewertungsfehler getrennt erfassen.
- JSPWiki bleibt Entwicklungsfall. Entwicklungs-/Pilotdaten von zurückgehaltener Evaluation trennen; verwundbare/gefixte Varianten eines Falls nicht über die Splits verteilen.
- Pilot gemäß `docs/PILOT_PROTOCOL.md` und `resources/pilot_config.json` ausführen: alle Findings mit `--finding-id all` in einer Extraktion, P höchstens zwei Aufrufe, D einer; D-Revision und Kontextfeld-Ablation separat vorgesehen. D hängt im Pilot nicht vom Erfolg des P-Reports ab. Änderungen nach Ergebniseinsicht mit neuer Protokollversion begründen. Vollständige Routenkosten zählen; gemeinsame Reports nicht doppelt in die Gesamtrechnung aufnehmen.
- Revisionen, Quellen, Hashes, Originaleingaben, Requests und Rohantworten erhalten. Leere Ergebnisse, Ausfälle und Reparaturen dokumentieren; nicht bis zum gewünschten Ergebnis wiederholen. Vorhandene Ausgaben nie überschreiben.
- Keine empirischen Ergebnisse erfinden. Der historische Report und die angenommene manuelle Revision mit 13 Claims sind als Entwicklungsbeispiel archiviert; keine unabhängige Wahrheitsreferenz. Die unveränderte Annotation dokumentiert ihren damaligen Stand, nicht den aktuellen Implementierungsplan. Fehlende historische Decomposition-/PoV-Rohdaten nicht als geprüft darstellen.
- Keine Zugangsdaten oder privaten Gesprächsinhalte einchecken. Lokale Schlüssel in `.env`, nur die leere `.env.example` versionieren. Unter `data/` sind ausschließlich die sechs ausdrücklich übernommenen Dateien des Reviews `VUL4J-18-review-001` und seiner Annotation versioniert; `.gitignore` enthält die genaue Auswahl. Alle übrigen generierten Daten bleiben ignoriert. Neue Archiv-Ausnahmen gezielt begründen und Herkunft/Lizenzen erhalten.
- Archivierte Originale nicht redigieren oder auf aktuelle Ressourcen-/Anbieternamen umschreiben. `.gitattributes` erhält ihre Bytes auch auf Windows; `resources/inherited_artifacts.json` dokumentiert Hashes und die Wiederherstellung der ursprünglichen Prompt-Zeilenumbrüche aus dem Request. Neue Annotationen und Modellläufe benötigen neue Pfade.
- Alle Modellschritte nutzen direkten OpenAI-Aufruf mit `OPENAI_API_KEY` aus Umgebung/`.env`, explizitem Modell und Tokenlimit. Pilotmodell, Reasoning und Tier sind jetzt festgelegt; Live-Pilot nur mit `06_run_pilot.py --execute --budget-usd ...`, bereitgestelltem Key und menschlich gewählter Kostengrenze. Preise vor späterem Start prüfen. Keine ungeplanten Live-Läufe, Retries oder Modellwechsel; Standalone-Skripte haben keinen monetären Schutz.

## Prüfungen

Im Repo-Wurzelverzeichnis mit Python 3.9+:

```bash
python3 -m unittest -v
git diff --check
```

Die Offline-Tests prüfen Vorbereitung, P/D, gemeinsames Profil, Paarung und
Pilotergänzungen mit synthetischen Antworten und archivierten Fixtures. Dazu
gehören Kontexttrennung, gleiche Codebytes, Herkunft, Zitate/Unicode-Offsets,
Katalogvarianten, vollständige Reports, Revision, Ablation, Extraktionsbaselines,
Budget-/Ausfallverhalten und neutrale Annotationsexporte. Temporäre Testpfade unter
macOS auflösen, ohne die produktive Symlink-Sperre abzuschwächen. Bei Codeänderungen
ausführen; weitere Tests nur für konkrete Risiken ergänzen. Windows kann einen
Symlink-Test bei fehlendem Privileg überspringen; ein Skip bestätigt keinen Schutz.
Offline-Tests sind keine Modell- oder Qualitätsresultate.

Optionaler echter Vorbereitungslauf bei Änderungen am Export/Download:

```bash
python3 src/01_prepare_case.py --output data/VUL4J-18-check
```

Ein neues Ziel wählen, falls dieses bereits existiert. Der Befehl führt keinen Java-PoV aus. `resources/reproduce_vul4j18.md` ist das historische Windows-Protokoll; die Originallogs sind hier nicht vorhanden und eine lokale Reproduktion ist nicht neu geprüft. Offline-Tests benötigen weder API-Key noch Inferenz oder Java.
