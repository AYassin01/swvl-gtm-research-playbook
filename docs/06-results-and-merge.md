# 6. Results, submission and merge

## Working branch

Each participant uses a unique `results/<timestamp>-<name>/` folder and a branch such as `results/ahmed-session6`. Codex creates the branch and prepares the artifacts. Keep course PDF, screenshots, videos, private records and raw provider dumps outside Git.

The [run-index template](../templates/run-index.md) describes the files and their purpose. The machine-readable state follows [session.json](../templates/session.json) and [ledger.json](../templates/ledger.json). These are blank templates, not observations or spending approvals.

## Final checks

From repo root:

```text
python scripts/audit.py repo
python -m unittest discover -s tests -v
python scripts/audit.py usage results/YOUR_RUN
python scripts/audit.py ready results/YOUR_RUN
```

Readiness requires the real Clay table with verified row/column evidence, actual market counts, a valid company list, a preregistered buyer experiment, an actual doubtful-result check, supported usage accounting, completed notes, session copy and playable video link. A failed numerical buyer rule does not itself fail readiness. The checker cannot authenticate source truth, observe sharing permissions, or establish instructor acceptance.

Review unknown actual costs explicitly. A run may honestly document unknown reported charges while retaining evidence-backed reservations within the approved cap; it may not invent a zero or exceed its authorization.

## Merge the result

After you provide the video URL and confirm source/access checks, Codex:

1. Updates the run README and [SUBMISSION.md](../SUBMISSION.md) with real links and counts.
2. Inspects and stages only the intended sanitized files.
3. Opens/updates a PR describing company scope, buyer result, tools used/skipped, actual/unknown costs and checks.
4. Waits for CI, then merges within the requested workflow when permitted. A protected branch or missing permission becomes a specific handoff, not a fabricated publication.

No separate research-release review is required by this class workflow. Teammates can review contributions without being impersonated. Never merge another teammate's unfinished work as yours.

## Submit one link

The repository URL is the single entry point. Its index must still link to all five required items:

1. Actual Clay workbook/table.
2. Four-line Task 1 note.
3. Accurate Codex conversation copy/link.
4. Three-line Task 2 note.
5. Actual three-minute English Loom.

The leader combines five real members' packages and adds the comparison required by the brief. Do not fabricate teammates, consensus or an overall winning hypothesis from missing data.
