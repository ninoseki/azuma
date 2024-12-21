import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: exists
detection:
  foo:
    a|exists: true
  bar:
    b|exists: false
  baz:
    c|exists: true
  condition: (foo or bar) and baz
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo"}, False),
        ({"a": "foo", "b": "bar"}, False),
        ({"b": "foo"}, False),
        ({"d": "foo"}, False),
        ({"c": "foo"}, True),
        ({"a": "foo", "c": "foo"}, True),
    ],
)
def test_exists(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
