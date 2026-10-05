"""Checks for reference leakage, preserved bytes, and safe failure."""

import hashlib
from importlib import import_module
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
prepare_case = import_module("01_prepare_case")


DATASET = (
    "vul_id,repo_slug,cve_id,human_patch\n"
    "VUL4J-18,apache/jspwiki,CVE-2019-0225,"
    "https://github.com/apache/jspwiki/commit/88d89d6523802c044cfcb7930cba40d8eeb21da2\n"
).encode()


def fake_download(url):
    if url.endswith("vul4j_dataset.csv"):
        return DATASET
    if "/apache/jspwiki/" in url:
        return b"// fixed reference only\r\n"
    if "/src/test/" in url:
        return b"// PoV reference only\r\n"
    return b"// original source bytes\r\n"


class PrepareCaseTests(unittest.TestCase):
    def test_model_context_excludes_reference_and_preserves_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "case"
            with patch.object(prepare_case, "download", side_effect=fake_download):
                prepare_case.prepare_case(output)

            model = output / "model_input"
            paths = {path.relative_to(model).as_posix() for path in model.rglob("*") if path.is_file()}
            self.assertEqual(paths, {
                "jspwiki-main/src/main/java/org/apache/wiki/WikiServlet.java",
                "jspwiki-main/src/main/java/org/apache/wiki/url/DefaultURLConstructor.java",
                "jspwiki-main/src/main/java/org/apache/wiki/url/URLConstructor.java",
                "jspwiki-main/src/main/resources/ini/jspwiki.properties",
                "jspwiki-war/src/main/webapp/WEB-INF/web.xml",
            })
            for path in paths:
                self.assertEqual((model / path).read_bytes(), b"// original source bytes\r\n")
            fixed = output / "reference/fixed" / prepare_case.CONSTRUCTOR
            pov = output / "reference/pov" / prepare_case.POV
            self.assertEqual(fixed.read_bytes(), b"// fixed reference only\r\n")
            self.assertEqual(pov.read_bytes(), b"// PoV reference only\r\n")
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["pov_status"], "not_run")
            for path, info in manifest["files"].items():
                self.assertEqual(info["sha256"], hashlib.sha256((output / path).read_bytes()).hexdigest())

    def test_existing_output_is_not_touched(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            marker = output / "keep.txt"
            marker.write_text("existing experiment")
            with patch.object(prepare_case, "download") as download:
                with self.assertRaises(FileExistsError):
                    prepare_case.prepare_case(output)
                download.assert_not_called()
            self.assertEqual(marker.read_text(), "existing experiment")

    def test_failed_download_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "case"
            responses = [DATASET, b"first downloaded file", URLError("network unavailable")]
            with patch.object(prepare_case, "download", side_effect=responses):
                with self.assertRaises(URLError):
                    prepare_case.prepare_case(output)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
