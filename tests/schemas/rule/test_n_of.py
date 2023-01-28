import pytest

from azuma import schemas


@pytest.fixture
def one_of_them_rule():
    return schemas.Rule.parse_raw(
        """
title: sample signature
logsource:
    category: test
detection:
    a: ["a"]
    b: ["b"]
    condition: 1 of them
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"log": "a"}, True),
        ({"log": "b"}, True),
        ({"log": "ab"}, True),
        ({"log": "c"}, False),
    ],
)
def test_1_of_them(event: dict, expected: bool, one_of_them_rule: schemas.Rule):
    assert one_of_them_rule.match(event) is expected


@pytest.fixture
def two_of_them_rule():
    return schemas.Rule.parse_raw(
        """
title: sample signature
logsource:
    category: test
detection:
    a: ["a"]
    b: ["b"]
    condition: 2 of them
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"log": "a"}, False),
        ({"log": "b"}, False),
        ({"log": "ab"}, True),
        ({"log": "c"}, False),
    ],
)
def test_2_of_them(event: dict, expected: bool, two_of_them_rule: schemas.Rule):
    assert two_of_them_rule.match(event) is expected


@pytest.fixture
def one_of_x_rule():
    return schemas.Rule.parse_raw(
        """
title: sample signature
logsource:
  category: test
detection:
    aa: ["aa"]
    ab: ["ab"]
    ba: ["ba"]
    bb: ["bb"]
    condition: 1 of a*
    """
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"log": "ab"}, True),
        ({"log": "1ab ba ca"}, True),
        ({"log": "ba"}, False),
        ({"log": "aabb"}, True),
    ],
)
def test_1_of_x(event: dict, expected: bool, one_of_x_rule: schemas.Rule):
    assert one_of_x_rule.match(event) is expected
