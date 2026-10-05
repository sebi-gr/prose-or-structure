"""Prepare neutral, unannotated code packets before inspecting pilot model outputs."""

import argparse
from importlib import import_module
from pathlib import Path
import tempfile

import case_context

generator = import_module("02_generate_findings")
CASE_IDS = ("VUL4J-15", "VUL4J-64", "VUL4J-41", "VUL4J-43", "VUL4J-76")
DOUBLE_ANNOTATION_CASES = {"VUL4J-15", "VUL4J-41"}
ORDER_SALT = "prose-or-structure-annotation-order-v1"
RESOURCES = Path(__file__).resolve().parents[1] / "resources"
SNAPSHOTS = ("annotation_protocol.md", "manual_annotation_template.md",
             "claim_codebook.md", "claim_profile.md", "claim_profile.schema.json")

WORKSHEET = """# Codereferenz — {packet_id}

Vor Einsicht in Modelloutputs und externe Fallreferenzen selbst ausfüllen.
Nur `code.txt` ist Fallevidenz. Keine automatisch erzeugten Wahrheitsurteile.

- Annotator/in:
- Datum:
- Startzeit (mit Zeitzone):
- Endzeit (mit Zeitzone):
- Tatsächliche Bearbeitungszeit in Minuten (Pausen abziehen):
- Pausen / Unterbrechungen:
- Vorwissen / frühere Einsicht in Code, Modelloutputs, Fixes oder Dataset:
- Hilfsmittel:
- Grenzen des vorliegenden Codekontexts:

## Relevantes Inventar

Wenige sicherheitsrelevante Propositionen und konkrete offene Fragen festlegen.
IDs K01, K02, … gelten nur in diesem Paket. Bedingungen, Negationen, Modalität,
Konfiguration und Geltungsbereich erhalten. Fehlendes Wissen nicht ergänzen.
Offene Fragen sind keine bestätigten Schwachstellen. Originalzeilen verwenden.

| ID | Art: proposition / open_question | Proposition oder konkrete offene Frage | Relevanz | Bedingungen / Scope | Datei und Originalzeilen | Sichtbare Evidenz / Grenze / zusätzlich benötigte Evidenz |
|---|---|---|---|---|---|---|
| | | | | | | |

## Abschluss durch die annotierende Person

- Mehrdeutigkeiten / nicht entscheidbare Punkte:
- Begründet ausgeschlossene triviale oder redundante Inhalte:
- Inventar vor Einsicht in Modelloutputs abgeschlossen am:
- Abweichungen vom vorgesehenen Ablauf:

Originalabgabe unverändert erhalten. Bei Doppelannotation zuerst unabhängig
abgeben; Unterschiede erst danach gemeinsam adjudizieren und separat festhalten.
"""

README = """# Vorbereitung der menschlichen Codereferenzen

Diese Ausgabe enthält zehn unannotierte Codepakete. Es wurden keine Referenzurteile,
Annotationszeiten oder Modelloutputs erzeugt. Jeder Paketordner enthält nur den
nummerierten Code und ein leeres `CodeReference.md`.

1. Die koordinierende Person verteilt nur den jeweiligen Paketordner und die
   generischen Dateien in `protocol/`. `linkage.json` und die ursprünglichen
   Fallverzeichnisse bleiben bei ihr; sie enthalten Fall-/Variantenkennungen.
2. Eine Person erstellt für alle zehn Pakete das relevante Codeinventar **vor**
   Einsicht in Modelloutputs, Datasetlabels, Fixes, Tests/PoVs und sonstige externe
   Fallreferenzen. Vorwissen und tatsächliche Start-/Endzeiten selbst eintragen;
   vorhandenes Vorwissen nicht als Blindierung ausgeben.
3. Für die vier vorab ausgewählten Pakete in `double_annotation_packet_ids` erstellt
   eine zweite menschliche Person unabhängig ihr eigenes Inventar. Beide erhalten
   eigene Kopien des leeren Arbeitsblatts und sehen die andere Abgabe vorher nicht.
   Ein zweites LLM ersetzt diese zweite Person nicht. Die koordinierende Person
   bewahrt Abgaben A/B getrennt auf, ohne Originaldateien zu überschreiben.
4. Erst danach Unterschiede und Adjudikation separat dokumentieren: beide
   Originalurteile, betroffene IDs, Entscheidung, Begründung und Entscheider/in.
   Unaufgelöste Unterschiede bleiben sichtbar; keine Übereinstimmung erfinden.

Die vorab bestimmte Teilmenge umfasst beide Varianten zweier Pilotfälle; ihre
Zuordnung steht ausschließlich in `linkage.json`. Packet-IDs ergeben sich aus
einer festen Hashreihenfolge und sind keine Zufallsstichprobe. Variantenlabels
und Generierungsroute fehlen in den Paketen. Dateinamen, Kommentare und Code können
Projekt oder Variante erkennen lassen: vollständige Blindierung ist nicht behauptet.
Originalcode wird für eine stärkere Verblindung weder redigiert noch anonymisiert.

`protocol/` enthält unveränderte Snapshots der generischen Annotationsressourcen.
Hashes der Ressourcen, Originalquellen und nummerierten Codepakete sowie die
getrennte Fallzuordnung stehen in `linkage.json`. Beim Vergleichen mit späteren
P/D-Ausgaben diese eingefrorenen Codeinventare verwenden; Reporttreue bei P ist
eine separate Annotation. Vorbereitung ist kein Abschluss menschlicher Annotation.
"""


# Prüft alle zehn registrierten Quellkontexte und Ressourcen vor dem Schreiben.
# Veröffentlicht neutrale Code-/Leerblattpakete und getrennte Zuordnung atomar in einem neuen Ziel.
# Führt keine Annotation, Modellabfrage oder Wahrheitsbewertung aus.
def prepare_annotations(cases_root: Path, output: Path) -> None:
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output already exists: {output}. Choose a new --output path.")
    catalog_bytes = case_context.CATALOG.read_bytes()
    packets = []
    for case_id in CASE_IDS:
        case = case_context.get_case(case_id)
        for variant in ("vulnerable", "fixed"):
            model_input = cases_root / case_id / variant / "model_input"
            files = generator.load_sources(model_input, case_id)
            generator.verify_variant(files, case_id, variant)
            code = generator.format_sources(files).encode("utf-8")
            packets.append({
                "case_id": case_id, "case_variant": variant,
                "revision": case["variants"][variant]["revision"],
                "source_sha256": {name: generator.sha256(data) for name, data in files.items()},
                "code_sha256": generator.sha256(code), "code": code,
                "double_annotation": case_id in DOUBLE_ANNOTATION_CASES,
                "order_key": generator.sha256(f"{ORDER_SALT}:{case_id}:{variant}".encode("utf-8")),
            })
    resources = {name: (RESOURCES / name).read_bytes() for name in SNAPSHOTS}
    if case_context.CATALOG.read_bytes() != catalog_bytes:
        raise ValueError("Pilot catalog changed during annotation preparation.")
    packets.sort(key=lambda packet: packet["order_key"])
    linkage = {
        "status": "awaiting_human_annotation",
        "catalog_sha256": generator.sha256(catalog_bytes),
        "resource_sha256": {name: generator.sha256(data) for name, data in resources.items()},
        "ordering": {"method": "sha256(salt:case_id:variant), ascending", "salt": ORDER_SALT},
        "double_annotation_cases": sorted(DOUBLE_ANNOTATION_CASES),
        "double_annotation_packet_ids": [], "packets": [],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as temporary:
        staging = Path(temporary) / "annotations"
        (staging / "protocol").mkdir(parents=True)
        for name, content in resources.items():
            (staging / "protocol" / name).write_bytes(content)
        for number, packet in enumerate(packets, 1):
            packet_id = f"packet-{number:02}"
            folder = staging / "packets" / packet_id
            folder.mkdir(parents=True)
            (folder / "code.txt").write_bytes(packet.pop("code"))
            (folder / "CodeReference.md").write_text(WORKSHEET.format(packet_id=packet_id), encoding="utf-8")
            packet.pop("order_key")
            packet["packet_id"] = packet_id
            linkage["packets"].append(packet)
            if packet["double_annotation"]:
                linkage["double_annotation_packet_ids"].append(packet_id)
        (staging / "linkage.json").write_bytes(generator.json_bytes(linkage))
        (staging / "README.md").write_text(README, encoding="utf-8")
        if output.exists() or output.is_symlink():
            raise FileExistsError(f"Output appeared during preparation: {output}")
        staging.rename(output)
    print(f"Prepared 10 blank annotation packets at {output.resolve()}; human annotation remains pending.")


# Liest vorbereitete Pilotfälle und ein neues Ziel für die menschlichen Arbeitsblätter.
# Meldet fehlende Quellen oder Integritätsfehler, ohne vorhandene Annotationen zu verändern.
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path("data") / "pilot_cases")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        prepare_annotations(args.cases, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Could not prepare annotations: {error}\n")


if __name__ == "__main__":
    main()
