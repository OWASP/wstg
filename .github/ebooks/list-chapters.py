#!/usr/bin/env python3
"""Emit Markdown chapter paths in reading order with synthetic chapter headings.

Walks the document tree (sorted by directory name), identifies nav-only READMEs,
and generates synthetic chapter headings for them.

A README.md is treated as "nav-only" if every non-blank, non-heading line is
just an optionally numbered/bulleted Markdown link (i.e., it's a table of
contents for that folder, not prose content). Its content is dropped, and
a synthetic H1 heading is generated instead from the folder name.

Synthetic headings:
  - Are marked with {.synthetic} class for filter identification
  - Use folder-based IDs: "3-Web_App_Testing" → H1 {.synthetic #web-app-testing}
  - Support numbered chapters (0-6) and lettered appendices (A-F)
  - Preserve chapter numbers/letters in display: "3. Web Application Testing"

Real prose README.md files (e.g. 0-Foreword, 1-About, 2-Introduction) are
kept as ordinary content files and processed normally.

Output is paths to all markdown files (synthetic + content) in reading order.
Source files are never modified; synthetic headings are written to --synthetic-dir.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

LINK_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")
LIST_MARKER_RE = re.compile(r"^[-*]\s+")
NUMBERING_RE = re.compile(r"^(?:Appendix\s+[A-Za-z]\.?|\d+(?:\.\d+)*\.?)\s*")
DIR_NUMBER_RE = re.compile(r"^(\d+)[.\-]")


def _is_nav_line(line: str) -> bool:
    line = line.strip()
    if not line or line.startswith("#"):
        return True
    line = LIST_MARKER_RE.sub("", line)
    line = NUMBERING_RE.sub("", line)
    line = LINK_RE.sub("", line)
    return line.strip() == ""


def is_nav_readme(path: str) -> bool:
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    return bool(lines) and all(_is_nav_line(line) for line in lines)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^\w-]", "", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def synthesize_heading(dirpath: str, root: str) -> tuple[str, str]:
    """Return (display title, anchor id) for a directory's chapter heading.

    The id is derived the same way links.lua derives a link target from a
    folder name (numbering stripped, then slugified) so it always matches.
    The display title preserves chapter numbers (0-6) and appendix letters
    (A-F) for clarity in the outline.
    """
    name = os.path.basename(dirpath)
    num_match = DIR_NUMBER_RE.match(name)
    letter_match = re.match(r"^([A-F])-", name)
    chapter_num = int(num_match.group(1)) if num_match else None
    chapter_letter = letter_match.group(1) if letter_match else None

    base = re.sub(r"^[\d.]+-", "", name)
    base = re.sub(r"^[A-Za-z]-", "", base)
    plain_title = base.replace("_", " ")
    anchor_id = slugify(plain_title)

    display_title = plain_title
    depth = len(os.path.relpath(dirpath, root).split(os.sep))

    if depth == 1:
        if chapter_num is not None:
            # All numbered chapters: "4-Web_Application_Security_Testing" → "4. Web Application Security Testing"
            display_title = f"{chapter_num}. {plain_title}"
        elif chapter_letter is not None:
            # Appendices: "A-History" → "A. History"
            display_title = f"{chapter_letter}. {plain_title}"
    elif depth == 2:
        # Subsection: preserve "4.0 Introduction and Objectives"
        parent_match = DIR_NUMBER_RE.match(os.path.basename(os.path.dirname(dirpath)))
        own_match = DIR_NUMBER_RE.match(name)
        if parent_match and own_match:
            display_title = f"{int(parent_match.group(1))}.{int(own_match.group(1))} {plain_title}"

    return display_title, anchor_id


def list_chapters(root: str, synthetic_dir: str) -> list[str]:
    root = os.path.abspath(root)
    results: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames.sort()

        content_files: list[str] = []
        nav_readme = False

        for filename in sorted(filenames):
            if not filename.lower().endswith(".md"):
                continue

            full_path = os.path.join(dirpath, filename)

            if filename.lower() == "readme.md" and is_nav_readme(full_path):
                nav_readme = True
                continue

            content_files.append(filename)

        if nav_readme and dirpath != root:
            title, anchor_id = synthesize_heading(dirpath, root)
            rel_dir = os.path.relpath(dirpath, root)
            synth_path = os.path.join(synthetic_dir, rel_dir + ".md")
            os.makedirs(os.path.dirname(synth_path), exist_ok=True)
            # All synthetic headings as L1 (for pagebreaks)
            # Document headings will be demoted, so this gives proper hierarchy
            # Mark with .synthetic class so the demote filter can identify and skip them
            with open(synth_path, "w", encoding="utf-8") as f:
                f.write(f"# {title} {{.synthetic #{anchor_id}}}\n")
            results.append(synth_path)

        for name in content_files:
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
    parser.add_argument(
        "--synthetic-dir",
        default="build-ebooks/synthetic",
        help="Where to write synthesized chapter headings",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"error: not a directory: {args.root}", file=sys.stderr)
        sys.exit(1)

    for path in list_chapters(args.root, args.synthetic_dir):
        print(path)


if __name__ == "__main__":
    main()
