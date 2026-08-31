#!/usr/bin/env python3
"""Post-process Pandoc Typst body for inclusion under --root ."""
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

    defs = Path(args.defs).read_text(encoding="utf-8")
    Path(args.out).write_text(defs + "\n" + text, encoding="utf-8")


if __name__ == "__main__":
    main()
