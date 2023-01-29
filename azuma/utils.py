from typing import Any


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
