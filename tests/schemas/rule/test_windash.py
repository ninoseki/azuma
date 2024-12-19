import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: windash
detection:
  foo:
    a|windash: " -f "
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": " -f "}, True),
        ({"a": " /f "}, True),
        ({"a": "foo"}, False),
    ],
)
def test_windash(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
