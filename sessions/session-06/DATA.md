# Session 6 run files

Copy [templates/session.json](templates/session.json) into a fresh run as `session.json`. It contains empty state, not research results. Read [the checker](check_submission.py) for exact structural checks. All source claims still require actual inspection.

## Minimal tables

`som-companies.csv` has exactly these headers:

```text
company_name,website,company_page_url
```

`buyer-results.csv` has exactly these headers, with one row per actual returned person:

```text
name,job_title,company,profile_link
```

Both are UTF-8 text; do not add evidence/enrichment columns to the submission tables.

## Audit objects in session.json

Each `company_audit` object records `website`, `fits_icp` (boolean), `service_source` (URL), and `site_source` (URL). Add `checked_at`, exact supported claims, scope, and `transport_status` (`current`, `historical_campaign`, or `unknown`) as needed. A source can support more than one claim only when its content actually does so. `company-audit.json` may mirror this list for readability; keep it consistent.

Each `people` object retains the four CSV fields plus `company_domain` and `classification` (`relevant`, `not_relevant`, or `unconfirmed`). For `relevant`, set `current_employer_supported`, `local_remit_supported`, and `transport_role_supported` only when the evidence establishes each, and supply an `evidence` array of URLs. Add narrow claim summaries and check dates. No emails or phones.

`markets` records actual Clay counts, three distinct search references, filters, timezone-aware observation timestamps, and `kind` (`exact` or `estimated`). SOM may instead be `capacity_selection` when it is an intentionally limited, verified selection for the 30-day workload; this is not the total count of all potential matching companies. TAM/SAM page lower bounds remain incomplete totals.

`rule.adopted_at`, `buyer_search.sample_frozen_at`, `request_saved_at`, and `started_at` preserve chronology. Never backdate them or claim the owner adopted a proposal. Keep the exact owner request in the named file.

The decision is `keep`, `change_titles`, or `change_filters`; it must follow the original threshold. At least one actual returned person must have a recorded doubtful-answer check. A zero-result run may be useful research, but cannot fabricate that required check.

`links` contains actual workbook/video URLs and paths to the two notes and session copy, relative to the run folder, or a real HTTPS session link. Do not use Windows paths as reviewer links. `access_checked` records the owner's real access review, not the program's assumption.

The readiness checker can reject malformed packaging and inconsistent declared evidence. It cannot verify that a web page supports the claim, whether the owner really checked access, or whether the instructor accepts the Codex substitution.
