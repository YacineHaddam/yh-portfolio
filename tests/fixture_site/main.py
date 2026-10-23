"""Entry point for the `macros` plugin: the Projects index macro lives in tools/."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

from project_cards import define_env  # noqa: E402,F401
