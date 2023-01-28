import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.parse_raw(
        """
title: endswith
detection:
  foo:
    a|endswith: foo
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo", "b": "bar", "c": "baz"}, True),
        ({"a": "foo"}, True),
        ({"a": "bar_foo"}, True),
        ({"a": "foobar"}, False),
        ({"b": "bar"}, False),
        ({"a": "bar", "b": "foo"}, False),
    ],
)
def test_endswith(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
