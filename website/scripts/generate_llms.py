#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt for LLM agent discovery.

Creates two files:
- llms.txt: Structured guide to WSTG content with metadata
- llms-full.txt: Complete markdown concatenation for offline use
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WEBSITE = Path(__file__).resolve().parents[1]
CHANNELS = {
    "latest": {
        "label": "Latest",
        "url_prefix": "https://wstg.owasp.org/latest",
        "md_prefix": "https://wstg.owasp.org/md/latest",
        "description": "Latest development version",
    },
    "v4.2": {
        "label": "v4.2 (Stable)",
        "url_prefix": "https://wstg.owasp.org/v4.2",
        "md_prefix": "https://wstg.owasp.org/md/v4.2",
        "description": "Current stable release",
    },
    "v4.1": {
        "label": "v4.1 (Archived)",
        "url_prefix": "https://wstg.owasp.org/v4.1",
        "md_prefix": "https://wstg.owasp.org/md/v4.1",
        "description": "Previous release (archived)",
    },
}

# Map README-style sections to meaningful category names
SECTION_NAMES = {
    "0-Foreword": "Foreword & Introduction",
    "1-About": "About WSTG",
    "2-Introduction": "Introduction",
    "3-The_OWASP_Testing_Framework": "Testing Framework",
    "4-Web_Application_Security_Testing": "Web Application Testing",
}


def get_section_title(path: Path) -> str:
    """Extract first H1 from markdown file."""
    try:
        text = path.read_text(encoding="utf-8")
        # Skip front matter
        if text.startswith("---"):
            _, _, rest = text.split("---", 2)
            text = rest
        # Find first H1
        for line in text.split("\n"):
            if line.startswith("# "):
                return line[2:].strip()
    except Exception:
        pass
    return path.stem.replace("_", " ")


def gather_content_tree(channel_key: str) -> dict:
    """Scan channel directory and build content structure."""
    channel_dir = WEBSITE / channel_key
    if not channel_dir.is_dir():
        return {}

    tree = {}
    for section_dir in sorted(channel_dir.iterdir()):
        if not section_dir.is_dir() or section_dir.name.startswith("_"):
            continue

        section_name = SECTION_NAMES.get(section_dir.name, section_dir.name.replace("_", " "))
        docs = []

        for md_file in sorted(section_dir.rglob("*.md")):
            # Skip README and index files at section root
            if md_file.name in ("README.md", "index.md") and md_file.parent == section_dir:
                continue

            rel_path = md_file.relative_to(section_dir)
            title = get_section_title(md_file)

            # Skip front matter from path for URL
            url_path = str(rel_path.with_suffix("")).replace("README", "")
            if url_path.endswith("/"):
                url_path = url_path[:-1]

            docs.append({
                "title": title,
                "url": f"{url_path}/",
                "path": str(rel_path),
            })

        if docs:
            tree[section_name] = docs

    return tree


def generate_llms_txt() -> str:
    """Generate main llms.txt discovery file."""
    lines = [
        "# OWASP Web Security Testing Guide",
        "",
        "> Comprehensive testing resource for web application security",
        "",
    ]

    for channel_key, channel_info in CHANNELS.items():
        lines.append(f"## {channel_info['label']}")
        lines.append("")
        lines.append(f"{channel_info['description']}")
        lines.append("")

        tree = gather_content_tree(channel_key)
        if not tree:
            continue

        lines.append(f"- [Interactive Guide]({channel_info['url_prefix']}/)")
        lines.append(f"- [Markdown Version]({channel_info['md_prefix']}/README.md)")
        lines.append("")

        for section_name, docs in sorted(tree.items()):
            lines.append(f"### {section_name}")
            lines.append("")
            for doc in docs[:10]:  # Limit to first 10 per section in summary
                url = f"{channel_info['md_prefix']}/{doc['path']}".replace("README.md", "").replace(".md", ".txt")
                lines.append(f"- [{doc['title']}]({url})")
            if len(docs) > 10:
                lines.append(f"- ... and {len(docs) - 10} more")
            lines.append("")

    lines.append("## Resources")
    lines.append("")
    lines.append("- [GitHub Repository](https://github.com/OWASP/wstg)")
    lines.append("- [Contribution Guide](https://github.com/OWASP/wstg/blob/master/CONTRIBUTING.md)")
    lines.append("- [Code of Conduct](https://github.com/OWASP/wstg/blob/master/CODE_OF_CONDUCT.md)")
    lines.append("")

    return "\n".join(lines)


def generate_llms_full_txt(channel_key: str = "latest") -> str:
    """Generate comprehensive markdown concatenation."""
    channel_dir = WEBSITE / channel_key
    if not channel_dir.is_dir():
        return ""

    lines = [
        f"# OWASP Web Security Testing Guide - {CHANNELS[channel_key]['label']}",
        "",
        "Complete markdown reference for LLM consumption.",
        "",
    ]

    for section_dir in sorted(channel_dir.iterdir()):
        if not section_dir.is_dir() or section_dir.name.startswith("_"):
            continue

        section_name = SECTION_NAMES.get(section_dir.name, section_dir.name.replace("_", " "))
        lines.append(f"## {section_name}")
        lines.append("")

        # Add section index if it exists
        index_file = section_dir / "index.md"
        if not index_file.is_file():
            index_file = section_dir / "README.md"

        if index_file.is_file():
            text = index_file.read_text(encoding="utf-8")
            # Remove front matter
            if text.startswith("---"):
                _, _, text = text.split("---", 2)
            lines.append(text.strip())
            lines.append("")

    # Check size and truncate if needed (target: < 500 KB)
    content = "\n".join(lines)
    if len(content) > 500000:
        # Keep only first N sections
        content = content[:480000] + "\n\n[... content truncated for LLM context size ...]"

    return content


def main() -> None:
    # Generate main llms.txt
    llms_txt = generate_llms_txt()
    llms_path = WEBSITE / "llms.txt"
    llms_path.write_text(llms_txt, encoding="utf-8")
    print(f"Generated {llms_path.relative_to(WEBSITE)}")

    # Generate comprehensive llms-full.txt for latest channel
    llms_full = generate_llms_full_txt("latest")
    if llms_full:
        llms_full_path = WEBSITE / "llms-full.txt"
        llms_full_path.write_text(llms_full, encoding="utf-8")
        print(f"Generated {llms_full_path.relative_to(WEBSITE)}")


if __name__ == "__main__":
    main()
