"""Shared fixtures for the built-site tests: the fixture project, built once per session."""

import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).parent
ZENSICAL = Path(sys.executable).parent / "zensical"
TEXT_SUFFIXES = {".html", ".json", ".xml", ".txt"}


@pytest.fixture(scope="session")
def fixture_dir() -> Path:
    return TESTS_DIR / "fixture_site"


@pytest.fixture(scope="session")
def bad_category_dir() -> Path:
    return TESTS_DIR / "fixture_bad_category"


@pytest.fixture(scope="session")
def build_strict() -> Callable[..., subprocess.CompletedProcess[str]]:
    """Run a strict, clean Zensical build in a project; extra kwargs go to subprocess.run."""

    def build(project: Path, **kwargs) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(ZENSICAL), "build", "--strict", "--clean"], cwd=project, **kwargs
        )

    return build


@pytest.fixture(scope="session")
def built_site(fixture_dir: Path, build_strict) -> Path:
    build_strict(fixture_dir, check=True)
    return fixture_dir / "site"


@pytest.fixture(scope="session")
def site_text(built_site: Path) -> dict[Path, str]:
    """Every text file in the built site, keyed by its path relative to the site."""
    return {
        p.relative_to(built_site): p.read_text(encoding="utf-8", errors="replace")
        for p in sorted(built_site.rglob("*"))
        if p.is_file() and p.suffix in TEXT_SUFFIXES
    }
