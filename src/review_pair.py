"""Check the saved review and the identical code context for a small paired run."""

from importlib import import_module
import json
from pathlib import Path
import re

import claim_profile
import case_context

generator = import_module("02_generate_findings")


# Liest genau ein explizites Artefakt ohne Symlink-Pfade oder automatische Dateisuche.
# Gibt Originalbytes zurück; fehlende Dateien und Links sind Startfehler.
def read_artifact(path: Path) -> bytes:
    absolute = path.absolute()
    if any(part.is_symlink() for part in (absolute, *absolute.parents)):
        raise ValueError(f"Review input must not use symlinks: {path}")
    return path.read_bytes()


# Prüft einen gespeicherten erfolgreichen registrierten Report anhand seiner Originalartefakte.
# Liest nur Manifest, Request, Rohantwort und Findings; sendet nichts und verändert keine Dateien.
# Der historische OpenRouter-Review braucht keine nachträglich erfundenen Metadatenfelder.
def load_review(review_run: Path) -> dict:
    manifest_bytes = read_artifact(review_run / "run_manifest.json")
    manifest = json.loads(manifest_bytes, object_pairs_hook=claim_profile.unique_object)
    if not isinstance(manifest, dict):
        raise ValueError("Expected a saved review manifest.")
    allowed_files = case_context.model_files(manifest.get("case_id"))
    if manifest.get("status") not in ("completed", "no_findings"):
        raise ValueError("Review must have completed or produced no_findings.")
    run_id = manifest.get("run_id")
    claim_profile.require_text(run_id, "Review run_id")
    source_hashes = manifest.get("source_sha256")
    if (not isinstance(source_hashes, dict) or set(source_hashes) != set(allowed_files)
            or any(not isinstance(h, str) or not re.fullmatch(r"[0-9a-f]{64}", h)
                   for h in source_hashes.values())):
        raise ValueError("Review must record hashes for exactly the registered source files.")
    if "case_variant" in manifest:
        claim_profile.require_text(manifest["case_variant"], "Review case_variant")

    request_bytes = read_artifact(review_run / "request.json")
    raw = read_artifact(review_run / "generation_raw.json")
    findings_bytes = read_artifact(review_run / "findings.jsonl")
    for field, content in (("request_sha256", request_bytes), ("response_sha256", raw)):
        if manifest.get(field) != generator.sha256(content):
            raise ValueError(f"Review {field} does not match its artifact.")
    if ("findings_sha256" in manifest
            and manifest["findings_sha256"] != generator.sha256(findings_bytes)):
        raise ValueError("Review findings_sha256 does not match findings.jsonl.")
    request = json.loads(request_bytes, object_pairs_hook=claim_profile.unique_object)
    messages = request.get("messages") if isinstance(request, dict) else None
    if (not isinstance(messages, list) or len(messages) != 2
            or any(not isinstance(m, dict) for m in messages)
            or [m.get("role") for m in messages] != ["system", "user"]
            or any(not isinstance(m.get("content"), str) for m in messages)):
        raise ValueError("Review request must contain its original system and code-only user messages.")
    response = json.loads(raw, object_pairs_hook=claim_profile.unique_object)
    # Use the stored provider content, not a new model call or the review's labels.
    try:
        original_findings = generator.parse_findings(response)
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError("Review response is not a complete findings response.") from error
    expected = [{"finding_id": f"{run_id}:F{index:03d}", **finding}
                for index, finding in enumerate(original_findings, 1)]
    findings = [json.loads(line, object_pairs_hook=claim_profile.unique_object)
                for line in findings_bytes.decode("utf-8").split("\n") if line.strip()]
    if findings != expected:
        raise ValueError("Review findings do not match the original response and run IDs.")
    expected_status = "completed" if findings else "no_findings"
    if manifest["status"] != expected_status:
        raise ValueError("Review status is inconsistent with its findings.")
    return {"manifest": manifest, "manifest_bytes": manifest_bytes,
            "request": request, "request_bytes": request_bytes,
            "findings_bytes": findings_bytes, "findings": findings}


# Prüft die gelesenen Quellbytes gegen den Review, einschließlich der tatsächlich gesendeten Ansicht.
# Verhindert falsche Paarung vor API-Aufruf/Ausgabeverzeichnis; liest selbst keine Quellen.
def verify_sources(files: dict, parent: dict) -> None:
    hashes = {name: generator.sha256(content) for name, content in files.items()}
    if hashes != parent["manifest"]["source_sha256"]:
        raise ValueError("Source files do not match the paired review hashes.")
    if generator.format_sources(files) != parent["request"]["messages"][1]["content"]:
        raise ValueError("Source context differs from the original review request.")
