# Herkunft und Bestandsprüfung

Stand: 2026-10-05, nach Archivierung des vereinbarten Entwicklungspakets. Laufender Plan: [WORKPLAN.md](../WORKPLAN.md); aktueller Stand: [HANDOFF.md](../HANDOFF.md). Code/Ressourcen, historische Dokumentationsbefunde und tatsächlich vorhandene Rohdaten bleiben getrennt.

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

Beim Import waren die übrigen 13 Dateien bytegleich zur Quelle. Der Nachweis beschreibt diesen Importzeitpunkt; spätere Änderungen werden über Git nachvollzogen. Der alte `review_prompt_v1.txt` heißt nun wie upstream `review_prompt.txt`, mit identischen Bytes. Historische Laufkopien dürfen deswegen nicht umbenannt werden.

Die neue Quelle stellt beide Modellschritte von OpenRouter auf direkte OpenAI Chat Completions um. Diese zusammengehörige Änderung einschließlich `.env.example` und Tests wurde übernommen; kein Live-Aufruf und keine Schlüsselübernahme. Neue Aufrufe haben keine `:free`-Beschränkung. Der historische Nemotron-Review bleibt ein OpenRouter-Lauf.

README, AGENTS, WORKPLAN und HANDOFF bleiben auf das neue P/D-Paper ausgerichtet. Der alte Verifikationsplan wird nicht zurückkopiert. Quellen für übernommene Entwicklungsbefunde sind das [Quell-HANDOFF](https://github.com/sebi-gr/What-Can-We-Verify/blob/5df7760459b741ae36bd91af4af89f6e3ecfe18d/HANDOFF.md) und der [Quell-WORKPLAN](https://github.com/sebi-gr/What-Can-We-Verify/blob/5df7760459b741ae36bd91af4af89f6e3ecfe18d/WORKPLAN.md).

## Projektskizze

Die [vierseitige PDF](../prose_or_structure_projektskizze.pdf), Version 0.1 vom 03.10.2026, wurde beim ersten Import vollständig gelesen und bleibt unverändert.

SHA-256: `feba77100f85f88b586e3c54e0e60f0fd120888dd88d894c78e3b5f107b774b2`.

RQs, P/D-Abgrenzung, Feldgruppen und Vergleichsbedingungen bestimmen den neuen Plan. Literaturangaben und Neuheitsbehauptung wurden bei den Importen nicht neu geprüft. Schritt 2 prüft fünf Profilquellen gezielt; vollständige Literatur- und Neuheitsabgrenzung bleiben vor der Hauptstudie offen.

## Archivimport der sechs Entwicklungsartefakte

Der Nutzer hat die ausgewählten Dateien aus dem anderen Rechner bereits in dieses Repo gepusht. Ausgangspunkt für die Einordnung ist Commit [`e24c634`](https://github.com/sebi-gr/prose-or-structure/tree/e24c6347d4fbd8a140af8d81e866f5a4fa9fe335); dort lagen die sechs Dateien im Repo-Wurzelverzeichnis. Sie sind jetzt unter ihren ursprünglichen logischen Run-/Annotationspfaden abgelegt. Insgesamt **108.158 Bytes**, keine großen Build-Verzeichnisse.

| Datei | Archivpfad |
|---|---|
| Angenommene manuelle Revision, 13 Claims | [manual_annotation_001.md](../data/annotations/VUL4J-18-review-001/manual_annotation_001.md) |
| Originalfinding mit ID und Report | [findings.jsonl](../data/runs/VUL4J-18-review-001/findings.jsonl) |
| Exakter historischer Request | [request.json](../data/runs/VUL4J-18-review-001/request.json) |
| Unveränderte Provider-Antwort | [generation_raw.json](../data/runs/VUL4J-18-review-001/generation_raw.json) |
| Ursprünglicher Review-Prompt | [review_prompt_v1.txt](../data/runs/VUL4J-18-review-001/review_prompt_v1.txt) |
| Historisches Laufmanifest | [run_manifest.json](../data/runs/VUL4J-18-review-001/run_manifest.json) |

[resources/inherited_artifacts.json](../resources/inherited_artifacts.json) hält Quellcommit, alte/neue Pfade, empfangene und archivierte SHA-256-Werte sowie die einzige Wiederherstellung fest. Die Daten gehören zum alten What-Can-We-Verify-Entwicklungsfall; der Git-Importweg führt über den Nutzercommit in diesem Repo. `.gitignore` erlaubt genau diese sechs Dateien, `.gitattributes` verhindert ihre automatische Zeilenumbruch-Konvertierung. Alle anderen neuen Daten bleiben ignoriert.

### Prüfergebnis: Originalreport und Annotation gehören zusammen

- Request- und Antwortbytes stimmen mit `request_sha256` und `response_sha256` im historischen Manifest überein. Requestparameter, Modell-/Provider-/Response-ID und Usage sind konsistent.
- Die Rohantwort ergibt exakt das gespeicherte Finding mit ID `0721c0a0-bba7-48c1-a63c-da196a69d97c:F001`, einschließlich unverändertem Titel und Report. Der Eingabelader des aktuellen P-Decomposers akzeptiert diese Datei; kein Modellrequest nötig.
- Der in der Annotation gespeicherte Finding-Hash `ac2711de8101111aa23a0861553cfe60489fa40393dc4806fc5e2b0bd794308a` stimmt. Eingebetteter Titel und Originalreport sind identisch mit dem Finding.
- 13 eindeutige manuelle Claim-IDs, alle 15 Originalzitate und die Auflösbarkeit der Kontextverweise geprüft. Das ist eine Konsistenzprüfung, keine erneute Bewertung der semantischen Qualität oder Wahrheit.
- Alle fünf aus fixierten Quellen vorbereiteten Modelldateien stimmen mit den historischen Quellhashes überein. Auch die daraus rekonstruierte vollständige User-Nachricht mit Pfaden und Originalzeilennummern entspricht dem gespeicherten Request exakt. Die zusätzliche `model_input/`-Kopie des alten Runs muss daher nicht versioniert werden.

### Wiederherstellung des historischen Prompts

Die gelieferte Git-Datei `review_prompt_v1.txt` hatte LF-Zeilenumbrüche (740 Bytes, SHA-256 `a9846dfe5458c8642631e38a22467c9f4bacfea92f22296d15c86f4a66638bd6`). Der historische Request enthält dieselben Zeilen mit CRLF (751 Bytes). Dessen unveränderte Systemnachricht ergibt exakt den im Manifest gespeicherten Prompt-Hash `e3dcce357e15d5040fc52fd58c707038fb1124946d834999d898d7d082bef0ee`.

Für das Archiv wurden diese Originalbytes direkt aus dem Request wiederhergestellt; weder Inhalt noch Manifest geändert. Die anderen fünf gelieferten Dateien sind bytegleich mit dem Eingang. Der heutige aktive Prompt `resources/review_prompt.txt` bleibt unverändert. Auch der historische Generatorhash lässt sich mit der CRLF-Fassung von `src/02_generate_findings.py` aus What-Can-We-Verify-Commit `8f9b25e` nachvollziehen; heutige OpenAI-Skripte werden nicht als damalige Implementierung ausgegeben.

Die Provider-Rohantwort enthält führende Leerzeilen mit Leerzeichen. Diese Bytes gehören zum geprüften Antwort-Hash und werden nicht bereinigt. `.gitattributes` nimmt ausschließlich `generation_raw.json` von der Whitespace-Prüfung aus und erlaubt für den historischen Prompt CRLF; die Formatprüfung für Projektcode und Dokumentation bleibt aktiv. Dies berücksichtigt auch den flachen CI-Checkout, bei dem Git den gesamten Baum statt nur Umbenennungen prüfen kann.

### Aussagegrenzen der historischen Daten

Das Manifest dokumentiert Run `0721c0a0-bba7-48c1-a63c-da196a69d97c`, Start 2026-09-23 14:31:07 UTC, `completed`, ein Finding. Modell `nvidia/nemotron-3-super-120b-a12b:free`, Provider Nvidia über OpenRouter, 8192 Tokenlimit, `reasoning.enabled=false`; 7,656 Sekunden, 25.832 Prompt-/216 Completion-Tokens, null gemeldete Reasoning-Tokens und gemeldete Kosten null. Diese gespeicherten Werte wurden mit der Rohantwort abgeglichen, nicht durch eine neue Inferenz reproduziert. `cost_usd` bleibt im Originalmanifest `null`.

Die Annotation vom 24.09.2026 benennt SG als Annotator, Codex-Unterstützung bei Revision/Prüfung und Vorwissen über Code/Fix/PoV. Sie ist die angenommene Entwicklungsrevision, keine unabhängige Wahrheitsreferenz. Historische Hinweise darin wie „Schema und Automation folgen“ oder „ignoriertes data/“ bleiben als Originaltext erhalten; den heutigen Stand beschreiben README und WORKPLAN.

Die Annotation verweist auf `claim_codebook_v0_2.md` (Hash `e7549f8b357b25225e1eff5057b5e9c99a190234d5cd1bc58793f0506992250a`), `manual_annotation_submitted_001.md` und `annotation_review_001.md`. Diese drei zusätzlichen historischen Dateien wurden nicht geliefert. Der heutige konsolidierte Codebook-Stand ist vorhanden, ersetzt aber nicht den alten Snapshot. Die Revisionsgeschichte lässt sich damit nicht vollständig prüfen; das verhindert die Weiterarbeit mit der angenommenen Annotation nicht.

## Rekonstruierbare Daten und optionale Ergänzungen

| Material | Stand und Entscheidung |
|---|---|
| VUL4J-18-Code, Fix, PoV-Testdatei, Exportmanifest | Lokal vorhanden und geprüft; mit `src/01_prepare_case.py` aus fixierten Quellen erneut erzeugbar, ignoriert |
| Java-Checkouts, Toolchain, Maven-Cache und Build-Ausgaben | Nicht übernommen; bei Bedarf separat neu aufsetzen. Vorbereitung allein führt keinen Java-Test aus. |
| Historische Decomposition-Läufe 001–003 | Nicht geliefert; optional für Vergleiche, keine Voraussetzung für Profilentwicklung oder neue Extraktion |
| Alte PoV-Rohlogs und Ergebnisdatei | Nicht geliefert; optionaler Beleg des damaligen Laufs. Protokoll vorhanden; ein neuer Lauf wäre neue Evidenz. |
| Alte Annotationsabgabe, Review und Codebook v0.2 | Nicht geliefert; optionale Ergänzung zur Revisionsgeschichte |

Laut [Quellhandoff](https://github.com/sebi-gr/What-Can-We-Verify/blob/5df7760459b741ae36bd91af4af89f6e3ecfe18d/HANDOFF.md) war Decomposition 001 ungültig, 002/003 formal gültig mit vier zu groben, wortgleichen Satz-Propositionen; in 003 waren alle Kontext-IDs leer. Letzte dokumentierte Run-ID: `c939bbd8-090a-4c51-b14d-998d1fc8653c`. Diese optionalen historischen Befunde sind mangels Rohdaten weiterhin nicht hier geprüft. Früher überschriebene Review-Versuche bleiben laut alten Notizen unvollständig dokumentiert.

Das unveränderte [PoV-Protokoll](../resources/reproduce_vul4j18.md) beschreibt die damaligen Windows-Pfade und zwei erwartete Assertion-Fehler der verwundbaren gegenüber zwei bestandenen Tests der gefixten Version, ohne Errors/Skips. Getestet wurde Mock-Forwarding, nicht beliebiger Dateizugriff oder die Wahrheit aller Claims. Hier wurde kein Java-Build/PoV neu ausgeführt. Die fehlenden alten Logs blockieren das vereinbarte minimale Übergabepaket nicht.

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

Sechs vom Nutzer gezielt gelieferte Entwicklungsartefakte sind nun unter `data/` versioniert; alle übrigen generierten Daten bleiben ignoriert. Der gespeicherte Request enthält den öffentlichen JSPWiki-Quellkontext samt ursprünglichen Lizenzkommentaren; weitere Lizenz-/Notice-Dateien werden mit der Fallvorbereitung geladen. Aktuelle Codebook-/Schema-Ressourcen liegen unter `resources/`. Keine Zugangsdaten übernommen. Dieses kleine Entwicklungsarchiv legt noch nicht die Archivierung der späteren Hauptstudie fest.

## Profilentwicklung, Schritt 2

Am 05.10.2026 wurden das gemeinsame [Profil](../resources/claim_profile.md),
Schema und Annotationsprotokoll erstellt; Codebook und Arbeitsblatt bewusst
weiterentwickelt. Die Importhashes bleiben als historische Herkunft erhalten;
der aktuelle Ressourcenstand ist über Git und bei neuen Läufen über deren
Snapshots nachvollziehbar. Die drei Python-Skripte, beide Prompts und der alte
P-Antwortvertrag wurden dabei nicht geändert.

[Entwicklungsfälle](../resources/profile_development/README.md) und
[sources.json](../resources/profile_development/sources.json) dokumentieren die
gezielt ausgewählten Vul4J-47-/Vul4J-9-Quellen: fixierte Upstream-/Benchmark-SHAs,
volle Quellhashes und archivierte Bytes/Zeilen. Jackson ist ein unveränderter
Ausschnitt (84–144), YAML eine unveränderte vollständige Datei. Beide gesamten
Originaldateien wurden bytegleich mit den fixierten Vul4J-Snapshots verglichen.
Die 19.000 Bytes Quell-/Lizenzmaterial bleiben unter Apache 2.0; LICENSE und
Notices liegen bei. Die Git-Attribute schützen Originalbytes und nehmen nur die
beiden Fremdquellen mit absichtlichen Leerzeichen von der Whitespace-Prüfung aus.

Die neuen JSON-Beispiele und Referenztabellen wurden durch Codex anhand dieser
Quellen und des historischen JSPWiki-Materials redaktionell erstellt. Keine
neue menschliche Annotation, keine unabhängige Ground Truth, kein API-Aufruf
und kein Java-Build/PoV. Der bekannte Report sowie Fix-/Datasetkenntnis beeinflussen
die Entwicklungsauswahl; diese Beispiele sind nicht verblindet oder zurückgehalten.
Alle sechs historischen Artefakte bleiben bytegleich zu `inherited_artifacts.json`.

## Umsetzung des gemeinsamen Profils, Schritt 3

Am 05.10.2026 wurde P auf Profil 0.1 umgestellt und die direkte D-Erzeugung
ergänzt. Die importierten Skripte 02/03 und der aktive P-Prompt wurden dabei
bewusst geändert; ursprüngliche Importhashes bleiben historische Nachweise.
Der Vorbereitungscode und der API-Transport sind unverändert. Ein gemeinsamer
Quellformatter bewahrt den bisherigen Requesttext; ein kleiner gemeinsamer
Validator ersetzt den alten achtteiligen P-Vertrag. D und Paarungsprüfung nutzen
keine zusätzlichen Laufzeitabhängigkeiten. Das alte aktive Antwortschema ist
entfernt, über Git aber vollständig nachvollziehbar.

`review_pair.py` prüft Originalrequest-/Antwortbytes gegen das Manifest und
Findingtext/IDs gegen die Rohantwort. D prüft außerdem die fünf Quellhashes und
die exakt rekonstruierte User-Nachricht. Der historische Review funktioniert
auch ohne nachträglich hinzugefügten Finding-Hash oder Variantenlabel; unbekannte
Varianten heißen in neuen Kindläufen `unspecified`. Originalmanifest unverändert.

60 Offline-Tests prüfen Profil, Paarung und Fehlerverhalten; ein zusätzlicher
Smoke-Test verwendete den archivierten JSPWiki-Report und das echte fünfteilige
Codepaket mit ausdrücklich ersetzten API-Antworten aus den Entwicklungsfixtures.
Vier P- und zwei D-Beispielclaims wurden formal akzeptiert. Das sind keine neu
generierten Claims oder Vergleichsresultate. Temporäre Ausgaben wurden entfernt;
kein HTTP-Modellaufruf, Java-Build oder PoV. Die sechs Archivdateien und die
Apache-Quell-/Lizenzfixtures bleiben bytegleich zu ihren Herkunftsnachweisen.

Die neuen Laufmanifeste speichern Ressourcen-/Implementierungshashes, Route/Stufe,
Fall/Variante, Parent-/Paar-ID, Modellparameter, Usage und Zeit. Nicht ausgewiesene
Kosten bleiben null. Alte Claimdateien werden weder automatisch migriert noch
überschrieben. Profil 0.1 ist jetzt operativ; Aussagen des vorherigen Abschnitts
beschreiben den Zustand unmittelbar nach Schritt 2.
