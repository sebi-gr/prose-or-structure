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
- Ausführbare Schritte liegen in `src/`, bisher `01_prepare_case.py`, `02_generate_findings.py` und `03_decompose_findings.py`; Tests passend in `tests/test_NN_verb_object.py`. Die Nummerierung ist keine Verpflichtung, die verzweigten P/D-Routen in eine lineare Pipeline zu pressen.
- Prompts, Codebook, Schema und statische Hilfsdateien liegen in `resources/`; pro Zweck eine aktuelle Datei ohne Versionssuffix, Historie in Git. Ressourcen relativ zur Skriptdatei auflösen. Originale Ressourcen-Snapshots in Laufverzeichnissen erhalten. Keine leeren Stubs anlegen.
- README, AGENTS, WORKPLAN, HANDOFF und LICENSE bleiben im Repo-Wurzelverzeichnis. Zusätzliche Herkunftsdokumentation liegt in `docs/`.

## Experimentelle Regeln

- P und D erhalten identische, fixierte Code-/Konfigurationsbytes. Der P-Extraktor erhält nur den unveränderten Report als Fallmaterial sowie generische Schema-/Codebook-Anweisungen; keine zusätzliche Codeanalyse.
- Fix, PoV, Advisory, Benchmark-Labels, Referenzannotation, Manifest und Projektdokumentation aus Generierungskontexten ausschließen. Bei Agenten den tatsächlichen Toolzugriff begrenzen; getrennte Ordner allein reichen nicht.
- Ein gemeinsames Claimprofil verwenden. Aussage, Annahmen/ergänzender Kontext, abgeleitete Prüfaufgabe und bereits vorliegende Evidenz getrennt halten. Akteur/Rechte, Voraussetzungen, Negation, Modalität, Quantoren und Geltungsbereich erhalten.
- Extraktionstreue ist keine Wahrheitsprüfung. Eine falsche Reportaussage kann korrekt extrahiert sein. Modellübereinstimmung oder ein erfolgreicher PoV bestätigt nicht automatisch alle Claims.
- Reportreferenz für P und unabhängige, auf den bereitgestellten Kontext bezogene Codereferenz getrennt erstellen. Nicht entscheidbare Claims und technische Bewertungsfehler getrennt erfassen.
- JSPWiki bleibt Entwicklungsfall. Entwicklungs-/Pilotdaten von zurückgehaltener Evaluation trennen; verwundbare/gefixte Varianten eines Falls nicht über die Splits verteilen.
- Vor Vergleichsläufen Modell, Prompts, Kontext, Reasoning, Budgets, Wiederholungen und Fehler-/Reparaturregeln festhalten. Vollständige Routen vergleichen; P hat zwei Aufrufe, D zunächst einen. D mit Überarbeitung und Kontextfeld-Ablation werden vorab separat geplant.
- Revisionen, Quellen, Hashes, Originaleingaben, Requests und Rohantworten erhalten. Leere Ergebnisse, Ausfälle und Reparaturen dokumentieren; nicht bis zum gewünschten Ergebnis wiederholen. Vorhandene Ausgaben nie überschreiben.
- Keine empirischen Ergebnisse erfinden. Das aktuelle Codebook und der P-Decomposer sind übernommen; die 13 ausgefüllten Claims und historischen Laufartefakte fehlen weiter im erreichbaren Git-Stand. Angaben dazu als übernommene Dokumentationsbefunde kennzeichnen. Ersatzbeispiele ausdrücklich als neu/synthetisch kennzeichnen.
- Keine Zugangsdaten oder privaten Gesprächsinhalte einchecken. Lokale Schlüssel in `.env`, nur die leere `.env.example` versionieren. Fall-, Lauf- und Annotationsdaten unter ignoriertem `data/` halten; eine spätere Veröffentlichung benötigt eine ausdrücklich dokumentierte Auswahl samt Herkunft und Lizenzen.
- Beide Modellschritte nutzen den übernommenen direkten OpenAI-Aufruf mit `OPENAI_API_KEY` aus Umgebung/`.env`, explizitem Modell und Tokenlimit. Die frühere OpenRouter-`:free`-Beschränkung gilt seit diesem Import nicht mehr. Anbieterwechsel und Reasoning-Option sind keine festgelegte Studienkonfiguration; keine ungeplanten Live-Läufe oder automatischen Retries.

## Prüfungen

Im Repo-Wurzelverzeichnis mit Python 3.9+:

```bash
python3 -m unittest -v
git diff --check
```

Die 29 Offline-Tests prüfen Vorbereitung, Reportgenerator und Decomposer mit synthetischen Antworten, einschließlich Kontexttrennung, exakter Zitate/Unicode-Offsets und Referenzen. Die Decomposer-Testfixtures verwenden einen aufgelösten temporären Basispfad, damit der macOS-Systemlink `/var` die Tests nicht vorzeitig beendet; die produktive Symlink-Sperre bleibt bestehen. Bei Codeänderungen ausführen; weitere Tests nur für konkrete Risiken ergänzen. Windows kann den Symlink-Test bei fehlendem Privileg überspringen; ein Skip bestätigt keinen Schutz.

Optionaler echter Vorbereitungslauf bei Änderungen am Export/Download:

```bash
python3 src/01_prepare_case.py --output data/VUL4J-18-check
```

Ein neues Ziel wählen, falls dieses bereits existiert. Der Befehl führt keinen Java-PoV aus. `resources/reproduce_vul4j18.md` ist das historische Windows-Protokoll; die Originallogs sind hier nicht vorhanden und eine lokale Reproduktion ist nicht neu geprüft. Offline-Tests benötigen weder API-Key noch Inferenz oder Java.
