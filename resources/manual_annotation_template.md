# Arbeitsblatt — {{CASE_OR_FINDING_ID}}

Kopiervorlage für [Profil 0.1](claim_profile.md) und
[Annotationsprotokoll 0.1](annotation_protocol.md). Nach `data/annotations/` in
einen neuen Pfad kopieren. Nur zum jeweiligen Durchgang passende Tabellen nutzen;
Referenzen und Ausgabeurteile in getrennten Dateien bearbeiten. Unausgefüllte
Vorlage ist kein Annotationsresultat. Die Links hier gelten am Vorlagenstandort;
in einer Arbeitskopie die Referenzen relativ zum neuen Pfad anpassen.

## Zuordnung

- Durchgang: Reportreferenz / Codereferenz / Ausgabebewertung / Adjudikation
- Fall, Variante, Split: AUSFÜLLEN
- Eingabepfade und SHA-256; bei P Finding-ID: AUSFÜLLEN
- Profil-/Codebook-Version und Git-Commit: AUSFÜLLEN
- Annotator/in, Datum, Zeitaufwand: AUSFÜLLEN
- Hilfsmittel, Vorwissen, Blindierung: AUSFÜLLEN
- Status: vorbereitet; noch keine menschliche Annotation

## Reportreferenz — nur P, ohne Codebewertung

Original-Titel und Original-Report unverändert beilegen oder eindeutig per
Datei/Hash referenzieren. Pro unabhängig beurteilbarer Aussage einen Block:

### R01

- Proposition: AUSFÜLLEN
- Exakte Zitate: `field`, `quote`, `occurrence` (einsbasiert)
- Familie, ggf. Subtyp, Begründung: AUSFÜLLEN
- Akteur/Rechte; Voraussetzungen; Negation; Modalität; Quantoren; Scope: AUSFÜLLEN
- Kontextreferenzen und Relation im Aussageinhalt: AUSFÜLLEN
- Grenze/alternative Lesart: AUSFÜLLEN oder keine

| Titel/Satz | Referenz-IDs oder begründeter Ausschluss |
|---|---|
| AUSFÜLLEN | |

## Codereferenz — vor Einsicht in Ausgaben

Codepaket/Manifest per Hash fixieren. Keine Fakten aus Fix/PoV/Advisory importieren.

| ID | Art (`proposition`/`open_question`) | Relevante Proposition/Frage | Relevanzgrund | Datei/Zeilen | Kontextgrenze |
|---|---|---|---|---|---|
| K01 | | | | | |

Externes Zusatzwissen, separat vom Codepaket: AUSFÜLLEN oder keines.

## Profilentwurf — optionale Entwicklung, keine Modellmessung

Für P/D-Beispiele alle Felder aus `claim_profile.schema.json` in einer separaten
JSON-Datei ausfüllen und hier Pfad/Hash vermerken. Herkunft deutlich benennen
(menschlich, KI-unterstützt oder konkreter Modelllauf). Keine menschliche
Bestätigung für automatisch erstellte Entwürfe eintragen.

- Profilausgabe: AUSFÜLLEN
- Prüfaufgaben/benötigte Evidenz/Zusatzannahmen von Aussagen getrennt: AUSFÜLLEN

## Zuordnung und Bewertung

| Referenz-ID | Ausgabe-IDs | Abdeckung (`full`/`partial`/`none`) | Fehlteil/Mehrdeutigkeit |
|---|---|---|---|
| AUSFÜLLEN | | | |

| Ausgabe-ID | P-Treue/Änderung (nur P) | Codeurteil | Konkrete Evidenz/fehlender Kontext | Unsicherheit | Prüfbarkeit |
|---|---|---|---|---|---|
| AUSFÜLLEN | | | | | |

Zusatzclaims ohne Referenzzuordnung und Duplikate: AUSFÜLLEN oder keine.
Lauf-/Bewertungsfehler separat: AUSFÜLLEN oder keine.

## Grenzen / Adjudikation

| IDs | Problem / Urteil A | Unabhängiges Urteil B | Entscheidung, Begründung, Person |
|---|---|---|---|
| AUSFÜLLEN | | | |

Originale A/B erhalten; eine Einzelbearbeitung nicht als Doppelannotation ausgeben.

## Abschluss

- [ ] Inputs/Hashes, Hilfsmittel, Vorwissen und Zeit dokumentiert.
- [ ] Aussagen inkl. Bedingungen, Negation, Modalität und Alternativen erhalten.
- [ ] Reporttreue, Codeurteil, Zusatzwissen und Prüfaufgabe getrennt.
- [ ] Coverage-Zuordnungen und ungelöste Grenzen nachvollziehbar.
- Ergebnis / offene Entscheidungen: AUSFÜLLEN
