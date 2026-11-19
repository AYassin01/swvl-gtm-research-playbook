"""CLI for guide, usage, and coursework packaging checks."""

import argparse
import json
from pathlib import Path
from checks import check_ready, check_repo, check_usage


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("repo", "usage", "ready"))
    p.add_argument("run_dir", nargs="?", type=Path)
    args = p.parse_args()
    if args.mode != "repo" and args.run_dir is None:
        p.error("usage/ready requires a run directory")
    try:
        if args.mode == "repo":
            errors, report = check_repo(Path(__file__).resolve().parents[1]), {}
        elif args.mode == "usage":
            errors, report = check_usage(args.run_dir)
        else:
            errors, report = check_ready(args.run_dir)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as e:
        print(json.dumps({"passed": False, "load_error": str(e)}))
        return 2
    print(json.dumps({"mode": args.mode, "passed": not errors, "report": report, "gaps": errors,
                      "limit": "Offline checks do not establish source truth, actual account access or instructor acceptance"}, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
