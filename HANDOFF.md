# Handoff: Prose or Structure?

Stand: 2026-10-05. Aktueller Plan: [WORKPLAN.md](WORKPLAN.md). Forschungsrichtung: [Projektskizze v0.1](prose_or_structure_projektskizze.pdf) vom 03.10.2026. Herkunft und vollständiges Artefaktinventar: [docs/PROVENANCE.md](docs/PROVENANCE.md).

## Ziel und Entscheidungen

Neues Paper zum Vergleich **P: Code → Report → Claims** mit **D: Code → Claims**, bei identischem Codekontext und gemeinsamem Claimprofil. RQ1 betrifft das Profil, RQ2 Qualität/Aufwand, RQ3 Darstellungsfehler und Kontextfeld-Ablation. Der alte Fokus auf eine breite automatische Verifikationspipeline ist hier ersetzt.

KISS bleibt verbindlich. Vorhandene Vorbereitung und Reportgenerierung werden weiterverwendet; die neuen Claim-Routen sind der nächste Implementierungsabschnitt. Keine neuen Modellläufe, keine automatische Modell-/Budgetauswahl und keine zusätzliche Provider-Abstraktion wurden für die Einrichtung eingeführt.

## Tatsächlicher Stand

- Zielrepo: [sebi-gr/prose-or-structure](https://github.com/sebi-gr/prose-or-structure), Branch `main`. Den aktuellen Commit und Remote-Stand zu Sessionbeginn mit Git prüfen.
- Importquelle: `What-Can-We-Verify`, nach Fetch `origin/main` auf `8f9b25e1d5d53208f6f58dba9ffba8396a68dd5c`. Der dortige lokale Checkout ist älter und blieb unverändert.
- Neun übernommene Dateien stimmen bytegleich mit dem fixierten Quellstand überein; Hashes in `resources/inherited_baseline.json`. Enthalten sind beide Skripte, alle bestehenden Tests, Prompt, historisches PoV-Protokoll, leere `.env.example` und die identische MIT-Lizenz.
- README und Workplan sind neu ausgerichtet, AGENTS angepasst, dieses Handoff neu geschrieben. PDF unverändert übernommen. Ignore-Regeln schützen Daten, lokale Schlüssel und Python-Umgebungen. `.github/workflows/checks.yml` führt die Offline-Tests und Whitespace-Prüfung auf GitHub aus.
- `data/VUL4J-18/` wurde hier frisch vorbereitet und geprüft; es ist lokal vorhanden und ignoriert. Ein frischer Clone muss es selbst erzeugen.
- Der Generator nutzt **OpenRouter Chat Completions**, verlangt eine explizite `:free`-Modell-ID und ein Ausgabetokenlimit, hat keine automatischen Fallbacks/Retry und liest den Key aus `.env`/Prozessumgebung. Es handelt sich nicht mehr um die ältere OpenAI-Responses-Implementierung.
- Fall-ID und fünf erlaubte Eingabepfade sind auf VUL4J-18 festgelegt. `--model-input` allein macht das Skript nicht mehrfallfähig.

**Nicht implementiert:** gemeinsames Claim-Schema, P-Extraktor, direkte D-Erzeugung, D-Überarbeitung, Baselines, Ablation und Vergleichsauswertung. Modell, Budget und Evaluationsprotokoll sind offen.

## Fehlende Originalartefakte

Die Skizze berichtet einen JSPWiki-Report, 13 manuelle Claims, ein erstes Codebook und einen reproduzierten Java-PoV. Im erreichbaren Stand sind nur die Pipeline und die Dokumentation zu Review/PoV vorhanden:

- Review-Run `0721c0a0-bba7-48c1-a63c-da196a69d97c`: in den Quellnotizen beschrieben, Rohartefakte fehlen.
- 13 Claims und ursprüngliches Codebook: in der Skizze genannt, Originaldateien nicht gefunden.
- PoV: historisches Windows-Protokoll übernommen, zugehörige Logs/Metadaten fehlen.

In beiden Projektordnern und der verfügbaren Git-Historie gesucht; Ablageort beim Nutzer angefragt. Die Einrichtung ist damit als Codebasis nutzbar, aber **keine vollständige Übernahme der empirischen Vorarbeit**. Alte Dokumentationsaussagen über lokal vorhandene Runs wurden nicht als aktueller Dateibestand übernommen. Fehlende Daten nicht erfinden oder still neu erzeugen.

## Geprüft am 05.10.2026

- macOS, Python **3.13.2**: `python3 -m unittest -v` — **15/15 bestanden, kein Skip**, einschließlich Symlink-Test. Ausschließlich synthetische Offline-Antworten.
- Beide CLI-Hilfen funktionieren aus dem Repo-Wurzelverzeichnis.
- Echter Vorbereitungslauf erfolgreich. Alle neun Download-Hashes geprüft; Dateien, Manifest und Dataset-Zeile bytegleich mit dem vorhandenen Export des Quellrepos. Fünf Modelldateien, 71.907 Bytes.
- Importdateien gegen fixierte Git-Blobs und SHA-256-Nachweis geprüft; PDF unverändert.
- 20 lokale Markdown-Verweise aufgelöst; `git diff --cached --check` ohne Befund. 18 versionierte Dateien einschließlich bestehender Lizenz geprüft; Daten, `.env`, Umgebungen und Caches ausgeschlossen, keine Treffer für die geprüften Zugangsdatenmuster.
- Arbeitsbaum und Index des Quellrepos unverändert. Der CI-Workflow ist eingerichtet; sein jeweils aktuelles Ergebnis ist unter GitHub Actions sichtbar.

**Nicht ausgeführt:** Live-Inferenz, neue manuelle Annotation, neuer Java-Build/PoV oder P/D-Experiment. Modellverfügbarkeit und Literatur/Neuheit wurden nicht neu geprüft. Historische Messergebnisse sind dokumentiert, nicht anhand vorhandener Rohdaten erneut validiert.

## Nächster Schritt

Mit **Schritten 1–2 in WORKPLAN** fortfahren: fehlende Originale sichern und Claimprofil/Annotationsregeln anhand echter Entwicklungsbeispiele präzisieren. Die Feldgruppen und methodischen Anforderungen sind im Plan vorbereitet; sie sind noch kein validiertes Codebook. Danach den kleinsten vollständigen P/D-Vergleich implementieren.

Die fehlenden Originale blockieren die Prüfung der historischen Annotation, nicht die Arbeit am Profilentwurf. Zusätzliche Entwicklungsfälle, zweiter Annotator, Modell/Budget und Pilotbestand bleiben zu entscheiden.
