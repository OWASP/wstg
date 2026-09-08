#!/usr/bin/env python3
"""Copy markdown files to _site for LLM agent access.

Creates text/plain versions of markdown files under /md/ prefix so agents
can access raw markdown without HTML parsing overhead.
"""

from __future__ import annotations

import shutil
from pathlib import Path

WEBSITE = Path(__file__).resolve().parents[1]
SITE = WEBSITE / "_site"
CHANNELS = ("latest", "v4.1", "v4.2")


def copy_channel_markdown(channel: str) -> int:
    """Copy all .md files from a channel to _site/md/{channel}/ as .txt files."""
    source = WEBSITE / channel
    if not source.is_dir():
        return 0

    dest_base = SITE / "md" / channel
    if dest_base.exists():
        shutil.rmtree(dest_base)
    dest_base.mkdir(parents=True, exist_ok=True)

    count = 0
    for md_file in source.rglob("*.md"):
        # Preserve directory structure, rename .md to .txt for text/plain delivery
        rel = md_file.relative_to(source)
        dest = dest_base / rel.with_suffix(".txt")

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(md_file, dest)
        count += 1

    print(f"Copied {count} markdown files to {dest_base.relative_to(SITE)}/ (as .txt)")
    return count


def main() -> None:
    if not SITE.is_dir():
        raise SystemExit(f"Build directory not found: {SITE}")

    total = 0
    for channel in CHANNELS:
        total += copy_channel_markdown(channel)

    print(f"Total: {total} markdown files copied for agent access")


if __name__ == "__main__":
    main()
