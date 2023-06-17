from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.parse import Protocol, load_file, load_str_bytes
from pydantic.utils import ROOT_KEY

YAML_CONTENT_TYPES = ["text/yaml", "application/x-yaml"]


class YAMLBaseModel(BaseModel):
    """BaseModel with YAML support"""

    @classmethod
    def parse_file(
        cls,
        path: str | Path,
        *,
        content_type: str = "text/yaml",
        encoding: str = "utf8",
        proto: Protocol | None = None,
        allow_pickle: bool = False,
    ):
        if content_type not in YAML_CONTENT_TYPES:
            obj = load_file(
                path,
                proto=proto,  # type: ignore
                content_type=content_type,
                encoding=encoding,
                allow_pickle=allow_pickle,
                json_loads=cls.__config__.json_loads,
            )
        else:
            with open(path, encoding=encoding) as f:
                obj = yaml.safe_load(f.read())

        return cls.parse_obj(obj)

    @classmethod
    def parse_raw(
        cls,
        b: str | bytes,
        *,
        content_type: str = "text/yaml",
        encoding: str = "utf8",
        proto: Protocol | None = None,
        allow_pickle: bool = False,
    ):
        try:
            if content_type not in YAML_CONTENT_TYPES:
                obj = load_str_bytes(
                    b,
                    proto=proto,  # type: ignore
                    content_type=content_type,
                    encoding=encoding,
                    allow_pickle=allow_pickle,
                    json_loads=cls.__config__.json_loads,
                )
            else:
                obj = yaml.safe_load(b)
        except (ValueError, TypeError, UnicodeDecodeError) as e:
            raise ValidationError([ErrorWrapper(e, loc=ROOT_KEY)], cls) from e

        return cls.parse_obj(obj)
