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

- [ ] The post is written on a `post/tsfm-part-1` branch, with `draft: true`, a category, tags (including a shared series tag), an excerpt marker, at least one code block and one maths expression.
- [x] The series convention is used: a shared tag, a consistent title prefix and a placeholder "next in series" link.
- [x] The PR passes `check` and is merged while still hidden. Verified: the post is absent from the live site, RSS and search.
- [ ] `draft` is removed in a follow-up PR. Verified: the post is live on the blog index, its category and tag pages, RSS and search, and its social card previews correctly.
- [x] Any friction found along the way is captured as a follow-up note for `/retro`.

## Comments

### 2026-10-25

Set up by the agent: the `post/tsfm-part-1` branch and `content/blog/posts/tsfm-part-1.md`, a skeleton with `draft: true`, category `machine-learning`, tags `time-series-foundation-models` and `forecasting`, the title prefix "Time series foundation models, part 1:", an excerpt marker, `TODO(author)` lines for every section, and one placeholder code block and one placeholder maths expression. The "next in series" line is plain text ("Part 2 … is coming soon"), not a link, because part 2 does not exist and a link to it would fail the strict build.

The post is still a skeleton, so the first criterion (the post is written) and the publish criterion are open and belong to the author. Both need the real text, and the placeholder code and maths replaced.

Verified: a strict build of the real site hides the draft: no file under `site/` mentions it. After the merge, the author checked the live site. Screenshots show the blog index listing only "Hello, world" and the RSS feed holding only that entry. The author reports the tags page and search are also clean. Not looked at: the category and archive pages. The merge itself is the author's report; I did not see the PR.

One anomaly: an earlier `site/` directory did contain the draft, with a page for it, the blog index and the search index. It was written in the same second as a `make check` build. A fresh `uv run zensical build --strict --clean` run afterwards did not contain it. The cause was not found. A preview server writing drafts into `site/` is the likely explanation, since VS Code held connections to port 8000, but nothing was listening when checked.

Friction found along the way, for `/retro`:

- The authoring extensions the spec promised (code highlighting with copy buttons, admonitions, tables, maths) had never been configured. Ticket 09 was the first thing to need them. They were added in `c25d1f3`.
- `md046` (code-block style) had to be turned off in `.pymarkdown.json`, because admonition bodies are indented and the linter reads them as code blocks.
- MathJax loads from unpkg at page view time, a third-party script on a public site. Pinned to 3.2.2.
- The footer contact links on the live site still point at the placeholders (`your-github-handle`, `your-linkedin-handle`, `you@example.com`) and the TODO comments in `zensical.toml` remain.
- GitHub rejected the first push because the commits carried a work email, which forced a rewrite of the whole local history before the repo went public.
- The agent's sandbox cannot run the real build, because the social plugin downloads its card font at build time, so every full `make check` needed the author to run it.
- The wizard skill's template was in a directory the agent could not read, so the publish wizard was written from scratch.
