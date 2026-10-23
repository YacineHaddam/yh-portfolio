"""Built-site check: builds a fixture project and asserts on the generated output.

Only the generated output directory is inspected, never the config or templates,
so these tests survive Zensical upgrades.
"""

import subprocess
import sys
from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixture_site"
ZENSICAL = Path(sys.executable).parent / "zensical"

SECTION_PAGES = {
    "Home": "index.html",
    "Projects": "projects/index.html",
    "Blog": "blog/index.html",
    "About": "about/index.html",
}

TEXT_SUFFIXES = {".html", ".json", ".xml", ".txt"}


@pytest.fixture(scope="session")
def built_site() -> Path:
    subprocess.run(
        [str(ZENSICAL), "build", "--strict", "--clean"],
        cwd=FIXTURE,
        check=True,
    )
    return FIXTURE / "site"


def _text_files(site: Path) -> dict[Path, str]:
    return {
        p.relative_to(site): p.read_text(encoding="utf-8")
        for p in sorted(site.rglob("*"))
        if p.is_file() and p.suffix in TEXT_SUFFIXES
    }


@pytest.mark.parametrize("section", SECTION_PAGES)
def test_section_page_exists(built_site: Path, section: str) -> None:
    assert (built_site / SECTION_PAGES[section]).is_file()


def test_published_post_has_its_own_page(built_site: Path) -> None:
    pages = [
        path
        for path, text in _text_files(built_site).items()
        if path.suffix == ".html" and "PUBLISHED-BODY-MARKER" in text
    ]
    assert len(pages) == 1


def test_blog_index_shows_excerpt_author_and_reading_time(built_site: Path) -> None:
    index = (built_site / "blog/index.html").read_text(encoding="utf-8")
    assert "Published fixture post" in index
    assert "PUBLISHED-EXCERPT-MARKER" in index
    assert "PUBLISHED-BODY-MARKER" not in index
    assert "Fixture Author" in index
    assert "min read" in index


def test_published_post_is_in_archive(built_site: Path) -> None:
    archive = [
        text
        for path, text in _text_files(built_site).items()
        if path.suffix == ".html" and "archive" in path.parts
    ]
    assert archive, "no archive page generated"
    assert any("Published fixture post" in text for text in archive)


def test_published_post_is_in_search_index(built_site: Path) -> None:
    search = (built_site / "search.json").read_text(encoding="utf-8")
    assert "Published fixture post" in search
    assert "PUBLISHED-BODY-MARKER" in search


@pytest.mark.parametrize(
    "needle",
    [
        "Hidden fixture post",
        "HIDDEN-EXCERPT-MARKER",
        "HIDDEN-BODY-MARKER",
        "hidden-post",
    ],
)
def test_hidden_post_appears_nowhere_in_built_site(
    built_site: Path, needle: str
) -> None:
    leaks = [
        str(path) for path, text in _text_files(built_site).items() if needle in text
    ]
    assert leaks == []
