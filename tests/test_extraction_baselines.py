"""Offline baseline checks: original spans, isolated prompts and complete-run outputs."""

from importlib import import_module
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
baseline = import_module("extraction_baselines")
generator = import_module("02_generate_findings")


class ExtractionBaselineTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.source = self.root / "model_input"
        for name in generator.MODEL_FILES:
            target = self.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("// DO_NOT_SEND_SOURCE\n", encoding="utf-8")
        self.review = self.root / "review"
        self.output = self.root / "baselines"
        self.make_review([{"title": "Fixture title", "report": "An input reaches a sink. It could matter if enabled."}])

    def response(self, text, finish="stop"):
        return json.dumps({
            "id": "synthetic-response", "model": "synthetic-snapshot",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            "choices": [{"finish_reason": finish, "message": {"role": "assistant", "content": text}}],
        }).encode() + b"\n "

    def make_review(self, findings):
        raw = self.response(json.dumps({"findings": findings}))
        with patch.object(generator, "load_api_key", return_value="synthetic-key"), \
                patch.object(generator, "request_review", return_value=(200, None, raw)):
            status = generator.generate_findings(self.source, self.review, "synthetic-model", 500)
        self.assertEqual(status, "completed" if findings else "no_findings")

    def run_baselines(self, requester):
        with patch.object(generator, "load_api_key", return_value="synthetic-key"):
            return baseline.run_baselines(self.review, self.output, "synthetic-model", 500, requester)

    def manifest(self):
        return json.loads((self.output / "run_manifest.json").read_bytes())

    def test_sentence_spans_preserve_unicode_offsets_and_exact_substrings(self):
        text = " \tÖffne 😀.\r\nCould fail?  Only if enabled!\nFinal fragment  "
        spans = baseline.sentence_spans(text)
        self.assertEqual([s["quote"] for s in spans], ["Öffne 😀.", "Could fail?", "Only if enabled!", "Final fragment"])
        for span in spans:
            self.assertEqual(text[span["start"]:span["end"]], span["quote"])
        self.assertEqual(spans[0]["start"], 2)
        self.assertEqual(baseline.sentence_spans(" \n \r\n"), [])

    def test_windows_cover_all_findings_and_include_title_targets(self):
        findings = [
            {"finding_id": "F1", "title": "First title. More title!", "report": "One. Two. Three. Four. Five. Six."},
            {"finding_id": "F2", "title": "Other title", "report": "Other sentence."},
        ]
        sentences, jobs = baseline.prepare_units(findings)
        self.assertEqual(len(sentences), 10)
        self.assertEqual(len(jobs), 10)
        self.assertEqual(jobs[0]["target_span"]["field"], "title")
        self.assertIn("<SOS>First title.<EOS>", jobs[0]["snippet"])
        self.assertIn("Report (context only): One. Two.", jobs[0]["snippet"])
        self.assertIn("First title. More title!", jobs[2]["snippet"])
        self.assertIn("Report: One. Two. Three. Four. <SOS>Five.<EOS> Six.", jobs[6]["snippet"])
        self.assertIn("Report: One. <SOS>One.<EOS> Two.", jobs[2]["snippet"])
        self.assertNotIn("First title", jobs[-1]["snippet"])
        self.assertEqual(jobs[-1]["sentence_index"], 1)

    def test_original_prompt_and_license_match_pinned_provenance(self):
        provenance = json.loads((baseline.RESOURCES / "provenance.json").read_bytes())
        self.assertEqual(provenance["commit"], "8714bca27b944b9659d6a966cdb92fb6fff8f72d")
        for item in provenance["files"]:
            content = (baseline.RESOURCES / item["file"]).read_bytes()
            self.assertEqual(generator.sha256(content), item["sha256"])
            self.assertEqual(len(content), item["bytes"])

    def test_success_preserves_requests_usage_raw_bytes_and_exact_deduplication(self):
        raws = [self.response("- Fixture title."),
                self.response("- The input reaches a sink.\n- The input is passed."),
                self.response("- The input reaches a sink.\n- It could matter if enabled.")]
        requester = Mock(side_effect=[(200, f"req{i}", raw) for i, raw in enumerate(raws, 1)])
        self.assertEqual(self.run_baselines(requester), "completed")
        self.assertEqual(requester.call_count, 3)
        for call in requester.call_args_list:
            body, key = call.args
            payload = json.loads(body)
            self.assertEqual(key, "synthetic-key")
            self.assertEqual(payload["reasoning_effort"], "none")
            self.assertEqual(payload["service_tier"], "default")
            self.assertNotIn("response_format", payload)
            self.assertNotIn("tools", payload)
            self.assertNotIn(b"DO_NOT_SEND_SOURCE", body)
            self.assertNotIn(b"claim_profile", body)
        manifest = self.manifest()
        self.assertEqual(manifest["planned_calls"], 3)
        self.assertEqual(manifest["completed_calls"], 3)
        self.assertEqual(manifest["unattempted_calls"], 0)
        self.assertEqual(manifest["calls"][0]["usage"]["total_tokens"], 15)
        self.assertIsNone(manifest["cost_usd"])
        claims = [json.loads(line) for line in (self.output / "veriscore_claims.jsonl").read_text().splitlines()]
        self.assertEqual(len(claims), 4)
        self.assertEqual(claims[1]["extraction_call_ids"], ["0002", "0003"])
        self.assertNotIn("source_quotes", claims[0])
        self.assertEqual((self.output / "calls/0001/generation_raw.json").read_bytes(), raws[0])
        self.assertEqual((self.output / "findings.jsonl").read_bytes(), (self.review / "findings.jsonl").read_bytes())
        self.assertEqual(generator.sha256((self.output / "sentence_claims.jsonl").read_bytes()),
                         manifest["sentence_claims_sha256"])
        self.assertEqual(manifest["sentence_claim_count"], 3)

    def test_valid_no_claims_is_completed_and_not_an_error(self):
        requester = Mock(return_value=(200, None, self.response("No verifiable claim.")))
        self.assertEqual(self.run_baselines(requester), "completed")
        self.assertEqual((self.output / "veriscore_claims.jsonl").read_bytes(), b"")
        self.assertEqual(self.manifest()["veriscore_claim_count"], 0)

    def test_invalid_later_response_stops_and_never_writes_partial_claim_file(self):
        requester = Mock(side_effect=[(200, None, self.response("- One valid claim.")),
                                      (200, None, self.response("An unexpected paragraph."))])
        self.assertEqual(self.run_baselines(requester), "invalid_output")
        self.assertTrue((self.output / "sentence_claims.jsonl").exists())
        self.assertFalse((self.output / "veriscore_claims.jsonl").exists())
        self.assertEqual(self.manifest()["completed_calls"], 1)
        self.assertEqual(self.manifest()["calls"][1]["status"], "invalid_output")
        self.assertTrue((self.output / "calls/0002/generation_raw.json").exists())

    def test_http_failure_retains_raw_error_and_skips_remaining_calls(self):
        requester = Mock(return_value=(429, "req-error", b'{"error":"limit"}'))
        self.assertEqual(self.run_baselines(requester), "run_error")
        self.assertEqual(requester.call_count, 1)
        self.assertEqual(self.manifest()["unattempted_calls"], 2)
        self.assertEqual((self.output / "calls/0001/generation_raw.json").read_bytes(), b'{"error":"limit"}')
        self.assertFalse((self.output / "veriscore_claims.jsonl").exists())

    def test_missing_key_keeps_sentence_baseline_without_request(self):
        requester = Mock()
        with patch.object(generator, "load_api_key", return_value=""):
            status = baseline.run_baselines(self.review, self.output, "synthetic-model", 500, requester)
        self.assertEqual(status, "run_error")
        requester.assert_not_called()
        self.assertEqual(self.manifest()["calls"], [])
        self.assertEqual(self.manifest()["unattempted_calls"], 3)
        self.assertTrue((self.output / "sentence_claims.jsonl").exists())

    def test_empty_review_needs_neither_api_key_nor_transport(self):
        self.review = self.root / "empty-review"
        self.make_review([])
        requester = Mock()
        with patch.object(generator, "load_api_key", side_effect=AssertionError("Must not need a key")):
            status = baseline.run_baselines(self.review, self.output, "synthetic-model", 500, requester)
        self.assertEqual(status, "no_findings")
        requester.assert_not_called()
        self.assertEqual((self.output / "sentence_claims.jsonl").read_bytes(), b"")
        self.assertEqual((self.output / "veriscore_claims.jsonl").read_bytes(), b"")

    def test_budget_guard_failure_is_recorded_without_retry_or_secret(self):
        requester = Mock(side_effect=RuntimeError("Budget guard rejected synthetic-key"))
        self.assertEqual(self.run_baselines(requester), "run_error")
        self.assertEqual(requester.call_count, 1)
        self.assertNotIn("synthetic-key", (self.output / "run_manifest.json").read_text())
        self.assertEqual(self.manifest()["unattempted_calls"], 2)

    def test_invalid_parent_and_existing_output_fail_before_transport(self):
        requester = Mock()
        path = self.review / "findings.jsonl"
        original = path.read_bytes()
        path.write_bytes(original.replace(b"Fixture title", b"Changed title"))
        with self.assertRaises(ValueError):
            self.run_baselines(requester)
        self.assertFalse(self.output.exists())
        path.write_bytes(original)
        self.output.mkdir()
        sentinel = self.output / "do-not-overwrite"
        sentinel.write_bytes(b"original")
        with self.assertRaises(FileExistsError):
            self.run_baselines(requester)
        self.assertEqual(sentinel.read_bytes(), b"original")
        requester.assert_not_called()

    def test_unexpected_output_is_rejected_without_repairs(self):
        for text in ["", " ", "1. Numbered claim.", "- ", "- Good.\nNote: Other text.",
                     "No verifiable claim.\n- Yet a claim.", "- No verifiable claim.",
                     "```\n- Good.\n```"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                baseline.parse_extraction(json.loads(self.response(text)))
        for finish in ["length", "content_filter", "tool_calls"]:
            with self.subTest(finish=finish), self.assertRaises(ValueError):
                baseline.parse_extraction(json.loads(self.response("- Could look valid.", finish)))
        refusal = json.loads(self.response("- Could look valid."))
        refusal["choices"][0]["message"]["refusal"] = "Refused"
        with self.assertRaises(ValueError):
            baseline.parse_extraction(refusal)


if __name__ == "__main__":
    unittest.main()
