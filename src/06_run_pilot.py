"""Validate and plan the small pilot; model calls require --execute and a budget."""

import argparse
from datetime import datetime, timezone
from importlib import import_module
import json
import math
from pathlib import Path
import random
import time

import case_context

generator = import_module("02_generate_findings")
decomposer = import_module("03_decompose_findings")
direct = import_module("04_generate_claims")
CONFIG = Path(__file__).resolve().parents[1] / "resources" / "pilot_config.json"


# Lädt die konkrete Pilotkonfiguration; Änderungen erfordern eine bewusste neue Protokollversion.
# Kein Modell-Fallback, keine Konfiguration aus Referenz- oder Modelldateien.
def load_config() -> dict:
    config = json.loads(CONFIG.read_bytes())
    if (config["model"] != "gpt-5.4-mini-2026-03-17"
            or config["reasoning_effort"] != "none" or config["service_tier"] != "default"
            or config["repetitions"] != 2
            or config["usd_per_million_tokens"] != {"input": .75, "cached_input": .075, "output": 4.5}):
        raise ValueError("Pilot configuration changed; review protocol and cost guard before running.")
    return config


# Prüft alle zehn Kontextpakete und legt Reihenfolge, Paarung und Zusatzversuche vorab fest.
# Schreibt nichts; jeder Kernvergleich hat zwei balancierte Wiederholungen, keine Ergebnisauswahl.
def make_plan(cases_root: Path) -> dict:
    config = load_config()
    catalog = case_context.load_catalog()
    contexts = []
    for case in catalog["cases"]:
        for variant in ("vulnerable", "fixed"):
            source = cases_root / case["case_id"] / variant / "model_input"
            files = generator.load_sources(source, case["case_id"])
            generator.verify_variant(files, case["case_id"], variant)
            contexts.append({"case_id": case["case_id"], "case_variant": variant,
                             "model_input": str(source.resolve()),
                             "source_sha256": {p: generator.sha256(b) for p, b in files.items()},
                             "code_context_sha256": generator.sha256(generator.format_sources(files).encode())})
    random.Random(config["order_seed"]).shuffle(contexts)
    jobs = []
    for repeat in range(1, config["repetitions"] + 1):
        for index, context in enumerate(contexts):
            base = f"{context['case_id']}/{context['case_variant']}/repeat-{repeat}"
            order = ["P_report", "P_claims", "D"] if (index + repeat) % 2 else ["D", "P_report", "P_claims"]
            for stage in order:
                jobs.append({**context, "repeat": repeat, "stage": stage, "id": f"{base}/{stage}",
                             "depends_on": f"{base}/P_report" if stage == "P_claims" else None})
    # Secondary comparisons use the first repeat; sharing P's report isolates the extraction change.
    for context in contexts:
        base = f"{context['case_id']}/{context['case_variant']}/repeat-1"
        jobs.append({**context, "repeat": 1, "stage": "D_revision", "id": f"{base}/D_revision",
                     "depends_on": f"{base}/D"})
        if context["case_id"] in config["subset_cases"]:
            for stage in ("P_no_context", "D_no_context", "P_baselines"):
                jobs.append({**context, "repeat": 1, "stage": stage, "id": f"{base}/{stage}",
                             "depends_on": f"{base}/P_report" if stage.startswith("P") else None})
    root = Path(__file__).resolve().parents[1]
    snapshots = [p for folder in (root / "src", root / "resources") for p in folder.rglob("*")
                 if p.is_file() and "__pycache__" not in p.parts]
    snapshots.extend(root / "docs" / name for name in ("PILOT_PROTOCOL.md", "PILOT_CASES.md"))
    return {"config": config, "contexts": contexts, "jobs": jobs,
            "implementation_resource_sha256": {str(p.relative_to(root)): generator.sha256(p.read_bytes())
                                                for p in sorted(snapshots)},
            "core_calls_max": 60, "revision_calls_max": 10, "ablation_calls_max": 8,
            "baseline_calls": "One per sentence in four complete first-repeat reports; unknown before P.",
            "annotation_status": "human_references_and_double_annotation_pending",
            "scientific_results": "not_evaluated"}


# Begrenzt diesen seriellen Lauf konservativ: UTF-8-Bytes plus Overhead als Input-Obergrenze,
# volles Outputlimit und ungecachter Standardpreis. Reservierungen werden niemals zurückgebucht.
# Persistiert vor jedem Request; bei unklarer Abrechnung/Transport stoppt der restliche Lauf.
class BudgetGuard:
    # Legt ein neues Budgetjournal an; ein vorheriger Lauf wird nie fortgesetzt oder überschrieben.
    def __init__(self, path: Path, limit: float, config: dict):
        if not math.isfinite(limit) or limit <= 0:
            raise ValueError("A finite positive USD limit is required.")
        self.path, self.limit, self.config = path, limit, config
        self.reserved = 0.0
        self.entries = []
        self.stop_reason = None
        self.save()

    # Schreibt Reservierungen und gemeldeten Verbrauch ohne Zugangsdaten atomar ins lokale Journal.
    def save(self) -> None:
        temporary = self.path.with_suffix(".tmp")
        temporary.write_bytes(generator.json_bytes({"limit_usd": self.limit,
            "reserved_upper_usd": self.reserved, "stop_reason": self.stop_reason, "calls": self.entries}))
        temporary.replace(self.path)

    # Sendet höchstens einen vorab budgetierten Request und gibt unveränderte Transportdaten zurück.
    # Ungewisse Kosten bleiben reserviert; keine automatischen Wiederholungen oder Modellwechsel.
    def request(self, body: bytes, key: str) -> tuple:
        payload = json.loads(body)
        if (payload.get("model") != self.config["model"] or payload.get("reasoning_effort") != "none"
                or payload.get("service_tier") != "default" or payload.get("tools")):
            raise ValueError("Request differs from the fixed pilot model, effort or service tier.")
        byte_bound = sum(len(m["content"].encode("utf-8")) for m in payload["messages"]) + 1024
        output_limit = payload["max_completion_tokens"]
        if not isinstance(output_limit, int) or isinstance(output_limit, bool) or output_limit < 1:
            raise ValueError("Invalid completion limit.")
        reservation = (byte_bound * .75 + output_limit * 4.5) / 1_000_000
        if byte_bound > 272_000 or byte_bound + output_limit > 400_000:
            self.stop_reason = "Conservative input/context bound exceeded; inspect before a new run."
        if self.reserved + reservation > self.limit:
            self.stop_reason = "Budget reservation would exceed the approved ceiling."
        if self.stop_reason:
            self.save()
            raise RuntimeError(self.stop_reason)
        entry = {"request_sha256": generator.sha256(body), "input_token_upper_bound": byte_bound,
                 "max_completion_tokens": output_limit, "reserved_usd": reservation,
                 "status": "reserved", "usage": None, "estimated_usage_cost_usd": None}
        self.reserved += reservation
        self.entries.append(entry)
        self.save()
        started = time.monotonic()
        try:
            result = generator.request_review(body, key)
            status, request_id, raw = result
            entry.update(status="returned", http_status=status, provider_request_id=request_id)
            try:
                response = json.loads(raw)
                usage = response.get("usage")
                entry["usage"] = usage
                prompt, completion = usage["prompt_tokens"], usage["completion_tokens"]
                cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0)
                if any(type(n) is not int or n < 0 for n in (prompt, completion, cached)) or cached > prompt:
                    raise ValueError("Invalid usage.")
                entry["estimated_usage_cost_usd"] = ((prompt-cached)*.75 + cached*.075 + completion*4.5)/1_000_000
                if prompt > byte_bound or completion > output_limit:
                    self.stop_reason = "Provider usage exceeds conservative reservation; inspect billing."
            except (ValueError, KeyError, TypeError, AttributeError):
                self.stop_reason = "Usage missing or invalid; cost remains reserved."
            if status != 200:
                self.stop_reason = f"Provider HTTP {status}; inspect response before another paid call."
            return result
        except BaseException:
            entry["status"] = "transport_uncertain"
            self.stop_reason = "Interrupted/failed transport; cost remains reserved."
            raise
        finally:
            entry["duration_seconds"] = round(time.monotonic() - started, 3)
            self.save()


# Plant standardmäßig ohne API. Bei --execute arbeitet sie die feste Liste einmal seriell ab.
# Unabhängige Routen laufen nach Formatfehlern weiter; abhängige und budgetgesperrte Schritte bleiben sichtbar.
def run_pilot(cases_root: Path, output: Path, execute: bool = False, budget_usd: float = None) -> dict:
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output already exists: {output}")
    plan = make_plan(cases_root)
    if execute:
        if budget_usd is None or not math.isfinite(budget_usd) or budget_usd <= 0:
            raise ValueError("--execute requires an explicit positive --budget-usd.")
        if not generator.load_api_key():
            raise ValueError("OPENAI_API_KEY is missing; no request sent.")
    output.mkdir(parents=True)
    (output / "plan.json").write_bytes(generator.json_bytes(plan))
    (output / "PILOT_PROTOCOL.md").write_bytes((CONFIG.parent.parent / "docs" / "PILOT_PROTOCOL.md").read_bytes())
    manifest = {"started_at": datetime.now(timezone.utc).isoformat(),
                "mode": "execute" if execute else "dry_run", "status": "planned",
                "plan_sha256": generator.sha256((output / "plan.json").read_bytes()), "jobs": []}
    (output / "pilot_manifest.json").write_bytes(generator.json_bytes(manifest))
    if not execute:
        return manifest
    config = plan["config"]
    guard = BudgetGuard(output / "budget_ledger.json", budget_usd, config)
    results = {}
    manifest["status"] = "running"
    try:
        for job in plan["jobs"]:
            stage, job_id = job["stage"], job["id"]
            target = output / "runs" / job_id
            dependency = job["depends_on"]
            dependency_status = results.get(dependency)
            if guard.stop_reason:
                status = "not_run_budget_or_transport_stop"
            elif dependency and dependency_status not in ("completed", "no_findings", "no_claims"):
                status = "not_run_parent_failed"
            elif dependency_status == "no_findings" and stage in ("P_claims", "P_no_context"):
                status = "no_report_no_claims"
            else:
                common = {"model": config["model"], "disable_reasoning": True, "requester": guard.request}
                context = Path(job["model_input"])
                token_limits = config["max_output_tokens"]
                parent_path = output / "runs" / dependency if dependency else None
                if stage == "P_report":
                    status = generator.generate_findings(context, target, max_output_tokens=token_limits["report"],
                        case_id=job["case_id"], case_variant=job["case_variant"], **common)
                elif stage in ("P_claims", "P_no_context"):
                    status = decomposer.decompose_findings(parent_path / "findings.jsonl", "all", target,
                        max_output_tokens=token_limits["claims"], no_context_fields=stage == "P_no_context", **common)
                elif stage == "P_baselines":
                    from extraction_baselines import run_baselines
                    status = run_baselines(parent_path, target, config["model"], token_limits["baseline"], guard.request)
                else:
                    status = direct.generate_claims(context, None, target,
                        max_output_tokens=token_limits["claims"], case_id=job["case_id"],
                        case_variant=job["case_variant"], no_context_fields=stage == "D_no_context",
                        prior_run=parent_path if stage == "D_revision" else None, **common)
            results[job_id] = status
            manifest["jobs"].append({"id": job_id, "status": status})
            (output / "pilot_manifest.json").write_bytes(generator.json_bytes(manifest))
        successes = {"completed", "no_findings", "no_claims", "no_report_no_claims"}
        manifest["status"] = "completed" if all(s in successes for s in results.values()) else "completed_with_failures"
    finally:
        if manifest["status"] == "running":
            manifest["status"] = "interrupted"
        manifest.update(finished_at=datetime.now(timezone.utc).isoformat(), stop_reason=guard.stop_reason,
                        scientific_results="not_evaluated; human annotation required")
        (output / "pilot_manifest.json").write_bytes(generator.json_bytes(manifest))
    return manifest


# Liest lokale Pfade und die explizite Live-/Budgetwahl; ohne --execute gibt es keine Modellaufrufe.
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path("data/pilot_cases"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--budget-usd", type=float)
    args = parser.parse_args()
    try:
        result = run_pilot(args.cases, args.output, args.execute, args.budget_usd)
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"Pilot not started/completed: {error}\n")
    print(f"Pilot: {result['status']}; {args.output.resolve()}")
    if result["status"] not in ("planned", "completed"):
        parser.exit(1, "Inspect pilot_manifest.json; no automatic retry.\n")


if __name__ == "__main__":
    main()
