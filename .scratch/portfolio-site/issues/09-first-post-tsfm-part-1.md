---
title: First post (TSFM series part 1) through the full workflow
status: ready-for-human
blocked-by: [02, 04, 05, 08]
---

# 09: First post (TSFM series part 1) through the full workflow

**What to build:** Part 1 of the "Time series foundation models" series (how they work, plus the main models and ecosystem) goes through the real publishing workflow end to end. This proves that the branch → hidden → PR → publish flow works on the live site with realistic content.

The writing is the author's. An agent can set up the branch, the front matter, the series conventions and the verification steps.

See the spec: Example content; Further Notes (example series).

**Blocked by:** 02 (Deploy to GitHub Pages via CI), 04 (Categories, tags and RSS), 05 (Source Markdown check for posts), 08 (Social cards and Open Graph metadata)

**Status:** ready-for-human

- [ ] The post is written on a `post/tsfm-part-1` branch, with `draft: true`, a category, tags (including a shared series tag), an excerpt marker, at least one code block and one maths expression.
- [ ] The series convention is used: a shared tag, a consistent title prefix and a placeholder "next in series" link.
- [ ] The PR passes `check` and is merged while still hidden. Verified: the post is absent from the live site, RSS and search.
- [ ] `draft` is removed in a follow-up PR. Verified: the post is live on the blog index, its category and tag pages, RSS and search, and its social card previews correctly.
- [ ] Any friction found along the way is captured as a follow-up note for `/retro`.
