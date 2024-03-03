import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: startswith
detection:
  foo:
    a|startswith: foo
  condition: foo
logsource:
  category: test
    """
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo", "b": "bar", "c": "baz"}, True),
        ({"a": "foo"}, True),
        ({"a": "foobar"}, True),
        ({"b": "bar"}, False),
        ({"a": "bar", "b": "foo"}, False),
    ],
)
def test_startswith(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
