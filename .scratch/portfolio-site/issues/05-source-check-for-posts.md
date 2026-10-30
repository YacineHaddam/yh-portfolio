---
title: Source Markdown check for posts
status: done
blocked-by: [04]
---

# 05: Source Markdown check for posts

**What to build:** Before building, `check` lints the source Markdown and reports every violation, with file and reason, in one pass. It catches broken or risky posts before Zensical runs. It covers both the fixture content and the real content.

See the spec: Check modules (Source check).

**Blocked by:** 04 (Categories, tags and RSS)

- [x] Input is a content directory and the category allow-list (one source of truth shared with the site config). Output is a list of violations, and it exits non-zero if there are any.
- [x] It fails on: invalid YAML front matter, a missing `date`/`title`/`categories` on a post, a malformed date, a non-boolean `draft`, or a category not in the allow-list.
- [x] It flags phone-number-like and street-address-like patterns in public content.
- [x] It runs Markdown style linting (headings, lists, formatting) with a committed config.
- [x] Fixtures exist for each failure kind. Tests assert on the reported violations, not on internals.
- [ ] `check` runs the source check first, then the builds, and CI picks it up with no workflow change. The `make check` half is done; the CI half is open until ticket 02 adds a workflow that runs `make check`.
- [x] The real content passes.

## Comments

### 2026-10-21

Implemented: `tools/source_check.py` (library function `check_content(content_dir, allowed_categories)` plus a command that reads `docs_dir` and `categories_allowed` from a `zensical.toml`), a committed `.pymarkdown.json`, fixtures under `tests/source_fixtures/` (one per failure kind, plus a valid one), `tests/test_source_check.py` and `tests/test_source_check_cli.py`. `make check` now runs the source check on the real and fixture sites before the strict build and `pytest`. `pymarkdownlnt` is a dev dependency and `pythonpath = ["tools"]` is set for pytest.

Verified: `pytest` passes (33 tests), `zensical build --strict --clean` passes, and the source check exits 0 on both the real content and the fixture site. Each failure kind has a test that asserts on the reported file and reason. The allow-list is read from `zensical.toml`, the same value the blog plugin enforces.

Notes and not verified:
- `make check` itself was not run. `uv` is broken in the agent sandbox, so each of its steps was run directly from `.venv/bin`, with `TZDIR` pointing at the `tzdata` package as in ticket 04. Without `TZDIR` the built-site tests error in the sandbox because `/usr/share/zoneinfo` is unreadable.
- The CI criterion is unticked on purpose. The repo has no `.github/workflows` yet (that is ticket 02), so nothing could be checked. The ticket 02 workflow should run `make check`.
- `tests/fixture_site/.../older-published-post.md` had no `categories`, so it failed the new check. I gave it `engineering`, not `notes`, because a built-site test requires that nothing links to `category/notes`.
- Markdown lint rules MD013 (line length), MD033 (inline HTML, needed for the `<!-- more -->` and tags markers) and MD041 (first line heading, since posts may take their title from front matter) are disabled in `.pymarkdown.json`. All other default rules are on.
- The phone and street patterns are heuristics. They are tested on one positive fixture each and on the clean real and fixture content, but there are no tests for near misses such as dates or version numbers. They also miss unseparated numbers (`07911123456`), 2-digit groups (`06 12 34 56 78`) and alphanumeric house numbers (`221B Baker Street`), and falsely flag three space-separated digit groups such as `12 000 000` in prose.
- The check only applies the post rules under `blog/posts/`, so a post placed elsewhere is not checked for date, categories or draft. Project front matter checks belong to ticket 06.
- A quoted date such as `"2026-01-15"` is reported as malformed, and a timestamp such as `2026-01-15 10:00` is accepted. Whether Zensical accepts the quoted form was not checked.

### 2026-10-21 (review fixes)

Fixed after code review, each with a fixture and a test that failed first: a scalar `categories: engineering` is now reported as "categories must be a list" (it was one violation per letter); front matter with no closing `---` is reported as "not closed" (it was treated as absent); a `# comment` inside a fenced code block no longer counts as a post title; non-mapping front matter is reported instead of treated as empty. Fenced code blocks are also skipped by the phone and address patterns. `pyyaml` is now a declared dependency, and `uv.lock` was edited by hand to match because `uv` cannot run in the sandbox. Run `uv lock` to confirm it. `test_real_content_passes` was replaced by a test on the fixture site, so no test depends on real content (`make check` covers that). A CRLF fixture passes, because Python normalises line endings on read. `pytest` passes (37 tests), and the source check and strict build pass on the real site.
