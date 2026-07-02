#!/usr/bin/env python3
"""
Generate bilingual SysReptor Markdown templates for the WSTG checklist findings.

The generated files intentionally follow the same Markdown contract as
templates/owasp-top10 so they can be parsed by import_sysreptor_owasp_templates.py:

- German translation first
- English translation second
- Overview, Description, Recommendation and Reproduction sections in both languages
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


DEFAULT_DATA_FILE = Path("wstg_checklist_app/data/wstg_checklist_data.js")
DEFAULT_FINDINGS_FILE = Path("wstg_checklist_app/builder/sysreptor_templates.json")
DEFAULT_OUTPUT_DIR = Path("templates/wstg-checklist")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate SysReptor Markdown templates for all WSTG checklist findings.",
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help=f"Generated checklist data file. Default: {DEFAULT_DATA_FILE}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to write templates to. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--findings-file",
        type=Path,
        default=DEFAULT_FINDINGS_FILE,
        help=f"Checklist finding template source. Default: {DEFAULT_FINDINGS_FILE}",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove existing generated Markdown files in the output directory before writing.",
    )
    return parser.parse_args()


def load_wstg_data(path: Path) -> dict[str, dict[str, Any]]:
    source = path.read_text(encoding="utf-8")
    match = re.search(r"const\s+wstgData\s*=\s*(?P<data>\[.*\]);\s*$", source, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Could not parse checklist data from {path}")
    data = json.loads(match.group("data"))
    return {module["id"]: module for module in data if "id" in module}


def load_findings(path: Path, modules: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    source = json.loads(path.read_text(encoding="utf-8"))
    findings: list[dict[str, Any]] = []

    module_order = {module_id: index for index, module_id in enumerate(modules)}
    sorted_items = sorted(
        source.items(),
        key=lambda item: (module_order.get(parent_module_id(item[0]), module_order.get(item[0], 9999)), item[0]),
    )

    for module_id, module_findings in sorted_items:
        module = modules.get(module_id) or modules.get(parent_module_id(module_id)) or fallback_module(module_id)
        for finding in module_findings:
            findings.append(
                {
                    **finding,
                    "module_id": module_id,
                    "module": module,
                }
            )
    return findings


def parent_module_id(module_id: str) -> str:
    return module_id.split(".", 1)[0]


def fallback_module(module_id: str) -> dict[str, Any]:
    return {
        "id": module_id,
        "title": module_id,
        "title_de": module_id,
        "category": "Uncategorized",
        "category_de": "Nicht kategorisiert",
        "category_index": 99,
        "goal": "",
        "goal_de": "",
        "expected_evidence": "",
        "expected_evidence_de": "",
    }


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-") or "template"


def category_dir(module: dict[str, Any]) -> str:
    index = int(module.get("category_index") or 99)
    return f"{index:02d}-{slugify(str(module.get('category') or 'uncategorized'))}"


def clean_markdown(value: str | None) -> str:
    if not value:
        return ""
    text = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text or text.lower().startswith(("no description available", "no summary provided", "no methodology defined")):
        return ""

    # Keep imported sections intact by demoting source headings below level two.
    text = re.sub(r"^(#{1,2})\s+", "### ", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def compact_markdown(value: str | None, *, max_chars: int = 1200, max_blocks: int = 3) -> str:
    text = clean_markdown(value)
    if not text:
        return ""

    blocks: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block or block.startswith("!["):
            continue
        candidate = "\n\n".join([*blocks, block])
        if blocks and len(candidate) > max_chars:
            break
        blocks.append(block)
        if len("\n\n".join(blocks)) >= max_chars or len(blocks) >= max_blocks:
            break

    result = "\n\n".join(blocks).strip()
    if len(result) > max_chars:
        sentence_cutoffs = [
            result.rfind(". ", 0, max_chars - 1),
            result.rfind("! ", 0, max_chars - 1),
            result.rfind("? ", 0, max_chars - 1),
        ]
        cutoff = max(sentence_cutoffs)
        if cutoff < 200:
            cutoff = result.rfind(" ", 0, max_chars - 1)
        result = result[: cutoff + 1 if cutoff > 200 else max_chars].rstrip(" .,;:")
        result += "."
    return result


def field(source: dict[str, Any], key: str, fallback: str = "") -> str:
    value = source.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def bullet_list(markdown: str) -> str:
    text = clean_markdown(markdown)
    if not text:
        return "- [TODO: Ergänzen]"
    return text


def german_template(finding: dict[str, Any]) -> str:
    module = finding["module"]
    title = field(finding, "title_de", field(finding, "title_en"))
    description = compact_markdown(
        field(finding, "description_de", field(finding, "description_en")),
        max_chars=1000,
        max_blocks=2,
    )
    consequences = compact_markdown(
        field(finding, "consequences_de", field(finding, "consequences_en")),
        max_chars=650,
        max_blocks=2,
    )
    recommendation = compact_markdown(module.get("reporting_hints_de"), max_chars=900, max_blocks=2)
    if not recommendation or recommendation.lower().startswith(("dokumentieren", "document")):
        recommendation = (
            "Es wird empfohlen, die Ursache der Schwachstelle serverseitig zu beheben, "
            "betroffene Eingaben, Berechtigungen und Konfigurationen robust abzusichern "
            "und die Wirksamkeit der Maßnahmen anschließend erneut zu prüfen."
        )

    goal = bullet_list(field(module, "goal_de", field(module, "goal")))
    evidence = compact_markdown(
        field(module, "expected_evidence_de", field(module, "expected_evidence")),
        max_chars=700,
        max_blocks=2,
    )
    module_title = field(module, "title_de", field(module, "title", finding["module_id"]))

    return f"""# {title}

| Schweregrad | [TODO: Schweregrad] |
| ----------- | ---- |
| CVSS Rating | [TODO: CVSS Rating] |
| CVSS Vektor | [TODO: CVSS Vektor] |
| Komponente  | Web Application |
| WSTG-ID     | {finding["module_id"]} |
| Finding-ID  | {finding["id"]} |

## Übersicht

Während der Sicherheitsüberprüfung wurde **{title}** identifiziert.

{description or "Die Feststellung betrifft eine sicherheitsrelevante Eigenschaft der getesteten Webanwendung."}

**Betroffene Ressource**

- **URL / Endpunkt:** `[TODO: URL / Endpunkt]`
- **HTTP-Methode:** `[TODO: GET / POST / PUT / ...]`
- **Parameter / Header:** `[TODO: Parameter / Header]`
- **Nachweis:** `[TODO: Screenshot / HTTP Request]`

---

## Beschreibung

{description or "Die Schwachstelle wurde im Rahmen der WSTG-Prüfung festgestellt."}

**Mögliche Auswirkungen**

{consequences or "Die Auswirkung hängt von der betroffenen Funktion, den vorhandenen Berechtigungen und den bereits implementierten Schutzmaßnahmen ab."}

**WSTG-Prüfbereich**

{module_title}

**Prüfziel des Moduls**

{goal}

---

## Empfehlung

{recommendation}

---

## Reproduktion

1. Die betroffene Funktion oder Schnittstelle identifizieren.
2. Die Eingaben, Berechtigungen, Zustände oder Konfigurationen gemäß dem WSTG-Prüfziel variieren.
3. Die Serverantworten und das Verhalten der Anwendung dokumentieren.
4. Den sicherheitsrelevanten Nachweis mit HTTP-Anfragen, Antworten und Screenshots belegen.

**Erwartete Nachweise**

{evidence or "[TODO: Nachweis ergänzen]"}

**Beispiel Request**

```http
[TODO: HTTP Request]
```
"""


def english_template(finding: dict[str, Any]) -> str:
    module = finding["module"]
    title = field(finding, "title_en", field(finding, "title_de"))
    description = compact_markdown(
        field(finding, "description_en", field(finding, "description_de")),
        max_chars=1000,
        max_blocks=2,
    )
    consequences = compact_markdown(
        field(finding, "consequences_en", field(finding, "consequences_de")),
        max_chars=650,
        max_blocks=2,
    )
    recommendation = compact_markdown(module.get("reporting_hints"), max_chars=900, max_blocks=2)
    if not recommendation or recommendation.lower().startswith(("document", "dokumentieren")):
        recommendation = (
            "It is recommended to remediate the root cause server-side, harden affected "
            "inputs, permissions, and configuration, and retest the control after remediation."
        )

    goal = bullet_list(field(module, "goal"))
    evidence = compact_markdown(module.get("expected_evidence"), max_chars=700, max_blocks=2)
    module_title = field(module, "title", finding["module_id"])

    return f"""# {title}

| Severity    | [TODO: Severity] |
| ----------- | ---- |
| CVSS Rating | [TODO: CVSS Rating] |
| CVSS Vector | [TODO: CVSS Vector] |
| Component   | Web Application |
| WSTG-ID     | {finding["module_id"]} |
| Finding-ID  | {finding["id"]} |

## Overview

During the security assessment, **{title}** was identified.

{description or "The finding concerns a security-relevant property of the tested web application."}

**Affected Resource**

- **URL / Endpoint:** `[TODO: URL / Endpoint]`
- **HTTP Method:** `[TODO: GET / POST / PUT / ...]`
- **Parameter / Header:** `[TODO: Parameter / Header]`
- **Evidence:** `[TODO: Screenshot / HTTP Request]`

---

## Description

{description or "The weakness was identified as part of the WSTG assessment."}

**Potential Impact**

{consequences or "The actual impact depends on the affected function, available privileges, and security controls already implemented."}

**WSTG Test Area**

{module_title}

**Module Test Objective**

{goal}

---

## Recommendation

{recommendation}

---

## Reproduction

1. Identify the affected function or interface.
2. Vary inputs, permissions, states, or configuration according to the WSTG test objective.
3. Document the server responses and the observed application behavior.
4. Support the security impact with HTTP requests, responses, and screenshots.

**Expected Evidence**

{evidence or "[TODO: Add evidence]"}

**Example Request**

```http
[TODO: HTTP Request]
```
"""


def render_template(finding: dict[str, Any]) -> str:
    return f"{german_template(finding).rstrip()}\n\n---\n\n{english_template(finding).rstrip()}\n"


def clean_output_dir(output_dir: Path) -> None:
    if not output_dir.exists():
        return
    for path in output_dir.rglob("*.md"):
        path.unlink()
    for path in sorted((p for p in output_dir.rglob("*") if p.is_dir()), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass


def write_templates(findings: list[dict[str, Any]], output_dir: Path) -> list[Path]:
    written: list[Path] = []
    for finding in findings:
        module = finding["module"]
        directory = output_dir / category_dir(module)
        title = field(finding, "title_en", field(finding, "title_de"))
        filename = f"{slugify(str(finding['id']))}-{slugify(title)}.md"
        path = directory / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_template(finding), encoding="utf-8")
        written.append(path)
    return written


def main() -> int:
    args = parse_args()
    modules = load_wstg_data(args.data_file)
    findings = load_findings(args.findings_file, modules)
    if not args.no_clean:
        clean_output_dir(args.output_dir)
    written = write_templates(findings, args.output_dir)
    print(f"Wrote {len(written)} WSTG checklist finding template(s) to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
