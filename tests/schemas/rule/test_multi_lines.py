import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: startswith
detection:
  foo:
    - aa
    - bb
  condition: foo
logsource:
  category: test
    """
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "aa\nbb"}, True),
        ({"a": "foo\naa"}, True),
        ({"a": "bar\naa"}, True),
        ({"a": "a\na"}, False),
        ({"a": "b\nb"}, False),
    ],
)
def test_with_multi_line(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
