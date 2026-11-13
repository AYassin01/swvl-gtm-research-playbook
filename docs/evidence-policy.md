# Evidence policy

Every factual criterion must be traceable to an opened source, its access date, the relevant site or campaign and a narrow interpretation. Provider discovery results are leads for verification.

## Claim types

| Type | Example | Publication rule |
| --- | --- | --- |
| Public fact | An employer role assigns transport vendor management | Cite the employer page and access date |
| Inference | A new account may change rider demand | Label it and give the discovery question |
| Proposal | A paid two-week pilot with no automatic rollover | Label it and identify required Swvl/buyer agreement |
| Unknown | Current invoice discrepancy, spend or signer | Keep it unknown until direct evidence arrives |

## Sources

Prefer original employer job descriptions, official sites, company disclosures, procurement notices and attributable professional announcements. Regulators and development institutions can provide market context. A vendor page establishes the vendor's own statement. Recruiter reposts and data-provider results are weaker signals until corroborated.

For each source record, store `id`, `url`, `status`, `observed_on`, `checked_on`, `publisher_type`, `supports` and a short `summary`. Allowed publication types are `employer`, `vendor`, `regulator`, `institution`, `professional_profile`, `press`, `provider`, `unreviewed`. A fresh release requires `status = opened`, a supported publication type, and an access check within 30 days of the run date.

`supports` lists claim keys such as `SW03.pain`. Narratives can additionally use named claim keys such as `segment.swvl_delivery`. Save summaries and necessary short excerpts, respecting source permissions. Do not commit entire articles or private raw provider responses.

Read the actual source page. A search snippet, homepage or generic directory cannot support a precise claim about a night route, local headcount or named buyer authority. If a source is blocked or gone, record the failure and lower confidence until a sufficient replacement is opened.

## Dates and scope

- `observed_on` records when a source entered the team's research.
- `checked_on` records when the page was last reopened.
- A score's `evidence_date` records its last substantive support review.
- `event_on` is the actual event date, used for trigger recency.
- `activity_on` dates the buyer activity used for persona 3.
- Keep future plans separate from completed events. Avoid substituting a crawl date or job-search ranking for a publication date.
- Confirm a Cairo/Giza operating site and the exact transport policy for the campaign. A global policy does not establish local delivery.

## Commercial boundary

Public evidence can justify discovery and a hypothesis. Purchase readiness requires the buyer's own problem magnitude, approval path, decision timing and willingness to change. Before proposing a route, confirm eligibility, pickup/drop-off obligations, fallback owner, safe operational scope and economics with Swvl and the buyer.

Treat public Swvl logos and parent-company relationships as a CRM review flag. They do not establish current route coverage, exclusivity or permission to approach an existing customer.

Private invoices and rider records belong in authorized private storage. Publish anonymized field definitions, aggregate findings and permissioned summaries. Remove names, phone numbers and precise home/pickup addresses from repo examples.
