#!/usr/bin/env python3
"""Emit Markdown paths under a tree in reading order.

Directories are sorted by name (WSTG numeric prefixes already sort correctly).
Within each directory, README.md is first; other *.md files follow sorted.
No content is modified — paths only.
"""

from __future__ import annotations

import argparse
import os
import sys


def list_chapters(root: str) -> list[str]:
    root = os.path.abspath(root)
    results: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames.sort()
        md_files = sorted(f for f in filenames if f.lower().endswith(".md"))
        if not md_files:
            continue
        readmes = [f for f in md_files if f.lower() == "readme.md"]
        others = [f for f in md_files if f.lower() != "readme.md"]
        for name in readmes + others:
            results.append(os.path.join(dirpath, name))

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default="document",
        help="Root directory to walk (default: document)",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"error: not a directory: {args.root}", file=sys.stderr)
        sys.exit(1)

    for path in list_chapters(args.root):
        print(path)


if __name__ == "__main__":
    main()