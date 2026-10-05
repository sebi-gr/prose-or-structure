# Gezielte Abgrenzung der Vorarbeiten

Stand: 2026-10-05. Diese Notiz prüft die sieben engsten Arbeiten aus der
[Projektskizze](../prose_or_structure_projektskizze.pdf). Sie ist vorbereitende
Literaturarbeit für Schritt 5, keine systematische Recherche, Neuheitsbewertung
oder Reproduktion. Hauptstichprobe und Auswertung werden erst nach dem Pilot
festgelegt. Zitierbare Metadaten stehen in
[references.bib](../resources/references.bib).

| Arbeit; geprüfte Primärquelle | Bestehender Ansatz | Bedeutung und Grenze für dieses Projekt |
|---|---|---|
| **DecompScore:** Wanner et al., *A Closer Look at Claim Decomposition*, *SEM 2024, S.153–175. [Publikation](https://aclanthology.org/2024.starsem-1.13/), [Volltext v1](https://arxiv.org/html/2403.11903v1), insbesondere §3. | Untersucht, wie Zerlegung nachgelagerte Faktizitätswerte verändert; bewertet Originaltreue, Abdeckung und Atomizität. | Motiviert getrennte Bewertung von P-Extraktion und Code-Grounding. Die Anzahl originalgestützter Teilclaims ist kein Ersatz für unsere auf relevante Sicherheitspropositionen begrenzte Coverage. |
| **VeriScore:** Song, Kim, Iyyer, Findings EMNLP 2024, S.9447–9474. [Publikation](https://aclanthology.org/2024.findings-emnlp.552/), [PDF](https://aclanthology.org/2024.findings-emnlp.552.pdf), §§2.1.2, 2.3. | Extrahiert eigenständig verständliche, überprüfbare Aussagen mit erforderlichen Modifikatoren; prüft sie anhand externer Suchergebnisse. Unentscheidbarkeit wird von Widerspruch getrennt. | Geeignete allgemeine Extraktionsbaseline. Der originale Ausschluss hypothetischer Aussagen passt nicht vollständig zu modalen Sicherheitsclaims; diese Grenze bleibt sichtbar. Unser primäres Codebook behält solche Claims bei. |
| **DnDScore:** Wanner, Van Durme, Dredze, EMNLP 2025, S.23609–23626. [Publikation](https://aclanthology.org/2025.emnlp-main.1205/); Metadaten und Abstract geprüft. | Untersucht das Zusammenspiel von Zerlegung, ergänzendem Kontext und Verifikation. Eingefügter Kontext kann selbst zusätzliche prüfbare Tatsachen enthalten. | Motiviert die Trennung von ursprünglicher Proposition und ergänzendem Kontext. Hieraus wird keine vollständige Verfahrensübernahme oder Leistungsbehauptung für Codeanalyse abgeleitet. |
| **LLMSAN:** Wang et al., *Sanitizing Large Language Models in Bug Detection with Data-Flow*, Findings EMNLP 2024, S.3790–3805. [Publikation](https://aclanthology.org/2024.findings-emnlp.217/); Metadaten und Abstract geprüft. | Lässt Datenflusspfade erzeugen, zerlegt sie in Programmeigenschaften und prüft sie mittels Parsing und LLMs. | Verwandt mit überprüfbaren Security-Aussagen. Als Vergleich nur für passende Datenfluss-Teilaufgaben; kein austauschbarer Extraktor allgemeiner Reportaussagen. Eine Integration ist nicht Teil des jetzigen PoC. |
| **GPTAid:** Liu et al., *Generating API Parameter Security Rules with LLM for API Misuse Detection*, NDSS 2025. [Veranstalterseite](https://www.ndss-symposium.org/ndss-paper/generating-api-parameter-security-rules-with-llm-for-api-misuse-detection/), [PDF](https://www.ndss-symposium.org/wp-content/uploads/2025-465-paper.pdf), Abstract und Einleitung. | Generiert API-Parameterregeln aus Quellcode; prüft und konkretisiert sie mit erzeugtem Aufruf-/Verletzungscode, Ausführungsfeedback und Codevergleich. | Zeigt die Bedeutung konkreter Aussagen für Prüfaufgaben. Dynamische API-Regelprüfung unterscheidet sich von unserem kontrollierten P/D-Vergleich bei gleichem begrenztem Java-Kontext. |
| **VERGE:** Singh et al., *Formal Refinement and Guidance Engine for Verifiable LLM Reasoning*, arXiv:2601.20055 **v2, 2026-05-02**. [Versionierte Primärquelle](https://arxiv.org/abs/2601.20055v2); Metadaten und Abstract geprüft. | Verbindet Claimzerlegung, Autoformalisierung, SMT-/Konsistenzprüfung und iterative Überarbeitung; nutzt außerdem Modellkonsens. | Konzeptionell verwandt, aber ein anderes Ziel und deutlich größerer Systemumfang. Logische Konsistenz oder Modellkonsens ist keine unabhängige Bestätigung eines Security-Claims im gegebenen Code. Kein Solver-/Ensemble-System geplant. |
| **EviGuard:** Zhou, Lei, Yang, *Machine-Verifiable Evidence Grounding for LLM-Based Industrial Incident Reasoning*, Applied Sciences **16(18), 8925**, 2026-09-08. [Verlagsquelle](https://www.mdpi.com/2076-3417/16/18/8925), insbesondere Abstract, §§1.2, 4.2, 7. | Übersetzt industrielle Incident-Hypothesen in eine begrenzte Claim-Sprache und prüft sie deterministisch gegen versionierte Provenienzgraphen; Handlungen hängen von gestützten Voraussetzungen ab. | Referenzexistenz und inhaltliche Unterstützung sind verschieden. Incident-Logs, Graphschema und spezialisierte Verifier bilden jedoch keine unmittelbar passende Baseline für unseren Code-Report-Vergleich. Keine Leistungsübertragung auf unsere Aufgabe. |

**Bibliographische Korrektur:** Die erste Seite des offiziellen GPTAid-PDFs nennt
`10.14722/ndss.2025.230465`; die Skizze nennt verkürzt `...23465`. Die Bibliographie
verwendet den geprüften DOI. Das originale Projektskizzen-PDF bleibt unverändert.
DecompScore wird über die publizierte *SEM-Fassung zitiert; der gezielt gelesene
Volltext war zusätzlich arXiv:2403.11903v1 vom 18.03.2024. VERGE bleibt ausdrücklich
ein versionierter Preprint. Für EviGuard ist das initiale Publikationsdatum
08.09.2026 maßgeblich; die [Versionsnotiz](https://www.mdpi.com/2076-3417/16/18/8925/notes)
führt aktualisierte Dateien vom 09.09.2026 auf.

## Baselineentscheidung für den Pilot

Neben der einfachen Satzzerlegung verwenden wir den originalen Non-QA-Prompt aus
dem [VeriScore-Autorenrepo](https://github.com/Yixiao-Song/VeriScore/tree/8714bca27b944b9659d6a966cdb92fb6fff8f72d),
Commit `8714bca27b944b9659d6a966cdb92fb6fff8f72d`. Prompt und Apache-2.0-Lizenz
sind bytegetreu übernommen; Herkunft und Hashes liegen unter
[resources/baselines](../resources/baselines/README.md).

Die kleine Umsetzung ist eine **VeriScore-basierte Extraktionsbaseline**, keine
Reproduktion des gesamten VeriScore-Systems: deterministische Regex-Satzgrenzen
ersetzen spaCy, alle originalen Titel- und Reportsätze werden bearbeitet, und der
fixierte Pilotmodell-Snapshot ersetzt das damalige Modell. Die Titelbehandlung,
Fensterbildung, strikte Bullet-Auswertung und Deduplizierung sind dort dokumentiert.
Die originale Hypothetika-Regel bleibt erhalten. Keine Websuche, Wahrheitsbewertung,
Sicherheitsprofil-Erzwingung oder automatische Reparatur wird hinzugefügt.
Aufrufzahl, Formatfehler und resultierende Auslassungen werden separat erfasst.

## Unsere geplante Untersuchung

Der geplante Beitrag ist der gepaarte Vergleich **Code → Report → Claims** mit
**Code → Claims** unter identischem Codekontext und gemeinsamem Zielprofil.
Reporttreue wird nur für P erhoben; Code-Grounding, relevante Coverage, erhaltene
Bedingungen/Unsicherheit, Prüfbarkeit und Aufwand betreffen beide Routen.
Budgetkontrolle durch D-Überarbeitung und eine kleine Kontextfeld-Ablation sind
separate Versuche. Das sind unsere Forschungsentscheidungen, keine bereits
belegten Ergebnisse oder aus den Arbeiten zwingend folgenden Regeln.

Der Blick auf diese sieben Arbeiten belegt weder Neuheit noch Überlegenheit
einer Route. Vor der Hauptstudie sind eine breitere Suche, die Prüfung weiterer
naher Arbeiten und die empirische Pilotbewertung weiterhin notwendig.
Die begriffliche Nutzung von CAE/SACM für Aussage, Kontext/Annahme und Evidenz ist
bereits im [Claimprofil](../resources/claim_profile.md#begründung-und-reichweite)
mit Primärquellen und Grenzen festgehalten; keine Standardimplementierung geplant.
