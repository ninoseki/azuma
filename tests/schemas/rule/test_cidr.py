import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: cidr
detection:
  foo:
    a|cidr: 192.168.0.0/24
  condition: foo
logsource:
  category: test
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "192.168.0.1"}, True),
        ({"a": "127.0.0.1"}, False),
    ],
)
def test_cidr(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
