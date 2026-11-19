# Session data fields

The [session template](session.json) contains no live results. Copy it into a real run, then fill only observed/adopted values.

- `project`: five parts and the adopted ICP. `scope_confirmed` and `team_hypothesis_confirmed` reflect real owner decisions.
- `markets`: three actual Clay counts, search references, filters and timezone-aware observation times. Kinds are `exact` or `estimated`; SOM may be `capacity_selection` for the deliberately selected 30-day workload. Page lower bounds remain incomplete totals.
- `company_audit`: entries with website, fits_icp boolean, nonempty `sources` array of actual service/site evidence, and supported claims. Label transport status separately as current, historical_campaign or unknown.
- `table`: actual URL, creation_path (`tool` or `browser`), row count, the exact three company columns, checked_at timestamp and evidence references for actual readback. A CSV path cannot stand in for the table.
- `sample_domains`, `sampling_method`, `rule`, `buyer_search`: the fixed sample, owner-adopted threshold/definition and actual chronology. Preserve the exact personal request file and actual search reference.
- `people`: the four buyer CSV fields plus company_domain and classification (`relevant`, `not_relevant`, `unconfirmed`). Relevant entries require true current_employer_supported, local_remit_supported and transport_role_supported, plus an evidence array. Do not set flags without support.
- `decision`: keep, change_titles or change_filters, following the original rule. A failed yield can be complete.
- `doubtful_check`: an actual returned profile, sources, finding and owner's real inspection state. Inaccessible evidence stays unconfirmed.
- `links`: portable run-relative note/session-copy paths or a real session URL, and the actual external video URL. `access_checked` reflects the owner's real access review.
- `declared_complete`: set true only when readiness passes and the actual deliverables exist. CI checks every run that declares completeness.

Evidence references are actual HTTP(S) URLs or existing sanitized files relative to the run. Never use private local Windows paths as reviewer links. See [ledger fields](ledger-fields.md) for usage accounting.
