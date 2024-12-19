import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: exists
detection:
  foo:
    a|exists: null
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo"}, True),
        ({"a": "bar"}, True),
        ({"b": "bar"}, False),
    ],
)
def test_exists(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
