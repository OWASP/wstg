#!/usr/bin/env python3
"""Generate checklists/checklist.json from WSTG chapter markdown files."""

import json
import os
import re
import sys
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any
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
                raise OpenCRELookupError(f"OpenCRE returned 404 for {url}") from e

            if attempt == retries - 1:
                raise

            time.sleep(2**attempt)

        except URLError as e:
            if attempt == retries - 1:
                raise OpenCRELookupError(f"OpenCRE request failed for {url}: {e}") from e

            time.sleep(2**attempt)

        except Exception as e:
            if attempt == retries - 1:
                raise OpenCRELookupError(f"Unexpected error requesting {url}: {e}") from e

            time.sleep(2**attempt)

    raise OpenCRELookupError(f"Failed to fetch OpenCRE data after {retries} attempts: {url}")


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


def fetch_mapping(test_id: str) -> tuple[str, list[str]]:
    base_url = (
        f"{OPENCRE_BASE_URL}/{quote(OPENCRE_STANDARD, safe='')}"
        f"?section={quote(test_id, safe='')}"
    )

    first_page = fetch_json_with_retry(base_url)
    all_cre_ids = extract_cre_ids(first_page, test_id)

    total_pages = first_page.get("total_pages", 1)
    if not isinstance(total_pages, int) or total_pages < 1:
        total_pages = 1

    for page in range(2, total_pages + 1):
        paged_url = f"{base_url}&page={page}"
        page_data = fetch_json_with_retry(paged_url)
        all_cre_ids.extend(extract_cre_ids(page_data, test_id))

    return test_id, list(dict.fromkeys(all_cre_ids))


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

    existing_cre_ids: dict[str, list[str]] = {}

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
                existing_cre_ids[test_id] = [
                    cre_id for cre_id in cre_ids if isinstance(cre_id, str)
                ]

    return existing_cre_ids


def _opencre_failure_is_404(message: str) -> bool:
    return "404" in message


def _opencre_failure_response_code(message: str) -> str:
    """Best-effort HTTP status from OpenCRE error text; ``—`` when not present."""
    m = re.search(r"returned (\d{3})\b", message)
    if m:
        return m.group(1)
    if "404" in message:
        return "404"
    return "—"


def _sort_opencre_failures_guide_order(
    rows: list[tuple[str, str]], guide_rank: dict[str, int]
) -> list[tuple[str, str]]:
    """Order failures like the checklist (chapter order, then markdown file order)."""
    sentinel = len(guide_rank) + 1
    return sorted(
        rows,
        key=lambda r: (guide_rank.get(r[0], sentinel), r[0]),
    )


def _emit_opencre_failure_report(
    failures: list[tuple[str, str]], guide_order_ids: list[str]
) -> None:
    if not failures:
        return
    guide_rank = {tid: i for i, tid in enumerate(guide_order_ids)}
    lines: list[str] = [
        "## Checklist JSON: OpenCRE lookup failures\n\n",
        f"{OPENCRE_LOOKUP_DESCRIPTION}\n\n",
        f"**{len(failures)}** WSTG test ID(s) could not be fetched from OpenCRE; "
        "existing `cre_ids` in `checklist.json` are kept when present.\n\n",
    ]
    not_found = _sort_opencre_failures_guide_order(
        [(tid, msg) for tid, msg in failures if _opencre_failure_is_404(msg)],
        guide_rank,
    )
    other = _sort_opencre_failures_guide_order(
        [(tid, msg) for tid, msg in failures if not _opencre_failure_is_404(msg)],
        guide_rank,
    )

    def append_table(title: str, rows: list[tuple[str, str]]) -> None:
        lines.append(f"### {title}\n\n")
        if not rows:
            lines.append("_None._\n\n")
            return
        lines.append("| WSTG ID | Response Code |\n")
        lines.append("| --- | --- |\n")
        for tid, msg in rows:
            code = _opencre_failure_response_code(msg)
            lines.append(f"| `{tid}` | {code} |\n")
        lines.append("\n")

    append_table(f"HTTP 404 ({len(not_found)})", not_found)
    append_table(f"Other errors ({len(other)})", other)
    emit_markdown_report("".join(lines))


def enrich_with_opencre(checklist: OrderedDict) -> OrderedDict:
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
    failures: list[tuple[str, str]] = []

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
            except Exception as exc:
                message = str(exc)
                results[test_id] = None
                failures.append((test_id, message))

    _emit_opencre_failure_report(failures, unique_ids)

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

    return checklist


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
    return meaningful_lines[-1] == "This content has been removed"


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


def _cre_mapping_success_rows(
    data: OrderedDict,
) -> list[tuple[str, str, str, str]]:
    """(category_label, test_id, test_name, cre_joined) for tests with non-empty cre_ids."""
    rows: list[tuple[str, str, str, str]] = []
    categories = data.get("categories", {})
    if not isinstance(categories, dict):
        return rows
    for category_label, category in categories.items():
        if not isinstance(category, dict):
            continue
        tests = category.get("tests", [])
        if not isinstance(tests, list):
            continue
        for test in tests:
            if not isinstance(test, dict):
                continue
            cre_ids = test.get("cre_ids")
            if not isinstance(cre_ids, list) or not cre_ids:
                continue
            parts = [str(x) for x in cre_ids if isinstance(x, str) and x]
            if not parts:
                continue
            joined = ", ".join(parts)
            if len(joined) > CRE_IDS_CELL_MAX_LEN:
                joined = joined[: CRE_IDS_CELL_MAX_LEN - 1] + "…"
            tid = test.get("id", "")
            name = test.get("name", "")
            if not isinstance(tid, str):
                tid = str(tid)
            if not isinstance(name, str):
                name = str(name)
            rows.append((str(category_label), tid, name, joined))
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def _write_cre_mapping_success_report(data: OrderedDict) -> None:
    rows = _cre_mapping_success_rows(data)
    lines: list[str] = ["## Checklist JSON: OpenCRE mappings (success)\n\n"]
    if not rows:
        lines.append("No tests have non-empty `cre_ids` after this run.\n")
        emit_markdown_report("".join(lines))
        return
    lines.append(
        f"{OPENCRE_LOOKUP_DESCRIPTION}\n\n"
        f"**{len(rows)}** checklist row(s) have at least one CRE id from OpenCRE.\n\n"
    )
    lines.append("| Category | ID | Name | CRE IDs |\n")
    lines.append("| --- | --- | --- | --- |\n")
    for category, tid, name, cre_cell in rows:
        safe_cat = category.replace("|", "\\|")
        safe_name = name.replace("|", "\\|")
        safe_cre = cre_cell.replace("|", "\\|")
        lines.append(f"| {safe_cat} | `{tid}` | {safe_name} | {safe_cre} |\n")
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
    data = enrich_with_opencre(data)
    _write_cre_mapping_success_report(data)
    _write_empty_objectives_report(_empty_objective_entries(data))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    OUTPUT_PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
