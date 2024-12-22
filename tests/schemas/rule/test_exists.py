import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo"}, False),
        ({"a": "foo", "b": "bar"}, False),
        ({"b": "foo"}, False),
        ({"d": "foo"}, False),
        ({"c": "foo"}, True),
        ({"a": "foo", "c": "foo"}, True),
    ],
)
def test_exists(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|exists: true
  bar:
    b|exists: false
  baz:
    c|exists: true
  condition: (foo or bar) and baz
""")
    assert rule.match(event) is expected
