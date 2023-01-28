import datetime


def is_valid_date_format(v: str) -> bool:
    try:
        datetime.datetime.strptime(v, "%Y/%m/%d")
        return True
    except Exception:
        return False
