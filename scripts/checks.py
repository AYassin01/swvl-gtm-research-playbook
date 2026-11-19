"""Offline packaging and usage checks. Source truth requires actual inspection."""

import csv
import json
import math
import re
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


COMPANY_COLUMNS = ["company_name", "website", "company_page_url"]
BUYER_COLUMNS = ["name", "job_title", "company", "profile_link"]


def web(value):
    p = urlparse(str(value))
    return p.scheme in {"http", "https"} and bool(p.hostname) and not p.username and not p.password


def host(value):
    return (urlparse(value if "://" in str(value) else "https://" + str(value)).hostname or "").lower().removeprefix("www.")


def stamp(value):
    try:
        d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return d if d.tzinfo else None
    except ValueError:
        return None


def amount(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def local(root, name):
    if not name or web(name):
        return None
    p = (root / str(name)).resolve()
    return p if p.is_relative_to(root.resolve()) and p.is_file() else None


def evidence(root, refs):
    return isinstance(refs, list) and bool(refs) and all(web(x) or local(root, x) for x in refs)


def load(root, name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def check_usage(root):
    root = Path(root).resolve()
    d = load(root, "ledger.json")
    errors, approvals, budgets, rows, ids = [], {}, {}, {}, set()

    def need(test, message):
        if not test:
            errors.append(message)

    need(d.get("schema_version") == "usage-v1", "Wrong usage schema")
    for a in d.get("approvals", []):
        key = (a.get("provider"), a.get("unit"))
        need(bool(a.get("id")) and a.get("id") not in approvals, "Approval IDs must be present and unique")
        need(all(key) and key not in budgets, "Use one approval per provider/unit; do not inflate caps with duplicates")
        need(amount(a.get("cap")) and stamp(a.get("approved_at")) and bool(a.get("owner_statement")), "Approval needs numeric cap, actual statement and aware timestamp")
        need(evidence(root, a.get("pricing_evidence")), "Approval requires applicable pricing evidence")
        approvals[a.get("id")] = a
        budgets[key] = a
    for e in d.get("events", []):
        need(bool(e.get("id")) and e.get("id") not in ids, "Event IDs must be present and unique")
        ids.add(e.get("id"))
        need(all(e.get(k) for k in ("provider", "tool", "job", "request_ref", "outcome", "unit")) and stamp(e.get("at")), "Every event needs tool/job/reference/outcome/unit and aware timestamp")
        key = (e.get("provider"), e.get("unit"))
        row = rows.setdefault(key, {"provider": key[0], "unit": key[1], "calls": 0, "conservative_accounted": 0,
                                    "reported_actual_subtotal": 0, "possibly_metered_unknown_calls": 0, "evidence": []})
        row["calls"] += 1
        metered, actual, reserved = e.get("metered"), e.get("actual"), e.get("reserved")
        need(type(metered) is bool or metered == "unknown", "Declare metered true/false/unknown")
        need(actual is None or amount(actual), "Actual charge must be finite/nonnegative or null")
        if actual is not None:
            need(evidence(root, e.get("actual_evidence")), "Reported actual, including zero, requires accounting evidence")
            if amount(actual):
                row["reported_actual_subtotal"] += actual
            row["evidence"].extend(e.get("actual_evidence") or [])
        if metered is not False:
            a = approvals.get(e.get("approval_id"), {})
            need((a.get("provider"), a.get("unit")) == key, "Possibly metered call requires matching provider/unit approval")
            start, approved = stamp(e.get("at")), stamp(a.get("approved_at"))
            need(start is not None and approved is not None and approved <= start, "Approval must precede the metered call")
            need(amount(reserved) and evidence(root, e.get("pricing_evidence")), "Possibly metered call requires a bounded reservation and price evidence")
            if amount(reserved):
                row["conservative_accounted"] += max(reserved, actual if amount(actual) else 0)
            row["possibly_metered_unknown_calls"] += actual is None
        else:
            need(evidence(root, e.get("pricing_evidence")), "Non-metered classification needs a documented basis")
            need(actual is None or actual == 0, "A positive charge cannot be labeled non-metered")
        row["evidence"].extend(e.get("pricing_evidence") or [])
    for key, row in rows.items():
        cap = budgets.get(key, {}).get("cap")
        row["approved_cap"] = cap
        row["evidence"] = sorted(set(row["evidence"]))
        if cap is not None and amount(cap):
            need(row["conservative_accounted"] <= cap, f"Approved cap exceeded for {key[0]}/{key[1]}")
    for b in d.get("balances", []):
        need(all(b.get(k) for k in ("provider", "unit")) and amount(b.get("value")) and stamp(b.get("at"))
             and evidence(root, b.get("evidence")), "Balance snapshots require actual values, times and evidence")
    return errors, {"units": list(rows.values()), "balance_observations": d.get("balances", []),
                    "note": "Reported actual subtotals are not unknown total charges; balance deltas are not automatically attributable"}


def check_ready(root):
    root = Path(root).resolve()
    d, errors = load(root, "session.json"), []

    def need(test, message):
        if not test:
            errors.append(message)

    def read_csv(name, fields):
        p = local(root, name)
        if not p:
            errors.append(f"Missing {name}")
            return []
        with p.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            need(reader.fieldnames == fields, f"{name}: exact submission columns required")
            rows = list(reader)
        need(all(None not in r and all(r.get(k) is not None for k in fields) for r in rows), f"Malformed {name}")
        return rows

    need(d.get("schema_version") == "session6-v1" and bool(d.get("owner")), "Missing Session 6 schema/owner")
    need(d.get("scope_confirmed") is True and d.get("team_hypothesis_confirmed") is True, "Scope and team hypothesis adoption pending")
    need(all(d.get("project", {}).get(k) for k in ("industry", "geography", "size_policy", "titles", "offer")) and bool(d.get("icp")), "Five project parts and falsifiable ICP required")
    counts, refs = [], []
    for key in ("tam", "sam", "som"):
        m = d.get("markets", {}).get(key, {})
        need(type(m.get("value")) is int and m["value"] >= 0, f"{key}: observed count required")
        kinds = {"exact", "estimated"} | ({"capacity_selection"} if key == "som" else set())
        need(m.get("kind") in kinds, f"{key}: page/lower-bound is not a completed total")
        need(m.get("provider") == "Clay" and all(m.get(k) for k in ("reference", "filters")) and stamp(m.get("observed_at")), f"{key}: actual Clay reference, filters and timestamp required")
        counts.append(m.get("value")); refs.append(m.get("reference"))
    need(len(set(refs)) == 3 and all(refs), "Three distinct Clay searches required")
    need(d.get("nesting_reviewed") is True, "Review logical search nesting")
    if all(type(n) is int for n in counts):
        need(counts[0] >= counts[1] >= counts[2], "TAM >= SAM >= SOM required")
    companies = read_csv("som-companies.csv", COMPANY_COLUMNS)
    domains = [host(c.get("website", "")) for c in companies]
    need(len(companies) >= 25 and len(set(domains)) == len(domains) and all(domains), "At least 25 distinct matching company domains required")
    audit = {host(x.get("website", "")): x for x in d.get("company_audit", [])}
    for c, dom in zip(companies, domains):
        a = audit.get(dom, {})
        need(bool(c.get("company_name")) and web(c.get("website")) and web(c.get("company_page_url")), "Company name, website and actual company page required")
        need(a.get("fits_icp") is True and evidence(root, a.get("sources")), f"Company-fit evidence missing: {dom}")
    need(counts[2] == len(companies), "SOM selected count must match the table rows")
    table = d.get("table", {})
    need(web(table.get("url")) and host(table.get("url", "")) == "app.clay.com" and table.get("creation_path") in {"tool", "browser"}, "Real tool/browser-created Clay table required; CSV alone is insufficient")
    need(table.get("rows") == len(companies) and table.get("columns") == COMPANY_COLUMNS and stamp(table.get("checked_at"))
         and evidence(root, table.get("evidence")), "Actual table row/column readback evidence required")
    sample = [host(x) for x in d.get("sample_domains", [])]
    need(len(sample) == 5 and len(set(sample)) == 5 and set(sample).issubset(domains) and bool(d.get("sampling_method")), "Frozen five-company sample/method required")
    rule, search = d.get("rule", {}), d.get("buyer_search", {})
    threshold = rule.get("threshold")
    need(type(threshold) is int and 1 <= threshold <= 10 and bool(rule.get("definition")), "Adopt a defined numerical rule")
    adopted, frozen, requested, start = [stamp(x) for x in (rule.get("adopted_at"), search.get("sample_frozen_at"), search.get("request_saved_at"), search.get("started_at"))]
    need(all((adopted, frozen, requested, start)) and adopted <= start and frozen <= requested <= start, "Rule, sample and owner request must precede buyer retrieval")
    need(bool(search.get("reference")) and local(root, search.get("request_file")), "Actual buyer query reference and exact owner request required")
    people = d.get("people", [])
    buyer_rows = read_csv("buyer-results.csv", BUYER_COLUMNS)
    need(Counter(tuple(r.get(k, "") for k in BUYER_COLUMNS) for r in buyer_rows) == Counter(tuple(r.get(k, "") for k in BUYER_COLUMNS) for r in people), "Buyer CSV must match original primary records")
    profiles = [p.get("profile_link") for p in people]
    per_company = Counter(host(p.get("company_domain", "")) for p in people)
    need(len(people) <= 10 and len(profiles) == len(set(profiles)) and set(per_company).issubset(sample) and all(n <= 2 for n in per_company.values()), "Primary sample is fixed: two per firm, ten requested; preserve/explain over-returns")
    verified, unknown = 0, 0
    for p in people:
        need(all(p.get(k) for k in BUYER_COLUMNS) and web(p.get("profile_link")), "Four professional fields and a real profile URL required")
        status = p.get("classification")
        need(status in {"relevant", "not_relevant", "unconfirmed"}, "Invalid person classification")
        if status == "relevant":
            verified += 1
            need(all(p.get(k) is True for k in ("current_employer_supported", "local_remit_supported", "transport_role_supported")) and evidence(root, p.get("evidence")), "Verified buyer needs current-employer/local/transport-role support")
        unknown += status == "unconfirmed"
    decision = {"keep"} if type(threshold) is int and verified >= threshold else {"change_titles", "change_filters"}
    need(d.get("decision") in decision, "Decision must follow the original rule; failed yield is valid")
    check = d.get("doubtful_check", {})
    need(bool(check.get("profile_link")) and check.get("profile_link") in profiles and bool(check.get("finding"))
         and evidence(root, check.get("sources")) and check.get("owner_checked") is True, "Actual doubtful-answer check and owner inspection required")
    links = d.get("links", {})
    for key, n in (("task1_note", 4), ("task2_note", 3)):
        p = local(root, links.get(key))
        lines = [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()] if p else []
        need(len(lines) == n and not any(x in "\n".join(lines) for x in ("PENDING", "TODO", "TBD")), f"{key}: exactly {n} completed nonempty lines required")
    need(web(links.get("session_copy")) or local(root, links.get("session_copy")), "Actual session copy/link required")
    need(web(links.get("video")) and d.get("access_checked") is True, "Real video and owner access check required")
    for name in ("config.md", "capabilities.md", "method.md", "approval.md", "market-searches.md", "buyer-checks.md", "evidence.md", "usage-report.md", "evaluation.md", "video-script.md"):
        p = local(root, name)
        need(p is not None and bool(p.read_text(encoding="utf-8").strip()), f"Missing supporting artifact: {name}")
    usage_errors, usage = check_usage(root)
    errors.extend(usage_errors)
    ledger = load(root, "ledger.json")
    need(any(str(e.get("provider", "")).lower() == "clay" for e in ledger.get("events", [])), "Actual Clay tool-use evidence required")
    need(any(str(a.get("provider", "")).lower() == "clay" for a in ledger.get("approvals", [])), "Actual numeric Clay scope approval required")
    return errors, {"som_rows": len(companies), "companies_returning_people": len(per_company), "people_found": len(people),
                    "verified_relevant": verified, "unconfirmed": unknown, "verified_requested_yield": verified / 10,
                    "true_precision": None if unknown or not people else verified / len(people), "usage": usage}


def check_repo(root):
    root = Path(root).resolve()
    try:
        names = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True).stdout.decode().split("\0")
        paths = [root / n for n in names if n]
    except (OSError, subprocess.CalledProcessError):
        paths = [p for p in root.rglob("*") if p.is_file() and not any(x in {".git", "__pycache__", ".private", "private", "raw"} for x in p.relative_to(root).parts)]
    errors = []
    for p in paths:
        rel = p.relative_to(root)
        if any(x in {".private", "private", "raw"} for x in rel.parts):
            errors.append(f"Private/raw path in tracked files: {rel}")
        if p.suffix not in {"", ".md", ".txt", ".json", ".csv", ".py", ".yml", ".yaml"} and p.name != ".gitignore":
            errors.append(f"Non-text deliverable: {rel}")
        try:
            s = p.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"Unreadable UTF-8 file: {rel}"); continue
        if "\x00" in s or re.search(r"gh[pousr]_[A-Za-z0-9]{30,}", s):
            errors.append(f"Binary/credential marker: {rel}")
        if p.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", s):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                if not (p.parent / target.split("#", 1)[0]).exists():
                    errors.append(f"Broken local link: {rel}: {target}")
    return errors
