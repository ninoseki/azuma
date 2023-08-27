import glob
import json
import typing as t
from functools import partial

import typer
from loguru import logger
from pydantic import BaseModel, Field, ValidationError
from returns.functions import raise_exception
from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import ResultE, safe

from azuma import schemas

app = typer.Typer()


class ScanResult(BaseModel):
    path: str = Field(...)
    matched: bool = Field(...)


@safe
def load_rules(path: str) -> list[schemas.Rule]:
    rules: list[schemas.Rule] = []

    for path_ in glob.glob(path):
        try:
            rules.append(schemas.Rule.parse_file(path_))
        except ValidationError:
            logger.info(f"Failed to load {path_}")

    return rules


@safe
def scan(rules: list[schemas.Rule], *, target: str) -> dict[str, list[dict]]:
    memo: dict[str, list[dict]] = {}
    for rule in rules:
        results: list[ScanResult] = []

        for path in glob.glob(target):
            with open(path) as f:
                data = json.loads(f.read())
                results.append(ScanResult(path=path, matched=rule.match(data)))

        key = f"{rule.title} ({rule.id or 'N/A'})"
        memo[key] = [r.model_dump() for r in results]

    return memo


@safe
def output(results: dict[str, list[dict]]) -> None:
    print(json.dumps(results))  # noqa: T201


@app.command()
def main(
    path: t.Annotated[
        str, typer.Argument(help="Path (or glob pattern) to rule YAML file(s)")
    ],
    target: t.Annotated[
        str, typer.Argument(help="Path (or glob pattern) to event JSON file(s)")
    ],
):
    task: ResultE[None] = flow(
        path, load_rules, bind(partial(scan, target=target)), bind(output)
    )
    task.alt(raise_exception)


if __name__ == "__main__":
    typer.run(main)
