"""Offline direct-route checks with paired synthetic review artifacts."""

from copy import deepcopy
from importlib import import_module
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
direct = import_module("04_generate_claims")


def claim_fixture():
    return {
        "claim_id": "C01", "proposition": "A synthetic input reaches a local operation.",
        "family": "data_flow", "subtype": None, "family_reason": "Synthetic data flow.",
        "context": {key: None for key in (
            "actor", "preconditions", "negation", "modality", "quantifier", "scope")},
        "source_quotes": [], "code_refs": [{
            "path": direct.generator.MODEL_FILES[0], "line_start": 1,
            "line_end": 1, "symbol": None}],
        "context_claim_ids": [],
        "verification": {"question": "Does the input reach the operation?",
                         "required_evidence": ["The supplied local source."], "assumptions": []},
    }


def response_fixture(claims, route="D"):
    return {
        "id": "synthetic-response", "model": "test-model",
        "usage": {"prompt_tokens": 10, "completion_tokens": 20},
        "choices": [{"finish_reason": "stop", "message": {
            "role": "assistant", "content": json.dumps({
                "profile_version": "0.1", "route": route, "claims": claims}),
        }}],
    }


class GenerateClaimsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.model_input = self.root / "model_input"
        self.source_bytes = {}
        for index, name in enumerate(direct.generator.MODEL_FILES):
            content = f"// source {index}: 🙂\r\nsecond line\r\n".encode("utf-8")
            path = self.model_input / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            self.source_bytes[name] = content
        self.review_run = self.root / "review"
        self.output = self.root / "direct"
        self.marker = "P_REPORT_REFERENCE_MUST_NOT_BE_SENT_TO_D"
        review_response = {
            "model": "test-model", "choices": [{"finish_reason": "stop", "message": {
                "role": "assistant", "content": json.dumps({"findings": [{
                    "title": self.marker, "report": self.marker}]}),
            }}],
        }
        key = patch.object(direct.generator, "load_api_key", return_value="synthetic-test-key")
        key.start()
        self.addCleanup(key.stop)
        with patch.object(direct.generator, "request_review", return_value=(
                200, "review-request", json.dumps(review_response).encode())):
            status = direct.generator.generate_findings(self.model_input, self.review_run, "test-model", 8192)
        self.assertEqual(status, "completed")

    def run_direct(self, **kwargs):
        return direct.generate_claims(self.model_input, self.review_run, self.output,
                                      "test-model", 8192, **kwargs)

    def manifest(self):
        return json.loads((self.output / "run_manifest.json").read_bytes())

    def test_identical_code_context_and_preserved_isolated_artifacts(self):
        for folder in ("reference", "annotations"):
            path = self.root / folder
            path.mkdir()
            (path / "reference.txt").write_text(self.marker)
        raw = json.dumps(response_fixture([claim_fixture()])).encode() + b"\n "
        with patch.object(direct.generator, "request_review", return_value=(200, "request-id", raw)) as request:
            self.assertEqual(self.run_direct(disable_reasoning=True), "completed")
        request.assert_called_once()
        sent = request.call_args.args[0]
        payload = json.loads(sent)
        previous = json.loads((self.review_run / "request.json").read_bytes())
        self.assertEqual(payload["messages"][1], previous["messages"][1])
        self.assertNotIn(self.marker, sent.decode())
        self.assertIn(direct.claim_profile.CODEBOOK.read_text(encoding="utf-8"),
                      payload["messages"][0]["content"])
        self.assertEqual(payload["reasoning_effort"], "none")
        self.assertNotIn("tools", payload)
        self.assertNotIn("provider", payload)
        self.assertFalse(payload["store"])
        self.assertEqual(payload["response_format"], {"type": "json_object"})
        self.assertEqual(payload["max_completion_tokens"], 8192)
        self.assertEqual((self.output / "request.json").read_bytes(), sent)
        self.assertEqual((self.output / "generation_raw.json").read_bytes(), raw)
        self.assertEqual((self.output / "review_manifest.json").read_bytes(),
                         (self.review_run / "run_manifest.json").read_bytes())
        manifest = self.manifest()
        review_manifest = json.loads((self.review_run / "run_manifest.json").read_bytes())
        self.assertEqual(manifest["paired_review_run_id"], review_manifest["run_id"])
        self.assertIsNone(manifest["parent_run_id"])
        self.assertEqual(manifest["route"], "D")
        self.assertEqual(manifest["stage"], "direct_claims")
        self.assertEqual(manifest["profile_version"], "0.1")
        self.assertEqual(manifest["codebook_version"], "0.1")
        self.assertEqual(manifest["request_sha256"], direct.sha256(sent))
        self.assertEqual(manifest["response_sha256"], direct.sha256(raw))
        self.assertEqual(manifest["source_sha256"], review_manifest["source_sha256"])
        for name, expected in manifest["source_sha256"].items():
            saved = (self.output / "model_input" / name).read_bytes()
            self.assertEqual(saved, self.source_bytes[name])
            self.assertEqual(direct.sha256(saved), expected)
        for name, expected in manifest["resource_sha256"].items():
            self.assertEqual(direct.sha256((self.output / name).read_bytes()), expected)
        for name, expected in manifest["implementation_sha256"].items():
            self.assertEqual(direct.sha256((Path(direct.__file__).parent / name).read_bytes()), expected)
        row = json.loads((self.output / "claims.jsonl").read_bytes())
        self.assertEqual(row, {"profile_version": "0.1", "route": "D",
                               "run_id": manifest["run_id"], **claim_fixture()})
        self.assertNotIn("finding_id", row)
        self.assertNotIn("verification_status", row)
        for path in self.output.rglob("*"):
            if path.is_file():
                self.assertNotIn(b"synthetic-test-key", path.read_bytes())

    def test_changed_source_rejected_before_output_or_request(self):
        first = self.model_input / direct.generator.MODEL_FILES[0]
        first.write_bytes(first.read_bytes() + b"altered")
        with patch.object(direct.generator, "request_review") as request:
            with self.assertRaises(ValueError):
                self.run_direct()
        request.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_p_and_d_share_profile_and_pair_without_sharing_report_context(self):
        decomposer = import_module("03_decompose_findings")
        parent = direct.review_pair.load_review(self.review_run)
        finding = parent["findings"][0]
        p_claim = claim_fixture()
        p_claim["source_quotes"] = [{"field": "report", "quote": finding["report"], "occurrence": 1}]
        p_output = self.root / "decomposition"
        p_raw = json.dumps(response_fixture([p_claim], route="P")).encode()
        with patch.object(direct.generator, "request_review", return_value=(200, None, p_raw)) as p_request:
            self.assertEqual(decomposer.decompose_findings(
                self.review_run / "findings.jsonl", finding["finding_id"],
                p_output, "test-model", 8192), "completed")
        d_raw = json.dumps(response_fixture([claim_fixture()])).encode()
        with patch.object(direct.generator, "request_review", return_value=(200, None, d_raw)) as d_request:
            self.assertEqual(self.run_direct(), "completed")
        p_manifest = json.loads((p_output / "run_manifest.json").read_bytes())
        d_manifest = self.manifest()
        for field in ("profile_version", "codebook_version", "source_sha256", "paired_review_run_id"):
            self.assertEqual(p_manifest[field], d_manifest[field])
        for resource in (direct.claim_profile.SCHEMA.name, direct.claim_profile.CODEBOOK.name):
            self.assertEqual((p_output / resource).read_bytes(), (self.output / resource).read_bytes())
        p_user = json.loads(p_request.call_args.args[0])["messages"][1]["content"]
        d_user = json.loads(d_request.call_args.args[0])["messages"][1]["content"]
        self.assertEqual(json.loads(p_user), {key: finding[key] for key in ("title", "report")})
        self.assertEqual(d_user, parent["request"]["messages"][1]["content"])
        self.assertNotIn(self.marker, d_user)

    def test_missing_source_hash_and_changed_review_context_rejected_before_start(self):
        manifest_path = self.review_run / "run_manifest.json"
        original = json.loads(manifest_path.read_bytes())
        missing = deepcopy(original)
        del missing["source_sha256"][direct.generator.MODEL_FILES[0]]
        manifest_path.write_bytes(direct.json_bytes(missing))
        with patch.object(direct.generator, "request_review") as request:
            with self.assertRaises(ValueError):
                self.run_direct()
        request.assert_not_called()
        self.assertFalse(self.output.exists())
        request_path = self.review_run / "request.json"
        previous = json.loads(request_path.read_bytes())
        previous["messages"][1]["content"] += "\nDifferent code context"
        changed = direct.json_bytes(previous)
        request_path.write_bytes(changed)
        original["request_sha256"] = direct.sha256(changed)
        manifest_path.write_bytes(direct.json_bytes(original))
        with patch.object(direct.generator, "request_review") as request:
            with self.assertRaises(ValueError):
                self.run_direct()
        request.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_invalid_claims_and_wrong_route_leave_no_partial_result(self):
        bad = {**deepcopy(claim_fixture()), "claim_id": "C02", "context_claim_ids": ["C99"]}
        variants = [response_fixture([claim_fixture(), bad]), response_fixture([], route="P")]
        for index, response in enumerate(variants):
            self.output = self.root / f"invalid-claims-{index}"
            raw = json.dumps(response).encode()
            with patch.object(direct.generator, "request_review", return_value=(200, None, raw)) as request:
                self.assertEqual(self.run_direct(), "invalid_output")
            request.assert_called_once()
            self.assertFalse((self.output / "claims.jsonl").exists())
            self.assertEqual((self.output / "generation_raw.json").read_bytes(), raw)
            self.assertEqual(json.loads((self.output / "validation.json").read_bytes())["status"], "failed")

    def test_unresolved_code_reference_is_retained_as_nonfatal_diagnostic(self):
        claim = claim_fixture()
        claim["code_refs"] = [{"path": "unseen/File.java", "line_start": 900,
                               "line_end": 902, "symbol": "unseen"}]
        raw = json.dumps(response_fixture([claim])).encode()
        with patch.object(direct.generator, "request_review", return_value=(200, None, raw)):
            self.assertEqual(self.run_direct(), "completed")
        row = json.loads((self.output / "claims.jsonl").read_bytes())
        self.assertEqual(row["code_refs"], claim["code_refs"])
        validation = json.loads((self.output / "validation.json").read_bytes())
        self.assertEqual(validation["status"], "passed")
        self.assertTrue(validation["code_ref_checks"])

    def test_empty_claims_are_recorded_without_retry(self):
        raw = json.dumps(response_fixture([])).encode()
        with patch.object(direct.generator, "request_review", return_value=(200, None, raw)) as request:
            self.assertEqual(self.run_direct(), "no_claims")
        request.assert_called_once()
        self.assertEqual((self.output / "claims.jsonl").read_bytes(), b"")
        self.assertEqual(self.manifest()["claim_count"], 0)
        self.assertNotIn("reasoning_effort", json.loads((self.output / "request.json").read_bytes()))

    def test_malformed_provider_output_is_preserved(self):
        response = response_fixture([])
        response["choices"][0]["finish_reason"] = "length"
        duplicate = response_fixture([])
        duplicate["choices"][0]["message"]["content"] = (
            '{"profile_version":"0.1","route":"D","claims":[],"claims":[]}')
        for index, raw in enumerate((b"{", b"[]", json.dumps(response).encode(),
                                     json.dumps(duplicate).encode())):
            self.output = self.root / f"malformed-{index}"
            with patch.object(direct.generator, "request_review", return_value=(200, None, raw)) as request:
                self.assertEqual(self.run_direct(), "invalid_output")
            request.assert_called_once()
            self.assertEqual((self.output / "generation_raw.json").read_bytes(), raw)
            self.assertFalse((self.output / "claims.jsonl").exists())

    def test_transport_provider_and_key_errors_remain_run_errors(self):
        for index, result in enumerate(((429, None, b"rate limit"),
                                        (200, None, b'{"error":{"code":503}}'))):
            self.output = self.root / f"provider-error-{index}"
            with patch.object(direct.generator, "request_review", return_value=result) as request:
                self.assertEqual(self.run_direct(), "run_error")
            request.assert_called_once()
            self.assertFalse((self.output / "claims.jsonl").exists())
        self.output = self.root / "network-error"
        with patch.object(direct.generator, "request_review", side_effect=URLError("offline")) as request:
            self.assertEqual(self.run_direct(), "run_error")
        request.assert_called_once()
        self.assertFalse((self.output / "generation_raw.json").exists())
        self.output = self.root / "missing-key"
        with patch.object(direct.generator, "load_api_key", return_value=""):
            with patch.object(direct.generator, "request_review") as request:
                self.assertEqual(self.run_direct(), "run_error")
        request.assert_not_called()
        self.assertEqual(self.manifest()["request_attempts"], 0)

    def test_existing_output_is_preserved_and_invalid_options_create_no_run(self):
        for model, budget in (("provider/model", 100), ("test-model", 0)):
            with self.assertRaises(ValueError):
                direct.generate_claims(self.model_input, self.review_run, self.output, model, budget)
        self.assertFalse(self.output.exists())
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_bytes(b"previous run")
        with patch.object(direct.generator, "request_review") as request:
            with self.assertRaises(FileExistsError):
                self.run_direct()
        request.assert_not_called()
        self.assertEqual(marker.read_bytes(), b"previous run")
        self.assertEqual(len(list(self.output.iterdir())), 1)


if __name__ == "__main__":
    unittest.main()
