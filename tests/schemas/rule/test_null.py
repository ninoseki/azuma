import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"y": "found"}, True),
        ({"z": "found"}, False),
        ({"y": "found", "x": "also"}, False),
    ],
)
def test_null_and_not_null(event: dict, expected: bool):
    rule = build_rule("""
detection:
  forbid:
    x: null
  filter:
    y: null
  condition: forbid and not filter
""")
    assert rule.match(event) is expected
