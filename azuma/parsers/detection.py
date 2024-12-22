import base64
import ipaddress
from typing import Any, Callable, Mapping

import regex as re

from azuma import types
from azuma.exceptions import UnsupportedFeatureError

from .utils import replace_placeholders, replace_with_placeholder

# TODO We need to support the rest of them
SUPPORTED_MODIFIERS = {
    "all",
    "base64",
    "base64offset",
    "cased",
    "cidr",
    "contains",
    "endswith",
    "exists",
    "gt",
    "gte",
    "lt",
    "lte",
    "re",
    "startswith",
    "utf16be",
    "utf16le",
    "wide",
    "windash",
    # re sub-modifiers
    "i",
    "m",
    "s",
    # 'expand',
    # 'fieldref',
    # "utf16",
}


def apply_base64_modifier(x: str) -> str:
    x = x.replace("\n", "")
    return base64.b64encode(x.encode()).decode()


def apply_base64offset_modifier(x: str) -> str:
    # modified from https://github.com/SigmaHQ/pySigma
    # (https://github.com/SigmaHQ/pySigma/blob/main/sigma/modifiers.py: SigmaBase64OffsetModifier)
    x = x.replace("\n", "")
    x = x.replace("\n", "")

    start_offsets = (0, 2, 3)
    end_offsets = (None, -3, -2)

    offsets: list[str] = []
    for i in range(3):
        offsets.append(
            base64.b64encode(i * b" " + x.encode())[
                start_offsets[i] : end_offsets[(len(x) + i) % 3]
            ].decode()
        )

    return f"({'|'.join(offsets)})"


WINDASH_PATTERN = re.compile("\\B[-/]\\b")

WINDASH_PLACEHOLDERS = (
    "-",
    "/",
    chr(int("2013", 16)),  # en_dash
    chr(int("2014", 16)),  # em_dash
    chr(int("2015", 16)),  # horizontal_bar
)


def windash_generator(x: str):
    replaced = replace_with_placeholder(x, WINDASH_PATTERN, "_windash")

    for placeholder in WINDASH_PLACEHOLDERS:
        yield replace_placeholders(replaced, placeholder)


def apply_windash_modifier(x: str) -> str:
    modified = set(windash_generator(x))
    return f"({'|'.join(modified)})"


def apply_utf_modifier(x: str, encoding: str) -> str:
    return "".join([c.encode(encoding).decode("utf-8") for c in x])


MODIFIER_FUNCTIONS: Mapping[str, Callable[[str], Any]] = {
    "base64": lambda x: apply_base64_modifier(x),
    "base64offset": lambda x: apply_base64offset_modifier(x),
    "contains": lambda x: f".*{x}.*",
    "endswith": lambda x: f".*{x}$",
    "startswith": lambda x: f"^{x}.*",
    "utf16be": lambda x: apply_utf_modifier(x, encoding="utf-16be"),
    "utf16le": lambda x: apply_utf_modifier(x, encoding="utf-16le"),
    "wide": lambda x: apply_utf_modifier(x, encoding="utf-16le"),
    "windash": lambda x: apply_windash_modifier(x),
}


def process_field_name(field_string: str) -> tuple[str, list[str]]:
    name_and_modifiers = field_string.split("|")
    name = name_and_modifiers.pop(0)
    modifiers = [m for m in name_and_modifiers if m]

    unsupported = set(modifiers) - SUPPORTED_MODIFIERS
    if unsupported:
        raise UnsupportedFeatureError(
            f"Unsupported field modifiers used: {unsupported}"
        )

    return name, modifiers


_NSC = NON_SPECIAL_CHARACTERS = r"[^\\*?]*"
ESCAPED_SPECIAL_CHARACTER = r"(?:\\[*?])"
ESCAPED_OTHER_CHARACTER = r"(?:\\[^*?])"
ESCAPED_WILDCARD_PATTERN = re.compile(
    rf"(?:{_NSC}{ESCAPED_SPECIAL_CHARACTER}*{ESCAPED_OTHER_CHARACTER})*"
)

UPTO_WILDCARD = re.compile(r"^([^\\?*]+|(?:\\[^?*\\])+)+")


def sigma_string_to_regex(original_value: str) -> str:
    value = original_value
    full_content: list[str] = []

    while value:
        # Grab any content up to the first wildcard
        match = UPTO_WILDCARD.match(value)

        if match:
            # The non regex content in the sigma string, may have characters special to regex
            matched = match.group(0)
            full_content.append(re.escape(matched))
            value = value[len(matched) :]
            continue

        if value.startswith("*"):
            full_content.append(".*")
            value = value[1:]
            continue

        if value.startswith("\\*"):
            full_content.append(re.escape("*"))
            value = value[2:]
            continue

        if value.startswith("?"):
            full_content.append(".")
            value = value[1:]
            continue

        if value.startswith("\\?"):
            full_content.append(re.escape("?"))
            value = value[2:]
            continue

        if value.startswith(r"\\*"):
            full_content.append(re.escape("\\") + ".*")
            value = value[3:]
            continue

        if value.startswith(r"\\?"):
            full_content.append(re.escape("\\") + ".")
            value = value[3:]
            continue

        if value.startswith("\\"):
            full_content.append(re.escape("\\"))
            value = value[1:]
            continue

        raise ValueError(f"Could not parse string matching pattern: {original_value}")

    return "".join(full_content)


def get_modified_value(value: str, modifiers: list[str] | None) -> str:
    if not modifiers:
        # If there are no modifiers, we assume exact match
        return f"^{value}$"

    for mod in modifiers:
        func = MODIFIER_FUNCTIONS.get(mod)
        value = func(value) if func else value

    return value


# NOTE: regex flags for non-re modifier case
MODIFIER_REGEX_FLAGS = re.V1 | re.DOTALL


def validate_base64_sub_modifier_condition(
    modifiers: list[str], sub_modifier: str
) -> None:
    has_base64 = "base64" in modifiers
    has_base64offset = "base64offset" in modifiers
    if all([not has_base64, not has_base64offset]):
        raise ValueError(
            f"{sub_modifier} modifier must be used with base64 or base64offset modifier"
        )

    sub_modifier_index = modifiers.index(sub_modifier)
    base64_index = modifiers.index("base64") if has_base64 else None
    base64offset_index = modifiers.index("base64offset") if has_base64offset else None
    if sub_modifier_index > (base64_index or base64offset_index or 0):
        raise ValueError(
            f"{sub_modifier} modifier must be used before base64 or base64offset modifier"
        )


def validate_exists_modifier_condition(modifiers: list[str]) -> None:
    if len(modifiers) > 1:
        raise ValueError("exists modifier cannot use along with other modifiers")


def validate_re_modifier_condition(modifiers: list[str]) -> None:
    re_index = modifiers.index("re")
    if re_index > 0:
        raise ValueError("re modifier must be used before other sub-modifiers")

    has_non_sub_modifiers = len(set(modifiers) - {"re", "i", "m", "s"}) > 0
    if has_non_sub_modifiers:
        raise ValueError(
            "re modifier cannot use along with other modifiers except re sub-modifiers"
        )


def apply_re_modifiers(value: str, modifiers: list[str]) -> types.Query:
    if "re" not in modifiers:
        return None

    validate_re_modifier_condition(modifiers)

    flags = re.V1
    if "i" in modifiers:
        flags |= re.IGNORECASE
    if "m" in modifiers:
        flags |= re.MULTILINE
    if "s" in modifiers:
        flags |= re.DOTALL

    return re.compile(value, flags=flags)


def apply_cidr_modifier(value: str, modifiers: list[str]) -> types.Query:
    if "cidr" not in modifiers:
        return None

    return lambda x: ipaddress.ip_address(x) in ipaddress.ip_network(value)  # type: ignore


def apply_lte_modifier(value: str, modifiers: list[str]) -> types.Query:
    if "lte" not in modifiers:
        return None

    return lambda x: float(x) <= float(value)  # type: ignore


def apply_lt_modifier(value: str, modifiers: list[str]) -> types.Query:
    if "lt" not in modifiers:
        return None

    return lambda x: float(x) < float(value)  # type: ignore


def apply_gte_modifier(value: str, modifiers: list[str]) -> types.Query:
    if "gte" not in modifiers:
        return None

    return lambda x: float(x) >= float(value)  # type: ignore


def apply_gt_modifier(value: str, modifiers: list[str]) -> types.Query:
    if "gt" not in modifiers:
        return None

    return lambda x: float(x) > float(value)  # type: ignore


def apply_modifiers(value: str, modifiers: list[str]) -> types.Query:
    """
    Apply as many modifiers as we can during signature construction
    to speed up the matching stage as much as possible.
    """
    # those modifiers have priority over the rest
    # in other words, they should not be able to use #get_modified_value
    for func in [
        apply_cidr_modifier,
        apply_lte_modifier,
        apply_lt_modifier,
        apply_gte_modifier,
        apply_gt_modifier,
        apply_re_modifiers,
    ]:
        result = func(value, modifiers)
        if result is not None:
            return result

    # re modifier should be applied beforehand if it's set well
    # so there should not be any re sub-modifiers left
    has_re_sub_modifiers = any(sub in modifiers for sub in {"i", "m", "s"})
    if has_re_sub_modifiers:
        raise ValueError("re sub-modifiers must be used with re modifier")

    # base64 sub-modifiers should be used with base64 or base64offset modifier
    base64_sub_modifiers = {"wide", "utf16be", "utf16le"}
    for base64_sub_modifier in base64_sub_modifiers:
        if base64_sub_modifier in modifiers:
            validate_base64_sub_modifier_condition(modifiers, base64_sub_modifier)

    has_cased = "cased" in modifiers
    has_base64 = "base64" in modifiers or "base64offset" in modifiers

    # don't use re.IGNORECASE if cased modifier is used or base64 or base64offset modifier is used
    flags = (
        MODIFIER_REGEX_FLAGS
        if (has_cased or has_base64)
        else MODIFIER_REGEX_FLAGS | re.IGNORECASE
    )

    if not ESCAPED_WILDCARD_PATTERN.fullmatch(value):
        # transform the unescaped wildcards to their regex equivalent
        reg_value = sigma_string_to_regex(value)
        value = get_modified_value(reg_value, modifiers)
        return re.compile(value, flags=flags)

    value = get_modified_value(value, modifiers)
    return str(value).replace("\\*", "*").replace("\\?", "?")


def normalize_field_map(field: dict[str, Any]) -> types.DetectionMap:
    def map_raw_key_value(raw_key: str, value: Any) -> types.DetectionItem:
        key, modifiers = process_field_name(raw_key)

        if value is None:
            return (key, ([None], modifiers))

        has_exists = "exists" in modifiers
        if has_exists:
            validate_exists_modifier_condition(modifiers)

            if value is True:
                # NOTE: use "*" to check whether a field exists or not
                return (key, ([apply_modifiers("*", [])], modifiers))

            if value is False:
                return (key, ([None], modifiers))

            # NOTE: value should not be a list when exists modifier is used
            raise ValueError("exists modifier must be used with boolean value")

        if isinstance(value, list):
            return (
                key,
                (
                    [
                        apply_modifiers(str(v), modifiers) if v is not None else None
                        for v in value
                    ],
                    modifiers,
                ),
            )

        return (key, ([apply_modifiers(str(value), modifiers)], modifiers))

    return [map_raw_key_value(raw_key, value) for raw_key, value in field.items()]
