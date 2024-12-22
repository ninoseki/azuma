import base64

import pytest

from tests.utils import build_rule


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
def test_base64offset(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|base64offset:
      - /bin/bash
      - /bin/sh
      - /bin/zsh
  condition: foo""")
    assert rule.match(event) is expected
