import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": 11}, True),
        ({"a": 10}, False),
        ({"a": 9}, False),
    ],
)
def test_gt(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|gt: 10
  condition: foo
""")
    assert rule.match(event) is expected
