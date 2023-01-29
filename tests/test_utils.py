import pytest

from azuma.utils import normalize_event


@pytest.mark.parametrize(
    "event,expected", [({"a": "AAA"}, {"a": "aaa"}), ({"A": "AAA"}, {"A": "aaa"})]
)
def test_normalize_event(event: dict, expected: dict):
    assert normalize_event(event) == expected


@pytest.mark.parametrize(
    "event,expected",
    [
        (
            {"a": "AAA", "b": {"c": ["FOO", "BAR"], "d": {"e": ("FOO", "BAR")}}},
            {"a": "aaa", "b": {"c": ["foo", "bar"], "d": {"e": ("foo", "bar")}}},
        ),
    ],
)
def test_normalize_event_with_nested_event(event: dict, expected: dict):
    assert normalize_event(event) == expected
