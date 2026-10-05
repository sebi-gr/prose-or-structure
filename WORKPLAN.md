# WORKPLAN — Prose or Structure?

Stand: 2026-10-05. Grundlage: [Projektskizze v0.1](prose_or_structure_projektskizze.pdf) vom 03.10.2026 und der überprüfte Import aus „What Can We Verify?“. Die Skizze ist ein Studienvorschlag; Umfang, Modell und Hauptstichprobe sind noch nicht beschlossen. Dieser Plan ersetzt den alten Verifikationsplan für dieses Repository.

## Ziel und aktueller Einstieg

Untersucht wird, wie **P: Code → Report → Claims** und **D: Code → Claims** sich bei identischem Quellkontext und gemeinsamem Claimprofil unterscheiden. RQ1 entwickelt das Profil, RQ2 vergleicht Qualität und Aufwand, RQ3 untersucht Darstellungsfehler und die Wirkung expliziter Kontextfelder. Eine Überlegenheit von D ist keine Annahme.

**Nächster Arbeitsschritt:** Die Originalartefakte des JSPWiki-Entwicklungsfalls sichern und daraus Claimprofil und Annotationsregeln v0.1 präzisieren. Die Suche und die fehlenden Dateien stehen in [docs/PROVENANCE.md](docs/PROVENANCE.md). Am Profil kann anhand der Skizze gearbeitet werden; die historische Zerlegung in 13 Claims darf ohne Originale nicht als überprüft oder importiert gelten.

## Meilensteine und Abschlusskriterien

| Schritt | Status | Fertig, wenn |
|---|---|---|
| 0. Repository und geerbte Basis | Erledigt | Importherkunft/Hashes festgehalten, 15/15 Tests und frischer Fallexport geprüft; Dokumentation und CI für den neuen Fokus eingerichtet. |
| 1. Entwicklungsartefakte sichern | Offen; Originale fehlen | Report samt Run-Artefakten, 13 Claims, ursprüngliches Codebook und PoV-Evidenz auffindbar, unverändert übernommen und ihrer Herkunft zugeordnet; verbleibende Lücken explizit entschieden. |
| 2. Claimprofil und Annotation v0.1 (RQ1) | Als Nächstes | Gemeinsames Profil, Codebook, Grenzfälle und getrennte Referenzregeln an JSPWiki und wenigen weiteren Entwicklungsfällen erprobt. |
| 3. Gepaarte P/D-Erzeugung implementieren | Geplant | P-Extraktor, D-Generator und gemeinsame formale Validierung mit gespeicherten Originalen, Kontexttrennung und gleichem Zielprofil funktionieren. |
| 4. Pilot vorbereiten und ausführen | Geplant | Protokoll vorab fixiert, beide Routen auf denselben 5–10 Fällen, Fehler und Annotationszeit vollständig erfasst; Vergleichbarkeit bewertet. |
| 5. Hauptstudie planen und einfrieren | Nach Pilot | Fallzahl, zurückgehaltene Fälle, Baselines, Budgetkontrolle, Ablation, Annotation und Auswertung begründet festgelegt; engste Vorarbeiten geprüft. |
| 6. Hauptstudie und Paper | Später | Gepaarte Ergebnisse, Unsicherheit, Fehleranalyse, Limitationen und reproduzierbare Forschungsartefakte vorhanden. |

Kein zusätzlicher Live-Review oder erneuter Java-Build ist Teil der Repository-Einrichtung. Der vorhandene Code implementiert Fallvorbereitung und den Reportteil von P. D, P-Extraktion und Vergleichsauswertung existieren noch nicht.

## 1. Vorarbeit als nachvollziehbare Entwicklungsbasis

- Den historischen Run mit ID `0721c0a0-bba7-48c1-a63c-da196a69d97c` samt Request, Prompt, Quellen, Rohantwort, Findings und Manifest wiederfinden. Laut Quelldokumentation enthält er ein Finding; das ist hier nicht anhand der Rohdaten nachgeprüft.
- Die 13 manuellen Claims und das erste Codebook aus der Skizze im Original sichern. Nicht mit dem älteren Schemaentwurf im alten WORKPLAN verwechseln.
- PoV-Logs, Befehlsmetadaten, Prüfsummen und Ergebnisdatei zum historischen Windows-Lauf übernehmen, soweit verfügbar. Das importierte Protokoll belegt zunächst die dokumentierte Durchführung, keine erneute lokale Prüfung.
- Bei Wiederfund Hashes und Zuordnung zwischen Report, Claims, Codebook und Fall erfassen. Unveränderte Originale und spätere Korrekturen separat speichern.
- Falls Originale nicht beschaffbar sind, den Verlust dokumentieren und einen neuen Entwicklungsdurchlauf ausdrücklich als solchen planen. Historische Daten niemals durch neu generierte Antworten ersetzen.

## 2. Gemeinsames Claimprofil und Referenzen (RQ1)

Ein kleines Profil aus Literatur und manueller Kodierung entwickeln. CAE/SACM dienen laut Skizze als begriffliche Grundlage; keine vollständige SACM-Implementierung und keine Lean-Formalisierung. Folgende Feldgruppen sind Arbeitsanforderungen, noch kein verabschiedetes JSON-Schema:

| Feldgruppe | Zu konkretisieren |
|---|---|
| Aussage | Claim-ID, Proposition, vorläufiger Typ; unabhängig bewertbare Aussagen trennen |
| Bedingungen und Umfang | Akteur/Rechte, Voraussetzungen, Negation, Modalität, Quantoren, betroffene Version/Konfiguration |
| Herkunft und Beziehungen | Codebezüge; Reportfundstelle bei P; ausdrücklich benannte Beziehungen zu anderen Claims |
| Prüfbezug | Benötigte Evidenz/Prüfaufgabe getrennt von Aussage, Annahmen und vorhandenen Belegen |

Der ältere Plan schlägt `location`, `data_flow`, `protection_precondition`, `exploitability_impact` sowie `other`/`unclear` vor. Das ist eine zu überprüfende Ausgangshypothese, keine validierte Taxonomie. Ausnutzbarkeit und Wirkung getrennt erfassen, wenn sie getrennt behauptet werden. Keine Kategorie pro Finding erzwingen.

Konkrete Entscheidungen vor der Implementierung:

- Fehlende Angaben, explizite Negation und unbekannte Zustände unterscheidbar machen; keinen Akteur, Schutz oder Impact hinzuerfinden.
- P-Zitate auf unveränderte Titel-/Reportfelder beziehen; D braucht keine künstliche Reportfundstelle. Als Offset-Konvention nullbasierte Unicode-Codepoints mit exklusivem Ende prüfen und dann festlegen.
- Beim P-Extraktor Codebezüge nur aus dem Report übernehmen. Ergänzender Kontext oder abgeleitete Prüfaufgaben dürfen nicht als im Report behauptete Aussage erscheinen.
- Claim-ID-Scope, Referenzen, Einheiten der Annotation, Mehrfachzuordnungen und Umgang mit mehrdeutigen Zitaten festlegen. Semantische Übereinstimmung zählt, nicht Wortlaut oder identische Claimzahl.
- **Reportreferenz für P:** tatsächlich enthaltene Propositionen und Bedingungen, unabhängig von ihrer Wahrheit.
- **Codereferenz für beide Routen:** vorab abgegrenzte relevante Propositionen und offene Fragen, bezogen auf das identische bereitgestellte Codepaket. Erkenntnisse aus zusätzlichem Patch-/PoV-Material getrennt kennzeichnen; sie machen fehlende Evidenz im Modellkontext nicht nachträglich sichtbar.
- Auf einem Teilbestand zwei unabhängig annotierende Personen, möglichst ohne Kenntnis der Route. Einzelurteile vor Adjudikation erhalten. Ein weiteres LLM darf unterstützen, aber nicht allein die Referenz bilden.

Ergebnis dieses Schritts: ein versioniertes Profil, ein Codebook mit echten Entwicklungsbeispielen/Grenzfällen und ein dokumentierter Annotationsablauf. Dateiformat und kleinste notwendige Validierung erst daran festlegen.

## 3. Kleinster vollständiger P/D-Versuch

Vorhandenen Reportgenerator weiterverwenden. Zuerst einen bereits gespeicherten Report für P extrahieren; dafür keinen neuen Report erzeugen. D erhält exakt das Quellpaket des zugehörigen P-Reports, ohne Referenzwissen. Alte PoC-Ausgaben dienen der Entwicklung und sind keine nachträglich kontrollierte Vergleichsstudie.

P-Extraktor, D-Erzeugung und Validierung als kleine nachvollziehbare Schritte ergänzen. Gleiche Felder und Definitionen für beide Routen, routenspezifische Herkunftsfelder zulassen. Keine Wahrheitslabels vom Generator als Referenzbewertung verwenden.

Je Lauf Route/Stufe, Fall/Variante, Run- und Parent-IDs, Schema-/Codebook-/Promptversion, Code-/Inputhashes, Modell/Provider, gesetzte Parameter, Rohantwort, Status, Laufzeit und verfügbare Token-/Kostenangaben speichern. Claim-IDs, Zitatbezüge und Beziehungen prüfen. Eine gültige Codeposition oder ein exaktes Zitat ist kein Wahrheitsnachweis.

Konkrete Tests für diese nächste Implementierung: identische Quellbytes für P/D, keine Quell-/Referenzbytes im P-Extraktorrequest, unveränderte Originalantworten, gültige Herkunftsbezüge sowie getrennte Behandlung leerer Ergebnisse, Formatfehler und Requestfehler. Reparaturregel vor Versuchen festlegen; der geerbte Generator hat keine automatische Reparatur oder Wiederholung.

Die bestehende Fall-ID und Dateiliste sind hart auf VUL4J-18 begrenzt. Erst für den nächsten konkreten Fall einen expliziten Fallkontext ergänzen; kein allgemeines Benchmark-Framework vorab bauen.

## 4. Pilotprotokoll (RQ2/RQ3)

Vorgeschlagen sind **5–10 gepaarte Codefälle** aus zunächst **2–3 Schwachstellenklassen**. Auswahl, genaue Zahl und Wiederholungen vor den Läufen festlegen. JSPWiki bleibt Entwicklung; unabhängige Evaluationsfälle früh zurückhalten. Verwundbare/gefixte Varianten und eng verwandte Fälle gemeinsam einem Split zuordnen.

Vor dem Pilot dokumentieren:

- Ein-/Ausschlusskriterien, reproduzierbare Revisionen, Quellpakete, Fall-/Varianten-IDs und Grenzen jedes Kontexts.
- Modellversion soweit verfügbar, Provider, Prompts, Formatvorgaben, Reasoning, Tokenbudget, Wiederholungen, Laufreihenfolge und Ausfall-/Reparaturregeln. Der geerbte `:free`-Aufruf ist eine technische Einschränkung, keine endgültige Versuchsauswahl.
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

- Ablage der historischen Report-, Claim-, Codebook- und PoV-Originale.
- Profil-/Annotationsdetails und Auswahl zusätzlicher Entwicklungsfälle.
- Modell/Provider, Reasoning, Budget, Wiederholungen und Baseline-Implementierungen.
- Zweiter Annotator, Pilotbestand und spätere Hauptstichprobe.

Automatische Verifier, universeller Scanner, Agentenplattform, eigenes Training und eine zweite Veröffentlichung sind kein Arbeitsauftrag dieses Plans. Unabhängige Evidenzverfahren bleiben eine mögliche Anschlussarbeit.
