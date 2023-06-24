import glob
import json
import typing as t

import typer
from loguru import logger
from pydantic import BaseModel, Field, ValidationError

from azuma import schemas

app = typer.Typer()


class ScanResult(BaseModel):
    path: str = Field(...)
    matched: bool = Field(...)


def load_rules(path: str) -> list[schemas.Rule]:
    rules: list[schemas.Rule] = []
    for path_ in glob.glob(path):
        try:
            rules.append(schemas.Rule.parse_file(path_))
        except ValidationError:
            logger.info(f"Failed to load {path_}")

    return rules


def scan(*, target: str, rules: list[schemas.Rule]) -> dict[str, list[dict]]:
    memo: dict[str, list[dict]] = {}
    for rule in rules:
        results: list[ScanResult] = []

        for path in glob.glob(target):
            with open(path) as f:
                data = json.loads(f.read())
                results.append(ScanResult(path=path, matched=rule.match(data)))

        key = f"{rule.title} ({rule.id or 'N/A'})"
        memo[key] = [r.dict() for r in results]

    return memo


@app.command()
def main(
    path: t.Annotated[
        str, typer.Argument(help="Path (or glob pattern) to rule YAML file(s)")
    ],
    target: t.Annotated[
        str, typer.Argument(help="Path (or glob pattern) to event JSON file(s)")
    ],
):
    rules = load_rules(path)
    results = scan(target=target, rules=rules)
    print(json.dumps(results))  # noqa: T201


if __name__ == "__main__":
    typer.run(main)
