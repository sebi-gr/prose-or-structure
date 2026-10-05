"""Offline integration checks for registered pilot contexts and complete P/D routes."""

from importlib import import_module
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import case_context

generator = import_module("02_generate_findings")
decomposer = import_module("03_decompose_findings")
direct = import_module("04_generate_claims")


def make_catalog(root):
    path = "src/Example.java"
    catalog = {"dataset": {"url": f"https://raw.githubusercontent.com/example/dataset/{'a' * 40}/data.csv",
                            "sha256": "a" * 64}, "cases": []}
    cases_root = root / "cases"
    for index, case_id in enumerate(("VUL4J-15", "VUL4J-64", "VUL4J-41", "VUL4J-43", "VUL4J-76"), 1):
        variants = {}
        for name, revision in (("vulnerable", f"{index:040x}"), ("fixed", f"{index + 10:040x}")):
            content = f"// SYNTHETIC_CODE_ONLY_{case_id}_{name}\r\n// 🙂 second line\r\n".encode()
            target = cases_root / case_id / name / "model_input" / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            variants[name] = {"revision": revision, "files": [{"path": path,
                "url": f"https://raw.githubusercontent.com/example/project/{revision}/{path}",
                "sha256": generator.sha256(content)}]}
        catalog["cases"].append({"case_id": case_id, "repo": "example/project",
            "weakness": "SYNTHETIC_REFERENCE_LABEL", "split": "pilot", "references": [],
            "case_commit": variants["vulnerable"]["revision"], "fix_commit": variants["fixed"]["revision"],
            "selection_reason": "Synthetic fixture.", "context_limits": "Synthetic local context.",
            "variants": variants})
    catalog_path = root / "catalog.json"
    catalog_path.write_bytes(generator.json_bytes(catalog))
    return catalog_path, cases_root


def claim_fixture(route="D", quote=None, no_context=False):
    claim = {"claim_id": "C01", "proposition": "An effect could occur if enabled.",
        "family": "exploitability_impact", "subtype": "impact", "family_reason": "Conditional effect.",
        "context": {key: None for key in ("actor", "preconditions", "negation", "modality", "quantifier", "scope")},
        "source_quotes": [] if route == "D" else [{"field": "report", "quote": quote, "occurrence": 1}],
        "code_refs": [], "context_claim_ids": [], "verification": {
            "question": "Could this occur if enabled?", "required_evidence": ["Code and configuration."],
            "assumptions": []}}
    if no_context:
        del claim["context"]
    return claim


def response(document):
    return (200, "synthetic-request", generator.json_bytes({"model": "test-model",
        "usage": {"prompt_tokens": 10, "completion_tokens": 20}, "choices": [{
            "finish_reason": "stop", "message": {"role": "assistant", "content": json.dumps(document)}}]}))


class PilotRouteTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.catalog_path, self.cases = make_catalog(self.root)
        for mocked in (patch.object(case_context, "CATALOG", self.catalog_path),
                       patch.object(generator, "load_api_key", return_value="synthetic-key"),
                       patch.object(generator, "request_review", side_effect=AssertionError("No network"))):
            mocked.start()
            self.addCleanup(mocked.stop)
        self.case_id = "VUL4J-15"
        self.source = self.cases / self.case_id / "vulnerable" / "model_input"
        self.review = self.root / "review"
        self.findings = [{"title": "First title", "report": "🙂 First effect.\r\nOnly if enabled."},
                         {"title": "Second title", "report": "Second effect is not established."}]

    def create_review(self):
        requester = Mock(return_value=response({"findings": self.findings}))
        self.assertEqual(generator.generate_findings(self.source, self.review, "test-model", 200,
            case_id=self.case_id, case_variant="vulnerable", requester=requester), "completed")
        return requester

    def test_multiple_cases_use_exact_registered_paths_and_pinned_variant_hashes(self):
        for case_id in ("VUL4J-15", "VUL4J-41"):
            source = self.cases / case_id / "vulnerable" / "model_input"
            (source / "REFERENCE_MUST_NOT_BE_SENT.txt").write_text("SYNTHETIC_REFERENCE_LABEL")
            requester = Mock(return_value=response({"findings": []}))
            output = self.root / f"review-{case_id}"
            self.assertEqual(generator.generate_findings(source, output, "test-model", 200,
                case_id=case_id, case_variant="vulnerable", requester=requester), "no_findings")
            sent = requester.call_args.args[0]
            self.assertNotIn(b"SYNTHETIC_REFERENCE_LABEL", sent)
            manifest = json.loads((output / "run_manifest.json").read_bytes())
            self.assertEqual(manifest["case_id"], case_id)
            self.assertEqual(set(manifest["source_sha256"]), {"src/Example.java"})
        output = self.root / "wrong-variant"
        requester = Mock()
        with self.assertRaises(ValueError):
            generator.generate_findings(self.source, output, "test-model", 200,
                case_id=self.case_id, case_variant="fixed", requester=requester)
        requester.assert_not_called()
        self.assertFalse(output.exists())

    def test_complete_p_report_keeps_both_findings_quotes_and_no_code(self):
        self.create_review()
        claims = [dict(claim_fixture("P", item["report"]), claim_id=f"C{index:02d}")
                  for index, item in enumerate(self.findings, 1)]
        requester = Mock(return_value=response({"profile_version": "0.1", "route": "P", "claims": claims}))
        output = self.root / "p-claims"
        with patch.object(generator, "load_sources", side_effect=AssertionError("P must not read source")):
            self.assertEqual(decomposer.decompose_findings(self.review / "findings.jsonl", "all", output,
                "test-model", 500, requester=requester), "completed")
        requester.assert_called_once()
        payload = json.loads(requester.call_args.args[0])
        finding = json.loads(payload["messages"][1]["content"])
        for item in self.findings:
            self.assertIn(item["title"], finding["report"])
            self.assertIn(item["report"], finding["report"])
        self.assertNotIn("SYNTHETIC_CODE_ONLY", requester.call_args.args[0].decode())
        self.assertNotIn("SYNTHETIC_REFERENCE_LABEL", requester.call_args.args[0].decode())
        saved = [json.loads(line) for line in (output / "claims.jsonl").read_text().splitlines()]
        for claim in saved:
            quote = claim["source_quotes"][0]
            self.assertEqual(finding[quote["field"]][quote["start"]:quote["end"]], quote["quote"])
        self.assertEqual(json.loads((output / "run_manifest.json").read_bytes())["report_unit"], "all_findings_v1")

    def test_independent_d_can_precede_p_and_revision_reads_only_original_claims(self):
        original = self.root / "d-first"
        document = {"profile_version": "0.1", "route": "D", "claims": [claim_fixture()]}
        requester = Mock(return_value=response(document))
        with patch.object(direct.review_pair, "load_review", side_effect=AssertionError("No P dependency")):
            self.assertEqual(direct.generate_claims(self.source, None, original, "test-model", 500,
                case_id=self.case_id, case_variant="vulnerable", requester=requester), "completed")
        self.assertFalse(self.review.exists())
        sent = json.loads(requester.call_args.args[0])
        self.assertEqual(sent["messages"][1]["content"], generator.format_sources(
            generator.load_sources(self.source, self.case_id)))
        (original / "annotations.json").write_text("ANNOTATION_MUST_NOT_BE_SENT")
        (original / "claims.jsonl").write_text("MUTATED_DERIVED_FILE_MUST_NOT_BE_SENT")
        revised = self.root / "d-revised"
        revision_requester = Mock(return_value=response(document))
        self.assertEqual(direct.generate_claims(self.source, None, revised, "test-model", 500,
            case_id=self.case_id, case_variant="vulnerable", prior_run=original,
            requester=revision_requester), "completed")
        sent = revision_requester.call_args.args[0].decode()
        self.assertIn(document["claims"][0]["proposition"], sent)
        self.assertNotIn("ANNOTATION_MUST_NOT_BE_SENT", sent)
        self.assertNotIn("MUTATED_DERIVED_FILE_MUST_NOT_BE_SENT", sent)
        self.assertNotIn("SYNTHETIC_REFERENCE_LABEL", sent)
        manifest = json.loads((revised / "run_manifest.json").read_bytes())
        self.assertEqual(manifest["stage"], "direct_revision")
        self.assertEqual(manifest["parent_run_id"], json.loads((original / "run_manifest.json").read_bytes())["run_id"])
        rejected = self.root / "wrong-revision"
        other = self.cases / self.case_id / "fixed" / "model_input"
        revision_requester.reset_mock()
        with self.assertRaises(ValueError):
            direct.generate_claims(other, None, rejected, "test-model", 500,
                case_id=self.case_id, case_variant="fixed", prior_run=original, requester=revision_requester)
        revision_requester.assert_not_called()
        self.assertFalse(rejected.exists())

    def test_both_route_ablations_save_claims_without_fabricated_context(self):
        self.create_review()
        for route in ("P", "D"):
            claim = claim_fixture(route, self.findings[0]["report"], no_context=True)
            requester = Mock(return_value=response({"profile_version": "0.1", "route": route, "claims": [claim]}))
            output = self.root / f"ablation-{route}"
            if route == "P":
                status = decomposer.decompose_findings(self.review / "findings.jsonl", "all", output,
                    "test-model", 500, no_context_fields=True, requester=requester)
            else:
                status = direct.generate_claims(self.source, None, output, "test-model", 500,
                    case_id=self.case_id, case_variant="vulnerable", no_context_fields=True, requester=requester)
            self.assertEqual(status, "completed")
            row = json.loads((output / "claims.jsonl").read_bytes())
            self.assertNotIn("context", row)
            self.assertIn("context_claim_ids", row)
            self.assertEqual(json.loads((output / "run_manifest.json").read_bytes())["profile_variant"], "no_context_fields")
            schema = json.loads((output / "claim_profile.schema.json").read_bytes())
            self.assertNotIn("context", schema["$defs"]["claim"]["properties"])


if __name__ == "__main__":
    unittest.main()
