from typing import Any

from pydantic import BaseModel, Field, root_validator

from azuma import types
from azuma.parsers import apply_modifiers, normalize_field_map, prepare_condition


class DetectionField(BaseModel):
    list_search: list[types.Query] = Field(default_factory=list)
    map_search: list[types.DetectionMap] = Field(default_factory=list)


def normalize_field_block(name: str, field: Any) -> DetectionField:
    if isinstance(field, dict):
        return DetectionField(map_search=[normalize_field_map(field)])

    if isinstance(field, list):
        if all(isinstance(_x, dict) for _x in field):
            return DetectionField(map_search=[normalize_field_map(_x) for _x in field])

        return DetectionField(
            list_search=[apply_modifiers(str(_x), ["contains"]) for _x in field]
        )

    raise ValueError(f"Failed to parse selection field {name}: {field}")


def normalize_detection(detection: dict[str, Any]) -> dict[str, DetectionField]:
    return {name: normalize_field_block(name, data) for name, data in detection.items()}


class Detection(BaseModel):
    detection: dict[str, DetectionField] = Field(...)
    timeframe: str | None = Field(default=None)
    condition: types.Condition = Field(...)

    @root_validator(pre=True)
    def transform(cls, values: Any):
        timeframe: str | None = None
        if "timeframe" in values:
            timeframe = values.pop("timeframe")

        condition = prepare_condition(values.pop("condition"))

        detection = normalize_detection(values)

        return {"condition": condition, "detection": detection, "timeframe": timeframe}

    def get_search_fields(self, search_id: str) -> DetectionField | None:
        return self.detection.get(search_id)

    @property
    def all_searches(self) -> dict[str, DetectionField]:
        return self.detection
