import re
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from . import schemas


Query = Optional[Union[str, re.Pattern, Any]]
DetectionMap = list[tuple[str, tuple[list[Query], list[str]]]]
Condition = Callable[["schemas.Rule", dict[Any, Any]], Any]
