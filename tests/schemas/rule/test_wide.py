import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: wide
detection:
  foo:
    a|wide|base64offset: ping
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "cABpAG4AZw"}, True),
        ({"a": "AAaQBuAGcA"}, True),
        ({"a": "wAGkAbgBnA"}, True),
        ({"a": "foo"}, False),
    ],
)
def test_wide(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
