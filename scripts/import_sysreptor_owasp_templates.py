#!/usr/bin/env python3
"""
Import Markdown finding templates from a local templates directory into SysReptor.

The script parses the bilingual Markdown files generated in this repository and
uploads each file as one multilingual SysReptor finding template using the
official `reptor` Python API client. German and English sections are imported as
translations of the same finding template.

Required for upload:
    pip3 install reptor

Authentication defaults:
    REPTOR_SERVER=https://sysreptor.example.com/
    REPTOR_TOKEN=<api-token>

Example dry run:
    python3 scripts/import_sysreptor_owasp_templates.py --dry-run

Example upload:
    REPTOR_SERVER=https://sysreptor.example.com/ \
    REPTOR_TOKEN=... \
    python3 scripts/import_sysreptor_owasp_templates.py

Successful uploads write a tab-separated template ID map to:
    sysreptor_template_id_map.txt

Default field mapping:
    Overview       -> summary
    Description    -> description
    Recommendation -> recommendation
    Reproduction   -> steps
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_TEMPLATE_DIR = Path("templates/owasp-top10")
SECTION_NAMES = {
    "en-US": {
        "overview": "Overview",
        "description": "Description",
        "recommendation": "Recommendation",
        "reproduction": "Reproduction",
    },
    "de-DE": {
        "overview": "\u00dcbersicht",
        "description": "Beschreibung",
        "recommendation": "Empfehlung",
        "reproduction": "Reproduktion",
    },
}
SEVERITY_MAP = {
    "informational": "info",
    "info": "info",
    "low": "low",
    "medium": "medium",
    "high": "high",
    "critical": "critical",
    "informativ": "info",
    "niedrig": "low",
    "mittel": "medium",
    "hoch": "high",
    "kritisch": "critical",
}


@dataclass(frozen=True)
class MarkdownTranslation:
    language: str
    title: str
    overview: str
    description: str
    recommendation: str
    reproduction: str
    severity: str | None
    cvss_vector: str | None


@dataclass(frozen=True)
class MarkdownTemplate:
    path: Path
    category: str
    slug: str
    translations: list[MarkdownTranslation]


@dataclass(frozen=True)
class ImportResult:
    status: str
    template_id: str | None
    title: str
    languages: list[str]
    source_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import bilingual Markdown templates into SysReptor finding templates.",
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=DEFAULT_TEMPLATE_DIR,
        help=f"Directory containing Markdown templates. Default: {DEFAULT_TEMPLATE_DIR}",
    )
    parser.add_argument(
        "--server",
        default=os.environ.get("REPTOR_SERVER"),
        help="SysReptor server URL. Defaults to REPTOR_SERVER.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("REPTOR_TOKEN"),
        help="SysReptor API token. Defaults to REPTOR_TOKEN.",
    )
    parser.add_argument(
        "--overview-field",
        default="summary",
        help="SysReptor field ID for the Overview section. Default: summary",
    )
    parser.add_argument(
        "--description-field",
        default="description",
        help="SysReptor field ID for the Description section. Default: description",
    )
    parser.add_argument(
        "--recommendation-field",
        default="recommendation",
        help="SysReptor field ID for the Recommendation section. Default: recommendation",
    )
    parser.add_argument(
        "--reproduction-field",
        default="steps",
        help="SysReptor field ID for the Reproduction section. Default: steps",
    )
    parser.add_argument(
        "--main-language",
        choices=("en-US", "de-DE"),
        default="en-US",
        help="Main translation language for duplicate checks and UI display. Default: en-US",
    )
    parser.add_argument(
        "--status",
        default="finished",
        help="Translation status to set in SysReptor. Default: finished",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Additional tag to add. Can be supplied multiple times.",
    )
    parser.add_argument(
        "--template-set-tag",
        default=None,
        help="Template set tag to add. Defaults to the templates directory name.",
    )
    parser.add_argument(
        "--include-metadata",
        action="store_true",
        help="Also import severity and CVSS vector when present.",
    )
    parser.add_argument(
        "--update-existing",
        action="store_true",
        help="Update an existing template with the same main title instead of skipping it.",
    )
    parser.add_argument(
        "--id-map-output",
        type=Path,
        default=Path("sysreptor_template_id_map.txt"),
        help="TXT file written after import with template IDs and names. Default: sysreptor_template_id_map.txt",
    )
    parser.add_argument(
        "--no-id-map",
        action="store_true",
        help="Do not write a template ID map after import.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and print what would be uploaded without contacting SysReptor.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print generated SysReptor payloads as JSON. Best used with --dry-run.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Only process the first N templates. Useful for testing.",
    )
    return parser.parse_args()


def strip_horizontal_rules(markdown: str) -> str:
    lines = markdown.strip().splitlines()
    while lines and lines[0].strip() == "---":
        lines.pop(0)
    while lines and lines[-1].strip() == "---":
        lines.pop()
    return "\n".join(lines).strip()


def extract_section(block: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$"
        rf"(?P<body>.*?)(?=^##\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(block)
    if not match:
        return ""
    return strip_horizontal_rules(match.group("body"))


def parse_table_value(block: str, labels: tuple[str, ...]) -> str | None:
    wanted = {label.lower() for label in labels}
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        label = cells[0].lower()
        if label in wanted:
            return cells[1].strip() or None
    return None


def split_language_blocks(markdown: str) -> list[str]:
    starts = [match.start() for match in re.finditer(r"(?m)^#\s+", markdown)]
    if not starts:
        return []
    starts.append(len(markdown))
    return [markdown[starts[i] : starts[i + 1]].strip() for i in range(len(starts) - 1)]


def infer_language(block: str) -> str:
    if re.search(r"(?m)^##\s+Overview\s*$", block):
        return "en-US"
    if re.search(r"(?m)^##\s+\u00dcbersicht\s*$", block):
        return "de-DE"
    raise ValueError("could not infer language from section headings")


def parse_translation(block: str) -> MarkdownTranslation:
    title_match = re.match(r"^#\s+(?P<title>[^\n]+)\s*", block)
    if not title_match:
        raise ValueError("missing top-level title")

    language = infer_language(block)
    headings = SECTION_NAMES[language]
    severity = parse_table_value(block, ("Severity", "Schweregrad"))
    cvss_vector = parse_table_value(block, ("CVSS Vector", "CVSS Vektor"))

    return MarkdownTranslation(
        language=language,
        title=title_match.group("title"),
        overview=extract_section(block, headings["overview"]),
        description=extract_section(block, headings["description"]),
        recommendation=extract_section(block, headings["recommendation"]),
        reproduction=extract_section(block, headings["reproduction"]),
        severity=severity,
        cvss_vector=cvss_vector,
    )


def parse_template(path: Path, root: Path) -> MarkdownTemplate:
    markdown = path.read_text(encoding="utf-8")
    translations = [parse_translation(block) for block in split_language_blocks(markdown)]
    if not translations:
        raise ValueError("no translations found")
    languages = {translation.language for translation in translations}
    required_languages = {"en-US", "de-DE"}
    if languages != required_languages:
        missing = ", ".join(sorted(required_languages - languages))
        extra = ", ".join(sorted(languages - required_languages))
        details = []
        if missing:
            details.append(f"missing: {missing}")
        if extra:
            details.append(f"unexpected: {extra}")
        raise ValueError(f"expected German and English translations ({'; '.join(details)})")

    missing_sections = [
        f"{translation.language}:{name}"
        for translation in translations
        for name in ("overview", "description", "recommendation", "reproduction")
        if not getattr(translation, name)
    ]
    if missing_sections:
        raise ValueError(f"missing section(s): {', '.join(missing_sections)}")

    relative = path.relative_to(root)
    category = relative.parts[0] if len(relative.parts) > 1 else "uncategorized"
    return MarkdownTemplate(
        path=path,
        category=category,
        slug=path.stem,
        translations=translations,
    )


def severity_value(raw: str | None) -> str | None:
    if not raw:
        return None
    return SEVERITY_MAP.get(raw.strip().lower())


def cvss_value(raw: str | None) -> str | None:
    if not raw:
        return None
    raw = raw.strip()
    return raw if raw.startswith("CVSS:") else None


def build_payload(template: MarkdownTemplate, args: argparse.Namespace) -> dict[str, Any]:
    translations: list[dict[str, Any]] = []
    ordered_translations = sorted(
        template.translations,
        key=lambda t: 0 if t.language == args.main_language else 1,
    )

    for index, translation in enumerate(ordered_translations):
        data: dict[str, Any] = {
            "title": translation.title,
            args.overview_field: translation.overview,
            args.description_field: translation.description,
            args.recommendation_field: translation.recommendation,
            args.reproduction_field: translation.reproduction,
        }

        if args.include_metadata:
            severity = severity_value(translation.severity)
            cvss = cvss_value(translation.cvss_vector)
            if severity:
                data["severity"] = severity
            if cvss:
                data["cvss"] = cvss

        translations.append(
            {
                "language": translation.language,
                "status": args.status,
                "is_main": index == 0,
                "data": data,
            }
        )

    tags = sorted({"web", args.template_set_tag, template.category, *args.tag})
    return {
        "translations": translations,
        "tags": tags,
    }


def main_title(payload: dict[str, Any]) -> str:
    for translation in payload["translations"]:
        if translation.get("is_main"):
            return str(translation["data"]["title"])
    return str(payload["translations"][0]["data"]["title"])


def payload_languages(payload: dict[str, Any]) -> list[str]:
    return [str(translation["language"]) for translation in payload["translations"]]


def iter_template_paths(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def exact_template_match(reptor: Any, title: str) -> Any | None:
    matches = reptor.api.templates.search(title)
    return next(
        (
            item
            for item in matches
            if any(getattr(translation.data, "title", None) == title for translation in item.translations)
        ),
        None,
    )


def write_id_map(results: list[ImportResult], output_path: Path) -> None:
    lines = [
        "status\ttemplate_id\ttitle\tlanguages\tsource_path",
        *[
            "\t".join(
                [
                    result.status,
                    result.template_id or "",
                    result.title,
                    ",".join(result.languages),
                    display_path(result.source_path),
                ]
            )
            for result in results
        ],
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def import_payloads(
    templates: list[MarkdownTemplate],
    payloads: list[dict[str, Any]],
    args: argparse.Namespace,
) -> tuple[int, int, list[ImportResult]]:
    if not args.server or not args.token:
        raise SystemExit("Missing SysReptor connection data. Set REPTOR_SERVER and REPTOR_TOKEN or pass --server and --token.")

    try:
        from reptor import Reptor
        from reptor.models.FindingTemplate import FindingTemplate
    except ImportError as exc:
        raise SystemExit("Missing dependency: install the official SysReptor client with `pip3 install reptor`.") from exc

    reptor = Reptor(server=args.server, token=args.token)
    uploaded = 0
    skipped = 0
    results: list[ImportResult] = []

    for source_template, payload in zip(templates, payloads):
        title = main_title(payload)
        languages = payload_languages(payload)
        template = FindingTemplate(payload)
        existing = exact_template_match(reptor, title)

        if existing and args.update_existing:
            updated = reptor.api.templates.update_template(existing.id, template)
            print(f"UPDATED {title} ({updated.id})")
            uploaded += 1
            results.append(
                ImportResult(
                    status="updated",
                    template_id=updated.id,
                    title=title,
                    languages=languages,
                    source_path=source_template.path,
                )
            )
            continue

        if existing:
            print(f"SKIPPED  {title} ({existing.id})")
            skipped += 1
            results.append(
                ImportResult(
                    status="skipped-existing",
                    template_id=existing.id,
                    title=title,
                    languages=languages,
                    source_path=source_template.path,
                )
            )
            continue

        result = reptor.api.templates.upload_template(template)
        if result:
            print(f"UPLOADED {title} ({result.id})")
            uploaded += 1
            results.append(
                ImportResult(
                    status="uploaded",
                    template_id=result.id,
                    title=title,
                    languages=languages,
                    source_path=source_template.path,
                )
            )
        else:
            print(f"SKIPPED  {title}")
            skipped += 1
            results.append(
                ImportResult(
                    status="skipped",
                    template_id=None,
                    title=title,
                    languages=languages,
                    source_path=source_template.path,
                )
            )

    return uploaded, skipped, results


def main() -> int:
    args = parse_args()
    root = args.templates_dir.resolve()
    if not root.is_dir():
        raise SystemExit(f"Template directory does not exist: {root}")
    if not args.template_set_tag:
        args.template_set_tag = root.name

    paths = iter_template_paths(root)
    if args.limit:
        paths = paths[: args.limit]

    parsed: list[MarkdownTemplate] = []
    errors: list[str] = []
    for path in paths:
        try:
            parsed.append(parse_template(path, root))
        except Exception as exc:  # noqa: BLE001 - include file context for import audits
            errors.append(f"{path}: {exc}")

    if errors:
        print("Parsing failed for one or more templates:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    payloads = [build_payload(template, args) for template in parsed]

    if args.json:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        if args.dry_run:
            return 0

    if args.dry_run:
        for template, payload in zip(parsed, payloads):
            languages = ", ".join(translation["language"] for translation in payload["translations"])
            print(f"DRY-RUN {display_path(template.path)}: {main_title(payload)} [{languages}]")
        print(f"Prepared {len(payloads)} template payload(s).")
        return 0

    uploaded, skipped, results = import_payloads(parsed, payloads, args)
    if not args.no_id_map:
        write_id_map(results, args.id_map_output)
        print(f"Template ID map written to {display_path(args.id_map_output.resolve())}.")
    print(f"Done. Uploaded/updated: {uploaded}. Skipped: {skipped}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
