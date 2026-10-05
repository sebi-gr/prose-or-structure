"""Decompose one saved finding with the claim codebook and validate its claim format."""

import argparse
from datetime import datetime, timezone
from importlib import import_module
from http.client import HTTPException
import json
from pathlib import Path
import time
from uuid import uuid4

import claim_profile
import review_pair
import pilot_profile

generator = import_module("02_generate_findings")
json_bytes = generator.json_bytes
sha256 = generator.sha256
RESOURCES = Path(__file__).resolve().parents[1] / "resources"
PROMPT = RESOURCES / "decomposition_prompt.txt"
CODEBOOK = claim_profile.CODEBOOK
SCHEMA = claim_profile.SCHEMA
PROFILE_VERSION = claim_profile.PROFILE_VERSION
unique_object = claim_profile.unique_object
require_keys = claim_profile.require_keys
require_text = claim_profile.require_text
parse_response = claim_profile.parse_response


# Lädt die explizite JSONL-Datei und wählt eine Finding-ID oder bündelt mit all sämtliche Findings.
# Verlangt Generatorfelder, lehnt Symlink-Pfade/doppelte IDs ab und liest keine Nachbardateien.
# Liefert die Originalbytes der Datei sowie das ausgewählte Finding zurück.
def load_finding(path: Path, finding_id: str) -> tuple:
    absolute = path.absolute()
    if any(part.is_symlink() for part in (absolute, *absolute.parents)):
        raise ValueError("Finding input must not use symlinks.")
    raw = path.read_bytes()
    selected = None
    ids = set()
    findings = []
    for number, line in enumerate(raw.decode("utf-8").split("\n"), 1):
        if not line.strip():
            continue
        finding = json.loads(line, object_pairs_hook=unique_object)
        require_keys(finding, {"finding_id", "title", "report"}, f"Input line {number}")
        for key, value in finding.items():
            require_text(value, f"Input line {number}.{key}")
        if finding["finding_id"] in ids:
            raise ValueError("Duplicate finding_id in input.")
        ids.add(finding["finding_id"])
        findings.append(finding)
        if finding["finding_id"] == finding_id:
            selected = finding
    if finding_id == "all" and findings:
        # Original title/report substrings remain unchanged; only section delimiters are added.
        selected = {"finding_id": "all", "title": "Complete security review",
                    "report": "\n\n".join(
                        f"[Finding {index}]\nTitle: {item['title']}\nReport:\n{item['report']}"
                        for index, item in enumerate(findings, 1))}
    if selected is None:
        raise ValueError("Selected finding_id was not found; no request sent.")
    return raw, selected


# Prüft das gemeinsame Profil für P und löst exakte Reportzitate auf.
# Delegiert dieselben Strukturregeln wie D; greift nicht auf Quellcode zu.
def validate_claims(document: dict, finding: dict) -> list:
    return claim_profile.validate_claims(document, "P", finding)


# Zerlegt ein ausgewähltes Finding oder den vollständigen Report in einem neuen Laufverzeichnis mit einem OpenAI-Modell.
# Speichert Originaleingabe, Codebook/Prompt/Schema, Request, Rohantwort, Validierung und gültige Claims.
# Prüft den zugehörigen gespeicherten Review als Provenienz; nur Titel/Report gelangen ins Modell.
# Nutzt den bestehenden Transport, ohne Quellcodeanalyse oder Referenzannotation.
# Kein Retry/Repair; bei Fehlern bleiben Artefakte erhalten, ohne partielle gültige Claims auszugeben.
def decompose_findings(findings_path: Path, finding_id: str, output: Path, model: str,
                       max_output_tokens: int, disable_reasoning: bool = False,
                       no_context_fields: bool = False, requester=None) -> str:
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output already exists: {output}. Choose a new --output path.")
    if not model or "/" in model or model.endswith(":free") or any(char.isspace() for char in model):
        raise ValueError("Select an explicit OpenAI model ID (without an OpenRouter prefix or :free suffix).")
    if max_output_tokens < 1:
        raise ValueError("A positive max-output-tokens value is required.")
    input_bytes, finding = load_finding(findings_path, finding_id)
    parent = review_pair.load_review(findings_path.parent)
    if input_bytes != parent["findings_bytes"]:
        raise ValueError("Input findings differ from the paired review findings.jsonl.")
    parent_manifest = parent["manifest"]
    resources = pilot_profile.resources(PROMPT, no_context_fields)
    if finding_id == "all":
        resources[PROMPT.name] += ("\nThe input is the complete review: all original finding titles and reports, "
                                  "in order. The generic title and [Finding N], Title:, Report: delimiters "
                                  "are assembly metadata, not security claims. Cover every original finding.\n").encode()
    system = (resources[PROMPT.name].decode("utf-8")
              + "\n\nCODEBOOK\n" + resources[CODEBOOK.name].decode("utf-8")
              + "\n\nRESPONSE SCHEMA\n" + resources[SCHEMA.name].decode("utf-8"))
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(
                {key: finding[key] for key in ("title", "report")}, ensure_ascii=False)},
        ],
        "max_completion_tokens": max_output_tokens,
        "service_tier": "default",
        "stream": False,
        "store": False,
        "response_format": {"type": "json_object"},
    }
    if disable_reasoning:
        payload["reasoning_effort"] = "none"
    body = json_bytes(payload)
    run_id = str(uuid4())
    manifest = {
        "run_id": run_id, "finding_id": finding_id,
        "route": "P", "stage": "report_decomposition",
        "report_unit": "all_findings_v1" if finding_id == "all" else "single_finding",
        "profile_variant": "no_context_fields" if no_context_fields else "full",
        "case_id": parent_manifest["case_id"],
        "case_variant": parent_manifest.get("case_variant", "unspecified"),
        "parent_run_id": parent_manifest["run_id"],
        "paired_review_run_id": parent_manifest["run_id"],
        "profile_version": PROFILE_VERSION,
        "codebook_version": claim_profile.CODEBOOK_VERSION,
        "source_sha256": parent_manifest["source_sha256"],
        "review_manifest_sha256": sha256(parent["manifest_bytes"]),
        "review_request_sha256": sha256(parent["request_bytes"]),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "provider": "openai", "endpoint": generator.ENDPOINT,
        "model_requested": model,
        "parameters": {key: value for key, value in payload.items() if key != "messages"},
        "findings_input_sha256": sha256(input_bytes),
        "finding_sha256": sha256(json_bytes(finding)),
        "resource_sha256": {name: sha256(content) for name, content in resources.items()},
        "implementation_sha256": {
            path.name: sha256(path.read_bytes()) for path in (
                Path(__file__), Path(claim_profile.__file__), Path(review_pair.__file__),
                Path(pilot_profile.__file__), Path(generator.case_context.__file__),
                Path(generator.__file__), Path(generator.prepare_case.__file__))},
        "request_sha256": sha256(body), "timeout_seconds": generator.TIMEOUT_SECONDS,
        "request_attempts": 0, "status": "running", "usage": None, "cost_usd": None,
    }
    validation = {"status": "not_run", "claim_count": None, "errors": [],
                  "scope": "Format, exact quotes and references; not semantic correctness or truth."}
    output.mkdir(parents=True)
    (output / "run_manifest.json").write_bytes(json_bytes(manifest))
    started = time.monotonic()
    phase = "setup"
    try:
        (output / "review_manifest.json").write_bytes(parent["manifest_bytes"])
        for name, content in resources.items():
            (output / name).write_bytes(content)
        (output / "findings_input.jsonl").write_bytes(input_bytes)
        (output / "finding.json").write_bytes(json_bytes(finding))
        (output / "request.json").write_bytes(body)
        api_key = generator.load_api_key()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing from the environment and project .env.")
        phase = "request"
        manifest["request_attempts"] = 1
        (output / "run_manifest.json").write_bytes(json_bytes(manifest))
        status, request_id, raw = (requester or generator.request_review)(body, api_key)
        (output / "decomposition_raw.json").write_bytes(raw)
        manifest.update(http_status=status, provider_request_id=request_id, response_sha256=sha256(raw))
        if status != 200:
            raise RuntimeError(f"Provider HTTP status {status}; see decomposition_raw.json.")
        phase = "response"
        response = json.loads(raw, object_pairs_hook=unique_object)
        if not isinstance(response, dict):
            raise ValueError("Provider response must be a JSON object.")
        manifest.update(model_returned=response.get("model"), usage=response.get("usage"),
                        response_id=response.get("id"),
                        system_fingerprint=response.get("system_fingerprint"))
        if response.get("error"):
            raise RuntimeError("Provider reported an error; see decomposition_raw.json.")
        document = parse_response(response)
        manifest["finish_reason"] = "stop"
        claims = pilot_profile.validate(document, "P", finding, no_context_fields)
        validation.update(status="passed", claim_count=len(claims))
        phase = "save"
        rows = [{"profile_version": PROFILE_VERSION, "route": "P", "run_id": run_id,
                 "finding_id": finding_id, **claim} for claim in claims]
        temporary = output / "claims.jsonl.tmp"
        temporary.write_bytes("".join(json.dumps(row, ensure_ascii=False) + "\n"
                                      for row in rows).encode("utf-8"))
        temporary.rename(output / "claims.jsonl")
        manifest.update(status="completed" if claims else "no_claims", claim_count=len(claims))
    except (ValueError, TypeError, KeyError) as error:
        status = "invalid_output" if phase == "response" else "run_error"
        manifest.update(status=status, error=f"{type(error).__name__}: {error}")
        if status == "invalid_output":
            validation.update(status="failed", errors=[str(error)])
    except (OSError, HTTPException, RuntimeError) as error:
        manifest.update(status="run_error", error=f"{type(error).__name__}: {error}")
    finally:
        if manifest["status"] == "running":
            manifest.update(status="run_error", error="Decomposition interrupted before completion.")
        manifest.update(duration_seconds=round(time.monotonic() - started, 3),
                        finished_at=datetime.now(timezone.utc).isoformat())
        (output / "validation.json").write_bytes(json_bytes(validation))
        (output / "run_manifest.json").write_bytes(json_bytes(manifest))
    return manifest["status"]


# Liest Finding-Auswahl und explizite Modell-/Budgetparameter und startet einen Lauf.
# Meldet gespeicherte Fehler mit Exit-Code 1; erfolgreich bedeutet nur formal gültige Claims.
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--findings", type=Path, required=True, help="Saved findings.jsonl beside its original manifest, request and raw response.")
    parser.add_argument("--finding-id", required=True, help="A finding_id, or all for one extraction of the complete report.")
    parser.add_argument("--output", type=Path, required=True, help="New run directory under data/.")
    parser.add_argument("--model", required=True, help="Explicit OpenAI model ID.")
    parser.add_argument("--max-output-tokens", type=int, required=True, help="Output budget including reasoning.")
    parser.add_argument("--no-reasoning", action="store_true", help="Send reasoning_effort=none; requires a model supporting none.")
    parser.add_argument("--no-context-fields", action="store_true", help="Planned context-field ablation.")
    args = parser.parse_args()
    try:
        status = decompose_findings(args.findings, args.finding_id, args.output, args.model,
                                    args.max_output_tokens, args.no_reasoning, args.no_context_fields)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Could not start decomposition: {error}\n")
    print(f"Decomposition status: {status}; saved at {args.output.resolve()}")
    if status not in ("completed", "no_claims"):
        manifest = json.loads((args.output / "run_manifest.json").read_bytes())
        parser.exit(1, f"Decomposition did not complete: {manifest.get('error', status)}\n"
                       "See run_manifest.json and validation.json. No automatic retry.\n")


if __name__ == "__main__":
    main()
