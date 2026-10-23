# yh-portfolio

Personal portfolio and blog, written in Markdown and built with [Zensical](https://zensical.org).

## Setup

Requires [uv](https://docs.astral.sh/uv/). Python 3.12 is pinned in `.python-version`.

```sh
uv sync
```

A fresh clone plus `uv sync` reproduces the locked environment (`uv.lock`).

## Preview

```sh
make serve
```

Starts the live-reload preview server (default http://localhost:8000).

## Check

```sh
make check
```

Runs the source Markdown check on the real and fixture content, then a strict build of
the real site (so a broken internal link fails it), then the tests. The tests include
the built-site check, which builds a separate fixture project in `tests/fixture_site/`
and asserts on its generated output only.

## Deploy

`.github/workflows/docs.yml` runs `make check` on every pull request and on every push
to `main`. A push to `main` then builds the site with `--strict --clean` and deploys it
to GitHub Pages, but only if `check` passed. Pull requests never deploy. The workflow
installs the locked `uv` environment without caching, as the Zensical docs advise.

The site is served at `https://<github-user>.github.io/yh-portfolio/`. The base URL is
the single `site_url` value in `zensical.toml`.

## Custom domain

To move to a custom domain later:

1. Change `site_url` in `zensical.toml` to the new address (for example
   `https://example.com/`).
2. Add a `CNAME` file containing the bare domain (`example.com`) to `content/`, so it
   is copied to the site root on every build.
3. Add the DNS record at your registrar, then set the custom domain in the repo's
   Settings → Pages. See the
   [GitHub Pages docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

## Upgrading Zensical

Zensical is alpha and pinned to an exact version in `pyproject.toml`.

```sh
uv lock --upgrade-package zensical
uv sync
make check
make refresh-docs
```

Merge the upgrade only if `make check` passes. Rebuild with `--clean` after upgrading
(`make check` already does).

## Docs for reference

```sh
make refresh-docs
```

Keeps local, gitignored copies of the docs in `references/`. Refresh them about weekly
and after every Zensical upgrade. Each folder has a `.refreshed` file recording the
upstream commit and the date.

- `references/zensical-docs/`: the [Zensical docs](https://github.com/zensical/docs).
- `references/mkdocs-material/`: the reference and setup pages of the
  [Material for MkDocs docs](https://squidfunk.github.io/mkdocs-material/reference/),
  as background. Zensical is its successor.

To add another source, add a line to the list in `scripts/refresh-docs.sh`.

## Layout

- `zensical.toml`: site config (content lives in `content/`, not the repo root)
- `content/`: Markdown pages
- `tools/`: the source check (`source_check.py`)
- `tests/`: the source check and built-site check, with their fixtures
- `scripts/`: helper scripts (`refresh-docs.sh`)
- `.github/workflows/`: CI and deploy (`docs.yml`)
