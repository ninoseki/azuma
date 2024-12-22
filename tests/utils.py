from functools import lru_cache

import yaml

from azuma.schemas import Rule


@lru_cache
def build_rule(
    detection: str,
    title: str | None = None,
    logsource: str | None = None,
):
    loaded = yaml.safe_load(detection)
    _detection = loaded.get("detection") or loaded

    rule = {
        "title": title or "dummy",
        "logsource": logsource or {"category": "dummy"},
        "detection": _detection,
    }
    return Rule.model_validate(rule)
