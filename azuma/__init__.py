import importlib.metadata

from .schemas import Rule, RuleSet  # noqa: F401

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

Rule.model_rebuild()
