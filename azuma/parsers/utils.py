# forked from https://github.com/SigmaHQ/pySigma/
import dataclasses

import regex as re


@dataclasses.dataclass
class Placeholder:
    name: str


def replace_with_placeholder(
    s: str, regex: re.Pattern, placeholder_name: str
) -> tuple[str | Placeholder, ...]:
    result: list[str | Placeholder] = []

    matched = False
    i = 0
    for m in regex.finditer(s):
        matched = True
        _s = s[i : m.start()]
        if _s != "":
            result.append(_s)
        result.append(Placeholder(placeholder_name))
        i = m.end()

    if matched:  # if matched, append remainder of string
        _s = s[i:]
        if _s != "":
            result.append(_s)
    else:  # no matches: append original string
        result.append(s)

    return tuple(result)


def replace_placeholders(
    replaced: tuple[str | Placeholder, ...], placeholder: str
) -> str:
    result: list[str] = []

    for rep in replaced:
        if isinstance(rep, Placeholder):
            result.append(placeholder)
        else:
            result.append(rep)

    return "".join(result)
