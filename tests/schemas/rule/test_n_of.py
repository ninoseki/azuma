import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"log": "a"}, True),
        ({"log": "b"}, True),
        ({"log": "ab"}, True),
        ({"log": "c"}, False),
    ],
)
def test_1_of_them(event: dict, expected: bool):
    rule = build_rule("""
detection:
  a: ["a"]
  b: ["b"]
  condition: 1 of them""")
    assert rule.match(event) is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"log": "a"}, False),
        ({"log": "b"}, False),
        ({"log": "ab"}, True),
        ({"log": "c"}, False),
    ],
)
def test_2_of_them(event: dict, expected: bool):
    rule = build_rule("""
detection:
  a: ["a"]
  b: ["b"]
  condition: 2 of them""")
    assert rule.match(event) is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"log": "ab"}, True),
        ({"log": "1ab ba ca"}, True),
        ({"log": "ba"}, False),
        ({"log": "aabb"}, True),
    ],
)
def test_1_of_x(event: dict, expected: bool):
    rule = build_rule("""
detection:
  aa: ["aa"]
  ab: ["ab"]
  ba: ["ba"]
  bb: ["bb"]
  condition: 1 of a*
""")
    assert rule.match(event) is expected
