---
title: Deploy to GitHub Pages via CI
status: done
blocked-by: [01]
---

# 02: Deploy to GitHub Pages via CI

**What to build:** Every PR runs the `check` command in CI. Every push to `main` runs `check` and then deploys the site to GitHub Pages at `<github-user>.github.io/yh-portfolio`. The site's base URL is one config value, so a custom domain is a small change later.

The human-only steps get a `/wizard` script: creating the public `yh-portfolio` repo, adding the remote, pushing, and setting the Pages source to "GitHub Actions".

**Blocked by:** 01 (Site skeleton that builds, with a check command)

- [x] The CI workflow installs the locked `uv` environment (no dependency caching, per Zensical docs) and runs `check`.
- [x] PRs run `check` but never deploy. `main` runs `check`, builds with strict and clean, and deploys.
- [x] A failing `check` blocks deployment.
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

Verified: the workflow ran on `main` and the site deployed. The author reports that everything works correctly, and a screenshot shows a post live at `https://yacinehaddam.github.io/yh-portfolio/blog/2026/10/21/hello-world/`. The nav links were checked by the author, not by me.

Verified with a throwaway PR (branch `test/ci-failing-check`, since deleted, closed unmerged) that added a link to a page that does not exist. On the PR, `Documentation / check` ran and failed in the strict build (`index.md:8`, "page does not exist", then `make check` exited non-zero), and `Documentation / deploy` was skipped; GitHub reported "This branch has not been deployed". Evidence is the author's screenshot and the pasted job log.

Caveat on "A failing `check` blocks deployment": the deploy was skipped on the PR because the job runs only for pushes to `main`, so the run itself does not isolate the `needs: check` gate. Blocking on `main` rests on `deploy` declaring `needs: check` (documented GitHub behaviour). A failing push to `main` was deliberately not tried against the live branch.
