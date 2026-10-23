"""Built-site check for social cards and Open Graph metadata on the fixture site."""

import re
from pathlib import Path

import pytest
from test_built_site import FIXTURE, built_site, site_text  # noqa: F401  (fixtures)

FIXTURE_SITE_URL = "https://fixture.example.com/portfolio/"
POST_MARKERS = ["PUBLISHED-BODY-MARKER", "OLDER-BODY-MARKER"]


def _post_html(site_text: dict[Path, str], marker: str) -> str:
    return next(
        text
        for path, text in site_text.items()
        if path.suffix == ".html" and marker in text
    )


def _meta(html: str, key: str) -> str:
    match = re.search(
        rf'<meta\s+(?:property|name)="{re.escape(key)}"\s+content="([^"]*)"', html
    )
    assert match, f"missing meta tag {key}"
    return match.group(1)


@pytest.mark.parametrize("marker", POST_MARKERS)
def test_published_post_has_open_graph_and_twitter_metadata(
    site_text: dict[Path, str], marker: str
) -> None:
    html = _post_html(site_text, marker)
    assert _meta(html, "og:title")
    assert _meta(html, "og:description")
    assert _meta(html, "twitter:card")
    assert _meta(html, "og:image").startswith(FIXTURE_SITE_URL)


@pytest.mark.parametrize("marker", POST_MARKERS)
def test_published_post_has_a_generated_card_image(
    built_site: Path, site_text: dict[Path, str], marker: str
) -> None:
    image_url = _meta(_post_html(site_text, marker), "og:image")
    card = built_site / image_url.removeprefix(FIXTURE_SITE_URL)
    assert card.is_file()
    assert card.stat().st_size > 0


def test_hidden_post_has_no_card_image(built_site: Path) -> None:
    assert (FIXTURE / "content/blog/posts/hidden-post.md").is_file()
    cards = [p.name for p in (built_site / "assets/images/social").rglob("*.png")]
    assert cards, "expected cards for published pages"
    assert not [name for name in cards if "hidden" in name]
