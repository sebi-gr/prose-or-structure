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
- Ausführbare Schritte liegen in `src/`, `01_prepare_case.py`, `02_generate_findings.py`, `03_decompose_findings.py` und `04_generate_claims.py`; gemeinsam genutzte kleine Helfer sind `claim_profile.py` und `review_pair.py`; Skripttests passend in `tests/test_NN_verb_object.py`, Helfertests unter `tests/test_<modul>.py`. Die Nummerierung ist keine Verpflichtung, die verzweigten P/D-Routen in eine lineare Pipeline zu pressen.
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
- Vor Vergleichsläufen Modell, Prompts, Kontext, Reasoning, Budgets, Wiederholungen und Fehler-/Reparaturregeln festhalten. Vollständige Routen vergleichen; Im Ein-Finding-PoC hat P zwei Aufrufe, D einen; derzeit benötigt P bei N Findings 1 + N Aufrufe. Vor Pilot die Reporteinheit festlegen und alle Findings berücksichtigen. D mit Überarbeitung und Kontextfeld-Ablation werden vorab separat geplant.
- Revisionen, Quellen, Hashes, Originaleingaben, Requests und Rohantworten erhalten. Leere Ergebnisse, Ausfälle und Reparaturen dokumentieren; nicht bis zum gewünschten Ergebnis wiederholen. Vorhandene Ausgaben nie überschreiben.
- Keine empirischen Ergebnisse erfinden. Der historische Report und die angenommene manuelle Revision mit 13 Claims sind als Entwicklungsbeispiel archiviert; keine unabhängige Wahrheitsreferenz. Die unveränderte Annotation dokumentiert ihren damaligen Stand, nicht den aktuellen Implementierungsplan. Fehlende historische Decomposition-/PoV-Rohdaten nicht als geprüft darstellen.
- Keine Zugangsdaten oder privaten Gesprächsinhalte einchecken. Lokale Schlüssel in `.env`, nur die leere `.env.example` versionieren. Unter `data/` sind ausschließlich die sechs ausdrücklich übernommenen Dateien des Reviews `VUL4J-18-review-001` und seiner Annotation versioniert; `.gitignore` enthält die genaue Auswahl. Alle übrigen generierten Daten bleiben ignoriert. Neue Archiv-Ausnahmen gezielt begründen und Herkunft/Lizenzen erhalten.
- Archivierte Originale nicht redigieren oder auf aktuelle Ressourcen-/Anbieternamen umschreiben. `.gitattributes` erhält ihre Bytes auch auf Windows; `resources/inherited_artifacts.json` dokumentiert Hashes und die Wiederherstellung der ursprünglichen Prompt-Zeilenumbrüche aus dem Request. Neue Annotationen und Modellläufe benötigen neue Pfade.
- Alle Modellschritte nutzen den übernommenen direkten OpenAI-Aufruf mit `OPENAI_API_KEY` aus Umgebung/`.env`, explizitem Modell und Tokenlimit. Die frühere OpenRouter-`:free`-Beschränkung gilt seit diesem Import nicht mehr. Anbieterwechsel und Reasoning-Option sind keine festgelegte Studienkonfiguration; keine ungeplanten Live-Läufe oder automatischen Retries.

## Prüfungen

Im Repo-Wurzelverzeichnis mit Python 3.9+:

```bash
python3 -m unittest -v
git diff --check
```

Die 60 Offline-Tests prüfen Vorbereitung, Reportgenerator, P/D, gemeinsames Profil und Paarung mit synthetischen Antworten sowie archivierten Fixtures. Dazu gehören Kontexttrennung, identische Quellbytes/gesendeter Codekontext, Herkunft, exakte Zitate/Unicode-Offsets und Referenzen. Die Decomposer-Testfixtures verwenden einen aufgelösten temporären Basispfad, damit der macOS-Systemlink `/var` die Tests nicht vorzeitig beendet; die produktive Symlink-Sperre bleibt bestehen. Bei Codeänderungen ausführen; weitere Tests nur für konkrete Risiken ergänzen. Windows kann den Symlink-Test bei fehlendem Privileg überspringen; ein Skip bestätigt keinen Schutz.

Optionaler echter Vorbereitungslauf bei Änderungen am Export/Download:

```bash
python3 src/01_prepare_case.py --output data/VUL4J-18-check
```

Ein neues Ziel wählen, falls dieses bereits existiert. Der Befehl führt keinen Java-PoV aus. `resources/reproduce_vul4j18.md` ist das historische Windows-Protokoll; die Originallogs sind hier nicht vorhanden und eine lokale Reproduktion ist nicht neu geprüft. Offline-Tests benötigen weder API-Key noch Inferenz oder Java.
