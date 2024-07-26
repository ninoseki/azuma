import itertools
import json
import sys
from functools import partial
from typing import Annotated, cast

import senkawa
import typer
from pydantic import BaseModel, Field, ValidationError
from pydantic_core import InitErrorDetails
from returns.functions import raise_exception
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from returns.result import ResultE, safe

from azuma import schemas

app = typer.Typer()


class ScanResult(BaseModel):
    path: str = Field(...)
    matched: bool = Field(...)


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
        results = [load_rule(path_) for path_ in senkawa.glob(path)]
        return [result.alt(raise_exception).unwrap() for result in results]

    @safe
    def scan(rules: list[schemas.Rule], *, target: str) -> dict[str, list[dict]]:
        memo: dict[str, list[dict]] = {}
        for rule in rules:
            results: list[ScanResult] = []

            for path in senkawa.glob(target):
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


OPTIONAL_FIELDS = [
    "author",
    "date",
    "description",
    "falsepositives",
    "fields",
    "id",
    "level",
    "license",
    "modified",
    "references",
    "related",
    "status",
    "tags",
]


@safe
def extra_checks(  # noqa: C901
    rule: schemas.Rule,
    *,
    check_id: bool = False,
    check_license: bool = False,
    check_author: bool = False,
    check_date: bool = False,
    check_modified: bool = False,
    check_description: bool = False,
    check_status: bool = False,
    check_level: bool = False,
    check_references: bool = False,
    check_tags: bool = False,
    check_fields: bool = False,
    check_related: bool = False,
    check_falsepositives: bool = False,
    check_all: bool = False,
) -> schemas.Rule:
    errors: list[InitErrorDetails] = []

    fields_to_check: set[str] = set(OPTIONAL_FIELDS) if check_all else set()

    if check_id:
        fields_to_check.add("id")

    if check_license:
        fields_to_check.add("license")

    if check_author:
        fields_to_check.add("author")

    if check_date:
        fields_to_check.add("date")

    if check_modified:
        fields_to_check.add("modified")

    if check_description:
        fields_to_check.add("description")

    if check_status:
        fields_to_check.add("status")

    if check_level:
        fields_to_check.add("level")

    if check_references:
        fields_to_check.add("references")

    if check_tags:
        fields_to_check.add("tags")

    if check_fields:
        fields_to_check.add("fields")

    if check_related:
        fields_to_check.add("related")

    if check_falsepositives:
        fields_to_check.add("falsepositives")

    dumped = rule.model_dump()
    for check in fields_to_check:
        if check not in dumped or dumped[check] is None:
            errors.append(InitErrorDetails(type="missing", loc=(check,)))  # type: ignore

    if len(errors) > 0:
        raise ValidationError.from_exception_data("Field required", errors)

    return rule


@app.command()
def validate(
    path: Annotated[
        list[str],
        typer.Argument(help="Path(s) (or glob pattern(s)) to rule YAML file(s)"),
    ],
    check_id: Annotated[
        bool, typer.Option(help="Check for missing 'id' field")
    ] = False,
    check_license: Annotated[
        bool, typer.Option(help="Check for missing 'license' field")
    ] = False,
    check_author: Annotated[
        bool, typer.Option(help="Check for missing 'author' field")
    ] = False,
    check_date: Annotated[
        bool, typer.Option(help="Check for missing 'date' field")
    ] = False,
    check_modified: Annotated[
        bool, typer.Option(help="Check for missing 'modified' field")
    ] = False,
    check_description: Annotated[
        bool, typer.Option(help="Check for missing 'description' field")
    ] = False,
    check_status: Annotated[
        bool, typer.Option(help="Check for missing 'status' field")
    ] = False,
    check_level: Annotated[
        bool, typer.Option(help="Check for missing 'level' field")
    ] = False,
    check_references: Annotated[
        bool, typer.Option(help="Check for missing 'references' field")
    ] = False,
    check_tags: Annotated[
        bool, typer.Option(help="Check for missing 'tags' field")
    ] = False,
    check_falsepositives: Annotated[
        bool, typer.Option(help="Check for missing 'falsepositives' field")
    ] = False,
    check_fields: Annotated[
        bool, typer.Option(help="Check for missing 'fields' field")
    ] = False,
    check_related: Annotated[
        bool, typer.Option(help="Check for missing 'related' field")
    ] = False,
    check_all: Annotated[
        bool, typer.Option(help="Check for all the missing optional fields")
    ] = False,
):
    memo: dict[str, ValidationError] = {}
    for path_ in itertools.chain.from_iterable([senkawa.glob(p) for p in path]):
        result: ResultE[schemas.Rule] = flow(
            path_,
            load_rule,
            bind(
                partial(
                    extra_checks,
                    check_id=check_id,
                    check_license=check_license,
                    check_author=check_author,
                    check_date=check_date,
                    check_modified=check_modified,
                    check_description=check_description,
                    check_status=check_status,
                    check_level=check_level,
                    check_references=check_references,
                    check_tags=check_tags,
                    check_fields=check_fields,
                    check_related=check_related,
                    check_falsepositives=check_falsepositives,
                    check_all=check_all,
                )
            ),
        )
        if not is_successful(result):
            memo[path_] = cast(ValidationError, result.failure())

    if not memo:
        return

    for path_, error in memo.items():
        print(f"{path_} has {error}\n", file=sys.stderr)  # noqa: T201

    sys.exit(1)


if __name__ == "__main__":
    typer.run(app())
