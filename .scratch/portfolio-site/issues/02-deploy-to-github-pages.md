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
- [ ] A wizard script walks the author through the repo, remote and Pages-source steps.
- [ ] Verified: the live URL serves the skeleton, and its nav links resolve under the `/yh-portfolio/` path.
- [ ] The README notes how to switch to a custom domain later (`site_url`, the CNAME file, the DNS record).
