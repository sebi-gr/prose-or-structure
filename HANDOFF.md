# Handoff: Prose or Structure?

Stand: 2026-10-05, nach Einordnung des kleinen Übergabepakets. Plan: [WORKPLAN.md](WORKPLAN.md). Forschungsrichtung: [Projektskizze v0.1](prose_or_structure_projektskizze.pdf). Herkunft und Prüfgrenzen: [docs/PROVENANCE.md](docs/PROVENANCE.md).

## Ziel und nächste Arbeit

Vergleich **P: Code → Report → Claims** mit **D: Code → Claims**, bei identischem Codekontext und gemeinsamem Claimprofil. RQ1: Profil; RQ2: Qualität/Aufwand; RQ3: Darstellungsfehler und Kontextfeld-Ablation. KISS bleibt verbindlich.

**Schritt 1 ist für den vereinbarten Minimalumfang abgeschlossen.** Originalreport und angenommene manuelle Revision mit 13 Claims sind verfügbar. Als Nächstes das bestehende Codebook/P-Schema anhand dieser Beispiele zum gemeinsamen P/D-Profil weiterentwickeln und getrennte Referenzregeln festlegen. P-Decomposer und Validierung weiterverwenden; D anschließend ergänzen. Kein neuer Report nötig.

## Verfügbares Entwicklungsarchiv

Die sechs vom Nutzer im Repo-Wurzelverzeichnis gepushten Dateien sind jetzt passend eingeordnet:

- `data/runs/VUL4J-18-review-001/`: `findings.jsonl`, `request.json`, `generation_raw.json`, `review_prompt_v1.txt`, `run_manifest.json`.
- `data/annotations/VUL4J-18-review-001/manual_annotation_001.md`: angenommene Entwicklungsrevision mit 13 Claims.
- Importweg, Eingangs-/Archivhashes und einzige Wiederherstellung: `resources/inherited_artifacts.json`. Gesamtumfang 108.158 Bytes.
- `.gitignore` lässt genau diese sechs Dateien zu; alle anderen Fall-/Laufdaten, Toolchains und Caches bleiben ignoriert. `.gitattributes` schützt archivierte Bytes vor Zeilenumbruch-Konvertierung. Originale nicht überschreiben oder auf neue Ressourcenbezeichnungen umschreiben.

Der Prompt wurde bei der Nachlieferung mit LF statt historischen CRLF-Zeilenumbrüchen versioniert. Die ursprünglichen Bytes wurden exakt aus der gespeicherten Request-Systemnachricht wiederhergestellt und passen zum Manifest-Hash. Alle anderen gelieferten Dateien blieben bytegleich. Das historische Manifest wurde nicht geändert.

## Geprüfte Zuordnung

- Request-, Antwort- und Prompt-Hashes passen zum Manifest; Parameter, Provider-/Modell-/Response-ID und Usage sind konsistent.
- Das Finding ist exakt aus der Rohantwort ableitbar und wird vom aktuellen P-Eingabelader gelesen. Run-ID: `0721c0a0-bba7-48c1-a63c-da196a69d97c`, ein Finding, damaliger OpenRouter/Nemotron-Lauf ohne Reasoning.
- Die Annotation referenziert exakt diese Finding-Datei per Hash/ID; eingebetteter Titel und Report sind identisch. 13 eindeutige Claim-IDs, alle 15 Originalzitate und auflösbare Kontextreferenzen geprüft.
- Die fünf lokal aus fixierten Quellen vorbereiteten Modelldateien passen zu den historischen Quellhashes; die daraus rekonstruierte gesamte User-Nachricht entspricht dem gespeicherten Request. Eine weitere versionierte Quellkopie ist nicht nötig.
- Diese Prüfungen belegen Konsistenz und Herkunft, keine neue Bewertung der Claim-Wahrheit oder Extraktionsqualität. Die Annotation nennt SG, Codex-Unterstützung und Vorwissen über Code/Fix/PoV; keine unabhängige Wahrheitsreferenz.

## Implementierungsstand

- Zielrepo: [sebi-gr/prose-or-structure](https://github.com/sebi-gr/prose-or-structure), Branch `main`; aktuellen Commit/Remote-Stand mit Git prüfen.
- Codebasis aus What-Can-We-Verify `5df7760459b741ae36bd91af4af89f6e3ecfe18d`; alle drei Pipeline-Skripte bytegleich. 15 Importdateien und zwei lokale Anpassungen (macOS-Testfixture, README-Linkanker) sind in `resources/inherited_baseline.json` festgehalten.
- `01_prepare_case.py`: fixierter VUL4J-18-Export. Lokale Daten vorhanden, für neue Clones erneut erzeugbar. Fall-ID und fünf erlaubte Pfade sind weiterhin fest auf VUL4J-18 begrenzt. Kein Java-Test durch die Vorbereitung.
- `02_generate_findings.py` und `03_decompose_findings.py`: heute direkte OpenAI Chat Completions, `OPENAI_API_KEY`, explizites Modell/Tokenlimit, JSON-Modus, `store=false`, keine Tools/Fallbacks/Retry. `--no-reasoning` setzt `reasoning_effort=none`, sofern vom Modell unterstützt. Diese Einstellungen gelten nicht rückwirkend für den archivierten OpenRouter-Lauf.
- P-Extraktion erhält nur ausgewählten Titel/Report plus Prompt/Codebook/Schema; lokale Validierung prüft Format, exakte Zitate/Offsets und Kontext-IDs. Das P-Schema mit `qualifiers` ist noch nicht das gemeinsame P/D-Profil.
- **Offen:** gemeinsames Profil, D-Erzeugung/Überarbeitung, Baselines, Ablation, Vergleichsauswertung sowie Modell/Budget und Evaluationsprotokoll.

## Optionale historische Ergänzungen

Die alten Decomposition-Rohdaten 001–003, PoV-Logs sowie die in der Annotation genannten Originalabgabe, das separate Review und das damalige Codebook v0.2 wurden nicht geliefert. Sie sind für den nächsten Entwicklungsschritt nicht erforderlich. Heutiges Codebook nicht als alten Snapshot ausgeben; deren vollständige Revisionsgeschichte bleibt ungeprüft.

Das PoV-Protokoll beschreibt den damaligen Windows-Lauf; die Original-Logs fehlen. Frühere Decomposition-Befunde sind nur als Quellnotizen übernommen. Neue Läufe können wir separat durchführen, erzeugen aber neue Evidenz und ersetzen keine historischen Rohdaten.

## Prüfstand und Grenzen

- Letzter Code-Prüfstand unverändert: macOS/Python 3.13.2, 29/29 Offline-Tests bestanden; drei CLI-Hilfen funktionieren. Pipeline-Code und Tests bei dieser Einordnung nicht verändert.
- Aktuell: sechs Artefakte samt Importnachweis und Bezügen geprüft, ohne Modellrequest. Staged Git-Blobs und Probe-Checkout mit `core.autocrlf=true` behalten die archivierten Hashes. Genau sechs Daten-Dateien versioniert, andere Ausgaben ignoriert; 38 lokale Links/Anker aufgelöst und `git diff --cached --check` ohne Befund. GitHub-CI führt die Offline-Tests aus.
- Kein Live-Modellaufruf, keine neue Annotation oder Java-Reproduktion. Archivierte historische Texte bleiben unverändert, auch wenn sie frühere Dateinamen oder damals offene Implementierungsschritte nennen.
