import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.parse_raw(
        """
title: test
detection:
  foo:
    - bar
  condition: foo
logsource:
  category: test
"""
    )


def test_match_with_list(rule: schemas.Rule):
    with pytest.raises(ValueError):
        rule.match([])  # type: ignore
