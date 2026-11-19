# WSTG Release Process

This document describes how WSTG releases work, including manual steps and automated workflows. The guide is published at `wstg.owasp.org` (Jekyll-based). The legacy OWASP.org deployment (`OWASP/www-project-web-security-testing-guide`) is no longer updated.

## Overview

Releases are driven by a git tag in the format `vMAJOR.MINOR` (e.g., `v4.2`, `v5.0`). The website discovers versions from tags, so nothing else needs editing:

- **Pre-tag PR**: Updates release content (must be merged before tagging).
- **Tag push**: `git tag v5.0 && git push origin v5.0` rebuilds and deploys `wstg.owasp.org`; the newest tag becomes `/stable/`, and the previous stable becomes an archived version. It also triggers the e-book build.

## Release Checklist

### Phase 1: Pre-Tag Preparation (Manual PR)

Before tagging, prepare the content updates that must exist in the tagged commit.

See [PR #613](https://github.com/OWASP/wstg/pull/613) for an example of pretag prep work (v4.2); its `.github/www/` changes no longer apply.

#### Content Updates

File: `README.md` (repository root)

- Update "currently working on" version (e.g., from "4.2" to "5.0").
- Update "last stable release" version and link.

File: `document/1-About/README.md` (formerly 1-Frontispiece; path may differ)

- Update version references and dates.

File: `document/2-Introduction/README.md`

- Update version mentions if applicable.

File: `document/6-Appendix/E-History.md`

- Add entry for the new release with date, key changes, and authors.

Reference: commit `f142504f` shows v4.2 prep changes to these files.

#### Create Pre-Tag PR

- Stage all content edits.
- Commit with message: "v5.0 Release Preparation - Content" (update version).
- Open PR for review by maintainers.
- **Merge to `master`.**

### Phase 2: Tag the Release (Maintainers Only)

```bash
git tag v5.0
git push upstream v5.0
```

(Use `upstream` if your remote points to your fork; use `origin` if you have direct push access to OWASP/wstg.)

### Phase 3: Verify the Website (Automatic)

Pushing the tag triggers `deploy-website.yml` (built from `master`). `website/scripts/prepare_site.py` finds the tag, builds `/v5.0/`, repoints `/stable/` and the version switcher, banners, home page, Downloads page, `llms.txt` and `/md/` copies. No `website/` edits are needed. Check the Actions run and spot-check `https://wstg.owasp.org/stable/`.

Only tags matching `v[0-9]*.[0-9]*` (and 4.1 or newer) are picked up. Prerelease names such as `v5.0-rc1` are ignored.

### Phase 4: Create GitHub Release (Manual)

After the pre-tag PR is merged, the tag is pushed and the website deploy succeeds:

1. Go to **GitHub → Releases → "Draft a new release"**.
2. Tag: `v5.0` (autocomplete from existing tag).
3. Release title: "WSTG v5.0" (example).
4. Description: Summary of major changes (optional).
5. Attach assets (optional):
    - Download the artifacts from the `build-ebooks-typst.yml` run triggered by the tag push (see Phase 5): `wstg-v5.0.pdf`, `wstg-v5.0.epub`.
    - Attach to the Release.
6. Publish.

### Phase 5: Build E-Books (Optional)

Pushing a release tag also runs the e-book build automatically (files are named after the tag; download them from the run). To build manually, see below. Select the cover image first:

- Directory: `.github/ebooks/assets/`
- Versioned covers exist: `cover-v4.1.jpg`, `cover-v4.2.jpg`, `cover-v4.3.jpg`, etc.
- To use a versioned cover for v5.0, either:
    - Create `cover-v5.0.jpg` if you have a new design, OR
    - Copy an existing versioned cover (e.g., `cover-v4.2.jpg`) to `cover-v5.0.jpg`, OR
    - Update the generic `cover.jpg` to use for all versions.
- The workflow uses whatever is at `.github/ebooks/assets/cover.jpg`.

Manual dispatch:

1. Go to **GitHub → Actions → "Build E-Books"** workflow.
2. Click **"Run workflow"** → Select branch and enter version (e.g., `v5.0`).
3. Wait for completion.
4. Download artifacts from the workflow run.
5. Attach to the GitHub Release created in Phase 4.

See `.github/workflows/build-ebooks-typst.yml` for details. The workflow checks out the specified version/branch and generates PDF and EPUB.

## Deployment Infrastructure

### New Website (wstg.owasp.org)

**Trigger:** Push to `master` touching `website/` or `document/`, a new release tag (`vMAJOR.MINOR`), or manual `workflow_dispatch` on `deploy-website.yml`. Always builds from `master`.

**Output:** Pushes to `gh-pages` branch (same repository).

**Deployment:** GitHub Pages configured on `gh-pages` / root with custom domain `wstg.owasp.org`.

**Channels:** Generated at:

- `/latest/` - working tree `document/`
- `/v5.0/`, `/v4.2/`, `/v4.1/` - one per release tag (pretty URLs with period)
- `/stable/` - path-preserving redirects to the newest tag
- `/v42/`, `/v41/` - legacy no-period redirects for old links (not created for newer versions)

The version list is written to `_data/versions.yaml` by `prepare_site.py` and drives the switcher, banners, home page, Downloads page and agent files.

**Per-page version switcher:** Powered by `_data/version_map.yaml` (generated by prepare_site.py). Lists all WSTG IDs and their URLs in each channel. Updated every time the site rebuilds.

## Important Constraints

### Naming Conventions

- **Git tags:** use a period: `v4.2`, `v5.0`.
- **Jekyll data/include keys:** drop the period: `v42`, `v50` (dots break Jekyll YAML/Liquid).
- **New site pretty URLs:** keep the period: `/v4.2/`, `/v5.0/`.

### Version Path Mapping

Example for v5.0:

| Item | Value | Notes |
|------|-------|-------|
| Git tag | `v5.0` | Created locally and pushed |
| Channel path | `v5.0` | Pretty URL on wstg.owasp.org (derived from the tag) |
| Data key | `v50` | Jekyll data key (no dot, derived) |
| wstg.owasp.org URL | `/v5.0/` | User-facing path (pretty) |

### Critical Ordering

1. Pre-tag PR merged (README and document updates).
2. Tag pushed (`git tag v5.0 && git push origin v5.0`).
3. `deploy-website.yml` and `build-ebooks-typst.yml` run automatically.

### Gotchas

**Newest tag is stable.** Tagging a new release immediately makes it `/stable/`. Don't push a release-shaped tag (`vX.Y`) until you mean to promote it.

**Manual rebuild.** Run `deploy-website.yml` via `workflow_dispatch` to rebuild without a new tag.

## One-Time Setup (for Administrators)

- Set GitHub Pages on OWASP/wstg to deploy from `gh-pages` / root, with custom domain `wstg.owasp.org`.
- Confirm `gh-pages` branch exists in OWASP/wstg (created by first `deploy-website.yml` run, or manually).

## See Also

- [Workflow Documentation](.github/workflows/README.md) - detailed workflow descriptions.
- [Website README](website/README.md) - channel structure, pretty URLs, local serve instructions.
- [CONTRIBUTING](CONTRIBUTING.md) - general contribution guidelines.
