#!/usr/bin/env python3
"""Generate nested WSTG sidebar YAML/HTML (and optional slim chapter ToC) from document/README.md."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

TOC_ENTRY = re.compile(
    r"^(#{2,5})\s+(?:([0-9.]+|[A-Za-z][A-Za-z0-9. ]*?)\s+)?\[(.*?)\]\((.*?)\)\s*$"
)
WSTG_ID_RE = re.compile(r"WSTG-[A-Z]+-\d+", re.IGNORECASE)

# Title substring/regex → filter aliases (A). Applied case-insensitively to titles.
TITLE_HINT_RULES: list[tuple[re.Pattern[str], list[str]]] = [
    (re.compile(r"cross[\s-]*site[\s-]*scripting"), ["xss"]),
    (re.compile(r"dom[\s-]*based"), ["dom xss", "domxss"]),
    (re.compile(r"sql[\s-]*injection"), ["sqli"]),
    (re.compile(r"no[\s-]*sql"), ["nosqli"]),
    (re.compile(r"ldap[\s-]*injection"), ["ldapi"]),
    # XML family: titles say "XML Injection" / "XPath Injection", not XXE.
    (re.compile(r"xml[\s-]*injection"), ["xxe", "xmli", "xml injection"]),
    (re.compile(r"xpath"), ["xpathi", "xml"]),
    (re.compile(r"ssi[\s-]*injection|server[\s-]*side[\s-]*include"), ["ssi injection"]),
    (re.compile(r"cross[\s-]*site[\s-]*request[\s-]*forgery"), ["csrf", "xsrf"]),
    (re.compile(r"server[\s-]*side[\s-]*request[\s-]*forgery"), ["ssrf"]),
    (re.compile(r"server[\s-]*side[\s-]*template[\s-]*injection"), ["ssti"]),
    (re.compile(r"client[\s-]*side[\s-]*template[\s-]*injection"), ["csti"]),
    (re.compile(r"multi[\s-]*factor[\s-]*authentication"), ["mfa", "2fa", "totp"]),
    (re.compile(r"broken[\s-]*object[\s-]*level[\s-]*authorization"), ["bola", "idor"]),
    (re.compile(r"broken[\s-]*function[\s-]*level[\s-]*authorization"), ["bfla"]),
    (re.compile(r"transport[\s-]*layer[\s-]*security"), ["tls", "ssl", "https"]),
    (re.compile(r"encrypted[\s-]*channel"), ["tls", "ssl", "https"]),
    (re.compile(r"unencrypted[\s-]*channel"), ["tls", "ssl", "https", "cleartext"]),
    (re.compile(r"response[\s-]*splitting"), ["crlf", "response splitting"]),
    (re.compile(r"\bcookie"), ["cookies", "set-cookie", "httponly", "samesite", "secure flag"]),
    (re.compile(r"cloud[\s-]*storage"), ["s3", "bucket", "blob storage"]),
    (re.compile(r"directory[\s-]*traversal"), ["path traversal", "dotdot", "lfi"]),
    (re.compile(r"sql[\s-]*server"), ["mssql", "sql server"]),
    (re.compile(r"ria[\s-]*cross[\s-]*domain|cross[\s-]*domain[\s-]*policy"), ["crossdomain.xml", "clientaccesspolicy"]),
    (re.compile(r"web[\s-]*messaging"), ["postmessage", "post message"]),
    (re.compile(r"reverse[\s-]*tabnabbing"), ["tabnabbing", "window.opener"]),
    (re.compile(r"clickjacking"), ["ui redress", "ui redressing", "x-frame-options", "framing"]),
    (re.compile(r"process[\s-]*timing"), ["race condition", "toctou"]),
    (re.compile(r"metafiles"), ["robots", "robots.txt", "sitemap", "sitemap.xml"]),
    (re.compile(r"lock[\s-]*out"), ["rate limit", "bruteforce", "brute force", "account lockout"]),
    (re.compile(r"number[\s-]*of[\s-]*times[\s-]*a[\s-]*function|function[\s-]*can[\s-]*be[\s-]*used"), ["rate limit", "bruteforce", "brute force"]),
    (re.compile(r"content[\s-]*security[\s-]*policy"), ["csp", "headers"]),
    (re.compile(r"http[\s-]*strict[\s-]*transport[\s-]*security"), ["hsts", "headers"]),
    (re.compile(r"json[\s-]*web[\s-]*token"), ["jwt"]),
    (re.compile(r"cross[\s-]*origin[\s-]*resource[\s-]*sharing"), ["cors", "headers"]),
    (re.compile(r"security[\s-]*header"), ["headers"]),
    (re.compile(r"cross[\s-]*site[\s-]*script[\s-]*inclusion"), ["xssi"]),
    (re.compile(r"file[\s-]*inclusion"), ["lfi", "rfi"]),
    (re.compile(r"command[\s-]*injection"), ["rce", "cmdi", "os command"]),
    (re.compile(r"code[\s-]*injection"), ["rce"]),
    (re.compile(r"http[\s-]*parameter[\s-]*pollution"), ["hpp"]),
    (re.compile(r"http[\s-]*verb[\s-]*tampering"), ["verb tampering"]),
    (re.compile(r"format[\s-]*string"), ["format string bug"]),
    (re.compile(r"csv[\s-]*injection"), ["formula injection"]),
    (re.compile(r"prototype[\s-]*pollution"), ["pp"]),
    (re.compile(r"mass[\s-]*assignment"), ["mass assign"]),
    (re.compile(r"padding[\s-]*oracle"), ["padding oracle attack"]),
    (re.compile(r"\bgraphql\b"), ["gql"]),
    (re.compile(r"\boauth\b"), ["oauth2"]),
    (re.compile(r"open[\s-]*redirect|url[\s-]*redirect"), ["open redirect"]),
    (re.compile(r"insecure[\s-]*direct[\s-]*object"), ["idor"]),
    (re.compile(r"privilege[\s-]*escalation"), ["privesc"]),
    (re.compile(r"request[\s-]*smuggling"), ["http smuggling"]),
    (re.compile(r"host[\s-]*header"), ["host header injection", "headers"]),
    (re.compile(r"imap|smtp"), ["email injection"]),
    (re.compile(r"websocket"), ["ws"]),
    (re.compile(r"browser[\s-]*storage"), ["localstorage", "sessionstorage"]),
]


def normalize_url(url: str) -> str:
    """Strip .md, map README → directory URL, lowercase fragments."""
    frag = ""
    if ".md#" in url:
        path, frag_raw = url.split(".md#", 1)
        url = path
        frag = "#" + frag_raw.lower()
    elif "#" in url and not url.startswith("#"):
        path, frag_raw = url.split("#", 1)
        url = path
        frag = "#" + frag_raw.lower()
        if url.endswith(".md"):
            url = url[:-3]
    elif url.endswith(".md"):
        url = url[:-3]
    else:
        url = url.replace(".md", "")

    if url == "README" or url.endswith("/README"):
        url = url[: -len("README")]
    if url == "":
        url = "./"
    return url + frag


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


def url_path_key(url: str) -> str:
    """Path part of a nav url, without fragment or trailing slash."""
    return url.split("#", 1)[0].rstrip("/")


def nest_fragment_siblings(nodes: list[dict]) -> list[dict]:
    """Nest path#fragment entries under the sibling that owns that path.

    ToC lists in-page sections (e.g. 3.2–3.7) as peers of their page (3.1).
    For the sidebar, those belong under the page node.
    """
    result: list[dict] = []
    by_path: dict[str, dict] = {}
    for node in nodes:
        url = node["url"]
        path = url_path_key(url)
        has_frag = "#" in url
        if has_frag and path in by_path:
            parent = by_path[path]
            kids = parent.setdefault("children", [])
            kids.append(node)
        else:
            result.append(node)
            if not has_frag and path:
                by_path[path] = node
    for node in result:
        kids = node.get("children")
        if kids:
            node["children"] = nest_fragment_siblings(kids)
    return result


def resolve_doc_path(doc_root: Path, nav_url: str) -> Path | None:
    """Map a nav url to a markdown file under doc_root."""
    path = nav_url.split("#", 1)[0]
    if not path:
        return None
    candidates: list[Path] = []
    if path.endswith("/"):
        candidates.append(doc_root / path / "README.md")
        candidates.append(doc_root / path.rstrip("/") / "README.md")
    else:
        candidates.append(doc_root / f"{path}.md")
        if path.endswith("README"):
            candidates.append(doc_root / f"{path}.md")
        else:
            candidates.append(doc_root / path / "README.md")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def extract_primary_ids(text: str) -> list[str]:
    """
    Collect WSTG IDs from the page header/ID table (first ~40 lines).

    Avoids picking up cross-references later in the body.
    """
    head = "\n".join(text.splitlines()[:40])
    found: list[str] = []
    seen: set[str] = set()
    for match in WSTG_ID_RE.findall(head):
        canonical = match.upper()
        if canonical not in seen:
            seen.add(canonical)
            found.append(canonical)
    return found


def hints_from_title(title: str) -> list[str]:
    lowered = title.lower()
    hints: list[str] = []
    for pattern, aliases in TITLE_HINT_RULES:
        if pattern.search(lowered):
            hints.extend(aliases)
    return hints


def hints_from_ids(ids: list[str]) -> list[str]:
    hints: list[str] = []
    for test_id in ids:
        lower = test_id.lower()
        hints.append(lower)
        # WSTG-INPV-01 → inpv-01
        parts = lower.split("-", 1)
        if len(parts) == 2:
            hints.append(parts[1])
    return hints


def build_hints(node: dict, doc_root: Path) -> list[str]:
    hints = hints_from_title(node["title"])
    doc_path = resolve_doc_path(doc_root, node["url"])
    if doc_path is not None:
        text = doc_path.read_text(encoding="utf-8", errors="replace")
        hints.extend(hints_from_ids(extract_primary_ids(text)))
    # De-dupe, preserve order, drop empties.
    seen: set[str] = set()
    unique: list[str] = []
    for hint in hints:
        key = hint.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(key)
    return unique


def attach_hints(nodes: list[dict], doc_root: Path) -> None:
    for node in nodes:
        hints = build_hints(node, doc_root)
        if hints:
            node["hints"] = hints
        children = node.get("children") or []
        if children:
            attach_hints(children, doc_root)


def yaml_escape(value: str) -> str:
    return value.replace("'", "''")


def emit_yaml_nodes(nodes: list[dict], indent: int = 0) -> list[str]:
    lines: list[str] = []
    pad = "  " * indent
    child_pad = "  " * (indent + 1)
    for node in nodes:
        lines.append(f"{pad}- title: '{yaml_escape(node['title'])}'")
        lines.append(f"{child_pad}url: {node['url']}")
        hints = node.get("hints") or []
        if hints:
            # Space-separated; quoted so YAML stays a single string.
            lines.append(f"{child_pad}hints: '{yaml_escape(' '.join(hints))}'")
        children = node.get("children") or []
        if children:
            lines.append(f"{child_pad}children:")
            lines.extend(emit_yaml_nodes(children, indent + 2))
    return lines


def generate_yaml(title: str, nodes: list[dict]) -> str:
    body = "\n".join(emit_yaml_nodes(nodes))
    return f"docs_list_title: {title}\ndocs:\n\n{body}\n"


def toc_h1_title(readme_text: str) -> str:
    """Use the channel ToC H1 (e.g. Contents on latest, Table of Contents on older tags)."""
    for line in readme_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip() or "Contents"
    return "Contents"


def chapter_toc_markdown(nodes: list[dict], *, heading: str = "Contents") -> str:
    """Chapter-level ToC for the web landing page (detail lives in the sidebar)."""
    lines = [
        f"# {heading}",
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


def emit_html_nodes(nodes: list[dict], url_prefix: str) -> list[str]:
    """
    Pre-render the tree as HTML so Jekyll/Liquid does not recurse.

    Uses the Liquid tag {{ site.baseurl }} literally; Jekyll expands it when the
    include is rendered. Current-path open/active state is handled in JS.
    """
    lines: list[str] = []
    base = "{{ site.baseurl }}/" + url_prefix.strip("/") + "/"
    for node in nodes:
        title = html.escape(node["title"], quote=True)
        url = html.escape(node["url"], quote=True)
        href = base + url
        children = node.get("children") or []
        hints = node.get("hints") or []
        hints_attr = (
            f' data-hints="{html.escape(" ".join(hints), quote=True)}"' if hints else ""
        )
        lines.append(f'<li class="wstg-nav-item" data-title="{title}"{hints_attr}>')
        if children:
            lines.append("<details>")
            lines.append("<summary>")
            lines.append('<span class="wstg-nav-summary-row">')
            lines.append('<span class="wstg-nav-chevron" aria-hidden="true"></span>')
            lines.append(
                f'<a href="{href}" data-nav-url="{url}" title="{title}">{title}</a>'
            )
            lines.append("</span>")
            lines.append("</summary>")
            lines.append("<ul>")
            lines.extend(emit_html_nodes(children, url_prefix))
            lines.append("</ul>")
            lines.append("</details>")
        else:
            lines.append(
                f'<a href="{href}" data-nav-url="{url}" title="{title}">{title}</a>'
            )
        lines.append("</li>")
    return lines


def generate_html_tree(nodes: list[dict], url_prefix: str) -> str:
    body = "\n".join(emit_html_nodes(nodes, url_prefix))
    header = (
        "{% comment %}Generated by generate_nav.py for url_prefix="
        + url_prefix
        + "; do not edit by hand.{% endcomment %}\n"
    )
    return header + body + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", type=Path, help="Path to document/README.md")
    parser.add_argument(
        "--title",
        required=True,
        help="docs_list_title value (from prepend.nav, without key)",
    )
    parser.add_argument(
        "--collection",
        required=True,
        help="Data/nav key (latest, stable, v41, v42) - no dots (Jekyll data keys)",
    )
    parser.add_argument(
        "--url-prefix",
        help="URL path segment (default: --collection). Use v4.1 while key stays v41.",
    )
    parser.add_argument(
        "--doc-root",
        type=Path,
        help="Root of markdown content for ID scraping (default: readme parent)",
    )
    parser.add_argument(
        "--yaml-out",
        type=Path,
        required=True,
        help="Output path for nested navigation YAML",
    )
    parser.add_argument(
        "--html-out",
        type=Path,
        help="Output path for pre-rendered nav tree HTML include",
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
    nodes = nest_fragment_siblings(nodes)

    doc_root = args.doc_root if args.doc_root is not None else args.readme.parent
    attach_hints(nodes, doc_root)
    url_prefix = args.url_prefix if args.url_prefix else args.collection

    args.yaml_out.parent.mkdir(parents=True, exist_ok=True)
    args.yaml_out.write_text(generate_yaml(args.title, nodes), encoding="utf-8")

    if args.html_out is not None:
        args.html_out.parent.mkdir(parents=True, exist_ok=True)
        args.html_out.write_text(
            generate_html_tree(nodes, url_prefix), encoding="utf-8"
        )

    if args.chapter_toc_out is not None:
        args.chapter_toc_out.parent.mkdir(parents=True, exist_ok=True)
        args.chapter_toc_out.write_text(
            chapter_toc_markdown(nodes, heading=toc_h1_title(text)),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
