# WORKPLAN — Prose or Structure?

Stand: 2026-10-05. Grundlage: [Projektskizze v0.1](prose_or_structure_projektskizze.pdf) vom 03.10.2026 und der überprüfte Import aus „What Can We Verify?“. Die Skizze ist ein Studienvorschlag; Umfang, Modell und Hauptstichprobe sind noch nicht beschlossen. Dieser Plan ersetzt den alten Verifikationsplan für dieses Repository.

## Ziel und aktueller Einstieg

Untersucht wird, wie **P: Code → Report → Claims** und **D: Code → Claims** sich bei identischem Quellkontext und gemeinsamem Claimprofil unterscheiden. RQ1 entwickelt das Profil, RQ2 vergleicht Qualität und Aufwand, RQ3 untersucht Darstellungsfehler und die Wirkung expliziter Kontextfelder. Eine Überlegenheit von D ist keine Annahme.

**Nächster Arbeitsschritt: Schritt 3.** P-Extraktor und Validierung auf das
[gemeinsame Profil 0.1](resources/claim_profile.md) umstellen und den kleinen
D-Schritt ergänzen. Dafür zuerst den archivierten Report nutzen; keinen neuen
Report erzeugen. Schritt 2 ist als Entwicklungs-PoC abgeschlossen, keine
abgeschlossene Validierung von RQ1 oder unabhängige menschliche Referenzstudie.

## Meilensteine und Abschlusskriterien

| Schritt | Status | Fertig, wenn |
|---|---|---|
| 0. Repository und geerbte Basis | Erledigt; neuer Import geprüft | Aktueller Stand mit drei Skripten übernommen, 29/29 Offline-Tests bestanden; Herkunft/Hashes, Dokumentation und CI vorhanden. |
| 1. Minimales Entwicklungspaket sichern | Erledigt | Sechs ausgewählte Report-/Annotationsdateien archiviert und auf Hashes, Originaltext und Zuordnung geprüft; rekonstruierbare Daten lokal belassen, zusätzliche historische Logs optional. |
| 2. Claimprofil und Annotation v0.1 (RQ1) | Erledigt als Entwicklungs-PoC | Gemeinsames Profil, Codebook, Grenzfälle und getrennte Referenzregeln an JSPWiki und wenigen weiteren Entwicklungsfällen erprobt. |
| 3. Gepaarte P/D-Erzeugung implementieren | P-Extraktor/Validierung vorhanden; D offen | Bestehende P-Komponenten auf das gemeinsame Profil angepasst und um D ergänzt; gespeicherte Originale, Kontexttrennung und gleiches Zielprofil funktionieren. |
| 4. Pilot vorbereiten und ausführen | Geplant | Protokoll vorab fixiert, beide Routen auf denselben 5–10 Fällen, Fehler und Annotationszeit vollständig erfasst; Vergleichbarkeit bewertet. |
| 5. Hauptstudie planen und einfrieren | Nach Pilot | Fallzahl, zurückgehaltene Fälle, Baselines, Budgetkontrolle, Ablation, Annotation und Auswertung begründet festgelegt; engste Vorarbeiten geprüft. |
| 6. Hauptstudie und Paper | Später | Gepaarte Ergebnisse, Unsicherheit, Fehleranalyse, Limitationen und reproduzierbare Forschungsartefakte vorhanden. |

Kein zusätzlicher Live-Review oder erneuter Java-Build ist Teil der Übernahme. Der vorhandene Code implementiert Fallvorbereitung, Reportgenerierung und P-Extraktion mit Format-/Zitat-/Referenzprüfung. Das gemeinsame P/D-Profil ist spezifiziert; seine Anbindung, D und Vergleichsauswertung fehlen noch. Der neue Quellstand verwendet direkt OpenAI statt OpenRouter; Modell und Studienbudget bleiben offen.

## 1. Vorarbeit als nachvollziehbare Entwicklungsbasis

- **Erledigt:** Run `0721c0a0-bba7-48c1-a63c-da196a69d97c` mit einem Finding, Request, Rohantwort, ursprünglichem Prompt und Manifest unter `data/runs/VUL4J-18-review-001/` archiviert. Hashes, Parameter, Provider-Metadaten und exakter Finding-Text stimmen überein.
- **Erledigt:** Die angenommene manuelle Revision unter `data/annotations/VUL4J-18-review-001/manual_annotation_001.md` ist vorhanden. Finding-Hash, eingebetteter Originaltext, 13 eindeutige Claim-IDs, 15 Originalzitate und Kontextverweise geprüft. Annotator SG mit Codex-Unterstützung und Vorwissen über Code/Fix/PoV; Entwicklungsbeispiel, keine unabhängige Wahrheitsreferenz.
- **Rekonstruierbar:** Die fünf Modelldateien sind lokal aus fixierten Quellen vorhanden, ihre Hashes und der vollständig rekonstruierte Requesttext passen zum historischen Lauf. Keine Übernahme kompletter Java-Checkouts, Toolchains oder Caches erforderlich. Ein Java-Neulauf wäre ein eigener, noch nicht ausgeführter Schritt.
- **Optionales historisches Zusatzmaterial:** automatische Decomposition-Läufe 001–003 und PoV-Logs. Deren alte Zusammenfassungen sind nicht neu anhand der Rohdaten geprüft. Für das Claimprofil und neue Experimente sind sie keine Voraussetzung; neue Läufe ersetzen keine historische Evidenz.
- **Begrenzte Revisionshistorie:** Die Annotation nennt ein damaliges Codebook v0.2, eine Originalabgabe und ein separates Review. Diese zusätzlichen Originale wurden nicht geliefert. Die angenommene Revision genügt für den nächsten Entwicklungsschritt; heutiges Codebook nicht als damaligen Snapshot ausgeben.
- Herkunft, Hashes und die Wiederherstellung der Prompt-CRLF-Zeilenumbrüche stehen in [docs/PROVENANCE.md](docs/PROVENANCE.md) und `resources/inherited_artifacts.json`. Archivierte Originale und spätere Revisionen getrennt halten.

## 2. Gemeinsames Claimprofil und Referenzen (RQ1)

**Ergebnis vom 05.10.2026:**

- [Profil 0.1](resources/claim_profile.md) und [JSON-Schema](resources/claim_profile.schema.json): gemeinsame Aussagefelder, sechs einfache Kontexttexte, P-Zitate/D-Leerliste, Codebezüge, lokale Kontext-IDs und getrennte Prüfaufgabe mit benötigter Evidenz/Zusatzannahmen.
- [Codebook](resources/claim_codebook.md): keine Zielclaimzahl; Bedingungen, Aussagekraft und Alternativen erhalten; nicht erwähnt, explizit verneint und ausdrücklich unbekannt unterscheiden. Kategorien bleiben vorläufig.
- [Annotationsprotokoll](resources/annotation_protocol.md) und [Arbeitsblatt](resources/manual_annotation_template.md): Reportreferenz und Codereferenz getrennt; semantische Mehrfachzuordnung, begrenzte Coverage-Einheiten, offene Fragen, Unsicherheit und Prüfbarkeit sowie unabhängige Doppelannotation/Adjudikation geregelt.
- [Entwicklungsdurchgang](resources/profile_development/README.md): JSPWiki/VUL4J-18 mit den 13 historischen Claims sowie VUL4J-47 (Jackson XML) und VUL4J-9 (YAML-Laden). Zehn ausgewählte Profilclaims in vier JSON-Beispielen, getrennte Referenzinventare, Grenzfälle und Quellen mit fixierten Revisionen/Hashes. Zusätzliche Quellen-/Lizenzdateien umfassen nur 19 KB.
- CAE/SACM, DecompScore, VeriScore und DnDScore gezielt als Primärquellen geprüft; Begründung und Übertragungsgrenzen im Profil. Keine vollständige Literaturübersicht oder SACM-Implementierung.

Festgelegte Details: `null` = nicht angegeben, explizite Negation/Unbekanntheit als
Text; P-Zitate exakt mit einsbasiertem Vorkommen, Offsets später lokal wie bisher;
Codebezüge nach jeweiligem Input erhalten, inhaltlich falsche Positionen beider
Routen separat bewerten. ID-Scope ist die einzelne Ausgabe, dauerhafte Zuordnung
über Run-ID. Vorhandene Evidenz und Wahrheitsurteile stehen ausschließlich in der
separaten Annotation. JSON-Schema plus wenige lokale Prüfungen genügen in Schritt 3.

Die neuen Beispiele sind KI-gestützte redaktionelle Entwicklungsarbeit, keine
neuen menschlichen Annotationen, Modellläufe oder PoV-Reproduktionen. Die historische
Annotation bleibt unverändert. Alle drei Fälle samt Varianten gehören fortan zur
Entwicklung, nicht zur zurückgehaltenen Evaluation. Realbeispiele/Referenzen stehen
außerhalb des an Modelle gesendeten Codebooks. Die allgemeine Codebook-Präzisierung
ist schon aktiv; der ausführbare P-Antwortvertrag bleibt bis Schritt 3 bei Version 1.

Validierung: vier Beispiele gegen Draft-2020-12-Schema geprüft, negative
Formatbeispiele abgelehnt; Zitate, lokale IDs, Zeilen/Hashes und originale
Archivbytes geprüft. Die 29 Offline-Regressionstests bleiben erfolgreich.
Die Taxonomie und Annotationszeit werden erst im Pilot empirisch geprüft;
zweite menschliche Annotation und Übereinstimmung sind weiterhin offen.

## 3. Kleinster vollständiger P/D-Versuch

Vorhandenen Reportgenerator weiterverwenden. Zuerst einen bereits gespeicherten Report für P extrahieren; dafür keinen neuen Report erzeugen. D erhält exakt das Quellpaket des zugehörigen P-Reports, ohne Referenzwissen. Alte PoC-Ausgaben dienen der Entwicklung und sind keine nachträglich kontrollierte Vergleichsstudie.

Den vorhandenen P-Extraktor (`src/03_decompose_findings.py`) und seine Validierung auf das vereinbarte gemeinsame Profil anpassen; D als kleinen Schritt ergänzen. Gleiche Felder und Definitionen für beide Routen, routenspezifische Herkunftsfelder zulassen. Keine Wahrheitslabels vom Generator als Referenzbewertung verwenden.

Je Lauf Route/Stufe, Fall/Variante, Run- und Parent-IDs, Schema-/Codebook-/Promptversion, Code-/Inputhashes, Modell/Provider, gesetzte Parameter, Rohantwort, Status, Laufzeit und verfügbare Token-/Kostenangaben speichern. Claim-IDs, Zitatbezüge und Beziehungen prüfen. Eine gültige Codeposition oder ein exaktes Zitat ist kein Wahrheitsnachweis.

Bereits getestete P-Eigenschaften: keine Quell-/Referenzbytes oder Nachbarfindings im Request, unveränderte Originalantworten, exakte Zitate/Offsets und Kontext-IDs, keine Teilclaims bei Fehlern. Für die nächste Implementierung insbesondere identische Quellbytes für P/D und das gemeinsame Profil prüfen. Leere Ergebnisse, Formatfehler und Requestfehler weiter trennen. Reparaturregel vor Versuchen festlegen; Generator und Decomposer haben keine automatische Reparatur oder Wiederholung.

Die bestehende Fall-ID und Dateiliste sind hart auf VUL4J-18 begrenzt. Erst für den nächsten konkreten Fall einen expliziten Fallkontext ergänzen; kein allgemeines Benchmark-Framework vorab bauen.

## 4. Pilotprotokoll (RQ2/RQ3)

Vorgeschlagen sind **5–10 gepaarte Codefälle** aus zunächst **2–3 Schwachstellenklassen**. Auswahl, genaue Zahl und Wiederholungen vor den Läufen festlegen. JSPWiki bleibt Entwicklung; unabhängige Evaluationsfälle früh zurückhalten. Verwundbare/gefixte Varianten und eng verwandte Fälle gemeinsam einem Split zuordnen.

Vor dem Pilot dokumentieren:

- Ein-/Ausschlusskriterien, reproduzierbare Revisionen, Quellpakete, Fall-/Varianten-IDs und Grenzen jedes Kontexts.
- Modellversion soweit verfügbar, Provider, Prompts, Formatvorgaben, Reasoning, Tokenbudget, Wiederholungen, Laufreihenfolge und Ausfall-/Reparaturregeln. Der geerbte direkte OpenAI-Aufruf ist die aktuelle Implementierung, keine endgültige Modell-/Budgetauswahl; die frühere `:free`-Beschränkung entfällt.
- P-Extraktionsvergleiche: einfache Satzaufteilung, ein vorhandener allgemeiner Claim-Extraktionsansatz und die codebookgestützte Variante. Den externen Ansatz nach Kompatibilitätsprüfung auswählen, keine Baseline als bereits implementiert ausgeben.
- D als direkte Schema-Prompting-Baseline; zusätzlich D mit einem Überarbeitungsschritt als Budgetkontrolle. Gleich viele Aufrufe garantieren kein gleiches Budget: tatsächliche Tokens, Laufzeit und Kosten über die gesamte Route erfassen.
- Kleine Ablation expliziter Kontextfelder **in beiden Routen**, mit vorab definiertem Teilbestand und unverändertem Bewertungsziel. Folgen für abgeleitete Prüfaufgaben analysieren.
- Annotator(en), Zeitmessung, Blindierung soweit möglich, getrennte Referenzen, semantische Zuordnungsregeln und Umgang mit Uneinigkeit.

Der Pilot prüft Annotationzeit, Fehlerarten, Vergleichbarkeit und technische Durchführbarkeit. Seine Fallzahl ist kein ausreichender Publikationsumfang. P/D vergleicht vollständige Erzeugungswege, isoliert also nicht automatisch den reinen Ausgabeformateffekt.

## 5. Auswertung und Übergang zur Hauptstudie

| Kriterium | Vorgesehene Operationalisierung |
|---|---|
| Fundierung im Code | Belegt / widerlegt / nicht entscheidbar im bereitgestellten Kontext; Unsicherheitskalibrierung separat |
| Relevante Abdeckung | Semantisch erfasste Propositionen eines vorab begrenzten Referenzbestands; Duplikate und triviale Mehrclaims nicht belohnen |
| Bedeutungstreue, nur P | Auslassungen, unbelegte Ergänzungen, Änderungen an Bedingungen, Negation, Akteur, Modalität und Umfang |
| Prüfbarkeit | Eindeutige Entitäten/Scope/Voraussetzungen und Übereinstimmung abgeleiteter Prüfaufgaben |
| Aufwand/Robustheit | Aufrufe, Tokens, Laufzeit, verfügbare Kosten, Formatfehler, Ausfälle, Reparaturen und Annotationzeit |

Gepaarte Unterschiede **pro Codefall** mit Effektgrößen und Konfidenzintervallen auswerten. Claims und Wiederholungen desselben Falls nicht als unabhängige Stichproben behandeln. Verfahren zur Unsicherheitsbestimmung, Aggregation, Nennern bei Null-Ergebnissen und Umgang mit fehlgeschlagenen Routen vor der Hauptstudie festlegen. Annotationsübereinstimmung und Urteile vor/nach Adjudikation getrennt berichten. Nichtsignifikanz ist kein Gleichwertigkeitsnachweis.

Die engsten Vorarbeiten aus Abschnitt 2 und der Literaturliste der Skizze gezielt prüfen: DnDScore, DecompScore, VeriScore, LLMSAN, GPTAid, VERGE und EviGuard. Die fünf Profilquellen sind in Schritt 2 gezielt geprüft; engste Security-Vergleiche, vollständige Literaturabgrenzung und Neuheitsbewertung bleiben offen. Security-Systeme nur bei kompatibler Teilaufgabe als Vergleich einsetzen. Bibliographie, passende Baseline und Abgrenzung vor der Hauptstudie festhalten.

Anhand des Piloten Hauptstichprobe, Präzisions-/Fallzahlbegründung, Zeitplan und Umfang mit der Betreuung abstimmen; zweiten Annotator klären. Danach Schema, Codebook, Prompts, Protokoll und Auswertung einfrieren. Ablage/Archivierung der Forschungsdaten festlegen, damit ein Clone plus freigegebene Daten die Studie nachvollziehbar macht.

## Offen, bevor neue Experimente starten

- Keine offene Datenübernahme als Voraussetzung für die Profilentwicklung; historische Zusatzlogs/Revisionsnotizen bleiben optional.
- Profil 0.1 in Schritt 3 anbinden; Grenzfälle und Annotationsaufwand anschließend im Pilot überprüfen.
- Modell/Provider, Reasoning, Budget, Wiederholungen und Baseline-Implementierungen.
- Zweiter Annotator, Pilotbestand und spätere Hauptstichprobe.

Automatische Verifier, universeller Scanner, Agentenplattform, eigenes Training und eine zweite Veröffentlichung sind kein Arbeitsauftrag dieses Plans. Unabhängige Evidenzverfahren bleiben eine mögliche Anschlussarbeit.
