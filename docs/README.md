# Dokumentation

## Projektüberblick

[Projektplan und Arbeitsstand (PDF)](projektstand.pdf) ist die aktuelle
Diskussionsgrundlage für Dr. Andreas Ekelhart. Die ersten fünf Abschnitte
erläutern den Projektplan der [ursprünglichen Skizze](../prose_or_structure_projektskizze.pdf)
und machen den Ablauf an echtem Code und Pilotausgaben verständlich.
Der damalige Arbeitsstand ist durch Profil, Prototyp, technischen Pilotabschluss
und nächste Schritte ersetzt. Der bereits geprüfte GPTAid-DOI ist korrigiert;
das Original-PDF bleibt unverändert.

Das ZIP-Beispiel führt von Code und Report zu P-/D-Claims und erklärt anschließend
Referenzen und Bewertung. VeriScore und der Vergleich mit und ohne Kontextfelder
werden gesondert erläutert. Die Beispielreferenzen und Bewertungsurteile dienen
der Erklärung; sie sind keine unabhängigen menschlichen Pilotannotationen.

Die [LaTeX-Quelle](projektstand.tex) enthält das vollständige Dokument einschließlich
Literatur und Layout. Kompilieren vom Repository-Wurzelverzeichnis:

```bash
tectonic --outdir docs docs/projektstand.tex
```

Alternativ mit einer üblichen TeX-Installation zweimal ausführen:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=docs docs/projektstand.tex
```

Die zweite Ausführung löst Querverweise und Seitenzahlen auf. Die PDF wird neben
der Quelle versioniert; Hilfsdateien bleiben ignoriert. LaTeX ist nur zum
Bearbeiten der Dokumentation erforderlich, nicht für den Forschungsprototyp.

## Methode und Nachweise

| Dokument | Inhalt |
|---|---|
| [Pilotprotokoll](PILOT_PROTOCOL.md) | Vor dem ersten Lauf fixiertes Versuchsdesign; historische Planfassung unverändert |
| [Fallauswahl](PILOT_CASES.md) | Quellen, Variantenpaarung, Grenzen und Holdout-Ausschlüsse |
| [Pilotbericht](PILOT_RUN_20261006.md) | Technische Ergebnisse, Validierungsfehler und Kosten des ersten Piloten |
| [Vorarbeiten](RELATED_WORK.md) | Gezielte Literaturabgrenzung und Baselineentscheidung |
| [Herkunft](PROVENANCE.md) | Import, archivierte Originale, Lizenzen und Evidenzgrenzen |
| [Claimprofil](../resources/claim_profile.md) | Gemeinsamer Antwortvertrag für P und D |
| [Annotationsprotokoll](../resources/annotation_protocol.md) | Getrennte Referenzen, Bewertungsregeln und Doppelannotation |

Der [Arbeitsplan](../WORKPLAN.md) enthält Status, Reihenfolge und offene
Entscheidungen; [HANDOFF.md](../HANDOFF.md) den knappen operativen Übergabestand.
Historische Entwicklungsschritte sind über Git und die Herkunftsnachweise
nachvollziehbar. Laufartefakte werden nicht als Sessionnotizen in die
Projektübersicht kopiert.
