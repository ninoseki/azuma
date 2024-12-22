import base64

import pytest

from azuma import schemas


@pytest.fixture
def rule():
    return schemas.Rule.model_validate_yaml(
        """
title: base64offset
detection:
  foo:
    a|base64offset:
      - /bin/bash
      - /bin/sh
      - /bin/zsh
  condition: foo
logsource:
  category: test"""
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": base64.encodebytes(b"/bin/bash").decode()}, True),
        ({"a": base64.b64encode(b"/bin/sh").decode()}, True),
        ({"a": base64.encodebytes(b"/BIN/BASH").decode()}, False),
        ({"a": base64.b64encode(b"/BIN/SH").decode()}, False),
        ({"a": "L2Jpbi9iYXNo"}, True),
        ({"a": "9iaW4vYmFza"}, True),
        ({"a": "vYmluL2Jhc2"}, True),
        ({"a": "foo"}, False),
    ],
)
def test_base64offset(event: dict, expected: bool, rule: schemas.Rule):
    assert rule.match(event) is expected
