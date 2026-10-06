# Handoff

Stand: 06.10.2026. Reihenfolge und Abschlusskriterien: [WORKPLAN.md](WORKPLAN.md).
Projektplan und fachlicher Stand: [Projektdokumentation](docs/projektstand.pdf).

## Überprüfter Stand

Profil 0.1, beide P/D-Routen, D-Revision, Kontextablation, Extraktionsbaselines und
Annotationsexport sind implementiert. Der erste Pilot nach
[Protokoll 0.1](docs/PILOT_PROTOCOL.md) ist technisch abgeschlossen: 76 von 82
Aufgaben erfolgreich, sechs ungültige Ausgaben, 122 API-Aufrufe ohne Retry.
[Technischer Bericht](docs/PILOT_RUN_20261006.md) mit Fehlern und Grenzen.
**Menschliche Referenzen und Qualitätsbewertung stehen aus.**

106 Offline-Tests bestanden. Request-/Antwort- und Quellhashes, identische
P/D-Codekontexte und die sechs historischen Archivdateien wurden geprüft.
Windows benötigt `-X utf8`; aktive Ressourcen behalten LF-Zeilenumbrüche.
Keine neue Java-/PoV-Ausführung. Die ursprüngliche Projektskizze und archivierte
Originale bleiben unverändert.

## Vorhandene lokale Artefakte

| Pfad (ignoriert) | Inhalt |
|---|---|
| `data/pilot_cases/` | Fünf hashgeprüfte Fälle mit beiden Varianten und getrennten Referenzen |
| `data/pilot/preflight-20261006/` | API-freier Versuchsplan |
| `data/pilot/live-001/` | Abgeschlossener Lauf mit Originaleingaben, Antworten, Manifesten und Budgetjournal |
| `data/annotations/pilot-001/` | Zehn neutrale Codepakete und leere Arbeitsblätter; Zuordnung separat |

Die 10-USD-Freigabe gehörte zum abgeschlossenen ersten Lauf; ein neuer Versuch
bedarf einer eigenen Entscheidung. Keine automatische Wiederholung oder
Fortsetzung. Lokale Rohdaten und `.env` bleiben ausgeschlossen; die Archivierung
der Hauptstudie ist noch festzulegen.

## Nächste Aktion

Menschliche Codereferenzen **vor Einsicht in Modelloutputs** erstellen, danach
separate Reportreferenzen und Claimurteile. Vier Pakete (beide Varianten von
VUL4J-15/41) benötigen eine unabhängige Zweitannotation vor Adjudikation.
Tatsächliche Minuten und Vorwissen erfassen. Keine KI-Ausgabe als menschliche
Referenz ausgeben; keine Qualitätsaussage aus Formatvalidität ableiten.

Hauptstichprobe, statistischen Plan und Umfang erst nach Pilotannotation mit der
Betreuung abstimmen. Entwicklung und Pilot vom Holdout ausschließen.
Historische Grenzen und Herkunft stehen in [PROVENANCE.md](docs/PROVENANCE.md),
Literaturabgrenzung in [RELATED_WORK.md](docs/RELATED_WORK.md).
