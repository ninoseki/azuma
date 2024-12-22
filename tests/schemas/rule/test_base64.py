import base64

import pytest

from tests.utils import build_rule


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": base64.encodebytes(b"foo").decode()}, True),
        ({"a": base64.b64encode(b"foo").decode()}, True),
        ({"a": base64.encodebytes(b"FOO").decode()}, False),
        ({"a": base64.b64encode(b"FOO").decode()}, False),
        ({"a": "foo"}, False),
    ],
)
def test_base64(event: dict, expected: bool):
    rule = build_rule("""
detection:
  foo:
    a|base64: foo
  condition: foo
    """)
    assert rule.match(event) is expected
