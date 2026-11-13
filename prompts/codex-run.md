# Copy-ready Codex prompt

Copy the entire text below into Codex while this repository is open. Edit the configuration before running. A new chat should have access to this repository and its inputs.

```text
RUN_MODE = REPLAY
AS_OF = 2026-11-13
RUN_AUTHOR = replace-with-your-name
RUN_DIR = runs/2026-11-13-your-name-replay
TARGET_ACCOUNTS = 25
CLAY_CREDITS_MAX = 0
CRUSTDATA_CREDITS_MAX = 0
TREG_USD_MAX = 0
PROVIDER_CALLS_MAX = 0
EXPORT_TO_DRIVE = false
DRIVE_OUTPUT_FOLDER = none

Act as the GTM research partner for GTMENA Cohort 01, Team 03 Pipeline. Work through this repository to create a reproducible, evidence-backed Swvl research package. Keep outputs in text formats and Mermaid. Read AGENTS.md first and follow the repository's documented schemas and evaluations.

CONTEXT
Our segment is Greater Cairo outsourced contact centers that already arrange employee rides for on-site late shifts. The primary operator is the Facilities or Transport Manager. Finance or Procurement may approve spend. Country/site leaders can be sponsors or referrals, with their specific authority unconfirmed until verified.

Our commercial hypothesis is that Facilities and Finance would value matching billed shuttle runs with trip and boarding records while keeping the promised ride benefit operating. Public demand signals do not establish discrepancies, losses, urgency or willingness to switch at any company.

READ FIRST
- inputs/brief.md and inputs/sources.md
- docs/segment-decision.md, docs/scoring.md and docs/evidence-policy.md
- docs/tool-routing.md, docs/evaluations.md and docs/data-contract.md
- data/baseline.json and the case-study Markdown documents
- templates/run.json and templates/human-review.md

MODES
REPLAY uses saved data only and makes zero external/provider calls. Reproduce the saved scores and routing, explain the segment decision, and identify gaps. Preserve historical dates and pending review. Write a replay summary and evaluation report in RUN_DIR. Do not relabel replay as fresh research.
PREVIEW researches three accounts, starting with VXI, iQor and TTEC unless a current disqualifier changes the sample. Set target_accounts to 3 in run.json. Apply the same claim and budget standards. Label the result a sample.
FULL seeks 25 distinct real operators after validating at least 15 relevant companies and 15 named current local buyer routes within clean accounts. Use public sources to close gaps before provider calls. If the acceptance gate or count cannot be met, return a truthful incomplete draft and the remaining gaps.
REFRESH starts from the latest reviewed run and rechecks only changed, stale, missing or contradicted fields. Preserve prior evidence and record the change. Its release gate matches FULL.

PREFLIGHT
1. Create a unique RUN_DIR and record the run author, date, mode and scope. Never overwrite an existing run without an explicit update instruction.
2. In a fresh-research mode, discover tools actually exposed in this session. Map their semantic jobs to Clay, Crustdata, treg, web retrieval, and optional Drive/GitHub. Record unavailable tools and fallbacks. Do not assume a tool exists from a server name.
3. Confirm the selected paying workspace where metadata is available. Read current schemas, access and prices. Numeric caps above are the maximum authorized provider spend. Zero means no metered calls for that provider. A balance is not authorization.
4. Build preflight.md with candidate filters, evidence gaps, tool jobs, known price bounds and stopping rules. Continue useful public-source work if a paid branch is unavailable.

ASSIGN TOOLS SPECIFIC JOBS
Local files/Python: reuse existing evidence, normalize domains, deduplicate parents/buying units, calculate scores and run evaluations. Use this before external lookups.
Web search and retrieval: find and open employer job descriptions, local site pages, dated announcements, procurement signals and Swvl's own delivery/reporting material. Record source support, dates and scope. Prefer original publishers. A search snippet alone is insufficient.
Clay: company candidate discovery only. Inspect its actual search schema and run one bounded query for up to 30 Egypt BPO/contact-center candidates. Reuse the returned task/search ID. Paginate once only if needed. Do not enrich every company, pull contacts, or request funding, traffic or technology data for this task. The current DSL example in docs/tool-routing.md is a starting point, subject to the live schema.
Crustdata: fill missing current local buyer roles only after public qualification. Inspect field definitions and current plan cost. Use narrow indexed people search on the verified current employer/domain, Cairo/Giza remit, and Facilities, Transport, Operations or Procurement role. At most two profiles per account and ten shortlisted accounts in FULL. Do not call premium live refresh unless a documented conflict changes the shortlist and the reserved cost fits the cap. Do not fetch emails, phone numbers or personal details.
treg: fill a named evidence gap only. Check authorized own tools first. Use catalog_search by task, then catalog_get to read current parameters and price, then one schema-valid call. Never guess an endpoint ID. Record price reservation and returned cost. Do not duplicate a successful direct provider lookup through treg. No general enrichment sweep.
Drive: read only explicitly supplied team inputs. Export only if EXPORT_TO_DRIVE is true and a real destination is supplied. Avoid duplicate files. Local Markdown/JSON outputs remain the reproducible source for this run.
GitHub: prepare the run for team review. Create a branch/PR only if explicitly requested in this session. Do not send outreach or commit private buyer records.

CREDIT DISCIPLINE
For each actual provider call, record provider, exact tool name, semantic job, entity/URL, cache_key, whether metered, known upper-bound reservation, actual charge if returned, unit, outcome and retry reason if repeated. Reserve costs before invoking the tool. Never execute an unpriced or unbounded metered call. Count empty results and billable errors. Keep currencies/credits separate. Enforce PROVIDER_CALLS_MAX across logged provider calls, including metadata.
Reuse unexpired cache entries. One repaired query/recovery per gap is the limit. Stop before a cap is exceeded, continue through sufficient public sources and record the shortfall. Report actual executed tools and skips in handoff.md. Do not invent historical calls or exact costs.

WORK STAGES
1. Validate the segment against transport demand, a material problem, reachable local buyer routes and Swvl delivery. For FULL/REFRESH, identify at least 15 clean relevant companies, 15 named current local routes into buyers, three independent employer transport signals, a specific transport-management workflow, and Swvl delivery evidence. Record these in segment_assessment and link source IDs. Purchase readiness stays unconfirmed until buyer validation.
2. Build the market and ICP. Compare five alternatives, articulate sourced pains with their limits, define three buying-committee personas, local fit, triggers and disqualifiers. Explain why the factory and airport approaches were set aside in the earlier research. Keep current facts distinct from historical decisions.
3. Build the offer. Include dream outcome, likelihood, time delay and effort. Pair three obstacles with solutions. Describe delivery and realistic risk reduction. Any paid two-week route pilot, no-rollover term, minimum riders, start date or performance target is proposed and needs Swvl/buyer agreement. Write a short one-line offer with no invented customer proof or guarantee.
4. Build the four-rung value ladder. For free invoice check, paid one-route pilot, managed site routes and multi-site expansion, specify buyer outcome, mechanism, effort/commitment, evidence needed and the bridge to the next rung. Expansion must follow demonstrated fit.
5. Score 25 distinct accounts in FULL/REFRESH, three in PREVIEW. Use exactly size, trigger, pain, persona and clean, each 1–3 with a rationale and source ID. Follow docs/scoring.md. Unknowns stay low and explicit. Normalize parents and buying units. A clean score of 1 excludes. CRM review precedes total score. Derive all totals and dispositions with the local Python functions.

EVIDENCE AND HONESTY
Open the actual page before setting status=opened. Record checked_on separately from event_on and activity_on. Global headcount is not local capacity. A transport role is not a known billing failure. A leader's title is not proof of signer authority. A Swvl customer logo triggers CRM review rather than automatic exclusion or an assumption of unserved routes.
Keep buyer_authority and invoice_gap unconfirmed unless direct permissioned evidence establishes them. Do not invent a company's problem, deadline, metrics or customer relationship. Cite the narrow claim supported and label assumptions.

OUTPUTS
In RUN_DIR produce preflight.md, run.json, segment-decision.md, market-and-icp.md, offer-stack.md, value-ladder.md, account-scorecard.md, evaluation.md and handoff.md. Store minimal public evidence summaries and URLs. Keep secrets, private operational records and raw provider dumps outside Git. Use the JSON structure in templates/run.json and docs/data-contract.md.

STRICT EVALUATIONS
Run python scripts/evaluate.py RUN_DIR/run.json and python -m unittest discover -s evals -v. Render the scorecard from run.json using scripts/render_scorecard.py. Repair structural failures and record the outcome.
For a fresh release, run python scripts/evaluate.py RUN_DIR/run.json --release. Do not claim release if any gate fails. Every score 3 requires its support tag, current evidence and confirmed scope. Trigger 3 needs an event within 90 days. Persona 3 needs attributable activity within 90 days.
Use prompts/review.md for an adversarial review. Leave human_review pending until a different named teammate actually reviews the sources and provides their six scores and findings. Do not impersonate a reviewer or self-approve. If review is pending, complete the draft and hand it off with that explicit status.

FINISH
Give a concise result with the run path, account count, disposition counts, actual tools used, spend/reservations per unit, evaluations passed/failed, remaining assumptions and the next concrete buyer-validation step. Include the Mermaid architecture link. Preserve the difference between historical replay, a current research draft and a reviewed release.
```
