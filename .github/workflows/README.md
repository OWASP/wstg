# Workflows Documentation

This directory contains GitHub Actions workflows for the WSTG repository. Helper scripts used by these workflows are located in the `scripts/` subdirectory (with its own README).

## Version Information

These workflows use:
- Node.js version 24
- GitHub Actions v6 for checkout (`actions/checkout@v6`) and setup actions (`actions/setup-node@v6`)
- Latest artifact actions (`actions/upload-artifact@v6`, `actions/download-artifact@v7.0.0`)
- `actions/github-script@v8` for GitHub API interactions

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
- Uses `actions/download-artifact@v7.0.0` for artifact retrieval
- Uses `actions/github-script@v8` for PR comment management

- Trigger: Other workflows `workflow_run`.

## `dummy.yml`

Utility action named "Markdown Lint Check" (same name as `md-lint-check.yml`) that serves as a fallback to satisfy branch protection requirements. This workflow only runs when NO Markdown files are changed in a PR (e.g., only an image or YAML that isn't linted). It's a complementary workflow to `md-lint-check.yml` that ensures the required "Markdown Lint Check" status check passes even when there are no Markdown files to lint.

- Trigger: Pull Requests (when no `.md` files are changed).

## `md-link-check.yml`

Checks Pull Requests for broken links.

This workflow includes security enhancements:
- Input validation for repository names and commit SHAs to prevent injection attacks
- Sparse checkout for security and efficiency (only checking out changed files)

- Trigger: Pull Requests (when `.md` files are changed, excluding `.github/**`). Manual (`workflow_dispatch`).
- Config File: `markdown-link-check-config.json`

## `md-lint-check.yml`

Checks Markdown files and flags style or syntax issues.

This workflow:
- Uses `markdownlint-cli2` for linting
- Leverages sparse checkout for security and efficiency (only checking out changed files)
- Uses `format_lint_output.py` script to format output for PR comments
- Uploads artifacts for both success and failure cases to work with `comment.yml`

Security enhancements:
- Input validation for repository names and commit SHAs to prevent injection attacks
- Sparse checkout for security and efficiency

- Trigger: Pull Requests (when `.md` files are changed, excluding `.github/**`).
- Config File: `.markdownlint.json`

## `md-textlint-check.yml`

Checks Markdown files for spelling style and typo issues.

This workflow includes security enhancements:
- Input validation for repository names and commit SHAs to prevent injection attacks
- Sparse checkout for security and efficiency (only checking out changed files)

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
