import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: re
detection:
  selection:
    a|re: ^foo$
  condition: selection
logsource:
  category: test
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo"}, True),
        ({"a": "Foo"}, False),
        ({"a": "foobar"}, False),
    ],
)
def test_re(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected


@pytest.fixture
def rule_with_i():
    return schemas.Rule.model_validate_yaml(
        """
title: re
detection:
  selection:
    a|re|i: ^foo$
  condition: selection
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
def test_re_with_i(event: dict, expected: bool, rule_with_i: schemas.Rule):
    assert rule_with_i.match(event) is expected


@pytest.fixture
def rule_with_m():
    return schemas.Rule.model_validate_yaml(
        """
title: re
detection:
  selection:
    a|re|m: X
  condition: selection
logsource:
  category: test
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "A\nB\nX"}, True),
        ({"a": "foobar"}, False),
    ],
)
def test_re_with_m(event: dict, expected: bool, rule_with_m: schemas.Rule):
    assert rule_with_m.match(event) is expected


@pytest.fixture
def re_with_multi_sub_modifiers():
    return schemas.Rule.model_validate_yaml(
        """
title: re
detection:
  selection:
    a|re|i|m|s: fo.bar
  condition: selection
logsource:
  category: test
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foobar"}, True),
        ({"a": "FOOBAR"}, True),
        ({"a": "Foo"}, False),
        ({"a": "Fo\nbar"}, True),
    ],
)
def test_re_with_multi_sub_modifiers(
    event: dict, expected: bool, re_with_multi_sub_modifiers: schemas.Rule
):
    assert re_with_multi_sub_modifiers.match(event) is expected
