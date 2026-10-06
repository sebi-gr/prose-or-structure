# Prose or Structure?

**Evaluating Security-Claim Generation in LLM-Based Code Analysis**

Ein Forschungsprototyp zum Vergleich zweier Wege vom selben Codekontext zu
strukturierten Sicherheitsbehauptungen:

- **P:** Code → Fließtextreport → extrahierte Claims
- **D:** Code → direkt erzeugte Claims

Beide Routen verwenden dasselbe Claimprofil. Untersucht werden Code-Fundierung,
relevante Abdeckung, erhaltene Voraussetzungen, Prüfbarkeit und Aufwand; bei P
zusätzlich die Treue zum Report. Eine korrekt extrahierte Aussage kann fachlich
falsch sein. Die Überlegenheit einer Route wird nicht vorausgesetzt.

## Projekt und Stand

Die [aktualisierte Projektdokumentation](docs/projektstand.pdf) beschreibt
Forschungsfragen, Studiendesign, Umsetzung und nächste Schritte. Ihre
[LaTeX-Quelle](docs/projektstand.tex) ist enthalten; die ursprüngliche
[Projektskizze](prose_or_structure_projektskizze.pdf) bleibt unverändert.

Das gemeinsame Profil, beide Erzeugungswege, Zusatzkontrollen und
Annotationsvorlagen sind implementiert. Der erste Pilot mit fünf Java-Fällen,
beiden Codevarianten und zwei Wiederholungen ist technisch abgeschlossen.
Sechs von 82 Aufgaben lieferten ungültige Ausgaben. **Die menschliche
Referenzannotation und der inhaltliche Qualitätsvergleich stehen noch aus.**
Details enthält der [Pilotbericht](docs/PILOT_RUN_20261006.md).

## Einstieg

Python **3.9+** genügt; der Prototyp verwendet ausschließlich die Standardbibliothek.
Für Offline-Tests sind weder API-Key noch Java oder Maven nötig. `-X utf8` stellt
auch unter Windows die erwartete Textkodierung sicher.

```bash
python -X utf8 -m unittest -v
python -X utf8 src/05_prepare_pilot.py --output data/pilot_cases
python -X utf8 src/06_run_pilot.py --cases data/pilot_cases --output data/pilot/preflight
python -X utf8 src/07_prepare_annotations.py --cases data/pilot_cases --output data/annotations/pilot
```

Die Vorbereitung lädt öffentliche Quellen aus fixierten Revisionen und prüft
Hashes. Der Pilotbefehl erstellt ohne `--execute` nur einen Plan. Jeder Export
und Lauf benötigt einen **neuen Ausgabepfad**; vorhandene Daten werden nicht
überschrieben. Die erzeugten Daten bleiben lokal und werden von Git ignoriert.

## Aufbau

| Skript in `src/` | Aufgabe |
|---|---|
| `01_prepare_case.py` | Historischen JSPWiki-Entwicklungsfall vorbereiten |
| `02_generate_findings.py` | Registrierten Codekontext in einen Report überführen |
| `03_decompose_findings.py` | Report vollständig in P-Claims zerlegen (`--finding-id all`) |
| `04_generate_claims.py` | D-Claims direkt erzeugen; optional einmal überarbeiten |
| `05_prepare_pilot.py` | Pilotfälle und getrenntes Referenzmaterial vorbereiten |
| `06_run_pilot.py` | Festen Versuchsplan erstellen oder budgetiert ausführen |
| `07_prepare_annotations.py` | Neutrale Codepakete und leere Arbeitsblätter exportieren |

Die Nummerierung bezeichnet Arbeitsschritte, keine lineare Pipeline. Prompts,
Schema, Codebook und Fallkatalog liegen in `resources/`, Tests in `tests/`.
Alle Skripte dokumentieren ihre Parameter über `--help`.

## Modellläufe

`OPENAI_API_KEY` wird aus der Umgebung oder der lokalen `.env` gelesen;
[.env.example](.env.example) enthält die Vorlage. Die Umgebung hat Vorrang.
Modell, Parameter und Outputlimits stehen in
[pilot_config.json](resources/pilot_config.json). Vor einem neuen Live-Lauf
Preise prüfen und eine Kostenobergrenze festlegen.

```bash
python -X utf8 src/06_run_pilot.py --cases data/pilot_cases \
  --output data/pilot/neuer-lauf --execute --budget-usd "$BUDGET_USD"
```

`BUDGET_USD` ist vorab auf die gewählte positive USD-Grenze zu setzen. Der Runner
reserviert vor jedem Request konservative Kosten und stoppt bei Budget-,
Provider- oder unklaren Transport-/Usage-Problemen. Keine automatischen Retries,
Reparaturen oder Modellwechsel. Standalone-Skripte haben **keine monetäre Sperre**.
Requests, Rohantworten, Ressourcen, Herkunft und Fehler bleiben erhalten;
Usage-basierte Kosten sind Schätzungen, keine Rechnungen.

## Vergleich und Annotation

P und D erhalten identische fixierte Codebytes. P extrahiert alle Findings in
höchstens zwei Aufrufen insgesamt; sein Extraktor sieht nur den Report und
allgemeine Profilanweisungen. D ist vom Erfolg des Reports unabhängig.
Patches, PoVs, Advisories, Labels und menschliche Referenzen werden nicht als
Modellkontext verwendet. Die Modelle haben keinen Toolzugriff.

Das [Claimprofil](resources/claim_profile.md) trennt Aussagen, Bedingungen,
Herkunft und abgeleitete Prüfaufgaben. Validatoren prüfen die Struktur und bei P
exakte Zitate; sie prüfen keine Wahrheit. Der Pilot enthält D-Revision,
Kontextfeld-Ablation sowie Satz- und VeriScore-basierte Extraktionsbaselines.

Menschliche **Codereferenzen entstehen vor Einsicht in Modelloutputs**.
P-Reportreferenzen werden davon getrennt erstellt. Das
[Annotationsprotokoll](resources/annotation_protocol.md) regelt Bewertung,
Unentscheidbarkeit, Doppelannotation und Adjudikation. Entwicklungs- und
Pilotprojekte bleiben von der späteren zurückgehaltenen Evaluation ausgeschlossen.

## Dokumentation und Reproduktion

- [Dokumentationsübersicht](docs/README.md): Projektpapier, Methode und Nachweise
- [WORKPLAN.md](WORKPLAN.md): Reihenfolge, Abschlusskriterien und offene Entscheidungen
- [HANDOFF.md](HANDOFF.md): knapper Stand für die Weiterarbeit
- [AGENTS.md](AGENTS.md): Entwicklungs- und Experimentregeln

LaTeX/PDF lassen sich mit [Tectonic](https://tectonic-typesetting.github.io/) oder
zweimal `pdflatex` aus der Quelle bauen; Details in der Dokumentationsübersicht.
Für Änderungen am Code: `python -X utf8 -m unittest -v` und `git diff --check`.
Offline-Tests prüfen Herkunft, Kontexttrennung, Paarung, Profil und Fehlerverhalten;
sie ersetzen keine Modellbewertung. Ein übersprungener Symlink-Test bestätigt
keinen Schutz.

## Herkunft und Lizenz

Der Prototyp basiert auf [What Can We Verify?](https://github.com/sebi-gr/What-Can-We-Verify).
[PROVENANCE.md](docs/PROVENANCE.md) dokumentiert Import und historische Evidenz.
Die sechs archivierten JSPWiki-Dateien sind Entwicklungsmaterial mit Vorwissen,
keine unabhängige Wahrheitsreferenz. Frühere PoV-Angaben wurden hier nicht neu
reproduziert.

Projektcode: [MIT](LICENSE). Fremde Quellen und Baseline-Prompts behalten ihre
Lizenzen und Herkunftshinweise. Zugangsdaten und generierte Laufdaten gehören
nicht ins Repository; ein gesondertes Forschungsdatenarchiv ist noch festzulegen.
