---
title: Projects section with card grid
status: ready-for-agent
blocked-by: [01, 05]
---

# 06: Projects section with card grid

**What to build:** The author adds a project by creating one Markdown file with standard front matter. The Projects index shows every project as a card (title, summary, tech), with no hand-editing of the index. Each card links to the project's case-study page, which links out to the repo and demo where they exist.

See the spec: Content model (Projects).

**Blocked by:** 01 (Site skeleton that builds, with a check command), 05 (Source Markdown check for posts)

**Status:** ready-for-agent

- [ ] Project front matter: `title` (string), `summary` (one-line string), `tech` (list of strings), `links` (optional `repo` and `demo` URLs), `featured` (boolean) and optional `cover` (image path).
- [ ] The project page body template guides a short case study: problem, what was built, result.
- [ ] The Projects index renders every project as a grid card automatically. If Zensical can't generate this without Python, document the chosen approach and its trade-off in an ADR.
- [ ] The source check validates project front matter: required fields, types and URL shape.
- [ ] Built-site check: every project fixture appears as a card on the Projects index, and an invalid project fixture fails the source check.
- [ ] `featured` is accepted but not yet used by any page.
- [ ] At least one real or placeholder project exists.
