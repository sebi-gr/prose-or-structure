"""Download the explicitly selected pilot contexts, with separate fixed variants and references."""

import argparse
import csv
import hashlib
from importlib import import_module
import io
from pathlib import Path
import re
import tempfile
from urllib.error import URLError

import case_context

prepare_case = import_module("01_prepare_case")
download = prepare_case.download
json_bytes = prepare_case.json_bytes


# Lädt eine festgelegte Quelle und prüft deren Originalbytes gegen den Kataloghash.
# UTF-8 wird für Modellquellen zusätzlich geprüft, ohne Zeilenumbrüche zu ändern.
def fetch_source(source: dict, text: bool = False) -> bytes:
    content = download(source["url"])
    if hashlib.sha256(content).hexdigest() != source["sha256"]:
        raise ValueError(f"Downloaded content hash differs: {source['url']}")
    if text:
        content.decode("utf-8")
    return content


# Baut ausgewählte Pilotfälle in einem neuen Ziel aus fixierten URLs und SHA-256-Hashes.
# Veröffentlicht erst nach vollständiger Prüfung; getrennte Varianten sind keine zusätzlichen Fälle.
# Referenzen/Labels stehen außerhalb model_input; führt weder Java noch PoVs oder Modelle aus.
def prepare_pilot(output: Path, case_id: str = None) -> None:
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output already exists: {output}. Choose a new --output path.")
    catalog = case_context.load_catalog()
    catalog_bytes = case_context.CATALOG.read_bytes()
    cases = [case for case in catalog["cases"] if case_id is None or case["case_id"] == case_id]
    if not cases:
        raise ValueError(f"Unknown pilot case ID: {case_id}")
    dataset = fetch_source(catalog["dataset"], text=True)
    rows = list(csv.DictReader(io.StringIO(dataset.decode("utf-8"))))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as temporary:
        staging = Path(temporary) / "pilot"
        staging.mkdir()
        for case in cases:
            matching_rows = [row for row in rows if row.get("vul_id") == case["case_id"]]
            if len(matching_rows) != 1:
                raise ValueError(f"Expected exactly one dataset row for {case['case_id']}.")
            row = matching_rows[0]
            patch_prefix = f"https://github.com/{case['repo']}/commit/"
            patch_url = row.get("human_patch", "")
            patch_revision = patch_url[len(patch_prefix):] if patch_url.startswith(patch_prefix) else ""
            if (row.get("repo_slug") != case["repo"]
                    or not re.fullmatch(r"[0-9a-f]{7,40}", patch_revision)
                    or not case["fix_commit"].startswith(patch_revision)):
                raise ValueError(f"Dataset row does not match {case['case_id']} repository and fix.")
            case_root = staging / case["case_id"]
            reference = case_root / "reference"
            reference.mkdir(parents=True)
            for source in case["references"]:
                content = fetch_source(source)
                target = reference / source["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            (reference / "vul4j_row.json").write_bytes(json_bytes(row))
            for variant_name, variant in case["variants"].items():
                variant_root = case_root / variant_name
                hashes = {}
                for source in variant["files"]:
                    content = fetch_source(source, text=True)
                    target = variant_root / "model_input" / source["path"]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                    hashes[source["path"]] = hashlib.sha256(content).hexdigest()
                manifest = {
                    "case_id": case["case_id"], "case_variant": variant_name, "split": "pilot",
                    "repo": case["repo"], "revision": variant["revision"],
                    "case_commit": case["case_commit"], "upstream_fix_commit": case["fix_commit"],
                    "source_sha256": hashes, "sources": variant["files"],
                    "catalog_sha256": hashlib.sha256(catalog_bytes).hexdigest(),
                    "dataset": catalog["dataset"], "references": case["references"],
                    "dataset_row_sha256": hashlib.sha256(json_bytes(row)).hexdigest(),
                    "review_mode": "localized_review", "context_limits": case["context_limits"],
                    "pov_status": "not_run",
                }
                (variant_root / "case_manifest.json").write_bytes(json_bytes(manifest))
        (staging / "pilot_cases.json").write_bytes(catalog_bytes)
        # Recheck before the single publish step; no output is usable before this rename.
        if output.exists() or output.is_symlink():
            raise FileExistsError(f"Output appeared during preparation: {output}")
        staging.rename(output)
    print(f"Prepared {len(cases)} pilot cases at {output.resolve()}; PoVs not run.")


# Liest neues Ausgabeverzeichnis und optional eine einzelne registrierte Pilotfall-ID.
# Meldet Download-/Integritätsfehler mit Exit-Code 1; unvollständige Exporte bleiben unveröffentlicht.
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data") / "pilot_cases",
                        help="New output root; never overwrite an existing preparation.")
    parser.add_argument("--case", dest="case_id", help="One registered pilot ID; omit for all selected cases.")
    args = parser.parse_args()
    try:
        prepare_pilot(args.output, args.case_id)
    except (OSError, URLError, ValueError) as error:
        parser.exit(1, f"Could not prepare pilot: {error}\n")


if __name__ == "__main__":
    main()
