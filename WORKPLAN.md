# Arbeitsplan

Stand: 06.10.2026. Forschungsgrundlage ist die
[Projektskizze](prose_or_structure_projektskizze.pdf), aktualisiert in der
[Projektdokumentation](docs/projektstand.pdf). Dieser Plan ist die maßgebliche
Quelle für Reihenfolge, Status, Abschlusskriterien und offene Entscheidungen.

## Ziel

Vergleich von **P: Code → Report → Claims** und **D: Code → Claims** bei identischem
Codekontext und gemeinsamem Claimprofil. RQ1 entwickelt das Profil, RQ2 vergleicht
Qualität und Aufwand, RQ3 untersucht Darstellungsfehler und explizite Kontextfelder.
Eine Überlegenheit von D wird nicht angenommen.

## Meilensteine

| Schritt | Status | Abschlusskriterium |
|---|---|---|
| 0. Repository und geerbte Basis | Erledigt | Import, Herkunft, Lizenzen und Offline-Prüfungen nachvollziehbar |
| 1. Entwicklungsmaterial sichern | Erledigt | Sechs historische Report-/Annotationsdateien mit Originalbytes und Hashes archiviert |
| 2. Profil und Annotation (RQ1) | Entwicklungs-PoC vorhanden | Gemeinsames Profil, Codebook, Grenzfälle und getrennte Referenzregeln ausgearbeitet |
| 3. Gepaarte P/D-Erzeugung | Implementiert | Beide Routen verwenden dieselben Codebytes und denselben Profilvalidator; Kontexttrennung und Herkunft geprüft |
| 4. Pilot | Generierung abgeschlossen; Annotation offen | Referenzen, Bewertungen, Fehler und Annotationszeit vollständig; Vergleichbarkeit beurteilt |
| 5. Hauptstudie planen | Literaturabgrenzung vorbereitet | Stichprobe, Baselines, Budget, Annotation und statistischer Plan nach dem Pilot begründet festgelegt und eingefroren |
| 6. Hauptstudie und Paper | Geplant | Gepaarte Ergebnisse, Unsicherheit, Fehleranalyse, Limitationen und reproduzierbare Artefakte vorhanden |

## Vorliegende Grundlage

- **Profil 0.1:** [Schema und Feldbedeutungen](resources/claim_profile.md),
  [Codebook](resources/claim_codebook.md), [Annotationsprotokoll](resources/annotation_protocol.md).
  Proposition, Kontext, Herkunft und Prüfaufgabe bleiben getrennt; Evidenz und
  Wahrheitsurteile liegen in der Annotation. Kategorien sind vorläufig.
- **Entwicklung:** JSPWiki, Jackson XML und Commons Configuration mit dokumentierten
  [Grenzfällen](resources/profile_development/README.md). Die historische assistierte
  13-Claim-Annotation und KI-gestützte Beispiele sind keine unabhängige Referenz.
- **Prototyp:** Vorbereitung, P/D, Revision, Ablation, Extraktionsbaselines,
  Kostenkontrolle und neutrale Annotationsexporte. 106 Offline-Tests bestanden.
- **Pilot:** fünf Fälle aus zwei Familien, beide Varianten, zwei Wiederholungen
  mit balancierter Reihenfolge. [Protokoll 0.1](docs/PILOT_PROTOCOL.md) und
  [Fallauswahl](docs/PILOT_CASES.md) sind vorab festgelegt. 82 Aufgaben bearbeitet,
  davon sechs ungültige Ausgaben; [technischer Bericht](docs/PILOT_RUN_20261006.md).
  Noch keine menschlichen Piloturteile oder Qualitätsresultate.
- **Literatur:** sieben engste Vorarbeiten gezielt [eingeordnet](docs/RELATED_WORK.md).
  Keine vollständige Literaturübersicht oder bestätigte Neuheit.

## Nächster Schritt: Pilotannotation

1. **Codereferenzen:** Alle zehn neutralen Codepakete vor Einsicht in Modelloutputs
   annotieren. Relevante Propositionen, Bedingungen, Positionen und offene Fragen
   begrenzen; Vorwissen, Hilfsmittel und tatsächliche aktive Minuten festhalten.
2. **Reportreferenzen:** Tatsächlich erzeugte P-Reporte unabhängig von den
   Extraktionen annotieren. Reporttreue und Wahrheit im Code getrennt bewerten.
3. **Claimbewertung:** Beide Routen und Zusatzbedingungen anhand der Referenzen
   beurteilen. Technische Ausfälle, leere Ergebnisse und nicht entscheidbare
   Aussagen getrennt erfassen; keine günstigen Findings oder Versuche auswählen.
4. **Doppelannotation:** Beide Varianten von VUL4J-15 und VUL4J-41 unabhängig von
   zwei Menschen beurteilen, Originalurteile erhalten, danach adjudizieren.
5. **Pilotentscheidung:** Annotationsaufwand, Kontextgrenzen, Robustheit und
   Vergleichbarkeit auswerten. Erst danach Profil-/Designänderungen entscheiden.

Schritt 4 ist erst mit diesen Referenzen und Bewertungen abgeschlossen.
Keine automatischen Wiederholungen der ungültigen Ausgaben. Änderungen nach
Ergebniseinsicht benötigen eine begründete neue Protokollversion.

## Auswertung und Übergang zur Hauptstudie

Fundierung, relevante Abdeckung, P-Bedeutungstreue, Prüfbarkeit und Aufwand folgen
den Definitionen im Annotationsprotokoll. Ganze Routenkosten zählen; gemeinsam
verwendete Reports bei Gesamtkosten nicht doppelt berechnen. D-Revision ist eine
Zwei-Aufruf-Kontrolle, keine Kontrolle mit identischem Tokenbudget.

Gepaarte Unterschiede werden **pro Codefall** ausgewertet; Varianten, Claims und
Wiederholungen sind keine unabhängigen Stichproben. Effektgrößen und Unsicherheit,
Ausfälle und Annotationsübereinstimmung separat berichten. Fünf Pilotfälle
begründen weder Signifikanz- noch Gleichwertigkeitsaussagen.

Vor der Hauptstudie mit der Betreuung festzulegen:

- Hauptstichprobe und Fallzahl-/Präzisionsbegründung, Zeitplan und realistischer Umfang;
- unabhängiger zweiter Annotator und Umgang mit Vorwissen;
- Aggregation, Nenner bei leeren Ergebnissen, fehlgeschlagene Routen und
  Verfahren zur Unsicherheitsbestimmung;
- abschließende Literaturabgrenzung, eingefrorene Ressourcen und Auswertungsplan;
- Ablage und Freigabe eines reproduzierbaren Forschungsdatenarchivs.

Alle Entwicklungs-/Pilotprojekte und ihre Varianten bleiben vom Holdout
ausgeschlossen. Automatische Verifier, Agentenplattform, eigener Modelltrainingslauf
oder eine zweite Veröffentlichung sind kein Teil des jetzigen Arbeitsauftrags.
