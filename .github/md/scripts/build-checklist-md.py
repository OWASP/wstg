#!/usr/bin/env python3
"""Generate checklists/checklist.md from checklists/checklist.json.

Tests whose markdown source has been removed are already excluded from
checklist.json (see generate_checklist_json.py's is_removed_placeholder_document),
so they never appear here either. Tests that have been merged into another
test's page remain in checklist.json as a normal entry and are rendered as a
normal row here, consistent with the xlsx checklist.
"""

import json
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CHECKLIST_JSON_PATH = REPO_ROOT / "checklists" / "checklist.json"
OUTPUT_PATH = REPO_ROOT / "checklists" / "checklist.md"

HEADER = ("Test ID", "Test Name", "Status", "Notes")


def build_rows(checklist: OrderedDict) -> list[tuple[str, str]]:
    """(category_id, category_or_test_name) rows; category rows are bold."""
    rows: list[tuple[str, str]] = []
    for category_key, category in checklist.get("categories", {}).items():
        rows.append((f"**{category['id']}**", f"**{category_key}**"))
        for test in category.get("tests", []):
            rows.append((test["id"], test["name"]))
    return rows


def render_table(rows: list[tuple[str, str]]) -> str:
    id_width = max(len(HEADER[0]), *(len(r[0]) for r in rows))
    name_width = max(len(HEADER[1]), *(len(r[1]) for r in rows))
    status_width = len(HEADER[2])
    notes_width = len(HEADER[3])

    def row_line(id_cell: str, name_cell: str) -> str:
        return (
            f"| {id_cell.ljust(id_width)} | {name_cell.ljust(name_width)} "
            f"| {' ' * status_width} | {' ' * notes_width} |"
        )

    lines = [
        row_line(*HEADER[:2]),
        f"|{'-' * (id_width + 2)}|{'-' * (name_width + 2)}"
        f"|{'-' * (status_width + 2)}|{'-' * (notes_width + 2)}|",
    ]
    lines.extend(row_line(id_cell, name_cell) for id_cell, name_cell in rows)
    return "\n".join(lines)


def main() -> None:
    checklist = json.loads(CHECKLIST_JSON_PATH.read_text(encoding="utf-8"))
    rows = build_rows(checklist)
    table = render_table(rows)
    content = (
        "# Testing Checklist\n\n"
        "The following is the list of items to test during the assessment:\n\n"
        '> Note: The `Status` column can be set for values similar to "Pass", "Fail", "N/A".\n\n'
        f"{table}\n"
    )
    OUTPUT_PATH.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
