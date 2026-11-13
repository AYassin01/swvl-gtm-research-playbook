"""Adversarial tests use fictional fixtures and the frozen historical dataset."""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from evaluate import CRITERIA, DIMENSIONS, TAGS, disposition, evaluate


def fixture():
    sources = []
    accounts = []
    for i in range(1, 4):
        sid = f"S{i}"
        aid = f"A{i}"
        sources.append({
            "id": sid, "url": f"https://example.com/employer/{i}", "status": "opened",
            "observed_on": "2026-11-13", "checked_on": "2026-11-13",
            "publisher_type": "employer", "summary": "Synthetic evidence for evaluator tests.",
            "supports": [f"{aid}.{k}" for k in CRITERIA],
        })
        accounts.append({
            "id": aid, "account": f"Fictional account {i}", "domain": f"account{i}.example",
            "buying_unit": f"unit{i}", "scope": "Fictional Cairo site",
            "named_route_in": f"Fictional local buyer {i}", "buyer_authority": "unconfirmed",
            "buyer_verified_on": "2026-11-13", "invoice_gap": "unconfirmed",
            "motion": "New logo", "next_check": "Verify the operating baseline.",
            "scores": {key: {
                "score": 3, "note": "Fictional supporting claim.", "source_id": sid,
                "support_tag": TAGS[key], "scope_confirmed": True,
                "evidence_date": "2026-11-13", "event_on": "2026-10-01",
                "activity_on": "2026-11-01",
            } for key in CRITERIA},
        })
    sources.append({
        "id": "S4", "url": "https://example.com/vendor", "status": "opened",
        "observed_on": "2026-11-13", "checked_on": "2026-11-13",
        "publisher_type": "vendor", "summary": "Synthetic delivery-capability statement.",
        "supports": ["segment.swvl_delivery"],
    })
    return {
        "schema_version": 1, "run_id": "synthetic-preview", "mode": "preview",
        "as_of": "2026-11-13", "author": "Run author", "target_accounts": 3,
        "budgets": {"clay_credits": 0, "crustdata_credits": 0, "treg_usd": 0, "provider_calls": 0},
        "tool_calls": [], "accounts": accounts, "sources": sources,
        "segment_assessment": {
            "status": "accepted_for_discovery", "purchase_readiness": "unconfirmed",
            "notes": "Synthetic preview qualification.",
            "employer_transport_source_ids": ["S1", "S2", "S3"],
            "workflow_source_ids": ["S1"], "swvl_delivery_source_ids": ["S4"],
        },
        "human_review": {
            "status": "approved", "reviewer": "Different reviewer", "reviewed_on": "2026-11-13",
            "dimensions": {k: 2 for k in DIMENSIONS}, "notes": "Synthetic review for test coverage.",
        },
    }


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.run = fixture()

    def fails(self, text, release=False):
        self.assertTrue(any(text in e for e in evaluate(self.run, release)), text)

    def test_valid_preview_release(self):
        self.assertEqual(evaluate(self.run, True), [])

    def test_baseline_reproduces_saved_counts(self):
        baseline = json.loads((ROOT / "data/baseline.json").read_text())
        self.assertEqual(evaluate(baseline), [])
        from collections import Counter
        self.assertEqual(Counter(disposition(a) for a in baseline["accounts"]), {
            "Priority discovery": 4, "Discovery queue": 10, "Verify first": 6,
            "CRM review": 4, "Exclude": 1,
        })
        self.assertTrue(evaluate(baseline, True))

    def test_exclusion_overrides_high_total(self):
        a = self.run["accounts"][0]
        a["scores"]["clean"]["score"] = 1
        self.assertEqual(disposition(a), "Exclude")

    def test_crm_overrides_high_total(self):
        a = self.run["accounts"][0]
        a["motion"] = "CRM review"
        self.assertEqual(disposition(a), "CRM review")

    def test_exclusion_also_overrides_crm(self):
        a = self.run["accounts"][0]
        a["motion"] = "CRM review"
        a["scores"]["clean"]["score"] = 1
        self.assertEqual(disposition(a), "Exclude")

    def test_duplicate_buying_unit(self):
        self.run["accounts"][1]["buying_unit"] = "unit1"
        self.fails("duplicate buying unit")

    def test_duplicate_domain(self):
        self.run["accounts"][1]["domain"] = "account1.example"
        self.fails("duplicate domain")

    def test_missing_source(self):
        self.run["accounts"][0]["scores"]["pain"]["source_id"] = "missing"
        self.fails("missing source reference")

    def test_boolean_cannot_be_score(self):
        self.run["accounts"][0]["scores"]["pain"]["score"] = True
        self.fails("score must be")

    def test_high_score_requires_support(self):
        self.run["accounts"][0]["scores"]["pain"]["support_tag"] = "funded_rides"
        self.fails("unsupported score 3", True)

    def test_stale_trigger_rejected(self):
        self.run["accounts"][0]["scores"]["trigger"]["event_on"] = "2025-01-01"
        self.fails("trigger event is stale", True)

    def test_future_trigger_rejected(self):
        self.run["accounts"][0]["scores"]["trigger"]["event_on"] = "2027-01-01"
        self.fails("trigger event is stale", True)

    def test_stale_buyer_activity_rejected(self):
        self.run["accounts"][0]["scores"]["persona"]["activity_on"] = "2025-01-01"
        self.fails("buyer activity is stale", True)

    def test_unopened_source_rejected(self):
        self.run["sources"][0]["status"] = "historical_import"
        self.fails("source was not opened", True)

    def test_self_review_rejected(self):
        self.run["human_review"]["reviewer"] = "Run author"
        self.fails("Independent named reviewer", True)

    def test_low_human_score_rejected(self):
        self.run["human_review"]["dimensions"]["source_support"] = 0
        self.fails("Human review threshold", True)

    def test_claimed_invoice_gap_requires_validation(self):
        self.run["accounts"][0]["invoice_gap"] = "confirmed"
        self.fails("permissioned invoice_gap validation")

    def test_missing_human_approval(self):
        self.run["human_review"]["status"] = "pending"
        self.fails("Human review pending", True)

    def call(self):
        self.run["budgets"]["provider_calls"] = 4
        self.run["budgets"]["treg_usd"] = 1
        return {
            "provider": "treg", "tool": "call", "job": "Fetch missing employer source",
            "entity": "https://example.com/job", "cache_key": "treg|job|example|2026-11",
            "metered": True, "reserved_cost": 0.2, "actual_cost": None,
            "unit": "treg_usd", "outcome": "success",
        }

    def test_unknown_cost_rejected(self):
        call = self.call()
        call["reserved_cost"] = None
        self.run["tool_calls"] = [call]
        self.fails("unknown or invalid cost reservation")

    def test_actual_cost_over_cap_rejected(self):
        call = self.call()
        call["actual_cost"] = 1.2
        self.run["tool_calls"] = [call]
        self.fails("Budget exceeded")

    def test_error_reservation_counts(self):
        call = self.call()
        call["outcome"] = "error"
        call["reserved_cost"] = 2
        self.run["tool_calls"] = [call]
        self.fails("Budget exceeded")

    def test_duplicate_call_requires_reason(self):
        call = self.call()
        self.run["tool_calls"] = [call, copy.deepcopy(call)]
        self.fails("duplicate lookup")

    def test_wrong_provider_unit_rejected(self):
        call = self.call()
        call["unit"] = "clay_credits"
        self.run["tool_calls"] = [call]
        self.fails("wrong cost unit")

    def test_infinite_cost_rejected(self):
        call = self.call()
        call["reserved_cost"] = float("inf")
        self.run["tool_calls"] = [call]
        self.fails("invalid cost reservation")

    def test_duplicate_claim_support_is_not_enough(self):
        self.run["segment_assessment"]["employer_transport_source_ids"] = ["S1", "S1", "S1"]
        self.fails("insufficient independent sources", True)

    def test_full_run_cannot_release_three_accounts(self):
        self.run["mode"] = "full"
        self.run["target_accounts"] = 25
        self.fails("Expected 25 accounts", True)

    def test_malformed_support_list_is_reported(self):
        self.run["sources"][0]["supports"] = None
        self.fails("supports must be a list", True)

    def test_malformed_criterion_is_reported(self):
        self.run["accounts"][0]["scores"]["persona"] = None
        self.fails("criterion must be an object", True)

    def test_invalid_root_is_reported(self):
        self.assertEqual(evaluate([]), ["Run must be a JSON object"])

    def test_query_credential_rejected(self):
        self.run["sources"][0]["url"] = "https://example.com/source?api_key=example-placeholder"
        self.fails("credential-bearing HTTPS URL")

    def test_malformed_provider_is_reported(self):
        call = self.call()
        call["provider"] = {"unexpected": "object"}
        self.run["tool_calls"] = [call]
        self.fails("unknown provider")


if __name__ == "__main__":
    unittest.main()
