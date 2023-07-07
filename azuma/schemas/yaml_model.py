import json
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

YAML_CONTENT_TYPES = ["text/yaml", "application/x-yaml"]


class YAMLBaseModel(BaseModel):
    """BaseModel with YAML support"""

    @classmethod
    def parse_file(  # type: ignore
        cls,
        path: str | Path,
        *,
        content_type: str | None = "text/yaml",
        encoding: str = "utf8",
        strict: bool | None = None,
        context: dict[str, Any] | None = None,
    ):
        with open(path, encoding=encoding) as f:
            text = f.read()

            if content_type in YAML_CONTENT_TYPES:
                obj = yaml.safe_load(text)
            else:
                obj = json.loads(text)

        return cls.model_validate(obj, strict=strict, context=context)

    @classmethod
    def parse_raw(  # type: ignore
        cls,
        b: str | bytes,
        *,
        content_type: str | None = "text/yaml",
        strict: bool | None = None,
        context: dict[str, Any] | None = None,
    ):
        if content_type in YAML_CONTENT_TYPES:
            obj = yaml.safe_load(b)
        else:
            obj = json.loads(b)

        return cls.model_validate(obj, strict=strict, context=context)
