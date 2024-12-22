import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "192.168.0.1"}, True),
        ({"a": "127.0.0.1"}, False),
    ],
)
def test_cidr(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|cidr: 192.168.0.0/24
  condition: foo""")
    assert rule.match(event) is expected
