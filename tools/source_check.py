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
PROJECTS_DIR = Path("projects")
LINT_CONFIG = Path(__file__).parent.parent / ".pymarkdown.json"
H1 = re.compile(r"^# \S", re.MULTILINE)
URL = re.compile(r"https?://[^\s/$.?#][^\s]*")
CODE_FENCE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)

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
    """The raw front matter block (None if absent or never closed) and the body after it."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4 :]


def without_code_blocks(text: str) -> str:
    return CODE_FENCE.sub("", text)


def check_post(
    path: Path, meta: dict, body: str, allowed_categories: list[str]
) -> list[Violation]:
    found: list[Violation] = []
    if "date" not in meta:
        found.append(Violation(path, "post is missing date"))
    elif not isinstance(meta["date"], datetime.date):  # YAML parses ISO dates itself
        found.append(Violation(path, f"malformed date {meta['date']!r} (use YYYY-MM-DD)"))
    if "title" not in meta and not H1.search(without_code_blocks(body)):
        found.append(Violation(path, "post is missing title (no title field or # heading)"))
    if "draft" in meta and not isinstance(meta["draft"], bool):
        found.append(Violation(path, f"draft must be true or false, got {meta['draft']!r}"))
    categories = meta.get("categories")
    if not categories:
        found.append(Violation(path, "post is missing categories"))
    elif not isinstance(categories, list):
        found.append(Violation(path, f"categories must be a list, got {categories!r}"))
    else:
        for category in categories:
            if category not in allowed_categories:
                found.append(Violation(path, f"category {category!r} is not allowed"))
    return found


def check_project(path: Path, meta: dict) -> list[Violation]:
    found: list[Violation] = []
    for field in ("title", "summary", "tech", "featured"):
        if field not in meta:
            found.append(Violation(path, f"project is missing {field}"))
    for field in ("title", "summary"):
        value = meta.get(field)
        if value is None:
            continue
        if not isinstance(value, str):
            found.append(Violation(path, f"{field} must be a string, got {value!r}"))
        elif field == "summary" and "\n" in value.strip():
            found.append(Violation(path, "summary must be one line"))
    tech = meta.get("tech")
    if tech is not None and not (
        isinstance(tech, list) and tech and all(isinstance(t, str) for t in tech)
    ):
        found.append(Violation(path, f"tech must be a list of strings, got {tech!r}"))
    if "featured" in meta and not isinstance(meta["featured"], bool):
        found.append(Violation(path, f"featured must be true or false, got {meta['featured']!r}"))
    links = meta.get("links")
    if links is not None:
        if not isinstance(links, dict):
            found.append(Violation(path, f"links must be a mapping, got {links!r}"))
        else:
            for key, url in links.items():
                if key not in ("repo", "demo"):
                    found.append(Violation(path, f"links.{key} is not a known link (use repo or demo)"))
                elif not (isinstance(url, str) and URL.fullmatch(url)):
                    found.append(Violation(path, f"links.{key} must be an http(s) URL, got {url!r}"))
    cover = meta.get("cover")
    if cover is not None and not isinstance(cover, str):
        found.append(Violation(path, f"cover must be an image path, got {cover!r}"))
    return found


def check_personal_data(path: Path, text: str) -> list[Violation]:
    found: list[Violation] = []
    prose = without_code_blocks(text)
    if match := PHONE.search(prose):
        found.append(Violation(path, f"looks like a phone number: {match.group().strip()!r}"))
    if match := STREET.search(prose):
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


def is_project_page(path: Path, content_dir: Path) -> bool:
    relative = path.relative_to(content_dir)
    return relative.is_relative_to(PROJECTS_DIR) and relative.name != "index.md"


def check_content(content_dir: Path, allowed_categories: list[str]) -> list[Violation]:
    found: list[Violation] = []
    for path in sorted(content_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        raw, body = split_front_matter(text)
        meta: dict = {}
        if raw is None and text.startswith("---\n"):
            found.append(Violation(path, "front matter is not closed (missing closing ---)"))
            continue
        if raw is not None:
            try:
                loaded = yaml.safe_load(raw)
            except yaml.YAMLError:
                found.append(Violation(path, "front matter is not valid YAML"))
                continue
            if loaded is not None and not isinstance(loaded, dict):
                found.append(Violation(path, "front matter is not valid YAML key/value pairs"))
                continue
            meta = loaded or {}
        if path.relative_to(content_dir).is_relative_to(POSTS_DIR):
            found.extend(check_post(path, meta, body, allowed_categories))
        elif is_project_page(path, content_dir):
            found.extend(check_project(path, meta))
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
