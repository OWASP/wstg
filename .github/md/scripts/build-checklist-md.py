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

# Fixed (not data-derived) column widths, generous enough for known IDs/names
# plus headroom for new ones. Fixed widths keep the table aligned like a
# hand-formatted one, while avoiding the whole-table reflow you'd get from
# computing widths from the widest current cell: unrelated rows only change
# when their own content changes, not when some other row's text does.
ID_WIDTH = 17
NAME_WIDTH = 74


def build_rows(checklist: OrderedDict) -> list[tuple[str, str]]:
    """(category_id, category_or_test_name) rows; category rows are bold."""
    rows: list[tuple[str, str]] = []
    for category_key, category in checklist.get("categories", {}).items():
        rows.append((f"**{category['id']}**", f"**{category_key}**"))
        for test in category.get("tests", []):
            rows.append((test["id"], test["name"]))
    return rows


def render_table(rows: list[tuple[str, str]]) -> str:
    def row_line(id_cell: str, name_cell: str, status_cell: str = "", notes_cell: str = "") -> str:
        id_width = max(ID_WIDTH, len(id_cell))
        name_width = max(NAME_WIDTH, len(name_cell))
        return (
            f"| {id_cell.ljust(id_width)} | {name_cell.ljust(name_width)} "
            f"| {status_cell.ljust(len(HEADER[2]))} | {notes_cell.ljust(len(HEADER[3]))} |"
        )

    lines = [
        row_line(HEADER[0], HEADER[1], HEADER[2], HEADER[3]),
        f"|{'-' * (ID_WIDTH + 2)}|{'-' * (NAME_WIDTH + 2)}"
        f"|{'-' * (len(HEADER[2]) + 2)}|{'-' * (len(HEADER[3]) + 2)}|",
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
