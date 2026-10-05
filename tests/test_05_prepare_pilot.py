"""Offline checks for the small pinned pilot registry and atomic source export."""

from copy import deepcopy
import hashlib
from importlib import import_module
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
pilot = import_module("05_prepare_pilot")
context = pilot.case_context


class PreparePilotTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.output = self.root / "prepared"
        self.catalog_path = self.root / "pilot_cases.json"
        self.downloads = {}
        self.paths = ("src/Parser.java", "config/service.xml")
        vulnerable = "1" * 40
        fixed = "2" * 40
        dataset_revision = "3" * 40
        dataset = ("vul_id,repo_slug,human_patch\n"
                   f"VUL4J-1,example/project,https://github.com/example/project/commit/{fixed}\n").encode()
        dataset_source = self.source("dataset.csv", dataset_revision, dataset)
        dataset_source.pop("path")
        reference = self.source("LICENSE", vulnerable, b"REFERENCE_LICENSE_MUST_STAY_SEPARATE\n")
        variants = {}
        for variant, revision in (("vulnerable", vulnerable), ("fixed", fixed)):
            variants[variant] = {
                "revision": revision,
                "files": [self.source(path, revision, f"{variant}: {path}\r\n// 🙂\r\n".encode())
                          for path in self.paths],
            }
        self.case = {
            "case_id": "VUL4J-1", "repo": "example/project", "weakness": "synthetic class",
            "case_commit": vulnerable, "fix_commit": fixed, "split": "pilot",
            "variants": variants, "references": [reference],
            "selection_reason": "Synthetic fixture only.", "context_limits": "Local test context only.",
        }
        self.catalog = {"dataset": dataset_source, "cases": [self.case]}
        self.save_catalog()
        registry = patch.object(context, "CATALOG", self.catalog_path)
        registry.start()
        self.addCleanup(registry.stop)
        downloader = patch.object(pilot, "download", side_effect=lambda url: self.downloads[url])
        self.download = downloader.start()
        self.addCleanup(downloader.stop)

    def source(self, path, revision, content):
        url = f"https://raw.githubusercontent.com/example/project/{revision}/{path}"
        self.downloads[url] = content
        return {"path": path, "url": url, "sha256": hashlib.sha256(content).hexdigest()}

    def save_catalog(self):
        self.catalog_path.write_bytes(pilot.json_bytes(self.catalog))

    def test_exact_sources_variants_references_and_provenance_are_separate(self):
        original = self.catalog_path.read_bytes()
        pilot.prepare_pilot(self.output)
        self.assertEqual((self.output / "pilot_cases.json").read_bytes(), original)
        self.assertEqual(context.get_case("VUL4J-1"), self.case)
        self.assertEqual(context.model_files("VUL4J-1"), self.paths)
        case_root = self.output / "VUL4J-1"
        for variant_name, variant in self.case["variants"].items():
            variant_root = case_root / variant_name
            inputs = variant_root / "model_input"
            self.assertEqual({str(path.relative_to(inputs)) for path in inputs.rglob("*") if path.is_file()},
                             set(self.paths))
            manifest = json.loads((variant_root / "case_manifest.json").read_bytes())
            self.assertEqual(manifest["case_id"], "VUL4J-1")
            self.assertEqual(manifest["case_variant"], variant_name)
            self.assertEqual(manifest["revision"], variant["revision"])
            self.assertEqual(manifest["catalog_sha256"], hashlib.sha256(original).hexdigest())
            self.assertEqual(manifest["pov_status"], "not_run")
            self.assertEqual(manifest["sources"], variant["files"])
            for source in variant["files"]:
                content = (inputs / source["path"]).read_bytes()
                self.assertEqual(content, self.downloads[source["url"]])
                self.assertEqual(manifest["source_sha256"][source["path"]], hashlib.sha256(content).hexdigest())
                self.assertNotIn(b"REFERENCE_LICENSE", content)
        reference = case_root / "reference"
        self.assertEqual((reference / "LICENSE").read_bytes(),
                         self.downloads[self.case["references"][0]["url"]])
        row = json.loads((reference / "vul4j_row.json").read_bytes())
        self.assertEqual(row["vul_id"], "VUL4J-1")
        self.assertEqual(self.download.call_count, 6)

    def test_download_hash_failure_removes_staging_and_publishes_nothing(self):
        url = self.case["variants"]["fixed"]["files"][-1]["url"]
        self.downloads[url] += b"changed"
        before = set(self.root.iterdir())
        with self.assertRaisesRegex(ValueError, "hash differs"):
            pilot.prepare_pilot(self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(set(self.root.iterdir()), before)

    def test_non_utf8_model_source_is_rejected_without_publishing(self):
        source = self.case["variants"]["fixed"]["files"][0]
        self.downloads[source["url"]] = b"\xff"
        source["sha256"] = hashlib.sha256(b"\xff").hexdigest()
        self.save_catalog()
        with self.assertRaises(UnicodeError):
            pilot.prepare_pilot(self.output)
        self.assertFalse(self.output.exists())

    def test_invalid_catalog_paths_and_variant_sets_fail_before_download(self):
        original = deepcopy(self.catalog)
        for path in ("../outside", "/absolute", "nested/../outside", "a\\b", "C:/file", "a//b"):
            with self.subTest(path=path):
                self.catalog = deepcopy(original)
                self.catalog["cases"][0]["variants"]["vulnerable"]["files"][0]["path"] = path
                self.save_catalog()
                with self.assertRaises(ValueError):
                    pilot.prepare_pilot(self.output)
        self.catalog = deepcopy(original)
        self.catalog["cases"][0]["variants"]["fixed"]["files"].pop()
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "path sets must match"):
            pilot.prepare_pilot(self.output)
        self.download.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_unknown_development_duplicate_and_unpinned_cases_are_rejected(self):
        with self.assertRaises(ValueError):
            pilot.prepare_pilot(self.output, "VUL4J-9999")
        with self.assertRaises(ValueError):
            context.model_files("VUL4J-9999")
        original = deepcopy(self.catalog)
        for case_id in ("VUL4J-18", "VUL4J-47", "VUL4J-9"):
            self.catalog = deepcopy(original)
            self.catalog["cases"][0]["case_id"] = case_id
            self.save_catalog()
            with self.assertRaises(ValueError):
                context.load_catalog()
        self.catalog = deepcopy(original)
        self.catalog["cases"].append(deepcopy(self.catalog["cases"][0]))
        self.save_catalog()
        with self.assertRaises(ValueError):
            context.load_catalog()
        self.catalog = deepcopy(original)
        source = self.catalog["cases"][0]["variants"]["fixed"]["files"][0]
        source["url"] = source["url"].replace("2" * 40, "main")
        self.save_catalog()
        with self.assertRaises(ValueError):
            context.load_catalog()
        self.download.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_missing_or_mismatched_dataset_case_cannot_be_prepared(self):
        original = self.case["fix_commit"]
        self.case["fix_commit"] = "9" * 40
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "Dataset row does not match"):
            pilot.prepare_pilot(self.output)
        self.assertFalse(self.output.exists())
        self.case["fix_commit"] = original
        self.case["case_id"] = "VUL4J-2"
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "exactly one dataset row"):
            pilot.prepare_pilot(self.output)
        self.assertFalse(self.output.exists())

    def test_existing_output_and_legacy_allowlist_are_preserved(self):
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_bytes(b"previous output")
        with self.assertRaises(FileExistsError):
            pilot.prepare_pilot(self.output)
        self.download.assert_not_called()
        self.assertEqual(marker.read_bytes(), b"previous output")
        with patch.object(context, "CATALOG", self.root / "missing.json"):
            self.assertEqual(context.model_files("VUL4J-18"), context.legacy.MODEL_FILES)

    def test_dataset_abbreviated_fix_must_be_a_matching_seven_to_forty_character_prefix(self):
        dataset_source = self.catalog["dataset"]
        patch_prefix = "https://github.com/example/project/commit/"
        revisions = (("2" * 7, True), ("2" * 8, True), ("2" * 40, True),
                     ("2" * 6, False), ("2" * 41, False), ("3" + "2" * 7, False))
        for index, (revision, valid) in enumerate(revisions):
            with self.subTest(revision=revision):
                self.output = self.root / f"short-fix-{index}"
                dataset = ("vul_id,repo_slug,human_patch\n"
                           f"VUL4J-1,example/project,{patch_prefix}{revision}\n").encode()
                self.downloads[dataset_source["url"]] = dataset
                dataset_source["sha256"] = hashlib.sha256(dataset).hexdigest()
                self.save_catalog()
                if valid:
                    pilot.prepare_pilot(self.output)
                    self.assertTrue((self.output / "VUL4J-1" / "fixed" / "case_manifest.json").exists())
                else:
                    with self.assertRaisesRegex(ValueError, "Dataset row does not match"):
                        pilot.prepare_pilot(self.output)
                    self.assertFalse(self.output.exists())

    def test_explicit_single_case_selection_has_the_same_directory_contract(self):
        second = deepcopy(self.case)
        second["case_id"] = "VUL4J-2"
        self.catalog["cases"].append(second)
        self.save_catalog()
        pilot.prepare_pilot(self.output, "VUL4J-1")
        self.assertTrue((self.output / "VUL4J-1" / "fixed" / "case_manifest.json").exists())
        self.assertFalse((self.output / "VUL4J-2").exists())


if __name__ == "__main__":
    unittest.main()
