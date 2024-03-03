import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: re
detection:
  selection:
    a|re: ^foo$
  condition: selection
logsource:
  category: test
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo"}, True),
        ({"a": "foobar"}, False),
    ],
)
def test_re(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
