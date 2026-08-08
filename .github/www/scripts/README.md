# www scripts

Helper scripts used when publishing WSTG content to
[OWASP/www-project-web-security-testing-guide](https://github.com/OWASP/www-project-web-security-testing-guide).

## generate_nav.py

Builds the website sidebar navigation from `document/README.md`.

**Outputs (as requested by flags):**

- Nested YAML for `_data/<collection>.yaml` (`docs` tree with optional `hints`)
- Pre-rendered HTML tree for `_includes/nav-tree-<collection>.html`
  (avoids Liquid `Nesting too deep` from recursive includes)
- Optional chapter-only markdown ToC for the collection landing page

**Filter hints (A + B):**

- **A.** Title alias rules (e.g. Cross Site Scripting → `xss`, XML Injection → `xxe`,
  XPath → `xml` / `xpathi`, SQL Injection → `sqli`)
- **B.** Primary `WSTG-*-*` IDs scraped from each page’s header ID table
  (first ~40 lines), plus short forms (`WSTG-INPV-01` → `inpv-01`)

Hints are emitted as `data-hints` on each nav item; the site JS matches filter
input against `data-title` and `data-hints`.

**Usage:**

```bash
python3 .github/www/scripts/generate_nav.py document/README.md \
  --title "WSTG Contents" \
  --collection latest \
  --yaml-out /path/to/www/_data/latest.yaml \
  --html-out /path/to/www/_includes/nav-tree-latest.html \
  --chapter-toc-out /tmp/wstg-chapter-toc.md
```

`--doc-root` defaults to the README’s parent directory (`document/`). Override
when scraping IDs from a different content tree (e.g. a versioned www folder).

Invoked by `www_latest_update.yml` and `www_stable_update.yml`.
