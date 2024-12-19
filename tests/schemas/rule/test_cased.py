import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: cased
detection:
  foo:
    a|cased: foo
  condition: foo
logsource:
  category: test
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "FOO"}, False),
        ({"a": "foo"}, True),
        ({"a": "Foo"}, False),
    ],
)
def test_cased(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
