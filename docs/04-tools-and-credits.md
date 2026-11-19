# 4. Tool roles and evidence-backed credits

The final report must answer: **what did Codex use, why, how much did it consume, and what supports that number?** A connection list or a successful tool call is not a cost report.

## Give every tool a job

| Tool | Job | Scope/cost discipline | Evidence |
| --- | --- | --- | --- |
| Codex/local Python | Orchestrate, deduplicate, calculate, validate and write artifacts | No data-provider enrichment for local arithmetic | Session extract, script output; model usage recorded separately if available |
| Clay search | Three market searches and primary company/buyer discovery | Approved scope; reuse search IDs; bounded pages; no irrelevant enrichment | Query/search IDs, filters, actual responses, timestamps and result counts |
| Browser control | Create/import/populate/verify Clay table; inspect totals/prices/usage not exposed by tools | Normal app interaction; no undocumented endpoints; no unrelated account changes | App URL/IDs, timestamped text observations, row/column readback |
| $deepline-gtm | Apply the installed skill's documented process | Read actual SKILL.md; no extra provider lookup merely to show use | Skill name/version/path when available; applied steps or skipped reason |
| Exa | Find a missing original source or professional evidence | A few targeted queries, not another prospect sweep | Request/reference, returned URL and actual usage evidence |
| Firecrawl | Retrieve selected source URLs when ordinary reading is insufficient | Single-page retrieval first; no broad crawl/deep-research job | Requested URL, retrieval ID, extracted supported claim and charge evidence |
| treg | Resolve one named residual gap with a suitable catalog endpoint | Read actual schema/pricing; no duplicate successful lookup | Catalog/endpoint reference, reserved cap, actual call ID/charge |
| People Data Labs MCP | Optional resolution of an ambiguous professional identity | No email/phone or bulk search; preserve separate PDL approval controls | Approval plus request/result/usage evidence, or explicit skipped reason |
| GitHub | Store the guide and sanitized run, open a PR and merge | Stage only the intended files; keep personal/private/raw material outside Git | Commit/PR links and check results |

Tools unused in the run must appear as **skipped**, with a reason and no invented calls. Other providers such as Crustdata are optional identity fallbacks, not additional primary result sets.

## Approval before metered work

1. Read the actual configured action/routine/search pricing and usage model, using current provider responses, official documentation or the app's displayed estimate.
2. Quote a numeric X for the bounded Clay work. State whether it is a supported complete upper bound or only an estimate. Keep data credits, billable Actions, search quotas, dollars and other provider units separate.
3. Ask the owner to approve the specific scope and numerical cap. Save the actual statement and timestamp in approval.md and ledger.json. Do not treat balances or a template as authorization.
4. Reserve the known bounded amount before an operation. Include retries, empty returns and errors if billable. Enforce caps conservatively and stop before an overrun. If only variable/incomplete pricing is available, explain that a precise hard cap is not established; do not invent a safe ceiling. Use a specifically approved bounded probe where supported, then quote the remaining work from actual evidence.
5. Ask again only when the approved scope/cap changes or a provider requires its own approval. Do not ask permission for every call already covered.

Do not buy credits, change a plan, enable auto top-ups, or modify PDL live-access/approval settings as part of the run.

## Actual usage evidence

Save minimal sanitized source records under the run's `evidence/` folder, as Markdown or JSON, and reference them from `ledger.json`:

- Provider-reported completed run totals or per-request usage, including returned IDs and billing units.
- Applicable price/estimate evidence used for the reservation; an estimate is not a charge.
- Before/after balances or quota snapshots with timestamps and their source. A balance delta is an observed workspace change; without attribution it is not an exact per-call charge.
- A text observation of a browser-visible usage field: page URL, label, value, timestamp and how it was observed. Do not invent UI labels or claim screenshots exist.

A workflow total can still accrue while paused/running; use terminal or settled accounting before calling it final. A completed call does not prove a zero charge. Keep `actual` null when the provider does not report it; use `actual = 0` only with actual zero-charge evidence. Free-tier credits are still units consumed.

## The report

Run `python scripts/audit.py usage results/YOUR_RUN`. It prints, per billing unit:

- approved caps;
- conservative reserved/accounted consumption;
- subtotal of reported actual charges;
- number of possibly metered calls whose actual charge is unknown;
- evidence references and validation gaps.

The program does **not** convert an unknown total to zero or attribute balance deltas to particular calls. Copy its output into usage-report.md, then explain provider gaps and any observed balance differences in plain language.

Keep model usage separate from provider credits. Never claim a total dollar cost unless all relevant rates and units are actually supported. The public repo should contain sanitized evidence summaries, not secrets or raw provider dumps.

## Current capability references

- [Clay developer documentation](https://developers.clay.com/llms.txt)
- [Clay table interface](https://developers.clay.com/tables.md)
- [Clay searches](https://developers.clay.com/searches.md)
- [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp)

Always verify the live tool schema and provider plan. Tool calls, data credits, billable Actions and search-result quotas are different quantities.
