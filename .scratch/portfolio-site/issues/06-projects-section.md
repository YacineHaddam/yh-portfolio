---
title: Projects section with card grid
status: done
blocked-by: [01, 05]
---

# 06: Projects section with card grid

**What to build:** The author adds a project by creating one Markdown file with standard front matter. The Projects index shows every project as a card (title, summary, tech), with no hand-editing of the index. Each card links to the project's case-study page, which links out to the repo and demo where they exist.

See the spec: Content model (Projects).

**Blocked by:** 01 (Site skeleton that builds, with a check command), 05 (Source Markdown check for posts)

**Status:** done

- [x] Project front matter: `title` (string), `summary` (one-line string), `tech` (list of strings), `links` (optional `repo` and `demo` URLs), `featured` (boolean) and optional `cover` (image path).
- [x] The project page body template guides a short case study: problem, what was built, result.
- [x] The Projects index renders every project as a grid card automatically. If Zensical can't generate this without Python, document the chosen approach and its trade-off in an ADR.
- [x] The source check validates project front matter: required fields, types and URL shape.
- [x] Built-site check: every project fixture appears as a card on the Projects index, and an invalid project fixture fails the source check.
- [x] `featured` is accepted but not yet used by any page.
- [x] At least one real or placeholder project exists.

## Comments

### 2026-10-22

Implemented: the `macros` plugin renders the card grid (`project_cards()`) and each project's repo and demo links (`project_links()`), from `tools/project_cards.py` through a root `main.py`. Jinja runs only on `projects/*.md`, so `{{ }}` in posts or the CV is never evaluated. The choice and its trade-off are in `docs/adr/0001-project-cards-use-the-macros-plugin.md`. The source check has a `check_project` rule set (required `title`, `summary`, `tech`, `featured`; types; one-line `summary`; `links` keys limited to `repo` and `demo` and values must be http(s) URLs; `cover` a string). There are fixtures for each failure kind under `tests/source_fixtures/project_*`, two project fixtures plus a generated index in `tests/fixture_site`, `templates/project.md` as the case-study template, and one placeholder project in `content/projects/`.

Verified: `make check` passes (source check on real and fixture content, strict build, 46 tests). Built-site tests assert that each fixture project is a card with its summary and tech linking to its own page, that the project page shows its repo and demo links, that a project without links has none, and that no template text is left on the index. The real site renders the placeholder card and its page. The macros spike also confirmed that `navigation` and `files` are empty in the macro, so the macro reads the files from disk.

Notes and not verified:
- The placeholder project has no `links`, because I did not want to invent a repo URL. Replace it with a real project.
- `cover` is validated as a string but not rendered on the card. The ticket only asks for it to be accepted.
- Cards are sorted by file name. Nothing reads `featured`, as the ticket says.
- `templates/project.md` is outside `content/`, so it is not built or source-checked. The case-study headings are guidance only; the source check does not require them.
- The visual look of the grid was not checked in a browser. The tests check the HTML.
- The `main.py` in the repo root and in `tests/fixture_site/` add `tools/` to `sys.path` and re-export `define_env`. Zensical's loading of `main.py` from the project directory is covered by the built-site tests, not by the docs.
- Not committed yet: `git` fails in the agent sandbox on `/etc/gitconfig` (`Operation not permitted`).
