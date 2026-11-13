## Change

Describe the problem, resulting behavior or evidence update, and affected account/claim IDs.

## Evidence and uncertainty

List source URLs, access dates, score changes and remaining buyer questions.

## Tool use and cost

State actual providers called, purpose, reserved/actual amounts and cache reuse. Use zero when no provider calls ran.

## Validation

- [ ] `python scripts/check_repo.py`
- [ ] `python scripts/evaluate.py data/baseline.json`
- [ ] `python -m unittest discover -s evals -v`
- [ ] New/changed run evaluated, or no run changed
- [ ] Release gate and independent review recorded, or PR explicitly remains a draft
- [ ] No private records, credentials, images or binaries
- [ ] Contribution and changelog updated where relevant

## Reviewer

Name the teammate responsible for factual review. Keep author and reviewer distinct.
