import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "aa\nbb"}, True),
        ({"a": "foo\naa"}, True),
        ({"a": "bar\naa"}, True),
        ({"a": "a\na"}, False),
        ({"a": "b\nb"}, False),
    ],
)
def test_with_multi_line(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    - aa
    - bb
  condition: foo
""")
    assert rule.match(event) is expected
