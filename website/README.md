# WSTG website (Jekyll)

Preview site for the Web Security Testing Guide. Source guide content lives in
`../document/` (latest) and release tags (stable / v4.x). This directory is the
Jekyll shell (VWAD-inspired L&F).

Published preview: `https://wstg.owasp.org/`

## Branch roles

| Branch | Role |
|--------|------|
| `master` | Guide (`document/`) plus this site **source** and deploy workflow (same idea as `.github/www` + `www_*_update` workflows). |
| `gh-pages` | **Built** static site only. Written by `.github/workflows/deploy-website.yml` (do not hand-edit). |

GitHub Pages should deploy from branch **`gh-pages`** / root (not “GitHub Actions”), with custom domain `wstg.owasp.org`.

## Channels

| Path | Content |
|------|---------|
| `/latest/` | Working-tree `document/` |
| `/v4.2/`, `/v4.1/` | Versioned snapshots from git tags |
| `/stable/` | Path-preserving redirects → current stable (`v4.2`) |
| `/v42/`, `/v41/` | Legacy redirects → `/v4.2/`, `/v4.1/` |

`/stable/` is a floating pointer, not a second copy of the guide. Prefer
`/v4.2/` (etc.) for citations. Set `stable_version` in `_config.yml` and
`CURRENT_STABLE` in `scripts/prepare_site.py` when the current release changes.

Prepare also rewrites Markdown for the site: strip `.md` from links, map
`README` → directory URLs, fix sibling `images/` paths on leaf pages, and turn
`README.md` files into redirects to their directory index.

Canonical version URLs use a **period** (`v4.1`). The old owasp.org publish
pipeline stripped periods (`v41`) for path/data-key safety; this site keeps
dot-free keys (`v41.yaml`, `nav-tree-v41.html`) while serving pretty paths.

Generated (do not commit): channel trees under `website/{latest,stable,v4.*,v41,v42}/`,
`_data/*.yaml`, and `_includes/nav-tree-*.html`.

## Local serve

From the repository root:

```bash
./website/serve.sh
# or a subset:
./website/serve.sh latest stable
python3 website/scripts/prepare_site.py
```

Then open `http://127.0.0.1:4000/`.

Requires Ruby 3.3+ (script defaults to `RBENV_VERSION=3.3.10`), Bundler, and
git tags `v4.1` / `v4.2` available locally for versioned channels.
