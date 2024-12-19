import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: lt
detection:
  foo:
    a|lt: 10
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": 11}, False),
        ({"a": 10}, False),
        ({"a": 9}, True),
    ],
)
def test_lt(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
