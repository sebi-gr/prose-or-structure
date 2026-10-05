# Handoff: Prose or Structure?

Stand: 2026-10-05, nach Übernahme des nachgelieferten Quellstands. Aktueller Plan: [WORKPLAN.md](WORKPLAN.md). Forschungsrichtung: [Projektskizze v0.1](prose_or_structure_projektskizze.pdf). Importnachweis und Artefaktinventar: [docs/PROVENANCE.md](docs/PROVENANCE.md).

## Ziel und Entscheidungen

Vergleich **P: Code → Report → Claims** mit **D: Code → Claims**, bei identischem Codekontext und gemeinsamem Claimprofil. RQ1 betrifft das Profil, RQ2 Qualität/Aufwand, RQ3 Darstellungsfehler und Kontextfeld-Ablation. KISS bleibt verbindlich; der alte breite Verifikationsplan wird nicht übernommen.

## Tatsächlicher Stand

- Zielrepo: [sebi-gr/prose-or-structure](https://github.com/sebi-gr/prose-or-structure), Branch `main`. Aktuellen Commit/Remote-Stand zu Sessionbeginn mit Git prüfen.
- Aktuelle Importquelle: `What-Can-We-Verify`, `origin/main` auf `5df7760459b741ae36bd91af4af89f6e3ecfe18d` nach Fetch. Der alte lokale Checkout des Quellrepos blieb unverändert.
- 15 Quelldateien übernommen: drei Pipeline-Skripte, vier Testdateien einschließlich `__init__.py`, sechs Ressourcen, leere `.env.example` und identische MIT-Lizenz. Herkunft und Hashes in `resources/inherited_baseline.json`.
- Neue Bestandteile: `src/03_decompose_findings.py`, `resources/claim_codebook.md`, `claim_response_schema.json`, `decomposition_prompt.txt`, `manual_annotation_template.md` sowie Decomposer-Tests. Der Review-Prompt heißt jetzt `review_prompt.txt`; sein Inhalt ist unverändert. Historische Namen bleiben in Git bzw. späteren Original-Laufkopien erhalten.
- Alle drei `src/`-Skripte sind bytegleich mit der Quelle. Lokale Anpassungen: Decomposer-Testfixture löst den temporären Basispfad auf; Linkanker der Annotationsvorlage passt zur neuen README. Beide Abweichungen sind im Importnachweis erfasst.
- Beide Modellschritte verwenden jetzt **direkte OpenAI Chat Completions**, `OPENAI_API_KEY` aus Umgebung/`.env`, explizites Modell/Tokenlimit, JSON-Modus, `store=false`, keine Tools/Fallbacks/Retry. `--no-reasoning` sendet `reasoning_effort=none`; Modellunterstützung ist Voraussetzung. Die frühere OpenRouter-`:free`-Beschränkung entfällt. Kein Live-Aufruf wurde ausgeführt.
- P-Decomposer sieht nur den ausgewählten Titel/Report plus Prompt, Codebook und Schema. Er prüft Format, exakte Zitate, Unicode-Codepoint-Offsets und Kontext-IDs. `completed` ist kein Qualitäts- oder Wahrheitsurteil.
- Das geerbte Schema ist ein **P-Extraktionsschema**, noch nicht das gemeinsame P/D-Profil. Bedingungen stehen gesammelt in `qualifiers`; explizite Kontext-, Codebezugs- und Prüfaufgabenfelder müssen für die neue Studie noch konkretisiert werden.
- `data/VUL4J-18/` ist hier lokal vorbereitet und ignoriert. Generator-Fall-ID und fünf erlaubte Dateipfade sind weiterhin fest auf VUL4J-18 begrenzt. Ein frischer Clone muss den Fall vorbereiten.

**Noch nicht implementiert:** direkte D-Erzeugung, gemeinsames P/D-Profil, D-Überarbeitung, Baselines, Ablation und Vergleichsauswertung. Modell/Budget und Evaluationsprotokoll bleiben offen.

## Historische Rohdaten weiterhin nicht im Git

Der neue Quellcommit enthält Code und Ressourcen, aber **keine `data/`-Dateien**. Das Quellrepo ignoriert weiterhin `/data/`. Codebook und Annotationsvorlage sind jetzt vorhanden; folgende Originale fehlen weiterhin:

- Review `0721c0a0-bba7-48c1-a63c-da196a69d97c`, einschließlich Request, Rohantwort, Findings und Manifest.
- Ausgefüllte Annotation `data/annotations/VUL4J-18-review-001/manual_annotation_001.md` mit 13 Claims. Laut Quellhandoff assistierte Entwicklung mit Vorwissen über Code/Fix/PoV, keine unabhängige Wahrheitsreferenz.
- Historische Decomposition-Läufe 001–003. Laut Quelle: 001 ungültig; 002/003 je vier zu grobe, wortgleiche Satz-Propositionen; in 003 keine Kontext-IDs. Letzte dokumentierte Run-ID: `c939bbd8-090a-4c51-b14d-998d1fc8653c`. Hier nicht anhand der Rohdaten nachgeprüft.
- PoV-Logs und Metadaten zu `data/pov/VUL4J-18-001/`; das historische Windows-Protokoll ist vorhanden.

Die betroffenen Dateien müssen vom anderen Rechner separat bereitgestellt oder gezielt versioniert werden; ein weiterer normaler Commit ignorierter Daten genügt nicht. Keine pauschale Aufnahme von `.env`, Toolchains oder Caches. Fehlende Originale nicht erfinden oder durch neue Modellantworten ersetzen.

## Prüfstand

- macOS / Python **3.13.2**: **29/29 Offline-Tests bestanden, kein Skip**. Alle drei CLI-Hilfen funktionieren. Tests verwenden synthetische Antworten, keine Inferenz.
- Der erste Testlauf scheiterte beim Decomposer am macOS-Systemlink `/var` im temporären Verzeichnis. Nur die Testfixture verwendet jetzt den tatsächlichen Basispfad; die produktive Symlink-Sperre wurde nicht gelockert.
- Die ursprüngliche Fallvorbereitung mit neun Download-Dateien und fünf Modelldateien (71.907 Bytes) bleibt unverändert; die entsprechende Implementierung ist identisch. Historischer Prüfstand und Manifest-Hash stehen in PROVENANCE.
- Alle 15 Importnachweise einschließlich lokaler Anpassungen geprüft; 28 lokale Dokumentationslinks samt Ankern aufgelöst, JSON-Dateien lesbar und `git diff --cached --check` ohne Befund. 24 versionierte Dateien geprüft; keine generierten Daten, Schlüsseldateien oder Caches aufgenommen. GitHub-CI führt dieselben Offline-Tests aus; jeweils aktuelles Ergebnis unter Actions.

**Nicht ausgeführt:** Live-Inferenz, neue Annotation, neuer Java-Build/PoV oder P/D-Experiment. Historische Laufbefunde sind übernommene Angaben; API-Verfügbarkeit und Extraktionsqualität wurden hier nicht live verifiziert.

## Nächster Schritt

Mit **Schritt 2 in WORKPLAN** das vorhandene Codebook/P-Schema zum gemeinsamen Claimprofil weiterentwickeln und die getrennten Annotationsreferenzen festlegen. Parallel fehlen die Original-Laufdaten aus Schritt 1. Danach den bestehenden P-Extraktor anpassen und D ergänzen. Kein neuer Report nötig, sobald der historische Run verfügbar ist.
