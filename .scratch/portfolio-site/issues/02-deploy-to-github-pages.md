---
title: Deploy to GitHub Pages via CI
status: ready-for-agent
blocked-by: [01]
---

# 02: Deploy to GitHub Pages via CI

**What to build:** Every PR runs the `check` command in CI. Every push to `main` runs `check` and then deploys the site to GitHub Pages at `<github-user>.github.io/yh-portfolio`. The site's base URL is one config value, so a custom domain is a small change later.

The human-only steps get a `/wizard` script: creating the public `yh-portfolio` repo, adding the remote, pushing, and setting the Pages source to "GitHub Actions".

**Blocked by:** 01 (Site skeleton that builds, with a check command)

**Status:** ready-for-agent

- [ ] The CI workflow installs the locked `uv` environment (no dependency caching, per Zensical docs) and runs `check`.
- [ ] PRs run `check` but never deploy. `main` runs `check`, builds with strict and clean, and deploys.
- [ ] A failing `check` blocks deployment.
- [ ] `site_url` is set to the GitHub Pages project address and is the only place the base URL is defined.
- [x] A wizard script walks the author through the repo, remote and Pages-source steps.
- [ ] Verified: the live URL serves the skeleton, and its nav links resolve under the `/yh-portfolio/` path.
- [x] The README notes how to switch to a custom domain later (`site_url`, the CNAME file, the DNS record).

## Comments

### 2026-10-22

Written: `.github/workflows/docs.yml` (a `check` job on every PR and push to `main`; a `deploy` job that `needs: check` and runs only on pushes to `main`), a Deploy and Custom domain section in the README, and `scripts/publish-wizard.sh`.

Verified: `make check` passes locally (54 tests). The wizard passes `bash -n`; `shellcheck` is not installed so it was not linted. The README section was reviewed by reading only.

Not verified, so left unticked:

- The workflow has never run. The action versions (copied from the Zensical publish docs, plus `astral-sh/setup-uv@v6`) are untested, so the first run on GitHub may need fixes. That covers the first three criteria.
- `site_url` is still the `your-github-handle` placeholder. The wizard fills it in, but it has not been run (it needs the author's input).
- The live URL and nav links need the repo and Pages source to exist.

No tests were added, by agreement: the workflow and wizard are not observable at the source-check or built-site seams.

The wizard was written from scratch because the wizard skill's `template.sh` is in a directory the session's permissions deny. It does not use that template's library.
