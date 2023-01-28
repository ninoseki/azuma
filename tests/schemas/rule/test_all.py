import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.parse_raw(
        """
title: all
detection:
  foo:
    a|contains|all:
      - foo
      - bar
  condition: foo
logsource:
  category: test
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foobar"}, True),
        ({"a": "foo"}, False),
        ({"a": "bar"}, False),
    ],
)
def test_all(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
