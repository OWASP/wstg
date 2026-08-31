#!/usr/bin/env python3
"""Emit Markdown chapter paths under a tree in reading order.

Directories are sorted by name (WSTG numeric prefixes already sort correctly).

README.md files are excluded because they generally contain navigation or
contents lists that would duplicate material in generated ebooks.

The exception is 1-About/README.md, which contains substantive introductory
content and must be included.

No content is modified — paths only.
"""

from __future__ import annotations

import argparse
import os
import sys


PRESERVED_READMES = {
    os.path.normpath(os.path.join("1-About", "README.md")),
}


def list_chapters(root: str) -> list[str]:
    root = os.path.abspath(root)
    results: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames.sort()

        md_files: list[str] = []

        for filename in sorted(filenames):
            if not filename.lower().endswith(".md"):
                continue

            full_path = os.path.join(dirpath, filename)
            relative_path = os.path.normpath(os.path.relpath(full_path, root))

            if (
                filename.lower() == "readme.md"
                and relative_path not in PRESERVED_READMES
            ):
                continue

            md_files.append(filename)

        for name in md_files:
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
