import pytest

from azuma import schemas


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
    rule = schemas.Rule.parse_raw(
        r"""
title: literal_star
logsource:
  category: test
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
    rule = schemas.Rule.parse_raw(
        r"""
title: literal_question
logsource:
  category: test
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
    rule = schemas.Rule.parse_raw(
        """
title: star
logsource:
  category: test
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
    rule = schemas.Rule.parse_raw(
        """
title: question
logsource:
  category: test
detection:
    field:
        x: a?a
    condition: field
    """
    )
    assert rule.match(event) is expected
