"""Source check: asserts on the violations reported for fixture content directories.

Each directory under source_fixtures/ holds content that breaks exactly one rule
(or none, for `valid`). Tests look only at which file is reported and why.
"""

from pathlib import Path

import pytest

from source_check import check_content

FIXTURES = Path(__file__).parent / "source_fixtures"
ALLOWED = ["engineering", "machine-learning", "career", "notes"]


def violations(kind: str) -> list[tuple[str, str]]:
    """(file name, reason) for every violation found in a fixture directory."""
    return [(v.path.name, v.reason) for v in check_content(FIXTURES / kind, ALLOWED)]


def test_valid_content_has_no_violations() -> None:
    assert violations("valid") == []


def test_invalid_yaml_front_matter_is_reported() -> None:
    found = violations("invalid_yaml")
    assert len(found) == 1
    name, reason = found[0]
    assert name == "broken.md"
    assert "front matter" in reason and "YAML" in reason


@pytest.mark.parametrize(
    ("kind", "name", "field"),
    [
        ("missing_date", "no-date.md", "date"),
        ("missing_title", "no-title.md", "title"),
        ("missing_categories", "no-categories.md", "categories"),
    ],
)
def test_missing_required_field_is_reported(kind: str, name: str, field: str) -> None:
    found = violations(kind)
    assert len(found) == 1
    assert found[0][0] == name
    assert f"missing {field}" in found[0][1]


@pytest.mark.parametrize(
    ("kind", "name", "expected"),
    [
        ("bad_date", "bad-date.md", "malformed date"),
        ("bad_draft", "bad-draft.md", "draft must be true or false"),
        ("bad_category", "bad-category.md", "category 'not-allowed' is not allowed"),
    ],
)
def test_invalid_field_value_is_reported(kind: str, name: str, expected: str) -> None:
    found = violations(kind)
    assert len(found) == 1
    assert found[0][0] == name
    assert expected in found[0][1]


@pytest.mark.parametrize(
    ("kind", "name", "expected"),
    [
        ("phone_number", "phone.md", "phone number"),
        ("street_address", "address.md", "street address"),
    ],
)
def test_personal_data_pattern_is_reported(kind: str, name: str, expected: str) -> None:
    found = violations(kind)
    assert len(found) == 1
    assert found[0][0] == name
    assert expected in found[0][1]


def test_markdown_style_violation_is_reported() -> None:
    found = violations("bad_markdown")
    assert len(found) == 1
    name, reason = found[0]
    assert name == "skipped-heading.md"
    assert "heading" in reason.lower()
