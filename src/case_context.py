"""Explicit source allowlists for the development case and the selected pilot cases."""

from importlib import import_module
import json
from pathlib import Path, PurePosixPath
import re

import claim_profile

legacy = import_module("01_prepare_case")
CATALOG = Path(__file__).resolve().parents[1] / "resources" / "pilot_cases.json"
DEVELOPMENT_CASES = {"VUL4J-18", "VUL4J-47", "VUL4J-9"}


# Prüft relative Originalpfade ohne Traversierung, Laufwerksnamen oder Windows-Trenner.
# Gibt den unveränderten Pfad zurück; wird vor Downloads und Schreibzugriffen verwendet.
def safe_path(path: object) -> str:
    if (not isinstance(path, str) or not path or "\\" in path or ":" in path
            or "\x00" in path or PurePosixPath(path).is_absolute()
            or any(part in ("", ".", "..") for part in path.split("/"))):
        raise ValueError(f"Unsafe relative file path: {path!r}")
    return path


# Prüft eine hexadezimale SHA-Kennung der angegebenen Länge ohne sie zu korrigieren.
# Die Bezeichnung wird ausschließlich für verständliche Katalogfehler verwendet.
def require_hash(value: object, length: int, label: str) -> None:
    if not isinstance(value, str) or not re.fullmatch(f"[0-9a-f]{{{length}}}", value):
        raise ValueError(f"{label}: expected a {length}-character SHA hash.")


# Prüft eine feste Downloadquelle mit SHA-256 und einer vollen Git-Revision in der URL.
# Der optionale Dateipfad bleibt relativ; Modellquellen müssen zur Variantenrevision passen.
def check_source(source: object, revision: str = None, with_path: bool = True) -> None:
    if not isinstance(source, dict):
        raise ValueError("Catalog source must be an object.")
    if with_path:
        safe_path(source.get("path"))
    require_hash(source.get("sha256"), 64, "Source sha256")
    url = source.get("url")
    if (not isinstance(url, str) or not url.startswith("https://raw.githubusercontent.com/")
            or not re.search(r"/[0-9a-f]{40}/", url)
            or (revision is not None and f"/{revision}/" not in url)):
        raise ValueError("Catalog URL must use a pinned GitHub raw revision.")


# Lädt und prüft den kleinen expliziten Pilotkatalog, einschließlich beider Quellenvarianten.
# Kein Download; Labels bleiben lokale Metadaten und werden nicht als Modellinput zurückgegeben.
def load_catalog() -> dict:
    catalog = json.loads(CATALOG.read_bytes(), object_pairs_hook=claim_profile.unique_object)
    if not isinstance(catalog, dict) or not isinstance(catalog.get("cases"), list) or not catalog["cases"]:
        raise ValueError("Pilot catalog must contain a nonempty cases list.")
    check_source(catalog.get("dataset"), with_path=False)
    ids = set()
    for case in catalog["cases"]:
        if not isinstance(case, dict):
            raise ValueError("Catalog case must be an object.")
        case_id = case.get("case_id")
        if (not isinstance(case_id, str) or not re.fullmatch(r"VUL4J-[0-9]+", case_id)
                or case_id in ids or case_id in DEVELOPMENT_CASES or case.get("split") != "pilot"):
            raise ValueError("Pilot case IDs must be unique, explicit and separate from development.")
        ids.add(case_id)
        for key in ("repo", "weakness", "selection_reason", "context_limits"):
            value = case.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{case_id}: missing {key} text.")
        require_hash(case.get("case_commit"), 40, "Case commit")
        require_hash(case.get("fix_commit"), 40, "Fix commit")
        variants = case.get("variants")
        if not isinstance(variants, dict) or set(variants) != {"vulnerable", "fixed"}:
            raise ValueError(f"{case_id}: exactly vulnerable and fixed variants are required.")
        path_sets = []
        for variant in variants.values():
            if not isinstance(variant, dict):
                raise ValueError("Catalog variant must be an object.")
            require_hash(variant.get("revision"), 40, "Variant revision")
            files = variant.get("files")
            if not isinstance(files, list) or not files:
                raise ValueError("Each pilot variant must list its model files.")
            paths = set()
            for source in files:
                check_source(source, variant["revision"])
                if source["path"] in paths:
                    raise ValueError("Duplicate model source path.")
                paths.add(source["path"])
            path_sets.append(paths)
        if path_sets[0] != path_sets[1]:
            raise ValueError(f"{case_id}: variant source path sets must match.")
        references = case.get("references")
        if not isinstance(references, list):
            raise ValueError("Case references must be a list.")
        paths = {"vul4j_row.json"}
        for source in references:
            check_source(source)
            if source["path"] in paths:
                raise ValueError("Duplicate or reserved reference path.")
            paths.add(source["path"])
    return catalog


# Wählt genau einen registrierten Pilotfall; unbekannte IDs werden nicht geraten.
# Liefert die geprüften Metadaten für Vorbereitung und lokale Herkunftsprüfung.
def get_case(case_id: str) -> dict:
    for case in load_catalog()["cases"]:
        if case["case_id"] == case_id:
            return case
    raise ValueError(f"Unknown pilot case ID: {case_id}")


# Liefert ausschließlich die erlaubten relativen Quelldateipfade eines bekannten Falls.
# Die geerbte VUL4J-18-Liste bleibt unverändert und benötigt keinen Pilotkatalog.
def model_files(case_id: str) -> tuple:
    if case_id == legacy.CASE_ID:
        return legacy.MODEL_FILES
    return tuple(source["path"] for source in get_case(case_id)["variants"]["vulnerable"]["files"])
