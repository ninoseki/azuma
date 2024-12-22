import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"foo": {"bar": "a"}}, True),
        ({"foo": {"bar": "b"}}, False),
        ({"foo": "bar"}, False),
        ({"log": "a"}, False),
    ],
)
def test_nested_dict(event: dict, expected: bool):
    rule = build_rule("""
detection:
  field:
    foo:
      bar: a
  condition: field
""")
    assert rule.match(event) is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"foo": {"bar": "a"}}, True),
        ({"foo": {"bar1": "a"}}, True),
        ({"foo": {"bar2": "a"}}, True),
        ({"foo": {"bar": "b"}}, False),
        ({"foo": "bar"}, False),
        ({"log": "a"}, False),
    ],
)
def test_nested_dict_with_wildcard(event: dict, expected: bool):
    rule = build_rule("""
detection:
  field:
    foo:
      bar*: a
  condition: field
""")
    assert rule.match(event) is expected
