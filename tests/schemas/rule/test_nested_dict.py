import pytest

from azuma import schemas


@pytest.fixture
def nested_rule():
    return schemas.Rule.parse_raw(
        """
title: sample signature
logsource:
    category: test
detection:
    field:
        foo:
            bar: a
    condition: field
    """
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"foo": {"bar": "a"}}, True),
        ({"foo": {"bar": "b"}}, False),
        ({"foo": "bar"}, False),
        ({"log": "a"}, False),
    ],
)
def test_nested_dict(event: dict, expected: bool, nested_rule: schemas.Rule):
    assert nested_rule.match(event) is expected


@pytest.fixture
def nested_with_wildcard_rule():
    return schemas.Rule.parse_raw(
        """
title: sample signature
logsource:
    category: test
detection:
    field:
        foo:
            bar*: a
    condition: field
    """
    )


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
def test_nested_dict_with_wildcard(
    event: dict, expected: bool, nested_with_wildcard_rule: schemas.Rule
):
    assert nested_with_wildcard_rule.match(event) is expected
