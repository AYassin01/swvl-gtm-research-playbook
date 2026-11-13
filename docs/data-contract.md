# Data contract

`data/baseline.json` is the complete historical input. `templates/run.json` is a fresh-run starting structure. The evaluator supports schema version 1 and Python 3.10+.

## Run fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer 1 |
| `run_id`, `author`, `as_of` | Unique run identity, real contributor and ISO date |
| `mode` | `replay`, `preview`, `full` or `refresh` |
| `target_accounts` | Positive integer, three for preview and at least 25 for full/refresh |
| `provenance` | Actual origin, import limitations and evidence reuse |
| `budgets` | Nonnegative caps for clay_credits, crustdata_credits, treg_usd and provider_calls |
| `tool_calls` | Actual Clay/Crustdata/treg calls, including metadata, errors and retries |
| `sources` | Deduplicated public source registry |
| `accounts` | Distinct local buying-unit records with five scored criteria |
| `segment_assessment` | Evidence references, discovery acceptance and purchase readiness |
| `human_review` | Actual independent reviewer and six dimension scores |

Dates use `YYYY-MM-DD`. Spend values must be finite numbers. `null` is permitted for an actual charge that was not returned, while a known reserved upper bound is still required. Zero budgets prohibit metered calls. `provider_calls` also bounds logged metadata calls. Public web/Drive/GitHub use is described separately in handoff.md.

## Account example

```json
{
  "id": "SW03",
  "account": "Company name",
  "domain": "example.com",
  "buying_unit": "example.com-egypt",
  "scope": "The specific Cairo site and campaign",
  "named_route_in": "Verified professional name and relevant local role",
  "buyer_authority": "unconfirmed",
  "buyer_verified_on": "2026-11-13",
  "invoice_gap": "unconfirmed",
  "motion": "New logo",
  "next_check": "Ask who approves the transport vendor.",
  "scores": {
    "pain": {
      "score": 3,
      "note": "The employer assigns transport record and vendor review responsibilities.",
      "source_id": "S001",
      "support_tag": "specific_transport_workflow",
      "scope_confirmed": true,
      "evidence_date": "2026-11-13"
    }
  }
}
```

The abbreviated example shows one criterion. A valid account requires exactly `size`, `trigger`, `pain`, `persona` and `clean`. See docs/scoring.md for high-score tags and event/activity dates. `named_route_in` may describe the missing role when persona is 1. Confirmed authority or an invoice gap requires a nonempty `buyer_authority_validation` or `invoice_gap_validation` summary based on permissioned evidence.

Normalize parent companies. Shared domains can represent independent buying units only with `parent` and `independent_buying_justification` populated on each duplicate-domain record. The reviewer must inspect the procurement evidence.

## Source example

```json
{
  "id": "S001",
  "url": "https://example.com/careers/transport-manager",
  "status": "opened",
  "observed_on": "2026-11-13",
  "checked_on": "2026-11-13",
  "publisher_type": "employer",
  "summary": "The employer describes local transport record and vendor responsibilities.",
  "supports": ["SW03.pain", "segment.transport_workflow"]
}
```

## Provider-call example

```json
{
  "provider": "treg",
  "tool": "actual_exposed_tool_name",
  "job": "Retrieve an employer source unavailable through public retrieval",
  "entity": "https://example.com/careers/transport-manager",
  "cache_key": "treg|employer-source|example.com/careers/transport-manager|2026-11",
  "metered": true,
  "reserved_cost": 0.02,
  "actual_cost": null,
  "unit": "treg_usd",
  "outcome": "success"
}
```

The example cost is fictional and illustrates the format. Use the live endpoint's actual quote. Add `repeat_reason` when repeating a cache key. A documented free metadata call uses `metered=false`, zero costs and `free_basis` naming the current provider documentation/tool price statement.

For safety in cap accounting, the evaluator reserves the larger of the quoted maximum and known actual charge. It is a conservative spend bound and may exceed the final settled bill. Report actual and reserved totals separately.
