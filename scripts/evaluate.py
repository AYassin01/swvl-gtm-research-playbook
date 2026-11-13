"""Offline structure, budget and release checks for a Team 03 research run."""

import argparse
import json
import math
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit


CRITERIA = ("size", "trigger", "pain", "persona", "clean")
UNITS = {"clay": "clay_credits", "crustdata": "crustdata_credits", "treg": "treg_usd"}
TAGS = {
    "size": "local_size_core",
    "trigger": "recent_trigger",
    "pain": "specific_transport_workflow",
    "persona": "named_active_buyer",
    "clean": "company_arranged_late_rides",
}
DIMENSIONS = (
    "source_support", "segment_purchase_logic", "buyer_mapping",
    "offer_deliverability", "score_calibration", "tool_cost_discipline",
)
PUBLISHERS = {
    "employer", "vendor", "regulator", "institution", "professional_profile",
    "press", "provider", "unreviewed",
}
STATUSES = {"historical_import", "opened", "blocked", "missing"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def recent(value, as_of, days):
    parsed = parse_date(value)
    return parsed is not None and as_of is not None and 0 <= (as_of - parsed).days <= days


def disposition(account):
    scores = {key: account["scores"][key]["score"] for key in CRITERIA}
    if scores["clean"] == 1:
        return "Exclude"
    if account["motion"] == "CRM review":
        return "CRM review"
    if (sum(scores.values()) >= 12 and scores["size"] >= 2
            and scores["persona"] >= 2 and scores["clean"] == 3
            and (scores["trigger"] == 3 or scores["pain"] == 3)):
        return "Priority discovery"
    if scores["clean"] == 3 and scores["pain"] >= 2 and scores["persona"] >= 2:
        return "Discovery queue"
    return "Verify first"


def evaluate(run, release=False):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    if not isinstance(run, dict):
        return ["Run must be a JSON object"]
    require(run.get("schema_version") == 1, "Unsupported schema_version")
    mode = run.get("mode")
    require(isinstance(mode, str) and mode in {"replay", "preview", "full", "refresh"}, "Invalid mode")
    if not isinstance(mode, str):
        mode = "invalid"
    as_of = parse_date(run.get("as_of"))
    require(as_of is not None, "Invalid as_of date")
    require(nonempty(run.get("run_id")), "Missing run_id")
    target = run.get("target_accounts")
    require(type(target) is int and target > 0, "Invalid target_accounts")
    if mode == "preview":
        require(target == 3, "Preview target must be 3")
    if mode in {"full", "refresh"}:
        require(type(target) is int and target >= 25, "Full/refresh target must be at least 25")

    accounts = run.get("accounts")
    sources = run.get("sources")
    calls = run.get("tool_calls")
    require(isinstance(accounts, list), "accounts must be a list")
    require(isinstance(sources, list), "sources must be a list")
    require(isinstance(calls, list), "tool_calls must be a list")
    if errors:
        return errors
    require(len(accounts) == target, f"Expected {target} accounts, found {len(accounts)}")

    source_map = {}
    urls = set()
    for source in sources:
        if not isinstance(source, dict):
            errors.append("Source must be an object")
            continue
        sid = source.get("id")
        require(nonempty(sid), "Missing source id")
        if not isinstance(sid, str):
            continue
        require(sid not in source_map, f"Duplicate source id {sid}")
        source_map[sid] = source
        url = source.get("url", "")
        try:
            parsed = urlsplit(url)
            sensitive_keys = {"api_key", "apikey", "access_token", "token", "secret", "authorization"}
            valid_url = (parsed.scheme == "https" and bool(parsed.hostname)
                         and not parsed.username and not parsed.password
                         and not any(key.lower() in sensitive_keys for key, _ in parse_qsl(parsed.query)))
        except (ValueError, TypeError, AttributeError):
            valid_url = False
        require(valid_url, f"{sid}: invalid or credential-bearing HTTPS URL")
        require(isinstance(url, str) and url not in urls, f"{sid}: duplicate or invalid URL")
        if isinstance(url, str):
            urls.add(url)
        status = source.get("status")
        publisher = source.get("publisher_type")
        require(isinstance(status, str) and status in STATUSES, f"{sid}: invalid source status")
        require(isinstance(publisher, str) and publisher in PUBLISHERS, f"{sid}: invalid publisher_type")
        require(parse_date(source.get("observed_on")) is not None, f"{sid}: invalid observed_on")
        require(isinstance(source.get("supports"), list), f"{sid}: supports must be a list")

    ids = set()
    units = set()
    domains = {}
    for account in accounts:
        if not isinstance(account, dict):
            errors.append("Account must be an object")
            continue
        aid = account.get("id")
        require(nonempty(aid), "Missing account id")
        if not isinstance(aid, str):
            continue
        require(aid not in ids, f"Duplicate account id {aid}")
        ids.add(aid)
        for field in ("account", "domain", "buying_unit", "scope", "named_route_in", "next_check"):
            require(nonempty(account.get(field)), f"{aid}: missing {field}")
        unit = str(account.get("buying_unit", "")).strip().lower()
        domain = str(account.get("domain", "")).strip().lower().removeprefix("www.")
        require(unit not in units, f"{aid}: duplicate buying unit")
        units.add(unit)
        if domain in domains:
            previous = domains[domain]
            require(nonempty(account.get("independent_buying_justification"))
                    and nonempty(previous.get("independent_buying_justification"))
                    and nonempty(account.get("parent")) and account.get("parent") == previous.get("parent"),
                    f"{aid}: duplicate domain without independent procurement evidence")
        domains[domain] = account
        require("/" not in domain and "." in domain and " " not in domain, f"{aid}: invalid bare domain")
        require(account.get("motion") in ("New logo", "CRM review"), f"{aid}: invalid motion")
        require(account.get("buyer_authority") in ("unconfirmed", "confirmed"), f"{aid}: invalid buyer_authority")
        require(account.get("invoice_gap") in ("unconfirmed", "confirmed"), f"{aid}: invalid invoice_gap")
        for field in ("buyer_authority", "invoice_gap"):
            if account.get(field) == "confirmed":
                require(nonempty(account.get(field + "_validation")), f"{aid}: missing permissioned {field} validation")
        scores = account.get("scores")
        if not isinstance(scores, dict) or set(scores) != set(CRITERIA):
            errors.append(f"{aid}: exactly five criteria required")
            continue
        for key, entry in scores.items():
            label = f"{aid}.{key}"
            if not isinstance(entry, dict):
                errors.append(f"{label}: criterion must be an object")
                continue
            score = entry.get("score")
            require(type(score) is int and score in (1, 2, 3), f"{label}: score must be 1, 2 or 3")
            require(nonempty(entry.get("note")), f"{label}: missing rationale")
            sid = entry.get("source_id")
            source = source_map.get(sid) if isinstance(sid, str) else None
            require(source is not None, f"{label}: missing source reference")
            if source:
                support = source.get("supports")
                require(isinstance(support, list) and label in support, f"{label}: source support map is missing claim")
            if release:
                require(recent(entry.get("evidence_date"), as_of, 30), f"{label}: stale or missing evidence_date")
                if source:
                    require(source.get("status") == "opened", f"{label}: source was not opened")
                    require(source.get("publisher_type") not in {"provider", "unreviewed"}, f"{label}: source requires independent verification")
                    require(recent(source.get("checked_on"), as_of, 30), f"{label}: stale or missing source check")
                    require(nonempty(source.get("summary")), f"{label}: source summary missing")
                if score == 3:
                    require(entry.get("support_tag") == TAGS[key], f"{label}: unsupported score 3")
                    require(entry.get("scope_confirmed") is True, f"{label}: local/campaign scope unconfirmed")
                if key == "trigger" and score == 3:
                    require(recent(entry.get("event_on"), as_of, 90), f"{label}: trigger event is stale or missing")
                if key == "persona" and score == 3:
                    require(recent(entry.get("activity_on"), as_of, 90), f"{label}: buyer activity is stale or missing")
        persona = scores.get("persona")
        if release and isinstance(persona, dict) and persona.get("score") in (2, 3):
            require(recent(account.get("buyer_verified_on"), as_of, 30), f"{aid}: current local buyer route not verified")

    budgets = run.get("budgets", {})
    require(isinstance(budgets, dict), "budgets must be an object")
    if not isinstance(budgets, dict):
        budgets = {}
    for unit in (*UNITS.values(), "provider_calls"):
        require(number(budgets.get(unit)), f"Missing or invalid budget {unit}")
    spent = Counter()
    cache = set()
    for index, call in enumerate(calls):
        prefix = f"Call {index + 1}"
        if not isinstance(call, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        provider = call.get("provider")
        known_provider = isinstance(provider, str) and provider in UNITS
        require(known_provider, f"{prefix}: unknown provider")
        for field in ("tool", "job", "entity", "cache_key"):
            require(nonempty(call.get(field)), f"{prefix}: missing {field}")
        cache_key = call.get("cache_key")
        if isinstance(cache_key, str):
            require(cache_key not in cache or nonempty(call.get("repeat_reason")), f"{prefix}: duplicate lookup without reason")
            cache.add(cache_key)
        require(call.get("outcome") in ("success", "empty", "error"), f"{prefix}: invalid outcome")
        require(type(call.get("metered")) is bool, f"{prefix}: metered must be explicit")
        reserved = call.get("reserved_cost")
        actual = call.get("actual_cost")
        require(number(reserved), f"{prefix}: unknown or invalid cost reservation")
        require(actual is None or number(actual), f"{prefix}: invalid actual cost")
        if call.get("metered") is False:
            require(reserved == 0 and actual in (None, 0), f"{prefix}: unmetered call has a charge")
            require(nonempty(call.get("free_basis")), f"{prefix}: missing free-price basis")
        require(known_provider and call.get("unit") == UNITS[provider], f"{prefix}: wrong cost unit")
        if known_provider and number(reserved) and (actual is None or number(actual)):
            spent[UNITS[provider]] += max(reserved, actual or 0)
    for unit, amount in spent.items():
        cap = budgets.get(unit)
        require(number(cap) and amount <= cap, f"Budget exceeded for {unit}")
    cap = budgets.get("provider_calls")
    require(number(cap) and len(calls) <= cap, "Provider call count exceeded")
    if mode == "replay":
        require(not calls, "Replay cannot contain new provider calls")

    if errors:
        return errors

    if release:
        require(mode in {"preview", "full", "refresh"}, "Historical replay cannot be a current release")
        require(nonempty(run.get("author")), "Missing run author")
        assessment = run.get("segment_assessment", {})
        require(isinstance(assessment, dict), "segment_assessment must be an object")
        if not isinstance(assessment, dict):
            assessment = {}
        require(assessment.get("status") == "accepted_for_discovery", "Segment acceptance pending")
        require(assessment.get("purchase_readiness") in ("unconfirmed", "buyer_validated"), "Missing purchase readiness assessment")
        require(nonempty(assessment.get("notes")), "Missing segment qualification notes")
        clean_accounts = [a for a in accounts if isinstance(a, dict) and a.get("scores", {}).get("clean", {}).get("score") == 3]
        named = [a for a in clean_accounts if a.get("scores", {}).get("persona", {}).get("score") in (2, 3)]
        minimum = 3 if mode == "preview" else 15
        require(len(clean_accounts) >= minimum, f"Need {minimum} clean relevant accounts")
        require(len(named) >= minimum, f"Need {minimum} named local buyer routes in clean accounts")
        for field, count, publisher in (
            ("employer_transport_source_ids", 3, {"employer"}),
            ("workflow_source_ids", 1, {"employer"}),
            ("swvl_delivery_source_ids", 1, {"vendor", "press"}),
        ):
            refs = assessment.get(field, [])
            valid_refs = isinstance(refs, list) and all(isinstance(s, str) for s in refs)
            require(valid_refs, f"{field}: must be a list of source IDs")
            refs = set(refs) if valid_refs else set()
            require(len(refs) >= count, f"{field}: insufficient independent sources")
            for sid in refs:
                source = source_map.get(sid, {})
                require(source.get("publisher_type") in publisher and source.get("status") == "opened"
                        and recent(source.get("checked_on"), as_of, 30)
                        and nonempty(source.get("summary")), f"{field}: unverified source {sid}")
        review = run.get("human_review", {})
        require(isinstance(review, dict), "human_review must be an object")
        if not isinstance(review, dict):
            review = {}
        require(review.get("status") == "approved", "Human review pending")
        reviewer = review.get("reviewer")
        require(nonempty(reviewer) and reviewer.strip().casefold() != str(run.get("author", "")).strip().casefold(), "Independent named reviewer required")
        require(recent(review.get("reviewed_on"), as_of, 30), "Human review date is stale or missing")
        require(nonempty(review.get("notes")), "Human review notes missing")
        dimensions = review.get("dimensions", {})
        valid = (isinstance(dimensions, dict) and set(dimensions) == set(DIMENSIONS)
                 and all(type(v) is int and v in (0, 1, 2) for v in dimensions.values()))
        require(valid, "Human review requires all six dimension scores")
        if valid:
            require(min(dimensions.values()) >= 1 and sum(dimensions.values()) >= 10, "Human review threshold not met")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    try:
        run = json.loads(args.run.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"INPUT ERROR: {error}")
        return 2
    errors = evaluate(run, args.release)
    if errors:
        print("EVALUATION FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("RELEASE PASS" if args.release else "STRUCTURE PASS")
    print(f"Run {run['run_id']}; as of {run['as_of']}; {len(run['accounts'])} accounts")
    print(dict(Counter(disposition(a) for a in run["accounts"])))
    if not args.release:
        print("HUMAN REVIEW " + str(run.get("human_review", {}).get("status", "pending")).upper())
        print("Source truth and purchase intent require independent evidence review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
