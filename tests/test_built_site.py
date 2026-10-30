"""Built-site check: builds a fixture project and asserts on the generated output.

Only the generated output directory is inspected, never the config or templates,
so these tests survive Zensical upgrades. The shared fixtures are in conftest.py.
"""

from pathlib import Path

import pytest

SECTION_PAGES = {
    "Home": "index.html",
    "Projects": "projects/index.html",
    "Blog": "blog/index.html",
    "About": "about/index.html",
}


@pytest.mark.parametrize("section", SECTION_PAGES)
def test_section_page_exists(built_site: Path, section: str) -> None:
    assert (built_site / SECTION_PAGES[section]).is_file()


def test_published_post_has_its_own_page(site_text: dict[Path, str]) -> None:
    pages = [
        path
        for path, text in site_text.items()
        if path.suffix == ".html" and "PUBLISHED-BODY-MARKER" in text
    ]
    assert len(pages) == 1


def test_blog_index_shows_excerpt_author_and_reading_time(
    site_text: dict[Path, str],
) -> None:
    index = site_text[Path("blog/index.html")]
    assert "Published fixture post" in index
    assert "PUBLISHED-EXCERPT-MARKER" in index
    assert "PUBLISHED-BODY-MARKER" not in index
    assert "Fixture Author" in index
    assert "min read" in index


def test_blog_index_paginates_newest_first(site_text: dict[Path, str]) -> None:
    first = site_text[Path("blog/index.html")]
    second = site_text[Path("blog/page/2/index.html")]
    assert "Published fixture post" in first
    assert "Older published fixture post" not in first
    assert "Older published fixture post" in second


def test_published_posts_are_in_archive(site_text: dict[Path, str]) -> None:
    archive = site_text[Path("blog/archive/2026/index.html")] + site_text[
        Path("blog/archive/2026/page/2/index.html")
    ]
    assert "Published fixture post" in archive
    assert "Older published fixture post" in archive


def test_published_post_is_in_search_index(site_text: dict[Path, str]) -> None:
    search = site_text[Path("search.json")]
    assert "Published fixture post" in search
    assert "PUBLISHED-BODY-MARKER" in search


@pytest.mark.parametrize(
    "needle",
    [
        "Hidden fixture post",
        "HIDDEN-EXCERPT-MARKER",
        "HIDDEN-BODY-MARKER",
        "hidden-fixture-post",
    ],
)
def test_hidden_post_appears_nowhere_in_built_site(
    site_text: dict[Path, str], fixture_dir: Path, needle: str
) -> None:
    # Guard against vacuous passes: the hidden post's source is part of the
    # fixture, and the blog it would have joined was built.
    assert (fixture_dir / "content/blog/posts/hidden-post.md").is_file()
    assert "Published fixture post" in site_text[Path("blog/index.html")]

    leaks = [str(path) for path, text in site_text.items() if needle in text]
    assert leaks == []


def test_published_post_is_on_its_category_page(site_text: dict[Path, str]) -> None:
    page = site_text[Path("blog/category/engineering/index.html")]
    assert "Published fixture post" in page


def test_published_post_is_on_its_tag_listing(site_text: dict[Path, str]) -> None:
    tags = site_text[Path("tags/index.html")]
    assert "published-fixture-tag" in tags
    assert "shared-fixture-tag" in tags
    assert "Published fixture post" in tags


def test_published_post_shows_categories_and_tags(site_text: dict[Path, str]) -> None:
    post = next(
        text
        for path, text in site_text.items()
        if path.suffix == ".html" and "PUBLISHED-BODY-MARKER" in text
    )
    assert "engineering" in post
    assert "published-fixture-tag" in post


def test_published_posts_are_in_rss_feed(site_text: dict[Path, str]) -> None:
    feed = site_text[Path("feed_rss_created.xml")]
    assert "Published fixture post" in feed
    assert "PUBLISHED-EXCERPT-MARKER" in feed


@pytest.mark.parametrize("needle", ["hidden-fixture-tag", "category/notes"])
def test_hidden_post_taxonomy_appears_nowhere(
    site_text: dict[Path, str], needle: str
) -> None:
    assert "Published fixture post" in site_text[Path("tags/index.html")]
    leaks = [str(path) for path, text in site_text.items() if needle in text]
    assert leaks == []


def test_disallowed_category_fails_the_build(build_strict, bad_category_dir: Path) -> None:
    result = build_strict(bad_category_dir, capture_output=True, text=True)
    assert result.returncode != 0
    assert "not-an-allowed-category" in result.stderr
    assert "outside categories_allowed" in result.stderr


@pytest.mark.parametrize(
    ("title", "summary", "tech", "page"),
    [
        ("Alpha fixture project", "ALPHA-SUMMARY-MARKER", "alpha-tech", "projects/alpha-project/index.html"),
        ("Beta fixture project", "BETA-SUMMARY-MARKER", "beta-tech", "projects/beta-project/index.html"),
    ],
)
def test_every_project_is_a_card_on_the_projects_index(
    site_text: dict[Path, str], title: str, summary: str, tech: str, page: str
) -> None:
    index = site_text[Path("projects/index.html")]
    assert "grid cards" in index
    assert title in index
    assert summary in index
    assert tech in index
    assert Path(page) in site_text
    assert f'href="{Path(page).parent.name}/"' in index


def test_project_page_links_out_to_repo_and_demo(site_text: dict[Path, str]) -> None:
    page = site_text[Path("projects/alpha-project/index.html")]
    assert "ALPHA-BODY-MARKER" in page
    assert "https://github.com/example/alpha" in page
    assert "https://example.com/alpha-demo" in page


def test_project_without_links_has_no_link_section(site_text: dict[Path, str]) -> None:
    page = site_text[Path("projects/beta-project/index.html")]
    assert "BETA-BODY-MARKER" in page
    assert "github.com/example" not in page


def test_projects_index_shows_no_unrendered_template(site_text: dict[Path, str]) -> None:
    assert "project_cards" not in site_text[Path("projects/index.html")]


@pytest.mark.parametrize(
    "link",
    [
        "https://github.com/fixture-user",
        "https://www.linkedin.com/in/fixture-user",
        "mailto:fixture@example.com",
    ],
)
def test_contact_links_render_on_every_page(
    site_text: dict[Path, str], link: str
) -> None:
    pages = {path: text for path, text in site_text.items() if path.suffix == ".html"}
    assert Path("about/index.html") in pages
    missing = [str(path) for path, text in pages.items() if f'href="{link}"' not in text]
    assert missing == []
