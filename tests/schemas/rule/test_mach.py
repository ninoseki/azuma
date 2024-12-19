import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: test
detection:
  foo:
    - bar
  condition: foo
logsource:
  category: test
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"foo": "bar"}, True),
        ({"foo": "Bar"}, True),
        ({"foo": "BAR"}, True),
        ({"foo": "baz"}, False),
    ],
)
def test_match(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected


def test_match_with_list(rule: schemas.Rule):
    with pytest.raises(ValueError):
        rule.match([])  # type: ignore
