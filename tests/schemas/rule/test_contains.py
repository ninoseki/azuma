import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo", "b": "bar", "c": "baz"}, True),
        ({"a": "foo"}, True),
        ({"a": "FOO"}, True),
        ({"a": "Foo"}, True),
        ({"b": "bar"}, False),
        ({"a": "bar", "b": "foo"}, False),
    ],
)
def test_contains(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|contains: foo
  condition: foo""")
    assert rule.match(event) is expected
