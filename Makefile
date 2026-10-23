.PHONY: serve check

serve:
	uv run zensical serve

# Strict build of the real site (broken internal links fail it), then the
# built-site check against its fixture project.
check:
	uv run zensical build --strict --clean
	uv run pytest
