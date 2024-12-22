import pytest

from azuma import schemas
from tests.utils import build_rule


@pytest.fixture
def rule():
    return build_rule(
        """
detection:
  foo:
    a|windash: " -f "
  condition: foo
"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": " -f "}, True),
        ({"a": " /f "}, True),
        ({"a": "foo"}, False),
    ],
)
def test_windash(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
