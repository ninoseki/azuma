import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: lte
detection:
  foo:
    a|lte: 10
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": 11}, False),
        ({"a": 10}, True),
        ({"a": 9}, True),
    ],
)
def test_lte(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
