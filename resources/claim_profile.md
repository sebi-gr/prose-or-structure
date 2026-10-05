# Gemeinsames Claimprofil

**Version 0.1 · 2026-10-05 · Entwicklungsvertrag für Schritt 3.**
Das [Schema](claim_profile.schema.json) beschreibt dieselbe Ausgabe für P und D.
Es ist noch nicht an die Skripte angeschlossen. Der ausführbare P-Extraktor nutzt
weiter `claim_response_schema.json` mit `schema_version: "1"`. Das sind zwei
verschiedene Zwecke, keine alternativ wählbaren Studienformate; Schritt 3 ersetzt
den alten Antwortvertrag. Keine automatische verlustfreie Migration behaupten.

## Einheit und Felder

Eine Datei enthält `profile_version: "0.1"`, `route: "P" | "D"` und `claims`.
Ein Claim ist eine eigenständig beurteilbare Proposition mit erhaltenem Kontext,
nicht automatisch ein Satz, eine Zeile oder ein Schwachstellenlabel. Leere
`claims` sind ein gültiges leeres Ergebnis. Die [Codebook-Regeln](claim_codebook.md)
gelten für beide Routen; nur P hat eine Reporttreue-Anforderung.

| Feld je Claim | Bedeutung |
|---|---|
| `claim_id` | `C01`, `C02`, optional Suffix wie `C09a`; eindeutig innerhalb einer Ausgabe |
| `proposition` | Vollständige Aussage einschließlich Bedingungen, Modalität und Negation |
| `family`, `subtype`, `family_reason` | Vorläufige Codebook-Familie, ggf. Exploitability-/Impact-Untertyp und kurze Begründung |
| `context` | Sechs explizite Aspekte der Aussage; Definition unten |
| `source_quotes` | P: exakte Titel-/Reportzitate; D: immer `[]` |
| `code_refs` | Genannte Codepositionen, keine Wahrheitsbelege; dürfen leer sein |
| `context_claim_ids` | Benötigte andere Claims derselben Ausgabe, keine Beweiskanten |
| `verification` | Abgeleitete Prüfaufgabe, benötigte Evidenz und zusätzliche Annahmen; kein Teil der behaupteten Proposition |

`context` enthält immer alle sechs Schlüssel; Werte sind Text oder `null`:

| Schlüssel | Erhaltene Bedeutung |
|---|---|
| `actor` | Akteur und ausdrücklich genannte Rechte/Authentisierung |
| `preconditions` | Voraussetzungen einschließlich Konfiguration; nicht als erfüllt ausgeben |
| `negation` | Explizite Verneinung mit ihrem Gegenstand und Geltungsbereich |
| `modality` | Möglichkeit, Gewissheitsabstufung oder Einschränkung wie „could“, „potentially“ |
| `quantifier` | Etwa „only“, „all“, „some“, inklusive Bezugsobjekt |
| `scope` | Genannter Ausführungspfad, Version, Konfiguration oder sonstige Begrenzung |

**Drei Zustände ohne zusätzliche Status-Taxonomie:** `null` bedeutet, dass der
Aspekt nicht angegeben ist. Ein explizites „keine Anmeldung erforderlich“ wird
als Text erhalten, ebenso „ob Anmeldung nötig ist, ist unbekannt“. Diese beiden
Angaben sind weder miteinander noch mit `null` identisch. Ein fehlender Schlüssel
ist ein Formatfehler. Eine kategorische Aussage ohne Modalwort erhält
`modality: null`; das macht sie nicht zu einer unsicheren Aussage. Keine
sprachliche Unsicherheit aus einem späteren Bewertungsurteil zurückschreiben.
Auch bei expliziten Kontextfeldern muss die Proposition selbst bedeutungstreu
bleiben. Textfelder statt Rechte-Ontologie oder Logiksprache reichen für den PoC.

## Herkunft und Beziehungen

- P zitiert `title` oder `report` unverändert mit `quote` und einsbasiertem
  `occurrence`. Überlappende Treffer zählen nach Startposition. Die Software
  berechnet später `start`/`end` als nullbasierte Unicode-Codepoints, Ende exklusiv;
  das Modell berechnet keine Offsets. Dieselbe Passage darf mehrere Claims tragen.
  Bei „this value“ auch die den Bezug auflösende Passage zitieren.
- D erhält keine künstlichen Reportzitate. Seine Codebezüge stammen aus dem
  gelieferten Codepaket. P übernimmt sie ausschließlich so, wie der Report sie
  behauptet: falsche Zeilen nicht korrigieren, ungenannte Pfadpräfixe nicht ergänzen.
- Ein Codebezug hat `path`, `line_start`, `line_end`, `symbol`. Nicht genannte
  Werte sind `null`; mindestens Pfad oder Symbol muss bekannt sein. Zeilen sind
  einsbasiert und beidseitig inklusiv, eine einzelne Zeile hat Start = Ende.
  P darf nur `WikiServlet.java` kennen; D verwendet den gelieferten relativen
  vollständigen Pfad. Kein Parser muss aus Symbolnamen eine Fundstelle erfinden.
- `context_claim_ids` verweist ausschließlich auf vorhandene andere lokale IDs.
  Richtung: **dieser Claim benötigt den referenzierten Claim zum Verständnis**.
  Ursache, Bedingung und Alternativen bleiben im Propositionstext; die ID allein
  behauptet keine Kausalität. Keine Selbstbezüge, Duplikate oder externen IDs.
- Stabile Identität außerhalb der Ausgabe ist `(run_id, claim_id)`; bei P
  zusätzlich das zugehörige Finding im Laufmanifest. Referenz-IDs sind separat
  (`R01` für Report, `K01` für Code). Keine Gleichheit nur wegen gleicher Nummer.

## Prüfaufgabe und Evidenz

`verification.question` benennt eine konkrete Frage zum Claim.
`required_evidence` listet, was diese Frage beantworten könnte.
`assumptions` listet zusätzliche, **nicht bestätigte** Arbeitsannahmen; Standard
ist `[]`. Explizite Bedingungen der Originalaussage gehören bereits in
`context.preconditions`, nicht automatisch in diese Zusatzannahmen.

P darf aus dem Report eine Prüfaufgabe ableiten, dabei aber keine neue Codeanalyse
oder angeblich vorhandene Belege hinzufügen. Eine Frage nach der Behandlung im
Ziel-JSP behauptet weder, dass dieser JSP unsicher ist, noch dass er vorliegt.
Zusatzannahmen legitimieren keine durch den jeweiligen Input nicht getragene
Proposition; P darf weiterhin falsche, im Report enthaltene Aussagen extrahieren. Kontext aus
außerhalb des jeweiligen Inputs bleibt im separaten Bewertungsblatt.

Vorhandene Evidenz, `supported`/`contradicted`/`inconclusive`, Reporttreue und
Adjudikation gehören **nicht** in die Generatorausgabe, sondern in die
[Annotation](annotation_protocol.md). Insbesondere ist ein Codebezug kein
Wahrheitsurteil. Kein `confidence`-Score, Verifier, Toolplan oder SACM-Graph nötig.

## Kleinste Validierung in Schritt 3

1. JSON-Schema: Version, Route, exakte Schlüssel, Typen, Familien/Subtypen,
   vollständige Kontextfelder, P-Zitate/D-Leerliste; kein Teilergebnis bei Fehlern.
2. Lokale Semantik: eindeutige IDs, vorhandene Kontextziele, keine Selbstbezüge;
   Zeilenpaare entweder beide `null` oder geordnet; mindestens Pfad oder Symbol.
3. P: Quote/Vorkommen auf dem unveränderten Report auflösen. D: genannte Pfade
   und Zeilen gegen das tatsächlich gelieferte Paket abgleichen. Nicht auflösbare
   Codebezüge separat protokollieren, bei beiden Routen als Inhalt erhalten und
   später bewerten; sie sind kein harter Formatfehler und werden nicht korrigiert.
4. Erwartete Route gegen Laufkonfiguration prüfen; Input- und Ressourcenhashes,
   Run-/Finding-ID und berechnete Offsets separat speichern. Unicode-Konvention
   und bestehende Kontexttrennung weiterverwenden.

Diese Prüfungen beweisen weder Wahrheit noch Abdeckung oder gute Atomizität.
Die [Entwicklungsbeispiele](profile_development/README.md) erproben das Format
an drei Fällen; sie sind keine verblindete Referenz oder Vergleichsmessung.

## Begründung und Reichweite

Die Projektskizze gibt die vier Feldgruppen vor. [CAE](https://www.adelard.com/asce/cae/)
und [SACM 2.2](https://www.omg.org/spec/SACM/2.2) motivieren die Trennung zwischen
Behauptung, Kontext/Annahme und Evidenz; wir implementieren keinen dieser Standards.
[Wanner et al., *SEM 2024](https://aclanthology.org/2024.starsem-1.13/),
*A Closer Look at Claim Decomposition*, DOI `10.18653/v1/2024.starsem-1.13`,
motiviert die getrennte Betrachtung von Zerlegung und nachgelagerter Faktizität.

[VeriScore, Findings EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.552/)
motiviert vollständige Modifikatoren und die Trennung fehlender von widerlegender
Evidenz. Abweichend von dessen Aufgabe behalten wir hypothetische Sicherheitsclaims.
[DnDScore, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1205/) zeigt bereits
im Abstract das Problem ergänzten Kontexts bei der Verifikation; hier wurden
Metadaten und Abstract geprüft, keine komplette Verfahrensübernahme abgeleitet.

Die konkreten Felder, Null-Konvention, Familien und Referenzregeln sind unsere
Operationalisierung. Fünf gezielt geprüfte Primärquellen sind keine systematische
Literaturübersicht und kein Nachweis von Neuheit oder validierter Taxonomie.
