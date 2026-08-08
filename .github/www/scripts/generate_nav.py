#!/usr/bin/env python3
"""Generate nested WSTG sidebar YAML (and optional slim chapter ToC) from document/README.md."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TOC_ENTRY = re.compile(
    r"^(#{2,5})\s+(?:([0-9.]+|[A-Za-z][A-Za-z0-9. ]*?)\s+)?\[(.*?)\]\((.*?)\)\s*$"
)


def normalize_url(url: str) -> str:
    """Match legacy deploy sed: lowercase fragments, strip .md extension."""
    if ".md#" in url:
        path, frag = url.split(".md#", 1)
        return f"{path}#{frag.lower()}"
    if url.endswith(".md"):
        return url[:-3]
    return url.replace(".md", "")


def parse_toc(text: str) -> list[dict]:
    """Parse markdown ToC headings into a nested list of {title, url, children?}."""
    roots: list[dict] = []
    stack: list[tuple[int, list]] = [(1, roots)]

    for line in text.splitlines():
        match = TOC_ENTRY.match(line)
        if not match:
            continue
        hashes, number, label, raw_url = match.groups()
        level = len(hashes)
        title = f"{number} {label}".strip() if number else label
        node: dict = {"title": title, "url": normalize_url(raw_url)}

        while stack and stack[-1][0] >= level:
            stack.pop()
        if not stack:
            stack = [(1, roots)]
        stack[-1][1].append(node)
        children: list[dict] = []
        node["children"] = children
        stack.append((level, children))

    def drop_empty_children(nodes: list[dict]) -> None:
        for node in nodes:
            kids = node.get("children") or []
            if kids:
                drop_empty_children(kids)
            else:
                node.pop("children", None)

    drop_empty_children(roots)
    return roots


def yaml_escape(value: str) -> str:
    return value.replace("'", "''")


def emit_yaml_nodes(nodes: list[dict], indent: int = 0) -> list[str]:
    lines: list[str] = []
    pad = "  " * indent
    child_pad = "  " * (indent + 1)
    for node in nodes:
        lines.append(f"{pad}- title: '{yaml_escape(node['title'])}'")
        lines.append(f"{child_pad}url: {node['url']}")
        children = node.get("children") or []
        if children:
            lines.append(f"{child_pad}children:")
            lines.extend(emit_yaml_nodes(children, indent + 2))
    return lines


def generate_yaml(title: str, nodes: list[dict]) -> str:
    body = "\n".join(emit_yaml_nodes(nodes))
    return f"docs_list_title: {title}\ndocs:\n\n{body}\n"


def chapter_toc_markdown(nodes: list[dict]) -> str:
    """Chapter-level ToC for the web landing page (detail lives in the sidebar)."""
    lines = [
        "# Table of Contents",
        "",
        "Use the **WSTG Contents** menu on the right to browse sections and tests. "
        "Chapter landing pages are linked below.",
        "",
    ]
    for node in nodes:
        # Reconstruct a relative markdown link from the nav url.
        url = node["url"]
        if "#" in url:
            path, frag = url.split("#", 1)
            link = f"{path}.md#{frag}" if path else f"#{frag}"
        elif url.endswith("/"):
            link = url
        else:
            link = f"{url}.md"
        # Titles already include the section number when present.
        lines.append(f"## [{node['title']}]({link})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", type=Path, help="Path to document/README.md")
    parser.add_argument(
        "--title",
        required=True,
        help="docs_list_title value (from prepend.nav, without key)",
    )
    parser.add_argument(
        "--yaml-out",
        type=Path,
        required=True,
        help="Output path for nested navigation YAML",
    )
    parser.add_argument(
        "--chapter-toc-out",
        type=Path,
        help="Optional slim chapter-only ToC markdown output",
    )
    args = parser.parse_args()

    text = args.readme.read_text(encoding="utf-8")
    nodes = parse_toc(text)
    if not nodes:
        raise SystemExit(f"No ToC entries parsed from {args.readme}")

    args.yaml_out.parent.mkdir(parents=True, exist_ok=True)
    args.yaml_out.write_text(generate_yaml(args.title, nodes), encoding="utf-8")

    if args.chapter_toc_out is not None:
        args.chapter_toc_out.parent.mkdir(parents=True, exist_ok=True)
        args.chapter_toc_out.write_text(chapter_toc_markdown(nodes), encoding="utf-8")


if __name__ == "__main__":
    main()
