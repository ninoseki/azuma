import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo", "b": "bar", "c": "baz"}, True),
        ({"a": "foo"}, True),
        ({"a": "FOO"}, True),
        ({"a": "Foo"}, True),
        ({"a": "bar_foo"}, True),
        ({"a": "foobar"}, False),
        ({"b": "bar"}, False),
        ({"a": "bar", "b": "foo"}, False),
    ],
)
def test_endswith(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|endswith: foo
  condition: foo""")
    assert rule.match(event) is expected
