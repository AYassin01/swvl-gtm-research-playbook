# Account scoring

The five dimensions below come from the supplied GTMENA rubric. Each receives 1, 2 or 3, with equal weight. The detailed thresholds are Team 03's operational interpretation.

| Dimension | 1 | 2 | 3 |
| --- | --- | --- | --- |
| Fit to ICP size | Outside | Edge | Core |
| Trigger present | None | Weak | Recent and clear |
| Pain evidence | None | Indirect | Public and specific |
| Reachable persona | Unknown | Found | Found and active |
| No disqualifier | Hits one | Unclear | Clean |

## Team thresholds

| Key | 3 | 2 | 1 |
| --- | --- | --- | --- |
| `size` | At least 250 local staff or production seats, or two verified Greater Cairo delivery sites | 50–249 locally, or local delivery with unconfirmed scale | Under 50 without a second site, or outside scope |
| `trigger` | A local launch, client ramp, added shift, renewal or tender within 90 days | Relevant event 91–365 days old, or a weaker transport/procurement vacancy | None found. Routine agent recruitment alone stays here |
| `pain` | A specific transport audit, records, performance-exception workflow or stated failure | Indirect demand such as funded late-shift rides | None found, or allowance only for the screened campaign |
| `persona` | Named relevant current local buyer or sponsor and attributable public activity within 90 days | Named relevant owner/referral, with activity or precise remit unconfirmed | Unknown, outdated or conflicting identity |
| `clean` | On-site outsourced CX and company-arranged late rides evidenced, with no public hold | Ride terms, local scope or incumbent status unclear | Evidenced hard stop for the screened campaign |

Global employee count cannot establish local size. Found and active does not establish budget authority. Pain 3 can establish management work without establishing a billing discrepancy.

## Routing precedence

1. `clean = 1` becomes **Exclude**.
2. `motion = CRM review` becomes **CRM review**, regardless of the total.
3. **Priority discovery** requires total at least 12, size and persona at least 2, clean 3, and trigger 3 or pain 3.
4. **Discovery queue** requires clean 3, pain at least 2 and persona at least 2.
5. Remaining accounts become **Verify first**.

A high score does not override an exclusion or account-owner check. Priority discovery is a route into qualification. Confirm campaign policy, recurring riders, transport owner, contract timing and Swvl ownership before outreach or pricing.

## Evidence fields for a fresh run

Each score needs `score`, `note` and `source_id`. For release, include `support_tag`, `evidence_date` and `scope_confirmed`. For trigger 3, add `event_on`. For persona 3, add `activity_on`.

| Key scored 3 | Required support tag |
| --- | --- |
| size | `local_size_core` |
| trigger | `recent_trigger` |
| pain | `specific_transport_workflow` |
| persona | `named_active_buyer` |
| clean | `company_arranged_late_rides` |

The human reviewer verifies that the source actually supports the tag and the stated site/campaign. Programmatic checks validate recorded fields and dates. Preserve disagreements in the PR instead of averaging unsupported claims into a score.
