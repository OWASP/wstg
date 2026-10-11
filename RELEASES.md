# WSTG Release Process

This document describes how WSTG releases work, including manual steps and automated workflows. WSTG maintains two parallel publishing pipelines: the legacy OWASP.org deployment and the newer `wstg.owasp.org` website (Jekyll-based).

## Overview

Releases are driven by a git tag in the format `v*` (e.g., `v4.2`, `v5.0`). The process involves preparation PRs and tagging:

- **Pre-tag PR**: Adds release configuration files (must be merged before tagging).
- **Tag push**: `git tag v5.0 && git push origin v5.0` triggers `www_stable_update.yml` (legacy pipeline).
- **Post-tag PR**: Updates CHANNELS, stable version, and downloads (auto-triggers new site rebuild).

The new website at `https://wstg.owasp.org/` rebuilds automatically when `website/scripts/prepare_site.py` or `_config.yml` is edited, but only if the referenced git tags already exist.

## Release Checklist

### Phase 1: Pre-Tag Preparation (Manual PR)

Before tagging, prepare version configuration files that must exist in the tagged commit.

See [PR #613](https://github.com/OWASP/wstg/pull/613) for a complete example of pre-tag prep work (v4.2).

#### Content Updates

File: `README.md` (repo root)

- Update "currently working on" version (e.g., from "4.2" to "5.0").
- Update "last stable release" version and link.

File: `document/1-About/README.md` (formerly 1-Frontispiece; path may differ)

- Update version references and dates.

File: `document/2-Introduction/README.md`

- Update version mentions if applicable.

File: `document/6-Appendix/E-History.md`

- Add entry for the new release with date, key changes, and authors.

Reference: commit `f142504f` shows v4.2 prep changes to these files.

#### Legacy Pipeline Configuration (OWASP.org)

File: `.github/www/<VERSION_PATH>/` (new directory, e.g., `.github/www/v50/` for tag `v5.0`)

Copy from the latest release directory (e.g., `.github/www/v42/`) as a template, then edit:

- **`prepend.txt`** - front matter prepended to every document.md file. Update version labels, breadcrumb text, and release date.
- **`info.md`** - metadata snippets for sidebar/navigation. Update version-specific text.
- **`prepend.nav`** - navigation title passed to `generate_nav.py`.
- **`README.md`** - version-specific instructions (rarely changed).

File: `.github/www/stable/prepend.txt`

- Update to reflect the new stable version in breadcrumbs (if this release becomes stable).

**Critical:** These files MUST be committed to the branch and tag. The `www_stable_update.yml` workflow checks out the tag and reads these files from within that tagged commit.

#### Create Pre-Tag PR

- Stage all content edits and `.github/www/<VERSION_PATH>/` directory.
- Stage `.github/www/stable/prepend.txt` (if promoting to stable).
- Commit with message: "v5.0 Release Preparation - Content and Pipeline Config" (update version).
- Open PR for review by maintainers.
- **Merge to `master`.**

### Phase 2: Tag the Release (Maintainers Only)

Only four authorized actors can trigger `www_stable_update.yml`: `kingthorin`, `ThunderSon`, `rejahrehim`, `victoriadrake`.

```bash
git tag v5.0
git push upstream v5.0
```

(Use `upstream` if your remote points to your fork; use `origin` if you have direct push access to OWASP/wstg.)

This immediately triggers `www_stable_update.yml`:

- Checks out the tag and the `OWASP/www-project-web-security-testing-guide` repository.
- Extracts `document/` from the tagged commit.
- Copies to `stable/` and `v50/` directories (removing periods from version numbers).
- Prepends front matter from `.github/www/v50/` and `.github/www/stable/`.
- Generates navigation YAML and HTML includes via `.github/www/scripts/generate_nav.py`.
- Pushes branch `stable-update` to wstgbot's fork.
- Opens a PR on `OWASP/www-project-web-security-testing-guide`.
- **Manual step:** Maintainers must review and merge the PR to publish to the legacy site.

### Phase 3: Post-Tag Configuration (Manual PR)

After tagging and confirming the tag exists, update the new site configuration. This PR auto-triggers the site rebuild.

#### New Pipeline (Jekyll Site at wstg.owasp.org)

File: `website/scripts/prepare_site.py`

- Add entry to `CHANNELS` tuple with:
    - `"path": "v5.0"` (pretty URL with period)
    - `"key": "v50"` (no-period Jekyll data/include key for YAML files and Liquid includes)
    - `"title"`: descriptive title (e.g., "WSTG Contents (v5.0)")
    - `"label"`: display label (e.g., "v5.0")
    - `"tag": "v5.0"` (git tag name; must exist or prepare_site.py will fail)

- If promoting to stable, update:
    - `CURRENT_STABLE = "v5.0"`
    - `PATH_REDIRECTS` entries (add/update legacy aliases like `v50` → `v5.0`)

File: `website/_config.yml`

- Update `stable_version: v5.0` (if this is the new stable).
- Add hardcoded version references if present (check current file for v4.2 entries).

File: `website/downloads.md`

- Add new version entry with date and links.

File: `.gitignore`

- Add entries for generated site directories:
    - `website/v5.0/` (new version directory)
    - `website/v50/` (if v50 alias is used)

#### Create Post-Tag PR

- Stage all `website/` edits and `.gitignore`.
- Commit with message: "Add v5.0 to Website - Update CHANNELS and Navigation" (update version).
- Open PR for review.
- **Merge to `master`.**

This merge automatically triggers `deploy-website.yml` (because `website/` changed). The workflow:

- Extracts guide snapshots from git tags and the working tree.
- Runs `prepare_site.py` to generate channel trees, navigation, and redirects (now that v5.0 tag exists).
- Builds Jekyll site to static HTML.
- Publishes to `gh-pages` branch (served at wstg.owasp.org).

### Phase 4: Create GitHub Release (Manual)

After both PRs are merged and workflows succeed:

1. Go to **GitHub → Releases → "Draft a new release"**.
2. Tag: `v5.0` (auto-complete from existing tag).
3. Release title: "WSTG v5.0" (example).
4. Description: Summary of major changes (optional).
5. Attach assets (optional):
    - Run `build-ebooks-typst.yml` workflow (manual dispatch), then download artifacts: `wstg-v5.0.pdf`, `wstg-v5.0.epub`.
    - Attach to the Release.
6. Publish.

### Phase 5: Build E-Books (Optional)

Before building, select the cover image:

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

### Legacy Pipeline (OWASP.org)

**Trigger:** Tag `v*` pushed to OWASP/wstg by authorized actor.

**Output repo:** `OWASP/www-project-web-security-testing-guide` (main branch).

**Deployment:** Maintained by OWASP; changes to main are served at versioned URLs:
- `https://owasp.org/www-project-web-security-testing-guide/v50/` (v5.0, no period)
- `https://owasp.org/www-project-web-security-testing-guide/stable/` (floating pointer)

**Actors:** Workflow runs only if pushed by one of four maintainers. Others must request delegation.

**Secrets:** `wstg_deploy_token` (must have write access to wstgbot's fork and OWASP/www-project). Administrators must set this.

### New Website (wstg.owasp.org)

**Trigger:** Manual merge of post-tag PR (touches `website/`), or manual `workflow_dispatch` on `deploy-website.yml`.

**Output:** Pushes to `gh-pages` branch (same repo).

**Deployment:** GitHub Pages configured on `gh-pages` / root with custom domain `wstg.owasp.org`.

**Channels:** Generated at:
- `/latest/` - working tree `document/`
- `/v5.0/`, `/v4.2/`, `/v4.1/` - from git tags (pretty URLs with period)
- `/stable/` - path-preserving redirects to current stable version
- `/v50/`, `/v42/`, `/v41/` - legacy no-period redirects (for old links and Jekyll data keys)

**Per-page version switcher:** Powered by `_data/version_map.yaml` (generated by prepare_site.py). Lists all WSTG IDs and their URLs in each channel. Updated every time the site rebuilds.

## Important Constraints

### Naming Conventions

- **Git tags:** use a period: `v4.2`, `v5.0`.
- **Jekyll data/include keys:** drop the period: `v42`, `v50` (dots break Jekyll YAML/Liquid).
- **Legacy site paths:** drop periods: `v42`, `v50`.
- **New site pretty URLs:** keep the period: `/v4.2/`, `/v5.0/`.
- **Directory names in .github/www/:** match the key (no period): `v50/`, `v42/`.

### Version Path Mapping

Example for v5.0:

| Item | Value | Notes |
|------|-------|-------|
| Git tag | `v5.0` | Created locally, pushed to trigger `www_stable_update.yml` |
| Git ref for site rebuild | `v5.0` | Tag must exist before `deploy-website.yml` runs |
| CHANNELS path | `v5.0` | Pretty URL on wstg.owasp.org |
| CHANNELS key | `v50` | Jekyll data key (no dot) |
| .github/www directory | `v50/` | Legacy pipeline config |
| www repo directory | `v50/` | Published to OWASP/www-project |
| wstg.owasp.org URL | `/v5.0/` | User-facing path (pretty) |
| owasp.org URL | `/v50/` | Legacy site (no period) |

### Critical Ordering

1. Pre-tag PR merged (README, document updates, `.github/www/v50/` files).
2. Tag pushed (`git tag v5.0 && git push origin v5.0`).
3. Verify `www_stable_update.yml` runs (check GitHub Actions). A PR appears on OWASP/www-project.
4. Maintainer reviews and merges the bot PR on www-project.
5. Post-tag PR merged (`website/scripts/prepare_site.py`, `_config.yml`, `.gitignore`, `downloads.md`).
6. `deploy-website.yml` auto-triggers and publishes to wstg.owasp.org.

**If you merge the post-tag PR before the tag exists,** `prepare_site.py` will fail in "Prepare channel trees" (missing git ref). Either wait for tagging, or temporarily comment out the new version in CHANNELS, merge, then add it back and re-merge.

### Gotchas

**Tag pattern `v*` is broad.** `v5.0-rc1` will match and trigger workflows. Pre-release tags should NOT match `v*` (use non-`v` names like `20250101` or `v5.0-rc1` on a feature branch). Tag `20230928` is an example of a non-matching name.

**Only four authorized actors.** If you are not one of the four, tagging must be delegated to a maintainer (push on their behalf, or temporary write access).

**www_stable_update.yml is silent on skip.** If the actor check fails, the workflow is skipped without error message. Check the Actions tab to confirm a run occurred.

**Website rebuild depends on tag.** If `prepare_site.py` references a tag that does not exist, the post-tag PR will merge but the workflow will fail. The solution: merge post-tag PR after tag exists (or temporarily remove the new version entry).

**Stale prep directories.** `.github/www/v43/` exists but was never tagged as v4.3. Before creating a new version directory, verify no stale prep dir exists: check `git log -- .github/www/v<VERSION_PATH>` for the last editor and tag that version references.

**Old owasp.org site still serves.** `/www-project-web-security-testing-guide/stable/` at owasp.org is separate from wstg.owasp.org. Both must be updated independently. Consider whether to maintain both in sync or deprecate the old one.

### Hardcoded Version References

The new website codebase hardcodes version numbers in several places. When adding a version, check and update these files:

- `website/_config.yml` - `stable_version`, channel paths, collection names
- `website/_includes/version-switcher.html` - hardcoded version list and logic for stable release
- `website/_includes/home-versions-nav.html` - navigation note showing current stable version
- `website/index.md` - version-related documentation

Run `grep -rn 'v4\.[0-9]\|v4[0-9]' website _includes` (skipping generated trees) to find all references.

## One-Time Setup (for Administrators)

- Create `wstg_deploy_token` secret in OWASP/wstg GitHub Actions settings. Token must have write access to wstgbot's fork of `www-project-web-security-testing-guide`.
- Ensure wstgbot's fork of `www-project-web-security-testing-guide` exists and has `main` branch tracking upstream.
- (Optional) Configure branch protection on `OWASP/www-project-web-security-testing-guide` main to require PR reviews.
- Set GitHub Pages on OWASP/wstg to deploy from `gh-pages` / root, with custom domain `wstg.owasp.org`.
- Confirm `gh-pages` branch exists in OWASP/wstg (created by first `deploy-website.yml` run, or manually).

## See Also

- [Workflow Documentation](.github/workflows/README.md) - detailed workflow descriptions.
- [Website README](website/README.md) - channel structure, pretty URLs, local serve instructions.
- [CONTRIBUTING](CONTRIBUTING.md) - general contribution guidelines.
