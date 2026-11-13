# Strict evaluations

Use deterministic checks and a separate human evidence review. Both are required for a fresh research release. The evaluator runs offline and cannot verify that a page supports a claim.

## Commands

```bash
python scripts/evaluate.py data/baseline.json
python -m unittest discover -s evals -v
python scripts/evaluate.py runs/YOUR_RUN/run.json --release
```

Exit 0 means the selected gate passes. Exit 1 means an evaluation failed. Invalid JSON or unreadable files return exit 2. `--release` adds current-evidence, acceptance and human-review requirements. The baseline intentionally fails that gate.

## Structural checks

- Schema version, mode, run date, account count and required records must be valid.
- Account IDs, domains and buying units must be unique. Separately procured units require distinct buying-unit keys, a shared parent field and explicit justification.
- Every account must have exactly five integer scores from 1 to 3, a nonempty rationale and a resolving HTTPS source.
- Source IDs and URLs must be unique. Credential-bearing URLs are rejected.
- Exclusion and CRM routing take precedence over totals. All dispositions are derived from scores.
- Cost reservations and actual costs must be finite nonnegative numbers in the correct provider unit. Cap checks use the larger of the reservation and known actual charge.
- Paid or possibly paid calls require a known reservation. Empty/error responses still count against budgets.
- Repeated cache keys require a written reason. The count cap includes metadata calls recorded in the ledger.

## Fresh-release checks

- Exactly the requested account count. FULL requests at least 25 and PREVIEW requests three. A PREVIEW can pass as a sample but cannot be labeled a complete team submission.
- All used sources were opened and checked within 30 days. Criterion-level reviews are also fresh.
- Every score 3 has its specific support tag and confirmed local/campaign scope.
- Trigger 3 requires an event within 90 days. Persona 3 requires dated activity within 90 days.
- At least 15 clean FULL accounts have named current buyer routes, and at least 15 pass the public screen. At least three distinct employer sources support transport demand. One source supports Swvl delivery and another supports the operational workflow.
- The run contains a segment assessment whose evidence links resolve and whose discovery acceptance is explicitly recorded. It also records that purchase readiness remains unconfirmed or records permissioned buyer validation.
- Human review is approved by a named reviewer other than the run author, dated within 30 days, with all six dimensions scored and notes. Minimum 10/12, with no zero.

## Human dimensions

Score each 0 for unsupported/incorrect, 1 for partial, or 2 for sufficient within the stated scope.

| Key | Review question |
| --- | --- |
| `source_support` | Does each cited page support the actual claim, including scope and date? |
| `segment_purchase_logic` | Are transport demand, buyer route and materiality questions explained honestly? |
| `buyer_mapping` | Are current employment, local remit, reachability and signer uncertainty clear? |
| `offer_deliverability` | Can the proposed mechanism be scoped credibly, with agreement needed on terms? |
| `score_calibration` | Do independent scores follow the rubric and routing precedence? |
| `tool_cost_discipline` | Did every external call have a job, bounded cost and nonduplicated purpose? |

For FULL, review all 25 accounts' fit, pain, persona and disqualifier evidence. Review each dated trigger and every score 3. Check all exclusions and CRM holds. Open sources directly. A second Codex session can challenge the work, while a teammate owns the final named review.

## Adversarial cases

The tests exercise high-scoring exclusions, CRM precedence, duplicate entities, dangling sources, invalid scores, unbounded costs, repeated lookup keys, stale trigger dates, unsupported high scores and missing human approval. Add a regression when a new failure is found.

Machine checks can be satisfied by false metadata. The reviewer must reject unsupported `opened`, `scope_confirmed`, cost and support-tag assertions. A green structural result must never be described as verified purchase intent.

The original course rubric supplied scoring dimensions and labels. These release thresholds, freshness windows and budget checks are additional team rules introduced for this repository.
