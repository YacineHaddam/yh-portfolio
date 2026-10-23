"""Source check as a command: exit status and output for a zensical.toml."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPT = ROOT / "tools" / "source_check.py"


def run_check(config: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(config)],
        capture_output=True,
        text=True,
    )


def test_fails_and_names_file_and_reason_for_a_bad_post() -> None:
    result = run_check(Path(__file__).parent / "source_cli_fixture" / "zensical.toml")
    assert result.returncode != 0
    assert "bad-category.md" in result.stdout
    assert "category 'not-allowed' is not allowed" in result.stdout


def test_real_content_passes() -> None:
    result = run_check(ROOT / "zensical.toml")
    assert result.stdout == ""
    assert result.returncode == 0
