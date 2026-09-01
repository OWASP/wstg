# Workflows Documentation

This directory contains GitHub Actions workflows for the WSTG repository. Helper scripts used by these workflows are located in the `scripts/` subdirectory (with its own README).

## Version Information

These workflows use:

- Node.js and Python for various automation tasks
- GitHub Actions for checkout, setup, artifact management, and API interactions

## `build-checklists.yml`

For building checklists and Create a PR with changes made in the master.

- Trigger: Push, Only when files inside document directory is changed. Manual (`workflow_dispatch`), GitHub web UI.
- See: `/.github/json/` for JSON checklist generation and `/.github/xlsx/` for XLSX build.

## `build-ebooks-typst.yml`

Builds PDF and EPUB e-books using Typst (modern implementation).

- Trigger: Manual (`workflow_dispatch`), GitHub web UI.
- Pipeline:
  1. **list-chapters.py**: Generates synthetic chapter headings and outputs files in reading order
  2. **build-link-manifest.py**: Extracts real heading IDs from Pandoc AST for accurate cross-chapter links
  3. **Pandoc filters**:
     - `links.lua`: Resolves cross-chapter links using the manifest
     - `demote-headings.lua`: Adjusts heading levels while preserving chapter hierarchy
  4. **fix-typst-body.py**: Applies style conversions (images, ID badges, etc.)
  5. **Typst compiler**: Generates final PDF
  6. **Pandoc EPUB**: Generates EPUB with same filter pipeline
- Uploads: PDF and EPUB as separate artifacts (uncompressed)
- See: `/.github/ebooks/` for configuration, filters, and templates

## `clean-workflow-runs.yml`

Tiddies up old workflow runs.

- Trigger: Schedule

## `comment.yml`

Triggered by the completion of other workflows in order to comment lint or other results on PRs.
On failure, those workflows upload `artifact.txt` (attached as `artifact`) with the content to be commented.
The PR number comes from the `workflow_run` event (not from the artifact).

This workflow:

- Minimizes (collapses) previous comments from the same workflow with appropriate classifiers:
    - `RESOLVED` when the workflow succeeds (no artifact required)
    - `OUTDATED` when the workflow fails and a new artifact is available
- Only posts NEW comments on failure (not on success)
- On failure, skips minimize/post if the artifact download fails, so prior feedback is not wiped
- Uses GitHub Actions for artifact retrieval and PR comment management

- Trigger: Other workflows `workflow_run`.

## `dummy.yml`

Utility action named "Markdown Lint Check" (same name as `md-lint-check.yml`) that serves as a fallback to satisfy branch protection requirements. This workflow only runs when NO Markdown files are changed in a PR (e.g., only an image or YAML that isn't linted). It's a complementary workflow to `md-lint-check.yml` that ensures the required "Markdown Lint Check" status check passes even when there are no Markdown files to lint.

- Trigger: Pull Requests (when no `.md` files are changed).

## `md-link-check.yml`

Checks Pull Requests for broken links.

This workflow:

- Checks out the **PR head** to the workspace root (provides the composite action files and the PR's content) and the **base branch** (OWASP/wstg `master`) into `base/`
- Uses the `.github/actions/get-changed-files` composite action with the exact `base.sha`/`head.sha` from the PR event for fork-safe changed-file detection
- Copies **all** changed files (including images and other assets) into `base/` so link targets exist, then runs the link checker only on changed `.md` files so relative links resolve correctly
- Config is always taken from `base/` (the base branch), not from the PR

- Trigger: Pull Requests (when `.md` files are changed, excluding `.github/**`).
- Changed-file detection also skips `website/` (Jekyll site source: HTML/Liquid templates are not guide Markdown).
- Config File: `markdown-link-check-config.json`

## `md-link-check-full.yml`

Checks all Markdown files in the repository for broken links.

- Trigger: Manual (`workflow_dispatch`), GitHub web UI.
- Skips `.github/` and `website/`.
- Config File: `markdown-link-check-config.json`

## `md-lint-check.yml`

Checks Markdown files and flags style or syntax issues.

This workflow:

- Checks out the **PR head** to the workspace root and the **base branch** (OWASP/wstg `master`) into `base/`
- Uses the `.github/actions/get-changed-files` composite action with the exact `base.sha`/`head.sha` from the PR event for fork-safe changed-file detection, then runs `markdownlint-cli2` only on changed `.md` files
- Uses `format_lint_output.py` from `base/.github/workflows/scripts/` to format output for PR comments
- On failure, uploads `artifact.txt` for `comment.yml`
- Config and scripts are always taken from `base/` (the base branch), not from the PR

- Trigger: Pull Requests (when `.md` files are changed, excluding `.github/**`).
- Changed-file detection also skips `website/`.
- Config File: `.markdownlint.json`

## `md-textlint-check.yml`

Checks Markdown files for spelling style and typo issues.

This workflow:

- Checks out the **PR head** to the workspace root and the **base branch** (OWASP/wstg `master`) into `base/`
- Uses the `.github/actions/get-changed-files` composite action with the exact `base.sha`/`head.sha` from the PR event for fork-safe changed-file detection, then runs textlint only on changed `.md` files
- Config is always taken from `base/` (the base branch), not from the PR

- Trigger: Pull Requests (when `.md` files are changed, excluding `.github/**`).
- Changed-file detection also skips `website/`.
- Config File: `.textlintrc`

## `www_latest_update.yml`

Publishes the latest web content using the @wstgbot account to
`OWASP/www-project-web-security-testing-guide`.

- Trigger: Push to `master` when `document/**` changes, or manual (`workflow_dispatch`).
- Copies `document/` into the www repo’s `latest/`, prepends front matter, copies `info.md`.
- Runs `.github/www/scripts/generate_nav.py` to write:
    - `_data/latest.yaml` (nested ToC + filter hints)
    - `_includes/nav-tree-latest.html` (pre-rendered sidebar tree)
    - Slim chapter-only `latest/README.md` / `index.md` landing ToC
- See: `/.github/www/latest/` and `/.github/www/scripts/README.md`.

## `www_stable_update.yml`

Publishes stable and versioned web content using the @wstgbot account to
`OWASP/www-project-web-security-testing-guide`.

- Trigger: Tag applied to repository (format `v*`).
- Same nav generation as latest, for `stable` and the version folder (e.g. `v42`),
  including `nav-tree-<collection>.html` and nested `_data/*.yaml`.
- See: `/.github/www/` and `/.github/www/scripts/README.md`.
