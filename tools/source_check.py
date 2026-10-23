"""Source check: lints the Markdown source of the site before it is built.

Input is a content directory and the category allow-list; output is a list of
violations. Run as a script, it exits non-zero if there are any.
"""

import datetime
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

import yaml
from pymarkdown.api import PyMarkdownApi

POSTS_DIR = Path("blog") / "posts"
LINT_CONFIG = Path(__file__).parent.parent / ".pymarkdown.json"
H1 = re.compile(r"^# \S", re.MULTILINE)

# Separated digit groups, e.g. +1 (555) 010-0199 or 555-010-0199. ISO dates
# (2026-01-15) don't match because their last group is too short.
PHONE = re.compile(r"(?<!\d)(?:\+\d{1,3}[\s.-]?)?(?:\(\d{2,4}\)|\d{2,4})[\s.-]\d{3,4}[\s.-]\d{3,4}(?!\d)")
# House number, one to three capitalised words, then a street type.
STREET = re.compile(
    r"\b\d{1,5}\s+(?:[A-Z][a-z]+\s+){1,3}"
    r"(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Way|Court|Ct)\b"
)


@dataclass(frozen=True)
class Violation:
    path: Path
    reason: str


def split_front_matter(text: str) -> tuple[str | None, str]:
    """The raw front matter block (None if absent) and the body after it."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4 :]


def check_post(
    path: Path, meta: dict, body: str, allowed_categories: list[str]
) -> list[Violation]:
    found: list[Violation] = []
    if "date" not in meta:
        found.append(Violation(path, "post is missing date"))
    elif not isinstance(meta["date"], datetime.date):  # YAML parses ISO dates itself
        found.append(Violation(path, f"malformed date {meta['date']!r} (use YYYY-MM-DD)"))
    if "title" not in meta and not H1.search(body):
        found.append(Violation(path, "post is missing title (no title field or # heading)"))
    if "draft" in meta and not isinstance(meta["draft"], bool):
        found.append(Violation(path, f"draft must be true or false, got {meta['draft']!r}"))
    categories = meta.get("categories")
    if not categories:
        found.append(Violation(path, "post is missing categories"))
    else:
        for category in categories:
            if category not in allowed_categories:
                found.append(Violation(path, f"category {category!r} is not allowed"))
    return found


def check_personal_data(path: Path, text: str) -> list[Violation]:
    found: list[Violation] = []
    if match := PHONE.search(text):
        found.append(Violation(path, f"looks like a phone number: {match.group().strip()!r}"))
    if match := STREET.search(text):
        found.append(Violation(path, f"looks like a street address: {match.group()!r}"))
    return found


def check_style(path: Path) -> list[Violation]:
    result = PyMarkdownApi().configuration_file_path(str(LINT_CONFIG)).scan_path(str(path))
    return [
        Violation(
            path,
            f"markdown style {f.rule_id} {f.rule_name} (line {f.line_number}): "
            f"{f.rule_description}",
        )
        for f in result.scan_failures
    ]


def check_content(content_dir: Path, allowed_categories: list[str]) -> list[Violation]:
    found: list[Violation] = []
    for path in sorted(content_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        raw, body = split_front_matter(text)
        meta: dict = {}
        if raw is not None:
            try:
                loaded = yaml.safe_load(raw)
            except yaml.YAMLError:
                found.append(Violation(path, "front matter is not valid YAML"))
                continue
            meta = loaded if isinstance(loaded, dict) else {}
        if path.relative_to(content_dir).is_relative_to(POSTS_DIR):
            found.extend(check_post(path, meta, body, allowed_categories))
        found.extend(check_personal_data(path, text))
        found.extend(check_style(path))
    return found


def main(argv: list[str]) -> int:
    """Check the content of the project described by a zensical.toml (default: ./zensical.toml)."""
    config_path = Path(argv[1] if len(argv) > 1 else "zensical.toml")
    project = tomllib.loads(config_path.read_text(encoding="utf-8"))["project"]
    content_dir = (config_path.parent / project["docs_dir"]).resolve()
    allowed = project["plugins"]["blog"]["categories_allowed"]
    violations = check_content(content_dir, allowed)
    for v in violations:
        print(f"{v.path}: {v.reason}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
