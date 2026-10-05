# WORKPLAN — Prose or Structure?

Stand: 2026-10-05. Grundlage: [Projektskizze v0.1](prose_or_structure_projektskizze.pdf) vom 03.10.2026 und der überprüfte Import aus „What Can We Verify?“. Die Skizze ist ein Studienvorschlag; Umfang, Modell und Hauptstichprobe sind noch nicht beschlossen. Dieser Plan ersetzt den alten Verifikationsplan für dieses Repository.

## Ziel und aktueller Einstieg

Untersucht wird, wie **P: Code → Report → Claims** und **D: Code → Claims** sich bei identischem Quellkontext und gemeinsamem Claimprofil unterscheiden. RQ1 entwickelt das Profil, RQ2 vergleicht Qualität und Aufwand, RQ3 untersucht Darstellungsfehler und die Wirkung expliziter Kontextfelder. Eine Überlegenheit von D ist keine Annahme.

**Nächster Arbeitsschritt:** Das [Codebook](resources/claim_codebook.md) und [P-Extraktionsschema](resources/claim_response_schema.json) anhand des jetzt archivierten Originalreports und der [manuellen Annotation mit 13 Claims](data/annotations/VUL4J-18-review-001/manual_annotation_001.md) zum gemeinsamen P/D-Claimprofil weiterentwickeln. P-Decomposer und formale Validierung sind vorhanden. Das vereinbarte kleine Übergabepaket ist geprüft; zusätzliche historische Decomposition-/PoV-Rohdaten sind optional, kein Blocker für diesen Schritt.

## Meilensteine und Abschlusskriterien

| Schritt | Status | Fertig, wenn |
|---|---|---|
| 0. Repository und geerbte Basis | Erledigt; neuer Import geprüft | Aktueller Stand mit drei Skripten übernommen, 29/29 Offline-Tests bestanden; Herkunft/Hashes, Dokumentation und CI vorhanden. |
| 1. Minimales Entwicklungspaket sichern | Erledigt | Sechs ausgewählte Report-/Annotationsdateien archiviert und auf Hashes, Originaltext und Zuordnung geprüft; rekonstruierbare Daten lokal belassen, zusätzliche historische Logs optional. |
| 2. Claimprofil und Annotation v0.1 (RQ1) | Als Nächstes | Gemeinsames Profil, Codebook, Grenzfälle und getrennte Referenzregeln an JSPWiki und wenigen weiteren Entwicklungsfällen erprobt. |
| 3. Gepaarte P/D-Erzeugung implementieren | P-Extraktor/Validierung vorhanden; D offen | Bestehende P-Komponenten auf das gemeinsame Profil angepasst und um D ergänzt; gespeicherte Originale, Kontexttrennung und gleiches Zielprofil funktionieren. |
| 4. Pilot vorbereiten und ausführen | Geplant | Protokoll vorab fixiert, beide Routen auf denselben 5–10 Fällen, Fehler und Annotationszeit vollständig erfasst; Vergleichbarkeit bewertet. |
| 5. Hauptstudie planen und einfrieren | Nach Pilot | Fallzahl, zurückgehaltene Fälle, Baselines, Budgetkontrolle, Ablation, Annotation und Auswertung begründet festgelegt; engste Vorarbeiten geprüft. |
| 6. Hauptstudie und Paper | Später | Gepaarte Ergebnisse, Unsicherheit, Fehleranalyse, Limitationen und reproduzierbare Forschungsartefakte vorhanden. |

Kein zusätzlicher Live-Review oder erneuter Java-Build ist Teil der Übernahme. Der vorhandene Code implementiert Fallvorbereitung, Reportgenerierung und P-Extraktion mit Format-/Zitat-/Referenzprüfung. D, das gemeinsame P/D-Profil und Vergleichsauswertung fehlen noch. Der neue Quellstand verwendet direkt OpenAI statt OpenRouter; Modell und Studienbudget bleiben offen.

## 1. Vorarbeit als nachvollziehbare Entwicklungsbasis

- **Erledigt:** Run `0721c0a0-bba7-48c1-a63c-da196a69d97c` mit einem Finding, Request, Rohantwort, ursprünglichem Prompt und Manifest unter `data/runs/VUL4J-18-review-001/` archiviert. Hashes, Parameter, Provider-Metadaten und exakter Finding-Text stimmen überein.
- **Erledigt:** Die angenommene manuelle Revision unter `data/annotations/VUL4J-18-review-001/manual_annotation_001.md` ist vorhanden. Finding-Hash, eingebetteter Originaltext, 13 eindeutige Claim-IDs, 15 Originalzitate und Kontextverweise geprüft. Annotator SG mit Codex-Unterstützung und Vorwissen über Code/Fix/PoV; Entwicklungsbeispiel, keine unabhängige Wahrheitsreferenz.
- **Rekonstruierbar:** Die fünf Modelldateien sind lokal aus fixierten Quellen vorhanden, ihre Hashes und der vollständig rekonstruierte Requesttext passen zum historischen Lauf. Keine Übernahme kompletter Java-Checkouts, Toolchains oder Caches erforderlich. Ein Java-Neulauf wäre ein eigener, noch nicht ausgeführter Schritt.
- **Optionales historisches Zusatzmaterial:** automatische Decomposition-Läufe 001–003 und PoV-Logs. Deren alte Zusammenfassungen sind nicht neu anhand der Rohdaten geprüft. Für das Claimprofil und neue Experimente sind sie keine Voraussetzung; neue Läufe ersetzen keine historische Evidenz.
- **Begrenzte Revisionshistorie:** Die Annotation nennt ein damaliges Codebook v0.2, eine Originalabgabe und ein separates Review. Diese zusätzlichen Originale wurden nicht geliefert. Die angenommene Revision genügt für den nächsten Entwicklungsschritt; heutiges Codebook nicht als damaligen Snapshot ausgeben.
- Herkunft, Hashes und die Wiederherstellung der Prompt-CRLF-Zeilenumbrüche stehen in [docs/PROVENANCE.md](docs/PROVENANCE.md) und `resources/inherited_artifacts.json`. Archivierte Originale und spätere Revisionen getrennt halten.

## 2. Gemeinsames Claimprofil und Referenzen (RQ1)

Ein kleines Profil aus Literatur und manueller Kodierung entwickeln. CAE/SACM dienen laut Skizze als begriffliche Grundlage; keine vollständige SACM-Implementierung und keine Lean-Formalisierung. Folgende Feldgruppen sind Arbeitsanforderungen, noch kein verabschiedetes JSON-Schema:

| Feldgruppe | Zu konkretisieren |
|---|---|
| Aussage | Claim-ID, Proposition, vorläufiger Typ; unabhängig bewertbare Aussagen trennen |
| Bedingungen und Umfang | Akteur/Rechte, Voraussetzungen, Negation, Modalität, Quantoren, betroffene Version/Konfiguration |
| Herkunft und Beziehungen | Codebezüge; Reportfundstelle bei P; ausdrücklich benannte Beziehungen zu anderen Claims |
| Prüfbezug | Benötigte Evidenz/Prüfaufgabe getrennt von Aussage, Annahmen und vorhandenen Belegen |

Das übernommene Codebook verwendet `location`, `data_flow`, `protection_precondition`, `exploitability_impact` sowie `other`/`unclear`. Das ist eine Entwicklungsbasis, keine validierte Taxonomie. Ausnutzbarkeit und Wirkung getrennt erfassen, wenn sie getrennt behauptet werden. Keine Kategorie pro Finding erzwingen. Das bestehende P-Schema bündelt Bedingungen in `qualifiers`; explizite Kontext-/Codebezugs-/Prüfaufgabenfelder für P/D fehlen noch.

Konkrete Entscheidungen vor der Implementierung:

- Fehlende Angaben, explizite Negation und unbekannte Zustände unterscheidbar machen; keinen Akteur, Schutz oder Impact hinzuerfinden.
- P-Zitate auf unveränderte Titel-/Reportfelder beziehen; D braucht keine künstliche Reportfundstelle. Der bestehende Decomposer verwendet exakte Zitate mit einsbasiertem Vorkommen und berechnet nullbasierte Unicode-Codepoint-Offsets mit exklusivem Ende; diese bereits getestete Konvention beibehalten, sofern kein begründeter Änderungsbedarf entsteht.
- Beim P-Extraktor Codebezüge nur aus dem Report übernehmen. Ergänzender Kontext oder abgeleitete Prüfaufgaben dürfen nicht als im Report behauptete Aussage erscheinen.
- Claim-ID-Scope, Referenzen, Einheiten der Annotation, Mehrfachzuordnungen und Umgang mit mehrdeutigen Zitaten festlegen. Semantische Übereinstimmung zählt, nicht Wortlaut oder identische Claimzahl.
- **Reportreferenz für P:** tatsächlich enthaltene Propositionen und Bedingungen, unabhängig von ihrer Wahrheit.
- **Codereferenz für beide Routen:** vorab abgegrenzte relevante Propositionen und offene Fragen, bezogen auf das identische bereitgestellte Codepaket. Erkenntnisse aus zusätzlichem Patch-/PoV-Material getrennt kennzeichnen; sie machen fehlende Evidenz im Modellkontext nicht nachträglich sichtbar.
- Auf einem Teilbestand zwei unabhängig annotierende Personen, möglichst ohne Kenntnis der Route. Einzelurteile vor Adjudikation erhalten. Ein weiteres LLM darf unterstützen, aber nicht allein die Referenz bilden.

Ergebnis dieses Schritts: ein versioniertes Profil, ein Codebook mit echten Entwicklungsbeispielen/Grenzfällen und ein dokumentierter Annotationsablauf. Dateiformat und kleinste notwendige Validierung erst daran festlegen.

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

Die engsten Vorarbeiten aus Abschnitt 2 und der Literaturliste der Skizze gezielt prüfen: DnDScore, DecompScore, VeriScore, LLMSAN, GPTAid, VERGE und EviGuard. Literaturangaben und Neuheitsabgrenzung wurden bei der Repo-Einrichtung nicht neu verifiziert. Security-Systeme nur bei kompatibler Teilaufgabe als Vergleich einsetzen. Bibliographie, passende Baseline und Abgrenzung vor der Hauptstudie festhalten.

Anhand des Piloten Hauptstichprobe, Präzisions-/Fallzahlbegründung, Zeitplan und Umfang mit der Betreuung abstimmen; zweiten Annotator klären. Danach Schema, Codebook, Prompts, Protokoll und Auswertung einfrieren. Ablage/Archivierung der Forschungsdaten festlegen, damit ein Clone plus freigegebene Daten die Studie nachvollziehbar macht.

## Offen, bevor neue Experimente starten

- Keine offene Datenübernahme als Voraussetzung für die Profilentwicklung; historische Zusatzlogs/Revisionsnotizen bleiben optional.
- Profil-/Annotationsdetails und Auswahl zusätzlicher Entwicklungsfälle.
- Modell/Provider, Reasoning, Budget, Wiederholungen und Baseline-Implementierungen.
- Zweiter Annotator, Pilotbestand und spätere Hauptstichprobe.

Automatische Verifier, universeller Scanner, Agentenplattform, eigenes Training und eine zweite Veröffentlichung sind kein Arbeitsauftrag dieses Plans. Unabhängige Evidenzverfahren bleiben eine mögliche Anschlussarbeit.
