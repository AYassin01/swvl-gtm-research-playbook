# Independent review prompt

```text
Review this Team 03 Swvl run as a skeptical teammate. Read AGENTS.md and docs/evaluations.md. RUN_DIR is supplied by the run owner. Use the current run.json and linked Markdown outputs. Make zero paid provider calls.

Run the deterministic evaluator and adversarial tests first. Then open the actual cited sources, starting with all score-3 claims, exclusions, CRM holds and the priority shortlist. In FULL, review every account's fit, pain, persona and disqualifier evidence and all dated triggers. Check whether the source supports the exact local site/campaign and the actual date.

Attempt to falsify these claims:
- The buyer already funds recurring late-shift transport.
- The named person is current and local, and their authority is represented accurately.
- A launch or hiring signal is recent and connected to a transport decision.
- A transport-management role establishes the stated workflow without inventing a failure.
- Swvl's documented capability covers the proposed mechanism, while pilot terms remain proposed.
- Every high score follows the rubric and no exclusion is overridden by a total.
- Tool calls had specific jobs, known reservations and correct nonduplicated costs.
- The value ladder gives a useful result at each stage and uses an evidence-based bridge.

List defects by account/claim ID, severity, source and exact correction. Separate missing support from contradictory support. Review all source metadata assertions rather than trusting status=opened. Do not silently replace missing evidence with assumptions.

Produce evaluation.md with deterministic output, reviewed claims, defects and six proposed human-dimension ratings. Keep approval pending. Ask a real teammate other than the run author to complete templates/human-review.md. Only record approved human_review metadata after that teammate has actually supplied their review. A second model session cannot impersonate the human reviewer.

Finish with PASS DRAFT REVIEW or REVISION REQUIRED and list the exact remaining release gates. This review may identify a failure without finishing a new provider research run.
```
