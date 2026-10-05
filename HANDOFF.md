# Handoff: Prose or Structure?

Stand: 2026-10-05, nach Schritt 3. Maßgeblich: [WORKPLAN.md](WORKPLAN.md),
[Projektskizze](prose_or_structure_projektskizze.pdf), [Herkunft](docs/PROVENANCE.md).

## Ziel und nächster Schritt

P: Code → Report → Claims und D: Code → Claims bei identischem Codekontext
vergleichen. RQ1 entwickelt das Profil, RQ2 vergleicht Qualität/Aufwand, RQ3
untersucht Darstellungsfehler und Kontextfelder. Keine Überlegenheit vorwegnehmen.

**Schritt 3 ist für den VUL4J-18-PoC implementiert und offline geprüft.**
Als Nächstes Schritt 4: Pilotprotokoll festlegen, dann die erforderlichen
Pilotergänzungen und geplanten Läufe. Modell, Budget, Reporteinheit, Fallbestand,
Referenzen/Doppelannotation, Baselines und Fehlerregeln sind noch offen.
Keine ungeplanten API-Aufrufe; in dieser Umsetzung wurde keiner ausgeführt.

## Ausführbare Basis

| Datei | Aktueller Zweck |
|---|---|
| `src/01_prepare_case.py` | Unveränderter Export von fünf VUL4J-18-Quelldateien und getrennten Referenzen; kein Java-Test |
| `src/02_generate_findings.py` | Prose-Review; vorhandener Transport, gemeinsame Quellformatierung, Route/Stufe/Variantenlabel und Finding-Hash ergänzt |
| `src/03_decompose_findings.py` | Ein gespeichertes Finding aus geprüftem Review → Profil 0.1; nur Titel/Report im fallbezogenen Modellinput |
| `src/04_generate_claims.py` | Direkte Profilclaims aus exakt demselben Codekontext wie der über `--review-run` bezeichnete Review |
| `src/claim_profile.py` | Gemeinsame feste Validierung, P-Zitate/Unicode-Offsets und getrennte D-Codepositionsdiagnosen |
| `src/review_pair.py` | Vier originale Reviewartefakte prüfen; Quellhashes und tatsächlich gesendeten Codekontext vergleichen |

Befehle stehen in [README.md](README.md). P benötigt neben `findings.jsonl`
Manifest, Request und Rohantwort desselben Reviews. D benötigt den Reviewordner
und die fünf Modelldateien; die lokale Vorbereitung stimmt mit dem historischen
Review überein. Abweichungen stoppen vor API-Aufruf und Ausgabeverzeichnis.
Die Fall-ID/Dateiliste bleibt bewusst auf VUL4J-18 begrenzt; XML/YAML sind weiterhin
nur Profilentwicklungsbeispiele. Kein allgemeines Benchmark-Framework gebaut.

Gemeinsamer Vertrag: [Profil 0.1](resources/claim_profile.md),
[Schema](resources/claim_profile.schema.json), [Codebook](resources/claim_codebook.md).
Der alte aktive `claim_response_schema.json`-Vertrag ist entfernt; alte Snapshots
und Git-Historie bleiben erhalten. `claims.jsonl` ergänzt lokale Run-/Routenfelder
und bei P Finding-ID/Quote-Offsets; das Antwortschema beschreibt den Modelloutput.
Keine generierten Wahrheitslabels. Falsche Codepositionen bleiben erhalten;
D protokolliert sie nichtfatal in `validation.json`, P liest dafür keinen Code.

Alle Modellschritte verwenden den vorhandenen OpenAI-Aufruf mit explizitem Modell
und Tokenlimit, `store=false`, ohne Tools, Retry oder Repair. Fehlende Schlüssel
senden nichts. Rohantworten und Fehler bleiben erhalten, keine Teilclaims oder
Überschreibung. `cost_usd` bleibt ohne Abrechnung null, gemeldete Usage gespeichert.
Unbekannte Varianten bleiben `unspecified`; `--case-variant` am Reportgenerator
ist ausschließlich ein Metadatenlabel und gelangt nicht ins Modell.

## Forschungskontext und Grenzen

- P und D teilen `paired_review_run_id` und Quellhashes. P nennt den Report als `parent_run_id`; D hat keinen kausalen Reportparent. Die ursprünglichen Parentdateien für spätere Prüfung erhalten.
- Der aktuelle Extraktor arbeitet pro Finding: P benötigt 1 + N Aufrufe bei N Findings, D einen für den Codefall. Der archivierte Ein-Finding-Fall erfüllt den Zwei-Aufruf-Entwurf. Vor Pilot Reporteinheit festlegen und alle Findings einbeziehen; keine günstige Auswahl einzelner Findings.
- `no_findings` bedeutet keine P-Extraktion und kann D verankern. Ein fehlgeschlagener P-Review kann D aktuell nicht verankern; fehlende Routen vorab im Pilotprotokoll regeln.
- [Annotationsprotokoll](resources/annotation_protocol.md) und [Arbeitsblatt](resources/manual_annotation_template.md) trennen Reporttreue, Codereferenz, Unsicherheit/Prüfbarkeit und Adjudikation. Neue Referenzen vor Einsicht in Ausgaben erstellen.
- Reale Beispiele/Referenzen unter `resources/profile_development/`, Annotationen und Manifeste nie als Modellkontext verwenden. Das Codebook bleibt generisch.
- Alle drei Profilentwicklungsfälle samt Varianten bleiben Entwicklung, nicht Holdout. Neue Beispiele sind KI-gestützte Entwürfe; keine unabhängige menschliche Referenz, Annotationzeit oder Übereinstimmung gemessen.
- D mit Überarbeitung, Extraktionsbaselines, Ablation, Pilot-/Hauptstudienauswertung fehlen weiterhin. Fünf Profilquellen gezielt geprüft; vollständige Literatur-/Neuheitsabgrenzung offen.

## Historisches Archiv erhalten

Sechs Originaldateien in `data/runs/VUL4J-18-review-001/` und
`data/annotations/VUL4J-18-review-001/`, zusammen 108.158 Bytes. Alle Hashes aus
`resources/inherited_artifacts.json` unverändert. SG-Annotation mit 13 Claims und
Codex-Unterstützung/Vorwissen bleibt genau erhalten. Historischer Run
`0721c0a0-bba7-48c1-a63c-da196a69d97c` war OpenRouter/Nemotron; keine nachträglich
kontrollierte Vergleichsstudie mit heutigen Modellen daraus ableiten.

Andere Downloads/Läufe bleiben ignoriert. Zusätzliche alte Decomposition-/PoV-Logs,
Originalabgabe/Review und damaliges Codebook v0.2 fehlen optional; heutige Dokumente
sind kein Ersatz für diese historischen Originale.

## Prüfstand

- **60 Offline-Tests bestanden**, inklusive gemeinsamer Profilfixtures, Unicode/Zitatkonvention, Herkunft, Quellpaarung, Requesttrennung, leerer/ungültiger Ergebnisse und Fehlerpersistenz.
- Archivierter JSPWiki-Report und reales Codepaket durch beide neuen Routen mit ausdrücklich ersetzten Modellantworten geprüft: vier P-/zwei D-Fixtureclaims, passende Hashes und gesendeter Codekontext. Temporäre Outputs entfernt; kein echter Modelllauf.
- Vier CLI-Hilfen und Whitespace-Prüfung erfolgreich. Originalarchiv und Fremdquellen unverändert; Links und Funktionskommentare geprüft.
- Keine neue Java-/PoV-Ausführung und keine P/D-Qualitätsmessung. Tests belegen lokale Implementierungseigenschaften, keine Live-Modellkompatibilität oder wissenschaftlichen Ergebnisse.
