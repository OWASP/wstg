#!/usr/bin/env python3
"""Generate checklists/checklist.json from WSTG chapter markdown files."""

import json
import os
import re
import sys
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed

# Repo root (…/wstg)
REPO_ROOT = Path(__file__).resolve().parents[3]
DOC_BASE = REPO_ROOT / "document" / "4-Web_Application_Security_Testing"
OUTPUT_PATH = REPO_ROOT / "checklists" / "checklist.json"
REFERENCE_PREFIX = (
    "https://owasp.org/www-project-web-security-testing-guide/latest/"
    "4-Web_Application_Security_Testing/"
)

OPENCRE_STANDARD = "OWASP Web Security Testing Guide (WSTG)"
OPENCRE_BASE_URL = "https://www.opencre.org/rest/v1/standard"
OPENCRE_LOOKUP_DESCRIPTION = (
    "OpenCRE is queried with `GET /rest/v1/standard/<OWASP Web Security Testing Guide "
    "(WSTG)>?section=<WSTG-ID>` (plus `&page=` when the section spans multiple pages)."
)
CRE_IDS_CELL_MAX_LEN = 240
DEFAULT_CONCURRENCY_LIMIT = 4

# ``cre_ids`` / OpenCRE markdown reports use emoji below. Consoles and dark-themed
# editors may use fonts or themes where some characters render monochrome, missing,
# or low contrast; GitHub's job summary / web UI often differs.
#
# Unicode variation selector-16 (U+FE0F): prefer emoji-style (often colored) glyphs over
# text-style symbols where the code point supports both presentations.
EMOJI_PRESENTATION_SELECTOR = "\uFE0F"

# Single map for ``cre_ids`` report emoji (delta bullets, headings, status column, legend).
_CRE_REPORT_EMOJI: dict[str, str] = {
    "Added": f"\u2795{EMOJI_PRESENTATION_SELECTOR}",  # ➕
    "Removed": f"\u2796{EMOJI_PRESENTATION_SELECTOR}",  # ➖
    "Updated": "\U0001F504",  # 🔄
    "Unchanged": f"\u2705{EMOJI_PRESENTATION_SELECTOR}",  # ✅
    "No mapping": "\U0001F6AB",  # 🚫
    "New": "\U0001F195",  # 🆕
}
RETRY_COUNT = 3
REQUEST_TIMEOUT = 30


def get_concurrency_limit() -> int:
    default_limit = min(os.cpu_count() or 1, DEFAULT_CONCURRENCY_LIMIT)
    raw_value = os.environ.get("OPENCRE_CONCURRENCY")

    if raw_value is None:
        return default_limit

    try:
        return max(1, int(raw_value))
    except ValueError:
        return default_limit


CONCURRENCY_LIMIT = get_concurrency_limit()


def emit_markdown_report(text: str) -> None:
    """Print markdown to stdout and append to GITHUB_STEP_SUMMARY when set."""
    print(text, flush=True)
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


class OpenCRELookupError(Exception):
    """Raised when an OpenCRE request cannot be resolved."""

    def __init__(self, message: str, *, http_status: int | None = None) -> None:
        super().__init__(message)
        self.http_status = http_status


def fetch_json_with_retry(url: str, retries: int = RETRY_COUNT) -> dict[str, Any]:
    for attempt in range(retries):
        try:
            req = Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/137.0.0.0 Safari/537.36"
                    ),
                },
            )

            with urlopen(req, timeout=REQUEST_TIMEOUT) as response:
                return json.loads(response.read().decode("utf-8"))

        except HTTPError as e:
            if e.code == 404:
                raise OpenCRELookupError(
                    f"OpenCRE returned HTTP {e.code} for {url}", http_status=e.code
                ) from e

            if attempt == retries - 1:
                raise OpenCRELookupError(
                    f"OpenCRE returned HTTP {e.code} for {url}", http_status=e.code
                ) from e

            time.sleep(2**attempt)

        except URLError as e:
            if attempt == retries - 1:
                raise OpenCRELookupError(
                    f"OpenCRE request failed for {url}: {e}", http_status=None
                ) from e

            time.sleep(2**attempt)

        except Exception as e:
            if attempt == retries - 1:
                raise OpenCRELookupError(
                    f"Unexpected error requesting {url}: {e}", http_status=None
                ) from e

            time.sleep(2**attempt)

    raise OpenCRELookupError(
        f"Failed to fetch OpenCRE data after {retries} attempts: {url}",
        http_status=None,
    )


def extract_cre_ids(data: dict[str, Any], section_id: str) -> list[str]:
    standards = data.get("standards", [])
    if not isinstance(standards, list):
        return []

    cre_ids: list[str] = []

    for item in standards:
        if not isinstance(item, dict):
            continue

        if item.get("section") != section_id:
            continue

        links = item.get("links", [])
        if not isinstance(links, list):
            continue

        for link in links:
            if not isinstance(link, dict):
                continue

            document = link.get("document", {})
            if not isinstance(document, dict):
                continue

            if document.get("doctype") == "CRE":
                cre_id = document.get("id")
                if cre_id:
                    cre_ids.append(cre_id)

    return list(dict.fromkeys(cre_ids))


def _opencre_coerce_total_pages(raw: Any) -> tuple[int, bool]:
    """
    Parse OpenCRE ``total_pages`` for pagination. Returns ``(pages, used_fallback)``.

    ``used_fallback`` is True when the value is ``None``, a ``bool``, a blank string
    (after strip), not accepted by ``int(...)``, or ``int(...) < 1``.

    Otherwise ``pages`` is ``int(...)`` with ``used_fallback`` False. That includes
    positive ``int`` values, strings ``int`` parses (e.g. ``"2"``), and ``float`` values
    (e.g. ``2.9`` truncates toward zero).
    """
    if raw is None:
        return 1, True
    if isinstance(raw, bool):
        return 1, True
    if isinstance(raw, str):
        raw = raw.strip()
        if raw == "":
            return 1, True
    try:
        n = int(raw)
    except (TypeError, ValueError):
        return 1, True
    if n < 1:
        return 1, True
    return n, False


def fetch_mapping(test_id: str) -> tuple[str, list[str]]:
    base_url = (
        f"{OPENCRE_BASE_URL}/{quote(OPENCRE_STANDARD, safe='')}"
        f"?section={quote(test_id, safe='')}"
    )

    first_page = fetch_json_with_retry(base_url)
    all_cre_ids = extract_cre_ids(first_page, test_id)

    raw_pages = first_page.get("total_pages", 1)
    total_pages, pages_fallback = _opencre_coerce_total_pages(raw_pages)
    if pages_fallback:
        print(
            f"WARNING: OpenCRE total_pages {raw_pages!r} for section {test_id!r} "
            f"invalid or not a positive page count; using {total_pages} for pagination.",
            file=sys.stderr,
        )

    for page in range(2, total_pages + 1):
        paged_url = f"{base_url}&page={page}"
        page_data = fetch_json_with_retry(paged_url)
        all_cre_ids.extend(extract_cre_ids(page_data, test_id))

    return test_id, list(dict.fromkeys(all_cre_ids))


def _cre_ids_map_from_categories(categories: dict[str, Any]) -> dict[str, list[str]]:
    """
    Build ``WSTG test id -> cre id list`` from a ``categories`` mapping (disk JSON or
    in-memory checklist). Last occurrence of a duplicate id wins.
    """
    out: dict[str, list[str]] = {}
    for category in categories.values():
        if not isinstance(category, dict):
            continue
        tests = category.get("tests", [])
        if not isinstance(tests, list):
            continue
        for test in tests:
            if not isinstance(test, dict):
                continue
            test_id = test.get("id")
            cre_ids = test.get("cre_ids")
            if isinstance(test_id, str) and isinstance(cre_ids, list):
                cleaned: list[str] = []
                for cre_id in cre_ids:
                    if not isinstance(cre_id, str):
                        continue
                    stripped = cre_id.strip()
                    if not stripped:
                        continue
                    cleaned.append(stripped)
                out[test_id] = cleaned
    return out


def load_existing_cre_ids(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"WARNING: Could not load existing checklist data from {path}: {exc}")
        return {}

    categories = data.get("categories", {})
    if not isinstance(categories, dict):
        return {}

    return _cre_ids_map_from_categories(categories)


def collect_cre_ids_by_test_id(checklist: OrderedDict) -> dict[str, list[str]]:
    """
    Normalized ``test id -> cre id list`` from an in-memory checklist.
    If the same WSTG id appears more than once, the last occurrence wins.
    """
    categories = checklist.get("categories", {})
    if not isinstance(categories, dict):
        return {}
    return _cre_ids_map_from_categories(categories)


def _format_cre_ids_cell(cre_ids: list[str]) -> str:
    joined = ", ".join(cre_ids)
    if len(joined) > CRE_IDS_CELL_MAX_LEN:
        return joined[: CRE_IDS_CELL_MAX_LEN - 1] + "…"
    return joined


def _sort_test_ids_guide_order(ids: Iterable[str], guide_rank: dict[str, int]) -> list[str]:
    sentinel = len(guide_rank) + 1
    return sorted(ids, key=lambda tid: (guide_rank.get(tid, sentinel), tid))


def collect_test_names_by_id(checklist: OrderedDict) -> dict[str, str]:
    """Last occurrence wins if the same WSTG id appears more than once."""
    names: dict[str, str] = {}
    categories = checklist.get("categories", {})
    if not isinstance(categories, dict):
        return names
    for category in categories.values():
        if not isinstance(category, dict):
            continue
        tests = category.get("tests", [])
        if not isinstance(tests, list):
            continue
        for test in tests:
            if not isinstance(test, dict):
                continue
            tid = test.get("id")
            if not isinstance(tid, str):
                continue
            names[tid] = str(test.get("name", ""))
    return names


def _cre_row_status(old: list[str], new: list[str]) -> str:
    """
    Machine status key comparing prior file vs after enrichment.
    ``Unchanged`` = same non-empty mapping as before; ``No mapping`` = no ``cre_ids`` now
    (including still-empty and cleared); ``New`` / ``Updated`` = mapping added or changed.
    """
    if old == new:
        return "Unchanged" if old else "No mapping"
    if not new:
        return "No mapping"
    if not old:
        return "New"
    return "Updated"


def _cre_status_display(status_key: str) -> str:
    """Status cell / legend text with leading icon."""
    icon = _CRE_REPORT_EMOJI.get(status_key, "\u2022")  # bullet fallback
    return f"{icon} {status_key}"


def enrich_with_opencre(
    checklist: OrderedDict,
) -> tuple[OrderedDict, dict[str, list[str]], list[str], list[tuple[str, int | None, str]]]:
    all_tests = []
    existing_cre_ids = load_existing_cre_ids(OUTPUT_PATH)

    categories = checklist.get("categories", {})
    if isinstance(categories, dict):
        for category in categories.values():
            if not isinstance(category, dict):
                continue

            tests = category.get("tests", [])
            if isinstance(tests, list):
                all_tests.extend(tests)

    unique_ids = list(
        dict.fromkeys(
            test.get("id")
            for test in all_tests
            if isinstance(test, dict) and test.get("id")
        )
    )

    results: dict[str, list[str] | None] = {}
    failures: list[tuple[str, int | None, str]] = []

    with ThreadPoolExecutor(max_workers=CONCURRENCY_LIMIT) as executor:
        futures = {
            executor.submit(fetch_mapping, test_id): test_id
            for test_id in unique_ids
        }

        for future in as_completed(futures):
            test_id = futures[future]
            try:
                returned_id, cre_ids = future.result()
                results[returned_id] = cre_ids
            except OpenCRELookupError as exc:
                results[test_id] = None
                failures.append((test_id, exc.http_status, str(exc)))
            except Exception as exc:
                results[test_id] = None
                failures.append((test_id, None, str(exc)))

    for test in all_tests:
        if not isinstance(test, dict):
            continue

        test_id = test.get("id")
        next_ids = results.get(test_id)

        if next_ids is None:
            prior_ids = existing_cre_ids.get(test_id)
            if prior_ids:
                test["cre_ids"] = prior_ids
            continue

        if not next_ids:
            if "cre_ids" in test:
                del test["cre_ids"]
            continue

        if test.get("cre_ids") != next_ids:
            test["cre_ids"] = next_ids

    return checklist, existing_cre_ids, unique_ids, failures


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


def is_removed_placeholder_document(content: str) -> bool:
    """True for stub markdown pages that only retain a removal notice."""
    meaningful_lines = [line.strip() for line in content.splitlines() if line.strip()]
    if len(meaningful_lines) < 4:
        return False
    last_meaningful_line = meaningful_lines[-1].rstrip().rstrip(".")
    return last_meaningful_line == "This content has been removed"


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
    """Build markdown for Test Objectives quality; emit to stdout and job summary."""
    lines: list[str] = []
    if not entries:
        lines.append("## Checklist JSON: WSTG markdown — Test Objectives\n\n")
        lines.append(
            "All checklist rows include at least one non-blank objective parsed from "
            "each chapter's `## Test Objectives` section.\n"
        )
    else:
        lines.append(
            "## Checklist JSON: WSTG markdown — empty or blank Test Objectives\n\n"
        )
        lines.append(
            "These rows have empty or whitespace-only objectives in JSON (from each "
            "chapter's `## Test Objectives` section). The Excel builder shows **N/A** "
            "for the objective column.\n\n"
        )
        lines.append("| Category | ID | Name |\n")
        lines.append("| --- | --- | --- |\n")
        for category, tid, name, _ref in entries:
            safe_cat = category.replace("|", "\\|")
            safe_name = name.replace("|", "\\|")
            lines.append(f"| {safe_cat} | `{tid}` | {safe_name} |\n")

    emit_markdown_report("".join(lines))


def _cre_guide_status_table_rows(
    data: OrderedDict,
    existing_cre_ids: dict[str, list[str]],
    new_cre: dict[str, list[str]],
    guide_order_ids: list[str],
) -> list[tuple[str, str, str, str]]:
    """
    One row per WSTG id in guide order: (test_id, name, status, cre_cell).
    ``cre_cell`` is ``—`` when there are no ``cre_ids``.
    """
    names = collect_test_names_by_id(data)
    rows: list[tuple[str, str, str, str]] = []
    for tid in guide_order_ids:
        old = existing_cre_ids.get(tid, [])
        new = new_cre.get(tid, [])
        status = _cre_row_status(old, new)
        parts = [str(x) for x in new if isinstance(x, str) and x]
        cre_cell = _format_cre_ids_cell(parts) if parts else "—"
        rows.append((tid, names.get(tid, ""), status, cre_cell))
    return rows


def _write_cre_opencre_summary_report(
    data: OrderedDict,
    existing_cre_ids: dict[str, list[str]],
    guide_order_ids: list[str],
    opencre_failures: list[tuple[str, int | None, str]],
) -> None:
    """
    One markdown section: ``cre_ids`` delta vs prior ``checklist.json`` plus a
    per-test table in guide order (ID, name, status, CRE ids).
    """
    guide_rank = {tid: i for i, tid in enumerate(guide_order_ids)}
    new_cre = collect_cre_ids_by_test_id(data)
    all_ids = set(existing_cre_ids) | set(new_cre) | set(guide_order_ids)

    added: list[str] = []
    removed: list[str] = []
    updated: list[str] = []
    unchanged: list[str] = []
    for tid in all_ids:
        old = existing_cre_ids.get(tid, [])
        new = new_cre.get(tid, [])
        if old == new:
            unchanged.append(tid)
        elif not old and new:
            added.append(tid)
        elif old and not new:
            removed.append(tid)
        else:
            updated.append(tid)

    unchanged_mapped = sum(
        1 for tid in unchanged if existing_cre_ids.get(tid, [])
    )
    unchanged_no_mapping = len(unchanged) - unchanged_mapped

    lines: list[str] = [
        "## Checklist JSON: OpenCRE and `cre_ids`\n\n",
        f"{OPENCRE_LOOKUP_DESCRIPTION}\n\n",
    ]
    if opencre_failures:
        n404 = sum(1 for _tid, st, _m in opencre_failures if st == 404)
        nother = len(opencre_failures) - n404
        lines.append(
            f"**OpenCRE:** {len(opencre_failures)} section lookup(s) failed "
            f"({n404} HTTP 404, {nother} other). Prior `cre_ids` from `checklist.json` "
            "were kept when present.\n\n"
        )
    lines.append("### Delta vs prior `checklist.json`\n\n")
    if not existing_cre_ids and not OUTPUT_PATH.exists():
        lines.append(
            f"Prior baseline had no stored `cre_ids` (`{OUTPUT_PATH.name}` missing).\n\n"
        )
    elif not existing_cre_ids:
        lines.append(
            f"Prior baseline had no stored `cre_ids` (empty or unreadable `{OUTPUT_PATH.name}`).\n\n"
        )
    else:
        lines.append(
            f"Compared against `cre_ids` previously read from `{OUTPUT_PATH.as_posix()}`.\n\n"
        )
    lines.append(
        "Counts are **per WSTG test id**; if the same id appeared more than once in JSON, "
        "the last occurrence in the file defines the prior value.\n\n"
    )
    _delta_summary: list[tuple[str, int, str]] = [
        ("Added", len(added), "No prior `cre_ids`, now non-empty"),
        ("Removed", len(removed), "Had `cre_ids`, now absent or empty"),
        ("Updated", len(updated), "Non-empty before and after, lists differ"),
        ("Unchanged", unchanged_mapped, "Same non-empty `cre_ids` as prior"),
        ("No mapping", unchanged_no_mapping, "No `cre_ids` before and after"),
    ]
    lines.append("| Status | Count | Disposition |\n")
    lines.append("| --- | --: | --- |\n")
    for label, count, disposition in _delta_summary:
        emoji = _CRE_REPORT_EMOJI[label]
        status_cell = f"{emoji} **{label}**"
        disp = disposition.replace("|", "\\|")
        lines.append(f"| {status_cell} | {count} | {disp} |\n")
    lines.append("\n")

    def pipe_escape(s: str) -> str:
        return s.replace("|", "\\|")

    if added:
        lines.append(f"#### {_CRE_REPORT_EMOJI['Added']} Added ({len(added)})\n\n")
        lines.append("| WSTG ID | CRE IDs |\n| --- | --- |\n")
        for tid in _sort_test_ids_guide_order(added, guide_rank):
            cell = pipe_escape(_format_cre_ids_cell(new_cre[tid]))
            lines.append(f"| `{tid}` | {cell} |\n")
        lines.append("\n")
    if removed:
        lines.append(f"#### {_CRE_REPORT_EMOJI['Removed']} Removed ({len(removed)})\n\n")
        lines.append("| WSTG ID | Previous CRE IDs |\n| --- | --- |\n")
        for tid in _sort_test_ids_guide_order(removed, guide_rank):
            cell = pipe_escape(_format_cre_ids_cell(existing_cre_ids[tid]))
            lines.append(f"| `{tid}` | {cell} |\n")
        lines.append("\n")
    if updated:
        lines.append(f"#### {_CRE_REPORT_EMOJI['Updated']} Updated ({len(updated)})\n\n")
        lines.append("| WSTG ID | Previous CRE IDs | New CRE IDs |\n| --- | --- | --- |\n")
        for tid in _sort_test_ids_guide_order(updated, guide_rank):
            prev_c = pipe_escape(_format_cre_ids_cell(existing_cre_ids[tid]))
            new_c_cell = pipe_escape(_format_cre_ids_cell(new_cre[tid]))
            lines.append(f"| `{tid}` | {prev_c} | {new_c_cell} |\n")
        lines.append("\n")

    lines.append("### `cre_ids` by test (guide order)\n\n")
    rows = _cre_guide_status_table_rows(
        data, existing_cre_ids, new_cre, guide_order_ids
    )
    lines.append(
        f"**{len(rows)}** test id(s). **Status** compares prior `checklist.json` to this run: "
        f"{_cre_status_display('Unchanged')} = same non-empty mapping; "
        f"{_cre_status_display('No mapping')} = no `cre_ids` now (including still empty or cleared); "
        f"{_cre_status_display('New')} / {_cre_status_display('Updated')} = mapping added or changed.\n\n"
    )
    lines.append("| WSTG ID | Name | Status | CRE IDs |\n")
    lines.append("| --- | --- | --- | --- |\n")
    for tid, name, status_key, cre_cell in rows:
        lines.append(
            f"| `{tid}` | {pipe_escape(name)} | {_cre_status_display(status_key)} | "
            f"{pipe_escape(cre_cell)} |\n"
        )
    emit_markdown_report("".join(lines))


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
            if is_removed_placeholder_document(text):
                continue
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
    data, existing_cre_ids, unique_ids, opencre_failures = enrich_with_opencre(data)
    _write_cre_opencre_summary_report(
        data, existing_cre_ids, unique_ids, opencre_failures
    )
    _write_empty_objectives_report(_empty_objective_entries(data))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    OUTPUT_PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
