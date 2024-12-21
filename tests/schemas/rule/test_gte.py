import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: gte
detection:
  foo:
    a|gte: 10
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": 11}, True),
        ({"a": 10}, True),
        ({"a": 9}, False),
    ],
)
def test_gte(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
