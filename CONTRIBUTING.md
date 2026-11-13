# Contributing

Use this repo as Team 03's shared working record. New contributors can start by verifying one account, challenging one score, improving a prompt or adding an evaluation for a real failure.

## Make one bounded change

1. Open an evidence, workflow or evaluation issue using the templates. Describe the claim or behavior you want to improve.
2. Create a branch such as `evidence/vxi-buyer-refresh`, `workflow/budget-ledger` or `evals/stale-trigger`.
3. Read AGENTS.md and the relevant policy. Reuse the latest evidence and state your provider budget before paid research.
4. Preserve data/baseline.json as the historical replay. Put fresh work in a unique `runs/<date>-<author>-<scope>/` folder.
5. Include sources, review dates, score changes and the next qualification question. Keep private records outside Git.
6. Run the offline checks and fill in the PR template.
7. Ask a different teammate to review the factual claims and contribution. Resolve their findings before calling the run reviewed.

```bash
git switch -c evidence/your-scope
python scripts/check_repo.py
python scripts/evaluate.py data/baseline.json
python -m unittest discover -s evals -v
git add docs prompts case-study data scripts evals templates CONTRIBUTORS.md CHANGELOG.md
git commit -m "Explain the concrete evidence or workflow change"
git push -u origin evidence/your-scope
```

Stage only the paths you actually changed. For a new research run, include its sanitized run folder explicitly. Use the latest reviewed run as the starting point when available. PRs can remain draft while evidence or human review is pending.

## Useful contribution lanes

| Lane | Example | Review focus |
| --- | --- | --- |
| Evidence | Verify a transport policy or local buyer role | Exact source, scope and date |
| Account qualification | Resolve a CRM hold or campaign exclusion | Correct routing and no unsupported authority |
| Offer development | Refine a pilot metric or value-ladder bridge | Buyer value, feasibility and agreed terms |
| Workflow | Improve provider routing or cache reuse | Specific job, cost and reproducibility |
| Evaluations | Add a failure case and repair a check | Test fails before the repair and passes after |
| Documentation | Make setup or onboarding clearer | Steps work for a teammate starting fresh |

## Ownership and attribution

Add your actual name/handle and contribution to CONTRIBUTORS.md. Keep the initiating workflow credited to Ahmed Yassin and the project credited to GTMENA Team 03 Pipeline. Each teammate may use their contribution in a portfolio with attribution and an accurate description of its status.

By contributing original material, you agree to its inclusion under the repository's MIT license. Keep third-party material to sourced summaries and permitted excerpts. GTMENA templates and provider data retain their own rights.

The first substantive PR can nominate maintainers and reviewers. Until the team agrees, record review responsibility per PR rather than assigning unconfirmed owners.
