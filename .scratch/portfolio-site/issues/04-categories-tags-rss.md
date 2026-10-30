---
title: Categories, tags and RSS
status: done
blocked-by: [03]
---

# 04: Categories, tags and RSS

**What to build:** Readers can browse posts by category (from a fixed allow-list) and by free-form tag, and follow the blog through an RSS feed. Hidden posts stay out of all of them. Using a category outside the allow-list fails the build.

See the spec: Content model (Blog, Tags); Site features (RSS).

**Blocked by:** 03 (Blog with published and hidden posts)

- [x] Category allow-list starts as `engineering`, `machine-learning`, `career` and `notes`, and is easy to edit.
- [x] Each category has a listing page. The native tags plugin gives each tag a listing page.
- [x] The native RSS plugin produces a feed of published posts.
- [x] Built-site check: the published fixture appears on its category page, its tag page(s) and in the RSS feed.
- [x] Built-site check: the hidden fixture appears in no category page, tag page or feed.
- [x] Built-site check: a fixture post with a disallowed category makes the build fail.
- [x] Posts show their categories and tags.

## Comments

### 2026-10-21

Implemented: `categories_allowed` on the blog plugin (real and fixture configs), the tags and RSS plugins, a `tags.md` page holding the `<!-- material/tags -->` listing, categories and tags on the fixture posts and the placeholder post, a `tests/fixture_bad_category` project, and built-site tests.

Verified: `pytest` passes (20 tests) and `zensical build --strict` passes on the real site. The bad-category build fails with `outside categories_allowed`, and the test asserts the offending category is named. Category pages are at `/blog/category/<name>/`.

Notes and not verified:
- The tags plugin renders all tags on one `/tags/` page, with a section per tag, rather than a separate page per tag.
- The RSS feed is scoped to `blog/posts/.*` in both the real and fixture configs, so it holds posts only, not site pages. The real site build was checked: its feed holds only the placeholder post. The nav has a Tags entry. The feeds are `feed_rss_created.xml` and `feed_rss_updated.xml`.
- Builds need a time zone database. In the agent sandbox `/usr/share/zoneinfo` is unreadable, so the tests ran with `TZDIR` pointing at the `tzdata` package (added to `pyproject.toml`). Not checked without `TZDIR`, or in CI.
- The visual look of the categories and tags on a post was not checked in a browser. The tests only check that they are in the HTML.
