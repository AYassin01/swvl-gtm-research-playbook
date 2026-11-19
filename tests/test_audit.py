"""Synthetic fixtures only; these are not live research or pricing observations."""

import copy
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from checks import BUYER_COLUMNS, COMPANY_COLUMNS, check_ready, check_usage, host


class EvidenceChecks(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        base = Path(__file__).resolve().parents[1]
        self.s = json.loads((base / "templates/session.json").read_text())
        self.s.update(scope_confirmed=True, team_hypothesis_confirmed=True, icp="Synthetic test ICP", nesting_reviewed=True,
                      sampling_method="Alphabetical first five", decision="change_titles", access_checked=True)
        self.s["project"] = dict(industry="Test", geography="Test", size_policy="All", titles=["Test"], offer="Test")
        self.companies = [dict(company_name=f"Test {i:02}", website=f"https://c{i:02}.example.test", company_page_url=f"https://c{i:02}.example.test/about") for i in range(25)]
        self.s["company_audit"] = [dict(website=c["website"], fits_icp=True, sources=[c["company_page_url"]]) for c in self.companies]
        for key, value in (("tam", 40), ("sam", 30), ("som", 25)):
            self.s["markets"][key].update(value=value, kind="exact", reference=f"synthetic-{key}", filters=f"Test {key}", observed_at="2026-11-19T10:00:00+02:00")
        self.s["table"].update(url="https://app.clay.com/workspaces/synthetic/tables/synthetic", creation_path="browser", rows=25, columns=COMPANY_COLUMNS,
                                checked_at="2026-11-19T10:01:00+02:00", evidence=["table-check.md"])
        self.s["sample_domains"] = [host(c["website"]) for c in self.companies[:5]]
        self.s["rule"].update(definition="Synthetic role support", adopted_at="2026-11-19T10:02:00+02:00")
        self.s["buyer_search"].update(sample_frozen_at="2026-11-19T10:03:00+02:00", request_saved_at="2026-11-19T10:04:00+02:00",
                                       started_at="2026-11-19T10:05:00+02:00", reference="synthetic-people")
        self.s["people"] = [dict(name="Synthetic Person", job_title="Test role", company="Test 00", profile_link="https://profiles.example.test/one",
                                 company_domain="c00.example.test", classification="unconfirmed")]
        self.s["doubtful_check"].update(profile_link=self.s["people"][0]["profile_link"], sources=["https://profiles.example.test/one"], finding="Unconfirmed", owner_checked=True)
        self.s["links"]["video"] = "https://video.example.test/test"
        self.ledger = dict(schema_version="usage-v1", approvals=[dict(id="a1", provider="Clay", unit="clay_credits", cap=10,
                          approved_at="2026-11-19T09:50:00+02:00", owner_statement="Synthetic test approval", pricing_evidence=["price.md"])],
                          events=[dict(id="e1", at="2026-11-19T10:00:00+02:00", provider="Clay", tool="synthetic-search", job="Company discovery",
                          request_ref="synthetic-request", outcome="success", unit="clay_credits", metered=True, approval_id="a1", reserved=2,
                          pricing_evidence=["price.md"], actual=None, actual_evidence=[])], balances=[])
        for name in ("config.md", "capabilities.md", "method.md", "approval.md", "market-searches.md", "buyer-checks.md", "evidence.md", "usage-report.md", "evaluation.md", "video-script.md", "buyer-request.md", "codex-session-copy.md", "price.md", "actual.md", "table-check.md"):
            (self.root / name).write_text("Synthetic fixture, not real evidence\n")
        (self.root / "task1-note.md").write_text("Counts\nSize reason\nExcluded type\nTrust risk\n")
        (self.root / "task2-note.md").write_text("Rule\nCounts\nChange titles\n")

    def save(self, columns=None):
        (self.root / "session.json").write_text(json.dumps(self.s))
        (self.root / "ledger.json").write_text(json.dumps(self.ledger))
        with (self.root / "som-companies.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=columns or COMPANY_COLUMNS)
            w.writeheader(); w.writerows(self.companies)
        with (self.root / "buyer-results.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=BUYER_COLUMNS, extrasaction="ignore")
            w.writeheader(); w.writerows(self.s["people"])

    def ready(self, columns=None):
        self.save(columns)
        return check_ready(self.root)

    def usage(self):
        self.save()
        return check_usage(self.root)

    def test_failed_buyer_hypothesis_can_be_complete(self):
        errors, report = self.ready()
        self.assertEqual(errors, [])
        self.assertEqual(report["verified_relevant"], 0)
        self.assertIsNone(report["true_precision"])

    def test_company_shortfall_blocks(self):
        self.companies = self.companies[:7]
        self.assertTrue(any("25 distinct" in x for x in self.ready()[0]))

    def test_page_is_not_market_total(self):
        self.s["markets"]["tam"]["kind"] = "lower_bound"
        self.assertTrue(any("page/lower-bound" in x for x in self.ready()[0]))

    def test_extra_company_columns_block(self):
        self.assertTrue(any("exact submission columns" in x for x in self.ready(COMPANY_COLUMNS + ["extra"])[0]))

    def test_local_csv_is_not_clay_table(self):
        self.s["table"]["url"] = "som-companies.csv"
        self.assertTrue(any("CSV alone" in x for x in self.ready()[0]))

    def test_table_readback_required(self):
        self.s["table"]["evidence"] = []
        self.assertTrue(any("readback evidence" in x for x in self.ready()[0]))

    def test_unrelated_web_link_is_not_clay_table(self):
        self.s["table"]["url"] = "https://files.example.test/som.csv"
        self.assertTrue(any("CSV alone" in x for x in self.ready()[0]))

    def test_rule_must_precede_lookup(self):
        self.s["rule"]["adopted_at"] = "2026-11-19T10:06:00+02:00"
        self.assertTrue(any("must precede" in x for x in self.ready()[0]))

    def test_unconfirmed_is_not_verified(self):
        self.s["decision"] = "keep"
        self.assertTrue(any("Decision must follow" in x for x in self.ready()[0]))

    def test_false_relevance_needs_sources(self):
        self.s["people"][0]["classification"] = "relevant"
        self.assertTrue(any("Verified buyer needs" in x for x in self.ready()[0]))

    def test_unknown_actual_is_not_zero(self):
        errors, report = self.usage()
        self.assertEqual(errors, [])
        row = report["units"][0]
        self.assertEqual(row["possibly_metered_unknown_calls"], 1)
        self.assertEqual(row["reported_actual_subtotal"], 0)
        self.assertIsNone(self.ledger["events"][0]["actual"])

    def test_reported_zero_needs_accounting_evidence(self):
        self.ledger["events"][0]["actual"] = 0
        self.assertTrue(any("including zero" in x for x in self.usage()[0]))

    def test_reported_charge_has_evidence(self):
        self.ledger["events"][0].update(actual=1, actual_evidence=["actual.md"])
        errors, report = self.usage()
        self.assertEqual(errors, [])
        self.assertEqual(report["units"][0]["reported_actual_subtotal"], 1)

    def test_reservation_is_not_actual_charge(self):
        _, report = self.usage()
        row = report["units"][0]
        self.assertEqual(row["conservative_accounted"], 2)
        self.assertEqual(row["reported_actual_subtotal"], 0)

    def test_cap_overrun_blocks(self):
        self.ledger["events"][0]["reserved"] = 11
        self.assertTrue(any("cap exceeded" in x for x in self.usage()[0]))

    def test_actual_overrun_is_not_hidden(self):
        self.ledger["events"][0].update(actual=11, actual_evidence=["actual.md"])
        self.assertTrue(any("cap exceeded" in x for x in self.usage()[0]))

    def test_unknown_reservation_blocks_metered_call(self):
        self.ledger["events"][0]["reserved"] = None
        self.assertTrue(any("bounded reservation" in x for x in self.usage()[0]))

    def test_approval_must_precede_spend(self):
        self.ledger["approvals"][0]["approved_at"] = "2026-11-19T10:01:00+02:00"
        self.assertTrue(any("precede" in x for x in self.usage()[0]))

    def test_duplicate_approvals_do_not_inflate_cap(self):
        a = copy.deepcopy(self.ledger["approvals"][0]); a["id"] = "a2"
        self.ledger["approvals"].append(a)
        self.assertTrue(any("inflate caps" in x for x in self.usage()[0]))

    def test_nonmetered_needs_documented_basis(self):
        self.ledger["events"][0].update(metered=False, pricing_evidence=[])
        self.assertTrue(any("documented basis" in x for x in self.usage()[0]))

    def test_missing_video_blocks(self):
        self.s["links"]["video"] = ""
        self.assertTrue(any("Real video" in x for x in self.ready()[0]))

    def test_template_note_blocks(self):
        (self.root / "task2-note.md").write_text("Rule\nPENDING\nDecision\n")
        self.assertTrue(any("task2_note" in x for x in self.ready()[0]))


if __name__ == "__main__":
    unittest.main()
