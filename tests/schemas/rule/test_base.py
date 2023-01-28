import pytest

from azuma import schemas


@pytest.fixture
def event():
    return {
        "cats": "good",
        "dogs": "good",
        "dog_count": 2,
        "birds": "many",
        "user": {"name": "foo"},
    }


@pytest.fixture
def base_signature():
    return """
title: sample signature
logsource:
    category: test
detection:
    true_expected: # dogs or dog_count
        - go?d
        - 2
    true_also_expected: # (dogs good or dogs ok) and cats good
        dogs:
            - good
            - ok
        cats: good
    true_cats_expected:
        cats: go*
    true_still_expected: # cats good or birds few
        - cats: good
        - birds: few
    false_expected: # frogs or trees
        - frogs
        - trees
    false_also_expected: # cats good and birds none
        cats: good
        birds: none
"""


@pytest.fixture
def complicated_condition(base_signature: str):
    return (
        base_signature
        + """
    condition: (all of true_*) and (1 of *_expected) and (1 of true_*) and not all of them and (all of them or true_expected)
"""
    )


def test_or_search(event: dict, base_signature: str):
    # Test a signature where the search block is just a list (or operation)
    # Also has an example of the ? wildcard embedded
    rule = schemas.Rule.parse_raw(base_signature + "    condition: true_expected")
    assert rule.match(event) is True


def test_value_or_search(event: dict, base_signature: str):
    # Test a signature where the search block has a list of values (or across those values)
    rule = schemas.Rule.parse_raw(base_signature + "    condition: true_also_expected")
    assert rule.match(event) is True


def test_value_wildcard_search(event: dict, base_signature: str):
    # has an example of the * wildcard embedded
    rule = schemas.Rule.parse_raw(base_signature + "    condition: true_cats_expected")
    assert rule.match(event) is True


def test_and_search(event: dict, base_signature: str):
    # Test a signature where the search block is just a map (and operation)
    rule = schemas.Rule.parse_raw(base_signature + "    condition: true_still_expected")
    assert rule.match(event) is True


def test_complicated_condition(event: dict, complicated_condition: str):
    rule = schemas.Rule.parse_raw(complicated_condition)
    assert rule.match(event) is True
