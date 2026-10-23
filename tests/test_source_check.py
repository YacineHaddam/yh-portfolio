"""Source check: asserts on the violations reported for fixture content directories.

Each directory under source_fixtures/ holds content that breaks exactly one rule
(or none, for `valid` and `crlf_valid`). Tests look only at which file is
reported and why.
"""

from pathlib import Path

import pytest

from source_check import check_content

FIXTURES = Path(__file__).parent / "source_fixtures"
ALLOWED = ["engineering", "machine-learning", "career", "notes"]


def violations(kind: str) -> list[tuple[str, str]]:
    """(file name, reason) for every violation found in a fixture directory."""
    return [(v.path.name, v.reason) for v in check_content(FIXTURES / kind, ALLOWED)]


@pytest.mark.parametrize("kind", ["valid", "crlf_valid"])
def test_valid_content_has_no_violations(kind: str) -> None:
    assert violations(kind) == []


def test_invalid_yaml_front_matter_is_reported() -> None:
    found = violations("invalid_yaml")
    assert len(found) == 1
    name, reason = found[0]
    assert name == "broken.md"
    assert "front matter" in reason and "YAML" in reason


@pytest.mark.parametrize(
    ("kind", "name", "expected"),
    [
        ("missing_date", "no-date.md", "missing date"),
        ("missing_title", "no-title.md", "missing title"),
        ("code_block_heading", "code-only.md", "missing title"),
        ("missing_categories", "no-categories.md", "missing categories"),
        ("unterminated_front_matter", "unterminated.md", "front matter is not closed"),
        ("scalar_categories", "scalar.md", "categories must be a list"),
        ("bad_date", "bad-date.md", "malformed date"),
        ("bad_draft", "bad-draft.md", "draft must be true or false"),
        ("bad_category", "bad-category.md", "category 'not-allowed' is not allowed"),
        ("phone_number", "phone.md", "phone number"),
        ("street_address", "address.md", "street address"),
        ("project_missing_summary", "no-summary.md", "project is missing summary"),
        ("project_bad_tech", "bad-tech.md", "tech must be a list of strings"),
        ("project_bad_featured", "bad-featured.md", "featured must be true or false"),
        ("project_bad_link", "bad-link.md", "links.repo must be an http(s) URL"),
        ("project_multiline_summary", "long-summary.md", "summary must be one line"),
    ],
)
def test_rule_violation_is_reported(kind: str, name: str, expected: str) -> None:
    found = violations(kind)
    assert len(found) == 1
    assert found[0][0] == name
    assert expected in found[0][1]
