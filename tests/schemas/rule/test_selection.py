import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: selection
detection:
  selection:
    Foo: bar
  condition: selection
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"Foo": "bar"}, True),
        ({"foo": "bar"}, False),
        ({"a": "bar", "b": "foo"}, False),
    ],
)
def test_selection(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
