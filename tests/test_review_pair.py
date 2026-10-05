"""Offline checks for pairing a saved prose review with identical D input."""

import copy
import hashlib
from importlib import import_module
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
generator = import_module("02_generate_findings")
pair = import_module("review_pair")

ARTIFACTS = ("run_manifest.json", "request.json", "generation_raw.json", "findings.jsonl")


class ReviewPairTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.model_input = self.root / "model_input"
        self.files = {
            name: f"// synthetic {index}\r\n// könnte gelten\r\n".encode()
            for index, name in enumerate(generator.MODEL_FILES)
        }
        for name, content in self.files.items():
            target = self.model_input / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        self.output = self.root / "review"
        self.findings = [{"title": " Synthetic title ", "report": "Could occur, if enabled.\nUnverified."}]
        self.make_review(self.output, self.findings)

    def make_review(self, output, findings):
        raw = json.dumps({
            "choices": [{
                "finish_reason": "stop",
                "message": {"role": "assistant", "content": json.dumps({"findings": findings})},
            }],
        }).encode() + b"\n "
        with patch.dict("os.environ", {"OPENAI_API_KEY": "synthetic-test-key"}), \
                patch.object(generator, "request_review", return_value=(200, None, raw)):
            status = generator.generate_findings(self.model_input, output, "synthetic-model", 100)
        self.assertEqual(status, "completed" if findings else "no_findings")
        manifest = json.loads((output / "run_manifest.json").read_bytes())
        manifest["findings_sha256"] = hashlib.sha256((output / "findings.jsonl").read_bytes()).hexdigest()
        (output / "run_manifest.json").write_bytes(generator.json_bytes(manifest))

    def save_manifest(self, manifest):
        (self.output / "run_manifest.json").write_bytes(generator.json_bytes(manifest))

    def test_snapshot_reads_only_four_artifacts_and_preserves_original_bytes(self):
        before = {name: (self.output / name).read_bytes() for name in ARTIFACTS}
        allowed = {self.output / name for name in ARTIFACTS}
        original_read = Path.read_bytes
        reads = []

        def read_artifact(path):
            self.assertIn(path, allowed)
            reads.append(path)
            return original_read(path)

        with patch.object(Path, "read_bytes", read_artifact), \
                patch.object(generator, "request_review") as request:
            parent = pair.load_review(self.output)
            self.assertIsNone(pair.verify_sources(self.files, parent))
        request.assert_not_called()
        self.assertEqual(set(reads), allowed)
        self.assertEqual(parent["manifest_bytes"], before["run_manifest.json"])
        self.assertEqual(parent["request_bytes"], before["request.json"])
        self.assertEqual(parent["findings_bytes"], before["findings.jsonl"])
        self.assertEqual(parent["request"], json.loads(before["request.json"]))
        self.assertEqual(parent["findings"], [{
            "finding_id": f"{parent['manifest']['run_id']}:F001", **self.findings[0],
        }])
        self.assertEqual(before, {name: (self.output / name).read_bytes() for name in ARTIFACTS})

    def test_archived_legacy_review_needs_no_saved_model_input_or_findings_hash(self):
        archive = Path(__file__).resolve().parents[1] / "data/runs/VUL4J-18-review-001"
        before = {name: (archive / name).read_bytes() for name in ARTIFACTS}
        self.assertFalse((archive / "model_input").exists())
        parent = pair.load_review(archive)
        self.assertNotIn("findings_sha256", parent["manifest"])
        self.assertEqual(parent["manifest"]["run_id"], "0721c0a0-bba7-48c1-a63c-da196a69d97c")
        self.assertEqual(parent["findings"][0]["title"], "Path Traversal via PathInfo in WikiServlet")
        self.assertEqual(before, {name: (archive / name).read_bytes() for name in ARTIFACTS})

    def test_no_findings_is_a_valid_parent(self):
        output = self.root / "empty-review"
        self.make_review(output, [])
        parent = pair.load_review(output)
        self.assertEqual(parent["findings"], [])
        self.assertEqual(parent["findings_bytes"], b"")
        self.assertIsNone(pair.verify_sources(self.files, parent))

    def test_changed_artifact_bytes_fail_even_when_json_meaning_is_unchanged(self):
        for name in ARTIFACTS[1:]:
            with self.subTest(artifact=name):
                target = self.output / name
                original = target.read_bytes()
                target.write_bytes(original + b" ")
                with self.assertRaises(ValueError):
                    pair.load_review(self.output)
                target.write_bytes(original)

    def test_findings_must_match_provider_text_and_ids_even_with_updated_hash(self):
        manifest = json.loads((self.output / "run_manifest.json").read_bytes())
        original = (self.output / "findings.jsonl").read_bytes()
        finding = json.loads(original)
        examples = [
            {**finding, "report": "Changed report."},
            {**finding, "title": finding["title"].strip()},
            {**finding, "finding_id": f"{manifest['run_id']}:F002"},
            {**finding, "extra": "not in the original response"},
        ]
        for row in examples:
            with self.subTest(row=row):
                content = (json.dumps(row) + "\n").encode()
                (self.output / "findings.jsonl").write_bytes(content)
                changed = {**manifest, "findings_sha256": hashlib.sha256(content).hexdigest()}
                self.save_manifest(changed)
                with self.assertRaises(ValueError):
                    pair.load_review(self.output)

    def test_incomplete_or_inconsistent_manifest_is_rejected(self):
        original = json.loads((self.output / "run_manifest.json").read_bytes())
        examples = [
            {**original, "status": "running"},
            {**original, "status": "invalid_output"},
            {**original, "status": "no_findings"},
            {**original, "case_id": "VUL4J-99"},
            {**original, "run_id": ""},
            {**original, "source_sha256": {}},
            {**original, "source_sha256": {**original["source_sha256"], "reference.java": "a" * 64}},
        ]
        for field in ["request_sha256", "response_sha256", "source_sha256"]:
            examples.append({key: value for key, value in original.items() if key != field})
        for index, manifest in enumerate(examples):
            with self.subTest(index=index):
                self.save_manifest(manifest)
                with self.assertRaises(ValueError):
                    pair.load_review(self.output)

    def test_pairing_checks_source_names_hashes_and_exact_request_context(self):
        parent = pair.load_review(self.output)
        name = next(iter(self.files))
        changed = {**self.files, name: b"// different bytes\n"}
        for files in [
            {key: value for key, value in self.files.items() if key != name},
            {**self.files, "reference.java": b"extra context"},
            changed,
        ]:
            with self.subTest(names=list(files)):
                with self.assertRaises(ValueError):
                    pair.verify_sources(files, parent)

        # A matching hash in a revised manifest cannot override what P actually saw.
        inconsistent = copy.deepcopy(parent)
        inconsistent["manifest"]["source_sha256"][name] = hashlib.sha256(changed[name]).hexdigest()
        with self.assertRaises(ValueError):
            pair.verify_sources(changed, inconsistent)

    def test_missing_artifact_is_rejected_without_fallback(self):
        for name in ARTIFACTS:
            with self.subTest(artifact=name):
                target = self.output / name
                content = target.read_bytes()
                target.unlink()
                with self.assertRaises((ValueError, FileNotFoundError)):
                    pair.load_review(self.output)
                target.write_bytes(content)

    def test_symlinked_artifacts_review_directory_and_ancestors_are_rejected(self):
        target = self.output / "request.json"
        outside = self.root / "request-original.json"
        outside.write_bytes(target.read_bytes())
        target.unlink()
        try:
            target.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"Symlink privileges unavailable: {error}")
        with self.assertRaises(ValueError):
            pair.load_review(self.output)
        target.unlink()
        target.write_bytes(outside.read_bytes())

        link = self.root / "linked-review"
        link.symlink_to(self.output, target_is_directory=True)
        with self.assertRaises(ValueError):
            pair.load_review(link)

        ancestor = self.root / "linked-root"
        ancestor.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            pair.load_review(ancestor / self.output.name)


if __name__ == "__main__":
    unittest.main()
