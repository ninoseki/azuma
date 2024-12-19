import pytest
import regex as re

from azuma.parsers.detection import base64offset_modifier, sigma_string_to_regex


@pytest.mark.parametrize(
    "v,expected",
    [
        (r".", r"\."),
        (r"*", r".*"),
        (r"?", r"."),
        (r".\*", r"\.\*"),
        (r".\?", r"\.\?"),
        (r".\*abc", r"\.\*abc"),
        (r".\*abc*", r"\.\*abc.*"),
        (r".\*abc?", r"\.\*abc."),
        (r".\*abc\?", r"\.\*abc\?"),
        (r".\*abc\\?", r"\.\*abc\\."),
        (r".\*abc\\\?", r"\.\*abc\\\\."),
    ],
)
def test_sigma_string_to_regex(v: str, expected: str):
    assert sigma_string_to_regex(v) == expected


@pytest.mark.parametrize(
    "v,expected",
    [
        (r"a\a", r"a\a"),
        (r"a\\a", r"a\\a"),
        (r"a\*a", "a*a"),
        (r"a*a", r"a a bunch of garbage a"),
    ],
)
def test_sigma_string_to_regex_with_fullmatch(v: str, expected: str):
    assert re.compile(sigma_string_to_regex(v)).fullmatch(expected)


def test_base64offset_modifier():
    assert (
        base64offset_modifier("/bin/bash") == "(L2Jpbi9iYXNo|9iaW4vYmFza|vYmluL2Jhc2)"
    )
