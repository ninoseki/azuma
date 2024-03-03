import pytest

from azuma import schemas


@pytest.fixture
def all_of_them_rule():
    return schemas.Rule.model_validate_yaml(
        """
title: sample signature
logsource:
  category: test
detection:
    a: ["a"]
    b: ["b"]
    condition: all of them
    """
    )


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
def test_all_of_them(event: dict, expected: bool, all_of_them_rule: schemas.Rule):
    assert all_of_them_rule.match(event) is expected


@pytest.fixture
def all_of_x_rule():
    return schemas.Rule.model_validate_yaml(
        """
title: sample signature
logsource:
  category: test
detection:
    aa: ["aa"]
    ab: ["ab"]
    ba: ["ba"]
    bb: ["bb"]
    condition: all of a*
    """
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"log": "aa"}, False),
        ({"log": "1ab ba ca"}, False),
        ({"log": "ba"}, False),
        ({"log": "aabb"}, True),
    ],
)
def test_all_of_x(event: dict, expected: bool, all_of_x_rule: schemas.Rule):
    assert all_of_x_rule.match(event) is expected
