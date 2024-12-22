import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"x": "a*ba"}, False),
        ({"x": "aba"}, False),
        ({"x": "a?a"}, False),
        ({"x": "a*a"}, True),
    ],
)
def test_escaped_wildcards_with_literal_starts(event: dict, expected: bool):
    rule = build_rule(
        r"""
detection:
  field:
    x: a\*a
  condition: field
"""
    )
    assert rule.match(event) is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"x": "a*ba"}, False),
        ({"x": "aba"}, False),
        ({"x": "a?a"}, True),
        ({"x": "a*a"}, False),
    ],
)
def test_escaped_wildcards_with_literal_question(event: dict, expected: bool):
    rule = build_rule(
        r"""
detection:
  field:
    x: a\?a
  condition: field
    """
    )
    assert rule.match(event) is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"x": "a*ba"}, True),
        ({"x": "aba"}, True),
        ({"x": "a?a"}, True),
        ({"x": "a*a"}, True),
    ],
)
def test_escaped_wildcards_with_star(event: dict, expected: bool):
    rule = build_rule(
        """
detection:
  field:
    x: a*a
  condition: field
"""
    )
    assert rule.match(event) is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"x": "a*ba"}, False),
        ({"x": "aba"}, True),
        ({"x": "a?a"}, True),
        ({"x": "a*a"}, True),
    ],
)
def test_escaped_wildcards_with_question(event: dict, expected: bool):
    rule = build_rule(
        """
detection:
  field:
    x: a?a
  condition: field
    """
    )
    assert rule.match(event) is expected
