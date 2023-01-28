from pathlib import Path

import pytest

from azuma import schemas


@pytest.fixture
def rule_set():
    return schemas.RuleSet.from_dir("tests/fixtures")


@pytest.fixture
def paths():
    p = Path("tests/fixtures")
    return list(p.glob("**/*.yml"))


def test_rules(rule_set: schemas.RuleSet, paths: list[Path]):
    assert len(rule_set.rules) == len(paths)


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo", "b": "bar", "c": "baz"}, 1),
        ({"a": "foo"}, 1),
        ({"a": "foobar"}, 1),
        ({"b": "bar"}, 0),
        ({"a": "bar", "b": "foo"}, 0),
    ],
)
def test_match_all(rule_set: schemas.RuleSet, event: dict, expected: int):
    matched = rule_set.match_all(event)
    assert len(matched) == expected
