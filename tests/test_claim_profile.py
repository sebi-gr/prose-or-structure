"""Offline checks of the shared profile and non-authoritative code diagnostics."""

from copy import deepcopy
from importlib import import_module
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
profile = import_module("claim_profile")


def claim_fixture():
    return {
        "claim_id": "C01", "proposition": "If enabled, a caller could access the resource.",
        "family": "exploitability_impact", "subtype": "impact", "family_reason": "Potential impact.",
        "context": {"actor": "a caller", "preconditions": "if enabled", "negation": None,
                    "modality": "could", "quantifier": None, "scope": "the resource"},
        "source_quotes": [], "code_refs": [], "context_claim_ids": [],
        "verification": {"question": "Can a caller access the resource if enabled?",
                         "required_evidence": ["Resource handler and configuration"], "assumptions": []},
    }


def document_fixture(claims=None, route="D"):
    return {"profile_version": "0.1", "route": route,
            "claims": [claim_fixture()] if claims is None else claims}


def code_ref(path="src/Handler.java", start=1, end=1, symbol=None):
    return {"path": path, "line_start": start, "line_end": end, "symbol": symbol}


class ClaimProfileTests(unittest.TestCase):
    def test_all_curated_examples_follow_shared_contract(self):
        data = json.loads((ROOT / "resources/profile_development/examples.json").read_bytes())
        finding = json.loads((ROOT / "data/runs/VUL4J-18-review-001/findings.jsonl").read_bytes())
        count = 0
        for example in data["examples"]:
            with self.subTest(example=example["example_id"]):
                document = example["output"]
                saved = deepcopy(document)
                claims = profile.validate_claims(document, document["route"], finding)
                self.assertEqual(saved, document)
                count += len(claims)
                for claim in claims:
                    for quote in claim["source_quotes"]:
                        self.assertEqual(finding[quote["field"]][quote["start"]:quote["end"]], quote["quote"])
        self.assertEqual(count, 10)

    def test_route_and_version_are_not_inferred_or_migrated(self):
        for document, route, finding in (
            (document_fixture(), "P", {"title": "Title", "report": "Report"}),
            (document_fixture(route="P"), "D", None),
            (document_fixture(), "unknown", None),
            ({"schema_version": "1", "claims": []}, "D", None),
            ({**document_fixture(), "profile_version": "0.2"}, "D", None),
            ({**document_fixture(), "claims": {}}, "D", None),
            (document_fixture(route="P"), "P", None),
        ):
            with self.subTest(document=document, route=route), self.assertRaises(ValueError):
                profile.validate_claims(document, route, finding)
        self.assertEqual(profile.validate_claims(document_fixture([]), "D"), [])
        self.assertEqual(profile.validate_claims(document_fixture([], "P"), "P",
                                                {"title": "Title", "report": "Report"}), [])

    def test_context_preserves_absence_negation_and_explicit_unknown(self):
        for actor in (None, "No authentication required", "Authentication requirement unknown"):
            claim = claim_fixture()
            claim["context"]["actor"] = actor
            resolved = profile.validate_claims(document_fixture([claim]), "D")[0]
            self.assertEqual(resolved["context"]["actor"], actor)
            self.assertEqual(resolved["proposition"], claim["proposition"])
        for key in profile.CONTEXT_FIELDS:
            for value in (" ", [], False, 4):
                claim = claim_fixture()
                claim["context"][key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    profile.validate_claims(document_fixture([claim]), "D")
            claim = claim_fixture()
            del claim["context"][key]
            with self.subTest(missing=key), self.assertRaises(ValueError):
                profile.validate_claims(document_fixture([claim]), "D")

    def test_exact_fields_and_text_types_reject_truth_labels(self):
        for key in profile.CLAIM_FIELDS:
            claim = claim_fixture()
            del claim[key]
            with self.subTest(missing=key), self.assertRaisesRegex(ValueError, "missing fields"):
                profile.validate_claims(document_fixture([claim]), "D")
        for field in ("proposition", "family_reason", "claim_id", "family"):
            for value in (None, " ", 0, []):
                claim = {**claim_fixture(), field: value}
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    profile.validate_claims(document_fixture([claim]), "D")
        for target in ("claim", "context", "verification"):
            claim = claim_fixture()
            (claim if target == "claim" else claim[target])["supported"] = True
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, "unexpected fields"):
                profile.validate_claims(document_fixture([claim]), "D")

    def test_family_and_subtype_boundaries_do_not_infer_categories(self):
        for family in profile.FAMILIES:
            valid = ("exploitability", "impact", "unclear") if family == "exploitability_impact" else (None,)
            for subtype in (None, "exploitability", "impact", "unclear", "novel"):
                document = document_fixture([{**claim_fixture(), "family": family, "subtype": subtype}])
                with self.subTest(family=family, subtype=subtype):
                    if subtype in valid:
                        self.assertEqual(profile.validate_claims(document, "D")[0]["family"], family)
                    else:
                        with self.assertRaises(ValueError):
                            profile.validate_claims(document, "D")
        with self.assertRaises(ValueError):
            profile.validate_claims(document_fixture([{**claim_fixture(), "family": "invented"}]), "D")

    def test_ids_are_unique_local_and_not_self_referential(self):
        first = claim_fixture()
        second = {**deepcopy(first), "claim_id": "C09a", "context_claim_ids": ["C01"]}
        self.assertEqual(len(profile.validate_claims(document_fixture([first, second]), "D")), 2)
        for references in (["C09a"], ["C99"], ["C01", "C01"], [True], ["C1"], "C01"):
            second["context_claim_ids"] = references
            with self.subTest(references=references), self.assertRaises(ValueError):
                profile.validate_claims(document_fixture([first, second]), "D")
        for claims in ([first, first], [{**first, "claim_id": "C1"}]):
            with self.assertRaises(ValueError):
                profile.validate_claims(document_fixture(claims), "D")

    def test_verification_remains_separate_and_lists_are_unique(self):
        for key, values in (
            ("question", (None, "", False)),
            ("required_evidence", ([], "code", [""], ["code", "code"], [False])),
            ("assumptions", (None, "assumption", [""], ["a", "a"], [2])),
        ):
            for value in values:
                claim = claim_fixture()
                claim["verification"][key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    profile.validate_claims(document_fixture([claim]), "D")

    def test_p_quotes_use_overlapping_unicode_offsets_and_preserve_crlf(self):
        finding = {"title": "🙂 title", "report": "🙂 ababa.\r\nConditional."}
        claim = claim_fixture()
        claim["source_quotes"] = [
            {"field": "report", "quote": "aba", "occurrence": 2},
            {"field": "report", "quote": ".\r\nConditional", "occurrence": 1},
            {"field": "title", "quote": "🙂", "occurrence": 1},
        ]
        document = document_fixture([claim], "P")
        saved = deepcopy(document)
        resolved = profile.validate_claims(document, "P", finding)
        self.assertEqual(document, saved)
        self.assertEqual(resolved[0]["source_quotes"][0]["start"], 4)
        self.assertEqual(resolved[0]["source_quotes"][0]["end"], 7)
        for quote in resolved[0]["source_quotes"]:
            self.assertEqual(finding[quote["field"]][quote["start"]:quote["end"]], quote["quote"])
        for quotes in ([], [{"field": "report", "quote": ".\nConditional", "occurrence": 1}],
                       [{"field": "report", "quote": "aba", "occurrence": 3}],
                       [{"field": "report", "quote": "aba", "occurrence": True}],
                       [{"field": "report", "quote": "aba", "occurrence": 0}],
                       [claim["source_quotes"][0]] * 2):
            with self.subTest(quotes=quotes), self.assertRaises(ValueError):
                profile.validate_claims(document_fixture([{**claim, "source_quotes": quotes}], "P"), "P", finding)
        with self.assertRaises(ValueError):
            profile.validate_claims(document_fixture([claim]), "D")

    def test_code_reference_structure_retains_unresolvable_paths_and_lines(self):
        for refs in (
            [], [code_ref("../../private.txt", 9000, 9001)],
            [code_ref(None, None, None, "Handler.run")],
            [code_ref("unknown.java", None, None)],
        ):
            claim = {**claim_fixture(), "code_refs": refs}
            self.assertEqual(profile.validate_claims(document_fixture([claim]), "D")[0]["code_refs"], refs)
        for refs in (
            None, [code_ref(None, None, None)], [code_ref(" ")],
            [code_ref(start=None)], [code_ref(end=None)], [code_ref(start=0)],
            [code_ref(start=True)], [code_ref(end=False)], [code_ref(start=2, end=1)],
            [code_ref(end=1.5)], [code_ref(symbol=[])], [code_ref(), code_ref()],
            [{**code_ref(), "supported": True}],
        ):
            with self.subTest(refs=refs), self.assertRaises(ValueError):
                profile.validate_claims(document_fixture([{**claim_fixture(), "code_refs": refs}]), "D")

    def test_code_diagnostics_only_use_provided_bytes_without_filesystem_access(self):
        claim = claim_fixture()
        claim["code_refs"] = [code_ref(start=1, end=2), code_ref(start=3, end=3),
                              code_ref("/etc/passwd"), code_ref("../../private.txt"),
                              code_ref(None, None, None, "Handler.run"),
                              code_ref(start=None, end=None), code_ref("Handler.java")]
        claims = profile.validate_claims(document_fixture([claim]), "D")
        saved = deepcopy(claims)
        files = {"src/Handler.java": "first🙂\r\nsecond\n".encode("utf-8")}
        with patch("builtins.open", side_effect=AssertionError("No filesystem reads")), \
                patch.object(Path, "open", side_effect=AssertionError("No filesystem reads")):
            diagnostics = profile.check_code_refs(claims, files)
        self.assertEqual(claims, saved)
        self.assertEqual(diagnostics, [{"claim_id": "C01", "ref_index": index, "status": status}
                                      for index, status in enumerate([
                                          "resolved", "out_of_range", "unresolved_path", "unresolved_path",
                                          "no_position", "no_position", "unresolved_path"])])

    def test_returned_claims_share_no_mutable_objects_with_input(self):
        claim = claim_fixture()
        claim["code_refs"] = [code_ref()]
        document = document_fixture([claim])
        saved = deepcopy(document)
        result = profile.validate_claims(document, "D")
        result[0]["context"]["actor"] = "changed"
        result[0]["verification"]["required_evidence"].append("changed")
        result[0]["code_refs"][0]["path"] = "changed"
        result[0]["context_claim_ids"].append("C99")
        self.assertEqual(document, saved)

    def test_provider_parser_rejects_incomplete_duplicate_and_nontext_outputs(self):
        response = {"choices": [{"finish_reason": "stop", "message": {
            "role": "assistant", "content": json.dumps(document_fixture([]))}}]}
        self.assertEqual(profile.parse_response(response), document_fixture([]))
        variants = [[], {}, {"choices": []}]
        for reason in ("length", "content_filter", "tool_calls", None):
            bad = deepcopy(response)
            bad["choices"][0]["finish_reason"] = reason
            variants.append(bad)
        for key, value in (("refusal", "refused"), ("tool_calls", [{}]), ("content", None),
                           ("content", '{"claims":[],"claims":[]}')):
            bad = deepcopy(response)
            bad["choices"][0]["message"][key] = value
            variants.append(bad)
        for bad in variants:
            with self.subTest(response=bad), self.assertRaises(ValueError):
                profile.parse_response(bad)


if __name__ == "__main__":
    unittest.main()
