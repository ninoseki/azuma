import contextlib
import datetime


def is_valid_date_format(v: str) -> bool:
    with contextlib.suppress(Exception):
        datetime.datetime.strptime(v, "%Y-%m-%d")
        return True

    return False
