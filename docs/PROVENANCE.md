# Herkunft und Bestandsprüfung

Stand: 2026-10-05, nach dem zweiten Import. Laufender Plan: [WORKPLAN.md](../WORKPLAN.md); aktueller Stand: [HANDOFF.md](../HANDOFF.md). Code/Ressourcen, historische Dokumentationsbefunde und tatsächlich vorhandene Rohdaten bleiben getrennt.

## Aktuelle Importquelle

- Repository: [sebi-gr/What-Can-We-Verify](https://github.com/sebi-gr/What-Can-We-Verify).
- Nach Fetch verwendeter Stand: `origin/main`, Commit [`5df7760459b741ae36bd91af4af89f6e3ecfe18d`](https://github.com/sebi-gr/What-Can-We-Verify/tree/5df7760459b741ae36bd91af4af89f6e3ecfe18d), „wip: handoff for prose or structure repo“.
- Import direkt aus den Git-Blobs; Checkout und Arbeitsdateien des älteren lokalen Quellrepos wurden nicht verändert.
- Der ursprüngliche Import aus `8f9b25e` ist in der Git-Historie dieses Repos erhalten. Der aktuelle Importnachweis ersetzt dessen Dateiliste; keine parallelen Dokumentversionen.

15 Quelldateien bilden die aktuelle Basis:

| Dateien | Zweck |
|---|---|
| `src/01_prepare_case.py`, `src/02_generate_findings.py`, `src/03_decompose_findings.py` | Vorbereitung, Reportgenerierung und P-Extraktion samt lokaler Validierung |
| `tests/__init__.py`, `tests/test_01_prepare_case.py`, `tests/test_02_generate_findings.py`, `tests/test_03_decompose_findings.py` | 29 Offline-Tests |
| `resources/review_prompt.txt`, `resources/decomposition_prompt.txt` | Aktuelle Prompts |
| `resources/claim_codebook.md`, `resources/claim_response_schema.json`, `resources/manual_annotation_template.md` | Codebook, P-Antwortvertrag und leere manuelle Vorlage |
| `resources/reproduce_vul4j18.md` | Unverändertes historisches Windows-PoV-Protokoll |
| `.env.example`, `LICENSE` | Leerer OpenAI-Key-Eintrag und identische MIT-Lizenz |

[resources/inherited_baseline.json](../resources/inherited_baseline.json) enthält pro Datei den Quell-SHA-256. Für zwei lokale Anpassungen sind zusätzlich `local_sha256` und die Begründung gespeichert:

- Decomposer-Testfixture: temporären Basispfad mit `resolve()` auflösen. Der macOS-Systemlink `/var` löste sonst bereits vor den fachlichen Tests die produktive Symlink-Sperre aus. Keine Änderung an dieser Sperre oder an den Pipeline-Skripten.
- Annotationsvorlage: README-Linkanker an die Dokumentation dieses Repos angepasst.

Die übrigen 13 Dateien sind bytegleich zur Quelle. Der Nachweis beschreibt diesen Importzeitpunkt; spätere Änderungen werden über Git nachvollzogen. Der alte `review_prompt_v1.txt` heißt nun wie upstream `review_prompt.txt`, mit identischen Bytes. Historische Laufkopien dürfen deswegen nicht umbenannt werden.

Die neue Quelle stellt beide Modellschritte von OpenRouter auf direkte OpenAI Chat Completions um. Diese zusammengehörige Änderung einschließlich `.env.example` und Tests wurde übernommen; kein Live-Aufruf und keine Schlüsselübernahme. Neue Aufrufe haben keine `:free`-Beschränkung. Der historische Nemotron-Review bleibt ein OpenRouter-Lauf.

README, AGENTS, WORKPLAN und HANDOFF bleiben auf das neue P/D-Paper ausgerichtet. Der alte Verifikationsplan wird nicht zurückkopiert. Quellen für übernommene Entwicklungsbefunde sind das [Quell-HANDOFF](https://github.com/sebi-gr/What-Can-We-Verify/blob/5df7760459b741ae36bd91af4af89f6e3ecfe18d/HANDOFF.md) und der [Quell-WORKPLAN](https://github.com/sebi-gr/What-Can-We-Verify/blob/5df7760459b741ae36bd91af4af89f6e3ecfe18d/WORKPLAN.md).

## Projektskizze

Die [vierseitige PDF](../prose_or_structure_projektskizze.pdf), Version 0.1 vom 03.10.2026, wurde beim ersten Import vollständig gelesen und bleibt unverändert.

SHA-256: `feba77100f85f88b586e3c54e0e60f0fd120888dd88d894c78e3b5f107b774b2`.

RQs, P/D-Abgrenzung, Feldgruppen und Vergleichsbedingungen bestimmen den neuen Plan. Literaturangaben und Neuheitsbehauptung wurden bei den Importen nicht neu geprüft; diese Prüfung bleibt vor der Hauptstudie offen.

## Daten- und Evidenzinventar

| Artefakt | Tatsächlicher Stand | Nötige Folgearbeit |
|---|---|---|
| VUL4J-18-Quellpaket/Referenzen | Lokal unter `data/VUL4J-18/`, ignoriert; beim ersten Import frisch erzeugt und geprüft | Bei frischem Clone vorbereiten |
| Aktuelles Codebook, Schema, Prompt, Vorlage | Aus `5df7760` importiert und versioniert | Zum gemeinsamen P/D-Profil weiterentwickeln |
| Historischer JSPWiki-Review | Dokumentiert; Request, Rohantwort, Findings, Manifest fehlen weiter | Originalen Run-Ordner beschaffen, Hashes/IDs prüfen |
| Ausgefüllte manuelle Annotation mit 13 Claims | Nur beschrieben; die importierte Vorlage ist keine ausgefüllte Annotation | `data/annotations/VUL4J-18-review-001/manual_annotation_001.md` samt zugehörigen Originalen beschaffen |
| Decomposition-Läufe 001–003 | Nur Status/Inhaltsbefunde in Quellnotizen; Rohartefakte fehlen | Laufordner unter `data/decompositions/` samt Ressourcen-Snapshots beschaffen |
| Differenzielle Java-PoV-Reproduktion | Protokoll vorhanden; Original-Logs/Metadaten fehlen | Historische Evidenz aus `data/pov/VUL4J-18-001/` sichern |
| Neue P/D-Experimente und unabhängige Referenzannotation | Noch nicht vorhanden | Nach Profil-/Protokollfestlegung implementieren |

Der vollständige Git-Baum von `5df7760` enthält **keine Datei unter `data/`**; die Quell-`.gitignore` enthält unverändert `/data/`. Auch die lokalen Projektordner enthalten nur das vorbereitete Fallpaket. Andere Rechner und private Gesprächsarchive wurden nicht durchsucht. Die Nachlieferung schließt die Lücke bei Implementierung und Codebook, nicht bei den empirischen Originalen.

Für die verbleibende Übernahme sind gezielt die genannten Run-/Annotations-/PoV-Artefakte samt Prüfsummen bereitzustellen. `.env`, heruntergeladene Toolchains, Maven-Caches und Build-Zwischenergebnisse gehören nicht pauschal dazu. Historische Ressourcenbytes und Daten nicht auf heutige Dateinamen/Schemawerte umschreiben.

### Historischer Review und manuelle Annotation

Das frühere [Handoff](https://github.com/sebi-gr/What-Can-We-Verify/blob/8f9b25e1d5d53208f6f58dba9ffba8396a68dd5c/HANDOFF.md) beschreibt Run `0721c0a0-bba7-48c1-a63c-da196a69d97c`, Start 2026-09-23 14:31:07 UTC, Pfad `data/runs/VUL4J-18-review-001/`, Status `completed`, ein Finding. Modell `nvidia/nemotron-3-super-120b-a12b:free`, Provider Nvidia, 8192 Tokenlimit, `reasoning.enabled=false`; berichtete 7,656 Sekunden, 25.832 Prompt-/216 Completion-Tokens, null Reasoning-Tokens und gemeldete Kosten null.

Das aktuelle Quellhandoff ergänzt 13 abgestimmte Entwicklungsclaims, mit Codex-Unterstützung und Vorwissen über Code/Fix/PoV. Das ist keine unabhängige Wahrheitsreferenz. Die Aussagen lassen sich hier ohne Originalannotation nicht prüfen. Frühere Review-Fehlversuche sind laut älteren Quellnotizen am wiederverwendeten Pfad nicht erhalten geblieben; diese Lücke bleibt bestehen.

### Historische automatische Zerlegung

Laut aktuellem Quellhandoff war Decomposition 001 ungültig; 002 und 003 waren formal gültig mit je vier wortgleichen Satz-Propositionen. Die feinere Granularität wurde nicht erreicht, in 003 waren alle Kontext-IDs leer. Letzte dokumentierte Run-ID: `c939bbd8-090a-4c51-b14d-998d1fc8653c`. Das sind übernommene Entwicklungsbefunde, keine hier erneut geprüften Messergebnisse oder allgemeine Modellaussage. Die neue OpenAI-Anbindung ist nicht als Ursache dieser historischen Ergebnisse auszugeben.

### Historischer PoV

[resources/reproduce_vul4j18.md](../resources/reproduce_vul4j18.md) bleibt unverändert. Seine lokalen Pfade beziehen sich auf das frühere Windows-Arbeitsverzeichnis, nicht auf vorhandene Dateien dieses Clones.

Das Protokoll nennt erfolgreiche Builds und unveränderte Tests `WikiServletTest#testNastyDoPost` und `#testDoGet`: verwundbar zwei Assertion-Fehler, gefixt zwei bestandene Tests, ohne Errors/Skips. Das betrifft Mock-Forwarding, nicht sämtliche Report-Claims oder End-to-End-Dateizugriff. Hier wurde kein Java-Build/PoV erneut ausgeführt.

## Fallvorbereitung: unveränderter Prüfstand

Beim ersten Import lief `python3 src/01_prepare_case.py` erfolgreich. Alle neun Download-Dateien stimmten mit ihren Manifest-Hashes und dem vorhandenen Quellrepo-Export überein; auch Manifest und Dataset-Zeile waren bytegleich. Modellkontext: fünf Dateien, 71.907 Originalbytes. Beim zweiten Import ist die Vorbereitung unverändert; der Download wurde nicht unnötig wiederholt.

SHA-256 des lokalen `manifest.json`: `c93abd6ff130bdbad6ed3896b7a85a4f3e69c3177b3df98741c7a409e3a255c3`.

| Quelle | Fixierte Revision |
|---|---|
| [Vul4J-Dataset](https://github.com/tuhh-softsec/Vul4J/blob/376411da11fa705019f731404de1d0679fe73537/dataset/vul4j_dataset.csv) | `376411da11fa705019f731404de1d0679fe73537` |
| [VUL4J-18-Benchmark](https://github.com/tuhh-softsec/Vul4J/tree/07ad7850a041876befb99847053e4b5e181597a5) | `07ad7850a041876befb99847053e4b5e181597a5` |
| [JSPWiki-Fix](https://github.com/apache/jspwiki/commit/88d89d6523802c044cfcb7930cba40d8eeb21da2) | `88d89d6523802c044cfcb7930cba40d8eeb21da2` |

Der Benchmark kann Anpassungen gegenüber Upstream enthalten. Der Export ist kein vollständiges ausführbares Checkout; `pov_status: not_run` bleibt korrekt für die Vorbereitung.

## Lizenzen und Ablage

Projektcode: [MIT](../LICENSE), Copyright 2026 Sebastian Grünewald. JSPWiki behält die mitgelieferten Upstream-Lizenzen/Notices. Vul4J-Dataset: [CC BY 4.0](https://github.com/tuhh-softsec/Vul4J/blob/376411da11fa705019f731404de1d0679fe73537/DATA_LICENSE). Die PDF enthält ihren Layout-Attributionshinweis.

Generierte Daten bleiben zunächst unversioniert unter `data/`; aktuelle Codebook-/Schema-Ressourcen liegen versioniert unter `resources/`. Keine Geheimnisse oder privaten Gespräche übernommen. Eine dokumentierte, gezielte Archivierung/Veröffentlichung der Forschungsdaten bleibt vor der Evaluation erforderlich.
