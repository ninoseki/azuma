import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foobar"}, True),
        ({"a": "foo"}, False),
        ({"a": "bar"}, False),
    ],
)
def test_all(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|contains|all:
      - foo
      - bar
  condition: foo
    """)
    assert rule.match(event) is expected
