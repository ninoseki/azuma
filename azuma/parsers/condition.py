"""
This parser uses lark to transform the condition strings from signatures into callbacks that
invoke the right sequence of searches into the rule and logic operations.
"""

import pathlib
from collections.abc import Callable
from typing import Any, cast

from lark import Lark, Token, Transformer, Tree

from azuma.exceptions import UnsupportedFeatureError
from azuma.matchers import analyze_x_of, match_search_id

BASE_PATH = pathlib.Path(__file__).parent
GRAMMAR_PATH = BASE_PATH / "../grammar.lark"

grammar = GRAMMAR_PATH.read_text()


class FactoryTransformer(Transformer):
    @staticmethod
    def start(args):
        return args[0]

    @staticmethod
    def search_id(args: list[Token]):
        name = args[0].value

        def match_hits(signature: Any, event: Any):
            return match_search_id(signature, event, name)

        return match_hits

    @staticmethod
    def search_pattern(args: list[Token]):
        return args[0].value

    @staticmethod
    def atom(args: list[Callable]):
        if not all(callable(x) for x in args):
            raise ValueError(args)

        return args[0]

    @staticmethod
    def not_rule(args: list[Any]):
        negate, value = args

        negate = cast(Tree | None, negate)
        value = cast(Callable, value)

        assert callable(value)

        if negate is None:
            return value

        def _negate(*state):
            return not value(*state)

        return _negate

    @staticmethod
    def and_rule(args: list[Callable]):
        if not all(callable(x) for x in args):
            raise ValueError(args)

        if len(args) == 1:
            return args[0]

        def _and_operation(*state):
            return all(component(*state) for component in args)

        return _and_operation

    @staticmethod
    def or_rule(args: list[Callable]):
        if not all(callable(x) for x in args):
            raise ValueError(args)

        if len(args) == 1:
            return args[0]

        def _or_operation(*state):
            return any(component(*state) for component in args)

        return _or_operation

    @staticmethod
    def pipe_rule(args: list[Callable]):
        return args[0]

    @staticmethod
    def x_of(args: Any):
        # Load the left side of the X of statement
        count: int | None = None
        if args[0].children[0].type == "NUMBER":
            count = int(args[0].children[0].value)

        # Load the right side of the X of statement
        selector: str | None = str(args[2])
        if selector == "them":
            selector = None

        # Create a closure on our
        def _check_of_sections(signature, event):
            return analyze_x_of(signature, event, count, selector)

        return _check_of_sections

    @staticmethod
    def aggregation_expression(args):
        raise UnsupportedFeatureError("Aggregation expressions not supported.")

    @staticmethod
    def near_aggregation(args):
        raise UnsupportedFeatureError("Near operation not supported.")


# Create & initialize Lark class instance
factory_parser = Lark(
    grammar, parser="lalr", transformer=FactoryTransformer(), strict=True
)


def prepare_condition(raw_condition: str | list) -> Tree:
    if isinstance(raw_condition, list):
        raw_condition = "(" + ") or (".join(raw_condition) + ")"

    return factory_parser.parse(raw_condition)
