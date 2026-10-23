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


@pytest.fixture(scope="session")
def built_site() -> Path:
    subprocess.run(
        [str(ZENSICAL), "build", "--strict", "--clean"],
        cwd=FIXTURE,
        check=True,
    )
    return FIXTURE / "site"


@pytest.mark.parametrize("section", SECTION_PAGES)
def test_section_page_exists(built_site: Path, section: str) -> None:
    assert (built_site / SECTION_PAGES[section]).is_file()
