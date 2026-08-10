#!/usr/bin/env python3
"""Prepare website channel trees (latest, versioned) and redirect aliases.

Canonical version URLs use a period (v4.1, v4.2). /stable/ is a floating
pointer: path-preserving redirects to the current stable version (not a second
content tree). Legacy no-period paths (v41, v42) from the old owasp.org deploy
also get static redirect pages. Data/nav keys stay dot-free (v41, v42) because
Jekyll _data / include names dislike dots.
"""

from __future__ import annotations

import argparse
import io
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WEBSITE = REPO_ROOT / "website"
DOCUMENT = REPO_ROOT / "document"
GENERATE_NAV = Path(__file__).resolve().parent / "generate_nav.py"

# Must match _config.yml stable_version.
CURRENT_STABLE = "v4.2"
STABLE_ALIAS = "stable"

# (disk/url path, data key, nav title, git tag or None for working tree)
CHANNELS = (
    {
        "path": "latest",
        "key": "latest",
        "title": "WSTG Contents",
        "label": "Latest",
        "tag": None,
    },
    {
        "path": "v4.2",
        "key": "v42",
        "title": "WSTG Contents (v4.2)",
        "label": "v4.2",
        "tag": "v4.2",
    },
    {
        "path": "v4.1",
        "key": "v41",
        "title": "WSTG Contents (v4.1)",
        "label": "v4.1",
        "tag": "v4.1",
    },
)

# Alias path → canonical path (path-preserving redirects)
PATH_REDIRECTS = (
    (STABLE_ALIAS, CURRENT_STABLE),
    ("v42", "v4.2"),
    ("v41", "v4.1"),
)

# Old content directory → new directory (within a channel). Applied only when the
# new path exists and the old path does not (working-tree /latest/). Versioned
# tag channels keep historical names (e.g. Frontispiece, "Table of Contents").
# /stable/ follows whatever CURRENT_STABLE points at.
CONTENT_RENAMES = (
    ("1-Frontispiece", "1-About"),
)


def front_matter(key: str, label: str, path: str) -> str:
    return (
        "---\n"
        "layout: document\n"
        f"title: WSTG - {label}\n"
        f"collection_name: {key}\n"
        f"channel_label: {label}\n"
        f"channel_path: {path}\n"
        "render_with_liquid: false\n"
        "---\n\n"
    )


def prepend_front_matter(path: Path, matter: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n") or text.startswith("---\r\n"):
        return
    path.write_text(matter + text, encoding="utf-8")


# Markdown hrefs that should not be rewritten (scheme / fragment-only / protocol-relative).
_SKIP_HREF = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|#|//)", re.IGNORECASE)
_MD_LINK = re.compile(r"\]\(([^)]+)\)")
# Real file assets keep their extension; dotted scenario names (05.1-foo) do not.
_ASSET_EXT = re.compile(
    r"\.(?:png|jpe?g|gif|svg|webp|pdf|html?|css|js)$", re.IGNORECASE
)


def rewrite_site_href(href: str, md_path: Path) -> str:
    """Adapt repo-relative markdown/image hrefs for Jekyll pretty permalinks."""
    href = href.strip()
    if not href:
        return href

    # Same-page anchors: kramdown ids are lowercase.
    if href.startswith("#"):
        return "#" + href[1:].lower()

    if _SKIP_HREF.match(href):
        return href

    frag = ""
    if "#" in href:
        href, frag_raw = href.split("#", 1)
        frag = "#" + frag_raw.lower()

    if href.endswith(".md"):
        href = href[:-3]

    if href == "README" or href.endswith("/README"):
        href = href[: -len("README")] or "./"

    # Leaf pages render as /path/Page/ (one directory deeper than the .md file's
    # folder). Every repo-relative href needs one extra ../ — same-folder
    # siblings (01-foo.md, images/x.png) and existing ../cross/folder links.
    if md_path.name.lower() not in ("readme.md", "index.md"):
        if href.startswith("./"):
            href = href[2:]
        if href and not href.startswith("/"):
            href = "../" + href

    # Pretty permalinks expect a trailing slash on directory-style paths.
    # Do not treat dotted scenario slugs (05.1-foo) as file assets.
    if href and not href.endswith("/") and not _ASSET_EXT.search(href):
        href += "/"

    return href + frag


def rewrite_markdown_file_links(path: Path) -> None:
    """Rewrite ](…) targets outside fenced code blocks."""
    text = path.read_text(encoding="utf-8")
    out: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        def repl(match: re.Match[str]) -> str:
            return "](" + rewrite_site_href(match.group(1), path) + ")"

        out.append(_MD_LINK.sub(repl, line))
    path.write_text("".join(out), encoding="utf-8")


def readme_to_index(root: Path) -> None:
    for readme in root.rglob("README.md"):
        shutil.copy2(readme, readme.with_name("index.md"))


def convert_readmes_to_redirects(channel_root: Path, channel_path: str) -> None:
    """Replace README.md with redirects to the directory index URL."""
    for readme in list(channel_root.rglob("README.md")):
        rel = readme.parent.relative_to(channel_root)
        suffix = "/" if str(rel) == "." else f"/{rel.as_posix()}/"
        write_redirect_page(readme, f"/{channel_path}{suffix}")


def set_root_index_to_foreword(channel_root: Path) -> None:
    foreword = channel_root / "0-Foreword" / "index.md"
    if not foreword.is_file():
        foreword = channel_root / "0-Foreword" / "README.md"
    if not foreword.is_file():
        raise SystemExit(f"Missing Foreword under {channel_root}")
    shutil.copy2(foreword, channel_root / "index.md")


def extract_document_from_tag(tag: str, dest: Path) -> None:
    """Extract document/ from a git tag into dest (contents of document/)."""
    proc = subprocess.run(
        ["git", "archive", "--format=tar", tag, "document"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(proc.stdout), mode="r:") as tar:
        for member in tar.getmembers():
            if not member.name.startswith("document/"):
                continue
            rel = member.name[len("document/") :]
            if not rel:
                continue
            member.name = rel
            tar.extract(member, path=dest)


def copy_working_document(dest: Path) -> None:
    if not DOCUMENT.is_dir():
        raise SystemExit(f"Missing document source: {DOCUMENT}")
    shutil.copytree(
        DOCUMENT,
        dest,
        ignore=shutil.ignore_patterns(".git", ".DS_Store"),
    )


def run_generate_nav(
    *,
    toc: Path,
    title: str,
    key: str,
    url_prefix: str,
    doc_root: Path,
) -> None:
    subprocess.run(
        [
            sys.executable,
            str(GENERATE_NAV),
            str(toc),
            "--title",
            title,
            "--collection",
            key,
            "--url-prefix",
            url_prefix,
            "--doc-root",
            str(doc_root),
            "--yaml-out",
            str(WEBSITE / "_data" / f"{key}.yaml"),
            "--html-out",
            str(WEBSITE / "_includes" / f"nav-tree-{key}.html"),
        ],
        check=True,
    )


def prepare_channel(channel: dict) -> Path:
    path = channel["path"]
    key = channel["key"]
    title = channel["title"]
    label = channel["label"]
    tag = channel["tag"]
    dest = WEBSITE / path

    if dest.exists():
        shutil.rmtree(dest)

    if tag is None:
        copy_working_document(dest)
    else:
        extract_document_from_tag(tag, dest)

    toc = dest / "README.md"
    if not toc.is_file():
        raise SystemExit(f"Missing ToC at {toc}")

    run_generate_nav(
        toc=toc, title=title, key=key, url_prefix=path, doc_root=dest
    )
    readme_to_index(dest)
    for md in dest.rglob("*.md"):
        rewrite_markdown_file_links(md)
    convert_readmes_to_redirects(dest, path)
    set_root_index_to_foreword(dest)
    add_content_renames(dest, path)
    matter = front_matter(key, label, path)
    for md in dest.rglob("*.md"):
        prepend_front_matter(md, matter)

    print(f"Prepared {dest} (key={key}, tag={tag or 'working-tree'})")
    return dest


def write_redirect_page(path: Path, redirect_path: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # redirect_path is site-absolute from baseurl (e.g. /v4.1/0-Foreword/).
    path.write_text(
        "---\n"
        "layout: redirect\n"
        f"redirect_path: {redirect_path}\n"
        "sitemap: false\n"
        "---\n",
        encoding="utf-8",
    )


def add_content_renames(channel_root: Path, channel_path: str) -> None:
    """Redirect renamed content paths when the channel has the new name only."""
    for old, new in CONTENT_RENAMES:
        old_dir = channel_root / old
        new_dir = channel_root / new
        if not new_dir.is_dir() or old_dir.exists():
            continue
        target = f"/{channel_path}/{new}/"
        write_redirect_page(old_dir / "index.md", target)
        write_redirect_page(old_dir / "README.md", target)
        print(f"  redirect /{channel_path}/{old}/ → {target}")


def prepare_path_redirects(canonical_path: str, alias_path: str) -> None:
    """Mirror every page under canonical_path as a redirect under alias_path."""
    canonical = WEBSITE / canonical_path
    if not canonical.is_dir():
        raise SystemExit(
            f"Need /{canonical_path}/ prepared before redirects for /{alias_path}/"
        )
    alias_root = WEBSITE / alias_path
    if alias_root.exists():
        shutil.rmtree(alias_root)

    for md in canonical.rglob("*.md"):
        rel = md.relative_to(canonical)
        # Directory landing pages (index + README alias) → canonical directory URL.
        if rel.name in ("index.md", "README.md"):
            rel_dir = rel.parent
            suffix = "/" if str(rel_dir) == "." else f"/{rel_dir.as_posix()}/"
        else:
            suffix = f"/{rel.with_suffix('').as_posix()}/"
        redirect_path = f"/{canonical_path}{suffix}"
        out = alias_root / rel
        write_redirect_page(out, redirect_path)

    print(f"Prepared redirects {alias_root} → /{canonical_path}/")


def remove_stable_content_artifacts() -> None:
    """Drop generated nav/data from when /stable/ was a full content channel."""
    for path in (
        WEBSITE / "_data" / "stable.yaml",
        WEBSITE / "_includes" / "nav-tree-stable.html",
    ):
        if path.is_file():
            path.unlink()
            print(f"Removed {path.relative_to(WEBSITE)}")


def prepare(channels: list[str] | None = None) -> None:
    wanted = set(channels) if channels else None
    alias_names = {a for a, _ in PATH_REDIRECTS}
    if wanted is not None:
        selected = tuple(
            c for c in CHANNELS if c["path"] in wanted or c["key"] in wanted
        )
        if not selected and not (wanted & alias_names):
            raise SystemExit(f"No matching channels for {channels}")
    else:
        selected = CHANNELS

    for channel in selected:
        prepare_channel(channel)

    prepared_paths = {c["path"] for c in selected}
    for alias, canonical in PATH_REDIRECTS:
        want_alias = wanted is None or alias in wanted or canonical in prepared_paths
        if not want_alias:
            continue
        if not (WEBSITE / canonical).is_dir():
            if wanted is not None and alias in wanted:
                raise SystemExit(
                    f"Need /{canonical}/ prepared before redirects for /{alias}/"
                )
            continue
        prepare_path_redirects(canonical, alias)

    remove_stable_content_artifacts()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "channels",
        nargs="*",
        help="Optional subset (latest, v4.1, v4.2, stable). Default: all.",
    )
    args = parser.parse_args()
    prepare(args.channels or None)


if __name__ == "__main__":
    main()
