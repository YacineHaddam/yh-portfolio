---
title: Blog with published and hidden posts
status: ready-for-agent
blocked-by: [01]
---

# 03: Blog with published and hidden posts

**What to build:** The Blog section lists published posts newest first. Each listing shows its date, author, excerpt and reading time, and listings paginate. A post marked `draft: true` is **hidden**. It shows in local preview, but appears nowhere in the built site: not its own page, the blog index, the archive or the search index. The built-site check proves this with fixture posts.

See the spec: Content model (Blog, Post states).

**Blocked by:** 01 (Site skeleton that builds, with a check command)

**Status:** ready-for-agent

- [x] Zensical's native blog plugin is enabled. The author profile is defined once and referenced by posts.
- [x] Posts have `date` (required), optional `updated`, `authors` and an optional boolean `draft`.
- [x] The blog index shows excerpts cut at the "more" marker, plus reading time, and paginates.
- [x] A date-based archive exists.
- [x] The fixture project contains at least one published and one hidden post.
- [x] Built-site check: the published fixture appears on its own page, the blog index, the archive and the search index.
- [x] Built-site check: the hidden fixture's title and unique marker text appear in **no** generated HTML file and not in the search index.
- [ ] Verified manually: a hidden post is visible in local preview.
- [x] One placeholder real post exists so the real Blog section isn't empty.

## Comments

### 2026-10-21

Implemented: blog plugin enabled in the real and fixture configs (excerpts, pagination, archive, reading time), author defined once in `content/blog/.authors.yml`, a published and a hidden fixture post, a placeholder real post, and built-site tests.

Verified: `zensical build --strict` passes on the real site, and `pytest` passes (12 tests). Flipping the hidden fixture to `draft: false` made 3 of the hiding tests fail, so those tests do bite.

Not verified: that a hidden post shows in local preview. `zensical serve` was denied in the agent sandbox, so that criterion stays unticked and the ticket is not marked done.
