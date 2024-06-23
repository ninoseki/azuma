from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class YamlBaseModel(BaseModel):
    """BaseModel with YAML support"""

    @classmethod
    def model_validate_file(  # type: ignore
        cls,
        path: str | Path,
        *,
        encoding: str = "utf8",
        strict: bool | None = None,
        context: dict[str, Any] | None = None,
    ):
        """Parse a YAML file.

        Args:
            path (str | Path): Path to a file.
            encoding (str, optional): Encoding. Defaults to "utf8".
            strict (bool | None, optional): Strict or not. Defaults to None.
            context (dict[str, Any] | None, optional): Context. Defaults to None.

        Returns:
            YamlBaseModel: Parsed instance.
        """
        with open(path, encoding=encoding) as f:
            text = f.read()

        obj = yaml.safe_load(text)
        return cls.model_validate(obj, strict=strict, context=context)

    @classmethod
    def model_validate_yaml(  # type: ignore
        cls,
        b: str | bytes,
        *,
        strict: bool | None = None,
        context: dict[str, Any] | None = None,
    ):
        """Parse a YAML text.

        Args:
            b (str | bytes): String or bytes.
            strict (bool | None, optional): Strict or not. Defaults to None.
            context (dict[str, Any] | None, optional): Context. Defaults to None.

        Returns:
            YamlBaseModel: Parsed instance.
        """
        obj = yaml.safe_load(b)
        return cls.model_validate(obj, strict=strict, context=context)
