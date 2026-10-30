"""Built-site check for social cards and Open Graph metadata on the fixture site."""

import re
from pathlib import Path

import pytest

FIXTURE_SITE_URL = "https://fixture.example.com/portfolio/"
CARDS_DIR = "assets/images/social"
POSTS = [
    ("PUBLISHED-BODY-MARKER", "Published fixture post"),
    ("OLDER-BODY-MARKER", "Older published fixture post"),
]


def _meta_tags(html: str) -> dict[str, str]:
    """Every <meta property|name=... content=...> in the page, whatever the attribute order."""
    tags: dict[str, str] = {}
    for tag in re.findall(r"<meta\s[^>]*>", html):
        key = re.search(r'(?:property|name)="([^"]*)"', tag)
        content = re.search(r'content="([^"]*)"', tag)
        if key and content:
            tags[key.group(1)] = content.group(1)
    return tags


def _post_page(site_text: dict[Path, str], marker: str) -> str:
    """The post's own page: the only page under blog/ with a post URL carrying the body marker."""
    pages = [
        text
        for path, text in site_text.items()
        if path.suffix == ".html"
        and path.parts[:1] == ("blog",)
        and "archive" not in path.parts
        and "page" not in path.parts
        and marker in text
    ]
    assert len(pages) == 1
    return pages[0]


@pytest.mark.parametrize(("marker", "title"), POSTS)
def test_published_post_has_open_graph_and_twitter_metadata(
    site_text: dict[Path, str], marker: str, title: str
) -> None:
    meta = _meta_tags(_post_page(site_text, marker))
    assert title in meta["og:title"]
    assert meta["og:description"]
    assert meta["twitter:card"] == "summary_large_image"
    assert meta["og:image"].startswith(FIXTURE_SITE_URL)
    assert meta["og:image"] != FIXTURE_SITE_URL


@pytest.mark.parametrize(("marker", "title"), POSTS)
def test_published_post_has_a_generated_card_image(
    built_site: Path, site_text: dict[Path, str], marker: str, title: str
) -> None:
    image_url = _meta_tags(_post_page(site_text, marker))["og:image"]
    card = built_site / image_url.removeprefix(FIXTURE_SITE_URL)
    assert card.is_file()
    assert card.stat().st_size > 0


def test_every_card_belongs_to_a_built_page_so_hidden_posts_get_none(
    built_site: Path, site_text: dict[Path, str], fixture_dir: Path
) -> None:
    # Guard against vacuous passes: the hidden post's source exists, and cards were made.
    assert (fixture_dir / "content/blog/posts/hidden-post.md").is_file()
    cards = {
        p.relative_to(built_site).as_posix()
        for p in (built_site / CARDS_DIR).rglob("*")
        if p.is_file()
    }
    assert cards

    referenced = {
        _meta_tags(text)["og:image"].removeprefix(FIXTURE_SITE_URL)
        for path, text in site_text.items()
        if path.suffix == ".html" and "og:image" in _meta_tags(text)
    }
    # A card whose page was not built (a hidden post) would be left unreferenced.
    assert cards - referenced == set()
    assert not [card for card in cards if "hidden" in card]
