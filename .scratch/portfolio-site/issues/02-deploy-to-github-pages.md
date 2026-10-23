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

- [x] The CI workflow installs the locked `uv` environment (no dependency caching, per Zensical docs) and runs `check`.
- [ ] PRs run `check` but never deploy. `main` runs `check`, builds with strict and clean, and deploys.
- [ ] A failing `check` blocks deployment.
- [x] `site_url` is set to the GitHub Pages project address and is the only place the base URL is defined.
- [x] A wizard script walks the author through the repo, remote and Pages-source steps.
- [x] Verified: the live URL serves the skeleton, and its nav links resolve under the `/yh-portfolio/` path.
- [x] The README notes how to switch to a custom domain later (`site_url`, the CNAME file, the DNS record).

## Comments

### 2026-10-22

Written: `.github/workflows/docs.yml` (a `check` job on every PR and push to `main`; a `deploy` job that `needs: check` and runs only on pushes to `main`), a Deploy and Custom domain section in the README, and `scripts/publish-wizard.sh`.

Verified: `make check` passes locally (54 tests). The wizard passes `bash -n`; `shellcheck` is not installed so it was not linted. The README section was reviewed by reading only.

No tests were added, by agreement: the workflow and wizard are not observable at the source-check or built-site seams.

The wizard was written from scratch because the wizard skill's `template.sh` is in a directory the session's permissions deny. It does not use that template's library.

### 2026-10-23

The author ran the wizard, set `site_url` to `https://YacineHaddam.github.io/yh-portfolio/`, pushed `main` and set the Pages source to GitHub Actions. The push first failed on GitHub's private-email protection (the commits carried a work address), so the 21 local commits were re-authored with the GitHub noreply address before pushing.

Verified: the workflow ran on `main` and the site deployed. The author reports that everything works correctly, and a screenshot shows a post live at `https://yacinehaddam.github.io/yh-portfolio/blog/2026/10/21/hello-world/`. That covers the locked-`uv` check, the live URL under `/yh-portfolio/`, and the single `site_url`. The nav links were checked by the author, not by me.

Not verified, so left unticked:

- A pull request has not been opened, so "PRs run `check` but never deploy" is untested. The `main` half (check, strict clean build, deploy) is confirmed by the deployed site.
- "A failing `check` blocks deployment" needs a throwaway PR or push with a deliberate failure. It is expected from `deploy` having `needs: check`, but has not been exercised.
