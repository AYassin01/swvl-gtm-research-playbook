"""Offline Session 6 packaging checks; cannot establish source truth or grading acceptance."""

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


COMPANY_COLUMNS = ["company_name", "website", "company_page_url"]
BUYER_COLUMNS = ["name", "job_title", "company", "profile_link"]


def domain(value):
    parsed = urlparse(value if "://" in str(value) else "https://" + str(value))
    return (parsed.hostname or "").lower().removeprefix("www.")


def web(value):
    parsed = urlparse(str(value))
    return parsed.scheme in {"http", "https"} and bool(parsed.hostname) and not parsed.username and not parsed.password


def timestamp(value):
    try:
        result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return result if result.tzinfo is not None else None
    except ValueError:
        return None


def validate_run(directory):
    root = Path(directory).resolve()
    data = json.loads((root / "session.json").read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        return ["session.json must be an object"], {}
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def local_file(relative):
        if not relative or web(relative):
            return None
        path = (root / relative).resolve()
        return path if path.is_relative_to(root) and path.is_file() else None

    def csv_rows(name, columns):
        path = root / name
        if not path.is_file():
            errors.append(f"Missing {name}")
            return []
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            require(reader.fieldnames == columns, f"{name} must have exactly {columns}")
            rows = list(reader)
        require(all(None not in row and all(row.get(key) is not None for key in columns) for row in rows),
                f"{name} contains malformed rows")
        return rows

    require(data.get("schema_version") == "session6-v1", "Wrong Session 6 schema")
    require(bool(data.get("owner")), "Missing owner")
    require(data.get("config_confirmed") is True, "Owner must confirm the new scope/config")
    require(data.get("team_hypothesis_confirmed") is True, "Team hypothesis coordination pending")
    project = data.get("project", {})
    require(all(project.get(k) for k in ("industry", "geography", "company_size", "titles", "offer")),
            "Five project parts are required")
    require(isinstance(project.get("titles"), list) and bool(project.get("titles")), "Title family must be a nonempty list")
    require(bool(data.get("icp")), "Missing falsifiable ICP")

    markets = data.get("markets", {})
    values, references = [], []
    for key in ("tam", "sam", "som"):
        item = markets.get(key, {})
        val = item.get("value")
        require(type(val) is int and val >= 0, f"{key}: observed nonnegative integer count required")
        kinds = {"exact", "estimated"} | ({"capacity_selection"} if key == "som" else set())
        require(item.get("kind") in kinds, f"{key}: unresolved page/lower-bound counts are not final totals")
        require(item.get("provider") == "Clay", f"{key}: count must come from Clay")
        require(bool(item.get("reference")) and bool(item.get("filters")) and timestamp(item.get("observed_at")),
                f"{key}: retain search reference, filters, and timezone-aware observation time")
        values.append(val)
        references.append(item.get("reference"))
    require(len(set(references)) == 3 and all(references), "Retain three distinct Clay search references")
    if all(type(x) is int for x in values):
        require(values[0] >= values[1] >= values[2], "Counts must satisfy TAM >= SAM >= SOM")
    require(data.get("nesting_reviewed") is True, "Logical filter/membership nesting must be reviewed")

    companies = csv_rows("som-companies.csv", COMPANY_COLUMNS)
    require(len(companies) >= 25, "At least 25 matching SOM companies required")
    domains = [domain(row.get("website", "")) for row in companies]
    require(len(domains) == len(set(domains)) and all(domains), "SOM domains must be present and unique")
    for row in companies:
        require(bool(row.get("company_name")) and web(row.get("website")) and web(row.get("company_page_url")),
                "Every company needs its name, real website URL, and company-page URL")
    if type(values[2]) is int:
        require(values[2] == len(companies), "SOM count must match the selected company rows")
    audits = {domain(x.get("website", "")): x for x in data.get("company_audit", [])}
    for host in domains:
        entry = audits.get(host, {})
        require(entry.get("fits_icp") is True and web(entry.get("service_source")) and web(entry.get("site_source")),
                f"Company-fit evidence missing for {host}")

    sample = [domain(x) for x in data.get("sample_domains", [])]
    require(len(sample) == 5 and len(set(sample)) == 5 and set(sample).issubset(domains),
            "Freeze five distinct sample companies from the SOM")
    require(bool(data.get("sampling_method")), "Document the neutral sampling method")
    rule, search = data.get("rule", {}), data.get("buyer_search", {})
    threshold = rule.get("min_verified_buyers")
    require(type(threshold) is int and 1 <= threshold <= 10 and bool(rule.get("definition")),
            "Adopt a defined numerical rule between 1 and 10")
    adopted, started = timestamp(rule.get("adopted_at")), timestamp(search.get("started_at"))
    require(adopted is not None and started is not None and adopted <= started,
            "Adopt the rule before buyer retrieval; include timezone-aware timestamps")
    frozen, requested = timestamp(search.get("sample_frozen_at")), timestamp(search.get("request_saved_at"))
    require(frozen is not None and requested is not None and started is not None and frozen <= requested <= started,
            "Freeze the sample and save the personal request before buyer retrieval")
    require(bool(search.get("reference")), "Missing actual buyer-search reference")
    require(local_file(search.get("exact_request_file")), "Missing the owner's exact saved buyer request")

    buyers = csv_rows("buyer-results.csv", BUYER_COLUMNS)
    people = data.get("people", [])
    require(all(isinstance(p, dict) for p in people), "People must be objects")
    profiles = [p.get("profile_link") for p in people]
    require(len(profiles) == len(set(profiles)), "Returned people must be deduplicated by profile")
    require(len(people) <= 10, "Primary experiment exceeds ten returned people; document the tool over-return")
    company_counts = Counter(domain(p.get("company_domain", "")) for p in people)
    require(set(company_counts).issubset(sample) and all(n <= 2 for n in company_counts.values()),
            "Primary people must belong to the frozen five with at most two per company")
    csv_set = [tuple(p.get(key, "") for key in BUYER_COLUMNS) for p in buyers]
    json_set = [tuple(p.get(key, "") for key in BUYER_COLUMNS) for p in people]
    require(Counter(csv_set) == Counter(json_set), "Buyer CSV must match the original people records")
    verified, unconfirmed = 0, 0
    for person in people:
        require(all(person.get(k) for k in BUYER_COLUMNS) and web(person.get("profile_link")),
                "Returned people need the four professional fields and a real profile URL")
        classification = person.get("classification")
        require(classification in {"relevant", "not_relevant", "unconfirmed"}, "Invalid buyer classification")
        if classification == "relevant":
            verified += 1
            require(all(person.get(k) is True for k in ("current_employer_supported", "local_remit_supported", "transport_role_supported"))
                    and bool(person.get("evidence")) and all(web(x) for x in person.get("evidence", [])),
                    "Verified buyer requires current-employer, local-remit, and transport-role evidence")
        unconfirmed += classification == "unconfirmed"
    expected = {"keep"} if type(threshold) is int and verified >= threshold else {"change_titles", "change_filters"}
    require(data.get("decision") in expected, "Decision must follow the original rule; failed yield is a valid experiment")

    doubtful = data.get("doubtful_check", {})
    require(bool(doubtful.get("profile_link")) and doubtful.get("profile_link") in profiles
            and bool(doubtful.get("finding")) and bool(doubtful.get("sources"))
            and all(web(x) for x in doubtful.get("sources", [])), "Document one actual doubtful returned person and its check")
    require(doubtful.get("owner_checked") is True, "Owner's doubtful-answer review is pending")
    links = data.get("links", {})
    for key in ("workbook", "video"):
        require(web(links.get(key)), f"Actual {key} URL required")
    for key, count in (("task1_note", 4), ("task2_note", 3)):
        path = local_file(links.get(key))
        lines = path.read_text(encoding="utf-8").splitlines() if path else []
        lines = [line for line in lines if line.strip()]
        require(len(lines) == count and not any(word in "\n".join(lines) for word in ("PENDING", "TODO", "TBD", "REPLACE_ME")),
                f"{key} needs exactly {count} completed nonempty lines")
    require(web(links.get("session_copy")) or local_file(links.get("session_copy")), "Real session link or local copy required")
    require(data.get("access_checked") is True, "Owner must check the leader's link access")
    for name in ("project-and-icp.md", "market-searches.md", "buyer-checks.md", "evidence.md", "credits.md", "evaluation.md", "video-script.md"):
        path = local_file(name)
        require(path is not None and bool(path.read_text(encoding="utf-8").strip()), f"Missing supporting artifact: {name}")
    summary = {"som_rows": len(companies), "companies_returning_people": len(company_counts), "people_found": len(people),
               "verified_relevant": verified, "unconfirmed": unconfirmed, "verified_requested_yield": verified / 10,
               "verified_return_rate": verified / len(people) if people else None,
               "true_precision": None if unconfirmed else (verified / len(people) if people else None)}
    return errors, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--ready", action="store_true", help="Exit 1 when required data or artifacts are incomplete")
    args = parser.parse_args()
    try:
        errors, summary = validate_run(args.run_dir)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(json.dumps({"ready": False, "load_error": str(error)}))
        return 2
    print(json.dumps({"ready": not errors, "summary": summary, "gaps": errors,
                      "limit": "Offline packaging checks do not establish source truth or instructor acceptance"}, indent=2))
    return int(bool(errors)) if args.ready else 0


if __name__ == "__main__":
    raise SystemExit(main())
