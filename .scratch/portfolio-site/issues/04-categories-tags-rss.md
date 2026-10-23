---
title: Categories, tags and RSS
status: ready-for-agent
blocked-by: [03]
---

# 04: Categories, tags and RSS

**What to build:** Readers can browse posts by category (from a fixed allow-list) and by free-form tag, and follow the blog through an RSS feed. Hidden posts stay out of all of them. Using a category outside the allow-list fails the build.

See the spec: Content model (Blog, Tags); Site features (RSS).

**Blocked by:** 03 (Blog with published and hidden posts)

**Status:** ready-for-agent

- [ ] Category allow-list starts as `engineering`, `machine-learning`, `career` and `notes`, and is easy to edit.
- [ ] Each category has a listing page. The native tags plugin gives each tag a listing page.
- [ ] The native RSS plugin produces a feed of published posts.
- [ ] Built-site check: the published fixture appears on its category page, its tag page(s) and in the RSS feed.
- [ ] Built-site check: the hidden fixture appears in no category page, tag page or feed.
- [ ] Built-site check: a fixture post with a disallowed category makes the build fail.
- [ ] Posts show their categories and tags.
