# Herkunft und Bestandsprüfung

Stand: 2026-10-05. Diese Datei trennt übernommenen Code, tatsächlich verfügbare Daten und nur dokumentierte Vorarbeit. Laufender Plan: [WORKPLAN.md](../WORKPLAN.md); aktueller Übergabestand: [HANDOFF.md](../HANDOFF.md).

## Importquelle

- Repository: [sebi-gr/What-Can-We-Verify](https://github.com/sebi-gr/What-Can-We-Verify).
- Nach `git fetch origin` verwendeter Stand: `origin/main`, Commit [`8f9b25e1d5d53208f6f58dba9ffba8396a68dd5c`](https://github.com/sebi-gr/What-Can-We-Verify/tree/8f9b25e1d5d53208f6f58dba9ffba8396a68dd5c).
- Der lokale Checkout des Quellrepos stand noch auf `finding-generator` / `67a776e`. Importiert wurde direkt aus den neueren Git-Blobs, nicht aus diesem veralteten Arbeitsbaum. Checkout und Arbeitsdateien des Quellrepos wurden nicht verändert.
- Die neue Repository-Historie bleibt eigenständig; keine Übernahme von `.git`, virtueller Umgebung, Schlüsseln oder alten Sessionchroniken.

Neun Dateien sind bytegleich mit dem fixierten Quellstand:

| Dateien | Zweck |
|---|---|
| `src/01_prepare_case.py`, `src/02_generate_findings.py` | Fallvorbereitung und Reportgenerierung |
| `tests/__init__.py`, `tests/test_01_prepare_case.py`, `tests/test_02_generate_findings.py` | Testsuche und 15 bestehende Offline-Tests |
| `resources/review_prompt_v1.txt` | Unveränderter Report-Prompt |
| `resources/reproduce_vul4j18.md` | Historisches Windows-PoV-Protokoll |
| `.env.example` | Leerer Konfigurationseintrag |
| `LICENSE` | Bereits vorhandene, identische MIT-Lizenz |

Die SHA-256-Werte stehen maschinenlesbar in [resources/inherited_baseline.json](../resources/inherited_baseline.json). Diese Datei beschreibt den **Importzeitpunkt**; spätere beabsichtigte Änderungen sind über Git nachvollziehbar und müssen nicht identisch mit der alten Basis bleiben.

`README.md`, `WORKPLAN.md` und `HANDOFF.md` wurden für das neue Paper neu geschrieben; `AGENTS.md` aus den bestehenden Regeln abgeleitet und auf P/D angepasst. Neu sind Herkunftsinventar, erweiterte Ignore-Regeln und ein kleiner Offline-CI-Workflow. Der alte Verifikationsplan bleibt im [fixierten Quellrepo](https://github.com/sebi-gr/What-Can-We-Verify/blob/8f9b25e1d5d53208f6f58dba9ffba8396a68dd5c/WORKPLAN.md) erhalten.

## Projektskizze

Die vorhandene [PDF](../prose_or_structure_projektskizze.pdf), vier Seiten, Version 0.1 vom 03.10.2026, wurde vollständig gelesen und unverändert übernommen.

SHA-256: `feba77100f85f88b586e3c54e0e60f0fd120888dd88d894c78e3b5f107b774b2`.

Ihre RQs, P/D-Abgrenzung, Feldgruppen und vorgeschlagenen Vergleichsbedingungen bestimmen den neuen Arbeitsplan. Die Literaturangaben und Neuheitsbehauptung wurden bei der Einrichtung nicht neu geprüft; der Plan enthält diese Prüfung vor der Hauptstudie.

## Daten- und Evidenzinventar

| Artefakt | Tatsächlicher Stand bei Einrichtung | Nötige Folgearbeit |
|---|---|---|
| VUL4J-18-Quellpaket und Referenzen | Unter `data/VUL4J-18/` frisch erzeugt; mit vorhandenem Export des Quellrepos bytegleich; ignoriert | Bei frischem Clone erneut vorbereiten |
| Historischer JSPWiki-Review | Im alten HANDOFF dokumentiert; Request, Rohantwort, Findings und Run-Manifest fehlen hier | Originalen Run-Ordner beschaffen und Hashes/IDs prüfen |
| Manuelle Zerlegung in 13 Claims | In Abschnitt 6 der Skizze genannt; keine Originaldatei gefunden | Originale einschließlich Bezug zum Report beschaffen |
| Erstes Codebook | In der Skizze genannt; im Git nur älterer Schema-/Kategorieentwurf | Tatsächliches Codebook beschaffen, dann weiterentwickeln |
| Differenzielle Java-PoV-Reproduktion | Versioniertes Protokoll übernommen; Originallogs und Metadaten fehlen hier | Historische Evidenz sichern; falls nötig einen separaten neuen Lauf planen |
| Neue P/D-Experimente und Referenzannotation | Noch nicht vorhanden | Nach Profil- und Protokollfestlegung implementieren |

Gesucht wurde in beiden lokalen Projektordnern einschließlich ignorierter `data/`-Dateien sowie in den nach Fetch verfügbaren Branches und der Git-Dateihistorie des Quellrepos. Im Quellordner ist nur der vorbereitete Fall vorhanden, kein `data/runs/` oder `data/pov/`. Andere Rechner, externe Datenspeicher und private Gesprächsarchive wurden nicht durchsucht. Der Ablageort der fehlenden Originale wurde beim Nutzer angefragt.

### Historischer Review: dokumentiert, hier nicht unabhängig geprüft

Das [alte HANDOFF](https://github.com/sebi-gr/What-Can-We-Verify/blob/8f9b25e1d5d53208f6f58dba9ffba8396a68dd5c/HANDOFF.md) nennt den erfolgreichen Lauf:

- Run-ID `0721c0a0-bba7-48c1-a63c-da196a69d97c`, Start 2026-09-23 14:31:07 UTC.
- Alter Pfad `data/runs/VUL4J-18-review-001/`, Status `completed`, ein Finding.
- `nvidia/nemotron-3-super-120b-a12b:free`, Provider Nvidia, Limit 8192 Tokens, `reasoning.enabled=false`.
- Berichtete Werte: 7,656 Sekunden, 25.832 Prompt-/216 Completion-Tokens, null Reasoning-Tokens und gemeldete Kosten null.

Das sind übernommene Metadaten, keine hier erneut geprüften Messergebnisse und keine Empfehlung eines heute verfügbaren Modells. Frühere Fehlversuche wurden laut Quellnotizen am wiederverwendeten Pfad nicht aufbewahrt. Diese Lücke nicht mit erfundenen Runs auffüllen; neue Läufe benötigen neue Verzeichnisse.

### Historischer PoV: Aussagegrenze

[resources/reproduce_vul4j18.md](../resources/reproduce_vul4j18.md) bleibt als Originalprotokoll unverändert. Alle darin genannten lokalen Pfade, insbesondere `data/pov/VUL4J-18-001/`, beziehen sich auf das frühere Windows-Arbeitsverzeichnis, nicht auf vorhandene Dateien dieses Clones.

Das Protokoll nennt erfolgreiche Builds und die unveränderten Tests `WikiServletTest#testNastyDoPost` und `#testDoGet`: verwundbar zwei Assertion-Fehler, gefixt zwei bestandene Tests, jeweils keine Errors/Skips. Dies betrifft Mock-Forwarding; es bestätigt nicht sämtliche Report-Claims oder End-to-End-Dateizugriff. Hier wurden weder Java-Build noch PoV erneut ausgeführt.

## Erneut geprüfte Fallvorbereitung

`python3 src/01_prepare_case.py` wurde im neuen Repo erfolgreich ausgeführt. Alle neun heruntergeladenen Dateien stimmen mit ihren Manifest-Hashes und den entsprechenden Dateien des vorhandenen Quellrepo-Exports überein. Auch `manifest.json` und `reference/vul4j_row.json` sind bytegleich. Modellkontext: fünf Dateien, insgesamt 71.907 Originalbytes.

SHA-256 des erzeugten `manifest.json`: `c93abd6ff130bdbad6ed3896b7a85a4f3e69c3177b3df98741c7a409e3a255c3`.

| Quelle | Fixierte Revision |
|---|---|
| [Vul4J-Dataset](https://github.com/tuhh-softsec/Vul4J/blob/376411da11fa705019f731404de1d0679fe73537/dataset/vul4j_dataset.csv) | `376411da11fa705019f731404de1d0679fe73537` |
| [VUL4J-18-Benchmark-Snapshot](https://github.com/tuhh-softsec/Vul4J/tree/07ad7850a041876befb99847053e4b5e181597a5) | `07ad7850a041876befb99847053e4b5e181597a5` |
| [JSPWiki-Fix](https://github.com/apache/jspwiki/commit/88d89d6523802c044cfcb7930cba40d8eeb21da2) | `88d89d6523802c044cfcb7930cba40d8eeb21da2` |

Der Benchmark kann Anpassungen gegenüber Upstream enthalten. Der Export ist kein ausführbares vollständiges Checkout. Sein `pov_status: not_run` bleibt korrekt für diesen Vorbereitungslauf.

## Lizenzen und Ablage

Eigener und übernommener Projektcode: [MIT](../LICENSE), Copyright 2026 Sebastian Grünewald. JSPWiki-Dateien behalten die mitgelieferten Upstream-Lizenzen/Notices. Das Vul4J-Dataset steht unter [CC BY 4.0](https://github.com/tuhh-softsec/Vul4J/blob/376411da11fa705019f731404de1d0679fe73537/DATA_LICENSE). Die PDF enthält ihren eigenen Hinweis zur Layoutvorlage.

Generierte Daten bleiben unversioniert unter `data/`; keine Geheimnisse oder privaten Gespräche werden übernommen. Das ist noch kein Archivierungskonzept für die fertige Studie. Eine dokumentierte Datenablage samt gezielter Veröffentlichungsentscheidung ist vor Evaluation erforderlich.
