import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.parse_raw(
        """
title: sample signature
logsource:
  category: test
detection:
    signs:
        - "red things"
        - "blue things"
    condition: signs
    """
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        (
            {
                "log": "all sorts of red things and blue things were there",
            },
            True,
        ),
    ],
)
def test_substrings(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
