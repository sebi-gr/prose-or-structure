"""Offline checks for source-only, blank and reproducible human annotation packets."""

import hashlib
from importlib import import_module
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
annotations = import_module("07_prepare_annotations")
context = annotations.case_context
generator = annotations.generator


class PrepareAnnotationsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.cases_root = self.root / "cases"
        self.output = self.root / "annotations"
        self.catalog_path = self.root / "pilot_cases.json"
        self.catalog = {"dataset": self.source("dataset.csv", "a" * 40, b"dataset"), "cases": []}
        self.sources = {}
        for index, case_id in enumerate(annotations.CASE_IDS):
            variants = {}
            for offset, variant in enumerate(("vulnerable", "fixed")):
                revision = f"{index * 2 + offset + 1:040x}"
                files = {
                    "src/Input.java": f"class Input {{ int value = {index * 2 + offset}; }}\r\n// 🙂\r\n".encode(),
                    "config/input.xml": b"<input enabled=\"true\"/>\n",
                }
                self.sources[case_id, variant] = files
                for name, data in files.items():
                    target = self.cases_root / case_id / variant / "model_input" / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                variants[variant] = {"revision": revision, "files": [
                    self.source(name, revision, data) for name, data in files.items()]}
            self.catalog["cases"].append({
                "case_id": case_id, "repo": "fixture/project", "weakness": "CWE-fixture",
                "case_commit": variants["vulnerable"]["revision"],
                "fix_commit": variants["fixed"]["revision"], "split": "pilot",
                "variants": variants, "references": [],
                "selection_reason": "Synthetic test only.", "context_limits": "Synthetic context only.",
            })
        self.catalog_path.write_bytes(generator.json_bytes(self.catalog))
        registry = patch.object(context, "CATALOG", self.catalog_path)
        registry.start()
        self.addCleanup(registry.stop)

    def source(self, path, revision, data):
        return {"path": path,
                "url": f"https://raw.githubusercontent.com/fixture/project/{revision}/{path}",
                "sha256": hashlib.sha256(data).hexdigest()}

    def test_ten_source_only_packets_blank_worksheets_and_separate_linkage(self):
        for case_id in annotations.CASE_IDS:
            reference = self.cases_root / case_id / "reference"
            reference.mkdir()
            (reference / "secret.txt").write_text("REFERENCE_MARKER_WITH_TRUTH_AND_FIX_LABELS")
            for variant in ("vulnerable", "fixed"):
                # Even an unlisted file next to allowed source files must not enter a packet.
                (self.cases_root / case_id / variant / "model_input" / "extra.txt").write_text("EXTRA_MARKER")
        annotations.prepare_annotations(self.cases_root, self.output)
        linkage = json.loads((self.output / "linkage.json").read_bytes())
        self.assertEqual(linkage["status"], "awaiting_human_annotation")
        self.assertEqual(len(linkage["packets"]), 10)
        self.assertEqual({p.name for p in (self.output / "packets").iterdir()},
                         {f"packet-{n:02}" for n in range(1, 11)})
        for item in linkage["packets"]:
            folder = self.output / "packets" / item["packet_id"]
            self.assertEqual({p.name for p in folder.iterdir()}, {"code.txt", "CodeReference.md"})
            files = self.sources[item["case_id"], item["case_variant"]]
            code = (folder / "code.txt").read_bytes()
            self.assertEqual(code, generator.format_sources(files).encode())
            self.assertEqual(item["code_sha256"], hashlib.sha256(code).hexdigest())
            self.assertEqual(item["source_sha256"], {p: hashlib.sha256(b).hexdigest() for p, b in files.items()})
            worksheet = (folder / "CodeReference.md").read_text()
            self.assertIn("- Annotator/in:\n", worksheet)
            self.assertIn("- Startzeit (mit Zeitzone):\n", worksheet)
            self.assertIn("- Endzeit (mit Zeitzone):\n", worksheet)
            self.assertIn("- Tatsächliche Bearbeitungszeit in Minuten (Pausen abziehen):\n", worksheet)
            self.assertIn("- Vorwissen / frühere Einsicht", worksheet)
            for forbidden in ("VUL4J-", "CWE-", "vulnerable", "fixed", item["revision"],
                              "REFERENCE_MARKER", "EXTRA_MARKER"):
                self.assertNotIn(forbidden, code.decode() + worksheet)
        selected = [p for p in linkage["packets"] if p["double_annotation"]]
        self.assertEqual({(p["case_id"], p["case_variant"]) for p in selected},
                         {(case, variant) for case in ("VUL4J-15", "VUL4J-41")
                          for variant in ("vulnerable", "fixed")})
        self.assertEqual(set(linkage["double_annotation_packet_ids"]), {p["packet_id"] for p in selected})

    def test_protocol_snapshots_hashes_and_order_are_reproducible(self):
        annotations.prepare_annotations(self.cases_root, self.output)
        second = self.root / "second"
        annotations.prepare_annotations(self.cases_root, second)
        linkage = json.loads((self.output / "linkage.json").read_bytes())
        self.assertEqual(linkage["catalog_sha256"], hashlib.sha256(self.catalog_path.read_bytes()).hexdigest())
        for name in annotations.SNAPSHOTS:
            original = (annotations.RESOURCES / name).read_bytes()
            self.assertEqual((self.output / "protocol" / name).read_bytes(), original)
            self.assertEqual(linkage["resource_sha256"][name], hashlib.sha256(original).hexdigest())
        for path in self.output.rglob("*"):
            if path.is_file():
                self.assertEqual(path.read_bytes(), (second / path.relative_to(self.output)).read_bytes())

    def test_last_source_hash_failure_leaves_no_partial_output(self):
        path = self.cases_root / annotations.CASE_IDS[-1] / "fixed" / "model_input" / "src/Input.java"
        path.write_bytes(path.read_bytes() + b"// changed\n")
        before = set(self.root.iterdir())
        with self.assertRaisesRegex(ValueError, "do not match"):
            annotations.prepare_annotations(self.cases_root, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(set(self.root.iterdir()), before)

    def test_missing_protocol_resource_fails_before_publication(self):
        with patch.object(annotations, "RESOURCES", self.root / "missing"):
            with self.assertRaises(FileNotFoundError):
                annotations.prepare_annotations(self.cases_root, self.output)
        self.assertFalse(self.output.exists())

    def test_existing_output_is_not_touched(self):
        self.output.mkdir()
        marker = self.output / "human_work.md"
        marker.write_text("Existing human annotation")
        with patch.object(generator, "load_sources") as read:
            with self.assertRaises(FileExistsError):
                annotations.prepare_annotations(self.cases_root, self.output)
        read.assert_not_called()
        self.assertEqual(marker.read_text(), "Existing human annotation")

    def test_source_symlink_cannot_reach_reference_content(self):
        source = self.cases_root / annotations.CASE_IDS[0] / "vulnerable" / "model_input" / "src/Input.java"
        other = self.root / "reference.java"
        other.write_bytes(source.read_bytes())
        source.unlink()
        try:
            source.symlink_to(other)
        except OSError:
            self.skipTest("This platform does not allow symlink creation.")
        with self.assertRaisesRegex(ValueError, "Symlinks"):
            annotations.prepare_annotations(self.cases_root, self.output)
        self.assertFalse(self.output.exists())

    def test_write_failure_cleans_staging_without_publishing(self):
        original = Path.write_bytes

        def fail_on_code(path, content):
            if path.name == "code.txt":
                raise OSError("Synthetic disk failure")
            return original(path, content)

        before = set(self.root.iterdir())
        with patch.object(Path, "write_bytes", fail_on_code):
            with self.assertRaisesRegex(OSError, "disk failure"):
                annotations.prepare_annotations(self.cases_root, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(set(self.root.iterdir()), before)


if __name__ == "__main__":
    unittest.main()
