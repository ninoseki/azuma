import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "FOO"}, False),
        ({"a": "foo"}, True),
        ({"a": "Foo"}, False),
    ],
)
def test_cased(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|cased: foo
  condition: foo""")
    assert rule.match(event) is expected
