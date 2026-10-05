# Annotationsprotokoll

Version 0.1 · 2026-10-05. Entwicklungsverfahren für das
[gemeinsame Profil](claim_profile.md); Hauptstudienprotokoll erst nach dem Pilot.
Markdown mit dem [Arbeitsblatt](manual_annotation_template.md) und JSON für
Profilausgaben genügt. Keine Annotationsplattform erforderlich.

## 1. Eingaben fixieren

Fall/Variante, Split, vollständige erlaubte Dateien und SHA-256, Report/Finding
bei P, Profil-/Codebook-Version und Git-Commit festhalten. Annahmen über die
Umgebung explizit begrenzen. Entwicklungsfälle und ihre gefixten Varianten bleiben
Entwicklung; sie werden nicht später als zurückgehaltene Evaluation verwendet.
Name/Kürzel, Datum, Hilfsmittel, Vorwissen und Bearbeitungszeit protokollieren.

Für neue Evaluation die Codereferenz **vor Einsicht in P/D-Ausgaben** erstellen.
Die nachträgliche JSPWiki-Entwicklungsanalyse erfüllt diese Blindierung nicht.
Nur das fixierte Modell-Codepaket darf Codereferenzurteile tragen. Extra-Patch,
PoV, Advisory oder vollständige Aufrufer separat als externe Evidenz notieren.
Ein PoV-Erfolg ist kein pauschales Label für alle Behauptungen im Fall.

## 2. Zwei getrennte Referenzen

**Reportreferenz (nur P):** Den unveränderten Titel/Report mit dem Codebook in
Propositionen `R01…` zerlegen, Quellen zitieren, Bedingungen und Aussagekraft
erhalten. Kein Code zur Korrektur heranziehen. Jeden Satz/Titel zuordnen oder
begründet ausschließen. Dieselbe Passage kann mehrere Propositionen tragen;
Redundanz braucht keinen zusätzlichen Claim. Mehrdeutige Lesarten dokumentieren.
Die historische Annotation darf Entwicklung unterstützen, ist aber keine
unabhängig bestätigte Referenz und keine vorgegebene Claimzahl.

**Codereferenz (P und D):** Kleinen relevanten Bestand `K01…` aus sichtbaren
Operationen, sicherheitsrelevanten Datenflüssen/Schutzbedingungen und offenen
Fragen formulieren. Pro Einheit Proposition/Frage, Relevanzgrund, konkrete
Datei/Zeilen und Kontextgrenze notieren. `kind: proposition | open_question`
unterscheidet belegbare Inhalte und fehlenden Kontext. Nicht jede Importzeile
oder triviale Operation aufnehmen. Bestand und Grenzen vor den Ausgaben fixieren,
damit viele triviale Claims keine bessere Abdeckung ergeben.

Offene Fragen separat von belegbaren Propositionen auswerten: „Aufrufer und
Authentisierung sind nicht sichtbar“ ist eine relevante Grenze; „das könnte
unsicher sein“ deckt sie nicht schon durch allgemeine Vagheit ab. Eine relevante
unbekannte Voraussetzung wird nie als erwiesene Schwachstelle gezählt.

## 3. Ausgaben semantisch zuordnen und bewerten

Referenz- und Ausgabe-IDs sind unabhängig. Pro Referenzeinheit alle relevanten
Ausgabe-IDs notieren, auch mehrere bei treuer Zerlegung. Ein Claim kann mehrere
Einheiten berühren. Zusammenhang, Subjekt, Negation, Quantoren, Bedingungen und
Modalität entscheiden, nicht identischer Wortlaut, IDs oder Claimzahl.

| Urteil | Regel |
|---|---|
| Abdeckung `full` | Gesamte Referenzproposition inkl. Einschränkungen aus einem Claim oder deren explizit zusammengehöriger Kombination rekonstruierbar |
| Abdeckung `partial` | Nur ein benannter Teil erfasst oder entscheidende Bedingung verändert; Fehlteil begründen |
| Abdeckung `none` | Kein inhaltlich passender Claim |
| P-Treue | Pro Zuordnung `faithful`, `changed` oder `ambiguous`; Änderungen als Addition, Akteur/Rechte, Bedingung, Negation, Modalität/Quantor, Scope oder Relation benennen |
| P-Auslassung | Reportreferenzeinheit ohne vollständige Abdeckung; getrennt von unbelegten Zusatzclaims erfassen |
| Codeurteil `supported` | Der bereitgestellte Code stützt die vollständige Proposition unter genau den genannten Bedingungen |
| Codeurteil `contradicted` | Sichtbare Evidenz widerspricht einer wesentlichen Aussage; konkrete Gegenstelle angeben |
| Codeurteil `inconclusive` | Paket entscheidet die Aussage nicht; fehlende Evidenz oder ungelöste Mehrdeutigkeit konkret benennen |

Duplikate können mehreren Claims zugeordnet werden, jede Referenzeinheit zählt
höchstens einmal. `partial` wird im Pilot separat berichtet, nicht willkürlich
als halber Treffer gewertet. Fehler im Lauf oder im Bewertungsprozess erhalten
einen eigenen Status (`run_error`/`annotation_error`); sie sind keine
`inconclusive`-Claims. Eine gültige leere Ausgabe hat keine Claimurteile und
deckt keine vorhandene Referenzeinheit ab. Keine Division durch null definieren;
Nenner und Aggregation werden im Pilotprotokoll festgelegt.

Bei unvermeidbar gebündelten Aussagen begründet ein Gegenbeleg `contradicted`;
ohne Gegenbeleg und mit offenem wesentlichen Teil `inconclusive`. Teilbefunde
notieren. Eine falsche Bedingung darf durch Aufteilung nicht unsichtbar werden.
Für „A oder B“ widerspricht allein „nicht A“ nicht der gesamten Disjunktion.
Ein `could` macht die Aussage weder wahr noch unprüfbar: benötigten Pfad und
Bedingungen prüfen; bei fehlender Evidenz offen lassen. Nie fehlende Evidenz
als Beweis der Unmöglichkeit verwenden.

**Unsicherheit separat:** Nach dem Codeurteil `appropriate`, `overstated`,
`understated` oder `not_evaluated` mit Begründung notieren. Beispielsweise
garantierter Impact bei unbekanntem Aufruferkontext ist überzogen; ein korrekt
eingeschränkter möglicher Impact kann trotzdem `inconclusive` bleiben.

**Prüfbarkeit:** Sind Gegenstand, Scope und Voraussetzungen hinreichend bestimmt,
und prüft `verification.question` dieselbe Proposition? `usable`, `needs_context`
oder `mismatched` mit konkreter Lücke. Zusätzliche Annahmen und benötigte Evidenz
nicht als tatsächlichen Systemzustand werten. Dass eine Aufgabe ausführbar
formuliert ist, beweist noch nicht die Aussage.

## 4. Unabhängigkeit und Abschluss

Für einen vorab bestimmten Pilot-/Studienteilbestand zwei Menschen unabhängig
annotieren lassen. Separate Dateien A/B mit Zeitstempel und Vorwissen erhalten;
keine gemeinsame Diskussion vor Abgabe. Ein zweites LLM ersetzt keinen zweiten
menschlichen Annotator. Route bei Codebewertung soweit möglich verbergen:
neutrale Ausgabe-IDs, randomisierte Reihenfolge, Reportzitate/Route aus der
Bewertungsansicht entfernen, Originale erhalten. P-Treue benötigt den Report
und kann gegenüber der Route nicht vollständig verblindet sein.

Zuordnungs-/Urteilsabweichungen in einem Adjudikationsblatt dokumentieren:
beide Originalurteile, betroffene IDs, Entscheidung, Begründung, Entscheider/in.
Unaufgelöste Unterschiede dürfen offen bleiben. Übereinstimmung **vor**
Adjudikation, geänderte Urteile und Endstand getrennt berichten; Metrik und
Subset-Größe vor Pilotbeginn festlegen. Heute liegen keine solchen Doppelurteile
oder Übereinstimmungswerte vor.

Codebook-Grenzfälle während Entwicklung sammeln. Bei Änderungen Version und Git
aktualisieren, betroffene Beispiele erneut prüfen; alte Läufe/Annotationen nicht
überschreiben. Nach Pilot Codebook/Referenzen einfrieren, spätere Änderungen als
Protokollabweichung dokumentieren. Effekte pro Fall auswerten, nicht Claims als
unabhängige Stichproben behandeln.
