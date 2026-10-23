---
title: Site skeleton that builds, with a check command
status: ready-for-agent
blocked-by: []
---

# 01: Site skeleton that builds, with a check command

**What to build:** A Zensical site the author can preview locally and build reproducibly. Running one `check` command verifies it. Visitors see a `modern`-themed site with a light/dark toggle and four nav sections (Home, Projects, Blog, About) with placeholder content. The built-site check exists as a harness with its own fixture project, ready for later tickets to add assertions.

See the spec: `.scratch/portfolio-site/spec.md` (Platform and tooling; Check modules).

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Zensical is pinned to an exact version via `uv`, on Python 3.12, with a committed lockfile. A fresh clone plus `uv sync` reproduces the environment.
- [ ] Config uses native `zensical.toml`. The content lives in a subdirectory, not the repo root.
- [ ] The `modern` theme is used, with light and dark palettes that follow the system preference and have a toggle.
- [ ] The nav shows Home, Projects, Blog and About, each with a placeholder page.
- [ ] A documented command starts the live-reload preview server.
- [ ] A single documented `check` command runs a strict build of the real site, and a broken internal link makes it fail.
- [ ] A built-site check harness builds a separate fixture project and asserts on its generated output. Its first assertion is that the four section pages exist.
- [ ] Build output and the Zensical cache are git-ignored.
- [ ] The README covers setup, preview, check and upgrading Zensical.
