# WORKPLAN — Prose or Structure?

Stand: 2026-10-05. Grundlage: [Projektskizze v0.1](prose_or_structure_projektskizze.pdf) vom 03.10.2026 und der überprüfte Import aus „What Can We Verify?“. Die Skizze ist ein Studienvorschlag; Umfang, Modell und Hauptstichprobe sind noch nicht beschlossen. Dieser Plan ersetzt den alten Verifikationsplan für dieses Repository.

## Ziel und aktueller Einstieg

Untersucht wird, wie **P: Code → Report → Claims** und **D: Code → Claims** sich bei identischem Quellkontext und gemeinsamem Claimprofil unterscheiden. RQ1 entwickelt das Profil, RQ2 vergleicht Qualität und Aufwand, RQ3 untersucht Darstellungsfehler und die Wirkung expliziter Kontextfelder. Eine Überlegenheit von D ist keine Annahme.

**Nächster Arbeitsschritt: Schritt 4, Pilotprotokoll.** Gemeinsames Profil und
gepaarte P/D-Erzeugung sind für den VUL4J-18-PoC implementiert und offline geprüft.
Vor Live-Läufen Modell/Budget, Fallbestand, vollständige P-Reporteinhaltseinheit,
Referenzen und Fehlerregeln fixieren. Keine Vergleichsergebnisse vorwegnehmen.

## Meilensteine und Abschlusskriterien

| Schritt | Status | Fertig, wenn |
|---|---|---|
| 0. Repository und geerbte Basis | Erledigt; neuer Import geprüft | Aktueller Stand mit drei Skripten übernommen, 29/29 Offline-Tests bestanden; Herkunft/Hashes, Dokumentation und CI vorhanden. |
| 1. Minimales Entwicklungspaket sichern | Erledigt | Sechs ausgewählte Report-/Annotationsdateien archiviert und auf Hashes, Originaltext und Zuordnung geprüft; rekonstruierbare Daten lokal belassen, zusätzliche historische Logs optional. |
| 2. Claimprofil und Annotation v0.1 (RQ1) | Erledigt als Entwicklungs-PoC | Gemeinsames Profil, Codebook, Grenzfälle und getrennte Referenzregeln an JSPWiki und wenigen weiteren Entwicklungsfällen erprobt. |
| 3. Gepaarte P/D-Erzeugung implementieren | Erledigt für den VUL4J-18-PoC, offline geprüft | Bestehende P-Komponenten auf das gemeinsame Profil angepasst und um D ergänzt; gespeicherte Originale, Kontexttrennung und gleiches Zielprofil funktionieren. |
| 4. Pilot vorbereiten und ausführen | Geplant | Protokoll vorab fixiert, beide Routen auf denselben 5–10 Fällen, Fehler und Annotationszeit vollständig erfasst; Vergleichbarkeit bewertet. |
| 5. Hauptstudie planen und einfrieren | Nach Pilot | Fallzahl, zurückgehaltene Fälle, Baselines, Budgetkontrolle, Ablation, Annotation und Auswertung begründet festgelegt; engste Vorarbeiten geprüft. |
| 6. Hauptstudie und Paper | Später | Gepaarte Ergebnisse, Unsicherheit, Fehleranalyse, Limitationen und reproduzierbare Forschungsartefakte vorhanden. |

Kein zusätzlicher Live-Review oder erneuter Java-Build ist Teil der Übernahme. Der vorhandene Code implementiert Fallvorbereitung, Reportgenerierung und P-Extraktion mit Format-/Zitat-/Referenzprüfung. Das gemeinsame P/D-Profil und D sind jetzt angebunden; Vergleichsauswertung und Pilot stehen aus. Der neue Quellstand verwendet direkt OpenAI statt OpenRouter; Modell und Studienbudget bleiben offen.

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
war bereits aktiv; der alte P-Antwortvertrag wurde anschließend in Schritt 3 ersetzt.

Validierung: vier Beispiele gegen Draft-2020-12-Schema geprüft, negative
Formatbeispiele abgelehnt; Zitate, lokale IDs, Zeilen/Hashes und originale
Archivbytes geprüft. Die 29 Offline-Regressionstests bleiben erfolgreich.
Die Taxonomie und Annotationszeit werden erst im Pilot empirisch geprüft;
zweite menschliche Annotation und Übereinstimmung sind weiterhin offen.

## 3. Kleinster vollständiger P/D-Versuch

**Ergebnis:** Bestehenden Reportgenerator beibehalten, P auf Profil 0.1 umgestellt
und `04_generate_claims.py` für D ergänzt. `claim_profile.py` ist der gemeinsame
kleine Validator; kein allgemeines Framework und keine neue Abhängigkeit.
Der alte aktive P-Antwortvertrag ist entfernt, historische Artefakte bleiben erhalten.

- P verwendet ein ausgewähltes gespeichertes Finding, prüft dessen Herkunft anhand des ursprünglichen Reviews und sendet nur Titel/Report plus generische Anweisungen.
- D prüft mit `review_pair.py` die Originalartefakte, alle fünf Quellhashes und den tatsächlich gesendeten nummerierten Codekontext des Reviews vor dem Request. Referenzmaterial und Reportinhalte fehlen in seinem Request.
- Laufmetadaten speichern Fall/Variante, Route/Stufe, Run-/Parent-/Paar-ID, Versionen/Hashes, Modell/Parameter, Originale, Laufzeit und Usage. Unbekannte Variantendaten bleiben `unspecified`, Kosten ohne Abrechnung `null`.
- Beide Routen prüfen dasselbe Profil, eindeutige IDs und Kontextbezüge; P löst exakte Zitate/Unicode-Offsets auf. D protokolliert Codepositionen als nichtfatale Diagnosen; falsche Positionen bleiben zur Inhaltsbewertung erhalten. Keine generierten Wahrheitslabels.
- Leere Claims, Formatfehler und technische Fehler getrennt; keine Teilclaims, automatische Reparatur, Retry oder Überschreibung vorhandener Läufe.
- 60 Offline-Tests einschließlich durchgängiger synthetischer P/D-Paarung sowie ein Smoke-Test mit archiviertem Report, realem JSPWiki-Code und ausdrücklich ersetzten Modellantworten bestanden. Kein echter API-Aufruf oder neuer Java-/PoV-Lauf.

**Umfangsgrenze:** P extrahiert weiterhin pro Finding. Der archivierte Review hat
eines, also entspricht der PoC P mit zwei Aufrufen und D mit einem. Bei N Findings
wären es für P 1 + N; alle Findings gehören in die Fallbewertung. Vor dem Pilot
die Reporteinheit für den Zwei-Aufruf-Entwurf festlegen oder den zusätzlichen
Aufwand explizit ins Protokoll aufnehmen. Nicht nachträglich Findings auswählen.
D kann einen leeren erfolgreichen Review als Anker nutzen, einen fehlgeschlagenen
Review noch nicht; Umgang mit fehlenden Routen vorab festlegen.

Fall-ID/Dateiliste bleiben bewusst VUL4J-18-spezifisch. Erst für den nächsten
konkreten Pilotfall erweitern. Historischer OpenRouter-Report plus heutige Routen
sind Entwicklungsmaterial und keine kontrollierte Vergleichsstudie.

## 4. Pilotprotokoll (RQ2/RQ3)

Vorgeschlagen sind **5–10 gepaarte Codefälle** aus zunächst **2–3 Schwachstellenklassen**. Auswahl, genaue Zahl und Wiederholungen vor den Läufen festlegen. JSPWiki bleibt Entwicklung; unabhängige Evaluationsfälle früh zurückhalten. Verwundbare/gefixte Varianten und eng verwandte Fälle gemeinsam einem Split zuordnen.

Vor dem Pilot dokumentieren:

- Ein-/Ausschlusskriterien, reproduzierbare Revisionen, Quellpakete, Fall-/Varianten-IDs und Grenzen jedes Kontexts.
- P-Reporteinheit/Anzahl Extraktionsaufrufe und Verhalten bei leeren/fehlgeschlagenen Reviews; vollständige Fallabdeckung sicherstellen.
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
- Pilotprotokoll samt Reporteinheit, Fehlerregeln und zusätzlichen ausführbaren Fällen festlegen; Grenzfälle/Annotationsaufwand im Pilot prüfen.
- Modell/Provider, Reasoning, Budget, Wiederholungen und Baseline-Implementierungen.
- Zweiter Annotator, Pilotbestand und spätere Hauptstichprobe.

Automatische Verifier, universeller Scanner, Agentenplattform, eigenes Training und eine zweite Veröffentlichung sind kein Arbeitsauftrag dieses Plans. Unabhängige Evidenzverfahren bleiben eine mögliche Anschlussarbeit.
