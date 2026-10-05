# Handoff: Prose or Structure?

Stand: 2026-10-05, nach Schritt 2. Maßgeblich: [WORKPLAN.md](WORKPLAN.md),
[Projektskizze](prose_or_structure_projektskizze.pdf), [Herkunft](docs/PROVENANCE.md).

## Ziel und nächster Schritt

P: Code → Report → Claims und D: Code → Claims bei identischem Codekontext
vergleichen. RQ1 entwickelt das Profil, RQ2 vergleicht Qualität/Aufwand, RQ3
untersucht Darstellungsfehler und Kontextfelder. Keine Überlegenheit vorwegnehmen.

**Schritt 2 ist als Entwicklungs-PoC erledigt. Als Nächstes Schritt 3:** Den
vorhandenen P-Extraktor samt Validierung auf das gemeinsame Profil umstellen und
einen kleinen D-Schritt ergänzen. Zuerst den archivierten Report verwenden;
kein neuer Report nötig. Nur den jeweils beauftragten Schritt implementieren.

## Verbindlicher Entwicklungsstand

- [Profil 0.1](resources/claim_profile.md) und [Schema](resources/claim_profile.schema.json): Aussage, sechs einfache Kontexttexte, Code-/Reportbezüge, lokale Kontext-IDs, getrennte Prüfaufgabe mit benötigter Evidenz und Zusatzannahmen. Vorhandene Evidenz und Wahrheitsurteile stehen separat.
- [Codebook](resources/claim_codebook.md): generische Regeln für P/D; nur erfundene Beispiele. Fehlend (`null`), explizite Negation und ausdrücklich unbekannt unterscheiden; Bedingungen und Alternativen bleiben in der Proposition.
- [Annotationsprotokoll](resources/annotation_protocol.md) mit [Arbeitsblatt](resources/manual_annotation_template.md): getrennte Report-/Codereferenz, semantische Coverage, offene Fragen, Unsicherheit/Prüfbarkeit, Doppelannotation und Adjudikation.
- [Entwicklungsdurchgang](resources/profile_development/README.md): historische 13 JSPWiki-Claims eingeordnet, zwei zusätzliche Codefälle (VUL4J-47/Jackson XML, VUL4J-9/YAML), getrennte Referenzinventare und zehn ausgewählte JSON-Beispielclaims. Quellen/Revisionen/Hashes und Apache-Lizenzen liegen bei; 19 KB Quell-/Lizenzmaterial.
- Die neuen Beispiele/Urteile sind KI-gestützte redaktionelle Entwürfe, keine unabhängige menschliche Referenz und keine Modellmessung. Keine neue Java-/PoV-Ausführung. Alle drei Fälle samt Varianten bleiben Entwicklung, nicht Holdout.
- Fünf Profilquellen gezielt geprüft; Begründung im Profil. Vollständige Literaturabgrenzung, Security-Baselines und Neuheitsbewertung bleiben offen.

Reale Beispiele, Referenzinventare, Annotationen und Quellenmanifeste **nicht an
Modelle senden**. Nur das generische Codebook ist Teil des bisherigen P-Requests.
Falsche Codepositionen in beiden Routen als Inhalt erhalten und separat bewerten;
P-Zitate müssen exakt zum Report passen. Keine zusätzlichen Referenzfakten in P.

## Was bereits ausführbar ist

Die drei Skripte stammen unverändert aus What-Can-We-Verify `5df7760`:

- `01_prepare_case.py`: fixierter VUL4J-18-Export, fünf erlaubte Modelldateien plus getrennte Referenzen. Lokal vorbereitet; in neuen Clones regenerieren. Kein allgemeiner Fallloader und kein Java-Test.
- `02_generate_findings.py`: Prose-Report aus genau diesem Paket.
- `03_decompose_findings.py`: ein ausgewähltes gespeichertes Finding, kein Code, keine Nachbarfindings. Format-/Zitat-/Unicode-Offset-/Kontext-ID-Prüfung vorhanden.

**Umstellungsgrenze:** `claim_response_schema.json` und der alte P-Prompt bleiben
operativ bei `schema_version: "1"` (acht Felder, freies `qualifiers`). Das neue
`claim_profile.schema.json` mit `profile_version: "0.1"` ist der Vertrag für
Schritt 3, noch kein auswählbarer Laufmodus. Nur die generischen Codebook-Regeln
sind bereits präzisiert. Bei der Umstellung alten Vertrag ersetzen, keine zweite
Pipeline pflegen. Bestehende Tests für Kontexttrennung/Originale weiterverwenden.

Beide vorhandenen Modellschritte verwenden direkten OpenAI-Zugriff mit
`OPENAI_API_KEY`, explizitem Modell/Tokenlimit, JSON-Modus, `store=false`, ohne
Tools/Retry/Repair. `--no-reasoning` setzt `reasoning_effort=none`, sofern unterstützt.
Modell, Budget, Wiederholungen und Pilotprotokoll sind nicht festgelegt;
keine ungeplanten Live-Läufe. Neue XML/YAML-Fixtures sind keine vom CLI bereits
unterstützten Fälle und kein gepaarter Versuch.

## Historisches Archiv erhalten

- `data/runs/VUL4J-18-review-001/`: Finding, Request, Rohantwort, Originalprompt und Manifest.
- `data/annotations/VUL4J-18-review-001/manual_annotation_001.md`: angenommene SG-Revision mit 13 Claims und Codex-Unterstützung/Vorwissen.
- Genau diese sechs Dateien unter `data/` versioniert, insgesamt 108.158 Bytes; andere Downloads/Läufe ignoriert. `inherited_artifacts.json` hält Hashes und Importweg fest. Keine Originale überschreiben.
- Historischer Run `0721c0a0-bba7-48c1-a63c-da196a69d97c`, OpenRouter/Nemotron; entspricht nicht dem heutigen Anbieter. Prompt-CRLF wurden beim Import aus dem Request exakt wiederhergestellt.
- Die fünf lokalen JSPWiki-Quelldateien passen zu den historischen Hashes; der gesamte Requesttext wurde beim Import rekonstruiert. Zusätzliche Quellkopie unnötig.
- Alte Decomposition-Rohdaten, PoV-Logs, ursprüngliche Annotationsabgabe/Review und damaliges Codebook v0.2 fehlen optional. Das heutige Codebook ist kein Ersatzsnapshot.

## Prüfstand und Grenzen

29/29 Offline-Regressionstests bestanden (macOS/Python 3.13.2). Die vier
Profilbeispiele wurden einmalig mit JSON Schema Draft 2020-12 validiert,
einschließlich negativer Formatproben; keine neue Projektabhängigkeit.
Exakte P-Zitate, Kontext-IDs, Codezeilen, Quell-/Archivhashes und lokale Links
geprüft. Die bestehenden Tests prüfen noch den alten ausführbaren P-Vertrag;
Profilvalidierung wird erst mit Schritt 3 Teil der Pipeline/Regressionstests.

Keine Messwerte zur P/D-Qualität, menschlichen Übereinstimmung oder Annotationzeit.
Profil und Familien bleiben vorläufig. Vor Pilot: Modell/Budget, Fallbestand,
Referenzen, Doppelannotator, Blindierung und Fehlerregeln festlegen. Der Pilot
umfasst vorgeschlagene 5–10 neue Fälle; Hauptstichprobe erst daraus begründen.
