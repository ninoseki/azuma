from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .rule import Rule


class RuleSet(BaseModel):
    rules: list[Rule] = Field(default_factory=list)

    def match_all(self, event: dict[Any, Any]) -> list[Rule]:
        """Check whether an event is matched with the rules

        Args:
            event (dict[Any, Any]): Event

        Returns:
            list[Rule]: A list of matched rules
        """
        matched: list[Rule] = []

        for rule in self.rules:
            if rule.match(event):
                matched.append(rule)

        return matched

    @classmethod
    def from_dir(cls, dir: str | Path, *, pattern="*.yml") -> "RuleSet":
        """Load rules from a directory

        Args:
            dir (str | Path): Directory
            pattern (str, optional): YAML file pattern. Defaults to "*.yml".

        Returns:
            RuleSet: Rule set
        """
        if isinstance(dir, str):
            dir = Path(dir)

        paths = dir.glob(f"**/{pattern}")
        return cls(rules=[Rule.parse_file(p) for p in paths])
