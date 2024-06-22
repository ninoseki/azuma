from pathlib import Path
from typing import Any

from pydantic import Field, RootModel

from .rule import Rule


class RuleSet(RootModel):
    root: list[Rule] = Field(default_factory=list)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def match_all(self, event: dict[Any, Any]) -> list[Rule]:
        """Check whether an event is matched with the rules

        Args:
            event (dict[Any, Any]): Event

        Returns:
            list[Rule]: A list of matched rules
        """
        return [rule for rule in self if rule.match(event)]

    def unique(self) -> "RuleSet":
        """Returns unique rule set.

        Returns:
            RuleSet: Rule set
        """
        seen: set[str] = set()

        filtered: list[Rule] = []
        for rule in self.root:
            if rule.id is None:
                filtered.append(rule)
                continue

            if rule.id not in seen:
                seen.add(rule.id)
                filtered.append(rule)

        return RuleSet(root=filtered)

    @classmethod
    def from_dir(cls, dir: str | Path, *, pattern="*.yml") -> "RuleSet":
        """Load rules from a directory

        Args:
            dir (str | Path): Directory
            pattern (str, optional): YAML file pattern. Defaults to "*.yml".

        Returns:
            RuleSet: Rule set
        """
        dir = Path(dir) if isinstance(dir, str) else dir
        paths = dir.glob(f"**/{pattern}")
        return cls(root=[Rule.model_validate_file(p) for p in paths])
