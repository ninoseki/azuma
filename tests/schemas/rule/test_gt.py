import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: gt
detection:
  foo:
    a|gt: 10
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": 11}, True),
        ({"a": 10}, False),
        ({"a": 9}, False),
    ],
)
def test_gt(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
