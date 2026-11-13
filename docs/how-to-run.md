# How to run

## Replay the saved case

Clone or download this repository and open a terminal in its root. Python 3.10+ is the only dependency for local checks.

```bash
git clone https://github.com/AYassin01/swvl-gtm-research-playbook.git
cd swvl-gtm-research-playbook
python scripts/evaluate.py data/baseline.json
python scripts/render_scorecard.py data/baseline.json
python -m unittest discover -s evals -v
```

The first command checks the saved rows, references, scoring rules and budget ledger. It prints `STRUCTURE PASS` and `HUMAN REVIEW PENDING`. It returns exit code 0 for a structurally valid replay. The release command below deliberately fails for the baseline because its sources were imported and human review is pending.

```bash
python scripts/evaluate.py data/baseline.json --release
```

REPLAY reconstructs the saved reasoning with zero paid lookups. Fresh research will produce different dates, candidates and scores as the market changes.

## Run fresh research with Codex

1. Follow [MCP setup](mcp-setup.md). Each teammate connects their own authorized accounts.
2. Open this repository in Codex, or start `codex` from its root. Confirm the repository's AGENTS.md is in scope.
3. Copy all of [prompts/codex-run.md](../prompts/codex-run.md) into the session. Set `RUN_MODE`, a unique `RUN_DIR`, `AS_OF`, owner and numeric budgets at the top.
4. Start with PREVIEW for three accounts. Keep paid budgets at zero for a public-source run. Supply positive caps only when you intend to use provider credits.
5. Codex reads the inputs, maps live tool names, writes a preflight plan, retrieves evidence, scores accounts, and evaluates the results.
6. FULL seeks 25 distinct operators after an initial segment check of at least 15. A shortfall becomes an explicit gap and blocks release. REFRESH touches only stale or changed evidence.
7. Use [prompts/review.md](../prompts/review.md) in a separate session or have a teammate inspect the sources. The reviewer records their own name, date and findings.
8. Create a PR with the run folder, the evaluation report, updated contributions and a description of what changed.

In hosted ChatGPT, attach or provide access to the repository text and select the required connected apps. Local `config.toml` does not configure hosted tools. If a provider is missing, continue through public sources and mark that job skipped or incomplete.

## Expected run outputs

| File inside RUN_DIR | Content |
| --- | --- |
| `preflight.md` | Surface, tools actually exposed, jobs, filters, caps and unresolved inputs |
| `run.json` | Accounts, source registry, tool ledger, budgets and review state |
| `segment-decision.md` | Acceptance evidence and remaining purchase questions |
| `market-and-icp.md` | Five alternatives, sourced pains, three personas, triggers and exclusions |
| `offer-stack.md` | Four value levers, three obstacles and solutions, delivery, proposed terms and one-line offer |
| `value-ladder.md` | Free, entry, core and premium with outcome, mechanism, commitment, evidence and bridge |
| `account-scorecard.md` | Rendered scores, dispositions and source-linked reasoning |
| `evaluation.md` | Deterministic results plus human review and unresolved failures |
| `handoff.md` | Actual tool usage, budget reservations/charges, shortlist and next questions |

The tools guide an agent workflow. They do not schedule work or execute provider calls by themselves. Drive export is optional and requires an explicit destination in the run prompt.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| MCP server listed but no tools | Reconnect in that client and inspect actual exposed capabilities |
| Provider filter rejected | Read its schema once, repair the query, and log the retry |
| Price unavailable | Skip the paid call and use public research within the run scope |
| Missing named local buyer | Score persona 1 and record the gap. A global CEO does not establish local transport authority |
| Source shows only an allowance | Check the specific campaign. Route-level disqualification takes precedence |
| Same parent appears twice | Merge into one buying unit unless independent local procurement is evidenced |
| New release fails | Repair the failed evidence or schema fields and rerun. Keep failures in evaluation.md |
