"""Synthetic fixtures only. These are not research records or real companies."""

import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("session6_check", Path(__file__).resolve().parents[1] / "check_submission.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class SessionChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = json.loads((Path(__file__).resolve().parents[1] / "templates/session.json").read_text())
        self.data.update(config_confirmed=True, team_hypothesis_confirmed=True, icp="Synthetic test ICP", nesting_reviewed=True,
                         sampling_method="Alphabetical first five", decision="change_titles", access_checked=True)
        self.data["project"] = dict(industry="Test", geography="Test", company_size="All", titles=["Test role"], offer="Test offer")
        self.companies = [dict(company_name=f"Test {n:02}", website=f"https://c{n:02}.example.test", company_page_url=f"https://c{n:02}.example.test/about") for n in range(25)]
        self.data["company_audit"] = [dict(website=c["website"], fits_icp=True, service_source=c["company_page_url"], site_source=c["company_page_url"]) for c in self.companies]
        for key, value in (("tam", 40), ("sam", 30), ("som", 25)):
            self.data["markets"][key].update(value=value, kind="exact", reference=f"test-{key}", filters=f"Test {key}", observed_at="2026-11-19T10:00:00+02:00")
        self.data["sample_domains"] = [CHECK.domain(c["website"]) for c in self.companies[:5]]
        self.data["rule"].update(definition="Supported test role", adopted_at="2026-11-19T10:01:00+02:00")
        self.data["buyer_search"].update(reference="test-people", sample_frozen_at="2026-11-19T10:02:00+02:00",
                                        request_saved_at="2026-11-19T10:03:00+02:00", started_at="2026-11-19T10:04:00+02:00")
        person = dict(name="Synthetic Person", job_title="Test role", company="Test 00", company_domain="c00.example.test",
                      profile_link="https://profiles.example.test/one", classification="unconfirmed")
        self.data["people"] = [person]
        self.data["doubtful_check"].update(profile_link=person["profile_link"], finding="Test profile remains unconfirmed",
                                           sources=[person["profile_link"]], owner_checked=True)
        self.data["links"].update(workbook="https://workbook.example.test/test", video="https://video.example.test/test")
        for name in ("project-and-icp.md", "market-searches.md", "buyer-checks.md", "evidence.md", "credits.md", "evaluation.md",
                     "video-script.md", "buyer-search-request.md", "codex-session-copy.md"):
            (self.root / name).write_text("Synthetic test artifact\n")
        (self.root / "task1-note.md").write_text("Counts recorded\nSize reason\nExcluded type\nOne risk\n")
        (self.root / "task2-note.md").write_text("Rule\nMeasured counts\nChange titles\n")

    def run_check(self, columns=None):
        (self.root / "session.json").write_text(json.dumps(self.data))
        with (self.root / "som-companies.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=columns or CHECK.COMPANY_COLUMNS)
            w.writeheader()
            w.writerows(self.companies)
        with (self.root / "buyer-results.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CHECK.BUYER_COLUMNS, extrasaction="ignore")
            w.writeheader()
            w.writerows(self.data["people"])
        return CHECK.validate_run(self.root)

    def test_failed_hypothesis_can_be_complete(self):
        errors, counts = self.run_check()
        self.assertEqual(errors, [])
        self.assertEqual(counts["verified_relevant"], 0)
        self.assertIsNone(counts["true_precision"])

    def test_company_shortfall_blocks(self):
        self.companies = self.companies[:7]
        self.assertTrue(any("At least 25" in x for x in self.run_check()[0]))

    def test_duplicate_domain_blocks(self):
        self.companies[-1]["website"] = self.companies[0]["website"]
        self.assertTrue(any("unique" in x for x in self.run_check()[0]))

    def test_extra_company_column_blocks(self):
        self.assertTrue(any("exactly" in x for x in self.run_check(CHECK.COMPANY_COLUMNS + ["enrichment"])[0]))

    def test_missing_website_blocks(self):
        self.companies[0]["website"] = ""
        self.assertTrue(any("real website" in x for x in self.run_check()[0]))

    def test_nonmatching_company_blocks(self):
        self.data["company_audit"][0]["fits_icp"] = False
        self.assertTrue(any("Company-fit evidence" in x for x in self.run_check()[0]))

    def test_page_lower_bound_blocks(self):
        self.data["markets"]["tam"]["kind"] = "lower_bound"
        self.assertTrue(any("lower-bound" in x for x in self.run_check()[0]))

    def test_changed_rule_after_results_blocks(self):
        self.data["rule"]["adopted_at"] = "2026-11-19T10:05:00+02:00"
        self.assertTrue(any("Adopt the rule before" in x for x in self.run_check()[0]))

    def test_late_personal_request_blocks(self):
        self.data["buyer_search"]["request_saved_at"] = "2026-11-19T10:05:00+02:00"
        self.assertTrue(any("personal request before" in x for x in self.run_check()[0]))

    def test_unconfirmed_is_not_verified(self):
        self.data["decision"] = "keep"
        errors, counts = self.run_check()
        self.assertEqual(counts["verified_relevant"], 0)
        self.assertTrue(any("Decision must follow" in x for x in errors))

    def test_claimed_relevance_needs_support(self):
        self.data["people"][0]["classification"] = "relevant"
        self.assertTrue(any("Verified buyer requires" in x for x in self.run_check()[0]))

    def test_missing_video_blocks(self):
        self.data["links"]["video"] = ""
        self.assertTrue(any("video URL" in x for x in self.run_check()[0]))

    def test_placeholder_note_blocks(self):
        (self.root / "task2-note.md").write_text("Rule\nPENDING\nDecision\n")
        self.assertTrue(any("task2_note" in x for x in self.run_check()[0]))


if __name__ == "__main__":
    unittest.main()
