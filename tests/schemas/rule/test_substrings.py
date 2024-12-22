import pytest

from tests.utils import build_rule


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
def test_substrings(event: dict, expected: bool):
    rule = build_rule(
        """
detection:
  signs:
    - "red things"
    - "blue things"
  condition: signs
    """
    )
    assert rule.match(event) is expected
