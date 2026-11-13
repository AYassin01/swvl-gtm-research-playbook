"""Check local Markdown links and keep the repository text-only."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {".md", ".txt", ".json", ".py", ".yml", ".yaml", ".gitignore", ""}
SKIP = {".git", "__pycache__"}


def check(root):
    errors = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in SKIP for part in relative.parts) or not path.is_file():
            continue
        if path.suffix not in ALLOWED and path.name != ".gitignore":
            errors.append(f"Unexpected non-text extension: {relative}")
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            errors.append(f"Cannot read as UTF-8 text: {relative}")
            continue
        if "\x00" in text:
            errors.append(f"Binary content: {relative}")
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                target = target.split("#", 1)[0]
                if target and not (path.parent / target).exists():
                    errors.append(f"Broken local link in {relative}: {target}")
        if re.search(r"gh[pousr]_[A-Za-z0-9]{30,}", text):
            errors.append(f"Potential GitHub credential in {relative}")
    return errors


if __name__ == "__main__":
    found = check(ROOT)
    for error in found:
        print(error)
    print("REPOSITORY FAIL" if found else "REPOSITORY PASS")
    raise SystemExit(bool(found))
