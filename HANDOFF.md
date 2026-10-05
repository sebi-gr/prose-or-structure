# Handoff: Prose or Structure?

Stand: 2026-10-05. Maßgeblich: [WORKPLAN.md](WORKPLAN.md),
[Projektskizze](prose_or_structure_projektskizze.pdf),
[Pilotprotokoll 0.1](docs/PILOT_PROTOCOL.md).

## Stand und nächste Aktion

Schritte 2–3 sind umgesetzt; **Schritt 4 ist technisch vorbereitet und offline
geprüft**, aber ohne neue Modellläufe oder menschliche Pilotbewertung.
Die beauftragte autonome Arbeit ist bis zum fehlenden API-Zugang und der noch
nicht gewählten Kostenobergrenze fortgeführt. Die Frage nach dem Budget wurde
bereits gestellt; keine Kostenfreigabe oder menschliche Annotation unterstellen.

Nächster ausführbarer Schritt: nach bereitgestelltem `OPENAI_API_KEY` in `.env`
oder Umgebung und gewählter USD-Grenze den fixierten Pilot einmal starten.
Preise bei späterem Start erneut prüfen. Befehl in README; neue Ausgabepfade,
keine automatischen Retries oder stillen Modellwechsel. Es gibt keinen aktiven
Hintergrundlauf. Danach tatsächliche Fehler/Usage auswerten; Codeinventare müssen
vor Einsicht der Annotatoren in Modellausgaben entstehen, nicht zwingend vor
bloßer Generierung. Menschliche Referenzen und Doppelannotation bleiben nötig.

## Vorbereiteter Versuch

- Fünf neue Fälle: VUL4J-15/64 (XXE), VUL4J-41/43/76 (Pfadverarbeitung).
  Je vulnerable/fixed, zwölf volle Quelldateien pro Variante insgesamt, jedes
  Kontextpaket unter 34 KB. Alle URLs/Revisionen/Hashes im Katalog.
- P bündelt alle Findings in einer gespeicherten Reportansicht (`finding-id all`),
  behält Originaltexte und braucht höchstens zwei Calls. Keine günstige Auswahl.
  D prüft dieselben Codebytes direkt gegen den Katalog und ist unabhängig von P.
- Modell `gpt-5.4-mini-2026-03-17`, Reasoning none, Default-Tier. Zwei
  Wiederholungen mit balancierter P/D-Reihenfolge; 60 Kernaufrufe maximal.
  D-Revision in Wiederholung 1: zehn Zusatzaufrufe. Beide Varianten 15/41:
  acht Ablationsaufrufe sowie Satz-/VeriScore-Baselines mit variabler Satzanzahl.
- D-Revision ist eine Zwei-Aufruf-Kontrolle, nicht tokenidentisch zu P.
  Kontextablation entfernt das explizite Objekt, erhält aber Propositionbedingungen
  und Kontext-IDs. VeriScore basiert auf einem lizenzierten Originalprompt,
  Regex-Satzgrenzen und zusätzlichen Titelsatzzielen; keine exakte Reproduktion.
- Feste Planreihenfolge, Ressourcen-/Implementierungshashes, Einzelrequests und
  Rohantworten erhalten. Der Runner reserviert vor dem Transport konservative
  Kosten; Budget-, HTTP-, Usage- und Transportprobleme stoppen den restlichen Lauf.
  Formatfehler sperren nur abhängige Stufen. Keine Rechnung oder wissenschaftlichen
  Qualitätsurteile aus geschätzten Kosten/Formatchecks ableiten.

## Dateien und lokale Artefakte

| Datei | Aufgabe |
|---|---|
| `src/01_prepare_case.py` | Unveränderter VUL4J-18-Export |
| `src/02_generate_findings.py` | Registrierter Codekontext → Report |
| `src/03_decompose_findings.py` | Einzelnes Finding oder vollständiger Report → P-Claims |
| `src/04_generate_claims.py` | Unabhängige Pilot-D-Claims; optional passende D-Revision |
| `src/05_prepare_pilot.py` | Atomarer Export aller Pilotquellen/Referenzen |
| `src/06_run_pilot.py` | API-freier Plan oder budgetierter Live-Lauf |
| `src/07_prepare_annotations.py` | Zehn neutrale Code-/Leerblattpakete |
| `src/case_context.py`, `pilot_profile.py`, `extraction_baselines.py` | Kleine konkrete Pilothelfer |
| `docs/RELATED_WORK.md`, `resources/references.bib` | Sieben geprüfte Vorarbeiten, Abgrenzung und korrigierte GPTAid-DOI |

Lokal vorhanden, absichtlich ignoriert:

- `data/pilot_cases/`: alle fünf Fälle mit beiden Varianten und getrennten
  Lizenzen/Testquellen. Hashes geprüft; keine Java-/PoV-Ausführung.
- `data/pilot/preflight-002/`: finaler API-freier Plan, 82 Aufgaben einschließlich
  vier Baselinegruppen. `preflight-001` ist der erhaltene frühere Entwicklungsstand.
- `data/annotations/pilot-001/`: zehn leere Arbeitsblätter und Codepakete,
  Zuordnung in separatem `linkage.json`. Vier Pakete für zweite unabhängige
  menschliche Annotation vorgewählt. Keine Urteile oder Zeiten ausgefüllt.

Ein Clone reproduziert diese Artefakte über die README-Befehle. Keine vollständigen
Java-Repositories, Toolchains oder tausende Builddateien nötig. APIs sehen nur die
Quell-Allowlist oder Reporttexte, niemals Labels, Referenzen oder Annotationen.
Der annotierte Pilot und ein Forschungsdatenarchiv stehen weiterhin aus.

## Prüfstand

- **106 Offline-Tests bestanden.** Neue Prüfungen für Katalogquellen, ganze
  Reports, D vor/nach P, Revision, beide Ablationen, Titel-/Satzbaselines,
  Budgetreservierungen und Fehlerisolation sowie Annotationsexport.
- Echter Download aller zehn Kontexte erfolgreich; finaler Dry-Run und
  Annotationsexport erfolgreich, ohne API-Zugriff.
- Vollständiger Ablauf auf realen Codepaketen mit **82 Aufgaben und 94 synthetischen
  Antworten** bestanden. Transport ausdrücklich ersetzt, temporäre Outputs
  entfernt. Keine Live-Kompatibilität oder Qualitätsmessung daraus ableiten.
- Sechs historische Archivdateien samt Hashes unverändert; alle Quellen und
  fremden Prompts behalten eigene Lizenzen. Funktionskommentare geprüft.
- Die geerbten JSPWiki-/Jackson-/YAML-Beispiele und alle Pilotprojekte bleiben
  vom späteren Holdout ausgeschlossen. Projekt-/Variantenverwandtschaft beachten.

## Menschliche Arbeit und wissenschaftliche Grenzen

Die Code-/Reportreferenzen und Claimurteile folgen dem Annotationsprotokoll.
Zwei unabhängige menschliche Annotationen für beide Varianten von 15/41 vor
Adjudikation; weitere Pakete mindestens einfach annotieren, echte aktive Minuten
und Vorwissen festhalten. Neutralnummern verbergen Labels, aber keine im Code
sichtbaren Projektmerkmale. Keine KI-Ausgabe als menschliche Wahrheit ausgeben.

Literaturvorbereitung für Schritt 5 ist vorhanden; breitere Neuheitsprüfung,
Pilotannotation, Hauptstichprobe, statistischer Plan und Abstimmung mit Betreuung
bleiben offen. Kein Hauptstudienlauf oder Ergebnispaper ohne diese Grundlagen.
Das historische Archiv unter `data/runs/VUL4J-18-review-001/` und seiner Annotation
bleibt Entwicklungsarbeit mit Vorwissen; heutige Ressourcen ersetzen keine damals
fehlenden Rohlogs oder historischen Codebook-Versionen.
