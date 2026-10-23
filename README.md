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

## Zensical docs for reference

```sh
make refresh-docs
```

Keeps a local, gitignored copy of the [Zensical docs](https://github.com/zensical/docs)
in `references/zensical-docs/`. Refresh it about weekly and after every Zensical upgrade.
`references/zensical-docs/.refreshed` records the upstream commit and the date.

## Layout

- `zensical.toml`: site config (content lives in `content/`, not the repo root)
- `content/`: Markdown pages
- `tools/`: the source check (`source_check.py`)
- `tests/`: the source check and built-site check, with their fixtures
- `scripts/`: helper scripts (`refresh-docs.sh`)
