import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"foo": "bar"}, True),
        ({"foo": "Bar"}, True),
        ({"foo": "BAR"}, True),
        ({"foo": "baz"}, False),
    ],
)
def test_match(event: dict, expected: bool):
    rule = build_rule(
        """
detection:
  foo:
    - bar
  condition: foo
"""
    )
    assert rule.match(event) is expected
