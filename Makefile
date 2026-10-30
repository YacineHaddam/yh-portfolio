.PHONY: serve check refresh-docs

serve:
	uv run zensical serve

# Python lint, then the source Markdown check of the real and fixture content, then a
# strict build of the real site (broken internal links fail it), then the tests (the
# built-site check against its fixture project, plus the source check's own tests).
check:
	uv run ruff check .
	uv run python tools/source_check.py zensical.toml
	uv run python tools/source_check.py tests/fixture_site/zensical.toml
	uv run zensical build --strict --clean
	uv run pytest

# Local copy of the Zensical docs, for reference (gitignored).
refresh-docs:
	bash scripts/refresh-docs.sh
