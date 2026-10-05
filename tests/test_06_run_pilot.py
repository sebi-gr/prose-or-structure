"""Offline planning, budget-journal and failure-isolation checks for the pilot runner."""

from collections import Counter
from importlib import import_module
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
pilot = import_module("06_run_pilot")
from tests.test_pilot_routes import make_catalog, response


class RunPilotTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        catalog_path, self.cases = make_catalog(self.root)
        registry = patch.object(pilot.case_context, "CATALOG", catalog_path)
        registry.start()
        self.addCleanup(registry.stop)
        self.config = pilot.load_config()
        self.output = self.root / "pilot"
        self.ledger = self.root / "budget.json"

    def body(self):
        return pilot.generator.json_bytes({"model": self.config["model"], "reasoning_effort": "none",
            "service_tier": "default", "max_completion_tokens": 100,
            "messages": [{"role": "system", "content": "Generic instructions"},
                         {"role": "user", "content": "🙂 source only"}]})

    def small_plan(self):
        plan = pilot.make_plan(self.cases)
        stages = {job["stage"]: job for job in plan["jobs"]
                  if job["case_id"] == "VUL4J-15" and job["case_variant"] == "vulnerable"
                  and job["repeat"] == 1}
        plan["jobs"] = [stages[name] for name in ("P_report", "P_claims", "D")]
        return plan

    def test_plan_balances_route_order_and_limits_extras_to_declared_repeats_and_subset(self):
        plan = pilot.make_plan(self.cases)
        self.assertEqual(len(plan["contexts"]), 10)
        self.assertEqual(len({job["id"] for job in plan["jobs"]}), len(plan["jobs"]))
        counts = Counter(job["stage"] for job in plan["jobs"])
        self.assertEqual(counts, {"P_report": 20, "P_claims": 20, "D": 20,
                                  "D_revision": 10, "P_no_context": 4, "D_no_context": 4,
                                  "P_baselines": 4})
        for context in plan["contexts"]:
            orders = []
            for repeat in (1, 2):
                jobs = [job for job in plan["jobs"] if job["case_id"] == context["case_id"]
                        and job["case_variant"] == context["case_variant"] and job["repeat"] == repeat
                        and job["stage"] in ("P_report", "P_claims", "D")]
                stages = [job["stage"] for job in jobs]
                self.assertLess(stages.index("P_report"), stages.index("P_claims"))
                p_claims = next(job for job in jobs if job["stage"] == "P_claims")
                p_report = next(job for job in jobs if job["stage"] == "P_report")
                self.assertEqual(p_claims["depends_on"], p_report["id"])
                orders.append([stage for stage in stages if stage != "P_claims"])
            self.assertEqual(orders[0], list(reversed(orders[1])))
        for job in plan["jobs"]:
            if job["stage"] not in ("P_report", "P_claims", "D"):
                self.assertEqual(job["repeat"], 1)
            if job["stage"] in ("P_no_context", "D_no_context", "P_baselines"):
                self.assertIn(job["case_id"], self.config["subset_cases"])
        self.assertEqual([job["id"] for job in plan["jobs"]],
                         [job["id"] for job in pilot.make_plan(self.cases)["jobs"]])

    def test_budget_reservation_is_persisted_before_transport_and_never_refunded(self):
        guard = pilot.BudgetGuard(self.ledger, 1, self.config)
        body = self.body()
        reservations = []
        def transport(sent, key):
            ledger = json.loads(self.ledger.read_bytes())
            self.assertEqual(sent, body)
            self.assertEqual(ledger["calls"][-1]["status"], "reserved")
            self.assertEqual(ledger["calls"][-1]["request_sha256"], pilot.generator.sha256(sent))
            self.assertGreater(ledger["reserved_upper_usd"], 0)
            self.assertNotIn(key, self.ledger.read_text())
            reservations.append(ledger["reserved_upper_usd"])
            return response({"claims": []})
        with patch.object(pilot.generator, "request_review", side_effect=transport) as request:
            guard.request(body, "SECRET_TEST_KEY")
            guard.request(body, "SECRET_TEST_KEY")
        self.assertEqual(request.call_count, 2)
        ledger = json.loads(self.ledger.read_bytes())
        self.assertEqual(ledger["reserved_upper_usd"], sum(entry["reserved_usd"] for entry in ledger["calls"]))
        self.assertGreater(reservations[1], reservations[0])
        self.assertEqual(ledger["calls"][0]["status"], "returned")
        self.assertIsNone(ledger["stop_reason"])

    def test_insufficient_budget_prevents_every_outbound_attempt(self):
        guard = pilot.BudgetGuard(self.ledger, .0000001, self.config)
        with patch.object(pilot.generator, "request_review") as request:
            for _ in range(2):
                with self.assertRaisesRegex(RuntimeError, "Budget reservation"):
                    guard.request(self.body(), "test-key")
        request.assert_not_called()
        ledger = json.loads(self.ledger.read_bytes())
        self.assertEqual(ledger["calls"], [])
        self.assertEqual(ledger["reserved_upper_usd"], 0)
        self.assertIn("Budget", ledger["stop_reason"])

    def test_unknown_usage_and_transport_failures_stop_later_calls_with_cost_reserved(self):
        for label, raw in (("missing", b'{}'), ("invalid", b'{"usage":{"prompt_tokens":true,"completion_tokens":2}}')):
            guard = pilot.BudgetGuard(self.root / f"{label}.json", 1, self.config)
            with patch.object(pilot.generator, "request_review", return_value=(200, None, raw)) as request:
                self.assertEqual(guard.request(self.body(), "key"), (200, None, raw))
                with self.assertRaises(RuntimeError):
                    guard.request(self.body(), "key")
            request.assert_called_once()
            self.assertGreater(guard.reserved, 0)
            self.assertIn("Usage", guard.stop_reason)
        guard = pilot.BudgetGuard(self.ledger, 1, self.config)
        with patch.object(pilot.generator, "request_review", side_effect=URLError("offline")) as request:
            with self.assertRaises(URLError):
                guard.request(self.body(), "key")
            with self.assertRaises(RuntimeError):
                guard.request(self.body(), "key")
        request.assert_called_once()
        ledger = json.loads(self.ledger.read_bytes())
        self.assertGreater(ledger["reserved_upper_usd"], 0)
        self.assertEqual(ledger["calls"][0]["status"], "transport_uncertain")

    def test_execute_requires_finite_budget_and_key_before_creating_output(self):
        with patch.object(pilot.generator, "request_review") as request:
            for limit in (None, 0, -1, float("inf"), float("nan")):
                with self.subTest(limit=limit), self.assertRaises(ValueError):
                    pilot.run_pilot(self.cases, self.output, execute=True, budget_usd=limit)
                self.assertFalse(self.output.exists())
            with patch.object(pilot.generator, "load_api_key", return_value=""):
                with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
                    pilot.run_pilot(self.cases, self.output, execute=True, budget_usd=1)
            self.assertFalse(self.output.exists())
        request.assert_not_called()

    def test_dry_run_never_reads_key_or_calls_provider(self):
        with patch.object(pilot.generator, "request_review", side_effect=AssertionError("No model request")) as request:
            with patch.object(pilot.generator, "load_api_key", side_effect=AssertionError("No API key needed")):
                result = pilot.run_pilot(self.cases, self.output)
        request.assert_not_called()
        self.assertEqual(result["mode"], "dry_run")
        self.assertEqual(result["status"], "planned")
        self.assertTrue((self.output / "plan.json").exists())
        self.assertFalse((self.output / "budget_ledger.json").exists())

    def test_independent_d_is_attempted_after_p_format_failure(self):
        malformed = response({"wrong_report_field": []})
        direct_response = response({"profile_version": "0.1", "route": "D", "claims": []})
        with patch.object(pilot, "make_plan", return_value=self.small_plan()):
            with patch.object(pilot.generator, "load_api_key", return_value="test-key"):
                with patch.object(pilot.generator, "request_review", side_effect=[malformed, direct_response]) as request:
                    result = pilot.run_pilot(self.cases, self.output, execute=True, budget_usd=1)
        self.assertEqual(request.call_count, 2)
        self.assertEqual([job["status"] for job in result["jobs"]],
                         ["invalid_output", "not_run_parent_failed", "no_claims"])
        self.assertEqual(result["status"], "completed_with_failures")
        self.assertIsNone(result["stop_reason"])

    def test_report_budget_stop_is_recorded_and_remaining_jobs_stay_visible(self):
        with patch.object(pilot, "make_plan", return_value=self.small_plan()):
            with patch.object(pilot.generator, "load_api_key", return_value="test-key"):
                with patch.object(pilot.generator, "request_review") as request:
                    result = pilot.run_pilot(self.cases, self.output, execute=True, budget_usd=.0000001)
        request.assert_not_called()
        self.assertEqual(len(result["jobs"]), 3)
        self.assertEqual(result["jobs"][0]["status"], "run_error")
        self.assertTrue(all(job["status"] == "not_run_budget_or_transport_stop" for job in result["jobs"][1:]))
        self.assertEqual(result["status"], "completed_with_failures")


if __name__ == "__main__":
    unittest.main()
