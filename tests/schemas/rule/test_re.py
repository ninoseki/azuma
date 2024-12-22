import pytest

from azuma import schemas
from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo"}, True),
        ({"a": "Foo"}, False),
        ({"a": "foobar"}, False),
    ],
)
def test_re(event: dict, expected: bool):
    rule = build_rule("""
detection:
  selection:
    a|re: ^foo$
  condition: selection
""")
    assert rule.match(event) is expected


@pytest.fixture
def rule_with_i():
    return schemas.Rule.model_validate_yaml(
        """
title: re

logsource:
  category: test
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo"}, True),
        ({"a": "Foo"}, True),
        ({"a": "foobar"}, False),
    ],
)
def test_re_with_i(event: dict, expected: bool):
    rule = build_rule("""
detection:
  selection:
    a|re|i: ^foo$
  condition: selection
""")
    assert rule.match(event) is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "A\nB\nX"}, True),
        ({"a": "foobar"}, False),
    ],
)
def test_re_with_m(event: dict, expected: bool):
    rule = build_rule("""
detection:
  selection:
    a|re|m: X
  condition: selection
""")
    assert rule.match(event) is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foobar"}, True),
        ({"a": "FOOBAR"}, True),
        ({"a": "Foo"}, False),
        ({"a": "Fo\nbar"}, True),
    ],
)
def test_re_with_multi_sub_modifiers(event: dict, expected: bool):
    rule = build_rule("""
detection:
  selection:
    a|re|i|m|s: fo.bar
  condition: selection
""")
    assert rule.match(event) is expected
