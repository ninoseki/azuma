from typing import Type

import pytest
import regex as re

from azuma.parsers.detection import (
    apply_base64offset_modifier,
    sigma_string_to_regex,
    validate_exists_modifier_condition,
    validate_wide_modifier_condition,
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


def test_base64offset_modifier():
    assert (
        apply_base64offset_modifier("/bin/bash")
        == "(L2Jpbi9iYXNo|9iaW4vYmFza|vYmluL2Jhc2)"
    )


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
        (["exists"], None),
        (["exists", "base64"], ValueError),
        (["exists", "re", "base64"], ValueError),
    ],
)
def test_validate_exists_modifier(modifiers: list[str], expected: Type[Exception]):
    if expected:
        with pytest.raises(expected):
            validate_exists_modifier_condition(modifiers)
    else:
        validate_exists_modifier_condition(modifiers)


@pytest.mark.parametrize(
    "modifiers,expected",
    [
        (["wide", "base64"], None),
        (["wide", "base64offset"], None),
        (["wide", "base64offset", "contains"], None),
        (["wide"], ValueError),
        (["base64", "wide"], ValueError),
        (["base64offset", "wide"], ValueError),
    ],
)
def test_validate_wide_modifier_order(modifiers: list[str], expected: Type[Exception]):
    if expected:
        with pytest.raises(expected):
            validate_wide_modifier_condition(modifiers)
    else:
        validate_wide_modifier_condition(modifiers)
