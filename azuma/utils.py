import glob
import itertools
from collections.abc import Iterable
from typing import Any, TypeVar

from braceexpand import braceexpand

T = TypeVar("T")


def flatten(iter: Iterable[Iterable[T]]) -> set[T]:
    return set(itertools.chain.from_iterable(iter))


def brace_expand(path: str | Iterable[str]) -> set[str]:
    if isinstance(path, str):
        path = [path]

    return flatten([list(braceexpand(p)) for p in path])


def glob_expand(path: str | Iterable[str]) -> set[str]:
    if isinstance(path, str):
        path = [path]

    return flatten([glob.glob(p) for p in path])


def expand_path(path: str | Iterable[str]) -> set[str]:
    return glob_expand(brace_expand(path))


def lowercase_values(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: lowercase_values(v) for k, v in obj.items()}

    if isinstance(obj, (list, set, tuple)):
        cast = type(obj)
        return cast(lowercase_values(o) for o in obj)

    if isinstance(obj, str):
        return obj.lower()

    return obj


def normalize_event(event: dict[Any, Any]) -> dict[Any, Any]:
    """Normalize event. Lowercase all string values in an event.

    Args:
        event (dict[Any, Any]): Event

    Returns:
        dict[Any, Any]: Normalized event
    """
    return lowercase_values(event.copy())
