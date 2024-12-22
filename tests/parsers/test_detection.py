from typing import Any

import pytest
import regex as re
from returns.result import safe

from azuma.parsers.detection import (
    apply_base64offset_modifier,
    apply_utf16_modifier,
    sigma_string_to_regex,
    validate_base64_sub_modifier_condition,
    validate_exists_modifier_condition,
    windash_generator,
)


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


def test_apply_base64offset_modifier():
    assert (
        apply_base64offset_modifier("/bin/bash")
        == "(L2Jpbi9iYXNo|9iaW4vYmFza|vYmluL2Jhc2)"
    )


@pytest.mark.parametrize(
    "v,encoding,expected",
    [
        ("cmd", "utf-16le", bytes.fromhex("63 00 6d 00 64 00")),
        ("cmd", "utf-16be", bytes.fromhex("00 63 00 6d 00 64")),
        ("cmd", "utf-16", bytes.fromhex("FF FE 63 00 6d 00 64 00")),
    ],
)
def test_apply_utf16_modifier(v: str, encoding: str, expected: bytes):
    assert apply_utf16_modifier(v, encoding=encoding) == expected


def test_windash_generator():
    assert set(windash_generator(" -param-name ")) == {
        " -param-name ",
        " /param-name ",
        " –param-name ",  # noqa: RUF001
        " —param-name ",
        " ―param-name ",
    }


@pytest.mark.parametrize(
    "modifiers,expected",
    [
        (["exists"], type(None)),
        (["exists", "base64"], ValueError),
        (["exists", "re", "base64"], ValueError),
    ],
)
def test_validate_exists_modifier(modifiers: list[str], expected: Any):
    @safe
    def inner():
        return validate_exists_modifier_condition(modifiers)

    result = inner()
    assert isinstance(result._inner_value, expected)


@pytest.mark.parametrize(
    "modifiers,expected",
    [
        (["wide", "base64"], type(None)),
        (["wide", "base64offset"], type(None)),
        (["wide", "base64offset", "contains"], type(None)),
        (["wide"], ValueError),
        (["base64", "wide"], ValueError),
        (["base64offset", "wide"], ValueError),
    ],
)
def test_validate_wide_modifier_order(modifiers: list[str], expected: Any):
    @safe
    def inner():
        return validate_base64_sub_modifier_condition(modifiers, "wide")

    result = inner()
    assert isinstance(result._inner_value, expected)
