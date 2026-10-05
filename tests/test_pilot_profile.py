"""The context ablation changes explicit fields, not the remaining claim semantics."""

from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pilot_profile

profile = pilot_profile.claim_profile


def claim_fixture():
    return {
        "claim_id": "C01", "proposition": "An actor could read data if enabled.",
        "family": "exploitability_impact", "subtype": "impact", "family_reason": "Possible effect.",
        "source_quotes": [], "code_refs": [], "context_claim_ids": [],
        "verification": {"question": "Can this effect occur if enabled?",
                         "required_evidence": ["Runtime configuration and the complete path."],
                         "assumptions": []},
    }


class PilotProfileTests(unittest.TestCase):
    def test_default_resources_and_validation_remain_unchanged(self):
        prompt = profile.RESOURCES / "decomposition_prompt.txt"
        resources = pilot_profile.resources(prompt)
        self.assertEqual(resources, {path.name: path.read_bytes()
                                    for path in (prompt, profile.CODEBOOK, profile.SCHEMA)})
        claim = claim_fixture()
        claim["context"] = {key: None for key in profile.CONTEXT_FIELDS}
        document = {"profile_version": "0.1", "route": "D", "claims": [claim]}
        self.assertEqual(pilot_profile.validate(document, "D"), profile.validate_claims(document, "D"))

    def test_ablation_removes_only_explicit_context_fields_from_contract(self):
        before = profile.SCHEMA.read_bytes()
        original = json.loads(before)
        for name in ("decomposition_prompt.txt", "direct_claim_prompt.txt"):
            resources = pilot_profile.resources(profile.RESOURCES / name, True)
            schema = json.loads(resources[profile.SCHEMA.name])
            claim = schema["$defs"]["claim"]
            self.assertNotIn("context", claim["required"])
            self.assertNotIn("context", claim["properties"])
            self.assertIn("context_claim_ids", claim["required"])
            self.assertFalse(claim["additionalProperties"])
            for key, value in original["$defs"]["claim"]["properties"].items():
                if key != "context":
                    self.assertEqual(claim["properties"][key], value)
            prompt = resources[name].decode()
            codebook = resources[profile.CODEBOOK.name].decode()
            self.assertNotIn("six context fields", prompt)
            self.assertNotIn("`context.preconditions`", codebook)
            self.assertNotIn("`modality: null`", codebook)
            self.assertIn("context_claim_ids", prompt)
            self.assertIn("Preserve all conditions in the proposition", prompt)
            self.assertIn("Bedingungen und Geltungsbereich bleiben in der Proposition", codebook)
            self.assertIn("Eine Bedingung nicht", codebook)
            self.assertIn("`verification.question`", codebook)
        self.assertEqual(profile.SCHEMA.read_bytes(), before)

    def test_ablation_validates_without_mutating_or_fabricating_fields(self):
        first = claim_fixture()
        second = {**deepcopy(first), "claim_id": "C02", "context_claim_ids": ["C01"]}
        document = {"profile_version": "0.1", "route": "D", "claims": [first, second]}
        original = deepcopy(document)
        claims = pilot_profile.validate(document, "D", no_context_fields=True)
        self.assertEqual(document, original)
        self.assertEqual(claims, document["claims"])
        self.assertTrue(all("context" not in claim for claim in claims))
        claims[1]["verification"]["assumptions"].append("Synthetic new assumption")
        self.assertEqual(document, original)
        with self.assertRaises(ValueError):
            pilot_profile.validate(document, "D")

    def test_ablation_keeps_exact_p_quotes_and_unicode_offsets(self):
        finding = {"title": "Report", "report": "🙂 ababa.\r\nIf enabled, it could occur."}
        claim = claim_fixture()
        claim["source_quotes"] = [{"field": "report", "quote": "aba", "occurrence": 2}]
        document = {"profile_version": "0.1", "route": "P", "claims": [claim]}
        result = pilot_profile.validate(document, "P", finding, no_context_fields=True)
        self.assertEqual(result[0]["source_quotes"][0],
                         {"field": "report", "quote": "aba", "occurrence": 2, "start": 4, "end": 7})
        self.assertNotIn("context", result[0])
        self.assertNotIn("start", document["claims"][0]["source_quotes"][0])

    def test_remaining_errors_and_explicit_context_are_not_silently_accepted(self):
        variants = [
            {**claim_fixture(), "context": {key: None for key in profile.CONTEXT_FIELDS}},
            {**claim_fixture(), "context": None},
            {**claim_fixture(), "context_claim_ids": ["C01"]},
            {**claim_fixture(), "context_claim_ids": ["C99"]},
            {**claim_fixture(), "verification_status": "supported"},
            {**claim_fixture(), "proposition": " "},
            {**claim_fixture(), "source_quotes": [{"field": "report", "quote": "x", "occurrence": 1}]},
            None,
        ]
        for claim in variants:
            with self.subTest(claim=claim), self.assertRaises(ValueError):
                pilot_profile.validate({"profile_version": "0.1", "route": "D", "claims": [claim]},
                                       "D", no_context_fields=True)
        for document in ({"profile_version": "0.1", "route": "P", "claims": []},
                         {"profile_version": "0.2", "route": "D", "claims": []},
                         {"profile_version": "0.1", "route": "D", "claims": {}}, []):
            with self.subTest(document=document), self.assertRaises(ValueError):
                pilot_profile.validate(document, "D", no_context_fields=True)
        self.assertEqual(pilot_profile.validate({"profile_version": "0.1", "route": "D", "claims": []},
                                               "D", no_context_fields=True), [])

    def test_changed_field_instructions_fail_instead_of_sending_a_conflicting_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            prompt = Path(directory) / "direct_claim_prompt.txt"
            original = profile.RESOURCES / prompt.name
            prompt.write_text(original.read_text().replace("six context fields", "a new context format"))
            with self.assertRaisesRegex(ValueError, "resource changed"):
                pilot_profile.resources(prompt, True)


if __name__ == "__main__":
    unittest.main()
