"""Two small report-extraction baselines; no code verification or live defaults."""

from datetime import datetime, timezone
from importlib import import_module
import json
from pathlib import Path
import re
import time
from uuid import uuid4

import claim_profile
import review_pair

generator = import_module("02_generate_findings")
RESOURCES = Path(__file__).resolve().parents[1] / "resources" / "baselines"
RESOURCE_NAMES = ("veriscore_extraction_non_qa.txt", "VERISCORE_LICENSE",
                  "provenance.json", "README.md")
SYSTEM_MESSAGE = (
    "You are a helpful assistant who can extract verifiable atomic claims from a piece of text. "
    "Each atomic fact should be verifiable against reliable external world knowledge (e.g., via Wikipedia)"
)
BOUNDARY = re.compile(r"(?<=[.!?])\s+|\r?\n")


# Zerlegt einen Originaltext deterministisch; gibt exakte Teiltexte und Unicode-Offsets zurück.
# Einfache Interpunktion/Zeilenumbrüche ersetzen spaCy; Abkürzungen bleiben eine dokumentierte Grenze.
def sentence_spans(text: str) -> list:
    spans = []
    start = 0
    ends = [(match.start(), match.end()) for match in BOUNDARY.finditer(text)]
    for end, next_start in [*ends, (len(text), len(text))]:
        left = start
        right = end
        while left < right and text[left].isspace():
            left += 1
        while right > left and text[right - 1].isspace():
            right -= 1
        if left < right:
            spans.append({"quote": text[left:right], "start": left, "end": right})
        start = next_start
    return spans


# Erstellt beide Baseline-Eingaben nur aus gespeicherten Titel-/Reporttexten.
# Satzclaims behalten Originalspans; VeriScore-Aufträge enthalten jeden Titel-/Reportsatz genau einmal.
def prepare_units(findings: list) -> tuple:
    sentence_claims, jobs = [], []
    for finding in findings:
        for field in ("title", "report"):
            spans = sentence_spans(finding[field])
            sentences = [span["quote"] for span in spans]
            for index, span in enumerate(spans):
                sentence_claims.append({
                    "claim_id": f"S{len(sentence_claims) + 1:04d}",
                    "finding_id": finding["finding_id"], "proposition": span["quote"],
                    "source_span": {"field": field, **span},
                })
                previous = " ".join(sentences[max(0, index - 3):index])
                following = " ".join(sentences[index + 1:index + 2])
                parts = [previous, f"<SOS>{span['quote']}<EOS>", following]
                if len(sentences) > 5:
                    parts.insert(0, sentences[0])
                window = " ".join(part for part in parts if part)
                snippet = (f"Title: {window}\nReport (context only): {finding['report']}" if field == "title"
                           else f"Title (context only): {finding['title']}\nReport: {window}")
                jobs.append({
                    "call_id": f"{len(jobs) + 1:04d}", "finding_id": finding["finding_id"],
                    "sentence_index": index + 1, "target_span": {"field": field, **span},
                    "snippet": snippet,
                })
    return sentence_claims, jobs


# Liest ausschließlich normal beendete Textantworten als Original-Bulletliste oder Leersentinel.
# Unbekannte Formate werden nicht repariert und keine überraschenden Textzeilen verschluckt.
def parse_extraction(response: dict) -> list:
    if not isinstance(response, dict) or response.get("error"):
        raise ValueError("Provider response must be an error-free object.")
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
        raise ValueError("Expected exactly one completion.")
    choice = choices[0]
    if choice.get("finish_reason") != "stop" or choice.get("error"):
        raise ValueError("Extraction completion did not finish normally.")
    message = choice.get("message")
    if (not isinstance(message, dict) or message.get("role") != "assistant"
            or message.get("refusal") or message.get("tool_calls") or message.get("function_call")
            or not isinstance(message.get("content"), str)):
        raise ValueError("Expected assistant text without refusal or tool calls.")
    content = message["content"].strip()
    if content == "No verifiable claim.":
        return []
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if (not lines or any(not line.startswith("- ") or not line[2:].strip()
                         or line[2:].strip() == "No verifiable claim." for line in lines)):
        raise ValueError("Expected only '- ' bullet claims or the standalone no-claim sentinel.")
    return [line[2:].strip() for line in lines]


# Schreibt eine fertig geprüfte Claimliste; Umbenennung verhindert erfolgreich aussehende Teiloutputs.
# Wird nur in einem vorher exklusiv reservierten neuen Laufverzeichnis aufgerufen.
def write_claims(path: Path, claims: list) -> None:
    content = "".join(json.dumps(claim, ensure_ascii=False) + "\n" for claim in claims).encode("utf-8")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(content)
    temporary.rename(path)


# Führt einen vorbereiteten VeriScore-Auftrag ohne Retry aus und erhält Request/Rohantwort/Metadaten.
# Gibt Status, Propositionen und Manifest zurück; erwartete Transport-/Formatfehler werden gespeichert.
def run_call(job: dict, output: Path, payload: dict, api_key: str, requester) -> tuple:
    output.mkdir()
    body = generator.json_bytes(payload)
    (output / "request.json").write_bytes(body)
    manifest = {key: value for key, value in job.items() if key != "snippet"}
    manifest.update(status="running", started_at=datetime.now(timezone.utc).isoformat(),
                    request_sha256=generator.sha256(body), request_attempts=0,
                    usage=None, cost_usd=None, endpoint=generator.ENDPOINT,
                    parameters={key: value for key, value in payload.items() if key != "messages"})
    target = output / "run_manifest.json"
    target.write_bytes(generator.json_bytes(manifest))
    started = time.monotonic()
    claims = []
    try:
        manifest["request_attempts"] = 1
        target.write_bytes(generator.json_bytes(manifest))
        status, request_id, raw = requester(body, api_key)
        (output / "generation_raw.json").write_bytes(raw)
        manifest.update(http_status=status, provider_request_id=request_id,
                        response_sha256=generator.sha256(raw))
        if status != 200:
            raise RuntimeError(f"Provider HTTP status {status}; see generation_raw.json.")
        try:
            response = json.loads(raw, object_pairs_hook=claim_profile.unique_object)
            if isinstance(response, dict):
                manifest.update(usage=response.get("usage"), model_returned=response.get("model"),
                                response_id=response.get("id"),
                                system_fingerprint=response.get("system_fingerprint"))
                if response.get("error"):
                    raise RuntimeError("Provider reported an error; see generation_raw.json.")
                choices = response.get("choices")
                if isinstance(choices, list) and choices and isinstance(choices[0], dict):
                    manifest["finish_reason"] = choices[0].get("finish_reason")
            claims = parse_extraction(response)
        except (ValueError, KeyError, TypeError, AttributeError) as error:
            manifest.update(status="invalid_output", error=f"{type(error).__name__}: {error}")
        else:
            manifest.update(status="completed", claim_count=len(claims))
    except Exception as error:
        # A caller's budget guard can stop before transport; preserve its reason without the key.
        message = str(error).replace(api_key, "[redacted]") if api_key else str(error)
        manifest.update(status="run_error", error=f"{type(error).__name__}: {message}")
    finally:
        if manifest["status"] == "running":
            manifest.update(status="run_error", error="Extraction interrupted before completion.")
        manifest.update(duration_seconds=round(time.monotonic() - started, 3),
                        finished_at=datetime.now(timezone.utc).isoformat())
        target.write_bytes(generator.json_bytes(manifest))
    return manifest["status"], claims, manifest


# Validiert einen fertigen Review und reserviert genau ein neues Baseline-Ausgabeverzeichnis.
# Bewahrt die kostenlose Satzbaseline bei API-Fehlern; VeriScore ist nur bei vollständigem Erfolg vorhanden.
# requester(body_bytes, key) ist optional für Budgetkontrolle/Offline-Tests; keine automatischen Retries.
def run_baselines(review_run: Path, output: Path, model: str,
                  max_output_tokens: int, requester=None) -> str:
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output already exists: {output}")
    if any(part.is_symlink() for part in (output.absolute(), *output.absolute().parents)):
        raise ValueError("Baseline output must not use symlinks.")
    if (not isinstance(model, str) or not model or "/" in model or model.endswith(":free")
            or any(char.isspace() for char in model)):
        raise ValueError("Select an explicit OpenAI model ID.")
    if type(max_output_tokens) is not int or max_output_tokens < 1:
        raise ValueError("A positive max_output_tokens integer is required.")
    parent = review_pair.load_review(review_run)
    resources = {name: (RESOURCES / name).read_bytes() for name in RESOURCE_NAMES}
    prompt = resources["veriscore_extraction_non_qa.txt"].decode("utf-8")
    sentence_claims, jobs = prepare_units(parent["findings"])
    run_id = str(uuid4())
    manifest = {
        "run_id": run_id, "parent_run_id": parent["manifest"]["run_id"],
        "case_id": parent["manifest"]["case_id"],
        "case_variant": parent["manifest"].get("case_variant", "unspecified"),
        "route": "P", "stage": "extraction_baselines", "status": "running",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "provider": "openai", "endpoint": generator.ENDPOINT, "model_requested": model,
        "parameters": {"reasoning_effort": "none", "max_completion_tokens": max_output_tokens,
                       "store": False, "stream": False, "service_tier": "default"},
        "input_sha256": {
            "run_manifest.json": generator.sha256(parent["manifest_bytes"]),
            "request.json": generator.sha256(parent["request_bytes"]),
            "generation_raw.json": parent["manifest"]["response_sha256"],
            "findings.jsonl": generator.sha256(parent["findings_bytes"]),
        },
        "source_sha256": parent["manifest"]["source_sha256"],
        "resource_sha256": {name: generator.sha256(content) for name, content in resources.items()},
        "implementation_sha256": generator.sha256(Path(__file__).read_bytes()),
        "review_pair_sha256": generator.sha256(Path(review_pair.__file__).read_bytes()),
        "transport_sha256": generator.sha256(Path(generator.__file__).read_bytes()),
        "sentence_baseline_status": "completed", "sentence_claim_count": len(sentence_claims),
        "planned_calls": len(jobs), "completed_calls": 0, "calls": [], "cost_usd": None,
    }
    output.mkdir(parents=True)
    (output / "resources").mkdir()
    for name, content in resources.items():
        (output / "resources" / name).write_bytes(content)
    (output / "findings.jsonl").write_bytes(parent["findings_bytes"])
    write_claims(output / "sentence_claims.jsonl", sentence_claims)
    manifest["sentence_claims_sha256"] = generator.sha256((output / "sentence_claims.jsonl").read_bytes())
    target = output / "run_manifest.json"
    target.write_bytes(generator.json_bytes(manifest))
    started = time.monotonic()
    claims = []
    deduplicated = {}
    try:
        api_key = generator.load_api_key() if jobs else ""
        if jobs and not api_key:
            raise ValueError("OPENAI_API_KEY is missing; no extraction request was sent.")
        (output / "calls").mkdir()
        for job in jobs:
            payload = {
                "model": model, **manifest["parameters"],
                "messages": [
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt.format(
                        snippet=job["snippet"], sentence=job["target_span"]["quote"])},
                ],
            }
            status, propositions, call_manifest = run_call(
                job, output / "calls" / job["call_id"], payload, api_key,
                requester if requester is not None else generator.request_review)
            manifest["calls"].append(call_manifest)
            if status != "completed":
                manifest.update(status=status, error=f"Call {job['call_id']} failed; see its manifest.")
                break
            manifest["completed_calls"] += 1
            for proposition in propositions:
                key = (job["finding_id"], proposition)
                if key not in deduplicated:
                    claim = {"claim_id": f"V{len(claims) + 1:04d}", "finding_id": job["finding_id"],
                             "proposition": proposition, "extraction_call_ids": []}
                    claims.append(claim)
                    deduplicated[key] = claim
                if job["call_id"] not in deduplicated[key]["extraction_call_ids"]:
                    deduplicated[key]["extraction_call_ids"].append(job["call_id"])
            target.write_bytes(generator.json_bytes(manifest))
        else:
            write_claims(output / "veriscore_claims.jsonl", claims)
            manifest.update(status="completed" if jobs else "no_findings",
                            veriscore_claim_count=len(claims),
                            veriscore_claims_sha256=generator.sha256(
                                (output / "veriscore_claims.jsonl").read_bytes()))
    except Exception as error:
        manifest.update(status="run_error", error=f"{type(error).__name__}: {error}")
    finally:
        if manifest["status"] == "running":
            manifest.update(status="run_error", error="Baselines interrupted before completion.")
        manifest.update(unattempted_calls=len(jobs) - len(manifest["calls"]),
                        duration_seconds=round(time.monotonic() - started, 3),
                        finished_at=datetime.now(timezone.utc).isoformat())
        target.write_bytes(generator.json_bytes(manifest))
    return manifest["status"]
