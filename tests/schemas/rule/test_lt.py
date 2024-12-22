import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": 11}, False),
        ({"a": 10}, False),
        ({"a": 9}, True),
    ],
)
def test_lt(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|lt: 10
  condition: foo
""")
    assert rule.match(event) is expected
