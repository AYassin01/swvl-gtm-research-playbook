# Tool jobs and credit rules

Use the first sufficient source and retrieve only the missing field. Connecting three providers does not require calling all three for every account.

| Tool | Assigned job | When to call | Stop condition |
| --- | --- | --- | --- |
| Local files and Python | Reuse evidence, deduplicate buying units, calculate routing, render Markdown and evaluate | At the start and after each changed batch | No external provider spend |
| Public web search and page retrieval | Verify local sites, transport policies, dated events, service capabilities and source support | For factual claims, starting with original employer or vendor pages | Stop once the claim is supported or a bounded search leaves it unknown |
| Clay | Discover candidate BPO/contact-center companies with Egypt operations | The saved list cannot meet the target or needs new operators | One initial query, then at most one corrected query and one needed page |
| Crustdata | Resolve missing current local buyer roles for shortlisted companies | Public evidence lacks a named Facilities, Transport, Operations or Procurement owner | At most two profiles per account, at most ten accounts per FULL run |
| treg | Resolve a specific evidence gap, such as a missing page or dated employer signal | Public retrieval failed or an explicitly needed field has no sufficient source | At most one retrieval path per gap, plus one justified recovery |
| Google Drive | Read authorized inputs and optionally export final deliverables | A run names input links or an output folder | No speculative workspace crawl or duplicate export |
| GitHub | Version reviewed text and coordinate contributions | A branch or PR is requested for the run | Keep one reviewable change per PR |

These are team limits. A lower provider or user cap takes precedence. LLM usage and web-search usage can have their own costs. The provider ledger here covers the explicitly budgeted Clay, Crustdata and treg usage.

## Clay

The current connection may expose `search_companies`, `get_task_context`, `load_more_search_results` and `get_current_workspace` under a Clay for Reps namespace. Read the actual schema before constructing a query. Save the search/task ID and reuse it.

A candidate query, using the documented Search DSL available during repository preparation, is below. It intentionally uses local operations as a discovery filter and avoids global headcount as proof of Cairo scale.

```text
select from companies where locations.any(country_name = "Egypt") and (description contains "contact center" or description contains "call center" or description contains "BPO") limit 30
```

The prompt explicitly asks for up to 30 candidates. Review results for spelling variants and local subsidiaries. If the schema rejects the query, inspect the live fields and repair once. Keep technology stack, funding, traffic and bulk contact enrichment outside this task unless a changed brief requires them.

## Crustdata

Use the free `list_search_fields`, `autocomplete_person_filter`, `identify_company`, `get_plan_access` and `get_credit_balance` capabilities when exposed and documented as free. Start with indexed `search_people` and request only current title, employer, location and professional profile URL.

Example semantic request for the live schema is “Find up to two current Cairo Facilities or Transportation leaders at this verified company domain.” Constrain the current employer, local remit and role. If none is found, a country Operations lead can be a referral with authority unconfirmed.

Do not automatically call live enrichment, contact-information, employee-review, developer-profile or job endpoints. A live refresh requires a specific conflict that changes routing and a known cost within the cap. Public sources remain the final support for published claims.

## treg

1. Check `my_tools` for an authorized team-owned capability that can fill the gap. A provider may still bill usage behind that tool.
2. Call `catalog_search` using the task, such as “retrieve public job posting text.”
3. Call `catalog_get` on the selected endpoint. Read inputs, price and the response shape.
4. Reserve a known maximum charge in the ledger. Use `call` once with exact schema-valid inputs.
5. Record returned cost, source URL, useful field and disposition. If actual cost is absent, retain the reserved upper bound.

Do not route the same Crustdata lookup back through treg or duplicate a successful web fetch. An endpoint ID copied from another run must be rediscovered before reuse.

## Budget and cache contract

- Default caps are zero. The run owner may set positive numeric caps in the prompt.
- Maintain separate units for `clay_credits`, `crustdata_credits` and `treg_usd`. Add a `provider_calls` cap as a second limit.
- Before each metered call, know a conservative upper bound. Charge that reservation against the cap until the reported actual cost is known.
- Log success, empty result, error and retry. Billable failures count. Never report a guessed actual charge.
- Build a cache key from provider, semantic job, normalized entity/URL, field set and freshness window. Reuse an unexpired result across teammates.
- A repeated cache key needs a written reason, such as conflicting current employment or an expired source. Use at most one repair per gap.
- Cache identity and static site facts for 30 days. Refresh buyer roles within 30 days of release and trigger status at release. Retain the original event date separately from the access date.
- Budget exhaustion stops the paid branch. Finish useful work from public sources and record the remaining gap.

New runs must list the tools that actually executed. The historical tool-use summary in the case study is attributed to the earlier workflow, with exact call history unavailable.
