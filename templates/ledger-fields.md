# Usage ledger fields

The [empty ledger](ledger.json) contains no live observations. Put a real ledger inside each run. Evidence references are accessible HTTP(S) sources or existing paths relative to that run. Local evidence should be minimal sanitized fields/observations, not a raw credential-bearing response.

## approvals[]

Fields: `id`, `provider`, `unit`, `cap` (finite nonnegative number), `approved_at` (timezone-aware ISO timestamp), `owner_statement`, and `pricing_evidence` (nonempty evidence references). Use one current approval per provider/unit bucket. Preserve any explicit cap amendment and statement in approval.md; do not add duplicated approvals to inflate the budget.

## events[]

Fields: `id`, `at`, `provider`, `tool`, `job`, `request_ref`, `outcome`, `unit`, `metered` (true, false, or "unknown"), `approval_id`, `reserved`, `pricing_evidence`, `actual`, `actual_evidence`.

For a possibly metered call, `approval_id` resolves to that provider/unit, `reserved` is a known finite bound with evidence, and the operation occurs after approval. `actual` is a reported nonnegative charge, or null if not reported. A reported zero also needs actual evidence. For a documented non-metered call, approval/reservation may be null, but pricing_evidence must establish the non-metered basis. Keep quotas in their own unit rather than silently bundling them with data credits.

Actual spend can exceed a reservation; that remains a recorded overrun, not a reason to edit away the charge. Checks compare the larger of each reservation and known actual to the approved cap. No provider call is omitted just because it failed or returned no people.

## balances[]

Fields: `provider`, `unit`, `at`, `value`, `evidence` (nonempty references), `concurrent_activity` (description or "unknown"). These are observed snapshots, not per-call charge assertions. The report lists them separately and does not attribute their difference automatically.

## Evidence examples by type

- A sanitized provider usage record: original request/run ID, terminal status, actual accounting field, unit, value, observation time.
- A configured price observation: exact operation/routine ID, active configuration, displayed quote/estimate, unit, scope and timestamp.
- A browser text observation: actual page URL, visible field label/value and observation time.

Every recorded value must come from a real observation. A script can validate structure and arithmetic but cannot establish whether the evidence was actually observed.
