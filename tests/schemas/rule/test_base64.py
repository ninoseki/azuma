import base64

import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.parse_raw(
        """
title: base64
detection:
  foo:
    a|base64: foo
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": base64.encodebytes(b"foo").decode()}, True),
        ({"a": base64.b64encode(b"foo").decode()}, True),
        ({"a": "foo"}, False),
    ],
)
def test_base64(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
