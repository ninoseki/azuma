import re
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from . import schemas


QueryFunction = Callable[[Any, Any], bool]
Query = Optional[Union[str, re.Pattern, QueryFunction, Any]]
DetectionItem = tuple[str, tuple[list[Query], list[str]]]
DetectionMap = list[DetectionItem]
Condition = Callable[["schemas.Rule", dict[Any, Any]], Any]
