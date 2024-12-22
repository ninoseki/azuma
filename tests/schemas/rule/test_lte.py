import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": 11}, False),
        ({"a": 10}, True),
        ({"a": 9}, True),
    ],
)
def test_lte(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|lte: 10
  condition: foo
""")
    assert rule.match(event) is expected
