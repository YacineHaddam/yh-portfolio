---
title: Site skeleton that builds, with a check command
status: done
blocked-by: []
---

# 01: Site skeleton that builds, with a check command

**What to build:** A Zensical site the author can preview locally and build reproducibly. Running one `check` command verifies it. Visitors see a `modern`-themed site with a light/dark toggle and four nav sections (Home, Projects, Blog, About) with placeholder content. The built-site check exists as a harness with its own fixture project, ready for later tickets to add assertions.

See the spec: `.scratch/portfolio-site/spec.md` (Platform and tooling; Check modules).

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Zensical is pinned to an exact version via `uv`, on Python 3.12, with a committed lockfile. A fresh clone plus `uv sync` reproduces the environment.
- [x] Config uses native `zensical.toml`. The content lives in a subdirectory, not the repo root.
- [x] The `modern` theme is used, with light and dark palettes that follow the system preference and have a toggle.
- [x] The nav shows Home, Projects, Blog and About, each with a placeholder page.
- [x] A documented command starts the live-reload preview server.
- [x] A single documented `check` command runs a strict build of the real site, and a broken internal link makes it fail.
- [x] A built-site check harness builds a separate fixture project and asserts on its generated output. Its first assertion is that the four section pages exist.
- [x] Build output and the Zensical cache are git-ignored.
- [x] The README covers setup, preview, check and upgrading Zensical.

## Comments

### 2026-10-21

Done in commits `d73b520` and `37bd270`. Verified: `zensical build --strict --clean` is clean on the real site, a deliberate broken internal link makes it exit 1, the 4 built-site tests pass, and removing a fixture page makes its test fail. The built HTML contains the system, light and dark palette entries with toggle labels.

Not verified: `make serve` and `make check` were not run as written (`make` and `uv` don't work inside the agent sandbox; the equivalent `.venv/bin` commands were run instead). The palette toggle was checked in the built HTML only, not in a browser.
