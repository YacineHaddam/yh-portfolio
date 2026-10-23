---
title: Source Markdown check for posts
status: ready-for-agent
blocked-by: [04]
---

# 05: Source Markdown check for posts

**What to build:** Before building, `check` lints the source Markdown and reports every violation, with file and reason, in one pass. It catches broken or risky posts before Zensical runs. It covers both the fixture content and the real content.

See the spec: Check modules (Source check).

**Blocked by:** 04 (Categories, tags and RSS)

**Status:** ready-for-agent

- [ ] Input is a content directory and the category allow-list (one source of truth shared with the site config). Output is a list of violations, and it exits non-zero if there are any.
- [ ] It fails on: invalid YAML front matter, a missing `date`/`title`/`categories` on a post, a malformed date, a non-boolean `draft`, or a category not in the allow-list.
- [ ] It flags phone-number-like and street-address-like patterns in public content.
- [ ] It runs Markdown style linting (headings, lists, formatting) with a committed config.
- [ ] Fixtures exist for each failure kind. Tests assert on the reported violations, not on internals.
- [ ] `check` runs the source check first, then the builds, and CI picks it up with no workflow change.
- [ ] The real content passes.
