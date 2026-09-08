#!/usr/bin/env python3
"""Post-process Pandoc Typst output to apply ebook-specific style conversions.

Transforms Pandoc's raw Typst markup for use in the WSTG ebook:
  - Fixes image paths to point to extracted media directory
  - Escapes backslashes in Windows paths
  - Converts ID table syntax to styled blue badge blocks
  - Prepends Pandoc definitions (fonts, utilities)

Outputs the final content.typ ready for inclusion in main.typ.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("body")
    p.add_argument("defs")
    p.add_argument("out")
    p.add_argument("--media-prefix", default="/build-ebooks/media/")
    args = p.parse_args()

    text = Path(args.body).read_text(encoding="utf-8")

    def esc_slash(m: re.Match[str]) -> str:
        indent, rest = m.group(1), m.group(2)
        if rest.startswith("/"):
            return m.group(0)  # // comment
        return f"{indent}\\/{rest}"

    text = re.sub(r"(?m)^([ \t]*)/(.*)$", esc_slash, text)

    # extract-media paths → root-absolute
    text = text.replace('#image("build-ebooks/media/', f'#image("{args.media_prefix}')
    text = text.replace('#image("media/', f'#image("{args.media_prefix}')

    # Convert ID tables to styled badges
    # Matches: #align(center)[#table(...[ID]...[WSTG-…]...)]
    def replace_id_table(m: re.Match[str]) -> str:
        id_val = m.group(1)
        return f'''#block(
  fill: rgb("#0080BD"),
  stroke: none,
  radius: 4pt,
  inset: (x: 12pt, y: 8pt),
  width: auto,
)[
  #set text(fill: white, weight: "medium")
  ID #h(1.5em) {id_val}
]'''

    text = re.sub(
        r'#align\(center\)\[#table\([^[]*\[ID\][^[]*\[(WSTG-[^\]]+)\][^]]*\)\s*\]',
        replace_id_table,
        text,
        flags=re.DOTALL,
    )

    defs = Path(args.defs).read_text(encoding="utf-8")
    Path(args.out).write_text(defs + "\n" + text, encoding="utf-8")


if __name__ == "__main__":
    main()
