# Workflows Documentation

This directory contains GitHub Actions workflows for the WSTG repository. Helper scripts used by these workflows are located in the `scripts/` subdirectory (with its own README).

## Version Information

These workflows use:
- Node.js and Python for various automation tasks
- GitHub Actions for checkout, setup, artifact management, and API interactions

## `build-checklists.yml`

For building checklists and Create a PR with changes made in the master.

- Trigger: Push, Only when files inside document directory is changed. Manual (`workflow_dispatch`), GitHub web UI.
- See: `/.github/xlsx/` in the root of the repository for XLSX build.

## `build-ebooks.yml`

For building PDF and EPUB e-Books at release.

- Trigger: Tag applied to repository. Manual (`workflow_dispatch`), GitHub web UI.
- See: `/.github/pdf/` in the root of the repository for PDF build specific configurations.
- See: `/.github/epub/` in the root of the repository for EPUB build specific configurations.

## `comment.yml`

Triggered by the completion of other workflows in order to comment lint or other results on PRs.
The workflows which leverage it should create a `pr_number` text file and `artifact.txt` with the content to be commented, which are attached to their workflow runs as `artifact`.

This workflow:
- Minimizes (collapses) previous comments from the same workflow run with appropriate classifiers:
  - `RESOLVED` when the workflow succeeds
  - `OUTDATED` when the workflow fails
- Only posts NEW comments on failure (not on success)
- Uses GitHub Actions for artifact retrieval and PR comment management

- Trigger: Other workflows `workflow_run`.

## `dummy.yml`

Utility action named "Markdown Lint Check" (same name as `md-lint-check.yml`) that serves as a fallback to satisfy branch protection requirements. This workflow only runs when NO Markdown files are changed in a PR (e.g., only an image or YAML that isn't linted). It's a complementary workflow to `md-lint-check.yml` that ensures the required "Markdown Lint Check" status check passes even when there are no Markdown files to lint.

- Trigger: Pull Requests (when no `.md` files are changed).

## `md-link-check.yml`

Checks Pull Requests for broken links.

This workflow:
- Checks out the **base branch** into `base/` and the **PR head** into `pr/` (each checkout uses an explicit path so neither overwrites the other)
- Uses inline `git diff` from `pr/` (no third-party action) to list changed `.md` files between the base ref and HEAD, excluding deleted files and paths under `.github/`
- Copies only those changed files from `pr/` into `base/`, then runs the link checker so relative links resolve correctly
- Config and scripts are always taken from `base/` (the base branch), not from the PR

- Trigger: Pull Requests (when `.md` files are changed, excluding `.github/**`). Manual (`workflow_dispatch`).
- Config File: `markdown-link-check-config.json`

## `md-lint-check.yml`

Checks Markdown files and flags style or syntax issues.

This workflow:
- Checks out the **base branch** into `base/` and the **PR head** into `pr/` (each checkout uses an explicit path so neither overwrites the other)
- Uses inline `git diff` from `pr/` to list changed `.md` files (excluding deleted files and `.github/`), then runs `markdownlint-cli2` only on those files under `pr/`
- Uses `format_lint_output.py` from `base/.github/workflows/scripts/` to format output for PR comments
- Uploads artifacts for both success and failure cases to work with `comment.yml`
- Config and scripts are always taken from `base/` (the base branch), not from the PR

- Trigger: Pull Requests (when `.md` files are changed, excluding `.github/**`).
- Config File: `.markdownlint.json`

## `md-textlint-check.yml`

Checks Markdown files for spelling style and typo issues.

This workflow:
- Checks out the **base branch** into `base/` and the **PR head** into `pr/` (each checkout uses an explicit path so neither overwrites the other)
- Uses inline `git diff` from `pr/` to list changed `.md` files (excluding deleted files and `.github/`), then runs textlint only on those files under `pr/`
- Config is always taken from `base/` (the base branch), not from the PR

- Trigger: Pull Requests (when `.md` files are changed, excluding `.github/**`).
- Config File: `.textlintrc`

## `www_latest_update.yml`

Publishes the latest web content using the @wstgbot account to `OWASP/www-project-web-security-testing-guide`.

- Trigger: Push.
- See: `/.github/www/latest/` in the root of the repository.

## `www_stable_update.yml`

Publishes stable and versioned web content using the @wstgbot account to `OWASP/www-project-web-security-testing-guide`.

- Trigger: Tag applied to repository (format `v*`).
- See: `/.github/www/` in the root of the repository.
