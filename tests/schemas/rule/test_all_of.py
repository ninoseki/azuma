import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"log": "a"}, False),
        ({"log": "b"}, False),
        ({"log": "ab"}, True),
        ({"log": "bac"}, True),
        ({"log": "c"}, False),
    ],
)
def test_all_of_them(event: dict, expected: bool):
    rule = build_rule("""
detection:
    a: ["a"]
    b: ["b"]
    condition: all of them
""")
    assert rule.match(event) is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"log": "aa"}, False),
        ({"log": "1ab ba ca"}, False),
        ({"log": "ba"}, False),
        ({"log": "aabb"}, True),
    ],
)
def test_all_of_x(event: dict, expected: bool):
    rule = build_rule("""
detection:
  aa: ["aa"]
  ab: ["ab"]
  ba: ["ba"]
  bb: ["bb"]
  condition: all of a*
""")
    assert rule.match(event) is expected
