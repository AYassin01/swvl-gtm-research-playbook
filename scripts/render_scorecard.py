"""Render a validated run as portable Markdown without network access."""

import argparse
import json
from pathlib import Path

from evaluate import CRITERIA, disposition, evaluate


ORDER = {name: i for i, name in enumerate((
    "Priority discovery", "Discovery queue", "Verify first", "CRM review", "Exclude",
))}


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def render(run):
    errors = evaluate(run)
    if errors:
        raise ValueError("Run failed structural validation: " + "; ".join(errors))
    sources = {s["id"]: s for s in run["sources"]}
    accounts = sorted(run["accounts"], key=lambda a: (
        ORDER[disposition(a)], -sum(a["scores"][k]["score"] for k in CRITERIA), a["id"],
    ))
    lines = [
        "# Account scorecard", "",
        f"Run `{run['run_id']}`. Evidence as of {run['as_of']}. Mode `{run['mode']}`.", "",
        "Scores and sources describe the recorded research scope. Recheck current facts before use.", "",
        "| ID | Account | Size | Trigger | Pain | Persona | Clean | Total | Disposition |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for account in accounts:
        values = [account["scores"][k]["score"] for k in CRITERIA]
        row = [account["id"], account["account"], *values, sum(values), disposition(account)]
        lines.append("| " + " | ".join(cell(v) for v in row) + " |")
    for account in accounts:
        lines.extend([
            "", f"## {account['id']} · {account['account']}", "",
            f"Domain `{account['domain']}`. Named route in — {account['named_route_in']}.", "",
            f"Next check — {account['next_check']}", "",
            "| Criterion | Score | Rationale and source |",
            "| --- | --- | --- |",
        ])
        for key in CRITERIA:
            entry = account["scores"][key]
            source = sources[entry["source_id"]]
            lines.append(f"| {key} | {entry['score']} | {cell(entry['note'])} [{source['id']}]({source['url']}) |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    try:
        print(render(json.loads(args.run.read_text(encoding="utf-8"))))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Render failed: {error}\n")


if __name__ == "__main__":
    main()
