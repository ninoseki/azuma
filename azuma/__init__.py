import importlib.metadata

from .schemas import Rule, RuleSet  # noqa: F401

__version__ = importlib.metadata.version(__name__)
