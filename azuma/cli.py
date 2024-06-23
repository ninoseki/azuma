import glob
import itertools
import json
import sys
from functools import partial
from typing import Annotated, cast

import typer
from pydantic import BaseModel, Field, ValidationError
from returns.functions import raise_exception
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from returns.result import ResultE, safe

from azuma import schemas

app = typer.Typer()


class ScanResult(BaseModel):
    path: str = Field(...)
    matched: bool = Field(...)


def expand_path(path: str | list[str]) -> set[str]:
    if isinstance(path, str):
        path = [path]

    expanded = [glob.glob(p) for p in path]
    return set(itertools.chain.from_iterable(expanded))


@safe(exceptions=(ValidationError,))
def load_rule(path: str) -> schemas.Rule:
    return schemas.Rule.model_validate_file(path)


@app.command()
def scan(
    path: Annotated[
        str, typer.Argument(help="Path (or glob pattern) to rule YAML file(s)")
    ],
    target: Annotated[
        str, typer.Argument(help="Path (or glob pattern) to event JSON file(s)")
    ],
):
    @safe
    def load_rules(path: str) -> list[schemas.Rule]:
        results = [load_rule(path_) for path_ in expand_path(path)]
        return [result.alt(raise_exception).unwrap() for result in results]

    @safe
    def scan(rules: list[schemas.Rule], *, target: str) -> dict[str, list[dict]]:
        memo: dict[str, list[dict]] = {}
        for rule in rules:
            results: list[ScanResult] = []

            for path in expand_path(target):
                with open(path) as f:
                    data = json.loads(f.read())
                    results.append(ScanResult(path=path, matched=rule.match(data)))

            key = rule.id or rule.title
            memo[key] = [r.model_dump() for r in results]

        return memo

    @safe
    def output(results: dict[str, list[dict]]) -> None:
        print(json.dumps(results))  # noqa: T201

    result: ResultE[None] = flow(
        path, load_rules, bind(partial(scan, target=target)), bind(output)
    )
    result.alt(raise_exception)


@app.command()
def validate(
    path: Annotated[
        list[str],
        typer.Argument(help="Path(s) (or glob pattern(s)) to rule YAML file(s)"),
    ],
):
    memo: dict[str, ValidationError] = {}
    for path_ in expand_path(path):
        result: ResultE[schemas.Rule] = flow(path_, load_rule)
        if not is_successful(result):
            memo[path_] = cast(ValidationError, result.failure())

    if not memo:
        return

    for path_, error in memo.items():
        print(f"{path_} has {error}\n", file=sys.stderr)  # noqa: T201

    sys.exit(1)


if __name__ == "__main__":
    typer.run(app())
