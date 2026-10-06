# Herkunft und Evidenzgrenzen

Diese Übersicht dokumentiert die übernommene Entwicklungsbasis und die Grenzen
historischer Nachweise. Der aktuelle Projektstand steht in der
[Projektdokumentation](projektstand.pdf), die weitere Arbeit im
[Arbeitsplan](../WORKPLAN.md).

## Code und Ressourcen

Ausgangspunkt ist [What Can We Verify?](https://github.com/sebi-gr/What-Can-We-Verify),
Commit [`5df7760459b741ae36bd91af4af89f6e3ecfe18d`](https://github.com/sebi-gr/What-Can-We-Verify/tree/5df7760459b741ae36bd91af4af89f6e3ecfe18d).
Übernommen wurden Fallvorbereitung, Reportgenerierung und P-Extraktion samt Tests,
Prompts, Codebook, Schema und Annotationsvorlage, das historische PoV-Protokoll
sowie Lizenz und leere Umgebungsvorlage.

[inherited_baseline.json](../resources/inherited_baseline.json) enthält die
ursprünglichen Dateipfade, Importhashes und begründeten lokalen Anpassungen.
Diese Hashes bezeichnen den Importstand, nicht die heute weiterentwickelten
Ressourcen. Der alte P-Antwortvertrag ist nur noch in Git erhalten; Profil 0.1
wird heute von P und D gemeinsam verwendet. Die Import- und Entwicklungshistorie
bleibt über Git nachvollziehbar.

## Archivierte Originale

Genau sechs historische Dateien sind unter `data/` versioniert:

- Report, Request, Rohantwort, ursprünglicher Prompt und Manifest in
  `data/runs/VUL4J-18-review-001/`;
- angenommene manuelle Revision in
  `data/annotations/VUL4J-18-review-001/manual_annotation_001.md`.

[inherited_artifacts.json](../resources/inherited_artifacts.json) dokumentiert
Herkunft und Hashes, einschließlich der Wiederherstellung der ursprünglichen
Prompt-CRLF-Zeilenumbrüche aus dem gespeicherten Request. `.gitattributes` erhält
diese Bytes plattformübergreifend. Die Dateien werden nicht an heutige
Anbieter-, Prompt- oder Ressourcenbezeichnungen angepasst.

Der historische Report enthält ein Finding. Die angenommene Annotation umfasst
13 Claims, 15 Originalzitate und Kontextbezüge. Sie wurde von SG mit
Codex-Unterstützung und Vorwissen über Code, Fix und PoV erstellt. Sie ist ein
Entwicklungsbeispiel, keine unabhängige Wahrheitsreferenz.

## Fehlende historische Nachweise

Die Annotation nennt ein damaliges Codebook v0.2, eine ursprüngliche Abgabe und
ein separates Review. Diese Originale wurden nicht übernommen; das heutige
Codebook ersetzt sie nicht. Auch die Rohdaten früherer Decomposition-Läufe und
Java-/PoV-Logs liegen hier nicht vor. Zusammenfassungen im
[historischen Handoff](https://github.com/sebi-gr/What-Can-We-Verify/blob/5df7760459b741ae36bd91af4af89f6e3ecfe18d/HANDOFF.md)
sind deshalb keine neu geprüften Ergebnisse.

Das unveränderte [PoV-Protokoll](../resources/reproduce_vul4j18.md) beschreibt
frühere Windows-Tests an verwundbarer und reparierter JSPWiki-Version. Geprüft
wurde laut Protokoll Mock-Forwarding; daraus folgt weder beliebiger Dateizugriff
noch die Wahrheit sämtlicher Claims. In diesem Repository wurde kein neuer
Java-Build oder PoV ausgeführt. Ein neuer Lauf wäre neue Evidenz.

## Quellen und Entwicklungsfälle

`01_prepare_case.py` rekonstruiert den begrenzten JSPWiki-Codekontext und getrennte
Referenzen aus fixierten Quellen. Ein Export ist kein vollständiges ausführbares
Repository. Zentrale Revisionen:

| Quelle | Revision |
|---|---|
| Vul4J-Dataset | `376411da11fa705019f731404de1d0679fe73537` |
| VUL4J-18-Benchmark | `07ad7850a041876befb99847053e4b5e181597a5` |
| JSPWiki-Fix | `88d89d6523802c044cfcb7930cba40d8eeb21da2` |

Die [Profilentwicklung](../resources/profile_development/README.md) ergänzt
Jackson XML (VUL4J-47) und Commons Configuration (VUL4J-9). Originalbytes,
Revisionen, Lizenzen und Zeilenbezüge stehen in
[sources.json](../resources/profile_development/sources.json). Beispiele und
Referenzentwürfe sind KI-gestützte redaktionelle Entwicklungsarbeit; sie werden
nicht an die Generierungsmodelle gesendet und ersetzen keine menschliche
Pilotannotation. Alle Entwicklungsprojekte bleiben vom Holdout ausgeschlossen.

Die neuen Pilotquellen und ihre Varianten sind separat im
[Fallkatalog](../resources/pilot_cases.json) dokumentiert. Herkunft, Lizenz und
Anpassungen der VeriScore-basierten Baseline stehen unter
[resources/baselines](../resources/baselines/README.md).

## Lizenzen und Archivierung

Projektcode: [MIT](../LICENSE), Copyright 2026 Sebastian Grünewald.
JSPWiki und die Entwicklungsquellen behalten ihre Upstream-Lizenzen und Notices;
das Vul4J-Dataset steht unter CC BY 4.0. Der gespeicherte historische Request
enthält öffentlichen JSPWiki-Code mit dessen Lizenzkommentaren. Weitere
Lizenzdateien werden bei der Vorbereitung mitgeladen.

Die ursprüngliche Projektskizze bleibt unverändert. Die aktualisierte LaTeX/PDF-
Fassung setzt den Plan neu und übernimmt den Layout-Attributionshinweis der
Skizze. Die GPTAid-DOI-Korrektur ist in [RELATED_WORK.md](RELATED_WORK.md) belegt.

Die sechs historischen Originale sind die einzigen Archiv-Ausnahmen unter `data/`.
Generierte Pilotdaten und Zugangsdaten bleiben ignoriert. Eine spätere Freigabe
von Forschungsdaten benötigt eine eigene Auswahl mit Herkunft und Lizenzen.
