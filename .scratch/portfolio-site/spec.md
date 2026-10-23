---
title: Personal portfolio + blog on Zensical
status: ready-for-agent
blocked-by: []
---

## Problem Statement

I want a personal site that does three jobs at once: show recruiters and hiring managers who I am and what I've built, give peers and the tech community a blog worth reading and following, and give me a place to write and keep things for myself. I want to write everything in Markdown, keep it in git, and use Zensical (the successor to Material for MkDocs) rather than a heavier web framework. I also want control over when an article is public: I need to be able to keep an article unreleased, either on its own branch or on `main`, without it showing up anywhere on the public site.

## Solution

A Markdown-based static site built with Zensical, using the `modern` theme and Zensical's default homepage for now, deployed to GitHub Pages from a public repo named `yh-portfolio`. The site has four sections: Home, Projects, Blog and About.

- **Blog**: uses Zensical's native blog plugin. A post is either **published** or **hidden** (`draft: true`). Hidden posts never appear on the built site. New posts are written on `post/<slug>` branches and published by merging a PR into `main`. Posts are organised by a fixed list of categories plus free-form tags. RSS feeds and social cards are on.
- **Projects**: one page per project with structured front matter, shown as a card grid on the Projects index.
- **About**: the CV itself, in Markdown, with an optional PDF download.

Two automated checks protect the site. The first lints the **source Markdown** (front matter, allowed values, no forbidden personal data). The second inspects the **built site** (what a visitor or crawler actually sees). Both run locally and in CI, and a failure blocks deployment.

The first real content is part 1 of an example series on time series foundation models. It exists mainly to exercise the whole pipeline.

## User Stories

### Visitors: recruiters and hiring managers

1. As a recruiter, I want the homepage to tell me who the author is and what they do within seconds, so that I can decide quickly whether to look further.
2. As a recruiter, I want a Projects section listing the author's work as cards, so that I can scan their experience at a glance.
3. As a recruiter, I want each project card to show a title, a one-line summary and the technologies used, so that I can match projects to the role I'm hiring for.
4. As a recruiter, I want each project to have its own page with a short case study (problem, what was built, result), so that I can judge depth, not just breadth.
5. As a recruiter, I want links to a project's repository and demo where they exist, so that I can verify the work.
6. As a recruiter, I want an About page that works as a CV (experience, skills, background), so that I don't need to request a separate document.
7. As a recruiter, I want an optional PDF version of the CV, so that I can attach it to an internal hiring pipeline.
8. As a recruiter, I want visible links to GitHub, LinkedIn and email, so that I can contact the author.
9. As a recruiter on my phone, I want the site to be readable on a small screen, so that I can review it between meetings.

### Visitors: peers and the tech community

10. As a peer, I want a Blog section listing published posts newest first, so that I can see what the author has been writing.
11. As a peer, I want each post to show its date, author, categories and tags, so that I can judge relevance and freshness.
12. As a peer, I want to browse posts by category, so that I can follow the broad topics I care about.
13. As a peer, I want to browse posts by tag, so that I can find every post about a specific technology.
14. As a peer, I want an archive of posts by date, so that I can explore older writing.
15. As a peer, I want paginated blog listings, so that the index stays fast as the blog grows.
16. As a peer, I want post excerpts on the blog index, so that I can decide what to read without opening every post.
17. As a peer, I want an estimated reading time on posts, so that I can decide when to read them.
18. As a peer, I want an RSS feed, so that I can follow the blog in my reader.
19. As a peer sharing a post on LinkedIn or X, I want a generated preview image and title, so that the share looks good and gets clicks.
20. As a peer, I want posts in a series to link to each other, so that I can read the series in order.
21. As a reader, I want full-text search across the site, so that I can find a topic quickly.
22. As a reader, I want a dark mode that follows my system preference and can be toggled, so that reading is comfortable.
23. As a reader of technical posts, I want well-rendered code blocks (with syntax highlighting and copy buttons), admonitions, tables and maths, so that technical content is easy to follow.
24. As a reader, I want internal links to always work, so that I never land on a missing page.

### Author: writing and publishing

25. As the author, I want to write every page and post in Markdown, so that I can use my normal editor and tools.
26. As the author, I want to start a new post on its own `post/<slug>` branch, so that unfinished work stays off `main`.
27. As the author, I want to publish a post by merging its PR into `main`, so that publishing is a deliberate, reviewable act recorded in git history.
28. As the author, I want to mark a post `draft: true` and have it disappear from the public site entirely (its page, the indexes, archive, categories, tags, RSS and search), so that I can keep an unreleased article on `main` safely.
29. As the author, I want hidden posts to remain visible in local preview, so that I can review them as they'll look when published.
30. As the author, I want to unpublish a post by setting it back to `draft: true`, so that taking something down is a one-line change.
31. As the author, I want to keep genuinely sensitive drafts on local, unpushed branches, so that they never reach the public repo.
32. As the author, I want a fixed list of allowed categories, with the build failing on anything else, so that I don't end up with near-duplicates like `dev` and `development`.
33. As the author, I want free-form tags, so that I can label posts precisely without editing a central list.
34. As the author, I want to control the excerpt shown on the blog index with a "more" marker, so that each listing reads well.
35. As the author, I want to define my author profile once and reference it from posts, so that author details stay consistent.
36. As the author, I want to group posts into a series with consistent naming and cross-links, so that multi-part articles hold together.

### Author: projects and about

37. As the author, I want to add a project by creating one Markdown file with standard front matter (`title`, `summary`, `tech`, `links`, `featured`, optional `cover`), so that adding work is quick and consistent.
38. As the author, I want the Projects index to show every project as a card without hand-editing the index, so that new projects appear automatically.
39. As the author, I want a `featured` flag on projects now, even though nothing reads it yet, so that the future custom homepage can use it without my editing every project.
40. As the author, I want to maintain my CV as the About page, so that it stays current and searchable.
41. As the author, I want to optionally attach a CV PDF, so that I can offer a downloadable version.

### Author: quality and safety checks

42. As the author, I want a source-Markdown check that fails when a post is missing required front matter (title, date, categories), so that broken posts never reach the site.
43. As the author, I want the source check to fail when a post uses a category outside the allowed list, so that I find out before building.
44. As the author, I want the source check to fail when a project is missing required front matter or has values of the wrong type, so that the Projects grid never breaks.
45. As the author, I want the source check to fail on malformed front matter (invalid YAML, unknown status values, a non-boolean `draft`), so that typos don't silently publish or hide something.
46. As the author, I want the source check to flag patterns that look like phone numbers or home addresses in public content, so that I don't leak personal data from a public repo.
47. As the author, I want Markdown style linting (headings, lists, line formatting), so that content stays consistent.
48. As the author, I want a built-site check proving hidden posts are absent from every page, feed and the search index, so that I can trust `draft: true`.
49. As the author, I want a built-site check proving published posts appear in the blog index, their categories, their tags and the RSS feed, so that publishing really works.
50. As the author, I want the build to run in strict mode so that broken internal links fail it, so that readers never hit dead links.
51. As the author, I want a built-site check that Home, Projects, Blog and About exist and that every project appears as a card, so that structural regressions are caught.
52. As the author, I want a built-site check that posts carry social-card images and Open Graph metadata, so that sharing never silently breaks.
53. As the author, I want all checks to use their own small test fixtures instead of my real content, so that they keep passing as I add, hide or delete real posts.
54. As the author, I want one command to run every check locally, so that I can verify before pushing.
55. As the author, I want CI to run the same checks on every PR and before every deploy, so that `main` and the live site are never broken.

### Author: tooling, deployment and maintenance

56. As the author, I want Zensical pinned to an exact version via `uv` with a lockfile, so that local and CI builds are identical and alpha churn only arrives when I choose it.
57. As the author, I want to upgrade Zensical deliberately with one command and have the checks confirm nothing broke, so that I get new features safely.
58. As the author, I want a local preview server with live reload, so that I see changes as I write.
59. As the author, I want the site deployed to GitHub Pages automatically when `main` changes, so that publishing needs no manual step.
60. As the author, I want the site to launch at the GitHub Pages project address now, with a clear path to a custom domain later, so that I'm not blocked on buying a domain.
61. As the author, I want the site's base URL to be one config value, so that switching to a custom domain is a small change.

### Example content

62. As the author, I want part 1 of a time series foundation model series (how they work, the main models and ecosystem) to be the first post through the full branch → draft → PR → publish flow, so that the pipeline is proven end to end with realistic content.
63. As the author, I want that first post to exercise categories, tags, code blocks, maths, an excerpt and social cards, so that the test covers every feature the blog relies on.

## Implementation Decisions

### Platform and tooling

- **Generator:** Zensical, pinned to an exact version (0.0.71 at the time of writing), Python 3.12, managed with `uv` and a committed lockfile. The native `zensical.toml` config format is used, not `mkdocs.yml`.
- **Project scaffold:** start from `zensical new`, then adapt its generated config and GitHub Actions workflow. Zensical requires the content directory to be a subdirectory, not the repo root.
- **Theme:** the `modern` variant. The palette has light and dark schemes, follows the system preference and has a toggle.
- **Homepage:** Zensical's default homepage behaviour for now, with a short intro and links. A custom homepage template is explicitly deferred.

### Content model

- **Sections:** Home, Projects, Blog and About, as top-level navigation.
- **Blog:** Zensical's native blog plugin.
  - Each post's front matter has `date` (required), optional `updated`, `authors`, `categories` and `tags`, plus `draft` (boolean).
  - Authors are defined once in the blog's authors file.
  - The category allow-list is enforced by the blog plugin: `engineering`, `machine-learning`, `career` and `notes` initially. The list is editable.
  - Pagination, archive and reading time are on. Excerpts use the "more" marker.
- **Post states:** exactly two. **Published** means no `draft` field, or `draft: false`. **Hidden** means `draft: true`. There is no "archived" state.
- **Publishing workflow:** a post is written on a `post/<slug>` branch and published by merging its PR into `main`. A hidden post may also live on `main`. The repo is public, so "hidden" means "not on the site", not "secret". Sensitive drafts stay on local, unpushed branches.
- **Tags:** the native tags plugin, with tag listing pages.
- **Series:** posts in a series share a tag and a consistent title prefix, and link to each other explicitly. No series plugin is used.
- **Projects:** one Markdown page per project with this front matter:
  - `title` (string)
  - `summary` (string, one line)
  - `tech` (list of strings)
  - `links` (a map with optional `repo` and `demo` URLs)
  - `featured` (boolean)
  - `cover` (optional image path)

  The body is a short case study: problem, what was built, result. The Projects index renders every project as a card grid, using Zensical's grid cards.
- **About:** the CV in Markdown, with an optional link to a CV PDF stored as a site asset. No phone number or home address appears anywhere in the repo.

### Site features

- **RSS:** the native RSS plugin is enabled for blog posts.
- **Social cards:** the native social plugin is enabled. It requires `site_url`.
- **Search:** the built-in client-side search is enabled. Hidden posts must not be in the search index.
- **Markdown extensions:** enough to cover code highlighting with copy buttons, admonitions, tables, maths, and the attribute-list and Markdown-in-HTML extensions needed for grid cards.
- **Not enabled:** comments and analytics.

### Hosting and deployment

- **Repo:** public, named `yh-portfolio`. The local folder is renamed from `cactus` by the author after this spec.
- **Hosting:** GitHub Pages with GitHub Actions as the source, initially at the project address `<github-user>.github.io/yh-portfolio`. `site_url` is the single place to change when a custom domain is added; a custom domain also needs a CNAME file and a DNS record.
- **CI:** a workflow that installs the locked environment with `uv`, runs both checks, builds with `--strict` and `--clean`, and deploys only from `main`. PRs run the checks but do not deploy. Zensical's docs advise against CI caching for now.
- **Issue tracker:** stays local markdown. Switching to GitHub Issues once the remote exists is optional and separate.

### Check modules

There are two test seams, with one command that runs both.

1. **Source check.** It reads Markdown files and their front matter. Its input is a content directory plus the category allow-list; its output is a list of violations, and it exits non-zero if there are any. It enforces:
   - Required post fields, and the `date` format.
   - That `draft` is a boolean.
   - That categories are in the allow-list.
   - The project front matter schema, including field types.
   - That front matter is valid YAML.
   - Forbidden personal-data patterns (phone numbers, street addresses) in public content.
   - Markdown style lint.
2. **Built-site check.** It runs a strict build of a fixture project and inspects the generated output directory, never the config or templates. It enforces:
   - That hidden-post fixtures are absent from every HTML page, the RSS feed(s) and the search index.
   - That published-post fixtures appear on the blog index, their category pages, their tag pages and in RSS.
   - That a post with a disallowed category fails the build.
   - That the Home, Projects, Blog and About pages exist.
   - That every project fixture appears as a card on the Projects index.
   - That social-card images and Open Graph and Twitter meta tags are present on posts.
   - That broken internal links fail the strict build.

## Testing Decisions

- **What makes a good test:** it asserts only on externally observable behaviour.
  - The source check asserts on the violations it reports for given Markdown inputs.
  - The built-site check asserts on what is present or absent in the generated site, the way a visitor, feed reader or crawler would see it.
  - Neither asserts on Zensical's config structure, template internals or plugin implementation, so the tests survive Zensical upgrades and future theme or homepage customisation.
- **Fixtures, not real content:** both checks run against dedicated fixture content: published posts, hidden posts, a post with a bad category, valid and invalid projects, and a file containing a fake phone number. Adding, hiding or deleting real posts never breaks a test.
- **Real content is also checked:** the source check runs over the real content directory too, and the real site is built in strict mode, so real posts get the same front matter and link guarantees.
- **Modules tested:** the source check and the built-site check, which are the only two seams. The ideal would be one seam; the source seam was added at the author's request to catch problems before building.
- **Regression use:** the built-site check is the safety net for upgrading Zensical. Upgrade the pinned version, run the checks, and merge only if they pass.
- **Prior art:** none. This is a greenfield repo, and these checks establish the pattern.

## Out of Scope

- A custom homepage template and a custom visual design. These get their own grilling session.
- Automatically listing latest posts and featured projects on the homepage. This was decided (automatic), but is blocked on the custom homepage.
- Buying and configuring a custom domain.
- Comments (Giscus) and analytics (privacy-friendly, e.g. GoatCounter, later).
- Multiple languages.
- A private-repo setup for truly private drafts.
- Research for the time series foundation model series, parts 2 and 3, and the zero-shot experiment. These happen after the site is set up.
- Migrating the issue tracker to GitHub Issues.

## Further Notes

- **Zensical is alpha (0.0.x)** and releases every few days.
  - Unlisted MkDocs plugins and unsupported settings are silently ignored. Treat the built-site check as the source of truth after any upgrade.
  - No "last updated from git" dates, no image optimisation and no privacy plugin yet.
  - Templates are MiniJinja and cannot call Python, which matters for the future custom homepage.
  - After upgrading, build with `--clean`.
- **Material for MkDocs** is in maintenance mode, with critical fixes ending around November 2026. Zensical reads `mkdocs.yml` too, so content is portable either way.
- **The example series** is "Time series foundation models", in 3 parts:
  1. How they work, and the ecosystem
  2. Best practices, for practitioners and a general technical audience
  3. Risks, limits and scaling

  Part 1 is the pipeline test. It may start rough as a draft and be polished before publishing.
- **Sources for Zensical facts:**
  - zensical.org/docs (setup/blog, setup/tags, customization, publish-your-site, compatibility/mkdocs/plugins)
  - zensical.org/roadmap
  - github.com/zensical/zensical/releases (v0.0.64 blog, v0.0.65 rss, v0.0.67 social)
