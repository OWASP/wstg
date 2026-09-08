#!/usr/bin/env python3
"""Build a manifest of heading ids from Pandoc's real AST.

Runs pandoc -t json on every chapter file, extracts heading identifiers
and their text, and outputs a JSON manifest mapping:
  {file-relative-to-root} -> {heading-slug -> pandoc-id}

This lets links.lua resolve cross-chapter links against ground truth instead
of guessing via regex, eliminating the "filename must match heading" brittle
assumption.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def slugify(text: str) -> str:
    """Match links.lua's slugify exactly."""
    text = text.lower()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^\w-]", "", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def extract_headings_from_json(json_data: dict) -> dict[str, str]:
    """Extract heading id -> heading text from pandoc JSON AST.

    Returns: {slug-of-heading-text -> pandoc-assigned-id}
    """
    headings = {}

    def walk(blocks):
        if not blocks:
            return
        for block in blocks:
            if not isinstance(block, dict):
                continue

            if block.get("t") == "Header":
                c = block.get("c", [])
                if len(c) >= 3:
                    content = c[1]  # inline content
                    heading_id = c[2]  # attributes [id, classes, kvpairs]

                    if content and isinstance(heading_id, list) and len(heading_id) > 0:
                        heading_id = heading_id[0]  # extract id string
                        text_parts = []

                        def extract_text(items):
                            for item in items:
                                if isinstance(item, dict):
                                    if item.get("t") == "Str":
                                        text_parts.append(item.get("c", ""))
                                    elif item.get("t") in ("Emph", "Strong", "Code"):
                                        extract_text(item.get("c", []))
                                    elif item.get("t") == "Link":
                                        c = item.get("c", [])
                                        if len(c) >= 2:
                                            extract_text(c[1])

                        extract_text(content)
                        if text_parts:
                            text = " ".join(text_parts)
                            slug = slugify(text)
                            if heading_id:
                                headings[slug] = heading_id

            # Recurse into nested structures
            for key, val in block.items():
                if key == "c" and isinstance(val, list):
                    # Only recurse on dict elements (blocks/inline content)
                    walk([v for v in val if isinstance(v, dict)])

    walk(json_data.get("blocks", []))
    return headings


def build_manifest(root: str, output: str) -> None:
    """Walk all .md files in root, extract headings, write manifest."""
    root = os.path.abspath(root)
    manifest: dict[str, dict[str, str]] = {}

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames.sort()
        for filename in sorted(filenames):
            if not filename.lower().endswith(".md"):
                continue

            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root)

            try:
                result = subprocess.run(
                    ["pandoc", "-t", "json", full_path],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                json_data = json.loads(result.stdout)
                headings = extract_headings_from_json(json_data)
                if headings:
                    manifest[rel_path] = headings
            except subprocess.CalledProcessError as e:
                print(f"warning: pandoc failed on {rel_path}: {e}", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"warning: invalid json from pandoc on {rel_path}: {e}", file=sys.stderr)

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote manifest to {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default="document",
        help="Root directory to scan for .md files",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="build-ebooks/link-manifest.json",
        help="Output manifest file",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"error: not a directory: {args.root}", file=sys.stderr)
        sys.exit(1)

    build_manifest(args.root, args.output)


if __name__ == "__main__":
    main()
