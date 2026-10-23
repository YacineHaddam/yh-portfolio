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

Runs a strict build of the real site, so a broken internal link fails it, then the
built-site tests. Those build a separate fixture project in `tests/fixture_site/` and
assert on its generated output only.

## Upgrading Zensical

Zensical is alpha and pinned to an exact version in `pyproject.toml`.

```sh
uv lock --upgrade-package zensical
uv sync
make check
```

Merge the upgrade only if `make check` passes. Rebuild with `--clean` after upgrading
(`make check` already does).

## Layout

- `zensical.toml`: site config (content lives in `content/`, not the repo root)
- `content/`: Markdown pages
- `tests/`: built-site check and its fixture project
