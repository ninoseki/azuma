import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"Foo": "bar"}, True),
        ({"foo": "bar"}, False),
        ({"a": "bar", "b": "foo"}, False),
    ],
)
def test_selection(event: dict, expected: bool):
    rule = build_rule("""
detection:
  selection:
    Foo: bar
  condition: selection
""")
    assert rule.match(event) is expected
