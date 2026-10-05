"""Generate direct claims from the exact source context of a saved prose review."""

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
PROMPT = Path(__file__).resolve().parents[1] / "resources" / "direct_claim_prompt.txt"


# Liest einen erfolgreichen direkten Vorgänger und gleicht seine Claims mit der Rohantwort ab.
# Liefert ausschließlich validierte Modellclaims, niemals Annotationen, Reportinhalte oder Metadaten als Input.
def load_prior(path: Path, files: dict, case_id: str, case_variant: str) -> dict:
    manifest_bytes = review_pair.read_artifact(path / "run_manifest.json")
    manifest = json.loads(manifest_bytes, object_pairs_hook=claim_profile.unique_object)
    raw = review_pair.read_artifact(path / "generation_raw.json")
    request_bytes = review_pair.read_artifact(path / "request.json")
    if (manifest.get("route") != "D" or manifest.get("stage") != "direct_claims"
            or manifest.get("profile_variant", "full") != "full"
            or manifest.get("status") not in ("completed", "no_claims")
            or manifest.get("case_id") != case_id or manifest.get("case_variant") != case_variant
            or manifest.get("source_sha256") != {n: sha256(b) for n, b in files.items()}
            or manifest.get("response_sha256") != sha256(raw)
            or manifest.get("request_sha256") != sha256(request_bytes)):
        raise ValueError("Revision needs a matching, successful original direct run.")
    request = json.loads(request_bytes)
    if request["messages"][1]["content"] != generator.format_sources(files):
        raise ValueError("Prior D code context differs.")
    document = claim_profile.parse_response(json.loads(raw, object_pairs_hook=claim_profile.unique_object))
    claims = claim_profile.validate_claims(document, "D")
    return {"manifest": manifest, "manifest_bytes": manifest_bytes,
            "claims_bytes": json_bytes({"profile_version": "0.1", "route": "D", "claims": claims})}


# Prüft die Paarung vor dem Start und erzeugt einmal direkt Claims aus exakt den P-Quellbytes.
# Speichert Eingaben, Ressourcen, Request, Rohantwort und Metadaten ohne Überschreiben oder Retry.
# Formale Fehler liefern keine Teilclaims; unauflösbare Codebezüge bleiben separate Diagnosen.
def generate_claims(model_input: Path, review_run: Path, output: Path, model: str,
                    max_output_tokens: int, disable_reasoning: bool = False,
                    case_id: str = generator.CASE_ID, case_variant: str = "unspecified",
                    no_context_fields: bool = False, prior_run: Path = None, requester=None) -> str:
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output already exists: {output}. Choose a new --output path.")
    if not model or "/" in model or model.endswith(":free") or any(char.isspace() for char in model):
        raise ValueError("Select an explicit OpenAI model ID (without an OpenRouter prefix or :free suffix).")
    if max_output_tokens < 1:
        raise ValueError("A positive max-output-tokens value is required.")
    parent = review_pair.load_review(review_run) if review_run is not None else None
    if parent is not None:
        case_id = parent["manifest"]["case_id"]
        case_variant = parent["manifest"].get("case_variant", "unspecified")
    elif case_id == generator.CASE_ID:
        raise ValueError("Independent D requires a registered pilot snapshot; legacy D needs review-run.")
    files = generator.load_sources(model_input, case_id)
    generator.verify_variant(files, case_id, case_variant)
    if parent is not None:
        review_pair.verify_sources(files, parent)
    resources = pilot_profile.resources(PROMPT, no_context_fields)
    prior = None
    if prior_run is not None:
        if no_context_fields:
            raise ValueError("Revision is planned only for the full profile.")
        prior = load_prior(prior_run, files, case_id, case_variant)
        revision_prompt = PROMPT.parent / "revision_prompt.txt"
        resources[revision_prompt.name] = revision_prompt.read_bytes()
    system = (resources[PROMPT.name].decode("utf-8")
              + "\n\nCODEBOOK\n" + resources[claim_profile.CODEBOOK.name].decode("utf-8")
              + "\n\nRESPONSE SCHEMA\n" + resources[claim_profile.SCHEMA.name].decode("utf-8"))
    if prior is not None:
        system += "\n\n" + resources["revision_prompt.txt"].decode("utf-8")
    user = generator.format_sources(files)
    if prior is not None:
        user += "\n\nPRIOR DIRECT CLAIMS (model output; check against the code)\n" + prior["claims_bytes"].decode("utf-8")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
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
        "run_id": run_id, "route": "D", "stage": "direct_revision" if prior else "direct_claims",
        "profile_variant": "no_context_fields" if no_context_fields else "full",
        "case_id": case_id,
        "case_variant": case_variant,
        "parent_run_id": prior["manifest"]["run_id"] if prior else None,
        "paired_review_run_id": parent["manifest"]["run_id"] if parent else None,
        "profile_version": claim_profile.PROFILE_VERSION,
        "codebook_version": claim_profile.CODEBOOK_VERSION,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "provider": "openai", "endpoint": generator.ENDPOINT,
        "model_requested": model,
        "parameters": {key: value for key, value in payload.items() if key != "messages"},
        "review_manifest_sha256": sha256(parent["manifest_bytes"]) if parent else None,
        "review_request_sha256": sha256(parent["request_bytes"]) if parent else None,
        "review_findings_sha256": sha256(parent["findings_bytes"]) if parent else None,
        "source_sha256": {name: sha256(content) for name, content in files.items()},
        "resource_sha256": {name: sha256(content) for name, content in resources.items()},
        "implementation_sha256": {
            path.name: sha256(path.read_bytes()) for path in (
                Path(__file__), Path(generator.__file__), Path(generator.prepare_case.__file__),
                Path(claim_profile.__file__), Path(review_pair.__file__),
                Path(pilot_profile.__file__), Path(generator.case_context.__file__))},
        "request_sha256": sha256(body), "timeout_seconds": generator.TIMEOUT_SECONDS,
        "request_attempts": 0, "status": "running", "usage": None, "cost_usd": None,
    }
    validation = {
        "status": "not_run", "claim_count": None, "errors": [], "code_ref_checks": [],
        "scope": "Format and local references; code locations are diagnostics, not truth judgments.",
    }
    output.mkdir(parents=True)
    (output / "run_manifest.json").write_bytes(json_bytes(manifest))
    started = time.monotonic()
    phase = "setup"
    try:
        for name, content in files.items():
            target = output / "model_input" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        for name, content in resources.items():
            (output / name).write_bytes(content)
        if parent is not None:
            (output / "review_manifest.json").write_bytes(parent["manifest_bytes"])
        if prior is not None:
            (output / "prior_manifest.json").write_bytes(prior["manifest_bytes"])
            (output / "prior_claims.json").write_bytes(prior["claims_bytes"])
        (output / "request.json").write_bytes(body)
        api_key = generator.load_api_key()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing from the environment and project .env.")
        phase = "request"
        manifest["request_attempts"] = 1
        (output / "run_manifest.json").write_bytes(json_bytes(manifest))
        status, request_id, raw = (requester or generator.request_review)(body, api_key)
        (output / "generation_raw.json").write_bytes(raw)
        manifest.update(http_status=status, provider_request_id=request_id, response_sha256=sha256(raw))
        if status != 200:
            raise RuntimeError(f"Provider HTTP status {status}; see generation_raw.json.")
        phase = "response"
        response = json.loads(raw, object_pairs_hook=claim_profile.unique_object)
        if not isinstance(response, dict):
            raise ValueError("Provider response must be a JSON object.")
        manifest.update(model_returned=response.get("model"), usage=response.get("usage"),
                        response_id=response.get("id"),
                        system_fingerprint=response.get("system_fingerprint"))
        if response.get("error"):
            raise RuntimeError("Provider reported an error; see generation_raw.json.")
        document = claim_profile.parse_response(response)
        manifest["finish_reason"] = "stop"
        claims = pilot_profile.validate(document, "D", no_context_fields=no_context_fields)
        checks = claim_profile.check_code_refs(claims, files)
        validation.update(status="passed", claim_count=len(claims), code_ref_checks=checks)
        phase = "save"
        rows = [{"profile_version": claim_profile.PROFILE_VERSION,
                 "route": "D", "run_id": run_id, **claim} for claim in claims]
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
            manifest.update(status="run_error", error="Direct generation interrupted before completion.")
        manifest.update(duration_seconds=round(time.monotonic() - started, 3),
                        finished_at=datetime.now(timezone.utc).isoformat())
        (output / "validation.json").write_bytes(json_bytes(validation))
        (output / "run_manifest.json").write_bytes(json_bytes(manifest))
    return manifest["status"]


# Liest Fallkontext, zugehörigen Review und explizite Modell-/Budgetparameter für einen D-Lauf.
# Meldet Start- und gespeicherte Lauffehler mit Exit-Code 1; führt keine Wiederholung aus.
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-input", type=Path,
                        default=Path("data") / generator.CASE_ID / "model_input")
    parser.add_argument("--review-run", type=Path,
                        help="Saved prose review whose exact source context is required.")
    parser.add_argument("--output", type=Path, required=True, help="New run directory under data/.")
    parser.add_argument("--model", required=True, help="Explicit OpenAI model ID.")
    parser.add_argument("--max-output-tokens", type=int, required=True,
                        help="Output budget including reasoning.")
    parser.add_argument("--no-reasoning", action="store_true",
                        help="Send reasoning_effort=none; requires a model supporting none.")
    parser.add_argument("--case-id", default=generator.CASE_ID)
    parser.add_argument("--case-variant", default="unspecified")
    parser.add_argument("--no-context-fields", action="store_true")
    parser.add_argument("--prior-run", type=Path, help="Completed direct run to revise once.")
    args = parser.parse_args()
    try:
        status = generate_claims(args.model_input, args.review_run, args.output, args.model,
                                 args.max_output_tokens, args.no_reasoning, args.case_id, args.case_variant,
                                 args.no_context_fields, args.prior_run)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Could not start direct generation: {error}\n")
    print(f"Direct generation status: {status}; saved at {args.output.resolve()}")
    if status not in ("completed", "no_claims"):
        manifest = json.loads((args.output / "run_manifest.json").read_bytes())
        parser.exit(1, f"Direct generation did not complete: {manifest.get('error', status)}\n"
                       "See run_manifest.json and validation.json. No automatic retry.\n")


if __name__ == "__main__":
    main()
