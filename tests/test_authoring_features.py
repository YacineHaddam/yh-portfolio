"""Built-site check for the authoring features posts rely on: highlighted code with a
copy button, admonitions, tables and maths. Asserts on the fixture site's output only."""

import re
from pathlib import Path

import pytest

PAGE = Path("authoring/index.html")


def test_code_block_is_highlighted_with_a_copy_button(
    site_text: dict[Path, str],
) -> None:
    page = site_text[PAGE]
    assert "FIXTURE-CODE-MARKER" in page
    assert re.search(r'class="[^"]*\bhighlight\b[^"]*"', page)
    assert "language-python" in page
    assert "content.code.copy" in page


def test_admonition_is_rendered(site_text: dict[Path, str]) -> None:
    page = site_text[PAGE]
    assert 'class="admonition note"' in page
    assert "FIXTURE-ADMONITION-MARKER" in page


def test_table_is_rendered(site_text: dict[Path, str]) -> None:
    page = site_text[PAGE]
    assert "<table>" in page
    assert "FIXTURE-TABLE-MARKER" in page


def test_maths_is_marked_up_for_the_renderer(site_text: dict[Path, str]) -> None:
    page = site_text[PAGE]
    assert 'class="arithmatex"' in page
    assert r"\(E = mc^2\)" in page
    assert r"\frac{n(n+1)}{2}" in page


@pytest.mark.parametrize("script", ["javascripts/mathjax.js", "tex-mml-chtml.js"])
def test_maths_renderer_is_loaded_by_the_page(
    site_text: dict[Path, str], script: str
) -> None:
    assert script in site_text[PAGE]


def test_mathjax_config_is_published(built_site: Path) -> None:
    assert (built_site / "javascripts/mathjax.js").is_file()
