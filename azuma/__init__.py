import importlib.metadata

import packaging.version
from pydantic import VERSION

from .schemas import Rule, RuleSet  # noqa: F401

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"


PYDANTIC_VERSION = packaging.version.parse(VERSION)

if packaging.version.parse("2.10.0") <= PYDANTIC_VERSION:
    Rule.model_rebuild()
