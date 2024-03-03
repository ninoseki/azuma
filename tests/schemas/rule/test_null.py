import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: sample signature
logsource:
  category: test
detection:
    forbid:
        x: null
    filter:
        y: null
    condition: forbid and not filter
    """
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"y": "found"}, True),
        ({"z": "found"}, False),
        ({"y": "found", "x": "also"}, False),
    ],
)
def test_null_and_not_null(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
