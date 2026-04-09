#!/usr/bin/env python3
"""Generate checklists/checklist.json from WSTG chapter markdown files."""

import json
import os
import re
import sys
from collections import OrderedDict
from pathlib import Path

# Repo root (…/wstg)
REPO_ROOT = Path(__file__).resolve().parents[3]
DOC_BASE = REPO_ROOT / "document" / "4-Web_Application_Security_Testing"
OUTPUT_PATH = REPO_ROOT / "checklists" / "checklist.json"
REFERENCE_PREFIX = (
    "https://owasp.org/www-project-web-security-testing-guide/latest/"
    "4-Web_Application_Security_Testing/"
)


def category_label_from_dirname(dirname: str) -> str | None:
    """Human-readable category name from a chapter folder (e.g. ``01-Information_Gathering``)."""
    segments = dirname.split("-")
    if not segments:
        return None
    try:
        prefix = int(segments[0])
    except ValueError:
        return None
    if prefix <= 0:
        return None
    if len(segments) > 2:
        rest = "-".join(segments[1:])
    else:
        rest = segments[1]
    return rest.replace("_", " ")


def wstg_id_from_table_line(line: str) -> str | None:
    """Return the first ``WSTG-…`` token found in a pipe-table row, if any."""
    if "|WSTG-" not in line:
        return None
    for part in line.split("|"):
        p = part.strip()
        if p.startswith("WSTG-"):
            return p
    return None


def category_wstg_id_from_intro(category_dir: Path) -> str | None:
    """Category id from the first ``WSTG-…`` id in ``01-*.md`` files (``WSTG-INFO-01`` → ``WSTG-INFO``)."""
    parts: list[str] = []
    for p in sorted(category_dir.glob("01-*.md")):
        parts.append(p.read_text(encoding="utf-8"))
    if not parts:
        return None
    for line in "\n".join(parts).splitlines():
        tid = wstg_id_from_table_line(line)
        if tid:
            return tid.replace("-01", "", 1)
    return None


def title_from_h1_prefix(content: str) -> str:
    """Strip the leading ``# `` from the document title line."""
    first = content.splitlines()[0] if content else ""
    return first[2:] if len(first) >= 2 else first


def _nonblank_lines_in_objectives_section(content: str) -> list[str]:
    """Lines under ``## Test Objectives`` until the next ``## `` heading; skips blank lines."""
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "## Test Objectives":
            i += 1
            break
        i += 1
    else:
        return []

    out: list[str] = []
    while i < len(lines):
        line = lines[i]
        if re.match(r"^## ", line):
            break
        if line.split():
            out.append(line)
        i += 1
    return out


def extract_test_objectives(content: str) -> list[str]:
    """
    Bullet text from the Test Objectives section: drop leading ``- `` on each line,
    normalize line breaks, and strip tab/CR/LF characters from each line body.

    If the section has no bullet lines, returns ``[\"\"]`` so downstream consumers
    still see a single (empty) objective like an empty checklist row.
    """
    section_lines = _nonblank_lines_in_objectives_section(content)
    block = "\n".join(section_lines)
    block = block.rstrip("\n")
    if block == "":
        physical_lines = [""]
    else:
        physical_lines = block.split("\n")

    objectives: list[str] = []
    for line in physical_lines:
        line = line.strip(" \t\n")
        cleaned = line.translate(str.maketrans("", "", "\t\r\n"))
        text = cleaned[2:] if len(cleaned) >= 2 else ""
        objectives.append(text)
    return objectives


def first_wstg_id_in_document(content: str) -> str | None:
    for line in content.splitlines():
        tid = wstg_id_from_table_line(line)
        if tid:
            return tid
    return None


def reference_url(relative_md_stem: str) -> str:
    return f"{REFERENCE_PREFIX}{relative_md_stem}"


def _objectives_are_empty_or_blank(objectives: list[str]) -> bool:
    if not objectives:
        return True
    return all(not o.strip() for o in objectives)


def _empty_objective_entries(
    data: OrderedDict,
) -> list[tuple[str, str, str, str]]:
    """(category_label, test_id, test_name, reference_url) for tests with no real objective text."""
    rows: list[tuple[str, str, str, str]] = []
    for category_label, category in data["categories"].items():
        for test in category["tests"]:
            objs = test.get("objectives", [])
            if _objectives_are_empty_or_blank(objs):
                rows.append(
                    (
                        category_label,
                        test["id"],
                        test["name"],
                        test["reference"],
                    )
                )
    return rows


def _write_empty_objectives_report(entries: list[tuple[str, str, str, str]]) -> None:
    """
    In GitHub Actions, append to the job summary. Locally, print to stderr.
    Never raises for missing env or IO errors beyond logging to stderr.
    """
    lines: list[str] = []
    if not entries:
        lines.append("## Checklist JSON: Test Objectives\n\n")
        lines.append(
            "All generated entries have at least one non-blank objective.\n"
        )
    else:
        lines.append("## Checklist JSON: empty or blank Test Objectives\n\n")
        lines.append(
            "These IDs have no non-blank objective strings; the Excel builder "
            "will show **N/A** for objectives.\n\n"
        )
        lines.append("| Category | ID | Name |\n")
        lines.append("| --- | --- | --- |\n")
        for category, tid, name, _ref in entries:
            safe_cat = category.replace("|", "\\|")
            safe_name = name.replace("|", "\\|")
            lines.append(f"| {safe_cat} | `{tid}` | {safe_name} |\n")

    text = "".join(lines)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        try:
            with open(summary_path, "a", encoding="utf-8") as fh:
                fh.write(text)
        except OSError as exc:
            print(
                f"Warning: could not write GITHUB_STEP_SUMMARY: {exc}",
                file=sys.stderr,
            )
            print(text, file=sys.stderr)
    else:
        print(text, file=sys.stderr)


def build_checklist() -> OrderedDict:
    categories: OrderedDict[str, OrderedDict] = OrderedDict()

    for category_dir in sorted(DOC_BASE.iterdir(), key=lambda p: p.name):
        if not category_dir.is_dir():
            continue
        cat_key = category_label_from_dirname(category_dir.name)
        if cat_key is None:
            continue

        cid = category_wstg_id_from_intro(category_dir)
        if not cid:
            continue

        tests: list[OrderedDict] = []
        for md_path in sorted(category_dir.glob("*.md")):
            if md_path.name == "README.md":
                continue
            text = md_path.read_text(encoding="utf-8")
            tid = first_wstg_id_in_document(text)
            if not tid:
                continue
            rel_stem = md_path.relative_to(DOC_BASE).as_posix()
            if rel_stem.endswith(".md"):
                rel_stem = rel_stem[: -len(".md")]
            tests.append(
                OrderedDict(
                    [
                        ("name", title_from_h1_prefix(text)),
                        ("id", tid),
                        ("reference", reference_url(rel_stem)),
                        ("objectives", extract_test_objectives(text)),
                    ]
                )
            )

        categories[cat_key] = OrderedDict([("id", cid), ("tests", tests)])

    return OrderedDict([("categories", categories)])


def main() -> None:
    data = build_checklist()
    _write_empty_objectives_report(_empty_objective_entries(data))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    OUTPUT_PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
